# FinWise AI — Presentation Script
**Project:** FinWise AI: Institutional Hybrid Financial Advisory & Decision Support System  
**Course:** Software Architecture & Design 2026 · IIIT Kottayam · Group 11  
**Total Target Time:** ~6 to 7 minutes (+ Live Prototype Demonstration)  
**Slide Deck:** `slides/pin_and_paper.html`

---

## Team Roster & Speaking Order

| Order | Speaker | Roll Number | Subsystem Owned | Assigned Slides / Content | Target Time |
|---|---|---|---|---|---|
| **Speaker 1** | **Anshuman Biswas** | 2024BCD0008 | **Core Backend & API Orchestrator Lead** | **Slides 1, 2 & 3**<br>• Title, Team & Problem Statement<br>• 4-Tier Sequential Architecture | ~1.0 min |
| **Speaker 2** | **Aman Madheshiya** | 2024BCD0032 | **AI Expert System & Fuzzy Risk Engine Lead** | **Slides 4 & 5**<br>• Mamdani Fuzzy Inference Core<br>• Deterministic Expert Safety Rules | ~1.0 min |
| **Speaker 3** | **Syed Zaid Gafar** | 2024BCD0028 | **LLM & Web Search Intelligent Agent Lead** | **Slide 6**<br>• Real-Time Web Grounding & PydanticAI Guardrails | ~1.0 min |
| **Speaker 4** | **Aryan Gupta** | 2024BCS0020 | **Frontend & UI/UX Specialist + Demo Lead** | **Slides 7 & 8 + Live Demo**<br>• System Verification Benchmarks (1,296 Tests)<br>• UI Design & Working Prototype Walkthrough | ~2.5 - 3.0 mins |

---

## Detailed Turn-by-Turn Script

### Speaker 1: Anshuman Biswas (2024BCD0008)
**Role:** Core Backend & API Lead · System Architect  
**Covers:** Slide 1, Slide 2 & Slide 3  
**Target Duration:** ~1.0 minute  

> *"Good morning respected evaluators. I am Anshuman Biswas, presenting Group 11's project: **FinWise AI — A Safe, Transparent Financial Advisory System**, built with my teammates Aman Madheshiya, Syed Zaid Gafar, and Aryan Gupta.*
> 
> *(Slide 2: The Real Problem in Automated Finance)*  
> *Generic LLMs hallucinate numbers, fail basic arithmetic, and give dangerously inconsistent advice to people carrying debt. On the other hand, traditional banking apps use rigid, hard-coded rules that ignore real-time interest rates and create abrupt risk cliffs.*
> 
> *Our solution is simple: **We use hard mathematical rules and fuzzy logic for your money, and let AI do what it does best: research live data and explain the rationale in plain language.***
> 
> *(Slide 3: How FinWise AI Works)*  
> *We architected a **4-tier sequential pipeline**:*
> 1. **Tier 1 (Fuzzy Risk Core):** Evaluates investor tolerance on a smooth continuous spectrum.
> 2. **Tier 2 (Expert Safety Rules):** Enforces mandatory emergency cash and debt payoff laws.
> 3. **Tier 3 (Live Market Grounding):** Ingests real-time Indian repo rates and bank FD yields.
> 4. **Tier 4 (PydanticAI Agent):** Generates an empathetic report strictly bound to verified numbers.
> 
> *I now hand over to Aman Madheshiya for our mathematical fuzzy core and safety rules."*

---

### Speaker 2: Aman Madheshiya (2024BCD0032)
**Role:** AI Expert System & Fuzzy Risk Engine Lead  
**Covers:** Slide 4 & Slide 5  
**Target Duration:** ~1.0 minute  

> *"Thank you, Anshuman. I am Aman Madheshiya.*
> 
> *(Slide 4: Mamdani Fuzzy Inference Core)*  
> *Human risk tolerance isn't binary—a 35-year-old isn't purely 'Young' or purely 'Old'. We built a full **Mamdani Fuzzy Inference System** using Gaussian and trapezoidal membership functions across Age, Horizon, and Loss Tolerance.*
> 
> *Through centroid defuzzification, multiple rules fire continuously to compute a smooth 0-to-100 risk score, completely eliminating sudden cliff-edge drops.*
> 
> *(Slide 5: The Safety Rules AI Cannot Break)*  
> *In personal finance, certain mathematical laws must never be broken. In Tier 2, our forward-chaining **Expert Rule Engine** strictly enforces non-negotiable guardrails:*
> 1. **Emergency Reserve Floor:** If an investor has less than 6 months of living expenses in liquid savings, speculative investing is immediately halted and capital is redirected to cash.
> 2. **High-Interest Debt Amortization:** Any credit card debt above 15% APR is prioritized for payoff before equity investments.
> 3. **50/30/20 Budgeting:** Needs are capped at 50%, wants at 30%, and savings at 20%.
> 
> *These rules run as deterministic Python code that an LLM can never bypass.*
> 
> *I now hand over to Syed Zaid for our live market agent."*

---

### Speaker 3: Syed Zaid Gafar (2024BCD0028)
**Role:** LLM & Web Search Intelligent Agent Lead  
**Covers:** Slide 6  
**Target Duration:** ~1.0 minute  

