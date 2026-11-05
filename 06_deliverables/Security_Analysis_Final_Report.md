# SECURITY ANALYSIS PROJECT REPORT

## Narrative vs. Numbers: Security Analysis of Trent, Asian Paints and TCS

**SUBJECT:** Security Analysis  
**GROUP:** Group 10  
**SUBMITTED TO:** Prof. Jagriti Bhattacharyya  

**Group Members:**
- Tejas Sampathkumar — 246213022
- Renee Gupta — 246213682
- Faizan Ali Siddiqui — 246213110
- Sure Manikanta — 246213296
- Ojasvi Paliwal — 246213434

---

## Summary
In this project we looked at three Indian stocks, Trent, Asian Paints and TCS, in three ways. First the usual financial valuation work: ratios, DCF models, peer comparisons and cash flow checks. Second, we ran earnings call transcripts through AI models to see what the market is saying versus what the numbers show. Third, we built a portfolio using a utility-based allocation model and put it in a Streamlit dashboard so we could play around with different investment scenarios.

---

## What we wanted to find out
Our main question was simple: where does market sentiment drift away from what a stock is actually worth in India, can we measure that gap using NLP, and can we use it to build a better portfolio?

We picked three companies that each show a different kind of gap:
- **Trent (hype and momentum):** The stock trades at a P/E of 94.1x and EV/EBITDA of 43.8x. The market is basically pricing in perfect growth for Zudio and Westside, and that is far ahead of what the discounted cash flows support.
- **Asian Paints (de-rating):** It has been the market leader for years, but its P/E has slipped from a 5-year median of 61.2x to 54.1x, while sector peers sit at 31.1x. The reason is tough price competition from Grasim's Birla Opus.
- **TCS (fear vs. fundamentals):** Its P/E is down at 18.4x because investors worry Generative AI will hurt traditional IT services. But the company makes a lot of cash: ₹72,398 Cr EBITDA, a CFO/PAT of 1.01x and ROCE above 45%.

---

## The three companies and their role in the portfolio
- **Trent Ltd. (TRENT.NS):** Fast fashion and apparel retailer. Market cap is ₹1,61,880 Cr and the price is ₹3,036. Its 5-year beta against the Nifty 50 is 1.83 (raw) or 1.56 (Blume-adjusted), and annualized volatility is 43.14%, which is high. We treat it as the high-beta growth driver.
- **Asian Paints Ltd. (ASIANPAINT.NS):** Makes decorative paints and coatings. Market cap is ₹2,33,853 Cr and the price is ₹2,438. Beta is 1.14 raw or 1.10 Blume, and volatility is 25.71%, which is moderate. We treat it as a low-correlation defensive anchor.
- **Tata Consultancy Services (TCS.NS):** Enterprise IT and cloud services. Market cap is ₹9,04,163 Cr and the price is ₹2,499. Beta is 1.15 raw or 1.10 Blume, and volatility is 28.45%, also moderate. We treat it as a cash-generating dividend anchor.

---

## Who we left out and why
- **ITC:** Tobacco tax distortions, the hotel de-merger and ESG filters would mess up the sentiment tracking.
- **HUL and Nestle India:** Their customer base overlaps too much with Asian Paints and Trent.
- **Cummins India and L&T:** Capital goods depend a lot on government spending cycles, not consumer trends or tech shifts.
- **Coal India:** State ownership and regulated pricing block out natural sentiment signals.

---

## Do these stocks actually diversify each other?
We used 60 months of return data (Oct 2021 to Oct 2026) and built a correlation matrix.

| Asset / Index | TRENT | ASIANPAINT | TCS | NIFTY 50 |
|---|---|---|---|---|
| **TRENT** | 1.000 | 0.403 | 0.350 | 0.571 |
| **ASIANPAINT** | 0.403 | 1.000 | 0.185 | 0.598 |
| **TCS** | 0.350 | 0.185 | 1.000 | 0.544 |
| **NIFTY 50** | 0.571 | 0.598 | 0.544 | 1.000 |

