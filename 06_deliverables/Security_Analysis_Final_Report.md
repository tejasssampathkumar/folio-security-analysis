# Narrative vs. Numbers: An AI-Augmented Security Analysis of Trent, Asian Paints and TCS, with a Lifecycle Portfolio Built on Utility-Based Allocation

**Course:** Security Analysis & Portfolio Management (SAPM) | **Faculty:** Prof. Jagriti  
**Valuation Cutoff Date:** November 3, 2026 | **Risk-Free Benchmarks:** 91-Day RBI T-Bill (6.80% p.a.) & 10-Year Benchmark G-Sec (7.473% p.a.) | **India ERP:** 7.08%  
**Interactive Terminal:** **Folio (`F.`)** Dynamic Streamlit & Ollama LLM Terminal (`http://localhost:8502`)

---

## PAGE 1: COMPANY SELECTION, CENTRAL THESIS & DIVERSIFICATION RATIONALE

### 1.1 Central Research Question & Core Thesis
Where does market sentiment diverge from fundamental valuation in Indian listed equities, and can that divergence be empirically measured, validated with natural language processing (NLP), and used to construct a utility-optimizing lifecycle portfolio?

We examine three distinct market archetypes:
1. **Trent Ltd. (Hype / Momentum Case):** A premium earnings multiple (P/E 94.1x, EV/EBITDA 43.8x) priced for flawless store rollout (Zudio/Westside) and continuous operating leverage, running substantially ahead of discounted cash flow fundamentals.
2. **Asian Paints Ltd. (De-Rating Case):** A 50-year market leader experiencing aggressive multiple contraction (P/E de-rated from 5Y median of 61.2x to 54.1x; peer comps at 31.1x) following the aggressive market entry and price-war discounting of Grasim's Birla Opus.
3. **Tata Consultancy Services Ltd. (Fear vs. Fundamentals Case):** P/E depressed to 18.4x by pervasive investor anxiety over Generative AI disrupting IT maintenance and coding work, despite exceptional cash generation (Rs 72,398 Cr EBITDA, 1.01x 5Y CFO/PAT conversion, and >45% ROCE).

Together, these archetypes represent sentiment running **ahead of**, **behind**, and **in conflict with** corporate fundamentals.

### 1.2 Company Snapshot & Structural Roles
| Metric / Parameter | Trent Ltd. (`TRENT.NS`) | Asian Paints Ltd. (`ASIANPAINT.NS`) | Tata Consultancy Services (`TCS.NS`) |
| :--- | :--- | :--- | :--- |
| **Primary Industry** | Apparel & Fast Fashion Retail | Decorative Paints & Coatings | Enterprise IT Services & Cloud |
| **Market Capitalization** | Rs 1,61,880 Cr | Rs 2,33,853 Cr | Rs 9,04,163 Cr |
| **Current Market Price (CMP)** | Rs 3,036.00 | Rs 2,438.00 | Rs 2,499.00 |
| **5-Year Beta vs. Nifty 50** | **1.83** (Raw) / **1.56** (Blume) | **1.14** (Raw) / **1.10** (Blume) | **1.15** (Raw) / **1.10** (Blume) |
| **Annualized Volatility (5Y)** | **43.14%** (High Volatility) | **25.71%** (Moderate) | **28.45%** (Moderate) |
| **Role in Portfolio** | High-beta capital appreciation engine | Low-correlation defensive quality anchor | Low-capex, high-cash dividend yield ballast |

### 1.3 Alternatives Considered and Formally Rejected
* **ITC Ltd.:** Rejected due to conglomerate tax distortion (tobacco excise duties), ongoing hotel de-merger complexities, and ESG institutional discounts, which confound pure sentiment modeling.
* **Hindustan Unilever (HUL) & Nestle India:** Rejected due to excessive demand overlap with Asian Paints and Trent in urban middle-class consumer staples.
* **Cummins India & L&T:** Rejected because capital goods cycles are heavily dependent on government capex announcements rather than retail consumer sentiment or technological disruption narratives.
* **Coal India:** Rejected due to dominant sovereign ownership and regulated pricing, which mutes market sentiment transmission.

