#!/usr/bin/env python3
"""
Extract above-the-fold critical CSS from css/site.css and inline it
into every page's <head>. The full site.css then loads asynchronously
via the standard preload/onload swap, so render isn't blocked by the
~38 KB stylesheet.

The extractor walks the CSS rule-by-rule (tracking brace depth) and
keeps rules whose selectors match the critical patterns below. For
@media wrappers, we recurse and keep only the inner rules that match.

Critical selector patterns aim to cover everything above the fold on
every page type (home, service, area, blog, calc, 404): nav bar,
top-bar contacts, mobile contact strip, hero blocks (np-hero, hp-hero,
lp-hero, ac-hero, th-hero), buttons, eyebrows, kickers, plus the base
reset (html/body/*) and Webflow's runtime classes (w-*).

If the extracted critical CSS misses something genuinely above-fold,
the visible symptom is "flash of unstyled content" until site.css
loads (~100-300ms later). Add the missing selector to CRITICAL_PATTERNS
below and re-run.
"""

from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CACHE_VERSION = "20260657"

# --- Critical selector patterns ---
# Each entry is a fragment that we look for INSIDE the selector text.
# Substring match is intentional — catches `.navbar`, `.navbar:hover`,
# `.navbar.w-nav`, `.navbar .nav-menu` etc.
CRITICAL_PATTERNS = [
    # Base reset & root tokens
    'html', 'body', '*::before', '*::after', ':root', '*,',
    # Top-level page chrome (the nav appears on every page above fold)
    '.nav-section', '.top-bar', '.tb-link', '.banner-script',
    '.contacts-in-top', '.navbar', '.brand', '.logo',
    '.nav-menu', '.navlink', '.menu-button',
    '.mobile-contct', '.mob-con-1', '.mob-menu-contact',
    '.dropdown', '.mega-', '.is-call', '.is-email', '.is-quote',
    # Webflow runtime classes (the nav uses these — keep them all)
    '.w-nav', '.w-dropdown', '.w-icon-nav-menu', '.w-inline-block',
    '.w-hidden-small', '.w-hidden-tiny', '.w-hidden-medium', '.w-hidden-main',
    '.w-mod-', '.w-button',
    # Hero blocks — every page type has one above the fold
    '.np-hero', '.np-kicker', '.np-btn', '.np-section-inner',
    '.hp-hero', '.hp-section-head', '.hp-eyebrow', '.hp-btn', '.hp-trust',
    '.hp-rating', '.hp-inner',
    '.lp-hero', '.lp-h1', '.lp-h3',
    '.ac-hero', '.ac-eyebrow', '.ac-stats', '.ac-sub',
    '.th-hero', '.th-eyebrow', '.th-stats',
    # Floating contact buttons (mobile)
    '.fab-', '.np-fab',
]

# Selectors we never want in critical CSS even if they happen to match.
EXCLUDE_PATTERNS = [
    '@keyframes', '@-webkit-keyframes', '@-moz-keyframes',
]

# Always include these at-rules verbatim if present.
ALWAYS_INCLUDE_AT = ['@font-face', '@charset']


def is_critical_selector(sel: str) -> bool:
    s = sel.strip()
    if not s:
        return False
    sl = s.lower()
    for ex in EXCLUDE_PATTERNS:
        if ex in sl:
            return False
    for p in CRITICAL_PATTERNS:
        if p.lower() in sl:
            return True
    return False


def split_top_level_rules(css: str) -> list[str]:
    """Return list of top-level CSS rules, each ending with its closing brace."""
    rules: list[str] = []
    depth = 0
    start = 0
    in_string = False
    string_ch = ''
    for i, ch in enumerate(css):
        if in_string:
            if ch == string_ch and css[i-1] != '\\':
                in_string = False
            continue
        if ch in ('"', "'"):
            in_string = True
            string_ch = ch
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                rules.append(css[start:i+1])
                start = i + 1
    # Trailing whitespace / charset rules without braces
    tail = css[start:].strip()
    if tail:
        rules.append(tail)
    return rules


def selector_of(rule: str) -> str:
    """Return text before the first '{' of a rule."""
    idx = rule.find('{')
    if idx == -1:
        return rule.strip()
    return rule[:idx].strip()


