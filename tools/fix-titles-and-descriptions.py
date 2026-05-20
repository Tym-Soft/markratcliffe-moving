#!/usr/bin/env python3
"""
Bulk fix for Rule 7 (meta description ≤145 chars) and Rule 8
(<title> pixel width ≤550px) across markratcliffemoving.co.uk.

Title shortening — progressive heuristics applied until ≤550px:
  1. Drop " — Family-Run Since 1982" trail
  2. Replace " | Mark Ratcliffe Moving" → " | Mark Ratcliffe"
  3. Drop the entire " | …" suffix
  4. Drop subtitle after " – " / " — " / ": "
  5. As last resort, hard-cut to ~52 chars at a space

Description shortening / synthesis:
  - Missing: synthesised from URL slug + H1 (templates per URL pattern)
  - Too long: truncate at word boundary at ≤142 chars + " …"

Updates `<title>`, `og:title`, JSON-LD BlogPosting "headline" (only for
blog posts), `<meta name="description">`, and `og:description` if
present.
"""

from __future__ import annotations
import os, re, sys, glob, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

sys.path.insert(0, os.path.join(ROOT, 'tools'))
from audit import title_pixel_width, TITLE_PX_MAX, META_DESC_MAX

TITLE_PX_TARGET = 545  # small safety margin under 550


# ------------------------------------------------------------------
# Title shortening
# ------------------------------------------------------------------
def shorten_title(t: str) -> str:
    """Return a shortened title under TITLE_PX_TARGET. Idempotent."""
    if title_pixel_width(t) <= TITLE_PX_TARGET:
        return t

    candidates: list[str] = []
    base = t

    # Step 1 — drop " — Family-Run Since 1982" suffix
    s = re.sub(r'\s*[—-]\s*Family[- ]Run\s+Since\s+1982\s*$', '', base, flags=re.I)
    if s != base: candidates.append(s); base = s

    # Step 2 — collapse "| Mark Ratcliffe Moving" → "| Mark Ratcliffe"
    s = re.sub(r'\|\s*Mark\s+Ratcliffe\s+Moving(?!\w)', '| Mark Ratcliffe', base)
    if s != base: candidates.append(s)

    # Step 3 — drop trailing " | …" entirely
    s2 = re.sub(r'\s*\|\s*[^|]+\s*$', '', base)
    if s2 != base: candidates.append(s2)

    # Step 4 — drop subtitle after the LAST en/em dash
    for sep in (' — ', ' – ', ' - '):
        if sep in base:
            head = base.rsplit(sep, 1)[0]
            candidates.append(head)
            break

    # Combine step 1 + step 2 + step 3/4 if needed
    s3 = re.sub(r'\s*[—-]\s*Family[- ]Run\s+Since\s+1982\s*$', '', t, flags=re.I)
    s3 = re.sub(r'\|\s*Mark\s+Ratcliffe\s+Moving(?!\w)', '| Mark Ratcliffe', s3)
    candidates.append(s3)
    s4 = re.sub(r'\s*\|\s*[^|]+\s*$', '', s3)
    candidates.append(s4)

    # Step 5 — pick the longest candidate that fits, else hard-cut
    candidates = [c.strip() for c in candidates if c and c != t]
    fitting = [c for c in candidates if title_pixel_width(c) <= TITLE_PX_TARGET]
    if fitting:
        # Prefer the LONGEST that fits (most info preserved)
        return max(fitting, key=len)

    # Hard cut at word boundary
    words = t.split()
    out: list[str] = []
    for w in words:
        trial = ' '.join(out + [w])
        if title_pixel_width(trial) > TITLE_PX_TARGET:
            break
        out.append(w)
    return ' '.join(out).rstrip(' ,—–-|:')


# ------------------------------------------------------------------
# Meta description synthesis / shortening
# ------------------------------------------------------------------
def slug_to_place(slug: str) -> str:
    s = re.sub(r'\.html$', '', slug)
    s = re.sub(r'-+moving-home-in-(sussex|surrey)$', '', s)
    parts = re.split(r'[-_]', s)
    return ' '.join(p.capitalize() for p in parts)

