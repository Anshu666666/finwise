import re

with open('report/finwise_architecture_light.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'(<svg[^>]*data-preset="classic"[^>]*>.*?</svg>)', html, re.DOTALL)
if m:
    svg = m.group(1)
    print("Found SVG! Length:", len(svg))
    print("First 300 chars:", svg[:300])
    with open('report/images/architecture_diagram_raw.svg', 'w', encoding='utf-8') as out:
        out.write(svg)
    print("Saved raw SVG")
else:
    print("Not found")
