#!/usr/bin/env python3
"""
Rebuild sitemap.xml from disk.

Scans every *.html file in the repo, skips redirect stubs and noindex
pages, and writes a fresh sitemap.xml with one <url> entry per
indexable page. Uses each file's mtime as <lastmod>.

Run from the site root:
    python3 tools/build-sitemap.py
"""

from __future__ import annotations
import glob, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'
SITEMAP  = 'sitemap.xml'

# Priority/changefreq heuristics by path
def metadata_for(path: str) -> tuple[str, str]:
    if path == 'index.html':
        return ('1.0', 'weekly')
    if path.startswith('blog/'):
        return ('0.6', 'monthly')
    if path.startswith('areas-covered/'):
        return ('0.7', 'monthly')
    if path.startswith('removals-') or path in ('hailsham-removals.html', 'man-and-van-eastbourne.html'):
        return ('0.8', 'monthly')
    return ('0.8', 'monthly')

def is_indexable(path: str) -> bool:
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read(4096)  # head is enough
    except OSError:
        return False
    if 'http-equiv="refresh"' in html: return False
    if 'window.location.replace' in html: return False
    # honour robots noindex
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    if m and 'noindex' in m.group(1).lower():
        return False
    return True

def loc_for(path: str) -> str:
    # index.html → / (clean root URL)
    if path == 'index.html':
        return BASE_URL + '/'
    # subdir index.html → /subdir/ (clean directory URL)
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path

def lastmod_for(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()

def main() -> int:
    paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    paths = [p for p in paths if os.path.isfile(p) and is_indexable(p)]

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        priority, freq = metadata_for(p)
        lines.append('  <url>')
        lines.append(f'    <loc>{loc_for(p)}</loc>')
        lines.append(f'    <lastmod>{lastmod_for(p)}</lastmod>')
        lines.append(f'    <changefreq>{freq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')
    lines.append('')

    open(SITEMAP, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'Rebuilt {SITEMAP} with {len(paths)} <url> entries.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
