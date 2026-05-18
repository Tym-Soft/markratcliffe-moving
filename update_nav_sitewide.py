#!/usr/bin/env python3
"""Replace the existing nav block in every original HTML page with the unified new nav."""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

# Same NAV body as in template.py — but allow nav-section wrapper to be optional in originals
NEW_NAV_INNER = '''    <div class="top-bar-wrapper w-hidden-small w-hidden-tiny">
      <div class="contacts-in-top-wrapper">
        <a href="tel:01323848008" class="tb-link w-inline-block"><div>01323 848 008</div></a>
        <a href="tel:07437414589" class="tb-link mob w-inline-block"><div>07437 414 589</div></a>
        <a href="mailto:mark@markratcliffemoving.co.uk" class="tb-link email w-inline-block"><div>mark@markratcliffemoving.co.uk</div></a>
      </div>
      <div class="banner-script">A member of the British Association of Removers Overseas Group</div>
      <a href="{P}mark-ratcliffe-moving-online-removals-quote.html" class="top-bar-quote">REQUEST A QUOTE</a>
    </div>
    <div data-collapse="medium" data-animation="default" data-duration="400" data-easing="ease" data-easing2="ease" role="banner" class="navbar w-nav">
      <a href="{INDEX}" class="brand w-nav-brand"><img src="{IMG}Mark-Ratcliffe.svg" width="180" height="60" alt="Mark Ratcliffe Moving and Storage — Eastbourne removals company logo" class="logo-img" decoding="async" fetchpriority="high"></a>
      <nav role="navigation" class="nav-menu w-nav-menu">
        <a href="{INDEX}" class="navlink w-nav-link">HOME</a>
        <a href="{P}about-us.html" class="navlink w-nav-link">ABOUT US</a>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>OUR SERVICES</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="{P}removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Removals Eastbourne</a>
            <a href="{P}man-and-van-eastbourne.html" class="dropdown-navlink w-dropdown-link">Man &amp; Van</a>
            <a href="{P}packing-services-eastbourne.html" class="dropdown-navlink w-dropdown-link">Packing Services</a>
            <a href="{P}office-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Office Removals</a>
            <a href="{P}house-clearance-eastbourne.html" class="dropdown-navlink w-dropdown-link">House Clearance</a>
            <a href="{P}international-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">International Removals</a>
            <a href="{P}european-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">European Removals</a>
          </nav>
        </div>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>AREAS COVERED</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="{P}removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Eastbourne</a>
            <a href="{P}hailsham-removals.html" class="dropdown-navlink w-dropdown-link">Hailsham</a>
            <a href="{P}removals-polegate.html" class="dropdown-navlink w-dropdown-link">Polegate</a>
            <a href="{P}removals-pevensey.html" class="dropdown-navlink w-dropdown-link">Pevensey</a>
            <a href="{P}removals-willingdon.html" class="dropdown-navlink w-dropdown-link">Willingdon</a>
            <a href="{P}removals-uckfield.html" class="dropdown-navlink w-dropdown-link">Uckfield</a>
            <a href="{P}removals-heathfield.html" class="dropdown-navlink w-dropdown-link">Heathfield</a>
            <a href="{P}removals-bexhill.html" class="dropdown-navlink w-dropdown-link">Bexhill</a>
            <a href="{P}areas-covered.html" class="dropdown-navlink w-dropdown-link">All Areas &rarr;</a>
          </nav>
        </div>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>RESOURCES</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="{P}moving-checklist-eastbourne.html" class="dropdown-navlink w-dropdown-link">Moving Checklist</a>
            <a href="{P}removals-eastbourne-cost.html" class="dropdown-navlink w-dropdown-link">Cost Guide</a>
            <a href="{P}faqs.html" class="dropdown-navlink w-dropdown-link">FAQs</a>
            <a href="{P}blog/index.html" class="dropdown-navlink w-dropdown-link">Blog</a>
          </nav>
        </div>
        <a href="{P}storage-eastbourne.html" class="navlink w-nav-link">SELF STORAGE</a>
        <a href="{P}thai-moving-services.html" class="navlink w-nav-link">UK - THAI</a>
        <a href="{P}reviews.html" class="navlink w-nav-link">REVIEWS</a>
        <a href="{P}contact-us.html" class="navlink w-nav-link">CONTACT</a>
      </nav>
      <div class="menu-button w-nav-button"><div class="w-icon-nav-menu"></div></div>
    </div>'''


def get_path_prefix(filepath: Path) -> tuple:
    """Returns (P, INDEX, IMG): path prefix for subdirectory pages."""
    rel = filepath.relative_to(ROOT)
    if len(rel.parts) > 1:
        return ("../", "../index.html", "../images/")
    return ("", "index.html", "images/")


# Pattern: match the existing top-bar-wrapper through closing of navbar's containing div
# In the originals there's <div class="nav-section"> wrapping these — but the inside is two divs:
#   top-bar-wrapper + navbar
# We'll match from <div class="top-bar-wrapper... to closing </div> of the navbar block.
NAV_PATTERN = re.compile(
    r'<div class="top-bar-wrapper[^>]*>.*?<div class="menu-button w-nav-button">.*?</div>\s*</div>\s*</div>',
    re.S
)


def update_file(fp: Path) -> bool:
    text = fp.read_text(encoding="utf-8")
    P, INDEX, IMG = get_path_prefix(fp)
    new_nav = NEW_NAV_INNER.replace("{P}", P).replace("{INDEX}", INDEX).replace("{IMG}", IMG)
    # The new nav doesn't include the outer closing div of nav-section, so end the replacement before the final </div>
    # Match the chunk that runs from top-bar-wrapper through navbar's closing div pair
    pattern = re.compile(
        r'<div class="top-bar-wrapper[^"]*"[^>]*>.*?<nav role="navigation"[^>]*class="nav-menu w-nav-menu">.*?</nav>\s*<div class="menu-button w-nav-button">\s*<div class="w-icon-nav-menu"></div>\s*</div>\s*</div>',
        re.S
    )
    new_text, n = pattern.subn(new_nav, text, count=1)
    if n > 0:
        fp.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    files = (list(ROOT.glob("*.html"))
             + list((ROOT / "areas-covered").glob("*.html"))
             + list((ROOT / "blog").glob("*.html")))
    updated = 0
    skipped = []
    for fp in files:
        try:
            if update_file(fp):
                updated += 1
            else:
                skipped.append(fp.name)
        except Exception as e:
            print(f"  ERR on {fp.name}: {e}")
    print(f"Updated nav in {updated} files. Skipped (no match): {len(skipped)}")
    if skipped:
        for s in skipped[:5]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
