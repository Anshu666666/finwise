---
name: anshuman-academic-html-report
description: Create publication-grade, IEEE-style academic project reports, technical whitepapers, and formal multi-page documentation in pure HTML and CSS with exact 1-to-1 A4 print-to-PDF budgeting, MathJax equations, scholarly booktabs tables, and embedded vector architecture diagrams.
risk: unknown
source: finwise-project
date_added: "2026-10-18"
---

# Academic HTML Report Design & Engineering Guide

Use this skill when asked to create, style, budget, or troubleshoot formal academic project reports, IEEE conference-style papers, thesis summaries, or technical engineering reports using pure HTML5 and Vanilla CSS that print or save to PDF with exact page-budget adherence.

---

## 1. Core Architecture & Mental Model

Traditional word processors (Word, Google Docs) and LaTeX often struggle with web presentation, interactive widgets, or modern SVG styling. Conversely, naive HTML-to-PDF exports suffer from arbitrary page splits, orphaned headings, and table cutoffs.

The **Academic HTML Report Pattern** bridges this gap by treating each page as a strictly bounded CSS physical unit (`<section class="report-page">`) inside an A4 container:

```
[Screen View]
  └── .no-print-toolbar (Sticky action bar: Print PDF, live prototype links)
  └── .report-sheet (Centered max-width: 210mm paper card with soft shadow)
       ├── <section class="report-page cover-page"> (Page 1: Title, Institution, Team)
       ├── <section class="report-page"> (Page 2: Abstract, Table of Contents)
       ├── <section class="report-page"> (Page 3: Chapter 1 Introduction)
       ├── ...
       └── <section class="report-page"> (Page N: Benchmarks, Conclusions, References)

[@media print]
  └── Removes shadows, toolbar, background tints
  └── Each .report-page triggers an explicit break-after: page
  └── Exact 1:1 mapping between DOM section and physical PDF page
```

---

## 2. CSS Design System & Print Rules

Place this base stylesheet in the `<style>` block of the HTML document.

### 2.1. The @page & Reset Configuration

```css
@page {
  size: A4 portrait;
  margin: 14mm 16mm 14mm 16mm;
  @bottom-right {
    content: counter(page);
    font-family: 'Times New Roman', Georgia, serif;
    font-size: 8.5pt;
  }
  @bottom-left {
    content: "Project Name · Institution Name (Course/Department)";
    font-family: 'Times New Roman', Georgia, serif;
    font-size: 8pt;
    color: #475569;
  }
}

* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact; /* Crucial: forces background fills and borders to print */
}

body {
  font-family: 'Times New Roman', Times, Georgia, serif;
  font-size: 10pt;
  line-height: 1.42;
  color: #0f172a;
  background: #e2e8f0; /* Soft slate screen background */
  margin: 0;
  padding: 16px;
}
```

### 2.2. Sheet & Page Containers

```css
/* Document container for screen viewing */
.report-sheet {
  max-width: 210mm;
  margin: 0 auto;
  background: #ffffff;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

/* Logical page container: exactly 1 physical A4 page */
.report-page {
  padding: 4mm 0;
  box-sizing: border-box;
  page-break-after: always;
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: #ffffff;
  position: relative;
}

/* Print Overrides */
@media print {
  body {
    background: transparent;
    padding: 0;
  }
  .no-print-toolbar {
    display: none !important;
  }
  .report-sheet {
    box-shadow: none;
    padding: 0;
    max-width: 100%;
  }
  .report-page {
    border: none;
    padding: 12mm 14mm 12mm 14mm;
  }
}
```

---

## 3. Strict Height Budgeting (Preventing Overflows)

The #1 defect in multi-page HTML reports is **page spill**—where a paragraph, table row, or image caption overflows by even 10 pixels, spawning an unwanted blank or semi-empty page.

### 3.1. Proportional Figure Classes

Never include arbitrary-sized images. Always assign images to deterministic height budget classes:

```css
.report-figure {
  margin: 8px 0 10px 0;
  text-align: center;
  page-break-inside: avoid;
}

.report-figure img {
  width: 100%;
  max-width: 155mm;
  height: auto;
  object-fit: contain;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  display: block;
  margin: 0 auto;
}

/* Height budget rules */
.img-single {
  max-height: 95mm !important; /* Single image + substantial text */
}
.img-dual {
  max-height: 64mm !important; /* Exactly two stacked plots + captions */
}
.img-triple {
  max-height: 48mm !important; /* Three stacked plots or screenshots */
}
```

