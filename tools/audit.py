#!/usr/bin/env python3
"""
markratcliffemoving.co.uk content audit.

Verifies the six build rules:
  1. Blogs are ≥2000 words.
  2. Location pages are ≥1500 words.
  3. Every page has ≥10 distinct in-body internal links.
  4. blog/index.html lists every blog post, newest-first, capped at 9.
  5. sitemap.xml contains a <url> for every indexable HTML page.
  6. No two indexable pages share the same <title> tag.

Run from the site root:
    python3 tools/audit.py

Exit codes:
    0  all rules pass
    1  one or more rules failed (list printed)
"""

from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BLOG_MIN_WORDS     = 2000
LOCATION_MIN_WORDS = 1500
BODY_LINKS_MIN     = 10
BLOG_INDEX_MAX     = 9

# Heuristic location-page detector. Anything starting with removals-* at the root,
# any subpage under areas-covered/, plus the two outliers in root.
LOCATION_GLOBS = [
    'removals-*.html',
    'areas-covered/*.html',
]
LOCATION_EXTRA = ['man-and-van-eastbourne.html', 'hailsham-removals.html']

NAV_END_RE   = re.compile(r'<div class="menu-button[^>]*>.*?</div>\s*</div>\s*</div>', re.S)
FOOTER_RE    = re.compile(r'<footer', re.S)
WORD_HEAD_RE = re.compile(r'<head.*?</head>', re.S | re.I)
WORD_SCRIPT  = re.compile(r'<script.*?</script>', re.S | re.I)
WORD_STYLE   = re.compile(r'<style.*?</style>',  re.S | re.I)
TAG_RE       = re.compile(r'<[^>]+>')
ENT_RE       = re.compile(r'&[a-z]+;')

def is_redirect_stub(html: str) -> bool:
    return 'http-equiv="refresh"' in html or 'window.location.replace' in html

def word_count(html: str) -> int:
    h = WORD_HEAD_RE.sub('', html)
    h = WORD_SCRIPT.sub('', h)
    h = WORD_STYLE.sub('', h)
    t = TAG_RE.sub(' ', h)
    t = ENT_RE.sub(' ', t)
    return len(t.split())

def body_internal_links(html: str, current_path: str) -> set[str]:
    m_start = NAV_END_RE.search(html)
    m_end   = FOOTER_RE.search(html)
    start   = m_start.end() if m_start else 0
    end     = m_end.start() if m_end else len(html)
    body    = html[start:end]
    refs    = re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', body)
    seen    = set()
    for href in refs:
        h = href.split('#')[0].split('?')[0].strip()
        if not h or h in ('/', './'): continue
        if h.startswith(('mailto:', 'tel:', 'javascript:', '#')): continue
        if h.startswith(('http://', 'https://', '//')):
            if 'markratcliffemoving.co.uk' not in h: continue
            m = re.search(r'markratcliffemoving\.co\.uk/(.+\.html)', h)
            if m: h = m.group(1)
        if not h.endswith('.html'): continue
        if h.startswith('../'): h = h[3:]
        elif h.startswith('./'): h = h[2:]
        # leave subdir-relative as-is — that's fine for distinctness counting
        seen.add(h)
    return seen

def all_pages() -> list[str]:
    paths = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
    )
    return sorted(p for p in paths if os.path.isfile(p))

def is_blog_post(path: str) -> bool:
    return path.startswith('blog/') and os.path.basename(path) != 'index.html'

def is_location_page(path: str) -> bool:
    base = os.path.basename(path)
    if path.startswith('areas-covered/'):
        return True
    if base in LOCATION_EXTRA:
        return True
    return base.startswith('removals-') and path.count('/') == 0

def blog_post_meta(path: str) -> dict | None:
    """Pull headline + datePublished from a blog post's BlogPosting JSON-LD."""
    html = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get('@type') == 'BlogPosting':
                return {
                    'slug': os.path.basename(path),
                    'date': item.get('datePublished'),
                    'headline': item.get('headline'),
                }
    return None

BASE_URL = 'https://www.markratcliffemoving.co.uk'

def indexable_pages(pages: list[str]) -> list[str]:
    out = []
    for p in pages:
        try:
            html = open(p, encoding='utf-8').read(4096)
        except OSError:
            continue
        if is_redirect_stub(html): continue
        m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
        if m and 'noindex' in m.group(1).lower():
            continue
        out.append(p)
    return out

def sitemap_locs() -> set[str]:
    try:
        xml = open('sitemap.xml', encoding='utf-8').read()
    except OSError:
        return set()
    return set(re.findall(r'<loc>([^<]+)</loc>', xml))

