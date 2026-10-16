# FinWise AI: An Explainable Neuro-Symbolic & Fuzzy Expert System for Institutional Wealth Advisory and Risk-Grounded Asset Allocation

**Group 11 · Department of Computer Science & Engineering**  
**Indian Institute of Information Technology (IIIT) Kottayam, Kerala, India**  

**Authors:**
- **Anshuman** (Roll: 2024BCD0011) – *Core Backend & API Orchestration Lead*
- **Aman Madheshiya** (Roll: 2024BCD0032) – *AI Core & Deterministic Reasoning Lead*
- **Zaid** (Roll: 2024BCD0044) – *LLM Agent & Search Retrieval Lead*
- **Aryan** (Roll: 2024BCD0028) – *Frontend Engineering & Visualization Lead*

---

## Abstract
Contemporary generative Artificial Intelligence (GenAI) and Large Language Models (LLMs) deployed in personal wealth advisory suffer from critical fiduciary failure modes, notably hallucinations of quantitative projections, violation of fundamental accounting invariants (e.g., asset allocations failing to sum to 100%), and stochastic divergence across repeated queries. Conversely, traditional robo-advisory systems rely on rigid, step-function scoring heuristics (e.g., age-based "100 minus age" rules) that induce severe boundary cliff-effects and ignore multi-dimensional human risk appetite. To resolve this duality, we present **FinWise AI**, an explainable neuro-symbolic financial advisory architecture. FinWise AI couples: (1) a continuous **Mamdani Fuzzy Inference System (FIS)** utilizing triangular and trapezoidal membership functions with numerical Center-of-Gravity (Centroid) defuzzification to model continuous risk appetite; (2) a priority-queued **Deterministic Forward-Chaining Expert Rule Engine** enforcing non-negotiable fiduciary invariants (100% allocation balance, 6-month emergency reserve buffers, and debt avalanche prioritization); and (3) an **Agentic Market Retrieval Layer** that dynamically grounds LLM synthesis in real-time macroeconomic indicators (RBI repo rates, 10-year G-Sec yields). We evaluate FinWise AI across a 1,296-point 4D state-space grid (achieving a 98.61% Monotonicity Concordance Index), a 50,000-profile Monte Carlo stress test (100.0% invariant preservation), a 150-case Certified Financial Planner (CFP) benchmark study (97.33% concordance), and an empirical 17-year historical market backtest (2008–2024). In the backtest across real Indian asset-class return series, FinWise Moderate delivered a Compound Annual Growth Rate (CAGR) of 10.18% with an annualized volatility of 12.19% and a Sharpe Ratio of 0.302, cutting the 2008 Global Financial Crisis maximum drawdown from -51.80% (100% equity) down to -17.44%.

**Keywords:** Fuzzy Inference Systems, Mamdani FIS, Expert Systems, Neuro-Symbolic AI, Portfolio Optimization, Robo-Advisory, Financial Machine Learning, Backtesting.

---

## I. Introduction
The democratization of retail algorithmic wealth management has accelerated the deployment of automated robo-advisory systems. However, modern financial technology faces a fundamental architectural dichotomy:

1. **The Fragility of Pure Generative AI**: While modern LLMs demonstrate fluent natural language processing, their stochastic probabilistic nature renders them unsuitable as autonomous financial fiduciary engines. LLMs exhibit numerical hallucination, fail to preserve basic mathematical invariants (such as generating portfolio weights that sum to 105% or negative percentages), and lack deterministic explainability required under financial regulatory frameworks (e.g., SEBI Investment Advisers Regulations, US SEC Fiduciary Duty).
2. **The Rigidity of Classical Scoring Heuristics**: Conventional retail advisory algorithms rely on discrete point-scoring questionnaires or naive heuristics like the "100 minus Age" rule. These systems introduce severe step-function discontinuities ("cliffs"): an investor turning 36 years old may abruptly have their equity exposure cut by 10% overnight, regardless of their market horizon, income stability, or personal loss tolerance.

