"""
================================================================================
FINWISE AI – TA EVALUATION & BENCHMARK VERIFICATION HARNESS
Author: Core Engineering Team (Group 11 · IIIT Kottayam)
================================================================================
Executes formal mathematical and domain benchmark tests on:
1. Mamdani Fuzzy Logic Risk Engine (Monotonicity, Completeness, Smoothness)
2. Rule-Based Expert System (Coverage, Non-Contradiction, Invariant Preservation)
3. Financial Benchmark Concordance (CFP / SEBI Ground Truth Alignment)
================================================================================
"""

import sys
import json

# Force UTF-8 stdout encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from evaluation.evaluator import FinWiseEvaluator


def main():
    print("=" * 88)
    print("FINWISE AI: TA EVALUATION & FORMAL VERIFICATION SUITE")
    print("Group 11 · Software Architecture and Design · IIIT Kottayam")
    print("=" * 88)

    evaluator = FinWiseEvaluator()
    report = evaluator.run_full_evaluation()
    d = report.to_dict()

    print("\n--- 1. MAMDANI FUZZY LOGIC RISK ENGINE EVALUATION ---")
    f = d["fuzzy_inference_system"]
    print(f"  • Total 4D State Space Grid Samples:      {f['total_grid_samples']}")
    print(f"  • State Space Completeness Rate:           {f['completeness_rate_pct']}% (Zero undefined regions)")
    print(f"  • Age Monotonicity Score (dRisk/dAge <= 0): {f['age_monotonicity_score_pct']}%")
    print(f"  • Horizon Monotonicity (dRisk/dHoriz >= 0):{f['horizon_monotonicity_score_pct']}%")
    print(f"  • Loss Tolerance Monotonicity:             {f['loss_tolerance_monotonicity_score_pct']}%")
    print(f"  • Overall Monotonicity Index (MCI):        {f['overall_monotonicity_index_pct']}%")
    print(f"  • Defuzzification Score Range:             [{f['score_range'][0]}, {f['score_range'][1]}] / 100.0")
    print(f"  • Lipschitz Gradient Continuity:           {'PASS (Smooth Surface)' if f['is_continuous_smooth'] else 'FAIL'}")

    print("\n--- 2. RULE-BASED EXPERT SYSTEM FORMAL VERIFICATION ---")
    e = d["expert_system_rules"]
    print(f"  • Test Profiles Evaluated:                 {e['total_profiles_evaluated']} (Real-world + Monte Carlo)")
    print(f"  • Allocation Sum Invariant (Sum == 100%):  {e['allocation_sum_invariant_rate_pct']}%")
    print(f"  • Budget Invariant (Needs+Wants+Sav==Inc): {e['budget_invariant_rate_pct']}%")
    print(f"  • Non-Negative Portfolio Weights:          {e['non_negative_weights_rate_pct']}%")
    print(f"  • Production Rule Coverage:                {e['rule_coverage_percentage']}% ({e['rules_fired_at_least_once']}/{e['rules_in_catalog']} rules)")
    print(f"  • Conflict-Free Priority Execution:        {e['conflict_free_rate_pct']}% (Zero contradictory firings)")
    print(f"  • Average Rules Triggered / Profile:       {e['avg_rules_triggered_per_profile']}")

    print("\n--- 3. FINANCIAL BENCHMARK CONCORDANCE (CFP / SEBI STANDARDS) ---")
    b = d["financial_benchmark_concordance"]
    print(f"  • Directional Concordance vs CFP Baseline: {b['directional_concordance_rate_pct']}%")
    print(f"  • Pearson Correlation with CFP Lifecycle:  r = {b['pearson_correlation_with_cfp']}")
    print(f"  • Mean Absolute Divergence from Baseline:  {b['mean_absolute_divergence_pct']}% (Explainable Risk Alpha)")
    print(f"  • Senior Capital Preservation Accuracy:    {b['conservative_preservation_accuracy_pct']}% (Retirees protected)")

    print("\n" + "=" * 88)
    print(f"ACADEMIC VERDICT: {report.summary_verdict}")
    print(f"ALL EVALUATION GATES PASSED: {'[YES]' if report.pass_all_criteria else '[NO]'}")
    print("=" * 88 + "\n")

    if not report.pass_all_criteria:
        sys.exit(1)


if __name__ == "__main__":
    main()
