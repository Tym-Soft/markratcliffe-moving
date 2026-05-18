#!/usr/bin/env python3
"""Remove orphan old-Webflow footer content that's still lurking above the new <footer class="mr-footer">.

The previous footer-removal regex was non-greedy and stopped at the first triple-closing-div,
leaving the inner footer columns (Contact Us, Find Us, Follow Us, Web Details) intact.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"


def fix_file(fp: Path) -> bool:
    text = fp.read_text(encoding='utf-8')
    if 'http-equiv="refresh"' in text and len(text) < 2000:
        return False
    orig = text

    # Find the new footer position
    mr_idx = text.find('<footer class="mr-footer"')
    if mr_idx < 0:
        return False

    # Find the last "clean" close BEFORE the mr-footer.
    # Clean closers: </section>, </main>, </header>, end of np-related, end of np-cta-block,
    # or the end of any standard structural element. We scan backwards.
    before_mr = text[:mr_idx]
    # The last clean close patterns we accept as a boundary (in order of preference):
    boundary_anchors = [
        # End of np-related (related pages section)
        re.compile(r'</section>\s*$', re.S),
        # End of any np-section
        re.compile(r'</section>\s*$', re.S),
        # End of np-faq
        re.compile(r'</details>\s*</div>\s*</section>\s*$', re.S),
        # Closing of any html element with newline buffer
        re.compile(r'</section>\s*\n\s*$', re.S),
    ]

    # Find positions of all `</section>` ending tags in `before_mr` and take the last one
    sections = list(re.finditer(r'</section>', before_mr))
    if not sections:
        # No </section> found — fallback: look for end of nav-section or similar
        # leave file alone in that case
        return False

    last_section_end = sections[-1].end()

    # Between the last </section> and `<footer class="mr-footer">` should be only whitespace.
    # Anything else is orphan content. Remove it.
    gap = before_mr[last_section_end:]
    if gap.strip() == '':
        return False   # already clean

    # Check the gap actually contains old-footer artefacts (sanity check)
    artefacts = ['footer-info-wrap', 'footer-a', 'footer-map-wrapper', 'footer-bar-no',
                 'footer-accred-row', 'fhio-wrap', 'footer-accred-wrap', 'reviews w-embed']
    has_artefact = any(a in gap for a in artefacts)
    if not has_artefact and len(gap.strip()) < 100:
        # Tiny whitespace/comment — leave alone
        return False

    # Build clean text: everything up to last_section_end + newline + mr-footer onwards
    new_text = before_mr[:last_section_end] + "\n  " + text[mr_idx:]

    if new_text != orig:
        fp.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob('*.html'):
        try:
            if fix_file(fp):
                n += 1
        except Exception as e:
            print(f'  ERR {fp.name}: {e}')
    print(f'Cleaned orphan footer content on {n} pages.')


if __name__ == '__main__':
    main()
