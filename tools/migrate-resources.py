#!/usr/bin/env python3
"""
Move the 8 pages that live under the Resources nav into /resources/.

  pricing.html                                  → /resources/pricing.html
  moving-checklist-eastbourne.html              → /resources/moving-checklist-eastbourne.html
  removals-eastbourne-cost.html                 → /resources/removals-eastbourne-cost.html
  helpful-tips.html                             → /resources/helpful-tips.html
  gallery.html                                  → /resources/gallery.html
  faqs.html                                     → /resources/faqs.html
  blog.html                                     → /resources/blog.html
  services/buy-packing-materials-eastbourne.html → /resources/buy-packing-materials-eastbourne.html

Also creates /resources/index.html (hub page that lists every resource)
to keep the URL structure consistent with /services/ and /areas-covered/.

Reuses the move + link-rewrite logic from tools/migrate-to-subdirs.py.
No redirects (per user policy); old URLs cease to exist.
"""

from __future__ import annotations
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE_URL = 'https://www.markratcliffemoving.co.uk'

MOVES: dict[str, str] = {
    'pricing.html':                                  'resources/pricing.html',
    'moving-checklist-eastbourne.html':              'resources/moving-checklist-eastbourne.html',
    'removals-eastbourne-cost.html':                 'resources/removals-eastbourne-cost.html',
    'helpful-tips.html':                             'resources/helpful-tips.html',
    'gallery.html':                                  'resources/gallery.html',
    'faqs.html':                                     'resources/faqs.html',
    'blog.html':                                     'resources/blog.html',
    'services/buy-packing-materials-eastbourne.html': 'resources/buy-packing-materials-eastbourne.html',
}


# --- href resolver / rewriter (copy of the proven logic from migrate-to-subdirs) ---
PROD_HOST_RE = re.compile(r'^https?://(?:www\.)?markratcliffemoving\.co\.uk', re.I)


def is_external(href: str) -> bool:
    if href.startswith(('mailto:', 'tel:', 'javascript:', 'data:')): return True
    if href.startswith(('http://', 'https://', '//')):
        return not PROD_HOST_RE.match(href)
    return False


def href_to_repo_path(href: str, file_dir: str):
    if not href or href.startswith('#'): return None
    if is_external(href): return None
    main = re.split(r'[?#]', href, maxsplit=1)[0]
    suffix = href[len(main):]
    if PROD_HOST_RE.match(href):
        path = PROD_HOST_RE.sub('', main).lstrip('/')
        return ('abs', path, suffix)
    if main.startswith('/'):
        return ('rel', main.lstrip('/'), suffix)
    if not main: return None
    joined = os.path.normpath(os.path.join(file_dir or '.', main)).replace(os.sep, '/')
    if joined == '.': joined = ''
    return ('rel', joined, suffix)


def apply_move(repo_path: str) -> str:
    return MOVES.get(repo_path, repo_path)


def render_href(repo_path: str, suffix: str, from_dir: str, is_abs: bool) -> str:
    if repo_path == '':
        if is_abs: return f'{BASE_URL}/{suffix}' if suffix else f'{BASE_URL}/'
        if from_dir in ('', '.'): return './' + suffix
        rel = os.path.relpath('.', from_dir).replace(os.sep, '/')
        return rel + '/' + suffix
    if repo_path.endswith('/index.html'):
        dir_path = repo_path[:-len('index.html')]
        if is_abs: return f'{BASE_URL}/{dir_path}{suffix}'
        rel = os.path.relpath(dir_path, from_dir or '.').replace(os.sep, '/')
        if not rel.endswith('/'): rel += '/'
        if rel == './': return './' + suffix
        return rel + suffix
    if repo_path == 'index.html':
        if is_abs: return f'{BASE_URL}/{suffix}' if suffix else f'{BASE_URL}/'
        if from_dir in ('', '.'): return './' + suffix
        rel = os.path.relpath('.', from_dir).replace(os.sep, '/')
        return rel + '/' + suffix
    if is_abs: return f'{BASE_URL}/{repo_path}{suffix}'
    rel = os.path.relpath(repo_path, from_dir or '.').replace(os.sep, '/')
    return rel + suffix


ATTR_RE = re.compile(r'(\b(?:href|src|data-src|action)=)"([^"]+)"', re.I)
ABS_HTML_URL_RE = re.compile(
    r'(https?://(?:www\.)?markratcliffemoving\.co\.uk)/([a-zA-Z0-9_\-./]+\.html)'
)


