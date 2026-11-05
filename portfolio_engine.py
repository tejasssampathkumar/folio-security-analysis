"""
Portfolio Optimization, Utility Allocation & Lifecycle SIP Engine
Project: AI-Augmented Security Analysis of Trent, Asian Paints, and TCS
Based on: Risk_Aversion_Questionnaire.pdf and SA_final_workbook.xlsx
"""

import os
import json
import openpyxl
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. LOAD DATA FROM SA_final_workbook.xlsx
# -------------------------------------------------------------
WORKBOOK_PATH = '/Users/tejassampathkumar/Desktop/SA/SA_final_workbook.xlsx'
OUTPUT_DIR = '/Users/tejassampathkumar/Desktop/SA/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

wb = openpyxl.load_workbook(WORKBOOK_PATH, data_only=True)
ws_ret = wb['returns']
ws_assump = wb['assumptions']
ws_wacc = wb['wacc']
ws_sum = wb['summary']

# Risk-free rates
RF_LONG_TERM = float(ws_assump['B6'].value)  # 10Y G-Sec: 7.47% (for DCF & CAPM)
RF_SHORT_TERM = 0.0680  # 91-Day RBI T-Bill: ~6.80% (for cash/T-bill portfolio blending)

# Pull raw adjusted close prices from B, C, D, E (rows 5 to 65, 61 price observations)
months_all = [ws_ret.cell(r, 1).value for r in range(5, 66)]
p_trent = np.array([float(ws_ret.cell(r, 2).value) for r in range(5, 66)])
p_ap = np.array([float(ws_ret.cell(r, 3).value) for r in range(5, 66)])
p_tcs = np.array([float(ws_ret.cell(r, 4).value) for r in range(5, 66)])
p_nifty = np.array([float(ws_ret.cell(r, 5).value) for r in range(5, 66)])

# Compute 60 monthly returns: P_t / P_{t-1} - 1
months = months_all[1:]
ret_trent = (p_trent[1:] / p_trent[:-1]) - 1.0
ret_ap = (p_ap[1:] / p_ap[:-1]) - 1.0
ret_tcs = (p_tcs[1:] / p_tcs[:-1]) - 1.0
ret_nifty = (p_nifty[1:] / p_nifty[:-1]) - 1.0

df_returns = pd.DataFrame({
    'TRENT': ret_trent,
    'ASIANPAINT': ret_ap,
    'TCS': ret_tcs,
    'NIFTY': ret_nifty
}, index=months)

cov_monthly = df_returns[['TRENT', 'ASIANPAINT', 'TCS']].cov()
cov_annual = cov_monthly * 12

# Also extract Blume-adjusted betas or default to CAPM betas
ERP = 0.0708  # 7.08% Prof Damodaran India ERP
ke_trent = RF_LONG_TERM + 1.559 * ERP  # ~18.5%
ke_ap = RF_LONG_TERM + 1.097 * ERP     # ~15.2%
ke_tcs = RF_LONG_TERM + 1.103 * ERP    # ~15.3%

exp_returns = np.array([ke_trent, ke_ap, ke_tcs])  # [Trent, Asian Paints, TCS]
stock_names = ['TRENT', 'ASIANPAINT', 'TCS']

# -------------------------------------------------------------
# 3. MEAN-VARIANCE OPTIMIZATION (MVO TANGENCY PORTFOLIO)
# -------------------------------------------------------------
def neg_sharpe(weights, exp_ret, cov_mat, rf):
    p_ret = np.dot(weights, exp_ret)
    p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights)))
    return -(p_ret - rf) / p_vol

# Constraints: sum(w) = 1, 0 <= w <= 1 (no shorting, no leverage)
bounds = tuple((0.05, 0.70) for _ in range(3))  # Max 70% per stock, min 5% for diversification
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
init_guess = np.array([1/3, 1/3, 1/3])

