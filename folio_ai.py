"""
Folio AI Strategist — Local Ollama integration for live strategic insights
and on-demand sentiment/bias classification.

Connects to http://localhost:11434 (Ollama REST API) using `llama3.1:latest`
by default, grounding every answer in the live workbook, market, valuation,
and portfolio numbers passed from the Folio terminal.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Generator, Iterable

OLLAMA_BASE = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:latest"


def ollama_status() -> dict:
    """Return {'online': bool, 'models': [str, ...], 'default': str}."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags", headers={"User-Agent": "Folio/1.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode())
        models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        default = DEFAULT_MODEL if DEFAULT_MODEL in models else (models[0] if models else DEFAULT_MODEL)
        return {"online": True, "models": models, "default": default}
    except Exception as exc:
        return {"online": False, "models": [], "default": DEFAULT_MODEL, "error": str(exc)}


def build_context_brief(
    wb_model: dict,
    metrics_df,
    tangency_weights: dict,
    tangency_stats: tuple[float, float, float],
    q_profile: dict,
    y_star: float,
    rf_long: float,
    rf_short: float,
    erp: float,
    ai_data: dict,
) -> str:
    """Build a compact, exact numerical briefing of the current dashboard state for the LLM."""
    mu_p, sig_p, sh_p = tangency_stats
    lines = [
        "PROJECT: Narrative vs. Numbers — AI-Augmented Security Analysis of Trent, Asian Paints, and TCS (NSE India).",
        f"MACRO INPUTS: 10Y G-Sec Rf = {rf_long*100:.2f}%, 91D T-Bill Rf = {rf_short*100:.2f}%, India ERP = {erp*100:.2f}%.",
        "",
        "VALUATION & FUNDAMENTALS (SA_final_workbook.xlsx):",
    ]
    for k in ("TRENT", "ASIANPAINT", "TCS"):
        st = wb_model["stocks"][k]
        mos_dcf = (st["dcf_iv"] - st["cmp"]) / st["dcf_iv"] * 100
        lines.append(
            f"- {k}: CMP Rs {st['cmp']:,.0f} | DCF IV Rs {st['dcf_iv']:,.1f} (MoS {mos_dcf:+.1f}%) | "
            f"Peer-Implied Rs {st['peer_iv']:,.0f} | Own-5Y-History Rs {st['own_iv']:,.0f} | "
            f"WACC {st['wacc']*100:.2f}%, g {st['g']*100:.1f}%, TV/EV {st['tv_pct']*100:.1f}% | "
            f"P/E {st['multiples']['P/E']['current']:.1f}x, EV/EBITDA {st['multiples']['EV/EBITDA']['current']:.1f}x | "
            f"Raw Beta {st['beta_raw_wb']:.2f}, Blume Beta {st['beta_adj_wb']:.2f}, CAPM Ke {st['ke_wb']*100:.2f}%."
        )

    lines.append("")
    lines.append("5-YEAR HISTORICAL RISK & PERFORMANCE METRICS (Annualised):")
    for idx, row in metrics_df.iterrows():
        ir_str = f"{row['Information ratio']:.2f}" if row["Information ratio"] == row["Information ratio"] else "n/a"
        lines.append(
            f"- {idx}: Return {row['Return (ann.)']*100:.2f}% (CAGR {row['CAGR']*100:.2f}%), "
            f"Vol {row['Volatility']*100:.2f}%, Beta {row['Beta']:.2f}, "
            f"Sharpe {row['Sharpe']:.2f}, Treynor {row['Treynor']*100:.2f}%, "
            f"Jensen Alpha {row['Jensen alpha']*100:+.2f}%, Info Ratio {ir_str}, "
            f"Max Drawdown {row['Max drawdown']*100:.1f}%."
        )

    lines.extend([
        "",
        "OPTIMAL MVO TANGENCY PORTFOLIO (Forward-looking CAPM expected returns):",
        f"- Weights: Trent {tangency_weights['TRENT']*100:.1f}%, Asian Paints {tangency_weights['ASIANPAINT']*100:.1f}%, TCS {tangency_weights['TCS']*100:.1f}%.",
        f"- Expected Return: {mu_p*100:.2f}%, Expected Volatility: {sig_p*100:.2f}%, Forward Sharpe: {sh_p:.2f}.",
        "",
        "ACTIVE INVESTOR QUESTIONNAIRE PROFILE (Risk_Aversion_Questionnaire.pdf):",
        f"- Section A (Ability): {q_profile['sec_a']}/20 | Section B (Attitude): {q_profile['sec_b']}/20 | "
        f"Raw R: {q_profile['raw_r']}/40 | Prudence Rule Triggered: {q_profile['prudence_triggered']} -> R_used: {q_profile['r_used']}/40.",
        f"- Risk-Aversion Coefficient A = {q_profile['A']:.1f} -> Basket: {q_profile['basket']}.",
        f"- Utility-Optimal Complete Portfolio (U = E(Rp) - 0.5*A*Var): Equity Share y* = {y_star*100:.1f}%, 91D T-Bills = {(1-y_star)*100:.1f}%.",
        f"- Resulting Complete Weights: Trent {y_star*tangency_weights['TRENT']*100:.1f}%, "
        f"Asian Paints {y_star*tangency_weights['ASIANPAINT']*100:.1f}%, "
        f"TCS {y_star*tangency_weights['TCS']*100:.1f}%, 91D T-Bill {(1-y_star)*100:.1f}%.",
        "",
        "AI SENTIMENT & HEADLINE BIAS FINDINGS:",
    ])
    for k in ("TRENT", "ASIANPAINT", "TCS"):
        s = ai_data["sentiment_data"][k]
        b = ai_data["bias_distribution"][k]
        lines.append(
            f"- {k}: Latest Concall Mgmt FinBERT {s['mgmt_finbert'][-1]:+.2f} vs Q&A {s['qa_finbert'][-1]:+.2f} "
            f"(Llama Mgmt {s['mgmt_llama'][-1]:+.2f} vs Q&A {s['qa_llama'][-1]:+.2f}). "
            f"Headline framing: Hype {b['Hype / FOMO']:.0f}%, Extrapolation {b['Extrapolation']:.0f}%, "
            f"Loss Aversion {b['Loss Aversion']:.0f}%, Neutral {b['Neutral / Factual']:.0f}%."
        )
    v = ai_data["validation_benchmarks"]
    lines.append(
        f"- 90-Sentence Human Benchmark: Llama 3.1 8B Accuracy {v['llama_metrics']['accuracy']:.1f}% (kappa {v['llama_metrics']['cohens_kappa']:.3f}) "
        f"vs FinBERT Accuracy {v['finbert_metrics']['accuracy']:.1f}% (kappa {v['finbert_metrics']['cohens_kappa']:.3f})."
    )
    return "\n".join(lines)


SYSTEM_INSTRUCTIONS = """You are the Folio Strategic Analyst for an Indian equity security analysis and portfolio management terminal.
Rules:
1. Ground every single claim in the exact figures from the LIVE DATASET BRIEFING provided. Cite specific rupees, percentages, betas, Sharpe/Treynor/Jensen's Alpha/Information ratios, WACC, and questionnaire scores.
2. Never use emojis. Write in crisp, institutional investment-research prose with concise bullet points and clear subheadings.
3. Directly contrast narrative/sentiment (concall tone and headline framing) against fundamental cash flows and risk-adjusted portfolio math.
"""


def stream_ollama_chat(
    messages: list[dict],
    context_brief: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> Generator[str, None, None]:
    """Stream tokens from local Ollama /api/chat."""
    sys_msg = {"role": "system", "content": f"{SYSTEM_INSTRUCTIONS}\n\n=== LIVE DATASET BRIEFING ===\n{context_brief}"}
    payload = {
        "model": model,
        "messages": [sys_msg] + messages,
        "stream": True,
        "options": {"temperature": temperature, "num_predict": 700},
    }
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        for raw_line in resp:
            if not raw_line:
                continue
            obj = json.loads(raw_line.decode("utf-8"))
            chunk = obj.get("message", {}).get("content", "")
            if chunk:
                yield chunk
            if obj.get("done"):
                break


def analyze_custom_text_ollama(
    text: str,
    company: str,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Classify a custom concall sentence or news headline via local Ollama into JSON."""
    prompt = (
        f"Analyze the following corporate statement or news headline for {company} (Indian NSE-listed company).\n"
        f"Text: \"{text}\"\n\n"
        "Respond ONLY with a valid JSON object containing exactly these keys:\n"
        '{"sentiment_label": "Positive" | "Neutral" | "Negative", '
        '"sentiment_score": float between -1.0 and 1.0, '
        '"behavioral_frame": "Hype / FOMO" | "Extrapolation" | "Loss Aversion" | "Neutral / Factual", '
        '"rationale": "One concise institutional sentence explaining the score and any corporate euphemism."}'
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 220},
    }
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    raw = out.get("response", "{}")
    return json.loads(raw)


PRESET_QUESTIONS = [
    (
        "Thesis Synthesis: Narrative vs. Numbers",
        "Synthesize how the Narrative vs. Numbers thesis plays out across Trent, Asian Paints, and TCS using our DCF intrinsic values, relative multiples, concall sentiment gaps, and headline bias shares.",
    ),
    (
        "Why MVO Favors Asian Paints & TCS Over Trent",
        "Explain why the forward-looking Mean-Variance Optimization allocates roughly 49.5% to Asian Paints and 39.4% to TCS while capping Trent at 11.1%, contrasting historical Sharpe/Alpha against forward CAPM risk-return.",
    ),
    (
        "Audit the 4 Performance Ratios",
        "Compare Trent, Asian Paints, TCS, the Equal-Weight portfolio, and the Tangency portfolio across Sharpe ratio, Treynor ratio, Jensen's alpha, and Information ratio. What does the Equal-Weight vs Nifty 50 comparison prove?",
    ),
    (
        "Evaluate Active Investor Profile & Prudence Rule",
        "Evaluate the current investor questionnaire profile (Section A vs Section B, Prudence Rule status, risk aversion A, basket, and equity/T-bill split) and recommend how their allocation should evolve along the 20-year SIP glide path.",
    ),
    (
        "Reverse-DCF & Valuation Stress Test",
        "Critique the DCF assumptions for Trent, Asian Paints, and TCS. Why are all three DCF intrinsic values below current market prices, and where do peer multiples and own 5-year history place each stock?",
    ),
]
