"""
Standalone script to generate publication-grade pedagogical Matplotlib diagrams
illustrating the complete Mamdani Fuzzy Inference System walkthrough for viva and documentation.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
matplotlib.use('Agg')
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
from fuzzy_logic.rules import RULE_BASE, evaluate_rule_base, evaluate_rule_base_detailed
from fuzzy_logic.risk_evaluator import FuzzyRiskEvaluator

def main():
    # Example Profile for Walkthrough
    age_val = 30.0
    inc_val = 85.0
    loss_val = 60.0
    horiz_val = 8.0

    age_mems = fuzzify_age(age_val)
    inc_mems = fuzzify_income_stability(inc_val)
    loss_mems = fuzzify_loss_tolerance(loss_val)
    horiz_mems = fuzzify_horizon(horiz_val)

    detailed_rules = evaluate_rule_base_detailed(age_mems, inc_mems, loss_mems, horiz_mems)
    alphas = evaluate_rule_base(age_mems, inc_mems, loss_mems, horiz_mems)

    evaluator = FuzzyRiskEvaluator(discretization_steps=200)
    result = evaluator.evaluate(age_val, inc_val, loss_val, horiz_val)
    crisp_score = result.crisp_risk_score

    # 3-Panel Walkthrough Plot
    fig, axes = plt.subplots(3, 1, figsize=(13, 14), facecolor='#FBF9F1')
    fig.subplots_adjust(hspace=0.45, left=0.09, right=0.94, top=0.94, bottom=0.06)

    c_blue = '#1E3A8A'
    c_amber = '#D97706'
    c_red = '#DC2626'
    c_green = '#15803D'

    # Panel 1: Input Membership Functions & Fuzzification
    ax1 = axes[0]
    ax1.set_facecolor('#FFFFFF')
    x_age = np.linspace(18, 80, 300)
    y_young = [trapmf(x, LinguisticVariables.AGE_YOUNG) for x in x_age]
    y_middle = [trimf(x, LinguisticVariables.AGE_MIDDLE) for x in x_age]
    y_senior = [trapmf(x, LinguisticVariables.AGE_SENIOR) for x in x_age]

    mu_y_val = age_mems["young"]
    mu_m_val = age_mems["middle"]
    mu_s_val = age_mems["senior"]

    ax1.plot(x_age, y_young, label=f"Young Set (mu = {mu_y_val:.2f})", color=c_blue, lw=2.2)
    ax1.plot(x_age, y_middle, label=f"Middle-Aged Set (mu = {mu_m_val:.2f})", color=c_amber, lw=2.2)
    ax1.plot(x_age, y_senior, label=f"Senior Set (mu = {mu_s_val:.2f})", color=c_red, lw=2.2)
    ax1.axvline(x=age_val, color=c_green, ls='--', lw=2.5, label=f"Crisp Input: Age = {int(age_val)}")
    ax1.scatter([age_val, age_val], [mu_y_val, mu_m_val], color=c_green, s=75, zorder=5)

    ax1.set_title("Stage 1: Fuzzification (Input Universe of Discourse & Membership Intersections for Age = 30)", fontsize=12, fontweight='bold', color=c_blue)
    ax1.set_xlabel("Age (Years)", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel("Degree of Membership (mu)", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, alpha=0.3, ls=':')
    ax1.legend(loc='upper right', framealpha=0.92, fontsize=9.5)

    # Panel 2: Rule Firing Strengths (All 22 Rules)
    ax2 = axes[1]
    ax2.set_facecolor('#FFFFFF')
    rule_ids = [r['rule_id'] for r in detailed_rules]
    firing_vals = [r['firing_strength'] for r in detailed_rules]
    colors = []
    for r in detailed_rules:
        if r['firing_strength'] == 0:
            colors.append('#E2E8F0')
        elif r['consequent'] == 'aggressive':
            colors.append(c_red)
        elif r['consequent'] == 'moderate':
            colors.append(c_amber)
        else:
            colors.append(c_blue)

    bars = ax2.bar(rule_ids, firing_vals, color=colors, edgecolor='#1E3A8A', lw=1.1)
    for bar, val in zip(bars, firing_vals):
        if val > 0:
            ax2.text(bar.get_x() + bar.get_width()/2.0, val + 0.02, f"{val:.2f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=c_blue)

    ax2.set_title("Stage 2: Rule Firing Strengths (alpha) of All 22 Mamdani Rules [T-Norm Min Evaluation]", fontsize=12, fontweight='bold', color=c_blue)
    ax2.set_xlabel("Fuzzy Rule Catalog (FR01 to FR22)", fontsize=10.5, fontweight='bold')
    ax2.set_ylabel("Firing Strength (alpha)", fontsize=10.5, fontweight='bold')
    ax2.set_ylim(0, 1.15)
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    ax2.grid(True, alpha=0.3, ls=':', axis='y')

    # Panel 3: Mamdani Implication, S-Norm Aggregation & Centroid Defuzzification
    ax3 = axes[2]
    ax3.set_facecolor('#FFFFFF')
    y_vals = np.linspace(0, 100, 300)
    mu_cons = np.array([trapmf(y, LinguisticVariables.RISK_CONSERVATIVE) for y in y_vals])
    mu_mod = np.array([trimf(y, LinguisticVariables.RISK_MODERATE) for y in y_vals])
    mu_agg = np.array([trapmf(y, LinguisticVariables.RISK_AGGRESSIVE) for y in y_vals])

    clip_cons = np.minimum(alphas['conservative'], mu_cons)
    clip_mod = np.minimum(alphas['moderate'], mu_mod)
    clip_agg = np.minimum(alphas['aggressive'], mu_agg)
    mu_aggregated = np.maximum(np.maximum(clip_cons, clip_mod), clip_agg)

    ax3.plot(y_vals, mu_cons, color=c_blue, ls=':', alpha=0.5, label=f"Conservative Set (alpha_max = {alphas['conservative']:.2f})")
    ax3.plot(y_vals, mu_mod, color=c_amber, ls=':', alpha=0.5, label=f"Moderate Set (alpha_max = {alphas['moderate']:.2f})")
    ax3.plot(y_vals, mu_agg, color=c_red, ls=':', alpha=0.5, label=f"Aggressive Set (alpha_max = {alphas['aggressive']:.2f})")

    ax3.fill_between(y_vals, 0, mu_aggregated, color='#3B82F6', alpha=0.35, label='Aggregated Fuzzy Area (S-Norm Max)')
    ax3.plot(y_vals, mu_aggregated, color='#1D4ED8', lw=2.2)

    ax3.axvline(x=crisp_score, color=c_green, lw=2.8, ls='--', label=f"Center of Gravity: Crisp Score R* = {crisp_score:.1f}")
    ax3.scatter([crisp_score], [0.25], color=c_green, s=90, zorder=6)

    ax3.set_title(f"Stages 3 & 4: Mamdani Implication, S-Norm Aggregation & Centroid Defuzzification (R* = {crisp_score:.1f})", fontsize=12, fontweight='bold', color=c_blue)
    ax3.set_xlabel("Risk Appetite Universe of Discourse [0 to 100]", fontsize=10.5, fontweight='bold')
    ax3.set_ylabel("Degree of Truth / Height (mu)", fontsize=10.5, fontweight='bold')
    ax3.set_ylim(-0.05, 1.05)
    ax3.grid(True, alpha=0.3, ls=':')
    ax3.legend(loc='upper left', framealpha=0.92, fontsize=9.5)

    out_dir = Path('docs/images')
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_path = out_dir / 'fuzzy_inference_walkthrough.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    print('SUCCESS: Saved walkthrough plot to', plot_path.resolve())

if __name__ == '__main__':
    main()
