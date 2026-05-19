#!/usr/bin/env python3
"""Generate blog posts 31-40 from the user's numbered list."""
from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TEMPLATE_PATH = 'blog/cost-of-moving-house-sussex-2026.html'

BLOGS = [
    # ---- Topic 31 ----
    {
        'slug': 'moving-house-in-winter.html',
        'title': 'Moving House in Winter: Essential Tips for Cold Weather Moves',
        'desc': 'Moving during winter? Learn how to prepare for cold weather, protect your belongings, and what extra steps you should take during a winter house move.',
        'kicker': 'Cold weather moves · Frost, fog and short days · 40 years on Sussex routes',
        'h1': 'Moving House in Winter — Essential Tips for Cold Weather Moves',
        'hero_sub': "Short days, frosty mornings, occasional snow. Winter moves are the quietest season for the industry — and the easiest to plan around if you know the variables.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Moving in winter',
        'intro_html': """<p style=\"font-size:1.15rem;\">Winter is the quietest season in the UK removals industry — November through February sees roughly half the volume of the May-to-September peak. For customers willing to move outside the summer rush, this means more diary flexibility, easier <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey scheduling</a>, and sometimes a modest discount on quotes. After forty years of <a href=\"../about-us.html\">Sussex removals</a> we&rsquo;ve learned exactly how to plan a winter move so the weather doesn&rsquo;t become a problem.</p>
<p>The three big winter variables are short daylight, cold temperatures (and occasional snow or ice), and the heating-and-condensation question for storage and the new property. This guide covers each, plus the practical clothing, vehicle and crew considerations for a calm winter move day.</p>""",
        'sections': [
            ('Daylight — the timing question',
             """<p>The first practical winter variable is daylight. UK sunrise in December and January is around 8am, sunset around 4pm — meaning effective working light from 8:30am to 3:30pm. A typical 3-bed move loads in 4&ndash;5 hours; if loading starts at 8am it finishes in good light. For 4&ndash;5 bed moves the loading can run past dark, which is workable but slower.</p>
<p>Our winter standard is to start the crew at the depot at 6:30am so we&rsquo;re at your property by 7:30am — half an hour earlier than the summer standard. The aim is to maximise productive daylight for the load. Unloading at the new property usually finishes by mid-afternoon for routine moves; longer-distance or larger moves may need lorry headlights and a portable LED at the unload end.</p>
<p>If your move involves a long drive (London-to-Sussex, the West Country, the North), the daylight question shifts to driving safety. We avoid scheduling a winter overnight stop where possible; the lorry is back at our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> before dark if at all possible. For winter international moves see <a href=\"../international-removals-eastbourne.html\">international removals</a> &mdash; the customs holding bay is climate-controlled regardless of season.</p>"""),
            ('Cold weather — protecting belongings and the lorry',
             """<p>Cold temperatures affect several categories of household possession. Electronics with lithium-ion batteries (laptops, power tools, e-bikes) lose capacity in cold and the batteries themselves can degrade if stored below freezing for extended periods. For winter moves we recommend removing batteries from sensitive devices and transporting them in your own car.</p>
<p>Liquids freeze. Wine, water-based cleaning products, watered-down paint, certain shampoos and toiletries can all freeze in an unheated lorry on a long winter journey. For shorter moves (under three hours) this isn&rsquo;t usually an issue; for longer hauls, pack liquids in a thermal bag with a hand warmer or transport them in your own car.</p>
<p>Plants in pots that freeze can crack — both the pot and the plant. Pad-wrap protects against impact but not against freezing. Plants travel with you in the car for winter moves wherever practical. For valuable specimen plants (citrus trees, large bay trees, established camellias), talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> and we&rsquo;ll arrange specific protection or recommend rescheduling if a heavy frost is forecast.</p>"""),
            ('Snow, ice and the contingency plan',
             """<p>UK snow is unpredictable but rarely severe enough to stop a Sussex move. We&rsquo;ve had one or two days a year over forty years where conditions actually became unworkable; the rest of the time the lorry runs as normal with winter tyres and the crew adjusts pace. Our diary policy: we don&rsquo;t cancel a winter move unless conditions are genuinely dangerous, and if we do cancel we reschedule at the earliest possible date with no extra charge.</p>
<p>If your move date forecasts snow or ice, talk to us 24 hours ahead. We&rsquo;ll monitor the Met Office warnings and either run as normal, start earlier, or reschedule. For chain-day completions the chain itself often controls the timing &mdash; if everyone else in the chain is going ahead, we&rsquo;ll go ahead too. If conditions are unworkable we&rsquo;ll discuss alternatives with you and your conveyancer.</p>
<p>Practical kit for the crew on snowy days: grit for the front path (we bring some, you can have some on standby), salt-tolerant pad-wrap blankets (the depot keeps a dedicated winter set), and waterproof footwear and gloves. The customer&rsquo;s job is to ensure paths are gritted, the front door area is accessible, and any external steps are de-iced. If you&rsquo;re not physically able to do this, mention it at survey and we&rsquo;ll arrange.</p>"""),
            ('The condensation question — heating and storage',
             """<p>The biggest invisible winter risk is condensation. When cold contents (from an unheated lorry) move into a warm house, the temperature differential causes moisture to condense on the cold surfaces. Furniture, paperwork, electronics, photographs &mdash; all at risk if they move from cold to warm quickly.</p>
<p>The fix is climate-stable storage if anything is going into the depot between completion dates. Our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> is insulated and ventilated, which prevents the cold-vs-warm differential that drives condensation. Customers using non-climate-stable storage (cheaper but unsuitable for winter long-term holding) sometimes find boxes of photos and books arriving damp at the destination. The <a href=\"how-to-choose-right-self-storage.html\">storage-format guide</a> covers the difference in detail.</p>
<p>At the new property, the equivalent fix is gentle warming. Don&rsquo;t blast the heating immediately after the lorry has unloaded into a cold house &mdash; the temperature shock causes condensation. Set the heating to come on gradually over a few hours rather than going from 8&deg;C to 22&deg;C in 15 minutes. For valuable contents like antiques and pianos (see <a href=\"moving-antiques-valuable-furniture.html\">antiques moving</a>), this gradual warming is genuinely important.</p>"""),
            ('Heating, broadband and the new-property checklist',
             """<p>Walk into the new property knowing where the heating system controls, fuse box, water stopcock, and the cooker isolator are. The previous owner may or may not have left clear instructions; the property survey or estate-agent move-in note usually flags any quirks. If the heating doesn&rsquo;t come on within an hour of arrival, escalate to a local heating engineer rather than waiting for goodwill.</p>
<p>Order broadband well ahead of move day. Openreach engineer appointments in East Sussex routinely run 2&ndash;3 weeks out, so booking should happen 4 weeks ahead at minimum. Winter is when home-working pressure makes broadband particularly critical; the &lsquo;first week without internet&rsquo; problem is harder to live with in November than in July.</p>
<p>The other utility setup tasks &mdash; gas, electric, water, council tax &mdash; are the same as any season. Photograph meters on arrival, submit readings the same day, set up direct debits in the first week. The <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> covers the full admin checklist for the first week.</p>"""),
            ('Clothing, vehicle prep and the family comfort plan',
             """<p>Winter move day clothing isn&rsquo;t glamorous but it matters. Layers (you&rsquo;ll be moving between cold outdoor air and warmer indoor space all day), waterproof boots (front paths get muddy quickly), waterproof jacket and gloves, and a beanie or warm hat. The crew is dressed for this; the customer often isn&rsquo;t. Cold hands and feet make the day significantly harder than it needs to be.</p>
<p>For the car: full tank of fuel the night before (winter mornings are not the time to discover the petrol station queue), de-iced and ready to go from the early start, screenwash topped up, tyre pressures checked. If you&rsquo;re driving anything precious (the houseplants, the pets, the children, the document folder) the car comfort matters.</p>
<p>Family comfort plan: a thermos of hot drink, sandwiches and snacks for the journey, a blanket for the dog, the children&rsquo;s warm coats packed accessibly rather than in the lorry. The first cup of tea at the new house is one of the small move-day pleasures regardless of season; in winter it&rsquo;s genuinely warming. The <a href=\"moving-day-survival-kit.html\">survival kit guide</a> covers the essentials.</p>"""),
        ],
        'faqs': [
            ("Is winter really cheaper for removals?",
             "Sometimes 5–10% lower than summer peak, plus more diary flexibility. The crew rates are identical; the saving comes from quieter demand. Worth considering if your completion timing allows."),
            ("What happens if it snows on move day?",
             "We monitor Met Office warnings 24 hours ahead and discuss with you if conditions are forecast. Most UK snow doesn't stop a Sussex move; in genuinely dangerous conditions we reschedule at no extra charge."),
            ("Will my belongings freeze in the lorry?",
             "Standard household contents are fine. Liquids, plants and electronics with lithium-ion batteries are the categories to watch for long-distance winter moves. Transport these in your own car where practical."),
            ("Is condensation really a problem in winter moves?",
             "Yes — moving cold contents into a warm house causes moisture to condense on the cold surfaces. Use gradual warming (not blast heating) at the new property and climate-stable storage for any between-contract holding."),
            ("What time does the crew start in winter?",
             "Half an hour earlier than summer — depot 6:30am, on your driveway by 7:30am. The aim is to maximise productive daylight for the load."),
        ],
    },

    # ---- Topic 32 ----
    {
        'slug': 'moving-over-christmas-and-new-year.html',
        'title': 'Moving House Over Christmas and New Year – What You Need to Know',
        'desc': 'Planning a Christmas or New Year house move? Here\'s everything you need to consider before booking a removal date over the festive period.',
        'kicker': 'Festive-period moves · Bank holidays · Quiet diary · Higher logistics',
        'h1': 'Moving House Over Christmas and New Year — What You Need to Know',
        'hero_sub': "Conveyancers close, banks shut for bank holidays, removers run skeleton diaries. Here is how to plan a successful festive-period move.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Christmas and New Year moves',
        'intro_html': """<p style=\"font-size:1.15rem;\">The festive period &mdash; from about December 22nd through to January 5th &mdash; is the quietest two weeks of the year in the UK removals industry. Most reputable firms run a skeleton service, conveyancers close their offices, banks close for the bank holidays, and the property market essentially pauses. For customers committed to a Christmas-or-New-Year completion, this guide covers what we&rsquo;ve learned about making it work.</p>
<p>It&rsquo;s perfectly possible to move successfully over this period &mdash; we do a handful of festive moves every year &mdash; but the variables shift. Booking lead times, deposit timing, chain availability and crew rates all behave differently. The detail below walks through each consideration so you arrive at the right decision for your situation.</p>""",
        'sections': [
            ('Why Christmas/New Year moves happen at all',
             """<p>The most common reason is the conveyancing calendar. UK property completions often cluster around the December bank-holiday cut-off because solicitors push to clear cases before the office closure. The result: a wave of late-December completions where the buyer and seller are committed but the wider market has gone quiet.</p>
<p>The second common reason is tax-year planning. December 31st is the cut-off for certain reliefs and capital-gains positions; a small percentage of moves are scheduled to complete just before year-end for tax purposes. The third reason is simply that the buyer or seller has personal flexibility (between jobs, sabbatical, retirement) and prefers the quieter period for the move itself.</p>
<p>None of these reasons are wrong, but each comes with the festive-period logistics overlay. Before committing to a Christmas completion, talk to your conveyancer about the office schedule and to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> about our diary availability. The <a href=\"cost-of-moving-house-sussex-2026.html\">2026 cost guide</a> covers the wider pricing picture.</p>"""),
            ('Bank holidays, conveyancing and the funds-release problem',
             """<p>Banks close on Christmas Day, Boxing Day, and New Year&rsquo;s Day. They also close any &ldquo;substitute&rdquo; bank-holiday days when 25 December or 1 January falls on a weekend. The practical effect on a property completion: funds cannot transfer on bank-holiday days. A &ldquo;completion&rdquo; scheduled for a closed-bank day is impossible &mdash; the chain has to complete the working day before or after.</p>
<p>The working days available for completion over the festive period are typically December 22nd, 23rd, 24th (often a half-day for solicitors) and then December 29th, 30th, 31st (often closed too) and January 2nd, 3rd. The actual workable days vary year-to-year based on which day of the week the bank holidays fall.</p>
<p>What this means for the customer: confirm with your conveyancer at least four weeks ahead which specific date the completion will land on. Don&rsquo;t book the removal until that date is confirmed. We&rsquo;ll provisionally hold a slot on a likely date but the final booking happens once the conveyancer confirms. See the <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> for the full 8-week run-up.</p>"""),
            ('Removal diary availability over the festive period',
             """<p>Most reputable Sussex removers (including us) run a reduced diary between December 22nd and January 5th. Crews take Christmas leave; the depot is staffed on a skeleton basis; the major moves happen on December 22nd&ndash;23rd or January 5th onwards. The mid-period (December 27th&ndash;January 3rd) is genuinely quiet.</p>
<p>If your completion date falls in the mid-period, book early &mdash; the few available crews fill up fast. December moves get booked from October onwards. January 5th onwards is similar &mdash; the post-holiday surge means anyone with a January completion is competing for slots that filled up before Christmas.</p>
<p>Rates over the festive period are usually the same as standard winter rates &mdash; we don&rsquo;t add a holiday surcharge for ordinary working days. Bank-holiday day work itself (rare, but possible) is charged at a premium because the crew is on holiday-pay rates. Talk to us about the specific date and we&rsquo;ll quote transparently. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers what to confirm in any quote.</p>"""),
            ('Storage between completion dates over Christmas',
             """<p>A surprising number of festive-period customers need storage between completions. The pattern: the December completion goes ahead on the 22nd or 23rd, the load goes into our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a>, and we redeliver in the first week of January when the new property completes.</p>
<p>The depot is staffed throughout the festive period for security and minor operations, but bulk in-and-out activity pauses between December 24th and January 2nd. If your storage needs are short (a week or two) this is fine &mdash; the contents sit safely in the climate-stable strong-room and are ready for redelivery as soon as the new completion lands.</p>
<p>Insurance, security and access arrangements continue as normal. Our depot has 24/7 CCTV and alarm monitoring throughout the festive period; the relevant details are in the <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance page</a>. The <a href=\"short-term-vs-long-term-storage.html\">short-vs-long-term storage guide</a> covers the contract terms.</p>"""),
            ('Practical considerations — children, pets, family',
             """<p>The festive period is when the household calendar is busiest with family commitments. School holidays, work parties, family gatherings, religious observances. Layering a house move on top is genuinely demanding. Make sure the family logistics &mdash; where the children stay, who hosts the pet, what the Christmas-dinner plan looks like &mdash; are decided well ahead.</p>
<p>Travel patterns over the festive period are also less predictable. Train strikes, road works, family visits from far away. If guests are arriving on the day of the move, they don&rsquo;t. Reschedule them for the next day. The move itself plus visiting guests on the same day is a recipe for missed pickups and tired arguments.</p>
<p>For the move day itself, the rule is the same as any season: keep children somewhere else if possible, plan the pet&rsquo;s day separately (see <a href=\"moving-house-with-pets.html\">moving with pets</a>), have a clear &ldquo;first night&rdquo; plan for food and bedtime. The <a href=\"moving-day-survival-kit.html\">survival kit guide</a> applies year-round.</p>"""),
            ('The first weekend in the new house',
             """<p>If your move completed on December 22nd&ndash;23rd, you&rsquo;re probably hosting Christmas in the new house within 48 hours. This sounds chaotic but is actually manageable: prioritise the kitchen (so cooking is possible) and the bedrooms (so guests have somewhere to sleep), leave everything else for January.</p>
<p>The <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a> covers the priority order; for Christmas-arrival, the additional priority is the dining table and chairs (or a workable substitute) and the basic Christmas Day cooking kit. If you have a pre-arranged Christmas-decoration set, that&rsquo;s the next priority &mdash; a Christmas tree up by Christmas Eve is a meaningful psychological win.</p>
<p>For New Year completions, the priority shifts. New Year completions typically have a quieter follow-up window than Christmas ones &mdash; you have a fortnight of January to unpack at a sensible pace. Use it. The temptation to power through the unpack in the first week leaves everyone exhausted by mid-January.</p>"""),
        ],
        'faqs': [
            ("Can we actually complete on a bank holiday?",
             "No. Banks don't transfer funds on closed days. Confirm the exact completion date with your conveyancer at least four weeks ahead; the workable festive-period days vary year-to-year."),
            ("Are removers more expensive over Christmas?",
             "Standard winter rates for ordinary working days. Bank-holiday day work (rare) carries a premium because the crew is on holiday-pay rates. We quote transparently."),
            ("Should I book early for a December move?",
             "Yes — December moves book up from October. The few crews available between December 22nd and January 5th fill up fast."),
            ("Can you store our belongings between Christmas completions?",
             "Yes — our depot strong-rooms are staffed throughout the festive period for security. Bulk in-and-out pauses between Christmas Eve and January 2nd, but short-term storage works fine."),
            ("Is it worth scheduling a Christmas move at all?",
             "If the property chain dictates the date, you don't have a choice. If you have flexibility, the November or January-onwards periods are easier. Talk to us at survey and we'll give you an honest view."),
        ],
    },

    # ---- Topic 33 ----
    {
        'slug': 'moving-during-school-holidays.html',
        'title': 'Moving House During School Holidays – Is It a Good Idea?',
        'desc': 'Should you move during school holidays? We break down the pros and cons to help you decide the best time to move with children.',
        'kicker': 'School-holiday moves · Pros, cons, timings for families',
        'h1': 'Moving House During School Holidays — Is It a Good Idea?',
        'hero_sub': "The honest pros and cons of timing a family move around the school calendar — when it works, when it doesn't, and how to plan either way.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'School-holiday moves',
        'intro_html': """<p style=\"font-size:1.15rem;\">School-holiday moves are one of the most common questions we get from families. The instinct is right &mdash; aligning a move with a school break reduces the academic-year disruption &mdash; but the practical decision is more nuanced than &ldquo;summer holiday = good time&rdquo;. After forty years of <a href=\"../about-us.html\">family-home Sussex removals</a> we have a clear view of when school-holiday moves work and when they don&rsquo;t.</p>
<p>The three main school holidays are Christmas (mid-December to early January), Easter (two weeks around April), and summer (late July to early September). Each comes with its own combination of pros, cons and pricing. This guide walks through the analysis for each, plus the practical scheduling considerations for families with school-age children.</p>""",
        'sections': [
            ('Summer holidays — the obvious choice and its trade-offs',
             """<p>The summer school holidays (late July through early September in England, with regional variation) are the most popular move window for families. The pull factors are clear: no school interruption, children can stay with grandparents or at holiday club, the weather is generally good, and most families have some annual leave they can stretch around the move.</p>
<p>The trade-offs: this is the absolute peak of the removals diary. End-of-July and August Saturdays book 12&ndash;14 weeks ahead. Conveyancing solicitors are at capacity. School-place administration runs to its tightest timelines (most school transitions happen across the summer break). And prices are at their seasonal peak &mdash; typically 10&ndash;15% above winter rates.</p>
<p>If your completion timing is flexible, the better summer windows are early July (just before peak), mid-week mid-month August, or the first week of September after the bank holiday. These are still busy but easier to book and slightly cheaper. The <a href=\"moving-house-in-summer.html\">moving-in-summer guide</a> covers the heat-specific operational details and the <a href=\"best-schools-eastbourne-families.html\">Eastbourne schools guide</a> covers the admissions timelines.</p>"""),
            ('Easter break — the underrated middle option',
             """<p>The Easter holidays (typically two weeks across late March and early April) are an under-used window for family moves. The school disruption is contained, the weather is improving, and removal diaries are quieter than summer. For families moving between school years (not changing school, just changing house), Easter is often the sweet spot.</p>
<p>The challenge with Easter: the dates shift year-to-year because Easter is based on the lunar calendar. Some years the Easter break falls in late March (overlapping with end-of-Q1 conveyancing rush); other years it falls in mid-April (overlapping with the start of the new tax year). Check the specific dates against your completion timing.</p>
<p>For families with children at independent schools, Easter breaks are usually longer (3 weeks vs the state-school 2) and offer more flexibility. For families with state-school children, the 2-week window is workable but tight if you also need to handle school admin (registering at a new school, attending a settling-in visit). The <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> covers the full 8-week run-up.</p>"""),
            ('Christmas break — only for forced timings',
             """<p>The Christmas holiday period (mid-December to early January) is generally not the right choice for a family move unless completion timing forces it. The reasons: bank holidays interrupt conveyancing, the removals diary is at skeleton level, family Christmas commitments overlap with the move, and the new property may be cold and not yet set up for winter living.</p>
<p>If your completion lands on December 22nd or 23rd, the move is genuinely possible and many families manage it. We&rsquo;ve covered the operational considerations in the <a href=\"moving-over-christmas-and-new-year.html\">Christmas-and-New-Year moving guide</a>. For families with younger children, Christmas in a half-unpacked house can be magical or chaotic depending on temperament; consider this honestly.</p>
<p>For a flexible Christmas-period move, the better dates are the first week of January (5th onwards) rather than the actual Christmas week. The post-holiday windows are quiet, diaries open up, and the children have a clear settling-in window before school restarts.</p>"""),
            ('Half-term breaks — the short-window option',
             """<p>Half-term breaks (typically one week in late October, mid-February, and late May/early June) are short windows but workable for shorter moves. The October half-term is the best of the three: enough time to pack and settle, neutral weather, no major holiday commitments. February half-term is workable but cold; May half-term is workable but starts to clash with the run-up to GCSE/A-level exams.</p>
<p>For local moves (within the same county, where the children stay at the same school), a half-term week is genuinely sufficient: pack the weekend before, move on Monday, unpack across the week, back to school the following Monday. For moves involving school transitions, half-term is too short &mdash; the registration and settling-in process takes longer than a week.</p>
<p>The advantage of half-term: removal diaries are between the seasonal peaks and prices are lower. The disadvantage: short window for any chain delays. If the chain slips by two days, your half-term move becomes a half-term-and-first-school-week move. Build in contingency. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers the chain-flexibility question.</p>"""),
            ('Mid-academic-year moves — when they make sense',
             """<p>Moving during the academic year is generally harder for families than holiday moves, but sometimes the right choice. For very young children (pre-school, reception), a mid-year move is essentially the same as a holiday move &mdash; the &ldquo;school&rdquo; is a nursery with flexible attendance. For primary children mid-year, the disruption is real but manageable.</p>
<p>For secondary children, mid-year moves are harder. Friendships are established, GCSE and A-level courses are mid-syllabus, and joining a new school in the middle of term is socially harder than at the start. If you have flexibility, summer or Easter is meaningfully better. If you don&rsquo;t, talk to the new school&rsquo;s pastoral team before move day &mdash; most good schools have settling-in protocols for mid-year arrivals.</p>
<p>The administrative timing also matters. Mid-year school transfers need direct application to the school rather than through the council process. Available places only exist if a current pupil leaves. The most-oversubscribed schools (in Eastbourne, that&rsquo;s several &mdash; see the <a href=\"best-schools-eastbourne-families.html\">schools guide</a>) rarely have mid-year places. Plan around this constraint, not against it.</p>"""),
            ('Booking timing and the family schedule',
             """<p>Once you&rsquo;ve picked the window, the booking timing matters. For summer moves, book the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> 12&ndash;16 weeks ahead. For Easter, 8&ndash;10 weeks. For half-term, 6&ndash;8 weeks. For Christmas, 10&ndash;12 weeks. These are all longer than the equivalent non-holiday booking lead times because every family is competing for the same windows.</p>
<p>Coordinate the family schedule explicitly. Who&rsquo;s looking after the children on move day? Who&rsquo;s walking the dog? Who&rsquo;s handling the meter readings and the final walkthrough? Who&rsquo;s travelling separately in the car? Write it down. The week before the move, do a dry-run of the day&rsquo;s schedule with the family so everyone knows their role.</p>
<p>One last consideration: the post-move settling-in period. School-holiday moves work best when there&rsquo;s still a week of holiday remaining after the move &mdash; time to unpack the children&rsquo;s rooms, register with the new school, walk the new neighbourhood. Plan for this gap; don&rsquo;t move on the last day of the holiday. The <a href=\"moving-house-with-children.html\">moving with children guide</a> covers the family logistics in detail.</p>"""),
        ],
        'faqs': [
            ("When is the best school holiday to move?",
             "Summer for the longest window, Easter for the best balance of weather and disruption, half-term for short local moves. Christmas is usually only the right choice if completion timing forces it."),
            ("How much earlier do I need to book a school-holiday move?",
             "12–16 weeks for summer. 8–10 weeks for Easter. 6–8 weeks for half-term. 10–12 weeks for Christmas. All longer than equivalent non-holiday booking windows."),
            ("Can I move mid-week during summer holiday and save money?",
             "Yes — mid-week mid-month August dates are easier to book and sometimes 10–15% cheaper than the Saturday peak. Worth considering if your completion is flexible."),
            ("How does a school-holiday move help children settle?",
             "Time to unpack their rooms, register with the new school, walk the neighbourhood, meet local children. Plan for at least a week of holiday remaining after the move, not the very last day."),
            ("What if my move date slides into the school term?",
             "Build contingency into the booking — don't book the move for the last day of the holiday window. If the chain slips and you end up with a school-term move, talk to both schools immediately about a phased transition."),
        ],
    },

    # ---- Topic 34 ----
    {
        'slug': 'moving-to-listed-building-sussex.html',
        'title': 'Moving into a Listed Building in Sussex – What You Need to Know',
        'desc': 'Moving to a Grade II listed property? Learn about narrow doors, parking restrictions, antique handling, and special care required for listed buildings.',
        'kicker': 'Listed-building moves · Grade I, II* and II · 40 years of period-property work',
        'h1': 'Moving into a Listed Building in Sussex — What You Need to Know',
        'hero_sub': "Narrow staircases, original fittings, conservation-area parking and the protection paperwork that comes with historic property. Here is how we handle it.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Listed-building moves',
        'intro_html': """<p style=\"font-size:1.15rem;\">Sussex has one of the highest concentrations of listed buildings in southern England &mdash; tile-hung Wealden farmhouses, Georgian townhouses in Lewes and Rye, Regency villas along the Brighton seafront, medieval cottages in the Downland villages. Moving into or out of a listed property has specific considerations that ordinary moves don&rsquo;t. After forty years of <a href=\"../about-us.html\">period-property removals</a> we&rsquo;ve refined the approach.</p>
<p>The four key considerations: physical access (narrow stairs, doorways, low ceilings), protection of original fittings (panelling, plaster, floors, fireplaces), parking and conservation-area restrictions, and the insurance/heritage paperwork. The detail below covers each. If you&rsquo;d rather discuss it in person, the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">free survey</a> covers all four.</p>""",
        'sections': [
            ('Grade levels and what they mean operationally',
             """<p>Listed buildings come in three grades. <strong>Grade I</strong> is the smallest category &mdash; properties of exceptional interest. <strong>Grade II*</strong> is the middle category &mdash; particularly important buildings of more than special interest. <strong>Grade II</strong> is the largest category and covers most listed houses &mdash; buildings of special interest warranting preservation.</p>
<p>For move-day operations, all three grades require the same protection approach &mdash; the legal protections apply to the building&rsquo;s historic fabric (walls, floors, fittings, plasterwork, joinery) regardless of grade. The differences appear in the wider paperwork: Grade I and II* properties typically have more detailed Heritage Statements and conservation officer involvement. For most domestic moves this doesn&rsquo;t affect the move itself.</p>
<p>What does affect the move: the historic fittings inside the property. Original fireplaces, panelling, plasterwork cornices, leaded windows, Tudor or Georgian floorboards &mdash; all of these need protection during the move. Damage caused during a move can be expensive to repair and (for Grade I and II*) sometimes legally problematic. Our <a href=\"how-our-pad-wrap-service-protects-furniture.html\">pad-wrap method</a> protects furniture; for listed buildings we also bring corner-board and doorframe protection for the building itself.</p>"""),
            ('Narrow access — stairs, doorways and the physical reality',
             """<p>Most listed buildings predate modern furniture sizes. Staircases are narrow (often 80&ndash;90cm against modern 100cm+), doorways are narrow, and ceilings are sometimes too low for taller modern wardrobes. A pre-survey of both properties &mdash; the one you&rsquo;re leaving and the listed one you&rsquo;re moving into &mdash; flags these issues before they become problems on move day.</p>
<p>Specific items that often won&rsquo;t fit: full-height modern wardrobes (designed for 2.4m ceilings, won&rsquo;t go up Tudor stairs), king-size beds in one piece (we split them at the headboard for narrow-stair properties), sofas wider than 90cm (we measure the narrowest staircase at survey), and large display cabinets. The good news: almost everything we&rsquo;ve ever moved has eventually fitted with the right combination of disassembly, alternative routes (sometimes the window with a hoist) and crew time.</p>
<p>If alternative routes are needed &mdash; a hoist through the first-floor window, for example &mdash; we organise this at survey. Furniture hoists cost extra but are sometimes the only option. For valuable contents like pianos (see <a href=\"moving-heavy-awkward-items.html\">moving heavy items</a>) or large display cabinets, the hoist is often the safest as well as the only option.</p>"""),
            ('Protecting the building itself',
             """<p>Standard removal practice protects the furniture. Listed-building practice also protects the property. We bring corner-board (rigid cardboard or foam corner protectors) for doorframes and architraves, soft floor coverings for original timber or stone floors, plus dust sheets for staircases and hallways. The building is dressed before any furniture moves.</p>
<p>The protection materials are removable without trace. We don&rsquo;t use tape directly on listed-building surfaces; everything is held in place with low-tack repositionable tape on the protection material itself, never on the building. For high-value or fragile historic finishes (original wallpaper, Lincrusta panelling, leaded windows), we&rsquo;ll talk through specific protections at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a>.</p>
<p>For Grade I and II* moves and the more valuable Grade II properties, we sometimes recommend a building-condition survey before the move &mdash; a photographic record of every room before any furniture moves in or out. This is the customer&rsquo;s insurance against later disputes about which marks were there before the move and which (if any) were caused by it. The <a href=\"../white-glove-service.html\">white-glove service</a> includes this as standard.</p>"""),
            ('Conservation-area parking and access',
             """<p>Many listed buildings sit in conservation areas with additional parking restrictions. The narrow lanes of Old Town Lewes, the seafront streets of Brighton Regency squares, the medieval centres of Rye and Chichester &mdash; all have access constraints for a 7.5-tonne lorry. Sometimes the lorry simply can&rsquo;t reach the property and we shuttle with a smaller van.</p>
<p>Apply for a parking suspension through the relevant council (East Sussex County Council, Brighton & Hove, Lewes District, or whichever) at least ten working days before move day. For listed-area moves the council sometimes requires additional documentation or pre-visit assessment. We&rsquo;ll handle the practical logistics; the customer applies for the suspension.</p>
<p>For Grade I and II* properties in conservation areas, the conservation officer may have an opinion on parking and access arrangements. This is unusual but happens for high-profile properties. If your purchase paperwork mentions a conservation officer&rsquo;s involvement, share the contact details at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> &mdash; we&rsquo;ll coordinate if needed.</p>"""),
            ('Insurance and the heritage-specific considerations',
             """<p>Standard goods-in-transit insurance covers transit damage to the customer&rsquo;s belongings. For listed-building moves, the building itself isn&rsquo;t covered by removal insurance &mdash; that&rsquo;s the property owner&rsquo;s home insurance. Most home insurance policies cover damage caused during a house move; check yours before move day.</p>
<p>For high-value contents &mdash; family antiques, fine art, valuable rugs &mdash; the standard removal insurance may have per-item limits. Items over £2,500 should be declared specifically on the removal contract. Items over £10,000 usually need a separate specialist policy. The <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance page</a> covers the limits.</p>
<p>For genuinely irreplaceable items (single-edition antiques, museum-grade pieces), we offer the <a href=\"../white-glove-service.html\">white-glove service</a> with individual wrapping, soft-foot rolling, and dedicated transport. For collections of moderate value &mdash; family silver, framed photographs, an antique clock or two &mdash; standard transit insurance with declared values is sufficient.</p>"""),
            ('Booking, surveying and the timeline',
             """<p>Listed-building moves benefit from longer planning. Book the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> 6&ndash;10 weeks ahead of move day. The survey itself takes 60&ndash;90 minutes for a typical listed property &mdash; longer than the 30&ndash;45 minutes for a standard house &mdash; because we&rsquo;re measuring access points, identifying protection requirements, and discussing any specific concerns about historic fittings.</p>
<p>The written quote follows within 48 hours and itemises the listed-building-specific work: building protection materials, corner-board, additional crew time, any specialist handling (piano, antiques, marble). The deposit and booking process is the same as standard moves &mdash; 20&ndash;25% on confirmation, balance on completion day, BAR APG-protected.</p>
<p>For overseas moves from listed Sussex properties (rare but happens), the <a href=\"../international-removals-eastbourne.html\">international removals service</a> coordinates with FIDI-network partners at the destination. Customs paperwork, fumigation certificates for wooden contents, and shipping-grade crating are all part of the standard package. Talk to us at survey if this applies.</p>"""),
        ],
        'faqs': [
            ("Will modern furniture fit into a listed building?",
             "Most will, but full-height modern wardrobes, king-size beds in one piece, and oversized sofas can be a problem. We measure access at survey and flag any items that need disassembly or alternative routes."),
            ("Do I need building permission for the move?",
             "No — moving furniture into a listed building doesn't require listed-building consent. What does require consent is any structural alteration. The move itself is fine."),
            ("Are listed-building moves more expensive?",
             "Marginally — additional building protection materials, longer survey, sometimes a hoist or shuttle van. We quote each line item transparently at survey; there's no premium surcharge."),
            ("Will you protect original fittings?",
             "Yes — corner-board on doorframes, soft floor coverings, dust sheets on staircases, low-tack tape on protection materials only (never on the building). For high-value historic finishes, we discuss specific protections at survey."),
            ("What about the parking restrictions in listed conservation areas?",
             "Apply for a parking suspension via the relevant council ten working days ahead. For tight access we shuttle with a smaller van. Some Grade I properties in conservation areas may need conservation officer coordination — we'll handle this if needed."),
        ],
    },

    # ---- Topic 35 ----
    {
        'slug': 'how-to-downsize-before-moving.html',
        'title': 'How to Downsize Before Moving House – A Practical Guide',
        'desc': 'Struggling with too much stuff? Our practical guide shows you how to declutter and downsize effectively before your house move.',
        'kicker': 'Downsizing · Decluttering · The honest path to less stuff',
        'h1': 'How to Downsize Before Moving House — A Practical Guide',
        'hero_sub': "Less stuff means a cheaper move, a calmer first week and a more comfortable new home. Here is how to make the cuts that actually stick.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Downsizing',
        'intro_html': """<p style=\"font-size:1.15rem;\">Every removal customer we&rsquo;ve ever surveyed has more stuff than they expected. The loft, the garage, the under-stairs cupboard, the spare bedroom &mdash; these are the silent accumulators of a household. Moving is the natural moment to thin them out, and the customers who do it well arrive at the new property with a lighter inventory, a lower removal cost, and a calmer first week. This guide is the practical method we&rsquo;ve seen work over forty years of <a href=\"../about-us.html\">Sussex family-home moves</a>.</p>
<p>The principle is simple: start six weeks ahead, work room-by-room, and use the four-pile method (keep, donate, sell, dispose). The detail below covers the categories that decluttering customers consistently struggle with most &mdash; sentimental items, clothing, books, and paperwork &mdash; plus the practical logistics of charity-shop runs, online selling, and tip visits.</p>""",
        'sections': [
            ('Start six weeks ahead and work room-by-room',
             """<p>The most common downsizing mistake is leaving it until the last fortnight. Six weeks ahead is the sweet spot: enough time to work through each room without rushing, enough time to find buyers for items worth selling, and enough time to do multiple charity-shop runs without making the new house feel impossible. Two weeks is too little; eight weeks is the perfect amount but rare.</p>
<p>The order: start with the rooms you use least &mdash; the loft, the garage, the spare bedroom, the under-stairs cupboard. Move to the medium-use rooms next (the living room, the dining room, the home office). Finish with the rooms you use every day (the kitchen, the bathrooms, the bedrooms). This order means the disruption peaks late in the process, not early when you still need the house to function.</p>
<p>Allow two hours per session and tackle one room at a time. Don&rsquo;t flit between rooms; that produces piles of half-sorted stuff in every room. The <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a> covers the parallel packing schedule that runs alongside the decluttering &mdash; both work better when they&rsquo;re sequenced consistently.</p>"""),
            ('The four-pile method — keep, donate, sell, dispose',
             """<p>For every item, decide on one of four piles. <strong>Keep</strong> goes back where it came from (and will be packed for the move). <strong>Donate</strong> goes to a charity shop or directly to someone who needs it. <strong>Sell</strong> goes to eBay, Facebook Marketplace, Gumtree or a local auction. <strong>Dispose</strong> goes to the council tip or the household recycling collection.</p>
<p>The decision criterion for each item: have I used this in the last 12 months, and would I buy it again today? If both answers are no, the item goes to donate, sell or dispose. The 12-month rule cuts through the &ldquo;but I might need it&rdquo; objection &mdash; if you didn&rsquo;t need it in the last year, you probably won&rsquo;t need it in the next year.</p>
<p>Don&rsquo;t over-engineer the sell pile. Many things people imagine they&rsquo;ll sell on eBay end up sitting in a box for months. Be honest about your time and motivation. For each &ldquo;sell&rdquo; item, ask: am I genuinely going to photograph this, list it, answer messages and post it within four weeks? If the answer is no, move it to donate. Charity shops always need stock; eBay always needs sellers.</p>"""),
            ('Sentimental items — the hardest category',
             """<p>Sentimental items are where most downsizing efforts stall. Family photographs, children&rsquo;s artwork, letters, grandfather&rsquo;s wartime memorabilia, the kids&rsquo; first toys. The 12-month rule doesn&rsquo;t apply here because the value isn&rsquo;t functional. The honest question is different: am I keeping this for myself, or am I keeping it because I feel I should?</p>
<p>The solution is rarely &ldquo;throw it away&rdquo;. The solution is usually &ldquo;keep less of it&rdquo;. A box of 20 of your child&rsquo;s drawings is more meaningful than two boxes of 200. A small album of family photographs is more meaningful than three crates of unsorted prints. The decluttering act is selecting the best, not eliminating the category.</p>
<p>For physical sentimental items you genuinely can&rsquo;t bear to part with but don&rsquo;t want to display, the answer is professional digitisation (for photos, letters, documents) or careful storage in our climate-stable <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a>. Storage costs are real but typically less than the regret of having thrown something away. The <a href=\"short-term-vs-long-term-storage.html\">storage-length guide</a> covers the cost considerations.</p>"""),
            ('Clothing and the wardrobe cull',
             """<p>The average UK adult wears about 30% of the clothes in their wardrobe regularly. The other 70% is split between &ldquo;keep for sentimental reasons&rdquo;, &ldquo;keep in case I lose weight / change jobs / go to that hypothetical wedding&rdquo;, and &ldquo;forgotten about entirely&rdquo;. A downsizing move is the right moment to thin all three.</p>
<p>The test: turn every hanger backwards in your wardrobe today. Every time you wear an item, hang it back facing forwards. After six weeks, the items still backwards are the candidates for the donate pile. This is harder than it sounds because the &ldquo;I might wear it&rdquo; objection is strong. Be honest.</p>
<p>For very high-value items (designer pieces, vintage couture) the sell pile is worth the effort &mdash; specialist consignment shops in Brighton and London give better returns than eBay. For mid-value items, eBay or local Facebook Marketplace works. For everything else, the local charity shop. Most Sussex charity shops are particularly happy to take winter coats and children&rsquo;s clothing. The <a href=\"how-to-pack-clothes-without-wrinkling.html\">wardrobe-packing guide</a> covers what to do with the keep pile.</p>"""),
            ('Books, paperwork and the digital era',
             """<p>Books are the category where decluttering instincts diverge most sharply. Some people happily donate hundreds of books and never miss them; others can&rsquo;t bear to part with any. The middle ground is usually right: keep the ones you&rsquo;ve genuinely re-read or refer to, plus the ones with sentimental value, and donate the rest to charity shops or to friends.</p>
<p>Paperwork is the same. Old bank statements, utility bills, tax returns going back decades, children&rsquo;s school certificates, expired insurance documents. Most can be safely shredded or digitised. The HMRC retention requirements are 5&ndash;7 years for most personal records; anything older can usually go. Bank statements are available online for current accounts; paper copies aren&rsquo;t needed.</p>
<p>For digital decluttering (the wardrobe of the modern age), do this before the move too &mdash; export old emails, organise photos, back up everything to a cloud service. Moving home is the right moment to also tidy the digital house. Less paperwork to move is straightforward; less digital clutter is even better.</p>"""),
            ('The practical logistics — disposal, donation, sale',
             """<p>For donation: most charity shops accept clean, sellable items by appointment or doorstep collection. Local Sussex charities &mdash; St Wilfrid&rsquo;s Hospice, Demelza, the British Heart Foundation &mdash; have established collection services for furniture and larger items. For smaller items, drop-offs at the local high-street charity shop work fine; pack into labelled bags for easy unloading.</p>
<p>For selling: eBay for collectibles and named-brand items, Facebook Marketplace for local furniture and household goods, Gumtree for cars and bikes, and specialist auction houses for antiques (Brighton and Eastbourne both have auction houses worth knowing about). For very valuable single items, talk to us at <a href=\"moving-antiques-valuable-furniture.html\">antiques moving</a> before listing &mdash; sometimes the better answer is to move and revalue.</p>
<p>For disposal: the council recycling centre (the tip) takes most household waste for free. Hazardous materials (paint, batteries, fluorescent tubes) go through specific recycling streams. Heavy furniture for disposal can be collected by the council (small charge) or by private services. We can recommend a <a href=\"../house-clearance-eastbourne.html\">house clearance service</a> if you&rsquo;ve inherited a property full of contents to deal with.</p>"""),
        ],
        'faqs': [
            ("How early should I start downsizing?",
             "Six weeks ahead is the sweet spot. Two weeks is too little; eight weeks is ideal but rare. Start with the rooms you use least (loft, garage, spare bedroom) and work towards the rooms you use most."),
            ("What's the right test for whether to keep something?",
             "Have I used this in the last 12 months, and would I buy it again today? If both answers are no, the item moves to donate, sell or dispose. The 12-month rule cuts through the 'but I might need it' objection."),
            ("How do I downsize sentimental items?",
             "Keep less of the category, not none. A box of 20 of your child's drawings is more meaningful than two boxes of 200. For items you can't bear to part with but don't want to display, digitise (for photos, letters) or use long-term storage."),
            ("Is it worth selling items rather than donating?",
             "Only if you're genuinely going to photograph, list and post within four weeks. Many 'sell' piles end up sitting unsold for months. Be honest about your time; charity shops always need stock."),
            ("What's the easiest way to dispose of furniture?",
             "Local charity shops collect for free for sellable items. The council tip takes most household waste at no charge. For inherited property full of contents, our house-clearance service handles the entire job."),
        ],
    },

    # ---- Topic 36 ----
    {
        'slug': 'moving-antiques-valuable-furniture.html',
        'title': 'Moving Antiques and Valuable Furniture – How We Protect Them',
        'desc': 'Moving antiques or valuable furniture? Discover how our specialist team safely handles and transports precious items.',
        'kicker': 'Antiques · Period furniture · Specialist handling since 1982',
        'h1': 'Moving Antiques and Valuable Furniture — How We Protect Them',
        'hero_sub': "Tudor oak, French polish, marquetry, marble and the specific protocols that get them across the country intact.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Antiques moving',
        'intro_html': """<p style=\"font-size:1.15rem;\">Antiques and valuable furniture demand a different standard of removal than ordinary household contents. The differences aren&rsquo;t mystical &mdash; they&rsquo;re practical: more careful wrapping, slower handling, specific protection for veneer and marquetry, custom crating for fragile pieces, and crews trained to recognise what they&rsquo;re handling. After forty years of <a href=\"../antiques-moving.html\">antiques moving across Sussex</a> we have a clear and tested approach.</p>
<p>This guide covers what counts as antique, the specific handling methods we use, the insurance considerations, and the survey process. For valuable single pieces or whole collections, our <a href=\"../white-glove-service.html\">white-glove service</a> is the relevant tier. For mixed inventories with some antiques alongside modern furniture, standard pad-wrap plus declared-value insurance is usually sufficient.</p>""",
        'sections': [
            ('What counts as antique — and why it matters',
             """<p>The standard antiques definition is &ldquo;more than 100 years old&rdquo;, but for removal purposes the more useful definition is &ldquo;valuable, irreplaceable or fragile&rdquo;. A solid oak Victorian wardrobe is technically antique but moves like ordinary furniture. A French marquetry escritoire from the same era is far more delicate and needs specialist handling regardless of age.</p>
<p>For survey purposes we treat the following as antique-handling items: anything with marquetry, anything with original gilt or gold leaf, anything with veneer (especially walnut, satinwood or rosewood), anything with marble or stone tops, anything mounted on splayed legs that can splay further, anything in glass-fronted display cabinets, and anything the customer specifically values at over &pound;2,500.</p>
<p>Within that category, the handling escalates with value. Items at &pound;2,500&ndash;&pound;10,000 get pad-wrap plus declared-value insurance. Items at &pound;10,000&ndash;&pound;50,000 typically get white-glove handling. Items above &pound;50,000 usually need a specialist art-and-antiques carrier with climate-controlled transport. We&rsquo;ll talk through the right tier at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> based on what you&rsquo;re moving.</p>"""),
            ('Wrapping methods for antique furniture',
             """<p>Standard <a href=\"how-our-pad-wrap-service-protects-furniture.html\">pad-wrap</a> is fine for many antiques. For more delicate pieces we add internal padding (acid-free tissue between drawers and against veneer surfaces), corner-board over vulnerable corners and edges, and soft-cotton cloth between the blanket and the finish for items with French polish or lacquer (the blanket weave can mark these finishes over a long journey).</p>
<p>For items with original gilt work or applied decoration, we use a tissue-then-cotton-then-blanket layering. The tissue protects against the cotton; the cotton protects against the blanket fibres; the blanket provides the impact cushioning. This sounds excessive until you see a piece arrive after a long journey with no marks at all where ordinary pad-wrap would have left a faint pattern.</p>
<p>For marquetry and inlay work, the rule is no tape on the surface ever. Tape lifts veneer; even &lsquo;painter&rsquo;s tape&rsquo; can lift original 18th-century shellac. All restraint is achieved through webbing straps over the pad-wrap, never adhesive directly on the wood. Mention any tape-applied previous protection at survey so we can replace it before transit.</p>"""),
            ('Glass, mirrors and the &ldquo;face-to-face&rdquo; rule',
             """<p>Glass-fronted antiques (display cabinets, bookcases, china cabinets) are among the highest-risk items in any move. The rule we follow: glass faces glass with padding between, never glass against wood or any other hard surface. The compressive forces in a lorry are vertical; glass surfaces face-to-face cushion each other; glass against wood concentrates force on the glass.</p>
<p>Original Georgian or Regency mirrors and looking-glasses get specific handling. The wooden frame and the glass are surveyed separately at the start &mdash; sometimes the glass is original and irreplaceable, sometimes the glass is a later replacement. Original glass needs custom crating; replacement glass is replaceable. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> about which is which.</p>
<p>For valuable mirrors over &pound;5,000, the standard transit method is bespoke crating with vertical orientation and soft internal padding. For collections of mirrors (a sideboard mirror set, for example), each mirror is crated individually. The crates are reusable and we collect them after the move.</p>"""),
            ('Marble, stone and the weight question',
             """<p>Marble and stone-topped furniture has two operational problems: weight and fragility. A typical marble dining table top weighs 80&ndash;120kg and can chip or crack if dropped, twisted or stacked improperly. The standard rule: marble travels separately from its base, padded vertically, never flat.</p>
<p>For removal, we lift the marble from the base with two crew members minimum, wrap it in heavy bubble plus pad-wrap, and stack it vertically against an interior lorry wall with foam between it and any neighbour. The base of the table is wrapped separately as ordinary furniture. At the new property they&rsquo;re reassembled in the destination room.</p>
<p>For stone fireplaces, garden statuary and outdoor stone ornaments, the principles are the same but the weight is often greater. We use specialist lifting equipment for items over 100kg. For pieces over 250kg we sometimes need a four-person crew or specialist sling equipment &mdash; both flagged at survey. The <a href=\"moving-heavy-awkward-items.html\">moving heavy items guide</a> covers the operational details for the heaviest pieces.</p>"""),
            ('Insurance and the declared-value question',
             """<p>Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers transit damage at typical per-item limits (£2,500 is a common ceiling). For antiques above this limit, items need declaring specifically on the contract before move day. Declared-value coverage is available up to most reasonable amounts; for genuinely high-value pieces (above &pound;25,000), a separate specialist policy is usually the right approach.</p>
<p>Photograph everything before the move. Wide shots of each piece, close-ups of any existing chips or marks, close-ups of any signatures, maker&rsquo;s marks or labels. These photos are invaluable in any post-move insurance discussion and they&rsquo;re also useful to the unpacking crew (you, in a fortnight&rsquo;s time) to know where each piece was originally.</p>
<p>For full collections &mdash; family silver, an art collection, a wine cellar &mdash; we recommend a written inventory before the move. We provide this as part of the <a href=\"../white-glove-service.html\">white-glove service</a>; for self-managed inventories the structure is straightforward (item, photograph, declared value, location at start, location at end). Insurance discussions go significantly better with a written inventory.</p>"""),
            ('The survey, the quote and the crew',
             """<p>Antique surveys take longer than standard surveys &mdash; typically 60&ndash;90 minutes for a property with significant antique content. The surveyor photographs each high-value piece, notes the protection requirements, and discusses any access challenges (narrow stairs, doorways, vehicle constraints &mdash; common in <a href=\"moving-to-listed-building-sussex.html\">listed buildings</a>). The quote follows within 48 hours and itemises the antique-specific work.</p>
<p>The crew assigned to antique-heavy moves is our most experienced team. Trained at our own staff training centre, specifically on antique handling, and selected for jobs where the inventory requires it. This isn&rsquo;t a marketing claim; it&rsquo;s an operational reality &mdash; the same crew that handles a routine 3-bed move isn&rsquo;t necessarily the right team for a country house with significant period content.</p>
<p>Booking lead times for antique moves are similar to standard moves &mdash; 6&ndash;10 weeks for end-of-month dates in the May-to-September peak. For very high-value moves (large country houses, art collections), book 12+ weeks ahead because the survey scheduling and crew assignment is more complex. Talk to us early at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a>.</p>"""),
        ],
        'faqs': [
            ("What counts as an antique for removal purposes?",
             "Practically: anything valuable, irreplaceable or fragile — marquetry, gilt work, veneer, marble or stone tops, glass-fronted cabinets, anything you specifically value at over £2,500. The legal '100 years old' definition is less useful than these handling-relevant categories."),
            ("Is antiques moving more expensive?",
             "Yes — additional protection materials, longer survey, sometimes custom crating, slower handling. We quote each line transparently at survey rather than adding a single 'antiques surcharge'."),
            ("Will my home contents insurance cover antiques in transit?",
             "Usually no — most home policies exclude items in transit. The removal firm's goods-in-transit insurance covers transit damage. For items above standard per-item limits (typically £2,500), declare them on the contract."),
            ("What about pianos and stone fireplaces?",
             "Pianos go via our piano-moving service with specialist trolleys and strapping. Stone fireplaces, garden statuary and large marble pieces use lifting equipment and four-person crews where weight requires it."),
            ("Can you store antiques between completion dates?",
             "Yes — our Lower Dicker depot has climate-stable strong-room storage suitable for high-value contents. For genuinely valuable items, the climate-stable conditions are non-negotiable; uninsulated storage causes damp damage over months."),
        ],
    },

    # ---- Topic 37 ----
    {
        'slug': 'moving-heavy-awkward-items.html',
        'title': 'Moving Heavy or Awkward Items Like Pianos and Safes',
        'desc': 'Need to move a piano, safe, or other difficult items? Learn how our experienced team handles heavy and awkward objects safely.',
        'kicker': 'Pianos · Safes · Stone · The heaviest, the awkwardest, the trickiest',
        'h1': 'Moving Heavy or Awkward Items — Pianos, Safes and the Truly Difficult',
        'hero_sub': "Some items need more than a strong back. Here is how we approach pianos, gun safes, marble worktops and other items that demand specialist handling.",
        'hero_img': 'mark-ratcliffe-crew-loading-piano-eastbourne.webp',
        'breadcrumb': 'Heavy items',
        'intro_html': """<p style=\"font-size:1.15rem;\">Some household items live outside the normal removal-day flow. Pianos, gun safes, garden safes, antique stone fireplaces, full-height bookshelves, gym equipment, ride-on mowers, outdoor hot tubs. They&rsquo;re heavy, awkward, and damage easily &mdash; both themselves and the property if mishandled. After forty years of <a href=\"../about-us.html\">specialist Sussex removals</a> we have specific equipment, methods and crew configurations for each.</p>
<p>This guide covers the most common heavy-item categories we handle, the equipment we use, the survey considerations, and what the customer needs to think about before move day. For pianos specifically we have a dedicated <a href=\"../piano-moving.html\">piano moving service</a>; for antiques and stone the <a href=\"moving-antiques-valuable-furniture.html\">antiques moving guide</a> covers the parallel considerations.</p>""",
        'sections': [
            ('Pianos — uprights, grands and the operational reality',
             """<p>Pianos divide into two main categories for moving: <strong>uprights</strong> (the rectangular floor-standing piano, typically 150&ndash;250kg) and <strong>grands</strong> (the horizontal concert-style piano, typically 250&ndash;500kg). Uprights are the more common household instrument and the easier of the two to move. Grands need disassembly: the legs and the lyre come off, the lid is folded down and strapped, and the body travels on a piano dolly.</p>
<p>Our standard piano move uses a 4-person crew minimum, specialist piano trolleys (heavy-duty wheeled platforms designed for the weight distribution), and pad-wrap blankets. The piano is wrapped in your home, lifted onto the trolley, and rolled or stair-climbed to the lorry. For pianos through narrow doorways, we sometimes hoist via window using a specialist platform &mdash; this is a separate quote item.</p>
<p>For grand pianos, the disassembly happens at the start of the move and the reassembly at the unload. The piano needs to be tuned within a fortnight of arriving at the new property &mdash; we&rsquo;ll recommend a local tuner if you don&rsquo;t already have one. The <a href=\"../piano-moving.html\">piano moving service</a> page covers the full process and the quote structure.</p>"""),
            ('Safes — domestic and commercial',
             """<p>Safes are heavier than they look and more fragile than they appear. A typical domestic gun safe is 80&ndash;200kg; commercial safes can run to 500kg+. The lifting points are usually the corners, but moving by the corners alone can twist the safe and damage the door seal. Specialist safe-moving equipment uses straps that distribute the load across the safe&rsquo;s base.</p>
<p>For domestic safes (gun safes, family safes, fire safes), we use a 2-3 person crew with a steel toe-cap policy and specialist lifting straps. The safe is wrapped in heavy bubble plus pad-wrap, lifted onto a trolley, and rolled to the lorry. At the unload end the process reverses.</p>
<p>For larger commercial safes (5-foot tall and above, weight over 300kg), we sometimes recommend a specialist safe-moving firm rather than handling it ourselves. The right answer depends on the safe size, the access constraints (stairs, doorways) and the value of what&rsquo;s inside. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> and we&rsquo;ll give an honest view.</p>"""),
            ('Stone, marble and architectural salvage',
             """<p>Stone items &mdash; fireplaces, garden statuary, outdoor planters, stone-tiled hearths &mdash; have weight as their primary handling challenge. A typical antique stone fireplace surround weighs 150&ndash;300kg. A large stone garden statue can be 100&ndash;500kg. Stone-topped tables and console units split between the stone (50&ndash;150kg) and the base (much lighter).</p>
<p>For stone items we use a 4-person crew minimum with lifting straps and (for items over 200kg) a specialist sling system. The stone is wrapped in heavy bubble plus pad-wrap and moved on a steel-framed dolly designed for the weight. Stairs add complexity &mdash; we often disassemble stone fireplaces into manageable component pieces if the original construction allows it.</p>
<p>Architectural salvage &mdash; mantelpieces, original radiators, cast-iron baths, wrought-iron gates &mdash; tends to be heavy and irregularly shaped. Each piece is treated individually with custom-fit pad-wrap and bespoke handling. For the most valuable architectural pieces (named-maker mantels, Victorian roll-top baths), our <a href=\"../white-glove-service.html\">white-glove service</a> is the relevant tier.</p>"""),
            ('Gym equipment, ride-on mowers and outdoor kit',
             """<p>Home gym equipment varies enormously in difficulty. A folding bench is easy. A multi-station home gym is a half-day disassembly project followed by a complex reassembly at the other end. Squat racks, weight stacks, treadmills and rowing machines all need methodical disassembly using the original manufacturer&rsquo;s manual where available.</p>
<p>If you still have the assembly manual from the original purchase, this saves significant time at the unload end. Photograph the equipment from multiple angles before disassembly &mdash; the photos are useful for reassembly and for any insurance considerations. Heavy weight plates pack into reinforced cartons of 4&ndash;6 plates each; never overfilled, never stacked too high.</p>
<p>Ride-on mowers and large garden machinery need fuel-drained before transit (the same applies to motorcycles, see <a href=\"what-you-can-and-cannot-store.html\">what you can store</a>). The blade is locked in the up position; the battery is disconnected; the body is pad-wrapped. For ride-on mowers above 200kg we use a ramp and winch system rather than manual lifting.</p>"""),
            ('Hot tubs, garden buildings and the genuinely awkward',
             """<p>Outdoor hot tubs are heavy (200&ndash;400kg empty, much more with water) and need draining 48 hours before move day. The plumbing is disconnected, the electric supply isolated, the cover removed and transported separately. The tub itself is lifted by a 4-person crew onto a flat-bed trolley and moved to the lorry; for very large hot tubs we sometimes use a sub-contracted specialist hot-tub-moving firm.</p>
<p>Garden buildings (sheds, greenhouses, log cabins, summerhouses) are usually too big to transport whole. We disassemble panel-by-panel, label each piece for reassembly, transport flat-pack-style, and reassemble at the new property. This is a specialist job and adds 1&ndash;2 days to the move; budget for it at survey if applicable.</p>
<p>Other awkward categories: full-height bookshelves with built-in fixings (often need disassembly), grandfather clocks (need their pendulum removed and transported separately &mdash; never lay flat), pool tables (the slate top weighs 100&ndash;300kg and needs specialist support during transit). Each of these has its own handling protocol that we&rsquo;ll cover at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a>.</p>"""),
            ('How we quote heavy-item moves',
             """<p>Heavy items are quoted as line items on the main removal quote, not as a separate contract. The line items typically include: crew time (additional crew members for the heavy item), specialist equipment (piano trolley, lifting straps, ramps), additional materials (heavy-duty pad-wrap, bubble, corner-board), and sub-contracted services if needed (specialist safe movers, hot-tub specialists).</p>
<p>The survey is where the heavy-item question gets answered. The surveyor sees the item, measures the access points, considers the routes in and out, and identifies any access constraints. For unusual items (an Edwardian iron range, a vintage car collection, a 19th-century billiard table), the survey may need a second visit with a specialist team member.</p>
<p>Booking timing: 6&ndash;10 weeks ahead is standard, longer if the heavy items need sub-contracted specialist services. For genuinely complex moves involving multiple heavy items (a large country house with pianos, antique fireplaces, marble pieces and outdoor sculpture), book 12&ndash;16 weeks ahead so we have time to coordinate the specialist resources. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> early.</p>"""),
        ],
        'faqs': [
            ("How heavy is too heavy for your crew to handle?",
             "We routinely handle items up to 500kg with a 4-person crew and specialist equipment. Items above 500kg sometimes need specialist sub-contracted services, depending on access constraints. We'll advise at survey."),
            ("Do pianos need re-tuning after a move?",
             "Yes — pianos should be re-tuned within a fortnight of arriving at the new property, regardless of how carefully they're moved. We can recommend a local tuner in your new area if you don't already have one."),
            ("Can you move a hot tub?",
             "Yes for most domestic sizes. It needs draining 48 hours before move day, plumbing and electrics disconnected, cover removed. For very large or specialist commercial hot tubs we sometimes use a sub-contracted specialist firm."),
            ("What about gun safes?",
             "Yes — domestic gun safes are routine for us. Specialist lifting straps, 2-3 person crew, careful handling. Larger commercial safes (300kg+) sometimes need a specialist safe-moving firm; we'll advise."),
            ("Will you disassemble and reassemble gym equipment?",
             "Yes — but it's a real time investment. A multi-station home gym is a half-day each side. Have the original assembly manual ready if you can; it saves significant crew time."),
        ],
    },

    # ---- Topic 38 ----
    {
        'slug': 'moving-fine-art-collectibles.html',
        'title': 'How to Safely Move Fine Art and Valuable Collectibles',
        'desc': 'Moving paintings, sculptures or valuable collections? We explain the specialist care and protection required for fine art and collectibles.',
        'kicker': 'Fine art · Collectibles · Museum-grade handling · Climate transport',
        'h1': 'How to Safely Move Fine Art and Valuable Collectibles',
        'hero_sub': "Paintings, sculptures, ceramics, photography, watches, coins — the items where the difference between a careful move and a careless one is measured in five-figure sums.",
        'hero_img': 'pad-wrapped-furniture-eastbourne-removals.webp',
        'breadcrumb': 'Fine art moving',
        'intro_html': """<p style=\"font-size:1.15rem;\">Fine art and high-value collectibles demand a level of care that ordinary household removal doesn&rsquo;t provide. The financial stakes are higher, the items are usually irreplaceable, and the damage potential from poor handling is measured in years of restoration work rather than minor scratches. After forty years of <a href=\"../about-us.html\">specialist Sussex removals</a> &mdash; including a steady stream of art and antique-collector moves through our <a href=\"../white-glove-service.html\">white-glove service</a> &mdash; we have a clear approach to this category.</p>
<p>This guide covers what counts as &lsquo;fine art&rsquo; for removal purposes, the protection methods we use, the climate considerations, the insurance and provenance paperwork, and the survey process. For genuinely museum-grade single pieces or whole collections we may also coordinate with specialist art-transport firms; the right answer depends on the items.</p>""",
        'sections': [
            ('What counts as fine art for removal',
             """<p>The art-and-collectibles category is broader than people often realise. It includes paintings (oil, watercolour, drawings on paper, prints), sculpture (bronze, marble, ceramic, modern composite), photography (signed editions, originals, large prints), works on paper (etchings, lithographs, signed prints, manuscripts), and a parallel category of high-value collectibles &mdash; watch collections, coin collections, stamp collections, signed sports memorabilia, fine wines, antique jewellery, rare books.</p>
<p>For removal handling, the categorisation we use is: <strong>flat works</strong> (paintings, photographs, framed prints &mdash; transported vertically), <strong>three-dimensional pieces</strong> (sculpture, ceramics, decorative arts &mdash; transported in custom crates), and <strong>collections</strong> (multi-item categories needing inventory, climate control, and security &mdash; coins, watches, wines).</p>
<p>Each category has its own handling protocol. For flat works, the rule is &lsquo;vertical, padded, separated&rsquo;. For three-dimensional, the rule is &lsquo;crated, oriented correctly, padded&rsquo;. For collections, the rule is &lsquo;inventoried, climate-controlled where needed, security-tracked&rsquo;. The detail follows.</p>"""),
            ('Paintings and framed works — the vertical rule',
             """<p>Paintings travel vertically, never flat. Flat transport causes compressive force on the canvas and frame; vertical transport directs forces along the frame structure where it&rsquo;s strong. We use bespoke painting crates &mdash; rigid wooden cases with internal foam padding sized to the specific painting &mdash; for high-value pieces. For mid-value pieces we use stiff cardboard art crates with foam interior.</p>
<p>The frame itself is the protection. We don&rsquo;t put bubble wrap or tissue directly on the painting surface &mdash; the painting&rsquo;s frame and the painting&rsquo;s glass (if framed) protect the paint surface. Around the frame we use heavy bubble wrap (2-3 layers), corner-board on every corner, then the outer crate. The crate is loaded onto the lorry secured upright against an internal lorry wall, never stacked.</p>
<p>For multiple paintings travelling together, we use slot-divider crates that hold 4-8 paintings separated by padded slots. This is more space-efficient and equally safe; ideal for collections of similar-size works. For valuable single pieces, a dedicated crate is the standard. The <a href=\"../white-glove-service.html\">white-glove service</a> includes the bespoke crating as standard.</p>"""),
            ('Sculpture, ceramics and three-dimensional works',
             """<p>Three-dimensional artworks need custom crating because the protection has to fit the irregular shape. We use bespoke wooden crates lined with high-density foam carved to match the specific piece. The foam holds the sculpture immobile in transit; the crate protects against impact. This is genuinely expensive (£100&ndash;£500 per crate depending on size) but it&rsquo;s the only reliable method for irreplaceable items.</p>
<p>Orientation matters. Bronze sculptures with thin extending limbs need the limbs supported during transit; ceramics with hollow construction need internal padding; large modern sculptures sometimes need disassembly into component pieces. Each item is surveyed individually and the right protection is engineered for it.</p>
<p>For very fragile pieces &mdash; original Greek pottery, Tang dynasty ceramics, museum-grade modern glass &mdash; we recommend a specialist art-transport firm rather than handling it ourselves. The customer&rsquo;s standard insurance limits and our standard transit insurance may not cover items at this value level. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> for an honest view.</p>"""),
            ('Climate, humidity and the long-distance question',
             """<p>Fine art is sensitive to humidity and temperature changes. Rapid environmental shifts can cause canvas to slacken, panel paintings to warp, varnish to bloom, and ceramics to crack. For short-distance moves (within a county, less than 2 hours&rsquo; drive) the environmental change is minimal. For longer moves, climate-controlled transport becomes important.</p>
<p>Our standard lorries are insulated but not climate-controlled. For ordinary household contents this is fine; for genuinely valuable art (above &pound;25,000 per piece), we recommend climate-controlled transport. This is usually sub-contracted to a specialist art-transport firm with a temperature- and humidity-monitored vehicle. The cost is meaningful but for the values involved it&rsquo;s appropriate.</p>
<p>For storage between completion dates, climate-stable storage is non-negotiable for art. Our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> is insulated and ventilated; for genuinely valuable collections needing controlled humidity, we coordinate with specialist art-storage providers. The <a href=\"what-you-can-and-cannot-store.html\">storage-rules guide</a> covers the broader storage considerations.</p>"""),
            ('Provenance, paperwork and insurance',
             """<p>For fine art moves, the paperwork side matters as much as the physical handling. Before move day, gather the provenance documents for each piece: purchase records, certificates of authenticity, conservation reports, valuation records, photographic catalogue. These travel with you in your own car, never in the lorry.</p>
<p>Standard <a href=\"../terms-conditions-and-insurance-details.html\">goods-in-transit insurance</a> covers transit damage at typical per-item limits. For art above these limits, declared-value coverage extends the limit; for genuinely high-value pieces, specialist art insurance is the right approach. The Hiscox and AXA Art-Insure policies are the standard UK options.</p>
<p>For very valuable single pieces (above &pound;100,000), the insurance discussion happens before the move quote &mdash; the insurer sometimes specifies the handling method, the transport firm, and the climate conditions. We work with the major UK art insurers regularly; talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> if your collection includes items at this value.</p>"""),
            ('Survey, quote and the white-glove option',
             """<p>Art surveys take longer than standard surveys &mdash; typically 90&ndash;120 minutes for a property with significant art content. We photograph each piece, note the dimensions, identify protection requirements, and discuss any access challenges. The written quote follows within 48 hours and itemises the art-specific work: crating, climate transport, declared-value insurance, specialist crew.</p>
<p>The <a href=\"../white-glove-service.html\">white-glove service</a> is the standard tier for art moves. It includes: bespoke crating for each piece, individual wrapping, photographic inventory, climate-controlled transport for the lorry, dedicated crew with art-handling training, and unwrapping at the destination in the customer&rsquo;s presence. The price is meaningful but for the value of contents it&rsquo;s appropriate.</p>
<p>Booking lead times for art moves are typically longer than standard. For end-of-month dates in the May-to-September peak, book 10&ndash;14 weeks ahead. For very high-value moves (full art collections, museum-grade pieces), 16+ weeks. The lead time covers the crate manufacture (bespoke crates are made-to-measure), the insurance coordination, and the crew scheduling.</p>"""),
        ],
        'faqs': [
            ("Do paintings really need to travel vertically?",
             "Yes — flat transport causes compressive force on the canvas and frame. Vertical transport directs forces along the frame's strong structural lines. This is industry-standard practice for art transport."),
            ("What does climate-controlled transport actually mean?",
             "A vehicle with temperature and humidity monitoring throughout transit, typically maintaining 18–22°C and 45–55% humidity. Standard removal lorries are insulated but not climate-controlled; for genuinely valuable art (above £25,000 per piece) we recommend specialist transport."),
            ("Is our standard insurance enough for fine art?",
             "For pieces below the per-item limit (typically £2,500), yes. Above that, declare items specifically. Above £25,000 per piece, specialist art insurance (Hiscox, AXA Art) is usually the right approach."),
            ("Can you store art between completion dates?",
             "Our Lower Dicker depot is climate-stable and suitable for moderate-value pieces. For genuinely valuable collections needing precise humidity control, we coordinate with specialist art-storage providers."),
            ("How early do I need to book a fine art move?",
             "10–14 weeks ahead for routine art moves; 16+ weeks for full collections needing bespoke crating and specialist insurance coordination. The lead time covers the crate manufacture and insurance setup."),
        ],
    },

    # ---- Topic 39 ----
    {
        'slug': 'office-relocation-minimise-disruption.html',
        'title': 'Office Relocation Guide: How to Move Your Business with Minimal Disruption',
        'desc': 'Planning an office move? Our guide shows businesses how to plan and execute an office relocation with the least amount of downtime.',
        'kicker': 'Office moves · Weekend relocations · Minimal downtime',
        'h1': 'Office Relocation Guide — How to Move Your Business with Minimal Disruption',
        'hero_sub': "Closed Friday, open Monday. Here is how a business-relocation specialist plans an office move so the team is working again before the kettle is on.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Office relocation',
        'intro_html': """<p style=\"font-size:1.15rem;\">An office move is fundamentally different from a house move. The business has to keep running; the IT needs to be up immediately; the team can&rsquo;t be without desks for more than a working day; and the cost of downtime usually dwarfs the cost of the removal itself. After forty years of <a href=\"../office-removals-eastbourne.html\">office relocations across Sussex</a> we have a clear and tested approach.</p>
<p>The principle is straightforward: plan early, run the move over a weekend or after-hours window, prioritise the IT and the immediate workstations, and have a clear day-1 desk-allocation plan. The detail below covers each phase. For the dedicated service page, see <a href=\"../office-removals-eastbourne.html\">office removals Eastbourne</a>; this guide covers the practical planning side.</p>""",
        'sections': [
            ('Plan twelve weeks ahead',
             """<p>The single biggest predictor of an office-move success is the planning lead time. Twelve weeks is the sweet spot for a 20-100 person office. Less than that is doable but cramped; more than that is sometimes necessary for larger operations (200+ desks, multiple sites, complex IT infrastructure).</p>
<p>The first four weeks: lease signed at the new property, IT survey of both buildings, broadband and phone-line orders placed (Openreach engineer appointments routinely run 4&ndash;6 weeks out in East Sussex), interior fit-out scheduled if needed. The next four weeks: furniture inventory, desk allocation plan, employee communications, packing materials ordered. The final four weeks: pack the non-essential areas, finalise the IT plan, confirm the move-day timeline with us.</p>
<p>Book the <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> in week 1 of the plan. The surveyor measures both properties, photographs access points, counts desks and furniture by type, and discusses the move-day schedule. The written quote follows within 48 hours and itemises by phase &mdash; packing, transit, unloading, setup at the new property.</p>"""),
            ('Run the move outside business hours',
             """<p>The standard office-move pattern is Friday-evening-through-Monday-morning. The business closes Friday at normal close, our crew arrives Friday at 5pm and works through to early morning Saturday packing and loading. Saturday is the lorry transit and the new-property setup; Sunday is for final placement, IT installation and testing; Monday morning the team arrives at functional workstations.</p>
<p>For smaller offices (under 15 people), the move can sometimes happen in a single evening &mdash; closed at 5pm, fully moved by midnight, open at the new property by 8am the next morning. For larger offices (100+ desks), a full weekend is the minimum; some moves run across a long bank-holiday weekend.</p>
<p>The Friday evening start matters because it gives the business a full weekend buffer if anything overruns. The Monday open is the deadline; the work happens earlier. We&rsquo;ve never missed a Monday morning office reopening across the moves we&rsquo;ve done; the planning buffer is the reason.</p>"""),
            ('IT — the make-or-break category',
             """<p>The IT is the highest-stakes single category in any office move. Servers, networking equipment, phones, workstations, printers, and the cabling that connects them. If the IT isn&rsquo;t working Monday morning, the business isn&rsquo;t working.</p>
<p>The IT plan starts six weeks ahead. The new property is surveyed for cable runs, network sockets, server-room conditions, and power supply. The internal IT team or external IT consultant maps each workstation to its new location with specific port allocations. Cable management plans are drawn up. The disconnection and reconnection schedule is agreed.</p>
<p>On move day, the IT runs ahead of the desk layout. Servers and networking equipment are moved first (sometimes overnight on the Thursday before the main move to give a full day to verify connectivity). Workstations follow on Friday/Saturday. By Sunday afternoon every workstation should be powered, networked, and showing the login screen. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> about coordinating with your IT team.</p>"""),
            ('Desk allocation, signage and the team experience',
             """<p>The team arriving Monday morning shouldn&rsquo;t need to ask where they&rsquo;re sitting. Each desk should be labelled with the team member&rsquo;s name. Each office, meeting room and quiet space should be signposted. The toilets, the kitchen, the printer, the post pigeonholes &mdash; all signposted clearly for the first week.</p>
<p>Before move day, share a floor plan with the team showing their new desk locations. The first morning is much calmer when everyone knows where they&rsquo;re heading. For larger teams, an informal welcome event in the new kitchen on the first Monday morning is worth the small cost &mdash; coffee, pastries, a moment to acknowledge the change.</p>
<p>Personal items on desks &mdash; family photos, plants, mugs, headphones &mdash; should be packed by each individual on Friday afternoon. Provide labelled storage boxes a week ahead and ask each team member to pack their own. This is the practical and respectful approach; the alternative (our crew packing personal belongings) is operationally slower and culturally awkward.</p>"""),
            ('Furniture, storage and the new-fit-out questions',
             """<p>Many office moves involve some furniture replacement &mdash; new desks for a growing team, ergonomic chairs replacing the older fleet, new meeting-room kit. Coordinate the new furniture deliveries with the move day. New furniture typically arrives Friday afternoon or Saturday morning; old furniture is removed at the same time.</p>
<p>Items going into storage rather than the new property &mdash; sometimes an office reduces in size or moves to a smaller layout &mdash; go to our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> directly from the old property. Long-term commercial storage works the same as residential: climate-stable strong-room or self-access self-storage depending on the access needs.</p>
<p>For specialist office equipment &mdash; safes, secure document storage, large printers, server racks &mdash; the same protocols apply as in the <a href=\"moving-heavy-awkward-items.html\">heavy items guide</a>. The crew assigned to office moves includes specialists trained on commercial equipment.</p>"""),
            ('The first week in the new office',
             """<p>The first week at the new property is when small issues surface. A meeting-room phone that won&rsquo;t connect. A printer that needs new IP-address mapping. A team member whose desk is in the wrong place because of a last-minute swap. Build in a project manager for the first week whose job is to log and resolve these issues quickly.</p>
<p>The IT issues usually concentrate in week 1 day 2&ndash;3. By then the volume of usage has hit the new network and any latent issues show up. Schedule the IT team to be on-site or fully available for the first three working days. For complex networks (multiple servers, VPNs, specialist software), week 1 is the testing period.</p>
<p>By the end of week 1, the new office should feel normal. Snags filed and either resolved or scheduled; signage adjusted based on usage patterns; meeting rooms booked normally; the team operating without daily reference to the move. The longest-tail item is usually the post and parcel re-direction &mdash; set up Royal Mail business re-direct for 12 months and confirm the new address with all major suppliers and customers in week 1.</p>"""),
        ],
        'faqs': [
            ("How long does an office move take?",
             "Smaller offices (under 15 people) can move in a single evening. 20–100 person offices typically take a weekend (Friday evening through Monday morning). Larger 100+ desk operations run across a long weekend or staged across two weekends."),
            ("When should we book the move?",
             "Twelve weeks ahead is the sweet spot. Less than eight weeks is doable but cramped; more is needed for larger operations or complex IT infrastructure."),
            ("Do you handle the IT disconnection and reconnection?",
             "We coordinate with your IT team but don't typically handle disconnection of server-room equipment. We move the physical hardware; your IT team handles configuration and cabling. We're happy to introduce IT specialist firms if you don't have one."),
            ("Can the business stay open during the move?",
             "The move-day window is closed-to-the-business. Most moves run Friday evening through Sunday so Monday-morning reopening works. For 24/7 operations we sometimes use a phased approach — half the office moves one weekend, the other half the following weekend."),
            ("How does the cost compare to residential moves?",
             "Office moves are typically priced by floor area and inventory rather than house bedrooms. A 20-person office is roughly equivalent to a large 5-bed residential move. Talk to us at survey for a detailed itemised quote."),
        ],
    },

    # ---- Topic 40 ----
    {
        'slug': 'moving-pub-or-restaurant.html',
        'title': "Moving a Pub or Restaurant – What You Need to Know",
        'desc': "Moving licensed premises? Learn the specific challenges and requirements when moving a pub, bar, or restaurant.",
        'kicker': 'Licensed premises moves · Pubs, bars, restaurants · Specialist coordination',
        'h1': 'Moving a Pub or Restaurant — What You Need to Know',
        'hero_sub': "Licensed premises moves are part-residential, part-commercial, part-asset-transfer. Here is the playbook for getting the new place open as quickly as possible.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Pub and restaurant moves',
        'intro_html': """<p style=\"font-size:1.15rem;\">Moving a pub, bar or restaurant is one of the more specialised relocation jobs we do. The premises are part residential (often a publican&rsquo;s flat above), part commercial (kitchen, cellar, bar, dining area), and the legal layer of licensing, food-safety and trading-standards adds complications no ordinary office move involves. After forty years of <a href=\"../about-us.html\">specialist Sussex removals</a> we&rsquo;ve handled the full range &mdash; village pubs changing hands, restaurants expanding to new sites, brewery-tied freeholds moving operators.</p>
<p>This guide walks through the licensing and admin lead-times, the physical-move considerations (cellar equipment, kitchen kit, bar furniture, dining layout), and the practical &lsquo;new place opens fast&rsquo; logistics. For very specialist installations (commercial brewing equipment, walk-in cold rooms, fixed banquet seating) we sometimes coordinate with specialist trades; this guide covers what we handle ourselves.</p>""",
        'sections': [
            ('Licensing lead time — start months ahead',
             """<p>The legal lead-time for moving a licensed premises far exceeds the lead-time of the physical move. A new premises licence for the new property typically takes 6&ndash;12 weeks to issue (longer if the local council is busy or if neighbours object). A premises licence transfer from an existing tenant is faster (usually 2&ndash;4 weeks) but still requires planning.</p>
<p>The Personal Licence (the operator&rsquo;s qualification) doesn&rsquo;t change with the move but the Designated Premises Supervisor on the licence may need updating. If the premises supervisor is changing too &mdash; common when an operator buys a second site or when a chef-owner takes over a pub &mdash; the transfer paperwork runs in parallel.</p>
<p>Food hygiene registration with the new local council is separate from the licensing process and runs on its own timeline. Most councils require 28 days&rsquo; notice before opening; some require an inspection before trading. Confirm with the new council&rsquo;s environmental health team at least 6 weeks before move day. The <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> covers the wider admin sequence.</p>"""),
            ('Cellar equipment, brewery contracts and the beer transfer',
             """<p>The cellar is the highest-stakes single area in any pub move. Beer lines, coolers, gas regulators, cellar cooling units, and the live stock itself (kegs, casks, bottles) all need careful handling. If the move is between brewery-tied properties, the brewery&rsquo;s engineering team usually disconnects and reconnects the lines. For free-house moves, an independent cellar-services firm handles it.</p>
<p>The beer stock is rarely transported in our lorry. Kegs and casks travel via the brewery&rsquo;s own logistics or are returned to the brewery and replaced at the new site. Cask ale in particular is condition-sensitive and won&rsquo;t survive a standard removal transit. Wine and spirit stock can travel via standard removal but in climate-controlled conditions for higher-end bottles &mdash; talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a>.</p>
<p>Cellar equipment &mdash; the cooling units, gas regulators, line-cleaning kit, glassware washers &mdash; usually transfers with the premises rather than the operator (it&rsquo;s often landlord/brewery property). Confirm the asset list with the freeholder before move day so there&rsquo;s no confusion about what stays and what goes.</p>"""),
            ('Kitchen equipment — gas, water, ventilation',
             """<p>Commercial kitchens have their own move-day complications. Gas-powered ranges and ovens need disconnection by a Gas Safe registered engineer (the same regulations as domestic but with stricter commercial-installation rules). Water-fed equipment (commercial dishwashers, ice machines, combi ovens) needs water-line disconnection and reconnection &mdash; usually by a commercial plumbing firm.</p>
<p>Extraction ventilation in a commercial kitchen is fixed plant rather than removable equipment &mdash; the ventilation system stays with the building. If the new premises has different ventilation specifications, the kitchen equipment may need to be reconfigured. This is sometimes the biggest single capital expense of the move.</p>
<p>Cold rooms, walk-in fridges and freezers are similarly fixed plant in most cases. If the new premises has equivalent installations, the move is just contents. If it doesn&rsquo;t, new installations need commissioning before opening &mdash; another 4&ndash;6 week lead time. Plan around this constraint, not against it.</p>"""),
            ('Bar furniture, glassware and the dining-room kit',
             """<p>The bar itself is usually fixed to the floor and stays with the property. The bar stock (glassware, bottles, spirits) moves with the operator. We pack glassware using the same techniques as <a href=\"how-to-pack-fragile-items.html\">fragile household items</a> &mdash; vertical stacking, internal tissue, divider-insert cartons. Glassware breakage on a careful pack is typically under 1%.</p>
<p>The dining-room kit &mdash; tables, chairs, sideboards, table linen, cutlery, plates &mdash; moves like ordinary commercial furniture. We pad-wrap each piece (see the <a href=\"how-our-pad-wrap-service-protects-furniture.html\">pad-wrap method</a>), pack the cutlery and china in removal-grade cartons, and load systematically. For higher-end restaurants with bespoke furniture (one-off banquettes, signature tables), the same antique-handling protocols apply as in the <a href=\"moving-antiques-valuable-furniture.html\">antiques moving guide</a>.</p>
<p>For collections of glassware, fine wines or other valuable bar stock, declared-value insurance covers them in transit. The <a href=\"../terms-conditions-and-insurance-details.html\">terms and insurance page</a> covers the limits; for collections above the standard per-item limit, specialist coverage is the right approach.</p>"""),
            ('The publican&rsquo;s flat — the residential side',
             """<p>Most pub moves include a publican&rsquo;s flat above the trading floor. This is a residential move running alongside the commercial one. We handle both as a single coordinated job: the flat contents move on the same day as the commercial fit-out, often with two separate lorries (one for residential, one for commercial) to keep things organised.</p>
<p>The residential side follows the same protocols as any house move &mdash; pad-wrapped furniture, packed cartons, the works. The packing-order and the survival-kit advice in our <a href=\"what-to-pack-first-when-moving-house.html\">packing-order guide</a> and <a href=\"moving-day-survival-kit.html\">survival kit guide</a> apply normally. The difference is the timing pressure: the publican needs to be operational at the new site within days of move day.</p>
<p>For families with children, the residential side gets more complex. The <a href=\"moving-house-with-children.html\">moving-with-children guide</a> covers the family logistics. For families with pets, the <a href=\"moving-house-with-pets.html\">moving-with-pets guide</a> applies. Pub-owning families often have both, plus a kitchen open the next day &mdash; a particularly demanding combination that benefits from extra planning lead time.</p>"""),
            ('Opening the new place — the first weeks',
             """<p>The fastest realistic opening time for a moved pub or restaurant is typically 7&ndash;10 days after move day. That covers physical setup, council inspections, licensing checks, staff briefings on the new layout, supplier deliveries, and a soft-launch period. Trying to open faster usually leads to problems with environmental health or the licensing authority.</p>
<p>For pubs in particular, the &lsquo;tied-house&rsquo; relationship matters. Brewery suppliers need to be coordinated for the first deliveries to the new site; some brewery contracts have minimum stock obligations at opening. Pubs moving between brewery groups need particular care &mdash; one brewery&rsquo;s account closes, another opens, and the changeover usually involves stock movement that needs separate logistics.</p>
<p>Staff &mdash; whether retained from the previous operator or new hires &mdash; need briefing on the new building before opening day. Front-of-house staff need to know the table layout; kitchen staff need to know the equipment locations and the food-safety designations of each preparation area. A half-day pre-opening rehearsal saves a chaotic first service. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> about scheduling the move to allow for this preparation week.</p>"""),
        ],
        'faqs': [
            ("How long do I need for the licensing process?",
             "New premises licence: 6–12 weeks. Premises licence transfer: 2–4 weeks. Food hygiene registration: usually 28 days' notice to the new council. Start the paperwork 12+ weeks ahead of move day."),
            ("Does my brewery contract transfer with the move?",
             "Tied-house contracts usually transfer with the property, not the operator. If you're moving between brewery groups, the contractual changeover runs in parallel with the move. Confirm the asset list with the freeholder before move day."),
            ("Will you handle the cellar equipment?",
             "We move the cellar contents (kegs in some cases, glassware, bar stock). The line-disconnection and cellar-cooling equipment usually transfers via the brewery's own engineering team or an independent cellar-services firm."),
            ("How quickly can the new pub open after the move?",
             "Realistically 7–10 days. That covers physical setup, council inspections, licensing checks, staff briefings, supplier deliveries and a soft launch. Trying to open faster usually causes regulatory issues."),
            ("Do you handle the publican's flat alongside the commercial move?",
             "Yes — both as a single coordinated job, usually with two lorries (one residential, one commercial). The residential side follows standard house-move protocols; the commercial side has the licensing and equipment considerations on top."),
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
        <li><a href="../office-removals-eastbourne.html">Office removals</a></li>
        <li><a href="../removals-eastbourne.html">Removals in Eastbourne</a></li>
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
  <link href="../css/normalize.css?v=20260549" rel="stylesheet">
  <link href="../css/components.css?v=20260549" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260549" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260549" rel="stylesheet">
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
  <script defer src="../js/nofollow-shim.js?v=20260549"></script>
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

n = 0
for blog in BLOGS:
    out_path = os.path.join('blog', blog['slug'])
    open(out_path, 'w', encoding='utf-8').write(render_blog(blog))
    n += 1
    print(f'  wrote {out_path}')
print(f'\nCreated {n} new blog posts.')
