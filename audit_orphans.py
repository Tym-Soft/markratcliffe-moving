#!/usr/bin/env python3
"""Find files on disk that nothing references."""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
EXCLUDE_DIRS = {'.git', 'admin-portal-xK7p9q', 'data', 'admin_build', 'page_builder', '__pycache__'}

# Collect every file on disk we care about
def collect_files(extensions):
    out = set()
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in extensions:
            out.add(str(p.relative_to(ROOT)))
    return out

html_files = collect_files({'.html'})
image_files = collect_files({'.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico'})
css_files = collect_files({'.css'})
js_files = collect_files({'.js'})

# Build the set of files that are *referenced* somewhere
referenced = set()

# Scan HTML for href / src / srcset / data-src
href_re = re.compile(r'''(?:href|src|action|data-src|content)\s*=\s*["']([^"'#?\s]+)''', re.I)
srcset_re = re.compile(r'''srcset\s*=\s*["']([^"']+)''', re.I)
css_url_re = re.compile(r'''url\(\s*["']?([^"')\s]+)''', re.I)

def normalize(ref, source_path):
    """Resolve relative ref into a repo-root-relative path."""
    ref = ref.strip()
    if ref.startswith(('http://', 'https://', '//', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    if ref.startswith('/'):
        ref = ref.lstrip('/')
    else:
        ref = str((Path(source_path).parent / ref).resolve().relative_to(ROOT.resolve())) if (ROOT / Path(source_path).parent / ref).resolve().is_relative_to(ROOT.resolve()) else None
    return ref

def scan(source_path):
    """Yield every referenced relative path from this file."""
    try:
        text = (ROOT / source_path).read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return
    for m in href_re.finditer(text):
        ref = normalize(m.group(1), source_path)
        if ref: yield ref
    for m in srcset_re.finditer(text):
        for part in m.group(1).split(','):
            url = part.strip().split()[0] if part.strip() else ''
            if url:
                ref = normalize(url, source_path)
                if ref: yield ref
    for m in css_url_re.finditer(text):
        ref = normalize(m.group(1), source_path)
        if ref: yield ref

# Pages reachable from sitemap.xml are alive
sitemap = ROOT / 'sitemap.xml'
if sitemap.exists():
    for m in re.finditer(r'<loc>([^<]+)</loc>', sitemap.read_text()):
        url = m.group(1)
        rel = url.split('://', 1)[-1].split('/', 1)[-1] or 'index.html'
        if not rel.endswith('.html') and '/' not in rel.rstrip('/'):
            rel = rel.rstrip('/') + '/index.html' if rel else 'index.html'
        referenced.add(rel)
referenced.add('index.html')
referenced.add('CNAME')
referenced.add('.nojekyll')
referenced.add('robots.txt')
referenced.add('sitemap.xml')
referenced.add('.htaccess')

# Scan HTML + CSS + JS for references
all_sources = html_files | css_files | js_files
for f in all_sources:
    for ref in scan(f):
        if ref:
            referenced.add(ref)
            # Pre-resize variants: if foo.webp is referenced, foo-p-500.webp is implicitly a variant
            # Already captured via srcset, no action needed
    # Also keep the source itself referenced if anything pointed at it
referenced |= set(all_sources)  # HTML/CSS/JS keep each other in scope

orphans = {
    'images': sorted(image_files - referenced),
    'css': sorted(css_files - referenced),
    'js': sorted(js_files - referenced),
    'html': sorted(html_files - referenced),
}

# HTML orphan check: also check if any html links to it as href
html_refs = set()
for f in all_sources:
    for ref in scan(f):
        if ref and ref.endswith('.html'):
            html_refs.add(ref)
orphans['html'] = sorted(html_files - html_refs - {'index.html', '404.html'})

print(f"DISK INVENTORY:")
print(f"  HTML pages: {len(html_files)}")
print(f"  Images:     {len(image_files)}")
print(f"  CSS files:  {len(css_files)}")
print(f"  JS files:   {len(js_files)}")
print()
print(f"ORPHANS (nothing references them):")
print(f"  Images:     {len(orphans['images'])}")
print(f"  CSS files:  {len(orphans['css'])}")
print(f"  JS files:   {len(orphans['js'])}")
print(f"  HTML pages: {len(orphans['html'])}")
print()
for kind, files in orphans.items():
    if not files: continue
    print(f"=== Orphan {kind} ({len(files)}) ===")
    for f in files:
        print(f"  {f}")
    print()
