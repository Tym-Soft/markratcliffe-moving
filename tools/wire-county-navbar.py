#!/usr/bin/env python3
"""
Wire the Areas Covered megamenu so the four county column headers
(East Sussex, West Sussex, Surrey, Kent) link to their landing pages.

Substitutes, per file with the right relative path to /areas-covered/:
  <div class="mega-h">East Sussex</div>
    →
  <a class="mega-h" href="{path}east-sussex.html">East Sussex</a>

Idempotent — files that already have the link form are left alone.
Mobile accordion JS in mobile-nav.js already returns early on desktop
(matchMedia max-width 991px), so on desktop the link navigates and on
mobile the accordion toggles. The "By Service" column stays a div.
"""

import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

COUNTIES = [
    ('East Sussex', 'east-sussex.html'),
    ('West Sussex', 'west-sussex.html'),
    ('Surrey',      'surrey.html'),
    ('Kent',        'kent.html'),
]


def main() -> int:
    paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    n_changed = 0
    for p in paths:
        file_dir = os.path.dirname(p)
        html = open(p, encoding='utf-8').read()
        original = html
        for name, slug in COUNTIES:
            href = os.path.relpath(f'areas-covered/{slug}', file_dir or '.').replace(os.sep, '/')
            html = html.replace(
                f'<div class="mega-h">{name}</div>',
                f'<a class="mega-h" href="{href}">{name}</a>',
            )
        if html != original:
            open(p, 'w', encoding='utf-8').write(html)
            n_changed += 1
    print(f'Wired county navbar links on {n_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
