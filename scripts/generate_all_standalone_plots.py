"""
Script: generate_all_standalone_plots.py
Generates individual, standalone, high-resolution PNG plots for each specific
figure in the FinWise AI formal engineering report.
"""
import os
import sys
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Single-thread OpenBLAS / MKL to prevent memory errors on Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fuzzy_logic.membership import (
    LinguisticVariables,
    fuzzify_age,
    fuzzify_horizon,
    fuzzify_income_stability,
    fuzzify_loss_tolerance,
    trapmf,
    trimf,
)
from fuzzy_logic.rules import evaluate_rule_base
from fuzzy_logic.risk_evaluator import FuzzyRiskEvaluator
from evaluation.backtester import PortfolioBacktester

# Target directories
img_dir = PROJECT_ROOT / "report" / "images"
frontend_asset_dir = PROJECT_ROOT / "frontend" / "assets"
img_dir.mkdir(parents=True, exist_ok=True)
frontend_asset_dir.mkdir(parents=True, exist_ok=True)

# Publication styling tokens
c_ink = "#1E3A8A"       # Primary deep navy
c_ink_light = "#2563EB" # Royal blue
c_red = "#DC2626"       # Crimson red
c_tan = "#D97706"       # Amber / tan
c_green = "#16A34A"     # Emerald green
c_slate = "#475569"     # Neutral slate
c_paper = "#FEF3C7"     # Subtle gold callout

# Evaluation Profile: Balanced Mid-Career Family (Age 38, Horizon 8y, LossTol 50, IncStab 85)
age = 38.0
horizon = 8.0
loss_tol = 50.0
inc_stab = 85.0

age_mems = fuzzify_age(age)
horiz_mems = fuzzify_horizon(horizon)
loss_mems = fuzzify_loss_tolerance(loss_tol)
inc_mems = fuzzify_income_stability(inc_stab)
alphas = evaluate_rule_base(age_mems, inc_mems, loss_mems, horiz_mems)

evaluator = FuzzyRiskEvaluator(discretization_steps=200)
eval_res = evaluator.evaluate(age=age, income_stability=inc_stab, loss_tolerance=loss_tol, investment_horizon_years=horizon)
crisp_score = eval_res.crisp_risk_score
risk_cat = eval_res.risk_category

y_vals = np.linspace(0, 100, 300)
mu_cons = np.array([trapmf(y, LinguisticVariables.RISK_CONSERVATIVE) for y in y_vals])
mu_mod = np.array([trimf(y, LinguisticVariables.RISK_MODERATE) for y in y_vals])
mu_agg = np.array([trapmf(y, LinguisticVariables.RISK_AGGRESSIVE) for y in y_vals])

clip_cons = np.minimum(alphas["conservative"], mu_cons)
clip_mod = np.minimum(alphas["moderate"], mu_mod)
clip_agg = np.minimum(alphas["aggressive"], mu_agg)
mu_aggregated = np.maximum(np.maximum(clip_cons, clip_mod), clip_agg)