Asian Paints and TCS are barely correlated (0.185), and Trent and TCS sit at 0.350. Putting them together brings down the overall risk of the portfolio.

---

## How the business performed over 5 years (FY22 to FY26)
- **Trent:** Revenue went from ₹4,498.02 Cr to ₹20,074.21 Cr, a 45.3% CAGR. EBITDA margin improved from 13.2% to 18.7% as private labels scaled up. Cumulative 5-year CFO/PAT is a healthy 1.19x.
- **Asian Paints:** Revenue grew from ₹29,101.28 Cr to ₹35,583.54 Cr, only a 5.2% CAGR. EBITDA margin bounced between 16.5% and 21.2% because of raw material costs and the discounting needed to fight Birla Opus. CFO/PAT is 1.11x.
- **TCS:** Revenue grew from ₹1,91,754 Cr to ₹2,67,021 Cr, an 8.6% CAGR, with EBITDA margin staying around 26.5% to 27.7% (₹72,398 Cr in FY26). The 5-year CFO/PAT is 1.01x, so cash flow has stayed strong.

---

## DCF valuation
We used standard Indian benchmark inputs, a risk-free rate of 7.473% (10Y G-Sec), an equity risk premium of 7.08%, a tax rate of 25.17%, Blume-adjusted betas and a fairly conservative terminal growth rate of 5.00%.

| Valuation Parameter | Trent (10Y Stage 1) | Asian Paints (5Y Stage 1) | TCS (5Y Stage 1) |
|---|---|---|---|
| **Blume beta** | 1.5592 | 1.0966 | 1.1026 |
| **Cost of equity** | 18.51% | 15.24% | 15.28% |
| **After-tax cost of debt** | 7.26% | 4.70% | 8.88% |
| **WACC** | 18.34% | 15.06% | 15.20% |
| **Stage 1 PV of cash flows** | ₹6,176.54 Cr | ₹12,710.27 Cr | ₹1,71,732.69 Cr |
| **Stage 2 PV (terminal value)** | ₹6,958.10 Cr | ₹25,200.01 Cr | ₹3,25,281.01 Cr |
| **Enterprise value** | ₹13,134.63 Cr | ₹37,910.29 Cr | ₹4,97,013.70 Cr |
| **Less: borrowings and leases** | ₹(2,561.25) Cr | ₹(3,928.93) Cr | ₹(11,283.00) Cr |
| **Plus: cash and investments** | ₹1,667.91 Cr | ₹8,135.42 Cr | ₹46,896.00 Cr |
| **Implied equity value** | ₹12,241.29 Cr | ₹42,116.78 Cr | ₹5,32,626.70 Cr |
| **Diluted shares** | 53.32 Cr | 95.92 Cr | 361.81 Cr |
| **DCF value per share** | ₹229.58 | ₹439.08 | ₹1,472.12 |
| **Current market price** | ₹3,036.00 | ₹2,438.00 | ₹2,499.00 |
| **Verdict** | Overvalued (-92.4%) | Overvalued (-82.0%) | Overvalued (-41.1%) |

---

## What the sensitivity tests showed
- **Trent:** At a WACC of 18.34% and Terminal growth of 5.0%, fair value comes out at ₹229.58. To justify ₹3,036, Trent would need to keep growing 30% or more every year for well over a decade.
- **Asian Paints:** Base value is ₹439.08, and it ranges from ₹380.89 to ₹525.64 across the scenarios we tested.
- **TCS:** Base value is ₹1,472.12, ranging from ₹1,274.18 to ₹1,764.73.

---

## Relative valuation and earnings quality
Here we used a 50/50 blend of P/E and EV/EBITDA, once with peer multiples and once with each company's own history.
- **Trent:** Peers (average 40.6x P/E) point to ₹1,540.75. Its own 5-year history (average 109.9x P/E) points to ₹4,132.13.
- **Asian Paints:** Peers (31.1x P/E) point to ₹1,375.48. Its own history (median 61.2x P/E) points to ₹2,679.70.
- **TCS:** Peers (industry average 18.3x P/E) point to ₹2,467.90, and its own history points to ₹3,869.93. TCS trades almost exactly in line with its sector.