### 3.2. Page Budget Allocation Table

For an A4 page with $14\text{mm}$ margins, total printable vertical height is approximately $269\text{mm}$. Allocate vertical budgets deliberately:

| Page Content Pattern | Heading & Text Budget | Figure / Table Budget | Captions & Padding |
|----------------------|-----------------------|-----------------------|--------------------|
| **Text Only** | ~240mm (800–900 words) | 0mm | 20mm |
| **1 Image + Text** | ~120mm (350–450 words) | 95mm (`.img-single`) | 35mm |
| **2 Stacked Images** | ~60mm (150–200 words) | $2 \times 64\text{mm} = 128\text{mm}$ (`.img-dual`) | 45mm |
| **Architecture Box** | ~90mm (250–300 words) | 110mm (`.architecture-box`) | 40mm |
| **Table + Summary** | ~110mm (300–400 words) | 100mm (`.table-container`) | 30mm |

---

## 4. Academic Front-Matter & Cover Page (Page 1)

Page 1 should serve as a dedicated title and author cover sheet that balances vertically using `justify-content: space-between`.

```html
<section class="report-page cover-page">
  <!-- Institute Banner -->
  <div class="cover-institute-header">
    <div class="cover-institute-name">Indian Institute of Information Technology (IIIT) Kottayam</div>
    <div class="cover-dept-name">Course: CSE311 Artificial Intelligence</div>
  </div>

  <!-- Document Title Area -->
  <div class="cover-title-area">
    <div class="cover-doc-type">B.Tech Project Report</div>
    <div class="cover-title">FinWise AI: Intelligent Financial Advisory System</div>
    <div class="cover-subtitle">
      Combining Continuous Mamdani Fuzzy Inference, Rule-Based Expert Systems, and Grounded AI
    </div>
  </div>

  <!-- Team Members Grid -->
  <div class="cover-meta-grid">
    <div class="cover-meta-title">Project Team Members</div>
    <table class="team-table">
      <tr>
        <td class="team-name">Student Name 1</td>
        <td class="team-roll">2024BCD0001</td>
        <td class="team-name">Student Name 2</td>
        <td class="team-roll">2024BCD0002</td>
      </tr>
    </table>
    <div class="cover-prototype-link">
      <strong>Live Deployed Prototype:</strong> 
      <a href="https://example.com" target="_blank">https://example.com</a>
    </div>
  </div>

  <!-- Cover Footer -->
  <div class="cover-footer">
    Submitted in partial fulfillment of the requirements for CSE311: Artificial Intelligence<br>
    Academic Term: Autumn 2026
  </div>
</section>
```

---

## 5. Scholarly Tables (Booktabs Format)

Standard HTML tables look primitive. Scholarly publications require **Booktabs**-style horizontal rules (heavy outer rules, lighter inner dividers, no vertical rules):

```css
table.formal-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8.8pt;
  line-height: 1.3;
  margin: 0 auto;
}
table.formal-table th {
  border-top: 1.8px solid #0f172a;
  border-bottom: 1.2px solid #0f172a;
  font-weight: bold;
  color: #0f172a;
  padding: 4px 6px;
  background: #f8fafc;
  text-align: center;
}
table.formal-table td {
  border-bottom: 0.6px solid #e2e8f0;
  padding: 3.5px 6px;
  text-align: center;
}
table.formal-table tr:last-child td {
  border-bottom: 1.8px solid #0f172a; /* Heavy closing bottom rule */
}
table.formal-table td.text-left {
  text-align: left;
}
```

---

## 6. Mathematical Equations with MathJax v3

To render LaTeX formulas cleanly on screen and in high-resolution vector print, configure MathJax in the `<head>`:

```html
<!-- MathJax Configuration -->
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      processEscapes: true
    },
    options: {
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
    }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

Format equations with numbered right-aligned markers using flexbox:

```html
<div class="math-block">
  <div class="math-equation">
    $$\mu_{\text{tri}}(x; a, b, c) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$$
  </div>
  <div class="math-num">(1)</div>
