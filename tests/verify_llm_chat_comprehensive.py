"""
Comprehensive Test Suite for FinWise AI ChatGPT Advisory Box LLM Response Handling.
Tests all 10 user message categories required by the specification:
1. Greetings ("hi")
2. Financial Deficit ("What is my emergency fund deficit?")
3. Debt Prioritization ("Why should I pay my high-interest debt first?")
4. Portfolio Allocation ("Explain my equity allocation.")
5. Post-Debt Follow-up ("What should I do after paying off my debt?")
6. Live Market Rates ("What is the current RBI repo rate?")
7. Pronoun Follow-up ("How long will it take me to build it?")
8. Unrelated Questions ("What is the capital of France?")
9. Exact User Numbers ("How much do I spend on monthly living expenses and debt EMI?")
10. Complex Financial Scenario ("Given my profile, if I receive a bonus of INR 100,000, how should I allocate it?")
"""

import re
import sys
import json
import uuid
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

LEAKED_REASONING_PATTERNS = [
    r"<think>", r"</think>",
    r"<thought>", r"</thought>",
    r"<reasoning>", r"</reasoning>",
    r"\[THINKING\]", r"\[/THINKING\]",
    r"^i need to ",
    r"^let me structure",
    r"^i should acknowledge",
    r"^i will answer by",
    r"^based on my instructions",
    r"^here'?s a thinking process",
    r"^thinking process:",
    r"^thought process:",
]

def check_no_reasoning_leakage(text: str, category_name: str):
    for pattern in LEAKED_REASONING_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            raise AssertionError(f"[{category_name}] Leaked reasoning detected matching '{pattern}': {match.group(0)}")

