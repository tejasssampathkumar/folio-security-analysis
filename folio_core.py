"""
Folio core analytics.

Pure data + maths layer used by the Streamlit app (app.py), the Ollama analyst
(folio_ai.py) and the batch exporter (portfolio_engine.py). No UI code here.

Sources
- Market data: Yahoo Finance chart API (daily OHLCV), cached in outputs/daily_market_data.csv
- Fundamentals / DCF / relative valuation: SA_final_workbook.xlsx (must be calculated + saved in Excel)
- Risk questionnaire scoring: Risk_Aversion_Questionnaire.pdf (10 questions, prudence rule, A = 10 - 0.3(R - 10))
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import minimize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
WORKBOOK = os.path.join(BASE_DIR, "SA_final_workbook.xlsx")
MARKET_CSV = os.path.join(OUTPUT_DIR, "daily_market_data.csv")
MARKET_META = os.path.join(OUTPUT_DIR, "daily_market_data_meta.json")

STOCKS = ["TRENT", "ASIANPAINT", "TCS"]
TICKERS = {"TRENT": "TRENT.NS", "ASIANPAINT": "ASIANPAINT.NS", "TCS": "TCS.NS", "NIFTY": "^NSEI"}
NAMES = {
    "TRENT": "Trent Ltd.",
    "ASIANPAINT": "Asian Paints Ltd.",
    "TCS": "Tata Consultancy Services Ltd.",
    "NIFTY": "Nifty 50 Index",
}
SHORT = {"TRENT": "Trent", "ASIANPAINT": "Asian Paints", "TCS": "TCS", "NIFTY": "Nifty 50"}
SECTOR = {
    "TRENT": "Apparel retail (Westside, Zudio)",
    "ASIANPAINT": "Decorative paints and coatings",
    "TCS": "IT services and consulting",
    "NIFTY": "Benchmark index",
}
THESIS = {
    "TRENT": "Hype / momentum: a very high multiple resting on a store-expansion story.",
    "ASIANPAINT": "De-rating: sentiment shifted as competition entered and margins came under pressure.",
    "TCS": "Fear vs fundamentals: AI-disruption worries against strong cash generation.",
}
DCF_SHEETS = {"TRENT": "trent_dcf", "ASIANPAINT": "asian_dcf", "TCS": "tcs_dcf"}
RATIO_SHEETS = {"TRENT": "trent_ratios", "ASIANPAINT": "asian_ratios", "TCS": "tcs_ratios"}
WB_COL = {"TRENT": "B", "ASIANPAINT": "C", "TCS": "D"}
RELVAL_ROWS = {"TRENT": (13, 11, 12, 16), "ASIANPAINT": (32, 30, 31, 35), "TCS": (51, 49, 50, 54)}

# Known share-count changes. Yahoo's TRENT series has an un-adjusted 3:2 gap
# (close 4,272.7 on 31-Dec-2025 -> open 2,852.7 on 1-Jan-2026, exactly 1/1.5; Yahoo lists a 3:2 split).
# The gap is detected from the data, so a future Yahoo fix will not be double-adjusted.
SPLIT_RATIOS = {"TRENT": 1.5}

# Questionnaire (Risk_Aversion_Questionnaire.pdf). Options listed as (label, points).
QUESTIONS = {
    "A": [
        ("Q1. What is your age group?",
         [("Under 30", 4), ("30 to 44", 3), ("45 to 59", 2), ("60 or above", 1)]),
        ("Q2. When will you first need a large part of the money you are setting aside?",
         [("More than 15 years from now", 4), ("Between 8 and 15 years", 3),
          ("Between 3 and 7 years", 2), ("Within the next 3 years", 1)]),
        ("Q3. How would you describe your income (or your supporter's) for the next few years?",
         [("Very steady and likely to grow", 4), ("Mostly steady", 3), ("Varies from year to year", 2),
          ("Uncertain, likely to fall, or no regular income", 1)]),
        ("Q4. How many people depend on your income, and how heavy are your fixed commitments?",
         [("Nobody depends on me; commitments are light", 4),
          ("One or two dependents, or manageable commitments", 3),
          ("Several dependents, or commitments take a large part of income", 2),
          ("Most income already committed; others rely on me fully", 1)]),
        ("Q5. If you lost your income tomorrow, how long could savings cover living costs?",
         [("12 months or more", 4), ("6 to 11 months", 3), ("3 to 5 months", 2), ("Less than 3 months", 1)]),
    ],
    "B": [
        ("Q6. You are offered a prize. Which option would you pick?",
         [("Rs 50,000 for certain", 1), ("50% chance of Rs 70,000, 50% chance of Rs 40,000", 2),
          ("50% chance of Rs 1,00,000, 50% chance of Rs 20,000", 3),
          ("50% chance of Rs 1,50,000, 50% chance of nothing", 4)]),
        ("Q7. You are offered a new job. Which would you most likely take?",
         [("Stay in my secure job, predictable pay, slow growth", 1),
          ("Similar job, slightly better pay, small chance of instability", 2),
          ("Growing company, notably higher pay, real chance the role disappears", 3),
          ("Own venture / very early-stage company: far more or nothing", 4)]),
        ("Q8. Rs 1,00,000 set aside falls to Rs 80,000 in a downturn. What would you do?",
         [("Take out everything to avoid losing more", 1), ("Take out part of it", 2),
          ("Do nothing and wait for it to recover", 3), ("Put in more, since it is cheaper now", 4)]),
        ("Q9. You are waiting two weeks for an important result. How do you usually feel?",
         [("Very anxious; hard to think about anything else", 1), ("Quite uneasy; I keep checking for news", 2),
          ("A little concerned, but I carry on normally", 3), ("Calm; I do what I can and move on", 4)]),
        ("Q10. What do you want from your savings?",
         [("Protect what I have; rather earn little than lose any", 1),
          ("Steady, modest growth with small ups and downs", 2),
          ("Good growth; I accept sizeable ups and downs", 3),
          ("Maximum growth; I accept large swings and serious losses", 4)]),
    ],
}
# Worked examples from the PDF (section subtotals A, B)
ARCHETYPES = {
    "Priya, 27, stable job": (17, 19),
    "Rahul, 41, mixed": (13, 14),
    "Meena, 58, cautious": (8, 7),
    "Arjun, 30, bold but stretched": (7, 16),
}


class WorkbookNotCalculated(RuntimeError):
    """Raised when the workbook has formulas without cached values (open + save it in Excel)."""


# --------------------------------------------------------------------------------------
# Market data
# --------------------------------------------------------------------------------------
def fetch_market_data(range_: str = "5y") -> pd.DataFrame:
    """Download daily OHLCV for all tickers from Yahoo and cache to CSV."""
    frames = []
    for name, sym in TICKERS.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(sym)}?range={range_}&interval=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode())["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
        idx = pd.to_datetime(
            [dt.datetime.fromtimestamp(t, dt.timezone(dt.timedelta(hours=5, minutes=30))).date() for t in res["timestamp"]]
        )
        frames.append(pd.DataFrame({
            f"{name}_Open": q["open"], f"{name}_High": q["high"], f"{name}_Low": q["low"],
            f"{name}_Close": q["close"], f"{name}_AdjClose": adj, f"{name}_Volume": q["volume"],
        }, index=idx))
    df = pd.concat(frames, axis=1)
    df = df[~df.index.duplicated(keep="last")].sort_index().ffill().dropna(how="any")
    df.index.name = "Date"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(MARKET_CSV)
    with open(MARKET_META, "w") as f:
        json.dump({"source": "Yahoo Finance chart API", "range": range_,
                   "downloaded_at": dt.datetime.now().isoformat(timespec="seconds")}, f, indent=2)
    return df


def _fix_split(df: pd.DataFrame, sym: str, ratio: float):
    """Divide pre-gap prices by `ratio` if an un-adjusted split gap is present. Returns (df, gap_date)."""
    prev_close = df[f"{sym}_Close"].shift(1)
    gap = df[f"{sym}_Open"] / prev_close
    hits = gap[(gap > (1 / ratio) * 0.97) & (gap < (1 / ratio) * 1.03)]
    if hits.empty:
        return df, None
    d0 = hits.index[0]
    mask = df.index < d0
    for fld in ("Open", "High", "Low", "Close", "AdjClose"):
        df.loc[mask, f"{sym}_{fld}"] = df.loc[mask, f"{sym}_{fld}"] / ratio
    df.loc[mask, f"{sym}_Volume"] = df.loc[mask, f"{sym}_Volume"] * ratio
    return df, d0


def load_market_data():
    """Load cached daily data, apply split fixes. Returns (df, notes, meta)."""
    if not os.path.exists(MARKET_CSV):
        fetch_market_data()
    df = pd.read_csv(MARKET_CSV, index_col="Date", parse_dates=True).sort_index().astype(float)
    notes = []
    for sym, ratio in SPLIT_RATIOS.items():
        df, d0 = _fix_split(df, sym, ratio)
        if d0 is not None:
            notes.append(f"{SHORT[sym]}: prices before {d0:%d %b %Y} divided by {ratio} "
                         f"(un-adjusted {int(ratio * 2)}:2 share split/bonus in the Yahoo series).")
    meta = {}
    if os.path.exists(MARKET_META):
        with open(MARKET_META) as f:
            meta = json.load(f)
    else:
        meta = {"source": "Yahoo Finance chart API",
                "downloaded_at": dt.datetime.fromtimestamp(os.path.getmtime(MARKET_CSV)).isoformat(timespec="seconds")}
    return df, notes, meta


def total_return_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Dividend-adjusted closes for the three stocks + Nifty."""
    return df[[f"{s}_AdjClose" for s in STOCKS + ["NIFTY"]]].rename(columns=lambda c: c.replace("_AdjClose", ""))


