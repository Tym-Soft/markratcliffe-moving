"""Area pages — 7 nearby towns. Each follows the same template with localised content."""
from template import (render, faq_schema, service_schema, breadcrumbs_schema,
                       hero, render_faq_accordion, BASE_URL)

AREAS = {
    "hailsham-removals": {
        "town": "Hailsham",
        "title": "Hailsham Removals | Lower Dicker Depot | Mark Ratcliffe",
        "description": "Local Hailsham removals from our Lower Dicker depot. House removals, man and van, storage. BAR registered, 40+ years experience. Free quote.",
        "h1": "Hailsham Removals — From Our Lower Dicker Depot",
        "intro": "Mark Ratcliffe Moving has been the trusted name for Hailsham removals since 1982. Our depot at Lower Dicker is a three-minute drive from Hailsham town centre, which means our crews are out the gate and at your door before most other companies have left their yard. We are BAR registered, family-run, and we use the same premium pad-wrap protection on a Hailsham flat move as we do on a country-house relocation.",
        "neighbourhoods": ["Lower Horsebridge", "Magham Down", "Hellingly", "Upper Dicker", "Stone Cross", "Old Town Hailsham"],
        "key_routes": "the A22, A271 and the Hailsham bypass",
        "local_landmarks": "the Cuckoo Trail, Quintins Way development and the Diplocks Industrial Estate",
        "case_study": {
            "title": "A 3-bedroom move from Quintins Way to Brighton",
            "body": "When a family in the new Quintins Way development outgrew their home and bought in Brighton, we surveyed on a Tuesday, packed on the Friday, loaded on the Saturday morning and were unpacking in Hove by 4pm — all within budget and with no chips on the piano."
        },
        "faqs": [
            ("How quickly can you start a removal in Hailsham?", "From our Lower Dicker depot we can usually have a crew on-site within two working days for smaller moves. For full house removals we recommend booking three to four weeks ahead during the May-September peak, but we will always tell you honestly what we can fit in."),
            ("Do you cover the new estates around Hailsham?", "Yes — we have moved many families in and out of Quintins Way, Park Farm, Mulberry Fields and the older Diplocks estates. We know the access routes and parking restrictions on each."),
            ("Can you store furniture in Hailsham?", "We run our Prestige steel self-storage rooms at our Lower Dicker depot, just outside Hailsham. Individual rooms from 30 sq ft, 24-hour CCTV, alarmed access. See our storage page for details."),
            ("Do you serve outlying Hailsham villages?", "Yes — Magham Down, Hellingly, Lower Horsebridge, Upper Dicker, Herstmonceux and Windmill Hill are all part of our daily routes."),
        ]
    },
    "removals-polegate": {
        "town": "Polegate",
        "title": "Removals Polegate | Local House Movers | Mark Ratcliffe",
        "description": "House removals in Polegate from our nearby Lower Dicker depot. Full pad-wrap protection, guaranteed move date, 40+ years experience.",
        "h1": "Polegate Removals — Your Nearby Family-Run Movers",
        "intro": "Polegate sits seven minutes from our Lower Dicker depot, so when you book Mark Ratcliffe Moving you get a genuinely local removal company — not a national chain routing a van down from the M25. We have been moving Polegate families since 1982 and we know every cul-de-sac off Polegate Drive, every speed bump on Wannock Lane and where the parking is tight on the Black Path.",
        "neighbourhoods": ["Polegate town centre", "Willingdon Trees", "Wannock", "Filching", "Folkington"],
        "key_routes": "the A22, A27 and A2270",
        "local_landmarks": "Polegate Railway Station, the Pony pub and the Old Mill",
        "case_study": {
            "title": "Downsizing from Wannock to Polegate town",
            "body": "A retiring couple moving from a 4-bedroom house in Wannock into a 2-bedroom bungalow in Polegate town centre needed us to also place several pieces into storage. We pad-wrapped, moved and containerised across one day — and they only had to unpack what they wanted in their new home."
        },
        "faqs": [
            ("How long does a typical Polegate house move take?", "A 2 or 3-bedroom local move from Polegate usually completes within a single day. A 4 or 5-bedroom or longer-distance move may need two days. We will tell you honestly during the survey."),
            ("Can you handle narrow-access streets in Polegate?", "Yes. We have shuttle vehicles for the tighter terraces off the Black Path and Polegate Drive. Our survey identifies access constraints in advance so the move-day team has the right vehicle."),
            ("Do you offer same-day man and van in Polegate?", "Sometimes — diary permitting. If you need a single bulky item moved or a small flat clearance, give us a call and we will tell you what we can fit in."),
        ]
    },
    "removals-pevensey": {
        "town": "Pevensey",
        "title": "Removals Pevensey | Coastal Movers | Mark Ratcliffe Moving",
        "description": "Pevensey and Pevensey Bay removals from our Lower Dicker depot. BAR registered, premium pad-wrap, guaranteed move date. Free quote.",
        "h1": "Removals in Pevensey and Pevensey Bay",
        "intro": "Whether you are moving from the village within the Norman castle walls or from a property right on the seafront at Pevensey Bay, we know the area. Mark Ratcliffe Moving has been working in Pevensey since 1982 — we understand the salt-air considerations for furniture, the access pinch-points on Pevensey High Street, and the seasonal traffic on the coast road.",
        "neighbourhoods": ["Pevensey village", "Pevensey Bay", "Westham", "Stone Cross", "Rickney"],
        "key_routes": "the A259, A27 and the A22",
        "local_landmarks": "Pevensey Castle, the Royal Oak and Castle pub and the Martello Tower",
        "case_study": {
            "title": "A seafront move from Pevensey Bay",
            "body": "A retired professional couple needed to move from a seafront flat at Pevensey Bay to a cottage in Pevensey village. We surveyed and identified the salt-air corrosion risk on antique furniture, used moisture-resistant pad-wrap and worked around the high tide times. The whole job ran on schedule."
        },
        "faqs": [
            ("Can you access the seafront properties at Pevensey Bay?", "Yes. We have moved into and out of every block on the Bay. We size the right vehicle to the access — a 7.5-tonne lorry for the wider parts, a shuttle van for tighter sections."),
            ("Do you move holiday homes or second homes in Pevensey?", "Often, yes. Many of our Pevensey jobs are part-furnished holiday-home swaps or second-home consolidation. We are happy to work to a flexible timetable that fits with rental handovers."),
            ("How do you protect furniture from sea air during a move?", "Our pad-wrap system seals each piece in quilted blankets before it leaves the room, which reduces moisture and salt exposure during transit. For valuable antiques we recommend our storage at Lower Dicker as a buffer."),
        ]
    },
    "removals-willingdon": {
        "town": "Willingdon",
        "title": "Removals Willingdon | Local House Movers | Mark Ratcliffe",
        "description": "Willingdon and Lower Willingdon removals. 40+ years local experience, BAR registered, full pad-wrap. Same crew that's served Sussex since 1982.",
        "h1": "Willingdon Removals — Trusted Local Movers",
        "intro": "Willingdon is just twelve minutes from our Lower Dicker depot, with our crews regularly running the A22 and A2270 corridor. We move both Upper Willingdon and Lower Willingdon residents, from small 1-bedroom flats off The Triangle to the larger family homes up Coombe Hill. We are BAR registered, family-run, and have been moving Sussex households since 1982.",
        "neighbourhoods": ["Upper Willingdon", "Lower Willingdon", "Coombe Hill", "Friday Street", "Eastbourne Downs"],
        "key_routes": "the A22 and A2270",
        "local_landmarks": "the Willingdon Triangle, the Wish Tower and Willingdon Golf Club",
        "case_study": {
            "title": "A family upsize from Friday Street to Coombe Hill",
            "body": "A growing family moved from a 3-bedroom semi on Friday Street to a 5-bedroom property on Coombe Hill with us. We sent two crews and two lorries, completed the move in a single day, and unpacked everything to the right room — even the awkward upright piano."
        },
        "faqs": [
            ("Is parking an issue for removals in Willingdon?", "Mostly no — Willingdon has fewer parking restrictions than central Eastbourne — but the older terraces near The Triangle can be tight. Our pre-move survey identifies any issues and we apply for suspension parking bays if needed."),
            ("Can you handle the steep driveways up Coombe Hill?", "Yes. We have experience with the inclines and tight turn-ins on Coombe Hill and Friday Street. We size our vehicles accordingly."),
            ("Do you offer storage near Willingdon?", "Our Prestige steel storage rooms are at our Lower Dicker depot — a 15-minute drive from Willingdon. Customers regularly use storage to bridge a sale-and-purchase gap."),
        ]
    },
    "removals-uckfield": {
        "town": "Uckfield",
        "title": "Removals Uckfield | Local Wealden Movers | Mark Ratcliffe",
        "description": "Uckfield removals from our Lower Dicker depot. BAR-registered, premium pad-wrap, guaranteed move date. Serving Wealden since 1982.",
        "h1": "Uckfield Removals — Wealden Specialists Since 1982",
        "intro": "Mark Ratcliffe Moving has covered Uckfield and the surrounding Wealden villages from our Lower Dicker depot since 1982. The A22 puts us within twenty-five minutes of Uckfield High Street, and our crews regularly work Buxted, Maresfield and Framfield as part of our daily rounds. We are a BAR-registered family business that pad-wraps every piece of furniture and guarantees your move date.",
        "neighbourhoods": ["Buxted", "Maresfield", "Framfield", "Ridgewood", "Manor Park"],
        "key_routes": "the A22 corridor",
        "local_landmarks": "Uckfield High Street, the Bridge Cottage and the Sussex Weald",
        "case_study": {
            "title": "A move from Uckfield to the coast",
            "body": "Empty-nesters in Uckfield wanted to move to a sea-view flat at Eastbourne. We surveyed in Uckfield, packed and pad-wrapped on the Thursday, loaded and shipped on the Friday — and stored a few items at Lower Dicker until the new flat was ready a fortnight later."
        },
        "faqs": [
            ("How far is Uckfield from your depot?", "Lower Dicker to Uckfield High Street is about 22 minutes via the A22. We do not charge a separate mileage premium for Uckfield — it is part of our standard service area."),
            ("Can you store furniture between an Uckfield sale and a coast purchase?", "Yes. Many of our Uckfield-to-coast (and coast-to-Uckfield) customers use our Prestige steel storage rooms to bridge a few-week gap between completion dates."),
            ("Do you cover the Wealden villages outside Uckfield town?", "Buxted, Maresfield, Framfield, High Hurstwood, Five Ash Down, Crowborough and Mayfield are all in our weekly routing. Ask us about your specific village."),
        ]
    },
    "removals-heathfield": {
        "town": "Heathfield",
        "title": "Removals Heathfield | Sussex Movers | Mark Ratcliffe Moving",
        "description": "Heathfield removals from Lower Dicker. 40+ years experience across Sussex, BAR registered, premium pad-wrap protection. Free quote.",
        "h1": "Heathfield Removals — Sussex Family Movers",
        "intro": "Heathfield is in our backyard — a thirty-minute run from our Lower Dicker depot via the A267. We have been moving Heathfield homes since 1982, including the village edges at Cross-in-Hand, Old Heathfield, Punnetts Town and Horam. We are a BAR-registered, family-run firm and our same trained crews handle a Heathfield bungalow with exactly the same pad-wrap care as a country mansion.",
        "neighbourhoods": ["Cross-in-Hand", "Old Heathfield", "Punnetts Town", "Horam", "Waldron"],
        "key_routes": "the A267 and A265",
        "local_landmarks": "the Heathfield Independent Cinema, Cuckoo Trail and Heathfield Park",
        "case_study": {
            "title": "Country house to coastal cottage from Heathfield",
            "body": "When a couple downsized from a 5-bedroom country home in Old Heathfield to a 2-bedroom coastal cottage, we deployed a four-man crew for one day of packing, two days of loading and one day of unpacking. Every item of antique furniture arrived intact thanks to our pad-wrap method."
        },
        "faqs": [
            ("How far is Heathfield from your depot?", "About 30 minutes via the A267 — well within our standard service area. We do not charge a mileage premium for Heathfield moves."),
            ("Can you handle large country-property removals around Heathfield?", "Yes. We routinely send multiple crews and multiple lorries for larger Heathfield properties, and we have the experience for antiques, art, pianos and wine cellars."),
            ("Do you offer storage near Heathfield?", "Our Prestige steel storage rooms are at our Lower Dicker depot, around 35 minutes from Heathfield. Many country-property downsizers store with us during the transition."),
        ]
    },
    "removals-bexhill": {
        "town": "Bexhill",
        "title": "Removals Bexhill | Local Coastal Movers | Mark Ratcliffe",
        "description": "Bexhill-on-Sea removals from our Sussex base. House removals, man and van, storage and international. BAR registered, 40+ years experience.",
        "h1": "Bexhill-on-Sea Removals — Trusted Coastal Movers",
        "intro": "Bexhill-on-Sea has been part of our regular routing for over four decades. From our Lower Dicker depot we reach Bexhill in about thirty minutes via the A259 coast road. We move terraced houses on Sea Road, art deco flats off Cooden Drive, family homes in Sidley and country properties on the Bexhill outskirts — all with the same BAR-standard pad-wrap care we have applied since 1982.",
        "neighbourhoods": ["Cooden", "Sidley", "Little Common", "Old Town Bexhill", "Pebsham"],
        "key_routes": "the A259 coast road and the A269",
        "local_landmarks": "the De La Warr Pavilion, Bexhill seafront and Bexhill Down",
        "case_study": {
            "title": "A De La Warr seafront flat move",
            "body": "A couple moving from a Cooden flat to one of the iconic De La Warr-area apartments needed us to coordinate with a tight 30-minute parking suspension. We pre-staged the lorry, sent a four-man crew and completed loading inside the window — and the unpacking finished by lunch."
        },
        "faqs": [
            ("Can you access Cooden Beach properties for removals?", "Yes. We have moved many of the properties along Cooden Drive and the seafront blocks. We always confirm vehicle size and parking suspensions during the survey."),
            ("Do you cover the smaller Bexhill villages?", "Pebsham, Sidley, Little Common and Hooe are all within our regular Bexhill routing."),
            ("Can you store furniture from a Bexhill move?", "Yes — our Prestige steel storage rooms at Lower Dicker are about 35 minutes from Bexhill. We routinely store furniture for Bexhill customers who are downsizing or in transition."),
        ]
    },
}


