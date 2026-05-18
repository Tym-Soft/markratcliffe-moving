#!/usr/bin/env python3
"""Inventory schema.org JSON-LD blocks on every HTML page."""
import re, glob, json

JSONLD_RE = re.compile(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', re.DOTALL | re.I)

rows = []
missing = []
for path in sorted(glob.glob('*.html') + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html')):
    text = open(path, encoding='utf-8', errors='ignore').read()
    blocks = JSONLD_RE.findall(text)
    types = []
    for b in blocks:
        try:
            data = json.loads(b)
            if isinstance(data, dict) and '@graph' in data:
                for item in data['@graph']:
                    if isinstance(item, dict) and '@type' in item:
                        t = item['@type']
                        types.append(t if isinstance(t, str) else '|'.join(t))
            elif isinstance(data, dict) and '@type' in data:
                t = data['@type']
                types.append(t if isinstance(t, str) else '|'.join(t))
        except Exception:
            types.append('(parse error)')
    rows.append((path, len(blocks), types))
    if not blocks:
        missing.append(path)

print(f"{'PAGE':<70}{'#':>3}  TYPES")
print('-' * 110)
for path, n, types in rows:
    print(f"{path:<70}{n:>3}  {', '.join(types)}")

print(f"\n{'='*60}")
print(f"Total pages: {len(rows)}")
print(f"With schema: {len(rows) - len(missing)}")
print(f"Missing:     {len(missing)}")
if missing:
    print("\nPages WITHOUT any schema:")
    for p in missing:
        print(f"  {p}")
