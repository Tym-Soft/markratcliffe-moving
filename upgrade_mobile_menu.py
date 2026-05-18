#!/usr/bin/env python3
"""Upgrade the mobile menu with more advanced lead-gen elements:
  - Promotional banner at the very top
  - Live availability indicator
  - 3 service tiles (one-tap entry)
  - Postcode quick-search
  - Customer testimonial card
Idempotent — re-runs replace existing blocks.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"


def P_for(fp):
    rel = fp.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""


def build_blocks(P):
    promo = '<div class="mob-menu-promo">🎁 <strong>Free pad-wrap protection</strong> &middot; included on every move</div>'

    availability = '<div class="mob-menu-availability">We&rsquo;re online now &middot; quotes within 60 minutes</div>'

    tiles = f'''        <div class="mob-menu-tiles">
          <a class="mob-menu-tile" href="{P}removals-eastbourne.html">
            <svg viewBox="0 0 24 24"><path d="M3 17h2v-7h12v7h2V8L12 3 3 8Zm6 0v-4h6v4Z"/></svg>
            House Removals
          </a>
          <a class="mob-menu-tile" href="{P}storage-eastbourne.html">
            <svg viewBox="0 0 24 24"><path d="M3 4h18v6H3Zm0 8h18v8H3Zm2 2v4h4v-4Z"/></svg>
            Secure Storage
          </a>
          <a class="mob-menu-tile" href="{P}international-removals-eastbourne.html">
            <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 0 1-7.7-6h2.6a6 6 0 0 0 5.1 4Zm-6-8c0-.34 0-.67.08-1H4.34A7.5 7.5 0 0 0 4 12a8 8 0 0 0 .34 2.2h1.8A6 6 0 0 1 6 12Zm5-8c1.66 0 3 1.34 3 3v.5h-2v-.5c0-.55-.45-1-1-1s-1 .45-1 1V7h2v2h-5V7h1V5.5c0-1.66 1.34-3 3-3Z"/></svg>
            International
          </a>
        </div>'''

    postcode = f'''        <div class="mob-menu-postcode">
          <label for="mob-pc">Get a quote for your postcode</label>
          <form class="pc-row" action="{P}mark-ratcliffe-moving-online-removals-quote.html" method="get">
            <input type="text" id="mob-pc" name="postcode" placeholder="e.g. BN21" maxlength="8" required>
            <button type="submit">Go</button>
          </form>
        </div>'''

    testimonial = '''        <div class="mob-menu-testimonial">
          <div class="stars">★★★★★</div>
          "From the survey to the final box being unpacked, the team handled our move with absolute care. Every piece of furniture was pad-wrapped &mdash; nothing arrived with a scratch."
          <cite>— S. Patel, Lewes (verified customer)</cite>
        </div>'''

    return promo, availability, tiles, postcode, testimonial


# Patterns to remove previously injected blocks (idempotency)
PATTERNS_TO_STRIP = [
    re.compile(r'<div class="mob-menu-promo">.*?</div>\s*', re.S),
    re.compile(r'<div class="mob-menu-availability">.*?</div>\s*', re.S),
    re.compile(r'<div class="mob-menu-tiles">.*?</div>\s*</div>\s*(?=<div class="mob-menu-)', re.S),
    re.compile(r'<div class="mob-menu-tiles">.*?</div>\s*', re.S),
    re.compile(r'<div class="mob-menu-postcode">.*?</div>\s*</div>\s*(?=<div class="mob-menu-)', re.S),
    re.compile(r'<div class="mob-menu-postcode">.*?</form>\s*</div>\s*', re.S),
    re.compile(r'<div class="mob-menu-testimonial">.*?</div>\s*', re.S),
]


def process(fp: Path) -> bool:
    text = fp.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False
    orig = text
    P = P_for(fp)

    # Strip previous instances
    for pat in PATTERNS_TO_STRIP:
        text = pat.sub('', text)

    promo, availability, tiles, postcode, testimonial = build_blocks(P)

    # Insert new blocks right before the mob-menu-cta block
    # Block order: promo → availability → tiles → postcode → testimonial → mob-menu-cta
    injection = (
        "        " + promo + "\n"
        "        " + availability + "\n"
        + tiles + "\n"
        + postcode + "\n"
        + testimonial + "\n"
    )

    # Find mob-menu-cta div and insert before it
    cta_idx = text.find('<div class="mob-menu-cta"')
    if cta_idx < 0:
        # Page may not have mob-menu-cta block — skip
        return False

    # Trim back to the start of the line/indentation
    line_start = text.rfind('\n', 0, cta_idx) + 1
    text = text[:line_start] + injection + text[line_start:]

    if text != orig:
        fp.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob("*.html"):
        try:
            if process(fp):
                n += 1
        except Exception as e:
            print(f"  ERR {fp.name}: {e}")
    print(f"Upgraded mobile menu on {n} pages.")


if __name__ == "__main__":
    main()
