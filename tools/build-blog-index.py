#!/usr/bin/env python3
"""
Rebuild the blog/index.html "Latest articles" grid.

Reads every blog/*.html (excluding index.html), pulls headline +
datePublished + description + image from its JSON-LD and meta tags,
sorts newest-first, and rewrites the `<div class="np-blog-grid"> ... </div>`
block inside blog/index.html. Max 9 cards shown.

Run from the site root:    python3 tools/build-blog-index.py
"""

from __future__ import annotations
import glob, json, os, re, sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, 'blog')
INDEX = os.path.join(BLOG_DIR, 'index.html')
MAX_CARDS = 9

CATEGORY_HINTS = [
    ('pad-wrap',         'Packing'),
    ('packing',          'Packing'),
    ('fragile',          'Packing'),
    ('checklist',        'Moving Tips'),
    ('prepare',          'Moving Tips'),
    ('cost',             'Cost & Quotes'),
    ('choosing',         'Choosing a Mover'),
    ('storage',          'Storage'),
    ('international',    'International'),
    ('overseas',         'International'),
]

def category_for(slug: str, title: str) -> str:
    s = (slug + ' ' + title).lower()
    for needle, cat in CATEGORY_HINTS:
        if needle in s:
            return cat
    return 'Moving Tips'

def extract_meta(path: str) -> dict | None:
    html = open(path, encoding='utf-8').read()
    if 'http-equiv="refresh"' in html or 'window.location.replace' in html:
        return None  # redirect stub

    # Try JSON-LD BlogPosting first
    headline = None
    date = None
    image = None
    description = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict): continue
            if item.get('@type') == 'BlogPosting':
                headline    = item.get('headline')    or headline
                date        = item.get('datePublished') or date
                description = item.get('description') or description
                img = item.get('image')
                if isinstance(img, dict): img = img.get('url')
                image = img or image

    # Fall back to <title> and meta description
    if not headline:
        m = re.search(r'<title>([^<]+)</title>', html)
        if m:
            headline = m.group(1).strip()
            # Strip site suffixes like " | Mark Ratcliffe Moving"
            headline = re.sub(r'\s*[|·—]\s*Mark Ratcliffe.*$', '', headline)
    if not description:
        m = re.search(r'<meta name="description" content="([^"]+)"', html)
        if m: description = m.group(1)
    if not image:
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m: image = m.group(1)

    if not headline: return None

    # Normalise image to a path relative to blog/index.html
    if image:
        image = image.split('?')[0]
        m = re.search(r'/images/([^/]+\.\w+)$', image)
        if m:
            image = '../images/' + m.group(1)
        elif image.startswith('../images/'):
            pass
        else:
            image = '../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp'

    # Sortable date: keep "YYYY-MM-DD"
    sort_date = date or '1970-01-01'

    return {
        'slug':        os.path.basename(path),
        'title':       unescape(headline.strip()),
        'date':        sort_date,
        'description': unescape((description or '').strip()),
        'image':       image,
    }

def render_card(post: dict) -> str:
    cat = category_for(post['slug'], post['title'])
    return (
        '          <article class="np-blog-card">\n'
        f'            <img src="{post["image"]}" alt="{post["title"]}" loading="lazy" decoding="async" width="600" height="360">\n'
        '            <div class="np-blog-card-body">\n'
        f'              <div class="np-blog-card-meta">{cat} &middot; {post["date"]}</div>\n'
        f'              <h3><a href="{post["slug"]}">{post["title"]}</a></h3>\n'
        f'              <p>{post["description"]}</p>\n'
        f'              <a href="{post["slug"]}"><strong>Read more &rarr;</strong></a>\n'
        '            </div>\n'
        '          </article>'
    )

def main() -> int:
    posts = []
    for path in glob.glob(os.path.join(BLOG_DIR, '*.html')):
        if os.path.basename(path) == 'index.html': continue
        meta = extract_meta(path)
        if meta: posts.append(meta)

    # Sort newest-first by datePublished, with the slug as a stable tiebreaker
    # so this ordering matches tools/audit.py and stays deterministic.
    posts.sort(key=lambda p: (p['date'] or '', p['slug'] or ''), reverse=True)
    visible = posts[:MAX_CARDS]

    grid_html = '<div class="np-blog-grid">\n' + '\n'.join(render_card(p) for p in visible) + '\n        </div>'

    index_html = open(INDEX, encoding='utf-8').read()
    # Locate the grid block by div-balanced scan
    start = index_html.find('<div class="np-blog-grid">')
    if start < 0:
        print('Could not find <div class="np-blog-grid"> in index.html', file=sys.stderr)
        return 1
    # Walk forward counting open/close <div> tags until depth returns to 0.
    depth = 0
    i = start
    end = -1
    DIV_OPEN  = re.compile(r'<div\b', re.I)
    DIV_CLOSE = re.compile(r'</div>', re.I)
    while i < len(index_html):
        next_open  = DIV_OPEN.search(index_html, i)
        next_close = DIV_CLOSE.search(index_html, i)
        if not next_close: break
        if next_open and next_open.start() < next_close.start():
            depth += 1
            i = next_open.end()
        else:
            depth -= 1
            i = next_close.end()
            if depth == 0:
                end = i
                break
    if end < 0:
        print('Could not find matching </div> for grid', file=sys.stderr)
        return 1
    new_index = index_html[:start] + grid_html + index_html[end:]
    open(INDEX, 'w', encoding='utf-8').write(new_index)
    print(f'Rebuilt {INDEX} with {len(visible)} cards (of {len(posts)} total posts).')
    if len(posts) > MAX_CARDS:
        print(f'  ({len(posts) - MAX_CARDS} older post(s) not shown; index capped at {MAX_CARDS}.)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
