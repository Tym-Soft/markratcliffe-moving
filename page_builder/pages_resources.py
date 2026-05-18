"""Resource pages: cost guide, moving checklist, FAQs."""
from template import (render, faq_schema, breadcrumbs_schema,
                       hero, render_faq_accordion, BASE_URL)
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"


# ============================================================================
# /removals-eastbourne-cost (1300 words)
# ============================================================================
def cost_guide():
    qas = [
        ("How much is the deposit?", "20% of the quoted price secures your move date. Balance is due on the day of completion. We accept bank transfer, card or cheque."),
        ("What if I add items on the day?", "Minor additions are usually absorbed. Significant additions (e.g. forgotten contents of an outbuilding) may be charged at our hourly rate. Always best to mention any uncertainty during the survey."),
        ("Are there hidden fuel surcharges?", "No. Our quotes are all-inclusive of fuel within our standard East Sussex service area. Long-distance moves include fuel in the quoted line item — no surprise add-ons."),
        ("Can I get a discount for an off-peak move?", "Often yes — Tuesday to Thursday in the middle of the month outside school holidays is our quietest time. Mention you have flexibility during the quote and we will tell you what we can do."),
    ]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Resources", ""), ("Cost Guide", "removals-eastbourne-cost.html")]),
        faq_schema(qas),
        {"@context": "https://schema.org", "@type": "Article",
         "headline": "How Much Do Removals Cost in Eastbourne? 2026 Price Guide",
         "author": {"@type": "Organization", "@id": f"{BASE_URL}/#organization"},
         "publisher": {"@type": "Organization", "@id": f"{BASE_URL}/#organization"},
         "datePublished": "2026-05-17", "dateModified": "2026-05-17"}
    ]
    meta = {
        "title": "How Much Do Removals Cost in Eastbourne? 2026 Price Guide",
        "description": "Eastbourne removals cost guide: typical prices, what affects them, and example quotes for studio to 4-bed moves. Honest, no obligation.",
        "url_rel": "removals-eastbourne-cost.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; Resources &rsaquo; Cost Guide</nav>
{hero("How Much Do Removals Cost in Eastbourne?", kicker="2026 Pricing Guide · Honest, no obligation")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Removal prices are one of the most-asked questions we get from Eastbourne customers — and one of the most opaque parts of the industry. This guide gives you honest, realistic 2026 pricing ranges for moves around Eastbourne and East Sussex, with the factors that drive them up or down. We publish guideline ranges, not headline "from £" prices, because every move is genuinely different and we believe you deserve a real number, not a marketing one.</p>
        <p><em>Prices last reviewed: May 2026. All amounts include VAT for domestic moves.</em></p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Typical price ranges for Eastbourne removals</h2>
        <table class="np-price-table">
          <thead>
            <tr><th>Property type</th><th>Local Eastbourne move</th><th>Move within East Sussex</th><th>Long-distance (UK)</th></tr>
          </thead>
          <tbody>
            <tr><td>Studio / 1-bed flat</td><td>£350 – £600</td><td>£450 – £700</td><td>£700 – £1,100</td></tr>
            <tr><td>2-bedroom home</td><td>£550 – £900</td><td>£700 – £1,100</td><td>£1,100 – £1,700</td></tr>
            <tr><td>3-bedroom home</td><td>£800 – £1,400</td><td>£1,000 – £1,700</td><td>£1,600 – £2,500</td></tr>
            <tr><td>4-bedroom home</td><td>£1,200 – £2,200</td><td>£1,500 – £2,600</td><td>£2,200 – £3,800</td></tr>
            <tr><td>5+ bedroom home</td><td>£1,800 – £3,500</td><td>£2,200 – £4,200</td><td>£3,000 – £6,000+</td></tr>
          </tbody>
        </table>
        <p>These ranges are guidelines based on standard moves in 2026. They assume reasonable access at both ends and no packing service. Add £350–£600 for full packing of a 3-bedroom home, or £150–£300 for fragile-only packing.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>What affects your removal cost</h2>

        <h3>Volume of belongings</h3>
        <p>The single biggest factor. Volume is measured in cubic feet during the survey — a typical 2-bedroom home is around 700 cu ft, a 3-bedroom 1,000–1,200 cu ft, a 4-bedroom 1,400–2,000 cu ft. More volume means more vehicle, more crew and more time.</p>

        <h3>Distance between properties</h3>
        <p>Within Eastbourne or East Sussex, the distance is rarely the dominant cost. For long-distance UK or international moves, distance becomes significant — both fuel and the labour-time the crew spends on the road.</p>

        <h3>Access at both properties</h3>
        <p>Restricted parking, narrow streets, long carries from the vehicle to the front door, lifts (especially small ones), tight stairwells, low ceilings and basements all add time. A 3-bedroom flat on the fourth floor with no lift can cost as much as a 5-bedroom house with driveway access.</p>

        <h3>Packing service</h3>
        <p>Self-pack is free; full packing for a 3-bedroom home typically adds £350–£600. Fragile-only packing is roughly half that. Materials are included in the quoted price.</p>

        <h3>Storage requirements</h3>
        <p>Storage is a separate monthly billing — typically £15–£40 per week depending on room size — and adds two transfer operations (in and out) which we charge as nominal labour.</p>

        <h3>Weekend / bank-holiday surcharges</h3>
        <p>Saturdays attract a small premium (10–15%); Sundays and bank holidays more. Many customers find a weekday move is cheaper and the crew is fresher.</p>

        <h3>Special items</h3>
        <p>Pianos, antiques, safes, hot tubs, fine art, motorbikes — each can need specialist handling, equipment or sub-contracted specialists. These are always quoted as a line item in the written quote.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>How we quote</h2>
        <p>Every Mark Ratcliffe move starts with a free survey — in your home, or by video call if you prefer. We walk through every room, agree what is moving and what is not, look at access at both ends, and discuss whether you want packing, storage, dismantling or any special-item handling. You receive an itemised written quote with absolutely no obligation, typically within 24 hours. There are no hidden fees, no fuel surcharges and no "from £" marketing prices.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Hidden costs to watch for with other firms</h2>
        <p>Comparing removal quotes is hard because firms structure them differently. Things to look for in any quote — including ours — before you sign:</p>
        <ul>
          <li><strong>Parking permit / suspension costs</strong> — sometimes included, sometimes extra</li>
          <li><strong>Dismantling and reassembly</strong> of beds, wardrobes, garden furniture</li>
          <li><strong>Stair surcharge</strong> per flight above the ground floor</li>
          <li><strong>Long carry surcharge</strong> from vehicle to front door over a certain distance</li>
          <li><strong>Fuel surcharge</strong> on long-distance moves</li>
          <li><strong>Waiting time</strong> for keys or other delays on completion day</li>
          <li><strong>Insurance excess</strong> if you need to claim</li>
          <li><strong>Cancellation fees</strong> if your purchase falls through</li>
        </ul>
        <p>Our quotes are all-inclusive within our published service area and we do not charge for postponements or cancellations.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Ways to keep your Eastbourne move affordable</h2>
        <ul>
          <li><strong>Move mid-week, mid-month, off-peak season.</strong> Tuesday-to-Thursday in the middle of the month between October and March is our cheapest slot.</li>
          <li><strong>Declutter first.</strong> Every cubic foot you do not move saves you money. Charity-shop donations or our charity-partner pickup are free.</li>
          <li><strong>Self-pack the easy items.</strong> Books, clothes and linen are easy to pack yourself; let us handle the fragile and breakable items.</li>
          <li><strong>Be flexible on the date.</strong> If your seller-buyer chain allows flexibility, we can sometimes offer a discount for filling a quieter slot in the diary.</li>
          <li><strong>Consider man-and-van for smaller moves.</strong> Studio and 1-bedroom moves are often cheaper as <a href="man-and-van-eastbourne.html">man and van</a> than as a full removal.</li>
        </ul>
      </div>
    </section>

{render_faq_accordion(qas)}
"""
    return meta, body


# ============================================================================
# /moving-checklist-eastbourne (1200 words)
# ============================================================================
def moving_checklist():
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Resources", ""), ("Moving Checklist", "moving-checklist-eastbourne.html")]),
        {"@context": "https://schema.org", "@type": "HowTo",
         "name": "The Eastbourne Moving House Checklist — 8 Weeks to Move Day",
         "description": "Free 8-week moving house checklist with tasks for every stage from 8 weeks before to after the move.",
         "datePublished": "2026-05-17"}
    ]
    meta = {
        "title": "Moving House Checklist Eastbourne | 8-Week Plan",
        "description": "Free 8-week moving house checklist for Eastbourne movers. Tasks for 8, 6, 4, 2, 1 weeks before, plus moving day and after.",
        "url_rel": "moving-checklist-eastbourne.html",
        "schemas": schemas,
    }
    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; Resources &rsaquo; Moving Checklist</nav>
{hero("The Eastbourne Moving House Checklist", kicker="8 weeks to move day · Save and share")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Moving house is one of the most stressful life events — but most of the stress comes from not knowing what to do when. We have built this 8-week Eastbourne moving checklist from the practical experience of helping families relocate across Sussex for over forty years. Work through it from the top and you will arrive on move day calmer, more organised and with fewer surprises.</p>
        <p><strong>Tip:</strong> bookmark this page or save it as a PDF on your phone. If you want it in printable form, ask us for a free PDF copy with your removal quote.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>8 weeks before — research and book</h2>
        <ul>
          <li>Confirm your move date (or expected window) with your conveyancer</li>
          <li>Decide on your removal approach: full service, man-and-van, or DIY hire</li>
          <li><strong>Request at least three written quotes</strong> from BAR-registered firms — including ours</li>
          <li>Book your <a href="removals-eastbourne.html">Eastbourne removal company</a> and pay the deposit to lock the date</li>
          <li>Start a moving folder (paper or digital) for documents, contacts, quotes and inventories</li>
          <li>Notify your landlord if renting; check notice periods and deposit-return procedures</li>
          <li>Start sorting belongings — what to keep, donate, sell or dispose of</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>6 weeks before — declutter and notify</h2>
        <ul>
          <li>Schedule charity-shop pickups for unwanted furniture and clothes</li>
          <li>List sellable items on eBay, Facebook Marketplace or Gumtree</li>
          <li>Take photos of valuable items and document any existing damage</li>
          <li>Notify schools, nurseries and after-school clubs of the move</li>
          <li>Start using up freezer food, tinned cupboard items and toiletries</li>
          <li>Order any packing materials you will need (we sell at our <a href="packaging-shop.html">Lower Dicker shop</a>)</li>
          <li>Book time off work for moving day and the day after</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>4 weeks before — change of address</h2>
        <ul>
          <li>Set up Royal Mail redirection (usually 3-6 months) — apply at the Post Office or online</li>
          <li>Notify banks, credit cards, pensions and insurance providers</li>
          <li>Update your driving licence and V5C log book with the DVLA</li>
          <li>Notify HMRC and update your details on the Government Gateway</li>
          <li>Inform doctor, dentist, optician and vet (transfer notes if needed)</li>
          <li>Tell utility suppliers — gas, electric, water, broadband, TV licence</li>
          <li>Cancel or transfer subscriptions: streaming, gym, magazines, milk delivery</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>2 weeks before — pack and organise</h2>
        <ul>
          <li>Start self-packing non-essential rooms — books, photos, off-season clothes</li>
          <li>Label every box with: room, contents, fragile flag, "open first" priority</li>
          <li>Pack a "moving day essentials" box: kettle, mugs, tea/coffee, biscuits, loo roll, chargers, basic toiletries, a change of clothes</li>
          <li>Confirm parking arrangements at both properties — apply for parking suspensions if needed</li>
          <li>Take final meter readings of gas, electric and water on moving day</li>
          <li>Defrost the freezer (start 48 hours before)</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>1 week before — final preparations</h2>
        <ul>
          <li>Confirm move-day arrangements with your removal company</li>
          <li>Finish packing everything except essentials</li>
          <li>Empty and clean the fridge and oven</li>
          <li>Take a photo of your old home's meter readings</li>
          <li>Withdraw cash for tips, parking, contingency</li>
          <li>Charge phones, cameras and power banks</li>
          <li>Confirm key handover times with your estate agent and solicitor</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>3 days before — final stretch</h2>
        <ul>
          <li>Final fridge and freezer clear — eat or donate remaining food</li>
          <li>Pack a separate box of medications, important documents, jewellery — these travel with you, not in the lorry</li>
          <li>Confirm pet arrangements (kennels, cattery, or trusted friend on the day)</li>
          <li>Set up the new utilities — book broadband installation for the new address</li>
          <li>Print or screenshot the new address and key collection details</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Moving day</h2>
        <ul>
          <li>Be ready and dressed before the crew arrives (typically 8–9am)</li>
          <li>Have the kettle accessible — offer drinks; it builds the relationship</li>
          <li>Walk the crew through the property and any items needing special care</li>
          <li>Keep valuables (jewellery, cash, documents, electronics) with you, not in the lorry</li>
          <li>Take final meter readings, photograph them with date and time visible</li>
          <li>Final walk-through to check nothing is left in cupboards, attic or shed</li>
          <li>Lock up and hand over keys per your solicitor's instructions</li>
          <li>Drive to the new address; arrive ahead of the lorry if possible</li>
          <li>Direct the crew where each piece of furniture and each box should go</li>
          <li>Walk through the inventory at the end; sign off only if you are happy</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>After the move</h2>
        <ul>
          <li>Take meter readings at the new property and report to suppliers</li>
          <li>Test smoke and CO alarms; replace batteries if needed</li>
          <li>Locate the stopcock, fuse box and gas isolation in your new home</li>
          <li>Register with new GP and dentist within the first week</li>
          <li>Register on the electoral roll at the new address</li>
          <li>Unpack one room at a time, starting with the kitchen and the main bedroom</li>
          <li>Recycle the cardboard — many local authorities offer free pickup; we will collect ours back at no charge</li>
          <li>If you stored items with us during the move, schedule your storage redelivery</li>
          <li>Write a thank-you review for your remover if they did well — it really helps small family businesses</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Want a printable PDF version?</h2>
        <p>Request your free Mark Ratcliffe Moving printable checklist as part of any quote — we will email a PDF that you can stick on the fridge for the duration of the move. Or call us on <a href="tel:01323848008">01323 848 008</a> and we will post one to you.</p>
      </div>
    </section>
"""
    return meta, body


# ============================================================================
# /faqs (1200 words)
# ============================================================================
def faqs():
    sections = [
        ("Booking & quotes", [
            ("How do I get a removal quote?", "Three ways: phone us on 01323 848 008, complete our online quote form, or request a free in-home or video survey. For accurate pricing we recommend the survey — it takes 30-45 minutes."),
            ("Is the quote binding?", "Yes. Once we have surveyed your home and issued a written quote, that price holds unless your inventory changes significantly. There are no hidden surcharges or fuel add-ons."),
            ("How long is a quote valid for?", "30 days from the date issued. If your move date is more than 30 days out, we can reissue or extend the quote."),
            ("What deposit do you require?", "20% of the quoted price secures your move date. Balance is payable on the day of completion."),
            ("Do you charge for the survey?", "No — all surveys are free with absolutely no obligation."),
        ]),
        ("On move day", [
            ("What time will the crew arrive?", "Typically 8:00–8:30am for a full day move. We will confirm a more precise window the day before."),
            ("Do I need to be there all day?", "Not necessarily — but it helps to be there at both ends to direct the crew on where things go. Many customers leave once loading is complete and meet the lorry at the destination."),
            ("What if my move-day parking is restricted?", "We arrange parking suspensions in advance for known restrictions. Mention this during the survey."),
            ("What happens if it rains?", "We move in all weathers. Pad-wrapping protects furniture from rain damage between the house and the lorry. We have waterproof covers for the loading area."),
            ("Should I pack the day before?", "For a full removal with our packing service — no, we pack on a pre-move day. For self-pack moves, yes — be packed the night before so the crew can load straight away."),
        ]),
        ("Packing & protection", [
            ("Do you supply boxes?", "Yes — included with the quoted packing service, or available to buy from our Lower Dicker packaging shop if you are self-packing."),
            ("Can I leave clothes in drawers?", "For lightweight items in sturdy drawer units, yes. For heavy items or fragile drawers we ask you to empty them."),
            ("Do you pack electronics?", "Yes. We are trained to handle TVs, computers and sound systems. Original boxes are best where you have them."),
            ("What does pad-wrap actually mean?", "Every piece of furniture is individually wrapped in a thick quilted blanket inside your home, taped, labelled, then carried to the lorry. It is only unwrapped once it has been placed in its final position in your new home."),
        ]),
        ("Storage", [
            ("How are your storage rooms different from a self-storage warehouse?", "Each customer has their own individual steel-walled room rather than a shelf or cage inside a shared warehouse. 24-hour CCTV, alarmed access."),
            ("What is the minimum storage term?", "Four weeks. After that you pay month-by-month with no long contract and no early-exit fees."),
            ("Can I access my storage room?", "Yes — by appointment during depot hours, normally with 24-hour notice."),
            ("Is my stored property insured?", "Storage insurance is available as an add-on and strongly recommended. We arrange cover through our broker."),
        ]),
        ("International", [
            ("How long does an international removal take?", "Air freight to Europe is 5-10 days door to door. Sea freight to Australia, USA or Thailand is 6-12 weeks. We give a more accurate window once we know destination and volume."),
            ("Do you handle customs paperwork?", "Yes — inventory packing list, valued inventory, customs declarations and Transfer of Residence (ToR1) paperwork are all prepared by us."),
            ("Can you ship to Thailand?", "Yes — UK to Thailand is one of our specialist routes. We ship regularly to Bangkok, Pattaya, Phuket and Chiang Mai."),
            ("What can't I ship internationally?", "Most countries prohibit firearms, explosives, narcotics, certain plants and seeds, ivory, and some food items. Many restrict alcohol and electronics. We provide a destination-specific list."),
        ]),
        ("Costs & payment", [
            ("How and when do I pay the balance?", "Balance is due on the day of completion. We accept bank transfer (faster payments), card or cheque."),
            ("What if my move date changes?", "No charge for postponements, cancellations or key waits. We simply update the diary at no extra cost."),
            ("Are tips for the crew expected?", "Tips are entirely optional and never expected. If your crew has gone above and beyond, a tip is appreciated — many customers offer £10-20 per person at the end of a good move."),
            ("Do you offer payment plans?", "For larger or international moves we can sometimes split the balance — speak to us during the quote process."),
        ]),
    ]
    all_qas = [qa for _, qas in sections for qa in qas]
    schemas = [
        breadcrumbs_schema([("Home", ""), ("FAQs", "faqs.html")]),
        faq_schema(all_qas),
    ]
    meta = {
        "title": "Removals & Storage FAQs | Mark Ratcliffe Moving Eastbourne",
        "description": "Common questions about Eastbourne removals, storage, packing and international moves. Honest answers from a family-run BAR-registered mover.",
        "url_rel": "faqs.html",
        "schemas": schemas,
    }

    sections_html = ""
    for i, (title, qas) in enumerate(sections):
        bg = " np-section-soft" if i % 2 == 0 else ""
        sections_html += f"""    <section class="np-section{bg}">
      <div class="np-inner">
        <h2>{title}</h2>
"""
        for q, a in qas:
            sections_html += f'        <details class="np-faq-item" style="margin-bottom:0.65rem;background:#fff;border:1px solid var(--np-border);border-radius:6px;padding:0.85rem 1.1rem;"><summary style="font-weight:600;cursor:pointer;color:var(--np-primary);">{q}</summary><p style="margin-top:0.75rem;">{a}</p></details>\n'
        sections_html += "      </div>\n    </section>\n"

    body = f"""  <nav class="np-breadcrumb"><a href="index.html">Home</a> &rsaquo; FAQs</nav>
{hero("Frequently Asked Questions", kicker="Honest answers from a family-run mover")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">These are the questions we get asked most often by Eastbourne, Hailsham and Sussex customers. If your question is not here, give us a call on <a href="tel:01323848008">01323 848 008</a> or email <a href="mailto:mark@markratcliffemoving.co.uk">mark@markratcliffemoving.co.uk</a> — we are happy to help.</p>
      </div>
    </section>

{sections_html}
"""
    return meta, body


PAGES = [
    ("removals-eastbourne-cost", cost_guide),
    ("moving-checklist-eastbourne", moving_checklist),
    ("faqs", faqs),
]


def build_all():
    built = []
    for slug, func in PAGES:
        meta, body = func()
        html = render(meta, body)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        built.append(slug)
    print(f"Built {len(built)} resource pages: {built}")


if __name__ == "__main__":
    build_all()