def period_returns(prices: pd.DataFrame, freq: str = "M", years: float | None = 5) -> pd.DataFrame:
    """Simple returns at month-end ('M') or daily ('D') frequency over the last `years`."""
    if years:
        prices = prices[prices.index >= prices.index[-1] - pd.DateOffset(months=int(round(years * 12)))]
    if freq == "M":
        prices = prices.resample("ME").last()
    return prices.pct_change().dropna(how="all")


# --------------------------------------------------------------------------------------
# Workbook
# --------------------------------------------------------------------------------------
def _num(v):
    return float(v) if isinstance(v, (int, float)) else None


def load_workbook_model(path: str = WORKBOOK) -> dict:
    wb = openpyxl.load_workbook(path, data_only=True)
    a = wb["assumptions"]
    if a["B6"].value is None or wb["summary"]["B7"].value is None:
        raise WorkbookNotCalculated("Open SA_final_workbook.xlsx in Excel and save it so formula values are cached.")
    model = {
        "assumptions": {
            "valuation_date": a["B5"].value, "rf": _num(a["B6"].value), "rf_note": a["C6"].value,
            "erp": _num(a["B7"].value), "erp_note": a["C7"].value, "tax": _num(a["B8"].value),
            "blume_w": _num(a["B10"].value), "g_step": _num(a["B12"].value), "w_step": _num(a["B13"].value),
            "tv_ceiling": _num(a["B18"].value), "accumulate_above": _num(a["B19"].value),
            "avoid_below": _num(a["B20"].value),
        },
        "stocks": {},
    }
    w, s, rv = wb["wacc"], wb["summary"], wb["relative_val"]
    for k in STOCKS:
        col = WB_COL[k]
        d = wb[DCF_SHEETS[k]]
        t, fcff = [], []
        for c in range(4, 30):
            tv, fv = d.cell(14, c).value, d.cell(30, c).value
            if not isinstance(tv, (int, float)) or not isinstance(fv, (int, float)):
                break
            t.append(float(tv)); fcff.append(float(fv))
        r = wb[RATIO_SHEETS[k]]
        years = [r.cell(4, c).value for c in range(2, 8)]
        ratios = {}
        for row in range(6, 60):
            lab = r.cell(row, 1).value
            if lab:
                ratios[str(lab).strip()] = [_num(r.cell(row, c).value) for c in range(2, 8)]
        crow, prow, orow, irow = RELVAL_ROWS[k]
        multiples = {}
        for i, (name, mcol) in enumerate([("P/E", 9), ("EV/EBITDA", 10), ("P/B", 11)]):
            multiples[name] = {"current": _num(rv.cell(crow, mcol).value), "peer_median": _num(rv.cell(prow, mcol).value),
                               "own_5y_median": _num(rv.cell(orow, mcol).value),
                               "peer_implied": _num(rv.cell(irow + i, 4).value),
                               "own_implied": _num(rv.cell(irow + i, 6).value),
                               "in_blend": _num(rv.cell(irow + i, 7).value)}
        model["stocks"][k] = {
            "cmp": _num(a[f"{col}23"].value),
            "shares_cr": _num(d["B8"].value), "debt": _num(d["B9"].value), "cash": _num(d["B10"].value),
            "wacc": _num(d["B6"].value), "g": _num(d["B7"].value),
            "dcf_t": t, "dcf_fcff": fcff,
            "dcf_iv": _num(s[f"{col}7"].value), "peer_iv": _num(s[f"{col}8"].value), "own_iv": _num(s[f"{col}9"].value),
            "tv_pct": _num(s[f"{col}16"].value), "verdict": s[f"{col}13"].value,
            "beta_raw_wb": _num(w[f"{col}7"].value), "beta_adj_wb": _num(w[f"{col}8"].value),
            "ke_wb": _num(w[f"{col}9"].value), "kd_wb": _num(w[f"{col}14"].value),
            "years": years, "ratios": ratios, "multiples": multiples,
        }
    return model


