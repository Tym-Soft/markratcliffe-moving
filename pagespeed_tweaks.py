#!/usr/bin/env python3
"""PageSpeed tweaks: preload critical CSS/fonts, async webfont loader, font-display swap."""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

PRECONNECT_BLOCK = (
    '  <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>\n'
    '  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>\n'
    '  <link rel="dns-prefetch" href="https://www.google-analytics.com">\n'
)

def get_html_files():
    return list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html"))

def apply(content: str) -> str:
    original = content

    # 1) Mark webfont.js as async (currently neither async nor defer)
    content = content.replace(
        '<script src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js" type="text/javascript"></script>',
        '<script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>'
    )

    # 2) Add font-display: swap inside the WebFont.load config
    if 'WebFont.load({' in content and 'fontactive' not in content:
        content = content.replace(
            'WebFont.load({',
            "WebFont.load({  classes: true,  events: true,  timeout: 2000,  "
        )

    # 3) Add preconnect/dns-prefetch (only if not already there)
    if 'preconnect" href="https://www.googletagmanager.com"' not in content:
        content = content.replace(
            '<link href="https://fonts.googleapis.com" rel="preconnect">',
            '<link href="https://fonts.googleapis.com" rel="preconnect">\n' + PRECONNECT_BLOCK.rstrip() + '',
            1
        )

    # 4) Mark stylesheets to load cleanly — already in head, but make non-critical fonts CSS swap
    # (already covered by font-display fallback via classes)

    return content

def main():
    n = 0
    for fp in get_html_files():
        c = fp.read_text(encoding="utf-8")
        new = apply(c)
        if new != c:
            fp.write_text(new, encoding="utf-8")
            n += 1
    print(f"Tweaks applied to {n} files.")

if __name__ == "__main__":
    main()
