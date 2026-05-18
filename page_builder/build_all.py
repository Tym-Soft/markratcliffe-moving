#!/usr/bin/env python3
"""Build all pages with expansions, then run nav JS fix, then update sitemap."""
import sys, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from template import render
from expansions import EXPANSION_MAP
import pages_services
import pages_areas
import pages_resources
import pages_blog

OUT = Path(__file__).resolve().parent.parent / "www.markratcliffemoving.co.uk"


def inject_expansion(body: str, slug: str) -> str:
    """Insert expansion block before the FAQ accordion (which starts with np-faq class)."""
    ex = EXPANSION_MAP.get(slug)
    if not ex:
        return body
    # Insert before the FAQ section
    if 'class="np-section np-faq"' in body:
        return body.replace('<section class="np-section np-faq">', ex + '\n    <section class="np-section np-faq">', 1)
    # FAQs page has no faq accordion at end — append at end
    if slug == "faqs":
        return body + ex
    return body + ex


def build_services():
    for slug, func in pages_services.PAGES:
        meta, body = func()
        body = inject_expansion(body, slug)
        html = render(meta, body)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
    print(f"Built {len(pages_services.PAGES)} service pages.")


def build_areas():
    for slug, data in pages_areas.AREAS.items():
        # Render the area page then inject expansion
        html_full = pages_areas.render_area_page(slug, data)
        # The render path already returned full html. We need to inject INSIDE body.
        ex = EXPANSION_MAP.get(slug)
        if ex:
            # Insert before the FAQ section pattern
            html_full = html_full.replace(
                '<section class="np-section np-faq">',
                ex + '\n    <section class="np-section np-faq">',
                1
            )
        (OUT / f"{slug}.html").write_text(html_full, encoding="utf-8")
    print(f"Built {len(pages_areas.AREAS)} area pages.")


def build_resources():
    for slug, func in pages_resources.PAGES:
        meta, body = func()
        body = inject_expansion(body, slug)
        html = render(meta, body)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
    print(f"Built {len(pages_resources.PAGES)} resource pages.")


def build_blog():
    pages_blog.build_all()


def main():
    build_services()
    build_areas()
    build_resources()
    build_blog()


if __name__ == "__main__":
    main()
