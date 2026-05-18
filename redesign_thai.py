#!/usr/bin/env python3
"""Redesign thai-moving-services.html — remove parallax backgrounds, clean layout."""
from pathlib import Path

FP = Path(__file__).parent / "www.markratcliffemoving.co.uk" / "thai-moving-services.html"


NEW_BODY = '''
  <!-- Hero -->
  <section class="th-hero">
    <div class="th-hero-pattern" aria-hidden="true"></div>
    <div class="th-hero-inner">
      <div class="th-hero-flags">
        <img src="images/UK-Thai.webp" loading="eager" width="235" height="178" alt="UK and Thailand flags" class="th-flags-img">
      </div>
      <p class="th-eyebrow">UK ↔ Thailand specialists</p>
      <h1>Welcome to Mark Ratcliffe UK - Thai Movers<strong> </strong></h1>
      <p class="th-hero-sub">Specialist door-to-door moving service between the UK and Thailand. Over 20 years on this route, more than 40 years moving overseas — and our own crews on both sides of the journey.</p>
      <div class="th-hero-cta">
        <a class="th-btn-primary" href="mark-ratcliffe-moving-online-removals-quote.html">Get a Free Quote</a>
        <a class="th-btn-ghost" href="tel:01323848008">Call 01323 848 008</a>
      </div>
    </div>
  </section>

  <!-- Trust stats strip -->
  <section class="th-stats">
    <div class="th-stats-inner">
      <div class="th-stat"><strong>40+</strong><span>Years moving overseas</span></div>
      <div class="th-stat"><strong>20+</strong><span>Years on UK ↔ Thailand</span></div>
      <div class="th-stat"><strong>BAR</strong><span>Overseas Group member</span></div>
      <div class="th-stat"><strong>200+</strong><span>Worldwide destinations</span></div>
    </div>
  </section>

  <!-- Intro: editorial body + accreditation aside -->
  <section class="th-section th-section-light">
    <div class="th-grid">
      <article class="th-prose">
        <p class="th-prose-lead">For hundreds of years, man&#x27;s quest to travel the globe in search of a better life overseas has been commonplace the world over. In the late 60&#x27;s and early 70&#x27;s containerisation was introduced to the global world of shipping, making a much more streamlined, faster and cost effective way to move commodities around the world. This boosted the household goods shipping and forwarding industry and significantly increased volumes of home Moves worldwide.</p>
        <p>Over the last few years, Thailand has become one of the most popular destinations for expatriation from the UK and household goods shipments continue to increase, which in turn helps to reduce shipping rates and makes moving household goods to Thailand much more economically viable than in previous years.</p>
        <p class="th-callout"><strong>If you&#x27;re considering a Move to Thailand, have household goods / personal effects to ship, then you&#x27;ve landed on the right page.</strong></p>
      </article>
      <aside class="th-aside">
        <p class="th-aside-eyebrow">Quality &amp; standards</p>
        <div class="th-badges-grid">
          <img src="images/BS-8564.webp" alt="BS 8564 quality accreditation" width="120" height="196" loading="lazy">
          <img src="images/OG-Large-Logo-Col-1-1.webp" alt="Quality service standards" width="120" height="156" loading="lazy">
        </div>
        <p class="th-aside-note">Independently inspected to BAR &amp; BS 8564 service standards. We hold our overseas moves to the same quality bar as a Sussex house removal.</p>
        <img src="images/MRM-Thai-Movers.webp" width="220" height="65" alt="Mark Ratcliffe UK to Thai Movers" loading="lazy" class="th-aside-brand">
      </aside>
    </div>
  </section>

  <!-- Service detail — door to door -->
  <section class="th-section">
    <div class="th-narrow">
      <p class="th-eyebrow-dark">Door-to-door service</p>
      <h2>We can uplift your furniture and effects from anywhere in the UK and deliver to your door anywhere in Thailand, with Full Destination Services. </h2>
      <p>Mark Ratcliffe Moving have been specialist overseas movers for over 40 years, specialising in Moves to Thailand for more than 20 years.</p>
      <p>From a single box or two, to a full house contents - Baggage shipments for students returning home, expats who are seeking a better life overseas and Thai Nationals who are sending goods home to their families, we regular travel the UK packing / wrapping and listing goods which are bound for a warmer climate. </p>
    </div>
  </section>

  <!-- Process strip (replaces the parallax sections with something useful) -->
  <section class="th-process-strip">
    <div class="th-narrow">
      <p class="th-eyebrow">How it works</p>
      <h2>From your UK doorstep to your Thai address</h2>
    </div>
    <div class="th-process-row">
      <div class="th-process-step">
        <div class="th-step-num">01</div>
        <h3>Free survey &amp; quote</h3>
        <p>In-home or video. We measure the volume, agree what is shipping, and itemise everything in a written, no-obligation quote.</p>
      </div>
      <div class="th-process-step">
        <div class="th-step-num">02</div>
        <h3>Export packing &amp; uplift</h3>
        <p>Our crew comes to your UK address, professionally export-packs every item, lists each piece, and loads everything onto our vehicle.</p>
      </div>
      <div class="th-process-step">
        <div class="th-step-num">03</div>
        <h3>Container &amp; shipping</h3>
        <p>Your goods are loaded into a 20ft or 40ft groupage container and shipped to our partner agent's depot in Bangkok.</p>
      </div>
      <div class="th-process-step">
        <div class="th-step-num">04</div>
        <h3>Door delivery in Thailand</h3>
        <p>Customs cleared, delivered to your Thai address, unpacked and set up in your new home with our trusted Bangkok crew.</p>
      </div>
    </div>
  </section>

  <!-- Brochure -->
  <section class="th-section th-section-light">
    <div class="th-narrow">
      <p class="th-eyebrow-dark">Information</p>
      <h2>Brochure.</h2>
      <p>Please read through our brochure below for overseas moving tips and an insight into how the procedure works and could work for you.</p>
    </div>
  </section>

  <!-- Nopi case study — editorial feature -->
  <section class="th-section">
    <div class="th-wide">
      <header class="th-case-header">
        <p class="th-eyebrow-dark">Case study · 2023</p>
        <h2>Nopi&#x27;s story.</h2>
        <p class="th-case-sub">A pre-move survey four years before completion — and a personal Bangkok doorstep handover.</p>
      </header>

      <figure class="th-feature-image">
        <img src="images/20231215_095019.webp" width="1920" height="1440"
             alt="Nopi's furniture and belongings precisely and carefully export wrapped and safely arrived in Thailand"
             sizes="(max-width: 1100px) 100vw, 1100px"
             srcset="images/20231215_095019-p-500.webp 500w, images/20231215_095019-p-800.webp 800w, images/20231215_095019-p-1080.webp 1080w, images/20231215_095019.webp 1920w"
             loading="lazy">
        <figcaption>Nopi&#x27;s furniture and belongings precisely and carefully export wrapped and safely arrived in Thailand.</figcaption>
      </figure>

      <div class="th-case-body">
        <figure class="th-side-image">
          <img src="images/Brochure-pic-.webp" width="600" height="405" alt="Mark and the United Relocations team" loading="lazy">
          <figcaption>Mark and the United Relocations team.</figcaption>
        </figure>
        <p>This move was for Nopi, a Thai National from Hailsham, I first went to see Nopi 4 years earlier to carry out a pre-move survey and following this we could then quote for Nopi&#x27;s Move back to her mother country.</p>
        <p>Following our updated quote, Nopi booked her move with us and after export wrapping her personal effects and furniture pieces under Nopi&#x27;s supervision of course, her household goods were loaded into a 40ft groupage container and arrived at our agents depot in Bangkok December 2023. It just so happened I was visiting our Bangkok agent at the time of Nopi&#x27;s delivery just a few miles away. Wanting to offer our valued customer a personal service, I jumped in the truck with our agents crew and decided to pay Nopi a surprise visit by unloading, unpacking and setting up with our Bangkok crew.</p>
        <p>Big shock and screams as Nopi opened the door to see me holding the first box off the truck of United Relocations (Thailand) Co. Ltd&#x27;s Moving truck!</p>
      </div>

      <figure class="th-feature-image">
        <img src="images/20231214_155942.webp" width="1920" height="1440"
             alt="Mark with the team after surprising Nopi"
             sizes="(max-width: 1100px) 100vw, 1100px"
             srcset="images/20231214_155942-p-500.webp 500w, images/20231214_155942-p-800.webp 800w, images/20231214_155942-p-1080.webp 1080w, images/20231214_155942.webp 1920w"
             loading="lazy">
        <figcaption>Mark with the team after surprising Nopi!</figcaption>
      </figure>

      <div class="th-pair">
        <figure>
          <img src="images/IMG_9796.webp" width="1924" height="2000" alt="The Bangkok delivery in progress" loading="lazy">
        </figure>
        <figure>
          <img src="images/IMG_7719.webp" width="1500" height="2000" alt="Nopi greets the team in Bangkok" loading="lazy">
        </figure>
      </div>
    </div>
  </section>

  <!-- Full Gallery placeholder -->
  <section class="th-section th-section-light">
    <div class="th-narrow">
      <p class="th-eyebrow-dark">Photo collection</p>
      <h2>Full Gallery.</h2>
    </div>
  </section>
'''


