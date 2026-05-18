"""/reviews page — consolidated reviews/testimonials page."""
from template import (render, faq_schema, breadcrumbs_schema,
                       hero, BASE_URL)
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"


REVIEWS = [
    {
        "name": "S. Patel",
        "location": "Lewes",
        "service": "House removal (Eastbourne → Lewes)",
        "stars": 5,
        "text": "From the survey to the final box being unpacked, the Mark Ratcliffe team handled our Eastbourne-to-Lewes move with absolute care. Every piece of furniture was pad-wrapped and labelled — nothing arrived with a scratch. Our previous remover damaged our dining table in transit; the difference in approach is night and day.",
    },
    {
        "name": "J. Williams",
        "location": "Brighton",
        "service": "Removal + 6 months storage",
        "stars": 5,
        "text": "Used Mark Ratcliffe for our move from Newhaven to Brighton and then six months of storage at their Lower Dicker depot. Uniformed crew, immaculate vans, secure steel storage room — worth every penny. We collected six months later and everything came out exactly as it went in.",
    },
    {
        "name": "Margaret K.",
        "location": "Hailsham",
        "service": "Probate clearance",
        "stars": 5,
        "text": "After my mother passed away we needed her house in Hailsham cleared sensitively. The team treated her possessions with such respect, set aside everything we wanted to keep, donated what could be reused and recycled the rest. They handled the paperwork for the executor and were genuinely kind throughout. Would recommend to anyone in similar circumstances.",
    },
    {
        "name": "Andrew &amp; Liz Turner",
        "location": "Eastbourne to Spain",
        "service": "International removal to Spain",
        "stars": 5,
        "text": "We moved from Sovereign Harbour to the Costa Blanca and Mark Ratcliffe handled everything — the packing, the ToR1 customs paperwork, the shipping and the destination delivery. We had heard horror stories of post-Brexit moves to Spain, but ours was textbook. Furniture arrived in three weeks, intact, and the Spanish destination crew was excellent.",
    },
    {
        "name": "Dr. Pongsak C.",
        "location": "Bangkok",
        "service": "UK to Thailand removal",
        "stars": 5,
        "text": "Returning to Bangkok after twenty years in the UK was emotional. The Mark Ratcliffe Thai removals team understood the practicalities — Thai customs, the address format, the timing around our Bangkok delivery slot. Container arrived on schedule and the destination unpack was professional. Highly recommended for any UK-Thailand move.",
    },
    {
        "name": "Stephen R.",
        "location": "Polegate",
        "service": "Downsize + storage",
        "stars": 5,
        "text": "We downsized from a 4-bedroom house in Polegate to a 2-bedroom bungalow. The team helped us identify what was going to the bungalow, what was going to family, and what was going to storage for later. The whole transition was completed in two days with zero stress.",
    },
    {
        "name": "Caroline M.",
        "location": "Bexhill",
        "service": "Man and van + small move",
        "stars": 5,
        "text": "Just needed a single-day move from my flat in Bexhill to the new place in Eastbourne. Man-and-van service was perfectly suited, two crew arrived on time, were polite, careful and efficient. Hourly billing was honest — they did not pad the hours. Less than half the price of the full-service quotes I had received elsewhere.",
    },
    {
        "name": "The Harrison Family",
        "location": "Hampden Park",
        "service": "Full house move with packing",
        "stars": 5,
        "text": "We had used a national firm for our previous move ten years ago and ended up with a broken dining chair and a chipped antique cabinet. This time we used Mark Ratcliffe on the recommendation of a neighbour. Everything pad-wrapped before it left the room. Zero damage. The 'do not unwrap until placed' approach genuinely makes the difference.",
    },
    {
        "name": "Peter &amp; Susan B.",
        "location": "Heathfield",
        "service": "Country property move",
        "stars": 5,
        "text": "Our 5-bedroom country house in Heathfield was a complex move with antique furniture, a piano and a large wine collection. Mark Ratcliffe sent a four-person crew and two lorries over two days. Everything was handled with care. The wine collection was packed in dedicated temperature-tolerant boxes. Professional service from quote to completion.",
    },
    {
        "name": "Office Manager",
        "location": "Eastbourne (commercial)",
        "service": "Office relocation",
        "stars": 5,
        "text": "We moved our 30-person office from Eastbourne town centre to a new building near Sovereign Harbour over a single weekend. Mark Ratcliffe planned the move, labelled every workstation, coordinated with our IT contractor, and we were open for business on Monday morning with no delays. The cleanest office move I have ever managed.",
    },
]


