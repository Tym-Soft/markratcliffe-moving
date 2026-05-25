#!/usr/bin/env python3
"""Sitewide link integrity audit — every HTML file, not just indexable pages.

Enforces user rules:
  - No 301 redirects on internal links (trailing slash on dirs, none on .html,
    no index.html in href, no http://, www-canonical).
  - No broken internal links: every <a href>, <script src>, <link href>,
    <img src>, <source srcset> resolves to a real file on disk.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
PROD_HOST = "www.markratcliffemoving.co.uk"

# Skip checking against external/data:/mailto:/tel:/javascript:/anchor-only
EXTERNAL_RE = re.compile(r"^(https?:|//|mailto:|tel:|javascript:|data:|#)", re.I)

# Matches absolute prod URLs we should treat as internal
PROD_URL_RE = re.compile(rf"^https?://(?:www\.)?{re.escape(PROD_HOST.replace('www.', ''))}", re.I)

# Self-host static asset roots that should resolve on disk
ASSET_ATTRS = {
    "a": "href",
    "link": "href",
    "script": "src",
    "img": "src",
    "source": "src",
    "iframe": "src",
    "video": "src",
    "audio": "src",
    "form": "action",
}

# Regex tag-attr finders (cheap, faster than a full HTML parser for this scope)
ATTR_RE = {
    tag: re.compile(rf"<{tag}\b[^>]*?\b{attr}\s*=\s*[\"']([^\"']+)[\"']", re.I)
    for tag, attr in ASSET_ATTRS.items()
}
# srcset is multi-URL — handle separately
SRCSET_RE = re.compile(r"<(?:source|img)\b[^>]*?\bsrcset\s*=\s*[\"']([^\"']+)[\"']", re.I)


def url_to_path(url: str, current_file: Path) -> tuple[Path | None, str]:
    """Resolve an internal URL to a filesystem path. Returns (path, normalised_href)."""
    raw = url.strip()
    if EXTERNAL_RE.match(raw):
        # mailto:/tel:/etc. — but if it's a prod URL, normalise to root-relative
        if PROD_URL_RE.match(raw):
            parsed = urlparse(raw)
            raw = parsed.path or "/"
            if parsed.query:
                raw += "?" + parsed.query
            if parsed.fragment:
                raw += "#" + parsed.fragment
        else:
            return None, raw  # external/non-http — not our problem

    # Drop query+fragment for file resolution
    href = raw.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None, raw  # pure fragment

    href = unquote(href)
    if href.startswith("/"):
        target = ROOT / href.lstrip("/")
    else:
        target = (current_file.parent / href).resolve()

    if target.is_dir() or href.endswith("/"):
        target = target / "index.html"

    return target, raw


def scan_file(path: Path):
    """Yield (kind, href, reason) for every issue in this file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        yield ("read-error", "", str(e))
        return

    for tag, regex in ATTR_RE.items():
        for m in regex.finditer(text):
            href = m.group(1)
            target, normalised = url_to_path(href, path)
            if target is None:
                continue  # external

            # Check broken
            if not target.exists():
                yield ("broken-link", href, f"<{tag}> target {target.relative_to(ROOT)} does not exist")
                continue

            # Check 301-trigger patterns on <a> and <form> hrefs only
            if tag in ("a", "form"):
                # strip query/fragment for pattern checks
                clean = href.split("#", 1)[0].split("?", 1)[0]
                if "index.html" in clean:
                    yield ("301-trigger", href, "href contains 'index.html' (CF would strip)")
                if clean.endswith(".html/"):
                    yield ("301-trigger", href, "trailing slash after .html (CF would strip)")
                # Directory link missing trailing slash → 301 to add one
                if clean and not clean.endswith("/") and not clean.endswith(".html") \
                        and not clean.startswith("mailto:") and not clean.startswith("tel:") \
                        and "." not in clean.rsplit("/", 1)[-1]:
                    # target resolved to a dir's index.html — means original href had no trailing slash
                    if target.name == "index.html" and target.parent.is_dir():
                        # Only flag if the href itself doesn't have the slash
                        href_no_qf = href.split("#", 1)[0].split("?", 1)[0]
                        if not href_no_qf.endswith("/"):
                            yield ("301-trigger", href, "directory href missing trailing slash (CF would 301)")
                # http:// internal links
                if href.lower().startswith("http://"):
                    yield ("301-trigger", href, "http:// link (CF would 301 to https)")
                # non-www absolute internal links
                m_abs = re.match(r"^https?://([^/]+)", href, re.I)
                if m_abs and m_abs.group(1).lower() == PROD_HOST.replace("www.", ""):
                    yield ("301-trigger", href, "non-www absolute link (CF would 301 to www)")

    # srcset URLs
    for m in SRCSET_RE.finditer(text):
        for entry in m.group(1).split(","):
            url = entry.strip().split()[0]
            if not url:
                continue
            target, _ = url_to_path(url, path)
            if target is None:
                continue
            if not target.exists():
                yield ("broken-link", url, f"<source/img srcset> target {target.relative_to(ROOT)} does not exist")


def main():
    html_files = sorted(ROOT.rglob("*.html"))
    # Skip data/ exports and any node_modules-style dirs (none expected, but be safe)
    html_files = [p for p in html_files if "/data/" not in str(p) and "/node_modules/" not in str(p)]

    total_broken = 0
    total_301 = 0
    files_with_issues = 0

    for f in html_files:
        issues = list(scan_file(f))
        if not issues:
            continue
        files_with_issues += 1
        rel = f.relative_to(ROOT)
        print(f"\n— {rel}")
        for kind, href, reason in issues:
            print(f"   [{kind}] {href}  ←  {reason}")
            if kind == "broken-link":
                total_broken += 1
            elif kind == "301-trigger":
                total_301 += 1

    print("\n" + "=" * 64)
    print(f"Scanned {len(html_files)} HTML files")
    print(f"  Files with issues: {files_with_issues}")
    print(f"  Broken links:      {total_broken}")
    print(f"  301-trigger links: {total_301}")
    print("=" * 64)
    sys.exit(1 if (total_broken + total_301) else 0)


if __name__ == "__main__":
    main()
