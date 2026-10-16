"""
Script to generate standalone, publication-quality individual PNG plots
for each stage of the Mamdani FIS and Market Backtest.
"""
import os
import sys
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

# Targets
report_img_dir = PROJECT_ROOT / "report" / "images"
frontend_asset_dir = PROJECT_ROOT / "frontend" / "assets"
report_img_dir.mkdir(parents=True, exist_ok=True)
frontend_asset_dir.mkdir(parents=True, exist_ok=True)

# Colors
c_ink = "#1F3A8A"
c_ink_light = "#3B82F6"
c_red = "#C2342B"
c_tan = "#C9A66B"
c_green = "#15803D"
c_paper = "#EFE56A"

# Profile parameters (Balanced Profile)
age, horizon, loss_tol, inc_stab = 38, 8, 50.0, 85.0
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

# ------------------------------------------------------------------------------
# 1. MAMDANI STEP 1: INPUT FUZZIFICATION (2x2 Clean Subplots)
# ------------------------------------------------------------------------------
fig1, axes = plt.subplots(2, 2, figsize=(9.5, 6.2), facecolor="#FFFFFF")
# Age
x_age = np.linspace(18, 85, 200)
axes[0, 0].plot(x_age, [trapmf(x, LinguisticVariables.AGE_YOUNG) for x in x_age], label="Young", color=c_ink_light, lw=2)
axes[0, 0].plot(x_age, [trimf(x, LinguisticVariables.AGE_MIDDLE) for x in x_age], label="Middle", color=c_tan, lw=2)
axes[0, 0].plot(x_age, [trapmf(x, LinguisticVariables.AGE_SENIOR) for x in x_age], label="Senior", color=c_red, lw=2)
axes[0, 0].axvline(age, color=c_ink, linestyle="--", lw=2, label=f"Input: {age}y")
axes[0, 0].set_title(f"Age Fuzzification (Input = {age}y)", fontsize=11, fontweight="bold", color=c_ink)
axes[0, 0].set_xlabel("Age (Years)", fontsize=9)
axes[0, 0].set_ylabel("Membership (μ)", fontsize=9)
axes[0, 0].legend(fontsize=8, loc="upper right")
axes[0, 0].grid(True, linestyle=":", alpha=0.5)

# Horizon
x_h = np.linspace(0, 30, 200)
axes[0, 1].plot(x_h, [trapmf(x, LinguisticVariables.HORIZON_SHORT) for x in x_h], label="Short (<3y)", color=c_red, lw=2)
axes[0, 1].plot(x_h, [trimf(x, LinguisticVariables.HORIZON_MEDIUM) for x in x_h], label="Medium (3-12y)", color=c_tan, lw=2)
axes[0, 1].plot(x_h, [trapmf(x, LinguisticVariables.HORIZON_LONG) for x in x_h], label="Long (>8y)", color=c_green, lw=2)
axes[0, 1].axvline(horizon, color=c_ink, linestyle="--", lw=2, label=f"Input: {horizon}y")
axes[0, 1].set_title(f"Horizon Fuzzification (Input = {horizon}y)", fontsize=11, fontweight="bold", color=c_ink)
axes[0, 1].set_xlabel("Horizon (Years)", fontsize=9)
axes[0, 1].set_ylabel("Membership (μ)", fontsize=9)
axes[0, 1].legend(fontsize=8, loc="upper right")
axes[0, 1].grid(True, linestyle=":", alpha=0.5)

# Loss Tolerance
x_l = np.linspace(0, 100, 200)
axes[1, 0].plot(x_l, [trapmf(x, LinguisticVariables.LOSS_LOW) for x in x_l], label="Low", color=c_red, lw=2)
axes[1, 0].plot(x_l, [trimf(x, LinguisticVariables.LOSS_MEDIUM) for x in x_l], label="Medium", color=c_tan, lw=2)
axes[1, 0].plot(x_l, [trapmf(x, LinguisticVariables.LOSS_HIGH) for x in x_l], label="High", color=c_green, lw=2)
axes[1, 0].axvline(loss_tol, color=c_ink, linestyle="--", lw=2, label=f"Input: {loss_tol:.0f}")
axes[1, 0].set_title(f"Loss Tolerance Fuzzification (Input = {loss_tol:.0f})", fontsize=11, fontweight="bold", color=c_ink)
axes[1, 0].set_xlabel("Loss Tolerance Scale [0-100]", fontsize=9)
axes[1, 0].set_ylabel("Membership (μ)", fontsize=9)
axes[1, 0].legend(fontsize=8, loc="upper right")
axes[1, 0].grid(True, linestyle=":", alpha=0.5)

