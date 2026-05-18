"""Blog hub + 3 starter posts."""
from template import (render, faq_schema, breadcrumbs_schema,
                       hero, render_faq_accordion, BASE_URL, TODAY)
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"
BLOG_DIR = OUT / "blog"
BLOG_DIR.mkdir(exist_ok=True)


POSTS = [
    {
        "slug": "moving-house-checklist-eastbourne",
        "title": "Moving House Checklist for Eastbourne Movers — 8-Week Plan",
        "h1": "The Ultimate Moving House Checklist for Eastbourne Movers",
        "description": "Free 8-week moving house checklist from Eastbourne's family-run removal company. Week-by-week tasks from booking to move day.",
        "category": "Moving Tips",
        "excerpt": "An honest 8-week countdown — the tasks that actually matter, in the order our crews tell their own families to tackle them.",
        "hero_image": "images/mark-ratcliffe-crew-loading-piano-eastbourne.webp",
    },
    {
        "slug": "how-to-pack-fragile-items",
        "title": "How to Pack Fragile Items for a House Move — Pad-Wrap Pros",
        "h1": "How to Pack Fragile Items Safely for a House Move",
        "description": "Learn how to pack fragile items properly for a house move — china, glass, electronics, art, mirrors. Advice from BAR-trained packers.",
        "category": "Packing",
        "excerpt": "Forty years of pad-wrapping experience distilled into a practical fragile-packing guide you can do at home.",
        "hero_image": "images/pad-wrapped-furniture-eastbourne-removals.webp",
    },
    {
        "slug": "choosing-a-removal-company-eastbourne",
        "title": "How to Choose a Removal Company in Eastbourne — 10 Checks",
        "h1": "How to Choose a Removal Company in Eastbourne",
        "description": "Ten checks to make before booking your Eastbourne removal company. BAR membership, insurance, reviews, quote transparency and more.",
        "category": "Choosing a Mover",
        "excerpt": "Not all removal firms are equal. Here are the ten checks that separate a safe choice from a stressful one.",
        "hero_image": "images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp",
    },
]


def blog_post_schema(post):
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "author": {"@type": "Organization", "@id": f"{BASE_URL}/#organization"},
        "publisher": {"@type": "Organization", "@id": f"{BASE_URL}/#organization"},
        "datePublished": TODAY,
        "dateModified": TODAY,
        "image": f"{BASE_URL}/{post['hero_image']}",
        "mainEntityOfPage": f"{BASE_URL}/blog/{post['slug']}.html",
    }