# --------------------------------------------------------------------------------------
# Valuation
# --------------------------------------------------------------------------------------
def dcf_value(fcff, t, wacc, g, debt, cash, shares):
    """Two-stage FCFF DCF identical to the workbook formula. Returns dict or None if WACC <= g."""
    fcff, t = np.asarray(fcff, float), np.asarray(t, float)
    if wacc <= g or len(fcff) == 0:
        return None
    pv_explicit = float(np.sum(fcff / (1 + wacc) ** t))
    tv = fcff[-1] * (1 + g) / (wacc - g)
    pv_tv = tv / (1 + wacc) ** t[-1]
    ev = pv_explicit + pv_tv
    eq = ev - debt + cash
    return {"pv_explicit": pv_explicit, "tv": tv, "pv_tv": pv_tv, "ev": ev, "equity": eq,
            "iv": eq / shares, "tv_pct": pv_tv / ev}


def dcf_grid(stock: dict, wacc: float, g: float, w_step=0.005, g_step=0.005):
    waccs = [wacc + i * w_step for i in range(-2, 3)]
    gs = [g + j * g_step for j in range(-2, 3)]
    z = []
    for w in waccs:
        row = []
        for gg in gs:
            v = dcf_value(stock["dcf_fcff"], stock["dcf_t"], w, gg, stock["debt"], stock["cash"], stock["shares_cr"])
            row.append(v["iv"] if v else np.nan)
        z.append(row)
    return waccs, gs, np.array(z)