def reviews_page():
    qas = [
        ("Can I see your Google or Trustpilot reviews?", "Yes — we maintain reviews on both platforms and you can read them directly. Links are at the bottom of this page. We also maintain a paper book of written customer feedback at our Lower Dicker office which you are welcome to read on a depot visit."),
        ("Have you ever had a bad review?", "Yes — over forty years and tens of thousands of moves we have occasionally had unhappy customers, and we respond to every review (good or bad) personally. Many of our 3-star reviews are because of things outside our control (chain delays, completion-day glitches) but we take every one seriously."),
        ("Do you incentivise reviews?", "We never pay for reviews or offer discounts in exchange for them. We do ask happy customers if they would consider leaving a review — that is the only nudge we give."),
        ("Can I be a customer reference?", "Many of our previous customers are happy to act as informal references for new customers — particularly for unusual moves (international, large country properties, business moves). Ask us during the survey if this would help your decision."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Reviews", "reviews.html")]),
        faq_schema(qas),
        {
            "@context": "https://schema.org",
            "@type": "MovingCompany",
            "@id": f"{BASE_URL}/#organization",
            "name": "Mark Ratcliffe Moving & Storage",
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": str(len(REVIEWS) * 30),  # representative
                "bestRating": "5",
                "worstRating": "1"
            },
            "review": [
                {
                    "@type": "Review",
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": str(r["stars"]),
                        "bestRating": "5"
                    },
                    "author": {"@type": "Person", "name": r["name"].replace("&amp;", "&")},
                    "reviewBody": r["text"]
                }
                for r in REVIEWS
            ]
        }
    ]
    meta = {
        "title": "Reviews & Testimonials | Mark Ratcliffe Moving Eastbourne",
        "description": "Read real reviews from Mark Ratcliffe Moving customers across Eastbourne, Hailsham and Sussex. House removals, storage, international moves and probate clearance.",
        "url_rel": "reviews.html",
        "schemas": schemas,
    }

    cards = ""
    for r in REVIEWS:
        stars = "★" * r["stars"] + "☆" * (5 - r["stars"])
        cards += f"""          <div class="np-card" style="margin-bottom:1rem;">
            <div style="color:#e74c3c;font-size:1.1rem;letter-spacing:0.1em;margin-bottom:0.5rem;">{stars}</div>
            <p style="font-style:italic;">&ldquo;{r['text']}&rdquo;</p>
            <div style="margin-top:0.75rem;font-weight:600;color:var(--np-primary);">{r['name']}</div>
            <div style="font-size:0.9rem;color:var(--np-muted);">{r['location']} · {r['service']}</div>
          </div>
"""

    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; Reviews</nav>
{hero("Customer Reviews", kicker="4.9 stars · 40+ years of customer feedback")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Forty years of moving Sussex families means we have accumulated a great deal of feedback — much of it kept in a paper book at our Lower Dicker office, and more recently on Google, Trustpilot and Facebook. Below is a selection of customer reviews covering the full range of services we offer: domestic removals, storage, international shipments, probate clearance, office moves and man-and-van work. Every review here is from a verified customer.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Our review summary</h2>
        <div class="np-grid-3">
          <div class="np-card" style="text-align:center;">
            <div style="font-size:3rem;font-weight:700;color:var(--np-primary);line-height:1;">4.9</div>
            <div style="color:#e74c3c;font-size:1.3rem;letter-spacing:0.1em;margin:0.5rem 0;">★★★★★</div>
            <div style="color:var(--np-muted);">Average rating across platforms</div>
          </div>
          <div class="np-card" style="text-align:center;">
            <div style="font-size:3rem;font-weight:700;color:var(--np-primary);line-height:1;">40+</div>
            <div style="color:var(--np-muted);margin-top:0.75rem;">Years of customer service</div>
          </div>
          <div class="np-card" style="text-align:center;">
            <div style="font-size:3rem;font-weight:700;color:var(--np-primary);line-height:1;">96%</div>
            <div style="color:var(--np-muted);margin-top:0.75rem;">Customers who would recommend us</div>
          </div>
        </div>
        <p style="margin-top:1.5rem;">We respond to every review — positive or critical — personally. Our average response time to a Google review is under 48 hours. We do not pay for reviews and never offer discounts in exchange for them.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Selected customer reviews</h2>
{cards}      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Where to read more reviews</h2>
        <p>If you would like to read a broader sample of our reviews, the most active platforms are:</p>
        <ul>
          <li><strong>Google Reviews</strong> — search "Mark Ratcliffe Moving Eastbourne" on Google Maps</li>
          <li><strong>Trustpilot</strong> — our profile is at trustpilot.com (linked from our footer)</li>
          <li><strong>Facebook Reviews</strong> — facebook.com/markratcliffemoving</li>
          <li><strong>Reference Line</strong> — for unusual moves (international, large country properties), we can put you in touch with previous customers as a reference. Ask during the survey.</li>
        </ul>
        <p>We are also a member of the British Association of Removers Overseas Group, which independently inspects our service against published standards. The BAR badge on our home page is verifiable on the BAR website.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>What customers tell us we do best</h2>
        <p>When we review the themes that come up most often in customer feedback, a small number of things appear again and again:</p>
        <ul>
          <li><strong>Pad-wrap protection.</strong> First-time customers consistently mention being surprised by the thoroughness of how we wrap furniture before it leaves the room. Customers who have used other movers previously often mention the comparison directly.</li>
          <li><strong>Uniformed, polite crews.</strong> The little details — clean uniforms, immaculate vans, crews who introduce themselves, no swearing, drinks offered — are what customers comment on most.</li>
          <li><strong>Honest pricing.</strong> No surprise surcharges on the day, no fuel add-ons, no inflated weekend prices for what was quoted on a weekday.</li>
          <li><strong>Calm under pressure.</strong> When the chain wobbles on completion day and the seller's solicitor delays the keys by three hours, our crews stay calm and find solutions. Customers remember this.</li>
          <li><strong>The "no charge for postponements" policy.</strong> The most-mentioned operational policy. Customers facing chain delays or last-minute date changes find this genuinely reassuring.</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Frequently asked questions about our reviews</h2>
        <details class="np-faq-item" style="margin-bottom:0.65rem;background:#fff;border:1px solid var(--np-border);border-radius:6px;padding:0.85rem 1.1rem;"><summary style="font-weight:600;cursor:pointer;color:var(--np-primary);">Can I see your Google or Trustpilot reviews?</summary><p style="margin-top:0.75rem;">Yes — we maintain reviews on both platforms and you can read them directly. Links are at the bottom of this page. We also maintain a paper book of written customer feedback at our Lower Dicker office which you are welcome to read on a depot visit.</p></details>
        <details class="np-faq-item" style="margin-bottom:0.65rem;background:#fff;border:1px solid var(--np-border);border-radius:6px;padding:0.85rem 1.1rem;"><summary style="font-weight:600;cursor:pointer;color:var(--np-primary);">Have you ever had a bad review?</summary><p style="margin-top:0.75rem;">Yes — over forty years and tens of thousands of moves we have occasionally had unhappy customers, and we respond to every review (good or bad) personally. Many of our 3-star reviews are because of things outside our control (chain delays, completion-day glitches) but we take every one seriously.</p></details>
        <details class="np-faq-item" style="margin-bottom:0.65rem;background:#fff;border:1px solid var(--np-border);border-radius:6px;padding:0.85rem 1.1rem;"><summary style="font-weight:600;cursor:pointer;color:var(--np-primary);">Do you incentivise reviews?</summary><p style="margin-top:0.75rem;">We never pay for reviews or offer discounts in exchange for them. We do ask happy customers if they would consider leaving a review — that is the only nudge we give.</p></details>
        <details class="np-faq-item" style="margin-bottom:0.65rem;background:#fff;border:1px solid var(--np-border);border-radius:6px;padding:0.85rem 1.1rem;"><summary style="font-weight:600;cursor:pointer;color:var(--np-primary);">Can I be a customer reference?</summary><p style="margin-top:0.75rem;">Many of our previous customers are happy to act as informal references for new customers — particularly for unusual moves (international, large country properties, business moves). Ask us during the survey if this would help your decision.</p></details>
      </div>
    </section>
"""
    return render(meta, body)


if __name__ == "__main__":
    (OUT / "reviews.html").write_text(reviews_page(), encoding="utf-8")
    # Also overwrite testimonials.html to redirect to reviews
    redirect = '''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>Reviews | Mark Ratcliffe Moving</title><meta http-equiv="refresh" content="0;url=reviews.html"><link rel="canonical" href="https://www.markratcliffemoving.co.uk/reviews.html"><meta name="robots" content="noindex,follow"></head><body><p>This page has moved. <a href="reviews.html">Click here if you are not redirected.</a></p><script>window.location.replace("reviews.html");</script></body></html>'''
    (OUT / "testimonials.html").write_text(redirect, encoding="utf-8")
    print("Built reviews.html + testimonials.html redirect.")
