#!/usr/bin/env python3
"""Fix per-page duplicate <img src> values.

Strategy: for each <img> tag in document order, the first occurrence of
a given basename is kept untouched; every subsequent occurrence on the
same page is rewritten to a different image from the project library
(preferring same-theme alternatives, falling back to general). Alt text
is rewritten to match the replacement.

Excluded from replacement (require manual handling):
  - accreditation logos (BAR / FHIO / IMA / BS-8564-2 / APG / UK-Thai group)
  - small SVG icons (acrobat_pdf.svg etc.)
  - the Mark-Ratcliffe.svg brand logo

Run from repo root: python3 tools/fix-dup-images.py
Then re-run tools/audit-dup-images.py to see remaining issues.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'admin-portal-xK7p9q', 'worker', '.git', 'node_modules', '.img-staging', 'tools'}

EXCLUDE_FROM_REPLACE = {
    'mark-BAR-in-frame.webp',
    'bs-8564-2-removals-storage-accreditation.webp',
    'apg-approved-payment-guarantee-uk-domestic.webp',
    'ima-international-movers-association-logo.webp',
    'uk-thai-movers-group-logo.webp',
    'fhio-accredited-member-logo.webp',
    'acrobat_pdf.svg',
    'Mark-Ratcliffe.svg',
}

REPLACEMENTS = {
    'packing': [
        ('mark-ratcliffe-export-packing-wrap-international.webp',          'Mark Ratcliffe export packing and wrap for an international shipment'),
        ('mark-ratcliffe-loading-thailand-shipping-container.webp',        'Mark Ratcliffe crew loading a Thailand-bound shipping container'),
        ('mark-ratcliffe-loading-shipping-thailand-international.webp',    'Mark Ratcliffe loading a Thailand-bound 20ft container at the depot'),
        ('mark-ratcliffe-removals-tea-carton.webp',                        'Mark Ratcliffe removals tea carton for books and dense items'),
        ('mark-ratcliffe-removals-long-box-carton-3-75-cuft.webp',         'Mark Ratcliffe 3.75 cu ft long box carton for awkward items'),
        ('mark-ratcliffe-removals-tall-box-carton-5-6-cuft.webp',          'Mark Ratcliffe 5.6 cu ft tall wardrobe carton'),
        ('mark-ratcliffe-removals-carton-3-cuft.webp',                     'Mark Ratcliffe 3 cu ft standard removals carton'),
        ('mark-ratcliffe-removals-tea-carton-4-cuft.webp',                 'Mark Ratcliffe 4 cu ft tea carton'),
    ],
    'fleet': [
        ('mark-ratcliffe-removals-fleet-pantechnicon-van-residential.webp','Mark Ratcliffe pantechnicon and van at a Sussex residential move'),
        ('mark-ratcliffe-removal-truck-detached-house-driveway.webp',      'Mark Ratcliffe removal truck on a detached house driveway'),
        ('mark-ratcliffe-road-train-removal-lorry-elite-moving.webp',      'Mark Ratcliffe road-train lift via Elite Moving'),
        ('mark-ratcliffe-matthew-james-trade-shipping-collaboration.webp', 'Mark Ratcliffe and Matthew James Global Relocations trade collaboration'),
        ('mark-ratcliffe-uk-thai-movers-branded-van.webp',                 'Mark Ratcliffe UK-Thai Movers branded van'),
        ('mark-ratcliffe-thai-themed-truck-mural-rear.webp',               'Hand-painted Thailand mural on a Mark Ratcliffe pantechnicon'),
        ('mark-ratcliffe-shipping-containers-international-removals-eastbourne.webp', 'Shipping containers at the Mark Ratcliffe Eastbourne depot'),
    ],
    'storage': [
        ('mark-ratcliffe-self-storage-room-wrapped-furniture-eastbourne.webp', 'Inside a Mark Ratcliffe Eastbourne steel-strong-room storage unit'),
    ],
    'sussex': [
        ('mark-ratcliffe-removal-crowborough-east-sussex.webp',            'Mark Ratcliffe removal in Crowborough, East Sussex'),
        ('mark-ratcliffe-hove-to-petersfield-sussex-hampshire-removal.webp','Mark Ratcliffe Hove to Petersfield removal'),
        ('mark-ratcliffe-sussex-to-ledbury-removal.webp',                  'Mark Ratcliffe long-distance Sussex to Ledbury removal'),
        ('mark-ratcliffe-late-night-collection-removals.webp',             'Mark Ratcliffe late-night removal collection'),
        ('mark-ratcliffe-movers-packers-shippers-sussex.webp',             'Mark Ratcliffe Sussex movers, packers and shippers crew'),
    ],
    'international': [
        ('mark-ratcliffe-shipping-bangkok-thailand-removals.webp',         'Mark Ratcliffe shipment bound for Bangkok, Thailand'),
        ('mark-ratcliffe-bracknell-to-bangkok-international-removal.webp', 'Mark Ratcliffe Bracknell to Bangkok international removal'),
        ('mark-ratcliffe-cheshire-to-downtown-bangkok-thailand.webp',      'Mark Ratcliffe Cheshire to downtown Bangkok shipment'),
        ('mark-ratcliffe-shipping-hua-hin-thailand-loading-uk.webp',       'Mark Ratcliffe UK loading day for a Hua Hin shipment'),
        ('mark-ratcliffe-thailand-groupage-shared-container.webp',         'Mark Ratcliffe Thailand groupage shared-container shipping'),
        ('mark-ratcliffe-cotswold-collection-thailand-shipping.webp',      'Mark Ratcliffe Cotswold collection for a Thailand-bound container'),
        ('mark-ratcliffe-europe-removals-copenhagen-lisbon.webp',          'Mark Ratcliffe European removals to Copenhagen and Lisbon'),
        ('mark-ratcliffe-croydon-to-thailand-shipment-collection.webp',    'Mark Ratcliffe Croydon collection for a Thailand-bound shipment'),
        ('mark-ratcliffe-800-cuft-uplift-samut-prakan-thailand.webp',      'Mark Ratcliffe 800 cu ft uplift bound for Samut Prakan, Thailand'),
        ('mark-ratcliffe-wimbledon-thai-festival-shipping.webp',           'Mark Ratcliffe trade work at the Wimbledon Thai Festival'),
        ('mark-ratcliffe-thai-shipment-delivery-thailand.webp',            'Mark Ratcliffe delivering a Thai shipment at the destination'),
        ('mark-ratcliffe-shipping-thailand-international-removal.webp',    'Mark Ratcliffe 20ft container ready to ship to Thailand'),
        ('mark-ratcliffe-international-shipping-removals.webp',            'Mark Ratcliffe trucks and trade partners on a multi-vehicle international load'),
        ('mark-ratcliffe-customer-loaded-boxes-hua-hin-thailand.webp',     'Mark Ratcliffe customer with packed boxes for a Hua Hin shipment'),
    ],
}

THEME_FOR = {
    'pad-wrapped-furniture-eastbourne-removals.webp': 'packing',
    'mark-ratcliffe-vans-front2.webp': 'fleet',
    'mark-ratcliffe-removal-fleet-vehicles-sussex.webp': 'fleet',
    'mark-ratcliffe-sleeper-cab-removal-lorry.webp': 'fleet',
    'mark-ratcliffe-modern-removal-lorry-eastbourne.webp': 'fleet',
    'mark-ratcliffe-wrapped-furniture-sussex.webp': 'packing',
    'mark-ratcliffe-crew-loading-piano-eastbourne.webp': 'packing',
    'mark-ratcliffe-1963-vintage-bedford-removal-van.webp': 'fleet',
    'packaging-shop-header.webp': 'packing',
    'white-modular-box-system.webp': 'packing',
    'nopi-belongings-export-wrapped-thailand.webp': 'international',
    'bangkok-delivery-team-surprise-nopi.webp': 'international',
}

SIMPLE_IMG_RE = re.compile(
    r'(<img\b[^>]*?\bsrc\s*=\s*["\'])([^"\']+)(["\'][^>]*?>)',
    re.IGNORECASE | re.DOTALL
)


def basename(src: str) -> str:
    s = src.split('?', 1)[0].split('#', 1)[0]
    return s.rsplit('/', 1)[-1]


def rel_prefix(src: str) -> str:
    s = src.split('?', 1)[0]
    if s.startswith('../images/'): return '../images/'
    if s.startswith('/images/'):   return '/images/'
    if s.startswith('images/'):    return 'images/'
    # Fallback: copy the part before the basename
    return s[:-len(basename(s))] if basename(s) else 'images/'


def candidates_for(theme: str):
    """Yield (file, alt) in order: same theme first, then others."""
    if theme in REPLACEMENTS:
        yield from REPLACEMENTS[theme]
    for t in REPLACEMENTS:
        if t != theme:
            yield from REPLACEMENTS[t]


def process_file(path: Path) -> int:
    """Return number of <img> tags rewritten."""
    text = path.read_text(encoding='utf-8', errors='replace')

    # First pass: catalogue every basename currently referenced on the page.
    page_srcs = set()
    for m in SIMPLE_IMG_RE.finditer(text):
        page_srcs.add(basename(m.group(2)))

    seen_count = {}
    inserted_replacements = set()
    rewrites = 0
    alt_re = re.compile(r'(\balt\s*=\s*["\'])([^"\']*)(["\'])', re.IGNORECASE)

    def replacement_for(orig_bn, prefix):
        theme = THEME_FOR.get(orig_bn, 'fleet')
        for cand, alt in candidates_for(theme):
            if cand in page_srcs:        continue
            if cand in inserted_replacements: continue
            return cand, alt, prefix + cand
        return None

    def repl(m):
        nonlocal rewrites
        pre, src, post = m.group(1), m.group(2), m.group(3)
        bn = basename(src)
        seen_count[bn] = seen_count.get(bn, 0) + 1
        if seen_count[bn] == 1:
            return m.group(0)
        if bn in EXCLUDE_FROM_REPLACE:
            return m.group(0)
        prefix = rel_prefix(src)
        choice = replacement_for(bn, prefix)
        if not choice:
            return m.group(0)
        cand, new_alt, new_src = choice
        inserted_replacements.add(cand)
        page_srcs.add(cand)
        new_post = alt_re.sub(lambda am: am.group(1) + new_alt + am.group(3), post, count=1)
        rewrites += 1
        return pre + new_src + new_post

    new_text = SIMPLE_IMG_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
    return rewrites


def main():
    total = 0
    files_changed = 0
    for path in sorted(ROOT.rglob('*.html')):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        n = process_file(path)
        if n > 0:
            files_changed += 1
            total += n
            print(f"  {path.relative_to(ROOT)}  ({n} <img> rewritten)")
    print(f"\nDone. {files_changed} file(s) changed; {total} <img> tag(s) rewritten.")


if __name__ == '__main__':
    main()
