#!/usr/bin/env python3
"""
Generate 14 new blog posts for markratcliffemoving.co.uk.

For each topic in BLOGS the script writes blog/<slug>.html with:
  - full template chrome (head, nav, hero, FAB, footer) cloned from
    blog/cost-of-moving-house-sussex-2026.html
  - JSON-LD BlogPosting + BreadcrumbList + FAQPage schemas
  - intro + 5 H2 sections + FAQ + related links
  - ≥10 contextual in-prose links

Re-runnable: existing files are overwritten.
Run from the site root:  python3 tools/create-new-blogs.py
"""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TEMPLATE_PATH = 'blog/cost-of-moving-house-sussex-2026.html'

# ----------------------- 14 BLOG TOPICS -----------------------------
# Each blog dict carries:
#   slug, title, desc, kicker, h1, hero_sub, hero_img (filename only),
#   breadcrumb (short label), intro_html, sections (list of (h2, html)),
#   faqs (list of (q, a) pairs).
# Section/intro HTML must contain in-prose <a href="..."> internal links
# (use href values relative to the blog/ folder — i.e. "../foo.html").

BLOGS = [
    # ---- Topic 5 ----
    {
        'slug': 'moving-to-eastbourne-area-guide.html',
        'title': 'Moving to Eastbourne: Complete Area Guide & Moving Tips',
        'desc': 'Thinking of moving to Eastbourne? Our local guide covers the best areas, parking rules, schools, and everything you need to know before you move.',
        'kicker': 'Local guide · Family-run since 1982 · Eastbourne specialists',
        'h1': 'Moving to Eastbourne — Complete Area Guide & Moving Tips',
        'hero_sub': "Where to live, how to plan the move, and what the local quirks are. Written by the team that has been running daily Eastbourne removals for over forty years.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Moving to Eastbourne',
        'intro_html': """<p style=\"font-size:1.15rem;\">Eastbourne is one of the South Coast's most consistently popular places to relocate to &mdash; quiet seafront, mature housing stock, strong schools, and a clear identity as a town that takes its civic life seriously. We've been a <a href=\"../about-us.html\">family-run Eastbourne remover</a> since 1982 and we've moved tens of thousands of households into the town and around it. This guide collects everything we wish first-time arrivals knew before move day.</p>
<p>The town breaks into half a dozen distinct neighbourhoods, each with its own price band, character and operational quirks for a removals lorry. We'll cover them in turn, then talk practicalities &mdash; parking, schools, transport &mdash; and finish with the move-logistics points specific to Eastbourne addresses. If you want a fixed-price <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">written quote</a> at any point, the survey is free.</p>""",
        'sections': [
            ('The neighbourhoods at a glance',
             """<p>Eastbourne's geography divides cleanly into recognisable patches. <strong>Meads</strong> sits to the south-west under the Downs — leafy, expensive, Victorian and Edwardian housing with steep streets, plus a meaningful share of basement flats and tile-hung period properties. Parking is permit-restricted in much of Meads and access for a 7.5-tonne lorry can be tight, so we always survey in person.</p>
<p><strong>Old Town</strong> is the original village centre around the parish church, with narrow lanes and a mix of converted Edwardian terraces and modern infill. The Old Town can be one-way and parking suspensions are often advisable for move day. <strong>Upperton</strong> sits between Old Town and the seafront — quieter residential terraces, popular with families. <strong>The Seafront and Devonshire Park</strong> area is dominated by larger Victorian villas, many converted to flats, plus newer apartment blocks near the pier.</p>
<p><strong>Hampden Park</strong> and <strong>Roselands</strong> are the inland family-home estates — post-war and 1960s semis on wider roads, easy lorry access, plenty of off-street parking. <strong>Sovereign Harbour</strong> is the modern marina development at the east end — apartments, town-houses and detached homes around the harbour, with controlled access and parking that needs pre-booking. For inbound moves to Sovereign, talking to the harbour office a week ahead saves stress on the day. Our <a href=\"../removals-eastbourne.html\">Eastbourne removals service</a> handles all of these.</p>"""),
            ('Parking and access — the bit nobody tells you',
             """<p>Permit zones cover most of Eastbourne's residential streets, including the whole of Meads, Old Town and the seafront. A removal lorry parked without a suspension on a permit street is a parking ticket waiting to happen and, more importantly, it blocks the operation. Apply for a parking suspension through Eastbourne Borough Council's online portal at least ten working days before move day. The cost is small (typically £50–£90) and pays for itself the first time you avoid a long carry to the lorry.</p>
<p>Some addresses simply can't take a 7.5-tonne lorry — the lanes around the Old Town and the steep Meads streets are the obvious examples. In those cases we'll shuttle: a smaller van ferries between your door and the main lorry parked further away. We'll spot this during the survey and price it in; no surprises on the day. The same applies to top-floor flats without lifts — talk to us at survey, not after.</p>
<p>If you're moving into a leasehold flat, ask the managing agent what the building's move-in policy is. Most Sovereign Harbour blocks and the bigger seafront conversions need lift bookings, protective floor coverings and sometimes weekend-only moves. We work with these all the time and a <a href=\"../full-packing-service.html\">full packing service</a> the day before makes lift-booked moves much easier to schedule.</p>"""),
            ('Schools, GPs and the boring-but-important admin',
             """<p>Eastbourne's secondary schools — Bede's, Eastbourne College, Cavendish, Causeway, Catmose and Bishop Bell — have catchment rules that move with the calendar. If a school place is part of why you're moving, check East Sussex County Council's application deadlines six months ahead of intake. Most arrivals we move don't realise the deadline has already passed.</p>
<p>GP and dentist registration is faster than people expect — most local practices accept new patients online inside a working day. Council tax is a five-minute online switchover (use the Eastbourne Borough Council change-of-address form). Bin and recycling rotas are colour-coded and posted online; the brown garden-waste service is a paid add-on you'll want to set up in week one if you have a garden.</p>
<p>Worth signing up for: the East Sussex parking permit if you're in a permit zone (apply online before move day), and the local Sussex weekly email from the council which is the easiest way to hear about road closures that might affect future moves or deliveries. We'll always email a list of these reminders after the move as part of our <a href=\"../helpful-tips.html\">helpful tips</a> follow-up.</p>"""),
            ('Routes and journey times to the town',
             """<p>Most of our inbound Eastbourne work comes from London via the A22, from Brighton or Hove along the coast, and from longer-distance moves via the M25 to the A22 corridor. London-to-Eastbourne is usually a single-day move with one crew if the inventory fits a single lorry; we leave the depot at first light and aim to be unloading by mid-afternoon at the latest. The completion-day chain logistics matter — we'll plan the start time around your conveyancer's funds-release timing, not the other way round.</p>
<p>From <a href=\"../removals-brighton.html\">Brighton</a> or <a href=\"../removals-worthing.html\">Worthing</a>, the coast road is fine outside the school-run hours but can be a slog in the morning peak. From <a href=\"../areas-covered/removals-lewes-moving-home-in-sussex.html\">Lewes</a>, <a href=\"../areas-covered/removals-newhaven-sussex.html\">Newhaven</a> and <a href=\"../areas-covered/removals-seaford.html\">Seaford</a>, it's a 20-to-40 minute lorry run depending on traffic. Any of these complete inside a single day.</p>
<p>For longer-distance arrivals — the West Country, the Midlands, the North — we schedule either a two-crew day or an overnight job with overnight secure storage at our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a>. Storage between completion dates is straightforward; we have steel strong-rooms on the mezzanine and self-storage units with 24/7 access on the ground floor.</p>"""),
            ('Booking your move and the survey process',
             """<p>The booking process for an Eastbourne move starts with a free in-home survey or video survey. The surveyor walks every room, counts cartons by size, photographs awkward corners and access points, and emails a <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">written, itemised quote</a> within 48 hours. We never quote a 3- or 4-bed move off a phone call — there's always something that gets missed and the price moves on the day.</p>
<p>Confirmation needs a 20–25% deposit, fully protected under the British Association of Removers' Advance Payment Guarantee. The balance is payable on the day of completion. We don't take cash for moves above £500 — card or bank transfer is standard. The whole process from first call to handover at the new front door usually takes between four and ten weeks; the busier May-to-September dates need the earlier end of that range.</p>
<p>If you'd like to read what previous Eastbourne customers said before booking, the <a href=\"../reviews.html\">reviews page</a> has the full Google and Trustpilot set. There's also a paper book of written customer feedback at our depot that you're welcome to read on a depot visit — handy if you want to see the unfiltered version.</p>"""),
        ],
        'faqs': [
            ("How early should I book an Eastbourne move?",
             "For end-of-month dates in the May–September peak, six to ten weeks ahead. Mid-week mid-month dates can sometimes be booked two to three weeks out. The earlier you book, the more choice of slot."),
            ("Do I need a parking suspension?",
             "On most Eastbourne residential streets, yes — Meads, Old Town, seafront and Upperton are nearly all permit-controlled. Apply via Eastbourne Borough Council ten working days ahead; the cost is £50–£90 and saves a long carry."),
            ("Can you handle Sovereign Harbour moves?",
             "Yes — we move into and out of the marina developments most months. Lift bookings and harbour-office notification need a week's notice; we'll handle the paperwork as part of the survey."),
            ("Do you offer storage between completion dates?",
             "Yes — at our A22 Lower Dicker depot. Steel strong-rooms on the mezzanine for short-term moves-in-storage, plus a fully fitted self-storage facility on the ground floor with 24/7 key-fob access."),
            ("Can you move me in from London?",
             "London to Eastbourne is one of our most-run routes. A typical 3-bed London move into Eastbourne is a single-day job with one crew, leaving the depot at first light and finishing mid-afternoon."),
        ],
    },

    # ---- Topic 8 ----
    {
        'slug': 'what-to-pack-first-when-moving-house.html',
        'title': 'What to Pack First When Moving House — Expert Order Guide',
        'desc': 'Not sure where to start packing? Follow our expert guide on the correct order to pack your belongings for a smoother, less stressful move.',
        'kicker': 'Packing order · Forty years of survey experience',
        'h1': 'What to Pack First When Moving House — A Room-by-Room Order Guide',
        'hero_sub': "There is a correct order to pack a house. Get it right and the last week is calm; get it wrong and you'll be sleeping on cardboard the night before move day.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'What to pack first',
        'intro_html': """<p style=\"font-size:1.15rem;\">Almost everyone we survey asks the same question at some point: <em>what should we actually pack first?</em> The instinct is to start in the most visible room — the living room or the kitchen — and the result is a fortnight of living out of half-packed cupboards. After forty years of <a href=\"../packing-services-eastbourne.html\">packing Sussex homes</a> we have a clear, tested order. This guide walks through it.</p>
<p>The principle is simple: pack the rooms you use least first, and finish with the rooms you genuinely need until move morning. That means lofts and outbuildings come early, kitchens and bathrooms come last. A 'first night' carton lives separately. Below is the order, broken into weeks, with the specific items to target at each stage.</p>""",
        'sections': [
            ('Weeks 4–6 before move day — lofts, garages and storage',
             """<p>The loft and the garage are where the surprises live. Almost every survey we do finds twice the volume the customer expected — boxes of family photos, retired crockery sets, the Christmas decorations, the camping gear that hasn't been used since 2014. Pull it all down onto the living-room floor and decide what's going, what's going to charity and what's going to the tip. This decision is much easier weeks before the move than the night before.</p>
<p>Old boxes from the loft are usually past their best — damp, dust-weakened cardboard that won't survive a lorry journey. Repack into <a href=\"../buy-packing-materials-eastbourne.html\">removal-grade cartons</a> with fresh tape. Label each carton with the room and a brief contents note, and number them so you can find anything during the move.</p>
<p>If you're using a <a href=\"../full-packing-service.html\">full packing service</a> on the day before move day, you can leave the loft and garage to the crew. But pulling it down ahead of time still saves you money — what's not coming with you doesn't need to be quoted, packed or moved.</p>"""),
            ('Weeks 2–4 before — books, decorations, archives',
             """<p>The second wave is anything you don't actively use day-to-day but want to keep. Books are at the top of this list. Pack books into <em>small</em> book cartons (no larger than 25cm cubed) because a large carton of books bursts under its own weight. Tape the carton bottoms with a double layer of vinyl tape and label them.</p>
<p>Decorations, ornaments, picture frames and the contents of display cabinets go next. These are the items that need real care — bubble wrap, internal tissue, vertical stacking for plates, padded wrapping for framed art. Our <a href=\"how-to-pack-fragile-items.html\">fragile items packing guide</a> walks through the specific techniques. If you'd rather not do it yourself, we offer a <a href=\"../packing-services-eastbourne.html\">fragile-only pack</a> the day before move day at a flat per-house rate.</p>
<p>This is also the week to pack archive paperwork — old bank statements you still need, tax documents, family records, kids' school certificates. Keep these in a labelled, weatherproof box and move it with you in your own car rather than in the lorry. Same goes for jewellery and any cash.</p>"""),
            ('Weeks 1–2 before — wardrobes, linens, hobby kit',
             """<p>By the week of the move you should be down to the everyday-use rooms. Pack wardrobes using hanging-wardrobe cartons (we drop these off the day before) — clothes go straight from rail to carton without folding. Out-of-season clothes have already been packed in week two; what's left is what you're currently wearing.</p>
<p>Linens, towels and bedding (except the bed that's actually in use) pack at this stage. Strip the spare-room beds, pack the duvets in clear bin liners (cheaper and works fine), and label each one with the room destination. Hobby gear — guitars, sewing kits, gardening tools that aren't currently being used — comes out now too.</p>
<p>If you have pets, the week before is when to organise their day-of arrangements. Many Eastbourne and Sussex customers we move arrange for a friend or pet-sitter to take dogs and cats away on move day; the lorry-noise plus open doors plus strangers can be genuinely stressful for animals. We've seen customers regret not arranging this more than just about any other planning miss.</p>"""),
            ('Move-day-minus-one — kitchen and bathroom',
             """<p>The kitchen is always the hardest room because almost every item is fragile, valuable in aggregate, or needed in the morning. The order: china and serving platters (Tuesday before), then non-essential glassware and the appliances (Wednesday), then the bulk of the cookware (Thursday), then the day-of essentials (Friday — kettle, two mugs, tea, biscuits, one set of cutlery and plates).</p>
<p>That last 'first-night' carton is the most important box in the whole house. It contains the things you'll need within an hour of arriving at the new place: kettle, mugs, tea bags, kitchen towel, a phone charger, basic toiletries, a tin of food for the cat. Tape it red and load it last so it comes off first. Several of our regular customers do this and swear by it.</p>
<p>The bathroom is similar — pack the cabinet contents (medicine, spare toothbrushes, bath products you don't use weekly) on Wednesday, leave the daily-use items in their pack until Friday morning, then transfer them into the toilet bag and they travel with you in the car. Don't forget the towel rail — most people leave a towel hanging there until the day of the move.</p>"""),
            ('Move morning — the last sweep',
             """<p>By the morning of move day everything should be packed except the four or five last-mile items: one kettle, the bed linen you slept in last night, the bathroom toilet bag, the first-night carton, and any work-from-home laptop and chargers. The crew arrives, pad-wraps the furniture in your home (this is our signature <a href=\"full-pad-wrap-protection-explained.html\">pad-wrap method</a>), loads the lorry in the right sequence, and you do the final walk-through of the property.</p>
<p>Check every cupboard, drawer, loft hatch and outbuilding before the keys go back. Take a photo of every wall, every socket and every meter reading — these are invaluable if there's a deposit dispute or a billing question later. If you've been a tenant, leave the property at least as clean as you found it; we have a <a href=\"../house-clearance-eastbourne.html\">house clearance service</a> if you've inherited rubbish from a previous resident.</p>
<p>Then it's done. The lorry leaves; you follow in your own car; the crew is on the driveway at the new property ten minutes before you arrive. The whole reason for packing in the right order is so that the last morning is calm, not chaotic. Our team have done this thousands of times — if you want the order applied for you, talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we'll handle the whole pack.</p>"""),
        ],
        'faqs': [
            ("How many weeks before should I start packing?",
             "Start the loft and the garage four to six weeks ahead. Books and decorations at two to four weeks. Wardrobes and linens the week before. Kitchen and bathroom in the final 48 hours. The 'first-night' carton last."),
            ("Should I pack the kitchen the week before?",
             "Pack the non-essentials (serving platters, second-best china, baking trays) but leave everyday cookware, glasses and one cutlery set until the day before. You'll need to eat right up to move morning."),
            ("Can you do the packing for me?",
             "Yes — a full pack the day before move day is one of our most popular services. The crew packs everything from books to kitchen china, supplies the materials, and labels every carton room-by-room."),
            ("What is the 'first-night' carton?",
             "One carton, taped red, packed last and loaded onto the lorry last so it comes off first at the new house. Kettle, two mugs, tea, kitchen towel, phone charger, basic toiletries. The single most useful box of the move."),
            ("What shouldn't go in the lorry?",
             "Jewellery, cash, passports, important documents, prescription medications, the laptop you work on. These travel with you in your own car. Standard removal insurance excludes high-value valuables anyway."),
        ],
    },

    # ---- Topic 9 ----
    {
        'slug': 'how-to-pack-kitchen-items-safely.html',
        'title': 'How to Pack Kitchen Items Safely for Moving',
        'desc': 'Packing the kitchen is the hardest part of any move. Learn how to safely pack plates, glasses, appliances and food items the professional way.',
        'kicker': 'Packing kitchens for forty years · The professional method',
        'h1': 'How to Pack Kitchen Items Safely — The Professional Method',
        'hero_sub': "The kitchen is the hardest room in any house to pack. China cracks, knives are dangerous, food spoils, appliances are awkward. Here is how we do it.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Packing kitchens',
        'intro_html': """<p style=\"font-size:1.15rem;\">Of the rooms we pack on every <a href=\"../full-packing-service.html\">full packing service</a> we deliver, the kitchen is the one that goes wrong most often when customers self-pack. Almost every breakage we ever see came from a kitchen carton — usually plates stacked flat, or wine glasses without internal padding, or a heavy chopping board landed on top of a cup. This guide walks through how the professionals do it.</p>
<p>Three rules cover most of what you need to know: pack heavy at the bottom and light on top, never stack plates flat, and always put internal padding into hollow items before you wrap the outside. The detail below applies those rules to every category of kitchen item, from china and glass through to small appliances and food.</p>""",
        'sections': [
            ('Materials — start with the right kit',
             """<p>The right materials are the difference between a kitchen that arrives intact and one that arrives with chips and cracks. You need <strong>removal-grade cartons</strong> in two sizes (small for heavy items like books and tinned food, medium for crockery and pans), <strong>50mm vinyl packing tape</strong> (not the pound-shop parcel tape — that releases in a warm lorry), <strong>bubble wrap</strong>, <strong>acid-free packing tissue</strong>, and <strong>divider inserts</strong> for glass and stemware. We stock all of these at our <a href=\"../packaging-shop.html\">Lower Dicker packaging shop</a>; if you'd rather buy a kit, the <a href=\"../buy-packing-materials-eastbourne.html\">packing materials page</a> has standard sets for one-bed up to five-bed homes.</p>
<p>Avoid newspaper for china and silver — newsprint transfers ink and you'll spend the first weekend at the new house cleaning it off. Tissue is cheap; buy proper packing tissue. Avoid old shoeboxes and reused supermarket boxes — they aren't built for stacking and the bases give out under the weight of a lorry-load on top.</p>
<p>The other piece of kit worth having is a permanent marker. Every carton needs the room (KITCHEN) and the contents (PLATES, FRAGILE, MUGS, etc.) written on at least three sides. Marker on the top alone is useless once a carton is stacked.</p>"""),
            ('Plates and china — the vertical rule',
             """<p>Plates always pack vertically, like records in a sleeve, never stacked flat. The compressive forces in a moving lorry are vertical; a stack of flat plates becomes a tower of shears that breaks the lowest plate. Vertical plates with tissue between each one transfer that force into the carton walls.</p>
<p>Bottom of the carton: a 4cm layer of crumpled tissue or bubble wrap. Then plates standing on their edges, each separated by a sheet of tissue. Wrap the largest plates first, fill the gaps with smaller ones, and finish with a generous layer of tissue on top. Don't overfill — a carton of plates should be lift-able with one hand. If it feels heavy, split it into two.</p>
<p>Fine china, antique china, family heirlooms — we'd usually recommend a fragile-only pack from a trained packer rather than self-pack. We offer this on most local moves as a flat per-house rate and it is by some margin the highest-value packing option we sell. The other option is our <a href=\"../white-glove-service.html\">white-glove service</a> where every fragile piece is individually wrapped and inventoried.</p>"""),
            ('Glassware, stemware and bottles',
             """<p>Wine glasses and stemware need internal padding — a small twist of tissue paper inside the bowl prevents the bowl walls from flexing inwards under stress. Without that internal pad, even a properly wrapped wine glass can crack across the bowl during transit. Tissue inside, then bubble wrap or tissue around the outside, then divider inserts in the carton.</p>
<p>Bottles — alcohol, vinegar, sauce — pose two problems: they're heavy and they're at risk of leaking onto everything else. Wrap each bottle in bubble wrap, seal the lid with electrical tape (more reliable than the screw cap on its own), and load bottles into a carton that you've lined with a heavy bin liner. If a bottle leaks, the liner stops the leak destroying the carton bottom and everything below.</p>
<p>For decanters, crystal and high-value glass, take photographs before packing — useful for both insurance purposes and for the unpacker (you, in a fortnight's time) to know where every piece is supposed to go. Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers breakages but for single items over £2,500 we'll want them listed specifically on the contract before move day.</p>"""),
            ('Appliances, knives and cookware',
             """<p>Small appliances — kettles, toasters, food processors, microwaves — pack in their original boxes if you still have them. If not, use a medium carton, fill the empty cavity inside the appliance with bubble wrap (so the internal components don't rattle), and wrap the outside in two layers of bubble. Label the carton with the appliance name and APPLIANCE-FRAGILE.</p>
<p>Knives and sharp blades need wrapping for the safety of whoever opens the carton at the other end. Wrap each blade individually in two layers of cardboard taped securely, then group them in a single labelled carton — KITCHEN-KNIVES-SHARP. Never wrap a knife and a fragile item together; a slip mid-unpacking can cut through bubble wrap and slice a hand.</p>
<p>Pans and heavier cookware go in the bottom of cartons. Cast iron, Le Creuset, heavy stockpots — stack in twos with tissue between, lid separately wrapped. Baking trays, oven dishes and Pyrex go on top of pans. As with plates, never overfill — a heavy carton is a carton that gets dropped. If you're not sure about a specific item, ask at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we'll cover it in the quote.</p>"""),
            ('Food, freezer contents and last-minute items',
             """<p>Food is the trickiest kitchen category because of three constraints: it spoils, it leaks, and removal insurance generally doesn't cover it. The honest answer for most moves is to run the cupboards down before moving — use up what you can in the four weeks before, donate unopened tins to a food bank, and arrive at the new house with only essentials in transit.</p>
<p>What does need to move: tinned goods (small carton, heavy-bottom-loaded), dry goods like rice, pasta and flour (sealed in their original packaging plus an extra bin-liner sleeve), oils and condiments (wrapped and bottle-lined as described above), and the contents of the freezer if the move is short enough that it'll stay frozen.</p>
<p>Freezer contents: empty the freezer 24 hours before move day, transfer to cool boxes with ice packs, and run them direct to the new property in your car rather than in the lorry. For longer moves (overseas, long-distance UK) the practical answer is to use the freezer down and not move its contents at all. Talk to us at <a href=\"../international-removals-eastbourne.html\">survey stage</a> if you're moving abroad — different countries have different food import rules and we can advise.</p>"""),
        ],
        'faqs': [
            ("Should I pack plates flat or on their edges?",
             "On their edges, always. Vertical stacking transfers compressive force into the carton walls; flat stacking concentrates it on the lowest plate and breaks it."),
            ("Do I need tissue inside wine glasses?",
             "Yes — internal tissue prevents the bowl walls flexing inwards under stress. Without it, even a well-wrapped wine glass can crack across the bowl during transit."),
            ("Can I use newspaper instead of tissue?",
             "For glassware, yes (with tissue still in the bowl). For china and silver, no — newsprint transfers ink and you'll spend the weekend cleaning it off. Tissue is cheap; just buy proper packing tissue."),
            ("Will you pack the kitchen for me?",
             "Yes — kitchen-only or full-house packing the day before move day. Trained crew, removal-grade cartons, written inventory. About £220–£340 for fragile-only on a typical 3-bed."),
            ("What about freezer contents?",
             "Empty 24 hours before, transfer to cool boxes with ice packs, run them in your car not the lorry. For long-distance or overseas moves, use the freezer down beforehand."),
        ],
    },

    # ---- Topic 10 ----
    {
        'slug': 'how-to-pack-clothes-without-wrinkling.html',
        'title': "How to Pack Clothes Without Wrinkling Them When Moving",
        'desc': 'Stop ironing everything again after your move. Discover the best methods to pack clothes so they stay wrinkle-free during transit.',
        'kicker': 'Wardrobe cartons · Vacuum bags · The pack-as-you-hang method',
        'h1': 'How to Pack Clothes Without Wrinkling — Move Day Wardrobe Guide',
        'hero_sub': "Re-ironing a whole wardrobe on day one in the new house is no one's idea of a relaxing arrival. Here is how to keep clothes crease-free in transit.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Packing clothes',
        'intro_html': """<p style=\"font-size:1.15rem;\">After the kitchen, the second-biggest 'will-we-be-OK?' worry on most house moves is the wardrobe. People imagine waking up at the new house and finding a knotted ball of crumpled fabric where their work shirts used to be. It's a solvable problem, and on a properly-equipped <a href=\"../packing-services-eastbourne.html\">packing service</a> we use four specific techniques that get clothes from old wardrobe to new wardrobe without a single iron stroke. This guide walks through them.</p>
<p>The core principle: keep clothes on their hangers wherever possible, and where they have to be folded, use the right kind of fold and the right kind of carton. Drag-and-stuff into a black bin liner is the worst possible approach. The right materials cost almost nothing and the right method takes no longer than the wrong one.</p>""",
        'sections': [
            ('Hanging wardrobe cartons — the gold standard',
             """<p>The single best way to move clothes wrinkle-free is the hanging wardrobe carton — a tall reinforced cardboard box with a built-in metal hanging rail across the top. Clothes go directly from your wardrobe rail to the carton rail without being folded or removed from their hangers. Suits, dresses, work shirts and tailored items arrive at the new house in exactly the state they left.</p>
<p>We supply hanging wardrobe cartons with every <a href=\"../full-packing-service.html\">full packing service</a> and you can also rent them separately for self-pack jobs. A typical wardrobe takes two to four of these cartons. They're not cheap to buy but they're reusable — we collect them after the move and re-use them on the next job, which keeps the per-move cost low.</p>
<p>For self-pack moves, we can drop the cartons off three to four days before move day, you load them at your own pace, and the crew loads them onto the lorry straight from your bedroom on move morning. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we'll include them in the quote.</p>"""),
            ('Folded clothes — the right way to pack a drawer',
             """<p>For clothes that don't need to stay on hangers — t-shirts, jeans, jumpers, casual wear — the right approach is to pack them folded in a single carton per drawer's worth, with tissue between layers for delicate fabrics. Don't overfill: an under-filled carton crushes less under the lorry's weight than a stuffed one.</p>
<p>Knitwear and jumpers fold differently from cotton t-shirts. For knitwear, fold sleeves inward and fold the whole jumper in half. For t-shirts, the supermarket-folding-board method works fine — keep the fold even and stack each item flat. Heavy items (jeans, jumpers) at the bottom, lighter items (t-shirts, vests) on top.</p>
<p>For sensitive fabrics — silk, fine wool, anything you take to the dry-cleaners — put a sheet of acid-free packing tissue between each piece. We stock proper packing tissue at our <a href=\"../packaging-shop.html\">Lower Dicker packaging shop</a>; the household variety from the supermarket works fine for most clothing but isn't acid-free for long-term storage.</p>"""),
            ('Vacuum-pack bags — for bulky items only',
             """<p>Vacuum-pack bags (the big plastic bags you suck the air out of with a vacuum cleaner) are excellent for one specific use case: bulky bedding, duvets, winter coats and large jumpers. They shrink the volume by roughly 75% and the items pack into a fraction of the carton space.</p>
<p>They are <em>not</em> the right solution for tailored clothing, anything that creases easily, or anything you intend to wear within a week of arrival. The compression that vacuum-packing relies on flattens shirt collars, jacket lapels and pleats in trousers. Use vacuum bags for what they're designed for, not as a general clothing solution.</p>
<p>For winter coats and ski jackets being moved into storage (we offer <a href=\"../storage-eastbourne.html\">self-storage at our depot</a>), vacuum-packing is also useful because it reduces the carton count and therefore the storage cost. Just unpack the bag for an hour every few months to let the fabric breathe.</p>"""),
            ('Shoes, accessories and the small-item problem',
             """<p>Shoes go in their original boxes wherever possible. The boxes were designed for the shoes; nothing else fits the shape as well. If you've thrown the boxes away, the alternative is to wrap each pair in tissue and pack them in small cartons of six to eight pairs each, separated by a layer of tissue. Don't mix shoes with clothes — sole dirt transfers onto fabric and you'll be cleaning it for weeks.</p>
<p>Handbags hold their shape better if you stuff them with tissue or bubble wrap before packing. Same goes for hats and millinery. For high-value items — designer handbags, family-jewellery cases, watch boxes — we'd recommend they travel with you in your own car rather than in the lorry, regardless of how carefully they're packed. Standard goods-in-transit insurance excludes high-value individual items unless they're declared in advance.</p>
<p>Jewellery, watches and small valuables follow the same rule. Don't put them in the lorry — pack them in a small bag and travel with them yourself. We'll cover the practical details at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> and the <a href=\"choosing-a-removal-company-eastbourne.html\">choosing a remover guide</a> has more on what insurance covers.</p>"""),
            ('Final week — wardrobe wind-down',
             """<p>By the week of the move you should be down to the clothes you're currently wearing. The seasonal wardrobe (winter coats in summer, summer shirts in winter) should have been packed two weeks earlier. The everyday wardrobe gets packed on the Wednesday-to-Friday before move day, with one small overnight bag containing two days' worth of clothes that travels with you in your car.</p>
<p>That overnight bag is more important than people realise. Lorries sometimes get delayed by traffic, chains slip by a day, completions can run late. If your suitcase of work clothes is on the wrong side of a delayed lorry, you have a problem. Keep two outfits with you, no exceptions.</p>
<p>Once the move is complete and the wardrobes are set up at the new house, our crew can hang the contents of the hanging wardrobe cartons directly into your new wardrobe on the same day. This is included in any <a href=\"../unpacking-service.html\">unpacking service</a> you've booked. For self-unpacking customers, the cartons stand upright in the bedroom and you can pull clothes from the rail directly.</p>"""),
        ],
        'faqs': [
            ("Will my suits and shirts crease?",
             "Not if they travel in hanging wardrobe cartons. Clothes go from your old wardrobe rail to the carton rail without being folded or unhooked from hangers."),
            ("Can I use bin liners instead?",
             "Not recommended. Bin liners offer no protection from creasing, snagging or external pressure. The wardrobe carton is reusable and the small extra cost saves you a weekend of ironing."),
            ("Are vacuum-pack bags safe for clothes?",
             "Only for bulky bedding, duvets and casual winter coats. Don't use them for tailored shirts, suits or anything that needs to look pressed on arrival — vacuum compression flattens collars and lapels."),
            ("What about shoes — original boxes or generic cartons?",
             "Original boxes wherever possible. If not, wrap each pair in tissue and pack six to eight pairs per small carton with tissue between. Never mix shoes and clothing — sole dirt transfers."),
            ("Should jewellery and watches go in the lorry?",
             "No. Travel with you in your own car. Standard transit insurance excludes high-value individual items unless they're declared in advance on the contract."),
        ],
    },

    # ---- Topic 11 ----
    {
        'slug': 'moving-to-brighton-area-guide.html',
        'title': 'Moving to Brighton: Complete Area Guide & Moving Tips',
        'desc': 'Planning to move to Brighton? Our local guide covers the best areas, parking, schools, transport links, and everything you need to know before moving.',
        'kicker': 'Brighton & Hove area guide · 40 years of moves into the city',
        'h1': 'Moving to Brighton — What You Need to Know in 2026',
        'hero_sub': "From the Lanes to Patcham, Hove to Kemp Town. The neighbourhoods, the parking quirks, and what to expect on move day in the UK's quirkiest seaside city.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Moving to Brighton',
        'intro_html': """<p style=\"font-size:1.15rem;\">Brighton is one of the most-requested destinations on our Sussex routes — the city's character, schools, transport links and seafront pull customers in from London, the Home Counties and overseas. We've been running <a href=\"../removals-brighton.html\">Brighton removals</a> for forty years and the city's geography has its own move-day rules that nowhere else in Sussex shares.</p>
<p>This guide walks through the neighbourhoods, the practical move-day logistics (Brighton parking is its own subject), and the schools, transport and admin you'll need to set up. If you'd rather skip ahead, the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">free survey form</a> takes ten minutes and we'll come back with a written quote inside two working days.</p>""",
        'sections': [
            ('Brighton neighbourhood overview',
             """<p>Brighton's neighbourhoods divide into roughly six broad groups. <strong>Kemp Town and the East</strong> is the Regency seafront area — Georgian crescents, the Royal Pavilion district, lots of converted Victorian terraces. Parking is mostly permit-controlled and access for lorries can be tight, particularly in the conservation-area streets.</p>
<p><strong>Central Brighton and the Lanes</strong> is the busy commercial heart — pedestrianised areas, limited daytime access for large vehicles, narrow back streets. Moves into Lanes-adjacent flats need careful planning and sometimes weekend slots when restrictions ease. <strong>Hove</strong> sits to the west — broader streets, Edwardian and Victorian villas, more parking, considerably easier for a 7.5-tonne lorry. We cover <a href=\"../areas-covered/removals-hove.html\">Hove removals</a> on the same daily rounds.</p>
<p><strong>Preston Park and the North</strong> covers the inland family suburbs — Preston Park, Withdean, Patcham, Hollingbury. Wider roads, plentiful off-street parking, mostly 1930s and post-war semis with the occasional detached house. <strong>Whitehawk and East Brighton</strong> has its own character, mostly low-rise post-war estates. <strong>Saltdean and Rottingdean</strong> are technically Brighton & Hove and we cover <a href=\"../removals-saltdean.html\">Saltdean</a> and <a href=\"../removals-rottingdean.html\">Rottingdean</a> as part of the same routes.</p>"""),
            ('Brighton parking — the most important single subject',
             """<p>If there's one thing to know before you book a Brighton move, it's that parking is the single biggest logistical variable in the city. Almost every residential street is permit-controlled. Some areas (Kemp Town, North Laine, the Lanes) have additional time-restricted bays. A removal lorry parked without a suspension on permit street is at risk of a ticket, a wheel clamp, or being asked to move mid-loading.</p>
<p>Apply for a parking suspension through Brighton & Hove City Council's parking suspensions portal at least ten working days before move day. The cost typically runs £80–£140 depending on the road category. The application can be done online and the council issues the cone-and-signage permit so the bays are reserved on the day.</p>
<p>Some addresses can't take a 7.5-tonne lorry at all — the narrow back streets of the Lanes, the steep streets of Kemp Town and parts of the North Laine. In those cases we shuttle: a smaller van runs between your front door and the main lorry parked legally further along. We'll spot this at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and price it in. No surprises on the day.</p>"""),
            ('Schools, transport and getting set up',
             """<p>Brighton & Hove City Council operates a complex secondary-school admissions system — the catchments aren't simply geographic; there's a lottery element for over-subscribed schools. If a specific school is part of why you're moving, check the council's school admissions guidance six months ahead of intake. Many arriving families don't realise the deadline has passed.</p>
<p>Public transport in Brighton is unusually good for a small city — frequent buses, a direct rail link to London Victoria (54 minutes), and the regional rail along the coast to <a href=\"../areas-covered/removals-lewes-moving-home-in-sussex.html\">Lewes</a> and <a href=\"../removals-eastbourne.html\">Eastbourne</a>. Car ownership is lower than the national average partly because of all this and partly because parking permits in some zones are expensive enough to be a deterrent.</p>
<p>Council-tax setup, GP and dentist registration, refuse collection rotas — all five-minute online forms through the Brighton & Hove City Council site. Sign up for the parking permit in your first week if you have a car; the application has a longer turnaround than other councils we work with. The <a href=\"../helpful-tips.html\">helpful tips section</a> covers the order to tick these off.</p>"""),
            ('Move-day logistics for Brighton addresses',
             """<p>Most Brighton moves we run are single-day jobs with one crew. Inbound from London is typically 90 minutes' drive with the lorry; inbound from <a href=\"../removals-hastings.html\">Hastings</a> or Eastbourne is the same again. The longer-distance moves (West Country, Midlands, North) are usually two-crew or overnight jobs.</p>
<p>The lorry leaves our <a href=\"../about-us.html\">Lower Dicker depot</a> in time to be on your driveway ten minutes before the stated load time. We pad-wrap furniture in your home before it leaves the room — this is our signature <a href=\"full-pad-wrap-protection-explained.html\">pad-wrap method</a>. Loading takes between three and eight hours depending on inventory size and access.</p>
<p>At the unload end, the same crew unwraps each piece in its final position in the new room. If you've booked the <a href=\"../unpacking-service.html\">unpacking service</a>, the team also unpacks cartons and removes the empty boxes the same day. Otherwise we come back later in the week (no charge if you're within standard delivery range) to collect the empties.</p>"""),
            ('When to book and how the survey works',
             """<p>For Brighton moves in the busier May-to-September period, book the survey eight to ten weeks ahead. Quieter mid-week mid-month dates can sometimes be booked two to three weeks out. The earlier you book, the more choice of slot and crew. We don't oversell our diary — once your date is held, it's held.</p>
<p>The survey itself takes 30 to 45 minutes. The surveyor walks every room, counts cartons by size, photographs the access points at both ends, and discusses any quirks (loft contents, narrow doorways, valuable items). The written, itemised quote follows within 48 hours. If you'd rather have a video survey (we do these via WhatsApp), the process is the same.</p>
<p>Confirmation needs a 20–25% deposit, fully protected under the British Association of Removers' Advance Payment Guarantee. The balance is paid on the day. The whole process from first call to handover at the new front door usually takes between four and ten weeks — Brighton moves in particular benefit from the longer end of that timeline because of the parking-suspension application lead time.</p>"""),
        ],
        'faqs': [
            ("Do I need a parking suspension for a Brighton move?",
             "On most residential streets, yes. Apply via Brighton & Hove City Council ten working days ahead — cost is £80–£140 depending on the road. The application is online and the council issues the cones."),
            ("Can your lorry access the Lanes?",
             "Some Lanes streets, no. We'll spot this at survey and arrange a shuttle: a smaller van between your front door and the main lorry parked legally further along."),
            ("How long does a Brighton move from London take?",
             "Typically a single day with one crew. Lorry leaves Lower Dicker first thing, on your driveway by mid-morning, finishing the unload mid-to-late afternoon depending on the unload property's access."),
            ("Do you cover Hove as well?",
             "Yes — Hove, Saltdean, Rottingdean and the surrounding villages are on the same daily routes. The hub of the city plus the eastern and western neighbourhoods are all standard coverage."),
            ("Can I do the move at the weekend?",
             "Yes — Saturday moves at no premium, Sunday moves on request. Some Lanes-adjacent flats actually have to be moved at weekends due to weekday traffic restrictions, which we plan around at survey."),
        ],
    },

    # ---- Topic 12 ----
    {
        'slug': 'moving-to-chichester-area-guide.html',
        'title': 'Moving to Chichester: What You Need to Know in 2026',
        'desc': 'Everything you need to know about moving to Chichester including listed properties, parking restrictions, Goodwood events, and local moving advice.',
        'kicker': 'Chichester area guide · West Sussex listed-property specialists',
        'h1': 'Moving to Chichester — Local Guide for 2026',
        'hero_sub': "Cathedral city with conservation-area constraints, listed buildings and Goodwood-week chaos. Here is how we plan moves into and out of Chichester.",
        'hero_img': 'mark-ratcliffe-vans-front2.webp',
        'breadcrumb': 'Moving to Chichester',
        'intro_html': """<p style=\"font-size:1.15rem;\">Chichester sits at the western end of our daily routes, a Roman cathedral city with a particular set of move-day constraints: a pedestrianised centre, a high concentration of listed properties, conservation-area parking restrictions, and the four Goodwood events a year that turn the whole local road network into a car park. We've handled <a href=\"../removals-chichester.html\">Chichester removals</a> for decades and this guide walks through what we've learned.</p>
<p>The good news: Chichester is a fundamentally welcoming city to move into. The schools are strong, the cultural life is unusually good for a city of 30,000, and the surrounding villages (Bosham, West Wittering, Goodwood, Petworth) are some of the most desirable in West Sussex. The logistics just need a bit more planning than a generic move.</p>""",
        'sections': [
            ('The cathedral city geography',
             """<p>Chichester's centre is the medieval grid of four roads (North Street, South Street, East Street, West Street) inside the city walls. Inside that grid, the streets are mostly pedestrianised, partially time-restricted, and the buildings are predominantly listed. Moves into a flat or a converted town-house inside the walls almost always need an early-morning or weekend slot when the pedestrian restrictions ease.</p>
<p>Outside the walls, the city spreads in four broad directions. The northern suburbs (Summersdale, Lavant, Mid Lavant) are mature family residential. The east (Whyke, Tangmere) has a mix of post-war and modern housing. The south (Donnington, Hunston) is quieter. The west (Fishbourne, Bosham, West Itchenor) is the prestige villages along the harbour, with a heavy concentration of period properties.</p>
<p>For most of these areas access for a 7.5-tonne lorry is straightforward — wider roads, more off-street parking. The exception is the Bosham peninsula, where some of the harbour-edge lanes are too narrow for a full lorry and we shuttle via a smaller van. We <a href=\"../areas-covered/removals-bexhill.html\">cover Bosham</a> as part of standard Chichester area routes.</p>"""),
            ('Listed buildings and conservation areas',
             """<p>The medieval city centre and significant surrounding districts are conservation areas, and a high proportion of the older properties are listed (Grade I, II* or II). Listed buildings come with two move-day considerations: you can't physically alter them without consent, and the historic fittings need real protection during the move-in.</p>
<p>Original fireplaces, panelling, plaster cornices, Tudor or Georgian floorboards — these can be damaged by careless furniture-moving in ways that are expensive to repair and sometimes legally problematic. Our standard <a href=\"full-pad-wrap-protection-explained.html\">pad-wrap method</a> protects furniture, but for listed properties we also bring corner-board and door-frame protection for the building itself. Mention any listed-building considerations at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a>.</p>
<p>If you're moving valuable antiques into a Chichester period property, we offer specialist services through our <a href=\"../antiques-moving.html\">antiques moving</a> and <a href=\"../white-glove-service.html\">white-glove relocation</a> — individual wrapping, soft-foot rolling, custom crating for marble and stone. The Lower Dicker depot also has a strong-room for between-completion storage of high-value contents.</p>"""),
            ('Goodwood Festival, Glorious Goodwood and the other event weeks',
             """<p>The four big Goodwood events — the Festival of Speed, Glorious Goodwood, the Revival and the Members' Meeting — bring tens of thousands of visitors to Chichester every year. The road network around the city saturates for the duration of each event, and removal lorries can be delayed by hours getting into or out of any address north of the city.</p>
<p>If your move date falls inside any of these event weeks, talk to us at survey and we'll either schedule around the peak hours (very early start, returning before the afternoon crush) or recommend moving the date entirely. The events run typically late June (Festival of Speed), late July to early August (Glorious Goodwood), September (Revival) and March (Members' Meeting).</p>
<p>Chichester Festival Theatre and the cathedral events calendar also push traffic at predictable points through the year, but these are smaller-scale and don't usually affect move-day operations meaningfully. The major-event weeks are the ones to plan around.</p>"""),
            ('Schools, transport and admin',
             """<p>Chichester's school options include the well-regarded Chichester High School (state secondary), Bishop Luffa, and the independent Prebendal School, Bishop Otter (St Mary's), and Dorking Grammar nearby. West Sussex County Council operates the admissions process; check application deadlines six months ahead of intake.</p>
<p>Rail connections from Chichester are reasonable but not exceptional — the Portsmouth-to-London Victoria line runs hourly to two-hourly, and the journey to London Victoria is about 100 minutes. Car ownership is the practical default. The A27 is the main east-west route and connects to the A3 for London.</p>
<p>Council-tax setup, GP and dentist registration, refuse collection — all online via Chichester District Council and West Sussex County Council. Worth setting up a parking permit early if you're inside the conservation area; the application has a slightly longer turnaround than newer councils.</p>"""),
            ('How we plan Chichester moves',
             """<p>Most Chichester moves run as standard single-day jobs with one crew, leaving our <a href=\"../about-us.html\">Lower Dicker depot</a> at first light and finishing the unload mid-to-late afternoon. From <a href=\"../removals-brighton.html\">Brighton</a>, the drive across is around 90 minutes. From London via the M25 and A3 it's about two hours.</p>
<p>For listed-building moves and high-value contents, we'll usually quote for the <a href=\"../white-glove-service.html\">white-glove option</a> or at minimum a full pad-wrap with corner-board protection. Antiques get individually wrapped. Marble and stone-topped furniture goes in custom crates if the journey is long. None of this is unusual for Chichester customers, but the survey is where we agree the scope.</p>
<p>Booking the survey takes ten minutes via the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">online quote form</a>. The surveyor visits within a week, we email the itemised written quote within 48 hours, and the deposit (20–25%) holds the date. The whole sequence from first call to handover usually takes four to ten weeks — Chichester moves in summer benefit from the longer end of that window because of Goodwood and the summer school holidays.</p>"""),
        ],
        'faqs': [
            ("Can your lorry access the cathedral city centre?",
             "Inside the city walls the streets are mostly pedestrianised. We schedule early-morning or weekend slots when restrictions ease, or shuttle via a smaller van from a legal parking point further out."),
            ("Do listed buildings need special handling?",
             "Yes — corner-board and door-frame protection for the building itself, plus our standard pad-wrap for furniture. Mention listed-building status at the survey and we'll quote accordingly."),
            ("How do Goodwood event weeks affect moves?",
             "Significantly — Festival of Speed, Glorious Goodwood, the Revival and the Members' Meeting all saturate the local road network. We'll either schedule around peak hours or recommend rescheduling the move date."),
            ("Do you cover Bosham, West Wittering and the harbour villages?",
             "Yes — the harbour-edge villages are all part of the standard Chichester area routes. Some of the narrow harbour lanes need a shuttle from a smaller van, which we'll cost in at survey."),
            ("How long is a London-to-Chichester move?",
             "Around two hours' drive with the lorry, so a typical single-crew day with morning load, motorway transit, and mid-to-late afternoon unload. Larger moves split across two crews or two days."),
        ],
    },

    # ---- Topic 13 ----
    {
        'slug': 'moving-to-hastings-area-guide.html',
        'title': 'Moving to Hastings: Area Guide & Local Moving Tips',
        'desc': 'Considering a move to Hastings? Discover the different areas, what to expect, and practical local advice from a Sussex removals company.',
        'kicker': 'Hastings area guide · Old Town to St Leonards · 40 years on the route',
        'h1': 'Moving to Hastings — Area Guide & Local Moving Tips',
        'hero_sub': "Old Town, the seafront, St Leonards, the inland estates. The areas, the access quirks, and what to know before move day in Hastings.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Moving to Hastings',
        'intro_html': """<p style=\"font-size:1.15rem;\">Hastings has had a remarkable decade — a genuine creative-industries renaissance in the Old Town, the steady gentrification of St Leonards, and a wave of London arrivals chasing affordable Victorian terraces by the sea. We run <a href=\"../removals-hastings.html\">Hastings removals</a> as one of the busiest routes on our weekly diary and this guide pulls together what we tell first-time arrivals.</p>
<p>The town is bigger than it looks from the seafront: half a dozen distinct districts, a steep topography, and a mix of Victorian terraces, post-war estates and newer infill. The move-day logistics vary considerably between them, and the cost of getting it wrong (a wasted morning, a parking ticket, a long carry) is meaningful. Below is the orientation we give every survey.</p>""",
        'sections': [
            ('Hastings neighbourhoods at a glance',
             """<p>The <strong>Old Town</strong> is the medieval and Tudor heart — narrow lanes between the East Hill and the West Hill, fishermen's huts on the beach, a strong artistic community. Move access in the Old Town is limited; the narrow streets won't take a 7.5-tonne lorry in most cases and we shuttle via a smaller van.</p>
<p><strong>The Seafront and Central Hastings</strong> is the Victorian and Edwardian terrace belt — large family townhouses, many converted to flats. Access is mostly fine but parking is permit-controlled. <strong>St Leonards</strong>, technically a separate town but functionally a Hastings suburb, sits to the west — Regency squares, Norman Road, the cosmopolitan high street. Parking is permit-restricted in much of St Leonards.</p>
<p><strong>The Inland Estates</strong> — Silverhill, Hollington, Ore Valley, Roebuck Park — are 1930s and post-war housing on wider roads. Lorry access is easy, off-street parking common. <strong>West Hill, East Hill and Mount Pleasant</strong> are the hillside districts — properties with sea views, steep approaches that can be tricky for a fully laden lorry. <strong>Bohemia, Hollington and the West</strong> are mostly post-war estates with straightforward access.</p>"""),
            ('Topography — the hill question',
             """<p>Hastings is built on hills, and several of its most attractive neighbourhoods (East Hill, West Hill, parts of St Leonards) involve steep approaches that affect move-day logistics. A 7.5-tonne lorry fully loaded approaches a 1-in-6 gradient slowly; the crew expects this and the survey will spot any properties where the approach needs a smaller van shuttle.</p>
<p>The other hill-related consideration is the carry from lorry to door. Properties with steep front gardens, basement-flat staircases or first-floor flats above shops add real time to the load and unload. We price for the work as part of the survey — there's no hidden surcharge on the day for properties we've already seen.</p>
<p>If your new house is at the top of a Hastings hill and your inbound lorry is coming from anywhere via London, the time you save by taking the A21 over the A22 is usually erased by the approach. The route planning is part of what our crews do, and we'll have driven it before. Our <a href=\"../about-us.html\">Lower Dicker depot</a> is about 35 minutes from central Hastings on most routes.</p>"""),
            ('Parking, permits and conservation areas',
             """<p>Hastings Borough Council operates a network of permit-controlled zones across most of the seafront and town-centre residential areas. A removal lorry parked without a suspension is at meaningful risk of a ticket. Apply for a parking suspension through the council's parking-suspensions portal at least ten working days before move day.</p>
<p>The Old Town and parts of St Leonards are conservation areas with additional restrictions — pavement-loading restrictions, sometimes time-of-day rules. These are flagged in the parking-suspension application process and the cost is modest (typically £50–£100).</p>
<p>One Hastings-specific quirk: some of the seafront roads are subject to additional restrictions during the peak summer season because of the volume of tourist traffic and the events programme. If your move date falls in late July or August on the seafront, talk to us at survey and we'll plan the schedule accordingly.</p>"""),
            ('Schools, transport and admin',
             """<p>Hastings's secondary schools include the Hastings High School, William Parker, Helenswood, and the independent Claverham Community College. East Sussex County Council operates the admissions process; check application deadlines six months ahead of intake.</p>
<p>Rail connections from Hastings are particularly good — the Hastings line to London Charing Cross takes about 90 minutes, and the regional coast line connects to <a href=\"../removals-bexhill.html\">Bexhill</a>, <a href=\"../removals-eastbourne.html\">Eastbourne</a>, <a href=\"../removals-brighton.html\">Brighton</a> and onwards. The A21 is the main road north towards London via Tunbridge Wells.</p>
<p>Council-tax setup, GP and dentist registration, refuse collection — all standard online forms through Hastings Borough Council and East Sussex County Council. The parking permit application takes a few working days; do it in your first week if you're inside a permit zone.</p>"""),
            ('Moving to and from Hastings — how it works',
             """<p>Most Hastings moves are single-day jobs with one crew. Inbound from London via the A21 is around two hours' drive with a fully loaded lorry. Inbound from <a href=\"../areas-covered/removals-tunbridge-wells-moving-home-in-sussex.html\">Tunbridge Wells</a> or <a href=\"../removals-eastbourne.html\">Eastbourne</a> is about 45 minutes. The longer-distance moves (West Country, Midlands, North) are usually two-crew or overnight.</p>
<p>The survey takes 30 to 45 minutes — we walk every room, photograph access at both ends, and discuss any quirks (loft contents, steep approaches, listed-building considerations). The <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">written quote</a> follows within 48 hours, itemised by line.</p>
<p>For storage between completion dates, our Lower Dicker depot has steel strong-rooms on the mezzanine and self-storage units with 24/7 access on the ground floor. We'll quote for it as part of the move if dates don't line up cleanly. The Hastings-to-depot route is straightforward — about 40 minutes — and we can hold the load overnight or for longer periods without difficulty.</p>"""),
        ],
        'faqs': [
            ("Can your lorry access the Old Town?",
             "Most Old Town streets are too narrow for a 7.5-tonne lorry. We shuttle via a smaller van from a legal parking point further out. We'll quote this at survey, no surprises on the day."),
            ("Are Hastings parking permits a problem?",
             "Most central and seafront streets are permit-controlled. Apply for a parking suspension via Hastings Borough Council ten working days ahead — cost is £50–£100."),
            ("Do you handle moves to the hillside districts (East Hill, West Hill)?",
             "Yes — these are part of our standard Hastings routes. Steep approaches sometimes need a smaller-van shuttle for the last 50 metres; we price this in at survey."),
            ("How long is a London-to-Hastings move?",
             "Around two hours' drive with the lorry, so a typical single-crew day with morning load, A21 transit, and mid-to-late afternoon unload."),
            ("Can you store our belongings between completion dates?",
             "Yes — steel strong-rooms on the mezzanine of our A22 Lower Dicker depot, plus self-storage units on the ground floor with 24/7 key-fob access. About 40 minutes drive from Hastings."),
        ],
    },

    # ---- Topic 14 ----
    {
        'slug': 'moving-to-worthing-area-guide.html',
        'title': 'Moving to Worthing: Complete Local Guide 2026',
        'desc': 'Moving to Worthing? Our guide covers the best areas to live, schools, transport, and useful local information for new residents.',
        'kicker': 'Worthing area guide · From the Seafront to Salvington',
        'h1': 'Moving to Worthing — Complete Local Guide for 2026',
        'hero_sub': "The Sussex town that quietly became one of the most-recommended coastal moves. Neighbourhoods, transport, schools and the move-day reality.",
        'hero_img': 'mark-ratcliffe-vans-front2.webp',
        'breadcrumb': 'Moving to Worthing',
        'intro_html': """<p style=\"font-size:1.15rem;\">Worthing has been one of the quiet success stories of the Sussex coast over the last decade. It went from a slightly tired Edwardian seaside town to a confident, family-friendly destination with strong schools, a busy independent retail scene and remarkably good value compared to Brighton next door. We run <a href=\"../removals-worthing.html\">Worthing removals</a> several times every week and this guide collects what we tell new arrivals.</p>
<p>The town is bigger than visitors realise — six or seven distinct neighbourhoods, a mix of Edwardian seafront grandeur, post-war suburbia, modern estates and Downland villages on its northern edge. The move-day logistics are generally easier than Brighton or Eastbourne, but a few quirks are worth knowing before booking.</p>""",
        'sections': [
            ('The Worthing neighbourhoods',
             """<p>The <strong>Seafront and Town Centre</strong> includes the Edwardian terraces and converted villas along Marine Parade and Brighton Road. Lots of converted flats, plenty of period detail, mostly easy lorry access but permit parking applies. <strong>West Worthing</strong> (Tarring, Goring) is the leafy western suburb with mature gardens and a high proportion of detached and semi-detached family homes.</p>
<p><strong>Broadwater and Findon Valley</strong> sit north of the centre — predominantly Edwardian and 1930s housing with wider streets, good for lorry access. <strong>Salvington</strong>, <strong>Durrington</strong> and <strong>High Salvington</strong> are the inland districts running up towards the Downs — mostly post-war and 1960s housing on broad estates. <strong>East Worthing</strong> includes Lancing border areas and the modern developments at Shoreham boundary; we cover <a href=\"../removals-shoreham-by-sea.html\">Shoreham removals</a> as part of the same routes.</p>
<p>The Downland villages on Worthing's north edge — Findon, Sompting, Lancing village, Steyning, <a href=\"../removals-storrington.html\">Storrington</a> — are technically separate but functionally part of the Worthing commuter belt. We run regular routes through all of them.</p>"""),
            ('Access and parking — Worthing specifics',
             """<p>Worthing's permit-controlled zones are smaller than Brighton's but still meaningful — most of the seafront, much of the town centre and parts of West Worthing. Apply for a parking suspension through Adur and Worthing Councils' online portal at least ten working days before move day. The cost typically runs £60–£100.</p>
<p>For the inland suburbs (Tarring, Durrington, Salvington) parking is mostly unrestricted and a removal lorry can usually pull onto the drive or kerb without difficulty. This is one of the practical reasons Worthing moves are often cheaper than equivalent Brighton moves — less time wasted on access logistics.</p>
<p>One Worthing-specific consideration: the seafront and town-centre roads are subject to additional restrictions during the summer events programme (carnival, food festivals, half-marathon). If your date falls during one of these weeks, talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> and we'll plan the schedule accordingly.</p>"""),
            ('Schools, GPs and the practical admin',
             """<p>Worthing's secondary schools include Worthing High School, Davison High School (girls), and the well-regarded Sir Robert Woodard Academy at Lancing. West Sussex County Council operates admissions; check the deadlines six months ahead of intake. Multiple independent prep and senior schools serve the area including Lancing College.</p>
<p>Rail connections from Worthing are good — the Brighton-to-Portsmouth line runs frequently with services to London Victoria via Three Bridges (about 90 minutes). Bus links across the town are reliable. The A27 is the main east-west road. Car ownership is the practical default for most households outside the central seafront flats.</p>
<p>Council-tax setup, GP and dentist registration, refuse collection rotas — all standard online forms via Adur and Worthing Councils and West Sussex County Council. Sign up for the parking permit in your first week if you're inside a permit zone. The <a href=\"../helpful-tips.html\">helpful tips section</a> has the suggested order.</p>"""),
            ('Storage, packing and the longer-distance moves',
             """<p>Many of our Worthing moves involve storage between completion dates — particularly the chain moves out of London where the Worthing purchase completes a fortnight or so after the London sale. Our <a href=\"../storage-eastbourne.html\">A22 Lower Dicker depot</a> handles between-completion storage for Worthing customers without difficulty; we hold the load in steel strong-rooms on the mezzanine and deliver to Worthing when the completion date arrives.</p>
<p>For longer-distance moves — Worthing to the West Country, the Midlands, the North — we run two-crew schedules or overnight jobs depending on inventory size. Inbound moves from London via the M25 and A24 are typically single-crew single-day jobs, about two hours' drive each way with the lorry.</p>
<p>Packing options for Worthing customers include the <a href=\"../full-packing-service.html\">full packing service</a> the day before move day, fragile-only packing for the kitchen and breakables, or a self-pack with materials supplied from our <a href=\"../buy-packing-materials-eastbourne.html\">packaging shop</a>. Most Worthing customers go for the fragile-only option — flat per-house rate, professional packers handle the kitchen and the display cabinets, the rest is self-pack.</p>"""),
            ('Booking and the survey process',
             """<p>The survey takes 30 to 45 minutes in person, or about the same length via video call. The surveyor walks every room, counts cartons, photographs access at both ends, and discusses any quirks. The <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">written quote</a> follows within 48 hours.</p>
<p>Confirmation needs a 20–25% deposit, protected under the British Association of Removers' Advance Payment Guarantee. The balance is paid on the day. The whole sequence from first call to handover usually takes four to ten weeks; for end-of-month dates in May to September, the earlier end of that range.</p>
<p>If you'd like to read what other Worthing customers said before booking, the <a href=\"../reviews.html\">reviews page</a> has the full Google and Trustpilot set. Booking the survey takes ten minutes via the online form — we'll come back within 48 hours to arrange a slot.</p>"""),
        ],
        'faqs': [
            ("Are Worthing moves cheaper than Brighton moves?",
             "Usually yes, by 10–15%, because the parking and access logistics are simpler. Less suspension cost, easier loading, less time wasted on shuttle work. The crew rates are identical."),
            ("Do you cover the Downland villages north of Worthing?",
             "Yes — Findon, Sompting, Steyning, Storrington, Lancing village. All part of standard Worthing area routes. The lorry runs through them on most weekday rounds."),
            ("How long is a London-to-Worthing move?",
             "Around two hours each way with a loaded lorry. A typical single-crew day with morning load, M25/A24 transit, and mid-to-late afternoon unload."),
            ("Can you store between completion dates?",
             "Yes — steel strong-rooms at our A22 Lower Dicker depot, about 50 minutes drive from Worthing. We hold the load and deliver when your completion date arrives."),
            ("What's the deposit and is it protected?",
             "20–25% on confirmation, balance on completion day. All deposits are protected under the British Association of Removers' Advance Payment Guarantee."),
        ],
    },

    # ---- Topic 15 ----
    {
        'slug': 'best-areas-to-live-east-sussex-2026.html',
        'title': 'Best Areas to Live in East Sussex in 2026',
        'desc': 'Not sure where to move in East Sussex? We break down the best areas to live based on lifestyle, schools, transport and property types.',
        'kicker': 'Where to live · East Sussex 2026 · A remover’s perspective',
        'h1': 'Best Areas to Live in East Sussex in 2026',
        'hero_sub': "Moving into East Sussex but not sure exactly where? After forty years of moving households around the county, here is our honest ranking by lifestyle.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Best areas in East Sussex',
        'intro_html': """<p style=\"font-size:1.15rem;\">When customers ask us where they should move in East Sussex, they're often weighing five or six different priorities: schools, transport, character of the town, property value, sea or countryside, and what feels right for the family. After four decades of <a href=\"../areas-covered.html\">moving households around East Sussex</a> we have a clear view of which towns suit which lifestyles. This guide isn't a definitive ranking — it's a remover's honest perspective.</p>
<p>We cover six East Sussex destinations in detail below — Eastbourne, Lewes, Hailsham, Bexhill, Hastings and the Downs villages — plus practical commentary on which areas best fit different family profiles. The aim is to save you a wasted weekend driving around a town that isn't going to be right.</p>""",
        'sections': [
            ('Eastbourne — the family-friendly seafront option',
             """<p>Eastbourne is the largest town in East Sussex and the one we move into more often than any other. The pull factors are consistent: long flat seafront for prams and bikes, strong primary and secondary schools, a fully covered shopping centre, and a property market that includes everything from Victorian seafront flats through 1930s family semis to modern Sovereign Harbour town-houses.</p>
<p>The downsides are minor but worth noting: parking is permit-restricted in most central neighbourhoods, the centre can feel quiet outside the summer months, and the rail journey to London Victoria via Lewes is around 90 minutes (not bad, but not as fast as Brighton's Thameslink). Our <a href=\"../removals-eastbourne.html\">Eastbourne removals service</a> sees us in the town almost daily; the <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne area guide</a> has the full neighbourhood breakdown.</p>
<p>Best for: families with school-age children, downsizers from London or the Home Counties, anyone who wants a seafront walk every morning without paying Brighton prices. Less good for: night-owls and people who need to be in central London more than twice a week.</p>"""),
            ('Lewes — the historic county town',
             """<p>Lewes is East Sussex's county town and one of the most charming small towns in southern England. The High Street is a museum of independent retail, the castle and the Anne of Cleves House anchor a tourist trade that supports good restaurants and cafés, and the rail link to London Victoria is unusually quick for a town this size — about 70 minutes direct.</p>
<p>The property market is narrow and expensive: a small supply of period townhouses, Edwardian semis on the slopes around the castle, and a smaller number of post-war detached homes on the inland fringes. Listed buildings are everywhere and move-day logistics need a survey. We cover <a href=\"../areas-covered/removals-lewes-moving-home-in-sussex.html\">Lewes removals</a> as part of standard daily routes; the steep High Street and narrow medieval lanes mean some addresses need a smaller-van shuttle.</p>
<p>Best for: London commuters who want a strong-character small town, families with a budget for period housing, anyone who values historic charm over modern convenience. Less good for: families needing five-bedroom modern detached homes (the supply is thin) or anyone who hates parallel parking on a steep hill.</p>"""),
            ('Hailsham, Polegate, Heathfield — the affordable middle',
             """<p>The triangle of Hailsham, Polegate and Heathfield sits between Eastbourne and the Downs and offers what is consistently the most affordable family housing in East Sussex. Hailsham is the largest, with a busy market square, supermarkets and a wide range of housing from terraced cottages through to large detached estates. <a href=\"../hailsham-removals.html\">Hailsham removals</a> is one of our most-run local routes.</p>
<p>Polegate sits between Hailsham and Eastbourne with quick rail access to both. Heathfield is the smallest and the prettiest, with a strong country-town feel and proximity to the High Weald AONB. All three benefit from straightforward move-day logistics — wider roads, more off-street parking, fewer permit zones than the coast.</p>
<p>Best for: families on a sensible budget who want value-for-money family housing within a short drive of the coast and the Downs. Less good for: anyone who prioritises a vibrant town centre with strong restaurant and cultural life.</p>"""),
            ('Bexhill, Hastings and the eastern coast',
             """<p>Eastern East Sussex — Bexhill, Hastings and St Leonards — is the value-for-money corner of the county. Bexhill is the gentle, slightly faded resort with the De La Warr Pavilion and a strong arts community. <a href=\"../removals-bexhill.html\">Bexhill removals</a> is a regular run for us. Hastings is the larger, busier coastal town with a renaissance Old Town and the strong London rail link via the A21 line.</p>
<p>St Leonards has been the surprise of the last decade — a transformation from sleepy seaside annex to one of the most creative small communities in the South-East. The Norman Road high street, the Victorian villas, the seafront walks. Our <a href=\"moving-to-hastings-area-guide.html\">moving to Hastings guide</a> has the full breakdown.</p>
<p>Best for: anyone wanting a sea view at sensible cost, creatives, downsizers from the South-East, families happy to be a 90-minute train ride from London. Less good for: families needing a five-day London commute or wanting the kind of polish you find in Brighton.</p>"""),
            ('Downland villages — the quiet option',
             """<p>If your move is driven by a wish to leave the noise of a town behind, the Downland villages on East Sussex's northern edge are the obvious answer. <a href=\"../removals-alfriston.html\">Alfriston</a>, <a href=\"../removals-uckfield.html\">Uckfield</a>, <a href=\"../removals-crowborough.html\">Crowborough</a>, <a href=\"../removals-mayfield.html\">Mayfield</a> and the villages of the High Weald AONB offer period cottages, listed farmhouses and a kind of quiet that suburban East Sussex can't match.</p>
<p>The trade-offs are real: school catchments are narrower and primaries are small (sometimes a positive), the rail links are slower (Crowborough to London Victoria is 75 minutes; smaller villages need a drive to a station), and the local services are limited (one village shop, maybe two pubs, a single GP surgery serving multiple villages).</p>
<p>Best for: families with older children who don't need a busy school choice, second-home buyers, downsizers, anyone who wants the AONB on the doorstep. Less good for: families with young children who want extensive local services, anyone needing a five-day London commute.</p>"""),
        ],
        'faqs': [
            ("Which East Sussex town has the fastest London commute?",
             "Lewes — direct trains to London Victoria in around 70 minutes. Eastbourne is 90 minutes via Lewes. Hastings is 90 minutes via the A21 line."),
            ("Which has the best schools?",
             "All East Sussex secondaries are administered by East Sussex County Council. Eastbourne College and Bede's are well-regarded independent options. State schools in Lewes and Eastbourne consistently score well; the rural primary catchments around the Downland villages are smaller but often closely-knit."),
            ("What's the most affordable family-housing area?",
             "The Hailsham–Polegate–Heathfield triangle is consistently the best value for family housing. Eastern East Sussex (Bexhill, Hastings, St Leonards) is the next tier."),
            ("Are property prices still rising in East Sussex?",
             "We're a removals firm, not estate agents — but observationally, the Eastbourne and Lewes markets have stabilised over 2025–2026 after a sharp post-pandemic rise. The eastern coast (Bexhill, Hastings) is still seeing meaningful inflow from London buyers."),
            ("Can you handle moves into rural Downland properties?",
             "Yes — we move into and out of the High Weald villages regularly. Narrow lanes sometimes need a smaller-van shuttle, which we'll cost in at the survey. The rural depots (Uckfield, Mayfield, Crowborough) are all standard coverage."),
        ],
    },

    # ---- Topic 16 ----
    {
        'slug': 'how-to-choose-right-self-storage.html',
        'title': "How to Choose the Right Self Storage for Your Needs",
        'desc': "Not sure what type of storage you need? We explain the different options and help you choose the perfect storage solution for your situation.",
        'kicker': 'Storage choices · Steel strong-rooms · Self-access lockers',
        'h1': 'How to Choose the Right Self Storage for Your Needs',
        'hero_sub': "Containerised vs. drive-up. Climate-stable vs. unheated. Short-term vs. long-term. What to ask before signing a storage contract.",
        'hero_img': 'mark-ratcliffe-vans-front2.webp',
        'breadcrumb': 'Choosing self-storage',
        'intro_html': """<p style=\"font-size:1.15rem;\">Self-storage is a category that looks identical from the outside but actually divides into half a dozen different formats with different costs, different security profiles and different access arrangements. After forty years operating our own <a href=\"../storage-eastbourne.html\">Lower Dicker storage facility</a> — and after handling thousands of customers using third-party storage between contracts — we have a clear view of how to pick the right type.</p>
<p>This guide walks through the formats, the questions to ask before signing, and the operational considerations that almost no comparison site mentions. The aim is to save you from either over-paying for storage you don't need or under-paying for storage that's the wrong fit.</p>""",
        'sections': [
            ('The formats — what “self-storage” actually means',
             """<p>The three main formats are <strong>containerised storage</strong>, <strong>drive-up self-storage</strong>, and <strong>strong-room storage</strong>. Containerised means your possessions go into a sealed wooden box (typically 8ft × 7ft × 5ft) which is stored in a warehouse. Drive-up self-storage means a steel-walled unit (sizes from 25 sq ft to 250+ sq ft) that you access by driving up to it. Strong-room storage is a secure warehouse room used by removal firms for short-term moves-in-storage between completions.</p>
<p>Containerised is the cheapest but the slowest to access — typically 24–48 hours' notice to retrieve anything. Drive-up is the most expensive per cubic foot but you can come and go 24/7. Strong-room is the cheapest for short-term (a few weeks between completion dates) but you can't usually access it yourself; the remover does it for you.</p>
<p>Our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> offers both strong-room storage on the mezzanine (for short-term between-contract moves) and drive-up self-storage on the ground floor (for longer-term needs and self-access). Most customers use one or the other; some use both — strong-room for furniture, drive-up for items they want regular access to.</p>"""),
            ('Climate, security and what the facility actually has',
             """<p>The questions worth asking any storage provider before signing: <em>Is it climate-stable?</em> (not climate-controlled — that's expensive and unnecessary for most household contents; climate-<em>stable</em> means insulated and well-ventilated, which is enough for furniture, books and most electronics). <em>What's the security setup?</em> (CCTV, alarmed, individual unit locks, key-fob entry, on-site staff). <em>What's the insurance position?</em> (most facilities require you to insure your contents separately, or via their policy).</p>
<p>Climate-stable matters because British winters bring condensation into uninsulated steel containers, and condensation ruins photographs, paperwork, fabric and electronics. If you're storing for more than a couple of months, climate-stable is non-negotiable. Our depot is climate-stable by design — fully insulated, ventilated, monitored.</p>
<p>Security is the visible bit but it's not just about cameras. The questions that matter: is the perimeter fenced? Is there 24-hour CCTV with recording (not just monitoring)? Is the building alarmed? Who has keys to the building outside hours? Are individual units padlocked by the customer or by the facility?</p>"""),
            ('How much space do you actually need?',
             """<p>This is the most common mistake — customers consistently book either too much or too little space. The rough rule: a 25 sq ft unit fits the contents of a single bedroom plus a few boxes. A 50 sq ft unit fits a one-bedroom flat. A 100 sq ft unit fits a two-bedroom flat or a three-bedroom house's worth of furniture without large items. A 200 sq ft unit fits the contents of a four-bedroom house.</p>
<p>Strong-room storage is priced per container or per cubic foot, which means the volume question is the right one — how many cartons and pieces of furniture, not how many square feet. A three-bedroom house typically fits in three or four containers. We'll cost this at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> as part of the removal quote.</p>
<p>The way to estimate is to imagine the contents of the house stacked floor-to-ceiling in one room. Pad-wrapped furniture stacks more efficiently than people expect because the wrapping protects against compression. If you're not sure, ask the storage provider to walk you through their unit sizes in person — most facilities will show you sample units before you sign.</p>"""),
            ('Access — how often will you actually go?',
             """<p>The mismatch we see most often is between access expectations and reality. Customers booking strong-room storage think they'll want monthly access; in practice they go twice in six months. Customers booking expensive drive-up self-storage think they'll go monthly; they go three times the entire contract.</p>
<p>Be honest with yourself about access. If the storage is for items you'll genuinely use (children's toys for a half-built house, your gym kit during a renovation, business stock that turns over) then drive-up is worth the extra cost. If it's furniture or boxes you're storing because the timing didn't work out, strong-room is cheaper and the access difference doesn't matter.</p>
<p>One operational point: if you're storing in a remover's strong-room between contract completions, the remover handles all the heavy lifting at both ends. Your job is just to decide what goes in and what gets delivered out. For drive-up self-storage you usually do the loading and unloading yourself, which means an extra van rental at both ends.</p>"""),
            ('Contracts, costs and what to watch for',
             """<p>Storage contracts vary hugely. The questions worth confirming in writing: <em>What's the minimum notice to vacate?</em> (typically a calendar month at a major facility, often just two weeks at a smaller one). <em>How is the price set?</em> (typically by unit size, but some include 'free' moves in/out for the first month — read the small print). <em>Are there exit costs?</em> (some facilities charge a 'final clean' fee). <em>Is the price guaranteed for the contract length, or does it review?</em></p>
<p>Insurance is the biggest variable. Most storage facilities won't insure your contents; you do that separately, either via their suggested broker or your own home contents policy (some policies extend to off-site storage; many do not). Confirm in writing what's covered and what isn't. Our depot insurance arrangements are explained in the <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance details</a>.</p>
<p>Final point: storage is a long game. The cheapest provider for the first three months is sometimes the most expensive at month twelve because of price escalators. Read the contract end-to-end before signing. If you'd like an independent view, talk to us — we've sub-let from most of the major storage operators across Sussex over the years and we know which contracts are honest.</p>"""),
        ],
        'faqs': [
            ("What's the difference between strong-room and drive-up self-storage?",
             "Strong-room is cheaper but you can't usually self-access — the remover retrieves items for you. Drive-up is more expensive but 24/7 accessible. Strong-room suits short-term between-contract moves; drive-up suits longer-term self-managed storage."),
            ("Do I need climate-controlled storage?",
             "Climate-controlled is rarely worth the cost; climate-stable (insulated, ventilated) is enough for most household contents. Avoid uninsulated steel-walled units for stays over two months — condensation ruins fabric, photos and electronics."),
            ("How much storage space do I need?",
             "Rough rule: 25 sq ft for one bedroom, 50 sq ft for a one-bed flat, 100 sq ft for two beds, 200 sq ft for a four-bed house. Volume not floor area is the variable; ask the facility to show you sample units."),
            ("What insurance do I need on stored contents?",
             "Most storage facilities don't insure your contents — you do that separately. Check whether your home contents policy extends to off-site storage; many don't. Get insurance confirmed in writing before move-in."),
            ("Can you organise storage between completion dates?",
             "Yes — strong-room storage at our Lower Dicker depot is one of the most common services we provide. We hold the load, deliver to your new property when the completion date arrives, no shuttling required from you."),
        ],
    },

    # ---- Topic 17 ----
    {
        'slug': 'short-term-vs-long-term-storage.html',
        'title': "Short Term vs Long Term Storage: Which One Is Right For You?",
        'desc': "Confused about storage lengths? Here's a clear breakdown of short-term and long-term storage and when to use each.",
        'kicker': 'Storage length · Two-week pause or two-year hold',
        'h1': 'Short-Term vs Long-Term Storage — Which One Is Right For You?',
        'hero_sub': "The decision is mostly about access frequency, contract terms and condensation. Here is how we help customers decide.",
        'hero_img': 'mark-ratcliffe-vans-front2.webp',
        'breadcrumb': 'Short vs long-term storage',
        'intro_html': """<p style=\"font-size:1.15rem;\">Most of our <a href=\"../storage-eastbourne.html\">Lower Dicker storage</a> customers fall cleanly into one of two categories: short-term (two to twelve weeks, usually between contract completions) or long-term (six months to several years, usually because of a renovation, a downsizing, or a move overseas). The two are priced and arranged completely differently, and confusing them costs real money.</p>
<p>This guide walks through how to decide which one applies to you, what each costs, and the operational considerations that change between them. As ever, the survey is free if you'd rather just discuss it in person.</p>""",
        'sections': [
            ('Short-term storage — what it actually means',
             """<p>Short-term storage in our world means two weeks to three months. The classic use case is the chain that doesn't quite line up — your sale completes a fortnight before your purchase, so the contents of your old house need to live somewhere in between. Other common short-term cases: a renovation that's running late, a temporary move to a serviced apartment, a downsizing where the new house isn't ready yet.</p>
<p>Short-term is best handled as <strong>strong-room storage</strong> at a remover's depot. Your contents go into a secure warehouse room, you don't need to access them, the remover handles loading and unloading at both ends. The cost is per week and is usually billed as part of the removal quote rather than as a separate contract. Our <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> will cost it as a line item.</p>
<p>The reason strong-room is right for short-term: there's no contract setup overhead, no notice-period costs, no insurance complexity. You're paying for storage time and one collection/delivery — that's it. The downside (no self-access) is irrelevant for two weeks.</p>"""),
            ('Long-term storage — different game',
             """<p>Long-term means six months or more. The use cases differ from short-term: a downsizing where you're keeping furniture for the next house, a renovation that will take a year or two, an extended move overseas where you don't want to ship everything yet, a business storing stock or files.</p>
<p>For long-term, the right format is usually <strong>self-access self-storage</strong> — a steel-walled unit you can come and go from. The advantages over strong-room: 24/7 access (you can collect the kids' winter coats at the weekend), padded unit pricing, and easier contract amendments if your storage need changes over time.</p>
<p>The disadvantages: higher monthly cost per cubic foot, you do your own moves in and out, and you need to think about insurance separately. Our <a href=\"../storage-eastbourne.html\">drive-up self-storage units</a> at the Lower Dicker depot offer key-fob access and individual unit padlocks; we can also handle moves in and out of the unit if you'd prefer not to.</p>"""),
            ('The decision matrix — which one to pick',
             """<p>The decision usually comes down to four questions. <strong>How long?</strong> Under three months — strong-room. Over six months — self-access. Three-to-six months — depends on the other factors. <strong>How often will you access it?</strong> Not at all — strong-room. Monthly or more — self-access. Quarterly — could go either way.</p>
<p><strong>Is the contents furniture or active stock?</strong> Furniture for a future house — strong-room is fine. Active stock you'll be drawing from — self-access. <strong>Do you have a van and time?</strong> Yes — self-access works. No — strong-room means the remover does all the heavy lifting.</p>
<p>Our practical recommendation: start with strong-room if you're under three months and you're not going to access it. Move to self-access if your storage need extends beyond that and you start wanting access. Many customers split — furniture in strong-room, items they want access to in a small self-access unit nearby.</p>"""),
            ('Condensation and climate — the long-term killer',
             """<p>The number-one cause of damage in long-term storage is condensation. British winters bring meaningful humidity changes into uninsulated steel-walled storage units, and the temperature cycling pulls moisture out of the air and into anything porous — paper, fabric, leather, electronics. Items stored uninsulated for more than three months can come out damp.</p>
<p>The fix is climate-stable storage — insulated walls, controlled ventilation, no direct sun. Climate-stable is different from climate-controlled (which is much more expensive and unnecessary for most household contents). Our depot is climate-stable by design; some self-storage providers offer it as a premium option.</p>
<p>If you're planning long-term storage of anything you care about — family photos, antiques, books, leather furniture — climate-stable is non-negotiable. Mention it specifically when comparing facilities; the savings on a non-climate-stable unit are real but the cost of replacing a damp-damaged piano or a mildewed book collection is much greater. The <a href=\"../antiques-moving.html\">antiques moving service</a> walks through what counts as climate-sensitive.</p>"""),
            ('Cost expectations and contract terms',
             """<p>Short-term strong-room storage typically runs £15–£35 per week per container (a container holds a one-bedroom flat or about half a three-bedroom house). Long-term self-access runs £20–£60 per month per 25 sq ft (so a 100 sq ft unit, big enough for most family homes, is £80–£240 a month). Prices vary considerably by region; Sussex generally sits in the middle.</p>
<p>Contract terms matter. Short-term storage usually runs week-by-week without notice obligations. Long-term self-access typically has a calendar-month notice period and sometimes an annual price review. Confirm in writing before signing what the exit costs are — some facilities charge a 'final clean' fee, some don't.</p>
<p>One financial point worth mentioning: if you're storing because of a chain delay, your home contents insurance usually doesn't cover items in off-site storage. The remover's or storage provider's insurance covers it instead, but at a different premium. Our <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance details</a> page explains how we handle it.</p>"""),
        ],
        'faqs': [
            ("How long counts as 'short-term'?",
             "Two weeks to three months. Beyond three months, the case for self-access starts to outweigh the case for strong-room because of access frequency and contract flexibility."),
            ("Is long-term storage damp?",
             "Not in a climate-stable facility (insulated, ventilated). Uninsulated steel-walled units in British winters bring condensation that ruins paper, fabric and electronics over months. Climate-stable is non-negotiable for long-term."),
            ("Can I move from short-term to long-term storage?",
             "Yes — many customers start with strong-room for the chain delay, then transfer to self-access if the storage need extends. We can handle the move internally at the Lower Dicker depot without you needing to do anything."),
            ("What's the average monthly cost?",
             "Strong-room: £15–£35 per week per container (about £60–£140/month per container). Self-access: £20–£60 per month per 25 sq ft. Sussex pricing is roughly the national average."),
            ("Does my home contents insurance cover off-site storage?",
             "Usually no, or only for a brief grace period after a move. The storage provider or remover will offer their own cover. Get this confirmed in writing before move-in."),
        ],
    },

    # ---- Topic 18 ----
    {
        'slug': 'what-you-can-and-cannot-store.html',
        'title': "What You Can and Can't Store in Self Storage Units",
        'desc': "Important safety and insurance information - a complete list of items you can and cannot put into self storage.",
        'kicker': 'Storage rules · What’s allowed, what isn’t, what spoils',
        'h1': "What You Can and Can't Store in Self Storage Units",
        'hero_sub': "Three lists: yes-store, conditional, and absolutely-not. Plus the items insurance won't cover even if they look fine on the shelf.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': "What to store",
        'intro_html': """<p style=\"font-size:1.15rem;\">Storage units aren't a free-for-all. There are items that storage facilities won't accept under any circumstances, items they'll accept but won't insure, and items that are technically allowed but will be ruined by the storage environment. After forty years operating our own <a href=\"../storage-eastbourne.html\">Lower Dicker storage facility</a> we have a clear list of all three categories.</p>
<p>This guide walks through them. The rules aren't quirky — they exist for fire safety, contamination prevention and insurance reasons — but they catch out customers who haven't asked the right questions before signing the storage contract. Knowing them in advance saves time and money.</p>""",
        'sections': [
            ('What you can store — the standard list',
             """<p>The bulk of household possessions are fine in self-storage. Furniture (sofas, beds, chairs, tables, wardrobes), boxes of books and clothing, kitchen contents (cookware, china, cutlery — emptied of food), bedroom contents (bedding, linens, soft furnishings), garage and shed contents (tools, garden furniture, bikes if drained of fuel), and most electronics (TVs, computers, hi-fi).</p>
<p>Antiques, art, mirrors and fragile items are allowed but need particular handling — wrap them properly using our <a href=\"how-to-pack-fragile-items.html\">fragile-packing techniques</a>, and label the carton clearly so it isn't stacked under heavy items. For high-value individual pieces, consider declaring them separately on the storage contract for insurance purposes.</p>
<p>Documents, paperwork and family records are allowed but should be in sealed, weatherproof boxes — preferably the plastic archive crates rather than cardboard. Books should be packed in small cartons (no larger than 25cm cubed) to prevent the carton bottoms giving way under stack weight. Both documents and books benefit from climate-stable storage rather than uninsulated units.</p>"""),
            ('Conditional — allowed with caveats',
             """<p>Several categories of item are allowed but with conditions. <strong>Appliances</strong> (washing machines, fridges, freezers, dishwashers) must be fully drained, dried and cleaned before storage — water residue causes mould and damages the appliance. <strong>Garden equipment</strong> with petrol engines (mowers, strimmers, chainsaws) must have all fuel drained and the tank vented before storage; some facilities require a written certificate.</p>
<p><strong>Bikes</strong> are fine but tyres must be inflated to riding pressure (low pressure encourages tube damage during storage). <strong>Musical instruments</strong> — pianos, guitars, brass — are allowed but need climate-stable conditions; humidity swings are particularly bad for stringed instruments. We handle pianos specifically through the <a href=\"../piano-moving.html\">piano moving service</a> and store them upright on padded plinths.</p>
<p><strong>Wines and spirits</strong> in unopened bottles are typically allowed for personal use but need lying flat and away from temperature extremes. Storage facilities don't usually allow commercial-quantity alcohol storage without a separate licence. <strong>Photography and film</strong> — slides, negatives, undeveloped prints — should ideally be in climate-stable units; basement and roof-mounted units are too unstable.</p>"""),
            ('What you absolutely cannot store',
             """<p>The list of absolute exclusions is short and serious. <strong>Anything alive</strong> — pets, plants, any biological material. Storage facilities are not appropriate environments for living organisms and most insurance policies specifically exclude them. <strong>Anything flammable or explosive</strong> — petrol (in containers), bottled gas, propane tanks, fireworks, ammunition, gunpowder, lighter fluid. These are fire-risk and many facilities have explicit no-flammable rules.</p>
<p><strong>Anything corrosive or hazardous</strong> — strong acids, large quantities of cleaning chemicals, paint thinners, pool chemicals. Small domestic quantities of household cleaners are usually fine; commercial-quantity hazardous substances are not. <strong>Anything illegal</strong> — drugs, stolen goods, unlicensed firearms. This is obvious but worth saying.</p>
<p><strong>Perishable food</strong> — fresh or frozen meat, dairy, eggs, anything that spoils. Tinned food and dried food in sealed packaging is usually fine. <strong>Cash and high-value valuables</strong> — most storage facilities won't insure these and most won't allow them at all. The <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance details</a> page lists the specific exclusions.</p>"""),
            ('Items that aren’t banned but will spoil',
             """<p>Beyond the formal exclusions, there are items that are technically allowed but will be damaged by the storage environment. <strong>Leather furniture</strong> in uninsulated units will dry, crack and develop mould over months. <strong>Solid-wood furniture</strong> with traditional finishes can warp or split due to humidity changes. <strong>Paper-based items</strong> (books, photo albums, archive boxes) absorb moisture and develop mildew in non-climate-stable conditions.</p>
<p><strong>Electronics</strong> with lithium-ion batteries (laptops, power tools, e-bikes) are technically fine but the batteries degrade in unconditioned storage and may not work after long periods. For long-term storage, remove the batteries and store them separately, ideally somewhere temperature-stable.</p>
<p><strong>Vinyl records</strong> warp in heat; <strong>candles</strong> melt and stain everything beneath them; <strong>aerosol cans</strong> can fail under temperature extremes (although small numbers of cans for personal use are usually fine). If you're storing for more than three months, the climate-stable difference is genuine — our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> is insulated, ventilated and monitored.</p>"""),
            ('How to check the rules at your chosen facility',
             """<p>Every storage facility has its own version of the prohibited-items list, usually printed on the contract you sign. Read it before signing. The rules are mostly identical across the industry but the specific edge cases (alcohol quantities, ammunition for licensed shooters, commercial stock) vary.</p>
<p>If you're not sure whether something is allowed, ask in writing before move-in day. Facility staff are happy to clarify; a phone call beforehand avoids the situation where the lorry arrives and an item gets refused at the door. We've had customers turn up with bottled propane for a camping setup and have to take it home again.</p>
<p>For removal-firm-managed storage (our depot, for example), the rules are integrated into our <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">written quote</a> — we flag any borderline items at the survey and you know in advance what's coming with us and what isn't. No surprises on the day.</p>"""),
        ],
        'faqs': [
            ("Can I store a washing machine in self-storage?",
             "Yes, but only if it's fully drained, dried and cleaned first. Water residue causes mould inside the drum and damages the bearings over storage time."),
            ("Are petrol items allowed in storage?",
             "No — all fuel must be drained and the tank vented before garden machinery (mowers, strimmers, chainsaws) goes into storage. Bottled gas and propane are always excluded."),
            ("Can I store wine and spirits?",
             "Personal quantities of unopened bottles, yes — lying flat, away from temperature extremes, climate-stable preferred. Commercial-quantity alcohol storage usually needs a separate licence."),
            ("Are electronics OK to store long-term?",
             "Most electronics are fine. Items with lithium-ion batteries should have the batteries removed and stored separately, ideally somewhere temperature-stable. Vinyl records, candles and photographic materials need climate-stable conditions."),
            ("How do I find out exactly what my facility allows?",
             "Read the contract terms before signing — every facility has a prohibited-items list. If anything is borderline, ask in writing before move-in day."),
        ],
    },

    # ---- Topic 19 ----
    {
        'slug': 'benefits-of-professional-packing-service.html',
        'title': "Why You Should Use a Professional Packing Service",
        'desc': "The real benefits of letting professionals pack for you. Save time, reduce stress, and protect your belongings.",
        'kicker': 'Packing services · Forty years of pad-wrap experience',
        'h1': 'Why You Should Use a Professional Packing Service',
        'hero_sub': "Not just convenience. Trained packers, the right materials, an insured outcome, and the most under-rated stress reducer on the whole move.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Why use professional packers',
        'intro_html': """<p style=\"font-size:1.15rem;\">Of all the services on a removals quote, the <a href=\"../full-packing-service.html\">packing line</a> is the one customers most often try to save on first. It's also the line where saving money turns into the most reliable false economy. After packing more than ten thousand homes since 1982 we have a clear, honest view of when professional packing makes sense and when self-pack is fine.</p>
<p>This guide walks through the genuine benefits — beyond “it's faster” — and the specific scenarios where the professional option saves more than it costs. We're a packing service provider so the conclusion is predictable, but the reasoning is worth reading either way.</p>""",
        'sections': [
            ('The damage-rate difference',
             """<p>The single biggest argument for professional packing is the damage rate. In our long-running internal records, self-packed cartons have roughly six times the breakage rate of professionally-packed cartons. The categories that go wrong are predictable: plates stacked flat, wine glasses without internal padding, framed art unprotected at the corners, electronics in over-sized boxes with no internal padding.</p>
<p>The professional difference isn't magic — it's training and materials. Our crews are trained at our own staff training centre (one of only a handful of UK removers with this), they use removal-grade cartons rather than supermarket boxes, and they use proper acid-free tissue rather than newspaper. The materials cost the firm slightly more per move; the damage-rate difference more than pays it back.</p>
<p>The breakage that does happen on professionally-packed jobs is covered by our standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a>. Self-pack damage is typically excluded by default — most insurers consider the customer's packing to be the source of the risk and won't cover it. That alone is often enough to justify the professional pack on high-value contents.</p>"""),
            ('Time and stress — the under-counted savings',
             """<p>The average household has roughly 80 to 120 cartons of contents, plus furniture. A professional pair of packers handles this in six to ten hours, the day before move day. A self-packing household typically spends 30 to 60 hours over three to four weeks doing the same job, around full-time work and other commitments. The labour cost of those hours, valued honestly, almost always exceeds the cost of the professional pack.</p>
<p>Stress is harder to quantify but worth mentioning. The week before move day is consistently the highest-stress week on the whole moving timeline. Adding 30 hours of packing labour to that week, in a house that's increasingly dismantled and inhabitable, is a meaningful psychological cost. Customers who book the <a href=\"../full-packing-service.html\">full packing service</a> consistently report move day as the calmest part of the process.</p>
<p>The other time cost is unpacking. Professionally-packed cartons are labelled by room and contents, numbered, and tracked on a written inventory. Unpacking goes faster because you can find anything you need. Self-packed cartons (no matter how diligent the labelling intention was) are usually a lottery to unpack.</p>"""),
            ('When professional packing makes most sense',
             """<p>Five scenarios where the professional pack is almost always worth it. First, anyone with a busy job. The packing time the week before is real and it costs you sleep, leisure or workplace performance, all of which are more expensive than the packing fee. Second, families with young children. Packing around a toddler is impossibly slow and the safety risks (small parts, tape gun, lifted heavy items) are real.</p>
<p>Third, elderly customers or anyone with mobility limitations. Packing 80+ cartons requires bending, lifting, reaching and crouching for sustained periods — genuinely unsuitable for many people. Fourth, anyone moving high-value contents. The damage-rate difference plus the insurance coverage difference adds up fast on art, antiques, china and electronics. The <a href=\"../white-glove-service.html\">white-glove service</a> is designed for this.</p>
<p>Fifth, anyone moving overseas. <a href=\"../international-removals-eastbourne.html\">International removals</a> require professionally-packed cartons with a verified packing list for customs purposes. Self-pack overseas is technically allowed in some destination countries but typically results in customs inspection delays and sometimes refused shipments. The professional pack is the practical standard.</p>"""),
            ('Hybrid packing — the practical middle ground',
             """<p>The full pack isn't the only option. The most common mid-tier is <strong>fragile-only packing</strong> — the crew handles the breakables (kitchen china, glass, display-cabinet contents, framed art, mirrors) the day before, and the customer self-packs the easy categories (books, clothing, linen, garage contents, hobby kit). About 60% of our packing customers go for this option.</p>
<p>Fragile-only packing is typically £220–£340 for a three-bedroom home, delivered in four to six hours by a trained pair. The customer's self-pack runs alongside in the days before; the crew works around it on the packing day. The damage-rate on a fragile-only pack is essentially identical to a full pack — the fragiles are where the damage risk concentrates.</p>
<p>The other hybrid is <strong>materials-only</strong> — we drop off removal-grade cartons, tape, bubble, tissue and blanket-rentals at your house three to four days before move day, and you do the whole pack yourself. This is the cheapest option and works well for customers with time, but the damage-rate is the same as fully-self-pack with supermarket boxes. The materials are stocked at our <a href=\"../packaging-shop.html\">Lower Dicker packaging shop</a>.</p>"""),
            ('What to ask any packing provider',
             """<p>Questions worth asking before booking any packing service. <em>Are your packers directly employed or sub-contracted?</em> (directly-employed crew are accountable and consistent; sub-contracted day labour isn't). <em>Are they trained at a specific training facility, or on the job?</em> (training centres exist for a reason; the on-the-job version varies wildly).</p>
<p><em>What materials do you use?</em> (removal-grade cartons and proper packing tissue are minimum standards; supermarket boxes and newspaper are red flags). <em>What's covered by insurance?</em> (full pack should be covered for breakage; self-pack often isn't). <em>What's the inventory practice?</em> (every carton should be numbered, labelled and on a written inventory).</p>
<p>Booking the survey takes ten minutes via our <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">online quote form</a>. The surveyor will recommend the right packing level based on the inventory and the move type. If you'd rather just discuss it on the phone first, we're happy to do that — call 01323 848 008.</p>"""),
        ],
        'faqs': [
            ("How much does professional packing cost?",
             "Fragile-only on a 3-bed home: typically £220–£340. Full pack on a 3-bed: typically £450–£800 depending on inventory. Both include all materials and a written inventory."),
            ("Is breakage covered by insurance?",
             "Professional packing is covered by standard goods-in-transit insurance. Self-packed cartons are usually excluded by default — most insurers consider the customer's packing to be the source of risk."),
            ("Can you pack just the kitchen?",
             "Yes — kitchen-only or fragile-only packing is one of our most popular options. Crew handles china, glass, electronics and breakables; you handle books, clothing and easy categories."),
            ("How long does a full pack take?",
             "Six to ten hours the day before move day for a typical 3-bed home. A pair of trained packers, all materials supplied, written room-by-room inventory delivered at the end."),
            ("Do I need to be there during the pack?",
             "Helpful but not essential. Most customers want to be around for the first hour to direct the packers to specific items (e.g. 'these go in storage, these come with us'), then leave the crew to it."),
        ],
    },

    # ---- Topic 20 ----
    {
        'slug': '10-most-commonly-forgotten-moving-items.html',
        'title': "10 Things People Always Forget When Moving House",
        'desc': "Don't get caught out on moving day. Here are the 10 most commonly forgotten items when people move house.",
        'kicker': 'Forgotten items · 40 years of move-day blind spots',
        'h1': '10 Things People Always Forget When Moving House',
        'hero_sub': "The contents of the loft. The garden shed. The freezer. The downstairs cupboard nobody opens. Here are the ten things every move forgets.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Commonly forgotten items',
        'intro_html': """<p style=\"font-size:1.15rem;\">After more than ten thousand moves we've seen the same items get forgotten on move day with surprising consistency. Some are funny (the bathroom toilet roll); some are genuinely expensive (the contents of a wine fridge); some are bureaucratically expensive (the keys to a leasehold property). All ten are preventable with a short walk-through the night before move day.</p>
<p>This is our list of the ten most-forgotten items, based on what our crews actually find left behind. Take a printout of it on move morning. If you'd like the crew to do the walk-through for you, the <a href=\"../full-packing-service.html\">full packing service</a> always includes an end-of-day sweep — but the buck still stops with the customer.</p>""",
        'sections': [
            ('1. The loft hatch',
             """<p>Almost every customer forgets to check the loft on move morning. The contents have usually been packed weeks earlier (good practice — see the <a href=\"what-to-pack-first-when-moving-house.html\">what-to-pack-first guide</a>), but the empty loft isn't always re-checked, and small items occasionally remain — old paperwork, a tube of Christmas lights, a single suitcase.</p>
<p>The fix: physically open the loft hatch and shine a torch into all four corners before the keys go back. Our crews do this on the end-of-day sweep, but it's worth doing yourself as a final check. Loft hatches are also worth photographing closed (with the latch in place) for any future deposit dispute.</p>"""),
            ('2. The garden shed and outbuildings',
             """<p>Sheds, summerhouses, garden offices and outbuildings get packed late and forgotten often. The lawnmower, the strimmer, the BBQ, garden tools, kids' bikes, the spare gas bottle — all common finds at the end of a move. Sheds are physically separate from the house so the natural walk-through can miss them.</p>
<p>The fix: do the shed walk-through as a separate exercise the day before. If you have any petrol-driven garden machinery, drain the fuel into a container and leave the empty tank vented; we won't transport sealed petrol containers and most <a href=\"../storage-eastbourne.html\">self-storage units</a> won't accept them either.</p>"""),
            ('3. The freezer and the wine fridge',
             """<p>Freezer contents are one of the highest-stake forgottens. Either the freezer gets emptied and refilled at the new house (the right approach) or the contents melt in transit and ruin the freezer plus everything around it. Wine fridges are similar — and contain meaningful value if forgotten.</p>
<p>The fix: empty the freezer 24 hours before move day, transfer perishables to cool boxes with ice packs, and run them to the new property in your own car rather than the lorry. Wine fridges should be unplugged the night before, drained of any water trays, and packed cool with bottles separately wrapped. The <a href=\"how-to-pack-kitchen-items-safely.html\">kitchen-packing guide</a> covers more detail.</p>"""),
            ('4. The keys (yes, all of them)',
             """<p>Keys get forgotten on move day with remarkable consistency. The set you handed to the estate agent for viewings. The spare set the neighbour holds. The keys to the leasehold building's front door, the bin store, the bike store. The keys to the loft access, the garage door, the safe in the back of the wardrobe.</p>
<p>The fix: assemble every key for the property in one place a week before move day. Label them clearly with what they open. Hand the entire set to the conveyancer or estate agent on completion day; don't let stray keys leave the property in random people's pockets. The new owner will thank you.</p>"""),
            ('5. The under-stair cupboard',
             """<p>The under-stair cupboard is the unsung black hole of the average British house. It usually contains the hoover, an ironing board, a stack of recycling, three lonely shoes, the box of decorations from two Christmases ago, and a dust-pan-and-brush. Everyone forgets it.</p>
<p>The fix: walk through every cupboard in the house the night before move day with a torch. The under-stair cupboard, the hall cupboard, the utility cupboard, the airing cupboard. Anything that's a "dead corner" is a candidate for forgetting. The crew will do this as part of the end-of-day sweep but it's worth verifying yourself.</p>"""),
            ('6. Outdoor furniture and pots',
             """<p>Garden furniture, outdoor planters, hanging baskets, the BBQ cover, the parasol. Outdoor items get forgotten because they're outside the natural walking path of a final house check. They're also some of the most replaceable items in the house if left behind — but the cost of replacing them adds up.</p>
<p>The fix: walk around the perimeter of the house, including the front garden, the side path and the back garden, the day before move day. Anything you want to take with you should be moved into the house or directly into the lorry. The crew will pack plants (if they're indoor plants in pots) but won't dig anything up.</p>"""),
            ('7. The meter readings',
             """<p>Meter readings aren't a physical item, but they're the most-forgotten admin task of move day. Without a final reading at the old property and an initial reading at the new property, you'll get billed estimated amounts that take weeks to correct.</p>
<p>The fix: photograph the gas meter, electricity meter and water meter at both properties on move morning. Photograph the numbers clearly with a timestamp visible. Email them to yourself so they're date-stamped. Submit the readings to both supplier accounts the same day. This is also the simplest evidence in any future billing dispute.</p>"""),
            ('8. The bathroom essentials',
             """<p>The bathroom is usually packed last, but the last items (toilet roll, hand soap, towel, toothbrush) are also the most likely to be forgotten. Customers arrive at the new house and discover the bathroom is unstocked — and the supermarket isn't around the corner.</p>
<p>The fix: pack a 'first-night' carton (labelled red, loaded last so it comes off first) containing two rolls of toilet paper, hand soap, a hand towel, your toiletries, a toothbrush, prescription medications, and any other bathroom essentials. This carton also doubles as the kitchen first-night carton with the kettle, mugs and tea.</p>"""),
            ('9. Important documents',
             """<p>Passports, birth certificates, mortgage documents, the children's medical records, the dog's vaccination card. Important documents get forgotten because they're often stored separately from the main packing flow — in a drawer in the home office, a safe, or a hidden corner of a wardrobe.</p>
<p>The fix: gather every important document in one folder a week before move day. Travel with that folder in your own car, not in the lorry. Standard goods-in-transit insurance excludes irreplaceable documents, so if the lorry is delayed, the documents are still with you. The <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance details</a> page has the full exclusion list.</p>"""),
            ('10. The neighbours’ contact details',
             """<p>This one is consistently overlooked. The neighbour who took the parcel last week, the neighbour who feeds the cat when you're away, the neighbour you exchange Christmas cards with. Their contact details are useful for redirecting post, occasional questions about the property, and just polite goodbye-and-stay-in-touch reasons.</p>
<p>The fix: a week before move day, pop next door and exchange phone numbers and email addresses with anyone you'd want to stay in touch with. Set up the Royal Mail post-redirect service so post forwards for six to twelve months. Tell anyone who has a key to your property to return it. Leave a forwarding note on the inside of the front door for any post that arrives in the first week.</p>"""),
        ],
        'faqs': [
            ("Will the crew check for forgotten items?",
             "Yes — every move includes an end-of-day sweep where the crew walks every room, cupboard and loft. But the buck still stops with the customer — the crew can miss what they can't see."),
            ("What should be in the 'first-night' carton?",
             "Kettle, mugs, tea/coffee, toilet paper, hand soap, toiletries, phone charger, prescription medications, kitchen towel, one mug per family member. Labelled red, loaded last."),
            ("Should documents travel in the lorry?",
             "No. Passports, certificates, important paperwork, jewellery, prescription medications and cash should all travel with you in your car. Standard transit insurance excludes irreplaceable documents."),
            ("Do I need to be there for the final walk-through?",
             "Yes, ideally. The crew can do the sweep, but only you know whether something is meant to stay (a fitted appliance, a chosen fitting) or come with you."),
            ("How do I make sure nothing's left at the new property either?",
             "The same walk-through in reverse — once the crew has unloaded, walk every room and confirm the inventory list matches what's arrived. Flag any missing items before the crew leaves."),
        ],
    },
]


