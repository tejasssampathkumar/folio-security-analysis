"""
FOLIO — AI-Augmented Security Analysis & Portfolio Terminal
Trent Ltd. (NSE: TRENT) | Asian Paints Ltd. (NSE: ASIANPAINT) | Tata Consultancy Services (NSE: TCS)
"""
from __future__ import annotations

import json
import os

import numpy as np
import openpyxl
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import folio_ai as fa
import folio_core as fc

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & TRADE GOTHIC / BRIGHT OFF-WHITE / RED-BLUE DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Folio | Security Analysis & Portfolio Terminal",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Color tokens
BG_MAIN = "#F7F8FA"
BG_CARD = "#FFFFFF"
BORDER = "#E2E8F0"
NAVY = "#0F172A"
BLUE_DARK = "#1E3A8A"
BLUE = "#2563EB"
BLUE_SOFT = "#EFF6FF"
RED = "#DC2626"
RED_SOFT = "#FEF2F2"
GREEN = "#059669"
GREEN_SOFT = "#ECFDF5"
AMBER = "#D97706"
SLATE = "#475569"
MUTED = "#64748B"
GRID = "#EEF2F6"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto+Condensed:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Trade Gothic', 'Trade Gothic Next', 'Roboto Condensed', 'Franklin Gothic Medium', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: {BG_MAIN} !important;
    color: {NAVY} !important;
}}

.block-container {{
    padding-top: 1.4rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1440px !important;
}}

h1, h2, h3, h4 {{
    font-family: 'Trade Gothic', 'Oswald', 'Roboto Condensed', sans-serif !important;
    letter-spacing: 0.4px;
    color: {NAVY} !important;
}}

/* Top Masthead */
.folio-masthead {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-top: 3px solid {BLUE};
    border-radius: 6px;
    padding: 14px 22px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}}
.folio-brand {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.folio-mark {{
    width: 44px;
    height: 44px;
    background: {BLUE_DARK};
    color: #FFFFFF;
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 27px;
    font-weight: 700;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    border-bottom: 3px solid {RED};
    line-height: 1;
}}
.folio-mark span {{
    color: {RED};
}}
.folio-wordmark {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {NAVY};
    line-height: 1;
}}
.folio-sub {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    color: {MUTED};
    margin-top: 4px;
}}
.folio-ticker-strip {{
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    align-items: center;
}}
.folio-mini-quote {{
    border-left: 2px solid {BORDER};
    padding-left: 14px;
}}
.folio-mini-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: {MUTED};
}}
.folio-mini-val {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 17px;
    font-weight: 700;
    color: {NAVY};
}}

/* Symbol Overview Header (TradingView SPX Style) */
.tv-symbol-bar {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}}
.tv-exchange-pill {{
    background: {BLUE_SOFT};
    color: {BLUE};
    border: 1px solid #BFDBFE;
    padding: 3px 9px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}}
.tv-thesis-pill {{
    background: {RED_SOFT};
    color: {RED};
    border: 1px solid #FECACA;
    padding: 3px 9px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}}
.tv-big-price {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 38px;
    font-weight: 700;
    color: {NAVY};
    line-height: 1.05;
}}
.tv-chg-pos {{
    background: {GREEN_SOFT};
    color: {GREEN};
    border: 1px solid #A7F3D0;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 14px;
}}
.tv-chg-neg {{
    background: {RED_SOFT};
    color: {RED};
    border: 1px solid #FECACA;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 14px;
}}
.tv-stat-grid {{
    display: grid;
    grid-template-columns: repeat(6, minmax(95px, 1fr));
    gap: 12px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid {BORDER};
}}
.tv-stat-cell-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: {MUTED};
}}
.tv-stat-cell-val {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 16px;
    font-weight: 600;
    color: {NAVY};
    margin-top: 2px;
}}

/* Trailing Returns Strip */
.tv-perf-strip {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin: 10px 0 14px 0;
}}
.tv-perf-box {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 8px 10px;
    text-align: center;
}}
.tv-perf-horizon {{
    font-size: 11px;
    font-weight: 700;
    color: {MUTED};
    letter-spacing: 0.7px;
}}
.tv-perf-num {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 16px;
    font-weight: 700;
    margin-top: 2px;
}}

/* Standard Cards */
.folio-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
}}
.folio-card-accent-blue {{
    border-top: 3px solid {BLUE};
}}
.folio-card-accent-red {{
    border-top: 3px solid {RED};
}}
.folio-card-kicker {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.85px;
    color: {MUTED};
    margin-bottom: 4px;
}}
.folio-card-metric {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 26px;
    font-weight: 700;
    color: {BLUE_DARK};
    line-height: 1.15;
}}
.folio-card-note {{
    font-size: 12px;
    color: {SLATE};
    margin-top: 5px;
    line-height: 1.35;
}}

/* Section Headers */
.folio-section-head {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 2px solid {NAVY};
    padding-bottom: 6px;
    margin: 14px 0 12px 0;
}}
.folio-section-title {{
    font-family: 'Oswald', 'Trade Gothic', sans-serif !important;
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: {NAVY};
}}
.folio-section-meta {{
    font-size: 12px;
    font-weight: 600;
    color: {MUTED};
}}

/* Navigation Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background-color: {BG_CARD};
    padding: 6px 8px;
    border-radius: 6px;
    border: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Oswald', 'Trade Gothic', 'Roboto Condensed', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    padding: 8px 16px !important;
    color: {SLATE} !important;
    border-radius: 4px !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: {BLUE} !important;
    color: #FFFFFF !important;
}}

/* Callout Banners */
.folio-alert-red {{
    background: {RED_SOFT};
    border-left: 4px solid {RED};
    padding: 11px 15px;
    border-radius: 0 5px 5px 0;
    color: #7F1D1D;
    font-size: 13px;
    margin: 10px 0;
}}
.folio-alert-blue {{
    background: {BLUE_SOFT};
    border-left: 4px solid {BLUE};
    padding: 11px 15px;
    border-radius: 0 5px 5px 0;
    color: {BLUE_DARK};
    font-size: 13px;
    margin: 10px 0;
}}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 2. CACHED DATA LOADERS
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_bundle():
    daily_df, split_notes, meta = fc.load_market_data()
    wb_model = fc.load_workbook_model()
    with open(os.path.join(fc.OUTPUT_DIR, "ai_pipeline_outputs.json")) as f:
        ai_data = json.load(f)

    # Also load exact 60-month returns from workbook `returns` tab so user can toggle
    wb = openpyxl.load_workbook(fc.WORKBOOK, data_only=True)
    ws_ret = wb["returns"]
    wb_months = [str(ws_ret.cell(r, 1).value) for r in range(6, 66)]
    wb_p = pd.DataFrame(
        {
            "TRENT": [float(ws_ret.cell(r, 2).value) for r in range(5, 66)],
            "ASIANPAINT": [float(ws_ret.cell(r, 3).value) for r in range(5, 66)],
            "TCS": [float(ws_ret.cell(r, 4).value) for r in range(5, 66)],
            "NIFTY": [float(ws_ret.cell(r, 5).value) for r in range(5, 66)],
        }
    )
    wb_monthly_rets = wb_p.pct_change().dropna()
    wb_monthly_rets.index = wb_months

    # Earnings quality summary from workbook
    ws_eq = wb["earnings_quality"]
    eq_rows = [
        {
            "Company": "Trent Ltd.",
            "5Y Cumulative CFO / PAT": f"{float(ws_eq['H8'].value):.2f}x",
            "5Y Avg Accruals Ratio": f"{float(ws_eq['H9'].value)*100:.2f}%",
            "Receivables - Sales Growth Gap": f"{float(ws_eq['H12'].value)*100:.1f}%",
            "Other Income % of PBT (5Y Avg)": f"{float(ws_eq['H13'].value)*100:.1f}%",
            "Key Footnote Audit": "Ind AS 116 lease liabilities (~Rs 3,500 Cr) drive reported borrowings; Tata RPTs <3% of net worth.",
        },
        {
            "Company": "Asian Paints Ltd.",
            "5Y Cumulative CFO / PAT": f"{float(ws_eq['H30'].value):.2f}x",
            "5Y Avg Accruals Ratio": f"{float(ws_eq['H31'].value)*100:.2f}%",
            "Receivables - Sales Growth Gap": f"{float(ws_eq['H34'].value)*100:.1f}%",
            "Other Income % of PBT (5Y Avg)": f"{float(ws_eq['H35'].value)*100:.1f}%",
            "Key Footnote Audit": "Disputed tax claims (~Rs 845 Cr, ~5.2% of net worth); strong dealer rebate discipline.",
        },
        {
            "Company": "TCS Ltd.",
            "5Y Cumulative CFO / PAT": f"{float(ws_eq['H52'].value):.2f}x",
            "5Y Avg Accruals Ratio": f"{float(ws_eq['H53'].value)*100:.2f}%",
            "Receivables - Sales Growth Gap": f"{float(ws_eq['H56'].value)*100:.1f}%",
            "Other Income % of PBT (5Y Avg)": f"{float(ws_eq['H57'].value)*100:.1f}%",
            "Key Footnote Audit": "Cash conversion >100% of PAT; net cash balance sheet; arm's-length Tata Sons transactions.",
        },
    ]
    return daily_df, split_notes, meta, wb_model, ai_data, wb_monthly_rets, pd.DataFrame(eq_rows)


