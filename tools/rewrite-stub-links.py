#!/usr/bin/env python3
"""
Rewrite internal links that still point at the 8 legacy redirect-stub
pages (noindex + canonical + 200ms refresh to a live page) so they
target the canonical destination directly.

The 8 stubs stay on disk — they're URL preservers for any old external
link still in the wild — but no internal link should surface them. SF
flags pages whose internal links land on canonicalised/noindex URLs.
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# stub path  →  canonical destination path (relative to repo root)
STUB_REDIRECTS = {
    'contact-us.html':                              'mark-ratcliffe-moving-online-removals-quote.html',
    'domestic-services.html':                       'removals-eastbourne.html',
    'man-van.html':                                 'man-and-van-eastbourne.html',
    'overseas-services.html':                       'international-removals-eastbourne.html',
    'secure-self-storage-rooms.html':               'storage-eastbourne.html',
    'testimonials.html':                            'reviews.html',
    'areas-covered/man-with-a-van-eastbourne.html': 'man-and-van-eastbourne.html',
    'areas-covered/removals-bexhill.html':          'removals-bexhill.html',
}

BASE = 'https://www.markratcliffemoving.co.uk'


def all_link_variants(stub: str) -> list[str]:
    """Every shape an internal href might take for `stub`."""
    out: list[str] = [
        stub,                                       # root-relative-ish bare
        './' + stub,                                # ./stub
        '../' + stub,                               # ../stub  (from subdir)
        '/' + stub,                                 # root-relative
        BASE + '/' + stub,                          # absolute production URL
    ]
    base = os.path.basename(stub)
    if '/' in stub:
        # also catch the bare basename form when used from inside the same subdir
        out.append(base)
        out.append('./' + base)
    return out


def replacement_href_for(stub: str, dest: str, file_path: str) -> str:
    """Pick a sensible relative href shape for `dest` when used from `file_path`."""
    in_subdir = '/' in file_path  # e.g. areas-covered/foo.html
    if '/' in dest:
        # destination is inside a subdir
        return ('../' if not in_subdir else '../') + dest if in_subdir else dest
    # destination at repo root
    return '../' + dest if in_subdir else dest


def fix(path: str) -> int:
    html = open(path, encoding='utf-8').read()
    original = html
    n = 0
    for stub, dest in STUB_REDIRECTS.items():
        new_href = replacement_href_for(stub, dest, path)
        for variant in all_link_variants(stub):
            # only replace href values, not arbitrary text
            pattern = re.compile(r'(href=)(["\'])' + re.escape(variant) + r'\2')
            new_html, k = pattern.subn(lambda m: f'{m.group(1)}{m.group(2)}{new_href}{m.group(2)}', html)
            if k:
                html = new_html
                n += k
    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
    return n


def main() -> int:
    paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
    )
    # Don't rewrite links INSIDE the stub files themselves (let them
    # continue to serve as redirects untouched).
    stub_files = set(STUB_REDIRECTS.keys())
    total = 0
    files = 0
    for p in paths:
        if p in stub_files:
            continue
        n = fix(p)
        if n:
            total += n
            files += 1
            print(f'{p:60s} → {n} stub link(s) rewritten')
    print()
    print(f'Rewrote {total} stub link(s) across {files} file(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
