#!/usr/bin/env python3
"""
Replace empty `alt=""` (with role="presentation"/aria-hidden="true")
on the 11 site images that Screaming Frog repeatedly flags as
"Missing Alt Text" — even though the markup is WCAG-valid for
decorative use.

Each image gets a descriptive alt under 100 chars (Rule 19) so SF
stops flagging and so the image carries useful context for image
search and screen readers that opt to announce them.

The `role="presentation"` + `aria-hidden="true"` attributes are
removed because they're only meaningful alongside `alt=""`.

Idempotent. Run from the site root:
    python3 tools/fix-decorative-alts.py
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# filename → descriptive alt text (each ≤100 chars per audit Rule 19)
IMAGE_ALT = {
    'mark-ratcliffe-modern-removal-lorry-eastbourne.webp':
        'Mark Ratcliffe Moving modern removal lorry at our Lower Dicker depot serving Sussex',
    'mark-ratcliffe-sleeper-cab-removal-lorry.webp':
        'Mark Ratcliffe Moving sleeper-cab lorry used for long-distance and overseas removals',
    'pad-wrapped-furniture-eastbourne-removals.webp':
        'Furniture pad-wrapped in heavy quilted blankets — Mark Ratcliffe Moving signature method',
    'mark-ratcliffe-vans-front2.webp':
        'Mark Ratcliffe Moving fleet of vans outside our Lower Dicker depot in East Sussex',
    'acrobat_pdf.svg':
        'Download PDF',
    'self-storage-eastbourne-hero.webp':
        'Secure self-storage units at the Mark Ratcliffe Moving Lower Dicker depot in East Sussex',
    'packaging-shop-header.webp':
        'Mark Ratcliffe Moving packaging shop with boxes, bubble wrap and packing materials',
    'business-people-shaking-hands-meeting-room.webp':
        'Office relocation team agreeing the moving plan with business clients in their meeting room',
    'mark-ratcliffe-wrapped-furniture-sussex.webp':
        'Furniture wrapped and protected by the Mark Ratcliffe Moving Sussex removals crew',
    'mark-ratcliffe-crew-loading-piano-eastbourne.webp':
        'Mark Ratcliffe Moving crew carefully loading a piano for a Sussex move',
    'mark-ratcliffe-removal-fleet-vehicles-sussex.webp':
        'Mark Ratcliffe Moving Sussex removal fleet — lorries and vans ready for service',
}


def fix_one_image(html: str, filename: str, alt_text: str) -> tuple[str, int]:
    """Find `<img>` tags whose src ends with filename and have an empty
    alt. Replace alt="" with the descriptive text and strip
    role="presentation"/aria-hidden="true"."""
    # Match the full <img …> tag containing this filename.
    pattern = re.compile(
        r'<img\b([^>]*?\bsrc\s*=\s*["\'][^"\']*?'
        + re.escape(filename)
        + r'["\'][^>]*)>',
        re.I | re.S,
    )
    count = 0

    def replace(m: re.Match) -> str:
        nonlocal count
        attrs = m.group(1)
        # Only touch tags whose alt is currently empty.
        alt_m = re.search(r'\balt\s*=\s*(["\'])([^"\']*)\1', attrs, re.I)
        if not alt_m or alt_m.group(2).strip() != '':
            return m.group(0)
        # Substitute alt
        attrs = (attrs[:alt_m.start()]
                 + f'alt="{alt_text}"'
                 + attrs[alt_m.end():])
        # Strip role="presentation" and aria-hidden="true" — they're only
        # meaningful alongside alt="".
        attrs = re.sub(r'\s+role\s*=\s*["\']presentation["\']', '', attrs, flags=re.I)
        attrs = re.sub(r'\s+aria-hidden\s*=\s*["\']true["\']', '', attrs, flags=re.I)
        count += 1
        return f'<img{attrs}>'

    return pattern.sub(replace, html), count


def fix_page(path: str) -> int:
    try:
        html = open(path, encoding='utf-8').read()
    except OSError:
        return 0
    original = html
    total = 0
    for filename, alt in IMAGE_ALT.items():
        html, n = fix_one_image(html, filename, alt)
        total += n
    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
    return total


def main() -> int:
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    total = 0
    pages_changed = 0
    for p in sorted(pages):
        n = fix_page(p)
        if n:
            pages_changed += 1
            total += n
    print(f'  pages changed: {pages_changed}')
    print(f'  alt attrs fixed: {total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