CSS = '''
  <style>
    /* === Thai moving services — clean editorial design === */

    /* Hero */
    .th-hero {
      position: relative; overflow: hidden;
      background: linear-gradient(135deg, #220b50 0%, #3a1a7a 60%, #1a0840 100%);
      color: #fff; padding: 5rem 1.5rem 4rem; text-align: center;
    }
    .th-hero-pattern {
      position: absolute; inset: 0; opacity: 0.06; pointer-events: none;
      background-image: radial-gradient(rgba(255,255,255,0.9) 1.2px, transparent 1.2px);
      background-size: 28px 28px;
    }
    .th-hero-inner { position: relative; max-width: 820px; margin: 0 auto; }
    .th-hero-flags { margin-bottom: 1rem; }
    .th-flags-img { display: inline-block; max-width: 140px; height: auto; }
    .th-eyebrow {
      color: #FFC107; font-size: 0.78rem; letter-spacing: 0.18em;
      text-transform: uppercase; font-weight: 700; margin: 0 0 0.6rem;
    }
    .th-eyebrow-dark { color: #d4af37; font-size: 0.75rem; letter-spacing: 0.18em;
      text-transform: uppercase; font-weight: 700; margin: 0 0 0.6rem; }
    .th-hero h1 {
      color: #fff !important; font-weight: 700 !important;
      font-size: clamp(1.85rem, 3.5vw, 2.75rem) !important;
      margin: 0 0 1.2rem !important; line-height: 1.18; letter-spacing: -0.01em;
    }
    .th-hero-sub {
      max-width: 660px; margin: 0 auto 2rem;
      color: rgba(255,255,255,0.88); font-size: 1.05rem; line-height: 1.6;
    }
    .th-hero-cta { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; }
    .th-btn-primary, .th-btn-ghost {
      display: inline-flex; align-items: center; padding: 0.95rem 1.85rem;
      border-radius: 999px; font-weight: 700; font-size: 0.92rem;
      text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;
      transition: transform .2s, box-shadow .2s, background .2s;
    }
    .th-btn-primary { background: #FFC107; color: #1a0840; box-shadow: 0 10px 30px -14px rgba(255,193,7,0.55); }
    .th-btn-primary:hover { background: #d4af37; transform: translateY(-2px); }
    .th-btn-ghost { background: rgba(255,255,255,0.08); color: #fff; border: 1.5px solid rgba(255,255,255,0.4); }
    .th-btn-ghost:hover { background: rgba(255,255,255,0.16); border-color: #fff; }

    /* Stats strip */
    .th-stats { background: #220b50; color: #fff; padding: 2rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.08); }
    .th-stats-inner {
      max-width: 1100px; margin: 0 auto;
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
      text-align: center;
    }
    @media (max-width: 700px) { .th-stats-inner { grid-template-columns: repeat(2, 1fr); gap: 1.5rem; } }
    .th-stat strong {
      display: block; color: #FFC107; font-weight: 800;
      font-size: clamp(1.5rem, 2.8vw, 2.1rem); line-height: 1;
    }
    .th-stat span {
      display: block; margin-top: 0.4rem;
      font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.08em;
      color: rgba(255,255,255,0.75);
    }

    /* Section base */
    .th-section { padding: 4rem 1.5rem; background: #fff; }
    .th-section-light { background: #f7f5fb; }
    .th-narrow { max-width: 760px; margin: 0 auto; }
    .th-wide   { max-width: 1100px; margin: 0 auto; }
    .th-section h2 {
      color: #220b50; font-size: clamp(1.5rem, 2.6vw, 2.1rem);
      font-weight: 700; margin: 0.4rem 0 1rem; letter-spacing: -0.01em; line-height: 1.25;
    }
    .th-section p {
      font-size: 1.05rem; line-height: 1.75; color: #1f1f1f; margin: 0 0 1rem;
    }

    /* Intro grid — body + aside */
    .th-grid {
      max-width: 1100px; margin: 0 auto;
      display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 3rem; align-items: start;
    }
    @media (max-width: 900px) { .th-grid { grid-template-columns: 1fr; gap: 2rem; } }
    .th-prose p { font-size: 1.05rem; line-height: 1.75; }
    .th-prose-lead { font-size: 1.12rem !important; line-height: 1.7 !important; color: #1f1f1f; }
    .th-callout {
      background: rgba(255,193,7,0.12); border-left: 3px solid #d4af37;
      padding: 1rem 1.2rem; border-radius: 4px; font-size: 1.05rem !important;
    }
    .th-aside {
      background: #fff; border: 1px solid #e0dceb; border-radius: 12px;
      padding: 1.5rem; text-align: center; position: sticky; top: 130px;
    }
    @media (max-width: 900px) { .th-aside { position: static; } }
    .th-aside-eyebrow {
      font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
      color: #220b50; font-weight: 700; margin: 0 0 1rem;
    }
    .th-badges-grid {
      display: flex; gap: 1rem; justify-content: center; align-items: center;
      margin-bottom: 0.85rem;
    }
    .th-badges-grid img { max-width: 80px; height: auto; }
    .th-aside-note { font-size: 0.85rem; color: #5a5a6a; line-height: 1.55; margin: 0 0 1rem; }
    .th-aside-brand { max-width: 180px; height: auto; opacity: 0.85; }

    /* Process strip (replaces parallax sections) */
    .th-process-strip {
      background: linear-gradient(180deg, #f7f5fb 0%, #efe9f7 100%);
      padding: 4rem 1.5rem;
    }
    .th-process-strip > .th-narrow { text-align: center; }
    .th-process-strip h2 {
      color: #220b50; font-size: clamp(1.5rem, 2.6vw, 2.1rem);
      font-weight: 700; margin: 0.4rem 0 2.5rem; letter-spacing: -0.01em;
    }
    .th-process-row {
      max-width: 1100px; margin: 0 auto;
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem;
    }
    @media (max-width: 900px) { .th-process-row { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 540px) { .th-process-row { grid-template-columns: 1fr; } }
    .th-process-step {
      background: #fff; border: 1px solid #e0dceb; border-radius: 12px;
      padding: 1.5rem 1.4rem; transition: transform .2s, box-shadow .2s;
    }
    .th-process-step:hover {
      transform: translateY(-3px);
      box-shadow: 0 14px 30px -18px rgba(34,11,80,0.25);
    }
    .th-step-num {
      display: inline-flex; align-items: center; justify-content: center;
      width: 44px; height: 44px;
      background: #220b50; color: #FFC107;
      font-weight: 800; font-size: 0.95rem;
      border-radius: 50%; margin-bottom: 0.85rem;
      letter-spacing: 0.04em;
    }
    .th-process-step h3 {
      color: #220b50; font-size: 1.05rem; font-weight: 700;
      margin: 0 0 0.5rem; letter-spacing: -0.01em;
    }
    .th-process-step p {
      font-size: 0.9rem; line-height: 1.55; color: #5a5a6a; margin: 0;
    }

    /* Case study */
    .th-case-header { text-align: center; margin-bottom: 2.5rem; }
    .th-case-sub {
      max-width: 600px; margin: 0.5rem auto 0;
      color: #5a5a6a; font-style: italic; font-size: 1.05rem !important;
    }
    .th-feature-image {
      margin: 2.5rem 0; border-radius: 14px; overflow: hidden;
      box-shadow: 0 20px 50px -25px rgba(34,11,80,0.35);
    }
    .th-feature-image img { display: block; width: 100%; height: auto; }
    .th-feature-image figcaption {
      padding: 0.85rem 1.25rem; background: #220b50; color: #fff;
      font-size: 0.92rem; text-align: center; font-style: italic;
    }
    .th-case-body {
      margin: 2rem 0;
      display: grid; grid-template-columns: 280px minmax(0, 1fr); gap: 2rem; align-items: start;
    }
    @media (max-width: 900px) { .th-case-body { grid-template-columns: 1fr; } }
    .th-side-image {
      margin: 0; border-radius: 12px; overflow: hidden;
      box-shadow: 0 10px 30px -16px rgba(34,11,80,0.25);
    }
    .th-side-image img { display: block; width: 100%; height: auto; }
    .th-side-image figcaption {
      padding: 0.5rem 0.85rem; background: rgba(34,11,80,0.04);
      font-size: 0.82rem; color: #5a5a6a; text-align: center;
    }
    .th-case-body p { font-size: 1.05rem; line-height: 1.7; }

    .th-pair {
      display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2.5rem;
    }
    @media (max-width: 700px) { .th-pair { grid-template-columns: 1fr; } }
    .th-pair figure {
      margin: 0; border-radius: 12px; overflow: hidden;
      box-shadow: 0 10px 30px -16px rgba(34,11,80,0.25);
      aspect-ratio: 4/5;
    }
    .th-pair img { display: block; width: 100%; height: 100%; object-fit: cover; }
  </style>'''


