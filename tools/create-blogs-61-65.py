#!/usr/bin/env python3
"""Generate blog posts 61-65."""
from __future__ import annotations
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TEMPLATE_PATH = 'blog/cost-of-moving-house-sussex-2026.html'

BLOGS = [
    # ---- 61 — alternative Christmas angle ----
    {
        'slug': 'moving-house-at-christmas-worth-it.html',
        'title': 'Moving House at Christmas – Is It Worth It?',
        'desc': 'Thinking about moving house over the festive period? We explain the pros, cons, and what you really need to consider before booking a Christmas move.',
        'kicker': 'Christmas moves · Pros, cons, the honest answer',
        'h1': 'Moving House at Christmas — Is It Worth It?',
        'hero_sub': "The pros, the cons, and the honest answer from a removal firm that has handled forty years of festive-period moves.",
        'hero_img': 'mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'breadcrumb': 'Is a Christmas move worth it?',
        'intro_html': """<p style=\"font-size:1.15rem;\">Most house moves cluster between May and September. The festive period &mdash; mid-December to early January &mdash; sees only a small fraction of the annual volume, and the question of whether to move during it is a real one for the small minority of households where the timing lands. After forty years of <a href=\"../about-us.html\">Sussex removals</a> we&rsquo;ve handled plenty of Christmas moves; this guide is the honest cost-benefit analysis.</p>
<p>The framing is straightforward. For some households a Christmas move is the only realistic option (the property chain dictates it). For others it&rsquo;s a deliberate choice (lower removals demand, quieter conveyancing market, certain tax considerations). For most households it&rsquo;s simply something to avoid if possible. The detail below walks through which category you&rsquo;re likely to fall into.</p>""",
        'sections': [
            ('The pros — what genuinely works about a Christmas move',
             """<p>Three genuine pros for festive-period moves. First, <strong>diary availability</strong>. The removals industry is at its quietest from December 22nd through January 5th &mdash; the slots that don&rsquo;t exist in July are easily available in December. For customers who need a specific date, the festive period is the easiest time of year to book.</p>
<p>Second, <strong>pricing</strong>. Most reputable removal firms (including us) don&rsquo;t charge a festive premium for ordinary working days. Pricing matches winter rates, which run 10&ndash;15% below summer peak. Bank-holiday day work is the exception &mdash; if you genuinely need the lorry on December 25th itself (which essentially never happens for property completions), that&rsquo;s a premium because the crew is on holiday pay.</p>
<p>Third, <strong>conveyancing predictability</strong>. The legal end of property transactions is at its quietest in the festive period. Solicitors who&rsquo;ve cleared their year-end backlog operate at slower pace; the completion-day chain delays that plague summer moves are rarer because there are fewer transactions competing for the same banking-day windows. For the customers who actually complete in late December, the experience can be unusually smooth.</p>"""),
            ('The cons — and these are real',
             """<p>The cons are real enough that we usually steer customers away from Christmas moves where they have flexibility. <strong>Bank holidays interrupt the working week.</strong> Christmas Day, Boxing Day, New Year&rsquo;s Day &mdash; banks closed, conveyancers closed, no funds-release possible. The available completion days vary year-to-year depending on which day of the week the holidays fall.</p>
<p><strong>Family commitments compete with the move.</strong> Christmas Day, school holidays, family visits, religious observances, the children&rsquo;s expectations of a normal Christmas. Layering a house move on top of all this is genuinely demanding for everyone in the household. For families with younger children, the impact on the child&rsquo;s Christmas can be meaningful.</p>
<p><strong>Weather is unpredictable.</strong> British December weather ranges from mild and damp to genuinely cold and icy. Snow, ice, fog &mdash; all possibilities that can delay or complicate a move. We work in most weathers (the <a href=\"moving-house-in-winter.html\">winter moving guide</a> covers the operational details), but the variability adds stress that summer moves don&rsquo;t carry.</p>"""),
            ('When a Christmas move is genuinely the right answer',
             """<p>Three scenarios where Christmas moves are genuinely the right choice. <strong>The property chain forces it.</strong> The most common scenario &mdash; the buyer&rsquo;s solicitor pushed for December 22nd completion, the seller agreed, the chain locked the date. The move happens because the alternative is to lose the property.</p>
<p><strong>Year-end tax planning.</strong> Some property transactions are timed around the December 31st cut-off for capital-gains reliefs, the start of a new tax year for ongoing rental income, or other tax considerations. The exact calculations are between the customer and their accountant; from our side the move is just another date.</p>
<p><strong>Personal circumstances align.</strong> Between jobs, sabbatical, retirement, downsizing without children at home &mdash; some households have unusual flexibility in December and use it deliberately. For these customers the quieter diary and lower stress level of the festive period actually make it a better choice than the summer peak.</p>"""),
            ('When to definitely avoid a Christmas move',
             """<p>Three scenarios where we&rsquo;d recommend rescheduling if at all possible. <strong>Families with school-age children</strong> &mdash; the Christmas break is short, the children&rsquo;s expectations of a normal Christmas matter, the school transition (if there is one) is harder to manage. The <a href=\"moving-during-school-holidays.html\">school-holiday moves guide</a> covers the alternative windows.</p>
<p><strong>First-time buyers and inexperienced movers.</strong> The festive period adds operational complexity (bank-holiday interruptions, weather, family commitments) that experienced movers can absorb but that first-timers find overwhelming. For first house moves, a quieter spring or autumn window is significantly easier.</p>
<p><strong>Households with elderly relatives or vulnerable members.</strong> The combined stress of Christmas plus a house move plus winter weather lands particularly hard on older household members. The case for waiting until February or March, or even moving in November before the festive period begins, is strong for these households.</p>"""),
            ('Practical planning for a Christmas move',
             """<p>If the move is happening, planning matters more than usual. Book the removal firm 10&ndash;12 weeks ahead (early October at minimum) &mdash; the few available December slots fill quickly. Confirm the exact completion date with your conveyancer at least 4 weeks ahead; bank-holiday-aware date confirmation is non-negotiable.</p>
<p>For the festive logistics, plan the Christmas Day arrangements first and the move second. If the move date is December 22nd or 23rd, the family is essentially hosting Christmas in a half-unpacked house. Pre-book a Christmas Day takeaway near the new property. Set a low bar for &ldquo;unpacked enough&rdquo;. Accept that the first Christmas in the new place may not look like a magazine spread.</p>
<p>For our specific service, the <a href=\"../full-packing-service.html\">full packing service</a> is the time-saver of choice for festive-period moves. The crew packs the house the day before; the customer manages the family schedule. For storage between completion dates (common for festive moves where the new property completes in early January after a late-December sale), our <a href=\"../storage-eastbourne.html\">Lower Dicker depot</a> handles short-term holding without difficulty.</p>"""),
            ('The honest bottom-line answer',
             """<p>For most households with flexibility, the answer to &ldquo;should we move at Christmas?&rdquo; is no &mdash; pick November or January-onwards instead. The combined family-and-festive stress isn&rsquo;t worth the diary availability and the modest pricing advantage.</p>
<p>For households without flexibility (chain-dictated dates, tax timing, personal circumstances) the answer is &ldquo;yes, with the right planning&rdquo;. The move is genuinely doable; the festive-period removals work we&rsquo;ve done over decades is a small but routine part of our diary. The reputation for &ldquo;Christmas moves are a disaster&rdquo; comes from poorly-planned ones, not the well-planned ones.</p>
<p>Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey stage</a> and we&rsquo;ll give an honest view based on your specific situation. The full operational detail is in the <a href=\"moving-over-christmas-and-new-year.html\">Christmas-and-New-Year moves guide</a>; this guide covers the decision rather than the operational logistics.</p>"""),
        ],
        'faqs': [
            ("Is a Christmas move actually cheaper?",
             "Marginally — 10–15% below summer peak. The crew rates are the same; the saving comes from the quieter winter demand pattern. Bank-holiday day work itself (rare) is a premium because the crew is on holiday pay."),
            ("Can we move on Christmas Eve?",
             "Yes, if a working banking day. December 24th is often a half-day for solicitors so funds-release windows are tight. Confirm with your conveyancer at least 4 weeks ahead."),
            ("What's the biggest reason to avoid a Christmas move?",
             "Family commitments. The combined stress of Christmas plus a house move plus a short post-move window before school restarts is genuinely demanding. For families with flexibility, pick November or January-onwards."),
            ("Can you actually fit us in over Christmas?",
             "Usually yes for short-notice. The festive-period diary is the easiest of the year to book into, particularly for mid-week dates between the bank holidays."),
            ("Is the new house going to be cold?",
             "Often yes — empty houses don't warm up quickly. Schedule the heating to come on a day before move day if possible. The winter moving guide covers the cold-weather operational details."),
        ],
    },

    # ---- 62 — Spring cleaning (NEW topic) ----
    {
        'slug': 'spring-cleaning-before-moving-house.html',
        'title': 'Spring Cleaning Before Moving House – A Complete Guide',
        'desc': "Moving in spring? Here's how to combine your spring clean with your house move to make packing much easier and faster.",
        'kicker': 'Spring cleaning · Move-day combined · The double-saving approach',
        'h1': 'Spring Cleaning Before Moving House — A Complete Guide',
        'hero_sub': "Spring is the right time for both. Here is how to combine the annual deep clean with the move so neither becomes a separate job.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Spring cleaning before moving',
        'intro_html': """<p style=\"font-size:1.15rem;\">Spring is the second-busiest removal season after summer &mdash; April and May see roughly 20% of the annual move volume, much of it driven by families wanting to be settled in the new house before the school summer holidays. It&rsquo;s also the traditional spring-cleaning season for British households. After forty years of <a href=\"../about-us.html\">Sussex moves</a> we&rsquo;ve consistently seen customers benefit from combining the two: the spring clean becomes the start of the move-day declutter, and the move becomes the end of the spring clean.</p>
<p>This guide walks through how to do it. The principle: clean as you pack rather than separately, declutter as you clean, and use the move date as the deadline that drives the whole exercise. The detail below covers the room-by-room sequence, the materials, and the timing alongside the broader <a href=\"how-to-prepare-for-your-house-move.html\">8-week preparation plan</a>.</p>""",
        'sections': [
            ('Why spring cleaning and moving combine well',
             """<p>Three reasons the combination works. <strong>The clutter ends up where the cleaning needs doing.</strong> Lofts, garages, sheds, the under-stair cupboards &mdash; these are the same places spring cleaning targets and the same places that need decluttering before a move. Doing both at once means you handle the contents once, not twice.</p>
<p><strong>The cleaning standard for end-of-tenancy or sale matches the spring-cleaning standard.</strong> If you&rsquo;re renting and need to return the property to deposit-return condition, the standard is essentially &ldquo;spring-cleaned&rdquo;. If you&rsquo;re selling and want to leave the property well for the new owner, the goodwill standard is the same. The cleaning happens once and serves both purposes.</p>
<p><strong>Spring weather makes the practical work easier.</strong> Open windows for airing rooms, longer daylight for working through cupboards, the garden in usable condition for sorting outdoor contents. None of this is true in November or January. For families who move in spring, the season actively helps.</p>"""),
            ('The combined approach — clean as you pack',
             """<p>The standard packing approach is room-by-room from the rooms used least to the rooms used most. The combined cleaning-and-packing approach overlays this: clean each room as you pack it. The carton-by-carton work and the clean-by-clean work happen together.</p>
<p>For each room: clear surfaces (decide what to pack, what to donate, what to dispose), pack the cartons, then deep-clean the empty surfaces. By move day the property is clean and packed simultaneously. The alternative &mdash; pack one weekend, clean another &mdash; takes more weekends and feels heavier overall.</p>
<p>The exception is the kitchen and bathroom, which can&rsquo;t be done early because you need to use them. Clean these in the final 48 hours before move day, in the order described in the <a href=\"how-to-clean-old-house-before-moving.html\">cleaning guide</a>. The other rooms get the combined treatment in the weeks running up to move day.</p>"""),
            ('The loft, garage and outdoor categories',
             """<p>Spring is the right season to tackle the outdoor and storage categories that get put off all year. The loft, the garage, the shed, the greenhouse, the BBQ-storage area &mdash; all benefit from longer daylight and warmer weather for the actual physical work.</p>
<p>The pattern: pull everything out of the loft/garage/shed onto a tarp on the lawn, sort into the four piles (keep, donate, sell, dispose), pack the keep pile into removal-grade cartons, drop the donate pile to local Sussex charities, list the sell pile online, schedule a tip run for the dispose pile. Two weekends typically clears the average loft.</p>
<p>For the dispose category specifically, spring is when local councils run additional bulky-waste collection days and recycling-centre slots are easier to book. Most East Sussex councils take garden waste, large furniture, and most household categories at the recycling centre at no charge; specific items (paint, batteries, hazardous chemicals) have separate streams. The <a href=\"how-to-downsize-before-moving.html\">downsizing guide</a> covers the broader disposal logistics.</p>"""),
            ('Materials and equipment for the combined approach',
             """<p>For a typical 3-bedroom home doing the combined exercise, the materials list is straightforward. <strong>Packing materials</strong>: 80&ndash;150 cartons of mixed size, vinyl packing tape, bubble wrap, packing tissue. We stock these at our <a href=\"../packaging-shop.html\">Lower Dicker packaging shop</a> in kits sized for 1-bed up to 5-bed homes.</p>
<p><strong>Cleaning materials</strong>: glass cleaner, bathroom limescale remover, oven cleaner (the heavy-duty kind for end-of-tenancy work), wood-floor cleaner, carpet shampoo if you have carpets, plus the basics (cloths, sponges, gloves, bin liners). Most households have some of this; bulk-up the categories that aren&rsquo;t standard.</p>
<p><strong>Disposal kit</strong>: heavy-duty bin liners for tip runs, a wheelbarrow or trolley for moving heavy items to the car for the tip, and (if you have a substantial garden) a green-waste subscription with the local council for the spring growth that won&rsquo;t fit the regular bin. Most of this is one-off purchase rather than ongoing cost.</p>"""),
            ('Timing — fitting it all into the 8-week plan',
             """<p>For an April or May move, the spring-cleaning-plus-move work distributes across the 8-week preparation window. <strong>Weeks 1&ndash;2 (8 weeks before)</strong>: book the removal firm, plan the room-by-room sequence, gather materials. <strong>Weeks 3&ndash;5 (5&ndash;7 weeks before)</strong>: tackle the loft, garage, shed and outdoor categories &mdash; clean and declutter together.</p>
<p><strong>Weeks 5&ndash;7 (1&ndash;3 weeks before)</strong>: the medium-use rooms (spare bedrooms, dining room, living room, home office). Clean as you pack. <strong>Final week</strong>: the daily-use rooms (kitchen, bathrooms, master bedroom) get cleaned and packed in the last 48 hours. <strong>Move day</strong>: final sweep of the empty property after the lorry leaves.</p>
<p>For tighter timelines (3&ndash;5 weeks rather than 8), compress proportionally. The <a href=\"how-to-organise-move-when-busy.html\">time-pressured moves guide</a> covers the triage approach. For very compressed moves, the cleaning side benefits from a professional one-off end-of-tenancy clean (&pound;100&ndash;&pound;200) rather than DIY.</p>"""),
            ('Specific spring-cleaning targets the rest of the year misses',
             """<p>Five categories that spring-clean specifically and a move-out particularly benefits from. <strong>Windows from outside.</strong> Most households clean windows from inside only; the outside gets neglected. A garden hose plus glass cleaner plus a squeegee handles the exterior in an hour for a 3-bed.</p>
<p><strong>Gutters and downpipes.</strong> Sussex winters dump leaves into gutters; spring is the right time to clear them. A ladder, gloves, a bin bag, and an hour of careful work. For two-storey houses, consider a one-off gutter-cleaning service (&pound;50&ndash;&pound;100) rather than the ladder work.</p>
<p><strong>Behind heavy furniture.</strong> The space behind the wardrobes, sideboards and bookshelves has been collecting dust for years. The move-out is the natural moment to access it.</p>
<p><strong>The garden shed and greenhouse interior.</strong> Both accumulate dust, cobwebs and spider colonies. Spring clean while the contents are pulled out for the move declutter.</p>
<p><strong>Patio and driveway pressure-washing.</strong> The exterior hardstanding looks dramatically better after a one-day pressure-wash. For owner-moves, this is the visible-from-the-road impression that the new buyer arrives to. For tenancy-end moves, it&rsquo;s part of the deposit-return goodwill effort. Hire a pressure-washer for a day for &pound;30&ndash;&pound;60, or buy one if you&rsquo;ll use it more than annually.</p>"""),
        ],
        'faqs': [
            ("Is spring genuinely a better time to move than summer?",
             "Easier weather, longer daylight, better for combining the spring clean. Diary is busier than winter but quieter than the August peak. For families wanting to settle before summer holidays, April-May is the natural window."),
            ("How do I know what to keep vs donate during the combined exercise?",
             "Have I used this in the last 12 months, and would I buy it again today? Both no = donate, sell or dispose. The downsizing guide covers the broader method."),
            ("Should I pay for a professional spring clean or DIY?",
             "DIY for owner-moves with goodwill standard. Professional clean (£100–£200) for end-of-tenancy where the deposit is at stake. The combination of move and clean compresses the timeline; professional help is often worth it."),
            ("Will my removal lorry take the disposal-pile items to the tip?",
             "No — we move household goods only, not waste. Plan a separate tip run before move day, or hire a private waste-removal service. Most East Sussex councils offer bulky-waste collection at modest cost."),
            ("How early should I start?",
             "Six to eight weeks ahead for a calm pace. Three to five weeks for a compressed timeline. Less than that and the case for hiring professional cleaning help becomes much stronger."),
        ],
    },

    # ---- 63 — alternative school-holiday angle ----
    {
        'slug': 'moving-during-school-holidays-pros-cons.html',
        'title': 'Moving During School Holidays: Should You Do It?',
        'desc': "Weighing up the pros and cons of moving during school holidays? Our guide helps you decide if it's the right choice for your family.",
        'kicker': 'School holidays · Family decision · The cost-benefit',
        'h1': 'Moving During School Holidays — Should You Do It?',
        'hero_sub': "An honest cost-benefit analysis of timing a family move around the school calendar. Sometimes it works, sometimes it doesn't.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'School-holiday move decision',
        'intro_html': """<p style=\"font-size:1.15rem;\">For families with school-age children, the school-holiday calendar is one of the most influential variables in deciding when to move. The instinct &mdash; align the move with a break to minimise academic disruption &mdash; is right in principle but the practical answer is more nuanced. After forty years of <a href=\"../about-us.html\">family-home Sussex removals</a> we&rsquo;ve seen which school-holiday moves work and which don&rsquo;t.</p>
<p>This guide is the decision-focused complementary to our <a href=\"moving-during-school-holidays.html\">school-holiday operational guide</a>. Where the operational guide covers the practicalities of each holiday window, this guide focuses on the cost-benefit of doing it at all versus an alternative timing.</p>""",
        'sections': [
            ('The case for moving during a school holiday',
             """<p>Three genuine pros. <strong>No academic disruption.</strong> Children don&rsquo;t miss school days; the school transition (if there is one) happens cleanly between terms or year-groups. For older children mid-syllabus, this is the strongest argument.</p>
<p><strong>Available childcare options.</strong> Holiday clubs, grandparent visits, paid childcare for the day &mdash; all easier to arrange in school holidays. For move day specifically, having the children somewhere else makes the move significantly calmer for everyone.</p>
<p><strong>Family schedule flexibility.</strong> One or both parents often have annual leave that they can stretch around school holidays. The week before move day is the demanding one for packing; having both parents available is much better than trying to do it solo with the children at school.</p>"""),
            ('The case against',
             """<p>Three real cons. <strong>Diary availability is worst.</strong> Summer-holiday Saturdays book up 12&ndash;16 weeks ahead and Easter and half-term Saturdays book 8&ndash;12 weeks ahead. Customers without that lead time can struggle to find a slot. Mid-week dates are easier; the <a href=\"how-to-save-money-on-house-move-2026.html\">save-money guide</a> covers the timing-based pricing.</p>
<p><strong>Pricing is at peak.</strong> School-holiday rates run 10&ndash;15% above off-peak rates. The crew rates are the same; the saving comes from quieter demand. For families on tight budgets, the alternative of moving the day before or the day after the school-holiday window can save meaningful money without much family impact.</p>
<p><strong>School admin still has hard deadlines.</strong> The school-place application, the catchment confirmation, the GP and dentist registration &mdash; none of these wait for the school holiday. Families who time the move for the holiday but leave the admin until after term-end consistently regret it.</p>"""),
            ('Summer holiday — the obvious window',
             """<p>The summer school holidays (late July through early September) are the most popular school-holiday move window. The pros are real: long window (6&ndash;7 weeks), genuine flexibility for the school transition, good weather for the practical work. The cons are also real: peak removals demand, highest pricing of the year, and the period where school-place administration is at its tightest.</p>
<p>For families with major school transitions (primary-to-secondary, secondary-to-sixth-form), the summer is essentially the only window that works. The <a href=\"best-schools-eastbourne-families.html\">Eastbourne schools guide</a> covers the admissions timelines.</p>
<p>For families staying in the same school catchment after the move, the summer window is helpful but not essential. Moving in early July before peak, or early September after peak, often works as well and costs less.</p>"""),
            ('Easter — the underrated middle option',
             """<p>The Easter holiday window is genuinely the best balance of the three for many families. Two weeks (sometimes three for independent schools), better weather than winter, quieter removals diary than summer, and clear school-transition timing for families changing schools at the start of the summer term.</p>
<p>The complications: Easter dates shift year-to-year (between late March and late April), the new tax year sometimes overlaps, and the chain timing can be awkward if your conveyancing extends into the post-Easter period. For most families with flexibility, though, the Easter window is meaningfully better than waiting for summer.</p>
<p>The <a href=\"moving-house-in-summer.html\">summer-moving guide</a> covers the seasonal operational details and the <a href=\"how-to-prepare-for-your-house-move.html\">how-to-prepare guide</a> covers the 8-week run-up that works well in the Easter window.</p>"""),
            ('Half-term — short windows that sometimes work',
             """<p>The October, February and May half-term windows are short (one week) but workable for specific scenarios. The right scenarios: local moves where the children stay at the same school, families with limited contingency for chain delays, and households that already have everything else organised and just need the final move day.</p>
<p>October half-term is the best of the three: enough time to settle, neutral weather, no major holiday commitments. February half-term is workable but cold (the <a href=\"moving-house-in-winter.html\">winter-moving guide</a> covers the cold-weather operational details). May half-term starts to clash with the run-up to GCSE/A-level exams; secondary-school families should usually avoid this window.</p>
<p>For half-term moves, build in contingency. The one-week window doesn&rsquo;t accommodate a two-day chain slip; if the chain&rsquo;s flexibility is uncertain, choose a longer window. The <a href=\"questions-to-ask-removals-company.html\">questions-to-ask guide</a> covers what to confirm about chain timing.</p>"""),
            ('When to move outside the school-holiday windows',
             """<p>Three scenarios where moving outside school holidays is genuinely the right choice. <strong>Very young children</strong> (under 5, pre-school). The school-holiday alignment matters less because the children&rsquo;s schedule isn&rsquo;t set by school terms. A November or January-onwards move can be calmer and cheaper.</p>
<p><strong>Families on tight budgets</strong>. The 10&ndash;15% pricing differential between school-holiday and off-peak dates is real money. For households where the budget is tight, a Tuesday in February move is dramatically cheaper than a Saturday in August.</p>
<p><strong>Older children with strong friendship networks</strong>. Secondary-school children often prefer to stay at school during a move rather than be packed off to grandparents&rsquo; for the week. Moving on a Tuesday during term-time can actually be less disruptive than moving during the summer break when their established holiday plans are disrupted.</p>"""),
        ],
        'faqs': [
            ("Is moving during school holidays really easier?",
             "For families with major school transitions, yes — academic disruption is minimised. For families staying in the same catchment, the differential is smaller and the price premium may not be worth it."),
            ("Which school holiday is the best to move in?",
             "Easter is the best balance for most families. Summer is necessary for major school transitions. Half-term is workable for short local moves. Christmas is generally to be avoided unless forced."),
            ("How much more does a school-holiday move cost?",
             "Typically 10–15% above off-peak rates. The crew rates are identical; the differential reflects quieter demand at off-peak times."),
            ("When should I book a summer-holiday move?",
             "12–16 weeks ahead for Saturdays. Mid-week dates are easier to book and slightly cheaper. The earlier the booking, the more choice of slot."),
            ("Should I move during half-term?",
             "Only for short local moves where the children stay at the same school. The one-week window doesn't accommodate chain delays well; for longer or more complex moves, choose a longer school-holiday window or move outside the school-holiday calendar."),
        ],
    },

    # ---- 64 — alternative eco-friendly listicle angle ----
    {
        'slug': 'ten-ways-eco-friendly-house-move.html',
        'title': '10 Ways to Make Your House Move More Eco-Friendly',
        'desc': 'Practical and achievable ways to reduce waste and make your house move more environmentally friendly in 2026.',
        'kicker': '10 practical methods · Reduce, reuse, offset',
        'h1': '10 Ways to Make Your House Move More Eco-Friendly',
        'hero_sub': "Ten practical steps from a Sussex remover that take less effort than expected and add up to a measurably greener move.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': '10 eco-friendly moving ideas',
        'intro_html': """<p style=\"font-size:1.15rem;\">Sustainable moving sounds like a marketing claim until you look at the concrete decisions. After forty years of <a href=\"../about-us.html\">Sussex removals</a> we have a clear list of what genuinely reduces a move&rsquo;s environmental footprint and what is window dressing. This guide lists the ten changes that actually matter, in rough order of impact.</p>
<p>The framing is &ldquo;reduce first, then reuse, then offset&rdquo; &mdash; the standard environmental hierarchy applied to a house move. The detail below covers each step practically. For the wider conversation, our <a href=\"eco-friendly-moving-sustainable-removals.html\">sustainable removals guide</a> covers the principles; this guide is the actionable checklist.</p>""",
        'sections': [
            ('1. Declutter ruthlessly before the survey',
             """<p>The single biggest environmental decision in any move is how much volume you actually move. A 3-bed household that genuinely declutters to a 2-bed inventory moves 30&ndash;40% less stuff, uses 30&ndash;40% less lorry capacity, and consumes proportionally less fuel and materials. Charity-shop and online-sale routes for items with life left in them; council recycling for items genuinely at the end of life.</p>
<p>The 12-month rule: have I used this in the last 12 months, and would I buy it again today? Both no = donate, sell or dispose. The <a href=\"how-to-downsize-before-moving.html\">downsizing guide</a> walks through the practical method. Local Sussex charities &mdash; St Wilfrid&rsquo;s Hospice, Demelza, the British Heart Foundation &mdash; collect for free for sellable items.</p>"""),
            ('2. Choose reusable crates over single-use cartons',
             """<p>Plastic rental crates from rental providers replace single-use cardboard cartons entirely. The crates get used across hundreds of moves over their working life; the per-move embodied carbon is a fraction of cardboard&rsquo;s. The cost differential is small (rental crates are marginally more expensive per move than disposable cardboard) but the environmental gain is meaningful.</p>
<p>For customers who prefer cardboard, our materials are sourced from recycled-content cartons where available and we collect and reuse cartons across multiple moves. The <a href=\"../packaging-shop.html\">Lower Dicker packaging shop</a> sells second-hand cartons at meaningfully lower prices than new; these have already done one or two moves and have several more in them.</p>"""),
            ('3. Pad-wrap rather than shrink-wrap furniture',
             """<p>Our standard <a href=\"how-our-pad-wrap-service-protects-furniture.html\">pad-wrap method</a> uses heavy quilted blankets laundered between every job and reused indefinitely. Shrink-wrap alternatives use 8&ndash;15kg of single-use plastic per typical 3-bed move; pad-wrap uses zero. The protection is better, the environmental cost is lower, and the customer experience is the same or better.</p>
<p>Most reputable removers include pad-wrap as standard on every full removal. Budget operators sometimes use shrink-wrap as a cheaper alternative; the customer pays slightly less for the move but the environmental and damage-rate trade-off is real. Worth confirming at <a href=\"questions-to-ask-removals-company.html\">survey stage</a> with any quote.</p>"""),
            ('4. Donate, sell or recycle &mdash; don&rsquo;t tip',
             """<p>For items that don&rsquo;t come with you, the disposal route matters. The hierarchy: <strong>donate to a charity shop</strong> (preserves the item&rsquo;s embodied carbon, helps a local charity), <strong>sell online or to a friend</strong> (same benefit), <strong>recycle through specific streams</strong> (electronics, batteries, paint, hazardous chemicals), and only <strong>then dispose to the tip</strong> for genuinely end-of-life items.</p>
<p>The temptation to tip everything is real because it&rsquo;s convenient. The environmental cost of tipping a working sofa or a usable wardrobe is the embodied carbon of someone else having to buy a replacement; the cost of donating the same item is essentially zero. Local councils in East Sussex offer kerbside bulky-waste collection at modest cost; charity shops collect for free for sellable items.</p>"""),
            ('5. Combine trips and plan the route',
             """<p>For self-pack moves, the multiple trips between home and the local DIY shop for more materials, plus the tip runs, plus the charity-shop drop-offs &mdash; all add up to real fuel use. Plan the route. Combine the materials run, the tip run, and the charity drop into a single weekend trip rather than multiple separate ones.</p>
<p>For the actual removal day, we plan the lorry route directly from old property to new with no intermediate stops. For moves involving storage, we use lorries that are already heading in that direction co-loading where possible. The <a href=\"how-to-make-move-carbon-neutral.html\">carbon-neutral moves guide</a> covers the route-efficiency angle.</p>"""),
            ('6. Move locally if you can',
             """<p>The single biggest carbon variable in any move is distance. A 20-mile move generates roughly a quarter of the carbon of a 200-mile move. For customers with flexibility about the destination, choosing local-to-the-current-area over long-distance is the largest single environmental decision.</p>
<p>Within Sussex, we routinely move customers between <a href=\"moving-to-eastbourne-area-guide.html\">Eastbourne</a>, <a href=\"moving-to-brighton-area-guide.html\">Brighton</a>, <a href=\"moving-to-hastings-area-guide.html\">Hastings</a>, <a href=\"moving-to-lewes-area-guide.html\">Lewes</a> and the wider South Coast as local moves. The carbon footprint of these moves is roughly a fifth of the equivalent London-to-Sussex relocation.</p>"""),
            ('7. Pick a fully-loaded lorry',
             """<p>A half-loaded lorry uses roughly the same diesel as a fully-loaded one to make the same journey. From a carbon-per-cubic-metre perspective, the fully-loaded lorry is dramatically more efficient. For households moving large inventories, picking the right lorry size at survey matters &mdash; an oversized lorry for a small move wastes diesel; an undersized lorry for a large move requires multiple trips.</p>
<p>For us as the operator: we size the lorry at survey based on inventory volume, and we don&rsquo;t over-promise capacity. For the customer: don&rsquo;t pay for a lorry size larger than you need on the assumption it&rsquo;s &ldquo;safer&rdquo;; the carbon and the cost are both proportional to the vehicle.</p>"""),
            ('8. Choose digital paperwork where possible',
             """<p>The amount of paper that historically came with a house move (the conveyancing pack, the removal contract, the inventory, the insurance documents, the new-address forms) is significant. Most of this now exists digitally. Choose digital signatures and emailed contracts over printed equivalents; archive electronically rather than in filing cabinets.</p>
<p>For our part, we offer digital quote documents, digital inventories, and electronic post-move follow-ups. For the customer, the change-of-address admin (banks, utilities, GP) is almost all online now. The shift from paper to digital is small per move but meaningful in aggregate across an industry doing tens of thousands of moves a year.</p>"""),
            ('9. Set up the new home efficiently',
             """<p>The first month at the new house is when environmental decisions compound. Set up the heating system to operate efficiently (smart thermostat, zoned heating where possible). Install LED bulbs where the existing ones are halogen or incandescent. Check the loft and wall insulation; the new house may have inherited poor insulation from a previous owner.</p>
<p>For appliances inherited with the property, check the energy ratings. A 15-year-old fridge or freezer consumes 2&ndash;3x the electricity of a modern equivalent; the replacement cost is recovered in 3&ndash;5 years of energy savings plus has lower lifetime carbon. The same applies to washing machines, dishwashers, ovens, and (most significantly) heating systems.</p>"""),
            ('10. Offset the residual footprint',
             """<p>After reducing what you can reduce and reusing what you can reuse, the residual footprint is the part that&rsquo;s genuinely unavoidable. A typical Sussex local move produces 60&ndash;120 kg CO2-eq even with best-practice operations. For customers wanting a genuinely net-zero move, offsetting through a verified scheme handles this residual.</p>
<p>Verified Carbon Standard (VCS), Gold Standard, or the UK Woodland Carbon Code are the credible options. The cost for a typical Sussex move is &pound;1&ndash;&pound;5 through gold-standard providers. For international moves at 2 tonnes CO2-eq, the cost is &pound;20&ndash;&pound;50. Modest relative to the move price and verifiable in writing. The <a href=\"how-to-make-move-carbon-neutral.html\">carbon-neutral moves guide</a> covers the verification standards in detail.</p>"""),
        ],
        'faqs': [
            ("What's the single biggest eco-friendly decision?",
             "Distance. Moving locally generates a fraction of the carbon of a long-distance move. For customers with destination flexibility, this is the largest single environmental lever."),
            ("Are reusable plastic crates worth it?",
             "For the environment, yes — each crate gets used across hundreds of moves. For the customer, marginally more expensive per move than disposable cardboard. We can source rental crates if requested."),
            ("Is pad-wrap genuinely more sustainable than shrink-wrap?",
             "Yes — pad-wrap blankets get washed and reused indefinitely. Shrink-wrap uses 8–15kg of single-use plastic per typical 3-bed move."),
            ("What about offsetting the carbon?",
             "After reducing and reusing, offset the residual through a gold-standard verified scheme. £1–£5 for a typical Sussex move; £20–£50 for international. Choose verified schemes, not unverified ones."),
            ("Can the removal lorry use lower-carbon fuel?",
             "HVO biofuel is an option in some lorry fleets. Most current UK removal fleets still use standard diesel. The industry-wide transition is slow but underway."),
        ],
    },

    # ---- 65 — alternative carbon offset angle ----
    {
        'slug': 'how-to-offset-carbon-emissions-moving.html',
        'title': 'How to Offset Your Carbon Emissions When Moving House',
        'desc': 'Want to make your removal as green as possible? Learn how to calculate and offset the carbon footprint of your house move.',
        'kicker': 'Carbon offsetting · Calculation, verification, action',
        'h1': 'How to Offset Your Carbon Emissions When Moving House',
        'hero_sub': "The maths, the verification standards, and the practical mechanics of offsetting your move's footprint properly.",
        'hero_img': 'mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'breadcrumb': 'Carbon offsetting your move',
        'intro_html': """<p style=\"font-size:1.15rem;\">Offsetting carbon emissions is one of those topics where the difference between &ldquo;done properly&rdquo; and &ldquo;greenwashed&rdquo; matters more than the headline action. A &pound;5 offset through a credible verified scheme is meaningfully different from a &pound;5 contribution to a vague tree-planting marketing exercise. After forty years of <a href=\"../about-us.html\">Sussex removals</a> and increasing customer interest in this topic, we&rsquo;ve learned how to do it credibly.</p>
<p>This guide walks through the calculation, the verification standards, and the practical mechanics. The aim is to give customers what they need to make their move genuinely net-zero rather than nominally so. For the wider carbon-neutral conversation, our <a href=\"how-to-make-move-carbon-neutral.html\">carbon-neutral moves guide</a> covers the broader principles; this guide is the operational checklist.</p>""",
        'sections': [
            ('Step 1 — calculate the actual footprint',
             """<p>Offsetting starts with an honest calculation of what you&rsquo;re offsetting. A typical 3-bed Sussex local move (under 50 miles) generates 60&ndash;120 kg CO2-equivalent. The breakdown: lorry diesel (40&ndash;80 kg, depending on distance and load), materials embedded carbon (10&ndash;25 kg, depending on cartons and packaging), depot overheads (5&ndash;15 kg, proportional to the share of the depot&rsquo;s annual energy your move represents).</p>
<p>For longer moves, the lorry-diesel component scales with distance. A 200-mile move sits at 200&ndash;350 kg CO2-eq; a 500-mile move at 500&ndash;800 kg. For international shipping, the calculation includes the shipping leg: a 20-foot container by sea to Australia generates 1.5&ndash;2.5 tonnes; the same container to the US is 0.6&ndash;1.2 tonnes.</p>
<p>We&rsquo;ll provide a CO2-eq calculation on the quote on request &mdash; this isn&rsquo;t a standard line but we can derive it from the move&rsquo;s logistical specifics. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a> if this matters to your move planning.</p>"""),
            ('Step 2 — reduce before offsetting',
             """<p>The honest approach is &ldquo;reduce first, then offset&rdquo;. Offsets work better at smaller numbers; reducing the footprint by 25&ndash;40% through good practice means the offset cost is correspondingly lower. The reduction options are covered in our <a href=\"ten-ways-eco-friendly-house-move.html\">10-ways eco-friendly moving guide</a>: declutter, use reusable materials, choose pad-wrap, plan efficient routes.</p>
<p>For most customers, the post-reduction residual footprint is in the range we&rsquo;ve given above for the move type. The offset then sizes against this residual. Customers who try to skip the reduction step and offset only end up paying more for the same net-zero outcome, and the offset purchase doesn&rsquo;t address the structural inefficiencies.</p>
<p>Once the reduction work is done, calculate what remains, and proceed to offsetting. The two steps are sequential, not alternatives.</p>"""),
            ('Step 3 — pick a verified scheme',
             """<p>The verification standards that matter: <strong>Verified Carbon Standard (VCS)</strong> &mdash; the global market leader for offset verification, independent monitoring of projects, additionality requirements. <strong>Gold Standard</strong> &mdash; similar standards with additional sustainable-development criteria. <strong>Climate, Community and Biodiversity Standards (CCB)</strong> &mdash; specifically certifies projects with social and biodiversity co-benefits. <strong>UK Woodland Carbon Code (WCC)</strong> &mdash; the UK-specific scheme for verified domestic tree-planting.</p>
<p>Schemes to be cautious about: unverified tree-planting projects (where the claim isn&rsquo;t externally audited), &ldquo;forest preservation&rdquo; offsets where the threat to the forest is overstated, and any scheme that won&rsquo;t provide a certificate of retirement after purchase. The certificate is the proof that the offset has been retired from the registry &mdash; without it, the same offset could be sold to another buyer.</p>
<p>For UK-based customers, the WCC has the appeal of domestic woodland creation with full verification. For broader offsetting (renewable energy projects, methane capture, etc.), VCS and Gold Standard are the global standards. Both produce certificate-tracked retirements that satisfy any serious accounting requirement.</p>"""),
            ('Step 4 — pick a credible provider',
             """<p>Major UK-accessible providers: Climate Care (UK-based, multi-scheme), Gold Standard Marketplace (international, gold-standard schemes only), Verra registry (VCS-verified projects), Trees for the Future (international tree-planting), Eden Reforestation Projects (verified tree-planting with social co-benefits). Each has its own focus and pricing.</p>
<p>Costs vary by scheme type. High-quality VCS or Gold Standard offsets typically run &pound;10&ndash;&pound;25 per tonne CO2-eq. Tree-planting schemes often slightly cheaper but with longer time horizons for the carbon to be sequestered. UK-based WCC schemes are typically &pound;20&ndash;&pound;40 per tonne CO2-eq with the benefit of domestic woodland creation.</p>
<p>For a typical Sussex move at 100 kg CO2-eq, the offset cost is &pound;1&ndash;&pound;4. For an international move at 2 tonnes, &pound;20&ndash;&pound;80. The cost is modest relative to the move price; the choice of scheme matters more than the absolute spend.</p>"""),
            ('Step 5 — purchase, retire, certificate',
             """<p>The mechanical steps. <strong>Purchase</strong> through the provider&rsquo;s online portal (typically credit card or invoice for larger amounts). <strong>Specify the project</strong> &mdash; most providers show available projects with their verification status. <strong>Retire the offset</strong> &mdash; the provider records the purchase against the project&rsquo;s registry and removes those credits from circulation. <strong>Receive the certificate</strong> &mdash; PDF or paper, with the project ID, the registry retirement number, and the CO2-eq amount retired.</p>
<p>Keep the certificate. It&rsquo;s the proof of the offset for any future reporting, insurance, or formal sustainability claims. For business moves, the certificate may be required for the company&rsquo;s sustainability accounting. For personal moves, it&rsquo;s the proof that the offset was actually retired rather than just paid for.</p>
<p>For customers who want us to handle the offsetting as part of the move quote, we can arrange it through verified providers and add it as a line item. The certificate comes to you after the move. Talk to us at <a href=\"../mark-ratcliffe-moving-online-removals-quote.html\">survey</a>.</p>"""),
            ('Limitations and the honest framing',
             """<p>Carbon offsetting is one tool among several. It addresses the climate-specific footprint of the move but not the wider environmental impact (local air quality near depots, materials extraction for blanket and lorry components, end-of-life disposal of materials). The honest framing: offsets handle CO2-eq, not broader environmental footprint.</p>
<p>For customers committed to a low-carbon life, the move is a small fraction of annual emissions. The bigger levers are home energy (heating, electricity), transport (car miles, flights), and food. The move-specific offset addresses the move; the wider household decisions matter more for the annual total.</p>
<p>Offsetting also doesn&rsquo;t replace reduction. The hierarchy is reduce-reuse-offset; offset-only is the &ldquo;avoid then offset&rdquo; principle backwards. For customers committed to an environmentally honest move, the full sequence matters. The <a href=\"eco-friendly-moving-sustainable-removals.html\">eco-friendly moves guide</a> covers the broader sequence.</p>"""),
        ],
        'faqs': [
            ("How do I calculate my move's footprint?",
             "Talk to us at survey — we can provide a CO2-eq estimate based on the move's specifics (distance, lorry size, inventory volume). Ballpark figures: 60–120 kg for a Sussex local move; 200–350 kg for a long-distance UK move; 1.5–2.5 tonnes for international shipping."),
            ("Which offset schemes are credible?",
             "Verified Carbon Standard (VCS), Gold Standard, Climate Community and Biodiversity (CCB), and the UK Woodland Carbon Code (WCC). Avoid unverified or vague schemes."),
            ("What does it cost?",
             "£10–£25 per tonne CO2-eq for verified offsets. For a typical Sussex move at 100 kg, £1–£4. For an international move at 2 tonnes, £20–£80. Modest relative to the overall move cost."),
            ("Can you arrange the offset as part of the move quote?",
             "Yes — we calculate the CO2-eq footprint, purchase verified offsets through a Gold Standard or VCS provider, and add it as a line item. The certificate comes to you after the move."),
            ("Is offsetting enough on its own?",
             "No — the right order is reduce first, then reuse what you can reuse, then offset the residual. Skipping the reduction step means the offset cost is higher and the structural inefficiencies aren't addressed."),
        ],
    },
]


# ----------------------- TEMPLATE LOADER (same as previous generators) ----
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
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": blog['h1'], "description": blog['desc'], "image": image_url,
        "datePublished": "2026-05-19", "dateModified": "2026-05-19",
        "author": {"@type": "Organization", "name": "Mark Ratcliffe Moving & Storage"},
        "publisher": {"@id": "https://www.markratcliffemoving.co.uk/#organization"},
        "mainEntityOfPage": canonical,
    }
    ld_breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.markratcliffemoving.co.uk/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.markratcliffemoving.co.uk/blog/index.html"},
            {"@type": "ListItem", "position": 3, "name": blog['breadcrumb']},
        ],
    }
    ld_faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in blog['faqs']],
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
  <link href="../css/normalize.css?v=20260552" rel="stylesheet">
  <link href="../css/components.css?v=20260552" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260552" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260552" rel="stylesheet">
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
  <script defer src="../js/nofollow-shim.js?v=20260552"></script>
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
