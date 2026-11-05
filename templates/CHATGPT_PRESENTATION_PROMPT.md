# Prompt for ChatGPT — SAPM Group 10 Presentation

## Files to attach before sending (ChatGPT can't read local paths, so upload these)

| # | File | Local path | Role |
|---|------|-----------|------|
| 1 | Black Red Simple Modern Stock Market Presentation.pptx | `/Users/tejassampathkumar/Desktop/SA/templates/Black Red Simple Modern Stock Market Presentation.pptx` | **Main template (edit this file directly)** |
| 2 | Black Red Simple Modern Stock Market Presentation.pdf | `/Users/tejassampathkumar/Desktop/SA/templates/Black Red Simple Modern Stock Market Presentation.pdf` | Visual reference for the main template |
| 3 | Green and Red Dynamic Stock Market Presentation.pptx | `/Users/tejassampathkumar/Desktop/SA/templates/Green and Red Dynamic Stock Market Presentation.pptx` | Secondary template (borrow graphs/images/elements only) |
| 4 | Green and Red Dynamic Stock Market Presentation.pdf | `/Users/tejassampathkumar/Desktop/SA/templates/Green and Red Dynamic Stock Market Presentation.pdf` | Visual reference for the secondary template |
| 5 | sa_v1.docx | `/Users/tejassampathkumar/Desktop/SA/sa_v1.docx` | **Final report: where the content and numbers come from** |
| 6 | SA_final_workbook_master.xlsx | `/Users/tejassampathkumar/Desktop/SA/SA_final_workbook_master.xlsx` | Audited numbers and chart data |
| 7 | chart_*.png (7 files) | `/Users/tejassampathkumar/Desktop/SA/templates/charts/` | Optional ready-made dark charts |
| 8 | Previous draft deck (optional) | `/Users/tejassampathkumar/Desktop/SA/06_deliverables/Security_Analysis_Presentation.pptx` | Layout reference only. **Don't copy its numbers** |

---

## PROMPT (copy everything below this line)

You're building a final group presentation for a university course. I've attached these files:

1. **`Black Red Simple Modern Stock Market Presentation.pptx`** (+ its PDF): this is the MAIN TEMPLATE. Edit this file directly and keep its exact look.
2. **`Green and Red Dynamic Stock Market Presentation.pptx`** (+ its PDF): a SECONDARY template. Only borrow graph styles, image elements, icons and decorative graphics from it, restyled to match the main template.
3. **`sa_v1.docx`**: our final report. This is the source of truth for all content.
4. **`SA_final_workbook_master.xlsx`**: our audited Excel workbook. Take all numbers and chart data from here.
5. **`chart_*.png`** (7 images): dark-themed charts already made in the template palette. Use them, or rebuild them as native PowerPoint charts if you can match the style.

### Course and team details (put these on the cover slide exactly as written)
- **Project title:** Narrative vs. Numbers: An AI-Augmented Security Analysis of Trent, Asian Paints & TCS, with a Lifecycle Portfolio Built on Utility-Based Allocation
- **Course:** Security Analysis & Portfolio Management (SAPM)
- **Faculty:** Prof. Jagriti Bhattacharyya
- **Group members:**
  - 246213022 – Tejas Sampathkumar
  - 246213682 – Renee Gupta
  - 246213110 – Faizan Ali Siddiqui
  - 246213296 – Sure Manikanta
  - 246213434 – Ojasvi Paliwal
- **Live dashboard link (closing slide):** https://folio-security-analysis.streamlit.app

