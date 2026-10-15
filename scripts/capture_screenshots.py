"""
Capture high-resolution screenshots of FinWise AI Web Application for the README.
"""
import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PROJECT_ROOT = Path(__file__).parent.resolve()
ASSETS_DIR = PROJECT_ROOT / "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1600,1050")
opts.add_argument("--force-device-scale-factor=1.25")
opts.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=opts)

try:
    print("[+] Loading FinWise AI Application at http://127.0.0.1:8000/app/ ...")
    driver.get("http://127.0.0.1:8000/app/")
    time.sleep(2.0)

    # 1. Capture Questionnaire View (Initial Hero)
    driver.execute_script("switchView('wizard'); window.scrollTo(0, 0);")
    time.sleep(0.5)
    driver.save_screenshot(str(ASSETS_DIR / "01_questionnaire_view.png"))
    print("[+] Saved 01_questionnaire_view.png")

    # 2. Select Family Persona
    driver.execute_script("loadPreset('family');")
    time.sleep(0.5)

    # 3. Click Submit Button
    print("[+] Clicking Execute Hybrid Advisory Pipeline button...")
    driver.find_element(By.ID, "btn-generate-plan").click()

    # Wait for dashboard to become active
    print("[+] Polling for dashboard view activation...")
    for _ in range(30):
        time.sleep(1)
        active = driver.execute_script("return document.getElementById('view-dashboard').classList.contains('active');")
        if active:
            print("[+] Dashboard activated!")
            break
    else:
        print("[!] Timeout waiting for dashboard view, forcing switchView('dashboard')")
        driver.execute_script("switchView('dashboard');")

    time.sleep(2.0)

    # 4. Top of Dashboard (Hero / Advisory Plan)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    driver.save_screenshot(str(ASSETS_DIR / "hero_dashboard.png"))
    driver.save_screenshot(str(ASSETS_DIR / "02_advisory_dashboard.png"))
    print("[+] Saved hero_dashboard.png & 02_advisory_dashboard.png")

    # 5. Mamdani Fuzzy Process (Matplotlib)
    driver.execute_script("""
        const container = document.getElementById('mamdani-plot-container');
        if (container && container.style.display === 'none') {
            toggleMamdaniView();
        }
        container.scrollIntoView({ behavior: 'instant', block: 'center' });
    """)
    time.sleep(1.0)
    driver.save_screenshot(str(ASSETS_DIR / "03_mamdani_fuzzy_process.png"))
    print("[+] Saved 03_mamdani_fuzzy_process.png")

    # 6. Interactive Advisor Chat
    driver.execute_script("switchView('chat'); window.scrollTo(0, 0);")
    time.sleep(0.5)
    print("[+] Triggering quick question in chat...")
    driver.execute_script("sendQuickChat('Should I pay off my high-interest debt or invest in equities first?');")
    
    # Wait for assistant response
    for _ in range(25):
        time.sleep(1)
        count = len(driver.find_elements(By.CSS_SELECTOR, "#chat-messages-list .chat-message-row"))
        if count >= 3:
            print(f"[+] Chat response received! Total messages: {count}")
            break

    time.sleep(1.0)
    driver.save_screenshot(str(ASSETS_DIR / "04_interactive_chat_guardrails.png"))
    print("[+] Saved 04_interactive_chat_guardrails.png")

    # 7. System Verification Benchmarks
    driver.execute_script("switchView('evaluation'); window.scrollTo(0, 0);")
    time.sleep(1.0)
    driver.save_screenshot(str(ASSETS_DIR / "05_system_verification_benchmarks.png"))
    print("[+] Saved 05_system_verification_benchmarks.png")

    print("[✓] All 6 screenshots saved successfully!")

finally:
    driver.quit()
