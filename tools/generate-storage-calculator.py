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


# ----------------------------------------------------------------------
# Typical inventory presets per bedroom count.
# Each entry: (category name, item name, quantity). Category + name must
# match the ITEMS table verbatim — the slug is computed identically to
# the inventory input ids so the JS auto-fill targets the right element.
# ----------------------------------------------------------------------
INVENTORY_PRESETS: dict[str, list[tuple[str, str, int]]] = {
    '1bed': [
        ('Bedroom (master)', 'Bed, double (mattress only)', 1),
        ('Bedroom (master)', 'Bed, double (base only)', 1),
        ('Bedroom (master)', 'Wardrobe, double', 1),
        ('Bedroom (master)', 'Chest of drawers, small', 1),
        ('Bedroom (master)', 'Bedside table', 1),
        ('Bedroom (master)', 'Mirror, full-length', 1),
        ('Living room', 'Sofa, 2-seater', 1),
        ('Living room', 'Armchair', 1),
        ('Living room', 'Coffee table', 1),
        ('Living room', 'TV, large (50"+)', 1),
        ('Living room', 'TV unit / stand', 1),
        ('Living room', 'Bookcase, small', 1),
        ('Living room', 'Floor lamp', 1),
        ('Dining room', 'Dining table, 4-seater', 1),
        ('Dining room', 'Dining chair', 2),
        ('Kitchen / utility', 'Fridge, undercounter', 1),
        ('Kitchen / utility', 'Washing machine', 1),
        ('Kitchen / utility', 'Microwave', 1),
        ('Kitchen / utility', 'Kettle', 1),
        ('Kitchen / utility', 'Toaster', 1),
        ('Kitchen / utility', 'Vacuum cleaner', 1),
        ('Kitchen / utility', 'Ironing board', 1),
        ('Bathroom', 'Bathroom cabinet', 1),
        ('Bathroom', 'Linen basket', 1),
        ('Boxes & cartons', 'Standard removals box (medium)', 30),
        ('Boxes & cartons', 'Book box (1.5 cu ft)', 5),
        ('Boxes & cartons', 'Wardrobe carton (tall)', 10),
        ('Boxes & cartons', 'Picture box (large flat)', 3),
        ('Boxes & cartons', 'Suitcase (large)', 2),
    ],
    '2bed': [
        ('Bedroom (master)', 'Bed, double (mattress only)', 1),
        ('Bedroom (master)', 'Bed, double (base only)', 1),
        ('Bedroom (master)', 'Wardrobe, double', 1),
        ('Bedroom (master)', 'Chest of drawers, large', 1),
        ('Bedroom (master)', 'Bedside table', 2),
        ('Bedroom (master)', 'Mirror, full-length', 1),
        ('Bedroom (master)', 'Dressing table', 1),
        ('Kids bedroom', 'Bed, single (mattress only)', 1),
        ('Kids bedroom', 'Bed, single (base only)', 1),
        ('Kids bedroom', 'Junior wardrobe', 1),
        ('Kids bedroom', 'Chest of drawers, kids', 1),
        ('Kids bedroom', 'Kids bedside table', 1),
        ('Hall / Foyer', 'Hall mirror', 1),
        ('Hall / Foyer', 'Shoe rack, small', 1),
        ('Hall / Foyer', 'Coat rack / stand', 1),
        ('Living room', 'Sofa, 3-seater', 1),
        ('Living room', 'Armchair', 1),
        ('Living room', 'Coffee table', 1),
        ('Living room', 'Side / lamp table', 1),
        ('Living room', 'TV, large (50"+)', 1),
        ('Living room', 'TV unit / stand', 1),
        ('Living room', 'Bookcase, large', 1),
        ('Living room', 'Floor lamp', 1),
        ('Living room', 'Mirror, large', 1),
        ('Dining room', 'Dining table, 4-seater', 1),
        ('Dining room', 'Dining chair', 4),
        ('Dining room', 'Sideboard', 1),
        ('Kitchen / utility', 'Fridge-freezer, tall', 1),
        ('Kitchen / utility', 'Washing machine', 1),
        ('Kitchen / utility', 'Cooker, freestanding', 1),
        ('Kitchen / utility', 'Microwave', 1),
        ('Kitchen / utility', 'Kettle', 1),
        ('Kitchen / utility', 'Toaster', 1),
        ('Kitchen / utility', 'Vacuum cleaner', 1),
        ('Kitchen / utility', 'Ironing board', 1),
        ('Bathroom', 'Bathroom cabinet', 1),
        ('Bathroom', 'Linen basket', 1),
        ('Bathroom', 'Vanity unit', 1),
        ('Boxes & cartons', 'Standard removals box (medium)', 50),
        ('Boxes & cartons', 'Book box (1.5 cu ft)', 10),
        ('Boxes & cartons', 'Wardrobe carton (tall)', 15),
        ('Boxes & cartons', 'Picture box (large flat)', 5),
        ('Boxes & cartons', 'Suitcase (large)', 2),
        ('Boxes & cartons', 'Suitcase (small)', 1),
    ],
    '3bed': [
        ('Bedroom (master)', 'Bed, king (mattress only)', 1),
        ('Bedroom (master)', 'Bed, king (base only)', 1),
        ('Bedroom (master)', 'Wardrobe, double', 1),
        ('Bedroom (master)', 'Chest of drawers, large', 1),
        ('Bedroom (master)', 'Bedside table', 2),
        ('Bedroom (master)', 'Mirror, full-length', 1),
        ('Bedroom (master)', 'Dressing table', 1),
        ('Bedroom (master)', 'Bedroom chair', 1),
        ('Kids bedroom', 'Bed, single (mattress only)', 2),
        ('Kids bedroom', 'Bed, single (base only)', 2),
        ('Kids bedroom', 'Junior wardrobe', 2),
        ('Kids bedroom', 'Chest of drawers, kids', 2),
        ('Kids bedroom', 'Kids bedside table', 2),
        ('Kids bedroom', 'Kids desk', 1),
        ('Kids bedroom', 'Kids desk chair', 1),
        ('Kids bedroom', 'Bookshelf', 1),
        ('Hall / Foyer', 'Hall table', 1),
        ('Hall / Foyer', 'Hall mirror', 1),
        ('Hall / Foyer', 'Shoe rack, large', 1),
        ('Hall / Foyer', 'Coat rack / stand', 1),
        ('Living room', 'Sofa, 3-seater', 1),
        ('Living room', 'Armchair', 2),
        ('Living room', 'Coffee table', 1),
        ('Living room', 'Side / lamp table', 2),
        ('Living room', 'TV, large (50"+)', 1),
        ('Living room', 'TV unit / stand', 1),
        ('Living room', 'Bookcase, large', 2),
        ('Living room', 'Sideboard', 1),
        ('Living room', 'Floor lamp', 1),
        ('Living room', 'Table lamp', 2),
        ('Living room', 'Mirror, large', 1),
        ('Dining room', 'Dining table, 6-seater', 1),
        ('Dining room', 'Dining chair', 6),
        ('Dining room', 'Sideboard', 1),
        ('Dining room', 'Display cabinet', 1),
        ('Kitchen / utility', 'Fridge-freezer, tall', 1),
        ('Kitchen / utility', 'Washing machine', 1),
        ('Kitchen / utility', 'Tumble dryer', 1),
        ('Kitchen / utility', 'Dishwasher', 1),
        ('Kitchen / utility', 'Cooker, freestanding', 1),
        ('Kitchen / utility', 'Microwave', 1),
        ('Kitchen / utility', 'Kettle', 1),
        ('Kitchen / utility', 'Toaster', 1),
        ('Kitchen / utility', 'Vacuum cleaner', 1),
        ('Kitchen / utility', 'Ironing board', 1),
        ('Bathroom', 'Bathroom cabinet', 1),
        ('Bathroom', 'Linen basket', 1),
        ('Bathroom', 'Vanity unit', 1),
        ('Bathroom', 'Storage shelves', 1),
        ('Boxes & cartons', 'Standard removals box (medium)', 70),
        ('Boxes & cartons', 'Book box (1.5 cu ft)', 15),
        ('Boxes & cartons', 'Wardrobe carton (tall)', 20),
        ('Boxes & cartons', 'Picture box (large flat)', 8),
        ('Boxes & cartons', 'Suitcase (large)', 3),
        ('Boxes & cartons', 'Suitcase (small)', 2),
        ('Garden & outdoor', 'Garden tools (set)', 1),
        ('Garden & outdoor', 'Lawnmower, push', 1),
    ],
    '4bed': [
        ('Bedroom (master)', 'Bed, king (mattress only)', 1),
        ('Bedroom (master)', 'Bed, king (base only)', 1),
        ('Bedroom (master)', 'Wardrobe, triple', 1),
        ('Bedroom (master)', 'Chest of drawers, large', 1),
        ('Bedroom (master)', 'Bedside table', 2),
        ('Bedroom (master)', 'Mirror, full-length', 1),
        ('Bedroom (master)', 'Dressing table', 1),
        ('Bedroom (master)', 'Dressing table mirror', 1),
        ('Bedroom (master)', 'Bedroom chair', 1),
        ('Bedroom (master)', 'Blanket box / ottoman', 1),
        ('Kids bedroom', 'Bed, single (mattress only)', 3),
        ('Kids bedroom', 'Bed, single (base only)', 3),
        ('Kids bedroom', 'Junior wardrobe', 3),
        ('Kids bedroom', 'Chest of drawers, kids', 3),
        ('Kids bedroom', 'Kids bedside table', 3),
        ('Kids bedroom', 'Kids desk', 2),
        ('Kids bedroom', 'Kids desk chair', 2),
        ('Kids bedroom', 'Bookshelf', 2),
        ('Kids bedroom', 'Toy chest', 1),
        ('Hall / Foyer', 'Hall table', 1),
        ('Hall / Foyer', 'Console table', 1),
        ('Hall / Foyer', 'Hall mirror', 1),
        ('Hall / Foyer', 'Shoe rack, large', 1),
        ('Hall / Foyer', 'Coat rack / stand', 1),
        ('Hall / Foyer', 'Boot bench', 1),
        ('Living room', 'Sofa, 3-seater', 1),
        ('Living room', 'Sofa, 2-seater', 1),
        ('Living room', 'Armchair', 2),
        ('Living room', 'Coffee table', 1),
        ('Living room', 'Side / lamp table', 2),
        ('Living room', 'TV, large (50"+)', 1),
        ('Living room', 'TV unit / stand', 1),
        ('Living room', 'Bookcase, large', 2),
        ('Living room', 'Sideboard', 1),
        ('Living room', 'Display cabinet', 1),
        ('Living room', 'Floor lamp', 1),
        ('Living room', 'Table lamp', 3),
        ('Living room', 'Mirror, large', 1),
        ('Dining room', 'Dining table, 6-seater', 1),
        ('Dining room', 'Dining chair', 6),
        ('Dining room', 'Carver chair', 2),
        ('Dining room', 'Sideboard', 1),
        ('Dining room', 'Display cabinet', 1),
        ('Dining room', 'Welsh dresser', 1),
        ('Kitchen / utility', 'Fridge-freezer, American', 1),
        ('Kitchen / utility', 'Washing machine', 1),
        ('Kitchen / utility', 'Tumble dryer', 1),
        ('Kitchen / utility', 'Dishwasher', 1),
        ('Kitchen / utility', 'Cooker, freestanding', 1),
        ('Kitchen / utility', 'Microwave', 1),
        ('Kitchen / utility', 'Kettle', 1),
        ('Kitchen / utility', 'Toaster', 1),
        ('Kitchen / utility', 'Stand mixer / food processor', 1),
        ('Kitchen / utility', 'Vacuum cleaner', 1),
        ('Kitchen / utility', 'Ironing board', 1),
        ('Kitchen / utility', 'Kitchen table', 1),
        ('Kitchen / utility', 'Kitchen chair', 4),
        ('Bathroom', 'Bathroom cabinet', 2),
        ('Bathroom', 'Linen basket', 1),
        ('Bathroom', 'Vanity unit', 1),
        ('Bathroom', 'Storage shelves', 1),
        ('Office / study', 'Desk', 1),
        ('Office / study', 'Office chair', 1),
        ('Office / study', 'Filing cabinet, 2-drawer', 1),
        ('Office / study', 'Computer (desktop tower)', 1),
        ('Office / study', 'Monitor', 1),
        ('Office / study', 'Printer', 1),
        ('Office / study', 'Bookcase, office', 1),
        ('Boxes & cartons', 'Standard removals box (medium)', 90),
        ('Boxes & cartons', 'Book box (1.5 cu ft)', 20),
        ('Boxes & cartons', 'Wardrobe carton (tall)', 25),
        ('Boxes & cartons', 'Picture box (large flat)', 10),
        ('Boxes & cartons', 'Suitcase (large)', 4),
        ('Boxes & cartons', 'Suitcase (small)', 2),
        ('Garden & outdoor', 'BBQ, kettle', 1),
        ('Garden & outdoor', 'Garden tools (set)', 1),
        ('Garden & outdoor', 'Lawnmower, push', 1),
        ('Garden & outdoor', 'Patio table', 1),
        ('Garden & outdoor', 'Patio chair (folding)', 4),
    ],
    '5bed': [
        ('Bedroom (master)', 'Bed, super-king (mattress only)', 1),
        ('Bedroom (master)', 'Bed, super-king (base only)', 1),
        ('Bedroom (master)', 'Wardrobe, triple', 1),
        ('Bedroom (master)', 'Chest of drawers, large', 2),
        ('Bedroom (master)', 'Bedside table', 2),
        ('Bedroom (master)', 'Mirror, full-length', 1),
        ('Bedroom (master)', 'Dressing table', 1),
        ('Bedroom (master)', 'Dressing table mirror', 1),
        ('Bedroom (master)', 'Bedroom chair', 2),
        ('Bedroom (master)', 'Blanket box / ottoman', 1),
        ('Kids bedroom', 'Bed, single (mattress only)', 4),
        ('Kids bedroom', 'Bed, single (base only)', 4),
        ('Kids bedroom', 'Junior wardrobe', 4),
        ('Kids bedroom', 'Chest of drawers, kids', 4),
        ('Kids bedroom', 'Kids bedside table', 4),
        ('Kids bedroom', 'Kids desk', 3),
        ('Kids bedroom', 'Kids desk chair', 3),
        ('Kids bedroom', 'Bookshelf', 3),
        ('Kids bedroom', 'Toy chest', 1),
        ('Hall / Foyer', 'Hall table', 1),
        ('Hall / Foyer', 'Console table', 1),
        ('Hall / Foyer', 'Hall mirror', 1),
        ('Hall / Foyer', 'Shoe rack, large', 1),
        ('Hall / Foyer', 'Coat rack / stand', 1),
        ('Hall / Foyer', 'Boot bench', 1),
        ('Hall / Foyer', 'Hall cabinet', 1),
        ('Living room', 'Sofa, 3-seater', 1),
        ('Living room', 'Sofa, 2-seater', 1),
        ('Living room', 'Armchair', 2),
        ('Living room', 'Coffee table', 1),
        ('Living room', 'Side / lamp table', 2),
        ('Living room', 'TV, large (50"+)', 2),
        ('Living room', 'TV unit / stand', 1),
        ('Living room', 'Bookcase, large', 2),
        ('Living room', 'Sideboard', 1),
        ('Living room', 'Display cabinet', 1),
        ('Living room', 'Drinks cabinet', 1),
        ('Living room', 'Floor lamp', 2),
        ('Living room', 'Table lamp', 3),
        ('Living room', 'Mirror, large', 2),
        ('Dining room', 'Dining table, 8-seater', 1),
        ('Dining room', 'Dining chair', 8),
        ('Dining room', 'Carver chair', 2),
        ('Dining room', 'Sideboard', 1),
        ('Dining room', 'Display cabinet', 1),
        ('Dining room', 'Welsh dresser', 1),
        ('Dining room', 'Drinks trolley', 1),
        ('Kitchen / utility', 'Fridge-freezer, American', 1),
        ('Kitchen / utility', 'Washing machine', 1),
        ('Kitchen / utility', 'Tumble dryer', 1),
        ('Kitchen / utility', 'Dishwasher', 1),
        ('Kitchen / utility', 'Range cooker', 1),
        ('Kitchen / utility', 'Microwave', 1),
        ('Kitchen / utility', 'Kettle', 1),
        ('Kitchen / utility', 'Toaster', 1),
        ('Kitchen / utility', 'Stand mixer / food processor', 1),
        ('Kitchen / utility', 'Vacuum cleaner', 1),
        ('Kitchen / utility', 'Ironing board', 1),
        ('Kitchen / utility', 'Kitchen table', 1),
        ('Kitchen / utility', 'Kitchen chair', 6),
        ('Bathroom', 'Bathroom cabinet', 2),
        ('Bathroom', 'Linen basket', 1),
        ('Bathroom', 'Vanity unit', 2),
        ('Bathroom', 'Storage shelves', 2),
        ('Office / study', 'Desk', 1),
        ('Office / study', 'Office chair', 1),
        ('Office / study', 'Filing cabinet, 4-drawer', 1),
        ('Office / study', 'Computer (desktop tower)', 1),
        ('Office / study', 'Monitor', 1),
        ('Office / study', 'Printer', 1),
        ('Office / study', 'Bookcase, office', 2),
        ('Boxes & cartons', 'Standard removals box (medium)', 110),
        ('Boxes & cartons', 'Book box (1.5 cu ft)', 25),
        ('Boxes & cartons', 'Wardrobe carton (tall)', 30),
        ('Boxes & cartons', 'Picture box (large flat)', 12),
        ('Boxes & cartons', 'Suitcase (large)', 4),
        ('Boxes & cartons', 'Suitcase (small)', 3),
        ('Garden & outdoor', 'BBQ, large gas', 1),
        ('Garden & outdoor', 'Garden tools (set)', 1),
        ('Garden & outdoor', 'Lawnmower, push', 1),
        ('Garden & outdoor', 'Patio table', 1),
        ('Garden & outdoor', 'Patio chair (folding)', 4),
        ('Garden & outdoor', 'Garden bench', 1),
        ('Specialist & other', 'Antique chest (large)', 1),
        ('Specialist & other', 'Piano, upright', 1),
    ],
}


