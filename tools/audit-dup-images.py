#!/usr/bin/env python3
"""Find duplicate <img src=…> usages within each HTML page.

Reports any page where the same src appears more than once. Considers
<img src=…> and <source srcset=…> entries (the SEO-visible image
references). CSS `background-image: url(…)` is intentionally NOT
counted — those are decorative and not crawled for indexable images.
Excludes:
  - Pages with `?` query strings stripped before comparison (so
    cache-busted variants `foo.webp?v=1` and `foo.webp?v=2` count as
    duplicates of `foo.webp`).
  - The /admin-portal-xK7p9q/ dir (local-only, gitignored).
  - The /worker/ dir (server code, not HTML pages).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'admin-portal-xK7p9q', 'worker', '.git', 'node_modules', '.img-staging', 'tools'}

IMG_SRC_RE = re.compile(r'<img\b[^>]*?\bsrc\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE | re.DOTALL)
SRCSET_RE = re.compile(r'\bsrcset\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
BG_URL_RE = re.compile(r'background(?:-image)?\s*:\s*url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.IGNORECASE)


def normalise(src: str) -> str:
    src = src.strip()
    # Drop query string + fragment for comparison purposes.
    src = src.split('?', 1)[0].split('#', 1)[0]
    # Don't dedupe trivial inline data URIs against each other (rare, but possible).
    if src.startswith('data:'):
        return ''
    return src


def collect_srcs(html: str):
    found = []
    for m in IMG_SRC_RE.finditer(html):
        n = normalise(m.group(1))
        if n:
            found.append(n)
    for m in SRCSET_RE.finditer(html):
        # srcset: "url1 1x, url2 2x" → take each url
        for piece in m.group(1).split(','):
            piece = piece.strip().split()
            if piece:
                n = normalise(piece[0])
                if n:
                    found.append(n)
    # CSS background-image references are intentionally not counted —
    # they're decorative and not crawled as indexable images. Keeping
    # the regex around in case we want to surface them as warnings later.
    _ = BG_URL_RE
    return found


def main():
    fail = 0
    pages_with_dupes = []
    for path in sorted(ROOT.rglob('*.html')):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        try:
            html = path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"!! {path.relative_to(ROOT)} — read error: {e}", file=sys.stderr)
            continue

        srcs = collect_srcs(html)
        seen = {}
        for s in srcs:
            seen[s] = seen.get(s, 0) + 1
        dupes = {s: c for s, c in seen.items() if c > 1}
        if dupes:
            fail += 1
            pages_with_dupes.append((path.relative_to(ROOT), dupes))

    if not pages_with_dupes:
        print("OK — no duplicate <img src> within any single page.")
        return 0

    print(f"Found duplicate-image issues on {len(pages_with_dupes)} page(s):\n")
    for page, dupes in pages_with_dupes:
        print(f"  {page}")
        for src, count in sorted(dupes.items(), key=lambda x: -x[1]):
            print(f"      ×{count}  {src}")
        print()
    return 1


if __name__ == '__main__':
    sys.exit(main())