def main():
    text = FP.read_text(encoding="utf-8")

    # The current rebuilt body starts at "  <!-- ====" comment and ends just before
    # "<div class="online-quote-section">"
    START_MARKER = '\n  <!--'  # use a less specific marker — find the first comment after nav close
    # Better: find a stable marker — the first child after <div class="nav-section">...</div>
    # We'll anchor on "<section class=\"tm-hero\">" OR the current parallax/hero start
    candidates = ['<section class="tm-hero">',  # current rebuild
                  '<section class="th-hero">',  # if re-running this script
                  '<div class="section mrm-thai-movers">']  # original Webflow
    start = -1
    for c in candidates:
        i = text.find(c)
        if i >= 0:
            start = i
            break
    end = text.find('<div class="online-quote-section">')
    if start < 0 or end < 0:
        print(f"Could not locate markers — start={start}, end={end}")
        return

    new_text = text[:start] + NEW_BODY.lstrip() + "\n" + CSS + "\n  " + text[end:]
    FP.write_text(new_text, encoding="utf-8")

    print(f"Replaced {end-start} chars with {len(NEW_BODY) + len(CSS)} chars of new body+CSS.")

    # Verify div balance
    import re
    clean = re.sub(r'<script\b.*?</script>', '', new_text, flags=re.S)
    clean = re.sub(r'<style\b.*?</style>', '', clean, flags=re.S)
    opens = len(re.findall(r'<div\b[^>]*>', clean))
    closes = len(re.findall(r'</div>', clean))
    print(f"Div balance: opens={opens} closes={closes} diff={opens-closes:+d}")


if __name__ == "__main__":
    main()