### 1.4 Empirical Sector Diversification Proof (5-Year Monthly Correlation Matrix)
Rather than assuming diversification, we compute the 60-month return correlation matrix (Oct 2021 – Oct 2026) from `SA_final_workbook.xlsx`:
$$\begin{pmatrix} & \text{TRENT} & \text{ASIANPAINT} & \text{TCS} & \text{NIFTY 50} \\ \text{TRENT} & 1.000 & 0.403 & 0.350 & 0.571 \\ \text{ASIANPAINT} & 0.403 & 1.000 & 0.185 & 0.598 \\ \text{TCS} & 0.350 & 0.185 & 1.000 & 0.544 \\ \text{NIFTY 50} & 0.571 & 0.598 & 0.544 & 1.000 \end{pmatrix}$$
*Cross-asset correlations between Asian Paints and TCS are exceptionally low ($0.185$), while Trent-TCS is $0.350$. This mathematically guarantees portfolio variance reduction when blended.*

---

## PAGE 2: TRADITIONAL VALUATION & EARNINGS QUALITY REVIEW

### 2.1 Five-Year Historical Financial Performance (FY22 – FY26)
* **Trent Ltd.:** Revenue grew from Rs 4,498.02 Cr (FY22) to Rs 20,074.21 Cr (FY26) at a 45.3% CAGR. EBITDA margin expanded from 12.76% to 18.73%, driven by private-label gross margins and operating leverage in Zudio. 5-year cumulative CFO/PAT conversion stands at 1.19x.
* **Asian Paints:** Revenue grew from Rs 29,101.28 Cr (FY22) to Rs 35,583.54 Cr (FY26) at a 5.2% CAGR. EBITDA margins ranged between 16.5% and 21.2% amidst raw material volatility (titanium dioxide/crude derivatives) and dealer discounting to defend market share against Grasim Birla Opus. 5-year cumulative CFO/PAT conversion is 1.11x.
* **TCS:** Revenue expanded from Rs 1,91,754 Cr (FY22) to Rs 2,67,021 Cr (FY26) at a 8.6% CAGR with industry-leading EBITDA margins maintained at 26.5%–27.7% (Rs 72,398 Cr FY26 EBITDA). Free cash flow conversion remained resilient with 5-year cumulative CFO/PAT at 1.01x, requiring minimal capex reinvestment to sustain organic growth.

### 2.2 Two-Stage FCFF Discounted Cash Flow (DCF) Valuation Model
Parameters anchored to sovereign benchmarks in `SA_final_workbook.xlsx`: Risk-Free Rate $R_f = 7.473\%$ (10Y G-Sec), Equity Risk Premium $ERP = 7.08\%$, Statutory Corporate Tax Rate $t = 25.17\%$, Blume Beta adjustment weight $0.67$, and Terminal Growth Rate $g = 5.00\%$ (anchored below long-run nominal Indian GDP growth).

| Valuation Parameter | Trent Ltd. (10Y Stage 1) | Asian Paints Ltd. (5Y Stage 1) | Tata Consultancy Services (5Y Stage 1) |
| :--- | :---: | :---: | :---: |
| **Blume-Adjusted Beta ($\beta$)** | 1.5592 | 1.0966 | 1.1026 |
| **Cost of Equity ($K_e$)** | 18.51% | 15.24% | 15.28% |
| **Pre-Tax Cost of Debt ($K_d$)** | 9.70% (Lease-dominated) | 6.28% | 11.87% (Lease interest) |
| **After-Tax Cost of Debt ($K_d(1-t)$)** | 7.26% | 4.70% | 8.88% |
| **Equity Weight ($E/V$)** | 98.44% | 98.35% | 98.77% |
| **Weighted Average Cost of Capital (WACC)** | **18.34%** | **15.06%** | **15.20%** |
| **Stage 1 (PV of Explicit FCFF)** | Rs 6,176.54 Cr (10Y) | Rs 12,710.27 Cr (5Y) | Rs 1,71,732.69 Cr (5Y) |
| **Stage 2 (PV of Terminal Value)** | Rs 6,958.10 Cr (52.98% of EV) | Rs 25,200.01 Cr (66.47% of EV) | Rs 3,25,281.01 Cr (65.45% of EV) |
| **Enterprise Value (EV)** | Rs 13,134.63 Cr | Rs 37,910.29 Cr | Rs 4,97,013.70 Cr |
| **Less: Total Borrowings & Leases** | Rs (2,561.25) Cr | Rs (3,928.93) Cr | Rs (11,283.00) Cr |
| **Plus: Cash & Marketable Investments** | Rs 1,667.91 Cr | Rs 8,135.42 Cr | Rs 46,896.00 Cr |
| **Implied Equity Value** | Rs 12,241.29 Cr | Rs 42,116.78 Cr | Rs 5,32,626.70 Cr |
| **Diluted Shares Outstanding** | 53.32 Cr | 95.92 Cr | 361.81 Cr |
| **DCF Intrinsic Value per Share** | **Rs 229.58** | **Rs 439.08** | **Rs 1,472.12** |
| **Current Market Price (CMP)** | **Rs 3,036.00** | **Rs 2,438.00** | **Rs 2,499.00** |
| **DCF Margin of Safety / Upside** | **-1,222.4% / -92.4% (Overvalued)** | **-455.2% / -82.0% (Overvalued)** | **-69.8% / -41.1% (Overvalued)** |

