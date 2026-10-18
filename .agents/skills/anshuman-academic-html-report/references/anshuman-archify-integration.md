# Archify-to-Report Integration Guide

This guide details the exact automated pipeline to generate, validate, extract, and theme an Archify system architecture diagram for direct embedding into an academic HTML report.

---

## 1. Candidate Architecture IR (`candidate.json`)

Store the diagram specification in `.archify/candidate.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/tt-a1i/archify/main/schemas/architecture.json",
  "diagram_type": "architecture",
  "name": "FinWise AI End-to-End System Architecture",
  "description": "Continuous Fuzzy Inference and Rule Engine Pipeline",
  "canvas": {
    "width": 1320,
    "height": 520
  },
  "boundaries": [
    {
      "id": "core-system",
      "label": "FinWise Core System Boundary",
      "kind": "system",
      "members": ["fastapi", "rule-engine", "fuzzy-engine", "db"]
    }
  ],
  "nodes": [
    {
      "id": "client",
      "label": "Investor Client",
      "sublabel": "Browser / Mobile View",
      "role": "frontend",
      "x": 100,
      "y": 240,
      "width": 140,
      "height": 60
    },
    {
      "id": "fastapi",
      "label": "FastAPI App Server",
      "sublabel": "REST API & Routing",
      "role": "backend",
      "x": 580,
      "y": 240,
      "width": 150,
      "height": 60
    },
    {
      "id": "fuzzy-engine",
      "label": "Mamdani Fuzzy Engine",
      "sublabel": "4 Inputs + Centroid FIS",
      "role": "backend",
      "x": 800,
      "y": 140,
      "width": 160,
      "height": 60
    },
    {
      "id": "rule-engine",
      "label": "Priority Rule Engine",
      "sublabel": "Conflict Res. & Invariants",
      "role": "backend",
      "x": 800,
      "y": 240,
      "width": 160,
      "height": 60
    },
    {
      "id": "db",
      "label": "SQLite Database",
      "sublabel": "Users, Allocations, Logs",
      "role": "database",
      "x": 1040,
      "y": 240,
      "width": 140,
      "height": 60
    }
  ],
  "edges": [
    {
      "id": "e-client-api",
      "from": "client",
      "to": "fastapi",
      "label": "HTTP :8000"
    },
    {
      "id": "e-api-fuzzy",
      "from": "fastapi",
      "to": "fuzzy-engine",
      "label": "investor metrics"
    },
    {
      "id": "e-fuzzy-rule",
      "from": "fuzzy-engine",
      "to": "rule-engine",
      "label": "crisp score R*"
    },
    {
      "id": "e-rule-db",
      "from": "rule-engine",
      "to": "db",
      "label": "save decisions"
    }
  ]
}
```

---

## 2. Compilation Commands

```powershell
# 1. Validate IR schema and Manhattan routing
archify validate architecture .archify/candidate.json --quality showcase

# 2. Render to standalone HTML
archify render architecture .archify/candidate.json report/diagram.html --quality showcase
```

---

## 3. Automated SVG Extraction & Light Theme Patching Script

Save this script as `extract_and_theme_svg.py` to convert the rendered Archify HTML into a clean, standalone, light-themed SVG ready for report embedding:

```python
import re

def extract_and_theme(html_path: str, svg_output_path: str):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract the SVG element
    m = re.search(r'(<svg\b[^>]*>.*?</svg>)', html, re.DOTALL)
    if not m:
        raise ValueError("No SVG found in Archify HTML output")

    svg = m.group(1)

    # 1. Enforce light theme color variables
    light_style = """
  <style>
    :root, svg {
      --bg: #ffffff;
      --grid: #e9edf2;
      --canvas-dot: #e2e8f0;
      --text: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --text-faint: #94a3b8;
      --panel: #ffffff;
      --panel-border: #cbd5e1;
      --lane-fill: rgba(248, 250, 252, 0.7);
      --lane-stroke: #cbd5e1;
      --arrow: #64748b;
      --arrow-emphasis: #0284c7;
      --mask: #ffffff;
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
      --external-fill: rgba(148, 163, 184, 0.16);
      --external-stroke: #64748b;
    }
    svg {
      background: #ffffff;
      color-scheme: light;
      border-radius: 8px;
    }
    .c-grid {
      fill: none !important;
      stroke: #e9edf2 !important;
      stroke-width: 0.5px;
    }
  </style>
"""
    # Replace existing SVG style with light theme style
    svg = re.sub(r'<style>.*?</style>', light_style, svg, flags=re.DOTALL)

    # 2. Fix the Black Sawtooth Bug: Enforce fill="none" on the pattern path
    svg = re.sub(
        r'(<path[^>]*class="c-grid"[^>]*)>',
        lambda match: match.group(0).replace('class="c-grid"', 'fill="none" stroke="#e9edf2" class="c-grid"')
        if 'fill=' not in match.group(0) else match.group(0),
        svg
    )

    # 3. Insert solid white background baseplate directly after <style>
    if '<rect width="100%" height="100%" fill="#ffffff"' not in svg:
        svg = re.sub(r'(</style>)', r'\1\n  <rect width="100%" height="100%" fill="#ffffff" rx="8"/>', svg)

    with open(svg_output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"[OK] Clean light-theme SVG exported to: {svg_output_path}")

if __name__ == "__main__":
    extract_and_theme("report/diagram.html", "report/images/architecture_diagram.svg")
```

---

## 4. Embedding in the Report

In your report's Chapter 3 (`<section class="report-page">`), place the SVG inside `.architecture-box`:

```html
<div class="report-figure">
  <div class="architecture-box">
    <!-- Paste clean SVG directly here -->
  </div>
  <div class="figure-caption">
    <strong>Fig 1.</strong> FinWise AI End-to-End System Architecture (~3:4 Aspect Ratio).
  </div>
</div>
```
