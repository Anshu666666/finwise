import re

with open('report/finwise_architecture_light.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the SVG element
m = re.search(r'(<svg\b[^>]*>.*?</svg>)', html, re.DOTALL)
if not m:
    raise RuntimeError("SVG not found in HTML")

svg_content = m.group(1)

# Ensure xmlns is present on svg root
if 'xmlns=' not in svg_content[:200]:
    svg_content = svg_content.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)

# Prepare self-contained styles for light theme
styles = """
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    :root, svg {
      --bg: #f8fafc;
      --grid: #e2e8f0;
      --canvas-dot: #cbd5e1;
      --text: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --text-faint: #94a3b8;
      --panel: #ffffff;
      --panel-border: #cbd5e1;
      --lane-fill: rgba(248, 250, 252, 0.7);
      --lane-stroke: #cbd5e1;
      --arrow: #64748b;
      --arrow-emphasis: #059669;
      --mask: #ffffff;
      --frontend-fill: rgba(34, 211, 238, 0.15);
      --frontend-stroke: #0891b2;
      --backend-fill: rgba(52, 211, 153, 0.18);
      --backend-stroke: #059669;
      --database-fill: rgba(167, 139, 250, 0.20);
      --database-stroke: #7c3aed;
      --cloud-fill: rgba(251, 191, 36, 0.18);
      --cloud-stroke: #d97706;
      --security-fill: rgba(251, 113, 133, 0.15);
      --security-stroke: #e11d48;
      --messagebus-fill: rgba(251, 146, 60, 0.15);
      --messagebus-stroke: #ea580c;
      --external-fill: rgba(148, 163, 184, 0.18);
      --external-stroke: #64748b;
    }

    svg {
      background: #ffffff;
      font-family: 'JetBrains Mono', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
      color-scheme: light;
    }

    /* Structural boundaries */
    .c-region {
      fill: rgba(241, 245, 249, 0.65);
      stroke: #0284c7;
      stroke-width: 1.5px;
      stroke-dasharray: 6 4;
      rx: 8px;
    }
    .c-security-group {
      fill: rgba(255, 241, 242, 0.5);
      stroke: #e11d48;
      stroke-width: 1.5px;
      stroke-dasharray: 4 3;
      rx: 8px;
    }

    /* Component node rectangles */
    [data-node-id] > rect:not(.c-mask) {
      stroke-width: 1.4px;
      rx: 6px;
    }
    .c-frontend   { fill: var(--frontend-fill);   stroke: var(--frontend-stroke); }
    .c-backend    { fill: var(--backend-fill);    stroke: var(--backend-stroke); }
    .c-database   { fill: var(--database-fill);   stroke: var(--database-stroke); }
    .c-cloud      { fill: var(--cloud-fill);      stroke: var(--cloud-stroke); }
    .c-security   { fill: var(--security-fill);   stroke: var(--security-stroke); }
    .c-external   { fill: var(--external-fill);   stroke: var(--external-stroke); }
    .c-mask       { fill: #ffffff; }

    /* Connection routes */
    .a-default  { stroke: #64748b; stroke-width: 1.5px; fill: none; }
    .a-emphasis { stroke: #0284c7; stroke-width: 2.2px; fill: none; }
    .a-dashed   { stroke: #64748b; stroke-width: 1.5px; stroke-dasharray: 5 4; fill: none; }

    /* Markers */
    .m-default  { fill: #64748b; }
    .m-emphasis { fill: #0284c7; }
    .m-dashed   { fill: #64748b; }
    .m-security { fill: #e11d48; }

    /* Labels & Typography */
    .t-primary {
      fill: #0f172a;
      font-weight: 700;
      font-size: 12.5px;
    }
    .t-muted {
      fill: #475569;
      font-size: 10px;
      font-weight: 500;
    }
    .t-dim {
      fill: #64748b;
      font-size: 9.5px;
    }
    .t-edge-default, .t-edge-emphasis, .t-edge-dashed {
      fill: #334155;
      font-size: 9.5px;
      font-weight: 600;
    }

    /* Component type badges */
    .t-frontend { fill: var(--frontend-stroke); }
    .t-backend  { fill: var(--backend-stroke); }
    .t-database { fill: var(--database-stroke); }
    .t-cloud    { fill: var(--cloud-stroke); }
    .t-security { fill: var(--security-stroke); }
    .t-external { fill: var(--external-stroke); }

    /* Label masks */
    [data-graph-role="structural-frame-label-mask"] {
      rx: 4px;
      fill: #f0fdf4;
      stroke: #86efac;
      stroke-width: 1px;
    }
    [data-composition-frame-kind="security-group"] > [data-graph-role="structural-frame-label-mask"] {
      fill: #fff1f2;
      stroke: #fca5a5;
    }
    g[data-edge-from] > rect.c-mask {
      rx: 5px;
      fill: #ffffff;
      stroke: #e2e8f0;
      stroke-width: 1px;
    }

    /* Sigil icons */
    .semantic-sigil { opacity: 0.85; }
    .sigil-fill { fill: currentColor; }
  </style>
"""

# Inject styles right after <svg ...>
insert_pos = svg_content.find('>') + 1
final_svg = svg_content[:insert_pos] + "\n" + styles + "\n" + svg_content[insert_pos:]

with open('report/images/architecture_diagram.svg', 'w', encoding='utf-8') as out:
    out.write(final_svg)

print("Saved report/images/architecture_diagram.svg! Size:", len(final_svg))
