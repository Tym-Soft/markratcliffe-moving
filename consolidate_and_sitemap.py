#!/usr/bin/env python3
"""Consolidate old pages with meta-refresh redirects + rebuild sitemap with today's date."""
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
BASE_URL = "https://www.markratcliffemoving.co.uk"
TODAY = "2026-05-18"

# Old URL -> New URL mapping (for consolidation)
REDIRECTS = {
    "secure-self-storage-rooms.html": "storage-eastbourne.html",
    "overseas-services.html": "international-removals-eastbourne.html",
    "man-van.html": "man-and-van-eastbourne.html",
    "domestic-services.html": "removals-eastbourne.html",
    "testimonials.html": "reviews.html",
    "areas-covered/removals-eastbourne.html": "../removals-eastbourne.html",
    "areas-covered/removals-bexhill.html": "../removals-bexhill.html",
    "areas-covered/man-with-a-van-eastbourne.html": "../man-and-van-eastbourne.html",
    "areas-covered/man-and-van-eastbourne.html": "../man-and-van-eastbourne.html",
    "areas-covered/removals-hailsham.html": "../hailsham-removals.html",
    "areas-covered/man-and-van-hailsham.html": "../hailsham-removals.html",
    "areas-covered/removals-uckfield.html": "../removals-uckfield.html",
    "areas-covered/removals-heathfield.html": "../removals-heathfield.html",
    "areas-covered/removals-polegate-moving-home-in-east-sussex.html": "../removals-polegate.html",
}


def make_redirect_html(target: str, title: str = "Redirecting..."):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta http-equiv="refresh" content="0;url={target}">
  <link rel="canonical" href="{BASE_URL}/{target.lstrip('../')}">
  <meta name="robots" content="noindex,follow">
</head>
<body>
  <p>This page has moved. <a href="{target}">Click here if you are not redirected automatically.</a></p>
  <script>window.location.replace("{target}");</script>
</body>
</html>"""


def apply_redirects():
    n = 0
    for old, new in REDIRECTS.items():
        p = ROOT / old
        if p.exists():
            p.write_text(make_redirect_html(new), encoding="utf-8")
            n += 1
    print(f"Applied {n} redirects.")


def build_sitemap():
    """Rebuild sitemap with all current URLs and today's date."""
    urls = []
    redirect_paths = set(REDIRECTS.keys())

    # Root-level HTML pages (not redirects)
    for fp in sorted(ROOT.glob("*.html")):
        rel = fp.name
        if rel in redirect_paths:
            continue
        urls.append(rel)

    # Blog pages
    if (ROOT / "blog").exists():
        for fp in sorted((ROOT / "blog").glob("*.html")):
            urls.append(f"blog/{fp.name}")

    # Original area pages (kept, not redirected) — they still rank
    if (ROOT / "areas-covered").exists():
        for fp in sorted((ROOT / "areas-covered").glob("*.html")):
            rel = f"areas-covered/{fp.name}"
            if rel in redirect_paths:
                continue
            urls.append(rel)

    def priority(rel: str):
        if rel == "index.html":
            return ("1.0", "weekly")
        # Main new service pages
        if rel in ("removals-eastbourne.html", "international-removals-eastbourne.html",
                   "storage-eastbourne.html", "man-and-van-eastbourne.html",
                   "packing-services-eastbourne.html", "office-removals-eastbourne.html",
                   "house-clearance-eastbourne.html", "european-removals-eastbourne.html"):
            return ("0.95", "weekly")
        # New area pages
        if rel in ("hailsham-removals.html", "removals-polegate.html", "removals-pevensey.html",
                   "removals-willingdon.html", "removals-uckfield.html", "removals-heathfield.html",
                   "removals-bexhill.html"):
            return ("0.9", "monthly")
        # Resources
        if rel in ("faqs.html", "moving-checklist-eastbourne.html", "removals-eastbourne-cost.html"):
            return ("0.85", "monthly")
        # Blog
        if rel.startswith("blog/"):
            return ("0.8", "monthly")
        # Areas-covered subpages
        if rel.startswith("areas-covered/"):
            return ("0.7", "monthly")
        if rel in ("contact-us.html", "about-us.html", "testimonials.html",
                   "mark-ratcliffe-moving-online-removals-quote.html"):
            return ("0.7", "monthly")
        return ("0.5", "yearly")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in urls:
        url = f"{BASE_URL}/" if rel == "index.html" else f"{BASE_URL}/{rel}"
        prio, freq = priority(rel)
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"sitemap.xml written ({len(urls)} URLs).")


def update_dates_in_html():
    """Update Last Published HTML comments to today across all pages."""
    n = 0
    for fp in list(ROOT.rglob("*.html")):
        text = fp.read_text(encoding="utf-8")
        new = text
        # Match any 'Last Published' comment with any date and replace
        import re
        new = re.sub(
            r'<!--\s*Last Published:.*?-->',
            f'<!-- Last Published: Mon May 18 2026 12:00:00 GMT+0000 (Coordinated Universal Time) -->',
            new, count=1
        )
        # Also update schema dateModified strings
        new = new.replace('"dateModified": "2026-05-17"', '"dateModified": "2026-05-18"')
        new = new.replace('"datePublished": "2026-05-17"', '"datePublished": "2026-05-18"')
        if new != text:
            fp.write_text(new, encoding="utf-8")
            n += 1
    print(f"Date stamps updated in {n} files.")


if __name__ == "__main__":
    apply_redirects()
    update_dates_in_html()
    build_sitemap()