def margin_of_safety(iv, cmp):
    return (iv - cmp) / iv if iv else np.nan


def verdict(mos, accumulate_above=0.2, avoid_below=-0.1):
    if mos is None or np.isnan(mos):
        return "n/a"
    return "Accumulate" if mos > accumulate_above else ("Avoid" if mos < avoid_below else "Hold")


# --------------------------------------------------------------------------------------
# Risk & performance
# --------------------------------------------------------------------------------------
def beta(r: pd.Series, m: pd.Series) -> float:
    x = pd.concat([r, m], axis=1).dropna()
    return float(np.cov(x.iloc[:, 0], x.iloc[:, 1], ddof=1)[0, 1] / np.var(x.iloc[:, 1], ddof=1))


def max_drawdown(r: pd.Series) -> float:
    w = (1 + r.fillna(0)).cumprod()
    return float((w / w.cummax() - 1).min())


def risk_metrics(rets: pd.DataFrame, bench: pd.Series, rf: float, ppy: int = 12) -> pd.DataFrame:
    """Annualised metrics. Return = arithmetic mean x ppy (workbook convention); CAGR shown separately."""
    rows = {}
    rb = bench.mean() * ppy
    for c in rets.columns:
        r = rets[c].dropna()
        ann = r.mean() * ppy
        vol = r.std(ddof=1) * np.sqrt(ppy)
        b = beta(r, bench)
        te = (r - bench.reindex(r.index)).std(ddof=1) * np.sqrt(ppy)
        n_years = len(r) / ppy
        cagr = (1 + r).prod() ** (1 / n_years) - 1 if n_years > 0 else np.nan
        rows[c] = {
            "Return (ann.)": ann, "CAGR": cagr, "Volatility": vol, "Beta": b,
            "Sharpe": (ann - rf) / vol if vol else np.nan,
            "Treynor": (ann - rf) / b if b else np.nan,
            "Jensen alpha": ann - (rf + b * (rb - rf)),
            "Tracking error": te,
            "Information ratio": (ann - rb) / te if te > 1e-12 else np.nan,
            "Max drawdown": max_drawdown(r),
        }
    return pd.DataFrame(rows).T


