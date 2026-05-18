#!/usr/bin/env python3
"""Replace the keyword-stuffed grid on areas-covered.html with a clean,
regional layout. Each town is named once with small service-pill links."""
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
FP = ROOT / "areas-covered.html"

# (town, county, [(service_label, url, kind), ...])
TOWNS = {
    "East Sussex": [
        ("Eastbourne",        [("Removals", "removals-eastbourne.html", "removals"),
                                ("Man & Van", "man-and-van-eastbourne.html", "manvan"),
                                ("Storage", "storage-eastbourne.html", "storage"),
                                ("International", "international-removals-eastbourne.html", "intl")]),
        ("Hailsham",          [("Removals", "hailsham-removals.html", "removals")]),
        ("Polegate",          [("Removals", "removals-polegate.html", "removals")]),
        ("Pevensey",          [("Removals", "removals-pevensey.html", "removals")]),
        ("Willingdon",        [("Removals", "removals-willingdon.html", "removals")]),
        ("Uckfield",          [("Removals", "removals-uckfield.html", "removals")]),
        ("Heathfield",        [("Removals", "removals-heathfield.html", "removals")]),
        ("Bexhill",           [("Removals", "removals-bexhill.html", "removals"),
                                ("International", "areas-covered/international-removals-in-bexhill.html", "intl")]),
        ("Newhaven",          [("Removals", "areas-covered/removals-newhaven-sussex.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-newhaven.html", "manvan"),
                                ("International", "areas-covered/international-removals-in-newhaven.html", "intl")]),
        ("Lewes",             [("Removals", "areas-covered/removals-lewes-moving-home-in-sussex.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-lewes.html", "manvan"),
                                ("International", "areas-covered/international-removals-in-lewes.html", "intl")]),
        ("Seaford",           [("Removals", "areas-covered/removals-seaford.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-seaford.html", "manvan")]),
        ("Hastings",          [("International", "areas-covered/international-removals-in-hastings.html", "intl")]),
        ("Hove",              [("Removals", "areas-covered/removals-hove.html", "removals"),
                                ("Man & Van", "areas-covered/man-with-a-van-hove.html", "manvan")]),
    ],
    "West Sussex": [
        ("Brighton",          [("Removals", "areas-covered/removals-brighton-sussex.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-brighton.html", "manvan"),
                                ("International", "areas-covered/international-removals-in-brighton.html", "intl")]),
        ("Worthing",          [("Removals", "areas-covered/removals-worthing-moving-home-in-sussex.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-worthing.html", "manvan")]),
        ("East Grinstead",    [("Removals", "areas-covered/removals-east-grinstead-moving-home-in-sussex.html", "removals")]),
        ("Crawley",           [("Removals", "areas-covered/removals-crawley.html", "removals")]),
        ("Horsham",           [("Man & Van", "areas-covered/man-and-van-horsham.html", "manvan")]),
        ("Haywards Heath",    [("Man & Van", "areas-covered/man-and-van-haywards-heath.html", "manvan")]),
    ],
    "Surrey": [
        ("Reigate",           [("Removals", "areas-covered/removals-reigate-moving-home-in-surrey.html", "removals")]),
        ("Leatherhead",       [("Removals", "areas-covered/removals-leatherhead.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-leatherhead.html", "manvan")]),
        ("Redhill",           [("Removals", "areas-covered/removals-redhill.html", "removals")]),
        ("Woking",            [("Removals", "areas-covered/removals-woking-surrey.html", "removals")]),
        ("Epsom",             [("Removals", "areas-covered/removals-epsom-surrey.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-epsom.html", "manvan")]),
        ("Guildford",         [("Removals", "areas-covered/removals-guildford.html", "removals")]),
        ("Weybridge",         [("Removals", "areas-covered/removals-weybridge.html", "removals")]),
    ],
    "Kent": [
        ("Tunbridge Wells",   [("Removals", "areas-covered/removals-tunbridge-wells-moving-home-in-sussex.html", "removals"),
                                ("Man & Van", "areas-covered/man-and-van-tunbridge-wells.html", "manvan"),
                                ("International", "areas-covered/international-removals-in-tunbridge-wells.html", "intl")]),
        ("Sevenoaks",         [("Removals", "areas-covered/removals-sevenoaks.html", "removals")]),
    ],
}