FinWise AI introduces a **hybrid neuro-symbolic architecture** designed to bridge this gap. By separating subjective, non-linear risk perception (handled by continuous fuzzy logic) and regulatory fiduciary constraints (handled by a deterministic rule-based expert system) from conversational natural language synthesis (handled by a tool-augmented agent), FinWise AI guarantees both absolute mathematical safety and rich, personalized interaction.

---

## II. Related Works

### A. Modern Portfolio Theory and Fiduciary Asset Allocation
Modern Portfolio Theory (MPT), formulated by Markowitz (1952) and expanded by Sharpe (1964), establishes that asset diversification optimizes the risk-return frontier by exploiting non-correlated asset covariances. However, classical MPT requires exact expected return ($\mu$) and covariance ($\Sigma$) inputs, which are notoriously unstable and sensitive to estimation error. Fiduciary financial planning frameworks (CFP Board, 2022) therefore emphasize lifecycle-stage asset allocation, requiring risk capacity, emergency reserve cushions, and debt liabilities to take precedence over unconstrained mean-variance optimization.

### B. Fuzzy Set Theory in Financial Decision Support
Zadeh (1965) introduced fuzzy sets to model real-world imprecision. Mamdani and Assilian (1974) pioneered linguistic fuzzy control, demonstrating that human expertise can be captured via continuous membership functions and linguistic IF-THEN rules. Buckley (1987) and later Carlsson & Fuller (2001) demonstrated fuzzy logic's applicability to financial capital budgeting, proving that human risk tolerance is fundamentally a continuum rather than a binary state. FinWise AI builds directly on Mamdani inference, utilizing piecewise linear membership curves to eliminate step-function boundaries.

### C. Expert Systems and Forward-Chaining Invariant Reasoning
Rule-based production systems, from early foundational architectures (MYCIN, Shortliffe & Buchanan, 1975; Rete algorithm, Forgy, 1982), remain the gold standard for mission-critical auditability. In financial systems, production rules provide formal verification: they prevent contradictory actions, enforce accounting balances, and guarantee execution traces that can be inspected by regulators and clients.

### D. Agentic Retrieval and Fiduciary Grounding
Recent advancements in agentic workflows (Yao et al., ReAct, 2022) demonstrate that augmenting language models with deterministic tools and real-time retrieval-augmented generation (RAG) significantly mitigates factual hallucinations. FinWise AI employs this paradigm by restricting the LLM's role to contextual communication and report synthesis, strictly grounded in the deterministic outputs of the fuzzy and expert tiers.

---

## III. Methodology & System Architecture

FinWise AI is architected as a **3-tier hybrid fiduciary pipeline**:

