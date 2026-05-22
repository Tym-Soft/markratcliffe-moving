#!/usr/bin/env python3
"""
Rewrite the <title> on pages where it matches the <h1> verbatim.

SEO best practice keeps the H1 as the page's bold on-page headline
and uses the <title> for the search-result snippet — the same string
in both spots wastes a differentiation opportunity. Screaming Frog
flags this under "Page Titles: Same as H1".

Each rewrite below keeps the page's keyword but reframes the angle
(e.g. add brand, year, distinguishing detail) so the title and H1
complement each other rather than duplicate. Lengths checked to
stay under audit Rule 8's 550px pixel width.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

REWRITES: dict[str, str] = {
    'areas-covered/surrey.html':
        'Surrey Removals | BAR-Member Movers Since 1982',
    'areas-covered/man-and-van-tunbridge-wells.html':
        'Tunbridge Wells Man &amp; Van | Same-Day Removals',
    'areas-covered/east-sussex.html':
        'East Sussex Removals &amp; Storage | BAR Member Since 1982',
    'blog/how-to-make-move-carbon-neutral.html':
        'Making Your House Move Carbon-Neutral (2026)',
    'blog/how-to-pack-electronics-safely.html':
        'Packing Electronics for Moving: Safe-Transit Checklist',
    'blog/best-day-of-week-to-move-house.html':
        'Best Day to Move House (Cost &amp; Logistics by Weekday)',
    'blog/spring-clean-while-moving.html':
        'Decluttering While You Pack: Spring-Clean Your Move',
    'blog/how-to-save-money-on-house-move-2026.html':
        'Cut House Move Costs in 2026: 15 Proven Savings Tips',
    'blog/essential-moving-day-survival-kit.html':
        'Moving Day Survival Kit: 25 Items to Pack in Your Car',
    'blog/moving-day-step-by-step-guide.html':
        'Move Day Timeline: Hour-by-Hour Removals Walk-Through',
    'blog/how-to-prepare-furniture-for-storage.html':
        'Preparing Furniture for Storage: 6-Step Long-Term Guide',
    'blog/fine-art-moving-guide.html':
        'Moving Fine Art: Crates, Climate &amp; Specialist Handling',
    'blog/how-our-pad-wrap-service-protects-furniture.html':
        'Pad-Wrap Furniture Protection Explained (BAR Method)',
    'blog/how-to-offset-carbon-emissions-moving.html':
        'Offsetting Moving Emissions: A Practical 2026 Guide',
    'blog/common-moving-scams-2026.html':
        'Removals Scams in 2026: Spot Them Before You Sign',
    'blog/business-office-relocation.html':
        'Office Relocation in Sussex: A Weekend Move Playbook',
    'blog/ten-ways-eco-friendly-house-move.html':
        '10 Eco-Friendly Moving Tips for a Greener House Move',
    'blog/what-you-can-and-cannot-store.html':
        'Self-Storage Restricted Items: What You Can&rsquo;t Store',
    'blog/should-you-move-yourself-or-hire-professionals.html':
        'DIY vs Professional Movers: Should You Hire Removers?',
    'blog/best-areas-to-live-east-sussex-2026.html':
        'Best East Sussex Places to Live in 2026 | Mover&rsquo;s Guide',
}

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)


def main() -> int:
    changed = 0
    for path, new_title in REWRITES.items():
        if not os.path.exists(path):
            print(f'  ! missing file: {path}', file=sys.stderr); continue
        html = open(path, encoding='utf-8').read()
        m = TITLE_RE.search(html)
        if not m:
            print(f'  ! no <title> on {path}', file=sys.stderr); continue
        new_html = html[:m.start()] + f'<title>{new_title}</title>' + html[m.end():]
        if new_html != html:
            open(path, 'w', encoding='utf-8').write(new_html)
            changed += 1
    print(f'  retitled {changed} pages')
    return 0


if __name__ == '__main__':
    sys.exit(main())