# ============================================================================
# /blog/index.html — hub
# ============================================================================
def blog_hub():
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Blog", "blog/index.html")]),
        {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Mark Ratcliffe Moving Blog",
            "description": "Removals tips, packing guides and storage advice from Eastbourne's family-run movers since 1982.",
            "url": f"{BASE_URL}/blog/index.html",
            "publisher": {"@type": "Organization", "@id": f"{BASE_URL}/#organization"},
        },
    ]
    meta = {
        "title": "Removals & Moving Tips Blog | Mark Ratcliffe Moving Eastbourne",
        "description": "Expert removals advice, moving checklists and storage guides from Mark Ratcliffe Moving — Eastbourne's family-run movers since 1982.",
        "url_rel": "blog/index.html",
        "schemas": schemas,
    }

    cards = ""
    for post in POSTS:
        cards += f"""          <article class="np-blog-card">
            <img src="../{post['hero_image']}" alt="{post['title']}" loading="lazy" decoding="async" width="600" height="360">
            <div class="np-blog-card-body">
              <div class="np-blog-card-meta">{post['category']} · {TODAY}</div>
              <h3><a href="{post['slug']}.html">{post['h1']}</a></h3>
              <p>{post['excerpt']}</p>
              <a href="{post['slug']}.html"><strong>Read more &rarr;</strong></a>
            </div>
          </article>
"""

    # Need to patch all relative links in hub since it's inside /blog/
    # We'll rewrite later via a fix-up; for now use ../ prefix in body links
    body = f"""  <nav class="np-breadcrumb"><a href="../index.html">Home</a> &rsaquo; Blog</nav>
{hero("The Mark Ratcliffe Moving Blog", kicker="Removals tips · Packing guides · Storage advice")}

    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Welcome to our blog. We have been moving Eastbourne and Sussex families since 1982 — over the years we have packed more crystal, wrapped more mahogany and survived more last-minute completion-date changes than we can count. This is where we share what we have learned. Every article is written by the team that does the work, not a marketing agency.</p>
        <p>To start with we have published three guides covering the most common questions we get asked: a full 8-week moving checklist, a fragile-item packing guide, and a checklist for choosing the right removal company in Eastbourne. More posts are on the way.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Latest articles</h2>
        <div class="np-blog-grid">
{cards}        </div>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Browse by category</h2>
        <ul>
          <li><strong>Moving Tips</strong> — getting organised, what to do when</li>
          <li><strong>Packing</strong> — pad-wrap, fragile items, materials</li>
          <li><strong>Storage</strong> — using our Prestige steel rooms</li>
          <li><strong>International</strong> — Thailand, Europe, post-Brexit customs</li>
          <li><strong>Cost &amp; Quotes</strong> — honest pricing guidance</li>
          <li><strong>Choosing a Mover</strong> — what to look for, what to avoid</li>
        </ul>
      </div>
    </section>
"""
    html = render(meta, body)
    # Fix relative paths since this page lives in /blog/
    html = html.replace('href="css/', 'href="../css/')
    html = html.replace('src="images/', 'src="../images/')
    html = html.replace('href="images/', 'href="../images/')
    html = html.replace('href="index.html"', 'href="../index.html"')
    html = html.replace('href="about-us.html"', 'href="../about-us.html"')
    html = html.replace('href="contact-us.html"', 'href="../contact-us.html"')
    html = html.replace('href="testimonials.html"', 'href="../testimonials.html"')
    html = html.replace('href="thai-moving-services.html"', 'href="../thai-moving-services.html"')
    html = html.replace('href="terms-conditions-and-insurance-details.html"', 'href="../terms-conditions-and-insurance-details.html"')
    html = html.replace('href="mark-ratcliffe-moving-online-removals-quote.html"', 'href="../mark-ratcliffe-moving-online-removals-quote.html"')
    html = html.replace('href="removals-eastbourne.html"', 'href="../removals-eastbourne.html"')
    html = html.replace('href="hailsham-removals.html"', 'href="../hailsham-removals.html"')
    html = html.replace('href="removals-polegate.html"', 'href="../removals-polegate.html"')
    html = html.replace('href="removals-pevensey.html"', 'href="../removals-pevensey.html"')
    html = html.replace('href="removals-willingdon.html"', 'href="../removals-willingdon.html"')
    html = html.replace('href="removals-uckfield.html"', 'href="../removals-uckfield.html"')
    html = html.replace('href="removals-heathfield.html"', 'href="../removals-heathfield.html"')
    html = html.replace('href="removals-bexhill.html"', 'href="../removals-bexhill.html"')
    html = html.replace('href="man-and-van-eastbourne.html"', 'href="../man-and-van-eastbourne.html"')
    html = html.replace('href="packing-services-eastbourne.html"', 'href="../packing-services-eastbourne.html"')
    html = html.replace('href="office-removals-eastbourne.html"', 'href="../office-removals-eastbourne.html"')
    html = html.replace('href="house-clearance-eastbourne.html"', 'href="../house-clearance-eastbourne.html"')
    html = html.replace('href="international-removals-eastbourne.html"', 'href="../international-removals-eastbourne.html"')
    html = html.replace('href="european-removals-eastbourne.html"', 'href="../european-removals-eastbourne.html"')
    html = html.replace('href="storage-eastbourne.html"', 'href="../storage-eastbourne.html"')
    html = html.replace('href="moving-checklist-eastbourne.html"', 'href="../moving-checklist-eastbourne.html"')
    html = html.replace('href="removals-eastbourne-cost.html"', 'href="../removals-eastbourne-cost.html"')
    html = html.replace('href="faqs.html"', 'href="../faqs.html"')
    html = html.replace('href="areas-covered.html"', 'href="../areas-covered.html"')
    html = html.replace('href="blog/index.html"', 'href="index.html"')
    return html


