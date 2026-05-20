#!/usr/bin/env python3
"""
The mega-menu uses <h4 class="mega-h">Category Name</h4> for dropdown
column titles. Those are navigation labels, not document headings —
they appear BEFORE the page's H1, which makes screen readers and
crawlers report a broken heading hierarchy.

This script converts every `<h4 class="mega-h">...</h4>` to
`<div class="mega-h">...</div>`. The class is preserved so the CSS
styling stays identical. Idempotent.
"""

import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PATTERN = re.compile(r'<h4\b(\s+class="mega-h")>(.*?)</h4>', re.S | re.I)

def fix(path: str) -> int:
    html = open(path, encoding='utf-8').read()
    new, n = PATTERN.subn(lambda m: f'<div{m.group(1)}>{m.group(2)}</div>', html)
    if n:
        open(path, 'w', encoding='utf-8').write(new)
    return n

def main() -> int:
    paths = sorted(glob.glob('*.html') + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html'))
    total = 0
    files = 0
    for p in paths:
        n = fix(p)
        if n:
            files += 1
            total += n
    print(f'Converted {total} <h4 class="mega-h"> → <div class="mega-h"> across {files} files.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
