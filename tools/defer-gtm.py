#!/usr/bin/env python3
"""
Defer Google Tag Manager (GTM) loading on every page from eager to
window.load. Lighthouse flags ~62 KiB of "unused JavaScript" because
GTM downloads + parses before the LCP image renders, even though
nothing in our setup needs it during initial render.

Before:
    <script async src="…/gtag/js?id=G-…"></script>
    <script>dataLayer=[];gtag(…);gtag('config',…);</script>

After:
    <script>
      dataLayer=[];
      gtag(…); gtag('config',…);
      // Load GTM after window.onload so it doesn't compete with the
      // critical-path resources (LCP image, CSS, fonts).
      window.addEventListener('load', function() {
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=G-…';
        document.head.appendChild(s);
      });
    </script>

GA still tracks the visit; events queued in dataLayer are flushed
the moment GTM finishes loading (typically ~200-500ms after onload).

Idempotent — script detects the deferred form and skips already-
updated pages.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

GTM_ID = 'G-Q111LKQEBP'

# 1. The eager <script async src=".../gtag/js?id=..."></script> tag.
EAGER_GTM_RE = re.compile(
    r'\s*<script\s+async(?:="")?\s+src="https://www\.googletagmanager\.com/gtag/js\?id=' + re.escape(GTM_ID) + r'"></script>\s*\n?',
    re.I,
)

# 2. The inline <script>…dataLayer…gtag…</script> body. Two variants
#    on the site (Webflow-export "developer_id" form and the lighter
#    blog form); we match either and rewrite to the deferred loader.
INLINE_GTM_RE = re.compile(
    r'<script(?:\s+type="text/javascript")?\s*>'
    r'window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];'
    r'function gtag\(\)\{dataLayer\.push\(arguments\);\}'
    r"(?P<extra>(?:gtag\('set'[^;]+;)?)"
    r"gtag\('js'[^;]+;"
    r"gtag\('config'[^;]+;"
    r'</script>',
    re.I | re.S,
)

DEFERRED_TEMPLATE = (
    '<script>'
    'window.dataLayer=window.dataLayer||[];'
    'function gtag(){{dataLayer.push(arguments);}}'
    '{extra}'
    "gtag('js',new Date());"
    "gtag('config','" + GTM_ID + "');"
    "window.addEventListener('load',function(){{"
    "var s=document.createElement('script');"
    "s.async=true;"
    "s.src='https://www.googletagmanager.com/gtag/js?id=" + GTM_ID + "';"
    "document.head.appendChild(s);"
    "}});"
    '</script>'
)

# Heuristic for "already deferred" — skip these.
ALREADY_DEFERRED_RE = re.compile(r"document\.createElement\('script'\)[^<]+gtag/js\?id=" + re.escape(GTM_ID), re.I)


def fix_page(path: str) -> bool:
    try:
        html = open(path, encoding='utf-8').read()
    except OSError:
        return False
    if ALREADY_DEFERRED_RE.search(html):
        return False  # idempotent
    original = html

    # Strip the eager async script tag (it'll be re-added by the
    # deferred loader inside the inline script).
    html = EAGER_GTM_RE.sub('\n  ', html, count=1)

    # Replace the inline script with the deferred variant.
    m = INLINE_GTM_RE.search(html)
    if not m:
        return False
    extra = m.group('extra') or ''
    html = html[:m.start()] + DEFERRED_TEMPLATE.format(extra=extra) + html[m.end():]

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False


def main() -> int:
    import glob
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    changed = 0
    for p in pages:
        if fix_page(p):
            changed += 1
    print(f'  deferred GTM on {changed} pages')
    return 0


if __name__ == '__main__':
    sys.exit(main())
