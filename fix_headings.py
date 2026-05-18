#!/usr/bin/env python3
"""Fix heading structure: one H1 per page, demote duplicate H1s to H2."""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

def get_html_files():
    files = list(ROOT.glob("*.html"))
    files += list((ROOT / "areas-covered").glob("*.html"))
    return files

def count_h1(content: str) -> int:
    return len(re.findall(r"<h1\b", content, re.I))

def demote_extra_h1s(content: str) -> str:
    """Keep first H1, demote subsequent H1s to H2."""
    found = {"n": 0}
    def replace(m):
        found["n"] += 1
        if found["n"] == 1:
            return m.group(0)
        return m.group(0).replace("<h1", "<h2", 1).replace("</h1>", "</h2>")
    # Process opening and closing as a pair using DOTALL match
    pattern = re.compile(r"<h1\b[^>]*>.*?</h1>", re.I | re.S)
    return pattern.sub(replace, content)

def fix_homepage(content: str) -> str:
    """Homepage has 0 H1s. Promote the hero H2 to H1 with the new copy."""
    old = '<h2 class="hero-image-heading">Premier Moving &amp; Storage Company<br>with Prestige Steel Strong Rooms</h2>'
    new = '<h1 class="hero-image-heading">Eastbourne Removals &amp; Storage Experts Since 1982</h1>\n      <p class="hero-image-subhead white" style="font-size:1.25rem;margin-top:0.5rem;">Premier Moving &amp; Storage Company with Prestige Steel Strong Rooms — serving Eastbourne, Newhaven, Lewes, Brighton and all Sussex.</p>'
    return content.replace(old, new, 1)

def main():
    for fp in get_html_files():
        content = fp.read_text(encoding="utf-8")
        original = content
        if fp.name == "index.html" and count_h1(content) == 0:
            content = fix_homepage(content)
        if count_h1(content) > 1:
            content = demote_extra_h1s(content)
        if content != original:
            fp.write_text(content, encoding="utf-8")
            print(f"Fixed: {fp.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