### 2.3 WACC $\times$ Terminal Growth ($g$) Sensitivity Matrices (Intrinsic Value in Rs)
* **Trent Ltd. (Base: Rs 229.58 at $WACC=18.34\%, g=5.0\%$):** Ranges from **Rs 195.86** ($WACC=19.34\%, g=4.0\%$) to **Rs 274.84** ($WACC=17.34\%, g=6.0\%$). Market price of Rs 3,036 requires sustaining >30% revenue growth well beyond a decade.
* **Asian Paints (Base: Rs 439.08 at $WACC=15.06\%, g=5.0\%$):** Ranges from **Rs 380.89** ($WACC=16.06\%, g=4.0\%$) to **Rs 525.64** ($WACC=14.06\%, g=6.0\%$).
* **TCS (Base: Rs 1,472.12 at $WACC=15.20\%, g=5.0\%$):** Ranges from **Rs 1,274.18** ($WACC=16.20\%, g=4.0\%$) to **Rs 1,764.73** ($WACC=14.20\%, g=6.0\%$).

### 2.4 Relative Valuation & Football-Field Synthesis (50/50 Blend of P/E & EV/EBITDA)
* **Trent Ltd.:** Peer-implied value is **Rs 1,540.75** (Peer median P/E 40.6x, EV/EBITDA 25.9x; `-97.0%` MoS); Own 5Y history implied value is **Rs 4,132.13** (5Y median P/E 109.9x, EV/EBITDA 67.8x; `+26.5%` MoS).
* **Asian Paints:** Peer-implied value is **Rs 1,375.48** (Peer median P/E 31.1x, EV/EBITDA 19.7x; `-77.2%` MoS); Own 5Y history implied value is **Rs 2,679.70** (5Y median P/E 61.2x, EV/EBITDA 37.6x; `+9.0%` MoS).
* **TCS:** Peer-implied value is **Rs 2,467.90** (Peer median P/E 18.3x, EV/EBITDA 12.2x; `-1.3%` MoS); Own 5Y history implied value is **Rs 3,869.93** (5Y median P/E 27.8x, EV/EBITDA 19.7x; `+35.4%` MoS). *TCS trades at exact parity with Indian IT peers.*

### 2.5 Earnings Quality, Footnote Review & Ind AS 116 Lease Liabilities
* **Earnings Quality Check (`earnings_quality` sheet):** 5-year cumulative CFO/PAT is **1.19x for Trent**, **1.11x for Asian Paints**, and **1.01x for TCS** (15/15 company-years pass `CFO/PAT > 0.80`), confirming that reported profits are backed by hard operating cash flow. Note: Beneish M-Score and DuPont decomposition are excluded by scope design.
* **Footnote & Data Hygiene Audit:** Trent's reported borrowings of Rs 2,561.25 Cr represent capitalized Ind AS 116 store lease liabilities across its Zudio/Westside network rather than bank debt. In the daily OHLCV market feed (`daily_market_data.csv`), an unadjusted 3:2 share split discontinuity on `2026-01-01` in `TRENT.NS` was detected and adjusted in `folio_core.py` so volatility and technical overlays remain distortion-free.

---

## PAGE 3: AI-AUGMENTED ANALYSIS, FOLIO (`F.`) TERMINAL & LIVE OLLAMA STRATEGIST

### 3.1 Dual-Model Concall NLP Pipeline (FinBERT vs. Local Ollama Llama 3.1 8B)
We pre-processed 24 earnings call transcripts across 8 quarters (FY25 Q1 to FY26 Q4), segmenting text into **Management Remarks** and **Analyst Q&A**, chunked into $\le 450$-token windows. Scoring applied ProsusAI FinBERT and local quantized Llama 3.1 8B (`llama3.1:latest` via Ollama).

```
Sentiment Trend Findings (Score scale: -1.0 to +1.0):
- Trent: Prepared Remarks (+0.70) outpaced Analyst Q&A (+0.44). The "Management Optimism Gap" widened in FY26 as analysts probed same-store-sales-growth (SSSG) moderation.
- Asian Paints: Sentiment plummeted from +0.28 (FY25 Q1) to -0.32 in Analyst Q&A by FY26 Q1 as Grasim Birla Opus rolled out dealer rebates.
- TCS: Stable sentiment spread (+0.38 Remarks vs +0.10 Q&A). Strong TCV announcements offset analyst queries regarding Generative AI billing rate pressures.
```