def rewrite_attrs(html: str, old_dir: str, new_dir: str) -> str:
    def sub(m):
        prefix, href = m.group(1), m.group(2)
        resolved = href_to_repo_path(href, old_dir)
        if resolved is None: return m.group(0)
        kind, repo_path, suffix = resolved
        new_repo_path = apply_move(repo_path)
        new_href = render_href(new_repo_path, suffix, new_dir, is_abs=(kind == 'abs'))
        return f'{prefix}"{new_href}"'
    return ATTR_RE.sub(sub, html)


def rewrite_abs_urls(html: str) -> str:
    def sub(m):
        host, path = m.group(1), m.group(2)
        new_path = apply_move(path)
        if new_path.endswith('/index.html'):
            new_path = new_path[:-len('index.html')]
        if new_path == 'index.html': new_path = ''
        return f'{host}/{new_path}'
    return ABS_HTML_URL_RE.sub(sub, html)


CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
OGURL_RE = re.compile(r'<meta\s+property="og:url"\s+content="([^"]+)"', re.I)


def canonical_for(new_path: str) -> str:
    if new_path == 'index.html': return f'{BASE_URL}/'
    if new_path.endswith('/index.html'): return f'{BASE_URL}/{new_path[:-len("index.html")]}'
    return f'{BASE_URL}/{new_path}'


