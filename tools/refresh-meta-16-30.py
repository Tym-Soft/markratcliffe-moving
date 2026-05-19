#!/usr/bin/env python3
"""Apply new titles + meta descriptions from the user's topics 16-30 to the
existing blog posts that cover those topics. All 15 topics overlap with
existing posts; this script refreshes the SEO metadata only."""
from __future__ import annotations
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UPDATES = [
    # (slug, title, description)
    ('moving-to-eastbourne-area-guide.html',
     'Moving to Eastbourne: Complete Area Guide & Moving Tips 2026',
     'Planning to move to Eastbourne? Our local guide covers the best areas, schools, parking rules, and everything you need to know before moving.'),
    ('moving-to-brighton-area-guide.html',
     'Moving to Brighton: Complete Area Guide & Local Tips',
     "Thinking of moving to Brighton? Get essential local advice including best areas, transport links, parking, and what it's really like to live there."),
    ('moving-to-chichester-area-guide.html',
     'Moving to Chichester: What You Need to Know in 2026',
     'Moving to Chichester? Our local guide covers listed properties, narrow streets, Goodwood events, parking restrictions, and specialist moving advice.'),
    ('moving-to-hastings-area-guide.html',
     'Moving to Hastings: Area Guide & What to Expect',
     'Considering a move to Hastings? Discover the different areas, local lifestyle, and practical moving tips for this historic coastal town.'),
    ('moving-to-worthing-area-guide.html',
     'Moving to Worthing: Complete Area Guide & Moving Tips',
     'Moving to Worthing? Our guide covers the best areas to live, local amenities, schools, and everything you need to know before relocating.'),
    ('best-areas-to-live-east-sussex-2026.html',
     'Best Areas to Live in East Sussex in 2026',
     'Not sure where to live in East Sussex? We rank the best areas based on lifestyle, schools, transport, and property types.'),
    ('moving-to-tunbridge-wells-area-guide.html',
     'Moving to Tunbridge Wells: Complete Local Guide 2026',
     'Moving to Tunbridge Wells? Our guide covers the best areas, schools, parking, and what you need to know about this popular Kent town.'),
    ('moving-to-lewes-area-guide.html',
     'Moving to Lewes: Local Guide & Moving Tips',
     "Thinking about moving to Lewes? Discover what it's really like to live here, including parking, property styles, and local considerations."),
    ('newhaven-or-seaford-which-is-better.html',
     'Newhaven vs Seaford: Which Town is Better to Move To?',
     "Can't decide between Newhaven and Seaford? We compare both towns to help you choose the right place to live."),
    ('moving-from-london-to-sussex.html',
     'Moving from London to Sussex: What You Really Need to Know',
     "Making the big move from London to Sussex? Here's what to expect, how much it costs, and tips for a smoother transition."),
    ('cost-of-living-eastbourne-vs-brighton.html',
     'Cost of Living: Eastbourne vs Brighton Comparison 2026',
     'Eastbourne or Brighton? We compare the cost of living, rent, house prices, and day-to-day expenses between both towns.'),
    ('best-schools-eastbourne-families.html',
     'Best Schools in Eastbourne – Guide for Families Moving to the Area',
     'Looking for good schools in Eastbourne? Our guide helps families choose the right area based on education quality and school ratings.'),
    ('eastbourne-parking-permits-when-moving.html',
     'Eastbourne Parking Permits & Rules When Moving House',
     'Everything you need to know about parking permits, suspension bays, and parking restrictions when moving in Eastbourne.'),
    ('moving-to-listed-building-sussex.html',
     'Moving to a Listed Building in Sussex – What You Need to Know',
     'Moving into a Grade II listed property? Learn about narrow doors, parking permits, antique furniture handling, and special moving requirements.'),
    ('moving-to-countryside-east-sussex.html',
     'Moving to the Countryside in East Sussex – What to Expect',
     "Thinking of moving to a rural village in East Sussex? Here's what you need to know about country lanes, access issues, and rural living."),
]

def html_escape_attr(s: str) -> str:
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
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*(")', r'\1' + title_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:title")', r'\1' + title_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*property="og:description"[^>]*content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:description")', r'\1' + desc_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*name="twitter:title"[^>]*content=")[^"]*(")', r'\1' + title_e + r'\2', html, count=1)
    html = re.sub(r'(<meta[^>]*name="twitter:description"[^>]*content=")[^"]*(")', r'\1' + desc_e + r'\2', html, count=1)

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
