"""
================================================================================
FINWISE AI – MAMDANI FUZZY INFERENCE MATPLOTLIB VISUALIZER
Author: Group 11 (Software Architecture & Design, IIIT Kottayam)
================================================================================
Generates publication-quality, pedagogical plots visualizing the 4 stages of
the Mamdani Fuzzy Inference System:
1. Fuzzification (Input Membership Functions & Crisp Input Intersections)
2. Fuzzy Rule Evaluation (Alpha Firing Strengths)
3. Mamdani Implication (Consequent Set Clipping)
4. Aggregation & Centroid Defuzzification (Center of Gravity Crisp Output)
================================================================================
"""

import io
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, Any, Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
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


def generate_mamdani_plot(
    age: float,
    horizon_years: float,
    loss_tolerance_val: float,
    income_stability_val: float,
    user_name: str = "Client Profile",
    save_path: Optional[str] = None,
) -> bytes:
    """
    Renders a comprehensive 4-panel Matplotlib diagram illustrating the complete
    Mamdani Fuzzy Inference process for an individual financial profile.
    """
    # 1. Run Fuzzification
    age_mems = fuzzify_age(age)
    horiz_mems = fuzzify_horizon(horizon_years)
    loss_mems = fuzzify_loss_tolerance(loss_tolerance_val)
    inc_mems = fuzzify_income_stability(income_stability_val)

    # 2. Rule Evaluation
    alphas = evaluate_rule_base(age_mems, inc_mems, loss_mems, horiz_mems)

    # 3. Output universe & Defuzzification
    evaluator = FuzzyRiskEvaluator(discretization_steps=200)
    eval_res = evaluator.evaluate(
        age=age,
        income_stability=income_stability_val,
        loss_tolerance=loss_tolerance_val,
        investment_horizon_years=horizon_years,
    )
    crisp_score = eval_res.crisp_risk_score
    risk_cat = eval_res.risk_category

    # Discretized domain for output [0, 100]
    y_vals = np.linspace(0, 100, 300)
    mu_cons = np.array([trapmf(y, LinguisticVariables.RISK_CONSERVATIVE) for y in y_vals])
    mu_mod = np.array([trimf(y, LinguisticVariables.RISK_MODERATE) for y in y_vals])
    mu_agg = np.array([trapmf(y, LinguisticVariables.RISK_AGGRESSIVE) for y in y_vals])

    # Clipped consequents
    clip_cons = np.minimum(alphas["conservative"], mu_cons)
    clip_mod = np.minimum(alphas["moderate"], mu_mod)
    clip_agg = np.minimum(alphas["aggressive"], mu_agg)
    mu_aggregated = np.maximum(np.maximum(clip_cons, clip_mod), clip_agg)

    # Styling Palette (Pin & Paper Legal Pad Style)
    c_ink = "#1F3A8A"
    c_ink_light = "#3B82F6"
    c_red = "#C2342B"
    c_cream = "#FBF9F1"
    c_paper = "#EFE56A"
    c_tan = "#C9A66B"
    c_green = "#15803D"

    fig = plt.figure(figsize=(14, 9), facecolor=c_cream)
    gs = fig.add_gridspec(2, 2, hspace=0.38, wspace=0.25, left=0.08, right=0.95, top=0.90, bottom=0.08)

    # --------------------------------------------------------------------------
    # SUBPLOT 1: INPUT 1 – AGE FUZZIFICATION
    # --------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#FFFFFF")
    x_age = np.linspace(18, 85, 200)
    y_young = [trapmf(x, LinguisticVariables.AGE_YOUNG) for x in x_age]
    y_middle = [trimf(x, LinguisticVariables.AGE_MIDDLE) for x in x_age]
    y_senior = [trapmf(x, LinguisticVariables.AGE_SENIOR) for x in x_age]

    ax1.plot(x_age, y_young, label="Young", color=c_ink_light, lw=2.2)
    ax1.plot(x_age, y_middle, label="Middle", color=c_tan, lw=2.2)
    ax1.plot(x_age, y_senior, label="Senior", color=c_red, lw=2.2)

    # Highlight user age
    ax1.axvline(age, color=c_ink, linestyle="--", lw=2, label=f"Input Age: {age}y")
    for name, deg, col in [("Young", age_mems["young"], c_ink_light),
                          ("Middle", age_mems["middle"], c_tan),
                          ("Senior", age_mems["senior"], c_red)]:
        if deg > 0.02:
            ax1.scatter([age], [deg], color=col, s=70, zorder=5)
            ax1.annotate(f"μ={deg:.2f}", (age + 1.2, deg), fontsize=10, fontweight="bold", color=c_ink)

    ax1.set_title(f"Step 1A: Age Fuzzification (Input = {age} years)", fontsize=13, fontweight="bold", color=c_ink, pad=8)
    ax1.set_xlabel("Age (Years)", fontsize=11, color=c_ink)
    ax1.set_ylabel("Membership Degree (μ)", fontsize=11, color=c_ink)
    ax1.set_ylim(-0.05, 1.15)
    ax1.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax1.grid(True, linestyle=":", alpha=0.5, color=c_ink)

    # --------------------------------------------------------------------------
    # SUBPLOT 2: INPUT 2 – INVESTMENT HORIZON FUZZIFICATION
    # --------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#FFFFFF")
    x_horiz = np.linspace(0, 30, 200)
    y_short = [trapmf(x, LinguisticVariables.HORIZON_SHORT) for x in x_horiz]
    y_med_h = [trimf(x, LinguisticVariables.HORIZON_MEDIUM) for x in x_horiz]
    y_long = [trapmf(x, LinguisticVariables.HORIZON_LONG) for x in x_horiz]

    ax2.plot(x_horiz, y_short, label="Short (<3y)", color=c_red, lw=2.2)
    ax2.plot(x_horiz, y_med_h, label="Medium (3-12y)", color=c_tan, lw=2.2)
    ax2.plot(x_horiz, y_long, label="Long (8-30y)", color=c_green, lw=2.2)

    # Highlight user horizon
    ax2.axvline(horizon_years, color=c_ink, linestyle="--", lw=2, label=f"Horizon: {horizon_years}y")
    for name, deg, col in [("Short", horiz_mems["short"], c_red),
                          ("Medium", horiz_mems["medium"], c_tan),
                          ("Long", horiz_mems["long"], c_green)]:
        if deg > 0.02:
            ax2.scatter([horizon_years], [deg], color=col, s=70, zorder=5)
            ax2.annotate(f"μ={deg:.2f}", (horizon_years + 0.6, deg), fontsize=10, fontweight="bold", color=c_ink)

    ax2.set_title(f"Step 1B: Horizon Fuzzification (Input = {horizon_years} yrs)", fontsize=13, fontweight="bold", color=c_ink, pad=8)
    ax2.set_xlabel("Investment Horizon (Years)", fontsize=11, color=c_ink)
    ax2.set_ylabel("Membership Degree (μ)", fontsize=11, color=c_ink)
    ax2.set_ylim(-0.05, 1.15)
    ax2.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax2.grid(True, linestyle=":", alpha=0.5, color=c_ink)

    # --------------------------------------------------------------------------
    # SUBPLOT 3: STEP 2 & 3 – RULE EVALUATION & MAMDANI IMPLICATION (CLIPPING)
    # --------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor("#FFFFFF")

    # Raw output membership sets (dashed)
    ax3.plot(y_vals, mu_cons, "--", color="#94A3B8", lw=1.5, label="Raw Conservative")
    ax3.plot(y_vals, mu_mod, "--", color="#CBD5E1", lw=1.5, label="Raw Moderate")
    ax3.plot(y_vals, mu_agg, "--", color="#94A3B8", lw=1.5, label="Raw Aggressive")

    # Shaded clipped consequents (Min Implication)
    ax3.fill_between(y_vals, 0, clip_cons, color=c_ink_light, alpha=0.45, label=f"Cons Cut (α={alphas['conservative']:.2f})")
    ax3.fill_between(y_vals, 0, clip_mod, color=c_tan, alpha=0.45, label=f"Mod Cut (α={alphas['moderate']:.2f})")
    ax3.fill_between(y_vals, 0, clip_agg, color=c_red, alpha=0.45, label=f"Agg Cut (α={alphas['aggressive']:.2f})")

    ax3.set_title("Step 2 & 3: Mamdani Implication (Min Clipping)", fontsize=13, fontweight="bold", color=c_ink, pad=8)
    ax3.set_xlabel("Risk Score Scale [0 - 100]", fontsize=11, color=c_ink)
    ax3.set_ylabel("Clipped Firing Height (α)", fontsize=11, color=c_ink)
    ax3.set_ylim(-0.05, 1.15)
    ax3.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax3.grid(True, linestyle=":", alpha=0.5, color=c_ink)

    # --------------------------------------------------------------------------
    # SUBPLOT 4: STEP 4 – AGGREGATION & CENTROID DEFUZZIFICATION
    # --------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor("#FFFFFF")

    # Aggregated shape (Max combination)
    ax4.fill_between(y_vals, 0, mu_aggregated, color=c_ink, alpha=0.35, label="Aggregated Fuzzy Set μ_Agg(y)")
    ax4.plot(y_vals, mu_aggregated, color=c_ink, lw=2.2)

    # Centroid line
    ax4.axvline(crisp_score, color=c_red, lw=3, linestyle="-",
                label=f"Defuzzified Centroid R* = {crisp_score:.1f}")

    # Annotate crisp result with an archival pin-style callout
    bbox_props = dict(boxstyle="round,pad=0.5", fc=c_paper, ec=c_ink, lw=1.8)
    ax4.text(
        crisp_score, 0.75,
        f"  R* = {crisp_score:.1f} / 100\n  Category: {risk_cat.upper()}  ",
        ha="center", va="center", color=c_ink, fontweight="bold", fontsize=11,
        bbox=bbox_props
    )

    ax4.set_title(f"Step 4: Centroid Defuzzification (R* = {crisp_score:.1f})", fontsize=13, fontweight="bold", color=c_ink, pad=8)
    ax4.set_xlabel("Risk Score Scale [0 - 100]", fontsize=11, color=c_ink)
    ax4.set_ylabel("Aggregated Truth μ_Agg(y)", fontsize=11, color=c_ink)
    ax4.set_ylim(-0.05, 1.15)
    ax4.legend(loc="upper left", framealpha=0.9, fontsize=9)
    ax4.grid(True, linestyle=":", alpha=0.5, color=c_ink)

    # Global Figure Title
    fig.suptitle(
        f"Mamdani Fuzzy Inference System (FIS) Workflow — {user_name}\n"
        f"Inputs: Age={age}y | Horizon={horizon_years}y | LossTol={loss_tolerance_val:.1f} | Result={crisp_score:.1f} ({risk_cat})",
        fontsize=15, fontweight="bold", color=c_ink, y=0.97
    )

    # Save to disk or buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=160, facecolor=fig.get_facecolor(), edgecolor="none")
    buf.seek(0)
    img_bytes = buf.getvalue()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(img_bytes)

    plt.close(fig)
    return img_bytes


