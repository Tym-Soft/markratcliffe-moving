#!/usr/bin/env python3
"""Three fixes:
 1. Add `new-pages.css` link to every page that's missing it
 2. Hide the old Webflow `.mobile-contct` (duplicate CALL US/EMAIL US bar)
 3. Add explicit width/height attrs to all SVG icons in mobile bars/tiles
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"


def fix_file(fp: Path) -> dict:
    text = fp.read_text(encoding='utf-8')
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return {'changes': []}
    orig = text
    changes = []

    # 1) Add new-pages.css link if missing.
    if 'new-pages.css' not in text:
        rel = fp.relative_to(ROOT)
        P = "../" if len(rel.parts) > 1 else ""
        link_tag = f'<link href="{P}css/new-pages.css" rel="stylesheet">'
        # Insert right after mark-ratcliffe-moving.css link if present
        m = re.search(r'<link[^>]+mark-ratcliffe-moving\.css[^>]*>', text)
        if m:
            insert_at = m.end()
            text = text[:insert_at] + '\n  ' + link_tag + text[insert_at:]
            changes.append('add-css-link')
        else:
            # Insert before </head>
            text = text.replace('</head>', f'  {link_tag}\n</head>', 1)
            changes.append('add-css-link-fallback')

    # 2) Add explicit width/height to SVGs in mobile action bar & tiles & service tiles.
    # Match <svg viewBox="0 0 24 24"> without width/height attrs and add them.
    def fix_svg(m):
        tag = m.group(0)
        if 'width=' in tag and 'height=' in tag:
            return tag
        # Determine size from context — default 24
        return tag.replace('<svg ', '<svg width="24" height="24" aria-hidden="true" ', 1)
    new_text = re.sub(r'<svg\s+viewBox="[^"]+">', fix_svg, text)
    if new_text != text:
        text = new_text
        changes.append('svg-dims')

    if text != orig:
        fp.write_text(text, encoding='utf-8')
    return {'file': str(fp.relative_to(ROOT)), 'changes': changes}


def main():
    counts = {}
    files = list(ROOT.rglob('*.html'))
    for fp in files:
        r = fix_file(fp)
        for c in r['changes']:
            counts[c] = counts.get(c, 0) + 1
    print(f'Processed {len(files)} files:')
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')


if __name__ == "__main__":
    main()