DESC_FALLBACKS: dict[str, str] = {
    'index.html':
        'Mark Ratcliffe Moving — family-run Sussex removals and storage since 1982. Free quotes, BAR member, fixed prices, packing & international moves.',
    'careers.html':
        'Join the Mark Ratcliffe Moving team — Sussex removals jobs in Lower Dicker, Eastbourne and beyond. Crew, drivers and packers wanted.',
    'packaging-shop.html':
        'Mark Ratcliffe Moving packaging shop in Eastbourne — boxes, tape, bubble wrap, blankets, wardrobe cartons and packing supplies for collection or delivery.',
    'terms-conditions-and-insurance-details.html':
        'Mark Ratcliffe Moving terms, conditions and insurance details — booking, deposits, liability, claims, cancellation and BAR standards.',
    'thai-moving-services.html':
        'UK to Thailand removals by Mark Ratcliffe Moving — door-to-door shipping, customs paperwork, container booking and Bangkok delivery from Sussex.',
    'mark-ratcliffe-moving-online-removals-quote.html':
        'Request a free Sussex removals quote from Mark Ratcliffe Moving — local, national or international. We reply within 48 hours.',
    'areas-covered.html':
        'Every Sussex, Surrey and Kent town we cover from our Lower Dicker base — full list of removals areas served by Mark Ratcliffe Moving since 1982.',
    'blog.html':
        'Sussex removals advice, packing guides and stories from 40+ years of Mark Ratcliffe Moving — the family-run remover’s blog.',
}

def synthesise_description(path: str, h1: str | None) -> str:
    base = os.path.basename(path)

    if path in DESC_FALLBACKS:
        return DESC_FALLBACKS[path]

    # areas-covered patterns
    if path.startswith('areas-covered/'):
        slug = base
        if slug.startswith('man-and-van-') or slug.startswith('man-with-a-van-'):
            place = slug_to_place(slug.replace('man-and-van-', '').replace('man-with-a-van-', ''))
            d = f'Man and Van in {place} — same-day single-item and small-load removals from Mark Ratcliffe Moving Sussex. Free quote, fixed price.'
        elif slug.startswith('international-removals-in-'):
            place = slug_to_place(slug.replace('international-removals-in-', ''))
            d = f'International removals from {place} by Mark Ratcliffe Moving — Europe, Thailand, Australia, USA. BAR Overseas Group member since 1982.'
        elif slug.startswith('removals-'):
            place = slug_to_place(slug.replace('removals-', ''))
            d = f'Removals in {place} by Mark Ratcliffe Moving — Sussex family-run remover since 1982. BAR member, free survey, fixed-price quotes.'
        else:
            d = f'{h1 or "Sussex removals"} — Mark Ratcliffe Moving, family-run remover serving Sussex, Surrey and Kent since 1982.'
        return d

    # Fallback: H1-based
    if h1:
        return f'{h1} — Mark Ratcliffe Moving, family-run Sussex removals and storage since 1982. Free survey, fixed-price quotes.'
    return 'Mark Ratcliffe Moving — family-run Sussex removals and storage since 1982. Free quotes, BAR member, fixed prices.'


def shorten_description(d: str) -> str:
    if len(d) <= META_DESC_MAX:
        return d
    # Trim at word boundary, end with ellipsis if cut mid-sentence
    target = META_DESC_MAX - 2
    cut = d[:target].rsplit(' ', 1)[0].rstrip(' ,;:—–-')
    if cut.endswith('.'):
        return cut
    return cut + ' …'


