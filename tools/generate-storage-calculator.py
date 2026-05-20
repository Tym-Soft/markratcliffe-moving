#!/usr/bin/env python3
"""
Generate /resources/storage-calculator.html — interactive volume +
weight calculator. Redesigned layout:

  • Horizontal category tab bar with simple SVG icons (scrollable)
  • Search input that filters items inside the active category
  • Each item row has a − / qty / + stepper instead of a plain input
  • 13 categories covering every typical room + spaces (~200 items)

Item volumes are BAR-style inventory estimates that the Mark Ratcliffe
Moving crews use to plan a Sussex job. They are deliberately rounded.
For an accurate quote the customer still books a free in-home survey.
"""

from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE_URL = 'https://www.markratcliffemoving.co.uk'

# ----------------------------------------------------------------------
# Simple inline-SVG icons, viewBox 0 0 40 40, stroke=currentColor 1.5
# Keep them recognisable but small — clean line drawings.
# ----------------------------------------------------------------------
ICON_BOXES = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="4" y="14" width="14" height="14" rx="1"/><rect x="22" y="14" width="14" height="14" rx="1"/><rect x="13" y="6" width="14" height="10" rx="1"/></svg>'
ICON_HALL = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M10 34V14a6 6 0 0 1 6-6h8a6 6 0 0 1 6 6v20"/><line x1="6" y1="34" x2="34" y2="34"/><circle cx="24" cy="22" r="0.8" fill="currentColor"/></svg>'
ICON_LIVING = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 24v6h28v-6"/><path d="M8 24v-6a3 3 0 0 1 3-3h18a3 3 0 0 1 3 3v6"/><path d="M11 24v-4h18v4"/></svg>'
ICON_DINING = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><line x1="6" y1="22" x2="34" y2="22"/><line x1="10" y1="22" x2="10" y2="32"/><line x1="30" y1="22" x2="30" y2="32"/><circle cx="20" cy="16" r="3"/><line x1="20" y1="19" x2="20" y2="22"/></svg>'
ICON_KITCHEN = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="6" y="10" width="28" height="22" rx="1"/><line x1="6" y1="18" x2="34" y2="18"/><circle cx="13" cy="25" r="2.5"/><circle cx="27" cy="25" r="2.5"/></svg>'
ICON_CONSERV = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 34V18l14-10 14 10v16"/><line x1="20" y1="8" x2="20" y2="34"/><line x1="6" y1="22" x2="34" y2="22"/></svg>'
ICON_BATHROOM = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 22h28v6a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4v-6Z"/><path d="M10 22v-8a3 3 0 0 1 6 0"/><line x1="6" y1="34" x2="10" y2="36"/><line x1="34" y1="34" x2="30" y2="36"/></svg>'
ICON_BEDROOM = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 28v-4a4 4 0 0 1 4-4h22a4 4 0 0 1 4 4v4"/><line x1="5" y1="28" x2="35" y2="28"/><line x1="5" y1="32" x2="35" y2="32"/><rect x="11" y="16" width="9" height="4" rx="1.5"/></svg>'
ICON_KIDS = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 28v-3a3 3 0 0 1 3-3h22a3 3 0 0 1 3 3v3"/><line x1="6" y1="28" x2="34" y2="28"/><path d="M30 16l1.6 3.3 3.6.5-2.6 2.5.6 3.6-3.2-1.7-3.2 1.7.6-3.6-2.6-2.5 3.6-.5z"/></svg>'
ICON_OFFICE = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="6" y="9" width="22" height="14" rx="1"/><line x1="14" y1="23" x2="14" y2="27"/><line x1="20" y1="23" x2="20" y2="27"/><line x1="11" y1="27" x2="23" y2="27"/><rect x="29" y="18" width="6" height="14" rx="0.5"/></svg>'
ICON_GARAGE = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 34V14l14-8 14 8v20"/><rect x="11" y="20" width="18" height="14"/><line x1="11" y1="26" x2="29" y2="26"/></svg>'
ICON_GARDEN = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="20" cy="14" r="6"/><path d="M14 18a8 8 0 0 0 12 0"/><line x1="20" y1="20" x2="20" y2="34"/><line x1="14" y1="34" x2="26" y2="34"/></svg>'
ICON_SPECIAL = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="6" y="14" width="28" height="14" rx="1"/><line x1="12" y1="14" x2="12" y2="22"/><line x1="16" y1="14" x2="16" y2="22"/><line x1="20" y1="14" x2="20" y2="22"/><line x1="24" y1="14" x2="24" y2="22"/><line x1="28" y1="14" x2="28" y2="22"/><line x1="6" y1="22" x2="34" y2="22"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="6"/><line x1="15.5" y1="15.5" x2="20" y2="20"/></svg>'


