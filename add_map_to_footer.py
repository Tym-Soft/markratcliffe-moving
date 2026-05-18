#!/usr/bin/env python3
"""Move/place the Google Map into the footer on every page (once).

Original Webflow pages: <div class="footer"> — add map as first child band
New np-footer pages: <footer class="np-footer"> — add map as first child band
Removes any existing standalone <div class="maps-wrapper"> blocks first to avoid duplicates.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

MAP_IFRAME = ('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2523.049709930351!2d0.29392331613135825!3d50.77465207183167!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47df7392bfec7151%3A0xf536886de6399c2e!2sMark+Ratcliffe+Moving+%26+Storage+Ltd!5e0!3m2!1sen!2suk!4v1549285879259" '
              'width="100%" height="100%" frameborder="0" style="border:0" allowfullscreen="" loading="lazy" '
              'title="Mark Ratcliffe Moving &amp; Storage Ltd — Lower Dicker location map"></iframe>')

MAP_BLOCK_WEBFLOW = f'''  <div class="footer-map-wrapper">
    <div class="footer-map">{MAP_IFRAME}</div>
  </div>
'''

MAP_BLOCK_NEW = f'''    <div class="np-footer-map">{MAP_IFRAME}</div>
'''


def process(fp: Path) -> dict:
    text = fp.read_text(encoding="utf-8")
    orig = text
    info = {"file": str(fp.relative_to(ROOT)), "actions": []}

    # Skip redirect stubs (tiny pages with meta-refresh)
    if "http-equiv=\"refresh\"" in text and len(text) < 2000:
        return info

    # 1) Remove any existing standalone maps-wrapper (above the footer in originals)
    standalone = re.compile(
        r'<div class="maps-wrapper">\s*<div class="google-map w-embed w-iframe">.*?</iframe></div>\s*</div>\s*',
        re.S
    )
    if standalone.search(text):
        text = standalone.sub('', text)
        info["actions"].append("removed-standalone")

    # 2) Remove any previously-injected footer map (to keep idempotent)
    prev_webflow = re.compile(r'<div class="footer-map-wrapper">.*?</div>\s*</div>\s*', re.S)
    prev_new = re.compile(r'<div class="np-footer-map">.*?</div>\s*', re.S)
    text = prev_webflow.sub('', text)
    text = prev_new.sub('', text)

    # 3) Insert into the appropriate footer
    if '<footer class="np-footer">' in text:
        new_text = text.replace(
            '<footer class="np-footer">\n    <div class="np-footer-grid">',
            f'<footer class="np-footer">\n{MAP_BLOCK_NEW}    <div class="np-footer-grid">',
            1
        )
        if new_text != text:
            info["actions"].append("inserted-np-footer-map")
            text = new_text
    elif '<div class="footer">' in text:
        new_text = text.replace(
            '<div class="footer">',
            f'<div class="footer">\n{MAP_BLOCK_WEBFLOW}',
            1
        )
        if new_text != text:
            info["actions"].append("inserted-webflow-footer-map")
            text = new_text

    if text != orig:
        fp.write_text(text, encoding="utf-8")
    return info


def main():
    files = list(ROOT.rglob("*.html"))
    counts = {}
    for fp in files:
        r = process(fp)
        for a in r["actions"]:
            counts[a] = counts.get(a, 0) + 1
    print(f"Processed {len(files)} files.")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