# --- /resources/index.html hub content ---
RESOURCES_INDEX = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>Resources Hub – Removals Pricing, Tips, FAQs & Cost Guides</title>
  <meta name="description" content="The Mark Ratcliffe Moving resources hub — pricing, checklists, cost guides, helpful tips, FAQs, gallery, packing materials and our removals blog.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="Mark Ratcliffe Moving & Storage">
  <meta name="theme-color" content="#4d2e8f">
  <meta property="og:title" content="Resources Hub – Removals Pricing, Tips, FAQs & Cost Guides">
  <meta property="og:description" content="The Mark Ratcliffe Moving resources hub — pricing, checklists, cost guides, helpful tips, FAQs, gallery, packing materials and our removals blog.">
  <meta property="og:image" content="https://www.markratcliffemoving.co.uk/images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving & Storage">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://cdn.yoshki.com" crossorigin>
  <link href="../css/normalize.css?v=20260560" rel="stylesheet">
  <link href="../css/components.css?v=20260560" rel="stylesheet">
  <link href="../css/mark-ratcliffe-moving.css?v=20260560" rel="stylesheet">
  <link href="../css/new-pages.css?v=20260560" rel="stylesheet">
  <link rel="preconnect" href="https://ajax.googleapis.com" crossorigin>
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <script async src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>WebFont.load({classes:true,timeout:2000,google:{families:["Inter:400,500,600,700,800","Fraunces:400,500,600,700"]}});;</script>
  <link href="../images/favicon.png" rel="shortcut icon">
  <link href="../images/webclip.png" rel="apple-touch-icon">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q111LKQEBP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-Q111LKQEBP');</script>
  <script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.markratcliffemoving.co.uk/"}, {"@type": "ListItem", "position": 2, "name": "Resources", "item": "https://www.markratcliffemoving.co.uk/resources/"}]}</script>
  <script type="application/ld+json">{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Resources Hub", "description": "Pricing, checklists, tips, FAQs, gallery and the blog from Mark Ratcliffe Moving.", "url": "https://www.markratcliffemoving.co.uk/resources/", "publisher": {"@type": "Organization", "@id": "https://www.markratcliffemoving.co.uk/#organization"}}</script>
  <link rel="canonical" href="https://www.markratcliffemoving.co.uk/resources/">
  <meta property="og:url" content="https://www.markratcliffemoving.co.uk/resources/">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' https:; script-src 'self' 'unsafe-inline' https://ajax.googleapis.com https://www.googletagmanager.com https://www.google-analytics.com https://cdn.yoshki.com https://d3e54v103j8qbb.cloudfront.net https://www.cognitoforms.com https://services.cognitoforms.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://ajax.googleapis.com https://www.cognitoforms.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com data:; frame-src https://www.google.com https://www.cognitoforms.com https://services.cognitoforms.com; connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://stats.g.doubleclick.net https://www.cognitoforms.com https://services.cognitoforms.com; object-src 'none'; base-uri 'self'; form-action 'self' https://www.cognitoforms.com https://services.cognitoforms.com">
  <meta name="referrer" content="strict-origin-when-cross-origin">
</head>
<body>
__NAVBAR__
  <header class="np-hero">
    <div class="np-hero-inner">
      <div class="np-kicker">Moving resources · Guides · Tools</div>
      <h1>Resources Hub for Sussex House Movers</h1>
      <p class="np-hero-sub">Every guide, tool and reference page in one place. Pricing transparency, the 8-week checklist, cost breakdowns, packing tips, FAQs, gallery, materials shop and the full blog.</p>
      <div class="np-hero-cta">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
    <img src="../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp" class="np-hero-bg" alt="" role="presentation" aria-hidden="true" decoding="async" fetchpriority="high" width="1800" height="1350">
  </header>

  <section class="np-section">
    <div class="np-inner">
      <p style="font-size:1.15rem;">This resources hub gathers every guide, checklist and reference page we publish for Sussex house movers in one place. Use the pricing guide to understand how removals quotes are built; the 8-week checklist to pace your preparation; the cost guide for honest Eastbourne removals price ranges; the helpful tips collection for things our crews wish customers knew; and the FAQs for the questions we get asked every week.</p>
      <p>If you need packing materials, our packaging shop ships boxes, tape, bubble wrap and blankets locally. The gallery shows recent moves so you can see what a Mark Ratcliffe crew actually looks like on the day, and the blog goes deeper on everything from antique furniture moving to school-holiday relocations.</p>
    </div>
  </section>

  <section class="np-section np-section-soft">
    <div class="np-inner">
      <h2>All resources</h2>
      <ul class="np-related-list">
        <li><a href="pricing.html">Removals Pricing</a></li>
        <li><a href="moving-checklist-eastbourne.html">8-Week Moving Checklist</a></li>
        <li><a href="removals-eastbourne-cost.html">Cost Guide</a></li>
        <li><a href="helpful-tips.html">Helpful Moving Tips</a></li>
        <li><a href="buy-packing-materials-eastbourne.html">Buy Packing Materials</a></li>
        <li><a href="gallery.html">Recent Moves Gallery</a></li>
        <li><a href="faqs.html">Frequently Asked Questions</a></li>
        <li><a href="blog.html">Removals Blog &amp; Articles</a></li>
        <li><a href="../blog/">Browse all blog posts</a></li>
        <li><a href="../about-us.html">About Mark Ratcliffe Moving</a></li>
        <li><a href="../reviews.html">Customer reviews</a></li>
        <li><a href="../services/">All services</a></li>
        <li><a href="../areas-covered/">Areas covered</a></li>
      </ul>
    </div>
  </section>

  <section class="np-section np-cta-block">
    <div class="np-inner">
      <h2>Ready to plan your move?</h2>
      <p>Once you have used the resources above, the next step is a free, no-obligation quote. We respond within 48 hours.</p>
      <div class="np-cta-row">
        <a href="../mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
  </section>
__FOOTER__
</body>
</html>
'''


# --- Execution ---
def main() -> int:
    missing = [s for s in MOVES if not os.path.isfile(s)]
    if missing:
        print('ERROR — missing source files:', missing, file=sys.stderr)
        return 1

    all_old = sorted(
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
    )

    # Pull navbar + footer fragments from an existing page so the hub
    # matches the rest of the site.
    sample = open('about-us.html', encoding='utf-8').read()
    nav_m = re.search(r'(  <div class="nav-section">.*?  </div>\s*</div>)', sample, re.S)
    footer_m = re.search(r'(  <footer.*?</footer>)', sample, re.S)
    navbar = nav_m.group(1) if nav_m else ''
    footer = footer_m.group(1) if footer_m else ''

    n_moved = 0
    n_rewritten = 0
    for old_path in all_old:
        new_path = MOVES.get(old_path, old_path)
        old_dir = os.path.dirname(old_path)
        new_dir = os.path.dirname(new_path)

        html = open(old_path, encoding='utf-8').read()
        original = html
        html = rewrite_attrs(html, old_dir, new_dir)
        html = rewrite_abs_urls(html)

        if old_path != new_path:
            new_canon = canonical_for(new_path)
            html = CANON_RE.sub(lambda mm: f'<link rel="canonical" href="{new_canon}"', html, count=1)
            html = OGURL_RE.sub(lambda mm: f'<meta property="og:url" content="{new_canon}"', html, count=1)

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

    # Create /resources/index.html (after the navbar is migrated)
    # The navbar fragment needs its hrefs translated as if it were at
    # depth 1 (since /resources/index.html is one level deep).
    nav_resourced = rewrite_attrs(navbar, '', 'resources')
    nav_resourced = rewrite_abs_urls(nav_resourced)
    footer_resourced = rewrite_attrs(footer, '', 'resources')
    footer_resourced = rewrite_abs_urls(footer_resourced)
    hub = RESOURCES_INDEX.replace('__NAVBAR__', nav_resourced).replace('__FOOTER__', footer_resourced)
    open('resources/index.html', 'w', encoding='utf-8').write(hub)
    print('  create   resources/index.html (resources hub)')

    print()
    print(f'Moved {n_moved} files. Rewrote {n_rewritten} in-place.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
