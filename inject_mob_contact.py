#!/usr/bin/env python3
"""Inject a CALL + EMAIL icon block at the end of each page's mobile menu.
 The block is hidden on desktop via CSS (.mob-menu-contact { display:none })
 and revealed only at ≤991px.
 Idempotent — re-running replaces an existing block.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"

BLOCK = '''        <div class="mob-menu-contact" aria-label="Quick contact">
          <a href="tel:01323848008" class="is-call" aria-label="Call us on 01323 848 008">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57a1 1 0 0 0-1.02.24l-2.2 2.2a15.05 15.05 0 0 1-6.59-6.59l2.2-2.2a1 1 0 0 0 .25-1.02A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1Z"/></svg>
            <span>Call us</span>
          </a>
          <a href="mailto:mark@markratcliffemoving.co.uk" class="is-email" aria-label="Email us">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/></svg>
            <span>Email us</span>
          </a>
        </div>
'''

# Strip any prior version (idempotency)
prev = re.compile(r'\s*<div class="mob-menu-contact"[^>]*>.*?</div>\s*</div>', re.S)


def process(fp: Path) -> bool:
    text = fp.read_text(encoding='utf-8')
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False
    orig = text
    # Remove old
    text = prev.sub('', text)

    # Find the closing of nav-menu (just before the menu-button div)
    # Pattern: ...</nav>\s*<div class="menu-button"
    new_text = re.sub(
        r'(\s*)(</nav>\s*<div class="menu-button)',
        BLOCK + r'\1\2',
        text, count=1
    )
    if new_text == text:
        # Some pages may use <nav role="navigation" class="nav-menu"> closing pattern
        new_text = re.sub(
            r'(\s*)</nav>(\s*<div class="menu-button)',
            r'\n' + BLOCK + r'\1</nav>\2',
            text, count=1
        )

    if new_text != orig:
        fp.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob('*.html'):
        try:
            if process(fp):
                n += 1
        except Exception as e:
            print(f'  ERR {fp.name}: {e}')
    print(f'Injected call/email mobile contact block on {n} pages.')


if __name__ == '__main__':
    main()
