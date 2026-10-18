import re

with open('report/images/architecture_diagram.svg', 'r', encoding='utf-8') as f:
    svg = f.read()

print("SVG read successfully, length:", len(svg))

with open('report/finwise_ieee_report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update CSS for .architecture-box
old_css = """    /* Architecture Box (~3:4 Aspect Ratio) */
    .architecture-box {
      border: 1.5px dashed #0284c7;
      background: #f0f9ff;
      border-radius: 4px;
      padding: 6px;
      text-align: center;
      margin: 6px auto;
      max-width: 145mm;
    }
    .architecture-box img {
      width: 100%;
      max-height: 120mm;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border: none;
    }"""

new_css = """    /* Architecture Box (Vector SVG Diagram) */
    .architecture-box {
      border: 1px solid #cbd5e1;
      background: #ffffff;
      border-radius: 6px;
      padding: 6px;
      text-align: center;
      margin: 6px auto;
      max-width: 175mm;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .architecture-box svg {
      width: 100%;
      height: auto;
      max-height: 110mm;
      display: block;
      margin: 0 auto;
      border: none;
    }"""

if old_css in html:
    html = html.replace(old_css, new_css)
    print("Updated .architecture-box CSS")
else:
    print("Warning: old_css not found")

# Replace Figure 1 inner content
old_fig = """        <div class="architecture-box">
          <img src="images/architecture_diagram.png" alt="FinWise AI Architecture Diagram" class="img-single" onerror="this.style.display='none'; document.getElementById('arch-err').style.display='block';">
          <div id="arch-err" style="display:none; padding: 22px; font-family: monospace; font-size: 8.5pt; color: #0284c7;">
            <strong>[Figure 1: Balanced ~3:4 System Architecture Diagram]</strong><br>
            <em>The 2-column Phase 1 / Phase 2 architecture code renders cleanly into this container.</em>
          </div>
        </div>"""

new_fig = f"""        <div class="architecture-box">
{svg}
        </div>"""

if old_fig in html:
    html = html.replace(old_fig, new_fig)
    print("Replaced Figure 1 with inline SVG!")
else:
    print("Warning: old_fig not found")

with open('report/finwise_ieee_report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated report/finwise_ieee_report.html successfully!")
