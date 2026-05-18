#!/usr/bin/env python3
"""Inject the new mobile-menu lead-gen block AND the floating mobile action bar
into every functional HTML page.

Idempotent — running again replaces any existing block.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

# Block that sits INSIDE the .nav-menu (visible only on mobile via CSS)
MOB_MENU_CTA = '''        <div class="mob-menu-cta" aria-label="Quick contact">
          <div class="mob-menu-cta__trust">
            <span><span class="star">★★★★★</span> 4.9 rating</span>
            <span>BAR registered</span>
            <span>Since 1982</span>
          </div>
          <a class="mob-menu-cta__phone" href="tel:01323848008">
            <small>CALL NOW · FREE QUOTE</small>
            01323 848 008
          </a>
          <a class="mob-menu-cta__quote" href="{P}mark-ratcliffe-moving-online-removals-quote.html">
            Get a Free Online Quote &rarr;
          </a>
          <form class="mob-menu-cta__form" action="{P}mark-ratcliffe-moving-online-removals-quote.html" method="get">
            <div class="mob-menu-cta__form-title">Or get a quick callback &mdash; 60 seconds</div>
            <input type="text" name="name" placeholder="Your name" required>
            <input type="tel" name="phone" placeholder="Your phone number" required>
            <input type="text" name="postcode" placeholder="Moving from (postcode)">
            <button type="submit">Request my callback</button>
          </form>
        </div>
'''

MOB_MENU_FOOT = '''        <div class="mob-menu-foot">
          <a href="mailto:mark@markratcliffemoving.co.uk">mark@markratcliffemoving.co.uk</a><br>
          Lower Dicker · Hailsham · East Sussex · BN27 4BU
          <strong>40+ years moving Sussex families</strong>
        </div>
'''

# Floating action bar pinned to the bottom of the viewport on mobile.
# Lives outside the nav so it shows regardless of whether the menu is open.
MOB_ACTION_BAR = '''  <div class="mob-action-bar" role="navigation" aria-label="Mobile contact bar">
    <a href="tel:01323848008" class="is-primary">
      <svg viewBox="0 0 24 24"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57a1 1 0 0 0-1.02.24l-2.2 2.2a15.05 15.05 0 0 1-6.59-6.59l2.2-2.2a1 1 0 0 0 .25-1.02A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1Z"/></svg>
      Call
    </a>
    <a href="sms:01323848008?&body=Hi%20Mark%20Ratcliffe%20Moving%2C%20I%27d%20like%20a%20quote." >
      <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2Z"/></svg>
      Text
    </a>
    <a href="https://wa.me/447437414589?text=Hi%20Mark%20Ratcliffe%20Moving%2C%20I%27d%20like%20a%20removal%20quote." class="is-whatsapp" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24"><path d="M12 0a12 12 0 0 0-10.4 18l-1.6 6 6.2-1.6A12 12 0 1 0 12 0Zm6.9 17c-.3.8-1.7 1.5-2.4 1.6-.6.1-1.4.1-2.3-.2-.5-.2-1.2-.4-2-.8-3.5-1.5-5.8-5.1-6-5.3-.2-.2-1.4-1.9-1.4-3.6 0-1.7.9-2.5 1.2-2.9.3-.3.7-.4 1-.4h.6c.3 0 .6 0 .9.7.3.7 1 2.4 1.1 2.6.1.2.2.5 0 .7l-.4.6c-.2.3-.4.4-.6.6-.2.2-.4.4-.2.7.2.3 1 1.6 2 2.5 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1.2-.2.8-1 1-1.3.3-.3.5-.3.8-.2.3.1 2 .9 2.3 1.1.3.2.5.2.6.4.1.2.1.9-.2 1.7Z"/></svg>
      WhatsApp
    </a>
    <a href="{P}mark-ratcliffe-moving-online-removals-quote.html">
      <svg viewBox="0 0 24 24"><path d="M5 4h14c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2Zm0 4 7 4 7-4V6l-7 4-7-4v2Z"/></svg>
      Quote
    </a>
  </div>
'''


CTA_RE = re.compile(r'<div class="mob-menu-cta".*?</div>\s*(?=<div class="mob-menu-foot"|<div class="menu-button|</nav>)', re.S)
FOOT_RE = re.compile(r'<div class="mob-menu-foot".*?</div>\s*(?=<div class="menu-button|</nav>)', re.S)
BAR_RE = re.compile(r'<div class="mob-action-bar".*?</div>\s*(?=<script|</body>)', re.S)


def get_prefix(fp: Path) -> str:
    rel = fp.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""


def process(fp: Path) -> bool:
    text = fp.read_text(encoding="utf-8")
    # Skip redirect stubs
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False

    orig = text
    P = get_prefix(fp)
    mob_cta = MOB_MENU_CTA.replace("{P}", P)
    mob_foot = MOB_MENU_FOOT
    mob_bar = MOB_ACTION_BAR.replace("{P}", P)

    # 1) Remove any previous injections
    text = CTA_RE.sub('', text)
    text = FOOT_RE.sub('', text)
    text = BAR_RE.sub('', text)

    # 2) Insert mob-menu-cta + mob-menu-foot inside the .nav-menu just after opening tag
    # Pattern: <nav role="navigation" class="nav-menu w-nav-menu">
    nav_open = re.search(r'<nav role="navigation" class="nav-menu w-nav-menu">', text)
    if nav_open:
        idx = nav_open.end()
        text = text[:idx] + "\n" + mob_cta + text[idx:]
        # Insert mob-menu-foot before </nav>...menu-button
        text = re.sub(
            r'(\s*)</nav>\s*<div class="menu-button',
            f'\\1{mob_foot}      </nav>\n      <div class="menu-button',
            text, count=1
        )

    # 3) Insert mob-action-bar before </body>
    if '<div class="mob-action-bar"' not in text:
        text = text.replace('</body>', mob_bar + '</body>', 1)

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
    print(f"Updated mobile menu on {n} pages.")


if __name__ == "__main__":
    main()
