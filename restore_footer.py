#!/usr/bin/env python3
"""Replace every page's footer with the unified professional footer
matching the original Webflow style. Includes:
  - Map at top
  - 4-column layout (Contact / Find Us / Follow Us / Web Details)
  - Prominent BAR Member No: placeholder
  - BAR badge widget (yoshki)
  - FHIO dispute resolution logo
  - Schema.org Product/AggregateRating block
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


def get_prefix(fp: Path) -> str:
    rel = fp.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""


def build_footer(P: str) -> str:
    return f'''  <div class="footer">
    <div class="footer-map-wrapper">
      <div class="footer-map">{MAP_IFRAME}</div>
    </div>
    <div class="_1200-wrapper">
      <div class="footer-neg w-clearfix">
        <div class="footer-a">
          <h4 class="white footer-title">Contact Us</h4>
          <div class="divider"></div>
          <div class="footer-info-wrap">
            <div class="info-icon-holder">
              <div><a href="tel:01323848008" class="footer-link">01323 848 008</a></div>
            </div>
          </div>
          <div class="footer-info-wrap">
            <div class="info-icon-holder _2">
              <div><a href="tel:07437414589" class="footer-link">07437 414 589</a></div>
            </div>
          </div>
          <div class="footer-info-wrap">
            <div class="info-icon-holder _2 _3">
              <div><a href="mailto:mark@markratcliffemoving.co.uk" class="footer-link">mark@markratcliffemoving.co.uk</a></div>
            </div>
          </div>
          <div class="footer-info-wrap">
            <div class="info-icon-holder _2 quote">
              <div><a href="{P}mark-ratcliffe-moving-online-removals-quote.html" class="footer-link">ONLINE QUOTE</a></div>
            </div>
          </div>
          <div class="footer-info-wrap">
            <div class="info-icon-holder _2 insurance">
              <div><a href="{P}terms-conditions-and-insurance-details.html" class="footer-link">TERMS, CONDITIONS &amp; INSURANCE</a></div>
            </div>
          </div>
        </div>

        <div class="footer-a b">
          <h4 class="white footer-title">Find Us</h4>
          <div class="divider"></div>
          <p class="white">Mark Ratcliffe Moving Ltd<br>Unit J12 Swallow Business Park<br>Diamond Drive, Lower Dicker<br>East Sussex BN27 4EL</p>
          <p class="white footer-bar-no"><strong>BAR Member No:</strong> [add your number]<br>
          <small>British Association of Removers Overseas Group</small></p>
          <div class="footer-accred-wrap">
            <div class="badge-image embed w-embed w-iframe"><iframe frameborder="0" scrolling="no" allowtransparency="true" width="220" height="86" src="https://yoshki.com/badge-bar.html" style="border:0px;margin:0px;padding:0px;backgroundColor:transparent;" title="Mark Ratcliffe Moving accreditation badges"></iframe></div>
          </div>
          <div class="footer-accred-row">
            <img src="{P}images/mark-BAR-in-frame.webp" width="60" height="65" alt="British Association of Removers member" loading="lazy">
            <img src="{P}images/bs-8564-2-removals-storage-accreditation.webp" width="60" height="98" alt="BS 8564-2 quality accreditation" loading="lazy">
            <img src="{P}images/apg-approved-payment-guarantee-uk-domestic.webp" width="65" height="77" alt="APG Approved Payment Guarantee" loading="lazy">
            <img src="{P}images/ima-international-movers-association-logo.webp" width="65" height="46" alt="International Movers Association" loading="lazy">
            <img src="{P}images/UK---Thai-Movers-Logo.webp" width="100" height="29" alt="UK to Thai Movers Group" loading="lazy">
          </div>
        </div>

        <div class="footer-a c">
          <h4 class="white footer-title">Follow Us</h4>
          <div class="divider"></div>
          <a href="https://www.facebook.com/mark.ratcliffe.10441" target="_blank" rel="noopener" class="w-inline-block"><img src="{P}images/facebook.svg" width="35" height="35" alt="Follow Mark Ratcliffe Moving on Facebook" class="hover-enlarge" decoding="async" loading="lazy"></a>
          <div>
            <a href="{P}areas-covered.html" class="button medium-margin-top w-button">Areas Covered</a>
          </div>
          <div class="fhio-wrap">
            <div>We adhere to the British Association of Removers Alternative Dispute Resolution Scheme which is independently operated by the:</div>
            <a href="http://www.fhio.org/" target="_blank" rel="noopener" class="w-inline-block"><img src="{P}images/FHIO-Logo-01.webp" width="300" height="100" loading="lazy" alt="Foundation of Independent Home Improvers (FHIO) accredited member" class="fhio-image"></a>
          </div>
        </div>

        <div class="footer-a d">
          <h4 class="white footer-title">Web Details</h4>
          <div class="divider"></div>
          <p class="white">&copy; EMV London Ltd t/a Mark Ratcliffe Moving <span class="current-year">2026</span></p>
          <p class="white"><small>Family-run · Established 1982 · Serving Sussex &amp; Surrey since 1982</small></p>
          <div class="white reviews w-embed">
            <div itemscope itemtype="https://schema.org/Product">
              <span itemprop="name">Mark Ratcliffe Moving &amp; Storage Ltd</span>
              <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
                Rated <span itemprop="ratingValue">4.9</span>/5 based on <span itemprop="reviewCount">120</span> reviews
              </div>
            </div>
          </div>
          <p class="white"><a href="{P}reviews.html" class="footer-link">Read our reviews →</a></p>
        </div>
      </div>
    </div>
  </div>
'''


# Match both footer types (original Webflow .footer and new np-footer)
WEBFLOW_FOOTER_RE = re.compile(
    r'<div class="footer">.*?</div>\s*</div>\s*</div>\s*(?=\s*<script|\s*<div id="fb-root"|\s*<div class="mob-action-bar"|\s*</body>)',
    re.S
)
NP_FOOTER_RE = re.compile(r'<footer class="np-footer">.*?</footer>', re.S)
# Also catch any np-cta-block that might be immediately above (we'll keep CTA on new pages by not removing it)


def process(fp: Path) -> bool:
    text = fp.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False
    orig = text
    P = get_prefix(fp)

    # Remove either footer
    text = NP_FOOTER_RE.sub('', text)
    text = WEBFLOW_FOOTER_RE.sub('', text)

    # Insert the unified footer before </body> (or before mob-action-bar / scripts)
    new_footer = build_footer(P)

    # Find earliest closing anchor: mob-action-bar, scripts at end, or </body>
    insertion = re.search(r'\s*(<div class="mob-action-bar"|<div id="fb-root"|<script[^>]*src="https://d3e54v103j8qbb)', text)
    if insertion:
        idx = insertion.start()
        text = text[:idx] + "\n" + new_footer + text[idx:]
    else:
        text = text.replace('</body>', new_footer + '\n</body>', 1)

    # Ensure current-year script is present (sets the year span dynamically)
    if 'current-year' in new_footer and 'querySelector(\'.current-year\')' not in text:
        yr_script = """  <script>document.addEventListener('DOMContentLoaded',function(){var s=document.querySelector('.current-year');if(s)s.textContent=new Date().getFullYear();});</script>
"""
        text = text.replace('</body>', yr_script + '</body>', 1)

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
    print(f"Unified professional footer applied to {n} pages.")


if __name__ == "__main__":
    main()
