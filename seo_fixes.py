#!/usr/bin/env python3
"""Apply SEO fixes across mirrored Mark Ratcliffe Moving site."""
import os, re, json, html
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
BASE_URL = "https://www.markratcliffemoving.co.uk"
TODAY = "2026-05-17"
TODAY_HTTP = "Sun May 17 2026 12:00:00 GMT+0000 (Coordinated Universal Time)"

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "MovingCompany",
    "name": "Mark Ratcliffe Moving & Storage",
    "url": BASE_URL,
    "logo": f"{BASE_URL}/images/mark-ratcliffe-moving-logo.png",
    "image": f"{BASE_URL}/images/mark-ratcliffe-vans-front2.jpg",
    "description": "Eastbourne's trusted family-run removals and storage company serving Sussex and Surrey since 1982.",
    "telephone": "+44-1323-431199",
    "priceRange": "££",
    "foundingDate": "1982",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Birch Industrial Estate",
        "addressLocality": "Eastbourne",
        "addressRegion": "East Sussex",
        "postalCode": "BN23 6PH",
        "addressCountry": "GB"
    },
    "areaServed": [
        {"@type": "City", "name": "Eastbourne"},
        {"@type": "City", "name": "Brighton"},
        {"@type": "City", "name": "Hastings"},
        {"@type": "City", "name": "Newhaven"},
        {"@type": "City", "name": "Lewes"},
        {"@type": "AdministrativeArea", "name": "East Sussex"},
        {"@type": "AdministrativeArea", "name": "West Sussex"},
        {"@type": "AdministrativeArea", "name": "Surrey"}
    ],
    "sameAs": [
        "https://www.facebook.com/markratcliffemoving",
        "https://www.instagram.com/markratcliffemoving"
    ],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "17:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"}
    ]
}

def get_html_files():
    files = list(ROOT.glob("*.html"))
    files += list((ROOT / "areas-covered").glob("*.html"))
    return files

def get_url(filepath: Path) -> str:
    rel = filepath.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{rel}"

def get_relative_prefix(filepath: Path) -> str:
    """Return '../' if file is in subdirectory, else ''."""
    rel = filepath.relative_to(ROOT)
    return "../" if len(rel.parts) > 1 else ""

def extract_title(content: str) -> str:
    m = re.search(r"<title>(.*?)</title>", content, re.S)
    return html.unescape(m.group(1).strip()) if m else ""

def extract_description(content: str) -> str:
    m = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', content)
    return html.unescape(m.group(1)) if m else ""

def add_canonical_and_schema(content: str, filepath: Path) -> str:
    url = get_url(filepath)
    title = extract_title(content)
    description = extract_description(content)

    # Skip if already added
    if 'rel="canonical"' in content:
        return content

    page_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "name": title,
        "description": description,
        "inLanguage": "en-GB",
        "dateModified": TODAY,
        "isPartOf": {
            "@type": "WebSite",
            "url": BASE_URL,
            "name": "Mark Ratcliffe Moving & Storage"
        },
        "about": {"@id": f"{BASE_URL}/#organization"}
    }

    # Add @id to org schema once for cross-referencing
    org = dict(ORG_SCHEMA)
    org["@id"] = f"{BASE_URL}/#organization"

    graph = {"@context": "https://schema.org", "@graph": [org, page_schema]}
    json_ld = json.dumps(graph, indent=2, ensure_ascii=False)

    inserts = (
        f'  <link rel="canonical" href="{url}">\n'
        f'  <meta name="robots" content="index,follow,max-image-preview:large">\n'
        f'  <meta name="author" content="Mark Ratcliffe Moving & Storage">\n'
        f'  <meta name="theme-color" content="#220b50">\n'
        f'  <meta property="og:url" content="{url}">\n'
        f'  <meta property="og:site_name" content="Mark Ratcliffe Moving & Storage">\n'
        f'  <meta property="og:locale" content="en_GB">\n'
        f'  <script type="application/ld+json">\n{json_ld}\n  </script>\n'
    )

    # Insert before </head>
    return content.replace("</head>", inserts + "</head>", 1)

def update_published_date(content: str) -> str:
    return re.sub(
        r"<!--\s*Last Published:.*?-->",
        f"<!-- Last Published: {TODAY_HTTP} -->",
        content,
        count=1
    )

def add_lazy_loading(content: str) -> str:
    """Add loading=lazy + decoding=async to img tags that don't have it."""
    # First img on page (hero) → eager; rest lazy
    img_pattern = re.compile(r"<img\b([^>]*)>", re.I)
    counter = {"n": 0}

    def replace(m):
        attrs = m.group(1)
        counter["n"] += 1
        if "loading=" in attrs:
            return m.group(0)
        if "decoding=" not in attrs:
            attrs = attrs + ' decoding="async"'
        # First image: keep eager (LCP); rest: lazy
        if counter["n"] == 1:
            attrs = attrs + ' fetchpriority="high"'
        else:
            attrs = attrs + ' loading="lazy"'
        return f"<img{attrs}>"

    return img_pattern.sub(replace, content)

def defer_scripts(content: str) -> str:
    """Add defer to non-critical scripts that are not async and not inline."""
    # Match <script src="..." ...> without async or defer (but preserve gtag config logic)
    def replace(m):
        tag = m.group(0)
        if "async" in tag or "defer" in tag:
            return tag
        # webfont loader is async-friendly, GA already async
        return tag.replace("<script ", "<script defer ", 1)
    # Only target script tags with src attribute that don't already have async/defer
    pattern = re.compile(r'<script\s+(?![^>]*\b(?:async|defer)\b)[^>]*\bsrc="[^"]+"[^>]*></script>', re.I)
    return pattern.sub(replace, content)

def main():
    files = get_html_files()
    print(f"Processing {len(files)} HTML files...")
    for fp in files:
        content = fp.read_text(encoding="utf-8")
        original = content
        content = update_published_date(content)
        content = add_canonical_and_schema(content, fp)
        content = add_lazy_loading(content)
        content = defer_scripts(content)
        if content != original:
            fp.write_text(content, encoding="utf-8")
    print("Done.")

if __name__ == "__main__":
    main()