def blume(raw_beta: float, w: float = 0.67) -> float:
    return w * raw_beta + (1 - w) * 1.0


def capm(beta_adj: float, rf: float, erp: float) -> float:
    return rf + beta_adj * erp


def port_stats(w, mu, cov):
    w = np.asarray(w, float)
    return float(w @ mu), float(np.sqrt(w @ cov @ w))


def tangency(mu, cov, rf, lo=0.05, hi=0.70):
    n = len(mu)
    lo = min(lo, 1.0 / n)
    hi = max(hi, 1.0 / n)

    def neg_sharpe(w):
        r, s = port_stats(w, mu, cov)
        return -(r - rf) / s

    res = minimize(neg_sharpe, np.full(n, 1 / n), method="SLSQP", bounds=[(lo, hi)] * n,
                   constraints={"type": "eq", "fun": lambda w: w.sum() - 1})
    return res.x


def efficient_frontier(mu, cov, lo=0.0, hi=1.0, n_pts=40):
    n = len(mu)
    gmv = minimize(lambda w: port_stats(w, mu, cov)[1], np.full(n, 1 / n), method="SLSQP",
                   bounds=[(lo, hi)] * n, constraints={"type": "eq", "fun": lambda w: w.sum() - 1}).x
    r_min = port_stats(gmv, mu, cov)[0]
    r_max = float(np.max(mu)) if hi >= 1 else float(np.sort(mu)[::-1][:int(np.ceil(1 / hi))].mean())
    pts = []
    for target in np.linspace(r_min, r_max, n_pts):
        cons = [{"type": "eq", "fun": lambda w: w.sum() - 1},
                {"type": "eq", "fun": lambda w, t=target: w @ mu - t}]
        res = minimize(lambda w: port_stats(w, mu, cov)[1], gmv, method="SLSQP", bounds=[(lo, hi)] * n, constraints=cons)
        if res.success:
            r, s = port_stats(res.x, mu, cov)
            pts.append((s, r))
    return pd.DataFrame(pts, columns=["vol", "ret"])


def portfolio_returns(rets: pd.DataFrame, weights: dict) -> pd.Series:
    """Periodically rebalanced portfolio return series."""
    cols = list(weights)
    w = np.array([weights[c] for c in cols])
    return (rets[cols] * w).sum(axis=1)


# --------------------------------------------------------------------------------------
# Questionnaire & allocation
# --------------------------------------------------------------------------------------
def score_questionnaire(sec_a: int, sec_b: int, prudence: bool = True) -> dict:
    raw = sec_a + sec_b
    triggered = prudence and abs(sec_a - sec_b) >= 6
    r_used = 2 * min(sec_a, sec_b) if triggered else raw
    A = round(10 - 0.3 * (r_used - 10), 1)
    basket = "Aggressive" if r_used >= 32 else ("Balanced" if r_used >= 22 else "Defensive")
    return {"sec_a": sec_a, "sec_b": sec_b, "raw_r": raw, "r_used": r_used,
            "prudence_triggered": triggered, "A": A, "basket": basket}


def equity_share(A: float, mu_p: float, sig_p: float, rf: float) -> float:
    """y* = (E(Rp) - Rf) / (A sigma^2), capped to [0, 1] (no leverage, no shorting the risky portfolio)."""
    return float(min(1.0, max(0.0, (mu_p - rf) / (A * sig_p ** 2))))


def utility(mu_c: float, sig_c: float, A: float) -> float:
    return mu_c - 0.5 * A * sig_c ** 2