### 3.2 Human Gold-Standard Validation (90-Sentence Benchmark)
To verify AI outputs rigorously rather than trusting black-box scores, 30 concall sentences per company were blind-labeled by the group:
* **FinBERT:** Accuracy = **82.2%**, Macro-F1 = **0.814**, Cohen's Kappa $\kappa = \mathbf{0.732}$.
* **Local Llama 3.1 8B:** Accuracy = **88.9%**, Macro-F1 = **0.885**, Cohen's Kappa $\kappa = \mathbf{0.829}$.
* **Disagreement Insight:** FinBERT misclassified Indian management euphemisms (e.g. "selective price calibration" was scored as positive corporate action by FinBERT [+0.34], whereas Llama 3.1 correctly identified defensive price cuts [-0.42], matching the human gold standard).

### 3.3 Behavioral Bias & Media Framing Classification (150 Financial News Headlines)
We classified 50 recent headlines per company into 4 behavioral framing categories:
1. **Trent Ltd. — Hype / FOMO Framing (54.0%):** Media narratives focused overwhelmingly on store count milestones and "next multi-bagger" labels, propelling market valuation to 94.1x P/E, completely detached from DCF intrinsic value.
2. **Asian Paints Ltd. — Extrapolation Bias (58.0%):** Headlines linearly extrapolated short-term pricing pressure to imply permanent disruption of a 50-year distribution network, depressing sentiment below historical franchise value.
3. **TCS — Loss Aversion / Disruption Fear (52.0%):** Media coverage fixated on GenAI replacement risks, overlooking continuous deal ramp-ups and 1.01x cash conversion.

### 3.4 Folio (`F.`) Dynamic Terminal & Live Ollama AI Strategist
Rather than presenting static charts, we engineered **Folio (`F.`)** (`app.py`, `folio_core.py`, `folio_ai.py`) — a TradingView SPX-inspired interactive Streamlit terminal styled in Trade Gothic typography, bright off-white (`#F7F8FA`), institutional blue (`#2563EB`), and crimson red (`#DC2626`) with zero emojis:
* **Interactive Simulation:** Users dynamically stress-test DCF WACC/growth sliders, toggle 60M vs. Daily split-adjusted covariance matrices, answer the 10-question risk profiler, and run 1,000-path GBM price fans and 2,000-path Monte Carlo SIP simulations.
* **Live Ollama Co-Pilot (`05 / FOLIO AI STRATEGIST`):** Connected to local `llama3.1:latest` (`localhost:11434`), injecting real-time dashboard metrics (live DCF IV, portfolio weights, Sharpe/Treynor/Alpha/IR, and risk score $A$) into the system prompt for grounded institutional interrogation and live sentence/headline framing classification.

---

## PAGE 4: PORTFOLIO ALLOCATION, LIFECYCLE SIP & FINAL VERDICTS

### 4.1 Optimal Risky Portfolio (Mean-Variance Optimization via Forward-Looking Returns)
Using forward-looking CAPM expected returns ($E(R_{\text{Trent}})=18.51\%, E(R_{\text{AP}})=15.24\%, E(R_{\text{TCS}})=15.28\%$), MVO with a 70% single-asset ceiling yields the **Optimal Tangency Portfolio**:
* **Trent Ltd.: 11.1%** (Constrained by high 43.14% annualized volatility)
* **Asian Paints Ltd.: 49.5%** (High weight due to low correlation with TCS [$0.185$] and quality stability)
* **Tata Consultancy Services: 39.4%** (High weight due to defensive cash flow and moderate volatility)
* **Forward Tangency Performance (vs. 91D T-Bill 6.80%):** Expected Return = **15.62%** | Expected Volatility = **21.21%** | Forward Sharpe Ratio = **+0.42**

### 4.2 Investor Risk Profiling & Utility Allocation Formula
Scored via the 10-Question Questionnaire ($R \in [10, 40]$) with the **Prudence Rule** ($|\text{Sec A} - \text{Sec B}| \ge 6 \implies R_{\text{used}} = 2 \times \min(\text{Sec A}, \text{Sec B})$):
$$A = 10 - 0.3 \times (R_{\text{used}} - 10), \quad y^* = \min\left(1.0, \frac{E(R_p) - R_{f,\text{tbill}}}{A \cdot \sigma_p^2}\right)$$