# Each entry: (display name, icon SVG, [(item name, cuft, cum, kg), …])
ITEMS: list[tuple[str, str, list[tuple[str, float, float, float]]]] = [
    ('Boxes & cartons', ICON_BOXES, [
        ('Tea-chest box (4.5 cu ft)',         4.5, 0.13, 15),
        ('Standard removals box (medium)',     3, 0.08, 12),
        ('Book box (1.5 cu ft)',               1.5, 0.04, 15),
        ('Linen box (large)',                  6, 0.17, 10),
        ('Wardrobe carton (tall)',             6, 0.17, 15),
        ('Wardrobe carton (mini)',             3, 0.08,  8),
        ('Plastic crate (large)',              4, 0.11, 12),
        ('Picture box (large flat)',           3, 0.08,  5),
        ('Bag / holdall',                      2, 0.06,  8),
        ('Suitcase (large)',                   4, 0.11, 15),
        ('Suitcase (small)',                   2, 0.06,  8),
        ('Vacuum-pack bag (clothes)',          2, 0.06,  5),
    ]),
    ('Hall / Foyer', ICON_HALL, [
        ('Hall table',                        10, 0.28, 20),
        ('Console table',                     12, 0.34, 25),
        ('Coat rack / stand',                  6, 0.17,  8),
        ('Umbrella stand',                     3, 0.08,  5),
        ('Shoe rack, small',                   4, 0.11, 10),
        ('Shoe rack, large',                   8, 0.23, 18),
        ('Hall mirror',                        5, 0.14, 12),
        ('Hall runner / rug',                  4, 0.11,  8),
        ('Boot bench',                        10, 0.28, 18),
        ('Hall cabinet',                      15, 0.42, 35),
        ('Freestanding coat cupboard',        20, 0.57, 45),
    ]),
    ('Living room', ICON_LIVING, [
        ('Sofa, 3-seater',                    35, 0.99, 50),
        ('Sofa, 2-seater',                    25, 0.71, 40),
        ('Sofa, corner',                      50, 1.42, 70),
        ('Sofa bed (2-seater)',               30, 0.85, 65),
        ('Sofa bed (3-seater)',               40, 1.13, 80),
        ('Armchair',                          15, 0.42, 25),
        ('Recliner chair',                    18, 0.51, 35),
        ('Footstool / ottoman',                4, 0.11,  5),
        ('Coffee table',                       8, 0.23, 15),
        ('Side / lamp table',                  4, 0.11,  8),
        ('Nest of tables',                     6, 0.17, 12),
        ('TV, large (50"+)',                   6, 0.17, 12),
        ('TV, small (under 40")',              3, 0.08,  7),
        ('TV unit / stand',                   10, 0.28, 25),
        ('Bookcase, small',                   12, 0.34, 25),
        ('Bookcase, large',                   20, 0.57, 40),
        ('Sideboard',                         18, 0.51, 45),
        ('Display cabinet',                   22, 0.62, 50),
        ('Drinks cabinet',                    14, 0.40, 30),
        ('Wine rack',                          6, 0.17, 12),
        ('Piano stool',                        3, 0.08,  8),
        ('Stereo HiFi (stack)',                8, 0.23, 25),
        ('Stereo, mini',                       3, 0.08,  8),
        ('Games console',                      2, 0.06,  5),
        ('Speakers (pair, floor-standing)',   10, 0.28, 25),
        ('Speakers (pair, bookshelf)',         4, 0.11, 10),
        ('Floor lamp',                         6, 0.17,  8),
        ('Table lamp',                         2, 0.06,  3),
        ('Rug, rolled (large)',                5, 0.14, 10),
        ('Rug, rolled (small)',                3, 0.08,  5),
        ('Mirror, large',                      5, 0.14, 12),
        ('Mirror, small',                      2, 0.06,  4),
        ('Curtains (pair)',                    3, 0.08,  6),
        ('Pot plant, large',                   6, 0.17, 15),
        ('Pot plant, small',                   2, 0.06,  4),
    ]),
    ('Dining room', ICON_DINING, [
        ('Dining table, 6-seater',            25, 0.71, 40),
        ('Dining table, 4-seater',            18, 0.51, 30),
        ('Dining table, 8-seater',            35, 0.99, 55),
        ('Dining table, extending',           30, 0.85, 45),
        ('Dining chair',                       5, 0.14,  5),
        ('Carver chair',                       7, 0.20,  8),
        ('Welsh dresser',                     30, 0.85, 75),
        ('Sideboard',                         22, 0.62, 50),
        ('China cabinet',                     25, 0.71, 60),
        ('Drinks trolley',                     6, 0.17, 15),
        ('Display cabinet',                   22, 0.62, 50),
        ('Wine rack',                          6, 0.17, 12),
        ('Floor lamp',                         6, 0.17,  8),
        ('Rug, rolled',                        5, 0.14, 10),
    ]),
    ('Kitchen / utility', ICON_KITCHEN, [
        ('Fridge-freezer, American',          30, 0.85, 90),
        ('Fridge-freezer, tall',              22, 0.62, 70),
        ('Fridge, undercounter',               8, 0.23, 30),
        ('Freezer, chest',                    15, 0.42, 50),
        ('Freezer, upright',                  12, 0.34, 45),
        ('Washing machine',                    8, 0.23, 70),
        ('Tumble dryer',                       8, 0.23, 35),
        ('Washer-dryer combo',                 9, 0.25, 75),
        ('Dishwasher',                         8, 0.23, 50),
        ('Cooker, freestanding',              12, 0.34, 60),
        ('Range cooker',                      25, 0.71,120),
        ('Microwave',                          3, 0.08, 12),
        ('Kitchen table',                     15, 0.42, 25),
        ('Kitchen chair',                      4, 0.11,  4),
        ('Bar stool',                          6, 0.17,  8),
        ('Kettle',                             1, 0.03,  2),
        ('Toaster',                            1, 0.03,  2),
        ('Stand mixer / food processor',       2, 0.06,  8),
        ('Vacuum cleaner',                     5, 0.14,  8),
        ('Ironing board',                      4, 0.11,  6),
        ('Mop &amp; bucket',                   3, 0.08,  4),
        ('Recycling bins (set)',               6, 0.17,  8),
    ]),
    ('Conservatory', ICON_CONSERV, [
        ('Conservatory sofa, 3-seat',         30, 0.85, 40),
        ('Conservatory sofa, 2-seat',         22, 0.62, 30),
        ('Conservatory armchair',             14, 0.40, 22),
        ('Coffee table, low',                  8, 0.23, 15),
        ('Wicker chair',                      12, 0.34, 12),
        ('Wicker sofa',                       25, 0.71, 30),
        ('Conservatory dining table',         18, 0.51, 30),
        ('Cane chair',                        10, 0.28, 10),
        ('Pot plants (large)',                 6, 0.17, 15),
        ('Garden swing seat',                 30, 0.85, 40),
    ]),
    ('Bathroom', ICON_BATHROOM, [
        ('Linen basket',                       4, 0.11,  6),
        ('Bath rack',                          1, 0.03,  2),
        ('Storage shelves',                    8, 0.23, 15),
        ('Vanity unit',                       12, 0.34, 35),
        ('Bathroom cabinet',                   6, 0.17, 18),
        ('Towel rail, freestanding',           4, 0.11,  8),
        ('Toilet brush stand',                 1, 0.03,  2),
        ('Wall mirror',                        4, 0.11, 10),
        ('Plant stand',                        3, 0.08,  6),
        ('Bathroom stool',                     3, 0.08,  5),
        ('Weighing scales',                    1, 0.03,  3),
    ]),
    ('Bedroom (master)', ICON_BEDROOM, [
        ('Bed, super-king (mattress only)',   35, 0.99, 30),
        ('Bed, super-king (base only)',       30, 0.85, 45),
        ('Bed, king (mattress only)',         30, 0.85, 25),
        ('Bed, king (base only)',             25, 0.71, 40),
        ('Bed, double (mattress only)',       22, 0.62, 20),
        ('Bed, double (base only)',           20, 0.57, 35),
        ('Headboard, single',                  6, 0.17, 15),
        ('Headboard, double',                 10, 0.28, 22),
        ('Headboard, king',                   12, 0.34, 28),
        ('Wardrobe, single',                  22, 0.62, 45),
        ('Wardrobe, double',                  35, 0.99, 75),
        ('Wardrobe, triple',                  50, 1.42,110),
        ('Chest of drawers, small',           14, 0.40, 30),
        ('Chest of drawers, large',           20, 0.57, 45),
        ('Bedside table',                      6, 0.17, 12),
        ('Dressing table',                    18, 0.51, 35),
        ('Dressing table mirror',              5, 0.14, 12),
        ('Vanity stool',                       4, 0.11,  6),
        ('Blanket box / ottoman',             10, 0.28, 20),
        ('Bedroom chair',                     12, 0.34, 20),
        ('Mirror, full-length',                6, 0.17, 15),
    ]),
    ('Kids bedroom', ICON_KIDS, [
        ('Bed, single (mattress only)',       14, 0.40, 12),
        ('Bed, single (base only)',           13, 0.37, 25),
        ('Bunk bed (full set)',               35, 0.99, 50),
        ('Cabin bed',                         30, 0.85, 60),
        ('Cot / crib',                        14, 0.40, 15),
        ('Toddler bed',                       18, 0.51, 25),
        ('Junior wardrobe',                   18, 0.51, 35),
        ('Chest of drawers, kids',            14, 0.40, 30),
        ('Bookshelf',                         12, 0.34, 25),
        ('Toy chest',                          8, 0.23, 15),
        ('Kids desk',                         12, 0.34, 25),
        ('Kids desk chair',                    6, 0.17, 10),
        ('Kids bedside table',                 6, 0.17, 12),
        ('Bean bag',                           5, 0.14,  4),
        ('Storage cube unit',                 14, 0.40, 25),
        ('Rocking horse',                      8, 0.23, 15),
        ('Doll house',                         8, 0.23, 12),
    ]),
    ('Office / study', ICON_OFFICE, [
        ('Desk',                              18, 0.51, 35),
        ('Office chair',                       8, 0.23, 12),
        ('Filing cabinet, 2-drawer',          10, 0.28, 30),
        ('Filing cabinet, 4-drawer',          18, 0.51, 50),
        ('Computer (desktop tower)',           4, 0.11, 10),
        ('Monitor',                            3, 0.08,  8),
        ('Printer',                            4, 0.11,  8),
        ('Bookcase, office',                  18, 0.51, 35),
        ('Shredder',                           3, 0.08, 10),
        ('Office safe (small)',                8, 0.23, 80),
        ('Whiteboard / pin board',             4, 0.11,  8),
        ('Photocopier (small)',               12, 0.34, 40),
    ]),
    ('Garage / shed', ICON_GARAGE, [
        ('Tool box',                           4, 0.11, 15),
        ('Toolbox (large rolling)',           12, 0.34, 45),
        ('Workbench',                         25, 0.71, 60),
        ('Lawnmower, push',                    8, 0.23, 15),
        ('Lawnmower, ride-on',                35, 0.99, 90),
        ('Strimmer / weed whacker',            4, 0.11,  8),
        ('Hedge trimmer',                      3, 0.08,  6),
        ('Chainsaw',                           3, 0.08,  8),
        ('Wheelbarrow',                       12, 0.34, 20),
        ('Bicycle',                           12, 0.34, 15),
        ('Motorbike',                         60, 1.70,180),
        ('Camping equipment (boxed)',         10, 0.28, 25),
        ('Extension ladders',                 14, 0.40, 18),
        ('Step ladder',                        6, 0.17, 10),
        ('Garden hose &amp; reel',             4, 0.11,  8),
        ('Pressure washer',                    5, 0.14, 15),
    ]),
    ('Garden &amp; outdoor', ICON_GARDEN, [
        ('BBQ, kettle',                        8, 0.23, 18),
        ('BBQ, large gas',                    18, 0.51, 40),
        ('Patio table',                       18, 0.51, 35),
        ('Patio chair (folding)',              4, 0.11,  4),
        ('Patio chair (rigid)',                6, 0.17,  8),
        ('Garden bench',                      14, 0.40, 30),
        ('Parasol / umbrella',                 5, 0.14,  8),
        ('Patio heater',                       8, 0.23, 15),
        ('Garden tools (set)',                 6, 0.17, 15),
        ('Plant pot, large',                   4, 0.11, 25),
        ('Plant pot, medium',                  2, 0.06, 10),
        ('Trampoline (medium)',               50, 1.42, 60),
        ('Slide / climbing frame',            60, 1.70, 80),
        ('Sun lounger',                       15, 0.42, 18),
        ('Garden shed (flat-pack)',           60, 1.70,120),
    ]),
    ('Specialist &amp; other', ICON_SPECIAL, [
        ('Piano, upright',                    65, 1.84,250),
        ('Piano, baby grand',                 90, 2.55,300),
        ('Piano, grand',                     110, 3.11,400),
        ('Pool table (full size)',            60, 1.70,200),
        ('Snooker table',                     70, 1.98,250),
        ('Safe, small',                        8, 0.23, 80),
        ('Safe, large',                       25, 0.71,200),
        ('Treadmill',                         25, 0.71, 80),
        ('Exercise bike',                     12, 0.34, 30),
        ('Cross-trainer',                     25, 0.71, 65),
        ('Multi-gym',                         50, 1.42,120),
        ('Rowing machine',                    18, 0.51, 40),
        ('Aquarium (empty)',                  10, 0.28, 25),
        ('Antique chest (large)',             20, 0.57, 60),
        ('Grandfather clock',                 18, 0.51, 60),
        ('Statue / sculpture',                 8, 0.23, 30),
        ('Hot tub (portable)',                50, 1.42,120),
        ('Quad bike',                         70, 1.98,200),
    ]),
]


