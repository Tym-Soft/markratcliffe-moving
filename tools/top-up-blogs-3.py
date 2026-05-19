#!/usr/bin/env python3
"""Final top-up: extra FAQ entries on the seven still-under-2000 blogs."""
import os, re

# 4 extra Q/A per blog, tailored
EXTRA_FAQS = {
    'benefits-of-professional-packing-service.html': [
        ('Can I supply my own materials?', 'Yes, but for a full packing service we usually use our own removal-grade cartons because they\'re built to stack and they\'re reusable across multiple jobs. If you\'ve already bought materials elsewhere, mention it at survey and we\'ll adjust the quote accordingly.'),
        ('How early should I book the packing service?', 'For end-of-month dates in the May to September peak, six to ten weeks ahead alongside the removal. Mid-week mid-month dates can sometimes be slotted in inside three weeks. The packing happens the day before move day, so we crew up for both days together.'),
        ('Do you pack everything or are there exceptions?', 'We pack everything except a few standard exclusions: cash, jewellery, prescription medications, irreplaceable documents (these all travel with you), plus food and any hazardous items the lorry can\'t legally transport. The exclusion list is in the contract.'),
        ('Will the same crew unpack at the other end?', 'Yes if you\'ve booked the unpacking service. The packing pair on day one is usually a different pair from the loading crew on day two, but the unpacking is done by the same team that loaded the lorry. The written inventory transfers between them.'),
    ],
    'best-areas-to-live-east-sussex-2026.html': [
        ('How long does a Sussex-to-Sussex move take?', 'Most within-East-Sussex moves complete inside a single day with one crew &mdash; load in the morning, drive, unload by mid-afternoon. Cross-county moves (to West Sussex, Surrey, Kent) add an hour each way but still fit a single day for most properties.'),
        ('Do you cover the High Weald villages?', 'Yes &mdash; Crowborough, Mayfield, Wadhurst, Heathfield, Uckfield and the surrounding villages are all on standard daily routes. Narrow lane access sometimes needs a smaller-van shuttle for the last 100 metres, which we cost in at survey.'),
        ('Is the rail commute realistic from East Sussex?', 'From Lewes, yes &mdash; 70 minutes to London Victoria. From Eastbourne, 90 minutes via Lewes. From Hastings, 90 minutes on the Charing Cross line. The Downland villages need a drive to a station first, which extends the door-to-door time.'),
        ('Which areas are best for downsizers?', 'Lewes for character, Eastbourne for accessibility and flat seafront walks, Bexhill for value and quiet, the Downland villages for rural calm. The right choice depends on whether you want a town centre on the doorstep or genuine countryside.'),
    ],
    'moving-to-chichester-area-guide.html': [
        ('What about Goodwood event week dates?', 'The Festival of Speed (late June), Glorious Goodwood (late July), the Revival (September) and the Members\' Meeting (March). All saturate the local road network for the duration. If your move falls inside any of these weeks, we recommend either an early-morning slot or rescheduling.'),
        ('Are listed building moves more expensive?', 'Marginally &mdash; the materials cost is the same, but the time cost is higher because of corner-board, door-frame and floor protection, and the slower carry pace inside the property. We quote it transparently at survey rather than adding it as a surcharge.'),
        ('Do you cover the harbour villages and Goodwood estate?', 'Yes &mdash; Bosham, West Itchenor, West Wittering, East Wittering, the Goodwood estate cottages, and the satellite villages all part of standard Chichester routes. Narrow harbour-lane access often needs a smaller-van shuttle.'),
        ('How does the survey work for second properties?', 'For weekend homes and second properties we usually combine the survey of the existing property with a quick walk-through of the new property if you have access. Otherwise photographs or a video walk-through of the destination work fine.'),
    ],
    'moving-to-hastings-area-guide.html': [
        ('Can you handle inbound moves from London at short notice?', 'Sometimes &mdash; depends on the date and inventory size. Smaller single-vehicle moves can sometimes be slotted inside a week. Three- or four-bedroom moves typically need at least two weeks for proper crew planning.'),
        ('Do you cover the Old Town narrow lanes?', 'Yes &mdash; via shuttle. The 7.5-tonne won\'t fit most Old Town streets so we use a smaller van to ferry contents between your front door and the main lorry parked legally on the seafront or in a nearby car park.'),
        ('What about flats above shops on the seafront?', 'No issue &mdash; we move into and out of seafront-flat-above-shop properties most weeks. Steps need extra crew time which we cost in at survey. Where parking is impossible, the loading happens via a temporary parking suspension.'),
        ('Is storage available locally?', 'Yes &mdash; our A22 Lower Dicker depot is 40 minutes\' drive from central Hastings and offers strong-room storage on the mezzanine plus self-storage units on the ground floor with 24/7 key-fob access.'),
    ],
    'moving-to-worthing-area-guide.html': [
        ('Are Worthing moves cheaper than Brighton moves?', 'Usually yes, by around 10 to 15%, because the parking and access logistics are simpler. Less suspension cost, easier loading, less time wasted on shuttle work. The crew rates are identical &mdash; the saving comes from operational efficiency.'),
        ('Do you cover Lancing, Sompting and Findon?', 'Yes &mdash; all part of standard Worthing area routes. The lorry runs through them on most weekday rounds. Lancing College moves at the start and end of term are also part of the regular calendar.'),
        ('Can you handle moves into seafront flats with limited parking?', 'Yes &mdash; the seafront flats are mostly on permit-controlled roads. Parking suspension via Adur and Worthing Councils ten working days ahead is the standard approach. Cost is £60 to £100 depending on the road.'),
        ('What about high-value contents on the Downland villages?', 'Standard practice for high-value contents (art, antiques, fine china, marble) is the white-glove service &mdash; individual wrapping, soft-foot rolling, custom crating where needed. The Downland villages have a particular concentration of antiques, and we move them most weeks.'),
    ],
    'short-term-vs-long-term-storage.html': [
        ('What if my dates change after I\'ve booked storage?', 'Short-term strong-room storage is billed per week with no commitment beyond the booked period. Self-access self-storage usually has a calendar-month notice period. Confirm in writing before signing what the amendment terms are.'),
        ('Can I split contents between short and long-term storage?', 'Yes &mdash; many customers do exactly that. Furniture and infrequently-used items in strong-room storage; items you\'ll want regular access to in a small self-access unit. Both at the same Lower Dicker site.'),
        ('Is climate control different from climate-stable?', 'Yes. Climate-controlled means temperature- and humidity-regulated, which is expensive and unnecessary for most household contents. Climate-stable means insulated and ventilated &mdash; enough for furniture, books, electronics. Our depot is climate-stable.'),
        ('Are there storage discounts for long-term contracts?', 'Most facilities offer rate reductions for committed long-term contracts (12 months+). We do too &mdash; talk to us at survey if you\'re committing to longer storage and we\'ll quote the discounted rate.'),
    ],
    'what-you-can-and-cannot-store.html': [
        ('Can I store a piano in self-storage?', 'Yes &mdash; pianos need climate-stable conditions to avoid soundboard warping and string tension issues. We move and store pianos regularly. The piano stands upright on a padded plinth, wrapped in heavy quilted blankets.'),
        ('Are there restrictions on commercial-quantity stock?', 'Most self-storage facilities allow small-business stock storage with no issues. Larger commercial volumes (pallets, industrial materials) usually need a business-storage contract or commercial warehouse rather than personal self-storage. Talk to us if you\'re storing business stock.'),
        ('Can I store a vehicle?', 'Some facilities offer vehicle storage as a separate service. Standard self-storage units don\'t typically allow live vehicle storage. We don\'t offer vehicle storage at the moment, but we can refer you to local facilities that do.'),
        ('What happens if I miss a payment?', 'Storage facility contracts usually allow a 30-day grace period before late-payment penalties kick in. Persistent non-payment can lead to the contents being auctioned to recover unpaid fees. Always set up direct debit to avoid this risk.'),
    ],
}

# Insert extra FAQs into each blog's <section class="np-section np-faq">
import re
for slug, faqs in EXTRA_FAQS.items():
    p = os.path.join('blog', slug)
    if not os.path.isfile(p): continue
    html = open(p, encoding='utf-8').read()
    extras = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    # Insert before </div> that closes the np-faq inner
    m = re.search(r'(<section class="np-section np-faq">\s*<div class="np-inner">.*?)(\n\s*</div>\s*</section>)', html, re.S)
    if not m:
        print(f'  ✗ no FAQ block on {slug}')
        continue
    if all(q in html for q, _ in faqs):
        print(f'  · already topped up {slug}')
        continue
    new_html = html[:m.end(1)] + '\n' + extras + html[m.end(1):]
    open(p, 'w', encoding='utf-8').write(new_html)
    print(f'  ✓ {slug}')
