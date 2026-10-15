import sys
sys.path.insert(0, ".")
from fastapi.testclient import TestClient
from backend.main import app

def test_eval_and_app():
    client = TestClient(app)

    # 1. Test /api/v1/health
    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200, f"Health check failed: {r_health.text}"
    print("[+] /api/v1/health OK:", r_health.json()["status"])

    # 2. Test /api/v1/advisory/evaluation-metrics
    r_eval = client.get("/api/v1/advisory/evaluation-metrics")
    assert r_eval.status_code == 200, f"Evaluation metrics failed: {r_eval.text}"
    data = r_eval.json()
    assert "fuzzy_inference_system" in data
    assert "expert_system_rules" in data
    assert "financial_benchmark_concordance" in data
    print("[+] /api/v1/advisory/evaluation-metrics OK: Monotonicity =", data["fuzzy_inference_system"]["overall_monotonicity_index_pct"], "%")

    # 3. Test static /app/
    r_app = client.get("/app/")
    assert r_app.status_code == 200, f"Static app mount failed: {r_app.status_code}"
    assert "FinWise AI" in r_app.text
    assert "AI Verification & TA Benchmarks" in r_app.text
    print("[+] Static /app/ mount OK: Served updated professional UI")

    # 4. Test root redirect
    r_root = client.get("/", follow_redirects=False)
    assert r_root.status_code == 307
    assert r_root.headers["location"] == "/app/"
    print("[+] Root redirect OK: / -> /app/")

    print("\n[SUCCESS] All FastAPI integration and evaluation endpoints verified!")

if __name__ == "__main__":
    test_eval_and_app()
