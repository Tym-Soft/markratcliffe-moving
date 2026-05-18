"""Shared template fragments for new page builds."""

BASE_URL = "https://www.markratcliffemoving.co.uk"
TODAY = "2026-05-18"
TODAY_HTTP = "Mon May 18 2026 12:00:00 GMT+0000 (Coordinated Universal Time)"

ORG_SCHEMA_INLINE = {
    "@type": "MovingCompany",
    "@id": f"{BASE_URL}/#organization",
    "name": "Mark Ratcliffe Moving & Storage",
    "url": BASE_URL,
    "logo": f"{BASE_URL}/images/Mark-Ratcliffe.svg",
    "telephone": "+44-1323-848008",
    "priceRange": "££",
    "foundingDate": "1982",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Lower Dicker",
        "addressLocality": "Hailsham",
        "addressRegion": "East Sussex",
        "postalCode": "BN27 4BU",
        "addressCountry": "GB"
    }
}


def head(title: str, description: str, url_rel: str, extra_schemas: list = None, og_image: str = None):
    """Build <head>. url_rel is relative path from site root (e.g. 'removals-eastbourne.html')."""
    abs_url = f"{BASE_URL}/{url_rel}" if url_rel else BASE_URL + "/"
    image = og_image or f"{BASE_URL}/images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp"

    extra_schemas = extra_schemas or []
    schema_blocks = "\n".join(
        f'  <script type="application/ld+json">{__import__("json").dumps(s, ensure_ascii=False)}</script>'
        for s in extra_schemas
    )

    return f"""<!DOCTYPE html><!-- Last Published: {TODAY_HTTP} -->
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving & Storage">
  <meta name="theme-color" content="#220b50">
  <link rel="canonical" href="{abs_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{abs_url}">
  <meta property="og:image" content="{image}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving & Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link href="css/normalize.css" rel="stylesheet">
  <link href="css/components.css" rel="stylesheet">
  <link href="css/mark-ratcliffe-moving.css" rel="stylesheet">
  <link href="css/new-pages.css" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>WebFont.load({{classes:true,timeout:2000,google:{{families:["Montserrat:300,400,500,600,700","Open Sans:400,600,700","Lato:300,400,700"]}}}});</script>
  <link href="images/favicon.png" rel="shortcut icon">
  <link href="images/webclip.png" rel="apple-touch-icon">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q111LKQEBP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-Q111LKQEBP');</script>
{schema_blocks}
</head>"""


