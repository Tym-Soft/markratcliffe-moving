#!/usr/bin/env python3
"""
Rewrite internal links so they use directory-style URLs and never
expose `index.html` to users or crawlers.

  href="index.html"         → href="./"
  href="../index.html"      → href="../"
  href="blog/index.html"    → href="blog/"
  href="../blog/index.html" → href="../blog/"
  href="/index.html"        → href="/"
  https://...co.uk/index.html → https://...co.uk/
  https://...co.uk/blog/index.html → https://...co.uk/blog/

Only rewrites href attributes inside HTML files. The index.html files
themselves stay on disk (GitHub Pages needs them to serve directory
URLs) but no link surfaces them, no sitemap entry surfaces them, and
the canonical on each index file points to its directory URL.

Idempotent — safe to re-run.
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# (regex, replacement) — replacements applied in order on each file.
# Match href values only, with single or double quotes.
PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Absolute production URLs
    (re.compile(r'(href=["\'])https://www\.markratcliffemoving\.co\.uk/index\.html'), r'\1https://www.markratcliffemoving.co.uk/'),
    (re.compile(r'(href=["\'])https://www\.markratcliffemoving\.co\.uk/blog/index\.html'), r'\1https://www.markratcliffemoving.co.uk/blog/'),
    (re.compile(r'(href=["\'])https://www\.markratcliffemoving\.co\.uk/areas-covered/index\.html'), r'\1https://www.markratcliffemoving.co.uk/areas-covered/'),
    # Root-relative
    (re.compile(r'(href=["\'])/index\.html(["\'])'), r'\1/\2'),
    (re.compile(r'(href=["\'])/blog/index\.html(["\'])'), r'\1/blog/\2'),
    (re.compile(r'(href=["\'])/areas-covered/index\.html(["\'])'), r'\1/areas-covered/\2'),
    # Relative — parent
    (re.compile(r'(href=["\'])\.\./index\.html(["\'])'),       r'\1../\2'),
    (re.compile(r'(href=["\'])\.\./blog/index\.html(["\'])'),  r'\1../blog/\2'),
    (re.compile(r'(href=["\'])\.\./areas-covered/index\.html(["\'])'), r'\1../areas-covered/\2'),
    # Relative — same dir
    (re.compile(r'(href=["\'])\./index\.html(["\'])'),         r'\1./\2'),
    (re.compile(r'(href=["\'])index\.html(["\'])'),            r'\1./\2'),
    (re.compile(r'(href=["\'])blog/index\.html(["\'])'),       r'\1blog/\2'),
    (re.compile(r'(href=["\'])areas-covered/index\.html(["\'])'), r'\1areas-covered/\2'),
]


def fix(path: str) -> int:
    html = open(path, encoding='utf-8').read()
    new = html
    for pat, repl in PATTERNS:
        new = pat.sub(repl, new)
    if new == html:
        return 0
    open(path, 'w', encoding='utf-8').write(new)
    # Count actual replacements by re-running the patterns against original
    n = 0
    for pat, _ in PATTERNS:
        n += len(pat.findall(html))
    return n


def main() -> int:
    paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
    )
    total_files = 0
    total_links = 0
    for p in paths:
        n = fix(p)
        if n:
            total_files += 1
            total_links += n
            print(f'{p:60s} → {n} link(s) rewritten')
    print()
    print(f'Rewrote {total_links} link(s) across {total_files} file(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
