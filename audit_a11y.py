#!/usr/bin/env python3
"""Find heading-order and identical-link issues across all pages."""
import re, glob, sys
from collections import defaultdict

def strip_html(s):
    return re.sub(r'<[^>]+>', '', s).strip()

heading_issues = []
link_issues = []

for f in sorted(glob.glob('*.html') + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html')):
    text = open(f, encoding='utf-8', errors='ignore').read()

    # --- Heading order: never skip down (h1->h3 is bad)
    levels = [(m.start(), int(m.group(1)), strip_html(m.group(2))[:60])
              for m in re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', text, re.DOTALL)]
    last = 0
    for pos, lvl, txt in levels:
        if last and lvl > last + 1:
            heading_issues.append((f, last, lvl, txt))
        last = lvl

    # --- Identical-link audit: same text → different href, OR same href → different text
    # Only consider visible-text anchors (ignore image-only)
    anchors = []
    for m in re.finditer(r'<a\b([^>]*?)>(.*?)</a>', text, re.DOTALL):
        attrs = m.group(1)
        inner = strip_html(m.group(2)).lower()
        if not inner: continue  # image-only or empty link — skip
        href_match = re.search(r'href=["\']([^"\']+)', attrs)
        if not href_match: continue
        href = href_match.group(1).split('#')[0].split('?')[0]
        if href.startswith(('tel:', 'mailto:', 'javascript:')): continue
        anchors.append((inner, href))

    # Same text → different href (real Lighthouse failure)
    text_to_hrefs = defaultdict(set)
    for txt, href in anchors:
        text_to_hrefs[txt].add(href)
    for txt, hrefs in text_to_hrefs.items():
        if len(hrefs) > 1 and len(txt) > 2:
            link_issues.append((f, 'SAME-TEXT-DIFF-HREF', txt, sorted(hrefs)))

print(f"=== HEADING ORDER ISSUES ({len(heading_issues)}) ===")
for f, last, lvl, txt in heading_issues[:40]:
    print(f"  {f}: h{last} → h{lvl}  (\"{txt}\")")
if len(heading_issues) > 40:
    print(f"  ... +{len(heading_issues)-40} more")

print(f"\n=== LINK ISSUES ({len(link_issues)}) ===")
for f, kind, txt, hrefs in link_issues[:40]:
    print(f"  {f}: '{txt}' → {hrefs}")
if len(link_issues) > 40:
    print(f"  ... +{len(link_issues)-40} more")