daily_df, split_notes, market_meta, wb_model, ai_data, wb_monthly_rets, eq_df = load_bundle()


def plot_layout(fig: go.Figure, height: int = 420, title: str | None = None, ytitle: str | None = None):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Oswald, Trade Gothic, sans-serif", size=15, color=NAVY)) if title else None,
        height=height,
        margin=dict(l=12, r=14, t=36 if title else 14, b=14),
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family="Trade Gothic, Roboto Condensed, sans-serif", size=12, color=SLATE),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(255,255,255,0.85)"),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, side="right", title=ytitle),
    )
    return fig


# -----------------------------------------------------------------------------
# 3. GLOBAL MODEL PARAMETERS & LIVE PORTFOLIO COMPUTATION
# -----------------------------------------------------------------------------
with st.expander("GLOBAL MODEL PARAMETERS & DATA BASIS (CLICK TO ADJUST LIVE)", expanded=False):
    g1, g2, g3, g4, g5 = st.columns([2.4, 1.4, 1.4, 1.4, 1.4])
    with g1:
        return_basis = st.selectbox(
            "Return Series Basis for Betas & Backtest",
            options=["Workbook 60M Series (Exact Excel Match)", "Daily Split-Adjusted Series (5Y Monthly)"],
            index=0,
        )
    with g2:
        rf_long = st.number_input(
            "10Y G-Sec Rf (% p.a. — DCF/CAPM)",
            min_value=4.0,
            max_value=10.0,
            value=round(wb_model["assumptions"]["rf"] * 100, 3),
            step=0.05,
        ) / 100.0
    with g3:
        rf_short = st.number_input(
            "91D T-Bill Rf (% p.a. — Portfolio)",
            min_value=3.0,
            max_value=9.5,
            value=6.80,
            step=0.05,
        ) / 100.0
    with g4:
        erp_in = st.number_input(
            "India Equity Risk Premium (%)",
            min_value=4.0,
            max_value=10.0,
            value=round(wb_model["assumptions"]["erp"] * 100, 2),
            step=0.10,
        ) / 100.0
    with g5:
        max_w_cap = st.slider("Max Single-Stock MVO Weight (%)", min_value=40, max_value=100, value=70, step=5) / 100.0

# Select active monthly return matrix
if "Workbook" in return_basis:
    active_m_rets = wb_monthly_rets.copy()
else:
    px_adj = fc.total_return_prices(daily_df)
    active_m_rets = fc.period_returns(px_adj, "M", 5)

cov_ann = active_m_rets[fc.STOCKS].cov() * 12

# Compute live CAPM expected returns from active betas
raw_betas = {k: fc.beta(active_m_rets[k], active_m_rets["NIFTY"]) for k in fc.STOCKS}
adj_betas = {k: fc.blume(raw_betas[k], wb_model["assumptions"]["blume_w"]) for k in fc.STOCKS}
capm_ke = {k: fc.capm(adj_betas[k], rf_long, erp_in) for k in fc.STOCKS}

mu_vec = np.array([capm_ke[k] for k in fc.STOCKS])
w_tan_arr = fc.tangency(mu_vec, cov_ann.values, rf_short, lo=0.05, hi=max_w_cap)
w_tan = {k: float(w_tan_arr[i]) for i, k in enumerate(fc.STOCKS)}
mu_tan, sig_tan = fc.port_stats(w_tan_arr, mu_vec, cov_ann.values)
sharpe_tan = (mu_tan - rf_short) / sig_tan

# Add Equal-Weight and Tangency series to monthly returns for the 4 performance ratios table
rets_with_ports = active_m_rets[fc.STOCKS].copy()
rets_with_ports["Equal-Weight (3 Stocks)"] = active_m_rets[fc.STOCKS].mean(axis=1)
rets_with_ports["Optimal Tangency Portfolio"] = fc.portfolio_returns(active_m_rets, w_tan)
rets_with_ports["Nifty 50 Benchmark"] = active_m_rets["NIFTY"]

metrics_table = fc.risk_metrics(rets_with_ports, active_m_rets["NIFTY"], rf_long, ppy=12)

# Initialize Questionnaire state in st.session_state so all tabs & AI Strategist share it
if "q_sec_a" not in st.session_state:
    st.session_state["q_sec_a"] = [4, 4, 4, 3, 3]  # default 18
if "q_sec_b" not in st.session_state:
    st.session_state["q_sec_b"] = [3, 3, 4, 3, 3]  # default 16
if "q_prudence" not in st.session_state:
    st.session_state["q_prudence"] = True

q_prof = fc.score_questionnaire(
    sum(st.session_state["q_sec_a"]),
    sum(st.session_state["q_sec_b"]),
    prudence=st.session_state["q_prudence"],
)
y_star_live = fc.equity_share(q_prof["A"], mu_tan, sig_tan, rf_short)

# -----------------------------------------------------------------------------
# 4. TOP MASTHEAD ("F." LOGO + FOLIO WORDMARK + LIVE TICKER STRIP)
# -----------------------------------------------------------------------------
ew_alpha = metrics_table.loc["Equal-Weight (3 Stocks)", "Jensen alpha"] * 100
ew_sharpe = metrics_table.loc["Equal-Weight (3 Stocks)", "Sharpe"]

