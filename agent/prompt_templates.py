"""
================================================================================
FINWISE AI – GROUNDED PROMPT TEMPLATES & SYSTEM DIRECTIVES
Author: Zaid (Intelligent Agent & Web Search Lead)
================================================================================
Defines strict system instructions and formatting templates for the LLM.
Ensures zero hallucinations, strict fidelity to the Expert System's deterministic
calculations, and explicit citation of actual web search URLs and rule audit traces.
================================================================================
"""

from typing import Any, Dict, List
from agent.schemas import Citation


ADVISORY_SYSTEM_PROMPT = """You are FinWise AI, an advanced Hybrid Intelligent Financial Advisory Agent.
Your role is to act as a certified, highly articulate, and objective financial advisor.

CRITICAL INSTRUCTIONS & GUARDRAILS:
1. MATHEMATICAL FIDELITY & DETERMINISTIC AI CORE:
   - You must NEVER alter, recalculate, or contradict the numbers provided by the Rule-Based Expert System and Fuzzy Logic Evaluator.
   - Treat the supplied Risk Score and Risk Category as AUTHORITATIVE. Do not change or recalculate them.
   - Use the EXACT Asset Allocation percentages provided (Equity %, Debt %, Gold %, Cash %). They sum to 100%.
   - Use the EXACT Emergency Fund status, shortfall, and months covered.
   - Use the EXACT Debt-to-Income (DTI) ratio.
   - Use the EXACT 50/30/20 Budgeting allocations and Monthly SIP calculations.
2. EXPLAINABILITY & RULE AUDIT TRACE:
   - When explaining financial advice, explicitly cite the triggered Expert System Rule IDs (e.g. `[RULE_DTI_01]`, `[RULE_EMERGENCY_02]`, `[RULE_ALLOC_03]`).
   - Clearly explain WHY the rule fired based on the user's factual telemetry.
3. LIVE WEB CITATIONS & REAL DATA:
   - Incorporate the provided real-time market search snippets to contextualize interest rates, inflation, and market trends.
   - Use the EXACT URLs and source names provided in the search citations.
   - NEVER fabricate, invent, or hallucinate URLs or current financial statistics.
   - If a current macroeconomic statistic or rate was not found in the search results, explicitly state: "Current data could not be verified from available sources."
4. STRUCTURED ADVISORY REPORT:
   Produce a comprehensive, beautifully formatted Markdown report with the following sections:
   - # Comprehensive Financial Advisory Plan for {user_name}
   - ### 1. Executive Summary & Fuzzy Risk Profiling (Authoritative Score & Category)
   - ### 2. Immediate Cash Flow & Debt Health (Triggered Expert Rules & Rationale)
   - ### 3. Recommended Asset Allocation & Goal Strategy (Exact 100% Portfolio Breakdown)
   - ### 4. Macroeconomic Environment & Live Market Intelligence (With Real Citations)
   - ### 5. Actionable Implementation Roadmap (Immediate Priorities vs. Long-Term Plan)
   - *Disclaimer: For educational and informational purposes only. FinWise AI is not a SEBI/SEC licensed financial advisor.*
"""