def body_of(rule: str) -> str:
    idx = rule.find('{')
    if idx == -1:
        return ''
    # Strip outer braces
    return rule[idx + 1:].rstrip().rstrip('}').strip()


def extract_critical(css: str) -> str:
    out: list[str] = []
    for rule in split_top_level_rules(css):
        sel = selector_of(rule)
        sel_lower = sel.lower()

        # Always-include at-rules
        if any(sel_lower.startswith(a) for a in ALWAYS_INCLUDE_AT):
            out.append(rule)
            continue

        # @media wrapper — recurse, keep critical inner rules
        if sel_lower.startswith('@media') or sel_lower.startswith('@supports'):
            inner = body_of(rule)
            kept_inner = extract_critical(inner)
            if kept_inner:
                out.append(f'{sel}{{{kept_inner}}}')
            continue

        # Regular rule — check its selector
        if is_critical_selector(sel):
            out.append(rule)

    return ''.join(out)


def main() -> int:
    src_path = 'css/site.css'
    try:
        css = open(src_path, encoding='utf-8').read()
    except OSError as e:
        print(f'  ! cannot read {src_path}: {e}', file=sys.stderr)
        return 1

    critical = extract_critical(css)
    open('css/critical.css', 'w', encoding='utf-8').write(critical)
    print(f'  critical.css: {len(critical):,} bytes from {len(css):,} bytes full css')

    # Inline-inject critical CSS into every page's <head>, replacing the
    # existing inline critical block if there is one, and rewrite the
    # existing <link rel="stylesheet"> to the deferred preload variant.
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
        + glob.glob('blog/*.html')
    )

    SENTINEL_START = '<!-- mrm:critical-css:start -->'
    SENTINEL_END = '<!-- mrm:critical-css:end -->'
    sentinel_re = re.compile(re.escape(SENTINEL_START) + r'.*?' + re.escape(SENTINEL_END), re.S)
    inline_block = (
        f'{SENTINEL_START}\n'
        f'<style>{critical}</style>\n'
        f'{SENTINEL_END}'
    )

    # Match either the synchronous <link> form OR the already-deferred
    # preload form (we update both — the preload variant just needs its
    # ?v= cache key refreshed if site.css changed).
    sync_link_re = re.compile(
        r'<link\s+href="((?:\.\./)?css/site\.css)\?v=\d+"\s+rel="stylesheet">',
        re.I,
    )
    deferred_link_re = re.compile(
        r'<link rel="preload" as="style" href="((?:\.\./)?css/site\.css)\?v=\d+"[^>]*>'
        r'<noscript><link rel="stylesheet" href="(?:\.\./)?css/site\.css\?v=\d+"></noscript>',
        re.I,
    )

    def deferred_link(prefix: str) -> str:
        href = f'{prefix}?v={CACHE_VERSION}'
        return (
            f'<link rel="preload" as="style" href="{href}" '
            f"onload=\"this.onload=null;this.rel='stylesheet'\">"
            f'<noscript><link rel="stylesheet" href="{href}"></noscript>'
        )

    changed = 0
    for path in pages:
        try:
            html = open(path, encoding='utf-8').read()
        except OSError:
            continue
        original = html

        # Strip any prior critical block (we re-inject the freshly-
        # extracted version below).
        html = sentinel_re.sub('', html)

        # Update / replace the CSS link (sync or deferred). Either way
        # the result is the deferred preload form at the new ?v= key.
        def _link_repl(m):
            return deferred_link(m.group(1))
        new_html, n = sync_link_re.subn(_link_repl, html, count=1)
        if not n:
            new_html, n = deferred_link_re.subn(_link_repl, html, count=1)
        if not n:
            continue  # this page doesn't reference site.css
        html = new_html

        # Inject the inline critical block right before </head>
        head_close = re.search(r'</head>', html, re.I)
        if not head_close:
            continue
        html = html[:head_close.start()] + inline_block + '\n' + html[head_close.start():]

        if html != original:
            open(path, 'w', encoding='utf-8').write(html)
            changed += 1

    print(f'  rewrote {changed} pages with inline critical CSS + deferred site.css')
    return 0


if __name__ == '__main__':
    sys.exit(main())
