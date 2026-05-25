#!/usr/bin/env python3
"""
Sitewide rewrite: the company was founded in 2017, not 1982.

Removes every fabricated longevity claim (since 1982, forty years,
four decades, tens of thousands of moves, etc.), strips BAR-membership
claims (per the prior E-E-A-T cleanup) and updates JSON-LD foundingDate.
Re-frames titles around quality signals instead of years-in-business.

Run from the site root:
    python3 tools/sweep-2017-rebrand.py            # dry-run, prints counts
    python3 tools/sweep-2017-rebrand.py --apply    # writes changes

Audit Rule 44 enforces zero regressions for the stale tokens this
script targets.
"""

from __future__ import annotations
import argparse, glob, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

GLOBS = ['*.html', 'services/*.html', 'areas-covered/*.html',
         'resources/*.html', 'blog/*.html']

# Ordered (regex, replacement) tuples. ORDER MATTERS — more-specific
# compound phrases first so they win before the generic single-token
# cleanups at the bottom. All patterns are case-sensitive by default;
# add (?i) inside the pattern for case-insensitive matches.
REPLACEMENTS: list[tuple[str, str]] = [

    # --- JSON-LD: founding date ----------------------------------------
    (r'"foundingDate"\s*:\s*"1982"',                  '"foundingDate":"2017"'),

    # --- Eyebrows / kickers / footer compound phrases ------------------
    # All rules preserve BAR-membership claims; only the 1982 longevity
    # part is dropped.
    (r'Family-run since 1982\s*&middot;\s*BAR member\s*&middot;\s*BS 8564 accredited',
     'Family-run independent business &middot; BAR member &middot; BS 8564 Accredited'),
    (r'Established 1982\s*&middot;\s*Professional BAR Service',
     'Established 2017 &middot; Professional BAR Service'),
    (r'&middot;\s*Family-run since 1982\s*&middot;', '&middot; Family-run independent business &middot;'),
    (r'&middot;\s*BAR member since 1982\s*&middot;', '&middot; BAR member &middot;'),
    (r'<span>BAR member since 1982</span>',          '<span>BAR member</span>'),

    # --- Meta-description / boilerplate "BAR member, family-run since 1982" pattern ---
    (r'BAR member,\s*family-run since 1982\.\s*Free survey\.',
     'BAR member, family-run independent business. Free survey.'),
    (r'BAR member,\s*family-run since 1982\.',
     'BAR member, family-run independent business.'),
    (r'BAR member,\s*family-run since 1982',
     'BAR member, family-run independent business'),
    (r'BAR member,\s*family-run since &hellip;',
     'BAR member, family-run independent business …'),
    (r'BAR member,\s*family-run since …',
     'BAR member, family-run independent business …'),

    # --- Title-tag trailing patterns ("X Since 1982" / "Movers Since 1982") ---
    (r'\|\s*Professional Movers Since 1982',     '| Professional Sussex Movers'),
    (r'\|\s*Family Movers Since 1982',           '| Local Family Movers'),
    (r'\|\s*Removals Since 1982',                '| Local Sussex Removals'),
    (r'\|\s*Local Movers Since 1982',            '| Local Sussex Movers'),
    (r'\|\s*Sussex Movers Since 1982',           '| Independent Sussex Movers'),
    (r'(throughout Sussex)\s+since 1982',        r'\1'),

    # --- Longevity sentence-prefix rewrites ----------------------------
    # Specific compound prefixes first; generic phrase tokens at the end.
    (r'After packing more than ten thousand homes since 1982',
     'From packing hundreds of homes'),
    (r'After more than ten thousand moves',  'From hundreds of moves'),
    (r'After ten thousand moves',            'From hundreds of moves'),
    (r'After forty years of moving',         'Through years of moving'),
    (r'After forty years of conversations',  'From years of conversations'),
    (r'After forty years of running',        'From years of running'),
    (r'After forty years of',                'From years of'),
    (r'After forty years',                   'Through years of work'),
    (r'After 40\+ years of moving',          'Through years of moving'),
    (r'After 40\+ years',                    'Through years of work'),
    (r'After 40 years of moving',            'Through years of moving'),
    (r'After 40 years',                      'Through years of work'),
    (r'After four decades of',               'From our work in'),
    (r'After four decades',                  'Through the years'),
    (r'From forty years on the road',        'From years on the road'),
    (r'From forty years of',                 'From years of'),
    (r'From forty years',                    'From years of work'),
    (r'From 40\+ years',                     'From years of experience'),
    (r'with over (?:forty|40\+?) years experience',  'with years of professional experience'),
    (r'over (?:forty|40\+?) years experience',       'years of professional experience'),
    (r'(?:forty|40\+?) years experience',            'years of professional experience'),
    (r'for over forty years',                'for years'),
    (r'for over 40 years',                   'for years'),
    (r'for forty years',                     'for years'),
    (r'Over forty years of',                 'Across years of'),
    (r'Over 40\+ years of',                  'Across years of'),
    (r'Over 40 years of',                    'Across years of'),
    (r'over forty years of',                 'across years of'),
    (r'over 40\+ years of',                  'across years of'),
    (r'over 40 years of',                    'across years of'),
    (r'Over forty years',                    'Over the years'),
    (r'over forty years',                    'over the years'),
    (r'Over 40\+ years',                     'Over the years'),
    (r'over 40\+ years',                     'over the years'),
    (r'Over 40 years',                       'Over the years'),
    (r'over 40 years',                       'over the years'),
    (r'Throughout forty years',              'Over the years'),
    (r'throughout forty years',              'over the years'),
    (r'Through forty years',                 'Through years'),
    (r'through forty years',                 'through years'),
    (r'forty years of experience',           'years of experience'),
    (r'forty years on the road',             'years on the road'),
    (r'forty years of',                      'years of'),
    (r'forty years',                         'years of trading'),
    (r'four decades of experience',          'years of experience'),
    (r'four decades of',                     'years of'),
    (r'Four decades of',                     'Years of'),
    (r'four decades',                        'years'),
    (r'40\+ years of experience',            'years of experience'),
    (r'40\+ years of',                       'years of'),
    (r'40\+ years',                          'years of trading'),
    (r'40 years of experience',              'years of experience'),
    (r'40 years of',                         'years of'),
    (r'40[- ]year[- ](history|legacy|tradition|story)', r'long \1'),
    (r'\b40-year\b',                         'multi-year'),
    (r'40 years',                            'years of trading'),
    (r'decades of experience',               'years of experience'),
    (r'decades of moving',                   'years of moving'),
    (r'decades of',                          'years of'),

    # Lingering "for/over decades" self-claims (subject = the company).
    # Generic uses about subject matter (e.g. "tax returns going back
    # decades", "the town's reputation has shifted over the last decade")
    # are not company self-claims and are left intact.
    (r"we&rsquo;ve worked the town for decades",     "we&rsquo;ve worked the town for years"),
    (r"we&rsquo;ve refined the process over decades", "we&rsquo;ve refined the process across many moves"),
    (r"we&rsquo;ve refined the downsizer service over decades", "we&rsquo;ve refined the downsizer service across many moves"),
    (r"we&rsquo;ve done over decades",               "we&rsquo;ve handled many times"),
    (r"have crews who&rsquo;ve worked these streets for decades", "have crews who&rsquo;ve worked these streets for years"),
    (r"crews who&rsquo;ve worked these streets for decades", "crews who&rsquo;ve worked these streets for years"),
    (r"for years, often decades",            "for years"),
    (r"handled high-value antique moves across the South East for decades",
     "handle high-value antique moves across the South East regularly"),
    (r"collected sheds, greenhouses and outdoor furniture over the decades",
     "collected sheds, greenhouses and outdoor furniture over the years"),
    (r"property market has settled into a Friday rhythm over decades",
     "property market settles into a Friday rhythm year after year"),
    # Generic catch-alls for any remaining "for decades" / "over decades"
    # phrases. Safe to apply broadly: the only non-self-claim contexts
    # ("furniture bought to live with for decades") still read fine as
    # "for years"; everything else stops over-claiming history.
    (r"for decades",                         "for years"),
    (r"over decades",                        "over the years"),
    (r"over the decades",                    "over the years"),

    # --- Implausible volume / scale claims -----------------------------
    (r'tens of thousands of moves',          'hundreds of moves'),
    (r'tens of thousands of cubic metres',   'hundreds of cubic metres'),
    (r'tens of thousands of',                'hundreds of'),
    (r'more than ten thousand homes',        'hundreds of homes'),
    (r'more than ten thousand moves',        'hundreds of moves'),
    (r'ten thousand moves',                  'hundreds of moves'),
    (r'ten thousand homes',                  'hundreds of homes'),
    (r'ten thousand',                        'hundreds of'),
    (r'\b10,000\+\s+moves',                  'hundreds of moves'),
    (r'\b5,000\+\s+moves',                   'hundreds of moves'),

    # --- BAR scrub (longest first) -------------------------------------
    # The "BAR membership" → "BAR mem|bership" boundary issue: handle
    # "membership" first so the trailing "ship" doesn't get stranded
    # when the shorter "BAR member" rule fires below.
    # One-time cleanup of artifacts already produced by an earlier pass
    # where "BAR member" + trailing "ship" stranded "movership".
    (r'independent Sussex movership',        'industry-body membership'),

    # BAR-related rules deliberately removed — the company IS BAR-affiliated,
    # so we keep all "BAR member"/"BAR-registered"/"BAR-trained"/"BAR APG"/
    # "British Association of Removers" claims in place. This sweep only
    # handles the 1982 → 2017 founding-date change and dependent longevity
    # claims ("forty years", "four decades", "tens of thousands of moves").

    # Fabricated origin-story paragraphs on the international-area pages:
    # these claim 1982 founding + mid-90s growth (28 staff/11 trucks/etc.)
    # which is incompatible with a 2017 founding. Reframe with truthful
    # current-state copy. Tolerates "started/began/opened" wording variants
    # and the NBSP / &#x27; entity differences via \s+ matchers below.
    (r"Mark Ratcliffe (?:began in the removals industry back in 2017|started in the removals industry in 2017|opened a second hand shop) [^<]*?warehouse containers\.?\s*",
     "Mark Ratcliffe Moving &amp; Storage is an independent Sussex removals company founded in 2017, operating from our purpose-built depot on the A22 at Lower Dicker. We specialise in full-service local, national and international moves &mdash; with dedicated UK&nbsp;&harr;&nbsp;Thailand expertise, European removals and worldwide door-to-door shipping. Our work is BS&nbsp;8564 accredited to the international standard for cross-border consumer moving services."),
    (r"In 2017, Mark Ratcliffe opened a second hand shop[^<]*?warehouse containers\.?\s*",
     "Mark Ratcliffe Moving &amp; Storage is an independent Sussex removals company founded in 2017, operating from our purpose-built depot on the A22 at Lower Dicker. We specialise in full-service local, national and international moves &mdash; with dedicated UK&nbsp;&harr;&nbsp;Thailand expertise, European removals and worldwide door-to-door shipping. Our work is BS&nbsp;8564 accredited to the international standard for cross-border consumer moving services."),

    # "40+" stat blocks (Thai page etc.) — replace longevity stat with a
    # quality stat to preserve grid layout.
    (r'<strong>40\+</strong><span>Years moving overseas</span>',
     '<strong>BS&nbsp;8564</strong><span>Accredited storage standard</span>'),
    (r'<strong>40\+</strong><span>Years experience</span>',
     '<strong>BS&nbsp;8564</strong><span>Accredited storage standard</span>'),
    (r'<strong>40\+</strong>\s*<span>Years',
     '<strong>BS&nbsp;8564</strong><span>Accredited storage standard – Years'),

    # --- "family-run" / "established" / "since" cleanups ---------------
    (r'family-run remover since 1982',       'family-run independent remover'),
    (r'Family-run since 1982',               'Family-run independent business'),
    (r'family-run since 1982',               'family-run independent business'),
    (r'family-run since &hellip;',           'family-run independent business …'),
    (r'family-run since …',                  'family-run independent business …'),
    (r'Eastbourne\'s family-run movers since 1982', "Eastbourne's family-run movers"),
    (r"Eastbourne&rsquo;s family-run movers since 1982", "Eastbourne&rsquo;s family-run movers"),

    (r'established in 1982',                 'established in 2017'),
    (r'Established in 1982',                 'Established in 2017'),
    (r'established 1982',                    'established 2017'),
    (r'Established 1982',                    'Established 2017'),
    (r'founded in 1982',                     'founded in 2017'),
    (r'Founded in 1982',                     'Founded in 2017'),
    (r'in January 1982',                     'in 2017'),
    (r'in 1982',                             'in 2017'),

    # --- Lone "since 1982" / "Since 1982" — must come AFTER all compound phrases ---
    # Order: edges first (so trailing-whitespace is consumed cleanly),
    # then mid-sentence (collapse to single space), then final cleanup.
    (r'\s*[—–-]\s*since 1982',               ''),     # " — since 1982" trailing
    (r'\s*\.\s*Since 1982\.',                '.'),    # ". Since 1982." sentence
    (r'\(since 1982\)',                      ''),
    (r'Since 1982,?\s+',                     ''),     # "Since 1982, we..."
    (r'\s+Since 1982\s+',                    ' '),    # mid-sentence — collapse to one space
    (r'\s+since 1982\s+',                    ' '),    # mid-sentence lowercase
    (r'\s+Since 1982\b',                     ''),     # trailing / before non-word
    (r'\s+since 1982\b',                     ''),     # trailing lowercase
    (r'Since 1982',                          ''),     # final residue
    (r'since 1982',                          ''),     # final residue
    (r'\b1982\b',                            '2017'), # last resort, isolated 1982 tokens

    # --- Targeted punctuation cleanup after deletions ------------------
    # Only narrowly-scoped patterns. Sitewide `\|\s*\|` was REMOVED
    # because it broke JavaScript `||` operators inside <script> tags.
    # Sitewide `&middot;\s*&middot;` was removed because the eyebrow/
    # footer compound-phrase rules above already produce clean output.
    # Capitalize a few specific sentence-starts where BAR-strip leaves
    # a lowercase fragment after a sentence-ending period.
    (r'(\. )trained packers',                r'\1Trained packers'),
    (r'(\. )trained crew',                   r'\1Trained crew'),
    (r'(\. )independent Sussex mover',       r'\1Independent Sussex mover'),
    # Lowercase "years of trading" mid-heading reads poorly; capitalize
    # only when it's the first text inside an <h2>/<h3>/<h4>.
    (r'(<h[234][^>]*>\s*)years of trading', r'\1Years of trading'),
    (r'(<h[234][^>]*>\s*)years of',          r'\1Years of'),
]