def save_plot(fig, filename):
    p1 = img_dir / filename
    p2 = frontend_asset_dir / filename
    fig.savefig(p1, dpi=220, bbox_inches="tight")
    fig.savefig(p2, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Successfully generated: {filename}")


# ==============================================================================
# PLOT 1: AGE FUZZIFICATION
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
x_age = np.linspace(18, 85, 300)
ax.plot(x_age, [trapmf(x, LinguisticVariables.AGE_YOUNG) for x in x_age], label="Young (18 - 36y)", color=c_ink_light, lw=2.5)
ax.plot(x_age, [trimf(x, LinguisticVariables.AGE_MIDDLE) for x in x_age], label="Middle-Aged (28 - 56y)", color=c_tan, lw=2.5)
ax.plot(x_age, [trapmf(x, LinguisticVariables.AGE_SENIOR) for x in x_age], label="Senior (48 - 80+y)", color=c_red, lw=2.5)
ax.axvline(age, color=c_ink, linestyle="--", lw=2.2, label=f"Client Input Age = {age:.0f} yrs")

for label, deg, col in [("Young", age_mems["young"], c_ink_light), ("Middle", age_mems["middle"], c_tan), ("Senior", age_mems["senior"], c_red)]:
    if deg > 0.01:
        ax.scatter([age], [deg], color=col, s=90, zorder=5)
        ax.annotate(f"μ_{label} = {deg:.2f}", (age + 1.2, deg + 0.03), fontsize=10.5, fontweight="bold", color=c_ink)

ax.set_title("Input Variable 1: Age Fuzzification Membership Functions (Universe: [18, 85])", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Investor Chronological Age (Years)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Fuzzy Membership Degree (μ)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(18, 85)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_01_fuzz_age.png")


# ==============================================================================
# PLOT 2: HORIZON FUZZIFICATION
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
x_h = np.linspace(0, 30, 300)
ax.plot(x_h, [trapmf(x, LinguisticVariables.HORIZON_SHORT) for x in x_h], label="Short Horizon (< 3 yrs)", color=c_red, lw=2.5)
ax.plot(x_h, [trimf(x, LinguisticVariables.HORIZON_MEDIUM) for x in x_h], label="Medium Horizon (3 - 12 yrs)", color=c_tan, lw=2.5)
ax.plot(x_h, [trapmf(x, LinguisticVariables.HORIZON_LONG) for x in x_h], label="Long Horizon (8 - 30 yrs)", color=c_green, lw=2.5)
ax.axvline(horizon, color=c_ink, linestyle="--", lw=2.2, label=f"Client Input Horizon = {horizon:.0f} yrs")

for label, deg, col in [("Short", horiz_mems["short"], c_red), ("Medium", horiz_mems["medium"], c_tan), ("Long", horiz_mems["long"], c_green)]:
    if deg > 0.01:
        ax.scatter([horizon], [deg], color=col, s=90, zorder=5)
        ax.annotate(f"μ_{label} = {deg:.2f}", (horizon + 0.6, deg + 0.03), fontsize=10.5, fontweight="bold", color=c_ink)

ax.set_title("Input Variable 2: Investment Horizon Fuzzification (Universe: [0, 30] Years)", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Target Investment Horizon (Years)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Fuzzy Membership Degree (μ)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(0, 30)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_02_fuzz_horizon.png")


# ==============================================================================
# PLOT 3: LOSS TOLERANCE FUZZIFICATION
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
x_l = np.linspace(0, 100, 300)
ax.plot(x_l, [trapmf(x, LinguisticVariables.LOSS_LOW) for x in x_l], label="Low Loss Tolerance (Conservative)", color=c_red, lw=2.5)
ax.plot(x_l, [trimf(x, LinguisticVariables.LOSS_MEDIUM) for x in x_l], label="Medium Loss Tolerance (Moderate)", color=c_tan, lw=2.5)
ax.plot(x_l, [trapmf(x, LinguisticVariables.LOSS_HIGH) for x in x_l], label="High Loss Tolerance (Aggressive)", color=c_green, lw=2.5)
ax.axvline(loss_tol, color=c_ink, linestyle="--", lw=2.2, label=f"Client Input Loss Tol = {loss_tol:.0f} / 100")

for label, deg, col in [("Low", loss_mems["low"], c_red), ("Medium", loss_mems["medium"], c_tan), ("High", loss_mems["high"], c_green)]:
    if deg > 0.01:
        ax.scatter([loss_tol], [deg], color=col, s=90, zorder=5)
        ax.annotate(f"μ_{label} = {deg:.2f}", (loss_tol + 1.5, deg + 0.03), fontsize=10.5, fontweight="bold", color=c_ink)

ax.set_title("Input Variable 3: Psychological Loss Tolerance Fuzzification (Universe: [0, 100])", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Psychological Loss Tolerance Score (Self-Reported)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Fuzzy Membership Degree (μ)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(0, 100)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_03_fuzz_loss_tol.png")


# ==============================================================================
# PLOT 4: INCOME STABILITY FUZZIFICATION
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
x_inc = np.linspace(0, 100, 300)
ax.plot(x_inc, [trapmf(x, LinguisticVariables.INCOME_UNSTABLE) for x in x_inc], label="Unstable (Freelance / Commission)", color=c_red, lw=2.5)
ax.plot(x_inc, [trimf(x, LinguisticVariables.INCOME_MODERATE) for x in x_inc], label="Moderate (Private Sector / SMB)", color=c_tan, lw=2.5)
ax.plot(x_inc, [trapmf(x, LinguisticVariables.INCOME_STABLE) for x in x_inc], label="Stable (Govt / Tenured Corporate)", color=c_green, lw=2.5)
ax.axvline(inc_stab, color=c_ink, linestyle="--", lw=2.2, label=f"Client Input Income Stability = {inc_stab:.0f} / 100")

for label, deg, col in [("Unstable", inc_mems["unstable"], c_red), ("Moderate", inc_mems["moderate"], c_tan), ("Stable", inc_mems["stable"], c_green)]:
    if deg > 0.01:
        ax.scatter([inc_stab], [deg], color=col, s=90, zorder=5)
        ax.annotate(f"μ_{label} = {deg:.2f}", (inc_stab + 1.5, deg + 0.03), fontsize=10.5, fontweight="bold", color=c_ink)

ax.set_title("Input Variable 4: Income Stability Fuzzification (Universe: [0, 100])", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Income Predictability & Employment Tenure Score", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Fuzzy Membership Degree (μ)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(0, 100)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_04_fuzz_income_stab.png")


# ==============================================================================
# PLOT 5: RULE EVALUATION FIRING STRENGTHS (BAR CHART)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
rule_labels = ["Conservative Consequent", "Moderate Consequent", "Aggressive Consequent"]
rule_vals = [alphas["conservative"], alphas["moderate"], alphas["aggressive"]]
bar_cols = [c_ink_light, c_tan, c_red]

bars = ax.barh(rule_labels, rule_vals, color=bar_cols, height=0.45, edgecolor=c_ink, lw=1.5)
for bar, val in zip(bars, rule_vals):
    ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f"Firing Height α = {val:.2f}",
            va="center", ha="left", fontsize=11, fontweight="bold", color=c_ink)

ax.set_xlim(0, 1.15)
ax.set_xlabel("Gödel T-Norm Minimum Firing Strength: α_i = min(μ_Age, μ_Horiz, μ_Loss, μ_Inc)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_title("Mamdani Rule Base Evaluation: Consequent Class Firing Strengths", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.grid(True, linestyle=":", alpha=0.6, axis="x")
save_plot(fig, "plot_05_rule_eval_bars.png")


# ==============================================================================
# PLOT 6: MAMDANI MIN-IMPLICATION (TRUNCATION)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
ax.plot(y_vals, mu_cons, "--", color="#94A3B8", lw=1.5, label="Raw Conservative Membership Set")
ax.plot(y_vals, mu_mod, "--", color="#CBD5E1", lw=1.5, label="Raw Moderate Membership Set")
ax.plot(y_vals, mu_agg, "--", color="#94A3B8", lw=1.5, label="Raw Aggressive Membership Set")

ax.fill_between(y_vals, 0, clip_cons, color=c_ink_light, alpha=0.45, label=f"Conservative Truncation (α = {alphas['conservative']:.2f})")
ax.fill_between(y_vals, 0, clip_mod, color=c_tan, alpha=0.45, label=f"Moderate Truncation (α = {alphas['moderate']:.2f})")
ax.fill_between(y_vals, 0, clip_agg, color=c_red, alpha=0.45, label=f"Aggressive Truncation (α = {alphas['aggressive']:.2f})")

ax.set_title("Mamdani Min-Implication: Consequent Membership Function Truncation", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Output Risk Appetite Universe Y [0 – 100]", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Clipped Firing Degree min(α_i, μ_Ci(y))", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(0, 100)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_06_mamdani_implication.png")


# ==============================================================================
# PLOT 7: AGGREGATION & CENTROID DEFUZZIFICATION
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.0), facecolor="#FFFFFF")
ax.fill_between(y_vals, 0, mu_aggregated, color=c_ink, alpha=0.35, label="Unified S-Norm Aggregated Fuzzy Set μ_Agg(y)")
ax.plot(y_vals, mu_aggregated, color=c_ink, lw=2.5)

ax.axvline(crisp_score, color=c_red, lw=3.2, linestyle="-", label=f"Defuzzified Centroid Balance Line: R* = {crisp_score:.1f}")

bbox_props = dict(boxstyle="round,pad=0.6", fc=c_paper, ec=c_ink, lw=1.6)
ax.text(
    crisp_score, 0.72,
    f"  Crisp Output: R* = {crisp_score:.1f} / 100\n  Risk Category: {risk_cat.upper()}  ",
    ha="center", va="center", color=c_ink, fontweight="bold", fontsize=11,
    bbox=bbox_props
)

ax.set_title(f"S-Norm Aggregation & Center of Gravity (Centroid) Defuzzification (R* = {crisp_score:.1f})", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Output Risk Appetite Universe Y [0 – 100]", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Aggregated Truth Degree μ_Agg(y)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylim(-0.05, 1.15)
ax.set_xlim(0, 100)
ax.legend(loc="upper left", framealpha=0.95, fontsize=9.5)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_07_defuzzification_centroid.png")


# ==============================================================================
# PLOT 8: 17-YEAR MARKET WEALTH TRAJECTORY (STANDALONE)
# ==============================================================================
backtester = PortfolioBacktester(risk_free_rate=0.065)
strategies = {
    "FinWise Moderate": {"equity": 0.475, "debt": 0.375, "gold": 0.10, "cash": 0.05},
    "100% Nifty 50": {"equity": 1.00, "debt": 0.0, "gold": 0.0, "cash": 0.0},
    "Traditional 60/40": {"equity": 0.60, "debt": 0.40, "gold": 0.0, "cash": 0.0},
    "Age-Based (100 - Age)": {"equity": 0.62, "debt": 0.38, "gold": 0.0, "cash": 0.0},
    "100% Fixed Deposit": {"equity": 0.0, "debt": 0.0, "gold": 0.0, "cash": 1.00},
}
results = {k: backtester.simulate_strategy(k, v) for k, v in strategies.items()}
years = [2007] + list(range(2008, 2025))
colors = {
    "FinWise Moderate": "#15803D",
    "100% Nifty 50": "#DC2626",
    "Traditional 60/40": "#2563EB",
    "Age-Based (100 - Age)": "#D97706",
    "100% Fixed Deposit": "#64748B"
}

fig, ax = plt.subplots(figsize=(10, 5.0), facecolor="#FFFFFF")
for name, m in results.items():
    lw = 2.8 if name == "FinWise Moderate" else 1.8
    ax.plot(years, m.wealth_series, label=f"{name} (CAGR: {m.cagr*100:.1f}%, Final: ₹{m.final_wealth:,.0f})",
            color=colors[name], lw=lw)

ax.set_title("17-Year Empirical Market Wealth Trajectory (2008–2024, Initial Wealth: ₹1,00,000)", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Calendar Year", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Portfolio Terminal Value (₹ INR)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("₹{x:,.0f}"))
ax.set_xlim(2007, 2024)
ax.legend(loc="upper left", fontsize=9.2, framealpha=0.95)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_08_backtest_wealth.png")


# ==============================================================================
# PLOT 9: 17-YEAR HISTORICAL UNDERWATER DRAWDOWN (STANDALONE)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.0), facecolor="#FFFFFF")
for name, m in results.items():
    lw = 2.6 if name == "FinWise Moderate" else 1.6
    ax.plot(years, [d * 100 for d in m.drawdown_series], label=f"{name} (Max DD: {m.max_drawdown*100:.1f}%)",
            color=colors[name], lw=lw)

ax.axvspan(2008, 2009, color="#FEE2E2", alpha=0.6, label="2008 Lehman GFC Crash")
ax.axvspan(2020, 2020.8, color="#FEF3C7", alpha=0.6, label="2020 COVID Shock")
ax.set_title("Historical Portfolio Drawdown & Crisis Stress Resilience (2008–2024)", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Calendar Year", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Drawdown from High-Water Mark (%)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_xlim(2007, 2024)
ax.legend(loc="lower left", fontsize=9.2, framealpha=0.95)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_09_backtest_drawdown.png")


# ==============================================================================
# PLOT 10: RISK-RETURN EFFICIENT FRONTIER (CAGR VS VOLATILITY)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.0), facecolor="#FFFFFF")
for name, m in results.items():
    vol_pct = m.annualized_volatility * 100
    cagr_pct = m.cagr * 100
    col = colors[name]
    size = 180 if name == "FinWise Moderate" else 110
    ax.scatter([vol_pct], [cagr_pct], color=col, s=size, zorder=5, edgecolors="#000000", lw=1.2)
    ax.annotate(
        f"{name}\n(Sharpe: {m.sharpe_ratio:.2f})",
        (vol_pct + 0.4, cagr_pct - 0.2),
        fontsize=9.5, fontweight="bold", color=col
    )

ax.set_title("Risk-Adjusted Efficient Frontier: CAGR vs. Annualized Volatility (σ)", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xlabel("Annualized Volatility σ (%) [Lower Risk →]", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_ylabel("Compound Annual Growth Rate CAGR (%) [Higher Return ↑]", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_xlim(0, 30)
ax.set_ylim(6, 12)
ax.grid(True, linestyle=":", alpha=0.6)
save_plot(fig, "plot_10_backtest_frontier.png")


# ==============================================================================
# PLOT 11: CRISIS STRESS-TEST COMPARISON (BAR CHART)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor="#FFFFFF")
strat_names = list(results.keys())
gfc_returns = [results[s].gfc_2008_return * 100 for s in strat_names]
covid_returns = [results[s].covid_2020_return * 100 for s in strat_names]

x = np.arange(len(strat_names))
width = 0.35

rects1 = ax.bar(x - width/2, gfc_returns, width, label="2008 Lehman GFC Crash", color=c_red, edgecolor=c_ink)
rects2 = ax.bar(x + width/2, covid_returns, width, label="2020 COVID Shock Rebound", color=c_green, edgecolor=c_ink)

for rect in rects1:
    height = rect.get_height()
    ax.annotate(f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, -12 if height < 0 else 3),
                textcoords="offset points",
                ha="center", va="bottom", fontsize=8.8, fontweight="bold")

for rect in rects2:
    height = rect.get_height()
    ax.annotate(f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3 if height >= 0 else -12),
                textcoords="offset points",
                ha="center", va="bottom", fontsize=8.8, fontweight="bold")

ax.set_ylabel("Annual Return (%)", fontsize=10.5, fontweight="semibold", color=c_ink)
ax.set_title("Crisis Stress-Test Performance: 2008 Lehman GFC Crash vs. 2020 COVID Shock", fontsize=12, fontweight="bold", color=c_ink, pad=10)
ax.set_xticks(x)
ax.set_xticklabels(strat_names, fontsize=9.2, rotation=12, ha="right")
ax.axhline(0, color="#000000", lw=1.0)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.95)
ax.grid(True, linestyle=":", alpha=0.5, axis="y")
save_plot(fig, "plot_11_backtest_crisis_bars.png")

print("\n[SUCCESS] Generated all 11 standalone, high-resolution individual PNG plots!")