### Are the profits real?
All three companies had CFO/PAT above 1.0 in every one of the 5 years (Trent 1.19x, Asian Paints 1.11x, TCS 1.01x). So the reported profits are backed by real cash.

A few adjustments and notes on the data:
- Trent's ₹2,561 Cr of debt is mostly store leases under Ind AS 116, not bank loans.
- We adjusted for Trent's 3:2 stock split in early 2026 so the price history stays clean.
- Asian Paints has ₹2,290 Cr of contingent liabilities and is facing a CCI inquiry.
- TCS has no financial debt.

---

## AI sentiment and media framing
We ran 24 earnings call transcripts (FY25 Q1 to FY26 Q4) through two models: ProsusAI FinBERT and a local Llama 3.1 8B.

### What the sentiment showed
- **Trent:** Management stayed very upbeat (+0.70), but analyst questions dropped to +0.44 as people started worrying about slowing same-store sales.
- **Asian Paints:** Analyst Q&A sentiment fell hard, from +0.28 to -0.32, as price cuts and dealer discounts started hurting profits.
- **TCS:** Prepared remarks stayed positive (+0.38), but analysts were more cautious (+0.10) because of GenAI worries.

### Which model was better?
We checked both models against human scoring on 90 sentences.

| Model | Accuracy | Macro-F1 | Cohen's kappa | What we saw |
|---|---|---|---|---|
| **FinBERT** | 82.2% | 0.814 | 0.732 | Good overall, but misread some Indian management phrasing |
| **Llama 3.1 8B** | 88.9% | 0.885 | 0.829 | Understood context better and caught subtle shifts in tone |

For example, FinBERT scored "selective price calibration" as positive (+0.34). Llama 3.1 correctly read it as defensive price cuts (-0.42), which matched the human score.

### How the media framed each company
We looked at 150 news headlines:
- **Trent (54% hype/FOMO):** Coverage was mostly about aggressive store additions and stock momentum, which feeds into the 94.1x P/E.
- **Asian Paints (58% extrapolation bias):** Headlines focused on short-term price competition and assumed it would permanently damage the company's distribution strength.
- **TCS (52% fear framing):** Media focused on GenAI replacing IT services and mostly ignored the strong cash generation and contract wins.

---

## Building the portfolio
We used forward-looking CAPM returns (Trent 18.51%, Asian Paints 15.24%, TCS 15.28%) with a 70% cap on any single stock. Mean-variance optimization gave us the tangency portfolio:
- **Trent:** 11.1%. Kept low because of its 43.14% volatility.
- **Asian Paints:** 49.5%. Gets a high weight because it has low correlation with TCS.
- **TCS:** 39.4%. Gets a high weight because of its stable cash flows and lower risk.

The portfolio's expected return is 15.62%, volatility is 21.21% and Sharpe ratio is +0.42.

### Allocation by risk profile
| Profile | Risk score | Risk aversion (A) | Equity | Cash/T-bills | Final split |
|---|---|---|---|---|---|
| **Aggressive** | 32 to 40 | 2.2 | 89.1% | 10.9% | Trent 9.9%, Asian Paints 44.1%, TCS 35.1%, T-bills 10.9% |
| **Balanced** | 22 to 31 | 4.9 | 40.0% | 60.0% | Trent 4.4%, Asian Paints 19.8%, TCS 15.7%, T-bills 60.0% |
| **Defensive** | 10 to 21 | 8.5 | 23.1% | 76.9% | Trent 2.6%, Asian Paints 11.4%, TCS 9.1%, T-bills 76.9% |

---

## 20-year lifecycle glide path
This assumes a starting SIP of ₹25,000 a month with a 10% step-up each year.
- **Years 1 to 7 (age 26 to 32):** 100% equity (aggressive). About ₹28.46 L invested, expected value ₹47.02 L.
- **Years 8 to 15 (age 33 to 40):** 65% equity and 35% debt (balanced). Total invested ₹73.44 L, expected value ₹1.34 Cr.
- **Years 16 to 20 (age 41 to 45):** 35% equity and 65% debt (defensive). Total invested ₹1.05 Cr, projected target ₹2.18 Cr.

