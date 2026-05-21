#!/usr/bin/env python3
"""
Crawl-issue cleanup pass — fixes the SEO problems Screaming Frog
surfaced after the structured-data rollout:

1. Removes the JS canonical / og:url injection script that lingers
   from a legacy Webflow export (87 pages). Every page already has
   a hardcoded <link rel="canonical"> + og:url meta — the JS is
   redundant and violates the "no JS-injected canonicals" rule
   (audit Rule 34).
2. Dedupes <meta name="description"> tags (41 pages have two — a
   legacy stub at the top of <head> in `content=... name=...`
   order, and the curated SEO copy further down in proper
   `name=... content=...` order). We keep the LAST one (the
   curated copy) and strip earlier duplicates.
3. Fixes JS path bugs on 4 blog pages that link to
   `src="js/mark-ratcliffe-moving.js"` (resolving to /blog/js/...
   404) instead of `src="../js/..."`.
4. Fixes the malformed og:title fragment on
   blog/10-most-commonly-forgotten-moving-items.html line 11.

Idempotent. Run from the site root:
    python3 tools/cleanup-html.py
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1. The legacy JS canonical injection script — single-line, well-defined
#    shape. We only kill the script that explicitly creates a "canonical"
#    rel; any other inline scripts on the page are untouched.
JS_CANONICAL_RE = re.compile(
    r'\s*<script>\(function\(\)\{[^<]*?setAttribute\("rel","canonical"\)[^<]*?\}\)\(\);</script>\s*\n?',
    re.S,
)

# 2. <meta name="description"> in either attribute order. We collect
#    every match and keep only the last.
META_DESC_RE = re.compile(
    r'\s*<meta\s+[^>]*?name\s*=\s*["\']description["\'][^>]*?>\s*\n?',
    re.I,
)
META_DESC_ALT_RE = re.compile(
    r'\s*<meta\s+[^>]*?content\s*=\s*["\'][^"\']*["\'][^>]*?name\s*=\s*["\']description["\'][^>]*?>\s*\n?',
    re.I,
)

# 3. <script src="js/..."> with no `../` prefix (in /blog/ context).
WRONG_BLOG_JS_RE = re.compile(r'(<script[^>]*?\ssrc=")js/')

# 4. Specific broken line in one blog post (preserved structure).
BROKEN_LINE_TARGET = 'blog/10-most-commonly-forgotten-moving-items.html'
BROKEN_LINE_OLD = '  H Most Commonly Forgotten Items When Moving House">\n'
BROKEN_LINE_NEW = '  <meta property="og:title" content="10 Most Commonly Forgotten Items When Moving House">\n'


def dedupe_meta_descriptions(html: str) -> tuple[str, int]:
    """Keep only the LAST <meta name=description> tag. Returns (new_html, removed_count)."""
    # Combine both attribute-order patterns into a single ordered list.
    matches: list[tuple[int, int]] = []
    for r in (META_DESC_RE, META_DESC_ALT_RE):
        for m in r.finditer(html):
            matches.append((m.start(), m.end()))
    # Deduplicate overlapping matches (alt regex might catch a tag that
    # the main one also matched — keep the union).
    matches = sorted(set(matches))
    # Filter out matches that are wholly inside an earlier match.
    filtered: list[tuple[int, int]] = []
    for s, e in matches:
        if any(s >= fs and e <= fe for fs, fe in filtered):
            continue
        filtered.append((s, e))
    if len(filtered) < 2:
        return html, 0
    # Drop every match except the last; iterate in reverse so prior
    # offsets stay valid.
    to_remove = filtered[:-1]
    for s, e in reversed(to_remove):
        html = html[:s] + html[e:]
    return html, len(to_remove)


def fix_page(path: str) -> tuple[bool, dict]:
    html = open(path, encoding='utf-8').read()
    original = html
    fixes = {'js_canonical': 0, 'meta_dedup': 0, 'blog_js_path': 0, 'broken_line': 0}

    # 1. Strip JS canonical injection scripts.
    new_html, n = JS_CANONICAL_RE.subn('', html)
    if n:
        html = new_html
        fixes['js_canonical'] = n

    # 2. Dedupe <meta name=description>.
    html, n = dedupe_meta_descriptions(html)
    fixes['meta_dedup'] = n

    # 3. Fix wrong JS paths in blog pages.
    if path.startswith('blog/'):
        new_html, n = WRONG_BLOG_JS_RE.subn(r'\1../js/', html)
        if n:
            html = new_html
            fixes['blog_js_path'] = n

    # 4. The one-off malformed line.
    if path == BROKEN_LINE_TARGET and BROKEN_LINE_OLD in html:
        html = html.replace(BROKEN_LINE_OLD, BROKEN_LINE_NEW)
        fixes['broken_line'] = 1

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
        return True, fixes
    return False, fixes


def main() -> int:
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    totals = {'js_canonical': 0, 'meta_dedup': 0, 'blog_js_path': 0, 'broken_line': 0}
    pages_changed = 0
    for p in sorted(pages):
        changed, fixes = fix_page(p)
        if changed:
            pages_changed += 1
        for k, v in fixes.items():
            totals[k] += v
    print(f'  pages changed:        {pages_changed}')
    print(f'  JS canonicals removed: {totals["js_canonical"]}')
    print(f'  meta descs deduped:    {totals["meta_dedup"]}')
    print(f'  blog JS paths fixed:   {totals["blog_js_path"]}')
    print(f'  broken og:title fixed: {totals["broken_line"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
