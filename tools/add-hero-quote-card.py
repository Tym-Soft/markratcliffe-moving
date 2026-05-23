#!/usr/bin/env python3
"""Add the Quick Estimate card to every page with a .np-hero banner.

For each eligible page:
  - Wraps the existing <div class="np-hero-inner"> children in a
    <div class="np-hero-card">.
  - Appends an <aside class="hp-hero-quote-card">…</aside> with the
    quick-quote markup.
  - Links the shared /css/hero-quote-card.css stylesheet in <head>.
  - Loads /js/hero-quote-card.js (deferred) before </body>.

Idempotent: re-running on an already-processed page is a no-op.

Skipped (commercial intent is low or the page is the calculator
destination itself):
  - 404.html
  - privacy-policy.html
  - terms-conditions-and-insurance-details.html
  - mark-ratcliffe-moving-online-removals-quote.html (already an iframe)
  - resources/storage-calculator.html (the calculator itself)
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'admin-portal-xK7p9q', 'worker', '.git', 'node_modules',
             '.img-staging', 'tools'}
SKIP_FILES = {
    '404.html',
    'privacy-policy.html',
    'terms-conditions-and-insurance-details.html',
    'mark-ratcliffe-moving-online-removals-quote.html',
    'resources/storage-calculator.html',
}

CSS_VERSION = '20260523'
JS_VERSION = '20260523'

QUOTE_CARD_HTML = '''
      <aside class="hp-hero-quote-card" aria-label="Quick estimate">
        <div class="hpqq-title" role="heading" aria-level="2">Get an instant estimate</div>
        <p class="hpqq-hint">Pick your home size, add the round-trip miles &mdash; we&rsquo;ll show a figure in real time.</p>

        <div class="hpqq-section">
          <span class="hpqq-label">Home size</span>
          <div class="hpqq-beds" role="radiogroup" aria-label="Home size">
            <button type="button" class="hpqq-bed" data-bed="tiny" data-cuft="300"  aria-pressed="false">Tiny</button>
            <button type="button" class="hpqq-bed" data-bed="1bed" data-cuft="500"  aria-pressed="false">1-bed</button>
            <button type="button" class="hpqq-bed" data-bed="2bed" data-cuft="800"  aria-pressed="false">2-bed</button>
            <button type="button" class="hpqq-bed is-active" data-bed="3bed" data-cuft="1000" aria-pressed="true">3-bed</button>
            <button type="button" class="hpqq-bed" data-bed="4bed" data-cuft="1800" aria-pressed="false">4-bed</button>
            <button type="button" class="hpqq-bed" data-bed="5bed" data-cuft="2800" aria-pressed="false">5+ bed</button>
          </div>
        </div>

        <div class="hpqq-section">
          <label class="hpqq-label" for="hpqq-miles">Round-trip miles</label>
          <input id="hpqq-miles" class="hpqq-input" type="number" min="0" value="0" inputmode="numeric">
          <span class="hpqq-mini">Depot &rarr; home &rarr; new home &rarr; depot.</span>
        </div>

        <div class="hpqq-result" role="status" aria-live="polite">
          <span class="hpqq-result-label">Estimate</span>
          <div class="hpqq-result-prices">
            <span class="hpqq-net">&pound;<span id="hpqq-net-amt">&mdash;</span></span>
            <span class="hpqq-gross">&pound;<span id="hpqq-gross-amt">&mdash;</span> <em>inc. VAT</em></span>
          </div>
        </div>

        <a href="{calc_url}?bed=3bed&amp;miles=0" id="hpqq-cta" class="hpqq-cta">Refine &amp; send quote &rarr;</a>

        <p class="hpqq-foot">Indicative figure. Final quote after free survey &mdash; pad-wrap, packing materials, access &amp; antiques may adjust the price.</p>
      </aside>
'''

NP_HERO_OPEN_RE = re.compile(
    r'(<header\s+class="np-hero">\s*<div\s+class="np-hero-inner">)',
    re.IGNORECASE
)
# Match the closing </div> that closes np-hero-inner. The inner div content
# typically ends with </div> right before either <img class="np-hero-bg" or
# the closing </header>.
NP_HERO_INNER_CLOSE_RE = re.compile(
    r'(</div>)\s*(<img[^>]*class="np-hero-bg[^"]*"[^>]*>\s*</header>)',
    re.IGNORECASE | re.DOTALL
)

# Alternative hero pattern (areas-covered + man-and-van pages):
#   <div class="hp-header inner ...">
#     <div class="_1200-wrapper">
#       <div class="lp-hero-flex">
#         <div class="lp-hero-cell">...title+copy...</div>
#         <div class="lp-hero-cell">
#           <h2>How we can help...</h2>
#           <div class="form-wrapper..."><script src="cognitoforms..."></script></div>
#         </div>
#       </div>
#   ...
# We swap the second cell's content for the quick-quote card.
LP_SECOND_CELL_RE = re.compile(
    r'<div class="lp-hero-cell">\s*<h2[^>]*>[^<]*</h2>\s*<div class="form-wrapper[^"]*">\s*<div class="w-embed[^"]*">\s*<script[^>]*cognitoforms[^>]*></script>\s*</div>\s*</div>\s*</div>',
    re.IGNORECASE | re.DOTALL
)

CSS_LINK_TOKEN = 'hero-quote-card.css'
JS_SRC_TOKEN = 'hero-quote-card.js'


def rel_prefix(path: Path) -> str:
    """Return relative URL prefix to the site root for a page at `path`."""
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1  # 0 for root files, 1 for services/foo.html, etc.
    return '../' * depth if depth > 0 else ''


def is_skipped(path: Path) -> bool:
    rel = str(path.relative_to(ROOT)).replace(os.sep, '/')
    if rel in SKIP_FILES:
        return True
    if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
        return True
    # Skip Google verification stubs (single-purpose pages).
    if path.name.startswith('google') and path.name.endswith('.html'):
        return True
    return False


def already_done(html: str) -> bool:
    return 'hp-hero-quote-card' in html or 'class="np-hero-card"' in html


def inject_card(html: str, calc_url: str) -> str:
    """Wrap np-hero-inner children in .np-hero-card and append the quote card."""
    # 1. Open: <header class="np-hero"><div class="np-hero-inner">
    #    → ... + <div class="np-hero-card">
    m = NP_HERO_OPEN_RE.search(html)
    if not m:
        return html
    open_end = m.end()
    html = html[:open_end] + '\n      <div class="np-hero-card">' + html[open_end:]

    # 2. Close: find the </div> that closes np-hero-inner and insert
    #    </div> (np-hero-card close) + quote card aside before it.
    card = QUOTE_CARD_HTML.format(calc_url=calc_url)
    def closer_repl(mc):
        return '</div>\n' + card + '      ' + mc.group(1) + mc.group(2)
    html_new = NP_HERO_INNER_CLOSE_RE.sub(closer_repl, html, count=1)
    if html_new == html:
        # No np-hero-bg img/closing-header pattern — fall back: try to close
        # before </header> alone.
        fallback = re.sub(
            r'(</div>)\s*(</header>)',
            lambda m: '</div>\n' + card + '      ' + m.group(1) + m.group(2),
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        html_new = fallback
    return html_new


def inject_css_link(html: str, css_href: str) -> str:
    if CSS_LINK_TOKEN in html:
        return html
    link_tag = f'  <link rel="stylesheet" href="{css_href}?v={CSS_VERSION}">\n'
    # Insert just before </head>.
    return re.sub(r'(\s*</head>)', '\n' + link_tag + r'\1', html, count=1, flags=re.IGNORECASE)


def inject_js_script(html: str, js_src: str) -> str:
    if JS_SRC_TOKEN in html:
        return html
    script_tag = f'  <script defer src="{js_src}?v={JS_VERSION}"></script>\n'
    return re.sub(r'(\s*</body>)', '\n' + script_tag + r'\1', html, count=1, flags=re.IGNORECASE)


def process_file(path: Path):
    try:
        html = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f'read error: {e}'

    has_np_hero = '<header class="np-hero"' in html or "<header class='np-hero'" in html
    has_lp_flex = 'class="lp-hero-flex"' in html and 'cognitoforms' in html.lower()
    if not has_np_hero and not has_lp_flex:
        return False, 'no hero pattern recognised'

    if already_done(html):
        return False, 'already done'

    prefix = rel_prefix(path)
    calc_url = f'{prefix}resources/storage-calculator.html'
    css_href = f'{prefix}css/hero-quote-card.css'
    js_src = f'{prefix}js/hero-quote-card.js'

    new_html = html
    if has_np_hero:
        new_html = inject_card(new_html, calc_url)
        if new_html == html:
            return False, 'card injection failed (np-hero markup unexpected)'
    elif has_lp_flex:
        # Build the card wrapped in lp-hero-cell so it sits in the existing flex layout.
        card_for_cell = '<div class="lp-hero-cell">\n' + QUOTE_CARD_HTML.format(calc_url=calc_url) + '          </div>'
        new_html, n = LP_SECOND_CELL_RE.subn(card_for_cell, new_html, count=1)
        if n == 0:
            return False, 'lp-hero-flex: second cell not matched'

    new_html = inject_css_link(new_html, css_href)
    new_html = inject_js_script(new_html, js_src)

    if new_html == html:
        return False, 'no change after injection'

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
            print(f'  ✓ {rel}')
        else:
            if msg == 'no np-hero' or msg == 'already done':
                skipped += 1
            else:
                failed.append((rel, msg))
                print(f'  ! {rel} — {msg}')
    print(f'\nDone. {changed} page(s) updated, {skipped} skipped.')
    if failed:
        print(f'{len(failed)} failure(s):')
        for r, m in failed:
            print(f'  - {r}: {m}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
