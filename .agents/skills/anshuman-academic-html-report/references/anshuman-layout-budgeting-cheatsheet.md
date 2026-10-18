# Academic HTML Report Layout & Page Budgeting Cheatsheet

## 1. Physical Dimensions of A4 Portrait

- **Full Sheet Size**: $210\text{mm} \times 297\text{mm}$ ($8.27 \times 11.69\text{ in}$)
- **Standard CSS Print Margins**:
  - Top: $14\text{mm}$
  - Bottom: $14\text{mm}$
  - Left: $16\text{mm}$
  - Right: $16\text{mm}$
- **Printable Content Area**:
  - Width: $210 - (16 + 16) = 178\text{mm}$
  - Height: $297 - (14 + 14) = 269\text{mm}$

---

## 2. Converting Millimeters to Pixels in Web Browsers

At the standard CSS 96 DPI specification:
- $1\text{mm} \approx 3.7795\text{px}$
- Sheet Width ($210\text{mm}$): $\approx 794\text{px}$
- Sheet Height ($297\text{mm}$): $\approx 1123\text{px}$
- Printable Height ($269\text{mm}$): $\approx 1016\text{px}$

When testing locally in a browser viewport (e.g., width 1200px), `.report-sheet` is centered with `max-width: 210mm` so the document looks identical on desktop monitors and on paper.

---

## 3. Strict Vertical Budgeting Formula

For each `<section class="report-page">`, the total height of all child elements MUST satisfy:

$$\sum (\text{Heading Height} + \text{Text Height} + \text{Margin/Padding} + \text{Figures/Tables}) \le 260\text{mm}$$

### Typical Height Consumption Estimates

| DOM Component | Typical Height | Notes |
|---|---|---|
| `h1.chapter-title` | $16\text{mm}$ | Includes font, border, bottom margin |
| `h2.section-heading` | $12\text{mm}$ | Margin-top 12px, margin-bottom 6px |
| Text paragraph (100 words) | $22\text{mm}$ | ~4 lines @ 10pt with 1.42 line-height |
| Single plot (`.img-single`) | $95\text{mm}$ | Max height constraint |
| Dual plot (`.img-dual`) | $64\text{mm}$ | Fits 2 plots per page with captions |
| Triple plot (`.img-triple`) | $48\text{mm}$ | Fits 3 compact sub-figures |
| Vector Architecture Box | $110\text{mm}$ | Fits wide SVG with 1–2 text paragraphs |
| Math Equation (`.math-block`) | $14\text{mm}$ | Display equation with spacing |
| Table (6 rows) | $32\text{mm}$ | Booktabs style with headers |
| Note box (`.note-box`) | $18\text{mm}$ | Highlight / syllabus alignment box |

---

## 4. Preventing Page Spills & Split Artifacts

### 1. `break-after: page` vs `page-break-after: always`
Always use both for legacy and modern Chromium print engine support:
```css
.report-page {
  page-break-after: always;
  break-after: page;
}
```

### 2. Orphan Heading Prevention
Prevent headers from rendering at the very bottom of a page without trailing text:
```css
h1, h2, h3 {
  page-break-after: avoid;
  break-after: avoid;
}
```

### 3. Figure & Table Atomic Containment
Prevent images and tables from breaking in half across page breaks:
```css
.report-figure, .table-container, .math-block {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

---

## 5. Debugging Page Overflow with Browser Tools

To verify whether a page overflows before printing:
1. Open DevTools in Chrome or Edge (`F12`).
2. Press `Ctrl + Shift + P` and type `Rendering`.
3. Choose **Emulate CSS media type** -> Select **print**.
4. Check the scroll height of each `.report-page`. If any page exceeds $\approx 1050\text{px}$, reduce paragraph word count or decrease `.img-*` max-height by 5–10mm.
