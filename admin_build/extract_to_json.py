#!/usr/bin/env python3
"""Extract content from every HTML page into editable JSON files.

For each page we capture:
- meta_title, meta_description, canonical_url
- h1
- intro_paragraph (lead text)
- hero_image (path to image)
- sections: list of {heading, body_html, kind} where kind in ('text', 'list', 'faq', 'grid', 'cards')
- alt_texts: {image_filename: alt_text}
- raw_body (fallback: cleaned full body for pages we couldn't fully parse)

Each page or blog post gets its own data/pages/{slug}.json or data/blog/{slug}.json.
"""
import re, json, html
from pathlib import Path

ROOT = Path(__file__).parent.parent / "www.markratcliffemoving.co.uk"
DATA = Path(__file__).parent.parent / "www.markratcliffemoving.co.uk" / "data"
PAGES_DIR = DATA / "pages"
BLOG_DIR = DATA / "blog"

PAGES_DIR.mkdir(parents=True, exist_ok=True)
BLOG_DIR.mkdir(parents=True, exist_ok=True)


def get_meta(content: str, name: str = None, prop: str = None) -> str:
    if name:
        m = re.search(rf'<meta\s+content="([^"]*)"\s+name="{name}"', content)
        if m: return html.unescape(m.group(1))
        m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', content)
        if m: return html.unescape(m.group(1))
    if prop:
        m = re.search(rf'<meta\s+property="{prop}"\s+content="([^"]*)"', content)
        if m: return html.unescape(m.group(1))
        m = re.search(rf'<meta\s+content="([^"]*)"\s+property="{prop}"', content)
        if m: return html.unescape(m.group(1))
    return ""


