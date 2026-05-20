#!/usr/bin/env python3
"""
URL restructure migration.

Moves service pages → /services/, location pages → /areas-covered/.
Updates every internal link, canonical, og:url, JSON-LD URL across the
whole site so no redirect is needed. Deletes 8 noindex stub files
(user explicitly chose no redirects).

After running this script, the old URLs no longer exist. The
`_redirects` and `_headers` files plus the meta-refresh stubs are NOT
recreated for the moved pages — the user wants the new URLs to be
THE URLs everywhere, internal links updated directly, no 302s, no
404s on any internal link.
"""

from __future__ import annotations
import os, re, sys, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'

# ----------------------------------------------------------------------
# Move map (source path → destination path, both repo-relative)
# ----------------------------------------------------------------------

SERVICE_PAGES = [
    'antiques-moving.html',
    'buy-packing-materials-eastbourne.html',
    'custom-crate-service.html',
    'european-removals-eastbourne.html',
    'full-packing-service.html',
    'house-clearance-eastbourne.html',
    'international-removals-eastbourne.html',
    'man-and-van-eastbourne.html',
    'office-removals-eastbourne.html',
    'packaging-shop.html',
    'packing-services-eastbourne.html',
    'piano-moving.html',
    'storage-eastbourne.html',
    'student-removals.html',
    'thai-moving-services.html',
    'unpacking-service.html',
    'white-glove-service.html',
]

# Every removals-*.html at root (except the cost guide) plus hailsham-removals
LOCATION_PAGES = sorted(
    [f for f in os.listdir('.')
     if f.startswith('removals-') and f.endswith('.html')
     and f != 'removals-eastbourne-cost.html'
     and os.path.isfile(f)]
    + ['hailsham-removals.html']
)

MOVES: dict[str, str] = {}
for slug in SERVICE_PAGES:
    MOVES[slug] = f'services/{slug}'
for slug in LOCATION_PAGES:
    MOVES[slug] = f'areas-covered/{slug}'
MOVES['services.html']      = 'services/index.html'
MOVES['areas-covered.html'] = 'areas-covered/index.html'

DELETIONS = [
    'contact-us.html',
    'domestic-services.html',
    'man-van.html',
    'overseas-services.html',
    'secure-self-storage-rooms.html',
    'testimonials.html',
    'areas-covered/man-with-a-van-eastbourne.html',
    'areas-covered/removals-bexhill.html',  # stub at new location for moved file
]


# ----------------------------------------------------------------------
# Path / href resolution helpers
# ----------------------------------------------------------------------

PROD_HOST_RE = re.compile(r'^https?://(?:www\.)?markratcliffemoving\.co\.uk', re.I)


def is_external(href: str) -> bool:
    """Return True if href should not be rewritten (external URL or special protocol)."""
    if href.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
        return True
    if href.startswith(('http://', 'https://', '//')):
        return not PROD_HOST_RE.match(href)
    return False


def href_to_repo_path(href: str, file_dir: str) -> tuple[str, str, str] | None:
    """Parse href and return (kind, repo_path, suffix). kind is 'abs' or 'rel'.
    Returns None for external / special hrefs and pure fragments."""
    if not href or href.startswith('#'):
        return None
    if is_external(href):
        return None

    # Split off ?query and #fragment
    main = re.split(r'[?#]', href, maxsplit=1)[0]
    suffix = href[len(main):]

    # Absolute URL to our production domain
    if PROD_HOST_RE.match(href):
        path = PROD_HOST_RE.sub('', main).lstrip('/')
        return ('abs', path, suffix)

    # Root-relative
    if main.startswith('/'):
        return ('rel', main.lstrip('/'), suffix)

    # Empty after stripping fragment
    if not main:
        return None

    # Relative
    joined = os.path.normpath(os.path.join(file_dir or '.', main)).replace(os.sep, '/')
    if joined == '.':
        joined = ''
    return ('rel', joined, suffix)


def apply_move(repo_path: str) -> str:
    """If repo_path is moving, return its new path. Else return the same.
    Also normalises */index.html → */ for directory URLs."""
    # Treat root index.html, blog/index.html etc. as directory URLs going in.
    # But preserve them so the renderer can produce the right form.
    if repo_path in MOVES:
        return MOVES[repo_path]
    return repo_path


def render_href(repo_path: str, suffix: str, from_dir: str, original_was_absolute: bool) -> str:
    """Render an href value pointing at repo_path, relative to from_dir."""
    # Empty path = homepage directory URL
    if repo_path == '':
        if original_was_absolute:
            return f'{BASE_URL}/{suffix}' if suffix else f'{BASE_URL}/'
        if from_dir in ('', '.'):
            return './' + suffix
        rel = os.path.relpath('.', from_dir).replace(os.sep, '/')
        return rel + '/' + suffix

    # */index.html → */ (directory URL)
    if repo_path.endswith('/index.html'):
        dir_path = repo_path[:-len('index.html')]  # 'services/' etc.
        if original_was_absolute:
            return f'{BASE_URL}/{dir_path}{suffix}'
        rel = os.path.relpath(dir_path, from_dir or '.').replace(os.sep, '/')
        if not rel.endswith('/'):
            rel += '/'
        if rel == './':
            return './' + suffix
        return rel + suffix

    # bare index.html at root → '/'
    if repo_path == 'index.html':
        if original_was_absolute:
            return f'{BASE_URL}/{suffix}' if suffix else f'{BASE_URL}/'
        if from_dir in ('', '.'):
            return './' + suffix
        rel = os.path.relpath('.', from_dir).replace(os.sep, '/')
        return rel + '/' + suffix

    if original_was_absolute:
        return f'{BASE_URL}/{repo_path}{suffix}'

    rel = os.path.relpath(repo_path, from_dir or '.').replace(os.sep, '/')
    return rel + suffix


