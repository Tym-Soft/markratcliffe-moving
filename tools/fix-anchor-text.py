#!/usr/bin/env python3
"""
Rewrite non-descriptive anchor text to descriptive copy.

Two patterns handled:

1. `<a aria-label="Learn more about X">Learn more →</a>` (42 instances
   on 7 city pages) — drop the aria-label and use the service name as
   visible text: `<a>Removals Eastbourne →</a>`

2. Legacy "here" / "click here" text (8 instances on areas-covered
   pages) — replace with descriptive phrasing that matches the
   surrounding sentence.
"""

import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Pattern 1 — Learn more → with aria-label carrying the descriptive
# version: drop aria-label, use the service name as visible text.
LEARN_MORE = re.compile(
    r'<a\s+href="([^"]+)"\s+aria-label="Learn more about ([^"]+)">Learn more (?:&rarr;|→)</a>',
    re.I,
)

# Pattern 2 — specific "here"/"click here" instances we already
# surveyed. Each entry: (search_substring, replacement_substring).
# Keys are kept short and unique enough to match exactly.
HERE_REPLACEMENTS = [
    ('Take a look at more testimonials <a href="../reviews.html">here</a>.',
     '<a href="../reviews.html">Read more customer reviews on our reviews page</a>.'),
    ('have to say about their experience with us <a href="../reviews.html">here</a>.',
     'have said about their experience — <a href="../reviews.html">read more customer reviews</a>.'),
    ('Take a look at more reviews <a href="../reviews.html">here</a>.',
     '<a href="../reviews.html">Read more customer reviews</a>.'),
    ('To read more reviews, simply click <a href="../reviews.html">here</a>.',
     '<a href="../reviews.html">Read more customer reviews on our reviews page</a>.'),
    ('have to say about us <a href="../reviews.html">here</a>.',
     'have said about us — <a href="../reviews.html">read more customer reviews</a>.'),
    ('To read more testimonials, simply click <a href="../reviews.html">here</a>.',
     '<a href="../reviews.html">Read more customer testimonials on our reviews page</a>.'),
    ('contact us <a href="../mark-ratcliffe-moving-online-removals-quote.html">here</a>',
     '<a href="../mark-ratcliffe-moving-online-removals-quote.html">request a free moving quote</a>'),
    ('give us contact us <a href="../mark-ratcliffe-moving-online-removals-quote.html">here</a>',
     '<a href="../mark-ratcliffe-moving-online-removals-quote.html">request a free moving quote</a>'),
]


def fix_file(path: str) -> int:
    html = open(path, encoding='utf-8').read()
    original = html
    n = 0

    # Pattern 1
    def lm_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        href, service = m.group(1), m.group(2)
        return f'<a href="{href}">{service} &rarr;</a>'
    html = LEARN_MORE.sub(lm_sub, html)

    # Pattern 2
    for needle, repl in HERE_REPLACEMENTS:
        if needle in html:
            html = html.replace(needle, repl)
            n += 1

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
    return n


def main() -> int:
    paths = sorted(glob.glob('*.html') + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html'))
    files = 0; total = 0
    for p in paths:
        n = fix_file(p)
        if n:
            files += 1; total += n
            print(f'{p:60s} → {n} rewrite(s)')
    print(f'\nRewrote {total} non-descriptive anchor(s) across {files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