def precompute_all_preset_plots():
    """
    Generates and saves visual Mamdani explanation plots for the 4 primary
    interactive persona templates in both frontend and web_demo asset directories.
    """
    presets = [
        {
            "id": "techie",
            "name": "Aarav Sharma (Young Tech Worker)",
            "age": 24,
            "horizon": 12,
            "loss_tol": 80.0,
            "income_stab": 90.0,
        },
        {
            "id": "family",
            "name": "Priya & Vikram Nair (Mid-Career Family)",
            "age": 38,
            "horizon": 8,
            "loss_tol": 50.0,
            "income_stab": 85.0,
        },
        {
            "id": "retiree",
            "name": "Col. K. R. Nambiar (Near-Retirement Senior)",
            "age": 68,
            "horizon": 3,
            "loss_tol": 20.0,
            "income_stab": 95.0,
        },
        {
            "id": "debt_stress",
            "name": "Sameer Sen (High Debt Stress)",
            "age": 29,
            "horizon": 4,
            "loss_tol": 30.0,
            "income_stab": 40.0,
        },
    ]

    base_dirs = [
        Path("frontend/assets"),
    ]

    for p in presets:
        for b in base_dirs:
            target = b / f"mamdani_{p['id']}.png"
            generate_mamdani_plot(
                age=p["age"],
                horizon_years=p["horizon"],
                loss_tolerance_val=p["loss_tol"],
                income_stability_val=p["income_stab"],
                user_name=p["name"],
                save_path=str(target),
            )
            print(f"[+] Generated Mamdani Plot -> {target}")


if __name__ == "__main__":
    precompute_all_preset_plots()
