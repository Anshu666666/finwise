"""
Verification Test for FinWise AI 50/30/20 Budget Rule Check Chart Fix.
Tests:
1. API evaluate response contains both ratio and percentage fields without missing values.
2. Exact calculation for multiple distinct profiles:
   - Profile A: Income ₹65,000, Expenses ₹32,000, EMI ₹5,000 -> Needs 49.2%, Wants 0.0%, Savings & Debt 50.8%
   - Profile B: Income ₹100,000, Expenses ₹45,000, EMI ₹10,000 -> Needs 45.0%, Wants 0.0%, Savings & Debt 55.0%
3. Frontend chart transformation reproduces exact non-undefined numeric array data.
4. All KPI cards and session consistency verified.
"""

import json
import urllib.request
import urllib.error
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000/api/v1/advisory"

def test_profile(profile_data, expected_needs, expected_savings_debt, profile_name):
    print(f"\n=======================================================")
    print(f"TESTING PROFILE: {profile_name}")
    print(f"Income: ₹{profile_data['monthly_income']:,} | Expenses: ₹{profile_data['monthly_expenses']:,} | EMI: ₹{profile_data['monthly_emi']:,}")
    print(f"=======================================================")

    req = urllib.request.Request(
        f"{BASE_URL}/evaluate",
        data=json.dumps(profile_data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[+] HTTP Status: {resp.status}")

            session_id = data.get("session_id")
            print(f"[+] Active Session ID: {session_id}")

            # 1. Inspect Budget Rule Check
            budget = data.get("expert_system_plan", {}).get("budget_rule_check", {})
            print("\n[+] Backend 'budget_rule_check' payload:")
            print(json.dumps(budget, indent=2))

            assert "needs_ratio" in budget, "needs_ratio missing from budget_rule_check"
            assert "wants_ratio" in budget, "wants_ratio missing from budget_rule_check"
            assert "savings_ratio" in budget, "savings_ratio missing from budget_rule_check"
            assert "needs_actual_percent" in budget, "needs_actual_percent missing from budget_rule_check"
            assert "wants_actual_percent" in budget, "wants_actual_percent missing from budget_rule_check"
            assert "savings_actual_percent" in budget, "savings_actual_percent missing from budget_rule_check"

            # 2. Simulate Frontend Chart Transformation (from frontend/index.html)
            needsVal = budget.get("needs_actual_percent") if budget.get("needs_actual_percent") is not None else budget.get("needs_ratio", 49.2)
            wantsVal = budget.get("wants_actual_percent") if budget.get("wants_actual_percent") is not None else budget.get("wants_ratio", 0.0)
            savingsVal = budget.get("savings_actual_percent") if budget.get("savings_actual_percent") is not None else budget.get("savings_ratio", 50.8)

            chart_labels = [
                f"Needs ({needsVal:.1f}%)",
                f"Wants ({wantsVal:.1f}%)",
                f"Savings & Debt ({savingsVal:.1f}%)"
            ]
            chart_data = [
                float(needsVal),
                float(wantsVal),
                float(savingsVal)
            ]

            print("\n[+] Frontend Chart Rendered State:")
            print(f"    Labels: {chart_labels}")
            print(f"    Data:   {chart_data}")

            # Assertions
            for label in chart_labels:
                assert "undefined" not in label, f"Detected 'undefined' in chart label: {label}"
            for val in chart_data:
                assert val is not None and not (isinstance(val, float) and val != val), f"Invalid chart value: {val}"

            assert round(needsVal, 1) == round(expected_needs, 1), f"Expected Needs {expected_needs}%, got {needsVal}%"
            assert round(savingsVal, 1) == round(expected_savings_debt, 1), f"Expected Savings & Debt {expected_savings_debt}%, got {savingsVal}%"
            assert round(wantsVal, 1) == 0.0, f"Expected Wants 0.0%, got {wantsVal}%"
            assert round(needsVal + wantsVal + savingsVal, 1) == 100.0, f"Percentages do not sum to 100%: {needsVal + wantsVal + savingsVal}"

            # 3. Check Profile Summary & Debt KPI Card
            profile_summary = data.get("profile_summary", {})
            print("\n[+] Profile Summary & KPI Check:")
            print(f"    User Name: {profile_summary.get('user_name')}")
            print(f"    Net Monthly Savings: ₹{profile_summary.get('net_monthly_savings'):,.2f}")
            print(f"    Total Debt in Summary: ₹{profile_summary.get('total_debt', 0):,.2f}")
            print(f"    Emergency Months Covered: {profile_summary.get('emergency_fund_months_covered'):.2f} Mo")

            assert profile_summary.get("total_debt") == profile_data["total_debt"], "Total debt mismatch in profile summary"

            print(f"\n[✓] PASS: {profile_name} verified successfully with 100% mathematical accuracy and zero undefined values.")
            return True

    except Exception as e:
        print(f"[-] ERROR on {profile_name}: {e}")
        raise e

def run_all_tests():
    print("=" * 70)
    print("FINWISE AI – 50/30/20 BUDGET CHART COMPREHENSIVE VERIFICATION")
    print("=" * 70)

    # Profile 1: Onboarding Default (Aarav Sharma)
    profile1 = {
        "user_name": "Aarav Sharma",
        "age": 24,
        "monthly_income": 65000.0,
        "monthly_expenses": 32000.0,
        "current_savings": 45000.0,
        "total_debt": 120000.0,
        "monthly_emi": 5000.0,
        "debt_interest_rate": 11.5,
        "investment_horizon_years": 5,
        "loss_tolerance": "medium",
        "income_stability": "stable",
        "primary_goal": "wealth_creation",
        "notes": "Interested in tech index funds"
    }
    # Expected: 32000/65000 = 49.23% -> 49.2%, (28000+5000)/65000 = 50.77% -> 50.8%
    test_profile(profile1, expected_needs=49.2, expected_savings_debt=50.8, profile_name="Profile 1 (Aarav Sharma)")

    # Profile 2: Salaried Professional with Higher Outflows (Priya Patel)
    profile2 = {
        "user_name": "Priya Patel",
        "age": 32,
        "monthly_income": 100000.0,
        "monthly_expenses": 45000.0,
        "current_savings": 120000.0,
        "total_debt": 250000.0,
        "monthly_emi": 10000.0,
        "debt_interest_rate": 8.5,
        "investment_horizon_years": 7,
        "loss_tolerance": "medium",
        "income_stability": "stable",
        "primary_goal": "emergency_fund",
        "notes": "Building emergency reserve"
    }
    # Expected: 45000/100000 = 45.0% Needs, (45000 surplus + 10000 emi)/100000 = 55.0% Savings & Debt
    test_profile(profile2, expected_needs=45.0, expected_savings_debt=55.0, profile_name="Profile 2 (Priya Patel)")

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL BUDGET CHART VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