# ============================================================================
# Blog post bodies
# ============================================================================
def blog_post_body(post, body_html):
    schemas = [
        breadcrumbs_schema([("Home", ""), ("Blog", "blog/index.html"), (post["title"], f"blog/{post['slug']}.html")]),
        blog_post_schema(post),
    ]
    meta = {
        "title": post["title"],
        "description": post["description"],
        "url_rel": f"blog/{post['slug']}.html",
        "schemas": schemas,
        "og_image": f"{BASE_URL}/{post['hero_image']}",
    }
    cat = post["category"]
    breadcrumb = f'<nav class="np-breadcrumb"><a href="../index.html">Home</a> &rsaquo; <a href="index.html">Blog</a> &rsaquo; {cat}</nav>'
    kicker_text = f"{cat} · Published {TODAY}"
    hero_img = '../' + post['hero_image']
    full_body = f"  {breadcrumb}\n{hero(post['h1'], kicker=kicker_text, image=hero_img)}\n{body_html}"
    html = render(meta, full_body)
    # Fix CSS/image paths and nav links for /blog/ subdir
    fixes = [
        ('href="css/', 'href="../css/'),
        ('src="images/', 'src="../images/'),
        ('href="images/', 'href="../images/'),
        ('href="index.html"', 'href="../index.html"'),
        ('href="about-us.html"', 'href="../about-us.html"'),
        ('href="contact-us.html"', 'href="../contact-us.html"'),
        ('href="testimonials.html"', 'href="../testimonials.html"'),
        ('href="thai-moving-services.html"', 'href="../thai-moving-services.html"'),
        ('href="terms-conditions-and-insurance-details.html"', 'href="../terms-conditions-and-insurance-details.html"'),
        ('href="mark-ratcliffe-moving-online-removals-quote.html"', 'href="../mark-ratcliffe-moving-online-removals-quote.html"'),
        ('href="removals-eastbourne.html"', 'href="../removals-eastbourne.html"'),
        ('href="hailsham-removals.html"', 'href="../hailsham-removals.html"'),
        ('href="removals-polegate.html"', 'href="../removals-polegate.html"'),
        ('href="removals-pevensey.html"', 'href="../removals-pevensey.html"'),
        ('href="removals-willingdon.html"', 'href="../removals-willingdon.html"'),
        ('href="removals-uckfield.html"', 'href="../removals-uckfield.html"'),
        ('href="removals-heathfield.html"', 'href="../removals-heathfield.html"'),
        ('href="removals-bexhill.html"', 'href="../removals-bexhill.html"'),
        ('href="man-and-van-eastbourne.html"', 'href="../man-and-van-eastbourne.html"'),
        ('href="packing-services-eastbourne.html"', 'href="../packing-services-eastbourne.html"'),
        ('href="office-removals-eastbourne.html"', 'href="../office-removals-eastbourne.html"'),
        ('href="house-clearance-eastbourne.html"', 'href="../house-clearance-eastbourne.html"'),
        ('href="international-removals-eastbourne.html"', 'href="../international-removals-eastbourne.html"'),
        ('href="european-removals-eastbourne.html"', 'href="../european-removals-eastbourne.html"'),
        ('href="storage-eastbourne.html"', 'href="../storage-eastbourne.html"'),
        ('href="moving-checklist-eastbourne.html"', 'href="../moving-checklist-eastbourne.html"'),
        ('href="removals-eastbourne-cost.html"', 'href="../removals-eastbourne-cost.html"'),
        ('href="faqs.html"', 'href="../faqs.html"'),
        ('href="areas-covered.html"', 'href="../areas-covered.html"'),
        ('href="blog/index.html"', 'href="index.html"'),
    ]
    for old, new in fixes:
        html = html.replace(old, new)
    return html


