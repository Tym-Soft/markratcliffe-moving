#!/usr/bin/env python3
"""Final pre-flight QA pass.
 1. Verify every functional page has meta title, meta description, H1.
 2. Find every internal link target and confirm the file exists.
 3. Find every image reference and confirm the file exists.
 4. Report sitemap coverage.
"""
import re, json
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

def is_real_page(fp):
    text = fp.read_text(encoding='utf-8', errors='ignore')
    return not ('http-equiv="refresh"' in text and len(text) < 2000)

pages = []
for fp in ROOT.rglob('*.html'):
    if is_real_page(fp):
        pages.append(fp)

print(f"Auditing {len(pages)} functional pages\n")

# ---------- 1) Meta coverage ----------
missing_title = []
missing_desc = []
missing_h1 = []
for fp in pages:
    text = fp.read_text(encoding='utf-8', errors='ignore')
    if not re.search(r'<title>[^<]+</title>', text):
        missing_title.append(fp.name)
    if not re.search(r'<meta[^>]+name="description"[^>]+content="[^"]+', text) \
        and not re.search(r'<meta[^>]+content="[^"]+"[^>]+name="description"', text):
        missing_desc.append(fp.name)
    if not re.search(r'<h1\b[^>]*>[\s\S]+?</h1>', text):
        missing_h1.append(fp.name)

print(f"=== Meta tag coverage ===")
print(f"  Missing <title>:           {len(missing_title)} pages")
print(f"  Missing meta description:  {len(missing_desc)} pages")
print(f"  Missing <h1>:              {len(missing_h1)} pages")
if missing_title[:3]: print(f"    examples: {missing_title[:3]}")
if missing_desc[:3]:  print(f"    examples: {missing_desc[:3]}")
if missing_h1[:3]:    print(f"    examples: {missing_h1[:3]}")
print()

# ---------- 2) Internal link validity ----------
all_html = {fp.relative_to(ROOT).as_posix() for fp in ROOT.rglob('*.html')}
broken_links = []

for fp in pages:
    text = fp.read_text(encoding='utf-8', errors='ignore')
    rel = fp.relative_to(ROOT)
    base = rel.parent if rel.parent != Path('.') else Path('')

    for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"', text):
        href = m.group(1)
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:', 'sms:', 'data:')):
            continue
        target = href.split('#')[0].split('?')[0]
        if not target:
            continue
        target_path = (ROOT / base / target).resolve()
        try:
            rel_target = target_path.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            continue
        if not target_path.exists():
            broken_links.append((fp.name, target))

print(f"=== Internal link validity ===")
print(f"  Broken internal links: {len(broken_links)}")
seen = set()
for src, tgt in broken_links[:8]:
    key = (src, tgt)
    if key in seen: continue
    seen.add(key)
    print(f"    {src} → {tgt}")
print()

# ---------- 3) Image reference validity ----------
images_on_disk = {f.name for f in (ROOT / 'images').iterdir() if f.is_file()}
broken_imgs = set()
for fp in pages:
    text = fp.read_text(encoding='utf-8', errors='ignore')
    for m in re.findall(r'src="images/([^"]+)"', text):
        name = m.split('?')[0]
        if name and name not in images_on_disk:
            broken_imgs.add(name)
    for srcset in re.findall(r'srcset="([^"]+)"', text):
        for part in srcset.split(','):
            part = part.strip()
            if part.startswith('images/'):
                name = part.split()[0][7:].split('?')[0]
                if name and name not in images_on_disk:
                    broken_imgs.add(name)
print(f"=== Image reference validity ===")
print(f"  Broken image refs (unique filenames): {len(broken_imgs)}")
for img in sorted(broken_imgs)[:5]:
    print(f"    {img}")
print()

# ---------- 4) Sitemap coverage ----------
sitemap_path = ROOT / 'sitemap.xml'
sitemap_urls = set()
if sitemap_path.exists():
    sm = sitemap_path.read_text(encoding='utf-8')
    for m in re.finditer(r'<loc>https?://[^/]+/([^<]*)</loc>', sm):
        sitemap_urls.add(m.group(1))

functional_paths = {fp.relative_to(ROOT).as_posix() for fp in pages}
# Normalise: index.html === "" in sitemap
functional_paths_normalised = {('' if p == 'index.html' else p) for p in functional_paths}

missing_from_sitemap = functional_paths_normalised - sitemap_urls
extra_in_sitemap = sitemap_urls - functional_paths_normalised

print(f"=== Sitemap coverage ===")
print(f"  Sitemap URLs:              {len(sitemap_urls)}")
print(f"  Functional pages on disk:  {len(functional_paths_normalised)}")
print(f"  In sitemap, not on disk:   {len(extra_in_sitemap)}")
print(f"  On disk, not in sitemap:   {len(missing_from_sitemap)}")
if missing_from_sitemap:
    for p in sorted(missing_from_sitemap)[:5]:
        print(f"    missing: {p}")
print()

# ---------- 5) Data store integrity ----------
data_pages = list((ROOT / 'data' / 'pages').glob('*.json'))
data_blog  = list((ROOT / 'data' / 'blog').glob('*.json'))
print(f"=== Data store ===")
print(f"  Page JSON records:         {len(data_pages)}")
print(f"  Blog JSON records:         {len(data_blog)}")
print(f"  Functional HTML pages:     {len(pages)}")
print()

print("=== SUMMARY ===")
score = 0; max_score = 5
if not missing_title and not missing_desc and not missing_h1: score += 1; print("  ✓ All pages have title/meta/H1")
else: print("  ✗ Some pages missing essential meta")
if not broken_links: score += 1; print("  ✓ Zero broken internal links")
else: print(f"  ✗ {len(broken_links)} broken internal links")
if not broken_imgs: score += 1; print("  ✓ Zero broken image references")
else: print(f"  ✗ {len(broken_imgs)} broken image references")
if not missing_from_sitemap and not extra_in_sitemap: score += 1; print("  ✓ Sitemap matches disk")
else: print(f"  ⚠ Sitemap discrepancy: +{len(extra_in_sitemap)} / −{len(missing_from_sitemap)}")
if len(data_pages) + len(data_blog) >= len(pages) - 5: score += 1; print("  ✓ Data store has records for most pages")
else: print("  ✗ Data store is incomplete")

print(f"\n  Overall: {score}/{max_score}")
