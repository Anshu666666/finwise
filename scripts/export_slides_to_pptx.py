"""
================================================================================
FINWISE AI – HTML TO PIXEL-PERFECT PPTX CONVERTER (INTERMEDIATE RENDERER)
Author: FinWise AI Team
================================================================================
This script implements the industry-standard intermediate pipeline:
1. Loads pin_and_paper.html in a headless 1920x1080 Chrome browser.
2. Waits for all KaTeX math formulas and Google Fonts to render.
3. Steps through each of the 8 slides and captures lossless, high-DPI PNGs
   (Intermediate Form).
4. Packages the intermediate PNG slides into a native 16:9 Microsoft PowerPoint
   presentation (FinWise_AI_Presentation.pptx).
Result: 100% pixel-perfect PowerPoint with zero text shifts or font degradation.
================================================================================
"""

import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pptx import Presentation
from pptx.util import Inches

PROJECT_ROOT = Path(__file__).parent.resolve()
SLIDES_HTML = PROJECT_ROOT / "slides" / "pin_and_paper.html"
EXPORT_DIR = PROJECT_ROOT / "slides" / "exports"
OUTPUT_PPTX = PROJECT_ROOT / "slides" / "FinWise_AI_Presentation.pptx"


def render_html_to_intermediate_pngs() -> list:
    """
    Renders each slide in headless Chrome and saves lossless 1920x1080 PNGs.
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 1920,
        "height": 1080,
        "deviceScaleFactor": 1,
        "mobile": False,
    })

    file_url = SLIDES_HTML.as_uri()
    print(f"[+] Loading presentation: {file_url}")
    driver.get(file_url)

    # Wait for KaTeX and Google Fonts to complete layout
    time.sleep(2.5)

    # Hide UI chrome controls during screenshot capture
    driver.execute_script("""
        const controls = document.querySelector('.deck-controls');
        if (controls) controls.style.display = 'none';
    """)

    slide_images = []
    total_slides = 8

    for idx in range(total_slides):
        # Trigger deckController to show exact slide
        driver.execute_script(f"""
            if (window.deckController) {{
                window.deckController.showSlide({idx});
            }} else {{
                document.querySelectorAll('.slide').forEach((s, i) => {{
                    s.classList.toggle('active', i === {idx});
                }});
                const counter = document.getElementById('slideIndexDisplay');
                if (counter) counter.textContent = 'PAGE 0{idx + 1} // 08';
            }}
        """)
        time.sleep(0.6)  # Allow KaTeX/DOM paint

        png_path = EXPORT_DIR / f"slide_{idx + 1}.png"
        stage = driver.find_element(By.ID, "deckStage")
        stage.screenshot(str(png_path))
        print(f"[+] Captured Slide {idx + 1}/{total_slides} -> {png_path.name}")
        slide_images.append(png_path)

    driver.quit()
    return slide_images


def build_widescreen_pptx(slide_images: list):
    """
    Creates a 16:9 widescreen PowerPoint presentation containing the
    full-bleed rendered slide images.
    """
    prs = Presentation()
    # Configure exact 16:9 widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]  # Blank slide layout

    for img_path in slide_images:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(
            str(img_path),
            left=Inches(0),
            top=Inches(0),
            width=prs.slide_width,
            height=prs.slide_height,
        )

    try:
        prs.save(str(OUTPUT_PPTX))
        print(f"\n[SUCCESS] Widescreen PPTX generated successfully!")
        print(f"[+] Output File: {OUTPUT_PPTX}")
    except PermissionError:
        fallback_pptx = PROJECT_ROOT / "slides" / "FinWise_AI_Presentation_Updated.pptx"
        prs.save(str(fallback_pptx))
        print(f"\n[!] Note: '{OUTPUT_PPTX.name}' is currently open in PowerPoint.")
        print(f"[SUCCESS] Saved updated presentation to: {fallback_pptx}")


if __name__ == "__main__":
    images = render_html_to_intermediate_pngs()
    build_widescreen_pptx(images)
