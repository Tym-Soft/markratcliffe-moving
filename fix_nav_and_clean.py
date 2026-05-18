#!/usr/bin/env python3
"""Final pass on every HTML page:
 1) Ensure jQuery + mark-ratcliffe-moving.js are loaded (for dropdown nav)
 2) Update menu TESTIMONIALS link to reviews.html
 3) Strip dead third-party scripts (AddThis, elfsight) from originals
 4) Strip absurdly large/embedded Webflow JSON metadata blocks from lightbox items
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
JQUERY_TAG = '<script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=54f032c21ccd6c2e19dae5a7" crossorigin="anonymous"></script>'
WF_TAG = '<script defer src="{P}js/mark-ratcliffe-moving.js"></script>'


def path_prefix(fp: Path) -> str:
    rel = fp.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""


def fix_file(fp: Path) -> dict:
    text = fp.read_text(encoding="utf-8")
    original = text
    changes = []
    P = path_prefix(fp)

    # 1) Strip AddThis widget
    if "addthis_widget.js" in text:
        text = re.sub(r'<!--\s*Go to www\.addthis\.com.*?-->\s*', '', text, flags=re.S)
        text = re.sub(r'<script[^>]+addthis_widget\.js[^>]*></script>', '', text)
        changes.append("strip-addthis")

    # 2) Strip elfsight platform script
    if "elfsight" in text:
        text = re.sub(r'<script[^>]+elfsight[^>]*></script>', '', text)
        changes.append("strip-elfsight")

    # 3) Update menu testimonials link → reviews.html
    if 'href="testimonials.html"' in text or 'href="../testimonials.html"' in text:
        text = text.replace('>TESTIMONIALS<', '>REVIEWS<')
        text = text.replace('href="testimonials.html" class="navlink', 'href="reviews.html" class="navlink')
        text = text.replace('href="../testimonials.html" class="navlink', 'href="../reviews.html" class="navlink')
        changes.append("menu-reviews")

    # 4) Ensure jquery + mark-ratcliffe-moving.js present (before </body>)
    needs_jq = "jquery-3.5.1.min" not in text
    needs_wf = "mark-ratcliffe-moving.js" not in text
    if needs_jq or needs_wf:
        scripts_to_add = ""
        if needs_jq:
            scripts_to_add += "  " + JQUERY_TAG + "\n"
        if needs_wf:
            scripts_to_add += "  " + WF_TAG.replace("{P}", P) + "\n"
        text = text.replace("</body>", scripts_to_add + "</body>", 1)
        if needs_jq: changes.append("add-jquery")
        if needs_wf: changes.append("add-wf-js")

    if text != original:
        fp.write_text(text, encoding="utf-8")
    return {"file": str(fp.relative_to(ROOT)), "changes": changes}


def main():
    files = list(ROOT.rglob("*.html"))
    stats = {"strip-addthis": 0, "strip-elfsight": 0, "menu-reviews": 0,
             "add-jquery": 0, "add-wf-js": 0, "unchanged": 0}
    for fp in files:
        r = fix_file(fp)
        if not r["changes"]:
            stats["unchanged"] += 1
        for c in r["changes"]:
            stats[c] = stats.get(c, 0) + 1
    print(f"Processed {len(files)} files:")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