# ----------------------------------------------------------------------
# Rewriters
# ----------------------------------------------------------------------

ATTR_RE = re.compile(r'(\b(?:href|src|data-src|action)=)"([^"]+)"', re.I)

# Anywhere-in-content absolute URL to a production .html page
ABS_HTML_URL_RE = re.compile(
    r'(https?://(?:www\.)?markratcliffemoving\.co\.uk)/([a-zA-Z0-9_\-./]+\.html)'
)


def rewrite_attrs(html: str, old_dir: str, new_dir: str) -> str:
    """Rewrite href/src/data-src/action values, resolving them from old_dir
    and producing a new relative path from new_dir."""
    def sub(m: re.Match) -> str:
        prefix, href = m.group(1), m.group(2)
        resolved = href_to_repo_path(href, old_dir)
        if resolved is None:
            return m.group(0)
        kind, repo_path, suffix = resolved
        new_repo_path = apply_move(repo_path)
        new_href = render_href(new_repo_path, suffix, new_dir,
                               original_was_absolute=(kind == 'abs'))
        return f'{prefix}"{new_href}"'
    return ATTR_RE.sub(sub, html)


def rewrite_jsonld_and_meta(html: str) -> str:
    """Rewrite absolute production URLs to .html pages anywhere in the body
    (JSON-LD blocks, meta tags, plain text mentions)."""
    def sub(m: re.Match) -> str:
        host = m.group(1)
        path = m.group(2)
        new_path = apply_move(path)
        if new_path.endswith('/index.html'):
            new_path = new_path[:-len('index.html')]  # directory URL
        if new_path == 'index.html':
            new_path = ''
        return f'{host}/{new_path}'
    return ABS_HTML_URL_RE.sub(sub, html)


CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
OGURL_RE = re.compile(r'<meta\s+property="og:url"\s+content="([^"]+)"', re.I)


def canonical_for(new_path: str) -> str:
    """Production URL for a file at new_path (directory URL for index.html)."""
    if new_path == 'index.html':
        return f'{BASE_URL}/'
    if new_path.endswith('/index.html'):
        return f'{BASE_URL}/{new_path[:-len("index.html")]}'
    return f'{BASE_URL}/{new_path}'


# ----------------------------------------------------------------------
# Execution
# ----------------------------------------------------------------------

def main() -> int:
    # Sanity check — every source file in MOVES must exist
    missing = [src for src in MOVES if not os.path.isfile(src)]
    if missing:
        print('ERROR — missing source files:', missing, file=sys.stderr)
        return 1

    # 1. Delete noindex stubs first (so a moved file can take their slot)
    n_deleted = 0
    for d in DELETIONS:
        if os.path.isfile(d):
            os.unlink(d)
            n_deleted += 1
            print(f'  delete   {d}')

    # 2. Collect every HTML file BEFORE moves so we know what to read
    all_old_paths = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
    )

    n_moved = 0
    n_rewritten = 0
    for old_path in all_old_paths:
        new_path = MOVES.get(old_path, old_path)
        old_dir = os.path.dirname(old_path)
        new_dir = os.path.dirname(new_path)

        html = open(old_path, encoding='utf-8').read()
        original = html

        # Rewrite href / src / action attributes
        html = rewrite_attrs(html, old_dir, new_dir)
        # Rewrite absolute production URLs anywhere (JSON-LD, etc.)
        html = rewrite_jsonld_and_meta(html)

        # If moving, also bake in correct canonical and og:url
        if old_path != new_path:
            new_canon = canonical_for(new_path)
            html = CANON_RE.sub(
                lambda mm: f'<link rel="canonical" href="{new_canon}"', html, count=1)
            html = OGURL_RE.sub(
                lambda mm: f'<meta property="og:url" content="{new_canon}"', html, count=1)

        if old_path == new_path:
            if html != original:
                open(old_path, 'w', encoding='utf-8').write(html)
                n_rewritten += 1
        else:
            os.makedirs(new_dir, exist_ok=True)
            open(new_path, 'w', encoding='utf-8').write(html)
            os.unlink(old_path)
            n_moved += 1
            print(f'  move     {old_path:55s} → {new_path}')

    print()
    print(f'Moved {n_moved} files. Rewrote {n_rewritten} in-place. Deleted {n_deleted} stubs.')

    # 3. Clear _redirects (user wants no redirects on the site)
    with open('_redirects', 'w') as f:
        f.write(
            '# User explicitly chose no redirects after the 2026-05-20 URL\n'
            '# restructure. Old root-level service / location URLs no longer\n'
            '# exist; every internal link points at the new path directly.\n'
            '# This file is intentionally empty of redirect mappings.\n'
        )
    print('Cleared _redirects.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