def slugify(s: str) -> str:
    s = re.sub(r'&[a-z]+;', '-', s.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


SAMPLE_PATH = 'resources/pricing.html'


def page_html() -> str:
    sample = open(SAMPLE_PATH, encoding='utf-8').read()
    nav_m = re.search(r'<body>(.*?)<header class="np-hero"', sample, re.S)
    navbar = '<body>' + nav_m.group(1) if nav_m else '<body>'
    navbar = re.sub(r'\s*<nav class="np-breadcrumb"[^>]*>.*?</nav>\s*', '\n  ', navbar, flags=re.S)
    footer_m = re.search(r'(<footer class="mr-footer".*?</footer>)', sample, re.S)
    footer = footer_m.group(1) if footer_m else ''
    csp_m = re.search(r'(<meta http-equiv="Content-Security-Policy"[^>]+>)', sample)
    csp = csp_m.group(1) if csp_m else ''
    ref_m = re.search(r'(<meta name="referrer"[^>]+>)', sample)
    referrer = ref_m.group(1) if ref_m else ''

    n_items = sum(len(items) for _, _, items in ITEMS)

    # Build tab bar + panels
    tab_buttons: list[str] = []
    panels: list[str] = []
    for idx, (cat_name, icon_svg, items) in enumerate(ITEMS):
        slug = 'cat-' + slugify(cat_name)
        active = ' active' if idx == 0 else ''
        aria_selected = 'true' if idx == 0 else 'false'
        tab_buttons.append(
            f'        <button type="button" class="calc-tab{active}" role="tab" id="tab-{slug}" '
            f'aria-controls="{slug}" aria-selected="{aria_selected}" data-target="{slug}">\n'
            f'          <span class="calc-tab-icon">{icon_svg}</span>\n'
            f'          <span class="calc-tab-label">{cat_name}</span>\n'
            f'        </button>'
        )
        rows: list[str] = []
        for name, cuft, cum, kg in items:
            inp_id = 'item-' + slug + '-' + slugify(name)
            rows.append(
                f'          <div class="calc-item">\n'
                f'            <div class="calc-item-text">\n'
                f'              <span class="calc-item-name">{name}</span>\n'
                f'              <span class="calc-item-vol">{cuft} cu ft &middot; {cum} cu m &middot; {int(kg)} kg</span>\n'
                f'            </div>\n'
                f'            <div class="qty-stepper">\n'
                f'              <button type="button" class="qty-btn qty-dec" aria-label="Decrease quantity of {name}">&minus;</button>\n'
                f'              <input id="{inp_id}" type="number" min="0" value="0" data-cuft="{cuft}" data-cum="{cum}" data-kg="{kg}" aria-label="Quantity of {name}">\n'
                f'              <button type="button" class="qty-btn qty-inc" aria-label="Increase quantity of {name}">+</button>\n'
                f'            </div>\n'
                f'          </div>'
            )
        rows_html = '\n'.join(rows)
        panels.append(
            f'        <div class="calc-cat-panel{active}" id="{slug}" role="tabpanel" '
            f'aria-labelledby="tab-{slug}">\n'
            f'{rows_html}\n'
            f'        </div>'
        )
    tabs_html = '\n'.join(tab_buttons)
    panels_html = '\n'.join(panels)

    canon = f'{BASE_URL}/resources/storage-calculator.html'

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>Storage Calculator – Cubic Feet, Cubic Meters &amp; Weight</title>
  <meta name="description" content="Free calculator from Mark Ratcliffe Moving — pick household items and quantities to see total cubic feet, cubic meters and weight.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving &amp; Storage">
  <meta name="theme-color" content="#4d2e8f">
  <meta property="og:title" content="Storage Calculator – Cubic Feet, Cubic Meters &amp; Weight">
  <meta property="og:description" content="Free calculator from Mark Ratcliffe Moving — pick household items and quantities to see total cubic feet, cubic meters and weight.">
  <meta property="og:image" content="{BASE_URL}/images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving &amp; Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://cdn.yoshki.com" crossorigin>
  <link href="../css/normalize.css?v=20260560" rel="stylesheet">
  <link href="../css/components.css?v=20260560" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260560" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260562" rel="stylesheet">
  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>WebFont.load({{classes:true,timeout:2000,google:{{families:["Inter:400,500,600,700,800","Fraunces:400,500,600,700"]}}}});;</script>
  <link href="../images/favicon.png" rel="shortcut icon">
  <link href="../images/webclip.png" rel="apple-touch-icon">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q111LKQEBP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-Q111LKQEBP');</script>
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}/"}}, {{"@type": "ListItem", "position": 2, "name": "Resources", "item": "{BASE_URL}/resources/"}}, {{"@type": "ListItem", "position": 3, "name": "Storage Calculator"}}]}}</script>
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebApplication", "name": "Mark Ratcliffe Storage Calculator", "applicationCategory": "UtilityApplication", "operatingSystem": "All", "description": "Free volume and weight calculator using BAR-style item inventory volumes used by Sussex removals crews since 1982.", "url": "{canon}", "publisher": {{"@type": "Organization", "@id": "{BASE_URL}/#organization"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "GBP"}}}}</script>
  <link rel="canonical" href="{canon}">
  <meta property="og:url" content="{canon}">
  {csp}
  {referrer}