opt_res = minimize(
    neg_sharpe,
    init_guess,
    args=(exp_returns, cov_annual.values, RF_SHORT_TERM),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

tangency_weights = opt_res.x
tangency_ret = np.dot(tangency_weights, exp_returns)
tangency_vol = np.sqrt(np.dot(tangency_weights.T, np.dot(cov_annual.values, tangency_weights)))
tangency_sharpe = (tangency_ret - RF_SHORT_TERM) / tangency_vol

# -------------------------------------------------------------
# 4. QUESTIONNAIRE SCORING & UTILITY-BASED ALLOCATION ENGINE
# -------------------------------------------------------------
def evaluate_risk_profile(answers_sec_a, answers_sec_b, apply_prudence=True):
    """
    Evaluates risk tolerance based on Risk_Aversion_Questionnaire.pdf
    answers_sec_a: list of 5 ints (1-4)
    answers_sec_b: list of 5 ints (1-4)
    """
    sub_a = sum(answers_sec_a)
    sub_b = sum(answers_sec_b)
    raw_r = sub_a + sub_b
    
    prudence_triggered = False
    if apply_prudence and abs(sub_a - sub_b) >= 6:
        r_used = 2 * min(sub_a, sub_b)
        prudence_triggered = True
    else:
        r_used = raw_r
        
    # Linear conversion: A = 10 - 0.3 * (R - 10)
    A = round(10.0 - 0.3 * (r_used - 10), 1)
    
    if r_used >= 32:
        basket = 'Aggressive'
    elif r_used >= 22:
        basket = 'Balanced'
    else:
        basket = 'Defensive'
        
    # Utility optimal equity share: y = (E(Rp) - Rf) / (A * sigma_p^2), capped at 1.0
    p_var = tangency_vol ** 2
    raw_y = (tangency_ret - RF_SHORT_TERM) / (A * p_var)
    y_star = min(1.0, max(0.0, raw_y))
    
    # Portfolio breakdown: y_star * tangency_weights in stocks, (1 - y_star) in 91D T-Bill
    asset_alloc = {
        'TRENT': round(y_star * tangency_weights[0] * 100, 2),
        'ASIANPAINT': round(y_star * tangency_weights[1] * 100, 2),
        'TCS': round(y_star * tangency_weights[2] * 100, 2),
        '91D_TBILL': round((1.0 - y_star) * 100, 2)
    }
    
    # Expected return and vol of complete portfolio
    c_ret = y_star * tangency_ret + (1.0 - y_star) * RF_SHORT_TERM
    c_vol = y_star * tangency_vol
    
    return {
        'sub_a': sub_a,
        'sub_b': sub_b,
        'raw_r': raw_r,
        'r_used': r_used,
        'prudence_triggered': prudence_triggered,
        'A': A,
        'basket': basket,
        'equity_share_pct': round(y_star * 100, 1),
        'tbill_share_pct': round((1.0 - y_star) * 100, 1),
        'asset_alloc_pct': asset_alloc,
        'expected_return_pct': round(c_ret * 100, 2),
        'expected_vol_pct': round(c_vol * 100, 2)
    }

# Pre-compute the 3 standard archetypes from questionnaire
archetypes = {
    'Aggressive (Priya, Age 27)': evaluate_risk_profile([4, 4, 3, 3, 3], [4, 4, 4, 3, 4]), # R=36 -> A=2.2
    'Balanced (Rahul, Age 41)': evaluate_risk_profile([3, 3, 3, 2, 2], [3, 3, 3, 2, 3]),    # R=27 -> A=4.9
    'Defensive (Meena, Age 58)': evaluate_risk_profile([1, 2, 2, 2, 1], [1, 2, 1, 2, 1]),   # R=15 -> A=8.5
    'Prudence Case (Arjun, 30)': evaluate_risk_profile([2, 2, 1, 1, 1], [4, 3, 3, 3, 3])   # subA=7, subB=16 -> R_used=14 -> A=8.8
}

# -------------------------------------------------------------
# 5. LIFECYCLE SIP GLIDE PATH (20-YEAR PROJECTION)
# -------------------------------------------------------------
def simulate_sip_glide_path(start_monthly_sip=25000, step_up_pct=0.10, years=20):
    """
    Simulates wealth accumulation over 20 years with age glide path:
    Years 1-7 (Age 25-32): Aggressive (A=2.2, y=100%)
    Years 8-15 (Age 32-40): Balanced (A=4.9, y=65%)
    Years 16-20 (Age 40-45+): Defensive (A=8.5, y=35%)
    """
    total_wealth = 0.0
    total_invested = 0.0
    history = []
    
    current_sip = start_monthly_sip
    
    for yr in range(1, years + 1):
        if yr <= 7:
            basket_name = 'Aggressive'
            y = 1.00
        elif yr <= 15:
            basket_name = 'Balanced'
            y = 0.65
        else:
            basket_name = 'Defensive'
            y = 0.35
            
        r_port = y * tangency_ret + (1 - y) * RF_SHORT_TERM
        monthly_r = (1 + r_port) ** (1/12) - 1
        
        for m in range(12):
            total_invested += current_sip
            total_wealth = (total_wealth + current_sip) * (1 + monthly_r)
            
        history.append({
            'year': yr,
            'age': 25 + yr,
            'basket': basket_name,
            'equity_pct': round(y * 100, 1),
            'monthly_sip': round(current_sip, 0),
            'cumulative_invested': round(total_invested, 0),
            'projected_wealth': round(total_wealth, 0)
        })
        current_sip *= (1 + step_up_pct)
        
    return pd.DataFrame(history)

df_sip = simulate_sip_glide_path()

# -------------------------------------------------------------
# 6. HISTORICAL BACKTEST & 4 CORE PERFORMANCE METRICS
# -------------------------------------------------------------
# Portfolio return series (Historical monthly)
ret_tangency = (
    tangency_weights[0] * ret_trent +
    tangency_weights[1] * ret_ap +
    tangency_weights[2] * ret_tcs
)
ret_ew = (ret_trent + ret_ap + ret_tcs) / 3.0

def calc_metrics(series, benchmark, rf_ann):
    ann_ret = np.mean(series) * 12
    ann_vol = np.std(series, ddof=1) * np.sqrt(12)
    cov_b = np.cov(series, benchmark)[0, 1]
    var_b = np.var(benchmark, ddof=1)
    beta = cov_b / var_b
    
    # 1. Sharpe
    sharpe = (ann_ret - rf_ann) / ann_vol if ann_vol > 0 else 0
    # 2. Treynor
    treynor = (ann_ret - rf_ann) / beta if beta != 0 else 0
    # 3. Jensen's Alpha
    b_ann_ret = np.mean(benchmark) * 12
    alpha = ann_ret - (rf_ann + beta * (b_ann_ret - rf_ann))
    # 4. Information Ratio
    te = np.std(series - benchmark, ddof=1) * np.sqrt(12)
    ir = (ann_ret - b_ann_ret) / te if te != 0 else 0
    
    return {
        'Annual Return (%)': round(ann_ret * 100, 2),
        'Annual Volatility (%)': round(ann_vol * 100, 2),
        'Beta vs Nifty': round(beta, 2),
        'Sharpe Ratio': round(sharpe, 2),
        'Treynor Ratio (%)': round(treynor * 100, 2),
        'Jensen Alpha (%)': round(alpha * 100, 2),
        'Tracking Error (%)': round(te * 100, 2),
        'Information Ratio': round(ir, 2)
    }

backtest_results = {
    'TRENT': calc_metrics(ret_trent, ret_nifty, RF_LONG_TERM),
    'ASIANPAINT': calc_metrics(ret_ap, ret_nifty, RF_LONG_TERM),
    'TCS': calc_metrics(ret_tcs, ret_nifty, RF_LONG_TERM),
    'Equal-Weight (3 Stocks)': calc_metrics(ret_ew, ret_nifty, RF_LONG_TERM),
    'Optimal Tangency Portfolio': calc_metrics(ret_tangency, ret_nifty, RF_LONG_TERM),
    'Nifty 50 Benchmark': calc_metrics(ret_nifty, ret_nifty, RF_LONG_TERM)
}

df_metrics = pd.DataFrame(backtest_results).T

# -------------------------------------------------------------
# 7. EXPORT SUMMARY & PLOTS
# -------------------------------------------------------------
# Save metrics to CSV
df_metrics.to_csv(os.path.join(OUTPUT_DIR, 'portfolio_performance_metrics.csv'))
df_sip.to_csv(os.path.join(OUTPUT_DIR, 'sip_glide_path_projection.csv'), index=False)

# Save summary JSON for Streamlit & Report
summary_data = {
    'weights': {
        'TRENT': round(tangency_weights[0] * 100, 2),
        'ASIANPAINT': round(tangency_weights[1] * 100, 2),
        'TCS': round(tangency_weights[2] * 100, 2)
    },
    'tangency_return_pct': round(tangency_ret * 100, 2),
    'tangency_vol_pct': round(tangency_vol * 100, 2),
    'tangency_sharpe': round(tangency_sharpe, 2),
    'archetypes': archetypes,
    'metrics_table': df_metrics.to_dict()
}

with open(os.path.join(OUTPUT_DIR, 'portfolio_summary.json'), 'w') as f:
    json.dump(summary_data, f, indent=4)

print("=== PORTFOLIO ENGINE EXECUTION SUCCESSFUL ===")
print("\nOptimal Risky Portfolio Weights:")
print(f"Trent: {tangency_weights[0]*100:.1f}%, Asian Paints: {tangency_weights[1]*100:.1f}%, TCS: {tangency_weights[2]*100:.1f}%")
print(f"Tangency Expected Return: {tangency_ret*100:.2f}%, Volatility: {tangency_vol*100:.2f}%, Sharpe: {tangency_sharpe:.2f}")

print("\n--- 4 CORE PERFORMANCE METRICS (HISTORICAL 5-YEAR BACKTEST) ---")
print(df_metrics[['Annual Return (%)', 'Annual Volatility (%)', 'Sharpe Ratio', 'Treynor Ratio (%)', 'Jensen Alpha (%)', 'Information Ratio']])

print("\n--- QUESTIONNAIRE ARCHETYPES & BASKETS ---")
for name, data in archetypes.items():
    print(f"\n{name}:")
    print(f"  Score R: {data['r_used']} -> A: {data['A']} -> Basket: {data['basket']}")
    print(f"  Allocation: Equity {data['equity_share_pct']}%, T-Bills {data['tbill_share_pct']}%")
    print(f"  Asset breakdown: {data['asset_alloc_pct']}")
