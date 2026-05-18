#!/usr/bin/env python3
"""Symmetrical, mobile-friendly footer with every page linked.
 Layout: Map full-width on top, then a 4-column grid (Services, Areas Covered, Resources, Contact),
 then a full-width accreditation row, then the copyright/colophon row.
 Mobile: stacks to single column with map at top.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

MAP_IFRAME = ('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2523.049709930351'
              '!2d0.29392331613135825!3d50.77465207183167!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1'
              '!3m3!1m2!1s0x47df7392bfec7151%3A0xf536886de6399c2e!2sMark+Ratcliffe+Moving+%26+Storage+Ltd'
              '!5e0!3m2!1sen!2suk!4v1549285879259" '
              'width="100%" height="100%" frameborder="0" style="border:0" allowfullscreen="" loading="lazy" '
              'title="Mark Ratcliffe Moving &amp; Storage Ltd — Lower Dicker location map"></iframe>')


def P_for(fp):
    rel = fp.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""


def build_footer(P):
    return f'''  <footer class="mr-footer" role="contentinfo">
    <div class="mr-footer-map">{MAP_IFRAME}</div>

    <div class="mr-footer-inner">
      <div class="mr-footer-grid">

        <div class="mr-footer-col">
          <h4 class="mr-footer-title">Services</h4>
          <ul class="mr-footer-list">
            <li><a href="{P}removals-eastbourne.html">Removals Eastbourne</a></li>
            <li><a href="{P}man-and-van-eastbourne.html">Man &amp; Van</a></li>
            <li><a href="{P}packing-services-eastbourne.html">Packing Services</a></li>
            <li><a href="{P}storage-eastbourne.html">Self Storage</a></li>
            <li><a href="{P}office-removals-eastbourne.html">Office Removals</a></li>
            <li><a href="{P}house-clearance-eastbourne.html">House Clearance</a></li>
            <li><a href="{P}international-removals-eastbourne.html">International Removals</a></li>
            <li><a href="{P}european-removals-eastbourne.html">European Removals</a></li>
            <li><a href="{P}thai-moving-services.html">UK – Thai Removals</a></li>
            <li><a href="{P}packaging-shop.html">Packaging Shop</a></li>
          </ul>
        </div>

        <div class="mr-footer-col">
          <h4 class="mr-footer-title">Areas Covered</h4>
          <ul class="mr-footer-list">
            <li><a href="{P}removals-eastbourne.html">Eastbourne</a></li>
            <li><a href="{P}hailsham-removals.html">Hailsham</a></li>
            <li><a href="{P}removals-polegate.html">Polegate</a></li>
            <li><a href="{P}removals-pevensey.html">Pevensey</a></li>
            <li><a href="{P}removals-willingdon.html">Willingdon</a></li>
            <li><a href="{P}removals-uckfield.html">Uckfield</a></li>
            <li><a href="{P}removals-heathfield.html">Heathfield</a></li>
            <li><a href="{P}removals-bexhill.html">Bexhill</a></li>
            <li><a href="{P}areas-covered.html"><strong>All Areas →</strong></a></li>
          </ul>
        </div>

        <div class="mr-footer-col">
          <h4 class="mr-footer-title">Resources</h4>
          <ul class="mr-footer-list">
            <li><a href="{P}moving-checklist-eastbourne.html">Moving Checklist</a></li>
            <li><a href="{P}removals-eastbourne-cost.html">Cost Guide</a></li>
            <li><a href="{P}faqs.html">FAQs</a></li>
            <li><a href="{P}blog/index.html">Blog</a></li>
            <li><a href="{P}reviews.html">Reviews</a></li>
            <li><a href="{P}about-us.html">About Us</a></li>
            <li><a href="{P}careers.html">Careers</a></li>
            <li><a href="{P}contact-us.html">Contact</a></li>
            <li><a href="{P}terms-conditions-and-insurance-details.html">Terms &amp; Insurance</a></li>
            <li><a href="{P}mark-ratcliffe-moving-online-removals-quote.html">Get a Quote</a></li>
          </ul>
        </div>

        <div class="mr-footer-col">
          <h4 class="mr-footer-title">Contact &amp; Visit</h4>
          <ul class="mr-footer-list mr-footer-contact">
            <li><a href="tel:01323848008">📞 01323 848 008</a></li>
            <li><a href="tel:07437414589">📱 07437 414 589</a></li>
            <li><a href="mailto:mark@markratcliffemoving.co.uk">✉ mark@markratcliffemoving.co.uk</a></li>
            <li>
              <strong>Mark Ratcliffe Moving Ltd</strong><br>
              Unit J12 Swallow Business Park<br>
              Diamond Drive, Lower Dicker<br>
              East Sussex BN27 4EL
            </li>
          </ul>
          <div class="mr-footer-bar">
            <strong>BAR Member No:</strong> [add your number]<br>
            <small>British Association of Removers Overseas Group</small>
          </div>
          <a class="mr-footer-social" href="https://www.facebook.com/mark.ratcliffe.10441" target="_blank" rel="noopener" aria-label="Follow us on Facebook">
            <img src="{P}images/facebook.svg" width="32" height="32" alt="Facebook" loading="lazy">
          </a>
        </div>

      </div>

      <div class="mr-footer-accred">
        <img src="{P}images/mark-BAR-in-frame.webp" width="70" height="76" alt="British Association of Removers member" loading="lazy">
        <img src="{P}images/bs-8564-2-removals-storage-accreditation.webp" width="70" height="115" alt="BS 8564 quality accreditation" loading="lazy">
        <img src="{P}images/apg-approved-payment-guarantee-uk-domestic.webp" width="75" height="89" alt="APG Approved Payment Guarantee" loading="lazy">
        <img src="{P}images/ima-international-movers-association-logo.webp" width="80" height="56" alt="International Movers Association" loading="lazy">
        <img src="{P}images/UK---Thai-Movers-Logo.webp" width="120" height="34" alt="UK to Thai Movers Group" loading="lazy">
        <img src="{P}images/FHIO-Logo-01.webp" width="120" height="40" alt="FHIO accredited member" loading="lazy">
      </div>

      <div class="mr-footer-bottom">
        <p>&copy; EMV London Ltd t/a Mark Ratcliffe Moving &amp; Storage <span class="current-year">2026</span> &middot; Family-run since 1982 &middot; <a href="{P}terms-conditions-and-insurance-details.html">Terms &amp; Insurance</a></p>
        <p class="mr-footer-rating" itemscope itemtype="https://schema.org/Product">
          <span itemprop="name">Mark Ratcliffe Moving &amp; Storage Ltd</span> –
          <span itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
            rated <span itemprop="ratingValue">4.9</span>/5 from <span itemprop="reviewCount">120</span> reviews
          </span>
        </p>
      </div>
    </div>
  </footer>
'''


# Patterns matching the previous Webflow footer, np-footer, and the .footer wrapper variant
OLD_FOOTERS = [
    re.compile(r'<footer class="np-footer">.*?</footer>', re.S),
    re.compile(r'<footer class="mr-footer"[^>]*>.*?</footer>', re.S),  # idempotency
    re.compile(r'<div class="footer">.*?</div>\s*</div>\s*</div>', re.S),
]


def process(fp: Path) -> bool:
    text = fp.read_text(encoding='utf-8')
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False
    orig = text
    P = P_for(fp)

    # Remove any existing footer block
    for pat in OLD_FOOTERS:
        text = pat.sub('', text, count=1)

    # Insert new footer just before </body> (or before any final scripts already there)
    new_footer = build_footer(P)
    # Inject before scripts (jquery / mark-ratcliffe-moving.js) if present near end
    m = re.search(r'\s*<script[^>]*src="https://d3e54v103j8qbb', text)
    if m:
        idx = m.start()
        text = text[:idx] + "\n" + new_footer + text[idx:]
    elif '</body>' in text:
        text = text.replace('</body>', new_footer + '\n</body>', 1)

    # Ensure current-year auto-updates
    if 'current-year' in new_footer and "querySelector('.current-year')" not in text:
        yr = """  <script>document.addEventListener('DOMContentLoaded',function(){var s=document.querySelector('.current-year');if(s)s.textContent=new Date().getFullYear();});</script>
"""
        text = text.replace('</body>', yr + '</body>', 1)

    if text != orig:
        fp.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob('*.html'):
        try:
            if process(fp):
                n += 1
        except Exception as e:
            print(f'  ERR {fp.name}: {e}')
    print(f'Symmetrical footer applied to {n} pages.')


if __name__ == '__main__':
    main()
