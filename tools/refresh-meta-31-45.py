#!/usr/bin/env python3
"""Refresh metadata on the 12 existing posts that match topics 31-45."""
from __future__ import annotations
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UPDATES = [
    ('full-pad-wrap-protection-explained.html',
     'The Complete Guide to Full Pad-Wrap Protection',
     'What is full pad-wrap protection and why is it the safest way to move? Our complete guide explains our 3-step process and how it protects your furniture better than standard methods.'),
    ('how-our-pad-wrap-service-protects-furniture.html',
     'How Our Full Pad-Wrap Service Protects Your Furniture',
     'Learn exactly how our professional full wrapping service works and why it offers far superior protection compared to standard removals.'),
    ('how-to-choose-right-self-storage.html',
     'How to Choose the Right Self Storage Solution for Your Needs',
     'Not sure what type of storage you need? Our guide helps you choose the best storage option based on your specific situation and budget.'),
    ('short-term-vs-long-term-storage.html',
     'Short Term vs Long Term Storage: Which One Should You Choose?',
     'Confused about storage durations? We explain the differences between short-term and long-term storage and when to use each.'),
    ('what-you-can-and-cannot-store.html',
     "What You Can and Can't Store in Self Storage Units",
     'Important safety information – a complete list of items you are allowed and not allowed to store in self storage units.'),
    ('benefits-of-professional-packing-service.html',
     'Benefits of Using a Professional Packing Service',
     'Why paying for a professional packing service is often worth it. Save time, reduce stress, and protect your belongings.'),
    ('how-to-pack-clothes-without-wrinkling.html',
     'How to Pack Clothes for Moving Without Wrinkling Them',
     'Stop ironing everything again after your move. Learn the best methods to pack clothes so they arrive wrinkle-free.'),
    ('how-to-pack-kitchen-items-safely.html',
     'How to Pack Kitchen Items Safely When Moving House',
     'The kitchen is the hardest room to pack. Learn professional techniques for safely packing plates, glasses, appliances and crockery.'),
    ('prestige-steel-storage-rooms.html',
     'Why Our Prestige Steel Storage Rooms Are Different',
     'Discover what makes our prestige steel storage rooms better than standard self storage units and why they offer superior protection.'),
    ('choosing-a-removal-company-eastbourne.html',
     'How to Choose a Reliable Removals Company in Sussex',
     "Don't risk your belongings. Learn the essential steps and questions to ask when choosing a trustworthy removals company in Sussex."),
    ('questions-to-ask-removals-company.html',
     '7 Important Questions You Must Ask Before Hiring Removers',
     'Protect yourself and your possessions. These are the 7 key questions every customer should ask before booking a removals company.'),
    ('how-to-spot-rogue-removal-traders.html',
     'How to Spot Rogue Traders in the Removals Industry',
     'Learn the warning signs of rogue traders and how to avoid scams when hiring a removals company.'),
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
    print(f'  ✓ refreshed {slug}')
print(f'\nUpdated {n} of {len(UPDATES)} posts.')