def expected_loc(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    return BASE_URL + '/' + path

def audit():
    pages = all_pages()
    failures = {
        'blog_word_count':       [],
        'location_word_count':   [],
        'internal_links':        [],
        'blog_index_listing':    [],
        'blog_index_order':      [],
        'sitemap':               [],
        'duplicate_titles':      [],
    }

    blog_posts = []
    blog_index_posts_listed = set()

    for path in pages:
        try:
            html = open(path, encoding='utf-8').read()
        except OSError:
            continue
        if is_redirect_stub(html):
            continue

        wc = word_count(html)
        link_count = len(body_internal_links(html, path))

        # Rule 1 — blog word count
        if is_blog_post(path):
            blog_posts.append(path)
            if wc < BLOG_MIN_WORDS:
                failures['blog_word_count'].append((wc, path))

        # Rule 2 — location word count
        if is_location_page(path):
            if wc < LOCATION_MIN_WORDS:
                failures['location_word_count'].append((wc, path))

        # Rule 3 — ≥10 in-body internal links
        if link_count < BODY_LINKS_MIN:
            failures['internal_links'].append((link_count, path))

    # Rule 4 — blog index
    index_path = 'blog/index.html'
    if os.path.isfile(index_path):
        index_html = open(index_path, encoding='utf-8').read()
        listed = []
        # Find each card's <h3><a href="slug">title</a> inside the .np-blog-grid
        m = re.search(
            r'<div class="np-blog-grid">(.*?)</div>\s*</div>',
            index_html,
            re.S,
        )
        if m:
            grid = m.group(1)
            for href_m in re.finditer(r'<h3><a href="([^"]+)">', grid):
                slug = href_m.group(1).split('#')[0].split('?')[0]
                listed.append(slug)
        # Visible count must be ≤ 9
        if len(listed) > BLOG_INDEX_MAX:
            failures['blog_index_listing'].append(
                f'visible count is {len(listed)} (>{BLOG_INDEX_MAX})'
            )
        # Every post should be listed (unless total > MAX, then top MAX by date should be listed)
        post_metas = [blog_post_meta(p) for p in blog_posts]
        post_metas = [m for m in post_metas if m]
        post_metas.sort(key=lambda x: (x.get('date') or '', x.get('slug') or ''), reverse=True)
        expected = [m['slug'] for m in post_metas[:BLOG_INDEX_MAX]]
        # Order check
        if listed and listed != expected:
            failures['blog_index_order'].append(
                f'index order does not match newest-first.\n'
                f'    Expected: {expected}\n'
                f'    Got:      {listed}'
            )
        # Listing-completeness check (when total posts ≤ MAX, every post must appear)
        if len(post_metas) <= BLOG_INDEX_MAX:
            missing = sorted(set(m['slug'] for m in post_metas) - set(listed))
            if missing:
                failures['blog_index_listing'].append(
                    f'missing posts on index: {missing}'
                )

    # Report
    any_fail = False
    print('=' * 64)
    print('markratcliffemoving.co.uk — content rule audit')
    print('=' * 64)

    def rule(name: str, ok_msg: str, fail_list):
        nonlocal any_fail
        if not fail_list:
            print(f'  ✓ {name}: {ok_msg}')
            return
        any_fail = True
        print(f'  ✗ {name}: {len(fail_list)} failure(s)')
        for f in fail_list[:20]:
            if isinstance(f, tuple):
                print(f'      {f[0]:>5}  {f[1]}')
            else:
                print(f'      {f}')
        if len(fail_list) > 20:
            print(f'      ... and {len(fail_list) - 20} more')

    rule('Rule 1 — blogs ≥%d words' % BLOG_MIN_WORDS,
         f'{len(blog_posts)} posts all ≥{BLOG_MIN_WORDS} words',
         failures['blog_word_count'])

    n_loc = sum(1 for p in pages if is_location_page(p) and not is_redirect_stub(open(p).read()))
    rule('Rule 2 — location pages ≥%d words' % LOCATION_MIN_WORDS,
         f'{n_loc} location pages all ≥{LOCATION_MIN_WORDS} words',
         failures['location_word_count'])

    n_total = sum(1 for p in pages if not is_redirect_stub(open(p).read()))
    rule('Rule 3 — ≥%d distinct in-body links' % BODY_LINKS_MIN,
         f'{n_total} pages all ≥{BODY_LINKS_MIN} links',
         failures['internal_links'])

    rule('Rule 4a — blog index lists every post (cap %d)' % BLOG_INDEX_MAX,
         'index lists every post, capped correctly',
         failures['blog_index_listing'])
    rule('Rule 4b — blog index ordered newest-first',
         'newest-first ordering correct',
         failures['blog_index_order'])

    # Rule 5 — sitemap covers every indexable page
    indexable = indexable_pages(pages)
    sitemap   = sitemap_locs()
    missing = []
    for p in indexable:
        if expected_loc(p) not in sitemap:
            missing.append(p)
    if missing:
        for m in missing:
            failures['sitemap'].append(('missing', m))
    extra = []
    indexable_set = {expected_loc(p) for p in indexable}
    for loc in sitemap:
        if loc not in indexable_set:
            extra.append(loc)
    if extra:
        for e in extra:
            failures['sitemap'].append(('orphan ', e))
    rule('Rule 5 — sitemap.xml covers every indexable page',
         f'{len(indexable)} indexable pages all listed; {len(sitemap)} sitemap entries match',
         failures['sitemap'])

    # Rule 6 — no duplicate <title> tags across indexable pages
    title_re = re.compile(r'<title>([^<]+)</title>', re.I)
    titles_seen: dict[str, list[str]] = {}
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m = title_re.search(html)
        if not m:
            failures['duplicate_titles'].append(('no-title', p))
            continue
        title = ' '.join(m.group(1).split()).strip()
        titles_seen.setdefault(title, []).append(p)
    for title, paths in titles_seen.items():
        if len(paths) > 1:
            failures['duplicate_titles'].append(
                f'"{title}" used by {len(paths)} pages: {", ".join(paths)}'
            )
    rule('Rule 6 — no duplicate <title> tags',
         f'{len(titles_seen)} unique titles across {len(indexable)} indexable pages',
         failures['duplicate_titles'])

    print('=' * 64)
    if any_fail:
        print('FAIL — one or more rules violated. See list above.')
        print('To regenerate the blog index after adding/removing posts:')
        print('    python3 tools/build-blog-index.py')
        print('To regenerate the sitemap after adding/removing pages:')
        print('    python3 tools/build-sitemap.py')
        return 1
    print('PASS — all six content rules satisfied.')
    return 0

if __name__ == '__main__':
    sys.exit(audit())
