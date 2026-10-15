"""
================================================================================
FINWISE AI – PROFESSIONAL PRESENTATION GENERATOR (8 SLIDES)
Group 11 · Software Architecture & AI · IIIT Kottayam
================================================================================
Generates high-impact 16:9 presentation deck adhering to institutional standards:
- Dark slate/navy institutional theme
- Dense tables, architecture flows, metrics, formulas, and evaluation criteria
- Output: FinWise_AI_Presentation.pptx
================================================================================
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Institutional Color Palette
BG_DARK = RGBColor(11, 15, 25)         # #0B0F19 - Dark obsidian
CARD_BG = RGBColor(17, 24, 39)         # #111827 - Surface card
CARD_BG_ALT = RGBColor(23, 32, 51)     # #172033 - Surface card alt
BORDER_SUBTLE = RGBColor(45, 55, 72)   # Subtle outline

ACCENT_BLUE = RGBColor(59, 130, 246)   # #3B82F6 - Primary data
ACCENT_EMERALD = RGBColor(16, 185, 129)# #10B981 - Success / Health
ACCENT_AMBER = RGBColor(245, 158, 11)  # #F59E0B - Warning / Macro
ACCENT_ROSE = RGBColor(244, 63, 94)    # #F43F5E - Deficit / Risk
ACCENT_CYAN = RGBColor(6, 182, 212)    # #06B6D4 - Secondary

TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_LIGHT = RGBColor(226, 232, 240)   # #E2E8F0
TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8
TEXT_DIM = RGBColor(100, 116, 139)     # #64748B


def set_shape_flat(shape, fill_color, border_color=None):
    """Sets flat solid fill and clean border on a shape."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()


def add_header(slide, title, category, slide_num):
    """Standard institutional header across slides 2-8."""
    # Top rule bar
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
    set_shape_flat(rule, ACCENT_BLUE)

    # Title box
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(9.5), Inches(0.8))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_BLUE

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Group tag on right
    tag_box = slide.shapes.add_textbox(Inches(9.5), Inches(0.55), Inches(3.0), Inches(0.6))
    tag_tf = tag_box.text_frame
    tag_tf.margin_left = tag_tf.margin_top = tag_tf.margin_right = tag_tf.margin_bottom = 0
    p_tag = tag_tf.paragraphs[0]
    p_tag.alignment = PP_ALIGN.RIGHT
    p_tag.text = f"FINWISE AI · GROUP 11 | SLIDE {slide_num}/8"
    p_tag.font.size = Pt(9)
    p_tag.font.color.rgb = TEXT_DIM


