#!/usr/bin/env python3
"""
Generate four county landing pages:
  /areas-covered/east-sussex.html
  /areas-covered/west-sussex.html
  /areas-covered/surrey.html
  /areas-covered/kent.html

Each page is unique content (Rules 6/11/25), ≥1500 words (Rule 2),
≥10 distinct in-body links (Rule 3), one H1 (Rule 26), full SEO chrome
(canonical, og, JSON-LD), CSP + Referrer-Policy (Rule 20).

Reuses the existing site CSS/JS bundle. Navbar + footer are copied
from an existing /areas-covered/ page so depth-relative hrefs match.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'

# ---- Town data per county ---------------------------------------------------
TOWNS = {
    'east-sussex': [
        ('Eastbourne',        'removals-eastbourne.html',
         "Our home town since 1982. From sea-front flats on Grand Parade to bungalows in Old Town and the period houses of Meads, our crews work every Eastbourne postcode (BN20–BN23) most weeks of the year."),
        ('Hailsham',          'hailsham-removals.html',
         "A traditional Sussex market town on the Cuckoo Trail with strong community feel. We move retirees into ground-floor flats and young families into the newer estates on the edge of town."),
        ('Bexhill',           'removals-bexhill.html',
         "Edwardian seaside town home to the De La Warr Pavilion. Many customers here are downsizers leaving large family homes for low-maintenance flats with sea views."),
        ('Hastings',          'removals-hastings.html',
         "Old Town twittens, the East Hill bohemian quarter and modern developments at St Leonards. The narrow streets near the seafront need our smaller lorries; the team plans accordingly."),
        ('Heathfield',        'removals-heathfield.html',
         "Set on the High Weald with sweeping South Downs views. Country properties here often sit at the end of long shingle drives; we send a four-person crew and the right lorry every time."),
        ('Uckfield',          'removals-uckfield.html',
         "A larger commuter town with strong rail links to London via Oxted. We see plenty of move-out-to-London customers but also retiring couples downsizing from Buxted to bungalows in town."),
        ('Pevensey',          'removals-pevensey.html',
         "Historic village with Pevensey Castle and A259 access. Levels approach and seafront-cottage parking is something only experienced Sussex crews navigate confidently."),
        ('Polegate',          'removals-polegate.html',
         "Commuter village just north of Eastbourne. The 1930s semis and newer estates make for straightforward moves; the team often pairs Polegate with another Eastbourne job the same day."),
        ('Willingdon',        'removals-willingdon.html',
         "Quiet residential area with downland walks. Most homes here are larger family houses; full pack-and-load is the typical service we provide."),
        ('Peacehaven',        'removals-peacehaven.html',
         "Coastal grid-layout streets with plenty of bungalows. Downsizers from inland Sussex frequently move here for the sea air; we handle several Peacehaven jobs every month."),
        ('Crowborough',       'removals-crowborough.html',
         "High Weald country town with forest-edge properties. Country homes with antiques and pianos are common; specialist pad-wrap protection gets a lot of use here."),
        ('Rye',               'removals-rye.html',
         "Cobbled streets, the Mermaid Inn and dozens of listed cottages. Access is the main challenge — narrow lanes, parking permits and properties that pre-date our lorry's turning circle. We always survey Rye in person."),
        ('Battle',            'removals-battle.html',
         "The 1066 battlefield town with mixed Georgian and Victorian housing. Country lanes around Battle need our smaller crews; we plan accordingly."),
        ('Robertsbridge',     'removals-robertsbridge.html',
         "Peaceful Rother valley village. Many Robertsbridge customers are downsizing from country houses with long drives and outbuildings — we send the right combination of lorry and crew."),
        ('Mayfield',          'removals-mayfield.html',
         "Pretty High Weald village with listed properties along the High Street. Move planning often includes road closures and council parking suspensions; we handle the paperwork."),
        ('Wadhurst',          'removals-wadhurst.html',
         "Forest-edge village with substantial country homes. Antique furniture, large gardens with outbuildings and full pad-wrap protection are the norm."),
        ('Forest Row',        'removals-forest-row.html',
         "Set on the edge of Ashdown Forest. Country moves here often include garden machinery and outdoor furniture; we blanket-wrap everything as standard."),
        ('Winchelsea',        'removals-winchelsea.html',
         "Hilltop medieval town with cobbled lanes. Listed buildings, narrow access and tight parking arrangements need careful pre-move surveys."),
        ('Alfriston',         'removals-alfriston.html',
         "Picturesque village in the Cuckmere valley. The narrow main street and listed houses require access planning; we work with the parish council on the day."),
        ('Friston',           'removals-friston.html',
         "Tiny downland village near the Seven Sisters. Period cottages with limited parking and steep approaches mean a smaller lorry, larger crew and careful planning."),
        ('Rottingdean',       'removals-rottingdean.html',
         "Coastal village on the edge of Brighton with Kipling literary heritage. Period cottages and modern flats both feature; we cover both with the right crew."),
        ('Saltdean',          'removals-saltdean.html',
         "Modernist suburb with the art-deco Lido. Large family homes and post-war estates; our team is at Saltdean most weeks."),
        ('Lewes',             'removals-lewes-moving-home-in-sussex.html',
         "County town in the Sussex chalk hills. Listed High Street properties, narrow access to medieval streets and routine parking suspensions are typical. We have moved Lewes families for decades."),
        ('Newhaven',          'removals-newhaven-sussex.html',
         "Coastal port town with cross-channel ferry access. Customs paperwork for cross-channel moves is something our overseas team handles routinely."),
        ('Seaford',           'removals-seaford.html',
         "Coastal town with chalk cliffs and a strong retirement community. Many Seaford customers downsize from larger inland properties; bungalow moves dominate."),
    ],

    'west-sussex': [
        ('Brighton',          'removals-brighton.html',
         "Vibrant city with everything from Regency squares to modern flats. Our crew is in Brighton every week, navigating the South Lanes, Kemp Town's hilly back streets and the suburb estates west of town. Parking suspensions are routine."),
        ('Hove',              'removals-hove.html',
         "Wide Regency squares, leafy streets and modern coastal flats. Hove moves are often straightforward but seafront parking suspension paperwork takes lead time."),
        ('Worthing',          'removals-worthing.html',
         "Long seafront promenade with a mix of period properties and modern flats. We move Worthing families regularly, often combining same-day Worthing and Lancing jobs."),
        ('Chichester',        'removals-chichester.html',
         "Cathedral city with Georgian elegance. Listed properties in the four-streets quadrant need careful access; permits, parking and surveyor visits are standard."),
        ('Arundel',           'removals-arundel.html',
         "Castle town on the River Arun. Steep streets, riverside cottages and listed buildings characterise Arundel; we plan with the council in advance for the tight access."),
        ('Bognor Regis',      'removals-bognor-regis.html',
         "Esplanade flats and bungalow downsizing dominate. The team covers Bognor most weeks, often pairing with Felpham and Aldwick moves."),
        ('Burgess Hill',      'removals-burgess-hill.html',
         "Mid-Sussex town with strong A23 access. Easy move logistics make Burgess Hill a regular weekday job; we cover the modern estates and older Cuckfield Road properties."),
        ('Horsham',           'removals-horsham.html',
         "West Sussex market town centred on the Carfax. The pedestrianised town centre means parking arrangements take planning; surrounding villages provide simpler access."),
        ('Haywards Heath',    'removals-haywards-heath.html',
         "Commuter town with the most direct London services in Sussex. Lindfield village adjacent has narrow streets needing smaller crews; the modern estates near the station are straightforward."),
        ('East Grinstead',    'removals-east-grinstead-moving-home-in-sussex.html',
         "At the top of the Sussex Weald with strong rail links to London. Period High Street properties contrast with newer estates; our crews adapt accordingly."),
        ('Crawley',           'removals-crawley.html',
         "New town with substantial commercial activity around Gatwick. Office relocations are common; we also handle the residential moves to the New Town's various neighbourhoods."),
        ('Petworth',          'removals-petworth.html',
         "Historic market town with art and antique heritage. Antique furniture handling is the priority; we send our most experienced packers for Petworth jobs."),
        ('Midhurst',          'removals-midhurst.html',
         "Pretty Sussex Weald town with timber-framed buildings. Listed property moves need access planning; we work with conservation guidance."),
        ('Billingshurst',     'removals-billingshurst.html',
         "Mid-Sussex village with strong rail links. Family homes and rural properties feature equally; both are straightforward removal jobs."),
        ('Steyning',          'removals-steyning.html',
         "Set below the South Downs with historic flint cottages. Steyning's narrow lanes and listed properties need careful pre-move surveying."),
        ('Henfield',          'removals-henfield.html',
         "Rural village with mixed period and modern housing. Long drives and country gardens are typical; we send the right vehicle for the access."),
        ('Shoreham-by-Sea',   'removals-shoreham-by-sea.html',
         "Coastal town with marina and Old Town. Houseboat moves are an occasional unusual request we handle alongside conventional removals."),
        ('Bramber',           'removals-bramber.html',
         "Tiny historic village by the River Adur. Cottage moves with limited access; we plan with neighbours and the council."),
        ('West Wittering',    'removals-west-wittering.html',
         "Coastal village famous for the beach. Holiday-home relocations are a significant share of West Wittering work."),
        ('Bosham',            'removals-bosham.html',
         "Picturesque tidal village with Saxon church. Listed properties and occasionally tidal-flooded roads mean Bosham moves need timing."),
        ('Goodwood',          'removals-goodwood.html',
         "Set on the Sussex Downs near the famous motor circuit. Estate properties with sweeping drives; full white-glove service is often appropriate."),
        ('Pulborough',        'removals-pulborough.html',
         "Pretty South Downs village above the River Arun. Riverside cottages and downland properties both feature with the right access plan."),
        ('Storrington',       'removals-storrington.html',
         "West Sussex village beneath Chantry Hill. Country homes and downsizing flats are both common; weekly crew visits."),
        ('Amberley',          'removals-amberley.html',
         "Hilltop village with castle and the chalk-pit museum. Narrow lanes and steep approaches need a smaller lorry and an experienced driver."),
    ],

    'surrey': [
        ('Guildford',         'removals-guildford.html',
         "Major Surrey town with the High Street's cobbled hill. Period properties, modern flats and surrounding country homes all feature; we handle Guildford moves most weeks."),
        ('Epsom',             'removals-epsom-surrey.html',
         "Famous for the Derby. Mix of Victorian houses, modern flats and rural properties on the Downs."),
        ('Leatherhead',       'removals-leatherhead.html',
         "Mole-valley commuter town. The narrow High Street and surrounding rural properties balance straightforward and challenging moves equally."),
        ('Redhill',           'removals-redhill.html',
         "Strategic position on the M23/M25. Easy access for our lorries; family moves to and from London are common."),
        ('Reigate',           'removals-reigate-moving-home-in-surrey.html',
         "Pretty market town below the North Downs. Period properties and large family homes characterise the moves we handle."),
        ('Weybridge',         'removals-weybridge.html',
         "Wealthy commuter town on the River Wey. Larger properties with antique furniture and white-glove handling are typical."),
        ('Woking',            'removals-woking-surrey.html',
         "Major Surrey commuter town with direct London Waterloo access. Office and residential moves both feature."),
        ('Haslemere',         'removals-haslemere.html',
         "Surrey town at the meeting of three counties. Steep wooded approaches and large country properties characterise Haslemere moves."),
        ('Cobham',            'removals-cobham.html',
         "Wealthy Surrey commuter town. Substantial properties with antique furniture and white-glove handling are typical."),
        ('Oxshott',           'removals-oxshott.html',
         "Affluent commuter village. Large gated properties and high-value contents; insurance and care are paramount."),
        ('Esher',             'removals-esher.html',
         "Surrey town with elegant Georgian buildings. Period property moves with antique furniture and pianos are common."),
        ('Virginia Water',    'removals-virginia-water.html',
         "Wealthy Wentworth-estate area. Estate properties with sweeping drives and full white-glove service required."),
        ('Ascot',             'removals-ascot.html',
         "Famous for the racecourse. Substantial properties on the Berkshire/Surrey border with antique and fine-art handling typical."),
        ('Farnham',           'removals-farnham.html',
         "Pretty Surrey market town with Georgian architecture. Listed properties and rural homes both feature."),
        ('Godalming',         'removals-godalming.html',
         "Historic town on the River Wey. Period properties and large family homes characterise the moves."),
        ('Dorking',           'removals-dorking.html',
         "Surrey market town at the base of Box Hill. Walking-distance High Street with cobbled lanes and rural surroundings."),
        ('East Horsley',      'removals-east-horsley.html',
         "Wealthy village in the Surrey Hills. Large family homes with country gardens and outbuildings."),
        ('West Horsley',      'removals-west-horsley.html',
         "Adjacent to East Horsley with similar profile. Long drives and substantial properties."),
        ('Kingswood',         'removals-kingswood.html',
         "Surrey village with golf-course housing. Affluent properties with antiques and fine art."),
        ('Banstead',          'removals-banstead.html',
         "Commuter village with mix of period and modern housing. Straightforward access for our lorries; weekly jobs."),
        ('Ewell',             'removals-ewell.html',
         "Surrey village absorbed by Epsom. Mix of family homes and small flats; family moves common."),
    ],

    'kent': [
        ('Tunbridge Wells',   'removals-tunbridge-wells-moving-home-in-sussex.html',
         "Royal spa town with The Pantiles. Listed Georgian and Victorian properties dominate; permits and access planning are routine."),
        ('Sevenoaks',         'removals-sevenoaks.html',
         "West Kent commuter town with Knole Park nearby. Substantial properties with antiques; we send our most experienced crews."),
        ('Tonbridge',         'removals-tonbridge.html',
         "Castle town on the River Medway. Period and modern properties both feature; access is mostly straightforward."),
        ('Westerham',         'removals-westerham.html',
         "Pretty Kent village with Pitt the Younger connections. Listed properties and rural surroundings characterise the moves."),
        ('Chislehurst',       'removals-chislehurst.html',
         "South-east London commuter village with mature trees and large family homes. White-glove handling for the period properties is typical."),
        ('Bromley',           'removals-bromley.html',
         "Major south-east London suburb. Mix of large family homes, modern flats and substantial properties; high move volume."),
        ('Beckenham',         'removals-beckenham.html',
         "Adjacent to Bromley with similar profile. Strong family-housing demand; many transfers from inner London."),
        ('Keston',            'removals-keston.html',
         "Quiet Kent village near Bromley. Country-edge family homes; mostly straightforward access."),
        ('Otford',            'removals-otford.html',
         "Pretty Kent commuter village with rail links. Family homes and country properties balance."),
        ('Canterbury',        'removals-canterbury.html',
         "Cathedral city with extensive medieval streets. Listed properties, parking suspensions and pedestrian access are the standard considerations."),
        ('Whitstable',        'removals-whitstable.html',
         "Coastal town famous for oysters and the Old Neptune pub. Period cottages and coastal flats both feature."),
        ('Tenterden',         'removals-tenterden.html',
         "Pretty Wealden town with timber-framed cottages. Listed property handling with antiques is typical."),
        ('Maidstone',         'removals-maidstone.html',
         "Kent county town on the River Medway. Mix of urban and rural moves; consistent weekly volume."),
        ('West Malling',      'removals-west-malling.html',
         "Affluent Kent market town with substantial properties. Antiques and white-glove handling common."),
    ],
}


# Per-county narrative content (unique per page for Rules 6/11/25)
COUNTY = {
    'east-sussex': {
        'title':       'Removals in East Sussex – Local Sussex Movers Since 1982',
        'desc':        'Removals across East Sussex by Mark Ratcliffe Moving — BAR member, family-run since 1982, every town from Eastbourne to Rye covered weekly.',
        'h1':          'Removals in East Sussex – Local Sussex Movers Since 1982',
        'kicker':      'Local moves · 25 East Sussex towns · BAR since 1982',
        'hero_sub':    'Forty-plus years of moving East Sussex families. Every town in the county covered weekly from our depot at Lower Dicker.',
        'image':       '../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp',
        'intro': (
            "East Sussex is where Mark Ratcliffe Moving has built its forty-plus-year reputation. From our depot at Lower Dicker — just outside Hailsham and within a thirty-minute drive of every East Sussex town — we cover the full county every week of the year. Our crews know the narrow twittens of Hastings Old Town, the parking suspensions needed at Lewes High Street, the access lanes around Forest Row's country properties, and the bungalow-downsizing patterns of the coastal towns. Most weeks we handle between fifteen and twenty-five East Sussex moves, ranging from single-flat moves in Eastbourne to substantial period properties in Crowborough. We're a member of the British Association of Removers (BAR) and accredited to BS 8564, the international removals standard. Every job carries the BAR Advance Payment Guarantee."
        ),
        'whyus': (
            "Why move with Mark Ratcliffe in East Sussex? Three reasons customers cite most often. First, local knowledge: our drivers know the parking suspensions, the narrow lanes, the levels access points and the loading restrictions of every East Sussex town. Second, the right equipment — a mixed fleet that lets us send the right-sized lorry for the access (sometimes a 7.5-tonne curtain-sider for a country estate, sometimes a 3.5-tonne short-wheelbase for a Rye lane). Third, the team: most of our crew have been with us for years, often decades. They have packed crystal, wrapped mahogany, manoeuvred grand pianos, and arranged international shipping while you're still looking for the kettle on moving morning."
        ),
        'cost': (
            "What removals cost in East Sussex depends on three things: distance, volume, and access. A simple two-bedroom move within Eastbourne typically lands at £450-£650 including packing materials but excluding full pack-up service. A three-bedroom move from Eastbourne to elsewhere in the county is usually £700-£1,100. Country properties with long drives, multi-floor access, listed-building considerations, antiques or pianos all push the price up. We always provide a free in-person survey before quoting — phone-only estimates risk surprises on the day. Our pricing page sets out indicative hourly and per-job rates; BAR membership means your customer deposit is protected under the Advance Payment Guarantee."
        ),
        'movetypes': (
            "Common East Sussex move types: downsizing from family homes to coastal bungalows (very common around Peacehaven, Saltdean, Seaford and Bexhill); first-home purchases in Hailsham, Polegate or Willingdon; country-property moves around Crowborough, Heathfield, Mayfield and Wadhurst (often with antiques and pianos); and moves out of the county to London, Brighton &amp; Hove, the Midlands or overseas. We also handle around twenty annual moves into care homes and supported-living developments across East Sussex — a slower, more considered service that respects the resident's dignity and the continuity of familiar belongings."
        ),
        'breadcrumb_name': 'East Sussex',
    },
    'west-sussex': {
        'title':       'Removals in West Sussex – Coastal & Country Movers',
        'desc':        'Removals across West Sussex by Mark Ratcliffe Moving — Brighton, Worthing, Chichester, Horsham and South Downs villages. BAR member since 1982.',
        'h1':          'Removals in West Sussex – Coastal &amp; Country Movers',
        'kicker':      'Coast · City · South Downs · 24 West Sussex towns',
        'hero_sub':    'From Brighton Regency squares to Chichester listed properties and rural Sussex Weald homes — every West Sussex town, every week.',
        'image':       '../images/mark-ratcliffe-removal-fleet-vehicles-sussex.webp',
        'intro': (
            "West Sussex stretches from urban Brighton &amp; Hove and the busy A23 corridor through to the cathedral city of Chichester, the New Town of Crawley, and the rural South Downs villages between. Mark Ratcliffe Moving covers the full county from our Lower Dicker depot, with crews in Brighton, Worthing, Horsham and Haywards Heath most weeks of the year. We understand the parking suspension regimes around the Regency squares, the listed-building constraints in Chichester's four-streets quadrant, the access challenges of the rural Weald villages, and the high-volume estate-modern housing of Crawley. Our drivers and packers have been doing West Sussex moves for decades; many have favourite tea-stops between jobs in the South Downs villages."
        ),
        'whyus': (
            "Why customers choose Mark Ratcliffe for West Sussex moves. The county is geographically and architecturally varied — what works in a Crawley new-town semi is the opposite of what's needed for a listed Chichester property — and our advantage is the depth of crew experience to adapt. We dispatch the right vehicle (3.5-tonne short-wheelbase for narrow village lanes; 18-tonne articulated for Brighton multi-storey blocks) and the right team size. We carry BAR membership and BS 8564 accreditation, which means a transparent quote, a written contract, and the Advance Payment Guarantee on every deposit. Our customer rating across hundreds of post-move reviews stays consistently above 4.9 stars."
        ),
        'cost': (
            "Removals cost in West Sussex varies by access and distance. A typical three-bedroom Brighton flat to another Brighton property is £800-£1,400 with full pack and unpack; a Chichester listed-property move with antiques and careful crating runs higher because of the longer pack time. Country moves around Petworth or Midhurst tend to take longer because of antique-furniture handling. We always come for an in-person survey — phone quotes for West Sussex moves rarely capture the access realities. See the pricing page for indicative hourly rates and our packing-material rates. All deposits are protected by the BAR Advance Payment Guarantee."
        ),
        'movetypes': (
            "West Sussex move types we handle every week: city flat moves around Brighton &amp; Hove (often involving parking suspension paperwork and lift logistics), family-home moves in Worthing, Horsham and Haywards Heath, country-property moves in the South Downs villages (Midhurst, Petworth, Storrington, Amberley), commercial office relocations in Crawley (often Gatwick-adjacent), and overseas removals via the international removals team. Significant volume goes out of West Sussex toward London (especially from Crawley and Haywards Heath) and inward from London buyers reaching the more affordable rural markets."
        ),
        'extra_section_title': 'West Sussex transport and access notes',
        'extra_section_body': (
            "West Sussex is criss-crossed by the A23 (Brighton/London corridor), the A24 toward Horsham, the A29 west toward Bognor, and the south coast A27 — all routes we drive routinely. The county has plenty of access challenges that catch out unfamiliar removers: Brighton's narrow Lanes need a 3.5-tonne lorry not a 7.5-tonne; Chichester's Pallant House quadrant has resident-only parking on weekdays; Goodwood-week and Glorious Goodwood block certain country lanes; Horsham's Carfax is pedestrianised. We pre-survey every West Sussex job, lodge parking suspension paperwork with the local council in advance, and brief the crew on access constraints before the day. For listed properties (and West Sussex has many — particularly in Chichester, Arundel, Midhurst and Petworth) we work to conservation-officer guidance and the BAR listed-property handling protocol. Antique furniture, fine art, large mirrors and pianos all get specialist pad-wrap and custom-crate handling where appropriate."
        ),
        'breadcrumb_name': 'West Sussex',
    },
    'surrey': {
        'title':       'Removals in Surrey – Sussex-Based Commuter-Belt Movers',
        'desc':        'Removals across Surrey by Mark Ratcliffe Moving — Guildford, Woking, Weybridge and Surrey Hills villages. BAR member, Sussex-based.',
        'h1':          'Removals in Surrey – Sussex-Based Commuter-Belt Movers',
        'kicker':      'Commuter belt · 21 Surrey towns · Antique &amp; white-glove specialists',
        'hero_sub':    'Sussex-based, Surrey-experienced. From Guildford to Woking, Weybridge to Ascot, our crews cover the M25 commuter belt with white-glove care for wealthier homes.',
        'image':       '../images/mark-ratcliffe-sleeper-cab-removal-lorry.webp',
        'intro': (
            "Surrey is the heart of the London commuter belt — affluent market towns, the Surrey Hills AONB villages, and wealthy enclaves like Wentworth, Oxshott and Cobham. Mark Ratcliffe Moving works Surrey from our Sussex base; the Lower Dicker depot puts every Surrey town within a one-hour drive via the A22, M25 or A3. Most Surrey moves we handle involve substantial properties with antique furniture, fine art, pianos and high-value contents — areas where our specialist services (pad-wrap protection, custom timber crating, white-glove handling, insured high-value transit) come into their own. Our crew have moved family heirlooms into Virginia Water mansions and downsizers into Guildford apartment buildings; the breadth of property type is what makes Surrey work interesting. We carry the BAR Advance Payment Guarantee on every Surrey deposit, BS 8564 accreditation for the international jobs we handle from Surrey, and a written contract before any pack-up begins. Our pricing is in-person-surveyed every time — phone-only Surrey quotes routinely under-estimate the true scope, and we'd rather be slower and accurate than fast and wrong."
        ),
        'whyus': (
            "Why a Sussex-based remover for Surrey moves? Three things matter. First, Mark Ratcliffe is a BAR-accredited specialist with decades of experience handling the antique furniture and fine-art content that wealthier Surrey homes typically include — that's not standard for every removals firm. Second, we charge transparent, in-person-surveyed quotes with no hidden mileage premium, which routinely comes out competitive against London-based removers for the round trip from anywhere south of the M25. Third, the team: our drivers and packers stay with us for years, often decades. They know how to wrap a chesterfield without tearing the leather, how to manoeuvre a Steinway B down a winding staircase, and how to load a customer's wine collection without breaking the cooling chain. Add the BAR Advance Payment Guarantee, the BS 8564 accreditation, the full-rate insurance options, and a long-tenure crew that takes care of customers' belongings the way they'd take care of their own — and Surrey customers see the value clearly."
        ),
        'cost': (
            "Surrey removals costs reflect access, distance from our Sussex base, and the specialist handling typically required. A standard three-bedroom move within Surrey runs £900-£1,500 fully packed and unpacked; a substantial seven-bedroom country house with antiques, fine art and a grand piano can run into multiple days and several thousand pounds. We do not apply a per-mile premium for Surrey; our quote reflects the actual day rate of crew and vehicle, plus packing materials at cost. Specialist handling — pad-wrap protection, custom crating for art and mirrors, climate-stable transit for antiques — is itemised separately so you can see exactly what each element costs. As with all our work, the BAR Advance Payment Guarantee protects your deposit, you have a written contract before we lift a single box, and our liability cover meets the BAR standard for full replacement value if you opt in."
        ),
        'movetypes': (
            "Surrey move types we handle every month: substantial-property moves around Cobham, Oxshott, Esher, Weybridge and Virginia Water (white-glove standard, multi-day pack-up sequence, specialist handling for antiques and art); commuter-town family moves around Guildford, Woking, Reigate and Redhill (typically two-to-three-day pack-and-move); downsizes from larger Surrey Hills properties to smaller homes (often involving careful inventory of treasured items that must travel with the customer, plus disposal arrangements for what's left behind); and a significant volume of long-distance moves OUT of Surrey to second homes on the Sussex coast, in the West Country, or overseas via our international team to Australia, Thailand, Canada or the EU. Office relocations are also routine in Woking, Guildford and the Crawley-bordering commercial parks — we handle them out-of-hours where the IT cutover demands a Sunday move."
        ),
        'extra_section_title': 'Surrey transport links and access notes',
        'extra_section_body': (
            "Surrey is well-served by the M25, the M3, the A3 and the A22 — every Surrey town from our Sussex base is inside a one-hour drive in normal traffic. The wealthier villages (Cobham, Oxshott, Esher, Virginia Water) have substantial driveways and easy access; the Surrey Hills villages (Holmbury St Mary, Peaslake, the Horsleys) have narrow lanes that need a smaller lorry. The commuter towns (Guildford, Woking, Reigate, Redhill) have residents' parking schemes that need suspension paperwork lodged a few days in advance — we handle the paperwork. For the gated Wentworth and St George's Hill estates, we coordinate with estate security in advance so the lorry can enter on schedule. Antique furniture, fine art, pianos and high-value contents are typical in Surrey jobs; full pad-wrap protection, custom crating and the BAR full-replacement-value insurance option are routinely used."
        ),
        'breadcrumb_name': 'Surrey',
    },
    'kent': {
        'title':       'Removals in Kent – Garden of England Movers from Sussex',
        'desc':        'Removals across Kent by Mark Ratcliffe Moving — Tunbridge Wells, Maidstone, Canterbury, Sevenoaks and Bromley. BAR member, Sussex-based.',
        'h1':          'Removals in Kent – Garden of England Movers',
        'kicker':      'Garden of England · 14 Kent towns · Listed &amp; country properties',
        'hero_sub':    'From the Pantiles in Tunbridge Wells to medieval Canterbury, the Wealden villages to south-east London suburbs — our Sussex crews work Kent weekly.',
        'image':       '../images/mark-ratcliffe-crew-loading-piano-eastbourne.webp',
        'intro': (
            "Kent — the Garden of England — combines pretty Wealden villages, listed Royal spa towns like Tunbridge Wells, the cathedral city of Canterbury, the county-town centre of Maidstone, and the densely populated south-east London suburbs of Bromley, Beckenham and Chislehurst. Mark Ratcliffe Moving covers Kent from our Sussex base at Lower Dicker, with crews in the county every week of the year. Many of our Kent jobs involve listed properties, antique furniture and the cobble-and-courtyard access that has to be surveyed in person. We are BAR-accredited and BS 8564 standard; every Kent deposit is covered by the Advance Payment Guarantee. The travel times from our Lower Dicker depot put almost every Kent town inside a one-hour radius — Tunbridge Wells is around forty minutes via the A21, Maidstone an hour via the A26, Canterbury an hour and ten via the A28, and the south-east London suburbs (Bromley, Beckenham, Chislehurst) are roughly an hour fifteen depending on M25 traffic. We do not apply a per-mile premium for Kent moves; the quote reflects the actual day rate of crew and vehicle, not the distance."
        ),
        'whyus': (
            "Why Mark Ratcliffe for Kent? Our Sussex depot is closer to most Kent towns than customers expect, and the absence of a London-overhead means our quotes routinely come out below comparable London-based firms doing the same round trip. We have specialist experience with listed properties, antiques and pianos — exactly the kind of contents you find in Tunbridge Wells, Sevenoaks, Tenterden and the rural Wealden villages — and our crew have been packing these belongings for decades. We carry the BAR-accredited paperwork to back the move: the written contract, transparent pricing, the Advance Payment Guarantee that protects your deposit, and the BS 8564 international-removals accreditation for the overseas Kent moves we handle several times a month. Add a long-tenure crew that's seen everything, a mixed fleet that lets us dispatch the right-sized lorry for the access, and a customer rating consistently above 4.9 stars across hundreds of post-move reviews."
        ),
        'cost': (
            "Kent removals cost depends on access, the listed-property quotient, and distance from our Sussex base. A standard three-bedroom Tunbridge Wells move is typically £800-£1,300 fully packed; a substantial Sevenoaks country house with antiques is £1,500-£3,000+. South-east London suburb moves to or from Bromley, Beckenham and Chislehurst run similar to inner-London prices because of access and parking complexity, not because of mileage. Cottage moves in Tenterden, Westerham and Otford typically include antique-furniture handling — itemised separately on the quote so you can see what each element costs. As with every Mark Ratcliffe job, the BAR Advance Payment Guarantee protects your deposit, you have a written contract before we lift a single box, and the liability cover meets the BAR standard for full replacement value if you opt in. Our pricing page sets out the indicative hourly and per-job framework."
        ),
        'movetypes': (
            "Kent moves we handle most weeks: listed-property moves in Tunbridge Wells, Sevenoaks, Tenterden and Canterbury (always pre-surveyed in person, always with antique handling, often with road-closure paperwork); family-home moves in Maidstone, Tonbridge and the wider Medway towns; high-volume suburban moves in Bromley, Beckenham and Chislehurst (where lift logistics and parking suspension paperwork dominate the planning); overseas removals via the international team — Kent customers move to Australia, Thailand, the EU, the USA and Canada most months — and office relocations around Maidstone, Tunbridge Wells and the south-east London commercial centres. Specialist services like white-glove handling, custom timber crating for art and mirrors, and pad-wrap protection for antique furniture get heavy use across the listed-property-rich Wealden parts of the county."
        ),
        'extra_section_title': 'Kent transport links and access notes',
        'extra_section_body': (
            "Kent is well-connected from our Sussex base. The A21 takes us straight to Tunbridge Wells and on toward Hastings; the A26 reaches Maidstone via Tonbridge; the A28 runs through Ashford to Canterbury. The M25 ring road handles the south-east London suburbs. Our drivers know which routes work for different vehicle sizes — the 18-tonne articulated does not fit every Wealden lane, so we send the right combination of lorry and crew for each Kent town. Parking is one of the bigger access challenges in Kent: Tunbridge Wells, Sevenoaks and Canterbury all have residents' parking schemes that require suspension paperwork lodged days in advance. The south-east London suburbs (Bromley, Beckenham, Chislehurst) require London-style parking suspensions through the local councils; we handle the paperwork for every customer. For listed properties, we additionally check with the conservation officer if there are any specific handling restrictions on doors, frames or floor coverings — every Kent listed-property move gets a pre-survey, and the crew is briefed on the specifics before the day."
        ),
        'breadcrumb_name': 'Kent',
    },
}


# ----------------------------------------------------------------------------
# Build a sample HTML chrome from an existing /areas-covered/ page so the
# navbar + footer match the rest of the site exactly. We just need head <meta>
# essentials, the nav, and the footer wrapper.
# ----------------------------------------------------------------------------
SAMPLE_PATH = 'areas-covered/removals-eastbourne.html'


def extract(html: str, pattern: str) -> str:
    m = re.search(pattern, html, re.S)
    return m.group(1) if m else ''


def page_html(slug: str, cfg: dict, towns: list[tuple]) -> str:
    sample = open(SAMPLE_PATH, encoding='utf-8').read()
    # The chrome we need: from <body> through end of navbar (the .nav-section), and the entire <footer>...</footer>.
    nav_m = re.search(r'(<body>.*?</div>\s*</div>\s*</div>)', sample, re.S)
    navbar = nav_m.group(1) if nav_m else '<body>'
    footer_m = re.search(r'(<footer class="mr-footer".*?</footer>)', sample, re.S)
    footer = footer_m.group(1) if footer_m else ''
    csp_m = re.search(r'(<meta http-equiv="Content-Security-Policy"[^>]+>)', sample)
    ref_m = re.search(r'(<meta name="referrer"[^>]+>)', sample)
    csp = csp_m.group(1) if csp_m else ''
    referrer = ref_m.group(1) if ref_m else ''

    canon = f'{BASE_URL}/areas-covered/{slug}.html'
    image_abs = cfg["image"].replace('../', f'{BASE_URL}/')

    # Towns markup
    town_items = []
    for name, town_slug, desc in towns:
        town_items.append(
            f'        <article class="np-county-town">\n'
            f'          <h3><a href="{town_slug}">{name}</a></h3>\n'
            f'          <p>{desc}</p>\n'
            f'        </article>'
        )
    towns_html = '\n'.join(town_items)

    # Cross-links to other counties for breadth (and to clear Rule 3)
    other_counties = []
    for k, c in COUNTY.items():
        if k == slug: continue
        other_counties.append(f'        <li><a href="{k}.html">Removals in {c["breadcrumb_name"]}</a></li>')
    other_counties_html = '\n'.join(other_counties)

    body = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['desc']}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving &amp; Storage">
  <meta name="theme-color" content="#4d2e8f">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['desc']}">
  <meta property="og:image" content="{image_abs}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving &amp; Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://cdn.yoshki.com" crossorigin>
  <link href="../css/normalize.css?v=20260560" rel="stylesheet">
  <link href="../css/components.css?v=20260560" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260560" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260560" rel="stylesheet">
  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>WebFont.load({{classes:true,timeout:2000,google:{{families:["Inter:400,500,600,700,800","Fraunces:400,500,600,700"]}}}});;</script>
  <link href="../images/favicon.png" rel="shortcut icon">
  <link href="../images/webclip.png" rel="apple-touch-icon">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q111LKQEBP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-Q111LKQEBP');</script>
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}/"}}, {{"@type": "ListItem", "position": 2, "name": "Areas covered", "item": "{BASE_URL}/areas-covered/"}}, {{"@type": "ListItem", "position": 3, "name": "{cfg['breadcrumb_name']}"}}]}}</script>
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "CollectionPage", "name": "{cfg['breadcrumb_name']} removals", "description": "{cfg['desc']}", "url": "{canon}", "publisher": {{"@type": "Organization", "@id": "{BASE_URL}/#organization"}}}}</script>
  <link rel="canonical" href="{canon}">
  <meta property="og:url" content="{canon}">
  {csp}
  {referrer}
</head>
{navbar}

  <header class="np-hero">
    <div class="np-hero-inner">
      <div class="np-kicker">{cfg['kicker']}</div>
      <h1>{cfg['h1']}</h1>
      <p class="np-hero-sub">{cfg['hero_sub']}</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="{cfg['image']}" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high" width="1800" height="1350">
  </header>

  <nav class="np-breadcrumb" aria-label="Breadcrumb"><a href="../">Home</a> &rsaquo; <a href="./">Areas covered</a> &rsaquo; {cfg['breadcrumb_name']}</nav>

  <section class="np-section">
    <div class="np-inner">
      <p style="font-size:1.15rem;">{cfg['intro']}</p>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Towns we cover in {cfg['breadcrumb_name']}</h2>
      <p>Click any town name for the full local removals page — covered postcodes, typical move types, access notes and customer reviews.</p>
      <div class="np-county-towns">
{towns_html}
      </div>
    </div>
  </section>

  <section class="np-section">
    <div class="np-inner">
      <h2>Why move with Mark Ratcliffe in {cfg['breadcrumb_name']}</h2>
      <p>{cfg['whyus']}</p>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>{cfg['breadcrumb_name']} removals cost guide</h2>
      <p>{cfg['cost']}</p>
      <p>For the full pricing breakdown, see our <a href="../resources/pricing.html">removals pricing guide</a> and our <a href="../resources/removals-eastbourne-cost.html">cost guide for Sussex moves</a>.</p>
    </div>
  </section>

  <section class="np-section">
    <div class="np-inner">
      <h2>Common move types in {cfg['breadcrumb_name']}</h2>
      <p>{cfg['movetypes']}</p>
      <p>If you're planning any of these, our <a href="../services/">services hub</a> lists every service in detail — from <a href="../services/full-packing-service.html">full packing</a> to <a href="../services/piano-moving.html">piano moving</a> and <a href="../services/international-removals-eastbourne.html">international relocation</a>.</p>
    </div>
  </section>

  {('<section class="np-section np-section-soft"><div class="np-inner"><h2>' + cfg['extra_section_title'] + '</h2><p>' + cfg['extra_section_body'] + '</p></div></section>') if cfg.get('extra_section_title') else ''}

  <section class="np-section np-section-soft" aria-label="Other counties">
    <div class="np-inner">
      <h2>Other counties we cover</h2>
      <ul class="np-related-list">
{other_counties_html}
        <li><a href="./">All areas covered</a></li>
        <li><a href="../resources/helpful-tips.html">Helpful moving tips</a></li>
        <li><a href="../resources/faqs.html">Frequently asked questions</a></li>
        <li><a href="../resources/gallery.html">Recent moves gallery</a></li>
        <li><a href="../reviews.html">Customer reviews</a></li>
      </ul>
    </div>
  </section>

  <section class="np-section np-cta-block">
    <div class="np-inner">
      <h2>Plan your {cfg['breadcrumb_name']} move</h2>
      <p>Use the free quote form for an instant indicative price, or call us on <a href="tel:01323848008">01323 848 008</a> for a free in-person survey. We respond within 48 hours.</p>
      <div class="np-cta-row">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
  </section>

  {footer}
</body>
</html>
"""
    return body


def main() -> int:
    if not os.path.isfile(SAMPLE_PATH):
        print(f'ERROR — sample page {SAMPLE_PATH} missing', file=sys.stderr)
        return 1
    for slug, cfg in COUNTY.items():
        towns = TOWNS[slug]
        # Verify every town slug exists
        missing = [s for _, s, _ in towns if not os.path.isfile(f'areas-covered/{s}')]
        if missing:
            print(f'WARN — {slug}: missing town slugs {missing[:3]}…', file=sys.stderr)
        html = page_html(slug, cfg, towns)
        out = f'areas-covered/{slug}.html'
        open(out, 'w', encoding='utf-8').write(html)
        wc = len(re.sub(r'<[^>]+>', ' ', html).split())
        print(f'  wrote {out} ({wc} words, {len(towns)} towns)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
