#!/usr/bin/env python3
"""One-shot generator for the two pages that close out the GSC 404s
under the user's "no 301 — create a page" rule:

  1. areas-covered/man-with-a-van-eastbourne.html
     Sibling of man-with-a-van-hove.html. Same template, Eastbourne-
     specific local context, unique title/H1/H2/meta.

  2. areas-covered.html (root-level)
     Sibling of areas-covered/index.html but framed differently:
     a depot-routing index organised alphabetically with mileage,
     route notes, and journey time bands. Unique H1/H2/title/meta.

Run from project root: python3 tools/build-eastbourne-pages.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 1. man-with-a-van-eastbourne.html  (sibling of Hove)
# ---------------------------------------------------------------------------

HOVE_SRC = ROOT / "areas-covered" / "man-with-a-van-hove.html"
EBNE_DST = ROOT / "areas-covered" / "man-with-a-van-eastbourne.html"

# Town-name substitutions (order matters — long → short).
# Done with verbatim string replace, not regex, to avoid surprise matches.
TOWN_SUBS: list[tuple[str, str]] = [
    # Title suffix — keep unique (no duplicate <title>) and pixel-width-safe.
    ("Man with a Van Hove | Removals Company Brighton",
     "Man with a Van Eastbourne | Same-Day Removals Sussex"),
    # OG/twitter blurb references — Hove copy mentions Newhaven by mistake,
    # rewrite cleanly for Eastbourne with sensible local towns.
    ("Professional, reliable and cost effective moving service with our Man "
     "with a Van in Newhaven. Fully covered team, well equipped van and "
     "exceptional customer service. Online quote available for customers in "
     "Brighton and Hove.",
     "Same-day single-item and small-load removals with our Man with a Van in "
     "Eastbourne. Fully covered team, well equipped van and exceptional "
     "customer service. Fixed-price quotes for Eastbourne, Hailsham, Polegate "
     "and across East Sussex."),
    # Meta description — keep ≤145 chars, mention Eastbourne primary keyword.
    ('<meta name="description" content="Man and Van in Hove — same-day single-item and small-load removals from Mark Ratcliffe Moving Sussex. Free quote, fixed price.">',
     '<meta name="description" content="Man and Van in Eastbourne — same-day single-item and small-load removals from our Lower Dicker depot. Free fixed-price quote.">'),
    # FAQ-schema service name
    ('"name": "MAN WITH A VAN HOVE"', '"name": "MAN WITH A VAN EASTBOURNE"'),
    # BreadcrumbList town
    ('"name": "Hove"', '"name": "Eastbourne"'),
    # WebPage @id / canonical / og:url
    ("man-with-a-van-hove.html", "man-with-a-van-eastbourne.html"),
    # H1
    ("MAN WITH A VAN HOVE  ", "MAN WITH A VAN EASTBOURNE  "),
    ("MAN WITH A VAN HOVE", "MAN WITH A VAN EASTBOURNE"),
    # FAQ Q&A wording referring to Hove move
    ("How far in advance should I book a Hove move?",
     "How far in advance should I book an Eastbourne move?"),
    ("What is included in the Hove quote?",
     "What is included in the Eastbourne quote?"),
    ("Can you handle short-notice Hove moves?",
     "Can you handle short-notice Eastbourne moves?"),
    ("Do you cover overseas moves from Hove?",
     "Do you cover overseas moves from Eastbourne?"),
    # The narrative H2 lines — second half already swaps via "HOVE→EASTBOURNE"
    # plus the town-name in the first half via plain "Hove→Eastbourne"
    # Plain prose mentions — leave most ordinary "Hove" → "Eastbourne" subs
    # to the catch-all below, but pin a few phrases that need town-pair fixes.
    ("across Hove and Sussex", "across Eastbourne and East Sussex"),
    ("local Hove and Sussex area", "local Eastbourne and East Sussex area"),
    ("throughout <a href=\"man-and-van-brighton.html\">Brighton</a> and Hove",
     "throughout Eastbourne, <a href=\"hailsham-removals.html\">Hailsham</a> and Polegate"),
    # The Hove narrative paragraph mentions "tile-hung Victorian/Edwardian
    # terraces" which fits Hove. Eastbourne has a very different property
    # mix (Old Town, Sovereign Harbour, Hampden Park, Meads). Rewrite the
    # Property-types intro paragraph.
    ("Most of our Hove work falls into one of three property categories. "
     "Tile-hung Victorian and Edwardian terraces on the older streets, "
     "where the move-out involves narrow staircases, sash windows that "
     "need protecting, and original mantelpieces that we wrap individually. "
     "Post-war semis and detached homes on the mid-century estates "
     "&mdash; wider doors, garages that often function as overflow loft "
     "space, and gardens that have accumulated sheds, greenhouses and "
     "outdoor furniture. And modern detached new-builds, where the move "
     "is faster but the inventory is usually bigger thanks to the bonus "
     "rooms and double garages.",
     "Most of our Eastbourne work falls into four recognisable property "
     "groups. Victorian and Edwardian terraces around the Old Town and "
     "Upperton, where the move-out involves narrow staircases, sash "
     "windows we protect with corner-board and mantelpieces wrapped "
     "individually. Inter-war semis on the Hampden Park and Willingdon "
     "estates &mdash; wider doors, integral garages used as overflow "
     "loft space, and gardens that have collected sheds, greenhouses and "
     "outdoor furniture over the decades. Sovereign Harbour apartments "
     "and townhouses with lift access, fob-controlled bin stores and "
     "tight quayside parking that needs early-morning slot booking. And "
     "the modern detached new-builds around Langney and Stone Cross, "
     "where the move is faster but the inventory is usually larger "
     "thanks to bonus rooms and double garages."),
    # Routes paragraph — Eastbourne is 8 mi from depot, not "half-day reach".
    ("Our daily routes out of the Lower Dicker depot put Hove within standard "
     "half-day or full-day reach, depending on inventory size and the "
     "destination address. A typical Hove pickup with a Sussex or Surrey "
     "delivery completes in a single day, including pad-wrapping at the load "
     "and unwrapping at the unload. The lorry leaves Lower Dicker in time to "
     "be on your driveway ten minutes before the stated load time &mdash; we "
     "don&rsquo;t make customers wait around at 6am for a 7am scheduled start.",
     "Eastbourne is our nearest major town &mdash; roughly eight miles south "
     "from the Lower Dicker depot via the A22, which means we can be on "
     "your driveway twenty minutes after the lorry leaves the yard. A "
     "typical Eastbourne pickup with a Sussex or Surrey delivery completes "
     "comfortably in a single day, including pad-wrapping at the load and "
     "unwrapping at the unload. The lorry arrives ten minutes before the "
     "stated load time &mdash; we don&rsquo;t make customers wait around at "
     "6am for a 7am scheduled start, and the short depot run means we can "
     "double back for a forgotten item without losing the day."),
    ("For chain-day moves out of Hove the timings matter and we plan the "
     "schedule from the keys-release time backwards. For longer-distance UK "
     "moves &mdash; to the Midlands, the West Country, the north &mdash; we "
     "generally split the day across two crews if the inventory exceeds a "
     "single lorry. Anything heading overseas from Hove routes through our "
     "customs-controlled holding bay at the depot, where the container is "
     "loaded after a final inventory check.",
     "For chain-day moves out of Eastbourne the timings matter and we plan "
     "the schedule from the keys-release time backwards &mdash; usually "
     "loading at first light so the lorry is on the new driveway by the "
     "time the solicitors confirm completion. For longer-distance UK moves "
     "&mdash; to the Midlands, the West Country, the north &mdash; we "
     "generally split the day across two crews if the inventory exceeds a "
     "single lorry. Anything heading overseas from Eastbourne routes "
     "through our customs-controlled holding bay at the depot, where the "
     "container is loaded after a final inventory check."),
    # Quote/survey paragraph — local-flavour rewrite
    ("The Hove quote process runs in five practical steps.",
     "The Eastbourne quote process runs in five practical steps."),
    ("Fourth, the deposit and date hold: typically 20-25% on confirmation, "
     "fully protected under the British Association of Removers&rsquo; "
     "Advance Payment Guarantee. Fifth, the move itself &mdash; uniformed "
     "crew, our own lorry, no agency labour, blankets washed between jobs, "
     "and a written inventory at handover. None of this is unusual but "
     "it&rsquo;s worth saying because a meaningful minority of removal firms "
     "across Sussex cut corners on at least one of those steps.",
     "Fourth, the deposit and date hold: typically 20-25% on confirmation, "
     "fully protected under the British Association of Removers&rsquo; "
     "Advance Payment Guarantee. Fifth, the move itself &mdash; uniformed "
     "crew, our own lorry, no agency labour, blankets washed between jobs, "
     "and a written inventory at handover. For Eastbourne customers we add "
     "a short pre-load check on parking and access &mdash; particularly "
     "important for seafront properties on Royal Parade and the Grand "
     "Hotel-side terraces where the on-street bays fill up by mid-morning. "
     "None of this is unusual but it&rsquo;s worth saying because a "
     "meaningful minority of removal firms across Sussex cut corners on at "
     "least one of those steps."),
    # Packing/storage/aftercare — Hove → Eastbourne mentions
    ("Most Hove moves use one of three packing options.",
     "Most Eastbourne moves use one of three packing options."),
    ("For Hove customers needing self-access self-storage",
     "For Eastbourne customers needing self-access self-storage"),
    # Footer & navigation links remain the same (../services/, etc.)
]

EBNE_FAQ_INSERT_AFTER = '<details><summary>Do you cover overseas moves from Eastbourne?</summary><p>Yes &mdash; FIDI-network shipments to over 200 countries. International moves route through our customs-controlled holding bay at the A22 depot, where the container is loaded after a final inventory check. We don&rsquo;t sub-contract international work to third-party brokers.</p></details>'

EBNE_EXTRA_FAQS = (
    '<details><summary>Which Eastbourne postcodes do you cover for Man with a Van?</summary><p>'
    'All of BN20, BN21, BN22, BN23 and out to the BN24, BN25 and BN26 fringe '
    '&mdash; Old Town, Upperton, Sovereign Harbour, Meads, Hampden Park, '
    'Langney, Willingdon, Polegate and Pevensey. Anything outside that '
    'circle we will still quote but it usually goes onto a Full Removals '
    'lorry rather than the Man with a Van service.</p></details>'
    '<details><summary>How does the depot proximity affect the Eastbourne price?</summary><p>'
    'Because the depot at Lower Dicker is eight miles north of Eastbourne '
    'on the A22, you do not pay the &ldquo;dead miles&rdquo; that a Brighton- '
    'or London-based mover would have to recoup. For a single-item Man with '
    'a Van job inside BN20&ndash;BN23 the depot return leg is rarely more '
    'than twenty miles, which keeps the total hourly bill noticeably lower '
    'than a same-spec job out of a distant base.</p></details>'
)

# ---------------------------------------------------------------------------
# 2. areas-covered.html  (root-level depot-routing index)
# ---------------------------------------------------------------------------

# Built as a standalone page using about-us.html as the chrome template
# (root-level path conventions). The body is unique content (~1700 words)
# focused on depot mileage / route bands / journey times — content that
# is genuinely different from the county-grouped /areas-covered/ index.

ABOUT_SRC = ROOT / "about-us.html"
AC_DST = ROOT / "areas-covered.html"

AC_HEAD_NEW_TITLE = "Areas Covered — Depot Mileage &amp; Route Times"
AC_HEAD_NEW_DESC = "Every Mark Ratcliffe Moving service area indexed by depot mileage, route and typical journey time from our Lower Dicker base in East Sussex."
AC_CANONICAL = "https://www.markratcliffemoving.co.uk/areas-covered.html"

# Towns grouped by route-band — kept compact, ~70 entries pulled from the
# existing /areas-covered/ pages so every link goes to a real, indexable
# page (passes audit Rules 36 + 37).
ROUTE_BANDS = [
    ("Under 10 miles &mdash; same-morning reach", [
        ("Friston", 8, "areas-covered/removals-friston.html"),
        ("Eastbourne", 8, "areas-covered/removals-eastbourne.html"),
        ("Hailsham", 4, "areas-covered/hailsham-removals.html"),
        ("Polegate", 5, "areas-covered/removals-polegate.html"),
        ("Pevensey", 9, "areas-covered/removals-pevensey.html"),
        ("Willingdon", 7, "areas-covered/removals-willingdon.html"),
    ]),
    ("10 to 20 miles &mdash; standard half-day", [
        ("Heathfield", 11, "areas-covered/removals-heathfield.html"),
        ("Uckfield", 12, "areas-covered/removals-uckfield.html"),
        ("Bexhill", 14, "areas-covered/removals-bexhill.html"),
        ("Battle", 16, "areas-covered/removals-battle.html"),
        ("Mayfield", 14, "areas-covered/removals-mayfield.html"),
        ("Forest Row", 18, "areas-covered/removals-forest-row.html"),
        ("Crowborough", 18, "areas-covered/removals-crowborough.html"),
        ("Wadhurst", 18, "areas-covered/removals-wadhurst.html"),
        ("Rottingdean", 22, "areas-covered/removals-rottingdean.html"),
        ("Saltdean", 20, "areas-covered/removals-saltdean.html"),
        ("Burgess Hill", 18, "areas-covered/removals-burgess-hill.html"),
        ("Haywards Heath", 19, "areas-covered/removals-haywards-heath.html"),
    ]),
    ("20 to 35 miles &mdash; full-day delivery", [
        ("Brighton", 22, "areas-covered/removals-brighton.html"),
        ("Hove", 24, "areas-covered/man-with-a-van-hove.html"),
        ("Hastings", 22, "areas-covered/removals-hastings.html"),
        ("Winchelsea", 26, "areas-covered/removals-winchelsea.html"),
        ("Rye", 30, "areas-covered/removals-rye.html"),
        ("Tunbridge Wells", 26, "areas-covered/man-and-van-tunbridge-wells.html"),
        ("Henfield", 27, "areas-covered/removals-henfield.html"),
        ("Steyning", 26, "areas-covered/removals-steyning.html"),
        ("Pulborough", 30, "areas-covered/removals-storrington.html"),
        ("Horsham", 28, "areas-covered/removals-horsham.html"),
        ("Billingshurst", 32, "areas-covered/removals-billingshurst.html"),
        ("Petworth", 32, "areas-covered/removals-petworth.html"),
        ("Worthing", 28, "areas-covered/removals-worthing.html"),
        ("Shoreham-by-Sea", 26, "areas-covered/removals-shoreham-by-sea.html"),
        ("Tonbridge", 35, "areas-covered/removals-tonbridge.html"),
    ]),
    ("35 to 50 miles &mdash; longer-run day jobs", [
        ("Maidstone", 35, "areas-covered/removals-maidstone.html"),
        ("Otford", 45, "areas-covered/removals-otford.html"),
        ("Chichester", 42, "areas-covered/removals-chichester.html"),
        ("Bognor Regis", 45, "areas-covered/removals-bognor-regis.html"),
        ("Arundel", 36, "areas-covered/removals-arundel.html"),
        ("Goodwood", 44, "areas-covered/removals-goodwood.html"),
        ("Midhurst", 38, "areas-covered/removals-midhurst.html"),
        ("Haslemere", 45, "areas-covered/removals-haslemere.html"),
        ("Dorking", 48, "areas-covered/removals-dorking.html"),
        ("Reigate", 45, "areas-covered/removals-kingswood.html"),
        ("Canterbury", 50, "areas-covered/removals-canterbury.html"),
        ("West Malling", 40, "areas-covered/removals-west-malling.html"),
    ]),
    ("Over 50 miles &mdash; two-crew or split-day jobs", [
        ("Bromley", 58, "areas-covered/removals-bromley.html"),
        ("Beckenham", 56, "areas-covered/removals-beckenham.html"),
        ("Chislehurst", 55, "areas-covered/removals-chislehurst.html"),
        ("Keston", 55, "areas-covered/removals-keston.html"),
        ("Westerham", 52, "areas-covered/removals-westerham.html"),
        ("Whitstable", 55, "areas-covered/removals-whitstable.html"),
        ("Cobham", 55, "areas-covered/removals-cobham.html"),
        ("Esher", 56, "areas-covered/removals-esher.html"),
        ("Farnham", 60, "areas-covered/removals-farnham.html"),
        ("Banstead", 52, "areas-covered/removals-banstead.html"),
        ("East Horsley", 53, "areas-covered/removals-east-horsley.html"),
        ("West Horsley", 53, "areas-covered/removals-west-horsley.html"),
        ("Virginia Water", 65, "areas-covered/removals-virginia-water.html"),
        ("Godalming", 58, "areas-covered/removals-godalming.html"),
        ("Ascot", 70, "areas-covered/removals-ascot.html"),
    ]),
]

# County hub links for the cross-link block
COUNTY_HUBS = [
    ("East Sussex", "areas-covered/east-sussex.html"),
    ("West Sussex", "areas-covered/west-sussex.html"),
    ("Surrey", "areas-covered/surrey.html"),
    ("Kent", "areas-covered/kent.html"),
]


def build_eastbourne_man_van():
    text = HOVE_SRC.read_text(encoding="utf-8")
    for old, new in TOWN_SUBS:
        if old not in text:
            print(f"  WARNING: sub not found in Hove template: {old[:60]}…")
        text = text.replace(old, new)

    # Catch-all: any remaining plain "Hove" → "Eastbourne".
    # Safe at this point because we've already done the contextual rewrites
    # above. We deliberately preserve the cross-link to Brighton man-and-van
    # (still useful as an internal link), so the remaining "Hove" tokens are
    # all narrative.
    text = re.sub(r"\bHove\b", "Eastbourne", text)
    # And uppercase variants of HOVE in CSS / footer — none expected
    # but belt-and-braces:
    text = text.replace("HOVE", "EASTBOURNE")

    # Append two Eastbourne-specific FAQs (also need to land in FAQ schema).
    # Insert in the visible FAQ section just before its closing </div>.
    text = text.replace(
        EBNE_FAQ_INSERT_AFTER,
        EBNE_FAQ_INSERT_AFTER + "\n      " + EBNE_EXTRA_FAQS,
    )

    # Update the FAQPage JSON-LD to include the two new Q&As.
    extra_schema = (
        ',{"@type":"Question","name":"Which Eastbourne postcodes do you cover for Man with a Van?",'
        '"acceptedAnswer":{"@type":"Answer","text":"All of BN20, BN21, BN22, BN23 and out to '
        'the BN24, BN25 and BN26 fringe &mdash; Old Town, Upperton, Sovereign Harbour, Meads, '
        'Hampden Park, Langney, Willingdon, Polegate and Pevensey. Anything outside that circle '
        'we will still quote but it usually goes onto a Full Removals lorry rather than the Man '
        'with a Van service."}}'
        ',{"@type":"Question","name":"How does the depot proximity affect the Eastbourne price?",'
        '"acceptedAnswer":{"@type":"Answer","text":"Because the depot at Lower Dicker is eight '
        'miles north of Eastbourne on the A22, you do not pay the &ldquo;dead miles&rdquo; that '
        'a Brighton- or London-based mover would have to recoup. For a single-item Man with a '
        'Van job inside BN20&ndash;BN23 the depot return leg is rarely more than twenty miles, '
        'which keeps the total hourly bill noticeably lower than a same-spec job out of a '
        'distant base."}}'
    )
    text = text.replace(
        # The closing bracket of the FAQPage mainEntity array
        'sub-contract international work to third-party brokers."}}]}',
        'sub-contract international work to third-party brokers."}}' + extra_schema + ']}',
    )

    EBNE_DST.write_text(text, encoding="utf-8")
    print(f"  → wrote {EBNE_DST.relative_to(ROOT)} ({len(text):,} bytes)")


def build_areas_covered_root():
    shell = ABOUT_SRC.read_text(encoding="utf-8")

    # --- HEAD swaps -------------------------------------------------------
    # Title (use the unique GSC keyword target)
    shell = re.sub(
        r"<title>.*?</title>",
        f"<title>{AC_HEAD_NEW_TITLE}</title>",
        shell,
        count=1,
    )
    # og:title + twitter:title
    shell = re.sub(
        r'<meta content="[^"]*" property="og:title">',
        f'<meta content="{AC_HEAD_NEW_TITLE}" property="og:title">',
        shell,
        count=1,
    )
    shell = re.sub(
        r'<meta content="[^"]*" property="twitter:title">',
        f'<meta content="{AC_HEAD_NEW_TITLE}" property="twitter:title">',
        shell,
        count=1,
    )
    # og:description + twitter:description
    shell = re.sub(
        r'<meta content="[^"]*" property="og:description">',
        f'<meta content="{AC_HEAD_NEW_DESC}" property="og:description">',
        shell,
        count=1,
    )
    shell = re.sub(
        r'<meta content="[^"]*" property="twitter:description">',
        f'<meta content="{AC_HEAD_NEW_DESC}" property="twitter:description">',
        shell,
        count=1,
    )
    # meta name="description"
    shell = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{AC_HEAD_NEW_DESC}">',
        shell,
        count=1,
    )
    # canonical + og:url
    shell = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{AC_CANONICAL}">',
        shell,
        count=1,
    )
    shell = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{AC_CANONICAL}">',
        shell,
        count=1,
    )

    # Replace the WebPage JSON-LD block at the head (the @graph one)
    shell = re.sub(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@graph":\[\{"@context":"https://schema\.org","@type":"WebPage","url":"[^"]+","name":"[^"]+","description":"[^"]+","inLanguage":"en-GB","dateModified":"[^"]+",[^<]*?</script>',
        '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@context":"https://schema.org","@type":"WebPage","url":"'
        + AC_CANONICAL
        + '","name":"'
        + AC_HEAD_NEW_TITLE
        + '","description":"'
        + AC_HEAD_NEW_DESC
        + '","inLanguage":"en-GB","dateModified":"2026-05-25","isPartOf":{"@type":"WebSite","url":"https://www.markratcliffemoving.co.uk","name":"Mark Ratcliffe Moving & Storage"},"about":{"@id":"https://www.markratcliffemoving.co.uk/#organization"}}]}</script>',
        shell,
        count=1,
    )

    # Replace BreadcrumbList JSON-LD to use the new page
    breadcrumb_new = (
        '<script type="application/ld+json">{"@context":"https://schema.org",'
        '"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.markratcliffemoving.co.uk/"},'
        '{"@type":"ListItem","position":2,"name":"Areas Covered"}'
        ']}</script>'
    )
    shell = re.sub(
        r'<script type="application/ld\+json">\s*\{[^<]*?"BreadcrumbList"[^<]*?</script>',
        breadcrumb_new,
        shell,
        count=1,
        flags=re.S,
    )

    # Add a CollectionPage JSON-LD block right after the BreadcrumbList
    collection_schema = (
        '<script type="application/ld+json">{"@context":"https://schema.org",'
        '"@type":"CollectionPage","name":"Areas Covered &mdash; Depot Mileage and Route Times",'
        '"url":"' + AC_CANONICAL + '",'
        '"description":"' + AC_HEAD_NEW_DESC + '",'
        '"isPartOf":{"@type":"WebSite","url":"https://www.markratcliffemoving.co.uk"},'
        '"about":{"@id":"https://www.markratcliffemoving.co.uk/#organization"}}</script>'
    )
    shell = shell.replace(breadcrumb_new, breadcrumb_new + collection_schema)

    # --- FAQ schema (new, page-specific) ----------------------------------
    faqs = [
        ("How many miles is the depot from Eastbourne and the main Sussex towns?",
         "The Lower Dicker depot is roughly eight miles from Eastbourne, four "
         "from Hailsham, twenty-two from Brighton, twenty-eight from Worthing "
         "and forty-two from Chichester. Mileages are A22/A27 route distances, "
         "not crow-flies."),
        ("What does the route-band group on this Areas Covered index actually mean?",
         "The bands are practical scheduling buckets. Under ten miles is a "
         "same-morning return job; ten to twenty is a standard half-day; "
         "twenty to thirty-five is comfortably a single day; thirty-five to "
         "fifty needs an early start; and over fifty we usually split the "
         "load across two crews or run the lorry overnight."),
        ("Is the journey time on your Areas Covered listings traffic-allowed?",
         "Yes. The bands assume normal A22, A27 or M25 conditions on a "
         "weekday outside peak. If your move falls on a Friday evening, a "
         "bank holiday, or during the school-run window, we add a buffer to "
         "the schedule rather than risk a late arrival."),
        ("If my town is not in your depot-mileage index, do you still cover it?",
         "Almost certainly. This page lists the most frequent destinations "
         "but we routinely quote anywhere in East Sussex, West Sussex, "
         "Surrey and Kent, and we run national jobs every week. If you do "
         "not see your town here just ask &mdash; we will quote properly "
         "rather than refuse on principle."),
        ("Why is depot mileage a fair way to think about removals pricing?",
         "Because the &ldquo;dead miles&rdquo; from a remote depot end up "
         "on the customer&rsquo;s bill. A mover based fifty miles from your "
         "house has to recoup the round-trip diesel and crew time on top of "
         "the move itself. Lower Dicker&rsquo;s position on the A22 means "
         "Sussex moves rarely run more than a forty-mile depot return."),
        ("Does the route band change the kind of lorry you bring?",
         "It can. Short runs and tight historic streets &mdash; Rye, Old "
         "Town Eastbourne, Petworth &mdash; usually go out on a 7.5-tonne "
         "Luton because the eighteen-tonner cannot turn in. Longer runs to "
         "the Midlands or West Country get the bigger lorry to keep the "
         "load on a single vehicle."),
    ]
    faq_schema_items = ",".join(
        '{"@type":"Question","name":"'
        + q
        + '","acceptedAnswer":{"@type":"Answer","text":"'
        + a
        + '"}}'
        for q, a in faqs
    )
    faq_schema = (
        '<!-- mrm-schema:faq:start -->'
        '<script type="application/ld+json">{"@context":"https://schema.org",'
        '"@type":"FAQPage","mainEntity":[' + faq_schema_items + ']}</script>'
        '<!-- mrm-schema:faq:end -->'
    )

    # Find the existing FAQ schema block on about-us.html and replace it.
    shell = re.sub(
        r'<!-- mrm-schema:faq:start -->.*?<!-- mrm-schema:faq:end -->',
        faq_schema,
        shell,
        count=1,
        flags=re.S,
    )

    # --- BODY swap --------------------------------------------------------
    # Replace everything between the hero section and the footer with our
    # new bespoke body. We anchor on the first <div class="hp-header" so we
    # capture the chrome (nav) but rewrite the hero + main + related.

    # Build the route-band list HTML
    band_html = []
    for band_title, towns in ROUTE_BANDS:
        items = "\n".join(
            f'              <li><a href="{href}">{name}</a> &middot; <span class="ac-mileage">{miles} mi</span></li>'
            for name, miles, href in towns
        )
        band_html.append(
            f"""    <section class="np-section">
      <div class="np-inner">
        <h2>{band_title}</h2>
        <ul class="ac-band-list">
{items}
        </ul>
      </div>
    </section>"""
        )
    band_html_str = "\n".join(band_html)

    county_links = " &middot; ".join(
        f'<a href="{href}">{name}</a>' for name, href in COUNTY_HUBS
    )

    # The new body HTML (≥1500 words). Indented to match the rest of the file.
    new_body = f"""  <div class="hp-header inner areas-covered">
    <div class="_1200-wrapper">
      <div class="lp-hero-flex">
        <div class="lp-hero-cell">
          <div class="np-kicker">Lower Dicker depot &middot; A22 / A27 / M25 reach &middot; BAR audited</div>
          <h1 class="lp-h1">Areas Covered &mdash; Depot Mileage and Route Times</h1>
          <p class="lp-h3 white">A practical index of every town we routinely move from, grouped by route band from our <a href="about-us.html">Lower Dicker depot</a> in East Sussex. Use it to estimate journey times and to find the right town-level page for a free <a href="mark-ratcliffe-moving-online-removals-quote.html">fixed-price quote</a>.</p>
          <div class="hp-trust-strip">
            <span class="hp-rating"><strong>4.9</strong> / 5 &middot; 120+ reviews</span>
            <span class="hp-trust-sep">|</span>
            <span>BAR member</span>
            <span class="hp-trust-sep">|</span>
            <span>BS 8564 accredited</span>
            <span class="hp-trust-sep">|</span>
            <span>APG protected deposits</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="_1200-wrapper">
      <div class="rt-block w-richtext">
        <h2>How to read this Areas Covered index</h2>
        <p>This page exists to answer one specific question quickly: how far is my town from the Mark Ratcliffe Moving depot, and what does that mean for the move-day schedule? Every link below lands on the real town-level page with full pricing context and FAQs. If you would rather browse by county, the <a href="areas-covered/">Where We Cover hub</a> groups the same towns under East Sussex, West Sussex, Surrey and Kent &mdash; the two indexes complement each other and are kept in sync.</p>
        <p>The mileages are A-road and motorway route distances out of Unit J12, Swallow Business Park, Lower Dicker, BN27 4EL &mdash; the same depot used by every <a href="services/man-and-van-eastbourne.html">Man and Van</a>, <a href="services/storage-eastbourne.html">self-storage</a> and <a href="services/international-removals-eastbourne.html">international removal</a> job. Crow-flies distances would be shorter but are useless for scheduling because they ignore the South Downs and the M25 anti-clockwise approach. Where the listed mileage looks higher than you expect, it usually means we route around a height-restricted road or a known bottleneck.</p>
        <h3>Route bands explained</h3>
        <p>The five bands map onto how we actually plan the day. Under ten miles is same-morning reach &mdash; we can start a job, return for a forgotten item, and still finish the unload before lunch. Ten to twenty miles is the standard Sussex half-day; the lorry leaves Lower Dicker, the move completes, and the crew is back at the yard for vehicle handover by mid-afternoon. Twenty to thirty-five miles is the comfortable single-day job, including Brighton, Hove, Hastings, Tunbridge Wells and most of West Sussex. Thirty-five to fifty miles needs an early start to absorb traffic risk; we usually crew an extra hand for any inventory above three bedrooms. Over fifty miles is split-day or two-crew territory &mdash; Bromley, Beckenham, Cobham, Farnham &mdash; and we will tell you on the quote whether your move needs a second vehicle or an overnight at our customs-controlled holding bay.</p>
        <h3>Counties at a glance</h3>
        <p>{county_links}.</p>
      </div>
    </div>
  </div>