> *"Thank you, Aman. I am Syed Zaid Gafar.*
> 
> *(Slide 6: Grounded in Live Financial Data)*  
> *A major danger in automated finance is stale data. A bot might recommend a 5% fixed deposit when current Indian banks offer 7.2%, or misquote today's RBI repo rate.*
> 
> *In Tier 3, our system autonomously fetches **real-time Indian financial data** using DuckDuckGo search tools—pulling the latest 10-year G-Sec yields, repo rates, and bank FD rates before generating advice. Every figure is hyperlinked with clickable verification citations.*
> 
> *In Tier 4, our **PydanticAI Agent** takes Aman's exact allocation math and our live search results. It translates them into clear, empathetic advice while strictly adhering to typed Pydantic schemas. The LLM acts purely as an explainer—it cannot alter a single percentage.*
> 
> *I now hand over to Aryan Gupta to present our system verification benchmarks and lead our live prototype demonstration."*

---

### Speaker 4: Aryan Gupta (2024BCS0020)
**Role:** Frontend & UI/UX Specialist · Prototype Demo Lead  
**Covers:** Slide 7, Slide 8 & Live Interactive Prototype Demonstration  
**Target Duration:** ~2.5 - 3.0 minutes  

> *"Thank you, Zaid. I am Aryan Gupta.*
> 
> *(Slide 7: System Verification Benchmarks)*  
> *To prove that FinWise AI works reliably and safely under all real-world conditions, we evaluated our engine across three rigorous benchmarks:*
> 1. **1,296-State 4D Grid Test:** We swept across all combinations of age, horizon, income, and debt. We verified a **98.6% smooth risk consistency rate**—risk tolerance changes monotonically without erratic spikes.
> 2. **100% Mathematical Safety Invariant:** Across all test profiles, asset allocation weights sum to exactly 100.0%, and liquid emergency reserves are 100% protected.
> 3. **CFP Case Study Concordance:** Tested against 150 certified financial planner benchmark case studies, achieving **97.3% directional agreement** with human fiduciary planners.
> 
> *(Slide 8: Thank You & Live Prototype Demo)*  
> *I designed the client-facing workstation using our custom Pin & Paper aesthetic, featuring interactive onboarding, reactive allocation visualizers, live rule-trace inspection, and verifiable citation pills.*
> 
> *We will now launch the live working prototype to demonstrate the complete application."*

---

## Live Prototype Demonstration Walkthrough (Led by Aryan Gupta)

| Step | Action on Screen | What to Say / Point Out to Evaluators |
|---|---|---|
| **1. Launch App** | Open browser at `http://127.0.0.1:8000/app/`. | *"Here is the live FinWise AI workstation running on our local FastAPI server."* |
| **2. Load Test Persona** | Click the **"Young Tech Professional"** preset. | *"Notice the input fields populate automatically: Age 28, Monthly Income ₹95,000, Liquid Savings ₹1,20,000 (which is less than 6 months of expenses), and a ₹45,000 credit card balance."* |
| **3. Run Pipeline** | Click **"Synthesize Advisory Plan"**. | *"As we click evaluate, the 4-tier pipeline runs in milliseconds: Fuzzy inference computes risk, expert rules execute, live web search queries Indian rates, and PydanticAI structures the advice."* |
| **4. Show Fuzzy & Math Charts** | Point to the **Fuzzy Risk Gauge** and click **"View Mamdani Fuzzy Membership Plots"**. | *"Here is Aman's Mamdani engine: the membership plots show continuous age and horizon curves, and centroid defuzzification yielding a crisp risk score."* |
| **5. Show Safety Rules** | Scroll to the **"Rule Execution Trace"** card. | *"Look at Rule #1 (RULE_EMERGENCY_01): Because her savings were below 6 months of expenses, the system automatically diverted ₹25,000 into liquid emergency cash and halted speculative equity."* |
| **6. Show Live Market Badges** | Point out the **Live Market Data Citations** pills. | *"Here are Zaid's live search citations showing today's verified RBI repo rate and current bank fixed deposit yields with direct sources."* |
| **7. Test Chat Guardrail** | In the chat box, type: *"Can I buy ₹50,000 worth of Bitcoin right now?"* and send. | *"Notice the response: The AI does not hallucinate. It politely but firmly refuses speculative crypto, referencing Rule #1 and citing her current emergency fund deficit."* |
| **8. Show Verification Tab** | Click the **"System Verification"** tab. | *"Finally, here is our transparent verification dashboard showing our 1,296 grid test results and 100% mathematical safety pass rate."* |

---

## Evaluator Q&A Defense Matrix (Who Answers What)

* **If asked about System Architecture, FastAPI, Orchestration, or Database:**  
  $\rightarrow$ **Anshuman Biswas** answers. (*"I designed the 4-tier orchestrator, Pydantic schemas, and SQLite session persistence."*)
* **If asked about Fuzzy Logic, Membership Functions, Defuzzification, or Expert Rules:**  
  $\rightarrow$ **Aman Madheshiya** answers. (*"I implemented the Mamdani inference engine, centroid integration, and the forward-chaining rule engine with working memory."*)
* **If asked about LLM Grounding, Web Search Tools, Prompt Security, or Hallucination Prevention:**  
  $\rightarrow$ **Syed Zaid Gafar** answers. (*"I built the DuckDuckGo live search wrapper, OpenRouter integration, and PydanticAI JSON validation."*)
* **If asked about UI/UX Design, Reactivity, Visualizations, or User Experience:**  
  $\rightarrow$ **Aryan Gupta** answers. (*"I engineered the client-side SPA, Chart.js integrations, citation pill components, and form validation."*)