# Income Stability
x_inc = np.linspace(0, 100, 200)
axes[1, 1].plot(x_inc, [trapmf(x, LinguisticVariables.INCOME_UNSTABLE) for x in x_inc], label="Unstable", color=c_red, lw=2)
axes[1, 1].plot(x_inc, [trimf(x, LinguisticVariables.INCOME_MODERATE) for x in x_inc], label="Moderate", color=c_tan, lw=2)
axes[1, 1].plot(x_inc, [trapmf(x, LinguisticVariables.INCOME_STABLE) for x in x_inc], label="Stable", color=c_green, lw=2)
axes[1, 1].axvline(inc_stab, color=c_ink, linestyle="--", lw=2, label=f"Input: {inc_stab:.0f}")
axes[1, 1].set_title(f"Income Stability Fuzzification (Input = {inc_stab:.0f})", fontsize=11, fontweight="bold", color=c_ink)
axes[1, 1].set_xlabel("Income Stability Scale [0-100]", fontsize=9)
axes[1, 1].set_ylabel("Membership (μ)", fontsize=9)
axes[1, 1].legend(fontsize=8, loc="upper right")
axes[1, 1].grid(True, linestyle=":", alpha=0.5)

plt.tight_layout()
p1 = report_img_dir / "mamdani_step1_inputs.png"
plt.savefig(p1, dpi=200)
plt.close(fig1)
print(f"[+] Saved -> {p1}")

# ------------------------------------------------------------------------------
# 2. MAMDANI STEP 2: RULE FIRING STRENGTHS (Standalone Horizontal Bar Plot)
# ------------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(8.5, 4.0), facecolor="#FFFFFF")
categories = ["Conservative", "Moderate", "Aggressive"]
bar_alphas = [alphas["conservative"], alphas["moderate"], alphas["aggressive"]]
bar_colors = [c_ink_light, c_tan, c_red]

bars = ax2.barh(categories, bar_alphas, color=bar_colors, height=0.5, edgecolor=c_ink, lw=1.2)
for bar, val in zip(bars, bar_alphas):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2, f"α = {val:.2f}",
             va="center", ha="left", fontsize=10, fontweight="bold", color=c_ink)

ax2.set_xlim(0, 1.15)
ax2.set_xlabel("Gödel Min Rule Firing Strength (α)", fontsize=10, fontweight="bold", color=c_ink)
ax2.set_title("Mamdani Rule Base Evaluation: Output Consequent Firing Strengths", fontsize=11, fontweight="bold", color=c_ink)
ax2.grid(True, linestyle=":", alpha=0.5, axis="x")
plt.tight_layout()
p2 = report_img_dir / "mamdani_step2_rules.png"
plt.savefig(p2, dpi=200)
plt.close(fig2)
print(f"[+] Saved -> {p2}")

# ------------------------------------------------------------------------------
# 3. MAMDANI STEP 3: IMPLICATION (CLIPPING) (Standalone Plot)
# ------------------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(8.5, 4.2), facecolor="#FFFFFF")
ax3.plot(y_vals, mu_cons, "--", color="#94A3B8", lw=1.5, label="Raw Conservative")
ax3.plot(y_vals, mu_mod, "--", color="#CBD5E1", lw=1.5, label="Raw Moderate")
ax3.plot(y_vals, mu_agg, "--", color="#94A3B8", lw=1.5, label="Raw Aggressive")

ax3.fill_between(y_vals, 0, clip_cons, color=c_ink_light, alpha=0.45, label=f"Conservative Cut (α={alphas['conservative']:.2f})")
ax3.fill_between(y_vals, 0, clip_mod, color=c_tan, alpha=0.45, label=f"Moderate Cut (α={alphas['moderate']:.2f})")
ax3.fill_between(y_vals, 0, clip_agg, color=c_red, alpha=0.45, label=f"Aggressive Cut (α={alphas['aggressive']:.2f})")

ax3.set_title("Mamdani Min-Implication: Consequent Membership Function Truncation", fontsize=11, fontweight="bold", color=c_ink)
ax3.set_xlabel("Output Risk Appetite Universe Y [0 – 100]", fontsize=10, color=c_ink)
ax3.set_ylabel("Clipped Firing Degree (μ)", fontsize=10, color=c_ink)
ax3.set_ylim(-0.05, 1.15)
ax3.legend(loc="upper right", framealpha=0.9, fontsize=9)
ax3.grid(True, linestyle=":", alpha=0.5)
plt.tight_layout()
p3 = report_img_dir / "mamdani_step3_implication.png"
plt.savefig(p3, dpi=200)
plt.close(fig3)
print(f"[+] Saved -> {p3}")

# ------------------------------------------------------------------------------
# 4. MAMDANI STEP 4: AGGREGATION & CENTROID DEFUZZIFICATION (Standalone Plot)
# ------------------------------------------------------------------------------
fig4, ax4 = plt.subplots(figsize=(8.5, 4.2), facecolor="#FFFFFF")
ax4.fill_between(y_vals, 0, mu_aggregated, color=c_ink, alpha=0.35, label="Unified Aggregated Set μ_Agg(y)")
ax4.plot(y_vals, mu_aggregated, color=c_ink, lw=2.2)

ax4.axvline(crisp_score, color=c_red, lw=3, linestyle="-", label=f"Center of Gravity Centroid R* = {crisp_score:.1f}")

