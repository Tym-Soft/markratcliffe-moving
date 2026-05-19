#!/usr/bin/env python3
"""Apply new titles + meta descriptions from the user's topics 1-14 to the
existing blog posts that cover those topics. The post bodies stay; the SEO
metadata is refreshed."""
from __future__ import annotations
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UPDATES = [
    ('how-to-prepare-for-your-house-move.html',
     'How to Prepare for a House Move in 2026 | Complete Checklist',
     'Moving house in 2026? Follow our complete step-by-step preparation guide with an 8-week checklist to make your move as smooth and stress-free as possible.'),
    ('moving-house-checklist-eastbourne.html',
     'Moving House Checklist: The Ultimate 8-Week Guide',
     'Never miss a thing with our complete 8-week moving house checklist. From planning to moving day, we cover every important step you need to take.'),
    ('what-to-pack-first-when-moving-house.html',
     'What to Pack First When Moving House – The Correct Order',
     'Not sure where to start packing? This guide shows you exactly what to pack first when moving house to avoid stress and last-minute panic.'),
    ('how-to-pack-fragile-items.html',
     'How to Pack Fragile Items Safely When Moving House',
     'Learn professional techniques for safely packing glass, china, mirrors, and other fragile items to prevent expensive breakages on moving day.'),
    ('moving-house-in-winter.html',
     'Moving House in Winter: Essential Tips & Advice',
     'Planning a winter house move? Discover the challenges of moving in cold weather and how to prepare for ice, snow, and short daylight hours.'),
    ('moving-house-in-summer.html',
     'Moving House in Summer: Tips to Beat the Heat',
     'Moving during hot summer months? Learn how to protect your belongings, stay cool, and keep your move running smoothly in the heat.'),
    ('cost-of-moving-house-sussex-2026.html',
     'How Much Does It Cost to Move House in Sussex in 2026?',
     'Get a clear breakdown of house moving costs in Sussex for 2026, including local moves, full packing, and storage options.'),
    ('10-most-commonly-forgotten-moving-items.html',
     '10 Most Commonly Forgotten Items When Moving House',
     "Don't get caught out on moving day. Here are the 10 things people forget most often when moving house."),
    ('how-to-organise-move-when-busy.html',
     "How to Organise Your House Move When You're Busy",
     'Short on time? Learn practical strategies to organise and plan your house move efficiently even with a hectic work and family schedule.'),
    ('moving-house-with-pets.html',
     'Moving House with Pets: Complete Guide for Cats & Dogs',
     'Moving with pets? Our complete guide covers how to prepare your dog or cat for moving day and help them settle into your new home.'),
    ('moving-house-with-children.html',
     'Moving House with Children: How to Make It Stress-Free',
     'Moving with kids can be challenging. Discover practical tips to reduce stress and keep your children happy throughout the moving process.'),
    ('moving-house-alone-practical-tips.html',
     'Moving House Alone: Practical Tips and Advice',
     'Moving solo? These practical tips will help you organise and manage your house move efficiently when doing it by yourself.'),
    ('how-to-downsize-before-moving.html',
     'How to Downsize Before Moving House – A Practical Guide',
     'Need to reduce the amount of stuff before moving? Learn effective decluttering and downsizing strategies that actually work.'),
    ('moving-from-flat-vs-house.html',
     'Moving from a Flat vs a House – Key Differences Explained',
     "What's the difference between moving from a flat and moving from a house? We compare the challenges, costs, and practical considerations."),
]

def html_escape_attr(s: str) -> str:
    # Light HTML escaping for use inside attribute="..."
    return s.replace('&', '&amp;').replace('"', '&quot;')

n = 0
for slug, title, desc in UPDATES:
    p = 'blog/' + slug
    if not os.path.isfile(p):
        print(f'  ✗ missing {p}')
        continue
    html = open(p, encoding='utf-8').read()
    title_e = html_escape_attr(title)
    desc_e  = html_escape_attr(desc)
    # Replace <title>…</title>
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)
    # Replace meta name="description"
    html = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)
    # Replace og:title (any form)
    html = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*(")', r'\1' + title_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:title")', r'\1' + title_e + r'\2', html, count=1)
    # Replace og:description
    html = re.sub(r'(<meta[^>]*property="og:description"[^>]*content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:description")', r'\1' + desc_e + r'\2', html, count=1)
    # Replace twitter:title and twitter:description if present
    html = re.sub(r'(<meta[^>]*name="twitter:title"[^>]*content=")[^"]*(")', r'\1' + title_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*name="twitter:description"[^>]*content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)
    # Update JSON-LD BlogPosting headline + description
    def update_blogposting(match):
        blob = match.group(1)
        try:
            data = json.loads(blob)
        except Exception:
            return match.group(0)
        items = data if isinstance(data, list) else [data]
        changed = False
        for item in items:
            if isinstance(item, dict) and item.get('@type') == 'BlogPosting':
                item['headline'] = title
                item['description'] = desc
                changed = True
        if not changed: return match.group(0)
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>',
                  update_blogposting, html, flags=re.S)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print(f'  ✓ refreshed metadata on {slug}')
print(f'\nUpdated {n} of {len(UPDATES)} posts.')
