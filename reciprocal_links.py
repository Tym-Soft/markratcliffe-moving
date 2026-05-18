#!/usr/bin/env python3
"""Find one-way body-content links between pages and add back-links.

We exclude links inside the nav (.nav-section / .navbar) and the footer
(.np-footer / .footer / .footer-map-wrapper) because those are persistent
on every page and would otherwise dominate the link graph.
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

# Pages we want to audit (skip redirect stubs)
def is_real_page(fp: Path) -> bool:
    text = fp.read_text(encoding="utf-8")
    return not ('http-equiv="refresh"' in text and len(text) < 2000)

# Strip nav and footer from HTML before extracting links
NAV_RE = re.compile(r'<div class="nav-section">.*?</div>\s*</div>\s*</div>', re.S)
NP_FOOTER_RE = re.compile(r'<footer class="np-footer">.*?</footer>', re.S)
WF_FOOTER_RE = re.compile(r'<div class="footer">.*?(?=<!-- (?:Copyright)? -->|\Z)', re.S)
MAP_RE = re.compile(r'<div class="(?:footer-map-wrapper|np-footer-map)"[^>]*>.*?</div>(?:\s*</div>)?', re.S)

def strip_chrome(text: str) -> str:
    text = NAV_RE.sub('', text)
    text = NP_FOOTER_RE.sub('', text)
    text = WF_FOOTER_RE.sub('', text)
    text = MAP_RE.sub('', text)
    return text


def normalize_target(href: str, source_dir: Path) -> str:
    """Convert relative href to a canonical 'slug.html' (root-relative)."""
    if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '?')):
        return ""
    # Strip anchor and query
    href = href.split('#')[0].split('?')[0]
    if not href:
        return ""
    # Resolve relative to source_dir
    target = (source_dir / href).resolve()
    try:
        rel = target.relative_to(ROOT.resolve())
    except ValueError:
        return ""
    return rel.as_posix()


def build_graph():
    """Returns {source_page: set(target_pages)} for body-content links only."""
    graph = defaultdict(set)
    pages = [fp for fp in ROOT.rglob("*.html") if is_real_page(fp)]
    for fp in pages:
        text = fp.read_text(encoding="utf-8")
        body = strip_chrome(text)
        source = fp.relative_to(ROOT).as_posix()
        source_dir = fp.parent
        for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"', body):
            target = normalize_target(m.group(1), source_dir)
            if target and target != source and target.endswith('.html'):
                graph[source].add(target)
    return graph, [fp.relative_to(ROOT).as_posix() for fp in pages]


def find_one_way(graph):
    """Return list of (source, target) where source→target exists but target→source missing."""
    one_way = []
    for src, targets in graph.items():
        for tgt in targets:
            if src not in graph.get(tgt, set()):
                one_way.append((src, tgt))
    return one_way


def page_title(fp: Path) -> str:
    text = fp.read_text(encoding="utf-8")
    m = re.search(r'<title>([^<]+)</title>', text)
    if m:
        # Take the part before " | " (brand)
        return m.group(1).split('|')[0].strip()
    return fp.stem.replace('-', ' ').title()


def insert_related(fp: Path, links_back: list):
    """Insert a 'Related pages' block before the CTA section or end of body."""
    if not links_back:
        return False
    text = fp.read_text(encoding="utf-8")

    # Build the related-pages HTML block
    items = []
    for slug in sorted(set(links_back)):
        target = ROOT / slug
        if not target.exists():
            continue
        title = page_title(target)
        # Build correct relative href from current page
        if '/' in fp.relative_to(ROOT).as_posix() and '/' not in slug:
            href = '../' + slug
        elif '/' not in fp.relative_to(ROOT).as_posix() and '/' in slug:
            href = slug
        else:
            href = slug.split('/')[-1] if fp.parent != ROOT else slug
        items.append(f'          <li><a href="{href}">{title}</a></li>')
    if not items:
        return False

    block = (
        '\n    <section class="np-section np-related" aria-label="Related pages">\n'
        '      <div class="np-inner">\n'
        '        <h2>Related pages on our site</h2>\n'
        '        <ul class="np-related-list">\n'
        + "\n".join(items) + "\n"
        '        </ul>\n'
        '      </div>\n'
        '    </section>\n'
    )

    # Skip if already present
    if 'class="np-section np-related"' in text:
        return False

    # Insert before the np-cta-block if present
    if 'class="np-section np-cta-block"' in text:
        new = text.replace('    <section class="np-section np-cta-block">',
                           block + '    <section class="np-section np-cta-block">', 1)
    elif '<footer class="np-footer">' in text:
        new = text.replace('<footer class="np-footer">', block + '  <footer class="np-footer">', 1)
    elif '<div class="footer">' in text:
        # Original Webflow pages — insert before footer
        new = text.replace('<div class="footer">', block + '  <div class="footer">', 1)
    else:
        return False

    if new != text:
        fp.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    graph, all_pages = build_graph()
    one_way = find_one_way(graph)
    print(f"Pages audited: {len(all_pages)}")
    print(f"Body-content links: {sum(len(t) for t in graph.values())}")
    print(f"One-way edges (A→B with no B→A): {len(one_way)}")

    # Group by target — for each target, list the pages linking to it that don't get a back-link
    targets_need_backlinks = defaultdict(list)
    for src, tgt in one_way:
        targets_need_backlinks[tgt].append(src)

    print(f"Pages needing back-links added: {len(targets_need_backlinks)}")

    # Add reciprocal links
    added = 0
    for target_slug, sources in targets_need_backlinks.items():
        target_fp = ROOT / target_slug
        if not target_fp.exists():
            continue
        # Cap at top 6 most-relevant back-links to avoid bloat
        sources_to_link = sources[:6]
        if insert_related(target_fp, sources_to_link):
            added += 1
    print(f"Inserted 'Related pages' block on {added} pages.")


if __name__ == "__main__":
    main()