# ------------------------------------------------------------------
# File-level fixer
# ------------------------------------------------------------------
TITLE_RE  = re.compile(r'<title>([^<]+)</title>', re.I)
OGT_RE    = re.compile(r'(<meta\s+property="og:title"\s+content=")([^"]*)(")', re.I)
DESC_RE   = re.compile(r'(<meta\s+name="description"\s+content=")([^"]*)(")', re.I)
OGD_RE    = re.compile(r'(<meta\s+property="og:description"\s+content=")([^"]*)(")', re.I)
H1_RE     = re.compile(r'<h1[^>]*>([^<]+)</h1>', re.I)
HEAD_RE   = re.compile(r'</head>', re.I)
HEADL_RE  = re.compile(r'"headline":\s*"([^"]*)"')

def is_redirect(html: str) -> bool:
    head = html[:4096]
    return 'http-equiv="refresh"' in head or 'window.location.replace' in head

def is_noindex(html: str) -> bool:
    head = html[:4096]
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', head, re.I)
    return bool(m and 'noindex' in m.group(1).lower())

def fix_file(path: str) -> str:
    html = open(path, encoding='utf-8').read()
    if is_redirect(html) or is_noindex(html):
        return 'skip-noindex'
    original = html
    changes: list[str] = []

    # --- Title ---
    tm = TITLE_RE.search(html)
    if tm:
        old_t = tm.group(1).strip()
        old_t = ' '.join(old_t.split())
        new_t = shorten_title(old_t)
        if new_t != old_t:
            html = html.replace(f'<title>{tm.group(1)}</title>', f'<title>{new_t}</title>', 1)
            changes.append(f'title {title_pixel_width(old_t)}→{title_pixel_width(new_t)}px')

            # Sync og:title
            ogm = OGT_RE.search(html)
            if ogm:
                old_og = ogm.group(2)
                # only sync if og matched the old title (case-sensitive)
                if old_og.strip() == old_t.strip() or htmllib.unescape(old_og).strip() == htmllib.unescape(old_t).strip():
                    html = OGT_RE.sub(lambda m: m.group(1) + new_t + m.group(3), html, count=1)
                    changes.append('og:title synced')

            # Sync JSON-LD BlogPosting headline ONLY if it equals the old title
            def headline_sub(m: re.Match) -> str:
                if m.group(1).strip() == old_t.strip() or htmllib.unescape(m.group(1)).strip() == htmllib.unescape(old_t).strip():
                    return f'"headline": "{new_t}"'
                return m.group(0)
            html, n = HEADL_RE.subn(headline_sub, html, count=1)
            if n:
                changes.append('headline synced')

    # --- Description ---
    dm = DESC_RE.search(html)
    h1m = H1_RE.search(html)
    h1_txt = (h1m.group(1).strip() if h1m else None)
    if h1_txt:
        h1_txt = re.sub(r'\s+', ' ', htmllib.unescape(h1_txt))

    if dm:
        old_d = dm.group(2)
        new_d = shorten_description(old_d)
        if new_d != old_d:
            html = DESC_RE.sub(lambda m: m.group(1) + new_d + m.group(3), html, count=1)
            changes.append(f'desc {len(old_d)}→{len(new_d)} chars')
            ogdm = OGD_RE.search(html)
            if ogdm and ogdm.group(2) == old_d:
                html = OGD_RE.sub(lambda m: m.group(1) + new_d + m.group(3), html, count=1)
                changes.append('og:desc synced')
    else:
        # Synthesise
        new_d = synthesise_description(path, h1_txt)
        new_d = shorten_description(new_d)
        tag = f'<meta name="description" content="{new_d}">\n  '
        html = HEAD_RE.sub(lambda m: tag + m.group(0), html, count=1)
        changes.append(f'desc synthesised ({len(new_d)} chars)')

    if html == original:
        return 'no-op'
    open(path, 'w', encoding='utf-8').write(html)
    return ', '.join(changes)


def main() -> int:
    paths = sorted(
        glob.glob('*.html') +
        glob.glob('areas-covered/*.html') +
        glob.glob('blog/*.html')
    )
    n_changed = 0
    for p in paths:
        result = fix_file(p)
        if result not in ('no-op', 'skip-noindex'):
            n_changed += 1
            print(f'{p:60s} → {result}')
    print()
    print(f'Updated {n_changed} files of {len(paths)} scanned.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