| Investor Basket | Score Range ($R$) | Representative $R \rightarrow A$ | Equity Share ($y^*$) | 91D T-Bill Share | Detailed Asset Allocation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Aggressive Basket** | 32 to 40 | $R=36 \rightarrow A=2.2$ | **89.1%** | 10.9% | Trent 9.9%, Asian Paints 44.1%, TCS 35.1%, T-Bills 10.9% |
| **Balanced Basket** | 22 to 31 | $R=27 \rightarrow A=4.9$ | **40.0%** | 60.0% | Trent 4.4%, Asian Paints 19.8%, TCS 15.7%, T-Bills 60.0% |
| **Defensive Basket** | 10 to 21 | $R=15 \rightarrow A=8.5$ | **23.1%** | 76.9% | Trent 2.6%, Asian Paints 11.4%, TCS 9.1%, T-Bills 76.9% |

### 4.3 20-Year Monthly SIP Lifecycle Glide Path
Starting at Rs 25,000/month with a 10% annual step-up (`sip_lifecycle` sheet):
* **Years 1–7 (Age 26–32, Early Career):** Aggressive allocation (100% equity). Cumulative Invested = Rs 28.46 Lakhs $\rightarrow$ Expected Wealth = Rs 47.02 Lakhs.
* **Years 8–15 (Age 33–40, Mid Career):** Balanced allocation (65% equity / 35% T-Bills). Cumulative Invested = Rs 73.44 Lakhs $\rightarrow$ Expected Wealth = Rs 1.34 Crores.
* **Years 16–20 (Age 41–45, Capital Preservation):** Defensive allocation (35% equity / 65% T-Bills). Total Invested = Rs 1.05 Crores $\rightarrow$ **Projected Terminal Wealth = Rs 2.18 Crores**.

### 4.4 Five-Year Historical Backtest & Core Performance Metrics (`returns` sheet, Oct 2021 – Oct 2026)
| Metric | Trent Ltd. | Asian Paints | TCS Ltd. | Equal-Weight (3 Stocks) | Tangency Portfolio (5Y Hist.) | Nifty 50 Benchmark |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Annualized Return** | 31.92% | -1.64% | 0.83% | **10.37%** | 3.06% | 6.22% |
| **Annualized Volatility** | 43.14% | 25.71% | 28.45% | **24.39%** | 21.21% | 13.43% |
| **Beta vs. Nifty 50 ($\beta$)** | 1.83 | 1.14 | 1.15 | **1.38** | 1.22 | 1.00 |
| **Sharpe Ratio ($R_f=7.473\%$)** | **+0.57** | -0.35 | -0.23 | **+0.12** | -0.21 | -0.09 |
| **Treynor's Ratio** | **+13.33%** | -7.96% | -5.76% | **+2.10%** | -3.60% | -1.25% |
| **Jensen's Alpha ($\alpha$)** | **+26.75%** | -7.68% | -5.20% | **+4.63%** | -2.88% | 0.00% |
| **Tracking Error vs. Nifty** | 37.14% | 20.70% | 23.96% | **16.69%** | 13.74% | 0.00% |
| **Information Ratio** | **+0.69** | -0.38 | -0.22 | **+0.25** | -0.23 | 0.00 |

*The Equal-Weight 3-Stock Portfolio delivered +4.63% annual Jensen's Alpha, +2.10% Treynor's Ratio, +0.12 Sharpe Ratio, and +0.25 Information Ratio over Nifty 50, proving the benefit of combining non-correlated sector leaders.*

### 4.5 Final Investment Verdicts & Limitations
* **Trent Ltd. — AVOID / PROFIT BOOKING:** CMP (Rs 3,036) stands >1,200% above DCF intrinsic value (Rs 229.58) and 97% above peer multiples. AI sentiment confirms hyper-optimism running ahead of physical store unit economics.
* **Asian Paints Ltd. — ACCUMULATE ON DIPS:** Significant de-rating post Birla Opus has discounted excessive disruption fear; trades below its own 5Y historical multiple implied value (Rs 2,679.70) with 1.11x CFO/PAT conversion.
* **Tata Consultancy Services — ACCUMULATE / CORE HOLD:** Trading at exact parity with IT peer multiples (Rs 2,467.90 peer-implied vs Rs 2,499 CMP) and a 35.4% discount to its own 5Y history (Rs 3,869.93), with negative AI disruption sentiment masking 1.01x cash conversion.
* **Limitations:** Past 5-year returns do not guarantee future performance. DCF valuation is sensitive to WACC and terminal growth inputs. Sentiment models trained on corporate transcripts may exhibit management optimism bias.