COMPILED = [(re.compile(p), r) for p, r in REPLACEMENTS]


def list_pages() -> list[str]:
    out: list[str] = []
    for pat in GLOBS:
        out.extend(glob.glob(pat))
    return sorted(p for p in out if os.path.isfile(p))


def sweep(path: str) -> tuple[str, str, int]:
    """Return (original, rewritten, change_count) for one file."""
    text = open(path, encoding='utf-8').read()
    rewritten = text
    count = 0
    for rx, sub in COMPILED:
        new, n = rx.subn(sub, rewritten)
        if n:
            count += n
            rewritten = new
    return text, rewritten, count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true',
                    help='write changes; default is dry-run')
    args = ap.parse_args()

    pages = list_pages()
    files_changed = 0
    total_replacements = 0
    per_section: Counter[str] = Counter()
    for p in pages:
        original, rewritten, n = sweep(p)
        if n == 0:
            continue
        files_changed += 1
        total_replacements += n
        section = p.split('/', 1)[0] if '/' in p else 'root'
        per_section[section] += n
        if args.apply:
            open(p, 'w', encoding='utf-8').write(rewritten)

    mode = 'APPLIED' if args.apply else 'DRY-RUN'
    print(f'{mode}: {files_changed} files changed, {total_replacements} replacements')
    for section, n in per_section.most_common():
        print(f'  {section:18s} {n:5d}')
    if not args.apply:
        print('\nRe-run with --apply to write changes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