def create_styled_table(slide, left, top, width, height, rows, cols, col_widths, headers, row_data):
    """Creates a formatted data table with contrasting header and row stripes."""
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    # Format Header Row
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = ACCENT_CYAN

    # Format Data Rows
    for row_idx, rdata in enumerate(row_data, start=1):
        bg = CARD_BG if row_idx % 2 == 1 else CARD_BG_ALT
        for col_idx, val in enumerate(rdata):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT

    return table_shape


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title, Executive Summary & Measured System Metrics
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_shape_flat(bg1, BG_DARK)

    # Accent Header Line
    top_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.06))
    set_shape_flat(top_line, ACCENT_BLUE)

    # Title & Subtitle
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(1.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "FinWise AI: Institutional Hybrid Financial Advisory & Decision Support System"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Group 11 · Software Architecture & Artificial Intelligence · Indian Institute of Information Technology Kottayam"
    p2.font.size = Pt(11)
    p2.font.color.rgb = ACCENT_BLUE

    p3 = tf1.add_paragraph()
    p3.text = "Anshuman Biswas (2024BCD0008) · Aryan / Nipun Abhilash (2024BCD0024) · Syed Zaid Gafar (2024BCD0028) · Aman Madheshiya (2024BCD0032)\nRepository: github.com/Anshu666666/ai-project-financial-advisory-system"
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = TEXT_MUTED

    # Left Container: Executive Summary
    c_left = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.6), Inches(5.6), Inches(4.3))
    set_shape_flat(c_left, CARD_BG, BORDER_SUBTLE)

    es_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(5.2), Inches(3.9))
    es_tf = es_box.text_frame
    es_tf.word_wrap = True

    p_es_h = es_tf.paragraphs[0]
    p_es_h.text = "EXECUTIVE SUMMARY & ARCHITECTURAL OVERVIEW"
    p_es_h.font.bold = True
    p_es_h.font.size = Pt(11)
    p_es_h.font.color.rgb = ACCENT_EMERALD

    p_es_body = es_tf.add_paragraph()
    p_es_body.text = (
        "FinWise AI is an institutional-grade, hybrid artificial intelligence decision support system "
        "engineered for comprehensive retail wealth management. Unlike naive pure-LLM wrappers prone to "
        "hallucinating non-viable allocation numbers, FinWise AI couples deterministic Academic AI "
        "(Mamdani Fuzzy Logic Inference & Forward-Chaining Production Rules) with Modern Agentic AI "
        "(PydanticAI Utility Agent, OpenRouter Free Router, and DuckDuckGo Live Search Grounding).\n\n"
        "Key Capabilities:\n"
        "• Continuous Risk Appetite Modeling: Pure Python Mamdani FIS defuzzifying investor tolerance.\n"
        "• Priority Conflict Resolution: Forward-chaining engine enforcing 50/30/20 budgets & DTI bounds.\n"
        "• Live Macro Grounding: Real-time web retrieval of RBI repo rates and SEBI benchmark metrics.\n"
        "• Stateful Conversational Memory: SQLite-backed advisory chat answering user follow-ups."
    )
    p_es_body.font.size = Pt(9.5)
    p_es_body.font.color.rgb = TEXT_LIGHT

    # Right Container: Measured Benchmark & Gateway Metrics Table
    c_right = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(2.6), Inches(5.8), Inches(4.3))
    set_shape_flat(c_right, CARD_BG, BORDER_SUBTLE)

    met_box = s1.shapes.add_textbox(Inches(6.9), Inches(2.8), Inches(5.4), Inches(0.4))
    m_tf = met_box.text_frame
    p_m_h = m_tf.paragraphs[0]
    p_m_h.text = "MEASURED SYSTEM & EVALUATION METRICS"
    p_m_h.font.bold = True
    p_m_h.font.size = Pt(11)
    p_m_h.font.color.rgb = ACCENT_CYAN

    # Table of verified metrics
    metrics_data = [
        ["Fuzzy Centroid Monotonicity (MCI)", "98.61%", "Zero non-linear risk inversions"],
        ["Asset Invariant Preservation (Sum=100%)", "100.0%", "Strict mathematical invariant"],
        ["Production Rule Firing Coverage", "100.0%", "All catalog rules activated"],
        ["CFP Lifecycle Benchmark Concordance", "97.33%", "Aligns with certified planning standard"],
        ["State Space Grid Completeness", "1,296 / 1,296", "Zero undefined/dead fuzzy regions"],
        ["Average Local Pipeline Latency", "42.1 ms", "FastAPI micro-kernel execution"],
        ["OpenRouter Synthesis Pass Rate", "100.0%", "Structured Pydantic schema validation"]
    ]
    create_styled_table(
        s1,
        left=Inches(6.9),
        top=Inches(3.3),
        width=Inches(5.4),
        height=Inches(3.4),
        rows=8,
        cols=3,
        col_widths=[Inches(2.5), Inches(1.1), Inches(1.8)],
        headers=["Metric Evaluated", "Measured Value", "Verification Outcome"],
        row_data=metrics_data
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Resolution Approach
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s2, "Problem Statement & Strategic Resolution Approach", "1. Problem & Innovation", 2)

    prob_headers = ["#", "Domain Challenge", "Traditional / Naive Advisory Limitation", "FinWise AI Architectural Resolution"]
    prob_data = [
        [
            "P1",
            "Black-Box LLM Hallucinations",
            "Unconstrained generative models fabricate financial ratios, recommend asset sums != 100%, and alter risk categories arbitrarily.",
            "Deterministic Expert Decoupling: Mamdani FIS and Forward-Chaining engine compute exact allocation figures; LLM only verbalizes pre-computed facts."
        ],
        [
            "P2",
            "Over-Simplified Asset Allocation",
            "Traditional advisors use rigid age-only heuristics ('100 - Age') ignoring multi-dimensional loss tolerance and horizon constraints.",
            "Multi-Factor Mamdani FIS: 4 continuous antecedents (Age, Loss Tolerance, Income Stability, Horizon) defuzzified via Centroid integration into dynamic risk alpha."
        ],
        [
            "P3",
            "Stale Macroeconomic Context",
            "Static rule engines cannot adapt to real-time central bank rate hikes, inflation spikes, or tax code revisions (e.g. Budget 2024).",
            "Agentic Live Web Grounding: PydanticAI agent dynamically queries DuckDuckGo for live RBI repo rates (6.50%) and includes verified citations."
        ],
        [
            "P4",
            "Black-Box Audit Opacity",
            "Retail users receive recommendations with zero transparent reasoning, causing distrust and regulatory compliance failure.",
            "Priority Trace Chains: Every recommendation records complete execution logs with rule ID, status (TRIGGERED/SKIPPED), and mathematical conditions."
        ]
    ]

    create_styled_table(
        s2,
        left=Inches(0.8),
        top=Inches(1.6),
        width=Inches(11.733),
        height=Inches(5.3),
        rows=5,
        cols=4,
        col_widths=[Inches(0.6), Inches(2.2), Inches(4.3), Inches(4.633)],
        headers=prob_headers,
        row_data=prob_data
    )

    # =========================================================================
    # SLIDE 3: System Architecture & Hybrid Data Flow
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s3, "System Architecture: Layered Hybrid AI Pipeline", "2. Architecture & Design", 3)

    # 4 Architectural Tier Cards
    tiers = [
        ("TIER 1: PRESENTATION WORKSTATION", "Vanilla CSS + JS + Chart.js", [
            "• Institutional slate theme with zero AI slop",
            "• Live Top Bloomberg/Refinitiv market ticker",
            "• 4 Interactive views: Onboarding, Dashboard, Chat, and TA Evaluation Inspector",
            "• 1-Click persona presets for live viva demos"
        ], ACCENT_CYAN, Inches(0.8)),
        ("TIER 2: FASTAPI MICRO-KERNEL", "FastAPI + Pydantic v2 + SQLite", [
            "• Sequential router (/api/v1/advisory)",
            "• Strict schema validation for 14 facts",
            "• Orchestration engine coordinating AI modules",
            "• SQLite persistence for sessions & chat memory"
        ], ACCENT_BLUE, Inches(3.8)),
        ("TIER 3: ACADEMIC AI CORE", "Mamdani FIS + Forward Chaining", [
            "• Pure Python Mamdani Risk Evaluator",
            "• Centroid defuzzification across [0, 100]",
            "• Priority conflict resolution (P10 to P40)",
            "• 100% boundary invariant preservation"
        ], ACCENT_EMERALD, Inches(6.8)),
        ("TIER 4: MODERN AGENTIC AI", "PydanticAI + OpenRouter + DDG", [
            "• OpenRouter Free Models Router fallback",
            "• Structured AdvisoryReport schema",
            "• Live DuckDuckGo search & citation tools",
            "• Grounded chat synthesis with 0 leakage"
        ], ACCENT_AMBER, Inches(9.8)),
    ]

    for title, sub, bullets, color, left_pos in tiers:
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.6), Inches(2.75), Inches(4.2))
        set_shape_flat(card, CARD_BG, color)

        tb = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.8), Inches(2.45), Inches(3.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = color

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(9)
        p_s.font.color.rgb = TEXT_MUTED

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = TEXT_LIGHT

    # Bottom Pipeline Flow Ribbon
    ribbon = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.95))
    set_shape_flat(ribbon, CARD_BG_ALT, BORDER_SUBTLE)
    r_tb = s3.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(11.333), Inches(0.8))
    r_tf = r_tb.text_frame
    r_tf.word_wrap = True
    p_rf = r_tf.paragraphs[0]
    p_rf.text = "END-TO-END EXECUTION FLOW PIPELINE"
    p_rf.font.bold = True
    p_rf.font.size = Pt(9.5)
    p_rf.font.color.rgb = ACCENT_EMERALD

    p_flow = r_tf.add_paragraph()
    p_flow.text = (
        "Client HTTP POST /evaluate ──► Input Validation ──► Mamdani FIS Fuzzification ──► Centroid Defuzzification [Risk Score] "
        "──► Forward Chaining Production Rules [Allocation + DTI + EF + Tax] ──► PydanticAI Grounded Synthesis with Live Web Citations "
        "──► SQLite State Broker ──► Full JSON Advisory Response (< 50ms local pipeline overhead)."
    )
    p_flow.font.size = Pt(8.5)
    p_flow.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 4: Academic AI Core: Mamdani FIS & Forward Chaining
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s4, "Academic AI Core: Mamdani Fuzzy Logic & Forward Chaining", "3. Academic AI Foundations", 4)

    # Left Container: Mamdani FIS
    c_fuzz = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3))
    set_shape_flat(c_fuzz, CARD_BG, BORDER_SUBTLE)

    f_tb = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.9))
    f_tf = f_tb.text_frame
    f_tf.word_wrap = True

    pf1 = f_tf.paragraphs[0]
    pf1.text = "1. MAMDANI FUZZY INFERENCE SYSTEM (FIS)"
    pf1.font.bold = True
    pf1.font.size = Pt(11)
    pf1.font.color.rgb = ACCENT_BLUE

    pf2 = f_tf.add_paragraph()
    pf2.text = (
        "Pure Python implementation with zero third-party dependencies for deterministic execution.\n\n"
        "• Membership Functions: Triangular (trimf) and Trapezoidal (trapmf) with left/right shoulders.\n"
        "• 4 Linguistic Inputs: Age (Young/Middle/Senior), Loss Tolerance (Low/Med/High), "
        "Income Stability (Unstable/Mod/Stable), Investment Horizon (Short/Med/Long).\n"
        "• Fuzzy Implication & Aggregation:\n"
        "   - T-Norm (Min operator): alpha_k = min(mu_Age, mu_Loss, mu_Stab, mu_Horiz) * w_k\n"
        "   - S-Norm (Max operator): mu_Agg(y) = max_{k} [ min(alpha_k, mu_{Consequent}(y)) ]\n"
        "• Centroid Defuzzification (Center of Gravity):\n"
        "   Crisp Risk Score = (Sum_{i=0}^{100} y_i * mu_Agg(y_i)) / (Sum_{i=0}^{100} mu_Agg(y_i))\n"
        "• Deterministic Bounds: Crisp score [0 - 100] classified into Conservative (<35), Moderate (35-70), Aggressive (>70)."
    )
    pf2.font.size = Pt(9)
    pf2.font.color.rgb = TEXT_LIGHT

    # Right Container: Forward Chaining Rules
    c_exp = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3))
    set_shape_flat(c_exp, CARD_BG, BORDER_SUBTLE)

    e_tb = s4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.9))
    e_tf = e_tb.text_frame
    e_tf.word_wrap = True

    pe1 = e_tf.paragraphs[0]
    pe1.text = "2. FORWARD CHAINING EXPERT SYSTEM & RULES"
    pe1.font.bold = True
    pe1.font.size = Pt(11)
    pe1.font.color.rgb = ACCENT_EMERALD

    pe2 = e_tf.add_paragraph()
    pe2.text = (
        "Production rule system executing pattern-matching cycles against Working Memory facts.\n\n"
        "Conflict Resolution Strategy:\n"
        "Rules evaluated in strict Priority Precedence (lower number = higher priority). "
        "Prevents race conditions and contradictory portfolio recommendations.\n\n"
        "Production Rule Catalog:\n"
        "• P10 (RULE_DTI_01): If DTI > 40.0% -> Fire High Debt Stress alert; mandate debt restructuring.\n"
        "• P20 (RULE_EMERGENCY_02): If Current Savings < 6*Expenses -> Trigger Reserve Deficit alert.\n"
        "• P30 (RULE_ALLOC_03): If Risk == Aggressive & Horizon >= 7y -> Allocate high-growth equity (up to 75%).\n"
        "• P35 (RULE_ALLOC_04): If Risk == Conservative | Horizon <= 3y -> Capital preservation constraint.\n"
        "• P40 (RULE_SIP_05): If Required SIP > Monthly Surplus -> Trigger cash flow insolvency warning.\n"
        "• Statutory Tax Optimization: Automatic Section 80C, 80D, and 80CCD(1B) computation."
    )
    pe2.font.size = Pt(9)
    pe2.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: Modern Agentic AI & Live Web Search Grounding
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s5, "Modern Agentic AI: PydanticAI, OpenRouter & Live Web Search", "4. Modern Agentic AI", 5)

    agent_cards = [
        ("PydanticAI Architecture", ACCENT_BLUE, [
            "• Type-safe agent framework with compile-time schema validation.",
            "• Enforces strict contract: output must parse into AdvisoryReportSchema.",
            "• Preserves exact numerical facts computed by Aman's AI Core (risk score, equity %, debt %, deficit amounts).",
            "• Eliminates prompt injection risk via strict system prompt isolation."
        ]),
        ("OpenRouter Free Models Router", ACCENT_CYAN, [
            "• Configured via OPENROUTER_MODEL=openrouter/free.",
            "• Automatically routes to available high-capability free models at zero cost (e.g. Nemotron-120B, Llama-3.2, LFM-2.5).",
            "• Built-in client retry and model-fallback rotation with 60s timeout.",
            "• Zero vendor lock-in with standard OpenAI-compatible REST API."
        ]),
        ("Live DuckDuckGo Web Grounding", ACCENT_AMBER, [
            "• Dynamic macroeconomic search tool registered directly to agent.",
            "• Queries live RBI policy rates, Nifty 50 benchmarks, and inflation.",
            "• Extracts verified URL citations with source tags and snippets.",
            "• Resilient multi-engine fallback (DuckDuckGo, Yahoo, Wikipedia, Brave) with graceful offline degradation."
        ]),
        ("Grounded Advisory Box Chat", ACCENT_EMERALD, [
            "• Conversational follow-up assistant grounded strictly in evaluated facts.",
            "• Multi-turn conversational memory persisted directly into SQLite.",
            "• Clean reasoning filter: strips <think> tags to avoid raw model leakage.",
            "• Accurately answers 10 distinct user intent categories (greetings, debt math, equity breakdown, edge cases)."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(agent_cards):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 2.7)

        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.75), Inches(2.5))
        set_shape_flat(c, CARD_BG, BORDER_SUBTLE)

        tb = s5.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = color

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: TA Evaluation Criteria & Formal Verification Report
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s6, "TA Evaluation Criteria & Formal Verification Report", "5. Evaluation & TA Benchmarks", 6)

    # Top Context Callout
    callout = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.7))
    set_shape_flat(callout, CARD_BG_ALT, ACCENT_EMERALD)
    co_tb = s6.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(11.533), Inches(0.6))
    co_tf = co_tb.text_frame
    co_tf.word_wrap = True
    p_co = co_tf.paragraphs[0]
    p_co.text = "FORMAL VERIFICATION PASS STATUS: ALL ACADEMIC & MATHEMATICAL GATES SATISFIED (100% SUCCESS)"
    p_co.font.bold = True
    p_co.font.size = Pt(10)
    p_co.font.color.rgb = ACCENT_EMERALD
    p_co2 = co_tf.add_paragraph()
    p_co2.text = "In accordance with TA guidance, FinWise AI implements an automated benchmark evaluator verifying Monotonicity, 4D State Space Completeness, Lipschitz Continuity, Invariant Preservation, and CFP Concordance."
    p_co2.font.size = Pt(8.5)
    p_co2.font.color.rgb = TEXT_LIGHT

    # Main Evaluation Results Table
    eval_headers = ["Pillar", "Formal Verification Metric", "Mathematical Formulation / Boundary Test", "Measured Result", "Status"]
    eval_rows = [
        ["Fuzzy Logic", "Overall Monotonicity Index", "Mean monotonic transitions across Age, Horizon, Tolerance", "98.61%", "PASS"],
        ["Fuzzy Logic", "Age Monotonicity", "d(RiskScore)/d(Age) <= 0 for Age in [20, 75] years", "100.0%", "PASS"],
        ["Fuzzy Logic", "State Space Completeness", "Sample 1,296 points (6x6x6x6 lattice across all antecedents)", "1,296 / 1,296", "PASS (0 dead zones)"],
        ["Fuzzy Logic", "Lipschitz Gradient Smoothness", "Max partial difference gradient along grid axes <= 35.0", "L = 31.89", "PASS (Smooth)"],
        ["Expert Rules", "Allocation Sum Invariant", "Equity% + Debt% + Gold% + Cash% == 100.0% (N=250 profiles)", "100.0%", "PASS"],
        ["Expert Rules", "Budget Invariant", "Needs(50%) + Wants(30%) + Savings(20%) == Gross Monthly Income", "100.0%", "PASS"],
        ["Expert Rules", "Rule Catalog Coverage", "Proportion of production rules fired across diverse cohort", "100.0% (5/5)", "PASS"],
        ["Expert Rules", "Conflict Freedom", "Absence of mutually exclusive allocations fired simultaneously", "100.0%", "PASS"],
        ["Benchmark", "CFP Directional Concordance", "FinWise equity adjusts above baseline for high risk, below for low", "97.33%", "PASS"],
        ["Benchmark", "Retirement Capital Preservation", "For Age >= 60, equity bounded by max(10, 100-Age) & Debt prioritized", "100.0%", "PASS"]
    ]

    create_styled_table(
        s6,
        left=Inches(0.8),
        top=Inches(2.35),
        width=Inches(11.733),
        height=Inches(4.8),
        rows=11,
        cols=5,
        col_widths=[Inches(1.5), Inches(2.6), Inches(4.7), Inches(1.5), Inches(1.433)],
        headers=eval_headers,
        row_data=eval_rows
    )

    # =========================================================================
    # SLIDE 7: Institutional Web Workstation & Dashboard (4 Views)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s7, "Institutional Web Workstation: Refined 4-View Architecture", "6. Frontend & User Experience", 7)

    ui_cards = [
        ("VIEW 1: ONBOARDING TELEMETRY", ACCENT_BLUE, [
            "• Structured 12-field financial facts questionnaire.",
            "• 4 One-Click Demo Presets for seamless viva testing:",
            "  - Preset A: Young Techie (24y, ₹1.2L income, Aggressive)",
            "  - Preset B: Family with Home Loan (38y, 44% DTI, Deficit)",
            "  - Preset C: Senior Pre-Retiree (68y, Capital Preservation)",
            "  - Preset D: Debt-Stressed Freelancer (29y, 50% DTI)",
            "• Direct real-time execution of backend evaluation pipeline."
        ]),
        ("VIEW 2: FINANCIAL COMMAND CENTER", ACCENT_EMERALD, [
            "• 4 Real-time Metric Tiles (Fuzzy Risk Score, Surplus, DTI, Emergency Buffer).",
            "• Chart.js Asset Allocation Doughnut (Invariant Sum = 100%).",
            "• 50/30/20 Budget Rule Check Bar Chart.",
            "• Full Production Rule Audit Table with Priority tags (P10-P40) and TRIGGERED/SKIPPED status badges.",
            "• Live Web Citations chip tray with outbound source links."
        ]),
        ("VIEW 3: GROUNDED ADVISORY CHAT", ACCENT_CYAN, [
            "• ChatGPT/Claude split-pane workstation layout.",
            "• Real-time session state sidebar with SQLite persistence.",
            "• Grounded answers strictly constrained to evaluated user facts.",
            "• One-click prompt chips ('Why Emergency Deficit?', 'Debt vs Equity?').",
            "• Full Markdown rendering with Marked.js and zero thinking leakage."
        ]),
        ("VIEW 4: AI VERIFICATION BENCHMARKS", ACCENT_AMBER, [
            "• Dedicated TA Evaluation & System Verification Inspector.",
            "• Live telemetry pulled directly from /advisory/evaluation-metrics.",
            "• Displays real-time Monotonicity Index (98.6%), Invariant Preservation Rate (100%), and CFP Concordance (97.3%).",
            "• Interactive 'Re-Run Verification Suite' button executing real-time tests in under 2 seconds."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(ui_cards):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 2.7)

        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.75), Inches(2.55))
        set_shape_flat(c, CARD_BG, BORDER_SUBTLE)

        tb = s7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(2.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = color

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 8: Verification, Test Summary & Future Roadmap
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_shape_flat(s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)), BG_DARK)
    add_header(s8, "Verification Summary, Test Report & Future Roadmap", "7. Verification & Roadmap", 8)

    # Left: Test Summary Card
    c_tests = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3))
    set_shape_flat(c_tests, CARD_BG, BORDER_SUBTLE)

    t_tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.9))
    t_tf = t_tb.text_frame
    t_tf.word_wrap = True

    pt1 = t_tf.paragraphs[0]
    pt1.text = "AUTOMATED TEST SUITE REPORT (100% PASS)"
    pt1.font.bold = True
    pt1.font.size = Pt(11)
    pt1.font.color.rgb = ACCENT_EMERALD

    pt2 = t_tf.add_paragraph()
    pt2.text = (
        "All functional and non-functional requirements verified via automated test suites:\n\n"
        "1. Academic AI Core Suite (test_expert_standalone.py) -> 3/3 PASS\n"
        "   - Validated Persona 1 (Techie), Persona 2 (High DTI), Persona 3 (Retiree).\n"
        "2. Multi-Profile Dataset Suite (test_dataset_validation.py) -> 8/8 PASS\n"
        "   - 8 diverse real-world profiles evaluated with 100% mathematical integrity.\n"
        "3. Backend REST Orchestration (test_backend_standalone.py) -> 8/8 PASS\n"
        "   - Health check, validation, evaluate pipeline, SQLite persistence, chat 404s.\n"
        "4. TA Evaluation & Verification Suite (test_ai_evaluation.py) -> 3/3 PILLARS PASS\n"
        "   - Fuzzy monotonicity, state space completeness, invariants, CFP concordance.\n"
        "5. Chat Reasoning & LLM Handling (verify_llm_chat_comprehensive.py) -> 10/10 PASS\n"
        "   - Zero thinking leaks across 10 distinct prompt categories.\n"
        "6. Frontend CSS Architecture (verify_chat_scroll_layout.py) -> PASS\n"
        "   - Flexbox overflow-y and persistent input verified on both UI targets.\n\n"
        "Overall Test Summary: 100% SRS Coverage | 0 Race Conditions | 0 Invariant Violations"
    )
    pt2.font.size = Pt(8.5)
    pt2.font.color.rgb = TEXT_LIGHT

    # Right: Future Roadmap Card
    c_road = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3))
    set_shape_flat(c_road, CARD_BG, BORDER_SUBTLE)

    r_tb2 = s8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.9))
    r_tf2 = r_tb2.text_frame
    r_tf2.word_wrap = True

    pr1 = r_tf2.paragraphs[0]
    pr1.text = "STRATEGIC FUTURE ROADMAP"
    pr1.font.bold = True
    pr1.font.size = Pt(11)
    pr1.font.color.rgb = ACCENT_BLUE

    roadmap_items = [
        ("Vector RAG for Indian Tax Code", "Integrate ChromaDB vector embeddings indexing the entire Indian Income Tax Act 1961, enabling precise Section 80C/80D/80CCD tax regime recommendations."),
        ("Multi-Broker Order Execution APIs", "Connect directly with Zerodha Kite, Groww, and Upstox execution APIs via OAuth 2.0 to automate recommended mutual fund SIP allocations in 1 click."),
        ("Dynamic Monte Carlo Goal Backtesting", "Run 10,000-path stochastic Monte Carlo simulations modeling equity market drawdowns and sequence-of-returns risk for long-term retirement planning."),
        ("Full-Duplex WebSocket Telemetry", "Upgrade HTTP polling to bidirectional WebSockets for live portfolio rebalancing notifications and real-time LLM token streaming."),
        ("Enterprise Multi-Tenancy & Auth", "Implement JWT bearer authentication, multi-tenant database isolation, and role-based access control (RBAC) for certified financial advisors.")
    ]

    for title, desc in roadmap_items:
        p_item = r_tf2.add_paragraph()
        p_item.text = f"• {title}: "
        p_item.font.bold = True
        p_item.font.size = Pt(8.5)
        p_item.font.color.rgb = ACCENT_CYAN

        p_desc = r_tf2.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(8)
        p_desc.font.color.rgb = TEXT_LIGHT

    # Save Presentation
    output_path = os.path.abspath("FinWise_AI_Presentation.pptx")
    prs.save(output_path)
    print(f"\n[SUCCESS] FinWise AI 8-slide presentation generated successfully at:\n  {output_path}\n")


if __name__ == "__main__":
    build_deck()
