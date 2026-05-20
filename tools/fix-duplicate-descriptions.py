#!/usr/bin/env python3
"""
Rewrite the meta description on each of the 20 paired blog posts so
no two indexable pages share the same description. Same idea as the
earlier duplicate-title fix but for descriptions.

Each new description is ≤145 chars, distinct from the sibling page's
description, and reframes the angle so search engines don't see
near-duplicate snippets.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, 'blog')

# slug → new meta description (≤145 chars, distinct from sibling)
NEW_DESCRIPTIONS = {
    'antique-furniture-moving-specialist.html':
        'Specialist antique furniture moving in Sussex — pad-wrap, custom crating and BAR-accredited handlers for irreplaceable pieces.',
    'business-office-relocation.html':
        'Sussex business office relocation — IT cutover planning, out-of-hours crew availability and lease overlap logistics, with fixed quotes.',
    'carbon-neutral-moves-explained.html':
        'Carbon neutral moves explained — what offsets actually do, how route optimisation helps, and which fleet choices cut emissions most.',
    'care-home-relocation-guide.html':
        'Care home relocation guide for families — moving an elderly resident with dignity, slower pace, continuity of belongings, full BAR cover.',
    'christmas-new-year-house-move.html':
        'Christmas and New Year house move logistics — completion timing, Bank Holiday rules, crew availability and the cost picture for Sussex.',
    'cleaning-checklist-moving-out.html':
        'End-of-tenancy cleaning checklist — room-by-room sheet our Sussex crews recommend for deposit returns and a spotless handover.',
    'customer-moving-stories.html':
        'Customer moving stories from Sussex — first-time buyers, retirees downsizing and families relocating from London, in their own words.',
    'diy-move-vs-professional.html':
        'DIY move vs professional removers — the true cost comparison once fuel, time off work, insurance gaps and damage risk are factored in.',
    'essential-moving-day-survival-kit.html':
        'Essential moving day survival kit — 25 must-have items for the first night box that does not go in the lorry, from a Sussex crew.',
    'fine-art-moving-guide.html':
        'Fine art moving guide — bespoke crates, climate-stable transport, museum-grade handling and the insurance valuation that protects you.',
    'heavy-item-moves-pianos-safes.html':
        'Heavy item moves in Sussex — pianos, safes, gun cabinets, grandfather clocks. Technique and the right gear matter more than brute force.',
    'how-to-avoid-moving-scams.html':
        'How to avoid moving scams in the UK — a customer due-diligence checklist of red flags, verification steps and what to do if targeted.',
    'licensed-premises-relocation.html':
        'Licensed premises relocation — pubs, bars and restaurants with stock, cellar gear, glassware and licence transfers handled in sequence.',
    'moving-day-step-by-step-guide.html':
        'Moving day step-by-step timeline — hour-by-hour, from the 8am crew arrival through to the signed inventory at the new property.',
    'overseas-removals-from-sussex.html':
        'Overseas removals from Sussex — container booking, customs paperwork, port handling and destination delivery, with the real cost picture.',
    'school-holiday-moves.html':
        'School holiday moves — the busiest weeks in the Sussex removals calendar. Booking lead time, peak pricing and childcare-on-the-day tips.',
    'spring-clean-while-moving.html':
        'Spring clean while moving — declutter as you pack to halve the total effort and leave the old home in better shape on completion day.',
    'student-move-tips-for-parents.html':
        'Student move tips for parents — term-start and end-of-year trips. What to pack, what to ship, what to leave at home, plus halls logistics.',
    'sustainable-removals-guide.html':
        'Sustainable removals guide — greener moving choices for Sussex 2026: reused crates, route optimisation and how offsets actually work.',
    'ways-to-save-on-house-move.html':
        'Ways to save on your house move — 12 practical tips from 40 years of Sussex removals. Small decisions that compound into hundreds saved.',
}


DESC_PATTERNS = [
    (re.compile(r'<meta\s+name="description"\s+content="[^"]*"', re.I),
     lambda new: f'<meta name="description" content="{new}"'),
    (re.compile(r'<meta\s+property="og:description"\s+content="[^"]*"', re.I),
     lambda new: f'<meta property="og:description" content="{new}"'),
]

# JSON-LD BlogPosting "description"
JSONLD_DESC_RE = re.compile(r'(\{"@context":\s*"https://schema\.org",\s*"@type":\s*"BlogPosting".*?\})', re.S)
JSONLD_DESC_FIELD = re.compile(r'"description":\s*"[^"]*"')


def fix(path: str, new_desc: str) -> bool:
    html = open(path, encoding='utf-8').read()
    original = html

    # meta name="description" and og:description — update both if either matches
    for pat, build in DESC_PATTERNS:
        html, n = pat.subn(build(new_desc), html, count=1)

    # JSON-LD BlogPosting description
    def jsonld_sub(m: re.Match) -> str:
        block = m.group(1)
        return JSONLD_DESC_FIELD.sub(f'"description": "{new_desc}"', block, count=1)
    html, _ = JSONLD_DESC_RE.subn(jsonld_sub, html, count=1)

    if html == original:
        return False
    open(path, 'w', encoding='utf-8').write(html)
    return True


def main() -> int:
    missing = [s for s in NEW_DESCRIPTIONS if not os.path.exists(os.path.join(BLOG, s))]
    if missing:
        print('Missing files:', missing, file=sys.stderr)
        return 1

    too_long = [s for s, d in NEW_DESCRIPTIONS.items() if len(d) > 145]
    if too_long:
        for s in too_long:
            print(f'  TOO LONG ({len(NEW_DESCRIPTIONS[s])} chars): {s}', file=sys.stderr)
        return 1

    for slug, desc in NEW_DESCRIPTIONS.items():
        ok = fix(os.path.join(BLOG, slug), desc)
        print(f'{slug:55s} → {"updated" if ok else "no change"}  ({len(desc)} chars)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
