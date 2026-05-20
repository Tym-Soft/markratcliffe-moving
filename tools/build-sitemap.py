#!/usr/bin/env python3
"""
Rebuild the sitemap as a SITEMAP INDEX plus five sub-sitemaps:

  /sitemap.xml             — index referencing the five files below
  /page-sitemap.xml        — root-level pages (homepage + about, careers,
                             quote, privacy, reviews, terms)
  /services-sitemap.xml    — /services/* (16 services + hub)
  /areas-sitemap.xml       — /areas-covered/* (county landings, town pages,
                             international/man-and-van sub-pages, hub)
  /resources-sitemap.xml   — /resources/* (pricing, checklists, FAQs etc.)
  /blog-sitemap.xml        — /blog/* (every article + hub)

The audit treats sitemap.xml as a sitemap index — Rule 5 traverses the
sub-sitemaps to verify every indexable page is listed exactly once.

Run from the site root:
    python3 tools/build-sitemap.py
"""

from __future__ import annotations
import glob, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'

# Bucket name → (output filename, glob patterns, priority, changefreq).
# Order determines sitemap-index order.
BUCKETS = [
    ('page',      'page-sitemap.xml',      ['*.html'],                 '1.0', 'weekly'),
    ('services',  'services-sitemap.xml',  ['services/*.html'],        '0.8', 'monthly'),
    ('areas',     'areas-sitemap.xml',     ['areas-covered/*.html'],   '0.8', 'monthly'),
    ('resources', 'resources-sitemap.xml', ['resources/*.html'],       '0.7', 'monthly'),
    ('blog',      'blog-sitemap.xml',      ['blog/*.html'],            '0.6', 'monthly'),
]


def is_indexable(path: str) -> bool:
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read(4096)
    except OSError:
        return False
    if 'http-equiv="refresh"' in html: return False
    if 'window.location.replace' in html: return False
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    if m and 'noindex' in m.group(1).lower():
        return False
    return True


def loc_for(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path


def lastmod_for(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


def write_urlset(out_path: str, paths: list[str], priority: str, freq: str) -> int:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        lines.append('  <url>')
        lines.append(f'    <loc>{loc_for(p)}</loc>')
        lines.append(f'    <lastmod>{lastmod_for(p)}</lastmod>')
        lines.append(f'    <changefreq>{freq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')
    lines.append('')
    open(out_path, 'w', encoding='utf-8').write('\n'.join(lines))
    return len(paths)


def write_sitemap_index(child_files: list[str]) -> int:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = datetime.now(tz=timezone.utc).date().isoformat()
    for f in child_files:
        lastmod = today
        if os.path.exists(f):
            lastmod = datetime.fromtimestamp(
                os.path.getmtime(f), tz=timezone.utc).date().isoformat()
        lines.append('  <sitemap>')
        lines.append(f'    <loc>{BASE_URL}/{f}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append('  </sitemap>')
    lines.append('</sitemapindex>')
    lines.append('')
    open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines))
    return len(child_files)


def main() -> int:
    written = []
    total_urls = 0
    for bucket_name, out_name, patterns, priority, freq in BUCKETS:
        paths: list[str] = []
        for pat in patterns:
            paths.extend(glob.glob(pat))
        paths = sorted(p for p in paths if os.path.isfile(p) and is_indexable(p))
        n = write_urlset(out_name, paths, priority, freq)
        written.append(out_name)
        total_urls += n
        print(f'  wrote {out_name:25s}  {n:3d} URLs')

    n_idx = write_sitemap_index(written)
    print(f'  wrote {"sitemap.xml":25s}  {n_idx} sub-sitemap entries')
    print(f'\nTotal indexable URLs across all sub-sitemaps: {total_urls}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