# ----------------------- TEMPLATE LOADER ----------------------------
TEMPLATE = open(TEMPLATE_PATH, encoding='utf-8').read()

# Find the boundaries:
# 1. Replace head metadata block (title, description, og, twitter)
# 2. Replace JSON-LD blocks
# 3. Replace hero <header class="np-hero"> ... </header>
# 4. Replace breadcrumb
# 5. Replace body sections from <section class="np-section"> after hero
#    up to and including the FAQ section.

def normalize_for_id(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def render_section(h2: str, html_body: str, soft: bool) -> str:
    cls = 'np-section np-section-soft' if soft else 'np-section'
    return f"""  <section class=\"{cls}\">
    <div class=\"np-inner\">
      <h2>{h2}</h2>
      {html_body}
    </div>
  </section>
"""

def render_faq(faqs: list[tuple[str, str]]) -> str:
    items = []
    for q, a in faqs:
        items.append(f'      <details><summary>{q}</summary><p>{a}</p></details>')
    return ('  <section class="np-section np-faq">\n'
            '    <div class="np-inner">\n'
            '      <h2>Frequently asked questions</h2>\n'
            + '\n'.join(items) + '\n'
            '    </div>\n'
            '  </section>\n')

def render_related(slug: str) -> str:
    return """  <section class="np-section np-related" aria-label="Related pages">
    <div class="np-inner">
      <h2>Related pages on our site</h2>
      <ul class="np-related-list">
        <li><a href="index.html">All blog articles</a></li>
        <li><a href="../mark-ratcliffe-moving-online-removals-quote.html">Get a free moving quote</a></li>
        <li><a href="../full-packing-service.html">Full packing service</a></li>
        <li><a href="../storage-eastbourne.html">Self-storage in Sussex</a></li>
        <li><a href="../international-removals-eastbourne.html">International removals</a></li>
        <li><a href="../piano-moving.html">Piano moving</a></li>
        <li><a href="../antiques-moving.html">Antiques moving</a></li>
        <li><a href="../removals-eastbourne.html">Removals in Eastbourne</a></li>
        <li><a href="../removals-brighton.html">Removals in Brighton</a></li>
        <li><a href="../areas-covered.html">All areas covered</a></li>
        <li><a href="../reviews.html">Read customer reviews</a></li>
        <li><a href="../about-us.html">About Mark Ratcliffe Moving</a></li>
      </ul>
    </div>
  </section>
"""

def render_cta() -> str:
    return """  <section class="np-section np-cta-band">
    <div class="np-inner">
      <h2>Ready to book your move?</h2>
      <p>Free in-home or video survey, written fixed-price quote, BAR-protected deposit. Sussex&rsquo;s family-run remover since 1982.</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
  </section>

"""

def render_body(blog: dict) -> str:
    parts = [f"""  <nav class="np-breadcrumb"><a href="../index.html">Home</a> &rsaquo; <a href="index.html">Blog</a> &rsaquo; {blog['breadcrumb']}</nav>

  <header class="np-hero">
    <div class="np-hero-inner">
      <div class="np-kicker">{blog['kicker']}</div>
      <h1>{blog['h1']}</h1>
      <p class="np-hero-sub">{blog['hero_sub']}</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="../images/{blog['hero_img']}" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high" width="1000" height="750">
  </header>

  <section class="np-section">
    <div class="np-inner">
      {blog['intro_html']}
    </div>
  </section>

  <aside class="np-toc-mount" aria-label="Table of contents"></aside>

"""]
    # Alternate soft/regular sections
    for i, (h2, body) in enumerate(blog['sections']):
        parts.append(render_section(h2, body, soft=(i % 2 == 0)))
    parts.append(render_cta())
    parts.append(render_faq(blog['faqs']))
    parts.append(render_related(blog['slug']))
    return ''.join(parts)


def render_head(blog: dict) -> str:
    canonical = f"https://www.markratcliffemoving.co.uk/blog/{blog['slug']}"
    image_url = f"https://www.markratcliffemoving.co.uk/images/{blog['hero_img']}"
    ld_blog = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": blog['h1'],
        "description": blog['desc'],
        "image": image_url,
        "datePublished": "2026-05-19",
        "dateModified": "2026-05-19",
        "author": {"@type": "Organization", "name": "Mark Ratcliffe Moving & Storage"},
        "publisher": {"@id": "https://www.markratcliffemoving.co.uk/#organization"},
        "mainEntityOfPage": canonical,
    }
    ld_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": "https://www.markratcliffemoving.co.uk/"},
            {"@type": "ListItem", "position": 2, "name": "Blog",
             "item": "https://www.markratcliffemoving.co.uk/blog/index.html"},
            {"@type": "ListItem", "position": 3, "name": blog['breadcrumb']},
        ],
    }
    ld_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in blog['faqs']
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{blog['title']}</title>
  <meta name="description" content="{blog['desc']}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving &amp; Storage">
  <meta name="theme-color" content="#4d2e8f">
  <meta property="og:title" content="{blog['title']}">
  <meta property="og:description" content="{blog['desc']}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Mark Ratcliffe Moving &amp; Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://cdn.yoshki.com" crossorigin>
  <link rel="preload" as="image" href="../images/{blog['hero_img']}" fetchpriority="high">
  <link href="../css/normalize.css?v=20260546" rel="stylesheet">
  <link href="../css/components.css?v=20260546" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260546" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260546" rel="stylesheet">
  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>WebFont.load({{classes:true,timeout:2000,google:{{families:["Inter:400,500,600,700,800","Fraunces:400,500,600,700"]}}}});</script>
  <link href="../images/favicon.png" rel="shortcut icon">
  <link href="../images/webclip.png" rel="apple-touch-icon">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q111LKQEBP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-Q111LKQEBP');</script>
  <script type="application/ld+json">{json.dumps(ld_blog, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(ld_breadcrumb, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
  <script>(function(){{var u=location.protocol+"//"+location.host+location.pathname;var d=document,h=d.head;var c=d.createElement("link");c.setAttribute("rel","canonical");c.setAttribute("href",u);h.appendChild(c);var o=d.createElement("meta");o.setAttribute("property","og:url");o.setAttribute("content",u);h.appendChild(o);}})();</script>
  <script defer src="../js/nofollow-shim.js?v=20260546"></script>
  <script defer src="../js/mobile-nav.js?v=20260546"></script>
</head>
"""

# Pull the nav block + footer block from the template (between </head> and the body content)
NAV_START = TEMPLATE.index('<body>')
NAV_END   = TEMPLATE.index('<nav class="np-breadcrumb">')
NAV_BLOCK = TEMPLATE[NAV_START:NAV_END]

FOOTER_START = TEMPLATE.index('<footer')
FOOTER_END   = TEMPLATE.rindex('</html>') + len('</html>')
FOOTER_BLOCK = TEMPLATE[FOOTER_START:FOOTER_END]


def render_blog(blog: dict) -> str:
    head = render_head(blog)
    body = render_body(blog)
    return head + NAV_BLOCK + body + FOOTER_BLOCK


# ----------------------- WRITE FILES --------------------------------
created = 0
for blog in BLOGS:
    out_path = os.path.join('blog', blog['slug'])
    html = render_blog(blog)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    created += 1
    print(f'  wrote {out_path}')

print(f'\nCreated {created} new blog posts.')
