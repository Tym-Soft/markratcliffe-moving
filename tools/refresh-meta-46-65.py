#!/usr/bin/env python3
"""Refresh SEO metadata on the 20 existing posts that match topics 46-65."""
from __future__ import annotations
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UPDATES = [
    ('real-customer-moving-stories.html',
     'Real Customer Moving Stories | Mark Ratcliffe Moving',
     "Read genuine stories from customers we've helped move across Sussex. Real experiences and feedback from happy clients."),
    ('common-moving-scams-2026.html',
     'Common Moving Scams in 2026 and How to Avoid Them',
     'Stay safe during your move. Learn the most common moving scams and practical ways to protect yourself from rogue traders.'),
    ('should-you-move-yourself-or-hire-professionals.html',
     'Should You Move Yourself or Hire Professional Removers?',
     'DIY move vs hiring professionals – a honest comparison of costs, time, effort, and risks to help you decide.'),
    ('how-to-save-money-on-house-move-2026.html',
     'How to Save Money on Your House Move in 2026',
     'Practical ways to reduce the cost of your house move without cutting corners on quality or safety.'),
    ('what-happens-on-moving-day.html',
     'What Happens on Moving Day – A Step-by-Step Guide',
     'Curious about moving day? We explain exactly what happens from the time our team arrives until everything is safely in your new home.'),
    ('how-to-clean-old-house-before-moving.html',
     'How to Clean Your Old House Before Moving Out – Room by Room Guide',
     'Moving out? Use our complete room-by-room cleaning checklist to leave your old property in perfect condition.'),
    ('moving-day-survival-kit.html',
     'Moving Day Survival Kit: Essential Items You Need',
     "Don't get caught without the basics. Here's exactly what should be in your moving day survival kit for you and your family."),
    ('office-relocation-minimise-disruption.html',
     'Office Relocation Guide: How to Minimise Business Disruption',
     'Planning an office move? Learn proven strategies to reduce downtime, keep your team productive, and ensure a smooth business relocation.'),
    ('moving-care-home-nursing-home.html',
     'Moving a Care Home or Nursing Home – Specialist Guide',
     'Moving vulnerable residents? Discover how we safely and sensitively handle care home and nursing home relocations with minimum stress.'),
    ('moving-pub-or-restaurant.html',
     'Moving a Pub or Restaurant: What You Need to Know',
     'Moving licensed premises? Learn the specific challenges, licensing requirements, and specialist equipment needed when moving a pub or restaurant.'),
    ('moving-heavy-awkward-items.html',
     'Moving Heavy & Awkward Items Like Pianos, Safes & Grandfathers Clocks',
     'Need to move a piano, safe, or other difficult items? We explain how our experienced team safely handles heavy and awkward objects.'),
    ('moving-antiques-valuable-furniture.html',
     'Moving Antiques and Valuable Furniture – Specialist Care',
     'Moving antique furniture or valuable pieces? Learn how our trained team protects and transports high-value items safely.'),
    ('moving-fine-art-collectibles.html',
     'Moving Fine Art and Collectibles – Professional Guide',
     'Moving paintings, sculptures or valuable collections? Discover the specialist packing and handling techniques we use for fine art.'),
    ('international-moves-from-sussex.html',
     'International Removals from Sussex – What You Need to Know',
     'Planning an overseas move from Sussex? Our guide covers customs, shipping, insurance, and everything involved in international removals.'),
    ('moving-student-belongings-parents-guide.html',
     'Moving Student Belongings: Helpful Tips for Parents',
     'Taking your son or daughter to university or bringing them home? Practical tips for safely moving student possessions.'),
    ('moving-over-christmas-and-new-year.html',
     'Moving House Over Christmas or New Year – Is It a Good Idea?',
     'Thinking of moving over the festive period? We explain the pros, cons, availability, and everything you need to consider before booking a Christmas or New Year move.'),
    ('spring-cleaning-before-moving-house.html',
     'Spring Cleaning Before Moving House – The Smart Way to Prepare',
     'Moving in spring? Combine your spring clean with your house move. Our room-by-room guide makes decluttering and packing much easier.'),
    ('moving-during-school-holidays.html',
     'Moving During School Holidays: Pros, Cons & Expert Advice',
     'Should you move during school holidays? We break down the advantages and disadvantages to help families make the best decision.'),
    ('eco-friendly-moving-sustainable-removals.html',
     'Eco-Friendly Moving: How to Have a Sustainable House Move',
     'Want to reduce your environmental impact? Discover practical ways to make your house move more eco-friendly and sustainable in 2026.'),
    ('how-to-make-move-carbon-neutral.html',
     'How to Make Your House Move Carbon Neutral',
     'Learn how to calculate and offset the carbon footprint of your house move. We explain simple ways to make your removal carbon neutral.'),
]

def esc(s): return s.replace('&', '&amp;').replace('"', '&quot;')

n = 0
for slug, title, desc in UPDATES:
    p = 'blog/' + slug
    if not os.path.isfile(p):
        print(f'  ✗ missing {p}')
        continue
    html = open(p, encoding='utf-8').read()
    title_e = esc(title); desc_e = esc(desc)

    # Lambda-based replacements so a title beginning with a digit can't be mis-parsed as backref
    html = re.sub(r'<title>[^<]*</title>', lambda m: f'<title>{title}</title>', html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  lambda m: m.group(1) + desc_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*(")',
                  lambda m: m.group(1) + title_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:title")',
                  lambda m: m.group(1) + title_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*property="og:description"[^>]*content=")[^"]*(")',
                  lambda m: m.group(1) + desc_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*content=")[^"]*("[^>]*property="og:description")',
                  lambda m: m.group(1) + desc_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*name="twitter:title"[^>]*content=")[^"]*(")',
                  lambda m: m.group(1) + title_e + m.group(2), html, count=1)
    html = re.sub(r'(<meta[^>]*name="twitter:description"[^>]*content=")[^"]*(")',
                  lambda m: m.group(1) + desc_e + m.group(2), html, count=1)

    def update_ld(match):
        try:
            data = json.loads(match.group(1))
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
    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_ld, html, flags=re.S)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print(f'  ✓ refreshed {slug}')
print(f'\nUpdated {n} of {len(UPDATES)} posts.')
