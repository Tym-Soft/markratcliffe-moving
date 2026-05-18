#!/usr/bin/env python3
"""Strip all the mobile lead-gen experiments to restore the clean original look:
 - mob-menu-promo
 - mob-menu-availability
 - mob-menu-tiles
 - mob-menu-postcode
 - mob-menu-testimonial
 - mob-menu-cta (trust strip + big call CTA + callback form)
 - mob-menu-foot (email/address block at end of menu)
 - mob-action-bar (floating bottom bar)

Also ensure new-pages.css is linked on every page (still needed for the new pages
content + footer styles).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

# All block patterns we're removing (greedy enough to catch the whole element)
REMOVALS = [
    # Promo banner — single line div
    re.compile(r'\s*<div class="mob-menu-promo">[^<]*<strong>[^<]*</strong>[^<]*</div>', re.S),
    re.compile(r'\s*<div class="mob-menu-promo">.*?</div>', re.S),
    # Availability indicator — single line
    re.compile(r'\s*<div class="mob-menu-availability">[^<]+</div>', re.S),
    # Service tiles (contain inner svgs and links)
    re.compile(r'\s*<div class="mob-menu-tiles">.*?</div>\s*</div>', re.S),
    re.compile(r'\s*<div class="mob-menu-tiles">.*?</a>\s*</div>', re.S),
    # Postcode quick-search
    re.compile(r'\s*<div class="mob-menu-postcode">.*?</form>\s*</div>', re.S),
    re.compile(r'\s*<div class="mob-menu-postcode">.*?</div>\s*</div>', re.S),
    # Testimonial
    re.compile(r'\s*<div class="mob-menu-testimonial">.*?</div>', re.S),
    # CTA block (largest one — has nested form + buttons)
    re.compile(r'\s*<div class="mob-menu-cta"[^>]*>.*?</form>\s*</div>', re.S),
    re.compile(r'\s*<div class="mob-menu-cta"[^>]*>.*?</div>\s*</div>', re.S),
    # Foot
    re.compile(r'\s*<div class="mob-menu-foot">.*?</div>', re.S),
    # Floating action bar
    re.compile(r'\s*<div class="mob-action-bar"[^>]*>.*?</div>\s*</div>', re.S),
    re.compile(r'\s*<div class="mob-action-bar"[^>]*>.*?</a>\s*</div>', re.S),
]


def fix_file(fp: Path) -> dict:
    text = fp.read_text(encoding='utf-8')
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return {'changes': []}
    orig = text
    changes = []

    # Apply each removal pattern multiple times until no more matches
    for pat in REMOVALS:
        new = pat.sub('', text)
        if new != text:
            text = new
            changes.append(pat.pattern[:40])

    # Ensure new-pages.css link is present (needed for footer + new pages styling)
    if 'new-pages.css' not in text:
        rel = fp.relative_to(ROOT)
        P = "../" if len(rel.parts) > 1 else ""
        link_tag = f'<link href="{P}css/new-pages.css" rel="stylesheet">'
        m = re.search(r'<link[^>]+mark-ratcliffe-moving\.css[^>]*>', text)
        if m:
            insert_at = m.end()
            text = text[:insert_at] + '\n  ' + link_tag + text[insert_at:]
        else:
            text = text.replace('</head>', f'  {link_tag}\n</head>', 1)
        changes.append('css-link-added')

    # Add svg dims (defensive)
    text = re.sub(
        r'<svg\s+viewBox="([^"]+)">',
        r'<svg viewBox="\1" width="24" height="24" aria-hidden="true">',
        text
    )

    if text != orig:
        fp.write_text(text, encoding='utf-8')
    return {'file': str(fp.relative_to(ROOT)), 'changes': changes}


def main():
    counts = {'with-changes': 0}
    files = list(ROOT.rglob('*.html'))
    for fp in files:
        r = fix_file(fp)
        if r['changes']:
            counts['with-changes'] += 1
    print(f'Processed {len(files)} files; modified {counts["with-changes"]}.')


if __name__ == "__main__":
    main()