def post_moving_checklist():
    body = """    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Moving house is consistently ranked among the most stressful life events. Most of that stress comes from not knowing what to do when. We have built this 8-week checklist from forty years of Eastbourne removals — the order in which we tell our own families to do things.</p>
        <p>The hidden truth about moving stress is that 80% of it is concentrated in the final two weeks, almost entirely because customers leave decisions and admin until then. If you start eight weeks before — even loosely — those final two weeks become calm. If you start two weeks before, the final two weeks are chaos. This checklist is structured around that observation.</p>
        <p>One more practical note: if your move date is uncertain (still subject to a property chain), use this checklist anyway. Treat the date as a target. The administrative steps still need doing; the packing steps are easy to adjust. Better to be ready three weeks early than three days late.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>8 weeks before</h2>
        <p>This is the planning window. The earlier you start, the calmer the next eight weeks will be.</p>
        <ul>
          <li>Confirm your target move date with your conveyancer (even if it later slips)</li>
          <li>Decide on the right service: <a href="../removals-eastbourne.html">full removal</a>, <a href="../man-and-van-eastbourne.html">man and van</a>, or DIY van hire</li>
          <li>Get three written quotes from <strong>BAR-registered</strong> firms — we are one of them</li>
          <li>Book your remover and pay the deposit to lock the date</li>
          <li>Start a moving folder for documents, contacts and inventories</li>
          <li>Begin sorting: keep, donate, sell, dispose</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>6 weeks before</h2>
        <ul>
          <li>Schedule charity pickups for unwanted furniture</li>
          <li>List sellable items on eBay or Facebook Marketplace</li>
          <li>Photograph valuable items and any existing damage</li>
          <li>Notify schools and after-school clubs</li>
          <li>Begin using up freezer food and pantry items</li>
          <li>Order packing materials if self-packing</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>4 weeks before — change of address</h2>
        <p>The single biggest cause of post-move stress is missed change-of-address notifications. Tackle this in one focused session.</p>
        <ul>
          <li>Set up Royal Mail redirection (3-6 months)</li>
          <li>Banks, credit cards, pensions, insurance</li>
          <li>DVLA — driving licence and V5C log book</li>
          <li>HMRC via the Government Gateway</li>
          <li>Doctor, dentist, optician, vet</li>
          <li>Utility suppliers — gas, electric, water, broadband</li>
          <li>Cancel subscriptions you no longer need</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>2 weeks before</h2>
        <ul>
          <li>Start self-packing non-essential rooms — books, photos, off-season clothes</li>
          <li>Label every box with room, contents, fragile flag, and an "open first" priority</li>
          <li>Pack a moving-day essentials box (kettle, mugs, tea, chargers, toiletries)</li>
          <li>Confirm parking at both properties — apply for suspensions if needed</li>
          <li>Defrost the freezer (start 48 hours before)</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>1 week before</h2>
        <ul>
          <li>Confirm move-day arrangements with your remover</li>
          <li>Finish packing everything except essentials</li>
          <li>Empty and clean the fridge and oven</li>
          <li>Photograph your old meters with date visible</li>
          <li>Withdraw cash for tips, parking and contingency</li>
          <li>Charge phones, cameras and power banks</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>3 days before</h2>
        <ul>
          <li>Empty the fridge and freezer</li>
          <li>Pack a separate box of medications, important documents and jewellery — these travel with you, not in the lorry</li>
          <li>Confirm pet arrangements</li>
          <li>Print or screenshot the new address and key collection details</li>
        </ul>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Moving day</h2>
        <ul>
          <li>Be ready and dressed before the crew arrives (8-9am typically)</li>
          <li>Offer drinks — build the relationship</li>
          <li>Walk the crew through the property and any items needing special care</li>
          <li>Keep valuables with you, not in the lorry</li>
          <li>Take final meter readings, photograph them</li>
          <li>Final walk-through — check cupboards, attic and shed</li>
          <li>Drive to the new address; arrive ahead of the lorry if possible</li>
          <li>Direct the crew where each piece goes</li>
          <li>Sign off only when you are happy</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>After the move</h2>
        <ul>
          <li>Take meter readings at the new property</li>
          <li>Test smoke and CO alarms</li>
          <li>Locate the stopcock, fuse box and gas isolation</li>
          <li>Register with new GP and dentist within the first week</li>
          <li>Register on the electoral roll</li>
          <li>Unpack one room at a time — kitchen and main bedroom first</li>
          <li>Recycle the cardboard — we will collect ours back at no charge</li>
          <li>Leave a review for your remover if they did well</li>
        </ul>
        <p>For a printable PDF version, request one with any <a href="../mark-ratcliffe-moving-online-removals-quote.html">quote</a> — we will email it to you.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>The five most common moving day problems — and how to avoid them</h2>
        <p>Over 40 years we have seen the same problems happen on move days again and again. None of them are catastrophic on their own, but together they turn a normal move into a stressful one. Plan around these five and your move day will run much more smoothly.</p>
        <p><strong>Problem 1: Keys not ready at the new property.</strong> Your seller's solicitor confirms keys at 1pm, then it slips to 2pm, then 3.30pm. Your lorry sits outside the new home for two hours. Mitigation: build a 2-hour key-delay buffer into your move plan, and ask if you can drop the lorry at the seller's solicitor's office or a neighbour's drive in the meantime.</p>
        <p><strong>Problem 2: Parking obstructed at one end.</strong> Even with parking suspensions in place, builders' vans, school-run cars and bin lorries appear on the day. Mitigation: arrive at both addresses 30 minutes before the lorry to physically hold the parking space if needed.</p>
        <p><strong>Problem 3: Stuff still in cupboards / attic / shed.</strong> The "I will pack that on the day" items that did not get packed. Mitigation: schedule a final walk-through the evening before, with a torch, and pack anything unmissed.</p>
        <p><strong>Problem 4: Lost paperwork.</strong> Your solicitor calls to ask for the EPC and you cannot find it. Mitigation: photograph every important document to phone-cloud storage at the 2-week-before stage. Originals can travel with the loose-papers box.</p>
        <p><strong>Problem 5: Children and pets underfoot.</strong> A 4-year-old at an active move site is a hazard. Mitigation: arrange childcare or a relative's house for move day. Same for pets — kennels or a friend's house, returned to you that evening.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Your post-move 30-day priority list</h2>
        <p>The first month after a move is when most "we will sort that out" tasks slip and then never get done. Use this 30-day list to keep momentum:</p>
        <ul>
          <li><strong>Day 1–3:</strong> Set up beds, kitchen and bathroom. These three rooms make a house feel like home faster than anything else.</li>
          <li><strong>Day 4–7:</strong> Register with new GP and dentist. Inform DVLA. Update the electoral roll.</li>
          <li><strong>Day 8–14:</strong> Unpack non-essential rooms. Hang pictures and put up shelves while you remember where things go.</li>
          <li><strong>Day 15–21:</strong> Tackle the garage, loft and shed. These are the boxes that never get unpacked otherwise.</li>
          <li><strong>Day 22–30:</strong> Final tidy. Recycle remaining cardboard (we will collect ours back free of charge). Write a review for your remover.</li>
        </ul>
        <p>If you have any questions about your upcoming move in Eastbourne or East Sussex, give us a call on <a href="tel:01323848008">01323 848 008</a>. We are always happy to share practical advice — even if you have not decided whether to use us yet.</p>
      </div>
    </section>
"""
    return body