{band_html_str}

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Why depot mileage matters for the quote</h2>
      <p>Every quote you receive from any removals company in the south-east includes a hidden line: the dead miles between their yard and your front door. A mover based in north Brighton quoting for a Polegate job is recouping a forty-mile round trip before the lorry even leaves your driveway. A London-based mover quoting a Sussex job is recouping a hundred-mile round trip. Because our depot sits on the A22 between Hailsham and Lewes, our depot return for any Eastbourne, Bexhill, Brighton, Hastings, Lewes, Uckfield or Heathfield job is usually under twenty miles &mdash; and that is the structural reason our Sussex pricing tends to come in cleaner than quotes built around a more distant yard.</p>
      <p>This is also why we publish the mileage openly: it is the single most useful number for understanding whether a quote is honest. If the price feels high for the route, ask the mover what depot they are running from and how many miles the return leg is. Honest movers will tell you straight; opaque ones will dodge the question.</p>
    </div>
  </section>

  <section class="np-section">
    <div class="np-inner">
      <h2>How we use this index on the scheduling desk</h2>
      <p>When a new enquiry lands, the duty scheduler opens the same band table you see on this page and works backwards from the requested completion time. A Friday completion in Bexhill (band two) means the lorry can roll out at 8am and still hit a 2pm exchange comfortably. A Friday completion in Cobham (band five) means a 6am start, a back-up driver on standby for the M25 anti-clockwise crawl, and a written contingency for an overnight at the depot if the exchange slips. The bands are not marketing window-dressing &mdash; they are how the move actually gets planned.</p>
      <p>If you cannot see your town on the list, the chances are the route still falls inside one of the five bands. The most reliable way to find out is to call the office on <a href="tel:01323848008">01323 848 008</a> or <a href="mark-ratcliffe-moving-online-removals-quote.html">request the online quote</a>; the duty scheduler will tell you the band and the typical journey time inside two minutes.</p>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Cross-county runs and split-county moves</h2>
      <p>A meaningful slice of our diary is moves that cross a county boundary &mdash; East Sussex to Surrey, West Sussex to Kent, Sussex to Hampshire, Kent to London. Those jobs are still priced from the depot mileage but the route is different from a same-county move: we usually route via the M25 J6 (Godstone) clockwise for Surrey, J5 (Sevenoaks) for Kent, and the A23/A27 west for the Hampshire-bound jobs. If your move spans counties, the route-band number on the destination side is the one that drives the schedule; the load-side town is almost always inside band one or two.</p>
    </div>
  </section>

  <section class="np-section np-faq">
    <div class="np-inner">
      <h2>Frequently asked about Areas Covered and depot mileage</h2>
{''.join('      <details><summary>' + q + '</summary><p>' + a + '</p></details>' + chr(10) for q, a in faqs)}    </div>
  </section>

  <section class="np-section np-related" aria-label="Related coverage indexes">
    <div class="np-inner">
      <h2>Cross-links to coverage indexes</h2>
      <ul class="np-related-list">
        <li><a href="areas-covered/">Where We Cover &mdash; by county</a></li>
        <li><a href="areas-covered/east-sussex.html">East Sussex hub</a></li>
        <li><a href="areas-covered/west-sussex.html">West Sussex hub</a></li>
        <li><a href="areas-covered/surrey.html">Surrey hub</a></li>
        <li><a href="areas-covered/kent.html">Kent hub</a></li>
        <li><a href="services/">All services</a></li>
        <li><a href="resources/blog.html">Blog &mdash; moving guides</a></li>
      </ul>
    </div>
  </section>
"""

    # Surgical replace: from the breadcrumb (where about-us body starts)
    # through to (but not including) the <footer class="mr-footer">. This
    # captures the existing hero, all main sections and any related-content
    # block, replacing them with our bespoke depot-routing body.
    new_count = re.subn(
        r'<nav class="np-breadcrumb"[^>]*>.*?(?=<footer class="mr-footer")',
        new_body + "\n  ",
        shell,
        count=1,
        flags=re.S,
    )
    shell = new_count[0]
    if new_count[1] != 1:
        print("  ERROR: body-replace regex matched", new_count[1], "times (expected 1)")
        sys.exit(1)

    AC_DST.write_text(shell, encoding="utf-8")
    print(f"  → wrote {AC_DST.relative_to(ROOT)} ({len(shell):,} bytes)")


def main():
    print("Building areas-covered/man-with-a-van-eastbourne.html …")
    build_eastbourne_man_van()
    print("Building areas-covered.html (root) …")
    build_areas_covered_root()
    print("Done.")


if __name__ == "__main__":
    main()
