#!/usr/bin/env python3
"""Extract all img tags from index.html with surrounding context for SEO audit."""
import re
from pathlib import Path

FILE = Path(__file__).parent / "www.markratcliffemoving.co.uk" / "index.html"
content = FILE.read_text(encoding="utf-8")
lines = content.split("\n")

# Find every line containing <img
img_pattern = re.compile(r"<img\b[^>]*>", re.I)
attr_pattern = re.compile(r'(\w[\w:-]*)\s*=\s*"([^"]*)"')

results = []
for i, line in enumerate(lines, 1):
    for m in img_pattern.finditer(line):
        tag = m.group(0)
        attrs = dict(attr_pattern.findall(tag))
        # Get nearest preceding heading or wrapper context
        ctx_above = []
        for j in range(max(0, i - 10), i - 1):
            l = lines[j].strip()
            if re.search(r"<h[1-6]\b|class=\"[^\"]*(?:section|footer|hero|nav|banner)[^\"]*\"|<title>", l):
                ctx_above.append(l[:200])
        ctx_above = ctx_above[-3:]
        results.append({
            "line": i,
            "src": attrs.get("src", ""),
            "alt": attrs.get("alt", ""),
            "width": attrs.get("width", ""),
            "height": attrs.get("height", ""),
            "class": attrs.get("class", ""),
            "loading": attrs.get("loading", ""),
            "context": ctx_above,
        })

for r in results:
    print(f"--- L{r['line']} ---")
    print(f"  src:    {r['src']}")
    print(f"  alt:    {r['alt']!r}")
    print(f"  w/h:    {r['width']}x{r['height']}")
    print(f"  class:  {r['class']}")
    print(f"  load:   {r['loading']}")
    if r['context']:
        print(f"  ctx:    {r['context'][-1][:160]}")
    print()

print(f"\nTotal: {len(results)} img tags")