def post_fragile_packing():
    body = """    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Fragile packing is where DIY moves usually go wrong. Most damage we see when a customer brings a job to us mid-move is from under-packed china or improperly wrapped art. Here is what forty years of pad-wrapping has taught us about packing fragile items safely.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>The materials that actually matter</h2>
        <ul>
          <li><strong>Triple-wall cartons</strong> — single-wall cardboard collapses under stack pressure. Triple-wall is what we use for kitchen and book boxes.</li>
          <li><strong>Bubble wrap</strong> — anti-static for electronics; standard bubble wrap for everything else. Three layers minimum for valuable items.</li>
          <li><strong>Archival tissue paper</strong> — for direct contact with china, fine art and antiques. Newspaper ink transfers and stains.</li>
          <li><strong>Packing paper / butcher paper</strong> — to fill voids inside boxes and prevent movement.</li>
          <li><strong>Strong tape</strong> — 50mm wide minimum. Cheap tape lets boxes burst open in the lorry.</li>
        </ul>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>How to pack china and ceramics</h2>
        <p>Stack vertically, not flat. Plates take far more impact load on their edges than their faces. Wrap each plate in archival tissue, then bundle three or four together, then bubble-wrap the bundle, then place on its edge (not flat) in a sturdy carton with crumpled paper in the bottom.</p>
        <p>Bowls and cups nest inside each other separated by tissue — but never stack more than three. Teapots and serving dishes go individually wrapped with the spout / handle separately padded.</p>

        <h2>How to pack glass and crystal</h2>
        <p>Stemware (wine glasses, champagne flutes) is the easiest thing to break and the easiest to pack well. Stuff the bowl loosely with tissue (do not compress — it acts as a shock absorber), wrap the entire glass in bubble wrap, then stand <em>upright</em> in a divided wine box. Never lay stemware on its side.</p>
        <p>Cut crystal and antique glass needs an extra layer — wrap in tissue, then bubble wrap, then individually box, then place in a larger box with padding around each individual box.</p>

        <h2>How to pack electronics</h2>
        <p>Original packaging is best where you have it. If not, use anti-static bubble wrap (the pink stuff) for anything with circuitry. Photograph the back of each device before disconnecting cables — saves an hour of head-scratching at the other end.</p>
        <p>TVs need a corner-padded carton. Computers travel best in their original or equivalent-spec boxes. Loose cables go in zip-lock bags labelled with the device they belong to.</p>

        <h2>How to pack art and mirrors</h2>
        <p>Anything framed and over A3 size needs a custom timber crate or, at minimum, two layers of bubble wrap then a flat cardboard slip-cover taped shut. Mirrors and glass-fronted art need an X of masking tape across the face — it does not prevent breakage, but it holds the shards together if the worst happens.</p>
        <p>For valuable art, our advice is to insure it specifically (your contents policy may exclude it during transit) and to use a specialist art shipper if the value is high.</p>

        <h2>How to pack lamps and lighting</h2>
        <p>Take the shade off, wrap separately, then box the shade with crumpled paper to hold its shape. The base — wrap the bulb area in bubble wrap, secure the cable to the base with tape, then stand upright in a box of similar lamps with padding between them.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>The pad-wrap method for furniture</h2>
        <p>This is what makes the biggest difference, and it is the thing DIY movers most often skip. <strong>Every piece of furniture should be wrapped in a quilted blanket before it leaves the room.</strong> Not the lorry. The room. The reason: it is the corners and edges of furniture that get chipped, and they get chipped on doorways, banisters, walls and other furniture during the carry to the vehicle — not in the lorry.</p>
        <p>If you cannot get pad-wrap blankets (or "removal blankets" / "moving pads" as they are sometimes called), use heavy duvets or old curtains as a substitute. Tape them on with painter's tape (which does not damage the furniture finish).</p>
        <figure class="np-image-block">
          <img src="../images/pad-wrapped-furniture-eastbourne-removals.webp" width="900" height="675" alt="Furniture being pad-wrapped before an Eastbourne home removal" loading="lazy" decoding="async">
          <figcaption>Pad-wrapping is the single biggest difference between a damaged move and a clean move.</figcaption>
        </figure>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>When to call us instead</h2>
        <p>Honestly, the maths is simple. For a 3-bedroom Eastbourne house with a significant fragile inventory, full packing typically adds £350-£600 to a removal quote — and you get triple-wall cartons, anti-static bubble, archival tissue, custom crates for awkward items, BAR-trained packers and a couple of days back in your life. For most customers that maths works.</p>
        <p>If you would rather pack yourself, you can buy all the materials from our <a href="../packaging-shop.html">Lower Dicker packaging shop</a> — and you can ask the crew on the day for advice on anything you are unsure about.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Specific guidance for the trickiest fragile items</h2>
        <p>Beyond the general principles, here is item-by-item guidance for the things that most often arrive damaged in self-packed moves.</p>
        <h3>Grandfather clocks</h3>
        <p>The pendulum and weights are removed first, wrapped separately and packed in a clearly labelled box. The clock case is pad-wrapped. If the case is glass-fronted, an X of masking tape across the glass holds shards together if the worst happens. Never lay a grandfather clock on its side — always upright in transit, even if it makes loading harder.</p>
        <h3>Marble and granite worktops or table tops</h3>
        <p>Vertical only, never flat. Marble can crack under its own weight if laid flat across a gap. We wrap in pad-blanket plus corrugated cardboard, then transport standing on a long edge in a custom crate.</p>
        <h3>Pianos</h3>
        <p>This is one to leave to specialists — including us. Pianos have specific pivot points, fragile internal components and weight distributions that are unforgiving of amateur lifting. Even moving a piano 10 metres within a house can damage it if done wrong. Always book a piano move (whether part of a removal or stand-alone) with a firm that has done it before.</p>
        <h3>Antique furniture with veneer or marquetry</h3>
        <p>Heat and humidity cycling causes veneer to lift. Pad-wrap thoroughly to maintain a stable micro-climate during transit. For long-term storage, our Prestige steel rooms are climate-stable, which is why they suit antiques better than communal warehouse storage.</p>
        <h3>Plates, particularly fine china</h3>
        <p>Recap: vertical, on edge, in dish-pack cartons with internal dividers. Wrap each plate in archival tissue first (newspaper transfers ink). Bundle three or four together with bubble wrap, then stand on edge in the carton. Pack crumpled paper around the bundles to fill voids. Mark the box FRAGILE and THIS WAY UP.</p>
        <h3>Outdoor sculptures and stone garden ornaments</h3>
        <p>Often heavier than they look. Padded blankets plus straps, lifted with the legs not the back, transported in a position that minimises stress on narrow points. Some stone (sandstone particularly) is genuinely fragile and we recommend professional handling.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>When to declare value and when to insure separately</h2>
        <p>Standard goods-in-transit insurance covers most household contents up to typical limits. But certain items need separate consideration:</p>
        <ul>
          <li><strong>Single items over £2,500.</strong> Declare these specifically on your removal contract and ensure they appear on the insurance schedule.</li>
          <li><strong>Fine art and antiques over £5,000.</strong> Best handled with a specialist art insurer; standard removal insurance may have valuation limits.</li>
          <li><strong>Cash, jewellery, important documents.</strong> Never put in the removal lorry — travel with you in your own vehicle. Standard policies typically exclude these.</li>
          <li><strong>Collections (wine, watches, coins, stamps).</strong> Often need a specialist collections policy. Tell us during the survey if you have collections worth more than £10,000.</li>
        </ul>
        <p>If you have any high-value or unusual items, mention them at survey stage — we can advise on packing, transport and insurance. The cost of getting this right is small; the cost of getting it wrong can be life-changing.</p>
      </div>
    </section>
"""
    return body