---

## 5-year backtest (Oct 2021 to Oct 2026)
| Metric | Trent | Asian Paints | TCS | Equal-weight (3 stocks) | Nifty 50 |
|---|---|---|---|---|---|
| **Annualized return** | 31.92% | -1.64% | 0.83% | 10.37% | 6.22% |
| **Annualized volatility** | 43.14% | 25.71% | 28.45% | 24.39% | 13.43% |
| **Beta vs Nifty** | 1.83 | 1.14 | 1.15 | 1.38 | 1.00 |
| **Sharpe ratio** | +0.57 | -0.35 | -0.23 | +0.12 | -0.09 |
| **Jensen's alpha** | +26.75% | -7.68% | -5.20% | +4.63% | 0.00% |
| **Information ratio** | +0.69 | -0.38 | -0.22 | +0.25 | 0.00 |

The simple equal-weight mix gave an alpha of +4.63% a year and an information ratio of +0.25 over the Nifty 50. Holding sector leaders that don't move together helps cover the downside of each stock.

---

## Final verdict (portfolio)
**Verdict: ACCUMULATE IN STAGES.** We back the three stocks as one diversified portfolio, weighted Asian Paints 49.5%, TCS 39.4% and Trent 11.1%, with the equity share set by the investor’s risk profile.

### Why we back the portfolio
1. **Diversification works:** Correlations between the stocks are only 0.185 to 0.403, so the optimised portfolio’s volatility (21.21%) is lower than every single stock (25.71% to 43.14%).
2. **Better return for the risk taken:** Expected return is 15.62% with a Sharpe ratio of +0.42. In the 5-year backtest even the simple equal-weight mix beat the Nifty 50: 10.37% vs 6.22% a year, alpha +4.63%, information ratio +0.25 and Sharpe +0.12 vs -0.09.
3. **Risk is controlled by position size:** Trent is the only stock priced for perfection (94.1x P/E, DCF value ₹229.58 vs price ₹3,036), so the model caps it at 11.1%. It still adds some of the growth (31.92% backtest return) without letting its 43.14% volatility drive the portfolio.
4. **About 89% sits in cash-backed businesses:** Asian Paints and TCS together make up 88.9%. All three stocks had CFO/PAT above 1.0x in every one of the 5 years, and TCS has no financial debt.
5. **Sentiment gives an entry point:** Analyst and media tone on the two core holdings looks harsher than their cash flows justify (Asian Paints analyst Q&A at -0.32, 58% extrapolation bias; TCS 52% fear framing). Trent’s coverage is 54% hype, which is another reason to keep it small.

### How to act on it
- **Match equity to risk profile:** Aggressive (score 32 to 40): 89.1% equity and 10.9% T-bills. Balanced (22 to 31): 40.0% and 60.0%. Defensive (10 to 21): 23.1% and 76.9%. Inside the equity part, keep the same 11.1 / 49.5 / 39.4 mix.
- **Build through a monthly SIP, not a lump sum:** Start at ₹25,000 a month with a 10% yearly step-up, and follow the glide path from 100% equity to 65% and then 35% over 20 years.
- **Rebalance once a year:** Trim Trent if it drifts well above its 11.1% target, and top up Asian Paints and TCS on dips.

### What could go wrong
- **Valuation:** The DCF puts all three stocks above intrinsic value (-92.4%, -82.0% and -41.1%). This is why we stage the entry. The verdict rests mainly on relative valuation, diversification and cash quality.
- **Market risk:** The equal-weight mix has a beta of 1.38, so it will fall harder than the Nifty 50 in a broad sell-off.
- **Limited evidence:** Only three stocks in three sectors, and the backtest covers one 5-year window and tested the equal-weight mix, not the optimised weights.
- **Stock-specific risks:** Birla Opus price war and the CCI inquiry (Asian Paints), GenAI disruption (TCS) and slowing same-store sales (Trent).
