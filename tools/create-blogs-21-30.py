#!/usr/bin/env python3
"""Generate blog posts 21-30 from the user's numbered list."""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TEMPLATE_PATH = 'blog/cost-of-moving-house-sussex-2026.html'

BLOGS = [
    # ---- Topic 21 ----
    {
        'slug': 'moving-house-with-children.html',
        'title': 'Moving House with Children: How to Make It Easier',
        'desc': 'Moving with kids? Our practical guide gives you tips to keep your children happy and reduce stress for the whole family during a house move.',
        'kicker': 'Family moves · Forty years of moving households with kids',
        'h1': 'Moving House with Children — How to Make the Whole Family Calmer',
        'hero_sub': "Kids feel the upheaval of a house move more than adults realise. Here is what a family-run remover has learned about keeping the whole household sane.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Moving with children',
        'intro_html': """<p style=\"font-size:1.15rem;\">A house move is one of the higher-stress life events for adults — for children it can be even more disorientating. Their bedroom is taken apart, their toys vanish into boxes, their familiar street disappears overnight, and the grown-ups around them are visibly more anxious than usual. After running <a href=\"../removals-eastbourne.html\">family-home removals across Sussex</a> for forty years we&rsquo;ve seen what works to keep children settled and what doesn&rsquo;t. This guide collects the practical advice we give every family at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a>.</p>
<p>The principle is straightforward: include the children in the process where you can, keep their familiar items together until the last moment, and plan the actual move day so they don&rsquo;t spend it bored in an empty house. The details below break this down by age band — toddlers, primary-school children, and teenagers all need different things.</p>""",
        'sections': [
            ('Involve them in the planning, age-appropriately',
             """<p>Children handle change much better when they understand it. For toddlers, that means a simple story-book explanation a fortnight before move day: &ldquo;we&rsquo;re going to live in a new house with a new garden&rdquo;. For primary-age children, give them a calendar with the move date marked and a small countdown they can tick off; this turns the unknown into something concrete. For teenagers, treat them like co-conspirators — share the floor plans, let them choose their new bedroom, ask their opinion on paint colours.</p>
<p>Visit the new house with the children at least once before move day if it&rsquo;s practical. Familiarity reduces anxiety. Show them their future bedroom, the garden, the local park, the nearest sweet shop. Take a photo of each space so they can look at it during the run-up. If you&rsquo;re moving from <a href=\"moving-from-london-to-sussex.html\">London to Sussex</a> or a similarly long move, a weekend visit is well worth the travel cost.</p>
<p>Pack a small box of their favourite things last and unpack it first at the new house — favourite teddy, two or three books, a small toy, the pillow they&rsquo;ve always slept on. This is the children&rsquo;s version of the adult &lsquo;first-night carton&rsquo; (covered in the <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a>). Knowing that bedtime will look and feel familiar is half the settling battle.</p>"""),
            ('Move-day logistics — where the children actually go',
             """<p>The single biggest practical question is what to do with the children on move day itself. The honest answer: somewhere else, if at all possible. The lorry, the crew, the dismantled house, the parents focused on logistics — none of this is fun for a child. Grandparents, friends, paid childcare for the day, school holidays days at a local club. Whatever works.</p>
<p>If they have to be at the property, set up a single safe space for them — usually the front sitting room or a quiet bedroom — with their favourite activities, snacks, drinks and a charged tablet or screen. Keep that room off-limits to the crew until everything else is packed. This stops them being underfoot during loading and gives them a base.</p>
<p>For the actual travel to the new house, pack a clearly-labelled overnight bag for each child: two days&rsquo; clothes, toothbrush, pyjamas, favourite teddy, two books, a portable game or activity. This bag travels in your car, not in the lorry. If the lorry runs late (it sometimes does — completion-day chains slip), you can still get the children fed, washed and into a familiar pair of pyjamas at the new house.</p>"""),
            ('The first 48 hours in the new house',
             """<p>The instinct is to unpack everything as fast as possible. The better approach with children: set up THEIR rooms first, even before the parent bedroom. A familiar bedroom by bedtime on move day is the single biggest contributor to a calm first night. Pad-wrapped furniture from our <a href=\"full-pad-wrap-protection-explained.html\">pad-wrap method</a> can be carried in still wrapped and unwrapped in their final position — so beds, wardrobes and chests of drawers can be set up quickly in the children&rsquo;s rooms.</p>
<p>Get the kitchen functional next — the kettle, the breakfast things, one set of plates and cutlery per family member. The order matters: kids want familiar food, parents want tea, and nobody wants to be searching for the toaster on the morning after move day. The detailed kitchen order is in the <a href=\"how-to-pack-kitchen-items-safely.html\">kitchen-packing guide</a>.</p>
<p>Walk the neighbourhood with the children on the first afternoon — find the nearest park, the local shop, the bus stop, the school if it&rsquo;s pre-term. A short walk shifts the new house from &lsquo;a strange place&rsquo; to &lsquo;our area&rsquo; surprisingly quickly. Photograph each landmark; some kids like to make a map.</p>"""),
            ('School transitions and the academic year',
             """<p>If your move involves a school transition (between primary and secondary, or between schools mid-year), the timing matters more than the location. Mid-year transitions are harder than between-year-group ones. If you have any flexibility on the move date, aligning with the summer holidays — late July, August, early September — is the best single thing you can do.</p>
<p>For East Sussex moves where school catchments are part of the decision, get the application in well before the published deadline. East Sussex County Council&rsquo;s admissions process has hard cut-off dates and out-of-catchment applications are competitive. The <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne area guide</a> walks through the local schools and the <a href=\"best-areas-to-live-east-sussex-2026.html\">best-areas-in-East-Sussex guide</a> covers the wider county.</p>
<p>Once school transfers are confirmed, contact the new school directly to ask about settling-in support. Most state primaries and secondaries have a system for new arrivals — a buddy, a class introduction, a meet-the-teacher session. Pushing for this in the first week of term makes a meaningful difference.</p>"""),
            ('Settling pets and managing the noise',
             """<p>Pets and children together on move day are a particular challenge. If you have a dog or cat, arranging for them to spend move day with friends or family helps both pets and kids — the children see less stress in the household and the pets see less chaos. The full pet-specific guide is at <a href=\"moving-house-with-pets.html\">moving with pets</a>.</p>
<p>Move-day noise can be genuinely distressing for younger children. Removal lorries, crew chatter, doors slamming, furniture being lifted. Headphones and a tablet with a favourite show help. So does giving the child a specific small &lsquo;job&rsquo; — packing their favourite toys into a labelled box, being the &lsquo;keeper of the snacks&rsquo;, supervising a teddy bear who isn&rsquo;t allowed in the lorry.</p>
<p>For high-value items going in the lorry — antiques, art, anything precious to the family — explain to older children that these items get extra protection (our <a href=\"../white-glove-service.html\">white-glove service</a> or <a href=\"../antiques-moving.html\">antiques moving</a> options). Knowing the family treasures are being looked after carefully is reassuring in its own way.</p>"""),
            ('A short post-move checklist for the family',
             """<p>Once the dust has settled and the boxes are mostly unpacked, the post-move week is when the cumulative tiredness shows. Build in some downtime — a family meal at the new local pub, a Saturday morning park visit, a takeaway evening. The temptation to power through the unpacking can leave everyone exhausted by week two.</p>
<p>For the admin side: register the children with the new GP and dentist in the first week (waits can be 4–8 weeks for appointments). Update the address with the school, any after-school clubs, the GP records, the children&rsquo;s health visitor records. The <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> has a full admin checklist.</p>
<p>Last point: the children may show the impact of the move two or three weeks after the actual day, not on the day itself. Sleep disturbance, clinginess, lower mood are all common and almost always resolve inside a month. If the patterns persist past a few weeks, the new school&rsquo;s pastoral team or the GP can help. Most families are completely settled six weeks in.</p>"""),
        ],
        'faqs': [
            ("Should the children be at the house on move day?",
             "If at all possible, no. Grandparents, friends, holiday club, paid childcare — whatever works. The lorry, the crew, the dismantled house, the parents focused on logistics — none of this is fun or safe for a child. If they have to be there, set up a single off-limits room for them."),
            ("How early should we tell young children about the move?",
             "Toddlers: a fortnight before, with a simple story-book explanation. Primary-age: 4–6 weeks before, with a calendar countdown they can tick off. Teenagers: as early as the decision is made; they want to feel consulted rather than informed."),
            ("What goes in the children's overnight bag?",
             "Two days' clothes, pyjamas, toothbrush, favourite teddy, two books, charged tablet or activity, snacks, water bottle. Travel with you in your own car, not in the lorry. If the lorry's delayed, the children are still set for the night."),
            ("Should the children's rooms be unpacked first?",
             "Yes — set up their rooms before the parent bedroom. A familiar bedroom by bedtime on move day is the single biggest contributor to a calm first night. Pad-wrapped furniture can be carried in still wrapped and unwrapped in its final position quickly."),
            ("Can your crew be quiet around younger children?",
             "Yes — let us know at survey if you have a baby or a child with sensory sensitivities and we'll brief the crew. Loading and unloading make noise, but we can manage the chatter and the timing of the more disruptive activities around quiet hours."),
        ],
    },

    # ---- Topic 22 ----
    {
        'slug': 'moving-house-with-pets.html',
        'title': 'Moving House with Pets: Complete Guide for Cat & Dog Owners',
        'desc': 'Moving with dogs or cats? Learn how to prepare your pets for moving day, reduce their anxiety, and settle them into your new home safely.',
        'kicker': 'Cats · Dogs · Small animals · 40 years of pet-friendly moves',
        'h1': 'Moving House with Pets — The Complete Guide for Cat &amp; Dog Owners',
        'hero_sub': "Pets read a house move very differently from humans. Here is how to plan the day so the animals stay calm and arrive safely settled.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Moving with pets',
        'intro_html': """<p style=\"font-size:1.15rem;\">Almost every <a href=\"../about-us.html\">family-run Sussex move</a> we&rsquo;ve done over forty years has involved a pet somewhere — usually a dog or a cat, occasionally a hamster, a rabbit, a parrot, or one memorable family of pygmy goats. Pets read a house move very differently from people: the sounds, the strangers, the dismantling of familiar furniture, the front door propped open for hours — every signal says something is wrong.</p>
<p>This guide covers the practical preparation for the four most common pet situations (cats, dogs, small caged animals, and exotics), the move day itself, and the first week in the new house. The aim is to keep the pet safe and avoid the cluster of avoidable problems we see most often: escaped cats, anxious dogs, transit-stressed small animals.</p>""",
        'sections': [
            ('Cats — the escape risk is your biggest issue',
             """<p>Cats handle moves badly and the biggest risk by some margin is escape. A panicked cat can squeeze through gaps you didn&rsquo;t know existed, vanish into the lorry while it&rsquo;s being loaded, or bolt the moment a door opens at the new house. The single most important rule: keep the cat confined to one carrier or one closed room throughout the entire move day.</p>
<p>The pattern that works: confine the cat to a single room the night before move day with food, water, litter tray, favourite blanket. Tape a clear sign to the door (&ldquo;DO NOT OPEN — CAT&rdquo;) so the crew knows not to go in. We pack and load the rest of the house around this. The cat travels with you in your own car at the end, ideally in a sturdy carrier.</p>
<p>At the new house, repeat the process in reverse — set up one quiet room with food, water, litter tray, blanket from the old house, and the favourite toy. Release the cat into this single room before any unpacking starts. Don&rsquo;t let the cat outdoors for at least two weeks at the new property; the standard guidance is &ldquo;butter on the paws&rdquo; (which is mostly placebo for owners) plus a fortnight indoors so they learn the new house as home.</p>"""),
            ('Dogs — exercise and boarding the move day',
             """<p>Dogs are more adaptable than cats but they still feel the upheaval. Most dogs do best out of the house entirely on move day — a long walk with a friend, a day at boarding kennels, an afternoon with grandparents. The chaos of removal day plus open doors plus strangers plus your own stress is a recipe for anxious behaviour.</p>
<p>If the dog has to be at the property, pick one secure room (utility room, garden if fully fenced) and keep them there during loading. Maintain their normal walking and feeding schedule as far as possible — a missed walk on move day adds to the stress. Travel with them in your own car, never in the lorry. We don&rsquo;t put pets in the lorry under any circumstances; it&rsquo;s neither legal nor safe.</p>
<p>At the new house, the priorities are familiar smells and a quiet base. Set up the dog&rsquo;s bed, blankets and water in one corner before doing anything else. Keep them on lead for the first few outdoor visits — even fully-trained dogs can spook at unfamiliar street smells. The first week is when most lost-pet calls happen; the local <a href=\"moving-to-eastbourne-area-guide.html\">vet registration</a> and updated microchip details should be top of the new-week list.</p>"""),
            ('Small caged animals — temperature and motion are the problems',
             """<p>Hamsters, rabbits, guinea pigs, gerbils, birds and similar small pets are best moved in their normal cage with extra absorbent bedding to soak up any spillage during transit. The cage travels in your own car, never in the lorry — temperature swings in a moving lorry can be dangerous for small mammals, particularly in summer or winter extremes.</p>
<p>Reduce or remove water bottles for the actual journey to prevent spillage; a small water-soaked piece of cucumber or apple provides enough hydration for a 1–2 hour drive. For longer drives (over four hours), stop in a shaded place and offer water briefly. Cover the cage partially with a light cloth to reduce visual stimulation; full coverage isn&rsquo;t necessary.</p>
<p>At the new house, set up the cage in a quiet room with stable temperature before introducing the pet. Birds particularly benefit from the cage being in the same orientation (window-facing or wall-facing) as in the old house. Maintain the normal feeding and cleaning schedule from day one; consistency matters more for small pets than for cats or dogs.</p>"""),
            ('Exotic pets and the special-case animals',
             """<p>Snakes, lizards, fish, larger parrots and exotic mammals each have their own requirements that are beyond the standard remover&rsquo;s scope. Aquariums in particular cannot be moved with water still in them — drain the tank, transport the fish in oxygenated bags from your local aquatic shop, and refill at the new house. The decor and substrate move separately.</p>
<p>Reptiles need temperature continuity — the journey itself is rarely fatal but extreme cold (winter moves) or heat (summer moves) can be. A heat pad with a battery pack or a thermal cool box is the standard approach. Talk to your reptile vet a week before move day for case-specific advice.</p>
<p>For valuable or particularly delicate pets — show animals, working dogs, breeding stock — we sometimes recommend dedicated pet transport services that specialise in this work. Our crews don&rsquo;t handle animal transport; we focus on the household contents. Mention any unusual pet situations at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we&rsquo;ll suggest a local specialist if needed.</p>"""),
            ('Admin — microchips, vets and insurance updates',
             """<p>The single most important post-move admin task for any pet owner is updating the microchip database with your new address. By UK law, microchips must reflect the current keeper&rsquo;s contact details, and an unupdated chip on a missing cat or dog turns a quick reunion into an expensive ordeal. Most microchip databases let you update online inside ten minutes.</p>
<p>Register with a new vet inside the first week. Most local practices accept new patients quickly. Transfer the medical records from the old vet (they&rsquo;ll usually send them on request). If your pet has ongoing prescriptions, make sure you have at least a fortnight&rsquo;s supply in hand to bridge the changeover. The <a href=\"how-to-prepare-for-your-house-move.html\">8-week preparation guide</a> covers the full admin checklist.</p>
<p>Pet insurance policies need address updates; some change in premium based on postcode. Ditto if you&rsquo;re changing from a postcode with low animal crime to one with higher (or vice versa). The local council&rsquo;s dog warden service may have a registration requirement for dogs; check the new council&rsquo;s website.</p>"""),
            ('Settling in — the first month',
             """<p>Pets typically take longer than humans to settle. Two to four weeks is normal for cats; one to two weeks for dogs; a few days for small caged animals. The signs of settling: normal appetite returning, normal sleep patterns, normal play behaviour, and (for cats and dogs) exploration of the new house at their own pace.</p>
<p>Signs of ongoing stress: persistent loss of appetite past 48 hours, hiding for more than three or four days, excessive vocalising, toilet issues, aggressive behaviour. Most of these resolve naturally inside a fortnight. If they persist past three weeks, a vet visit is worth the consultation fee — anxiety can be treated with a short course of medication if needed.</p>
<p>If your move was long-distance (London-to-Sussex, for example — see the <a href=\"moving-from-london-to-sussex.html\">London-to-Sussex guide</a>) or international (the <a href=\"../international-removals-eastbourne.html\">international removals page</a> has the basics), pet relocation needs additional planning around quarantine rules, vaccinations and import certificates. Specialist pet-relocation firms handle these end-to-end.</p>"""),
        ],
        'faqs': [
            ("Can pets travel in the removal lorry?",
             "No. We don't transport live animals under any circumstances — it's neither legal nor safe. Pets travel with you in your own car, in a sturdy carrier for cats and small animals, or on the back seat with a harness for dogs."),
            ("How long before I let my cat outside at the new house?",
             "Two weeks indoors at the new property is the standard guidance. Cats learn the house as home during this time and are far less likely to try to return to the old property. Once outdoors, supervise the first few visits."),
            ("Should I sedate my pet for the move?",
             "Usually no. Routine sedation isn't recommended for healthy adult pets — it can mask warning signs of stress and add risk. For genuinely anxious pets, a vet can prescribe a one-day calming medication, but this is a vet-led decision."),
            ("What about feeding on move day?",
             "Light meal at the usual time, then no large meals during transit. Cats and dogs can get travel-sick; small mammals shouldn't have full water bottles. Resume normal feeding once the pet is settled in the new house."),
            ("Do you handle pet relocation for international moves?",
             "We don't transport pets ourselves, but for international moves we work alongside specialist pet-relocation firms who handle vaccinations, paperwork and the transit itself. Mention this at survey and we'll recommend a partner."),
        ],
    },

    # ---- Topic 23 ----
    {
        'slug': 'moving-from-london-to-sussex.html',
        'title': "Moving from London to Sussex: What You Really Need to Know",
        'desc': "Making the move from London to Sussex? Here's what to expect, how much it costs, and tips to make the transition smoother.",
        'kicker': 'London → Sussex · One of our most-run weekly routes',
        'h1': 'Moving from London to Sussex — What You Really Need to Know',
        'hero_sub': "The price differences, the practical logistics, the lifestyle reset, and the move-day specifics from one of the most-asked routes on our diary.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'London to Sussex',
        'intro_html': """<p style=\"font-size:1.15rem;\">The London-to-Sussex move has been one of the steadiest routes on our weekly diary for two decades, and the pace has only accelerated since 2020. The pull factors are consistent: cheaper houses, better space-per-pound, strong schools, fast trains, a coastline. The push factors are familiar to anyone who&rsquo;s lived in a London zone 3 or 4 for a decade or more. We move dozens of London-to-Sussex households every year and this guide collects the practical advice we give every family at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a>.</p>
<p>The structure below walks through the lifestyle reset (what changes about everyday life), the financial picture (what you can actually expect to gain), and the move-day logistics. The aim is to make sure you arrive in Sussex with realistic expectations and a calm move-day plan.</p>""",
        'sections': [
            ('The lifestyle reset — what actually changes',
             """<p>The single biggest lifestyle change is the slower default tempo. London runs at a pace that residents stop noticing until they leave; Sussex doesn&rsquo;t. Restaurants close earlier, shops aren&rsquo;t open 24 hours, public transport is less frequent, and a meaningful share of evenings end with most people at home rather than out. For families with young children this is overwhelmingly a positive. For singles in their twenties and early thirties used to a busy London social life it&rsquo;s the change that takes longest to adjust to.</p>
<p>Car dependence varies sharply by destination. <a href=\"moving-to-brighton-area-guide.html\">Brighton</a>, <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne</a>, <a href=\"moving-to-hastings-area-guide.html\">Hastings</a> and Lewes are walkable, transit-friendly and many residents don&rsquo;t own a car. The smaller towns and Downland villages (Forest Row, Mayfield, Wadhurst, the Hailsham hinterland) need a car for everyday life. If you&rsquo;re car-free in London and want to stay that way, your destination choice is meaningful.</p>
<p>The countryside, the beaches and the South Downs become genuinely part of everyday life rather than weekend outings. Most Sussex households take this for granted within a month. For Londoners arriving from the inner zones, the abundance of outdoor space — proper countryside walks within a 10-minute drive — is consistently the part they enjoy most. Have a look at the <a href=\"best-areas-to-live-east-sussex-2026.html\">best-areas-in-East-Sussex guide</a> for the lifestyle comparison.</p>"""),
            ('The financial picture — what you actually gain',
             """<p>The price differential between London and East Sussex is real but smaller than the headlines suggest in 2026. A three-bedroom Victorian terrace in zone 3/4 London might sell at £700–£900k; the same house in Eastbourne or Hastings is £400–£600k. That gap funds a meaningful deposit-paydown or a step up to a four-bedroom property. West Sussex (Chichester, Worthing, Horsham) sits in between.</p>
<p>The non-mortgage costs shift in your favour. Council tax bands are usually lower; parking permits cheaper; food and household-supplies prices comparable; school fees (if you&rsquo;re using independents) are 20–30% lower at equivalent schools. The compensating cost is the commute: a London Bridge season ticket from Eastbourne in 2026 is £6–7k a year, from Hastings around £6k, from Brighton £4.5k. Factor this into the total household budget.</p>
<p>The full cost picture for the move itself is in our <a href=\"cost-of-moving-house-sussex-2026.html\">2026 cost of moving guide</a> — a typical 3-bed London-to-Eastbourne move sits in the £1,100–£1,500 range, plus optional packing services (£220–£800 depending on scope), plus stamp duty and conveyancing on the property side.</p>"""),
            ('Commute realities — the train timings',
             """<p>If a London commute is part of the plan, the train timings matter. Brighton to London Victoria via Thameslink: 54 minutes direct, every 10 minutes peak. Eastbourne to London Victoria: 90 minutes via Lewes, half-hourly. Hastings to London Charing Cross: 90 minutes, hourly. Lewes to London Victoria: 70 minutes, half-hourly. Worthing to London Victoria via Three Bridges: 90 minutes. Chichester to London Victoria via Three Bridges: 100 minutes.</p>
<p>The reliability of the southern rail network has improved significantly since 2024 but engineering works on weekends and bank holidays still happen. If you commute five days a week, factor in monthly disruption of one or two days. Hybrid working (2–3 days office, 2–3 days home) is the practical pattern for most London commuters we move; full-time office attendance from East Sussex is uncommon now.</p>
<p>Annual season tickets are paid up front and need committing to. If you&rsquo;re moving with uncertainty about whether the commute will work, monthly tickets are 30% more expensive but let you bail out without losing money. Half-year passes split the difference. Confirm the office attendance pattern with your employer before committing to the season ticket.</p>"""),
            ('Picking the right Sussex destination',
             """<p>For families with school-age children: <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne</a> (large town, multiple secondary options, longer commute), <a href=\"moving-to-brighton-area-guide.html\">Brighton/Hove</a> (city character, faster commute, complex catchments), or one of the Downland-adjacent towns (Lewes, Burgess Hill, Haywards Heath) with the village-school option. Each has trade-offs covered in the <a href=\"best-schools-eastbourne-families.html\">Eastbourne schools guide</a> and the wider <a href=\"best-areas-to-live-east-sussex-2026.html\">best-areas guide</a>.</p>
<p>For young professional couples wanting a Sussex lifestyle without giving up easy London access: Lewes, Brighton, or Hove. Quick trains, urban character, walkable centres. For older couples or downsizers: Eastbourne, Worthing, Bexhill, Chichester. Slower pace, more space, longer trains.</p>
<p>For families with budget for a country property: the Downland villages on the High Weald — Mayfield, Wadhurst, Crowborough, Forest Row, Robertsbridge. Cottage-style or larger detached properties, smaller schools, real rural feel. The <a href=\"moving-to-listed-building-sussex.html\">listed-building guide</a> covers what to expect for period properties in these areas.</p>"""),
            ('The move-day logistics from London',
             """<p>A typical London-to-Sussex move is a single-day job with one crew, leaving our <a href=\"../about-us.html\">Lower Dicker depot</a> at first light to be in London by mid-morning. Loading takes 4–8 hours depending on inventory size and access; the return drive is 1.5–2.5 hours; unload finishes mid-to-late afternoon. We pad-wrap everything in your London home before it leaves the room — see the <a href=\"how-our-pad-wrap-service-protects-furniture.html\">pad-wrap service guide</a>.</p>
<p>The chain-day completion timings shape the schedule. Most London sales complete at noon or 1pm, which means the lorry arrives at 7–8am, loading runs through the morning, and we leave the property as soon as keys are released. For the new property, we aim to be parked outside within 15 minutes of your conveyancer&rsquo;s funds-released notification. If the chain slips by an hour or two — which happens — we wait without extra charge.</p>
<p>London-specific issues: parking suspensions in most boroughs (£100–£300 depending on the postcode, applied for 10 working days ahead), lift-booking for blocks of flats, weekend-only restrictions in some pedestrianised streets. We&rsquo;ll spot all of these at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> — survey in person where possible, video survey otherwise.</p>"""),
            ('The first month in Sussex',
             """<p>Schools first if children are involved (admissions deadlines have hard cut-offs). GP and dentist registration in week one. Council tax setup the day after completion. Broadband ordered three weeks ahead of move day (Openreach engineer slots can run 2–3 weeks). Sign up for the local council&rsquo;s email newsletter. The full admin sequence is in the <a href=\"how-to-prepare-for-your-house-move.html\">8-week preparation guide</a>.</p>
<p>On the social side, Londoners often find the rhythm shift takes 2–3 months. Join one local thing — a parkrun, a walking group, the village pub quiz, a class. Sussex doesn&rsquo;t do strangers-at-the-bar in the way London bars do; the village pub model needs you to show up multiple Friday evenings before becoming a face people recognise.</p>
<p>The other thing worth saying: most Londoners we move report a quiet relief at month three. The pace becomes pleasant rather than disorientating, the new house starts to feel like home, and the question of &ldquo;was this the right decision&rdquo; mostly disappears. The minority that don&rsquo;t settle usually find it&rsquo;s the commute that breaks the equation, not the lifestyle.</p>"""),
        ],
        'faqs': [
            ("How long does a London-to-Sussex move take?",
             "Single day with one crew for most 3-bed moves. Lorry leaves Lower Dicker at first light, in London by mid-morning, load through the day, return drive 1.5–2.5 hours, unload mid-to-late afternoon. Larger 4–5 bed moves split across two days or two crews."),
            ("How much does it cost?",
             "A typical 3-bed London-to-Eastbourne move sits in the £1,100–£1,500 range. Add £220–£340 for fragile-only packing or £450–£800 for a full pack. The detailed breakdown is in the cost-of-moving guide."),
            ("Do you handle London parking suspensions?",
             "We can advise on the application but the customer applies through the relevant borough council ten working days ahead. Costs vary by borough (£100–£300). Some buildings also need lift bookings — we'll flag this at survey."),
            ("Which is easier from London — Brighton or Eastbourne?",
             "Brighton — direct Thameslink route, 54 minutes, frequent. Eastbourne is via Lewes (90 minutes, half-hourly). Hastings is on the slower Charing Cross line (90 minutes, hourly)."),
            ("Can you do the move on a Saturday?",
             "Yes — Saturday moves at no premium, Sunday on request. Many London buildings actually require weekend moves because of weekday parking restrictions in pedestrianised areas. We'll work out the right day at survey."),
        ],
    },

    # ---- Topic 24 ----
    {
        'slug': 'best-schools-eastbourne-families.html',
        'title': 'Best Schools in Eastbourne – Guide for Families Moving to the Area',
        'desc': 'Looking for the best schools in Eastbourne? Our guide helps families choose the right area based on education and school quality.',
        'kicker': 'Eastbourne schools · A practical guide for relocating families',
        'h1': 'Best Schools in Eastbourne — A Guide for Families Moving to the Area',
        'hero_sub': "State, independent, primary, secondary. The schools, the catchments, the application deadlines, and where families typically settle.",
        'hero_img': 'mark-ratcliffe-vans-front2.webp',
        'breadcrumb': 'Eastbourne schools',
        'intro_html': """<p style=\"font-size:1.15rem;\">We&rsquo;re a <a href=\"../about-us.html\">family-run Eastbourne remover</a>, not an educational consultant, so this guide is written from the perspective of forty years of moving families <em>into</em> Eastbourne and listening to what they tell us afterwards about how schools worked out. It&rsquo;s practical rather than exhaustive, and where possible we point you at the school&rsquo;s own admissions information rather than restating it inaccurately.</p>
<p>Eastbourne&rsquo;s school landscape divides into three groups: state primaries (large network, mostly catchment-based), state secondaries (smaller number, several oversubscribed), and the independent sector (one of the strongest in the South East). The right choice depends on the family&rsquo;s priorities and the address you&rsquo;re considering. Below is the rough lay of the land.</p>""",
        'sections': [
            ('The state secondary schools — the big four',
             """<p>Eastbourne&rsquo;s main state secondary schools are Cavendish School, Causeway School, Catmose College, Bishop Bell C of E School, and Willingdon Community School. Each has its own character. Cavendish, in the centre of town, is the largest and one of the most oversubscribed; catchment varies year-on-year but typically covers the central and seafront areas of Eastbourne. Causeway, west of the town, tends to draw from West Eastbourne and Willingdon.</p>
<p>Bishop Bell, the C of E secondary, has a faith-based admissions component. Willingdon serves the northern suburbs and the Hailsham-side villages. Catmose has a strong record but a tight catchment. East Sussex County Council operates the admissions process; the catchment rules use distance plus other criteria including siblings already at the school and looked-after-children priority.</p>
<p>The application deadline is October 31st for the September intake the following year. Out-of-catchment applications are accepted but compete against in-catchment applications, which usually means a place isn&rsquo;t available unless the school is undersubscribed. If a specific secondary school is part of why you&rsquo;re moving, get the address verified inside the catchment <em>before</em> committing to the property.</p>"""),
            ('Independent secondary — Eastbourne College and Bede&rsquo;s',
             """<p>Two of the South East&rsquo;s strongest independent schools sit in Eastbourne: Eastbourne College in the centre of town near the seafront, and Bede&rsquo;s School in Upper Dicker (technically Wealden, a 15-minute drive from Eastbourne). Both are full HMC member schools with strong academic, sporting and creative records.</p>
<p>Eastbourne College is co-educational, day and boarding, around 700 pupils. The campus is unusual for being genuinely embedded in the town — pupils walk along the seafront on the way to and from school. Bede&rsquo;s is day and boarding, around 800 pupils across senior school and the prep, with strong music, sport and theatre programmes. Bede&rsquo;s tends to attract more boarders; Eastbourne College&rsquo;s day-pupil population is larger.</p>
<p>Fees are at the lower end of the HMC range for both schools — typically 20–30% below equivalent London independents. This is consistent with what we hear from London-arriving families weighing the financial picture (the <a href=\"moving-from-london-to-sussex.html\">London-to-Sussex guide</a> covers the wider cost differential). Both schools have entrance tests at 11 (year 7), 13 (year 9) and 16 (year 12).</p>"""),
            ('Primary schools and the early-years picture',
             """<p>Eastbourne has a large network of state primaries — Bourne, Stafford, Stone Cross, Roselands, Ocklynge, Tollgate, Motcombe, Pashley Down, plus several church primaries and the Steiner-style St Andrew&rsquo;s. Catchments are tight; most primaries draw almost entirely from their immediate streets.</p>
<p>The independent prep schools — St Andrew&rsquo;s Prep (linked to Eastbourne College), Wakefield House, Battle Abbey Prep, and the Bede&rsquo;s Prep at Duke&rsquo;s Mews — feed into the corresponding senior schools. If you&rsquo;re planning the independent route from year 7, the prep route is the conventional path.</p>
<p>For early years (nursery and reception), East Sussex County Council&rsquo;s 30-hours free childcare scheme operates from age 3 and many primaries have on-site nurseries. Private nurseries are plentiful in the town. The <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne area guide</a> covers the neighbourhood breakdown for picking the right primary catchment.</p>"""),
            ('Choosing the area — which neighbourhood for which school',
             """<p>For Cavendish School families: central Eastbourne, the seafront, Old Town — most addresses fall within the historical catchment. For Causeway: West Eastbourne (Hampden Park, Roselands border, Willingdon). For Willingdon: the northern suburbs including Willingdon itself and the Polegate/Hailsham-side fringes. For Catmose: the inner residential streets close to the school. For Bishop Bell: faith-based admissions, location less important than the C of E criteria.</p>
<p>For Eastbourne College or Bede&rsquo;s: address is mostly irrelevant — both schools take day pupils from across Eastbourne and the surrounding villages, plus boarders nationwide. Many families pick the neighbourhood for other reasons (Meads for proximity to the College, the inland suburbs for the village-feel) rather than for school catchment.</p>
<p>For families with primary-age children, the catchment is much tighter and the choice of street matters. Bourne and Stafford typically draw from the streets immediately around them. Roselands and Stone Cross primary similarly. Use the school&rsquo;s last-year admissions distance as the rough guide — the council publishes this annually.</p>"""),
            ('Application deadlines and the admissions calendar',
             """<p>The key dates: <strong>15 January</strong> for primary admissions for the September intake the same year. <strong>31 October</strong> for secondary admissions for the September intake the following year. Late applications are accepted but go to the back of the queue for oversubscribed schools. Independent schools have their own deadlines, typically 6–12 months ahead of intake, with entrance assessments in the autumn term before intake.</p>
<p>If your move date is uncertain because of a chain or because the new house isn&rsquo;t yet purchased, you can apply on the basis of the new address as long as you have a verifiable completion date. The council will accept conditional applications and confirm once the move is final. Don&rsquo;t apply on an old address and try to switch later — that almost always loses the priority.</p>
<p>For mid-year transfers (between January and July, or between September and December), apply directly to the schools rather than through the council coordinated process. Mid-year places only open if a current pupil leaves; the most-oversubscribed schools rarely have mid-year places. Plan around the academic-year boundaries where possible. The <a href=\"moving-during-school-holidays.html\">school-holiday moving guide</a> walks through the timing considerations.</p>"""),
            ('A short note on Eastbourne&rsquo;s sixth-form options',
             """<p>For year-12 entry, the main state options are Cavendish&rsquo;s sixth form, the East Sussex College Eastbourne campus (formerly Sussex Downs College), and Catmose College sixth. Independent options include Eastbourne College sixth and Bede&rsquo;s sixth, both with strong academic records and good university destinations.</p>
<p>The College campus offers a much wider vocational and BTEC range than the school sixths — useful for pupils heading into apprenticeships, the creative industries, or specific career paths. The Eastbourne College and Bede&rsquo;s sixths skew strongly toward A-level and university routes, with most leavers going to Russell Group universities.</p>
<p>If your move involves a year-12 transfer, talk to the receiving sixth form directly about subject availability. Some niche A-level combinations (further maths plus three other sciences, for example, or specific language pairings) may only be available at one or two schools in the town. Confirm before move day.</p>"""),
        ],
        'faqs': [
            ("When are the application deadlines?",
             "Primary: 15 January for September intake the same year. Secondary: 31 October for September intake the following year. Independent schools have their own deadlines and entrance assessments typically 6–12 months ahead of intake."),
            ("Can I apply for a school place before completing on the house?",
             "Yes, on a conditional basis — the council accepts applications based on a verifiable completion date. Don't apply on the old address and try to switch later; that usually loses the catchment priority."),
            ("Which is the most oversubscribed state secondary?",
             "Cavendish has historically been the most oversubscribed; Causeway and Willingdon are also competitive in their catchment areas. Bishop Bell uses faith-based criteria so the standard distance rules don't apply in the same way."),
            ("Are the independent schools as expensive as London?",
             "No — Eastbourne College and Bede's fees are typically 20–30% below equivalent London independents. This is one of the consistent draws for London-arriving families."),
            ("What about sixth-form transfers?",
             "Apply directly to the receiving sixth form rather than through the council process. Confirm subject availability for niche A-level combinations before move day — not every school offers every combination."),
        ],
    },

    # ---- Topic 25 ----
    {
        'slug': 'moving-house-in-summer.html',
        'title': 'Moving House in Summer: Tips to Stay Cool and Organised',
        'desc': "Moving during the hot summer months? Here's how to beat the heat, protect your belongings, and stay organised on moving day.",
        'kicker': 'Summer moves · Heat, kit and timing · 40 years on Sussex routes',
        'h1': 'Moving House in Summer — Tips to Stay Cool and Organised',
        'hero_sub': "Summer is the peak removals season and the trickiest weather to plan around. Here is how a Sussex remover handles July and August moves.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Moving in summer',
        'intro_html': """<p style=\"font-size:1.15rem;\">May through September is the peak season for UK house moves and consistently the busiest months on our diary. It&rsquo;s also the trickiest weather to plan around — hot lorries, dehydrated crews, melted candles, fading furniture, and the constant tension between starting early to beat the heat and starting late enough that the customer is actually awake. After forty years of <a href=\"../removals-eastbourne.html\">summer Sussex moves</a> we&rsquo;ve refined the approach. This guide walks through it.</p>
<p>The three big summer-specific considerations: protecting your belongings from heat, keeping the crew (and yourself) safe and hydrated, and timing the move-day schedule around the hottest hours. The detail below covers each in practical terms.</p>""",
        'sections': [
            ('Booking the date — book early or take what is left',
             """<p>Summer slots fill faster than any other time of year. End-of-July and August dates routinely book up 10–14 weeks ahead. Mid-week mid-month August dates are slightly easier but still competitive. If you have a specific summer date in mind — particularly the school-holiday period — get the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> booked at the earliest possible point.</p>
<p>Saturday moves in July and August often need booking 12+ weeks ahead. Sunday moves are sometimes available with shorter notice but at a premium across most of the industry. Mid-week (Tuesday, Wednesday, Thursday) mid-month dates in June or early September are usually 15–20% easier to slot and sometimes cheaper. Worth considering if your completion timing allows flexibility.</p>
<p>If your move is in the school summer holidays (late July through August), confirm that any school transitions are administratively in hand. The <a href=\"moving-during-school-holidays.html\">school-holiday move guide</a> walks through the considerations and the <a href=\"best-schools-eastbourne-families.html\">Eastbourne schools guide</a> covers admissions deadlines.</p>"""),
            ('Protecting belongings from summer heat',
             """<p>Several categories of household possession suffer in summer transit. Candles melt and stain everything around them — pack candles separately, ideally in cool boxes with ice packs if the move is more than a couple of hours&rsquo; drive. Wax records and vinyl warp in heat — pack vertically, never flat, away from direct sun in the lorry.</p>
<p>Electronics with lithium-ion batteries (laptops, power tools, e-bikes) can degrade in extended summer heat. For long-distance summer moves, remove the batteries and pack them separately, ideally in your own car. Photographs, paintings and framed art are at higher risk in summer because heat plus humidity accelerates fading and adhesive failure; our <a href=\"how-to-pack-fragile-items.html\">fragile-packing guide</a> covers the materials and methods.</p>
<p>Anything edible (chocolate, oils, wine) needs particular care. Wine and spirits prefer cool, dark, low-vibration transit; if you have a serious wine collection consider professional wine-relocation specialists rather than standard removal. Olive oil and other liquid foods can leak in heat — wrap bottle lids in electrical tape, line cartons with bin liners. For all these issues talk to us at survey and we&rsquo;ll work the cool-box logistics into the plan.</p>"""),
            ('Crew, hydration and the early-start strategy',
             """<p>The single best move-day-summer strategy is the early start. Our summer crews typically leave the depot at 6am to be on the property by 7am. Loading from 7am to 11am beats the worst of the midday heat; the lorry is moving (and therefore the load is in motion-cooled air) by lunchtime; the unload happens between 1pm and 5pm at the new property.</p>
<p>Hydration is genuinely critical. Removal crews work hard physically and in summer the calorie and water requirements are higher than people realise. We carry chilled water on every summer job and our crews take 10-minute breaks every 90 minutes. If you&rsquo;d like to support the crew, leaving a kettle, mugs, biscuits and ice for cold water available throughout the load is a small kindness that pays back in pace.</p>
<p>For you and the family, the same applies. Hat, sunscreen, water bottle. The work of supervising a move and walking between two properties on a hot day is more tiring than people expect. Take regular short rests, ideally indoors with the curtains closed against the sun. The <a href=\"moving-day-survival-kit.html\">moving-day survival kit guide</a> covers the essentials.</p>"""),
            ('Garden contents and plants in the heat',
             """<p>Summer is the hardest season for transporting plants. Houseplants survive 4–8 hours in a closed lorry on a hot day but anything longer than that risks heat damage, particularly for the more delicate varieties. For long-distance summer moves, plants typically travel with you in the car with the windows cracked.</p>
<p>Garden plants in pots — bay trees, olive trees, large potted shrubs — are heavy and bulky in lorries and need extra protection. We pad-wrap them like furniture using our <a href=\"full-pad-wrap-protection-explained.html\">pad-wrap method</a> and stand them upright. Watered plants are heavy and more likely to leak; water deeply 24 hours before move day, then don&rsquo;t water on the day itself.</p>
<p>For items in the garden shed — bags of compost, fertilisers, weedkillers, BBQ accessories — most of these are fine in summer lorry transit but the chemical category needs care. Don&rsquo;t pack anything with the warning &ldquo;keep away from direct sunlight&rdquo; in a lorry that will sit in 30-degree heat. Talk to us at survey about anything questionable.</p>"""),
            ('Hot lorry days — what the crew watches for',
             """<p>On the lorry itself we manage heat through a few standard practices. Loading order: lightest and most heat-sensitive items go in last (top of the load), heaviest and least heat-sensitive items go in first (bottom). This keeps the most-vulnerable items in the cooler part of the lorry near the door and accessible if a stop is needed.</p>
<p>For long-distance summer moves we plan rest stops that allow the lorry door to be opened in shade, refreshing the internal air. For overnight stays (where storage between completion dates is needed), the load goes into our climate-stable <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> overnight rather than sitting in a lorry on a depot yard.</p>
<p>Particularly for international moves in summer (see <a href=\"../international-removals-eastbourne.html\">international removals</a>), the customs holding period at the depot is climate-controlled. Containerised shipments are ventilated. The whole logistic chain accounts for heat as a variable in a way that the customer rarely sees but which makes a real difference to what arrives intact.</p>"""),
            ('The first 48 hours in the new house — summer specifics',
             """<p>At the new property, the first job after the crew leaves is to get cool air moving through the house. Open the windows top and bottom; if the new property has air conditioning, set it to a moderate cooling cycle (not blast cold — that&rsquo;s wasteful and uncomfortable). Many of the boxes have been in a hot lorry for hours; airing the house also airs the cartons before you start unpacking.</p>
<p>Unpack the bedroom first (so beds are made up before bedtime in the heat), then the kitchen (so cold drinks are accessible), then the bathroom. The same order works in summer as it does any season — see the <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a> — but the urgency around the kitchen is higher in summer because of dehydration risk.</p>
<p>If you&rsquo;ve moved in extreme heat (over 30 degrees C), check sensitive contents within 24 hours of unloading rather than weeks. Wine in particular can suffer subtle damage that&rsquo;s only obvious at first opening. Photographs and paintings should be inspected within a week of move day. Any concerns, contact us — standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers transit damage including heat-related issues on professionally-packed contents.</p>"""),
        ],
        'faqs': [
            ("How early should we book a summer move?",
             "10–14 weeks ahead for the May–September peak, particularly Saturday dates and the school-holiday period (late July through August). Mid-week mid-month dates in June or early September are easier to slot."),
            ("Will the lorry get too hot for our belongings?",
             "Standard household contents are fine in normal summer transit. The categories that need extra care are candles, vinyl records, photographs, wine, electronics with lithium-ion batteries and any chemicals labelled to avoid heat. We work cool boxes into the plan at survey."),
            ("Can the crew work in a 30-degree heatwave?",
             "Yes, with early starts (6am depot, 7am at property) and frequent breaks. We carry chilled water and take 10-minute rests every 90 minutes. The unload finishes by mid-afternoon to avoid the hottest hours."),
            ("Should plants travel in the lorry?",
             "Houseplants for short moves, yes. For long-distance summer moves, plants travel with you in the car with the windows cracked. Large potted garden plants — bay trees, olives — go pad-wrapped upright in the lorry."),
            ("Do you offer cooling during transit?",
             "The lorries are insulated and ventilated, not air-conditioned in the load space. For genuinely temperature-sensitive contents (wine collections, fine art) we recommend specialist climate-controlled transport on top of our standard service."),
        ],
    },

    # ---- Topic 26 ----
    {
        'slug': 'how-our-pad-wrap-service-protects-furniture.html',
        'title': 'How Our Full Pad-Wrap Service Protects Your Furniture',
        'desc': 'Learn exactly how our professional full pad-wrap service works and why it\'s the safest way to move your furniture.',
        'kicker': 'Our signature method · Pad-wrap as standard on every full removal',
        'h1': 'How Our Full Pad-Wrap Service Protects Your Furniture',
        'hero_sub': "The materials, the method, the why. The single biggest reason for our damage-free record across forty years of Sussex removals.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Pad-wrap service',
        'intro_html': """<p style=\"font-size:1.15rem;\">Pad-wrap is the single most important thing we do. It&rsquo;s the reason our customers come back, the reason their grandmothers&rsquo; dressers arrive on the other end of an international move without a single scratch, and the reason we still get telephone enquiries from neighbours who watched us pad-wrap a friend&rsquo;s furniture three doors down. This guide explains exactly what the service is, what it costs, and why it works.</p>
<p>The principle is simple: every freestanding piece of furniture is individually wrapped in heavy quilted blankets <em>in your home</em>, then only unwrapped once it&rsquo;s in its final position at the new property. The wrapped piece never touches another wrapped piece without padding between them. The detail below explains each part of the method.</p>""",
        'sections': [
            ('What pad-wrap actually means',
             """<p>Pad-wrap is the use of industry-weight quilted moving blankets to individually wrap freestanding furniture so it&rsquo;s protected from chips, scratches, dents and pressure marks during a move. The blankets are heavy — much heavier than household throws — and stitched with closed seams so the filling doesn&rsquo;t shift. They&rsquo;re tied in place using webbing straps rather than tape, so nothing adhesive touches the furniture finish.</p>
<p>A typical 3-bedroom house contains 40&ndash;80 pieces of pad-wrappable furniture: beds, wardrobes, chests of drawers, sideboards, dining tables, coffee tables, sofas, armchairs, dressers, bookcases, desk units. Each is wrapped individually, before it&rsquo;s loaded, in your home. The wrapping doesn&rsquo;t come off until the piece is in its final room and position at the new property.</p>
<p>This is the version every BAR-registered remover should be doing. In practice the industry varies — some firms use thin throws or hardware-store blankets, some wrap in the lorry rather than the room, some don&rsquo;t pad-wrap at all and rely on shrink-wrap or bubble wrap (which provides no real cushioning). The differences are real and measurable in damage rates. See our <a href=\"full-pad-wrap-protection-explained.html\">full pad-wrap protection explained</a> guide for the wider context.</p>"""),
            ('The three-step process in detail',
             """<p><strong>Step 1 — Wrap in your home.</strong> Every piece of furniture is pad-wrapped where it stands. Drawer fronts are taped (with non-residue tape so finishes aren&rsquo;t damaged), corners protected with corner-board where needed, fragile detail covered, hardware (handles, latches) padded. The blanket goes on, the webbing strap holds it in place, and the piece is ready to move. Average time per piece: 3&ndash;5 minutes.</p>
<p><strong>Step 2 — Load stack-safe.</strong> Wrapped pieces go straight to the lorry and are loaded in a sequence that protects them from each other. Heaviest at the bottom, lightest on top. Wrapped corners face wrapped corners — pad-on-pad, never pad-on-glass-or-veneer. Strapped to the bulkhead and the lorry walls so nothing shifts in transit. For longer moves, the lorry is configured with internal mooring points specifically for this. Pieces never get unwrapped in transit.</p>
<p><strong>Step 3 — Unwrap in final position.</strong> At the new property, the wrapped piece is carried in (still wrapped, including up stairs and through doorways), placed in the room you&rsquo;ve chosen, in the exact position you choose. Only then does the wrapping come off. The result: pieces arrive in the new property looking identical to how they left the old property.</p>"""),
            ('Why most removers skip this step',
             """<p>Pad-wrap is more expensive for the remover than the alternatives. Industry-weight blankets cost meaningfully more than thin throws or single-use bubble wrap. They need to be laundered between every job — we have an in-house laundry system at our <a href=\"../about-us.html\">Lower Dicker depot</a> for this. And the wrapping itself takes crew time — 3&ndash;5 minutes per piece × 50 pieces = roughly 3 hours added to the load day.</p>
<p>So a budget remover saves money on three fronts by not pad-wrapping: lower materials cost, no laundry overhead, faster load times. The customer sometimes gets a slightly cheaper quote. The downside is what arrives at the other end — chips, scratches, pressure dents — and an awkward conversation about whether the customer&rsquo;s home contents insurance covers the damage.</p>
<p>For most professionally-run removers, pad-wrap is included on every full removal as standard, not an extra. We&rsquo;ve included it on every quote since 1982. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers what to confirm with any remover before booking — pad-wrap is at the top of the list.</p>"""),
            ('What gets pad-wrapped (and what doesn&rsquo;t)',
             """<p>Every piece of freestanding furniture larger than a side table gets pad-wrapped. That includes obvious targets — wardrobes, beds, chests of drawers, sideboards, sofas, armchairs, dining tables — and less obvious ones like the bedside table, the small writing desk, the hall console, the children&rsquo;s nightstands. If it has finished edges, it gets wrapped.</p>
<p>What doesn&rsquo;t get pad-wrapped: packed cartons (those have their own protection internally — see our <a href=\"how-to-pack-fragile-items.html\">fragile-packing guide</a>), small items like lamps and small decorative objects (these are packed in cartons), mattresses (these get specific plastic mattress covers, not pad-wrap), and white goods (these have their own packaging or shipping protectors).</p>
<p>Special-care items — antiques, art, marble or stone, glass-fronted display cabinets, pianos — get pad-wrap plus additional protection. For these we&rsquo;d typically also use corner-board for the building (so the piece doesn&rsquo;t mark doorways or walls in transit) and custom crating where the piece is genuinely irreplaceable. The <a href=\"moving-antiques-valuable-furniture.html\">antiques-moving guide</a> covers this in more detail and the <a href=\"../white-glove-service.html\">white-glove service</a> is the relevant tier for very high-value contents.</p>"""),
            ('The difference it makes &mdash; measurable',
             """<p>Internal records aren&rsquo;t scientific surveys but they&rsquo;re telling. Across the moves we&rsquo;ve done since 1982, the damage rate on pad-wrapped contents is roughly an order of magnitude lower than the damage rate on contents we&rsquo;ve seen at the unload end from non-pad-wrapped removers (where we&rsquo;ve been the second-mover on a customer reclaiming from a budget operator&rsquo;s storage).</p>
<p>The categories where the difference shows: chips on furniture corners (almost zero on pad-wrapped jobs vs commonplace on shrink-wrapped jobs), pressure dents on upholstery (rare on pad-wrap, occasional on cling-film), scratches on veneer and lacquered finishes (extremely rare on pad-wrap, fairly common otherwise). Glass cracks and breakages depend more on the loading sequence than the wrap, but pad-wrap helps because the wrapped glass piece is protected from neighbours during transit.</p>
<p>The insurance picture follows the same pattern. Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers transit damage on professionally-wrapped pieces. Claims rates are correspondingly lower across professionally-wrapped moves. The differential isn&rsquo;t marketing; it&rsquo;s measurable in the data.</p>"""),
            ('What customers can do to help &mdash; and what we always include',
             """<p>The customer&rsquo;s role in a pad-wrapped move is mostly to stay out of the way. The crew works faster when they have clear access to each room and a chair to put the wrapping on while it&rsquo;s being applied. Move smaller items (lamps, decorative objects) out of the room before the crew arrives so the path to the furniture is unobstructed.</p>
<p>What we always include on every full removal at no extra cost: pad-wrap protection (as described above), removal-grade cartons sized correctly, a written and itemised quote, and BAR-protected deposit handling under the Advance Payment Guarantee. None of this is an add-on or premium tier. It&rsquo;s the standard service.</p>
<p>What costs extra: packing (full pack £450&ndash;£800 on a 3-bed, fragile-only £220&ndash;&pound;340), specialist handling (piano, antiques, marble), storage between completion dates, international/overseas customs handling. All quoted as separate line items so you see what each costs. Book the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">free survey</a> to get the itemised quote.</p>"""),
        ],
        'faqs': [
            ("Is pad-wrap an extra cost?",
             "No. Pad-wrap is included on every full removal we quote — it's standard, not premium. The crew time and the blanket materials are all part of the headline price."),
            ("How long does pad-wrapping a 3-bed take?",
             "Around 90 minutes for our standard 3-crew team. We start wrapping as soon as we arrive and continue through the morning while another crew member loads the lorry."),
            ("Can I supply my own blankets?",
             "You can but we'd strongly recommend our own. Industry-weight blankets are heavier and stitched to take the weight of a fully-loaded lorry. Hardware-store blankets often aren't, and a thin blanket failing in transit defeats the whole point."),
            ("Do you pad-wrap on international moves too?",
             "Yes. The same method applies for FIDI-network international shipments — every piece pad-wrapped before it goes into the customs-controlled holding bay at our depot, sealed inside the container."),
            ("What if I see a scratch at the unload end?",
             "Flag it before the crew leaves so we can photograph it and start the claim under our goods-in-transit insurance. Standard cover handles transit damage on professionally-wrapped contents."),
        ],
    },

    # ---- Topic 27 ----
    {
        'slug': 'what-happens-on-moving-day.html',
        'title': 'What Happens on Moving Day – A Step-by-Step Guide',
        'desc': 'Curious about moving day? We walk you through exactly what happens from the moment our team arrives until everything is in your new home.',
        'kicker': 'Move-day walkthrough · What to expect, hour by hour',
        'h1': 'What Happens on Moving Day — A Step-by-Step Guide',
        'hero_sub': "From the crew arriving on your driveway to the lorry pulling away from the new house, here is the entire day broken down into the calls and the milestones.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Moving day step by step',
        'intro_html': """<p style=\"font-size:1.15rem;\">Most of our customers have only ever done one or two house moves in their adult lives. Each time, the entire day is unfamiliar — what time does the lorry arrive, how long does loading take, when do we hand keys over, where do we sit during the load, what happens if the chain slips. This guide walks through the entire day from the moment the crew turns onto your driveway to the moment the lorry pulls away from the new house.</p>
<p>The structure follows a typical single-day single-crew move — the most common pattern we run. Multi-day or two-crew moves follow the same logic with extended timings. If you have a specific timing question about your own upcoming move, talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we&rsquo;ll plot the actual hour-by-hour schedule.</p>""",
        'sections': [
            ('07:30 — the crew arrives',
             """<p>Standard move-day start is 8am at the property. The crew leaves our <a href=\"../about-us.html\">Lower Dicker depot</a> at 7am to be on your driveway 10 minutes before the stated start time. They&rsquo;ll knock at 7:50–7:55, introduce themselves by name, and walk through with you to confirm the inventory and access plan.</p>
<p>What to have ready: a clear path through every room (small items packed, breakables packed, larger items in their final positions), a kettle and mugs available, and the keys to anything they&rsquo;ll need access to. The crew lead will ask whether anything is fragile or particularly valuable, and which items go in the lorry first vs. last (often the &lsquo;first-night carton&rsquo; — see <a href=\"what-to-pack-first-when-moving-house.html\">what-to-pack-first guide</a> — is loaded last so it comes off first).</p>
<p>The walkthrough takes 10–15 minutes. By 8:10 the crew is back at the lorry collecting their kit (blankets, straps, dollies, corner-board) and bringing it into the property. From 8:15 the pad-wrapping starts in the room with the most furniture — usually the master bedroom or the living room.</p>"""),
            ('08:00 to 12:00 — pad-wrap and load',
             """<p>Pad-wrapping happens in your home before any piece leaves the room. The crew works through one room at a time, wrapping the freestanding furniture in heavy quilted blankets and webbing straps. The wrapped pieces are carried out, into the lorry, and loaded in a stack-safe sequence. Cartons follow in a planned order — heavy at the bottom, fragile near the top. See <a href=\"how-our-pad-wrap-service-protects-furniture.html\">how our pad-wrap service works</a> for the detail.</p>
<p>The customer&rsquo;s job during loading is to stay out of the way and answer questions when asked. The biggest mistake customers make on move-day is trying to direct the loading sequence — the crew knows what they&rsquo;re doing, and well-meaning supervision typically slows things down by 20–30%. Make tea, photograph the empty rooms as they finish, take the dog for a walk.</p>
<p>For a 3-bedroom house the loading typically completes by 11:30–12:30. Larger 4–5 bed properties run to 1–2pm. The lorry is fully strapped down and ready to roll once loading completes; the final sweep with the customer takes 10–15 minutes. By the time you&rsquo;re ready to lock the front door for the last time, the lorry is engine-running on the driveway.</p>"""),
            ('12:00 — keys, completion and the transition',
             """<p>The chain-day completion timing shapes everything from this point. Most UK sales complete at noon or 1pm — meaning your solicitor confirms funds transferred, and the estate agent releases the keys to the buyer. The same happens in reverse at the new property — your solicitor confirms funds out, the seller&rsquo;s agent releases keys to you. The whole sequence usually plays out between 11am and 1pm.</p>
<p>If the chain runs to time, the lorry leaves your old property at 12:30, you follow in your own car, and we&rsquo;re both at the new property by 1pm. If the chain slips — which happens, often by 30–90 minutes — the lorry sits on the road outside your old property while everyone waits for the funds to release. We don&rsquo;t charge for these waits; they&rsquo;re built into the day&rsquo;s schedule.</p>
<p>For longer chain slips (over 3 hours) we&rsquo;ll move the lorry to a holding spot rather than block your old neighbours&rsquo; road. For overnight chain failures (rare but it does happen), the load goes into our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> overnight and we redeliver the next day. There&rsquo;s no extra charge for the overnight; the inconvenience is enough.</p>"""),
            ('13:00 — arrival at the new property',
             """<p>The lorry arrives at the new property 10 minutes before you do (we leave ahead so we&rsquo;re there ready). The crew walks the new property with you to confirm the room layout, where each piece of furniture goes, and any access constraints (lift bookings, narrow doorways, stairs). This takes 5–10 minutes and matters because once the unloading starts, mistakes are slow to undo.</p>
<p>For new-build properties, the crew will check whether any doorways are too narrow for the wrapped furniture — sometimes furniture that fitted into the old property doesn&rsquo;t fit into the new. We&rsquo;ve usually spotted this at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> but occasionally a piece needs additional disassembly on the day. Talk to the crew lead about anything questionable.</p>
<p>Unloading then runs in reverse to loading. Lightest items off first (the boxes from the top of the load); furniture in the middle of the sequence; heaviest base-load items off last. Each piece of pad-wrapped furniture is carried in still wrapped, placed in its final position in the room, and unwrapped there. By 3–4pm the lorry is empty and the crew is doing the end-of-day sweep with you.</p>"""),
            ('16:00 — end-of-day sweep and inventory check',
             """<p>The end-of-day sweep is the last formal phase of the move. The crew lead walks through the new property with you, checking every room against the inventory list, confirming each piece is in the right room and in the right position. Any concerns — a scratch you spotted, a piece in the wrong room — get noted on the sheet and resolved before the crew leaves.</p>
<p>This is the moment to flag anything that doesn&rsquo;t look right. Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers transit damage but claims work much better when they&rsquo;re flagged on the day rather than discovered a week later. The crew will photograph anything questionable and we&rsquo;ll start the process right then.</p>
<p>If you&rsquo;ve booked the <a href=\"../unpacking-service.html\">unpacking service</a>, the crew stays for an additional 2–4 hours to unpack the cartons and remove the empty boxes. Otherwise they leave you with the cartons in place; we come back later in the week (free of charge if you&rsquo;re within range) to collect empty boxes once you&rsquo;ve unpacked.</p>"""),
            ('17:00 onwards — the first evening at the new house',
             """<p>Once the crew leaves, the property is yours. Whatever organisational state you&rsquo;ve left it in — total chaos or surprisingly orderly — the priority for the first evening is the same: working kitchen, made bed, functioning bathroom. The <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a> covers the &lsquo;first-night carton&rsquo; concept; if you packed one, this is where it pays off.</p>
<p>Take meter readings (gas, electric, water) and photograph them. Walk the perimeter to check security — windows closed, doors locked, alarm code working if there&rsquo;s an alarm. If the previous owners left any keys (often a spare set in a kitchen drawer), gather them. Put a forwarding-address note on the inside of the front door for any post that arrives in the first week.</p>
<p>And then — most importantly — sit down. Make a cup of tea. Order a takeaway. The move is done. The unpacking can wait until morning. The <a href=\"moving-day-survival-kit.html\">survival kit guide</a> covers what to have on hand to make the first night calm rather than chaotic.</p>"""),
        ],
        'faqs': [
            ("What time does the crew arrive?",
             "Standard start is 8am, with the crew on your driveway by 7:50. The lorry leaves Lower Dicker at 7am to be at your property in time."),
            ("How long does the load take?",
             "A typical 3-bed home loads in 4–4.5 hours including pad-wrapping. Larger 4–5 bed properties run 5–7 hours. Smaller moves (1–2 bed) often complete in 2–3 hours."),
            ("What happens if the chain slips on completion day?",
             "We wait. There's no extra charge for chain delays up to several hours. For longer slips (3+ hours) we move the lorry to a holding spot; for overnight failures, the load goes into our climate-stable depot and we redeliver the next day."),
            ("Should I direct the loading?",
             "No — let the crew lead the sequence. They know what's going in first vs. last and how to stack pieces stack-safe. The biggest move-day mistake customers make is over-supervising the load."),
            ("What if I find damage at the unload?",
             "Flag it before the crew leaves so we can photograph it and start the goods-in-transit insurance claim immediately. Day-of claims process much faster than week-later ones."),
        ],
    },

    # ---- Topic 28 ----
    {
        'slug': 'questions-to-ask-removals-company.html',
        'title': '7 Questions You Must Ask Before Hiring a Removals Company',
        'desc': 'Protect yourself and your belongings. These are the essential questions every customer should ask before booking a removals company.',
        'kicker': 'Choosing a remover · 7 questions, 0 sales talk',
        'h1': '7 Questions You Must Ask Before Hiring a Removals Company',
        'hero_sub': "Most customers ask about price. The questions that actually predict the move quality are different. Here are the seven we wish every customer asked.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': '7 questions to ask',
        'intro_html': """<p style=\"font-size:1.15rem;\">If you ask any removals company &ldquo;how much&rdquo; they&rsquo;ll give you a number. The number is the easy bit. The harder bit — and the bit that actually determines whether your move goes well — is the seven questions below. We&rsquo;d ask these of every quote we received, including our own, before booking a Sussex removals firm.</p>
<p>This isn&rsquo;t a sales pitch (or if it is, it&rsquo;s a transparent one). The questions are the ones the industry generally doesn&rsquo;t want customers to ask because the answers vary so much. The <a href=\"choosing-a-removal-company-eastbourne.html\">choosing-a-removal-company guide</a> has a longer version of this with more detail; this one is the &lsquo;phone in hand&rsquo; short list.</p>""",
        'sections': [
            ('1. Are you a member of the British Association of Removers?',
             """<p>The British Association of Removers (BAR) is the industry trade body in the UK. Member firms are audited annually, sign up to a code of practice, and operate under the BAR Advance Payment Guarantee — which protects customer deposits if the worst happens to the firm during the contract. Non-member firms have none of these protections.</p>
<p>Membership isn&rsquo;t a guarantee of quality but it&rsquo;s a meaningful filter. The audit cost and the conduct standards keep out the lower end of the market. Most reputable Sussex removers are BAR members; the ones who aren&rsquo;t usually have a reason they don&rsquo;t want to be.</p>
<p>How to verify: the BAR website lists current members by postcode. Don&rsquo;t take the remover&rsquo;s word for it — go to bar.co.uk and search. Confirm the membership number matches. Our <a href=\"../about-us.html\">company history page</a> includes our BAR details and audit dates.</p>"""),
            ('2. What insurance do you carry, and what does it cover?',
             """<p>Three insurance categories matter for a remover: goods-in-transit insurance (covers your belongings during the move), public liability insurance (covers if the crew damages your property), and yard insurance (covers your belongings while in their depot or storage). All three should be at meaningful limits.</p>
<p>Ask specifically: <em>what&rsquo;s the per-item limit on goods-in-transit?</em> Single items over £2,500 need declaring separately on most policies. <em>What&rsquo;s the total cover for the move?</em> A typical 3-bed home is around £100,000 of contents at replacement value; if the per-move limit is £25,000, you&rsquo;re underinsured. <em>What&rsquo;s excluded?</em> Self-packed cartons, cash, jewellery, irreplaceable documents are common exclusions.</p>
<p>Get the answer in writing before booking. Our <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance details</a> page covers the full picture for our cover. Other reputable firms will have similar documentation; an unwillingness to share it is itself an answer.</p>"""),
            ('3. Are your crew directly employed or sub-contracted?',
             """<p>This question separates the professional firms from the broker model. Directly employed crew are on the firm&rsquo;s payroll, trained by the firm, accountable to the firm, and consistent move-to-move. Sub-contracted crew are agency labour or day workers, varying by job, trained by whoever happened to be there last week.</p>
<p>The damage rate, the timekeeping, the customer-service experience and the actual furniture-handling competence all correlate strongly with the directly-employed model. National lead-generation sites that sub-let work to whichever local firm has capacity that day operate the broker model by definition; whether your specific move is with their employed crew or a sub-contracted one is impossible to predict.</p>
<p>Ask directly: <em>will the people I&rsquo;ll meet at the survey be the same people who move me?</em> For a directly-employed firm, the answer is yes. For a broker, the answer is some version of &ldquo;it depends on the day&rdquo;. The <a href=\"how-to-spot-rogue-removal-traders.html\">rogue-trader guide</a> covers the broker model in more depth.</p>"""),
            ('4. Do you pad-wrap furniture, and how?',
             """<p>Pad-wrap is the industry-best method for protecting furniture in transit (see <a href=\"how-our-pad-wrap-service-protects-furniture.html\">how our pad-wrap service works</a>). Not every remover does it; many use cheaper alternatives like shrink-wrap (cling film), thin throws, or no protection at all.</p>
<p>Ask specifically: <em>do you wrap before the piece leaves the room?</em> Wrapping in the lorry doesn&rsquo;t protect the piece during the carry-out, which is where most damage happens. <em>What materials do you use?</em> Industry-weight quilted blankets, washed between jobs, are the standard. Hardware-store blankets and supermarket throws aren&rsquo;t. <em>Is it included or extra?</em> For a professional firm it&rsquo;s standard on every full removal.</p>
<p>A useful follow-up: ask to see a blanket from their van. A firm that does pad-wrap as standard has clean, heavy, professionally-laundered blankets and is happy to demonstrate. A firm that doesn&rsquo;t will have a few thin throws used as makeweights, or none at all. The blanket in the van tells you more than the brochure on the kitchen table.</p>"""),
            ('5. Is the quote fixed or estimated?',
             """<p>Most reputable removers issue fixed-price written quotes after an in-home or video survey. The price doesn&rsquo;t move on the day unless the customer adds work that wasn&rsquo;t in the original scope (&ldquo;can you also move the loft contents?&rdquo; — that gets quoted on the spot). Estimated quotes — &ldquo;it&rsquo;ll be around X&rdquo; — are red flags.</p>
<p>Ask specifically: <em>is this a quote or an estimate?</em> The legal definitions differ. A quote is binding; an estimate is not. <em>What triggers a price change?</em> Legitimate triggers (significant extra work added) vs. illegitimate ones (the crew finds the lorry needs longer than expected because the surveyor underestimated). <em>Is the quote itemised?</em> You should see line items for crew, lorry, fuel, pad-wrap, materials, insurance, any specialist handling.</p>
<p>For full transparency on our pricing approach, the <a href=\"cost-of-moving-house-sussex-2026.html\">2026 cost of moving guide</a> walks through what each line costs. The <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey form</a> generates a written, itemised, fixed-price quote within 48 hours.</p>"""),
            ('6. What is the deposit structure and is it protected?',
             """<p>Most reputable removers take a 20&ndash;25% deposit on booking, with the balance payable on the day of completion. The deposit should be protected under the BAR Advance Payment Guarantee — meaning if the firm fails between booking and move day, the deposit is refunded by the BAR scheme. Non-BAR firms don&rsquo;t have this protection, and the deposit is at risk.</p>
<p>Ask: <em>what percentage deposit do you require, and when is the balance due?</em> 20&ndash;25% on booking, balance on completion day is the standard. Anything higher than 50% upfront is unusual. <em>Is the deposit refundable if I cancel?</em> Most contracts have a sliding cancellation scale based on how far ahead of the move date. <em>Is the deposit BAR APG-protected?</em> For BAR firms, yes; otherwise no.</p>
<p>Confirm the protection in writing. The APG certificate number should be on the contract or available on request. The <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance page</a> has the full deposit structure for our cover.</p>"""),
            ('7. Can you give me references from recent customers?',
             """<p>Independent reviews tell you more than the firm&rsquo;s own marketing. Google Reviews, Trustpilot and Which? are the major UK platforms. Look for the volume (a firm with 5 reviews tells you little; 100+ is meaningful), the recency (last 12 months should be plentiful), and the response pattern from the firm itself (do they respond to bad reviews professionally, or ignore them).</p>
<p>Better: ask for a customer reference from a recent move. Most reputable firms have customers willing to do a brief reference call. The conversation is far more revealing than the written review — a 10-minute phone call with someone who moved 2 months ago tells you exactly what to expect.</p>
<p>For our own moves, the <a href=\"../reviews.html\">reviews page</a> has the full Google and Trustpilot record. We&rsquo;ll also share customer references on request — particularly useful for unusual moves (international, large country properties, business moves). Talk to us at the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> and we&rsquo;ll put you in touch with a recent customer with a similar profile.</p>"""),
        ],
        'faqs': [
            ("How important is BAR membership really?",
             "Important. It's not a guarantee of quality but it's a meaningful filter — audited annually, code of practice, APG deposit protection. Most reputable Sussex firms are members; the ones who aren't usually have a reason."),
            ("What's the difference between a quote and an estimate?",
             "A quote is a binding price; an estimate is a guess. Insist on a fixed-price quote in writing after an in-home or video survey. 'Around £X' over the phone is not a quote."),
            ("How can I check if a firm is BAR-registered?",
             "The BAR website at bar.co.uk lists current members. Don't take the remover's word for it — search and confirm the membership number matches."),
            ("Is sub-contracted crew always a bad sign?",
             "Usually yes for predictability. Directly-employed crews are trained and accountable; sub-contracted day labour varies wildly job-to-job. Ask the question directly at survey."),
            ("What deposit is normal?",
             "20–25% on booking, balance on completion day. Anything higher than 50% upfront is unusual. The deposit should be BAR APG-protected for BAR firms."),
        ],
    },

    # ---- Topic 29 ----
    {
        'slug': 'how-to-spot-rogue-removal-traders.html',
        'title': 'How to Spot Rogue Traders and Avoid Moving Scams',
        'desc': 'Don\'t fall victim to rogue traders. Learn the warning signs and how to choose a legitimate, trustworthy removals company.',
        'kicker': 'Spotting the rogues · A 40-year-old removal firm\'s honest take',
        'h1': 'How to Spot Rogue Traders and Avoid Moving Scams',
        'hero_sub': "The warning signs the industry would rather not advertise. From upfront-cash demands to lorries-in-lay-bys, here is what tells a rogue from a real remover.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Avoiding rogue removers',
        'intro_html': """<p style=\"font-size:1.15rem;\">The UK removals industry has a long tail of operators ranging from genuinely professional firms (BAR members, directly-employed crews, proper insurance) to opportunists running a single van out of a lay-by. The middle ground is the dangerous zone — firms that look professional online, take your deposit, and disappear or deliver dramatically below the implied promise. This guide explains how to tell the difference.</p>
<p>This is written by a 40-year-old <a href=\"../about-us.html\">BAR-registered family Sussex remover</a>, so the bias is obvious. The warning signs below come from the industry forums, the BAR enforcement records, and the post-move conversations we&rsquo;ve had with customers who reclaimed contents from rogue operators. The signals are real.</p>""",
        'sections': [
            ('Warning sign one — the upfront cash demand',
             """<p>Legitimate removers take a 20&ndash;25% deposit on booking (BAR APG-protected) and the balance on the day of completion. Card or bank transfer is standard. Cash for amounts over £500 is unusual; cash for the full move price is a major red flag.</p>
<p>The rogue pattern: &ldquo;we need 100% cash up front, and you&rsquo;ll get a £200 discount for paying in cash&rdquo;. This combines two scam mechanisms — the discount is a bait, the cash is untraceable. Once paid, the firm either delivers a much-degraded move (no pad-wrap, untrained crew, damage on arrival) or vanishes entirely.</p>
<p>The fix: insist on card or bank transfer with a deposit-and-balance structure. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers the deposit-structure question in detail; the <a href=\"../terms-conditions-and-insurance-details.html\">terms page</a> shows what a normal deposit arrangement looks like.</p>"""),
            ('Warning sign two — quote-by-phone for a large move',
             """<p>A quote-by-phone is fine for genuinely small jobs (single room, studio flat, baggage shipment). For anything 2-bedroom and above, the survey is the only way to give an accurate price. A firm offering a binding price for a 3-bed home over the phone is either (a) inexperienced and likely to add charges on the day, or (b) deliberately underquoting to lock the job in.</p>
<p>The rogue pattern: &ldquo;sure, &pound;400 for the whole move, no need for a survey, send your sort code&rdquo;. On the day, the lorry shows up undersized, the crew is two people not four, and the customer is offered &ldquo;upgrade options&rdquo; mid-load at hugely inflated rates.</p>
<p>The fix: insist on an in-home survey or video survey. Most reputable firms offer both. The survey is free and produces a written, itemised, fixed-price quote within 48 hours. Our <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey form</a> takes ten minutes.</p>"""),
            ('Warning sign three — no business address or just a mobile number',
             """<p>Legitimate removers have a registered business address (visible at Companies House), a landline phone number (visible on the website), and a depot or yard that you could visit if needed. Rogue operators often run from a mobile phone, a PO box, or an address that&rsquo;s a virtual mailbox.</p>
<p>The signal isn&rsquo;t the mobile number itself (most professional firms have mobile contact too) — it&rsquo;s the absence of a permanent address. Search the firm name at Companies House; if no record exists, it&rsquo;s unincorporated (which isn&rsquo;t illegal but limits your legal recourse). Search the address on Google Street View; if it&rsquo;s a residential property or doesn&rsquo;t exist, that&rsquo;s a red flag.</p>
<p>The fix: verify the registered address and visit the depot if it&rsquo;s practical. Reputable firms welcome depot visits (we&rsquo;d be happy to show you the <a href=\"../about-us.html\">Lower Dicker site</a>). A firm refusing or unable to host a visit has a reason.</p>"""),
            ('Warning sign four — no BAR membership, no proper insurance',
             """<p>Non-BAR firms aren&rsquo;t always rogues (some legitimate small operators choose not to pay the membership fee) but the BAR membership filter catches most of the bad actors. The Advance Payment Guarantee in particular is something no rogue would sign up to — it requires audited financials.</p>
<p>The same applies to insurance. A legitimate remover carries goods-in-transit insurance (often £25,000&ndash;&pound;100,000 per move), public liability (typically £2M+), and yard insurance. Ask to see the certificate. A firm unable or unwilling to produce insurance documentation isn&rsquo;t insured, and your contents aren&rsquo;t covered.</p>
<p>The fix: verify BAR membership at bar.co.uk, request insurance certificates in writing. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers this in detail. Our <a href=\"../terms-conditions-and-insurance-details.html\">terms page</a> shows the documents we&rsquo;d expect any reputable remover to share.</p>"""),
            ('Warning sign five — vague crew, vague vehicles, vague depot',
             """<p>Ask three questions: <em>are your crew employees or sub-contracted?</em>, <em>do you own your lorries or hire them?</em>, <em>where is your depot?</em>. Legitimate firms answer all three immediately and specifically. Rogues hedge — &ldquo;it depends on the day&rdquo;, &ldquo;we use a network of trusted partners&rdquo;, &ldquo;we&rsquo;re mobile-based&rdquo;.</p>
<p>The signal is the specificity of the answer. A directly-employed firm names individual crew members; an owned-fleet firm names the specific lorries; a depot-based firm gives the address and says &ldquo;come visit any time&rdquo;. The hedging answers indicate a broker model at best or a rogue at worst.</p>
<p>The fix: ask the questions, and weigh the answers. The broker-model topic is covered in the <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> and the <a href=\"choosing-a-removal-company-eastbourne.html\">choosing-a-remover guide</a>. Our crews are <a href=\"../about-us.html\">directly employed</a>, our lorries are owned, our depot is at Lower Dicker.</p>"""),
            ('Warning sign six — pressure to book, vague website, fake reviews',
             """<p>High-pressure sales tactics — &ldquo;this slot expires today&rdquo;, &ldquo;the price goes up tomorrow&rdquo; — are red flags. Legitimate removers have busy diaries but the conversion process is patient; they want the customer to be comfortable with the booking. Pressure is for rogues operating on a high-churn, low-retention model.</p>
<p>The website itself is a signal. Spelling mistakes, broken contact forms, no specific address, stock photos with no genuine staff or fleet images, customer testimonials with no names or dates. None of these are conclusive on their own but combined they paint a picture.</p>
<p>Reviews are the other signal. Search the firm on Google, Trustpilot and the BAR site. If reviews are all five-star and posted in clusters, they may be fake. If the firm has zero negative reviews ever, they may be filtering. A reputable firm has mostly-positive reviews with some negatives, all responded to professionally. Our <a href=\"../reviews.html\">reviews page</a> has the unfiltered set.</p>"""),
            ('What to do if you suspect you have been targeted',
             """<p>If you&rsquo;ve already paid a deposit to a firm you now suspect is rogue, act fast. Contact your bank and report the transaction (some bank cards offer Section 75 protection on credit transactions). Contact Action Fraud (the UK reporting service) and the BAR (who will investigate if the firm claimed membership it didn&rsquo;t have).</p>
<p>If a rogue operator has already collected your contents and you can&rsquo;t reach them, contact the police and Trading Standards immediately. The contents may be at the operator&rsquo;s yard waiting for a ransom-pricing demand; quick action prevents this. The BAR will also help member firms recover legitimate customer contents from non-member operators.</p>
<p>The best protection is the prevention — pick a BAR-registered, properly-insured, directly-employed firm at booking. The hour of due diligence at the start saves the months of frustration if things go wrong. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> if you&rsquo;d like a second opinion on a quote you&rsquo;ve received elsewhere — we&rsquo;re happy to share what we&rsquo;d look for.</p>"""),
        ],
        'faqs': [
            ("How common are rogue removal scams in the UK?",
             "Rare for fully-trained Sussex moves with BAR-member firms, more common for budget operators and quote-by-phone arrangements. The BAR enforcement team handles a handful of cases per year nationally."),
            ("If a firm asks for 50% deposit, are they rogue?",
             "Not necessarily, but it's higher than the BAR-standard 20–25%. Ask why. If the answer is convincing (specialist work, very high-value contents, international with import duties), it may be legitimate. If the answer is vague, walk away."),
            ("Should I ever pay in cash?",
             "For amounts under £500, fine if you prefer. For full removal payments, no — card or bank transfer keeps the transaction traceable and gives you Section 75 protection on credit cards."),
            ("What if the firm isn't BAR but seems otherwise legitimate?",
             "Some genuinely good small operators choose not to be BAR. If the firm checks out on every other criterion (Companies House, insurance, references, depot), they may still be a sensible choice — but you lose the APG deposit protection."),
            ("Where do I report a suspected rogue?",
             "Action Fraud (UK national fraud reporting), Trading Standards, and BAR if the firm claimed BAR membership. If contents have been collected and the firm is unreachable, contact the police immediately."),
        ],
    },

    # ---- Topic 30 ----
    {
        'slug': 'moving-day-survival-kit.html',
        'title': 'Moving Day Survival Kit: Essential Items You Need',
        'desc': 'Don\'t get caught without the basics. Here\'s exactly what should be in your moving day survival kit.',
        'kicker': 'The survival kit · 40 years of move-day blind spots',
        'h1': 'Moving Day Survival Kit — The Essential Items You Need',
        'hero_sub': "The kettle is the obvious one. The other twenty items are the ones nobody thinks of until they need them at 9pm in an unfamiliar kitchen.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Survival kit',
        'intro_html': """<p style=\"font-size:1.15rem;\">After ten thousand moves we&rsquo;ve watched a lot of move-day mornings unfold. The pattern is consistent: the family that packed a proper survival kit for the day is calm by 5pm and asleep on a real bed by 11pm; the family that didn&rsquo;t is still hunting for the toothbrush at midnight. The difference is one carton.</p>
<p>This guide is the contents of that one carton. Tape it red. Pack it last. Load it last onto the lorry so it comes off first at the new property. Or better — travel with it in your own car so it&rsquo;s never out of your hands. The list below is the everything-you-actually-need-on-day-one set, drawn from the practical experience of moving households since 1982.</p>""",
        'sections': [
            ('The kitchen bare essentials',
             """<p>The first-night kitchen needs to function at a minimum level the moment you arrive. The kettle is non-negotiable. So is one mug per family member, tea or coffee, milk (bring it in a cool bag from the old house), sugar if you take it, kitchen towel, and a roll of clingfilm or some sandwich bags for the food you&rsquo;ll buy on the way.</p>
<p>Add: one set of plates and cutlery per family member (single set, not the family wedding china), one mug, one frying pan, one saucepan, one chopping board, a knife, a spatula. Bottle opener and wine opener — yes, both. A few sponges, washing-up liquid, a tea-towel. Salt, pepper, oil. That&rsquo;s the entire kitchen for 24 hours.</p>
<p>What you don&rsquo;t need on day one: the food processor, the slow cooker, the spice rack, the second-best china, the third saucepan. Pack those properly using the <a href=\"how-to-pack-kitchen-items-safely.html\">kitchen-packing guide</a> — they&rsquo;ll surface in the proper unpacking over the following week.</p>"""),
            ('The bathroom and toilet kit',
             """<p>The bathroom is the most common forgotten room. The list: toilet roll (two rolls — the previous owner has almost certainly taken theirs), hand soap or liquid soap, a hand towel and one bath towel per family member, your toiletries (toothbrush, toothpaste, deodorant, shampoo, soap), any prescription medications.</p>
<p>For families with younger children: their bath toys, their shampoo, their toothbrush in its travel case, any specific products they need. For adults with allergies or medical conditions: your specific medications and the prescription paperwork. Don&rsquo;t leave prescriptions in the lorry — they travel with you in the car always.</p>
<p>A small first-aid kit covers minor injuries from the move itself — bandages, ibuprofen, antiseptic wipes, plasters. Moving day generates more scrapes and bumps than people expect; having the kit accessible saves a chemist run on day one.</p>"""),
            ('The bedroom and sleep essentials',
             """<p>Bedding is the second-most-common overlooked category. You need: one set of sheets, one duvet cover and pillowcases per bed, the duvet itself, pillows, a blanket (handy if the heating isn&rsquo;t working yet). If you have children, their familiar bedding and any sleep-companion teddy or comforter.</p>
<p>The beds themselves will be among the first pieces unloaded from the lorry (the crew loads them in a stack-safe order — see the <a href=\"what-happens-on-moving-day.html\">moving-day step-by-step guide</a>). Make them up before anything else — the rest of the unpacking can wait, but a made bed is the single biggest contribution to a calm first night.</p>
<p>If you&rsquo;ve booked a full <a href=\"../full-packing-service.html\">packing service</a>, our crew can also put the bedding back on once the bed frames are reassembled. Mention it at survey. Otherwise, pack the bedding into one clearly-labelled carton (FIRST NIGHT / BEDROOM) and unpack it within the first 30 minutes of arriving.</p>"""),
            ('Tools, batteries and the random useful items',
             """<p>A small toolkit saves a lot of swearing on the first night. The list: a Stanley knife or scissors for opening cartons (the crew brings their own but you&rsquo;ll be unpacking after they leave), a small screwdriver set (Phillips and flat), a hammer, a tape measure, a level. Picture hooks and a small bag of screws. A roll of masking tape for labelling.</p>
<p>Batteries — AA and AAA — for the smoke alarms, the remote controls, the kids&rsquo; battery-operated toys. The new house&rsquo;s smoke alarms are almost certainly bleeping because the previous owners didn&rsquo;t change them; the bleep at 2am is one of moving day&rsquo;s great clich&eacute;s. Have batteries on hand.</p>
<p>Other random useful items: a torch (and spare batteries), a power strip (your laptop charger plus the kettle plus a phone), bin bags (everything generates them on move day), a notepad and a pen. The notepad is for the meter readings, the things-to-do list, and the &ldquo;ask the previous owner about X&rdquo; list.</p>"""),
            ('Documents and the &ldquo;don&rsquo;t lose this&rdquo; bag',
             """<p>One small bag with documents that should never leave your sight. Passports, driving licences, the move contract, the contract for the property purchase, the conveyancer&rsquo;s contact details, the keys to the new property (handed to you on completion day — don&rsquo;t put them in your pocket and forget which pocket), insurance documents, the children&rsquo;s school records, pet vaccination records.</p>
<p>Add: any cash you&rsquo;re carrying, jewellery, prescription medications. These should NEVER go in the lorry. Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> excludes irreplaceable documents and valuables; the safest place for them is in your car or on your person.</p>
<p>Phone chargers — at least two (one for the car, one for the new house). One phone charger gets misplaced on every move; having a spare prevents the &ldquo;phone died at 7pm&rdquo; failure mode. A power bank as backup if you can. The <a href=\"10-most-commonly-forgotten-moving-items.html\">10-most-forgotten-items guide</a> covers the wider list.</p>"""),
            ('Food, drink, and the &ldquo;eat tonight&rdquo; plan',
             """<p>The kitchen won&rsquo;t be functional for proper cooking on the first night. Plan for this. Either pre-arrange a takeaway from a local place near the new property (Just Eat, Deliveroo and Uber Eats all work; pick the place before move day), or pack a cooler box with sandwich-makings, fruit, drinks and snacks for the family.</p>
<p>Add a few bottles of water. The water at the new property is fine to drink but the kettle won&rsquo;t be unpacked for the first hour and cold tap water from an unfamiliar pipe is psychologically less appealing than a cool bottle from the cooler. Same logic for milk and soft drinks for the kids.</p>
<p>For adults: a bottle of wine or beer in a cool bag, opened with the bottle opener from the kitchen kit. The first sit-down at the new house is one of the small move-day pleasures; having something nice to drink isn&rsquo;t a luxury, it&rsquo;s an investment in psychological wellbeing. The <a href=\"what-happens-on-moving-day.html\">step-by-step guide</a> covers when this moment usually arrives.</p>"""),
            ('Pets, plants, and the special-case items',
             """<p>If you have pets, their entire daily kit travels with you in the car. Food bowl, water bowl, food, leash, favourite toy, carrier (for cats), blanket from the old house, prescribed medications. The <a href=\"moving-house-with-pets.html\">moving-with-pets guide</a> covers the broader plan.</p>
<p>Houseplants travel in the car too if the journey is short. For longer moves they may need to go in the lorry — talk to us at survey. Either way, mark the cartons clearly. Plants that survive a move are usually the ones whose conditions stayed roughly consistent across the day.</p>
<p>For older relatives or anyone with mobility issues moving with you: their specific needs (walking stick, reading glasses, hearing aids, medication, a comfortable chair to sit in during the load) need to be planned for explicitly. Don&rsquo;t leave older relatives in an empty room with no chair to sit on; arrange for one comfortable chair to remain accessible throughout the load and the unload.</p>"""),
        ],
        'faqs': [
            ("What's the single most important item?",
             "The kettle. Plus mugs, tea, milk. The first sit-down with a cup of tea is the moment the move stops being chaos and starts being &lsquo;our new house&rsquo;."),
            ("Where should the survival kit travel — car or lorry?",
             "Your car, not the lorry. If you absolutely have to put it in the lorry, tape it bright red, label it FIRST NIGHT, and load it LAST so it's the FIRST off at the other end."),
            ("Do I need separate kits for each family member?",
             "One shared kit for the household, plus a small personal overnight bag per person (clothes, toothbrush, pyjamas, phone charger). Children&rsquo;s overnight bags should include a favourite teddy."),
            ("What about food for the first day?",
             "Either pre-arrange a takeaway from a local place near the new property, or pack a cool bag with sandwich-makings and snacks. The kitchen won&rsquo;t be functional for proper cooking in the first 24 hours."),
            ("Should I pack the toolkit with the moving boxes?",
             "Separately, in the survival kit. You'll need the Stanley knife, screwdriver, hammer and tape measure within the first hour at the new house — they shouldn't be buried in a packed carton."),
        ],
    },
]


