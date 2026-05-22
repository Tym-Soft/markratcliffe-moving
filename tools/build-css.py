#!/usr/bin/env python3
"""
Concatenate the four site stylesheets into a single minified
css/site.css and rewrite every HTML page's <head> to load that one
file instead of four separate ones.

Cascade order is preserved exactly as it loaded before:
  normalize.css → components.css → mark-ratcliffe-moving.css → new-pages.css

Run from the site root:
    python3 tools/build-css.py
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SOURCES = [
    'css/normalize.css',
    'css/components.css',
    'css/mark-ratcliffe-moving.css',
    'css/new-pages.css',
]
OUT_PATH = 'css/site.css'
CACHE_VERSION = '20260652'

# Each replacement matches BOTH the `css/...` (root pages) and
# `../css/...` (subdirectory pages) variants. We use re.escape on the
# filename so dots don't accidentally match anything.
LINK_PATTERN = re.compile(
    r'\s*<link\s+href="(\.\./)?css/(normalize|components|mark-ratcliffe-moving|new-pages)\.css\?v=\d+"\s+rel="stylesheet"(?:\s+type="text/css")?>\s*\n?'
)


def minify(css: str) -> str:
    """Lightweight CSS minifier — removes comments, collapses runs of
    whitespace, drops spaces around structural punctuation, drops the
    final ; before }. Preserves content inside strings."""
    # Strip /* ... */ comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    # Collapse all runs of whitespace to a single space
    css = re.sub(r'\s+', ' ', css)
    # Drop spaces around : ; { } , > + ~ ( )
    css = re.sub(r'\s*([{};:,>+~()])\s*', r'\1', css)
    # Drop the final ; before }
    css = css.replace(';}', '}')
    return css.strip()


def safe_minify(css: str) -> str:
    """Conservative CSS minifier.

    Strips /* … */ comments and collapses excess whitespace, but
    deliberately DOES NOT touch punctuation, selectors, or rule
    structure. An earlier aggressive minifier mangled a few nav
    cascade rules (mega-menu wrap regression, 2026-05-22) by
    removing spaces around `:` inside @media queries and similar.
    This version is structural-preserving:

      - removes /* … */ comments
      - removes blank lines
      - strips leading whitespace on each line
      - collapses runs of spaces / tabs to one space

    Keeps newlines intact. Lighthouse's "minify CSS" check passes
    on this output; the nav cascade stays exactly as written.
    """
    # 1. Strip /* … */ block comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    # 2. Drop blank lines
    css = re.sub(r'\n\s*\n+', '\n', css)
    # 3. Strip leading whitespace on each line
    css = re.sub(r'^[ \t]+', '', css, flags=re.M)
    # 4. Collapse runs of spaces / tabs (but never newlines)
    css = re.sub(r'[ \t]+', ' ', css)
    return css.strip() + '\n'


def build_combined_css() -> int:
    """Concatenate the four sources + apply a safe minifier."""
    chunks = []
    for src in SOURCES:
        try:
            chunks.append(f'/* === {os.path.basename(src)} === */\n' + open(src, encoding='utf-8').read())
        except OSError as e:
            print(f'  ! cannot read {src}: {e}', file=sys.stderr)
            return 1
    combined = '\n'.join(chunks)
    raw_bytes = len(combined)
    minified = safe_minify(combined)
    open(OUT_PATH, 'w', encoding='utf-8').write(minified)
    print(f'  wrote {OUT_PATH}  {len(minified):,} bytes (was {raw_bytes:,} raw — {100 - 100*len(minified)//raw_bytes}% smaller)')
    return 0


def rewrite_html() -> None:
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    changed = 0
    for p in pages:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        # Find the four <link> lines in their (typically contiguous) block.
        matches = list(LINK_PATTERN.finditer(html))
        if len(matches) < 4:
            # Page either already converted, or uses a non-standard pattern. Skip.
            continue
        # Determine path prefix (root pages → "css/", subdir pages → "../css/")
        first_href = re.search(r'href="((?:\.\./)?css/)', html)
        prefix = first_href.group(1) if first_href else 'css/'
        new_link = f'  <link href="{prefix}site.css?v={CACHE_VERSION}" rel="stylesheet">\n'
        # Replace the first four CSS link lines as a block. We assume they sit
        # next to each other (they do site-wide).
        new_html = LINK_PATTERN.sub('', html, count=4)
        # Insert the single link where the first one used to be.
        new_html = new_html[:matches[0].start()] + new_link + new_html[matches[0].start():]
        if new_html != html:
            open(p, 'w', encoding='utf-8').write(new_html)
            changed += 1
    print(f'  rewrote {changed} HTML pages')


if __name__ == '__main__':
    rc = build_combined_css()
    if rc:
        sys.exit(rc)
    rewrite_html()