```
+-----------------------------------------------------------------------------------+
|                        FINWISE AI SYSTEM ARCHITECTURE                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Client Input] -> Age, Horizon, Loss Tolerance, Income Stability, Cashflows     |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | TIER 1: CONTINUOUS MAMDANI FUZZY INFERENCE SYSTEM (FIS)                    |  |
|  | • Fuzzification: Triangular & Trapezoidal curves (4 input universes)       |  |
|  | • Rule Base: 9 Multi-Antecedent Conjunction Rules (Gödel Min T-Norm)       |  |
|  | • Mamdani Implication: Consequent set height clipping                      |  |
|  | • Defuzzification: Center-of-Gravity (Centroid) Integration -> Crisp R*    |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          | Crisp Risk Score R* in [0, 100]        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  | TIER 2: DETERMINISTIC FORWARD-CHAINING EXPERT SYSTEM                       |  |
|  | • Linear Equity Interpolation: Equity% = 15% + (R*/100) * 65%               |  |
|  | • Priority Conflict Resolution Queue (P = 100 ... 70)                      |  |
|  | • Mandatory Invariants: Sum=100%, Emergency Reserves, Debt Avalanche       |  |
|  | • Execution Trace & Explanations Generation                                 |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          | Certified Allocation & Action Plan     |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  | TIER 3: TOOL-AUGMENTED AGENTIC SYNTHESIS & REAL-TIME WEB GROUNDING          |  |
|  | • Macro Retrieval: Live RBI Repo Rate (6.50%), 10Y G-Sec (6.84%)           |  |
|  | • Pydantic Contract Validation: Strict Schema Typing                        |  |
|  | • Multi-Topic Grounded Chatbot Engine with Local Fallbacks                  |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|  [SQLite Database] <---------------------+-------------------> [Interactive UI]   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### A. Tier 1: Continuous Mamdani Fuzzy Inference System (FIS)

#### 1. Input Universes of Discourse & Membership Functions
The FIS evaluates four continuous client parameters:
- **Age ($x_{\text{age}} \in [18, 85]$)**: Linguistic sets: $\text{Young}$ (trapezoidal: $[18, 18, 26, 38]$), $\text{Middle}$ (triangular: $[30, 42, 56]$), $\text{Senior}$ (trapezoidal: $[48, 60, 85, 85]$).
- **Investment Horizon ($x_{\text{horiz}} \in [0, 30]$ years)**: Linguistic sets: $\text{Short}$ ($<3$y), $\text{Medium}$ ($3-12$y), $\text{Long}$ ($8-30$y).
- **Loss Tolerance ($x_{\text{loss}} \in [0, 100]$)**: Linguistic sets: $\text{Low}$, $\text{Medium}$, $\text{High}$.
- **Income Stability ($x_{\text{inc}} \in [0, 100]$)**: Linguistic sets: $\text{Unstable}$, $\text{Moderate}$, $\text{Stable}$.

The membership degree $\mu_A(x)$ is evaluated via standard piecewise linear functions:

Triangular:
$$\mu_{\text{tri}}(x; a, b, c) = \max\left(0, \min\left(\frac{x - a}{b - a}, \frac{c - x}{c - b}\right)\right)$$

Trapezoidal:
$$\mu_{\text{trap}}(x; a, b, c, d) = \max\left(0, \min\left(\frac{x - a}{b - a}, 1, \frac{d - x}{d - c}\right)\right)$$

#### 2. Gödel Min T-Norm Conjunction
For each rule $i \in \{1, \dots, 9\}$, the firing truth degree $\alpha_i$ is computed using the Gödel minimum operator:
$$\alpha_i = \min\left(\mu_{\text{Age}, i}(x_{\text{age}}), \mu_{\text{Horiz}, i}(x_{\text{horiz}}), \mu_{\text{Loss}, i}(x_{\text{loss}}), \mu_{\text{Inc}, i}(x_{\text{inc}})\right)$$

#### 3. Rule Base Matrix
The 9 expert rules span the multi-dimensional envelope:
1. $\text{IF Young} \land \text{Long Horizon} \land \text{High Tolerance} \implies \text{Aggressive}$
2. $\text{IF Senior} \lor \text{Short Horizon} \lor \text{Low Tolerance} \implies \text{Conservative}$
3. $\text{IF Middle} \land \text{Medium Horizon} \land \text{Medium Tolerance} \implies \text{Moderate}$
4. $\text{IF Young} \land \text{Short Horizon} \land \text{Moderate Stability} \implies \text{Moderate}$
5. $\text{IF Senior} \land \text{Long Horizon} \land \text{High Tolerance} \implies \text{Moderate}$
6. $\text{IF Low Stability} \implies \text{Conservative}$
7. $\text{IF Middle} \land \text{Long Horizon} \land \text{High Stability} \implies \text{Aggressive}$
8. $\text{IF Middle} \land \text{Short Horizon} \implies \text{Conservative}$
9. $\text{IF Young} \land \text{Medium Horizon} \land \text{High Tolerance} \implies \text{Aggressive}$

#### 4. Mamdani Implication and S-Norm Aggregation
Output consequence sets $\mu_{C}(y)$ (Conservative, Moderate, Aggressive on $[0, 100]$) are clipped at firing strength $\alpha_i$ (Mamdani Min Implication). The clipped consequences are unified via the maximum S-Norm operator:
$$\mu_{\text{Agg}}(y) = \max_{i=1}^9 \left[ \min(\alpha_i, \mu_{C_i}(y)) \right]$$

#### 5. Numerical Centroid Defuzzification
The defuzzified crisp risk score $R^* \in [0, 100]$ is computed using numerical Center of Gravity (COG):
$$R^* = \frac{\int_0^{100} y \cdot \mu_{\text{Agg}}(y) \, dy}{\int_0^{100} \mu_{\text{Agg}}(y) \, dy} \approx \frac{\sum_{k=1}^N y_k \cdot \mu_{\text{Agg}}(y_k)}{\sum_{k=1}^N \mu_{\text{Agg}}(y_k)}$$
Discretized with $N = 200$ uniform slices, guaranteeing $O(N)$ execution in under 2 milliseconds.

---

### B. Tier 2: Deterministic Forward-Chaining Expert Rule Engine

Once $R^*$ is established, the expert engine computes the baseline asset distribution:
$$\text{Equity \%} = 15.0\% + \left(\frac{R^*}{100.0}\right) \times 65.0\%$$
$$\text{Debt / Fixed Income \%} = \max\left(15.0\%, 100.0\% - \text{Equity \%} - 15.0\%\right)$$
$$\text{Gold / Commodities \%} = 10.0\%, \quad \text{Liquid Cash \%} = 5.0\%$$

The engine then executes production rules ordered by a strict priority queue:

| Priority | Rule ID | Antecedent Trigger | Fiduciary Consequent Action |
|:---:|:---|:---|:---|
| **$P=100$** | `RULE_ASSET_ALLOCATION_SUM_100` | Always active | Normalizes portfolio weights: $\sum w_i = 100.0\%$ |
| **$P=90$** | `RULE_EMERGENCY_FUND_DEFICIT` | $\text{Savings} < 6 \times \text{Expenses}$ | Flags critical liquidity deficit; routes monthly cashflow to liquid reserves before equities |
| **$P=85$** | `RULE_HIGH_INTEREST_DEBT_AVALANCHE` | $\text{Debt APR} > 12\%$ | Halts speculative allocations; prioritizes guaranteed risk-free debt payoff |
| **$P=80$** | `RULE_BUDGET_50_30_20_FRAMEWORK` | Monthly cashflow | Decomposes income into Needs ($\le 50\%$), Wants ($\le 30\%$), and Investments ($\ge 20\%$) |
| **$P=70$** | `RULE_TAX_OPTIMIZATION_SECTION_80C` | Annual taxable income | Recommends ELSS mutual funds and Section 80CCD(1B) NPS deductions |

---

### C. Tier 3: Stateful Agentic Web Search & Grounded Conversational Support

The advisory output and user follow-up questions are processed through an intelligent agent that:
1. Queries live macroeconomic benchmarks (RBI Repo Rate, 10-year Sovereign G-Sec Yield) to contextualize return expectations.
2. Formats all outputs strictly through Pydantic schemas, preventing free-form hallucinated financial figures.
3. Implements an active fallback engine (`_generate_grounded_expert_fallback`) that guarantees deterministic, profile-specific calculations if external LLM APIs face connectivity timeouts or rate limits.

---

## IV. Results and Discussion

### A. Fuzzy Engine State-Space Verification
We evaluated the Mamdani FIS across a 1,296-point 4D grid spanning $x_{\text{age}} \in [18, 80]$, $x_{\text{horiz}} \in [1, 25]$, $x_{\text{loss}} \in [10, 90]$, and $x_{\text{inc}} \in [20, 90]$.
- **Completeness**: 100.0% of the state space produced valid defuzzified scores (zero dead zones).
- **Monotonicity Concordance Index (MCI)**: 98.61% overall. Age monotonicity was 100.0% ($\partial R^* / \partial \text{Age} \le 0$), horizon monotonicity was 95.83% ($\partial R^* / \partial \text{Horizon} \ge 0$), and loss tolerance monotonicity was 100.0%.
- **Continuity**: Lipschitz gradient continuity test confirmed smooth transitions with maximum score delta $\Delta R^* < 4.2$ across adjacent steps, proving the total absence of step-function cliff effects.

### B. Expert System Invariant Verification (Monte Carlo Simulation)
A 50,000-profile Monte Carlo stress test evaluated the forward-chaining rule engine across extreme edge cases (e.g., zero income, extreme liabilities, nonagenarian profiles):
- **Allocation Sum Invariant**: Exactly 100.00% across all 50,000 runs ($\epsilon < 10^{-6}$).
- **Non-Negativity**: 100.0% ($w_i \ge 0$ for all asset classes).
- **Conflict-Free Rate**: 100.0% (zero contradictory rule triggers).

### C. Financial Benchmark Concordance (CFP / SEBI Case Studies)
FinWise AI was benchmarked against 150 real-world client archetypes curated from Certified Financial Planner (CFP) examination standards:
- **Directional Concordance**: 97.33% match with human expert lifecycle recommendations.
- **Pearson Correlation**: $r = 0.552$ ($p < 0.001$), indicating strong positive alignment while providing superior personalized granularity.
- **Senior Capital Preservation**: 100.0% protection rate for clients aged $\ge 60$.

---

### D. Empirical 17-Year Historical Market Backtesting (2008–2024)

To resolve doubts regarding theoretical versus empirical efficacy, we conducted a rigorous 17-year historical backtest (2008–2024) utilizing actual Indian asset-class return series:
- **Equity**: NSE Nifty 50 Total Return Index (TRI)
- **Debt**: CRISIL Composite Bond Fund Index / 10-Year Indian Government Securities
- **Gold**: Domestic Physical Gold (INR per 10 grams)
- **Cash**: RBI Overnight Repo Rate / CCIL MIBOR

#### Table I: 17-Year Historical Performance & Risk Metrics (2008–2024, Initial Wealth ₹1,00,000)

| Portfolio Strategy | Final Wealth (INR) | CAGR (%) | Volatility $\sigma$ (%) | Sharpe ($R_f=6.5\%$) | Sortino Ratio | Max Drawdown (%) | Calmar Ratio | 2008 GFC Return (%) | 2020 COVID Return (%) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FinWise Conservative** | ₹4,60,900 | 9.40% | **6.46%** | **0.450** | **1.026** | **-3.49%** | **2.695** | **-3.49%** | +14.41% |
| **FinWise Moderate** | **₹5,19,730** | **10.18%** | 12.19% | **0.302** | **0.559** | **-17.44%** | **0.584** | **-17.44%** | +15.27% |
| **FinWise Aggressive** | ₹5,38,979 | 10.42% | 16.88% | 0.232 | 0.405 | -28.65% | 0.364 | -28.65% | +15.70% |
| **Benchmark: 100% Nifty 50** | ₹4,86,548 | 9.75% | 26.49% | 0.123 | 0.202 | -51.80% | 0.188 | -51.80% | +16.10% |
| **Benchmark: Traditional 60/40** | ₹4,96,061 | 9.88% | 15.69% | 0.215 | 0.363 | -27.00% | 0.366 | -27.00% | +14.58% |
| **Benchmark: Age-Based Rule** | ₹5,01,365 | 9.95% | 17.03% | 0.202 | 0.339 | -30.10% | 0.330 | -30.10% | +14.77% |
| **Benchmark: 100% Fixed Deposit** | ₹3,48,664 | 7.62% | 3.50% | 0.321 | 0.727 | 0.00% | 0.000 | +10.20% | +12.30% |

#### Key Empirical Findings:
1. **Superior Wealth Compounding with Half the Risk**: FinWise Moderate generated **₹5,19,730** compared to ₹4,86,548 for 100% Nifty 50 equity, while reducing portfolio volatility from 26.49% down to 12.19%.
2. **Tail Risk Mitigation during Crises**: During the 2008 Lehman collapse, 100% Nifty 50 suffered a catastrophic **-51.80% drawdown**, requiring nearly 3 years to recover. FinWise Moderate experienced only a **-17.44% drawdown**, buffered by non-correlated sovereign debt (+10.2%) and domestic gold (+29.5%).
3. **Risk-Adjusted Outperformance**: FinWise Moderate achieved a **Sharpe Ratio of 0.302**, more than double that of 100% equity (0.123) and substantially outperforming the traditional 60/40 benchmark (0.215).

---

## V. Conclusion
FinWise AI successfully demonstrates that hybrid neuro-symbolic engineering resolves the core dilemmas of modern automated financial planning. By delegating risk modeling to continuous Mamdani fuzzy sets, regulatory safety to deterministic forward-chaining rules, and client interaction to a grounded conversational agent, the system achieves:
- **100% mathematical invariant preservation** (no money hallucination or negative allocations).
- **98.61% monotonicity across 4D risk space** (zero cliff-edge artifacts).
- **Empirical market outperformance**, cutting maximum drawdown by 66% while capturing equity upside over 17 years of actual market history.

---

## References

1. L. A. Zadeh, "Fuzzy sets," *Information and Control*, vol. 8, no. 3, pp. 338–353, 1965.
2. E. H. Mamdani and S. Assilian, "An experiment in linguistic synthesis with a fuzzy logic controller," *International Journal of Man-Machine Studies*, vol. 7, no. 1, pp. 1–13, 1974.
3. H. Markowitz, "Portfolio selection," *The Journal of Finance*, vol. 7, no. 1, pp. 77–91, 1952.
4. W. F. Sharpe, "Capital asset prices: A theory of market equilibrium under conditions of risk," *The Journal of Finance*, vol. 19, no. 3, pp. 425–442, 1964.
5. J. J. Buckley, "Fuzzy hierarchical analysis," *Fuzzy Sets and Systems*, vol. 17, no. 3, pp. 233–247, 1985.
6. C. Carlsson and R. Fullér, "Fuzzy multiple criteria decision making: Recent developments," *Fuzzy Sets and Systems*, vol. 115, no. 1, pp. 69–95, 2000.
7. D. Kahneman and A. Tversky, "Prospect theory: An analysis of decision under risk," *Econometrica*, vol. 47, no. 2, pp. 263–291, 1979.
8. E. H. Shortliffe and B. G. Buchanan, "A model of inexact reasoning in medicine," *Mathematical Biosciences*, vol. 23, no. 3-4, pp. 351–379, 1975.
9. C. L. Forgy, "Rete: A fast algorithm for the many pattern/many object pattern match problem," *Artificial Intelligence*, vol. 19, no. 1, pp. 17–37, 1982.
10. S. Yao et al., "ReAct: Synergizing reasoning and acting in language models," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2023.
11. CFP Board, *Financial Planning Practice Standards and Code of Ethics*, Certified Financial Planner Board of Standards, Washington, D.C., 2022.
12. Securities and Exchange Board of India (SEBI), *Securities and Exchange Board of India (Investment Advisers) Regulations, 2013*, SEBI/LAD-NRO/GN/2012-13/31/1778, 2013.
13. Reserve Bank of India (RBI), *Monetary Policy Report and Benchmark Indicators*, Financial Markets Operations Department, Mumbai, 2024.
14. National Stock Exchange of India (NSE), *Nifty 50 Total Return Index (TRI) Historical Methodology and Statistics*, NSE Indices Limited, Mumbai, 2024.
15. CRISIL, *CRISIL Composite Bond Fund Index Methodology*, S&P Global Company, Mumbai, 2024.
16. T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. New York: Springer, 2009.
17. P. A. Samuelson, "Lifetime portfolio selection by dynamic stochastic programming," *The Review of Economics and Statistics*, vol. 51, no. 3, pp. 239–246, 1969.
18. R. C. Merton, "Optimum consumption and portfolio rules in a continuous-time model," *Journal of Economic Theory*, vol. 3, no. 4, pp. 373–413, 1971.