SERVICE_ICONS = {
    "removals": (
        # House icon
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">'
        '<path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1Z"/></svg>',
        "House moves",
    ),
    "manvan": (
        # Van icon
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">'
        '<path d="M1 17V7a1 1 0 0 1 1-1h11v11"/><path d="M13 10h5l4 5v2h-3"/>'
        '<circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
        "Man & Van",
    ),
    "storage": (
        # Box icon
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">'
        '<path d="m3 7 9-4 9 4-9 4Z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/></svg>',
        "Storage",
    ),
    "intl": (
        # Globe icon
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18"/>'
        '<path d="M12 3a14 14 0 0 0 0 18"/></svg>',
        "International",
    ),
}


def render_town(town, services):
    slug = town.lower().replace(" ", "-")
    # Order: removals → manvan → storage → intl (visual consistency)
    order = ["removals", "manvan", "storage", "intl"]
    services_by_kind = {k: (label, url) for label, url, k in services}
    icons = ""
    for kind in order:
        if kind not in services_by_kind:
            continue
        _label, url = services_by_kind[kind]
        svg, srv_name = SERVICE_ICONS[kind]
        # The link text for screen readers (and search engines) is a natural phrase
        # rather than a repeated stuffed keyword.
        sr_label = f"{srv_name} in {town}"
        icons += (
            f'          <a class="ac-icon ac-icon-{kind}" href="{url}" '
            f'data-srv="{kind}" aria-label="{sr_label}" title="{sr_label}">'
            f'{svg}</a>\n'
        )
    data_services = ",".join(k for k in order if k in services_by_kind)
    return f'''      <article class="ac-town" data-name="{slug}" data-services="{data_services}">
        <h3 class="ac-town-name">{town}</h3>
        <div class="ac-icons">
{icons}        </div>
      </article>
'''


def render_region(region, towns):
    cards = "".join(render_town(t, s) for t, s in towns)
    return f'''  <section class="ac-region">
    <div class="ac-region-inner">
      <header class="ac-region-head">
        <h2 class="ac-region-title">{region}</h2>
        <p class="ac-region-meta">{len(towns)} town{"s" if len(towns) != 1 else ""} covered</p>
      </header>
      <div class="ac-grid">
{cards}      </div>
    </div>
  </section>
'''