# Navigation — uses the exact existing site structure (nav-section / top-bar-wrapper / navbar)
NAV = """  <div class="nav-section">
    <div class="top-bar-wrapper w-hidden-small w-hidden-tiny">
      <div class="contacts-in-top-wrapper">
        <a href="tel:01323848008" class="tb-link w-inline-block"><div>01323 848 008</div></a>
        <a href="tel:07437414589" class="tb-link mob w-inline-block"><div>07437 414 589</div></a>
        <a href="mailto:mark@markratcliffemoving.co.uk" class="tb-link email w-inline-block"><div>mark@markratcliffemoving.co.uk</div></a>
      </div>
      <div class="banner-script">A member of the British Association of Removers Overseas Group</div>
      <a href="mark-ratcliffe-moving-online-removals-quote.html" class="top-bar-quote">REQUEST A QUOTE</a>
    </div>
    <div data-collapse="medium" data-animation="default" data-duration="400" data-easing="ease" data-easing2="ease" role="banner" class="navbar w-nav">
      <a href="index.html" class="brand w-nav-brand"><img src="images/Mark-Ratcliffe.svg" width="180" height="60" alt="Mark Ratcliffe Moving and Storage — Eastbourne removals company logo" class="logo-img" decoding="async" fetchpriority="high"></a>
      <nav role="navigation" class="nav-menu w-nav-menu">
        <a href="index.html" class="navlink w-nav-link">HOME</a>
        <a href="about-us.html" class="navlink w-nav-link">ABOUT US</a>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>OUR SERVICES</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Removals Eastbourne</a>
            <a href="man-and-van-eastbourne.html" class="dropdown-navlink w-dropdown-link">Man &amp; Van</a>
            <a href="packing-services-eastbourne.html" class="dropdown-navlink w-dropdown-link">Packing Services</a>
            <a href="office-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Office Removals</a>
            <a href="house-clearance-eastbourne.html" class="dropdown-navlink w-dropdown-link">House Clearance</a>
            <a href="international-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">International Removals</a>
            <a href="european-removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">European Removals</a>
          </nav>
        </div>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>AREAS COVERED</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="removals-eastbourne.html" class="dropdown-navlink w-dropdown-link">Eastbourne</a>
            <a href="hailsham-removals.html" class="dropdown-navlink w-dropdown-link">Hailsham</a>
            <a href="removals-polegate.html" class="dropdown-navlink w-dropdown-link">Polegate</a>
            <a href="removals-pevensey.html" class="dropdown-navlink w-dropdown-link">Pevensey</a>
            <a href="removals-willingdon.html" class="dropdown-navlink w-dropdown-link">Willingdon</a>
            <a href="removals-uckfield.html" class="dropdown-navlink w-dropdown-link">Uckfield</a>
            <a href="removals-heathfield.html" class="dropdown-navlink w-dropdown-link">Heathfield</a>
            <a href="removals-bexhill.html" class="dropdown-navlink w-dropdown-link">Bexhill</a>
            <a href="areas-covered.html" class="dropdown-navlink w-dropdown-link">All Areas &rarr;</a>
          </nav>
        </div>
        <div data-hover="false" data-delay="0" class="navlink dropdown w-dropdown">
          <div class="dropdown-toggle w-dropdown-toggle"><div class="icon w-icon-dropdown-toggle"></div><div>RESOURCES</div></div>
          <nav class="dropdown-list w-dropdown-list">
            <a href="moving-checklist-eastbourne.html" class="dropdown-navlink w-dropdown-link">Moving Checklist</a>
            <a href="removals-eastbourne-cost.html" class="dropdown-navlink w-dropdown-link">Cost Guide</a>
            <a href="faqs.html" class="dropdown-navlink w-dropdown-link">FAQs</a>
            <a href="blog/index.html" class="dropdown-navlink w-dropdown-link">Blog</a>
          </nav>
        </div>
        <a href="storage-eastbourne.html" class="navlink w-nav-link">SELF STORAGE</a>
        <a href="thai-moving-services.html" class="navlink w-nav-link">UK - THAI</a>
        <a href="reviews.html" class="navlink w-nav-link">REVIEWS</a>
        <a href="contact-us.html" class="navlink w-nav-link">CONTACT</a>
      </nav>
      <div class="menu-button w-nav-button"><div class="w-icon-nav-menu"></div></div>
    </div>
  </div>"""


def hero(title: str, kicker: str = "", image: str = "images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp"):
    return f"""  <header class="np-hero">
    <div class="np-hero-inner">
      {f'<div class="np-kicker">{kicker}</div>' if kicker else ''}
      <h1>{title}</h1>
      <div class="np-hero-cta">
        <a href="mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="{image}" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high">
  </header>"""


