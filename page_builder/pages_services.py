"""Service pages — 8 core service pages."""
from template import (render, faq_schema, service_schema, breadcrumbs_schema,
                       hero, render_faq_accordion, BASE_URL)
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"


# ============================================================================
# 1. /removals-eastbourne (1500 words, flagship)
# ============================================================================
def removals_eastbourne():
    qas = [
        ("How much do removals cost in Eastbourne?", "Eastbourne removal costs vary by volume, distance and packing service. As a guide, a 2-bedroom local Eastbourne move typically runs £550–£900 and a 3-bedroom move £800–£1,400. Our full cost guide breaks down every factor."),
        ("How far in advance should I book my Eastbourne move?", "We recommend 4–6 weeks during the peak May–September season. For off-peak moves we can often book within 1–2 weeks. A 20% deposit locks in your guaranteed move date."),
        ("Are you BAR registered?", "Yes — Mark Ratcliffe Moving is a member of the British Association of Removers Overseas Group, which means we are independently inspected against BAR standards for premises, vehicles, training and customer service."),
        ("Do you offer same-day or next-day removals in Eastbourne?", "For smaller man-and-van jobs we sometimes can. Full house removals require survey and packing time so we usually need at least a few days' notice — give us a call and we will tell you what is honestly possible."),
        ("What happens if my move date changes?", "There is no charge for postponements, cancellations or key waits. We simply update the diary at no extra cost — one of the things our Eastbourne customers tell us they value most."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Removals Eastbourne", "removals-eastbourne.html")]),
        service_schema(
            "Eastbourne Removals",
            "Full-service domestic house removals across Eastbourne and East Sussex from Mark Ratcliffe Moving — BAR registered, family-run since 1982.",
            "Eastbourne"
        ),
        faq_schema(qas),
    ]
    meta = {
        "title": "Removals Eastbourne | BAR Registered | Mark Ratcliffe Moving",
        "description": "Trusted Eastbourne removals since 1982. BAR-registered, full pad-wrap protection and guaranteed move dates across East Sussex. Free quote.",
        "url_rel": "removals-eastbourne.html",
        "schemas": schemas,
    }

    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; Removals Eastbourne</nav>
{hero("Eastbourne Removals — Family-Run Since 1982", kicker="BAR registered · 40+ years · Pad-wrap protection")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Mark Ratcliffe Moving is Eastbourne's family-run removal company — established in 1982 and BAR registered. From our Lower Dicker depot, just outside Hailsham, our trained, uniformed crews cover every postcode in Eastbourne and the surrounding East Sussex area. Whether you are moving a one-bedroom flat in Old Town or a four-bedroom family home in Sovereign Harbour, we apply the same premium pad-wrap protection and guaranteed move date that has built our reputation over four decades.</p>
        <ul class="np-usp-list">
          <li>BAR-registered family business — independently inspected to industry standards</li>
          <li>Premium pad-wrap protection on every item of furniture</li>
          <li>Guaranteed move date locked in with your 20% deposit</li>
          <li>No charge for postponements, key waits or cancellations</li>
          <li>Trained, uniformed crews in liveried, immaculate vans</li>
          <li>Full insurance and our own Prestige steel storage at Lower Dicker</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Why Eastbourne families have chosen us since 1982</h2>
        <p>We are a family business. Mark started the firm in 1982 and over forty years it has grown into one of Sussex's most experienced removal companies — but the family ethos has not changed. Every quote is honest, every crew is trained in-house, and every move is delivered to the standard we would expect for our own homes. Many of our Eastbourne customers are repeat clients or referred to us by neighbours, friends or solicitors we have worked with for decades.</p>
        <p>From our depot at Lower Dicker we reach every Eastbourne postcode — Old Town, Hampden Park, Langney, Sovereign Harbour, Roselands, Meads, the seafront, Town Centre and the surrounding villages of Willingdon, Polegate and Pevensey — in well under thirty minutes. That means lower mileage, lower cost and faster response than nationals routing in from outside the area.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Our Eastbourne removal service in detail</h2>

        <h3>Free pre-move survey</h3>
        <p>Every removal starts with a free survey — either in your home or via video call, whichever you prefer. We walk through every room, agree what is moving and what is going to storage or charity, identify access constraints (parking, lifts, low beams), and discuss whether you want us to pack everything or just the fragile items. You then receive an itemised written quote with absolutely no obligation.</p>

        <h3>Premium full pad-wrap protection</h3>
        <p>This is what makes a Mark Ratcliffe move different from a generic removal. Every piece of furniture — sideboards, wardrobes, dining tables, bedside cabinets, the lot — is individually wrapped in a thick quilted blanket inside your home before it leaves the room. We tape it, we label it, we carry it to the lorry, and it is only unwrapped once it has been placed in its final position in your new property. Many of our customers tell us the absence of chips, scratches or dings is the single biggest difference they noticed compared with a previous remover.</p>

        <figure class="np-image-block">
          <img src="images/pad-wrapped-furniture-eastbourne-removals.webp" width="900" height="675" alt="Furniture individually pad-wrapped and labelled before an Eastbourne home removal" loading="lazy" decoding="async">
          <figcaption>Pad-wrapping in progress — each piece quilted and labelled before it leaves the room.</figcaption>
        </figure>

        <h3>Trained, uniformed crews</h3>
        <p>Our removers are trained in-house at our dedicated staff training centre to BS 8564-aligned standards. That covers fragile packing, furniture lifting and handling, vehicle loading, customer service and health-and-safety. They arrive on move day in branded uniforms, in immaculate company vans — small details, but they reflect how we run the rest of the operation.</p>

        <h3>Guaranteed move date</h3>
        <p>When you pay your 20% deposit, your move date is locked in. No slippage, no surprises. And critically — there is no charge if your completion date moves, if your buyer pulls out, or if you need to cancel. Removals customers across Eastbourne are often surprised when we explain this; many removal firms levy substantial change fees. We do not.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Areas of Eastbourne we cover from our depot</h2>
        <p>From Lower Dicker we routinely move every part of Eastbourne and surrounding villages. Our standard Eastbourne service area — with no travel premium — includes:</p>
        <div class="np-grid-3">
          <div><strong>Town Centre &amp; Seafront</strong><br>Town Centre, Seafront, Meads, Devonshire Park</div>
          <div><strong>Old Town &amp; West</strong><br>Old Town, Upperton, Saffrons, Compton Place</div>
          <div><strong>North Eastbourne</strong><br>Hampden Park, Roselands, Bridgemere, Ratton</div>
          <div><strong>East Eastbourne</strong><br>Langney, Sovereign Harbour, Pevensey Bay</div>
          <div><strong>South Coast</strong><br>Lower Meads, Holywell, the Beachy Head road</div>
          <div><strong>Surrounding villages</strong><br><a href="removals-willingdon.html">Willingdon</a>, <a href="removals-polegate.html">Polegate</a>, <a href="removals-pevensey.html">Pevensey</a>, <a href="hailsham-removals.html">Hailsham</a></div>
        </div>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Pricing — how an Eastbourne removal quote is built</h2>
        <p>We do not believe in misleading "from £" headline prices. Every move is different, so every quote is built around your specific circumstances. The main factors are: the volume of your possessions (measured in cubic feet during the survey), the distance between properties, the access at both ends, whether you want a packing service, and whether you have any special items (pianos, antiques, safes, hot tubs).</p>
        <p>For a sense of guideline pricing, see our <a href="removals-eastbourne-cost.html">full Eastbourne removals cost guide</a>. As a quick reference: a 2-bedroom local Eastbourne move typically runs £550–£900; a 3-bedroom move £800–£1,400; a 4-bedroom-plus move £1,200–£2,200. Long-distance and international moves are quoted separately.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Real Eastbourne moves we have handled</h2>
        <div class="np-grid-2">
          <div class="np-card np-card-feature">
            <h3>3-bedroom Old Town to Brighton</h3>
            <p>A young family upgrading from a 3-bedroom terraced house in Old Town to a larger property in Brighton's Seven Dials. We surveyed on the Saturday, packed and pad-wrapped on the Thursday, completed on the Friday morning and unpacked by the early afternoon. Nothing chipped, nothing missing, and the kids' bedrooms were the priority unpack.</p>
          </div>
          <div class="np-card np-card-feature">
            <h3>Retirement downsize from Sovereign Harbour</h3>
            <p>A retiring couple moving from a 4-bedroom Sovereign Harbour marina house to a 2-bedroom flat in Lewes. We placed a third of their possessions into our Prestige steel storage at Lower Dicker for their children to claim, donated a vanload via our charity partner, and delivered the remainder to their new home over two days.</p>
          </div>
        </div>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 2. /packing-services-eastbourne (1200 words)
# ============================================================================
def packing_services():
    qas = [
        ("Do I have to use your packing service?", "No. Many customers pack their own boxes and we just move them. But our pad-wrap protection of furniture is included on every full removal — that is what makes the most difference to whether things arrive damaged."),
        ("How far ahead do you need to pack?", "We typically pack one to two days before moving day. For larger homes we may start three to four days ahead. The survey will set a packing schedule that works around your routine."),
        ("Can I leave clothes in drawers?", "Yes for lightweight items in solid drawer units. For heavy items or fragile drawers we ask you to empty them so the unit can be moved safely. We will tell you on the day."),
        ("Do you pack electronics?", "We do. Our crews are trained to handle TVs, computers, sound systems and other electronics. Original boxes are best where you have them; otherwise we wrap and crate to manufacturer-equivalent standards."),
        ("What does professional packing cost?", "Full packing for a 3-bedroom home typically adds £350–£600 to a removal. Fragile-only packing is roughly half that. Materials are usually included."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("Packing Services", "packing-services-eastbourne.html")]),
        service_schema("Professional Packing Services Eastbourne",
                       "Premium pad-wrap and fragile packing service for Eastbourne removals — BAR-trained packers since 1982.",
                       "Eastbourne"),
        faq_schema(qas),
    ]
    meta = {
        "title": "Packing Services Eastbourne | Pad-Wrap Specialists | Mark Ratcliffe",
        "description": "Professional packing services in Eastbourne. Full pad-wrapping, export-grade crating and fragile packing. BAR-trained packers since 1982.",
        "url_rel": "packing-services-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; Packing Services</nav>
{hero("Professional Packing Services in Eastbourne", kicker="Pad-wrap specialists · BAR-trained packers", image="images/pad-wrapped-furniture-eastbourne-removals.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Packing well is the single biggest factor in whether your possessions arrive intact. Mark Ratcliffe Moving's packing service in Eastbourne is built around our signature pad-wrap method — the same approach used by premium international movers — combined with proper export-grade materials and trained, BAR-standard packers. We can pack everything for you, just the fragile items, or supply you with materials to pack yourself.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Why our packing is different</h2>
        <p>Most removal companies use bubble wrap, newspaper and standard cartons. We do too — but only for breakables inside boxes. Our real difference is what we do with your <em>furniture</em>. Every dining table, every sideboard, every wardrobe, every bedside cabinet is individually wrapped in a thick quilted blanket inside your home, taped securely and labelled, before it is carried to the lorry. It is only unwrapped once it has been placed in its final position in your new property. The result is far fewer chips, scratches and dings than a standard remover delivers.</p>
        <figure class="np-image-block">
          <img src="images/pad-wrapped-furniture-eastbourne-removals.webp" width="900" height="675" alt="Eastbourne removal furniture being individually pad-wrapped and labelled" loading="lazy" decoding="async">
          <figcaption>Our pad-wrap method protects furniture from the moment it leaves your room to the moment it is placed in your new home.</figcaption>
        </figure>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Packing services we offer</h2>
        <div class="np-grid-2">
          <div class="np-card">
            <h3>Full packing service</h3>
            <p>We pack absolutely everything — clothing, kitchen, books, ornaments, electronics, art. Ideal if you want zero packing stress, or if you are working full-time and cannot give over a fortnight to wrapping things. Typically completed one or two days before moving day.</p>
          </div>
          <div class="np-card">
            <h3>Fragile-only packing</h3>
            <p>You pack the easy stuff (clothes, linen, books) and we handle anything breakable — china, glassware, mirrors, art, picture frames, lamps, ceramics, electronics. This is the most popular option for self-packers.</p>
          </div>
          <div class="np-card">
            <h3>Export packing and crating</h3>
            <p>Higher-spec packing for international moves and long-term storage. We use moisture-resistant pad-wrap, custom timber crates for art and antiques, and we comply with destination-country wood-packaging regulations (ISPM-15 where required).</p>
          </div>
          <div class="np-card">
            <h3>Unpacking on arrival</h3>
            <p>Optional add-on. Once we have placed your furniture in the right room and unwrapped it, our crew can also unpack your boxes, remove the materials and take the cardboard away for recycling. Especially popular with downsizers and seniors.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Our packing materials</h2>
        <p>The cardboard you use matters. Cheap single-wall cartons collapse under stack pressure and are the leading cause of damage in self-packed moves. We use:</p>
        <ul>
          <li><strong>Triple-wall corrugated cartons</strong> for kitchen and book boxes.</li>
          <li><strong>Wardrobe cartons</strong> with built-in hanging rail — your clothes go directly from your wardrobe to ours without folding.</li>
          <li><strong>Anti-static bubble wrap</strong> for electronics and sensitive items.</li>
          <li><strong>Archival tissue paper</strong> for china, fine art and antiques.</li>
          <li><strong>Custom timber crates</strong> for paintings, sculptures, mirrors and grandfather clocks.</li>
          <li><strong>Mattress and sofa bags</strong> with anti-dust closures.</li>
        </ul>
        <p>If you are packing yourself, you can buy any of these materials from our <a href="packaging-shop.html">packaging shop</a> — collected from our Lower Dicker depot or delivered to your door.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>The pad-wrap process, step by step</h2>
        <ol>
          <li><strong>Survey and inventory.</strong> We walk through every room with you and agree what is moving, what needs special handling, and what is staying.</li>
          <li><strong>Pre-move pack day.</strong> One or two days before, our team pads, wraps and labels every item of furniture and packs every fragile item into properly sized cartons.</li>
          <li><strong>Move day load.</strong> Every wrapped piece is carried out of your home (it never gets unwrapped to manoeuvre), loaded into the lorry in a stack-safe sequence, and strapped.</li>
          <li><strong>Delivery and placement.</strong> At your new home we carry items in still wrapped, place each piece in its final position, and only then remove the pad-wrap and reveal the furniture.</li>
          <li><strong>Optional unpack and clear-up.</strong> If you have requested it, we unpack your boxes into agreed locations, fold and remove the cartons and take the wrapping back to our depot for re-use.</li>
        </ol>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>How much does packing cost?</h2>
        <p>The honest answer is that packing prices depend on volume and fragility — a flat in Old Town with a few crates and a sideboard takes a fraction of the time of a 4-bedroom country home with a wine cellar and antique furniture. As a guide, full packing for a 3-bedroom Eastbourne home typically adds £350–£600 to your removal quote; fragile-only packing roughly half that. Materials are included in the quoted price.</p>
        <p>For a precise quote, request a survey — we will give you an itemised figure with no obligation.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 3. /storage-eastbourne (1300 words)
# ============================================================================
def storage_eastbourne():
    qas = [
        ("How are your storage rooms different from a self-storage warehouse?", "Each customer has their own individual steel-walled room, not a shelf or a cage inside a shared warehouse. You sign in at our depot and your possessions are sealed inside your room with 24-hour CCTV and alarmed access."),
        ("What sizes of storage room do you offer?", "From small 30 sq ft rooms (suitable for the contents of a studio flat or office) up to 200+ sq ft rooms for a full house. We will measure your inventory during the survey and recommend the right size."),
        ("How long is the minimum storage term?", "Four weeks. After that you pay month-by-month — no long contracts and no early-exit fees."),
        ("Can I access my storage room?", "Yes — by appointment during depot hours, normally with 24-hour notice. Many customers store their long-term archive items and access only occasionally; some access weekly during transition periods."),
        ("Is my stored property insured?", "Storage insurance is available as an add-on and we strongly recommend it. We can arrange cover through our broker, or you can extend your existing household contents policy."),
        ("Can I store a vehicle, motorbike or boat?", "Subject to availability — yes for cars and motorbikes that have been drained of fuel. Boats and large items depend on dimensions; ask us."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("Storage Eastbourne", "storage-eastbourne.html")]),
        service_schema("Self Storage Eastbourne",
                       "Secure self storage in Eastbourne / Lower Dicker. Individual steel Prestige rooms with CCTV and alarmed access.",
                       "Eastbourne"),
        faq_schema(qas),
    ]
    meta = {
        "title": "Storage Eastbourne | Prestige Steel Rooms | Mark Ratcliffe",
        "description": "Secure self storage in Eastbourne / Lower Dicker. Individual steel Prestige rooms, 24-hour CCTV, alarmed access. Short and long-term storage.",
        "url_rel": "storage-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; Storage</nav>
{hero("Secure Storage in Eastbourne — Prestige Steel Rooms", kicker="Individual steel rooms · 24-hour CCTV · Alarmed access", image="images/Storage.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Mark Ratcliffe Moving runs a dedicated Prestige steel storage facility at our Lower Dicker depot, just outside Hailsham and a short drive from Eastbourne. Unlike communal self-storage warehouses where everyone's possessions sit on open shelves or in shared cages, every customer here has their own individual steel-walled room — sealed, alarmed and CCTV-monitored. It is the same level of security we give our own family's possessions.</p>
        <ul class="np-usp-list">
          <li>Individual steel-walled rooms — not shared cages or shelves</li>
          <li>24-hour CCTV and alarmed perimeter</li>
          <li>Dry, ventilated environment — no damp, no rodents</li>
          <li>Direct vehicle access — no long carries up corridors</li>
          <li>Same firm packs, moves and stores — no double-handling</li>
          <li>Month-by-month billing, no long contracts</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>What makes Prestige storage different</h2>
        <p>Most self-storage facilities you see advertised are huge warehouses where customers rent a unit inside a large open space — sometimes a shelf, sometimes a cage, sometimes a metal box with a roll-up door. They work fine for many people, but they have downsides: shared air, shared corridors, shared access codes, and a feeling of being inside a busy industrial estate.</p>
        <p>Our Prestige steel rooms are different. Each is a self-contained, individual steel-walled room with its own door, its own lock and its own internal volume. When your possessions go into one, you are the only person who accesses it. It is closer to a private vault than a warehouse cage. For people storing antiques, art, family heirlooms or business stock, the difference matters.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Our Prestige steel storage at a glance</h2>
        <div class="np-grid-2">
          <div class="np-card">
            <h3>24-hour CCTV and alarmed access</h3>
            <p>Every entry and exit is logged. CCTV covers the perimeter, the depot yard and the storage corridors. The site is alarmed out of hours.</p>
          </div>
          <div class="np-card">
            <h3>Individual room sizes</h3>
            <p>Rooms range from 30 sq ft (around the contents of a studio flat or small office) up to 200+ sq ft (a full house). We measure your inventory and recommend the right size — we do not oversell.</p>
          </div>
          <div class="np-card">
            <h3>Pristine, dry, ventilated environment</h3>
            <p>The building is dry, ventilated and pest-controlled. We do not store food, hazardous goods or anything that creates moisture. Your possessions come out the same condition they went in.</p>
          </div>
          <div class="np-card">
            <h3>Direct vehicle access</h3>
            <p>Our depot has direct vehicle access to the storage rooms — no long carries down narrow corridors. That makes both loading and unloading faster and gentler on your furniture.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Who uses our Eastbourne storage</h2>
        <p>Our storage customers fall into a few clear groups:</p>
        <ul>
          <li><strong>Between-moves customers.</strong> You have completed on your sale but your purchase is delayed. We pack, pad-wrap, store and redeliver to your new home when you are ready.</li>
          <li><strong>Downsizers.</strong> You are moving from a larger home into a smaller one and want a buffer to decide what to keep and what to pass on to family.</li>
          <li><strong>Expats and international movers.</strong> You are relocating abroad and want a UK base for items you are not shipping yet — or for items returning expats want stored before they find a property.</li>
          <li><strong>Business overflow.</strong> Stock, archives, retail-display inventory, exhibition kit. Our document and stock storage is GDPR-aware.</li>
          <li><strong>Students and renters.</strong> Particularly summer storage for student accommodation between leases.</li>
          <li><strong>Renovation customers.</strong> Whole-house renovations are easier when the contents are out of the way for a few months.</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>How storage works with your move</h2>
        <p>One of the biggest advantages of using Mark Ratcliffe for both your removal and your storage is that everything is handled by one team using the same pad-wrap method, all the way through. We pad-wrap and load at your origin property, drive to our Lower Dicker depot, transfer directly into your individual storage room (no double-handling, no extra carries), and when you are ready we reverse the process to deliver into your new home. Compare this with using a remover for the move and a separate self-storage facility for the storage: every transfer is an extra handling opportunity, and every handling is an opportunity for damage.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Pricing and minimum terms</h2>
        <p>We bill monthly with a four-week minimum. After your first four weeks you can extend month-by-month for as long as you need, with no long contract and no early-exit fees. As a guide, a 30 sq ft room (studio-flat contents) starts from around £15 per week; a 100 sq ft room (3-bed house contents) from around £40 per week. Pricing depends on the time of year and our current availability — call for a same-day quote.</p>
        <p>Storage insurance is available as an add-on and we strongly recommend it. We can arrange cover through our broker.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>How to book a storage room</h2>
        <p>Two routes. If your storage is part of a removal we are handling, your survey will include the storage inventory and we will recommend a room size and pricing. If you are storage-only, call us or use the form — we can usually arrange a room within a few days. Visit our depot at Lower Dicker any time during business hours; we are happy to show you the facility before you commit.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 4. /international-removals-eastbourne (1500 words)
# ============================================================================
def international_removals():
    qas = [
        ("How long does an international removal take?", "Air freight to Europe is typically 5–10 days door to door. Sea freight to Australia, NZ, USA or Thailand is typically 6–12 weeks. We will give you a more accurate window once we know the destination, port and volume."),
        ("Do you handle customs documentation?", "Yes. We prepare the inventory packing list, valued inventory, customs declarations and Transfer of Residence (ToR1) paperwork for UK leavers. Our destination agents handle the import side at the other end."),
        ("Can I include a car in my international removal?", "Sometimes — depending on the destination's import rules and your container space. We can advise on car shipping options including using a specialist car-shipping partner."),
        ("Do you ship to Thailand specifically?", "Yes — UK to Thailand is one of our specialist routes. Bangkok, Pattaya, Phuket and Chiang Mai are all destinations we ship to regularly, with experienced destination agents and an understanding of Thai customs."),
        ("Are my goods insured during international shipment?", "Comprehensive marine transit insurance is available and strongly recommended. We arrange cover via our specialist broker; premiums typically run 2–3% of the declared value."),
        ("What can't I ship?", "Most countries prohibit firearms, explosives, narcotics, certain plants and seeds, ivory, some food items and hazardous chemicals. Many also restrict alcohol, electronics and antiques. We will give you a destination-specific prohibited list during the survey."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("International Removals", "international-removals-eastbourne.html")]),
        service_schema("International Removals Eastbourne",
                       "International removals from Eastbourne to 200+ countries. UK-Thailand specialist, BAR Overseas Group member.",
                       "Worldwide"),
        faq_schema(qas),
    ]
    meta = {
        "title": "International Removals Eastbourne | Thailand & Worldwide",
        "description": "International removals from Eastbourne to over 200 countries. UK-Thailand specialists, BAR Overseas Group member. Door-to-door service.",
        "url_rel": "international-removals-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; International</nav>
{hero("International Removals from Eastbourne — Thailand and Beyond", kicker="BAR Overseas Group member · UK-Thailand specialist", image="images/mark-ratcliffe-sleeper-cab-removal-lorry.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Mark Ratcliffe Moving is a full member of the British Association of Removers Overseas Group. From our Lower Dicker depot just outside Eastbourne we have arranged international relocations to more than 200 countries and territories. We are a specialist UK-to-Thailand mover, and we routinely handle moves to France, Spain, Australia, New Zealand, the USA, Canada, the UAE and South Africa. Every international move uses our premium pad-wrap and export-grade crating, handled by trained crews and partnered with vetted destination agents at the other end.</p>
        <ul class="np-usp-list">
          <li>BAR Overseas Group member — independently inspected to international removal standards</li>
          <li>Specialist UK-to-Thailand expertise — Bangkok, Pattaya, Phuket, Chiang Mai</li>
          <li>Sole-use containers (20' / 40') or part-load (groupage) options</li>
          <li>Full customs documentation handled — including ToR1 relief paperwork</li>
          <li>Vetted destination agents in 200+ countries</li>
          <li>Marine transit insurance available through our specialist broker</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Our international removal service</h2>

        <h3>Survey and quotation</h3>
        <p>We start with a survey — in your home, by video call, or in some cases by detailed inventory list. The output is a cubic-metre volume figure, which is the key number for international shipping, plus an itemised quotation showing packing, transport, freight, customs and destination delivery as separate line items.</p>

        <h3>Export packing and crating</h3>
        <p>Export packing is more rigorous than domestic packing because your possessions will spend weeks at sea. We use moisture-resistant pad-wrap, anti-corrosion paper for metalwork, custom timber crates for art and antiques, and our wood-packaging complies with ISPM-15 for destination countries that require it.</p>

        <h3>Container loading</h3>
        <p>Smaller moves typically ship as a part-load (groupage) — your possessions share a container with other shipments going to the same region. Full house moves usually ship as sole-use 20-foot or 40-foot containers. We will recommend the right option based on volume, urgency and budget.</p>

        <h3>Shipping and customs clearance</h3>
        <p>Sea freight is the most common method for non-EU destinations; air freight is faster but considerably more expensive and only used for smaller, urgent shipments. We prepare all UK export documentation including the inventory packing list, valued inventory and any Transfer of Residence forms. Our destination agents handle the import paperwork at the other end.</p>

        <h3>Delivery at destination</h3>
        <p>Our vetted destination agents collect your container, transport to your new home, unpack the boxes into agreed rooms, reassemble furniture and remove all packing debris. You receive the same kind of careful unpack at the other end as you got at packing — that is the whole point of using a BAR Overseas Group member rather than booking a freight forwarder yourself.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Specialist UK to Thailand removals</h2>
        <p>UK-Thailand is one of our specialist routes. We have moved many British residents to Bangkok, Pattaya, Phuket, Chiang Mai, Koh Samui and the wider Thai market — and many Thai-British couples in the other direction. Our service includes:</p>
        <ul>
          <li>Direct experience of Thai customs requirements — including the new electronic clearance system</li>
          <li>Understanding of Thai address conventions and the practical access constraints at typical Thai apartments and houses</li>
          <li>Specialist crating for items that need extra protection in the tropical climate</li>
          <li>Trusted local destination agents in each major Thai city</li>
          <li>Practical advice on what to ship versus what to buy locally</li>
        </ul>
        <figure class="np-image-block">
          <img src="images/MRM-Thai-Movers.webp" width="900" height="600" alt="Mark Ratcliffe Moving UK to Thailand removals — specialist Thai destination service" loading="lazy" decoding="async">
          <figcaption>Our UK-Thailand removals service is one of our specialisms.</figcaption>
        </figure>
        <p>See our dedicated <a href="thai-moving-services.html">Thai removals page</a> for more on shipping to Thailand specifically.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Other popular destinations from Eastbourne</h2>
        <div class="np-grid-3">
          <div class="np-card"><h3>France</h3><p>All regions; common destinations include Dordogne, Provence, Charente, Brittany, the south coast. Sea freight via Dover or Channel Tunnel.</p></div>
          <div class="np-card"><h3>Spain</h3><p>Costa Blanca, Costa del Sol, Catalonia, the Balearics and inland Andalucía. Sea freight or full-load by road.</p></div>
          <div class="np-card"><h3>Australia &amp; NZ</h3><p>Sydney, Melbourne, Perth, Brisbane, Auckland, Wellington. Strict quarantine — we know the rules.</p></div>
          <div class="np-card"><h3>USA &amp; Canada</h3><p>East and west coasts. Customs increasingly digital; ToR1 relief paperwork supported.</p></div>
          <div class="np-card"><h3>UAE</h3><p>Dubai, Abu Dhabi, Sharjah. Air or sea freight; restrictions on alcohol and certain media items.</p></div>
          <div class="np-card"><h3>South Africa</h3><p>Cape Town, Johannesburg, Durban. Sea freight typically 8–10 weeks.</p></div>
        </div>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Documentation we'll help with</h2>
        <p>International moves involve significantly more paperwork than domestic moves, and getting it wrong delays or impounds shipments. We prepare and check:</p>
        <ul>
          <li><strong>Inventory packing list</strong> — every box and item documented for customs</li>
          <li><strong>Valued inventory</strong> — for insurance and customs declarations</li>
          <li><strong>Transfer of Residence (ToR1)</strong> for UK leavers entitled to customs relief on personal effects</li>
          <li><strong>Visa / residency confirmation</strong> — required for many countries' customs to release goods</li>
          <li><strong>Power of attorney</strong> for destination customs where required</li>
          <li><strong>ATA Carnets</strong> for temporary imports (rare but available)</li>
        </ul>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 5. /man-and-van-eastbourne (1100 words)
# ============================================================================
def man_and_van():
    qas = [
        ("How much is your man and van service in Eastbourne?", "Our hourly rate starts from £55 per hour for one mover plus driver, with a 2-hour minimum. A weekend or evening surcharge applies. Larger vans and additional movers are quoted separately."),
        ("Can you do same-day man and van in Eastbourne?", "Sometimes — it depends on our diary. We do not promise same-day in advance; call us and we will tell you honestly what we can fit in today."),
        ("What is the difference between man-and-van and a full removal?", "Man-and-van is hourly, uses a smaller vehicle (Luton or 3.5-tonne), suits small flats, single items and student moves. A full removal is quoted as a fixed job, uses larger lorries and includes our full pad-wrap protection and packing service."),
        ("Do you supply boxes for man-and-van jobs?", "Yes — we can drop materials in advance or you can collect from our Lower Dicker depot. Pad-wrap and blankets are included with the vehicle."),
        ("Can I use man-and-van for an IKEA collection?", "Absolutely — IKEA flat-pack collections, eBay pickups and Facebook Marketplace runs are some of our most common man-and-van jobs. Tell us the address and dimensions and we will quote."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("Man and Van Eastbourne", "man-and-van-eastbourne.html")]),
        service_schema("Man and Van Eastbourne",
                       "Same-day and small moves in Eastbourne. Hourly rate with BAR-trained crews and proper pad-wrap protection.",
                       "Eastbourne"),
        faq_schema(qas),
    ]
    meta = {
        "title": "Man and Van Eastbourne | Same-Day & Small Moves | Mark Ratcliffe",
        "description": "Reliable man and van service in Eastbourne. Same-day, single items, small moves. Same BAR-trained crews, lower price point. From £55/hour.",
        "url_rel": "man-and-van-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; Man and Van</nav>
{hero("Man and Van Eastbourne — Same Trusted Team, Smaller Job", kicker="From £55/hour · BAR-trained crews · Pad-wrap included")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Not every move needs a 7.5-tonne lorry and a full pre-pack. For studio flats, 1-bedroom moves, single bulky items, student moves and IKEA collections, our man-and-van service in Eastbourne offers the same trained crews and pad-wrap protection at a lower hourly price point. We are still a BAR-registered firm; we just use a smaller vehicle and bill by the hour rather than as a fixed quote.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>When man-and-van is right for you</h2>
        <ul>
          <li><strong>Studio or 1-bedroom flat moves</strong> within Eastbourne or East Sussex</li>
          <li><strong>Single bulky items</strong> — a sofa, a fridge-freezer, a piano, a workshop bench</li>
          <li><strong>IKEA or furniture-shop collections</strong> — let us pick up your flatpacks while you carry on with your day</li>
          <li><strong>eBay / Facebook Marketplace runs</strong> — both ends of the country if needed</li>
          <li><strong>Student moves</strong> — between halls, into rentals, end-of-summer storage</li>
          <li><strong>Storage transfers</strong> — moving items between our storage and your home</li>
          <li><strong>Clearance light</strong> — taking unwanted items to charity or the tip</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>What is included</h2>
        <div class="np-grid-2">
          <div class="np-card">
            <h3>Driver plus 1 or 2 movers</h3>
            <p>Choose one helper or two. One helper is fine for most studio and 1-bed moves; two helpers speed up larger jobs and reduce the hours billed.</p>
          </div>
          <div class="np-card">
            <h3>Luton van or 3.5-tonne vehicle</h3>
            <p>Our man-and-van vehicles have load areas of around 600 cubic feet — equivalent to a studio flat or a generously full 1-bedroom flat.</p>
          </div>
          <div class="np-card">
            <h3>Blankets, straps, dollies</h3>
            <p>Standard equipment included — pad-wrap blankets, ratchet straps, sack barrows, furniture sliders. No extra equipment fees.</p>
          </div>
          <div class="np-card">
            <h3>Optional packing materials</h3>
            <p>Need boxes too? We can drop materials in advance or you can collect them from our Lower Dicker depot.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Same-day service — when we can</h2>
        <p>Many removal firms advertise "same-day" knowing they will charge a premium when you call. We do not. We will tell you honestly whether we have a crew available today, and if we do, the price is the standard hourly rate. If not, we will offer the next available slot — usually within 24-48 hours during the off-peak season.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Pricing</h2>
        <table class="np-price-table">
          <thead><tr><th>Configuration</th><th>From</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td>Driver + 1 mover, Luton van</td><td>£55 / hour</td><td>2-hour minimum, weekday rate</td></tr>
            <tr><td>Driver + 2 movers, Luton van</td><td>£75 / hour</td><td>2-hour minimum, weekday rate</td></tr>
            <tr><td>Driver + 2 movers, 3.5-tonne</td><td>£85 / hour</td><td>2-hour minimum, weekday rate</td></tr>
            <tr><td>Weekend / evening / bank holiday</td><td>+25%</td><td>Applied to the relevant hourly rate</td></tr>
          </tbody>
        </table>
        <p>Prices include all standard moving equipment. Long-distance jobs (outside East Sussex) are quoted as a fixed rate rather than hourly.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Areas we cover</h2>
        <p>Our man-and-van service covers the whole BN postcode area and surrounding districts: Eastbourne, <a href="hailsham-removals.html">Hailsham</a>, <a href="removals-polegate.html">Polegate</a>, <a href="removals-pevensey.html">Pevensey</a>, <a href="removals-willingdon.html">Willingdon</a>, <a href="removals-uckfield.html">Uckfield</a>, <a href="removals-heathfield.html">Heathfield</a>, <a href="removals-bexhill.html">Bexhill</a> and the surrounding Sussex coast and Weald. We will travel further for the right job — ask us.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 6. /office-removals-eastbourne (1200 words)
# ============================================================================
def office_removals():
    qas = [
        ("Can you move our office out-of-hours?", "Yes — evening, weekend and bank-holiday moves are a standard option. Many of our office customers move on a Friday evening / Saturday so they can start trading on Monday in the new premises."),
        ("How do you handle our IT equipment?", "Each workstation is labelled in advance with its destination floor, room and desk. We use anti-static bubble wrap for sensitive items and we transport in dedicated, climate-controlled compartments. We can also liaise with your IT team to coordinate disconnect and reconnect."),
        ("Are you insured for high-value office equipment?", "Yes. We carry full goods-in-transit insurance, and additional declared-value insurance is available for high-value equipment (servers, lab equipment, art collections). We will quote based on your declared inventory value."),
        ("Can you store office records during a fit-out?", "Yes — short and long-term document storage at our Prestige steel facility. We can also arrange GDPR-compliant secure destruction of old paper records via our partner."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("Office Removals", "office-removals-eastbourne.html")]),
        service_schema("Office and Commercial Removals Eastbourne",
                       "Business office moves in Eastbourne with minimal downtime. Out-of-hours moves, IT equipment, document storage.",
                       "Eastbourne"),
        faq_schema(qas),
    ]
    meta = {
        "title": "Office Removals Eastbourne | Commercial Moves | Mark Ratcliffe",
        "description": "Office and commercial removals in Eastbourne. Out-of-hours moves, IT equipment, minimal downtime. BAR-registered. Free site survey.",
        "url_rel": "office-removals-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; Office Removals</nav>
{hero("Office and Commercial Removals in Eastbourne", kicker="Minimal downtime · Out-of-hours options · IT-aware", image="images/business-people-shaking-hands-meeting-room.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Move your business without losing a day. Mark Ratcliffe Moving's office removal service in Eastbourne is built around minimising downtime — we move out-of-hours, label and map every workstation in advance, and handle IT equipment with the care it needs. We are BAR-registered, fully insured for goods in transit, and our crews have moved everything from two-person consultancies up to multi-floor regional offices.</p>
        <ul class="np-usp-list">
          <li>Out-of-hours moves — evenings, weekends, bank holidays</li>
          <li>Pre-move planning with floor plans and IT inventory</li>
          <li>Anti-static, label-and-map approach to workstations</li>
          <li>Furniture dismantling and reassembly included</li>
          <li>Document storage and GDPR-aware destruction available</li>
          <li>Single point of contact throughout the project</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Our commercial moving service</h2>

        <h3>Pre-move planning and site survey</h3>
        <p>Every office move starts with a site survey at both the origin and the destination. We map floor plans, count workstations, identify IT cabinets and server rooms, check lift access and parking restrictions, and discuss the timing window. The output is a project plan — typically a Gantt-style schedule from a few hours' work for a small office through to a phased move across multiple weekends for larger sites.</p>

        <h3>IT equipment handling</h3>
        <p>IT is where most office moves go wrong. We label every monitor, every PC, every cable bundle with its destination floor, room and desk number. Sensitive equipment is wrapped in anti-static bubble. Servers travel last and arrive first, in a dedicated van. We can coordinate with your IT team or your managed-service provider to schedule the disconnect-reconnect — or, for smaller offices, we can recommend a local IT partner.</p>

        <h3>Furniture dismantling and reassembly</h3>
        <p>Most modern office furniture — desks, partitions, storage cabinets, meeting-room tables — needs to be dismantled to fit through lifts and doorways. Our crews include experienced furniture fitters. We bring the right tools, we keep every fixing in labelled bags, and we reassemble at the destination.</p>

        <h3>Out-of-hours moves</h3>
        <p>The most common request: "we close at 6pm Friday, we open at 8am Monday — can you do the move in between?" Yes. Friday-evening / Saturday moves are our most common office pattern. Bank-holiday Mondays work well for longer moves.</p>

        <h3>Secure document handling</h3>
        <p>Paper records are a particular liability under UK GDPR. We can transport sealed file boxes between offices, transfer them into our Prestige steel storage for long-term retention, or arrange GDPR-compliant secure destruction via our partner with a certificate of destruction issued for each batch.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Industries we move</h2>
        <p>We have moved offices across many regulated and non-regulated sectors in Eastbourne and Sussex, including:</p>
        <ul>
          <li><strong>Solicitors and law firms</strong> — case-file handling under GDPR, client confidentiality</li>
          <li><strong>Dental and medical practices</strong> — patient-record handling, sensitive equipment</li>
          <li><strong>Accountancy and financial services</strong> — multi-screen workstation moves, document retention</li>
          <li><strong>Retail and showroom</strong> — stock transfers, display fittings, point-of-sale tech</li>
          <li><strong>Education and training</strong> — schools, training centres, classroom moves</li>
          <li><strong>Charities and not-for-profits</strong> — Sussex-based charities relocating between premises</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Project management — your single point of contact</h2>
        <p>Office moves involve a lot of moving parts: your facilities team, your IT team, the building manager at both ends, the landlord's representative, sometimes a fit-out contractor. We assign a single project lead from our team who takes on the coordination, runs the pre-move site visits, attends planning calls, and is on-site through the move itself. You deal with one person, not a different remover each time.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Pricing for office moves</h2>
        <p>Office removal pricing is based on volume of equipment, distance between premises, complexity of dismantle / reassemble, IT scope, and downtime tolerance (out-of-hours and bank-holiday work attracts a premium). We do not publish flat per-desk rates because it leads to under-quoting and bad outcomes for customers. Every office quote follows a site survey and is itemised — you see exactly what you are paying for.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 7. /house-clearance-eastbourne (1000 words)
# ============================================================================
def house_clearance():
    qas = [
        ("Are you licensed to remove waste?", "Yes. We are registered as an upper-tier waste carrier with the Environment Agency. You can ask for a copy of our registration certificate before booking."),
        ("Can you handle probate house clearance?", "Yes — sensitively. We work directly with executors and solicitors, agree what is to be retained for family, what is to be sold or donated, and what is to be disposed of. We can also arrange a probate valuation."),
        ("What happens to items I do not want?", "We sort: items that can be donated go to our charity partner, items that can be recycled go to the appropriate recycling stream, items with resale value can be auctioned, and only what remains goes to licensed waste."),
        ("Do you clear hoarder properties?", "Yes — we have experience of hoarder clearances and we approach them sensitively, without judgement. Allow longer for the sort and clearance. Hazardous biological waste, if present, is handled by a specialist partner."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("House Clearance", "house-clearance-eastbourne.html")]),
        service_schema("House Clearance Eastbourne",
                       "Compassionate, full-service house clearance in Eastbourne for probate, downsizing and end-of-tenancy.",
                       "Eastbourne"),
        faq_schema(qas),
    ]
    meta = {
        "title": "House Clearance Eastbourne | Furniture & Probate | Mark Ratcliffe",
        "description": "Compassionate, full-service house clearance in Eastbourne. Probate, downsizing and furniture removal. Licensed waste carriers. Free quote.",
        "url_rel": "house-clearance-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; House Clearance</nav>
{hero("House Clearance in Eastbourne — Done with Care", kicker="Probate · Downsizing · Licensed waste carrier")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">House clearance is often a difficult job done at a difficult time. Mark Ratcliffe Moving's clearance service in Eastbourne is built on the same family values as our removal business: we treat your home and the possessions inside it with respect, we sort carefully rather than skip-and-bin, and we work patiently with families, executors and solicitors. We are an Environment Agency upper-tier registered waste carrier, so everything we remove is handled legally and traceably.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>When you need our clearance service</h2>
        <ul>
          <li><strong>Probate clearance</strong> — after a bereavement, to ready a property for sale or transfer</li>
          <li><strong>Downsizing</strong> — moving into a smaller home and needing to thin out years of accumulated possessions</li>
          <li><strong>End of tenancy</strong> — landlords needing to clear and reset a rental property between tenants</li>
          <li><strong>Property sale preparation</strong> — clearing a home before it goes on the market</li>
          <li><strong>Garage, loft and outbuilding clearance</strong> — partial clearance, not the whole house</li>
          <li><strong>Hoarder property</strong> — sensitive, judgement-free clearance with longer time allowance</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>How our house clearance works</h2>

        <h3>Walk-through and fixed quote</h3>
        <p>We start with a free walk-through of the property — taking notes on volume, access, special items and any complications. You then receive a fixed-price written quote with no obligation. For probate clearances we can also identify items of resale value and recommend an auction route where appropriate.</p>

        <h3>Sort, retain, donate, recycle, dispose</h3>
        <p>On clearance day, our team works through the property room by room. Items earmarked for family are bagged separately and either delivered or stored. Items in good condition go to our charity partner. Recyclable materials go to the right recycling stream. Items with resale value can be set aside for auction. Only what genuinely cannot be reused is taken to licensed waste — and we provide a transfer note for it.</p>

        <h3>Licensed waste carrier</h3>
        <p>We are registered with the Environment Agency as an upper-tier waste carrier (registration available on request). Many one-person clearance operations are not — and using an unlicensed carrier can leave the property owner liable if waste is fly-tipped. Always ask for a registration number before booking any clearance company.</p>

        <h3>Same-day or scheduled clearance</h3>
        <p>For smaller jobs we can sometimes clear within a day or two. Larger probate clearances usually take two to four days depending on size and the time needed to sort sensitively.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Probate clearance with sensitivity</h2>
        <p>Probate is the most common reason families call us. We understand that a clearance after a bereavement is not just an administrative task — it is a moment of letting go. Our team works at the family's pace, with patience and care. We can:</p>
        <ul>
          <li>Work alongside executors and probate solicitors</li>
          <li>Identify items of possible value for a probate valuation</li>
          <li>Bag and store family-retained items at our Lower Dicker storage for collection</li>
          <li>Arrange auction or charity routes for the rest</li>
          <li>Issue waste transfer notes and a written completion record</li>
        </ul>
        <p>Many of our probate clients come to us through Sussex solicitors we have worked with for decades.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>What we donate versus dispose</h2>
        <p>Our default is to maximise donation and recycling and minimise landfill. Typical proportions on a domestic clearance run roughly 30% donate, 40% recycle, 20% reuse-or-auction, 10% landfill — though it varies considerably by property. We work with established Sussex charity partners (Hospice and other registered charities) and we keep the donation paperwork for executors who need it for accounts.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Pricing</h2>
        <p>House clearance pricing is based on volume (number of skip-equivalents), access at the property, special items (white goods, paints, chemicals, hazardous waste) and the level of sort required. As a guide, a 2-bedroom flat clearance typically runs £450–£800; a 3-bedroom semi £700–£1,400; a larger 4 or 5-bedroom probate clearance £1,200–£2,500. All quotes are itemised and fixed — no surprises on the day.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# 8. /european-removals-eastbourne (1200 words)
# ============================================================================
def european_removals():
    qas = [
        ("How long does a European removal take?", "From Eastbourne, France and the Netherlands typically deliver within 7–10 days; Spain and Portugal within 10–14; Italy and Germany 7–12; Scandinavia 10–14. Part-loads take longer than sole-loads."),
        ("Do I still need customs paperwork after Brexit?", "Yes. Even though the UK is no longer in the EU customs union, your possessions need an inventory packing list, valued inventory, and where applicable, Transfer of Residence relief paperwork to avoid being charged duty and VAT at the destination."),
        ("What is ToR1 / Transfer of Residence relief?", "ToR1 is the customs scheme that allows UK residents moving permanently to an EU country to import their personal effects without paying duty or VAT, provided they have owned the items for at least 6 months and will live in the destination for at least 12 months. We handle the paperwork."),
        ("Can I send my car to Europe with my furniture?", "Often yes — depending on container space and destination rules. We typically use a specialist car-shipping partner for vehicles and coordinate timing with the household goods shipment."),
        ("Are part-loads cheaper than sole-loads?", "Yes — significantly. A part-load (sharing container space) can be a third to a half the cost of a sole-use container for the same volume. The trade-off is timing flexibility — you fit around the consolidator's schedule."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Services", "removals-eastbourne.html"), ("European Removals", "european-removals-eastbourne.html")]),
        service_schema("European Removals Eastbourne",
                       "European removals from Eastbourne to France, Spain, Italy, Portugal and beyond. Customs documentation, ToR1 relief, part-loads, full-loads.",
                       "Europe"),
        faq_schema(qas),
    ]
    meta = {
        "title": "European Removals Eastbourne | France, Spain & EU Moves",
        "description": "European removals from Eastbourne to France, Spain, Italy, Portugal and beyond. Customs documentation, part-loads, full-loads. Free quote.",
        "url_rel": "european-removals-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="removals-eastbourne.html">Services</a> &rsaquo; European Removals</nav>
{hero("European Removals from Eastbourne", kicker="France · Spain · Italy · Portugal · the rest of Europe", image="images/mark-ratcliffe-sleeper-cab-removal-lorry.webp")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Mark Ratcliffe Moving is a specialist European mover from our Eastbourne and Lower Dicker base. Since 1982 we have arranged thousands of relocations between the UK and the European mainland — and post-Brexit, doing this properly matters more than ever, because the paperwork mistakes that used to cost a delay now cost duty and VAT. We are a BAR Overseas Group member with vetted destination agents across Europe and we handle the customs documentation end-to-end.</p>
        <ul class="np-usp-list">
          <li>BAR Overseas Group member — post-Brexit customs expertise</li>
          <li>Transfer of Residence (ToR1) relief paperwork prepared for you</li>
          <li>Sole-load (full container) or part-load (groupage) options</li>
          <li>Vetted destination agents throughout Europe</li>
          <li>Premium pad-wrap and export-grade packing</li>
          <li>Door-to-door service — Eastbourne to your new European address</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Post-Brexit European moves made simple</h2>
        <p>Before 2021, moving from the UK to Spain or France was largely just a long drive with the right paperwork in the cab. Today it involves a customs declaration on each side, T1 or T2 transit documents in some cases, and — for permanent relocations — a Transfer of Residence relief claim to avoid being charged import VAT and duty on your own possessions. Getting it wrong costs money and time. We handle all of this for you as standard.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>How our European removal service works</h2>

        <h3>Survey and quote</h3>
        <p>Free in-home or video survey to measure volume in cubic metres and itemise the contents. We then quote sole-load (you pay for a full vehicle) or part-load (you share space with other shipments going your way) — typically the latter saves significant money for smaller moves.</p>

        <h3>Pad-wrap and export packing</h3>
        <p>European shipments use our pad-wrap protection on furniture and export-grade packing for fragile items. The journey may be only a few days, but the loading, unloading and customs handling steps mean the goods are moved more times than a domestic move, so packing has to be more rigorous.</p>

        <h3>Sole-load or part-load</h3>
        <p>For a full 3-bedroom or larger house, a sole-load typically works out better — your possessions go direct from Eastbourne to your new address with no transhipment, usually in 4–8 days for nearby countries. For a smaller move (one or two rooms, a flat, or just specific items), a part-load is far cheaper and only takes a few days longer.</p>

        <h3>Customs documentation</h3>
        <p>We prepare the inventory packing list, valued inventory, ToR1 relief application (UK side), and the destination customs paperwork via our agent. You sign and we file. We chase the destination clearance so you do not have to.</p>

        <h3>Delivery and unpacking at destination</h3>
        <p>Our destination agent delivers, unpacks furniture into agreed rooms and removes the wrapping. Optional add-on services like reassembly of large furniture and box-by-box unpacking are available.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Popular European destinations from Eastbourne</h2>
        <div class="np-grid-2">
          <div class="np-card">
            <h3>France</h3>
            <p>Common destinations: Dordogne, Charente, Brittany, Normandy, Provence, the Cote d'Azur. Channel Tunnel or Dover-Calais ferry route. Typical 7–10 day delivery from Eastbourne.</p>
          </div>
          <div class="np-card">
            <h3>Spain</h3>
            <p>Costa Blanca, Costa del Sol, inland Andalucía, Catalonia, Balearics. Road transport via France for the mainland; ferry from the mainland for the Balearics. Typical 10–14 days.</p>
          </div>
          <div class="np-card">
            <h3>Italy</h3>
            <p>Northern Italy (Lombardy, Veneto), Tuscany, Lazio, Puglia. Typical 8–12 days from Eastbourne.</p>
          </div>
          <div class="np-card">
            <h3>Portugal</h3>
            <p>Algarve, Lisbon area, Porto. Typical 10–14 days. Popular for UK retirees post-Brexit using the D7 visa.</p>
          </div>
          <div class="np-card">
            <h3>Germany &amp; Netherlands</h3>
            <p>Frankfurt, Munich, Berlin, Amsterdam, the Hague. Typical 5–8 days. Common destinations for work relocations.</p>
          </div>
          <div class="np-card">
            <h3>Switzerland, Austria, Scandinavia</h3>
            <p>Specialist routes — Switzerland in particular has strict customs rules around used personal effects. Allow 10–14 days and budget more for paperwork.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Transfer of Residence (ToR1) customs relief explained</h2>
        <p>ToR1 is the EU customs scheme that allows people moving permanently to an EU country to bring their personal effects without paying duty or import VAT — provided certain conditions are met:</p>
        <ul>
          <li>You are moving your <strong>normal place of residence</strong> to the destination country</li>
          <li>You have <strong>owned and used</strong> the goods for at least 6 months</li>
          <li>You will <strong>live in the destination country</strong> for at least 12 months</li>
          <li>You file the ToR1 paperwork <strong>in advance</strong> of the goods arriving</li>
        </ul>
        <p>The cost of getting ToR1 wrong is typically 20–25% of the value of your possessions in import VAT and duty — a multi-thousand-pound penalty for missing paperwork. We file the ToR1 for every eligible customer as part of our service.</p>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


PAGES = [
    ("removals-eastbourne", removals_eastbourne),
    ("packing-services-eastbourne", packing_services),
    ("storage-eastbourne", storage_eastbourne),
    ("international-removals-eastbourne", international_removals),
    ("man-and-van-eastbourne", man_and_van),
    ("office-removals-eastbourne", office_removals),
    ("house-clearance-eastbourne", house_clearance),
    ("european-removals-eastbourne", european_removals),
]


def build_all():
    built = []
    for slug, func in PAGES:
        meta, body = func()
        html = render(meta, body)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        built.append(slug)
    print(f"Built {len(built)} service pages: {built}")


if __name__ == "__main__":
    build_all()
