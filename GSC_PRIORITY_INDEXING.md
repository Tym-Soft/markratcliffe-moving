# GSC Manual Request-Indexing — Priority List

**Issue:** "Discovered, currently not indexed" — 176 URLs Google has queued but
not yet crawled. Detected 2026-05-23 after the URL restructure went live.

**How to use this list:**
1. Go to **Google Search Console → URL Inspection** (top search bar).
2. Paste each URL one at a time. Hit Enter.
3. Click **"Request Indexing"** on the inspection result.
4. Google allows **roughly 10 requests per 24 hours**. Spread the list
   across 3 days. After each batch, give it 48-72h before checking back.
5. Don't refresh the same URL more than once per week — that resets the
   queue position instead of moving it forward.

Tier-1 hubs go first because once they're indexed, they distribute crawl
priority to every deep page they link to. Don't skip them for individual
town pages.

---

## Day 1 — Hubs and HQ-area money pages

These are the structural backbone. Indexing them first unblocks discovery
for everything underneath.

1. `https://www.markratcliffemoving.co.uk/areas-covered/`
   Why: Primary geographic hub. Distributes crawl priority to 108 area pages.
2. `https://www.markratcliffemoving.co.uk/services/`
   Why: Primary service hub. Distributes crawl priority to 17 service pages.
3. `https://www.markratcliffemoving.co.uk/resources/`
   Why: Resources hub (cost guides, materials, checklists). Trust + commercial.
4. `https://www.markratcliffemoving.co.uk/blog/`
   Why: Blog hub. Signals to Google that fresh content publication exists.
5. `https://www.markratcliffemoving.co.uk/reviews.html`
   Why: Trust signal. Many users search "[company name] reviews" — it should
   rank from day one.
6. `https://www.markratcliffemoving.co.uk/areas-covered/removals-eastbourne.html`
   Why: HQ town. Highest local-search intent for the business address.
7. `https://www.markratcliffemoving.co.uk/areas-covered/east-sussex.html`
   Why: Primary county hub. Captures broader county-level searches.
8. `https://www.markratcliffemoving.co.uk/areas-covered/removals-brighton.html`
   Why: Highest-volume removals search in the service area.
9. `https://www.markratcliffemoving.co.uk/services/storage-eastbourne.html`
   Why: High-margin service in HQ town — premium storage rooms.
10. `https://www.markratcliffemoving.co.uk/services/man-and-van-eastbourne.html`
    Why: High-volume "man and van" search in HQ town.

---

## Day 2 — Counties + remaining money services + top satellites

11. `https://www.markratcliffemoving.co.uk/areas-covered/west-sussex.html`
12. `https://www.markratcliffemoving.co.uk/areas-covered/surrey.html`
13. `https://www.markratcliffemoving.co.uk/areas-covered/kent.html`
14. `https://www.markratcliffemoving.co.uk/areas-covered/hailsham-removals.html`
    Why: 4 mi from depot — frequent jobs, strong local intent.
15. `https://www.markratcliffemoving.co.uk/services/international-removals-eastbourne.html`
    Why: Premium service, FIDI-network differentiator.
16. `https://www.markratcliffemoving.co.uk/services/office-removals-eastbourne.html`
17. `https://www.markratcliffemoving.co.uk/services/house-clearance-eastbourne.html`
18. `https://www.markratcliffemoving.co.uk/services/packing-services-eastbourne.html`
19. `https://www.markratcliffemoving.co.uk/areas-covered/removals-bexhill.html`
20. `https://www.markratcliffemoving.co.uk/areas-covered/removals-hastings.html`

---

## Day 3 — Top satellite town pages + flagship resources

21. `https://www.markratcliffemoving.co.uk/areas-covered/removals-tonbridge.html`
22. `https://www.markratcliffemoving.co.uk/areas-covered/man-and-van-tunbridge-wells.html`
23. `https://www.markratcliffemoving.co.uk/areas-covered/removals-worthing.html`
24. `https://www.markratcliffemoving.co.uk/areas-covered/removals-horsham.html`
25. `https://www.markratcliffemoving.co.uk/areas-covered/removals-chichester.html`
26. `https://www.markratcliffemoving.co.uk/areas-covered/removals-maidstone.html`
27. `https://www.markratcliffemoving.co.uk/resources/pricing.html`
    Why: Commercial-intent searches — "removals price" / "moving cost".
28. `https://www.markratcliffemoving.co.uk/resources/removals-eastbourne-cost.html`
    Why: Long-tail commercial — "cost of removals eastbourne".
29. `https://www.markratcliffemoving.co.uk/resources/buy-packing-materials-eastbourne.html`
    Why: Transactional intent — packing materials purchase.
30. `https://www.markratcliffemoving.co.uk/blog/best-day-of-week-to-move-house.html`
    Why: Evergreen, high-search-volume info query.

---

## Don't bother manually requesting these (let the queue handle)

- The remaining ~146 URLs (smaller town pages, deeper blog posts).
  Google will crawl through them naturally over the next 4-8 weeks now that
  the technical health is clean and the hubs are indexed.

## After the 3 days

- Resubmit the sitemap in GSC (Sitemaps → re-enter the URL → Submit).
- Check the Indexing → Pages report again in a week — expect 30-60 of
  these to have moved to "Indexed".
- The remaining will normalise over 2-3 months unless you also build
  external backlinks to deep pages (industry directories, local press,
  supplier reciprocals are the usual moves).

---

*Generated 2026-05-25 in response to GSC "Discovered, currently not indexed"
report covering 176 affected pages.*
