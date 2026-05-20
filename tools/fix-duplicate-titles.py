#!/usr/bin/env python3
"""
One-shot fix for duplicate <title>/<h1> across the 20 paired blog posts
that share a topic with an older sibling.

For each B-file in the RENAMES map below, this updates:
  - <title>
  - <meta property="og:title">
  - JSON-LD BlogPosting "headline"
  - <h1>
  - injects a one-sentence lead at the top of the first <p>
    so the new keyword phrase appears in the first paragraph
    (per the H1-keyword-in-lead rule).

Idempotent: if the file already has the new title we skip.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, 'blog')

RENAMES: dict[str, dict[str, str]] = {
    'how-to-avoid-moving-scams.html': {
        'title': "How to Avoid Moving Scams in the UK – Customer's Due-Diligence Guide",
        'h1':    "How to Avoid Moving Scams – A UK Customer's Due-Diligence Guide",
        'kw':    "How to avoid moving scams",
        'lead':  "How to avoid moving scams comes down to a handful of verification steps you can run before you ever pay a deposit.",
    },
    'sustainable-removals-guide.html': {
        'title': "Sustainable Removals Guide – Greener Moving in Sussex 2026",
        'h1':    "Sustainable Removals Guide – Greener Moving in 2026",
        'kw':    "sustainable removals",
        'lead':  "This sustainable removals guide explains the practical choices that reduce the carbon footprint of a Sussex house move without inflating the cost.",
    },
    'cleaning-checklist-moving-out.html': {
        'title': "Cleaning Checklist for Moving Out – End-of-Tenancy Room-by-Room Guide",
        'h1':    "Cleaning Checklist for Moving Out – Room-by-Room",
        'kw':    "cleaning checklist for moving out",
        'lead':  "This cleaning checklist for moving out is the room-by-room sheet our crews recommend to customers who want their deposit back or their old home spotless for the next family.",
    },
    'carbon-neutral-moves-explained.html': {
        'title': "Carbon Neutral Moves Explained – Offsets, Routes & Fleet Choices",
        'h1':    "Carbon Neutral Moves Explained – Offsets, Routes & Fleet",
        'kw':    "carbon neutral moves",
        'lead':  "Carbon neutral moves are an option more Sussex families are asking for, but the term covers several very different practical approaches — offsets, route optimisation and fleet choices each carry different real-world cost and impact.",
    },
    'ways-to-save-on-house-move.html': {
        'title': "Ways to Save on Your House Move – 12 Practical 2026 Tips",
        'h1':    "Ways to Save on Your House Move – 12 Practical Tips",
        'kw':    "ways to save on your house move",
        'lead':  "These ways to save on your house move come straight from forty years of customer conversations — small decisions that compound into hundreds of pounds without cutting corners on safety.",
    },
    'overseas-removals-from-sussex.html': {
        'title': "Overseas Removals from Sussex – Containers, Customs & Costs",
        'h1':    "Overseas Removals from Sussex – Containers, Customs & Costs",
        'kw':    "overseas removals from Sussex",
        'lead':  "Overseas removals from Sussex follow a specific operational rhythm — container booking, customs paperwork, port handling and destination delivery — and the cost picture is genuinely different from what most first-time international movers expect.",
    },
    'care-home-relocation-guide.html': {
        'title': "Care Home Relocation Guide – Moving an Elderly Resident with Care",
        'h1':    "Care Home Relocation Guide – Moving an Elderly Resident with Care",
        'kw':    "care home relocation",
        'lead':  "A care home relocation needs a calmer, slower pace than a standard house move — the dignity of the resident and the continuity of their belongings matter more than the clock.",
    },
    'antique-furniture-moving-specialist.html': {
        'title': "Antique Furniture Moving Specialist – Pad-Wrap, Crating & Insurance",
        'h1':    "Antique Furniture Moving Specialist – Pad-Wrap & Crating",
        'kw':    "antique furniture moving specialist",
        'lead':  "Working with an antique furniture moving specialist matters when the piece in question can't be replaced — pad-wrap, custom crating and the right insurance value are non-negotiable.",
    },
    'licensed-premises-relocation.html': {
        'title': "Licensed Premises Relocation – Pub, Bar & Restaurant Movers",
        'h1':    "Licensed Premises Relocation – Pubs, Bars & Restaurants",
        'kw':    "licensed premises relocation",
        'lead':  "A licensed premises relocation has its own rhythm — stock, cellar gear, glassware, gaming machines and a license that often needs transferring before the day the doors close at the old site.",
    },
    'essential-moving-day-survival-kit.html': {
        'title': "Essential Moving Day Survival Kit – 25 Must-Have Items",
        'h1':    "Essential Moving Day Survival Kit – 25 Must-Have Items",
        'kw':    "essential moving day survival kit",
        'lead':  "An essential moving day survival kit is the one box that does not go in the lorry — kettle, mugs, chargers, toilet roll, the few things that make the first night in the new home liveable.",
    },
    'school-holiday-moves.html': {
        'title': "School Holiday Moves – Booking, Cost & Childcare Tips",
        'h1':    "School Holiday Moves – Booking, Cost & Childcare",
        'kw':    "school holiday moves",
        'lead':  "School holiday moves are the busiest weeks in the Sussex removals calendar — books up early, costs reflect demand, and there are practical childcare and emotional-readiness pieces that matter more than most parents expect.",
    },
    'fine-art-moving-guide.html': {
        'title': "Fine Art Moving Guide – Bespoke Crates & Climate Control",
        'h1':    "Fine Art Moving Guide – Bespoke Crates & Climate Control",
        'kw':    "fine art moving",
        'lead':  "Fine art moving is its own discipline — bespoke crates, climate-stable transport, museum-grade handling and an insurance valuation framework that is different from household contents cover.",
    },
    'heavy-item-moves-pianos-safes.html': {
        'title': "Heavy Item Moves – Pianos, Safes & Awkward Loads in Sussex",
        'h1':    "Heavy Item Moves – Pianos, Safes & Awkward Loads",
        'kw':    "heavy item moves",
        'lead':  "Heavy item moves — pianos, safes, gun cabinets, grandfather clocks — depend on technique and the right equipment rather than brute strength, and a four-person crew with the correct gear is dramatically safer than two willing volunteers.",
    },
    'christmas-new-year-house-move.html': {
        'title': "Christmas & New Year House Move – Booking, Cost & Logistics",
        'h1':    "Christmas & New Year House Move – Booking, Cost & Logistics",
        'kw':    "Christmas and New Year house move",
        'lead':  "A Christmas and New Year house move is one of the quieter windows in the Sussex removals calendar but the operational logistics — completion timing, crew availability, Bank Holiday rules — are unusual and worth planning around.",
    },
    'student-move-tips-for-parents.html': {
        'title': "Student Move Tips for Parents – Term-Start & End-of-Year Help",
        'h1':    "Student Move Tips for Parents – Term Start & End",
        'kw':    "student move tips for parents",
        'lead':  "These student move tips for parents come from many term-start and end-of-year trips up and down the country — what to pack, what to ship, what to leave at home, and the small logistics that save a five-hour round trip.",
    },
    'business-office-relocation.html': {
        'title': "Business Office Relocation – Sussex Commercial Movers",
        'h1':    "Business Office Relocation – Sussex Commercial Movers",
        'kw':    "business office relocation",
        'lead':  "A business office relocation is a project, not a moving day — the IT cutover window, employee communication, lease overlap and out-of-hours crew availability all matter more than the lorry size.",
    },
    'customer-moving-stories.html': {
        'title': "Customer Moving Stories from Sussex – Real Removals Reviews",
        'h1':    "Customer Moving Stories from Sussex – Real Reviews",
        'kw':    "customer moving stories",
        'lead':  "These customer moving stories from Sussex households — first-time buyers, retirees downsizing, families relocating from London — are the real-world picture of what booking us looks like in 2026.",
    },
    'diy-move-vs-professional.html': {
        'title': "DIY Move vs Professional Removers – True Cost Comparison",
        'h1':    "DIY Move vs Professional Removers – True Cost Comparison",
        'kw':    "DIY move vs professional",
        'lead':  "The DIY move vs professional removers comparison is rarely as simple as the rental-van quote suggests — fuel, time off work, insurance gaps and the real-world risk of damage all change the picture.",
    },
    'spring-clean-while-moving.html': {
        'title': "Spring Clean While Moving – Declutter as You Pack",
        'h1':    "Spring Clean While Moving – Declutter As You Pack",
        'kw':    "spring clean while moving",
        'lead':  "Choosing to spring clean while moving sounds like doubling the work, but if the cleaning is paced into the packing it actually halves the total effort and leaves the old home in better shape on completion day.",
    },
    'moving-day-step-by-step-guide.html': {
        'title': "Moving Day Step-by-Step Guide – Hour-by-Hour Timeline",
        'h1':    "Moving Day Step-by-Step Guide – Hour-by-Hour Timeline",
        'kw':    "moving day step-by-step",
        'lead':  "This moving day step-by-step timeline walks you through the typical Sussex house move from the 8am crew arrival through to the final signed inventory at the new property after dark.",
    },
}


# ------------------------------------------------------------------
def replace_first(html: str, pattern: str, replacement: str, flags=0) -> tuple[str, int]:
    new_html, n = re.subn(pattern, replacement, html, count=1, flags=flags)
    return new_html, n


def inject_lead(html: str, lead: str) -> tuple[str, bool]:
    """Inject lead sentence at start of first <p> after </header>.

    Skips if lead text already present (idempotency).
    Returns (new_html, injected_bool).
    """
    if lead in html:
        return html, False

    # Find first <p ...>CONTENT</p> after </header>
    header_end = html.find('</header>')
    if header_end < 0:
        return html, False

    after = html[header_end:]
    m = re.search(r'<p\b([^>]*)>(.*?)</p>', after, re.S)
    if not m:
        return html, False

    abs_start = header_end + m.start()
    abs_end   = header_end + m.end()
    attrs   = m.group(1)
    content = m.group(2).lstrip()
    new_p   = f'<p{attrs}>{lead} {content}</p>'

    return html[:abs_start] + new_p + html[abs_end:], True


def fix_file(path: str, cfg: dict[str, str]) -> str:
    html = open(path, encoding='utf-8').read()
    original = html
    changes: list[str] = []

    title = cfg['title']
    h1    = cfg['h1']
    lead  = cfg['lead']

    new_html, n = replace_first(
        html,
        r'<title>[^<]*</title>',
        f'<title>{title}</title>',
    )
    if n: changes.append('title'); html = new_html

    new_html, n = replace_first(
        html,
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{title}"',
    )
    if n: changes.append('og'); html = new_html

    # JSON-LD BlogPosting headline (only the first BlogPosting block)
    def headline_sub(m: re.Match) -> str:
        block = m.group(0)
        return re.sub(r'"headline":\s*"[^"]*"', f'"headline": "{h1}"', block, count=1)
    new_html, n = re.subn(
        r'\{"@context":\s*"https://schema\.org",\s*"@type":\s*"BlogPosting".*?\}',
        headline_sub,
        html,
        count=1,
        flags=re.S,
    )
    if n: changes.append('headline'); html = new_html

    new_html, n = replace_first(
        html,
        r'<h1>[^<]*</h1>',
        f'<h1>{h1}</h1>',
    )
    if n: changes.append('h1'); html = new_html

    html, injected = inject_lead(html, lead)
    if injected: changes.append('lead')

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
        return ', '.join(changes) or 'no-op'
    return 'skipped (already up to date)'


def main() -> int:
    missing = []
    for slug in RENAMES:
        p = os.path.join(BLOG, slug)
        if not os.path.exists(p):
            missing.append(slug)
    if missing:
        print('Missing files:', missing, file=sys.stderr)
        return 1

    for slug, cfg in RENAMES.items():
        result = fix_file(os.path.join(BLOG, slug), cfg)
        print(f'{slug:55s} → {result}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
