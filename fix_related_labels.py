#!/usr/bin/env python3
"""Simplify the visible text on every link inside <ul class="np-related-list">
so it stops looking like keyword stuffing. URLs stay intact.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

# Exact-match label rewrites
LABEL_MAP = {
    # Town pages — strip "Removals" prefix/suffix → just the town
    "Hailsham Removals": "Hailsham",
    "Removals Pevensey": "Pevensey",
    "Removals Uckfield": "Uckfield",
    "Removals Heathfield": "Heathfield",
    "Removals Polegate": "Polegate",
    "Removals Willingdon": "Willingdon",
    "Removals Lewes": "Lewes",
    "Removals Newhaven": "Newhaven",
    "Removals East Grinstead": "East Grinstead",
    "Removals Epsom": "Epsom",
    "Removals Woking": "Woking",
    "Removals Eastbourne": "Eastbourne",
    "Removals Guildford - Top Removal Companies in Guildford": "Guildford",

    # Man-and-Van regional pages — keep service-clarity, drop redundancy
    "Man and Van Eastbourne":   "Man &amp; Van — Eastbourne",
    "Man and Van Leatherhead":  "Man &amp; Van — Leatherhead",
    "Man and Van Newhaven":     "Man &amp; Van — Newhaven",
    "Man with a Van Hove":      "Man &amp; Van — Hove",

    # Service pages — simplify
    "Packing Services Eastbourne":      "Packing Services",
    "Storage Eastbourne":               "Storage",
    "International Removals Eastbourne": "International Removals",
    "European Removals Eastbourne":     "European Removals",

    # Resource pages — short, descriptive
    "Removals & Moving Tips Blog":          "Blog",
    "Removals &amp; Moving Tips Blog":      "Blog",
    "Removals & Storage FAQs":              "FAQs",
    "Removals &amp; Storage FAQs":          "FAQs",
    "How Much Do Removals Cost in Eastbourne? 2026 Price Guide": "Cost Guide",
    "Moving House Checklist Eastbourne":    "Moving Checklist",
    "Moving House Checklist for Eastbourne Movers — 8-Week Plan": "Moving Checklist",
    "How to Pack Fragile Items for a House Move — Pad-Wrap Pros": "How to Pack Fragile Items",

    # Homepage title — just say Home
    "Removals Eastbourne - Storage Eastbourne - Eastbourne Removals": "Home",

    # Packaging shop
    "Mark Ratcliffe Moving &amp; Storage Packaging Shop Eastbourne, Sussex": "Packaging Shop",
    "Mark Ratcliffe Moving & Storage Packaging Shop Eastbourne, Sussex":    "Packaging Shop",

    # Areas — keep as-is
    # "Areas Covered" left alone
}


def fix_file(fp: Path) -> bool:
    text = fp.read_text(encoding='utf-8')
    orig = text

    # Only operate inside <ul class="np-related-list"> blocks
    def rewrite_ul(m):
        block = m.group(0)
        for old, new in LABEL_MAP.items():
            block = re.sub(
                r'(<a [^>]+>)' + re.escape(old) + r'(</a>)',
                r'\1' + new + r'\2',
                block
            )
        return block

    text = re.sub(r'<ul class="np-related-list">.*?</ul>', rewrite_ul, text, flags=re.S)

    if text != orig:
        fp.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob('*.html'):
        if fix_file(fp):
            n += 1
    print(f'Updated related-pages labels on {n} files.')

    # Re-audit labels for any leftovers
    from collections import Counter
    leftovers = Counter()
    for fp in ROOT.rglob('*.html'):
        text = fp.read_text(errors='ignore')
        for ulm in re.finditer(r'<ul class="np-related-list">(.*?)</ul>', text, re.S):
            for am in re.finditer(r'<a [^>]+>([^<]+)</a>', ulm.group(1)):
                lbl = am.group(1).strip()
                # Flag anything still containing "Removals" or "Man and Van" (which we cleaned up)
                if 'Removals' in lbl or 'Man and Van' in lbl or 'Man with a Van' in lbl:
                    leftovers[lbl] += 1
    if leftovers:
        print('\n⚠ Labels still containing keyword-stuffing patterns:')
        for lbl, n in leftovers.most_common():
            print(f'  {n}× {lbl}')
    else:
        print('\n✓ All keyword-stuffed labels simplified.')


if __name__ == '__main__':
    main()