def get_title(content: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", content)
    return html.unescape(m.group(1).strip()) if m else ""


def get_canonical(content: str) -> str:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    return m.group(1) if m else ""


def get_h1(content: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S)
    if m:
        return clean_text(m.group(1))
    return ""


def clean_text(s: str) -> str:
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


# Strip nav, footer, scripts, styles, head — everything except body content
def isolate_body(content: str) -> str:
    body = re.search(r'<body[^>]*>(.*?)</body>', content, re.S)
    if not body:
        return content
    text = body.group(1)
    # Strip nav-section, mobile-contct, navbar
    text = re.sub(r'<div class="nav-section">.*?</div>\s*</div>\s*</div>', '', text, flags=re.S, count=1)
    text = re.sub(r'<div class="mobile-contct">.*?</div>\s*', '', text, flags=re.S, count=1)
    # Strip Webflow original footer and new footer
    text = re.sub(r'<footer class="np-footer">.*?</footer>', '', text, flags=re.S)
    text = re.sub(r'<div class="footer">.*?(?=<script|\Z)', '', text, flags=re.S)
    # Strip standalone map wrappers, online-quote-section, scripts
    text = re.sub(r'<div class="footer-map-wrapper">.*?</div>\s*</div>\s*', '', text, flags=re.S)
    text = re.sub(r'<div class="maps-wrapper">.*?</div>\s*</div>\s*', '', text, flags=re.S)
    text = re.sub(r'<div class="online-quote-section">.*?</div>\s*</div>\s*</div>\s*', '', text, flags=re.S)
    text = re.sub(r'<script\b[^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'<style\b[^>]*>.*?</style>', '', text, flags=re.S)
    # Strip np-cta-block (auto-injected, can be regenerated)
    text = re.sub(r'<section class="np-section np-cta-block">.*?</section>', '', text, flags=re.S)
    return text.strip()


def extract_sections(body: str) -> list:
    """Find <section> blocks with H2 headings; return as list of dicts."""
    sections = []
    section_pattern = re.compile(
        r'<section[^>]*class="np-section[^"]*"[^>]*>\s*<div class="np-inner">(.*?)</div>\s*</section>',
        re.S
    )
    for m in section_pattern.finditer(body):
        inner = m.group(1).strip()
        # Try to identify section type
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', inner, re.S)
        heading = clean_text(h2.group(1)) if h2 else ""
        # The rest is content
        body_html = inner
        kind = "text"
        if "<details" in inner: kind = "faq"
        elif 'class="np-grid' in inner: kind = "grid"
        elif 'class="np-blog' in inner: kind = "blog"
        sections.append({
            "heading": heading,
            "kind": kind,
            "body_html": body_html
        })
    return sections


def extract_intro(body: str) -> str:
    """Get the first prominent intro paragraph (font-size:1.15rem)."""
    m = re.search(r'<p style="font-size:1\.15rem[^"]*">(.*?)</p>', body, re.S)
    if m:
        return m.group(1).strip()
    # Fallback: first <p>
    m = re.search(r'<p[^>]*>(.*?)</p>', body, re.S)
    if m:
        return m.group(1).strip()
    return ""


def extract_hero_image(body: str) -> dict:
    """Pull the hero image src and kicker."""
    m = re.search(r'<header class="np-hero">.*?<img\s+src="([^"]+)"', body, re.S)
    src = m.group(1) if m else ""
    kicker_m = re.search(r'<div class="np-kicker">([^<]*)</div>', body)
    kicker = clean_text(kicker_m.group(1)) if kicker_m else ""
    return {"src": src, "kicker": kicker}


def extract_faqs(body: str) -> list:
    """Find FAQ details blocks."""
    faqs = []
    for m in re.finditer(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>', body, re.S):
        q = clean_text(m.group(1))
        a = clean_text(m.group(2))
        faqs.append({"q": q, "a": a})
    return faqs


def extract_images(body: str) -> list:
    """List all <img> with alt text."""
    imgs = []
    seen = set()
    for m in re.finditer(r'<img\s+([^>]+)>', body):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        src = attrs.get('src', '')
        if not src or src in seen: continue
        seen.add(src)
        imgs.append({
            "src": src,
            "alt": attrs.get('alt', ''),
            "width": attrs.get('width', ''),
            "height": attrs.get('height', ''),
        })
    return imgs


def detect_page_type(filepath: Path) -> str:
    name = filepath.stem
    if filepath.parts[-2] == "blog":
        return "blog" if name != "index" else "blog-hub"
    if name == "index":
        return "home"
    return "page"


def extract_page(fp: Path) -> dict:
    content = fp.read_text(encoding="utf-8")
    body = isolate_body(content)
    rel = fp.relative_to(ROOT).as_posix()
    slug = fp.stem if fp.parent == ROOT else f"{fp.parent.name}/{fp.stem}"
    data = {
        "slug": slug,
        "filename": rel,
        "type": detect_page_type(fp),
        "meta_title": get_title(content),
        "meta_description": get_meta(content, name="description"),
        "canonical_url": get_canonical(content),
        "og_image": get_meta(content, prop="og:image"),
        "h1": get_h1(body or content),
        "intro_paragraph": extract_intro(body),
        "hero": extract_hero_image(body),
        "sections": extract_sections(body),
        "faqs": extract_faqs(body),
        "images": extract_images(body),
        "raw_body": body,  # kept as fallback for full editor mode
    }
    return data


def main():
    # Identify the meta-refresh redirect stubs to skip
    pages_processed = []
    blog_processed = []
    for fp in list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html")):
        content = fp.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in content and len(content) < 2000:
            continue
        data = extract_page(fp)
        out = PAGES_DIR / f"{data['slug'].replace('/', '__')}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        pages_processed.append(data['slug'])

    for fp in (ROOT / "blog").glob("*.html") if (ROOT / "blog").exists() else []:
        data = extract_page(fp)
        # Save under blog/
        out = BLOG_DIR / f"{fp.stem}.json"
        data['type'] = 'blog-hub' if fp.stem == 'index' else 'blog'
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        blog_processed.append(fp.stem)

    print(f"Extracted {len(pages_processed)} pages to data/pages/")
    print(f"Extracted {len(blog_processed)} blog files to data/blog/")


if __name__ == "__main__":
    main()