# --------------------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------------------
def sip_projection(monthly: float, step_up: float, years: int, start_age: int, A_start: float, A_end: float,
                   mu_p: float, sig_p: float, rf: float, n_paths: int = 2000, seed: int = 7) -> pd.DataFrame:
    """Monthly SIP with a glide path: A moves linearly from A_start to A_end; equity share y*(A) each year.
    Returns yearly rows with deterministic (expected) wealth and Monte Carlo p10/p50/p90."""
    rng = np.random.default_rng(seed)
    wealth_det, invested = 0.0, 0.0
    wealth = np.zeros(n_paths)
    sip = monthly
    out = []
    for yr in range(1, years + 1):
        A_t = A_start + (A_end - A_start) * (yr - 1) / max(years - 1, 1)
        y = equity_share(A_t, mu_p, sig_p, rf)
        mu_c = y * mu_p + (1 - y) * rf
        sig_c = y * sig_p
        m_mu, m_sig = mu_c / 12, sig_c / np.sqrt(12)
        for _ in range(12):
            invested += sip
            wealth_det = (wealth_det + sip) * (1 + m_mu)
            wealth = (wealth + sip) * (1 + rng.normal(m_mu, m_sig, n_paths))
        p10, p50, p90 = np.percentile(wealth, [10, 50, 90])
        out.append({"year": yr, "age": start_age + yr, "A": round(A_t, 2), "equity_share": y,
                    "monthly_sip": sip, "invested": invested, "expected": wealth_det,
                    "p10": p10, "p50": p50, "p90": p90})
        sip *= 1 + step_up
    return pd.DataFrame(out)


def monte_carlo_gbm(close: pd.Series, days: int = 252, n_paths: int = 1000, lookback_days: int = 756, seed: int = 11):
    """GBM scenario fan using historical log-return drift/vol. Returns DataFrame of percentiles by day."""
    lr = np.log(close).diff().dropna().iloc[-lookback_days:]
    mu, sig = lr.mean(), lr.std(ddof=1)
    rng = np.random.default_rng(seed)
    shocks = rng.normal(mu, sig, (days, n_paths))
    paths = close.iloc[-1] * np.exp(np.cumsum(shocks, axis=0))
    pct = np.percentile(paths, [10, 25, 50, 75, 90], axis=1).T
    idx = pd.bdate_range(close.index[-1] + pd.Timedelta(days=1), periods=days)
    return pd.DataFrame(pct, index=idx, columns=["p10", "p25", "p50", "p75", "p90"]), {"mu_d": mu, "sig_d": sig}


# --------------------------------------------------------------------------------------
# Technicals
# --------------------------------------------------------------------------------------
def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def macd(close: pd.Series):
    m = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
    s = m.ewm(span=9, adjust=False).mean()
    return m, s, m - s


def technical_summary(close: pd.Series) -> dict:
    """TradingView-style tally: price vs SMA 20/50/100/200, RSI(14), MACD vs signal."""
    px = close.iloc[-1]
    signals = {}
    for n in (20, 50, 100, 200):
        ma = close.rolling(n).mean().iloc[-1]
        signals[f"SMA {n}"] = ("Buy" if px > ma else "Sell", ma)
    r = rsi(close).iloc[-1]
    signals["RSI (14)"] = ("Buy" if r < 30 else ("Sell" if r > 70 else "Neutral"), r)
    m, s, _ = macd(close)
    signals["MACD (12,26,9)"] = ("Buy" if m.iloc[-1] > s.iloc[-1] else "Sell", m.iloc[-1] - s.iloc[-1])
    buys = sum(v[0] == "Buy" for v in signals.values())
    sells = sum(v[0] == "Sell" for v in signals.values())
    score = (buys - sells) / len(signals)
    label = ("Strong sell" if score <= -0.5 else "Sell" if score < -0.1 else
             "Neutral" if score <= 0.1 else "Buy" if score < 0.5 else "Strong buy")
    return {"signals": signals, "buys": buys, "sells": sells,
            "neutral": len(signals) - buys - sells, "score": score, "label": label, "rsi": r}


def trailing_returns(close: pd.Series) -> dict:
    last = close.index[-1]
    out = {}
    for lab, off in [("1W", pd.DateOffset(weeks=1)), ("1M", pd.DateOffset(months=1)), ("3M", pd.DateOffset(months=3)),
                     ("6M", pd.DateOffset(months=6)), ("YTD", None), ("1Y", pd.DateOffset(years=1)),
                     ("5Y", pd.DateOffset(years=5))]:
        start = pd.Timestamp(year=last.year, month=1, day=1) if lab == "YTD" else last - off
        base = close[close.index <= start]
        base = base.iloc[-1] if len(base) else close.iloc[0]
        out[lab] = close.iloc[-1] / base - 1
    return out