st.markdown(
    f"""
<div class="folio-masthead">
    <div class="folio-brand">
        <div class="folio-mark">F<span>.</span></div>
        <div>
            <div class="folio-wordmark">FOLIO</div>
            <div class="folio-sub">Narrative vs. Numbers &middot; Security Analysis &amp; Lifecycle Portfolio Terminal</div>
        </div>
    </div>
    <div class="folio-ticker-strip">
        <div class="folio-mini-quote">
            <div class="folio-mini-label">NSE: TRENT</div>
            <div class="folio-mini-val">Rs {wb_model['stocks']['TRENT']['cmp']:,.0f} <span style="color:{RED};font-size:12px;">DCF Rs {wb_model['stocks']['TRENT']['dcf_iv']:,.0f}</span></div>
        </div>
        <div class="folio-mini-quote">
            <div class="folio-mini-label">NSE: ASIANPAINT</div>
            <div class="folio-mini-val">Rs {wb_model['stocks']['ASIANPAINT']['cmp']:,.0f} <span style="color:{BLUE};font-size:12px;">Own-5Y Rs {wb_model['stocks']['ASIANPAINT']['own_iv']:,.0f}</span></div>
        </div>
        <div class="folio-mini-quote">
            <div class="folio-mini-label">NSE: TCS</div>
            <div class="folio-mini-val">Rs {wb_model['stocks']['TCS']['cmp']:,.0f} <span style="color:{GREEN};font-size:12px;">Peer Rs {wb_model['stocks']['TCS']['peer_iv']:,.0f}</span></div>
        </div>
        <div class="folio-mini-quote">
            <div class="folio-mini-label">10Y G-SEC / 91D T-BILL</div>
            <div class="folio-mini-val" style="color:{BLUE_DARK};">{rf_long*100:.2f}% / {rf_short*100:.2f}%</div>
        </div>
        <div class="folio-mini-quote">
            <div class="folio-mini-label">TANGENCY SHARPE / EW ALPHA</div>
            <div class="folio-mini-val" style="color:{GREEN};">{sharpe_tan:+.2f} / {ew_alpha:+.2f}%</div>
        </div>
        <div class="folio-mini-quote">
            <div class="folio-mini-label">ACTIVE PROFILE (A = {q_prof['A']:.1f})</div>
            <div class="folio-mini-val" style="color:{BLUE};">{q_prof['basket'].upper()} &middot; {y_star_live*100:.0f}% EQ</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5. FIVE NAVIGATION TABS (ZERO EMOJIS)
# -----------------------------------------------------------------------------
tab_mkt, tab_port, tab_risk, tab_val, tab_ai = st.tabs(
    [
        "01 / MARKET TERMINAL",
        "02 / PORTFOLIO & RATIOS",
        "03 / RISK QUESTIONNAIRE & SIP",
        "04 / VALUATION & NLP LAB",
        "05 / FOLIO AI STRATEGIST",
    ]
)

# =============================================================================
# TAB 1: MARKET TERMINAL (TRADINGVIEW SPX-STYLE SYMBOL PAGE)
# =============================================================================
with tab_mkt:
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2.8, 2.2, 2.2, 2.8])
    with ctrl1:
        sym = st.selectbox(
            "INSTRUMENT",
            options=["TRENT", "ASIANPAINT", "TCS", "TBILL"],
            format_func=lambda k: {
                "TRENT": "TRENT — Trent Ltd. (NSE)",
                "ASIANPAINT": "ASIANPAINT — Asian Paints Ltd. (NSE)",
                "TCS": "TCS — Tata Consultancy Services Ltd. (NSE)",
                "TBILL": "IN91TB / IN10YG — Sovereign Risk-Free Benchmarks (RBI)",
            }[k],
        )
    with ctrl2:
        tf = st.radio("HORIZON", options=["1M", "3M", "6M", "YTD", "1Y", "5Y", "ALL"], index=5, horizontal=True)
    with ctrl3:
        chart_mode = st.radio("CHART MODE", options=["Area", "Candlestick", "Line"], index=0, horizontal=True)
    with ctrl4:
        sub_indicator = st.radio(
            "LOWER OSCILLATOR & FORECAST",
            options=["RSI (14)", "MACD (12,26,9)", "1Y Monte Carlo Fan"],
            index=0,
            horizontal=True,
        )

    if sym != "TBILL":
        s_open = daily_df[f"{sym}_Open"]
        s_high = daily_df[f"{sym}_High"]
        s_low = daily_df[f"{sym}_Low"]
        s_close = daily_df[f"{sym}_Close"]
        s_vol = daily_df[f"{sym}_Volume"]

        ma50 = s_close.rolling(50).mean()
        ma200 = s_close.rolling(200).mean()
        rsi_ser = fc.rsi(s_close, 14)
        macd_l, macd_s, macd_h = fc.macd(s_close)
        tech = fc.technical_summary(s_close)
        tr_rets = fc.trailing_returns(s_close)

        end_dt = daily_df.index[-1]
        start_dt = {
            "1M": end_dt - pd.DateOffset(months=1),
            "3M": end_dt - pd.DateOffset(months=3),
            "6M": end_dt - pd.DateOffset(months=6),
            "YTD": pd.Timestamp(year=end_dt.year, month=1, day=1),
            "1Y": end_dt - pd.DateOffset(years=1),
            "5Y": end_dt - pd.DateOffset(years=5),
            "ALL": daily_df.index[0],
        }[tf]

        sl = daily_df.index >= start_dt
        idx = daily_df.index[sl]
        c_sl = s_close[sl]
        o_sl, h_sl, l_sl, v_sl = s_open[sl], s_high[sl], s_low[sl], s_vol[sl]

        last_px = float(c_sl.iloc[-1])
        first_px = float(c_sl.iloc[0])
        prev_px = float(c_sl.iloc[-2]) if len(c_sl) > 1 else first_px
        day_chg = last_px - prev_px
        day_pct = day_chg / prev_px * 100
        period_pct = (last_px / first_px - 1) * 100

        w52_slice = s_close.iloc[-252:]
        w52_lo, w52_hi = float(w52_slice.min()), float(w52_slice.max())
        st_wb = wb_model["stocks"][sym]
        mcap_cr = st_wb["cmp"] * st_wb["shares_cr"]

        day_cls = "tv-chg-pos" if day_chg >= 0 else "tv-chg-neg"
        per_cls = "tv-chg-pos" if period_pct >= 0 else "tv-chg-neg"
        sig_color = GREEN if "buy" in tech["label"].lower() else (RED if "sell" in tech["label"].lower() else SLATE)

        st.markdown(
            f"""
        <div class="tv-symbol-bar">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:14px;">
                <div>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span class="tv-exchange-pill">NSE : {sym}</span>
                        <span style="font-size:13px;font-weight:700;color:{SLATE};text-transform:uppercase;">{fc.SECTOR[sym]}</span>
                        <span class="tv-thesis-pill">{fc.THESIS[sym].split(':')[0]}</span>
                    </div>
                    <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;">
                        <span style="font-family:'Oswald','Trade Gothic',sans-serif;font-size:24px;font-weight:700;color:{BLUE_DARK};">{fc.NAMES[sym]}</span>
                        <span class="tv-big-price">Rs {last_px:,.2f}</span>
                        <span class="{day_cls}">1D {day_chg:+.2f} ({day_pct:+.2f}%)</span>
                        <span class="{per_cls}">{tf} {period_pct:+.2f}%</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="tv-stat-cell-label">TECHNICAL CONSENSUS ({tech['buys']} BUY / {tech['neutral']} NEUTRAL / {tech['sells']} SELL)</div>
                    <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:{sig_color};text-transform:uppercase;margin-top:2px;">
                        {tech['label']} &middot; RSI {tech['rsi']:.1f}
                    </div>
                </div>
            </div>
            <div class="tv-stat-grid">
                <div>
                    <div class="tv-stat-cell-label">52-WEEK RANGE</div>
                    <div class="tv-stat-cell-val">Rs {w52_lo:,.0f} &ndash; Rs {w52_hi:,.0f}</div>
                </div>
                <div>
                    <div class="tv-stat-cell-label">MARKET CAP (WB)</div>
                    <div class="tv-stat-cell-val">Rs {mcap_cr:,.0f} Cr</div>
                </div>
                <div>
                    <div class="tv-stat-cell-label">P/E &middot; EV/EBITDA</div>
                    <div class="tv-stat-cell-val">{st_wb['multiples']['P/E']['current']:.1f}x &middot; {st_wb['multiples']['EV/EBITDA']['current']:.1f}x</div>
                </div>
                <div>
                    <div class="tv-stat-cell-label">DCF INTRINSIC VALUE</div>
                    <div class="tv-stat-cell-val" style="color:{RED};">Rs {st_wb['dcf_iv']:,.1f}</div>
                </div>
                <div>
                    <div class="tv-stat-cell-label">PEER-IMPLIED VALUE</div>
                    <div class="tv-stat-cell-val" style="color:{BLUE};">Rs {st_wb['peer_iv']:,.0f}</div>
                </div>
                <div>
                    <div class="tv-stat-cell-label">OWN 5Y MEDIAN VALUE</div>
                    <div class="tv-stat-cell-val" style="color:{GREEN};">Rs {st_wb['own_iv']:,.0f}</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Trailing Returns Strip (TradingView bottom performance tiles)
        boxes_html = []
        for h_lab, r_val in tr_rets.items():
            c_hex = GREEN if r_val >= 0 else RED
            boxes_html.append(
                f'<div class="tv-perf-box">'
                f'<div class="tv-perf-horizon">{h_lab} RETURN</div>'
                f'<div class="tv-perf-num" style="color:{c_hex};">{r_val*100:+.2f}%</div>'
                f"</div>"
            )
        st.markdown(f'<div class="tv-perf-strip">{"".join(boxes_html)}</div>', unsafe_allow_html=True)

        # Overlay checkboxes
        ov1, ov2, ov3, ov4 = st.columns(4)
        show_ma50 = ov1.checkbox("Show 50-Day SMA", value=True)
        show_ma200 = ov2.checkbox("Show 200-Day SMA", value=True)
        show_Peer = ov3.checkbox("Show Peer-Implied & Own-5Y Reference Lines", value=True)
        show_dcf = ov4.checkbox("Show DCF Intrinsic Value Line", value=True)

        # Build 3-row TradingView Chart
        fig_tv = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=[0.64, 0.16, 0.20],
        )

        if chart_mode == "Candlestick":
            fig_tv.add_trace(
                go.Candlestick(
                    x=idx,
                    open=o_sl,
                    high=h_sl,
                    low=l_sl,
                    close=c_sl,
                    name=f"{sym} OHLC",
                    increasing_line_color=BLUE,
                    decreasing_line_color=RED,
                    increasing_fillcolor=BLUE,
                    decreasing_fillcolor=RED,
                ),
                row=1,
                col=1,
            )
        elif chart_mode == "Area":
            line_col = BLUE if period_pct >= 0 else RED
            fill_col = "rgba(37, 99, 235, 0.12)" if period_pct >= 0 else "rgba(220, 38, 38, 0.10)"
            fig_tv.add_trace(
                go.Scatter(
                    x=idx,
                    y=c_sl,
                    mode="lines",
                    name=f"{sym} Close",
                    line=dict(color=line_col, width=2.4),
                    fill="tozeroy",
                    fillcolor=fill_col,
                ),
                row=1,
                col=1,
            )
        else:
            fig_tv.add_trace(
                go.Scatter(x=idx, y=c_sl, mode="lines", name=f"{sym} Close", line=dict(color=BLUE_DARK, width=2.4)),
                row=1,
                col=1,
            )

        if show_ma50:
            fig_tv.add_trace(
                go.Scatter(x=idx, y=ma50[sl], mode="lines", name="SMA 50", line=dict(color=BLUE, width=1.4, dash="dot")),
                row=1,
                col=1,
            )
        if show_ma200:
            fig_tv.add_trace(
                go.Scatter(x=idx, y=ma200[sl], mode="lines", name="SMA 200", line=dict(color=RED, width=1.6)),
                row=1,
                col=1,
            )
        if show_dcf:
            fig_tv.add_hline(
                y=st_wb["dcf_iv"],
                line_dash="dash",
                line_color=RED,
                line_width=1.4,
                annotation_text=f"DCF IV: Rs {st_wb['dcf_iv']:,.0f}",
                annotation_position="bottom left",
                row=1,
                col=1,
            )
        if show_Peer:
            fig_tv.add_hline(
                y=st_wb["peer_iv"],
                line_dash="dot",
                line_color=BLUE,
                line_width=1.3,
                annotation_text=f"Peer Multiples: Rs {st_wb['peer_iv']:,.0f}",
                annotation_position="top left",
                row=1,
                col=1,
            )

        # If Monte Carlo Fan selected, project 1Y forward on row 1 as well
        if sub_indicator == "1Y Monte Carlo Fan":
            mc_df, mc_stats = fc.monte_carlo_gbm(s_close, days=252, n_paths=1000)
            fig_tv.add_trace(
                go.Scatter(x=mc_df.index, y=mc_df["p90"], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"),
                row=1,
                col=1,
            )
            fig_tv.add_trace(
                go.Scatter(
                    x=mc_df.index,
                    y=mc_df["p10"],
                    mode="lines",
                    fill="tonexty",
                    fillcolor="rgba(37, 99, 235, 0.12)",
                    line=dict(width=0),
                    name="MC p10–p90 Band",
                ),
                row=1,
                col=1,
            )
            fig_tv.add_trace(
                go.Scatter(
                    x=mc_df.index,
                    y=mc_df["p50"],
                    mode="lines",
                    name="MC Median Path (p50)",
                    line=dict(color=BLUE, width=2, dash="dash"),
                ),
                row=1,
                col=1,
            )

        # Row 2: Volume
        v_colors = [BLUE if c >= o else RED for c, o in zip(c_sl, o_sl)]
        fig_tv.add_trace(
            go.Bar(x=idx, y=v_sl, name="Volume", marker_color=v_colors, opacity=0.65),
            row=2,
            col=1,
        )

        # Row 3: RSI or MACD
        if sub_indicator in ("RSI (14)", "1Y Monte Carlo Fan"):
            fig_tv.add_trace(
                go.Scatter(x=idx, y=rsi_ser[sl], mode="lines", name="RSI (14)", line=dict(color=BLUE_DARK, width=1.6)),
                row=3,
                col=1,
            )
            fig_tv.add_hline(y=70, line_dash="dot", line_color=RED, line_width=1, row=3, col=1)
            fig_tv.add_hline(y=30, line_dash="dot", line_color=GREEN, line_width=1, row=3, col=1)
            r3_title = "RSI (14)"
        else:
            h_vals = macd_h[sl]
            h_cols = [BLUE if v >= 0 else RED for v in h_vals]
            fig_tv.add_trace(go.Bar(x=idx, y=h_vals, name="MACD Hist", marker_color=h_cols, opacity=0.6), row=3, col=1)
            fig_tv.add_trace(go.Scatter(x=idx, y=macd_l[sl], mode="lines", name="MACD", line=dict(color=BLUE_DARK, width=1.5)), row=3, col=1)
            fig_tv.add_trace(go.Scatter(x=idx, y=macd_s[sl], mode="lines", name="Signal", line=dict(color=RED, width=1.4)), row=3, col=1)
            r3_title = "MACD"

        fig_tv.update_layout(
            height=640,
            margin=dict(l=12, r=14, t=10, b=10),
            paper_bgcolor=BG_CARD,
            plot_bgcolor=BG_CARD,
            font=dict(family="Trade Gothic, Roboto Condensed, sans-serif", size=12, color=SLATE),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor=GRID, rangeslider=dict(visible=False)),
            yaxis=dict(showgrid=True, gridcolor=GRID, side="right", title="Price (Rs)"),
            xaxis2=dict(showgrid=True, gridcolor=GRID),
            yaxis2=dict(showgrid=True, gridcolor=GRID, side="right", title="Volume"),
            xaxis3=dict(showgrid=True, gridcolor=GRID),
            yaxis3=dict(showgrid=True, gridcolor=GRID, side="right", title=r3_title),
        )
        st.plotly_chart(fig_tv, width="stretch")

        if split_notes and sym == "TRENT":
            st.markdown(
                f'<div class="folio-alert-blue"><strong>Corporate Action Data Note:</strong> {split_notes[0]}</div>',
                unsafe_allow_html=True,
            )

    else:
        # Sovereign T-Bill & 10Y G-Sec Cumulative Yield Curve View
        st.markdown(
            f"""
        <div class="tv-symbol-bar">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div>
                    <span class="tv-exchange-pill">RBI SOVEREIGN BENCHMARKS</span>
                    <div style="display:flex;align-items:baseline;gap:16px;margin-top:6px;">
                        <span style="font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;color:{BLUE_DARK};">Sovereign Risk-Free Rate Term Structure</span>
                        <span class="tv-big-price">{rf_short*100:.2f}% <span style="font-size:18px;color:{MUTED};">(91D T-Bill)</span></span>
                        <span class="tv-big-price" style="color:{BLUE};">{rf_long*100:.2f}% <span style="font-size:18px;color:{MUTED};">(10Y G-Sec)</span></span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="tv-stat-cell-label">ROLE IN MODEL</div>
                    <div style="font-size:13px;font-weight:700;color:{NAVY};">91D T-Bill blends with Optimal Risky Portfolio &middot; 10Y G-Sec anchors CAPM &amp; DCF WACC</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        t_idx = daily_df.index
        r_tb_d = (1 + rf_short) ** (1 / 252) - 1
        r_gs_d = (1 + rf_long) ** (1 / 252) - 1
        tb_nav = 100.0 * np.cumprod(np.full(len(t_idx), 1 + r_tb_d))
        gs_nav = 100.0 * np.cumprod(np.full(len(t_idx), 1 + r_gs_d))
        nifty_nav = daily_df["NIFTY_Close"] / daily_df["NIFTY_Close"].iloc[0] * 100.0

        fig_rf = go.Figure()
        fig_rf.add_trace(go.Scatter(x=t_idx, y=tb_nav, name=f"91-Day RBI T-Bill ({rf_short*100:.2f}% p.a.)", line=dict(color=BLUE, width=2.8)))
        fig_rf.add_trace(go.Scatter(x=t_idx, y=gs_nav, name=f"10-Year India G-Sec ({rf_long*100:.2f}% p.a.)", line=dict(color=RED, width=2.4, dash="dash")))
        fig_rf.add_trace(go.Scatter(x=t_idx, y=nifty_nav, name="Nifty 50 Index (Base = 100)", line=dict(color=SLATE, width=1.8, dash="dot")))
        plot_layout(fig_rf, height=480, title="5-Year Reinvested Sovereign Total Return Index vs. Nifty 50 (Base = 100)", ytitle="Index Value (Base 100)")
        st.plotly_chart(fig_rf, width="stretch")


# =============================================================================
# TAB 2: PORTFOLIO COMMAND & PERFORMANCE RATIOS
# =============================================================================
with tab_port:
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">02A / FOUR CORE RISK-ADJUSTED PERFORMANCE RATIOS (5-YEAR AUDIT)</div>
        <div class="folio-section-meta">SHARPE &middot; TREYNOR &middot; JENSEN'S ALPHA &middot; INFORMATION RATIO</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    p_inspect = st.selectbox(
        "Select Portfolio or Security to Highlight in KPI Cards",
        options=["Equal-Weight (3 Stocks)", "Optimal Tangency Portfolio", "TRENT", "ASIANPAINT", "TCS"],
        index=0,
    )
    row_sel = metrics_table.loc[p_inspect]
    row_nif = metrics_table.loc["Nifty 50 Benchmark"]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-blue">
            <div class="folio-card-kicker">SHARPE RATIO &middot; (Rp - Rf) / VOL</div>
            <div class="folio-card-metric">{row_sel['Sharpe']:+.2f} <span style="font-size:14px;color:{MUTED};">vs Nifty {row_nif['Sharpe']:+.2f}</span></div>
            <div class="folio-card-note">Forward MVO Tangency Sharpe: <strong>+{sharpe_tan:.2f}</strong> (at Rf = {rf_short*100:.2f}%).</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-blue">
            <div class="folio-card-kicker">TREYNOR RATIO &middot; (Rp - Rf) / BETA</div>
            <div class="folio-card-metric">{row_sel['Treynor']*100:+.2f}% <span style="font-size:14px;color:{MUTED};">Beta {row_sel['Beta']:.2f}</span></div>
            <div class="folio-card-note">Nifty 50 Benchmark Treynor: <strong>{row_nif['Treynor']*100:+.2f}%</strong> (Beta = 1.00).</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with k3:
        a_col = GREEN if row_sel["Jensen alpha"] >= 0 else RED
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-red">
            <div class="folio-card-kicker">JENSEN'S ALPHA &middot; Rp - CAPM</div>
            <div class="folio-card-metric" style="color:{a_col};">{row_sel['Jensen alpha']*100:+.2f}% <span style="font-size:14px;color:{MUTED};">p.a.</span></div>
            <div class="folio-card-note">Abnormal annual return above CAPM benchmark expectation.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with k4:
        ir_col = GREEN if row_sel["Information ratio"] >= 0 else RED
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-red">
            <div class="folio-card-kicker">INFORMATION RATIO &middot; ACTIVE / TE</div>
            <div class="folio-card-metric" style="color:{ir_col};">{row_sel['Information ratio']:+.2f} <span style="font-size:14px;color:{MUTED};">TE {row_sel['Tracking error']*100:.1f}%</span></div>
            <div class="folio-card-note">Active return over Nifty 50 per unit of tracking error.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Cumulative Wealth & Drawdown Chart
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">02B / 5-YEAR CUMULATIVE WEALTH OF RS 1,00,000 &amp; UNDERWATER DRAWDOWN</div>
        <div class="folio-section-meta">COMPARE INDIVIDUAL EQUITIES, TANGENCY, COMPLETE UTILITY PORTFOLIO, EQUAL-WEIGHT &amp; NIFTY 50</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    px_norm = daily_df[["TRENT_Close", "ASIANPAINT_Close", "TCS_Close", "NIFTY_Close"]].copy()
    px_norm = px_norm / px_norm.iloc[0] * 100000.0
    tan_nav = w_tan["TRENT"] * px_norm["TRENT_Close"] + w_tan["ASIANPAINT"] * px_norm["ASIANPAINT_Close"] + w_tan["TCS"] * px_norm["TCS_Close"]
    ew_nav = (px_norm["TRENT_Close"] + px_norm["ASIANPAINT_Close"] + px_norm["TCS_Close"]) / 3.0
    tb_nav_rs = 100000.0 * np.cumprod(np.full(len(px_norm), (1 + rf_short) ** (1 / 252)))
    complete_nav = y_star_live * tan_nav + (1 - y_star_live) * tb_nav_rs

    show_indiv = st.checkbox("Overlay Individual Stock Wealth Curves (Trent, Asian Paints, TCS)", value=False)

    fig_wealth = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.70, 0.30])
    fig_wealth.add_trace(
        go.Scatter(x=px_norm.index, y=ew_nav, name=f"Equal-Weight 3-Stock (Rs {ew_nav.iloc[-1]:,.0f})", line=dict(color=BLUE, width=2.7)),
        row=1,
        col=1,
    )
    fig_wealth.add_trace(
        go.Scatter(x=px_norm.index, y=complete_nav, name=f"Active Investor Utility Portfolio ({q_prof['basket']}, Rs {complete_nav.iloc[-1]:,.0f})", line=dict(color=RED, width=2.6)),
        row=1,
        col=1,
    )
    fig_wealth.add_trace(
        go.Scatter(x=px_norm.index, y=tan_nav, name=f"MVO Tangency Portfolio (Rs {tan_nav.iloc[-1]:,.0f})", line=dict(color=BLUE_DARK, width=2.0, dash="dash")),
        row=1,
        col=1,
    )
    fig_wealth.add_trace(
        go.Scatter(x=px_norm.index, y=px_norm["NIFTY_Close"], name=f"Nifty 50 Benchmark (Rs {px_norm['NIFTY_Close'].iloc[-1]:,.0f})", line=dict(color=SLATE, width=1.8, dash="dot")),
        row=1,
        col=1,
    )
    fig_wealth.add_trace(
        go.Scatter(x=px_norm.index, y=tb_nav_rs, name=f"91-Day Sovereign T-Bill (Rs {tb_nav_rs[-1]:,.0f})", line=dict(color=GREEN, width=1.6, dash="dashdot")),
        row=1,
        col=1,
    )
    if show_indiv:
        fig_wealth.add_trace(go.Scatter(x=px_norm.index, y=px_norm["TRENT_Close"], name="Trent Ltd.", line=dict(width=1.3)), row=1, col=1)
        fig_wealth.add_trace(go.Scatter(x=px_norm.index, y=px_norm["ASIANPAINT_Close"], name="Asian Paints", line=dict(width=1.3)), row=1, col=1)
        fig_wealth.add_trace(go.Scatter(x=px_norm.index, y=px_norm["TCS_Close"], name="TCS", line=dict(width=1.3)), row=1, col=1)

    # Underwater Drawdown
    for ser, nm, col in [(ew_nav, "EW Drawdown", BLUE), (tan_nav, "Tangency Drawdown", RED), (px_norm["NIFTY_Close"], "Nifty Drawdown", SLATE)]:
        dd = (ser / ser.cummax() - 1) * 100
        fig_wealth.add_trace(go.Scatter(x=px_norm.index, y=dd, name=nm, line=dict(color=col, width=1.5)), row=2, col=1)

    fig_wealth.update_layout(
        height=560,
        margin=dict(l=12, r=14, t=12, b=12),
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family="Trade Gothic, Roboto Condensed, sans-serif", size=12, color=SLATE),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor=GRID),
        yaxis=dict(showgrid=True, gridcolor=GRID, side="right", title="Portfolio Value (Rs)"),
        xaxis2=dict(showgrid=True, gridcolor=GRID),
        yaxis2=dict(showgrid=True, gridcolor=GRID, side="right", title="Drawdown (%)"),
    )
    st.plotly_chart(fig_wealth, width="stretch")

    # Row: Efficient Frontier + CAL | Weights & Correlation Heatmap
    ef_col, wt_col = st.columns([5.6, 4.4])
    with ef_col:
        st.markdown(
            """
        <div class="folio-section-head">
            <div class="folio-section-title">02C / EFFICIENT FRONTIER &amp; CAPITAL ALLOCATION LINE (CAL)</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        ef_df = fc.efficient_frontier(mu_vec, cov_ann.values, lo=0.0, hi=1.0, n_pts=45)
        cal_vols = np.linspace(0, 0.36, 40)
        cal_rets = rf_short + sharpe_tan * cal_vols
        c_vol = y_star_live * sig_tan
        c_ret = y_star_live * mu_tan + (1 - y_star_live) * rf_short

        fig_ef = go.Figure()
        fig_ef.add_trace(
            go.Scatter(x=ef_df["vol"] * 100, y=ef_df["ret"] * 100, mode="lines", name="Unconstrained Efficient Frontier", line=dict(color=BLUE_DARK, width=2.5))
        )
        fig_ef.add_trace(
            go.Scatter(x=cal_vols * 100, y=cal_rets * 100, mode="lines", name="Capital Allocation Line (CAL)", line=dict(color=BLUE, width=2, dash="dash"))
        )
        fig_ef.add_trace(
            go.Scatter(
                x=[sig_tan * 100],
                y=[mu_tan * 100],
                mode="markers+text",
                name="Optimal Tangency Portfolio",
                text=["Tangency"],
                textposition="top left",
                marker=dict(color=BLUE, size=13, symbol="diamond"),
            )
        )
        fig_ef.add_trace(
            go.Scatter(
                x=[c_vol * 100],
                y=[c_ret * 100],
                mode="markers+text",
                name=f"Investor Point (A={q_prof['A']:.1f}, y*={y_star_live*100:.0f}%)",
                text=[f"Investor ({q_prof['basket']})"],
                textposition="bottom right",
                marker=dict(color=RED, size=14, symbol="star"),
            )
        )
        for i, k in enumerate(fc.STOCKS):
            sv = np.sqrt(cov_ann.loc[k, k]) * 100
            sr = mu_vec[i] * 100
            fig_ef.add_trace(
                go.Scatter(
                    x=[sv],
                    y=[sr],
                    mode="markers+text",
                    name=fc.SHORT[k],
                    text=[fc.SHORT[k]],
                    textposition="top center",
                    marker=dict(color=NAVY, size=9),
                )
            )
        plot_layout(fig_ef, height=390, ytitle="Expected Annual Return (%)")
        fig_ef.update_xaxes(title_text="Annualised Volatility (%)")
        st.plotly_chart(fig_ef, width="stretch")

    with wt_col:
        st.markdown(
            """
        <div class="folio-section-head">
            <div class="folio-section-title">02D / CORRELATION MATRIX &amp; MVO WEIGHTS</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        corr_m = active_m_rets[["TRENT", "ASIANPAINT", "TCS", "NIFTY"]].corr()
        fig_corr = go.Figure(
            data=go.Heatmap(
                z=corr_m.values,
                x=["Trent", "Asian Paints", "TCS", "Nifty 50"],
                y=["Trent", "Asian Paints", "TCS", "Nifty 50"],
                colorscale=[[0.0, "#EFF6FF"], [0.5, "#60A5FA"], [1.0, "#1E3A8A"]],
                zmin=0,
                zmax=1,
                text=np.round(corr_m.values, 3),
                texttemplate="%{text:.2f}",
                textfont=dict(size=13, family="Oswald, sans-serif"),
            )
        )
        plot_layout(fig_corr, height=235, title="60-Month Return Correlation Heatmap (Asian Paints vs TCS = 0.19)")
        st.plotly_chart(fig_corr, width="stretch")

        wt_df = pd.DataFrame(
            {
                "Asset": ["Asian Paints Ltd.", "Tata Consultancy Services", "Trent Ltd.", "91-Day RBI T-Bill"],
                "Risky Tangency Weight": [f"{w_tan['ASIANPAINT']*100:.1f}%", f"{w_tan['TCS']*100:.1f}%", f"{w_tan['TRENT']*100:.1f}%", "0.0%"],
                f"Complete Utility Weight ({q_prof['basket']})": [
                    f"{y_star_live*w_tan['ASIANPAINT']*100:.1f}%",
                    f"{y_star_live*w_tan['TCS']*100:.1f}%",
                    f"{y_star_live*w_tan['TRENT']*100:.1f}%",
                    f"{(1-y_star_live)*100:.1f}%",
                ],
                "CAPM Expected Return": [f"{capm_ke['ASIANPAINT']*100:.2f}%", f"{capm_ke['TCS']*100:.2f}%", f"{capm_ke['TRENT']*100:.2f}%", f"{rf_short*100:.2f}%"],
            }
        )
        st.dataframe(wt_df, width="stretch", hide_index=True)

    # Full 10-column Risk & Performance Audit Table
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">02E / COMPLETE RISK &amp; PERFORMANCE AUDIT TABLE</div>
        <div class="folio-section-meta">ALL FOUR MEMORY-SPECIFIED RATIOS PLUS BETA, CAGR &amp; MAX DRAWDOWN</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    disp_m = metrics_table.copy()
    for pct_col in ("Return (ann.)", "CAGR", "Volatility", "Treynor", "Jensen alpha", "Tracking error", "Max drawdown"):
        disp_m[pct_col] = disp_m[pct_col].map(lambda x: f"{x*100:+.2f}%" if pd.notna(x) else "-")
    for num_col in ("Beta", "Sharpe", "Information ratio"):
        disp_m[num_col] = disp_m[num_col].map(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
    st.dataframe(disp_m, width="stretch")


# =============================================================================
# TAB 3: RISK QUESTIONNAIRE & LIFECYCLE SIP GLIDE PATH
# =============================================================================
with tab_risk:
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">03A / INVESTOR RISK-AVERSION QUESTIONNAIRE (10 QUESTIONS + PRUDENCE RULE)</div>
        <div class="folio-section-meta">A = 10 &minus; 0.3 &times; (R &minus; 10) &middot; U = E(Rp) &minus; 0.5 &times; A &times; VAR</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    preset_col, prud_col = st.columns([6, 4])
    with preset_col:
        preset_choice = st.radio(
            "Load Worked Archetype from PDF or Use Custom Interactive Answers Below",
            options=[
                "Custom Interactive Answers",
                "Priya, 27, stable job (Sec A=17, Sec B=19 -> Aggressive)",
                "Rahul, 41, mixed (Sec A=13, Sec B=14 -> Balanced)",
                "Meena, 58, cautious (Sec A=8, Sec B=7 -> Defensive)",
                "Arjun, 30, bold but stretched (Sec A=7, Sec B=16 -> Prudence Triggered)",
            ],
            index=0,
            horizontal=True,
        )
    with prud_col:
        st.session_state["q_prudence"] = st.checkbox(
            "Apply Prudence Rule: If |Section A - Section B| >= 6, set R = 2 x min(Section A, Section B)",
            value=st.session_state["q_prudence"],
        )

    qa_col, qb_col = st.columns(2)
    ans_a, ans_b = [], []
    with qa_col:
        st.markdown(
            f'<div style="background:{BLUE_SOFT};border-left:4px solid {BLUE};padding:8px 12px;font-weight:700;color:{BLUE_DARK};margin-bottom:10px;">'
            "SECTION A: YOUR SITUATION (ABILITY TO TAKE RISK &middot; Q1 TO Q5)</div>",
            unsafe_allow_html=True,
        )
        for idx_q, (q_text, opts) in enumerate(fc.QUESTIONS["A"]):
            sel = st.selectbox(
                q_text,
                options=opts,
                index=0 if idx_q < 3 else 1,
                format_func=lambda x: f"{x[0]}  [{x[1]} pts]",
                key=f"qa_{idx_q}",
            )
            ans_a.append(sel[1])

    with qb_col:
        st.markdown(
            f'<div style="background:{RED_SOFT};border-left:4px solid {RED};padding:8px 12px;font-weight:700;color:{RED};margin-bottom:10px;">'
            "SECTION B: YOUR ATTITUDES (WILLINGNESS TO TAKE RISK &middot; Q6 TO Q10)</div>",
            unsafe_allow_html=True,
        )
        for idx_q, (q_text, opts) in enumerate(fc.QUESTIONS["B"]):
            sel = st.selectbox(
                q_text,
                options=opts,
                index=2,
                format_func=lambda x: f"{x[0]}  [{x[1]} pts]",
                key=f"qb_{idx_q}",
            )
            ans_b.append(sel[1])

    st.session_state["q_sec_a"] = ans_a
    st.session_state["q_sec_b"] = ans_b

    if preset_choice.startswith("Priya"):
        sa, sb = 17, 19
    elif preset_choice.startswith("Rahul"):
        sa, sb = 13, 14
    elif preset_choice.startswith("Meena"):
        sa, sb = 8, 7
    elif preset_choice.startswith("Arjun"):
        sa, sb = 7, 16
    else:
        sa, sb = sum(ans_a), sum(ans_b)

    q_prof = fc.score_questionnaire(sa, sb, prudence=st.session_state["q_prudence"])
    y_star_live = fc.equity_share(q_prof["A"], mu_tan, sig_tan, rf_short)
    c_ret_live = y_star_live * mu_tan + (1 - y_star_live) * rf_short
    c_vol_live = y_star_live * sig_tan
    u_live = fc.utility(c_ret_live, c_vol_live, q_prof["A"])

    if q_prof["prudence_triggered"]:
        st.markdown(
            f"""
        <div class="folio-alert-red">
            <strong>PRUDENCE RULE ACTIVE:</strong> Section A ({sa} pts) and Section B ({sb} pts) differ by
            <strong>{abs(sa - sb)} points (&ge; 6)</strong>. Raw score R = {q_prof['raw_r']} is replaced with
            <strong>2 &times; min({sa}, {sb}) = {q_prof['r_used']}</strong> so portfolio risk never exceeds either financial ability or temperament.
        </div>
        """,
            unsafe_allow_html=True,
        )

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-blue">
            <div class="folio-card-kicker">SCORE R USED (SEC A: {sa} | SEC B: {sb})</div>
            <div class="folio-card-metric">{q_prof['r_used']} / 40 <span style="font-size:14px;color:{MUTED};">Raw {q_prof['raw_r']}</span></div>
            <div class="folio-card-note">Range 10 to 40 across 10 questions.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-blue">
            <div class="folio-card-kicker">RISK-AVERSION COEFFICIENT (A)</div>
            <div class="folio-card-metric">{q_prof['A']:.1f} <span style="font-size:14px;color:{MUTED};">Scale 1&ndash;10</span></div>
            <div class="folio-card-note">A = 10 &minus; 0.3 &times; ({q_prof['r_used']} &minus; 10).</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with r3:
        b_col = RED if q_prof["basket"] == "Aggressive" else (BLUE if q_prof["basket"] == "Balanced" else GREEN)
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-red">
            <div class="folio-card-kicker">ASSIGNED INVESTOR BASKET</div>
            <div class="folio-card-metric" style="color:{b_col};">{q_prof['basket'].upper()}</div>
            <div class="folio-card-note">Expected Utility U = {u_live*100:.2f}% | E(Rc) = {c_ret_live*100:.2f}%, Vol = {c_vol_live*100:.2f}%.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with r4:
        st.markdown(
            f"""
        <div class="folio-card folio-card-accent-red">
            <div class="folio-card-kicker">OPTIMAL UTILITY ALLOCATION (y*)</div>
            <div class="folio-card-metric">{y_star_live*100:.1f}% EQ <span style="font-size:14px;color:{MUTED};">{(1-y_star_live)*100:.1f}% T-Bill</span></div>
            <div class="folio-card-note">AP {y_star_live*w_tan['ASIANPAINT']*100:.1f}% &middot; TCS {y_star_live*w_tan['TCS']*100:.1f}% &middot; Trent {y_star_live*w_tan['TRENT']*100:.1f}%.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Worked Archetypes Reference Table
    arch_rows = []
    for name, (a_pts, b_pts) in fc.ARCHETYPES.items():
        sc = fc.score_questionnaire(a_pts, b_pts, prudence=st.session_state["q_prudence"])
        ys = fc.equity_share(sc["A"], mu_tan, sig_tan, rf_short)
        arch_rows.append(
            {
                "Respondent": name,
                "Sec A": a_pts,
                "Sec B": b_pts,
                "Raw R": sc["raw_r"],
                "R Used": sc["r_used"],
                "Prudence": "Yes" if sc["prudence_triggered"] else "No",
                "Risk Aversion A": sc["A"],
                "Basket": sc["basket"],
                "Equity Share (y*)": f"{ys*100:.1f}%",
                "91D T-Bill Share": f"{(1-ys)*100:.1f}%",
                "Asian Paints": f"{ys*w_tan['ASIANPAINT']*100:.1f}%",
                "TCS": f"{ys*w_tan['TCS']*100:.1f}%",
                "Trent": f"{ys*w_tan['TRENT']*100:.1f}%",
            }
        )
    st.dataframe(pd.DataFrame(arch_rows), width="stretch", hide_index=True)

    # Interactive 20-Year Monthly SIP & Glide Path Simulator
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">03B / LIFECYCLE MONTHLY SIP &amp; DYNAMIC GLIDE PATH SIMULATOR</div>
        <div class="folio-section-meta">MONTE CARLO P10 / P50 / P90 WEALTH FAN + AGE-DEPENDENT EQUITY GLIDE</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    s1, s2, s3, s4, s5 = st.columns(5)
    sip_mo = s1.number_input("Starting Monthly SIP (Rs)", min_value=5000, max_value=500000, value=25000, step=5000)
    sip_step = s2.slider("Annual SIP Step-Up (%)", min_value=0, max_value=25, value=10, step=1) / 100.0
    sip_yrs = s3.slider("Investment Horizon (Years)", min_value=5, max_value=35, value=20, step=1)
    sip_age = s4.number_input("Starting Age", min_value=18, max_value=60, value=25, step=1)
    sip_a_end = s5.slider("Terminal Risk Aversion A (at Horizon End)", min_value=4.0, max_value=10.0, value=8.5, step=0.5)

    sip_sim = fc.sip_projection(
        monthly=sip_mo,
        step_up=sip_step,
        years=sip_yrs,
        start_age=sip_age,
        A_start=q_prof["A"],
        A_end=sip_a_end,
        mu_p=mu_tan,
        sig_p=sig_tan,
        rf=rf_short,
    )

    fig_sip = make_subplots(specs=[[{"secondary_y": True}]])
    fig_sip.add_trace(
        go.Scatter(x=sip_sim["age"], y=sip_sim["p90"] / 1e7, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"),
        secondary_y=False,
    )
    fig_sip.add_trace(
        go.Scatter(
            x=sip_sim["age"],
            y=sip_sim["p10"] / 1e7,
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(37, 99, 235, 0.12)",
            line=dict(width=0),
            name="Monte Carlo p10–p90 Band",
        ),
        secondary_y=False,
    )
    fig_sip.add_trace(
        go.Scatter(x=sip_sim["age"], y=sip_sim["expected"] / 1e7, name="Expected Wealth (Rs Cr)", line=dict(color=BLUE, width=3)),
        secondary_y=False,
    )
    fig_sip.add_trace(
        go.Scatter(x=sip_sim["age"], y=sip_sim["invested"] / 1e7, name="Cumulative Capital Invested (Rs Cr)", line=dict(color=SLATE, width=2, dash="dot")),
        secondary_y=False,
    )
    fig_sip.add_trace(
        go.Scatter(x=sip_sim["age"], y=sip_sim["equity_share"] * 100, name="Equity Allocation y*(A) (%)", mode="lines+markers", line=dict(color=RED, width=2.2)),
        secondary_y=True,
    )
    plot_layout(
        fig_sip,
        height=430,
        title=f"Projected Terminal Wealth at Age {int(sip_sim['age'].iloc[-1])}: Rs {sip_sim['expected'].iloc[-1]/1e7:.2f} Cr (Invested Rs {sip_sim['invested'].iloc[-1]/1e7:.2f} Cr | p10 Rs {sip_sim['p10'].iloc[-1]/1e7:.2f} Cr – p90 Rs {sip_sim['p90'].iloc[-1]/1e7:.2f} Cr)",
    )
    fig_sip.update_xaxes(title_text="Investor Age (Years)")
    fig_sip.update_yaxes(title_text="Wealth (Rs Crores)", secondary_y=False, showgrid=True, gridcolor=GRID)
    fig_sip.update_yaxes(title_text="Equity Share (%)", secondary_y=True, range=[0, 108], showgrid=False)
    st.plotly_chart(fig_sip, width="stretch")


# =============================================================================
# TAB 4: VALUATION & NLP SENTIMENT LAB
# =============================================================================
with tab_val:
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">04A / INTERACTIVE TWO-STAGE FCFF DCF SANDBOX &amp; SENSITIVITY HEATMAP</div>
        <div class="folio-section-meta">ADJUST WACC, TERMINAL GROWTH (g) &amp; FCFF SCALE TO STRESS-TEST INTRINSIC VALUE</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    v_c1, v_c2, v_c3, v_c4 = st.columns([2.4, 2.5, 2.5, 2.6])
    with v_c1:
        val_co = st.selectbox("Select Company for Valuation & NLP Deep-Dive", options=fc.STOCKS, format_func=lambda k: f"{fc.NAMES[k]} ({k})")
    st_co = wb_model["stocks"][val_co]
    with v_c2:
        wacc_in = st.slider(
            f"{fc.SHORT[val_co]} WACC (%)",
            min_value=8.0,
            max_value=24.0,
            value=round(st_co["wacc"] * 100, 2),
            step=0.25,
        ) / 100.0
    with v_c3:
        g_in = st.slider(
            f"{fc.SHORT[val_co]} Terminal Growth g (%)",
            min_value=2.0,
            max_value=7.5,
            value=round(st_co["g"] * 100, 2),
            step=0.25,
        ) / 100.0
    with v_c4:
        fcff_mult = st.slider(
            "Explicit Forecast FCFF Scale Multiplier (x)",
            min_value=0.70,
            max_value=2.00,
            value=1.00,
            step=0.05,
        )

    scaled_fcff = [x * fcff_mult for x in st_co["dcf_fcff"]]
    dcf_res = fc.dcf_value(scaled_fcff, st_co["dcf_t"], wacc_in, g_in, st_co["debt"], st_co["cash"], st_co["shares_cr"])

    if dcf_res:
        mos_live = fc.margin_of_safety(dcf_res["iv"], st_co["cmp"])
        verd_live = fc.verdict(mos_live, wb_model["assumptions"]["accumulate_above"], wb_model["assumptions"]["avoid_below"])
        d1, d2, d3, d4 = st.columns(4)
        d1.markdown(
            f'<div class="folio-card folio-card-accent-red"><div class="folio-card-kicker">LIVE DCF INTRINSIC VALUE</div>'
            f'<div class="folio-card-metric">Rs {dcf_res["iv"]:,.1f} <span style="font-size:14px;color:{MUTED};">CMP Rs {st_co["cmp"]:,.0f}</span></div>'
            f'<div class="folio-card-note">Workbook baseline IV: Rs {st_co["dcf_iv"]:,.1f}</div></div>',
            unsafe_allow_html=True,
        )
        d2.markdown(
            f'<div class="folio-card folio-card-accent-blue"><div class="folio-card-kicker">ENTERPRISE VALUE &amp; TV SHARE</div>'
            f'<div class="folio-card-metric">Rs {dcf_res["ev"]:,.0f} Cr</div>'
            f'<div class="folio-card-note">Terminal Value = {dcf_res["tv_pct"]*100:.1f}% of EV (Ceiling 75%).</div></div>',
            unsafe_allow_html=True,
        )
        d3.markdown(
            f'<div class="folio-card folio-card-accent-blue"><div class="folio-card-kicker">MARGIN OF SAFETY &amp; VERDICT</div>'
            f'<div class="folio-card-metric" style="color:{RED if mos_live<0 else GREEN};">{verd_live.upper()}</div>'
            f'<div class="folio-card-note">Upside vs CMP: {(dcf_res["iv"]/st_co["cmp"]-1)*100:+.1f}% (MoS {mos_live*100:+.1f}%).</div></div>',
            unsafe_allow_html=True,
        )
        d4.markdown(
            f'<div class="folio-card folio-card-accent-red"><div class="folio-card-kicker">PEER &amp; OWN-5Y IMPLIED</div>'
            f'<div class="folio-card-metric" style="color:{BLUE};">Rs {st_co["peer_iv"]:,.0f}</div>'
            f'<div class="folio-card-note">Own 5-Year Median Implied: <strong>Rs {st_co["own_iv"]:,.0f}</strong>.</div></div>',
            unsafe_allow_html=True,
        )

    hm_col, fb_col = st.columns([5, 5])
    with hm_col:
        stock_scaled = dict(st_co, dcf_fcff=scaled_fcff)
        w_grid, g_grid, z_mat = fc.dcf_grid(stock_scaled, wacc_in, g_in)
        fig_hm = go.Figure(
            data=go.Heatmap(
                z=z_mat,
                x=[f"g = {gg*100:.1f}%" for gg in g_grid],
                y=[f"WACC = {ww*100:.2f}%" for ww in w_grid],
                colorscale=[[0.0, "#FEF2F2"], [0.5, "#DBEAFE"], [1.0, "#1E3A8A"]],
                text=np.round(z_mat, 1),
                texttemplate="Rs %{text:,.0f}",
                textfont=dict(family="Oswald, sans-serif", size=13),
            )
        )
        plot_layout(fig_hm, height=340, title=f"{fc.SHORT[val_co]} 5x5 DCF Sensitivity Matrix (WACC vs Terminal Growth g)")
        st.plotly_chart(fig_hm, width="stretch")

    with fb_col:
        cos_lbl = [fc.SHORT[k] for k in fc.STOCKS]
        fig_fb = go.Figure()
        fig_fb.add_trace(go.Bar(name="DCF Intrinsic Value", x=cos_lbl, y=[wb_model["stocks"][k]["dcf_iv"] for k in fc.STOCKS], marker_color=RED))
        fig_fb.add_trace(go.Bar(name="Peer Multiples Implied", x=cos_lbl, y=[wb_model["stocks"][k]["peer_iv"] for k in fc.STOCKS], marker_color=BLUE))
        fig_fb.add_trace(go.Bar(name="Own 5Y History Implied", x=cos_lbl, y=[wb_model["stocks"][k]["own_iv"] for k in fc.STOCKS], marker_color=BLUE_DARK))
        fig_fb.add_trace(go.Bar(name="Current Market Price (CMP)", x=cos_lbl, y=[wb_model["stocks"][k]["cmp"] for k in fc.STOCKS], marker_color=NAVY))
        fig_fb.update_layout(barmode="group")
        plot_layout(fig_fb, height=340, title="Cross-Company Valuation Football Field (Rs per Share)", ytitle="Rs per Share")
        st.plotly_chart(fig_fb, width="stretch")

    # 5-Year Fundamental Ratio Explorer & Earnings Quality Audit
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">04B / 5-YEAR FUNDAMENTAL TRAJECTORY &amp; EARNINGS QUALITY AUDIT</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    rat_col, eq_col = st.columns([5.2, 4.8])
    with rat_col:
        yrs = st_co["years"]
        rats = st_co["ratios"]
        fig_rat = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rat.add_trace(go.Bar(x=yrs, y=rats["sales"], name="Revenue (Rs Cr)", marker_color=BLUE, opacity=0.78), secondary_y=False)
        fig_rat.add_trace(go.Bar(x=yrs, y=rats["net profit"], name="Net Profit (Rs Cr)", marker_color=BLUE_DARK, opacity=0.88), secondary_y=False)
        fig_rat.add_trace(
            go.Scatter(x=yrs, y=[x * 100 if x else None for x in rats["EBITDA margin"]], name="EBITDA Margin (%)", line=dict(color=RED, width=2.5)),
            secondary_y=True,
        )
        fig_rat.add_trace(
            go.Scatter(x=yrs, y=[x * 100 if x else None for x in rats["ROCE"]], name="ROCE (%)", line=dict(color=GREEN, width=2.2, dash="dash")),
            secondary_y=True,
        )
        plot_layout(fig_rat, height=320, title=f"{fc.NAMES[val_co]} — 6-Year Revenue, PAT, EBITDA Margin & ROCE")
        fig_rat.update_yaxes(title_text="Rs Crore", secondary_y=False)
        fig_rat.update_yaxes(title_text="Margin / ROCE (%)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_rat, width="stretch")

    with eq_col:
        st.dataframe(eq_df, width="stretch", hide_index=True)
        for fn in ai_data["verified_footnotes"]:
            st.markdown(
                f'<div style="background:{BG_CARD};border:1px solid {BORDER};border-left:3px solid {BLUE};padding:8px 12px;border-radius:4px;margin-bottom:6px;font-size:12px;">'
                f'<strong>{fn["company"]} &middot; {fn["category"]}</strong> '
                f'<span style="color:{GREEN};font-weight:700;">[{fn["verification_status"]}]</span><br>'
                f'<em>"{fn["quote"]}"</em> &mdash; {fn["impact"]}</div>',
                unsafe_allow_html=True,
            )

    # 8-Quarter Concall Sentiment & 150-Headline Bias Lab
    st.markdown(
        """
    <div class="folio-section-head">
        <div class="folio-section-title">04C / DUAL-MODEL CONCALL SENTIMENT (FINBERT VS LLAMA 3.1) &amp; 150-HEADLINE BIAS</div>
        <div class="folio-section-meta">8 QUARTERS &middot; 90-SENTENCE HUMAN VALIDATION BENCHMARK</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    sent_col, bias_col = st.columns([5.4, 4.6])
    with sent_col:
        s_co = ai_data["sentiment_data"][val_co]
        fig_sent = go.Figure()
        fig_sent.add_trace(go.Scatter(x=s_co["quarters"], y=s_co["mgmt_finbert"], name="Mgmt Remarks (FinBERT)", line=dict(color=BLUE, width=2.6)))
        fig_sent.add_trace(go.Scatter(x=s_co["quarters"], y=s_co["qa_finbert"], name="Analyst Q&A (FinBERT)", line=dict(color=RED, width=2.6)))
        fig_sent.add_trace(go.Scatter(x=s_co["quarters"], y=s_co["mgmt_llama"], name="Mgmt Remarks (Llama 3.1)", line=dict(color=BLUE_DARK, width=1.8, dash="dot")))
        fig_sent.add_trace(go.Scatter(x=s_co["quarters"], y=s_co["qa_llama"], name="Analyst Q&A (Llama 3.1)", line=dict(color=AMBER, width=1.8, dash="dot")))
        fig_sent.add_hline(y=0, line_color=SLATE, line_width=1, line_dash="dash")
        plot_layout(fig_sent, height=340, title=f"{fc.NAMES[val_co]} — 8-Quarter Concall Sentiment Trajectory (-1 to +1)", ytitle="Sentiment Score")
        st.plotly_chart(fig_sent, width="stretch")
        st.caption(f"Driver: {s_co['driver']}")

    with bias_col:
        bias_df = pd.DataFrame(ai_data["bias_distribution"]).T
        fig_bias = go.Figure()
        for b_name, b_color in [
            ("Hype / FOMO", RED),
            ("Extrapolation", AMBER),
            ("Loss Aversion", BLUE_DARK),
            ("Neutral / Factual", SLATE),
        ]:
            fig_bias.add_trace(
                go.Bar(name=b_name, x=["Trent", "Asian Paints", "TCS"], y=[bias_df.loc[k, b_name] for k in fc.STOCKS], marker_color=b_color)
            )
        fig_bias.update_layout(barmode="stack")
        plot_layout(fig_bias, height=340, title="150-Headline Behavioral Bias Classification (% of 50 Headlines/Co)", ytitle="Share of Headlines (%)")
        st.plotly_chart(fig_bias, width="stretch")

    # Disagreement Matrix + Live Ollama Custom Sentence Scorer
    st.markdown("**FinBERT vs. Local Llama 3.1 Disagreement Audit (90-Sentence Validation: Llama 88.9% Acc, kappa 0.829 vs FinBERT 82.2% Acc, kappa 0.732)**")
    st.dataframe(pd.DataFrame(ai_data["disagreements"]), width="stretch", hide_index=True)

    with st.expander("LIVE OLLAMA SENTIMENT & BIAS CLASSIFIER — TEST ANY CUSTOM CONCALL QUOTE OR HEADLINE", expanded=False):
        sc1, sc2, sc3 = st.columns([2, 6, 2])
        test_co = sc1.selectbox("Target Company", options=["Asian Paints", "Trent Ltd.", "TCS"], key="live_nlp_co")
        test_txt = sc2.text_input(
            "Enter Earnings Call Sentence or Financial News Headline",
            value="We calibrated dealer rebates selectively across decorative emulsions to defend market share against new entrants.",
        )
        if sc3.button("Score via Ollama Llama 3.1", width="stretch"):
            try:
                res_nlp = fa.analyze_custom_text_ollama(test_txt, test_co)
                st.json(res_nlp)
            except Exception as exc:
                st.error(f"Ollama request failed: {exc}")


# =============================================================================
# TAB 5: FOLIO AI STRATEGIST (LIVE OLLAMA LLM ON PORT 11434)
# =============================================================================
with tab_ai:
    ol_stat = fa.ollama_status()
    status_str = f"ONLINE ({ol_stat['default']})" if ol_stat["online"] else "OFFLINE (Start `ollama serve`)"
    st.markdown(
        f"""
    <div class="folio-section-head">
        <div class="folio-section-title">05 / FOLIO AI STRATEGIST &mdash; LIVE DATASET-GROUNDED OLLAMA CO-PILOT</div>
        <div class="folio-section-meta">STATUS: {status_str}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    context_brief = fa.build_context_brief(
        wb_model=wb_model,
        metrics_df=metrics_table,
        tangency_weights=w_tan,
        tangency_stats=(mu_tan, sig_tan, sharpe_tan),
        q_profile=q_prof,
        y_star=y_star_live,
        rf_long=rf_long,
        rf_short=rf_short,
        erp=erp_in,
        ai_data=ai_data,
    )

    ai_top1, ai_top2, ai_top3 = st.columns([3, 2, 5])
    with ai_top1:
        chosen_model = st.selectbox(
            "Local Ollama Model",
            options=ol_stat["models"] if ol_stat["models"] else [fa.DEFAULT_MODEL],
            index=0,
        )
    with ai_top2:
        temp_in = st.slider("Reasoning Temperature", min_value=0.0, max_value=0.8, value=0.2, step=0.05)
    with ai_top3:
        with st.expander("Inspect Live Numerical Context Injected into Ollama System Prompt"):
            st.code(context_brief, language="text")

    st.markdown("**One-Click Strategic Prompts (Click any button to query Ollama with live dashboard state):**")
    p_cols = st.columns(len(fa.PRESET_QUESTIONS))
    triggered_prompt = None
    for idx_p, (btn_label, btn_prompt) in enumerate(fa.PRESET_QUESTIONS):
        if p_cols[idx_p].button(btn_label, width="stretch", key=f"preset_btn_{idx_p}"):
            triggered_prompt = btn_prompt

    if "folio_chat" not in st.session_state:
        st.session_state["folio_chat"] = [
            {
                "role": "assistant",
                "content": (
                    "Folio AI Strategist initialized. Every response is grounded in your live workbook valuations "
                    "(Trent DCF Rs 229.6, Asian Paints Rs 439.1, TCS Rs 1,472.1), the 4 performance ratios "
                    "(Sharpe, Treynor, Jensen's Alpha, Information Ratio), MVO tangency weights "
                    f"(Asian Paints {w_tan['ASIANPAINT']*100:.1f}%, TCS {w_tan['TCS']*100:.1f}%, Trent {w_tan['TRENT']*100:.1f}%), "
                    f"and your active questionnaire profile (A = {q_prof['A']:.1f}, {q_prof['basket']}, {y_star_live*100:.1f}% Equity). "
                    "Select a strategic prompt above or ask any question below."
                ),
            }
        ]

    for msg in st.session_state["folio_chat"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask Folio AI Strategist about valuation gaps, MVO weights, Sharpe/Treynor/Alpha/IR, or SIP glide paths...")
    active_prompt = triggered_prompt or user_query

    if active_prompt:
        st.session_state["folio_chat"].append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        with st.chat_message("assistant"):
            if ol_stat["online"]:
                try:
                    history_for_llm = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state["folio_chat"][-6:]
                    ]
                    response_text = st.write_stream(
                        fa.stream_ollama_chat(
                            messages=history_for_llm,
                            context_brief=context_brief,
                            model=chosen_model,
                            temperature=temp_in,
                        )
                    )
                    st.session_state["folio_chat"].append({"role": "assistant", "content": response_text})
                except Exception as exc:
                    st.error(f"Ollama streaming error: {exc}")
            else:
                st.warning("Ollama server is currently offline. Run `ollama serve` in your terminal to enable live generation.")