</div>
```

```css
.math-block {
  margin: 6px 0;
  padding: 2px 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: center;
}
.math-equation {
  flex: 1;
  text-align: center;
  font-size: 10.2pt;
}
.math-num {
  font-size: 9pt;
  color: #475569;
  padding-left: 10px;
  white-space: nowrap;
}
```

---

## 7. Vector Architecture Diagrams (Archify Pipeline & SVG Embedding)

Embedding vector diagrams directly into the HTML document ensures razor-sharp 300+ DPI text and lines when printing to PDF, without pixelation or blurry raster artifacts.

### 7.1. The End-to-End Archify-to-Report Workflow

```
[System Architecture Model]
       │
       ▼
 1. Author candidate IR (`.archify/candidate.json`)
       │
       ▼
 2. Validate (`archify validate architecture .archify/candidate.json --quality showcase`)
       │  ├── Check bounds separation (boundary-encloses-non-member)
       │  └── Check edge label clearance (≥94px horizontal spacing)
       ▼
 3. Render (`archify render architecture .archify/candidate.json diagram.html --quality showcase`)
       │
       ▼
 4. Extract `<svg>` from the rendered HTML & inject light theme styling
       │  ├── Fix grid pattern bug: fill="none !important;"
       │  └── Add solid white baseplate: <rect width="100%" height="100%" fill="#ffffff"/>
       ▼
 5. Embed inline into report's `<div class="architecture-box">`
