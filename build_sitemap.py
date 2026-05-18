#!/usr/bin/env python3
"""Build sitemap.xml and robots.txt for the mirrored site."""
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
BASE_URL = "https://www.markratcliffemoving.co.uk"
TODAY = "2026-05-17"

# Priority + changefreq per URL pattern
def priority(rel: str):
    if rel == "":
        return ("1.0", "weekly")
    if rel in ("domestic-services.html", "overseas-services.html",
              "secure-self-storage-rooms.html", "man-van.html",
              "thai-moving-services.html", "areas-covered.html",
              "packaging-shop.html"):
        return ("0.9", "monthly")
    if rel.startswith("areas-covered/"):
        return ("0.8", "monthly")
    if rel in ("contact-us.html", "about-us.html",
              "mark-ratcliffe-moving-online-removals-quote.html",
              "testimonials.html", "careers.html"):
        return ("0.7", "monthly")
    return ("0.5", "yearly")

def collect_urls():
    pages = []
    for fp in ROOT.glob("*.html"):
        rel = fp.name
        if rel == "index.html":
            pages.append("")
        else:
            pages.append(rel)
    for fp in (ROOT / "areas-covered").glob("*.html"):
        pages.append(f"areas-covered/{fp.name}")
    return sorted(pages)

def build_sitemap():
    urls = collect_urls()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:image="http://www.google.com/schemas/sitemap-image/0.9">']
    for rel in urls:
        url = f"{BASE_URL}/" if rel == "" else f"{BASE_URL}/{rel}"
        prio, freq = priority(rel)
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"sitemap.xml written ({len(urls)} URLs)")

def build_robots():
    txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /css/\n"
        "Disallow: /js/\n"
        "\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(txt, encoding="utf-8")
    print("robots.txt written")

if __name__ == "__main__":
    build_sitemap()
    build_robots()