def render_area_page(slug: str, data: dict) -> str:
    town = data["town"]
    qas = data["faqs"]

    schemas = [
        breadcrumbs_schema([
            ("Home", ""), ("Areas Covered", "areas-covered.html"), (f"{town} Removals", f"{slug}.html")
        ]),
        service_schema(
            name=f"Removals in {town}",
            description=f"Full-service house removals, man and van, storage and international removals in {town}, East Sussex.",
            area_served=town
        ),
        faq_schema(qas)
    ]

    meta = {
        "title": data["title"],
        "description": data["description"],
        "url_rel": f"{slug}.html",
        "schemas": schemas,
    }

    neighbourhoods_html = ", ".join(f"<a href=\"#\">{n}</a>" for n in data["neighbourhoods"][:-1]) + f" and {data['neighbourhoods'][-1]}"

    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="areas-covered.html">Areas Covered</a> &rsaquo; {town} Removals</nav>
{hero(data['h1'], kicker=f"Family-run since 1982 · BAR registered", image="images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">{data['intro']}</p>
        <ul class="np-usp-list">
          <li>BAR-registered family business — 40+ years moving Sussex households</li>
          <li>Premium pad-wrap protection on every item</li>
          <li>Guaranteed move date once your 20% deposit is received</li>
          <li>No charge for postponements, key waits or cancellations</li>
          <li>Trained, uniformed crews in liveried vans</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>The {town} removal services we offer</h2>
        <div class="np-grid-3">
          <div class="np-card">
            <h3>Full house removals</h3>
            <p>Single rooms, full houses, country estates. We pad-wrap, label, transport and place every item in your new home.</p>
            <a href="removals-eastbourne.html">Learn more →</a>
          </div>
          <div class="np-card">
            <h3>Man and van {town}</h3>
            <p>Smaller, budget-friendly moves. Same BAR-trained crew, smaller vehicle, hourly rate.</p>
            <a href="man-and-van-eastbourne.html">Learn more →</a>
          </div>
          <div class="np-card">
            <h3>Storage near {town}</h3>
            <p>Individual steel Prestige rooms at our Lower Dicker depot. CCTV, alarmed access, monthly billing.</p>
            <a href="storage-eastbourne.html">Learn more →</a>
          </div>
          <div class="np-card">
            <h3>International from {town}</h3>
            <p>Specialist UK to Thailand and worldwide door-to-door relocation service from your {town} home.</p>
            <a href="international-removals-eastbourne.html">Learn more →</a>
          </div>
          <div class="np-card">
            <h3>Packing services</h3>
            <p>Full or fragile-only packing — our premium pad-wrap method is what separates a Mark Ratcliffe move from a generic remover.</p>
            <a href="packing-services-eastbourne.html">Learn more →</a>
          </div>
          <div class="np-card">
            <h3>Office &amp; commercial</h3>
            <p>Out-of-hours business moves with minimal downtime. IT-equipment handling and document storage.</p>
            <a href="office-removals-eastbourne.html">Learn more →</a>
          </div>
        </div>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Why local matters when you choose a {town} removal company</h2>
        <p>Choosing a local removal firm for your {town} move is not just about convenience — it is about cost, reliability and routing knowledge. From our Lower Dicker depot, our crews reach {town} via {data['key_routes']}, and they know the area's quirks: where parking is tight, which streets have low bridges, where the parking-suspension applications need to go and what time the school-run traffic builds up. National movers pricing in a {town} job have to factor in the long empty leg back to their yard; we do not, so our quotes are typically more competitive for {town} addresses.</p>
        <p>We are also part of the local community. You will recognise our vans on {data['key_routes']}, you may have seen them at {data['local_landmarks']}, and our family has been part of Sussex life for over forty years. Many of our customers are repeat clients or referrals from neighbours we moved years earlier.</p>
        <p>We cover {neighbourhoods_html} as part of our standard {town} service area, with no extra travel charges within these districts.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>How we protect your possessions</h2>
        <p>Every {town} move uses our signature pad-wrap process. Each piece of furniture is individually wrapped in a thick quilted blanket inside your home, taped, labelled, then carried out — and only unwrapped once it is placed in its final position in your new property. This is the same method used by high-end international movers, and it is why our breakage rate is a fraction of the industry average.</p>
        <figure class="np-image-block">
          <img src="images/pad-wrapped-furniture-eastbourne-removals.webp" width="900" height="675" alt="Furniture individually pad-wrapped and labelled before a Sussex home removal" loading="lazy" decoding="async">
          <figcaption>Every item is quilted and labelled in your home before it moves — our signature pad-wrap method.</figcaption>
        </figure>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>A recent {town} move</h2>
        <div class="np-card np-card-feature">
          <h3>{data['case_study']['title']}</h3>
          <p>{data['case_study']['body']}</p>
        </div>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return render(meta, body)


def build_all():
    from pathlib import Path
    OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"
    written = []
    for slug, data in AREAS.items():
        html = render_area_page(slug, data)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        written.append(slug)
    print(f"Built {len(written)} area pages: {written}")


if __name__ == "__main__":
    build_all()