def post_choosing_remover():
    body = """    <section class="np-section">
      <div class="np-inner">
        <p style="font-size:1.15rem;">Booking the wrong removal company is one of the costlier mistakes you can make during a house move. Here are the ten checks we recommend running on any firm — including us — before you sign a contract or pay a deposit.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>1. BAR membership</h2>
        <p>The British Association of Removers is the industry's main trade body. Members are independently inspected against standards covering premises, vehicles, training, customer service, financial stability and complaints handling. They also operate an advance-payment guarantee scheme. <strong>If a company is not a BAR member, ask why.</strong></p>

        <h2>2. Goods-in-transit insurance</h2>
        <p>Ask to see a copy of the insurance certificate. £50,000 minimum is standard for a domestic remover; bigger firms should have £100,000 or higher. Check that the policy is current — some firms quote old certificates.</p>

        <h2>3. Established for at least five years</h2>
        <p>Companies House is free to search. Look for a track record of at least five years' trading. Many removal firms come and go — and if something goes wrong with your move, you want a company that will still be around in three months when you make the claim.</p>

        <h2>4. Real, verifiable reviews</h2>
        <p>Google Reviews are harder to fake than checkatrade or company-controlled testimonial pages. Look for: at least 50 reviews, an average above 4.5, and reviews spread over time (not 30 reviews all posted in one week). Read a few of the 3-star reviews — they often show how the firm responds when something goes wrong.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>5. A free, in-home survey</h2>
        <p>Any quote given over the phone without seeing the property should be treated as a rough estimate at best. Reputable firms send a surveyor (in person or by video call) to walk every room, measure access constraints, and discuss packing and special items. If the firm refuses to survey or pressures you to book without one, walk away.</p>

        <h2>6. A written, itemised quote</h2>
        <p>The quote should list — separately — the labour, the vehicle, packing materials (if used), parking permits, insurance, and any special-item charges. "All-in" quotes that lump everything together make it impossible to compare between firms and easy for hidden costs to appear on the day.</p>

        <h2>7. Transparent cancellation and change terms</h2>
        <p>Ask explicitly: "what happens if my completion date moves?" Many firms charge a significant fee — sometimes 25-50% of the quote — for date changes. We do not, but you need to know the policy in writing before you book.</p>

        <h2>8. Pad-wrap or blanket protection on furniture</h2>
        <p>This is the single most important question to ask: "how do you protect furniture during the carry to the lorry?" A good firm will say "we pad-wrap every piece in your home before it leaves the room." A poor firm will say "we use blankets in the lorry" — which is too late, because most damage happens on the carry, not in transit.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>9. Uniformed, trained crews — not casual labour</h2>
        <p>Ask if the crew are directly employed and trained, or hired through an agency. Direct employment with in-house training (look for BS 8564-aligned standards) means the people moving your house care about the company's reputation. Agency labour does not.</p>

        <h2>10. Deposit terms and protection</h2>
        <p>A 10-25% deposit is normal and reasonable. A 50%+ deposit, or full payment before move day, is a red flag. Check whether the deposit is held in a client account or BAR-administered advance-payment scheme — that protects you if the firm goes bust between your deposit and your move date.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>Two final questions to ask</h2>
        <p>If a firm passes the ten checks, two final conversational questions reveal a lot:</p>
        <ul>
          <li><strong>"Have you moved a property in my street or postcode recently?"</strong> — Local firms will know the access constraints. A firm routing in from outside the area will not.</li>
          <li><strong>"What was the most awkward move you handled last month?"</strong> — Confident, experienced firms will have a good answer. Vague answers suggest inexperience.</li>
        </ul>
        <p>If you are getting a removal quote in Eastbourne, we would be glad to be one of the three you compare. Call us on <a href="tel:01323848008">01323 848 008</a> or <a href="../mark-ratcliffe-moving-online-removals-quote.html">request a quote online</a>.</p>
      </div>
    </section>

    <section class="np-section">
      <div class="np-inner">
        <h2>The red flags that should make you walk away</h2>
        <p>Beyond the positive things to check for, there are warning signs that should disqualify a removal firm immediately. If you encounter any of these, walk away even if the price is appealing.</p>
        <p><strong>Cash-only requests for the deposit.</strong> A legitimate firm accepts bank transfer, card or cheque. Cash-only is either tax evasion or a sign that the firm cannot maintain a business bank account.</p>
        <p><strong>No physical office address.</strong> "We will come to you for the survey" is fine, but if the firm has no published depot or office address, ask why. Reputable removers have premises you can visit.</p>
        <p><strong>Pressure to book quickly.</strong> "This price is only valid today" is a classic pressure tactic. Reputable firms hold quotes for 30 days because they are confident in their pricing.</p>
        <p><strong>Reluctance to provide insurance details.</strong> Any legitimate firm will email a copy of their goods-in-transit insurance certificate without hesitation. Hesitation here is the single biggest red flag.</p>
        <p><strong>Vague answers about who will actually move you.</strong> "It depends on the day" might mean they sub-contract to whoever has capacity — agency labour with no training and no accountability. Ask explicitly: "will the people I meet at the survey be the same people who move me?"</p>
        <p><strong>Unprofessional communication.</strong> Misspellings on the website, broken contact forms, no response to email for days. These are not just signs of a small operation; they are signs of a poorly run business.</p>
      </div>
    </section>

    <section class="np-section np-section-soft">
      <div class="np-inner">
        <h2>Why comparing three quotes matters</h2>
        <p>The reason most consumer-advice publications recommend getting three quotes is not just to compare price — it is to compare process. Three legitimate quotes from three BAR-registered firms will be within 10–20% of each other on price. If one of them is 40% lower, something is missing from the quote (often the packing, insurance or fuel) and you need to know what.</p>
        <p>The three quotes also let you compare how each firm conducts the survey and the conversation. A good survey lasts 30–45 minutes, walks every room, asks about access at both ends, and follows up with a written quote within 24 hours. A bad survey is rushed, generic and followed by a quote that arrives in a week. The way a firm runs its sales process tells you a lot about how it will run your move.</p>
        <p>One final tip: when you call to ask for a quote, listen to who answers the phone. At good removal firms it is the office manager or one of the family. At struggling firms it goes through to voicemail or a generic answering service. The phone is the front door of the business — and what you hear is what you will get.</p>
      </div>
    </section>
"""
    return body


POST_BODIES = {
    "moving-house-checklist-eastbourne": post_moving_checklist,
    "how-to-pack-fragile-items": post_fragile_packing,
    "choosing-a-removal-company-eastbourne": post_choosing_remover,
}


def build_all():
    # Hub
    (BLOG_DIR / "index.html").write_text(blog_hub(), encoding="utf-8")
    # Posts
    for post in POSTS:
        body = POST_BODIES[post["slug"]]()
        html = blog_post_body(post, body)
        (BLOG_DIR / f"{post['slug']}.html").write_text(html, encoding="utf-8")
    print(f"Built blog hub + {len(POSTS)} posts.")


if __name__ == "__main__":
    build_all()