def build_body():
    total_towns = sum(len(t) for t in TOWNS.values())
    regions_html = "".join(render_region(r, ts) for r, ts in TOWNS.items())

    # Filter toggle buttons — each service name appears here exactly once
    filter_btns = ""
    for kind, (svg, label) in SERVICE_ICONS.items():
        filter_btns += (
            f'        <button type="button" class="ac-srv-btn ac-srv-btn-{kind}" '
            f'data-srv="{kind}" aria-pressed="false">'
            f'<span class="ac-srv-icon">{svg}</span>{label}</button>\n'
        )

    return f'''
  <!-- Hero -->
  <section class="ac-hero">
    <div class="ac-hero-pattern" aria-hidden="true"></div>
    <div class="ac-hero-inner">
      <p class="ac-eyebrow">Service Area</p>
      <h1>Where We Cover</h1>
      <p class="ac-sub">Family-run moving and storage for East Sussex, West Sussex, Surrey and Kent — with international shipping to over 200 destinations worldwide. Find your town below or call <a href="tel:01323848008">01323 848 008</a>.</p>
      <div class="ac-stats" role="list">
        <div role="listitem"><strong>{total_towns}</strong><span>Towns covered</span></div>
        <div role="listitem"><strong>{len(TOWNS)}</strong><span>Counties</span></div>
        <div role="listitem"><strong>40+</strong><span>Years experience</span></div>
        <div role="listitem"><strong>200+</strong><span>International destinations</span></div>
      </div>
    </div>
  </section>

  <!-- Search + service filter (each service name shown once) -->
  <section class="ac-filter">
    <div class="ac-filter-inner">
      <div class="ac-filter-input">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4.35-4.35"/></svg>
        <input id="ac-search" type="text" placeholder="Find your town…" autocomplete="off" aria-label="Filter towns by name">
        <button id="ac-clear" type="button" aria-label="Clear filter" hidden>&times;</button>
      </div>
      <div class="ac-filter-services" aria-label="Filter by service type">
{filter_btns}      </div>
    </div>
  </section>

{regions_html}
  <!-- No-results placeholder (toggled by JS) -->
  <p id="ac-empty" class="ac-empty" hidden>No towns match those filters. Try a shorter word — or call <a href="tel:01323848008">01323 848 008</a>.</p>

  <!-- Where we're based -->
  <section class="ac-map-section">
    <div class="ac-map-inner">
      <p class="ac-eyebrow ac-eyebrow-light">Our depot</p>
      <h2 class="ac-map-title">Centrally placed for Sussex, Surrey &amp; Kent</h2>
      <p class="ac-map-sub">Our Lower Dicker depot is on the A22 — minutes from Hailsham, Eastbourne and the M25/A23 corridor. That gives us short response times across the whole region.</p>
    </div>
  </section>

  <!-- Search + service filter JS -->
  <script>
    (function () {{
      var input = document.getElementById('ac-search');
      var clear = document.getElementById('ac-clear');
      var empty = document.getElementById('ac-empty');
      var srvBtns = document.querySelectorAll('.ac-srv-btn');
      if (!input) return;
      var regions = document.querySelectorAll('.ac-region');
      var activeServices = new Set();  // empty = no filter

      function apply() {{
        var q = (input.value || '').trim().toLowerCase().replace(/\\s+/g, '-');
        var anyVisible = false;
        regions.forEach(function (r) {{
          var visibleInRegion = 0;
          r.querySelectorAll('.ac-town').forEach(function (t) {{
            var name = t.getAttribute('data-name') || '';
            var srvs = (t.getAttribute('data-services') || '').split(',');
            var nameMatch = !q || name.indexOf(q) !== -1;
            var srvMatch = activeServices.size === 0
              || srvs.some(function (s) {{ return activeServices.has(s); }});
            var match = nameMatch && srvMatch;
            t.hidden = !match;
            if (match) visibleInRegion++;
          }});
          r.hidden = visibleInRegion === 0;
          if (visibleInRegion > 0) anyVisible = true;
        }});
        empty.hidden = anyVisible;
        clear.hidden = !q && activeServices.size === 0;
      }}

      input.addEventListener('input', apply);
      clear.addEventListener('click', function () {{
        input.value = '';
        activeServices.clear();
        srvBtns.forEach(function (b) {{
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        }});
        apply(); input.focus();
      }});
      srvBtns.forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          var s = btn.getAttribute('data-srv');
          if (activeServices.has(s)) {{
            activeServices.delete(s);
            btn.classList.remove('is-active');
            btn.setAttribute('aria-pressed', 'false');
          }} else {{
            activeServices.add(s);
            btn.classList.add('is-active');
            btn.setAttribute('aria-pressed', 'true');
          }}
          apply();
        }});
      }});
    }})();
  </script>

  <style>
    .ac-hero {{ position: relative; overflow: hidden;
      background: linear-gradient(135deg, #220b50 0%, #3a1a7a 60%, #1a0840 100%);
      color: #fff; padding: 4rem 1.5rem 4.5rem; text-align: center; }}
    .ac-hero-pattern {{ position: absolute; inset: 0; opacity: 0.06;
      background-image: radial-gradient(rgba(255,255,255,0.9) 1.2px, transparent 1.2px);
      background-size: 28px 28px; pointer-events: none; }}
    .ac-hero-inner {{ position: relative; max-width: 920px; margin: 0 auto; }}
    .ac-eyebrow {{ color: #FFC107; font-size: 0.78rem; letter-spacing: 0.18em;
      text-transform: uppercase; font-weight: 700; margin: 0 0 0.6rem; }}
    .ac-eyebrow-light {{ color: #d4af37; }}
    .ac-hero h1 {{ color: #fff !important; font-size: clamp(2.2rem, 5vw, 3.5rem) !important;
      font-weight: 700 !important; margin: 0 0 1rem !important; letter-spacing: -0.01em;
      line-height: 1.1; }}
    .ac-sub {{ color: rgba(255,255,255,0.88); font-size: 1.08rem; line-height: 1.6;
      max-width: 680px; margin: 0 auto 2rem; }}
    .ac-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
      max-width: 720px; margin: 0 auto; padding-top: 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.15); }}
    @media (max-width: 640px) {{ .ac-stats {{ grid-template-columns: repeat(2, 1fr); }} }}
    .ac-stats > div {{ display: flex; flex-direction: column; align-items: center; }}
    .ac-stats strong {{ font-size: clamp(1.6rem, 3vw, 2.2rem); color: #FFC107;
      font-weight: 800; line-height: 1; }}
    .ac-stats span {{ font-size: 0.78rem; color: rgba(255,255,255,0.78);
      text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.5rem; }}

    /* Filter strip */
    .ac-filter {{ background: #fff; padding: 1.5rem 1.5rem;
      border-bottom: 1px solid #e0dceb; position: sticky; top: 116px; z-index: 30;
      box-shadow: 0 2px 14px -8px rgba(34,11,80,0.15); }}
    @media (max-width: 991px) {{ .ac-filter {{ top: 78px; }} }}
    .ac-filter-inner {{ max-width: 1100px; margin: 0 auto;
      display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 1.5rem; align-items: center; }}
    @media (max-width: 760px) {{
      .ac-filter-inner {{ grid-template-columns: 1fr; gap: 0.85rem; }}
    }}
    .ac-filter-input {{ position: relative; display: flex; align-items: center; }}
    .ac-filter-input svg {{ position: absolute; left: 14px; color: #5a5a6a; }}
    .ac-filter-input input {{
      width: 100%; padding: 0.85rem 2.6rem 0.85rem 2.6rem;
      font-size: 1rem; border: 1px solid #e0dceb; border-radius: 999px;
      background: #f7f5fb; transition: border-color .15s, box-shadow .15s;
    }}
    .ac-filter-input input:focus {{ outline: none; border-color: #220b50;
      background: #fff; box-shadow: 0 0 0 4px rgba(34,11,80,0.08); }}
    .ac-filter-input button {{ position: absolute; right: 12px;
      background: #e0dceb; color: #220b50; border: none; cursor: pointer;
      width: 26px; height: 26px; border-radius: 50%; font-size: 1.1rem;
      line-height: 0; display: inline-flex; align-items: center; justify-content: center;
    }}

    /* Service filter toggle buttons — each service name appears here ONCE */
    .ac-filter-services {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
    .ac-srv-btn {{
      display: inline-flex; align-items: center; gap: 0.45rem;
      padding: 0.45rem 0.85rem; border: 1.5px solid #e0dceb;
      background: #fff; color: #220b50;
      border-radius: 999px; cursor: pointer;
      font-size: 0.82rem; font-weight: 600; letter-spacing: 0.01em;
      transition: all .15s ease;
      font-family: inherit;
    }}
    .ac-srv-btn .ac-srv-icon {{
      display: inline-flex; width: 18px; height: 18px;
      align-items: center; justify-content: center; color: currentColor;
    }}
    .ac-srv-btn .ac-srv-icon svg {{ width: 100%; height: 100%; }}
    .ac-srv-btn:hover {{ border-color: #220b50; }}
    .ac-srv-btn.is-active {{ background: #220b50; color: #fff; border-color: #220b50; }}
    .ac-srv-btn-manvan.is-active   {{ background: #d4af37; color: #1f1f1f; border-color: #d4af37; }}
    .ac-srv-btn-storage.is-active  {{ background: #3a1a7a; color: #fff; border-color: #3a1a7a; }}
    .ac-srv-btn-intl.is-active     {{ background: #e74c3c; color: #fff; border-color: #e74c3c; }}

    /* Service icons under each town name */
    .ac-icons {{ display: flex; gap: 0.45rem; flex-wrap: wrap; }}
    .ac-icon {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 34px; height: 34px; border-radius: 50%;
      text-decoration: none;
      border: 1.5px solid;
      transition: transform .15s, box-shadow .15s, background .15s, color .15s;
    }}
    .ac-icon svg {{ width: 18px; height: 18px; }}
    /* Each icon colour-codes its service type without ever showing the word */
    .ac-icon-removals  {{ color: #220b50;       border-color: rgba(34,11,80,0.25); background: rgba(34,11,80,0.06); }}
    .ac-icon-manvan    {{ color: #8a6e15;       border-color: rgba(212,175,55,0.45); background: rgba(212,175,55,0.10); }}
    .ac-icon-storage   {{ color: #3a1a7a;       border-color: rgba(58,26,122,0.30); background: rgba(58,26,122,0.07); }}
    .ac-icon-intl      {{ color: #c0392b;       border-color: rgba(231,76,60,0.35); background: rgba(231,76,60,0.08); }}
    .ac-icon:hover, .ac-icon:focus {{
      transform: translateY(-2px); outline: none;
      box-shadow: 0 8px 16px -8px rgba(34,11,80,0.4);
    }}
    .ac-icon-removals:hover  {{ background: #220b50; color: #fff; }}
    .ac-icon-manvan:hover    {{ background: #d4af37; color: #1f1f1f; }}
    .ac-icon-storage:hover   {{ background: #3a1a7a; color: #fff; }}
    .ac-icon-intl:hover      {{ background: #e74c3c; color: #fff; }}

    /* Region sections */
    .ac-region {{ padding: 3rem 1.5rem 2rem; background: #fff; }}
    .ac-region:nth-of-type(odd) {{ background: #fafaff; }}
    .ac-region-inner {{ max-width: 1200px; margin: 0 auto; }}
    .ac-region-head {{ display: flex; align-items: baseline; justify-content: space-between;
      gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;
      padding-bottom: 1rem; border-bottom: 2px solid rgba(212,175,55,0.4); }}
    .ac-region-title {{ color: #220b50; font-size: clamp(1.6rem, 2.5vw, 2.1rem);
      font-weight: 700; margin: 0; letter-spacing: -0.01em; }}
    .ac-region-meta {{ color: #5a5a6a; font-size: 0.85rem;
      text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; margin: 0; }}

    /* Town grid */
    .ac-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 1rem; }}
    .ac-town {{ background: #fff; border: 1px solid #e0dceb; border-radius: 12px;
      padding: 1.1rem 1.25rem; transition: transform .2s, box-shadow .2s, border-color .2s; }}
    .ac-town:hover {{ transform: translateY(-2px);
      box-shadow: 0 14px 30px -20px rgba(34,11,80,0.3); border-color: rgba(34,11,80,0.25); }}
    .ac-town-name {{ color: #220b50 !important; font-size: 1.15rem !important;
      font-weight: 700 !important; margin: 0 0 0.6rem !important; letter-spacing: -0.01em; }}
    .ac-services {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}

    .ac-empty {{ max-width: 600px; margin: 2rem auto; padding: 1.25rem;
      background: #fff; border: 1px dashed #e0dceb; border-radius: 10px;
      color: #5a5a6a; text-align: center; }}
    .ac-empty a {{ color: #220b50; font-weight: 700; }}

    /* Map / depot section */
    .ac-map-section {{ background: linear-gradient(180deg, #fff 0%, #f7f5fb 100%);
      padding: 3rem 1.5rem 2rem; text-align: center; }}
    .ac-map-inner {{ max-width: 760px; margin: 0 auto; }}
    .ac-map-title {{ color: #220b50; font-size: clamp(1.5rem, 2.5vw, 2rem) !important;
      font-weight: 600; margin: 0 0 0.85rem !important; }}
    .ac-map-sub {{ color: #5a5a6a; font-size: 1rem; line-height: 1.65; margin: 0 0 1rem; }}
  </style>
'''