# ----------------------- TEMPLATE LOADER ----------------------------
TEMPLATE = open(TEMPLATE_PATH, encoding='utf-8').read()

def render_section(h2, html_body, soft):
    cls = 'np-section np-section-soft' if soft else 'np-section'
    return f"""  <section class="{cls}">
    <div class="np-inner">
      <h2>{h2}</h2>
      {html_body}
    </div>
  </section>
"""

def render_faq(faqs):
    items = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return ('  <section class="np-section np-faq">\n'
            '    <div class="np-inner">\n'
            '      <h2>Frequently asked questions</h2>\n'
            + items + '\n'
            '    </div>\n'
            '  </section>\n')

def render_related(slug):
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

def render_cta():
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

def render_closing():
    return """  <section class="np-section">
    <div class="np-inner">
      <h2>Why customers choose Mark Ratcliffe Moving for Sussex moves</h2>
      <p>We've been a <a href="../about-us.html">family-run Sussex remover</a> since 1982 &mdash; the same name on the lorry as the name on the paperwork. Mark personally surveys the high-value and overseas moves; our crews are directly employed (not casual day labour) and trained at our own staff training centre, one of only a handful of UK removers with that facility on site.</p>
      <p>Standard inclusions on every full removal: pad-wrap protection for every freestanding piece of furniture, removal-grade cartons, a written and itemised <a href="../mark-ratcliffe-moving-online-removals-quote.html">fixed-price quote</a> with no surprises on the day, and the British Association of Removers' Advance Payment Guarantee protecting every deposit. The result, over forty years and tens of thousands of moves, is a 4.9/5 review average across <a href="../reviews.html">120+ independent Google reviews</a>.</p>
      <p>Booking the survey takes ten minutes. Whether it's a one-bedroom flat across <a href="../removals-eastbourne.html">Eastbourne</a> or a country house to <a href="../international-removals-eastbourne.html">overseas</a>, the process is the same: in-home or video survey, written quote within 48 hours, deposit-protected booking, and a calm move day.</p>
    </div>
  </section>
"""