### Design rules (strict: do not deviate from the template's format)
- Use the Black Red Simple Modern template as the base. Keep its slide size (20" × 11.25"), pure black background, white text, red accent (#FF1E27), grey card borders, background grid lines, rounded cards, pill badges, top header bar and candlestick graphics.
- **Fonts:** match the template exactly. That means **Poppins** (Bold for titles, Medium/Regular for body, Light/Light Italic for captions). Don't bring in any other font.
- Replace every placeholder ("Northline Group", "Lorem ipsum", "www.reallygreatsite.com", "Menu" and so on) with real content. Put "SAPM Group 10" in the top-left header slot.
- Reuse the template's existing slide layouts and fit content into the existing cards. Don't invent new layouts.
- Size and space everything properly. No overlapping text or images, no text spilling outside its card, keep consistent margins, and keep body text at 12pt or larger so it's readable.
- Include **proper graphs** on the content slides: correlation heatmap, valuation football-field, sentiment trajectory, bias breakdown, efficient frontier + CAL, 20-year SIP glide path, and cumulative wealth backtest. Native editable PowerPoint charts are preferred. Use the attached PNGs where a native chart isn't practical.
- Borrow images/graphic elements from the Green and Red template where they help, recoloured to black/red/white.

### Content rules
- **Don't include per-stock deep-dive slides or individual buy/sell/hold recommendations.**
- Include only **ONE small section** on overall portfolio performance (portfolio vs Nifty 50 vs T-Bill).
- Organise the slides around the **grading rubric** so the flow is clear:
  1. Company Selection & Diversification (10 marks)
  2. AI-Augmented Analysis: concall NLP + headline behavioural bias (10 marks)
  3. Theory & Creativity: valuation framework, CAPM/WACC, utility theory (10 marks)
  4. Portfolio Construction: tangency portfolio, three investor baskets, 20-year SIP glide path (10 marks)
  5. Presentation (10 marks): clarity, cohesion, synthesis

### Suggested 10-slide flow (matches the template's 10 slides)
1. **Cover:** title, team, faculty
2. **Agenda / Project architecture:** the rubric criteria
3. **Company selection & diversification:** three archetypes (Trent = hype/momentum, Asian Paints = de-rating, TCS = fear vs fundamentals) + correlation heatmap
4. **Traditional valuation & quality audit:** two-stage FCFF DCF, relative valuation, CFO/PAT earnings quality, Ind AS 116 lease note + football-field chart (keep it framework-level, not stock pitches)
5. **AI concall NLP:** FinBERT vs local Llama 3.1 across 24 transcripts, validated on a 90-sentence human gold standard + sentiment chart
6. **Behavioural bias lab:** 150 headlines classified for framing/bias + bias chart
7. **Portfolio theory & utility:** efficient frontier, CAL, tangency weights, U = E(R) − ½·A·σ², risk questionnaire → A, Prudence Rule, three baskets
8. **20-year SIP lifecycle glide path:** Monte Carlo glide path chart
9. **Overall portfolio performance (the one small section):** Sharpe, Treynor, Jensen's alpha, Information Ratio vs Nifty 50 + wealth backtest chart
10. **Conclusion / Thank you:** 3–4 key takeaways + dashboard link

### Key audited numbers (check each one against the workbook/report and use the workbook value if they differ)
- Risk-free: 10Y G-Sec 7.473% (CAPM/DCF); 91-day T-Bill 6.80% (cash leg of portfolios). ERP 7.08%, terminal g 5.00%.
- WACC: Trent 18.34%, Asian Paints 15.06%, TCS 15.20%. 5Y CFO/PAT: 1.19x / 1.11x / 1.01x.
- Asian Paints vs TCS return correlation: 0.185.
- Tangency portfolio: Asian Paints 49.5%, TCS 39.4%, Trent 11.1%; forward E[Rp] 15.62%, σp 21.21%, Sharpe 0.42.
- Baskets: Aggressive A = 2.2 → 89.1% equity / 10.9% T-Bill; Balanced A = 4.9 → 40% / 60%; Defensive A = 8.5 → 23.1% / 76.9%.
- Risk aversion: A = 10 − 0.3 × (R_used − 10), from a 10-question questionnaire (R ∈ [10, 40]). Prudence Rule: if |Sec A − Sec B| ≥ 6, then R_used = 2 × min(Sec A, Sec B).
- 5Y performance (Oct 2021 – Oct 2026), Equal-Weight portfolio: Sharpe +0.12, Treynor +2.10%, Jensen's α +4.63%, Information Ratio +0.25; Nifty 50 Sharpe −0.09.
- Wealth backtest: ₹1.00L → ₹1.64L (equal-weight) vs ₹1.35L (Nifty 50) vs ₹1.39L (91D T-Bill).
- 20-year SIP: about ₹1.05 Cr invested → about ₹2.18 Cr expected corpus.

**Don't make up any statistic.** If a number isn't in the report or workbook, leave it out.

### Deliverables
1. The finished **.pptx**, built on the main template file with all original graphics kept.
2. **Speaker notes** on every slide (about 60–75 seconds each, 10–12 minutes in total), split between the 5 members.
3. A short list of anything you couldn't match exactly (fonts, graphics) so I can fix it in Canva/PowerPoint.

Before building, briefly confirm the slide-by-slide plan. Then produce the file.