bbox_props = dict(boxstyle="round,pad=0.5", fc=c_paper, ec=c_ink, lw=1.5)
ax4.text(
    crisp_score, 0.70,
    f"  Defuzzified Score R* = {crisp_score:.1f} / 100\n  Risk Category: {risk_cat.upper()}  ",
    ha="center", va="center", color=c_ink, fontweight="bold", fontsize=10,
    bbox=bbox_props
)

ax4.set_title(f"S-Norm Aggregation & Center of Gravity Defuzzification (R* = {crisp_score:.1f})", fontsize=11, fontweight="bold", color=c_ink)
ax4.set_xlabel("Output Risk Appetite Universe Y [0 – 100]", fontsize=10, color=c_ink)
ax4.set_ylabel("Aggregated Truth Value μ_Agg(y)", fontsize=10, color=c_ink)
ax4.set_ylim(-0.05, 1.15)
ax4.legend(loc="upper left", framealpha=0.9, fontsize=9)
ax4.grid(True, linestyle=":", alpha=0.5)
plt.tight_layout()
p4 = report_img_dir / "mamdani_step4_defuzzification.png"
plt.savefig(p4, dpi=200)
plt.close(fig4)
print(f"[+] Saved -> {p4}")

# ------------------------------------------------------------------------------
# 5. STANDALONE 17-YEAR BACKTEST PLOTS (Wealth Trajectory & Drawdown)
# ------------------------------------------------------------------------------
backtester = PortfolioBacktester(risk_free_rate=0.065)
strategies = {
    "FinWise Moderate": {"equity": 0.475, "debt": 0.375, "gold": 0.10, "cash": 0.05},
    "100% Nifty 50": {"equity": 1.00, "debt": 0.0, "gold": 0.0, "cash": 0.0},
    "Traditional 60/40": {"equity": 0.60, "debt": 0.40, "gold": 0.0, "cash": 0.0},
    "100% Fixed Deposit": {"equity": 0.0, "debt": 0.0, "gold": 0.0, "cash": 1.00},
}
results = {k: backtester.simulate_strategy(k, v) for k, v in strategies.items()}
years = [2007] + list(range(2008, 2025))
colors = {"FinWise Moderate": "#15803D", "100% Nifty 50": "#C2342B", "Traditional 60/40": "#3B82F6", "100% Fixed Deposit": "#64748B"}

# Standalone Wealth Trajectory
fig5, ax5 = plt.subplots(figsize=(9.0, 4.5), facecolor="#FFFFFF")
for name, m in results.items():
    ax5.plot(years, m.wealth_series, label=f"{name} (CAGR: {m.cagr*100:.1f}%, Final: ₹{m.final_wealth:,.0f})",
             color=colors[name], lw=2.4 if name=="FinWise Moderate" else 1.8)
ax5.set_title("17-Year Empirical Market Wealth Trajectory (2008–2024, Initial Base: ₹1,00,000)", fontsize=11, fontweight="bold", color=c_ink)
ax5.set_xlabel("Calendar Year", fontsize=10, color=c_ink)
ax5.set_ylabel("Portfolio Value (₹ INR)", fontsize=10, color=c_ink)
ax5.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("₹{x:,.0f}"))
ax5.legend(loc="upper left", fontsize=8.5, framealpha=0.95)
ax5.grid(True, linestyle=":", alpha=0.5)
plt.tight_layout()
p5 = report_img_dir / "backtest_wealth_trajectory.png"
plt.savefig(p5, dpi=200)
plt.close(fig5)
print(f"[+] Saved -> {p5}")

# Standalone Drawdown Curve
fig6, ax6 = plt.subplots(figsize=(9.0, 4.2), facecolor="#FFFFFF")
for name, m in results.items():
    ax6.plot(years, [d * 100 for d in m.drawdown_series], label=f"{name} (Max DD: {m.max_drawdown*100:.1f}%)",
             color=colors[name], lw=2.2 if name=="FinWise Moderate" else 1.5)
ax6.axvspan(2008, 2009, color="#FEE2E2", alpha=0.6, label="2008 Lehman GFC Crash")
ax6.axvspan(2020, 2020.8, color="#FEF3C7", alpha=0.6, label="2020 COVID Shock")
ax6.set_title("Historical Portfolio Drawdown & Crisis Resilience Comparison (2008–2024)", fontsize=11, fontweight="bold", color=c_ink)
ax6.set_xlabel("Calendar Year", fontsize=10, color=c_ink)
ax6.set_ylabel("Drawdown Percentage (%)", fontsize=10, color=c_ink)
ax6.legend(loc="lower left", fontsize=8.5, framealpha=0.95)
ax6.grid(True, linestyle=":", alpha=0.5)
plt.tight_layout()
p6 = report_img_dir / "backtest_drawdown_underwater.png"
plt.savefig(p6, dpi=200)
plt.close(fig6)
print(f"[+] Saved -> {p6}")

print("\n[SUCCESS] All standalone individual plots generated successfully!")
