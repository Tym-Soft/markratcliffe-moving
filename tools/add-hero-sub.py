#!/usr/bin/env python3
"""Add a sub paragraph (`<p class="np-hero-sub">…</p>`) to every hero
that's missing one. Sub copy is page-type-aware and references the
page's location/topic so each one is SEO-distinct.

Idempotent: skips pages that already have a .np-hero-sub paragraph
inside .np-hero-card.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'admin-portal-xK7p9q', 'worker', '.git', 'node_modules',
             '.img-staging', 'tools'}

SERVICE_SUBS = {
    'antiques-moving': 'Specialist antiques moving with full pad-wrap, custom crating and climate-controlled transport. Family-run since 1982, BAR-member service for fragile, period and high-value pieces across Sussex and the UK.',
    'custom-crate-service': 'Custom-built export crates for fine art, antiques and high-value items. Sized to your piece, built in our depot workshop, IPPC-compliant for international sea and air freight. BAR-member service.',
    'european-removals-eastbourne': 'European removals from Eastbourne — Spain, France, Germany, Portugal, Italy and beyond. Full pad-wrap, road-freight with our own crews, fixed-price quotes and BAR Overseas Group member since 1982.',
    'full-packing-service': 'Full packing service by our trained crew — every cup, lamp and painting wrapped in your home, inventoried and labelled. BAR-member standard since 1982. Save your weekend, keep the breakages out.',
    'house-clearance-eastbourne': 'House clearance in Eastbourne and across East Sussex — sympathetic, fully insured and family-run. We sort, donate and dispose responsibly, with itemised quotes and a 48-hour turnaround on most jobs.',
    'international-removals-eastbourne': 'International removals from Eastbourne — UK-Thai specialist plus 200+ worldwide destinations. Full export pad-wrap, sea or air freight, customs handling and BAR Overseas Group member since 1982.',
    'man-and-van-eastbourne': 'Man-and-van service in Eastbourne — fixed-price quotes, fully insured, pad-wrap as standard. The same care as a full-house move, scaled to single items, studio flats and small loads. Family-run since 1982.',
    'office-removals-eastbourne': 'Office removals in Eastbourne and across Sussex — weekend and out-of-hours scheduling, IT-safe handling, fixed-price quotes and BAR-member service. Minimum disruption, maximum care since 1982.',
    'packaging-shop': 'Buy moving boxes, bubble wrap, tape and packing materials from our Lower Dicker depot. Removals-grade stock, bulk prices and same-day collection. Boxes the pros actually use, available to the public.',
    'packing-services-eastbourne': 'Professional packing in Eastbourne — full or part-pack, pad-wrap standard, inventoried and labelled. BAR-member service, family-run since 1982. The pack-day stress, off your plate.',
    'piano-moving': 'Specialist piano moving — uprights, grands, baby grands, antiques. Dedicated piano skids, padded boards, two-crew lift as standard. Insured, BAR-member, family-run since 1982 across Sussex and the UK.',
    'storage-eastbourne': 'Self-storage in Eastbourne — clean, dry, steel strong-rooms in our purpose-built Lower Dicker depot. Short or long term, full inventory, pad-wrapped storage as standard. BS 8564 accredited.',
    'student-removals': 'Student removals across Sussex universities — Brighton, Sussex, Chichester, Surrey. Fixed-price quotes, scaled to a single room or a four-bed share, with the same pad-wrap care we use on family moves.',
    'thai-moving-services': 'UK-Thailand specialist removals — full and part-container, door-to-door service, 20+ years on the route. BAR Overseas Group member with our own crews at both ends of the journey since 1982.',
    'unpacking-service': 'Unpacking service at your new home — every box opened, contents placed where you want them, packing materials removed. Pair it with our full packing for a true door-to-door experience.',
    'white-glove-service': 'White-glove removals — concierge-level service for high-net-worth households, antiques, period properties and complex relocations. Confidential, insured, BAR-member, family-run since 1982.',
}

RESOURCE_SUBS = {
    'pricing': 'Transparent removals pricing from Mark Ratcliffe Moving — typical figures by home size, by distance, and by service add-ons. Fixed-price quotes after a free survey. No hidden mileage clauses.',
    'moving-checklist-eastbourne': 'The 8-week moving checklist from Mark Ratcliffe Moving — what to do, when to do it, and how to keep moving day calm. Born from 40+ years of Sussex removals experience.',
    'removals-eastbourne-cost': 'How much do removals cost in Eastbourne? Real-world price ranges by home size, distance and service level. Direct from a family-run Sussex remover with 40+ years on the road.',
    'helpful-tips': 'Practical moving tips from Mark Ratcliffe Moving — packing technique, antique handling, parking logistics, completion-day planning. 40+ years of Sussex removals know-how, distilled.',
    'buy-packing-materials-eastbourne': 'Buy boxes, bubble wrap, tape and packing materials in Eastbourne — collected from our Lower Dicker depot or delivered. Removals-grade stock at bulk prices, no minimum order.',
    'gallery': 'Photos from real moves — our crews, our lorries, our pad-wrap technique and our UK-Thai shipping work. Family-run Sussex removals as it actually happens, not stock imagery.',
    'faqs': 'Common questions about moving with Mark Ratcliffe Moving & Storage — pricing, insurance, dates, access, antiques, storage and international shipping. Plain-English answers from a family-run remover.',
    'blog': 'Moving guides, how-tos and Sussex removals stories from Mark Ratcliffe Moving & Storage — family-run, BAR-member and on the road since 1982.',
    'index': 'Free moving resources from Mark Ratcliffe Moving — pricing, checklists, cost guides, helpful tips, packing materials and our moving & storage calculator. All from a family-run Sussex remover since 1982.',
}

NP_HERO_CARD_PATTERN = re.compile(
    r'(<div class="np-hero-card">\s*(?:<div class="np-kicker">.*?</div>\s*)?<h1[^>]*>([^<]+)</h1>)',
    re.IGNORECASE | re.DOTALL
)


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)


def town_from_filename(stem: str) -> str:
    """Best-effort extraction of the location from an areas-covered filename."""
    s = stem
    for prefix in ('international-removals-in-', 'man-and-van-', 'man-with-a-van-', 'removals-'):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    # Strip trailing descriptors like "-moving-home-in-sussex".
    for tail in ('-moving-home-in-sussex', '-moving-home-in-surrey',
                 '-surrey', '-sussex'):
        if s.endswith(tail):
            s = s[: -len(tail)]
            break
    return s.replace('-', ' ').title()


def make_sub(path: Path, h1: str) -> str:
    rel = str(path.relative_to(ROOT))
    stem = path.stem  # filename without .html

    # Service pages — explicit copy per service.
    if rel.startswith('services/') and stem in SERVICE_SUBS:
        return SERVICE_SUBS[stem]
    if rel.startswith('services/') and stem == 'index':
        return 'All our removals and storage services in one place — packing, piano, antiques, office, international, self-storage and more. Family-run Sussex specialists since 1982.'

    # Resource pages.
    if rel.startswith('resources/') and stem in RESOURCE_SUBS:
        return RESOURCE_SUBS[stem]

    # Areas-covered: use the town name.
    if rel.startswith('areas-covered/'):
        town = town_from_filename(stem)
        if stem.startswith('international-removals-in-'):
            return (f'International removals from {town} — UK-Thai specialist routes plus 200+ '
                    f'worldwide destinations. Full export pad-wrap, sea and air freight, BAR '
                    f'Overseas Group member, family-run since 1982.')
        if stem.startswith('man-and-van-') or stem.startswith('man-with-a-van-'):
            return (f'Man-and-van service in {town} — fixed-price quotes, fully insured, with '
                    f'the same pad-wrap protection we use on every full-house move. Family-run '
                    f'from our Lower Dicker depot since 1982.')
        if stem in ('east-sussex', 'kent'):
            return (f'Family-run removals across {town} — Eastbourne to the Kentish coast, with '
                    f'BAR-member service, full pad-wrap and fixed-price written quotes. 40+ '
                    f'years moving households across the South East.')
        if stem == 'index':
            return ('Every town we cover in East Sussex, West Sussex, Surrey and Kent — plus '
                    'international removals to 200+ destinations. 84 towns served from our '
                    'Lower Dicker depot, family-run since 1982.')
        # Default removals page.
        return (f'Family-run removals in {town} since 1982 — full pad-wrap, fixed-price written '
                f'quotes and BAR-member service from our Lower Dicker depot. 40+ years moving '
                f'households across Sussex, Surrey, Kent and beyond.')

    # Blog pages — generic supportive copy.
    if rel.startswith('blog/'):
        return ('Practical moving advice from Mark Ratcliffe Moving & Storage — family-run, '
                'BAR-member Sussex removals since 1982. 40+ years of know-how distilled into '
                'short, useful guides.')

    # Root-level pages (about, careers, reviews, etc).
    return ('Family-run removals and storage since 1982 — BAR-member service, full pad-wrap '
            'protection and fixed-price written quotes across Sussex, Surrey, Kent and beyond.')


def process_file(path: Path) -> tuple[bool, str]:
    try:
        html = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f'read error: {e}'

    # Only target pages that already have the np-hero-card wrapper.
    if 'class="np-hero-card"' not in html:
        return False, 'no np-hero-card'

    # Skip if it already has a sub paragraph in the hero card.
    if re.search(r'<div class="np-hero-card">.*?<p class="np-hero-sub"', html, re.DOTALL):
        return False, 'already has np-hero-sub'

    m = NP_HERO_CARD_PATTERN.search(html)
    if not m:
        return False, 'np-hero-card markup unexpected'

    h1_text = m.group(2).strip()
    sub_text = make_sub(path, h1_text)
    # XML-escape minimally — only the ampersands and angle brackets that could
    # break HTML. Our copy doesn't contain those, so this is defensive only.
    sub_text = (sub_text.replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;'))

    sub_html = f'\n      <p class="np-hero-sub">{sub_text}</p>'
    new_html = (html[:m.end()] + sub_html + html[m.end():])
    path.write_text(new_html, encoding='utf-8')
    return True, 'updated'


def main():
    changed = 0
    skipped = 0
    failed = []
    for path in sorted(ROOT.rglob('*.html')):
        if is_skipped(path):
            continue
        ok, msg = process_file(path)
        rel = path.relative_to(ROOT)
        if ok:
            changed += 1
        else:
            if msg in ('no np-hero-card', 'already has np-hero-sub'):
                skipped += 1
            else:
                failed.append((rel, msg))
    print(f'Done. {changed} updated, {skipped} skipped.')
    if failed:
        print(f'{len(failed)} failures:')
        for r, m in failed[:25]:
            print(f'  - {r}: {m}')
    return 0 if not failed else 1


if __name__ == '__main__':
    sys.exit(main())