def render_body(blog):
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
    for i, (h2, body) in enumerate(blog['sections']):
        parts.append(render_section(h2, body, soft=(i % 2 == 0)))
    parts.append(render_closing())
    parts.append(render_cta())
    parts.append(render_faq(blog['faqs']))
    parts.append(render_related(blog['slug']))
    return ''.join(parts)


def render_head(blog):
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
  <link href="../css/normalize.css?v=20260548" rel="stylesheet">
  <link href="../css/components.css?v=20260548" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260548" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260548" rel="stylesheet">
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
  <script defer src="../js/nofollow-shim.js?v=20260548"></script>
</head>
"""

NAV_START = TEMPLATE.index('<body>')
NAV_END   = TEMPLATE.index('<nav class="np-breadcrumb">')
NAV_BLOCK = TEMPLATE[NAV_START:NAV_END]

FOOTER_START = TEMPLATE.index('<footer')
FOOTER_END   = TEMPLATE.rindex('</html>') + len('</html>')
FOOTER_BLOCK = TEMPLATE[FOOTER_START:FOOTER_END]


def render_blog(blog):
    return render_head(blog) + NAV_BLOCK + render_body(blog) + FOOTER_BLOCK


# ----------------------- WRITE FILES --------------------------------
n = 0
for blog in BLOGS:
    out_path = os.path.join('blog', blog['slug'])
    open(out_path, 'w', encoding='utf-8').write(render_blog(blog))
    n += 1
    print(f'  wrote {out_path}')
print(f'\nCreated {n} new blog posts.')