</head>
{navbar}

  <header class="np-hero">
    <div class="np-hero-inner">
      <div class="np-kicker">Free tool · BAR-style volumes · Sussex removers since 1982</div>
      <h1>Storage &amp; Removals Volume Calculator</h1>
      <p class="np-hero-sub">Tick the items in your home and the calculator updates cubic feet, cubic meters and weight in real time — handy for sizing a storage unit or working out which lorry size you&rsquo;ll need.</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high" width="1800" height="1350">
  </header>

  <nav class="np-breadcrumb" aria-label="Breadcrumb"><a href="../">Home</a> &rsaquo; <a href="./">Resources</a> &rsaquo; Storage Calculator</nav>

  <section class="np-section">
    <div class="np-inner">
      <p style="font-size:1.15rem;">Use this free Mark Ratcliffe Moving calculator to estimate the volume and weight of your house contents. Pick a room from the tab bar, search or scroll the items in that room, then use the &minus; / + buttons to set the quantity. The totals at the top update live. The figures are based on the inventory volumes our BAR-trained crews use every week to plan Sussex removals jobs — derived from the British Association of Removers&rsquo; standard volume sheet that&rsquo;s been the industry reference for decades. Use the result to size your storage unit, work out which lorry size you&rsquo;ll need on moving day, or pre-fill a quote request — and call us on <a href="tel:01323848008">01323 848 008</a> if you&rsquo;d prefer one of our team to walk through it with you. We&rsquo;ve been doing this since 1982; the numbers below are the ones we actually trust on a real moving day.</p>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Volume calculator — pick a room</h2>

      <div class="calc-totals" aria-live="polite" id="calc-totals">
        <div><strong id="total-cuft">0</strong><span>cu ft</span></div>
        <div><strong id="total-cum">0.00</strong><span>cu m</span></div>
        <div><strong id="total-kg">0</strong><span>kg</span></div>
        <div><strong id="van-estimate">No items selected</strong><span>load size</span></div>
      </div>

      <div class="storage-calc" id="storage-calc">
        <div class="calc-tabs" role="tablist" aria-label="Room categories">
{tabs_html}
        </div>

        <label class="calc-search" aria-label="Search items">
          <span class="calc-search-icon">{ICON_SEARCH}</span>
          <input type="search" id="calc-search-input" placeholder="Search Boxes &amp; cartons" aria-label="Search items in the active category">
        </label>

        <div class="calc-panels">
{panels_html}
        </div>

        <div class="calc-actions">
          <button id="calc-reset" type="button" class="np-btn np-btn-secondary">Reset all quantities</button>
          <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Send these figures with a quote request</a>
        </div>
      </div>
    </div>
  </section>

  <section class="np-section">
    <div class="np-inner">
      <h2>How to use the calculator</h2>
      <p>Walk through your home one room at a time. Across the {len(ITEMS)} category tabs above we cover {n_items} common household items. Click a tab to switch rooms, use the search box to jump to a specific item, then tap &minus; or + to set the quantity. The totals box at the top updates live. Three things to remember:</p>
      <ul>
        <li><strong>Estimates, not exact.</strong> Our crews see the same item dimensions vary by 10-20%. The figures here are the BAR-style averages we use to plan a Sussex job; they get you in the right ballpark.</li>
        <li><strong>Allow for boxes.</strong> A typical three-bedroom Sussex house has 60-80 standard removal boxes once everything is packed; if you don&rsquo;t know yet, allow 75 tea-chest-sized boxes for planning purposes.</li>
        <li><strong>Storage versus lorry.</strong> The same volume of contents takes a different shape in a storage container than on a lorry — your storage quote and your removals quote may both reference the cu ft figure but the practical implications differ. We&rsquo;ll explain on the survey.</li>
      </ul>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Lorry-size guide for Mark Ratcliffe Moving jobs</h2>
      <p>Our crews use these rough cubic-footage bands to choose which lorry leaves the depot on the day. The calculator above gives a load-size estimate based on the same bands:</p>
      <ul>
        <li><strong>Up to 80 cu ft</strong> — a small van load. A single-person move, a few items only.</li>
        <li><strong>80-250 cu ft</strong> — Luton van load. A small flat or one-bedroom property.</li>
        <li><strong>250-600 cu ft</strong> — 3.5-tonne lorry. A two-bedroom flat or small house.</li>
        <li><strong>600-1100 cu ft</strong> — 7.5-tonne lorry. A typical three- to four-bedroom Sussex home.</li>
        <li><strong>1100-1700 cu ft</strong> — 18-tonne lorry. A large four-bedroom house with contents.</li>
        <li><strong>1700+ cu ft</strong> — articulated lorry or multiple loads. A substantial country property with antiques and outbuildings.</li>
      </ul>
      <p>For an accurate price (with the BAR Advance Payment Guarantee protecting your deposit and our BS 8564 international-removals accreditation), book a <a href="../mark-ratcliffe-moving-online-removals-quote.html">free in-home survey</a>. We respond within 48 hours.</p>
    </div>
  </section>

  <section class="np-section np-related" aria-label="Related resources">
    <div class="np-inner">
      <h2>Related resources</h2>
      <ul class="np-related-list">
        <li><a href="pricing.html">Removals pricing guide</a></li>
        <li><a href="moving-checklist-eastbourne.html">8-week moving checklist</a></li>
        <li><a href="removals-eastbourne-cost.html">Cost guide for Sussex moves</a></li>
        <li><a href="helpful-tips.html">Helpful moving tips</a></li>
        <li><a href="buy-packing-materials-eastbourne.html">Buy packing materials</a></li>
        <li><a href="faqs.html">Frequently asked questions</a></li>
        <li><a href="../services/storage-eastbourne.html">Self-storage in Eastbourne</a></li>
        <li><a href="../services/full-packing-service.html">Full packing service</a></li>
        <li><a href="../areas-covered/">All areas we cover</a></li>
        <li><a href="../reviews.html">Customer reviews</a></li>
      </ul>
    </div>
  </section>

  <section class="np-section np-cta-block">
    <div class="np-inner">
      <h2>Ready to book your move?</h2>
      <p>Once you have your cu ft / kg figure, request a free quote and we&rsquo;ll come back within 48 hours with an itemised written estimate.</p>
      <div class="np-cta-row">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
  </section>

  {footer}

  <!-- Site-wide nav JS: jQuery + Webflow site script + mobile-nav. Without these
       the megamenu dropdowns and mobile hamburger don't work. -->
  <script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=54f032c21ccd6c2e19dae5a7" crossorigin="anonymous"></script>
  <script defer src="../js/mark-ratcliffe-moving.js?v=20260558"></script>
  <script defer src="../js/mobile-nav.js?v=20260560"></script>
  <script defer src="../js/storage-calculator.js?v=20260562"></script>
</body>
</html>
"""


def main() -> int:
    if not os.path.isfile(SAMPLE_PATH):
        print(f'ERROR — sample {SAMPLE_PATH} missing', file=sys.stderr)
        return 1
    os.makedirs('resources', exist_ok=True)
    open('resources/storage-calculator.html', 'w', encoding='utf-8').write(page_html())
    n = sum(len(items) for _, _, items in ITEMS)
    print(f'  wrote resources/storage-calculator.html ({n} items across {len(ITEMS)} categories)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