FOOTER = """  <footer class="np-footer">
    <div class="np-footer-map"><iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2523.049709930351!2d0.29392331613135825!3d50.77465207183167!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47df7392bfec7151%3A0xf536886de6399c2e!2sMark+Ratcliffe+Moving+%26+Storage+Ltd!5e0!3m2!1sen!2suk!4v1549285879259" width="100%" height="100%" frameborder="0" style="border:0" allowfullscreen="" loading="lazy" title="Mark Ratcliffe Moving &amp; Storage Ltd — Lower Dicker location map"></iframe></div>
    <div class="np-footer-grid">
      <div class="np-footer-col">
        <img src="images/Mark-Ratcliffe.svg" width="200" height="68" alt="Mark Ratcliffe Moving and Storage logo" decoding="async" loading="lazy">
        <p>Family-run removals and storage company serving Eastbourne, Hailsham and Sussex since 1982. BAR registered. Premium pad-wrap protection on every move.</p>
      </div>
      <div class="np-footer-col">
        <h4>Contact</h4>
        <p><a href="tel:01323848008">01323 848 008</a><br>
        <a href="tel:07437414589">07437 414 589</a><br>
        <a href="mailto:mark@markratcliffemoving.co.uk">mark@markratcliffemoving.co.uk</a></p>
        <p>Lower Dicker<br>Hailsham, East Sussex<br>BN27 4BU</p>
      </div>
      <div class="np-footer-col">
        <h4>Services</h4>
        <ul class="np-footer-list">
          <li><a href="removals-eastbourne.html">Removals Eastbourne</a></li>
          <li><a href="man-and-van-eastbourne.html">Man &amp; Van</a></li>
          <li><a href="packing-services-eastbourne.html">Packing Services</a></li>
          <li><a href="storage-eastbourne.html">Storage</a></li>
          <li><a href="office-removals-eastbourne.html">Office Removals</a></li>
          <li><a href="international-removals-eastbourne.html">International</a></li>
        </ul>
      </div>
      <div class="np-footer-col">
        <h4>Areas Covered</h4>
        <ul class="np-footer-list">
          <li><a href="hailsham-removals.html">Hailsham</a></li>
          <li><a href="removals-polegate.html">Polegate</a></li>
          <li><a href="removals-pevensey.html">Pevensey</a></li>
          <li><a href="removals-willingdon.html">Willingdon</a></li>
          <li><a href="removals-uckfield.html">Uckfield</a></li>
          <li><a href="removals-heathfield.html">Heathfield</a></li>
          <li><a href="removals-bexhill.html">Bexhill</a></li>
          <li><a href="areas-covered.html">All Areas →</a></li>
        </ul>
      </div>
      <div class="np-footer-col">
        <h4>Resources</h4>
        <ul class="np-footer-list">
          <li><a href="moving-checklist-eastbourne.html">Moving Checklist</a></li>
          <li><a href="removals-eastbourne-cost.html">Cost Guide</a></li>
          <li><a href="faqs.html">FAQs</a></li>
          <li><a href="blog/index.html">Blog</a></li>
          <li><a href="reviews.html">Reviews</a></li>
        </ul>
      </div>
    </div>
    <div class="np-footer-bottom">
      <p>&copy; 1982–2026 Mark Ratcliffe Moving &amp; Storage Ltd. BAR registered. <a href="terms-conditions-and-insurance-details.html">Terms &amp; Insurance</a></p>
    </div>
  </footer>"""


CLOSE = """  <script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=54f032c21ccd6c2e19dae5a7" crossorigin="anonymous"></script>
  <script defer src="js/mark-ratcliffe-moving.js"></script>
</body>
</html>"""


def cta_block(heading="Ready to book your move?"):
    return f"""    <section class="np-section np-cta-block">
      <div class="np-inner">
        <h2>{heading}</h2>
        <p>Call us today for a free, no-obligation quote — or use our online form. Whether it's a one-room move or a full international relocation, we've handled it before.</p>
        <div class="np-cta-row">
          <a href="mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
          <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
        </div>
      </div>
    </section>"""


def render(meta, body):
    """Assemble a full HTML page."""
    return (
        head(meta["title"], meta["description"], meta["url_rel"],
             extra_schemas=meta.get("schemas", []),
             og_image=meta.get("og_image"))
        + "\n<body>\n"
        + NAV + "\n"
        + body + "\n"
        + cta_block() + "\n"
        + FOOTER + "\n"
        + CLOSE
    )


def breadcrumbs_schema(items):
    """items: list of (name, url_rel) tuples. Last one is current page."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": f"{BASE_URL}/{rel}" if rel else f"{BASE_URL}/"
            }
            for i, (name, rel) in enumerate(items)
        ]
    }


def faq_schema(qas):
    """qas: list of (question, answer_html_plaintext)."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            }
            for q, a in qas
        ]
    }


def service_schema(name, description, area_served="East Sussex"):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "provider": {"@id": f"{BASE_URL}/#organization"},
        "areaServed": area_served,
        "serviceType": name
    }


def render_faq_accordion(qas):
    out = ['    <section class="np-section np-faq">', '      <div class="np-inner">', '        <h2>Frequently Asked Questions</h2>']
    for q, a in qas:
        out.append(f'        <details><summary>{q}</summary><p>{a}</p></details>')
    out.append('      </div>')
    out.append('    </section>')
    return "\n".join(out)
