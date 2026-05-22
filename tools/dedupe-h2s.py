#!/usr/bin/env python3
"""
Rewrite every duplicated <h2> across the site so each is unique to
its page. The page's <h1> supplies the topic anchor — that keeps the
rewritten H2 on-topic and naturally varied across pages.

Strategy:
  1. Build a page → H1 map (Rule 11 already guarantees uniqueness).
  2. Build an H2 → pages-using-it map. Anything appearing on more
     than one page is a duplicate the audit's new Rule 39 will flag.
  3. For each duplicate H2, pick a per-page rewrite template that
     stitches in the page's topic (derived from the H1) so the result
     stays grammatical and topical.
  4. Re-pass: if two pages still share a rewritten H2, add a smaller
     differentiator (file slug) until everything is unique.

The tool is idempotent — running it again on already-unique H2s does
nothing, because the lookup map only contains current duplicates.
"""

from __future__ import annotations
import glob, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# --- Regexes ---
H1_RE = re.compile(r'<h1\b[^>]*>(.*?)</h1>', re.I | re.S)
H2_RE = re.compile(r'(<h2\b[^>]*>)(.*?)(</h2>)', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')
ENT_RE = re.compile(r'&[a-z]+;|&#\d+;', re.I)
NAV_END_RE = re.compile(r'</nav>\s*</div>|</nav>(?!\s*<)', re.I | re.S)
FOOTER_RE = re.compile(r'<footer\b', re.I)


def clean(text: str) -> str:
    """Strip HTML tags and entities; collapse whitespace."""
    t = ENT_RE.sub(' ', TAG_RE.sub('', text))
    return re.sub(r'\s+', ' ', t).strip()


def body_window(html: str) -> tuple[int, int]:
    m = NAV_END_RE.search(html); start = m.end() if m else 0
    m = FOOTER_RE.search(html); end = m.start() if m else len(html)
    return start, end


def extract_h1(html: str) -> str:
    m = H1_RE.search(html)
    return clean(m.group(1)) if m else ''


def topic_for(path: str, h1: str) -> str:
    """Compact subject phrase to drop into rewritten H2s.
    Prefers a tidy version of the H1; falls back to the filename."""
    if h1:
        t = h1
        # Trim trailing tagline after em-dash or pipe
        for sep in (' — ', ' – ', ' - ', ' | '):
            if sep in t:
                t = t.split(sep, 1)[0]
        t = t.strip().rstrip('?!.,;:')
        # Drop a leading "Removals " / "Moving " so we don't double-up
        return t
    # Filename fallback (e.g. "man-and-van-eastbourne.html" → "Man and Van Eastbourne")
    name = os.path.splitext(os.path.basename(path))[0]
    return ' '.join(w.capitalize() for w in name.replace('-', ' ').split())


# --- Rewrite templates ---
# Each entry: lowercase-normalised H2 → callable(topic) → new H2.
# Only patterns with ≥2 occurrences across the site need handling,
# but we cover the long tail too so a single run resolves everything.
def rw(s: str): return lambda t: s.format(topic=t)

REWRITES: dict[str, callable] = {
    'frequently asked questions':                                       rw('Frequently asked about {topic}'),
    'frequently asked questions about your move':                       rw('Frequently asked about {topic}'),
    'related pages on our site':                                        rw('More on {topic}'),
    'related pages':                                                    rw('More on {topic}'),
    'ready to book your move?':                                         rw('Ready to plan your {topic}?'),
    'why customers choose mark ratcliffe moving for sussex moves':      rw('Why customers choose us for {topic}'),
    'reviews and how to book':                                          rw('Reviews and how to book your {topic}'),
    'useful resources for your move':                                   rw('Useful resources for your {topic}'),
    'how can we help you today?':                                       rw('How we can help with {topic}'),
    'useful reading from our blog':                                     rw('Reading to support your {topic}'),
    'how to book your move with us':                                    rw('How to book your {topic} with us'),
    'a final thought':                                                  rw('A final thought on {topic}'),
    'six reasons our customers come back and recommend us':             rw('Six reasons our {topic} customers come back'),
    'six reasons our customers come back — and recommend us':           rw('Six reasons our {topic} customers come back'),
    'worth adding':                                                     rw('Worth adding to your {topic}'),
    'useful links':                                                     rw('Useful links for {topic}'),
    'how we protect your possessions':                                  rw('How we protect your possessions on {topic}'),
    'one last thought':                                                 rw('One last thought on {topic}'),
    'what sets us apart from generic national movers':                  rw('What sets us apart on {topic}'),
    'what to expect on move day with us':                               rw('What to expect on a {topic} move day'),
    'one last point':                                                   rw('One last point on {topic}'),
    'the full pad-wrap process in three steps':                         rw('The pad-wrap process for your {topic}'),
    'the full pad-wrap process — in three steps':                       rw('The pad-wrap process for your {topic}'),
    'other counties we cover':                                          rw('Other counties we cover from {topic}'),
    'keep reading':                                                     rw('Keep reading on {topic}'),
    'talk to a real human about your move':                             rw('Talk to a real human about your {topic}'),
    'rated 4.9 out of 5 — from 120+ independent reviews':               rw('What {topic} customers say'),
    'from a single room to a four-bedroom international relocation':    rw('Service range for your {topic}'),
    'every accreditation a real, externally-audited body':              rw('Accreditations behind your {topic}'),
}


def first_pass(pages: list[str], h1_for: dict[str, str]) -> dict[str, list[tuple[int, int, str]]]:
    """Return per-page list of (h2_start, h2_end, new_h2_text) edits.

    Only edits H2s in the body window (skips nav/footer)."""
    edits: dict[str, list[tuple[int, int, str]]] = defaultdict(list)

    # First, find all duplicates as they currently exist.
    h2_to_pages: dict[str, set[str]] = defaultdict(set)
    for p in pages:
        html = open(p, encoding='utf-8').read()
        s, e = body_window(html)
        for m in H2_RE.finditer(html[s:e]):
            text = clean(m.group(2)).lower()
            if text:
                h2_to_pages[text].add(p)
    dup_texts = {t for t, ps in h2_to_pages.items() if len(ps) > 1}

    # Now plan rewrites — for each page, for each H2 whose normalised
    # text is in dup_texts, generate a new unique text.
    candidate_h2: dict[str, set[str]] = defaultdict(set)
    for p in pages:
        html = open(p, encoding='utf-8').read()
        s, e = body_window(html)
        topic = topic_for(p, h1_for.get(p, ''))
        for m in H2_RE.finditer(html[s:e]):
            text = clean(m.group(2))
            norm = text.lower()
            if norm not in dup_texts:
                continue
            tmpl = REWRITES.get(norm)
            if tmpl is None:
                # Fallback: append the page topic.
                new_text = f'{text} — {topic}'
            else:
                new_text = tmpl(topic)
            # Collision check — keep stepping until unique across the site.
            attempt = new_text
            counter = 2
            while attempt.lower() in candidate_h2 and p not in candidate_h2[attempt.lower()]:
                attempt = f'{new_text} ({counter})'
                counter += 1
            candidate_h2[attempt.lower()].add(p)
            abs_start = s + m.start()
            abs_end = s + m.end()
            edits[p].append((abs_start, abs_end, m.group(1) + attempt + m.group(3)))

    return edits


def apply_edits(path: str, edits: list[tuple[int, int, str]]) -> bool:
    if not edits:
        return False
    html = open(path, encoding='utf-8').read()
    # Apply in reverse so earlier offsets stay valid.
    for start, end, replacement in sorted(edits, key=lambda x: -x[0]):
        html = html[:start] + replacement + html[end:]
    open(path, 'w', encoding='utf-8').write(html)
    return True


def main() -> int:
    pages = []
    for pat in ('*.html', 'areas-covered/*.html', 'services/*.html', 'resources/*.html', 'blog/*.html'):
        for p in glob.glob(pat):
            if os.path.basename(p) == '404.html': continue
            if os.path.basename(p).startswith('google'): continue
            head = open(p, encoding='utf-8').read(4096)
            m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', head, re.I)
            if m and 'noindex' in m.group(1).lower(): continue
            pages.append(p)

    h1_for = {p: extract_h1(open(p, encoding='utf-8').read()) for p in pages}

    edits = first_pass(pages, h1_for)
    pages_changed = 0
    h2s_rewritten = 0
    for p, e in edits.items():
        if apply_edits(p, e):
            pages_changed += 1
            h2s_rewritten += len(e)

    print(f'  pages with H2 rewrites: {pages_changed}')
    print(f'  H2s rewritten total:    {h2s_rewritten}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
