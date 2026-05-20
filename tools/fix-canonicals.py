#!/usr/bin/env python3
"""
Replace the runtime JS canonical injection with static
<link rel="canonical"> + <meta property="og:url"> tags hardcoded to
the production www.markratcliffemoving.co.uk URL for each page.

Reason: many crawlers (Screaming Frog by default, Bingbot, etc.) do
not execute JavaScript, so the JS-injected canonical reads as
missing. Worse, the JS used location.host — so on the GitHub Pages
staging URL it canonicalised the page to itself instead of production.

Idempotent — pages that already have a static canonical pointing at
the correct production URL are skipped.
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE = 'https://www.markratcliffemoving.co.uk'

JS_BLOCK_RE = re.compile(
    r'\s*<script>\s*\(function\(\)\{\s*var u = location\.protocol.*?\}\)\(\);\s*</script>',
    re.S,
)
EXISTING_CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
EXISTING_OGURL_RE = re.compile(r'<meta\s+property="og:url"\s+content="([^"]+)"', re.I)
HEAD_CLOSE_RE     = re.compile(r'</head>', re.I)

def production_url(path: str) -> str:
    p = path.replace(os.sep, '/')
    if p == 'index.html':
        return BASE + '/'
    return BASE + '/' + p

def is_redirect(html: str) -> bool:
    head = html[:4096]
    return 'http-equiv="refresh"' in head or 'window.location.replace' in head

def is_noindex(html: str) -> bool:
    head = html[:4096]
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', head, re.I)
    return bool(m and 'noindex' in m.group(1).lower())

def fix(path: str) -> str:
    html = open(path, encoding='utf-8').read()
    if is_redirect(html) or is_noindex(html):
        return 'skip'
    original = html
    target = production_url(path)
    changes: list[str] = []

    # 1. Remove the JS canonical/og:url injection block if present
    if JS_BLOCK_RE.search(html):
        html = JS_BLOCK_RE.sub('', html)
        changes.append('removed JS block')

    # 2. Insert / update <link rel="canonical">
    m = EXISTING_CANON_RE.search(html)
    if m:
        if m.group(1) != target:
            html = EXISTING_CANON_RE.sub(
                lambda mm: f'<link rel="canonical" href="{target}"',
                html, count=1,
            )
            changes.append('updated canonical')
    else:
        tag = f'  <link rel="canonical" href="{target}">\n  <meta property="og:url" content="{target}">\n'
        # If og:url already exists separately, only insert canonical
        if EXISTING_OGURL_RE.search(html):
            tag = f'  <link rel="canonical" href="{target}">\n'
            changes.append('added canonical')
        else:
            changes.append('added canonical+og:url')
        html = HEAD_CLOSE_RE.sub(tag + '</head>', html, count=1)

    # 3. Ensure og:url is present and correct
    m = EXISTING_OGURL_RE.search(html)
    if m:
        if m.group(1) != target:
            html = EXISTING_OGURL_RE.sub(
                lambda mm: f'<meta property="og:url" content="{target}"',
                html, count=1,
            )
            changes.append('updated og:url')
    else:
        tag = f'  <meta property="og:url" content="{target}">\n'
        html = HEAD_CLOSE_RE.sub(tag + '</head>', html, count=1)
        changes.append('added og:url')

    if html == original:
        return 'no-op'
    open(path, 'w', encoding='utf-8').write(html)
    return ', '.join(changes)


def main() -> int:
    paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
    )
    n_changed = 0
    for p in paths:
        r = fix(p)
        if r not in ('no-op', 'skip'):
            n_changed += 1
            print(f'{p:60s} → {r}')
    print()
    print(f'Updated {n_changed} of {len(paths)} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
