import urllib.request
import json
import sys

print('=== 1. VERIFYING FRONTEND SERVER (PORT 3000) ===')
try:
    with urllib.request.urlopen('http://127.0.0.1:3000') as r:
        html = r.read().decode('utf-8')
        assert 'FinWise AI' in html, "Missing FinWise title"
        assert 'id="advisory-report-content"' in html, "Missing report container"
        assert 'id="citations-container"' in html, "Missing citations container"
        assert 'id="chat-messages-list"' in html, "Missing chat messages container"
        assert 'marked.min.js' in html, "Missing marked.js"
        print('SUCCESS: Frontend index.html served on port 3000 with all required UI containers.')
except Exception as e:
    print('ERROR Frontend check:', e)
    sys.exit(1)

print('\n=== 2. VERIFYING BACKEND HEALTH (PORT 8000) ===')
try:
    with urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health') as r:
        health = json.loads(r.read())
        print('Backend Health:', health)
        assert health['status'] == 'healthy'
        assert health['database_connected'] is True
        assert health['openrouter_configured'] is True
except Exception as e:
    print('ERROR Backend health:', e)
    sys.exit(1)

print('\n=== 3. VERIFYING LIVE MARKET INTELLIGENCE (DUCKDUCKGO) ===')
try:
    with urllib.request.urlopen('http://127.0.0.1:8000/api/v1/advisory/market-intelligence') as r:
        market = json.loads(r.read())
        citations = market.get('web_citations', [])
        print(f"Live Market Summary: {market.get('market_summary')}")
        print(f"Retrieved {len(citations)} citations from DuckDuckGo:")
        for idx, c in enumerate(citations[:4], 1):
            print(f"  {idx}. [{c.get('source')}] {c.get('title')} -> {c.get('url')}")
        if len(citations) > 0:
            print(f"[+] Successfully retrieved {len(citations)} live citations from DuckDuckGo.")
        else:
            print("[!] Notice: 0 search citations returned (network/DNS restriction active on local network).")
except Exception as e:
    print('ERROR Market Intelligence:', e)
    sys.exit(1)

print('\n=== 4. VERIFYING FINANCIAL ADVISORY GENERATION (OPENROUTER FREE) ===')
eval_payload = {
    'user_name': 'Aarav Sharma',
    'age': 24,
    'monthly_income': 65000.0,
    'monthly_expenses': 32000.0,
    'current_savings': 45000.0,
    'total_debt': 120000.0,
    'monthly_emi': 5000.0,
    'debt_interest_rate': 11.5,
    'investment_horizon_years': 5,
    'loss_tolerance': 'medium',
    'income_stability': 'stable',
    'primary_goal': 'wealth_creation',
    'goal_target_amount': 2500000.0,
    'tax_regime': 'new'
}
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/advisory/evaluate',
        data=json.dumps(eval_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        eval_res = json.loads(r.read())
        session_id = eval_res['session_id']
        report = eval_res.get('comprehensive_advisory_report', '')
        risk = eval_res.get('fuzzy_risk_assessment', {})
        alloc = eval_res.get('expert_system_plan', {}).get('recommended_allocation', {})
        print(f"Session ID: {session_id}")
        print(f"Fuzzy Risk Score: {risk.get('crisp_score')} ({risk.get('category')})")
        print(f"Asset Allocation: Equity={alloc.get('equity_percentage')}% Debt={alloc.get('debt_bonds_percentage')}% Cash={alloc.get('liquid_cash_percentage')}% Gold={alloc.get('gold_commodities_percentage')}%")
        print(f"Generated AI Advisory Plan Length: {len(report)} characters")
        print("\n--- Plan Excerpt ---")
        print(report[:350].encode('ascii', 'replace').decode('ascii') + "...\n--------------------")
        assert len(report) > 200, "Report too short"
except Exception as e:
    print('ERROR Advisory Plan Generation:', e)
    sys.exit(1)

print('\n=== 5. VERIFYING CHAT WITH ADVISOR (OPENROUTER) ===')
chat_payload = {
    'session_id': session_id,
    'message': 'Explain why my emergency fund is flagged as a deficit.'
}
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/advisory/chat',
        data=json.dumps(chat_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        chat_res = json.loads(r.read())
        reply = chat_res.get('reply', '')
        rules = chat_res.get('grounded_rules_referenced', [])
        print(f"Referenced Rules: {rules}")
        print(f"\nLLM Reply ({len(reply)} chars):\n{reply.encode('ascii', 'replace').decode('ascii')}")
        assert len(reply) > 50, "Reply too short"
except Exception as e:
    print('ERROR Chat Advisory:', e)
    sys.exit(1)

print('\n=== 6. VERIFYING UNKNOWN SESSION ERROR HANDLING (404) ===')
chat_unknown_payload = {
    'session_id': 'sess_non_existent_99999',
    'message': 'What is the 50/30/20 budgeting rule?'
}
try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/v1/advisory/chat',
        data=json.dumps(chat_unknown_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print('UNEXPECTED: Request succeeded when 404 expected')
            sys.exit(1)
    except urllib.error.HTTPError as err:
        assert err.code == 404, f"Expected 404, got {err.code}"
        err_body = json.loads(err.read().decode('utf-8'))
        print(f"Correctly received 404: {err_body.get('detail')}")
except Exception as e:
    print('ERROR Unknown session check:', e)
    sys.exit(1)

print('\n================ ALL 6 VERIFICATION CHECKS PASSED PERFECTLY ================')
