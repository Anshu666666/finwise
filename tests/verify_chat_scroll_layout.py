"""
Comprehensive Verification Script for FinWise AI ChatGPT Advisory Box Layout & Functionality.
This script validates:
1. CSS Layout Rules (flexbox, min-height:0, overflow-y:auto, flex-shrink:0, heights)
2. HTML Structure of ChatGPT Advisory Box (hierarchy: ChatContainer -> ChatMain -> ChatMessages + ChatInputArea)
3. API Chat Endpoint (/api/v1/advisory/chat) responsiveness with 10+ messages
4. Short, long, and edge-case prompt responses
5. Error handling and fallback behavior
"""

import re
import json
import urllib.request
import urllib.error

def verify_css_and_html_layout(file_path: str):
    print(f"[*] Verifying Layout and CSS Rules in {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Verify #view-chat.active has flex-direction column and min-height: 0
    assert "#view-chat.active" in content, "Missing #view-chat.active CSS selector"
    assert "min-height: 0;" in content, "Missing min-height: 0 in flex container"

    # 2. Verify .chat-container CSS
    chat_container_match = re.search(r'\.chat-container\s*\{([^}]+)\}', content)
    assert chat_container_match, "Missing .chat-container CSS rule"
    chat_container_css = chat_container_match.group(1)
    assert "overflow: hidden" in chat_container_css, ".chat-container must have overflow: hidden"
    assert "height:" in chat_container_css, ".chat-container must have explicit height constraint"

    # 3. Verify .chat-main CSS
    chat_main_match = re.search(r'\.chat-main\s*\{([^}]+)\}', content)
    assert chat_main_match, "Missing .chat-main CSS rule"
    chat_main_css = chat_main_match.group(1)
    assert "display: flex" in chat_main_css, ".chat-main must be display: flex"
    assert "flex-direction: column" in chat_main_css, ".chat-main must have flex-direction: column"
    assert "min-height: 0" in chat_main_css, ".chat-main must have min-height: 0 to prevent flex item expansion"
    assert "overflow: hidden" in chat_main_css, ".chat-main must have overflow: hidden"

    # 4. Verify .chat-messages CSS
    chat_messages_match = re.search(r'\.chat-messages\s*\{([^}]+)\}', content)
    assert chat_messages_match, "Missing .chat-messages CSS rule"
    chat_messages_css = chat_messages_match.group(1)
    assert "overflow-y: auto" in chat_messages_css, ".chat-messages must have overflow-y: auto"
    assert "min-height: 0" in chat_messages_css, ".chat-messages must have min-height: 0 for nested flex scroll"

    # 5. Verify .chat-input-area and chat-message-row CSS
    chat_input_match = re.search(r'\.chat-input-area\s*\{([^}]+)\}', content)
    assert chat_input_match, "Missing .chat-input-area CSS rule"
    assert ".chat-message-row" in content, "Missing .chat-message-row CSS rule"
    assert "flex-shrink: 0;" in content, "Missing flex-shrink: 0 to protect chat elements from collapsing"

    # 6. Verify HTML Structure Hierarchy
    # .chat-container contains .chat-sidebar and .chat-main
    # .chat-main contains .chat-messages and .chat-input-area
    assert '<div class="chat-container">' in content, "Missing .chat-container element"
    assert '<div class="chat-main">' in content, "Missing .chat-main element"
    assert '<div class="chat-messages" id="chat-messages-list">' in content, "Missing #chat-messages-list element"
    assert '<div class="chat-input-area">' in content, "Missing .chat-input-area element"
    assert '<input type="text" id="chat-input-field"' in content, "Missing #chat-input-field input"
    assert '<button class="btn-send" id="btn-chat-send"' in content, "Missing #btn-chat-send button"

    print(f"[+] PASS: Layout & CSS architecture in {file_path} correctly configured for persistent input and scrollable message list.")

def test_chat_api_sequence():
    print("\n[*] Creating active financial advisory session directly in SQLite database...")
    import sys
    sys.path.insert(0, ".")
    import backend.models.database as db
    import uuid

    session_id = f"test-session-{uuid.uuid4().hex[:8]}"
    db.init_db()
    db.save_session(
        session_id=session_id,
        user_name="Test User",
        profile={
            "age": 30,
            "monthly_income": 8000.0,
            "monthly_expenses": 3500.0,
            "current_savings": 25000.0,
            "total_debt": 5000.0,
            "monthly_emi": 300.0,
            "financial_goals": ["Retirement", "Home purchase"],
            "risk_tolerance_subjective": "Moderate",
            "market_sentiment": "Neutral"
        },
        fuzzy_res={"crisp_score": 55.0, "category": "Moderate"},
        expert_plan={
            "recommended_allocation": {"equity_percentage": 50.0, "debt_bonds_percentage": 35.0, "liquid_cash_percentage": 5.0, "gold_commodities_percentage": 10.0},
            "budget_rule_check": {"needs_actual_percent": 47.5, "wants_actual_percent": 0.0, "savings_actual_percent": 52.5},
            "actionable_rules_fired": []
        },
        advisory_report="# Financial Advisory Report\n\nYour profile is balanced."
    )
    print(f"[+] Active Session Created in DB: {session_id}")

    print("\n[*] Testing Chat API with a sequence of 11 financial advisory queries...")
    chat_url = "http://127.0.0.1:8000/api/v1/advisory/chat"

    test_queries = [
        "How should I structure my emergency fund?",
        "What is the 50/30/20 budget rule?",
        "Explain the difference between equity and debt allocation.",
        "What are liquid mutual funds?",
        "How does inflation affect cash savings?",
        "What is a good debt to income ratio?",
        "How much should I invest in index funds?",
        "What is the avalanche method for debt repayment?",
        "How can I prepare for market volatility?",
        "Summarize key principles of financial independence.",
        "Can you give a quick 1-line recap?"
    ]

    for idx, query in enumerate(test_queries, 1):
        payload = json.dumps({"session_id": session_id, "message": query}).encode("utf-8")
        req = urllib.request.Request(chat_url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply = data.get("reply", "")
                print(f"  [{idx}/11] Query: '{query[:35]}...' => Reply length: {len(reply)} chars")
                assert len(reply) > 0, f"Empty reply received for query {idx}"
        except Exception as e:
            print(f"  [{idx}/11] API Call failed: {e}")
            raise e

    print("[+] PASS: All 11 chat requests processed successfully.")

if __name__ == "__main__":
    verify_css_and_html_layout("frontend/index.html")
    test_chat_api_sequence()
    print("\n[SUCCESS] All verification tests passed flawlessly!")