```

### 7.2. Step 1: Authoring Architecture IR (`candidate.json`)

Define nodes, boundaries, lanes, and routed edges with semantic roles:

```json
{
  "diagram_type": "architecture",
  "name": "FinWise AI End-to-End System Architecture",
  "description": "Continuous Fuzzy Inference and Rule Engine Pipeline",
  "canvas": { "width": 1320, "height": 520 },
  "boundaries": [
    {
      "id": "core-system",
      "label": "FinWise Core System Boundary",
      "kind": "system",
      "members": ["fastapi", "rule-engine", "fuzzy-engine", "db"]
    }
  ],
  "nodes": [
    { "id": "client", "label": "Investor Client", "role": "frontend", "x": 100, "y": 240, "width": 140, "height": 60 },
    { "id": "fastapi", "label": "FastAPI App Server", "role": "backend", "x": 580, "y": 240, "width": 150, "height": 60 },
    { "id": "fuzzy-engine", "label": "Mamdani Fuzzy Engine", "role": "backend", "x": 800, "y": 140, "width": 160, "height": 60 },
    { "id": "rule-engine", "label": "Priority Rule Engine", "role": "backend", "x": 800, "y": 240, "width": 160, "height": 60 },
    { "id": "db", "label": "SQLite Database", "role": "database", "x": 1040, "y": 240, "width": 140, "height": 60 }
  ],
  "edges": [
    { "from": "client", "to": "fastapi", "label": "HTTP :8000" },
    { "from": "fastapi", "to": "fuzzy-engine", "label": "investor metrics" },
    { "from": "fuzzy-engine", "to": "rule-engine", "label": "crisp score R*" },
    { "from": "rule-engine", "to": "db", "label": "save decisions" }
  ]
}
```

### 7.3. Step 2: Validation Gates & Layout Rules

Run Archify's validator before rendering:
```powershell
archify validate architecture .archify/candidate.json --quality showcase
```

Key validation rules enforced by the compiler:
1. **`layout/boundary-encloses-non-member`**: A boundary box must NOT visually intersect or enclose components that are not listed in its `"members"` array. Keep external services (e.g. LLM APIs, external feeds) completely outside the boundary coordinates.
2. **`layout/label-clearance`**: Horizontal edge labels require a minimum coordinate clearance between source and target nodes ($\ge 94\text{px}$). Avoid placing nodes too close horizontally if edges contain descriptive text labels.

### 7.4. Step 3 & 4: Compiling and Extracting the Light-Theme SVG

Compile to HTML with Archify:
```powershell
archify render architecture .archify/candidate.json report/diagram.html --quality showcase
```

To embed cleanly inside the academic report, extract the `<svg>` element from the compiled HTML and inject the light-theme palette variables into the SVG `<style>` block:

```css
:root, svg {
  --bg: #ffffff;
  --grid: #e9edf2;
  --canvas-dot: #e2e8f0;
  --text: #0f172a;
  --text-muted: #475569;
  --text-dim: #64748b;
  --panel: #ffffff;
  --panel-border: #cbd5e1;
  --arrow: #64748b;
  --arrow-emphasis: #0284c7;
  --frontend-fill: rgba(34, 211, 238, 0.14);
  --frontend-stroke: #0891b2;
  --backend-fill: rgba(52, 211, 153, 0.16);
  --backend-stroke: #059669;
  --database-fill: rgba(167, 139, 250, 0.18);
  --database-stroke: #7c3aed;
  --cloud-fill: rgba(251, 191, 36, 0.16);
  --cloud-stroke: #d97706;
  --security-fill: rgba(251, 113, 133, 0.14);
  --security-stroke: #e11d48;
}
```

### 7.5. Critical SVG Gotchas & Pitfalls

1. **The Black Sawtooth / Checkerboard Bug**:
   - In standard W3C SVG, an unstyled `<pattern>` path defaults to `fill: black`. If using Archify's background grid pattern:
     ```html
     <!-- WRONG: Pattern path without fill renders as a dense black optical checkerboard -->
     <pattern id="grid">
       <path d="M 30 0 L 0 0 0 30" class="c-grid"/>
     </pattern>
     
     <!-- CORRECT: Explicitly declare fill="none !important;" and stroke in style or attribute -->
     <pattern id="grid">
       <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e9edf2" stroke-width="0.5" class="c-grid"/>
     </pattern>
     ```
     And in CSS:
     ```css
     .c-grid { fill: none !important; stroke: #e9edf2; stroke-width: 0.5px; }
     ```
2. **Solid White Baseplate**: Always insert `<rect width="100%" height="100%" fill="#ffffff" rx="8"/>` as the very first element inside `<svg>` so the diagram never displays transparent background artifacts during PDF printing.

### 7.6. In-Report Embedding Container

```html
<div class="report-figure">
  <div class="architecture-box">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1320 518" role="img">
      <!-- Clean, self-contained SVG diagram -->
    </svg>
  </div>
  <div class="figure-caption">
    <strong>Fig 1.</strong> FinWise AI End-to-End System Architecture.
  </div>
</div>
```

```css
.architecture-box {
  border: 1px solid #cbd5e1;
  background: #ffffff;
  border-radius: 6px;
  padding: 6px;
  text-align: center;
  margin: 6px auto;
  max-width: 175mm;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
.architecture-box svg {
  width: 100%;
  height: auto;
  max-height: 110mm;
  display: block;
  margin: 0 auto;
}
```

---

## 8. Interactive Screen Toolbar

Add a top navigation toolbar for users viewing the file directly in a web browser. Ensure it hides completely during printing.

```html
<div class="no-print-toolbar">
  <div>
    <span style="font-weight:700;">Project Report</span> · CSE311 Artificial Intelligence
  </div>
  <div>
    <a href="https://example.com" target="_blank" class="toolbar-link">🌐 Live Prototype</a>
    <button class="btn-pdf" onclick="window.print()">
      🖨️ Print / Save as PDF
    </button>
  </div>
</div>
```

```css
.no-print-toolbar {
  max-width: 210mm;
  margin: 0 auto 14px auto;
  background: #0f172a;
  color: #ffffff;
  padding: 10px 18px;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.no-print-toolbar .btn-pdf {
  background: #2563eb;
  color: #ffffff;
  font-weight: 700;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}
.no-print-toolbar .btn-pdf:hover {
  background: #1d4ed8;
}
@media print {
  .no-print-toolbar {
    display: none !important;
  }
}
```

---

## 9. Verification & Quality Assurance Protocol

Before delivering the final report to the user:

1. **Verify Section-to-Page Count**:
   Count the `<section class="report-page">` tags in the HTML file. If the report claims to be 14 pages, there must be exactly 14 `<section class="report-page">` elements.
2. **Verify Heading Page-Break Hygiene**:
   Ensure `h1, h2, h3` have `page-break-after: avoid;` to prevent orphan titles sitting at the bottom of pages.
3. **Verify Citation Anchors**:
   Ensure every in-text citation `<a href="#ref1" class="cite-link">[1]</a>` links to a matching `<li id="ref1">` in the References chapter.
4. **Browser Subagent Visual Inspection**:
   Run a browser subagent to navigate to `file:///path/to/report.html`, take viewport screenshots of key pages (Cover, Architecture Figure, Data Tables, and Conclusion), and verify:
   - No horizontal scrollbars.
   - No pattern filling bugs on diagrams.
   - Clean MathJax LaTeX rendering without raw LaTeX source code showing.
   - Text is justified with no awkward river gaps.