def run_chat_tests():
    import sys
    sys.path.insert(0, ".")
    import backend.models.database as db

    print("=" * 80)
    print("FINWISE AI – COMPREHENSIVE LLM CHAT ADVISORY TEST SUITE")
    print("=" * 80)

    # 1. Setup a realistic active financial advisory session in SQLite DB
    session_id = f"test-adv-session-{uuid.uuid4().hex[:8]}"
    db.init_db()

    profile = {
        "user_name": "Aarav Sharma",
        "age": 32,
        "monthly_income": 95000.0,
        "monthly_expenses": 42000.0,
        "monthly_emi": 15000.0,
        "total_debt": 250000.0,
        "current_savings": 60000.0,
        "investment_horizon_years": 7,
        "financial_goals": ["Retirement Wealth", "Child Education Fund"],
        "risk_tolerance_subjective": "Moderate",
        "market_sentiment": "Neutral"
    }

    fuzzy_res = {
        "crisp_score": 54.5,
        "category": "Moderate",
        "rationale": "Moderate risk profile calibrated from stable professional income, 7-year horizon, and active debt obligations."
    }

    expert_plan = {
        "recommended_allocation": {
            "equity_percentage": 50.0,
            "debt_bonds_percentage": 35.0,
            "liquid_cash_percentage": 5.0,
            "gold_commodities_percentage": 10.0
        },
        "asset_allocation": {
            "equity_percentage": 50.0,
            "debt_percentage": 35.0,
            "gold_percentage": 10.0,
            "cash_percentage": 5.0
        },
        "emergency_fund": {
            "current_fund": 60000.0,
            "target_fund": 252000.0,  # 42,000 * 6
            "shortfall": 192000.0,    # 252,000 - 60,000
            "months_covered": 1.4,
            "status": "Critical Deficit",
            "recommendation": "Allocate surplus to liquid funds until 6 months (INR 2,52,000) is reached."
        },
        "debt_analysis": {
            "dti_ratio": 15.8,  # (15,000 / 95,000) * 100
            "dti_status": "Manageable",
            "recommendation": "Accelerate repayment of high-interest portion before aggressive equity exposure.",
            "total_debt": 250000.0
        },
        "budget_breakdown": {
            "needs_allocation": 47500.0,
            "wants_allocation": 28500.0,
            "savings_allocation": 19000.0,
            "investable_surplus": 38000.0
        },
        "actionable_rules_fired": [
            {
                "rule_id": "RULE_EMERGENCY_01",
                "title": "Severe Emergency Reserve Shortfall",
                "severity": "CRITICAL",
                "explanation": "Liquid savings cover only 1.4 months vs 6.0 months target (INR 1,92,000 deficit)."
            },
            {
                "rule_id": "RULE_DEBT_AVALANCHE",
                "title": "High-Interest Debt Prioritization",
                "severity": "HIGH",
                "explanation": "Guaranteed debt interest savings mathematically outperform expected market equity returns."
            }
        ]
    }

    db.save_session(
        session_id=session_id,
        user_name="Aarav Sharma",
        profile=profile,
        fuzzy_res=fuzzy_res,
        expert_plan=expert_plan,
        advisory_report="# Financial Advisory Plan for Aarav Sharma\n\nVerified plan loaded."
    )
    print(f"[+] Active Session Created in DB: {session_id}")

    chat_url = "http://127.0.0.1:8000/api/v1/advisory/chat"

    test_scenarios = [
        (
            "1. Natural Greeting",
            "hi",
            lambda r: any(w in r.lower() for w in ["aarav", "hello", "hi", "assist", "welcome", "help"]) and len(r) < 800
        ),
        (
            "2. Emergency Fund Deficit Calculation",
            "What is my emergency fund deficit?",
            lambda r: any(w in r for w in ["1,92,000", "192000", "1.4", "2,52,000", "252000", "60,000", "60000", "42,000", "6 months"])
        ),
        (
            "3. Debt Prioritization Reasoning",
            "Why should I pay my high-interest debt first?",
            lambda r: any(w in r.lower() for w in ["debt", "interest", "guaranteed", "priority", "emergency", "avalanche"])
        ),
        (
            "4. Portfolio Allocation Explanation",
            "Explain my equity allocation.",
            lambda r: any(w in r for w in ["50%", "50.0%", "50 percent", "moderate", "Moderate"])
        ),
        (
            "5. Post-Debt Follow-up Strategy",
            "What should I do after paying off my debt?",
            lambda r: any(w in r.lower() for w in ["emergency", "fund", "sip", "equity", "invest", "surplus", "allocation"])
        ),
        (
            "6. Live Macro / RBI Repo Rate Inquiry",
            "What is the current RBI repo rate?",
            lambda r: any(w in r.lower() for w in ["rbi", "repo", "6.5", "rate", "percent", "monetary"])
        ),
        (
            "7. Pronoun Multi-turn Context",
            "How long will it take me to build it?",
            lambda r: any(w in r.lower() for w in ["month", "surplus", "emergency", "save", "year", "target"])
        ),
        (
            "8. Out-of-Scope Politeness & Scope Redirection",
            "What is the capital of France?",
            lambda r: any(w in r.lower() for w in ["paris", "financial", "advisory", "assist", "planning", "scope"])
        ),
        (
            "9. Exact Profile Telemetry Grounding",
            "How much do I spend on monthly living expenses and debt EMI?",
            lambda r: any(w in r for w in ["42,000", "42000", "15,000", "15000"])
        ),
        (
            "10. Complex Scenario / Bonus Allocation",
            "Given my profile, if I receive a bonus of INR 100,000, how should I prioritize it?",
            lambda r: any(w in r.lower() for w in ["emergency", "debt", "fund", "shortfall", "allocate", "priority"])
        )
    ]

    for idx, (name, prompt, validator) in enumerate(test_scenarios, 1):
        print(f"\n--- [Test {idx}/10] {name} ---")
        print(f"User: '{prompt}'")

        payload = json.dumps({"session_id": session_id, "message": prompt}).encode("utf-8")
        req = urllib.request.Request(chat_url, data=payload, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply = data.get("reply", "")
                print(f"Assistant Response ({len(reply)} chars):")
                print("-" * 50)
                print(reply[:300] + ("..." if len(reply) > 300 else ""))
                print("-" * 50)

                # Assertions
                assert len(reply.strip()) > 0, f"Empty reply on test {idx}"
                check_no_reasoning_leakage(reply, name)
                is_valid = validator(reply)
                if not is_valid:
                    print(f"[!] Warning on validation check for test {idx}, response was: {reply}")
                assert is_valid, f"Response content validation failed for test {idx}: {name}"
                print(f"[+] PASS: {name}")

        except Exception as e:
            print(f"[-] FAILED on test {idx} ({name}): {e}")
            raise e

    print("\n" + "=" * 80)
    print("[SUCCESS] ALL 10 CATEGORY TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    run_chat_tests()