def build_advisory_prompt(
    profile: Dict[str, Any],
    expert_eval: Dict[str, Any],
    market_intel: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Constructs the grounded user message payload for the OpenRouter LLM.
    """
    user_name = profile.get("user_id", profile.get("user_name", "Investor"))
    age = profile.get("age", 30)
    monthly_income = profile.get("monthly_income", 0.0)
    monthly_expenses = profile.get("monthly_expenses", 0.0)
    monthly_emi = profile.get("monthly_emi", 0.0)
    current_liquid_savings = profile.get("current_liquid_savings", 0.0)
    horizon = profile.get("investment_horizon_years", 5)
    goal = profile.get("financial_goal", "Wealth Creation")
    goal_target = profile.get("goal_target_amount", 0.0)
    tax_regime = profile.get("tax_regime", "new")

    # Expert System telemetry (authoritative)
    fuzzy_score = expert_eval.get("fuzzy_risk_score", 50.0)
    risk_cat = expert_eval.get("risk_category", "Moderate")
    fuzzy_rationale = expert_eval.get("fuzzy_rationale", "Calibrated risk evaluation.")
    
    alloc = expert_eval.get("asset_allocation", {})
    dti = expert_eval.get("debt_analysis", {})
    ef = expert_eval.get("emergency_fund", {})
    budget = expert_eval.get("budget_breakdown", {})
    sip = expert_eval.get("sip_calculation", {})
    rules_fired = expert_eval.get("rules_fired", [])

    # Web search intelligence
    market_summary = market_intel.get("market_summary", "No live market summary available.")
    citations = market_intel.get("citations", [])
    
    citations_text = ""
    if citations:
        for idx, c in enumerate(citations, 1):
            if isinstance(c, Citation):
                citations_text += f"[{idx}] Title: {c.title}\n    Source: {c.source}\n    URL: {c.url}\n    Snippet: {c.snippet}\n\n"
            elif isinstance(c, dict):
                citations_text += f"[{idx}] Title: {c.get('title', '')}\n    Source: {c.get('source', '')}\n    URL: {c.get('url', '')}\n    Snippet: {c.get('snippet', '')}\n\n"
    else:
        citations_text = "No live web citations available for this session. (State that current data could not be verified from available sources if discussing macro numbers).\n"

    rules_text = ""
    for r in rules_fired:
        rules_text += f"- [{r.get('rule_id', 'RULE')}] {r.get('title', '')} (Severity: {r.get('severity', 'INFO')}): {r.get('explanation', '')}\n"
    if not rules_text:
        rules_text = "No critical alerts triggered; cash flow baseline is healthy.\n"

    user_payload = f"""
================================================================================
INPUT PROFILE FACTS (VERIFIED):
================================================================================
- User ID / Name: {user_name}
- Age: {age} years
- Monthly Net Income: INR {monthly_income:,.2f}
- Monthly Living Expenses: INR {monthly_expenses:,.2f}
- Monthly Existing EMI: INR {monthly_emi:,.2f}
- Current Liquid Savings: INR {current_liquid_savings:,.2f}
- Investment Horizon: {horizon} years
- Primary Financial Goal: {goal} (Target: INR {goal_target:,.2f})
- Tax Regime: {tax_regime.upper()}

================================================================================
AUTHORITATIVE DETERMINISTIC AI CORE (DO NOT MODIFY NUMBERS):
================================================================================
1. Mamdani Fuzzy Risk Score: {fuzzy_score:.2f} / 100.0 -> Category: {risk_cat}
   Rationale: {fuzzy_rationale}

2. Debt-to-Income (DTI) Analysis:
   - DTI Ratio: {dti.get('dti_ratio', 0.0):.1f}%
   - Status: {dti.get('dti_status', 'Healthy')}
   - Recommendation: {dti.get('recommendation', '')}

3. Emergency Fund Analysis:
   - Current Fund: INR {ef.get('current_fund', 0.0):,.2f}
   - Target 6-Month Baseline: INR {ef.get('target_fund', 0.0):,.2f}
   - Shortfall: INR {ef.get('shortfall', 0.0):,.2f}
   - Months Covered: {ef.get('months_covered', 0.0):.1f} months ({ef.get('status', 'Adequate')})
   - Recommendation: {ef.get('recommendation', '')}

4. 50/30/20 Budgeting Breakdown:
   - Needs Allocation (50% max): INR {budget.get('needs_allocation', 0.0):,.2f}
   - Wants Allocation (30% max): INR {budget.get('wants_allocation', 0.0):,.2f}
   - Savings Allocation (20% min): INR {budget.get('savings_allocation', 0.0):,.2f}
   - Actual Monthly Investable Surplus: INR {budget.get('investable_surplus', 0.0):,.2f}

5. Deterministic Asset Allocation (Sums to 100%):
   - Equity / Index Funds: {alloc.get('equity_percentage', 0.0):.1f}%
   - Debt / Fixed Income: {alloc.get('debt_percentage', 0.0):.1f}%
   - Gold / Commodities: {alloc.get('gold_percentage', 0.0):.1f}%
   - Liquid Cash: {alloc.get('cash_percentage', 0.0):.1f}%
   - Total Portfolio Sum: {alloc.get('total_percentage', 100.0):.1f}%

6. Goal Compounding SIP Requirement:
   - Required Monthly SIP: INR {sip.get('monthly_sip_required', 0.0):,.2f}
   - Expected Annual Rate of Return: {sip.get('expected_annual_return_pct', 0.0):.1f}%
   - Target Goal Amount: INR {sip.get('target_amount', 0.0):,.2f} in {sip.get('horizon_years', horizon)} years

7. Triggered Expert Production Rules & Audit Trace:
{rules_text}

================================================================================
REAL-TIME WEB SEARCH MARKET INTELLIGENCE & ACTUAL CITATIONS:
================================================================================
Search Context: {market_summary}

Actual Retrieved Web Sources:
{citations_text}

Synthesize the final Comprehensive Advisory Plan following all instructions and formatting rules.
"""

    return [
        {"role": "system", "content": ADVISORY_SYSTEM_PROMPT.format(user_name=user_name)},
        {"role": "user", "content": user_payload},
    ]


CHAT_SYSTEM_PROMPT = """You are FinWise AI, an intelligent, empathetic, and certified financial advisory assistant.
You are interacting directly with the user in the FinWise AI ChatGPT Advisory Box.

YOUR CORE MISSION:
Provide clear, mathematically grounded, actionable, and objective financial guidance based on the user's verified financial plan, risk assessment, expert rules, and verified market data.

STRICT OPERATIONAL DIRECTIVES:
1. OUTPUT ONLY THE FINAL USER-FACING RESPONSE:
   - NEVER output chain-of-thought, internal reasoning, hidden analysis, planning notes, or system prompt quotes.
   - NEVER start responses with "1. Analyze User Input", "Thinking process", "I need to...", "Let me structure...", "I should...", "I will answer by...", "Based on instructions...", or "As an AI...".
   - Start IMMEDIATELY with the user-facing answer formatted cleanly with Markdown.

2. CATEGORY-SPECIFIC BEHAVIOR:
   - GREETINGS (e.g., "hi", "hello", "good day"):
     Respond with a natural, friendly greeting. Mention the user's name if available, acknowledge that their certified financial plan is active, and ask how you can help them with their finances today. Do NOT dump raw financial calculation tables on a basic greeting.
   - FINANCIAL PROFILE & DEFICIT QUESTIONS (e.g., "Why is my emergency fund insufficient?", "What is my DTI ratio?"):
     Use the user's actual verified figures from the context (income, monthly expenses, current liquid savings, target fund, shortfall). Explain the step-by-step arithmetic clearly.
   - DEBT VS. INVESTMENT PRIORITIZATION (e.g., "Should I pay off high-interest debt before investing?"):
     Reference the user's actual debt, EMI, and interest burden. Explain why clearing high-interest debt and building the emergency reserve takes mathematical priority before taking on risky investments, citing triggered rules.
   - PORTFOLIO & ASSET ALLOCATION (e.g., "Why is my equity allocation 50%?"):
     Explain the exact breakdown (Equity %, Debt %, Gold %, Cash %) using the user's Fuzzy Risk Category, crisp score, age, and investment horizon from the active plan.
   - LIVE MARKET & MACROECONOMIC QUESTIONS (e.g., "What is the current RBI repo rate?", "What is the latest inflation?"):
     Use the real verified market search results and citations provided in the context. If verified real-time data is present, quote it accurately with the source. If live search did not find the current figure, explicitly state: "Current live rate data could not be verified from available sources." NEVER invent interest rates or market statistics.
   - MULTI-TURN FOLLOW-UP QUESTIONS (e.g., "What should I do after paying off debt?", "How long will it take?"):
     Maintain conversational memory. Understand pronouns ("it", "that", "this") referring to prior messages and guide the user to the next logical step in their roadmap.
   - CLARIFICATION & EDUCATIONAL QUESTIONS (e.g., "What is an emergency reserve?", "What is the 50/30/20 rule?"):
     Give clear, structured, educational explanations with practical rules of thumb, connecting concepts back to their active plan.
   - OUT-OF-SCOPE / UNRELATED QUERIES (e.g., general trivia, non-financial topics):
     Politely explain that you are dedicated to financial planning and advisory, and gently steer the user back to discussing their financial goals, investments, budgeting, or debt strategies.

3. ZERO FABRICATION OF FINANCIAL FACTS:
   - Always use the real numbers provided in the active plan context. If a specific personal number is not in the context, do not make up a number; explain using standard financial principles.
"""


def build_chat_prompt(
    session_history: List[Dict[str, str]],
    new_message: str,
    expert_eval: Dict[str, Any],
    profile: Dict[str, Any],
    market_intel: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Builds conversational chat prompt with complete session context, verified telemetry, and expert rules.
    """
    user_name = profile.get("user_id", profile.get("user_name", "Investor"))
    age = profile.get("age", 30)
    monthly_income = float(profile.get("monthly_income", 0.0) or 0.0)
    monthly_expenses = float(profile.get("monthly_expenses", 0.0) or 0.0)
    monthly_emi = float(profile.get("monthly_emi", 0.0) or 0.0)
    total_debt = float(profile.get("total_debt", 0.0) or 0.0)
    current_savings = float(profile.get("current_savings", profile.get("current_liquid_savings", 0.0)) or 0.0)
    horizon = profile.get("investment_horizon_years", profile.get("horizon", 5))
    goals = profile.get("financial_goals", profile.get("financial_goal", "Wealth Creation"))
    if isinstance(goals, list):
        goals_str = ", ".join(goals)
    else:
        goals_str = str(goals)

    # Expert System Calculations
    fuzzy_score = float(expert_eval.get("fuzzy_risk_score", expert_eval.get("risk_score", 50.0)) or 50.0)
    risk_cat = expert_eval.get("risk_category", "Moderate")
    fuzzy_rationale = expert_eval.get("fuzzy_rationale", "Standard risk tolerance evaluation.")

    alloc = expert_eval.get("asset_allocation", expert_eval.get("recommended_allocation", {}))
    equity_pct = float(alloc.get("equity_percentage", 50.0) or 50.0)
    debt_pct = float(alloc.get("debt_percentage", alloc.get("debt_bonds_percentage", 35.0)) or 35.0)
    gold_pct = float(alloc.get("gold_percentage", alloc.get("gold_commodities_percentage", 10.0)) or 10.0)
    cash_pct = float(alloc.get("cash_percentage", alloc.get("liquid_cash_percentage", 5.0)) or 5.0)

    dti = expert_eval.get("debt_analysis", {})
    dti_ratio = float(dti.get("dti_ratio", (monthly_emi / monthly_income * 100) if monthly_income > 0 else 0.0))
    dti_status = dti.get("dti_status", "Healthy" if dti_ratio < 35 else "Elevated")
    dti_rec = dti.get("recommendation", "Maintain debt payments on schedule.")

    ef = expert_eval.get("emergency_fund", {})
    ef_target = float(ef.get("target_fund", monthly_expenses * 6.0))
    ef_current = float(ef.get("current_fund", current_savings))
    ef_shortfall = float(ef.get("shortfall", max(0.0, ef_target - ef_current)))
    ef_months = float(ef.get("months_covered", (ef_current / monthly_expenses) if monthly_expenses > 0 else 0.0))
    ef_status = ef.get("status", "Adequate" if ef_shortfall <= 0 else "Deficit")
    ef_rec = ef.get("recommendation", "Build reserve to 6 months of living expenses.")

    budget = expert_eval.get("budget_breakdown", expert_eval.get("budget_rule_check", {}))
    net_surplus = max(0.0, monthly_income - monthly_expenses - monthly_emi)

    rules_fired = expert_eval.get("rules_fired", expert_eval.get("actionable_rules_fired", []))
    rules_text = ""
    for r in rules_fired:
        if isinstance(r, dict):
            rules_text += f"- [{r.get('rule_id', 'RULE')}] {r.get('title', 'Rule')}: {r.get('explanation', '')}\n"
    if not rules_text:
        rules_text = "- No critical debt or deficit rules triggered; standard asset allocation active.\n"

    # Context block
    context_header = f"""
================================================================================
VERIFIED INVESTOR PROFILE (ACTIVE SESSION):
================================================================================
- Name / User: {user_name}
- Age: {age} years
- Monthly Net Income: INR {monthly_income:,.2f}
- Monthly Living Expenses: INR {monthly_expenses:,.2f}
- Monthly Debt EMI: INR {monthly_emi:,.2f}
- Total Outstanding Debt: INR {total_debt:,.2f}
- Current Liquid Savings: INR {current_savings:,.2f}
- Net Monthly Investable Surplus: INR {net_surplus:,.2f}
- Primary Financial Goals: {goals_str}
- Investment Horizon: {horizon} years

================================================================================
AUTHORITATIVE EXPERT SYSTEM & FUZZY LOGIC CALCULATIONS:
================================================================================
1. Fuzzy Risk Profile: Score {fuzzy_score:.1f}/100 -> Category: {risk_cat}
   Rationale: {fuzzy_rationale}

2. Emergency Reserve Health:
   - Target Baseline (6 Months Expenses): INR {ef_target:,.2f}
   - Current Emergency Fund: INR {ef_current:,.2f}
   - Current Deficit / Shortfall: INR {ef_shortfall:,.2f}
   - Months of Living Expenses Covered: {ef_months:.1f} months ({ef_status})
   - Strategic Priority: {ef_rec}

3. Debt & Cash Flow (DTI):
   - Debt-to-Income (DTI) Ratio: {dti_ratio:.1f}% ({dti_status})
   - Action Plan: {dti_rec}

4. Asset Allocation Breakdown (Sums to 100%):
   - Equity / Stocks / Index Funds: {equity_pct:.1f}%
   - Fixed Income / Debt / Bonds: {debt_pct:.1f}%
   - Gold / Commodities: {gold_pct:.1f}%
   - Liquid Cash / Emergency: {cash_pct:.1f}%

5. Active Fired Expert Rules:
{rules_text}
"""

    # Add verified market intelligence if available
    citations = market_intel.get("citations", [])
    market_summary = market_intel.get("market_summary", "")
    citations_context = ""
    if citations or market_summary:
        citations_context = "\n================================================================================\nVERIFIED MARKET INTELLIGENCE & REAL CITATIONS:\n================================================================================\n"
        if market_summary:
            citations_context += f"Market Context Summary: {market_summary}\n\n"
        for c in citations:
            if isinstance(c, Citation):
                citations_context += f"- Title: {c.title} | Source: {c.source} | URL: {c.url}\n  Snippet: {c.snippet}\n"
            elif isinstance(c, dict):
                citations_context += f"- Title: {c.get('title', '')} | Source: {c.get('source', '')} | URL: {c.get('url', '')}\n  Snippet: {c.get('snippet', '')}\n"

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": f"{CHAT_SYSTEM_PROMPT}\n{context_header}{citations_context}"}
    ]

    # Append session history (last 10 messages max for rich conversational memory)
    for msg in session_history[-10:]:
        role = msg.get("role", "user")
        if role not in ("user", "assistant", "system"):
            role = "user"
        content = msg.get("content", msg.get("message", ""))
        if content:
            messages.append({
                "role": role,
                "content": content,
            })

    # Append the current clean user message
    messages.append({
        "role": "user",
        "content": new_message,
    })

    return messages