def main():
    text = FP.read_text(encoding="utf-8")
    # Support both the original Webflow markup AND a previous run of this script
    candidate_starts = [
        '<!-- Hero -->\n  <section class="ac-hero">',
        '<section class="ac-hero">',
        '<div class="hp-header inner contact">',
    ]
    start = -1
    for marker in candidate_starts:
        idx = text.find(marker)
        if idx >= 0:
            start = idx
            break
    END_MARKER = '<div class="online-quote-section">'
    end = text.find(END_MARKER)
    if start < 0 or end < 0:
        print(f"Could not locate markers, aborting. start={start}, end={end}")
        return

    new_block = build_body()
    new_text  = text[:start] + new_block + text[end:]
    FP.write_text(new_text, encoding="utf-8")
    print(f"Replaced {end - start} chars with {len(new_block)} chars.")

    # Verify div balance
    import re
    clean = re.sub(r'<script\b.*?</script>', '', new_text, flags=re.S)
    clean = re.sub(r'<style\b.*?</style>', '', clean, flags=re.S)
    opens  = len(re.findall(r'<div\b[^>]*>', clean))
    closes = len(re.findall(r'</div>', clean))
    print(f"Div balance: opens={opens} closes={closes} diff={opens-closes:+d}")


if __name__ == "__main__":
    main()