def emit_inventory_presets_js() -> str:
    """Emit BED_INVENTORY as a JS object whose keys match the item input ids."""
    lines = ['  var BED_INVENTORY = {']
    for bed, items in INVENTORY_PRESETS.items():
        lines.append(f"    '{bed}': {{")
        for cat, name, qty in items:
            slug = slugify(cat) + '-' + slugify(name)
            lines.append(f"      'item-{slug}': {qty},")
        lines.append('    },')
    lines.append('  };')
    return '\n'.join(lines)


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
  <title>Removals Cost Calculator – Volume, Mileage &amp; Vehicle</title>
  <meta name="description" content="Free Mark Ratcliffe Moving calculator — pick items, set mileage, see vehicle size and an itemised cost estimate for your Sussex move.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving &amp; Storage">
  <meta name="theme-color" content="#4d2e8f">
  <meta property="og:title" content="Removals Cost Calculator – Volume, Mileage &amp; Vehicle">
  <meta property="og:description" content="Free Mark Ratcliffe Moving calculator — pick items, set mileage, see vehicle size and an itemised cost estimate for your Sussex move.">
  <meta property="og:image" content="{BASE_URL}/images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving &amp; Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://cdn.yoshki.com" crossorigin>
  <link href="../css/normalize.css?v=20260560" rel="stylesheet">
  <link href="../css/components.css?v=20260560" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260560" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260575" rel="stylesheet">
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
      <h1>Removals Cost &amp; Volume Calculator</h1>
      <p class="np-hero-sub">Tick the items in your home, set the move distance and the calculator returns cubic feet, vehicle size, weight and an itemised cost estimate — the same numbers our crews use to plan a Sussex job.</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high" width="1800" height="1350">
  </header>

  <nav class="np-breadcrumb" aria-label="Breadcrumb"><a href="../">Home</a> &rsaquo; <a href="./">Resources</a> &rsaquo; Storage Calculator</nav>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>Volume calculator — pick a room</h2>

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
          <a href="#quote-form" class="np-btn np-btn-primary">Send these figures with a quote request</a>
        </div>
      </div>
    </div>
  </section>

  <section class="np-section">
    <div class="np-inner">
      <h2>What would you like to calculate?</h2>

      <fieldset class="mode-selector" id="mode-selector">
        <legend class="sr-only">Calculator mode</legend>
        <label class="mode-option">
          <input type="radio" name="calc-mode" value="removals">
          <span><strong>Removals cost only</strong><small>The cost of moving your items to a new home.</small></span>
        </label>
        <label class="mode-option">
          <input type="radio" name="calc-mode" value="storage">
          <span><strong>Storage cost only</strong><small>The cost of storing your items in a Prestige steel room.</small></span>
        </label>
        <label class="mode-option">
          <input type="radio" name="calc-mode" value="both" checked>
          <span><strong>Both removals + storage</strong><small>The full picture for a move-and-store job.</small></span>
        </label>
      </fieldset>

      <div class="calc-totals" aria-live="polite" id="calc-totals">
        <div><strong id="total-cuft">0</strong><span>cu ft</span></div>
        <div><strong id="total-cum">0.00</strong><span>cu m</span></div>
        <div><strong id="total-kg">0</strong><span>kg</span></div>
        <div><strong id="van-estimate">No items selected</strong><span>load size</span></div>
      </div>

      <div class="volume-inputs">
        <fieldset class="cost-size-input">
          <legend class="cost-input-label">Bedrooms</legend>
          <label class="cost-size-option">
            <input type="radio" name="home-size" value="1bed">
            <span><strong>1-bed flat or studio</strong> <small>~700 cu ft &middot; Luton Van &middot; £360 min</small></span>
          </label>
          <label class="cost-size-option">
            <input type="radio" name="home-size" value="2bed">
            <span><strong>2-bed home</strong> <small>~1,000 cu ft &middot; 7.5 – 18 Tonne lorry &middot; £650 min</small></span>
          </label>
          <label class="cost-size-option">
            <input type="radio" name="home-size" value="3bed" checked>
            <span><strong>3-bed home</strong> <small>~1,350 cu ft &middot; 7.5 – 18 Tonne lorry &middot; £650 min</small></span>
          </label>
          <label class="cost-size-option">
            <input type="radio" name="home-size" value="4bed">
            <span><strong>4-bed home</strong> <small>~1,800 cu ft &middot; 18 Tonne+ / Artic &middot; £1,000 min</small></span>
          </label>
          <label class="cost-size-option">
            <input type="radio" name="home-size" value="5bed">
            <span><strong>5+ bed / antiques / country</strong> <small>~2,500+ cu ft &middot; 18 Tonne+ / Artic &middot; £1,000 min</small></span>
          </label>
        </fieldset>

        <label class="cost-manual-cuft" id="cost-manual-cuft-wrap">
          <span class="cost-input-label">Cubic feet (if you&rsquo;re not using the inventory)</span>
          <input type="number" id="cost-manual-cuft" min="0" step="50" value="1350" inputmode="numeric" aria-describedby="cost-manual-cuft-help">
          <span class="cost-input-help" id="cost-manual-cuft-help">Auto-fills with the typical figure for your chosen bedroom count. Tick items above to override with a precise volume.</span>
        </label>
      </div>

      <aside class="inventory-prompt" id="inventory-prompt" hidden>
        <div class="inventory-prompt-text">
          <strong>Want a head start?</strong>
          <span id="inventory-prompt-detail">Load a typical 3-bed inventory into the item picker above. We&rsquo;ve worked out a standard loadout for that size of home — you can tweak the quantities after.</span>
        </div>
        <div class="inventory-prompt-actions">
          <button type="button" id="load-inventory-btn" class="np-btn np-btn-primary">Load typical inventory</button>
          <button type="button" id="dismiss-inventory-prompt" class="inventory-prompt-skip">Skip — I&rsquo;ll use the cu ft figure</button>
        </div>
      </aside>

      <p data-show-modes="removals both">Enter the round-trip distance for the move below. The calculator multiplies the volume by the £/cu ft rate for your home size, adds the mileage at the per-vehicle rate, and applies the minimum charge if the volume cost would be lower.</p>

      <div class="cost-estimator" id="cost-estimator" data-show-modes="removals both">
        <div class="cost-inputs">
          <label class="cost-input">
            <span class="cost-input-label">Total job miles (depot → old home → new home → depot)</span>
            <input type="number" id="cost-miles" min="0" value="30" inputmode="numeric" aria-describedby="cost-miles-help">
            <span class="cost-input-help" id="cost-miles-help">Typical Sussex local move: 25-50 mi. Sussex → London: 100-150 mi. Sussex → north UK: 400-600 mi.</span>
          </label>
        </div>

        <div class="cost-output" aria-live="polite">
          <div class="cost-headline">
            <div class="cost-headline-amount" id="cost-total">£0</div>
            <div class="cost-headline-label" id="cost-headline-label">Estimated removals cost</div>
          </div>
          <dl class="cost-breakdown">
            <div class="cost-line"><dt>Vehicle</dt><dd><strong id="cost-vehicle">—</strong></dd></div>
            <div class="cost-line"><dt>Volume cost</dt><dd><strong id="cost-volume">£0</strong></dd></div>
            <div class="cost-line"><dt>Mileage</dt><dd><strong id="cost-mileage">£0</strong></dd></div>
            <div class="cost-line"><dt>Minimum charge</dt><dd><strong id="cost-minimum">£0</strong></dd></div>
          </dl>
        </div>
      </div>

      <div class="storage-block" id="storage-block" data-show-modes="storage both">
        <label class="storage-toggle">
          <input type="checkbox" id="storage-enabled">
          <span><strong>Do you also need storage?</strong> Add our self-storage to the estimate.</span>
        </label>
        <div class="storage-details" id="storage-details" hidden>
          <div class="storage-fields">
            <label class="storage-weeks-field">
              <span class="storage-label">Weeks of storage</span>
              <input type="number" id="storage-weeks" min="1" value="4">
            </label>
            <p class="storage-help">Unit size is picked automatically from your selected volume — a Prestige steel storage room at our Lower Dicker depot. Rates include VAT and goods-in-storage insurance.</p>
          </div>
          <div class="storage-output">
            <div class="cost-headline cost-headline-storage">
              <div class="cost-headline-amount" id="storage-total">£0.00</div>
              <div class="cost-headline-label" id="storage-headline-label">Estimated storage cost</div>
            </div>
            <dl class="cost-breakdown">
              <div class="cost-line"><dt>Recommended unit</dt><dd><strong id="storage-unit">—</strong></dd></div>
              <div class="cost-line"><dt>Weekly rate (inc VAT &amp; insurance)</dt><dd><strong id="storage-weekly">£0.00</strong></dd></div>
            </dl>
            <p class="storage-alt">Also available: <strong>75 sqft low-ceiling room at £6.91/week</strong> (inc VAT &amp; insurance) — ideal if your contents won&rsquo;t stack high.</p>
          </div>
        </div>
      </div>

      <div class="cost-grand-total" id="cost-grand-total" hidden data-show-modes="both">
        <div class="cost-grand-amount" id="cost-grand-total-value">£0</div>
        <div class="cost-grand-label">Total estimate · removals + storage</div>
      </div>

      <p class="cost-disclaimer"><strong>Estimate only.</strong> The exact quote depends on access, stairs, the listed-property quotient, packing materials, antiques handling, timing and the actual storage duration you book. For an accurate, written, BAR-Advance-Payment-Guarantee-protected quote please <a href="../mark-ratcliffe-moving-online-removals-quote.html">request a free survey</a> — we respond within 48 hours.</p>
    </div>
  </section>

  <section class="np-section np-section-soft" id="quote-form">
    <div class="np-inner">
      <h2>Send these figures with a quote request</h2>
      <p>Fill in your details below. When you click <strong>Send quote request</strong> we open your email app with every item you ticked, the calculated cubic feet, vehicle band and cost estimate already in the message — you just click send. We reply within 48 hours.</p>

      <form class="quote-form" id="quote-request-form">
        <div class="quote-form-grid">
          <label>
            <span class="quote-form-label">Your email</span>
            <input type="email" name="email" id="qf-email" required autocomplete="email" placeholder="you@example.com">
          </label>
          <label>
            <span class="quote-form-label">Phone number</span>
            <input type="tel" name="phone" id="qf-phone" required autocomplete="tel" placeholder="01234 567 890">
          </label>
          <label>
            <span class="quote-form-label">Moving FROM (postcode)</span>
            <input type="text" name="from_postcode" id="qf-from" required autocomplete="postal-code" placeholder="BN21 3AB">
          </label>
          <label>
            <span class="quote-form-label">Moving TO (postcode)</span>
            <input type="text" name="to_postcode" id="qf-to" required autocomplete="postal-code" placeholder="TN22 5JD">
          </label>
          <label class="quote-form-full">
            <span class="quote-form-label">Anything else we should know? (optional)</span>
            <textarea name="notes" id="qf-notes" rows="3" placeholder="Preferred move date, access notes, listed property, antiques, etc."></textarea>
          </label>
        </div>
        <div class="quote-form-actions">
          <button type="submit" class="np-btn np-btn-primary">Send quote request</button>
          <p class="quote-form-help">Opens your email app with everything pre-filled. Goes to <a href="mailto:office@markratcliffemoving.co.uk">office@markratcliffemoving.co.uk</a> — just hit send.</p>
        </div>
        <div class="quote-form-status" id="qf-status" role="status" aria-live="polite"></div>
      </form>
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
      <h2>Mark Ratcliffe Moving pricing model</h2>
      <p>Each bedroom count maps to the vehicle our crews actually send, the per-cu-ft rate we apply, the per-mile mileage rate for that vehicle, and a minimum-charge floor. The calculator uses these published figures directly:</p>
      <table class="rate-table">
        <thead>
          <tr>
            <th>Home size</th>
            <th>Vehicle</th>
            <th>£ / cu ft</th>
            <th>£ / mile</th>
            <th>Minimum charge</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1-bed</strong><br><span class="rate-table-sub">flat or studio</span></td>
            <td>Luton Van (3.5t)</td>
            <td>£2.25</td>
            <td>£2.00</td>
            <td><strong>£360</strong></td>
          </tr>
          <tr>
            <td><strong>2-bed</strong><br><span class="rate-table-sub">home</span></td>
            <td>7.5 – 18 Tonne lorry</td>
            <td>£1.60</td>
            <td>£2.75</td>
            <td><strong>£650</strong></td>
          </tr>
          <tr>
            <td><strong>3-bed</strong><br><span class="rate-table-sub">home</span></td>
            <td>7.5 – 18 Tonne lorry</td>
            <td>£1.60</td>
            <td>£2.75</td>
            <td><strong>£650</strong></td>
          </tr>
          <tr>
            <td><strong>4-bed</strong><br><span class="rate-table-sub">home</span></td>
            <td>18 Tonne+ / 44 Tonne Artic</td>
            <td>£1.30</td>
            <td>£3.50</td>
            <td><strong>£1,000</strong></td>
          </tr>
          <tr>
            <td><strong>5+ bed</strong><br><span class="rate-table-sub">antiques / country property</span></td>
            <td>18 Tonne+ / 44 Tonne Artic</td>
            <td>£1.30</td>
            <td>£3.50</td>
            <td><strong>£1,000</strong></td>
          </tr>
        </tbody>
      </table>
      <p>The cost formula: <strong>cost = max(minimum charge, (volume × £/cu ft) + (miles × £/mile))</strong>. The minimum charge protects against very small jobs that wouldn&rsquo;t otherwise cover the day &mdash; but the minimum covers the <em>whole</em> job (volume plus mileage), so adding more inventory or more miles only pushes the price up once the combined figure passes the floor. Specialist services (piano moving, antique handling, custom crating, white-glove relocation, international shipping) sit on top of the base figure. Every customer deposit is covered by the BAR Advance Payment Guarantee, and our processes are certified to the BS 8564 international removals standard.</p>
      <p>For an accurate price, book a <a href="../mark-ratcliffe-moving-online-removals-quote.html">free in-home survey</a>. We respond within 48 hours.</p>
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

  <!-- Inventory presets — slugs match the item input ids, computed at
       build time by the Python generator. -->
  <script>
__BED_INVENTORY__
  </script>

  <!-- Site-wide nav JS: jQuery + Webflow site script + mobile-nav. Without these
       the megamenu dropdowns and mobile hamburger don't work. -->
  <script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=54f032c21ccd6c2e19dae5a7" crossorigin="anonymous"></script>
  <script defer src="../js/mark-ratcliffe-moving.js?v=20260558"></script>
  <script defer src="../js/mobile-nav.js?v=20260560"></script>
  <script defer src="../js/storage-calculator.js?v=20260575"></script>
</body>
</html>
"""


def main() -> int:
    if not os.path.isfile(SAMPLE_PATH):
        print(f'ERROR — sample {SAMPLE_PATH} missing', file=sys.stderr)
        return 1
    os.makedirs('resources', exist_ok=True)
    html = page_html().replace('__BED_INVENTORY__', emit_inventory_presets_js())
    open('resources/storage-calculator.html', 'w', encoding='utf-8').write(html)
    n = sum(len(items) for _, _, items in ITEMS)
    print(f'  wrote resources/storage-calculator.html ({n} items / {len(ITEMS)} cats / {sum(len(v) for v in INVENTORY_PRESETS.values())} preset rows)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
