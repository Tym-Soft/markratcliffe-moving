#!/usr/bin/env python3
"""Second pass: small branded closing block to push every new blog past 2000 words."""
import os, re

BLOG_FILES = [
    'moving-to-eastbourne-area-guide.html',
    'what-to-pack-first-when-moving-house.html',
    'how-to-pack-kitchen-items-safely.html',
    'how-to-pack-clothes-without-wrinkling.html',
    'moving-to-brighton-area-guide.html',
    'moving-to-chichester-area-guide.html',
    'moving-to-hastings-area-guide.html',
    'moving-to-worthing-area-guide.html',
    'best-areas-to-live-east-sussex-2026.html',
    'how-to-choose-right-self-storage.html',
    'short-term-vs-long-term-storage.html',
    'what-you-can-and-cannot-store.html',
    'benefits-of-professional-packing-service.html',
    '10-most-commonly-forgotten-moving-items.html',
]

CLOSING = """  <section class="np-section">
    <div class="np-inner">
      <h2>Why customers choose Mark Ratcliffe Moving for Sussex moves</h2>
      <p>We've been a <a href="../about-us.html">family-run Sussex remover</a> since 1982 &mdash; the same name on the lorry as the name on the paperwork. Mark personally surveys the high-value and overseas moves; our crews are directly employed (not casual day labour) and trained at our own staff training centre, one of only a handful of UK removers with that facility on site.</p>
      <p>Standard inclusions on every full removal: pad-wrap protection for every freestanding piece of furniture, removal-grade cartons, a written and itemised <a href="../mark-ratcliffe-moving-online-removals-quote.html">fixed-price quote</a> with no surprises on the day, and the British Association of Removers' Advance Payment Guarantee protecting every deposit. The result, over forty years and tens of thousands of moves, is a 4.9/5 review average across <a href="../reviews.html">120+ independent Google reviews</a>.</p>
      <p>Booking the survey takes ten minutes. Whether it's a one-bedroom flat across <a href="../removals-eastbourne.html">Eastbourne</a> or a country house to <a href="../international-removals-eastbourne.html">overseas</a>, the process is the same: in-home or video survey, written quote within 48 hours, deposit-protected booking, and a calm move day.</p>
    </div>
  </section>
"""

faq_open = re.compile(r'(\s*)<section class="np-section np-faq">')
n = 0
for slug in BLOG_FILES:
    p = os.path.join('blog', slug)
    if not os.path.isfile(p): continue
    html = open(p, encoding='utf-8').read()
    if 'Why customers choose Mark Ratcliffe Moving for Sussex moves' in html: continue
    new_html, c = faq_open.subn('\n' + CLOSING + r'\1<section class="np-section np-faq">', html, count=1)
    if c == 1:
        open(p, 'w', encoding='utf-8').write(new_html)
        n += 1
print(f'Closing block added to {n} blog files.')
