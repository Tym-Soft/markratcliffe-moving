#!/usr/bin/env python3
"""Add the trust strip (4.9 / 5 · 120+ reviews | BAR member | ...) to every
hero card that doesn't already have it. The homepage already has it inline;
this fills in the inner pages so every banner shows the same trust block.

Idempotent: skips pages that already contain `class="hp-trust-strip"`.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'admin-portal-xK7p9q', 'worker', '.git', 'node_modules',
             '.img-staging', 'tools'}

TRUST_STRIP = '''<div class="hp-trust-strip">
        <span class="hp-rating"><strong>4.9</strong> / 5 &middot; 120+ reviews</span>
        <span class="hp-trust-sep">|</span>
        <span>BAR member</span>
        <span class="hp-trust-sep">|</span>
        <span>BS 8564 accredited</span>
        <span class="hp-trust-sep">|</span>
        <span>APG protected deposits</span>
      </div>'''

# Patterns to inject into. For each, place the trust strip just before
# the closing </div> of the card wrapper.
CARD_PATTERNS = [
    # .np-hero-card — closed by </div> followed by <aside class="hp-hero-quote-card"
    (re.compile(r'(\s*)</div>(\s*<aside class="hp-hero-quote-card")', re.IGNORECASE), 'np-hero-card'),
    # .ac-hero-card — same pattern
    # .th-hero-card — same pattern
    # All three end the same way: </div>(whitespace)<aside class="hp-hero-quote-card"
]

# For .lp-hero-flex pages: the trust strip goes inside the FIRST .lp-hero-cell
# (the one with the title + copy, NOT the one that now holds our card).
LP_FIRST_CELL_RE = re.compile(
    r'(<div class="lp-hero-cell">\s*<div class="np-kicker">.*?</div>\s*<h1[^>]*>.*?</h1>\s*<p[^>]*>.*?</p>\s*)</div>',
    re.IGNORECASE | re.DOTALL
)


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)


def process_file(path: Path):
    try:
        html = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f'read error: {e}'

    # Skip if no card on this page at all.
    if 'hp-hero-quote-card' not in html:
        return False, 'no card'

    # Skip if trust strip already in the hero card area.
    # Check by counting occurrences — the homepage already has one in the
    # hero, so 1 occurrence on homepage = already done. Inner pages might
    # have 0 = needs adding.
    # Simpler heuristic: if hp-trust-strip immediately precedes the
    # aside hp-hero-quote-card, it's already done.
    if re.search(r'class="hp-trust-strip"[^<]*<.*?</div>\s*<aside class="hp-hero-quote-card"', html, re.DOTALL):
        return False, 'already has trust strip'

    new_html = html
    changed = False

    # Try the np-hero / ac-hero / th-hero pattern: close </div> followed by aside.
    pattern = re.compile(r'(\s*)</div>(\s*)<aside class="hp-hero-quote-card"', re.IGNORECASE)
    if pattern.search(new_html):
        new_html, n = pattern.subn(
            lambda m: m.group(1) + '  ' + TRUST_STRIP + '\n' + m.group(1) + '</div>' + m.group(2) + '<aside class="hp-hero-quote-card"',
            new_html,
            count=1
        )
        if n > 0:
            changed = True

    # If we didn't match the np-hero pattern, try the lp-hero-cell pattern.
    if not changed:
        def lp_inject(m):
            return m.group(1) + '\n        ' + TRUST_STRIP + '\n      </div>'
        new_html, n = LP_FIRST_CELL_RE.subn(lp_inject, new_html, count=1)
        if n > 0:
            changed = True

    if not changed:
        return False, 'no card-close pattern matched'

    path.write_text(new_html, encoding='utf-8')
    return True, 'updated'


def main():
    changed = 0
    skipped = 0
    failed = []
    for path in sorted(ROOT.rglob('*.html')):
        if is_skipped(path):
            continue
        ok, msg = process_file(path)
        rel = path.relative_to(ROOT)
        if ok:
            changed += 1
        else:
            if msg in ('no card', 'already has trust strip'):
                skipped += 1
            else:
                failed.append((rel, msg))
    print(f'Done. {changed} updated, {skipped} skipped.')
    if failed:
        print(f'{len(failed)} failures:')
        for r, m in failed[:25]:
            print(f'  - {r}: {m}')
    return 0 if not failed else 1


if __name__ == '__main__':
    sys.exit(main())
