#!/usr/bin/env python3
"""
Add Content-Security-Policy and Referrer-Policy meta tags to every
indexable page's <head>.

GitHub Pages does not allow custom HTTP response headers, so these
two security policies are delivered via <meta> tags. The other SF-
flagged headers (X-Frame-Options, X-Content-Type-Options) cannot be
set via meta — they require edge / server config and stay on the
deployment to-do list.

The CSP is intentionally permissive enough to keep existing inline
scripts (GTM, dataLayer, webfont loader) working. Tighten over time.

Idempotent — pages that already have both tags are skipped.
"""

import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CSP = (
    "default-src 'self' https:; "
    "script-src 'self' 'unsafe-inline' https://ajax.googleapis.com https://www.googletagmanager.com https://www.google-analytics.com https://cdn.yoshki.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://ajax.googleapis.com; "
    "img-src 'self' data: https:; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "frame-src https://www.google.com; "
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://stats.g.doubleclick.net; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)
REFERRER = "strict-origin-when-cross-origin"

CSP_TAG = f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'
REF_TAG = f'<meta name="referrer" content="{REFERRER}">'

CSP_RE = re.compile(r'<meta\s+http-equiv="Content-Security-Policy"[^>]*>', re.I)
REF_RE = re.compile(r'<meta\s+name="referrer"[^>]*>', re.I)
HEAD_CLOSE_RE = re.compile(r'</head>', re.I)


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
    changes: list[str] = []

    # CSP
    if CSP_RE.search(html):
        # Refresh to current policy (in case CSP value evolves)
        new_html, n = CSP_RE.subn(CSP_TAG, html, count=1)
        if new_html != html:
            html = new_html
            changes.append('CSP refreshed')
    else:
        html = HEAD_CLOSE_RE.sub('  ' + CSP_TAG + '\n</head>', html, count=1)
        changes.append('CSP added')

    # Referrer-Policy
    if REF_RE.search(html):
        new_html, n = REF_RE.subn(REF_TAG, html, count=1)
        if new_html != html:
            html = new_html
            changes.append('Referrer refreshed')
    else:
        html = HEAD_CLOSE_RE.sub('  ' + REF_TAG + '\n</head>', html, count=1)
        changes.append('Referrer added')

    if html == original:
        return 'no-op'
    open(path, 'w', encoding='utf-8').write(html)
    return ', '.join(changes)


def main() -> int:
    paths = sorted(glob.glob('*.html') + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html'))
    n_changed = 0
    for p in paths:
        r = fix(p)
        if r not in ('no-op', 'skip'):
            n_changed += 1
            if n_changed <= 6 or n_changed % 50 == 0:
                print(f'{p:60s} → {r}')
    print()
    print(f'Updated {n_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
