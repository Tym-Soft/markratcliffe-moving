#!/usr/bin/env python3
"""Final per-image SEO fixes on index.html + cleanup of remaining .jpeg variants."""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
IMG_DIR = ROOT / "images"
INDEX = ROOT / "index.html"

# Step 1: rename remaining .jpeg variants (the original renamer missed these)
JPEG_RENAMES = {
    "272763708_1997416893773723_7179548589196086698_n": "pad-wrapped-furniture-eastbourne-removals",
    "20200701_154903": "mark-ratcliffe-crew-loading-piano-eastbourne",
    "1963-Vintage-Moving-Van-1": "mark-ratcliffe-1963-vintage-bedford-removal-van",
    "1963-Vintage-Moving-Van-3": "mark-ratcliffe-1963-vintage-van-restored",
    "20211023_180112": "mark-ratcliffe-modern-removal-lorry-eastbourne",
    "271863336_1988393178009428_8288437399475883358_n": "mark-ratcliffe-removal-fleet-vehicles-sussex",
}

def rename_jpeg_variants():
    renamed = []
    for stem_old, stem_new in JPEG_RENAMES.items():
        for f in IMG_DIR.glob(f"{stem_old}*.jpeg"):
            new_name = f.name.replace(stem_old, stem_new)
            new_path = IMG_DIR / new_name
            f.rename(new_path)
            renamed.append((f.name, new_name))
    return renamed

def update_html_refs(html_files, renamed):
    for fp in html_files:
        text = fp.read_text(encoding="utf-8")
        new = text
        for old, n in renamed:
            new = new.replace(old, n)
        if new != text:
            fp.write_text(new, encoding="utf-8")

# Step 2: apply per-image fixes in index.html
def fix_index():
    text = INDEX.read_text(encoding="utf-8")

    # #1 Header logo — fix Newhaven reference, add height
    text = text.replace(
        '<img src="images/Mark-Ratcliffe.svg" width="180" alt="Removals Newhaven - Mark Ratcliffe logo " class="logo-img" decoding="async" fetchpriority="high">',
        '<img src="images/Mark-Ratcliffe.svg" width="180" height="60" alt="Mark Ratcliffe Moving and Storage — Eastbourne removals company logo" class="logo-img" decoding="async" fetchpriority="high">'
    )

    # #2 Pad-wrapped furniture — picture/webp + new alt + height + figure
    text = text.replace(
        '<img src="images/pad-wrapped-furniture-eastbourne-removals.jpg" width="480" alt="photo of Japanese sock wrapped furniture" sizes="(max-width: 479px) 100vw, 480px" srcset="images/pad-wrapped-furniture-eastbourne-removals-p-500.jpeg 500w, images/pad-wrapped-furniture-eastbourne-removals-p-800.jpeg 800w, images/pad-wrapped-furniture-eastbourne-removals.jpg 1000w" class="lb-image" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/pad-wrapped-furniture-eastbourne-removals.webp"><img src="images/pad-wrapped-furniture-eastbourne-removals.jpg" width="480" height="360" alt="Furniture individually pad-wrapped and labelled before a Sussex home removal" sizes="(max-width: 479px) 100vw, 480px" srcset="images/pad-wrapped-furniture-eastbourne-removals-p-500.jpeg 500w, images/pad-wrapped-furniture-eastbourne-removals-p-800.jpeg 800w, images/pad-wrapped-furniture-eastbourne-removals.jpg 1000w" class="lb-image" decoding="async" loading="lazy"></picture>'
    )

    # #3 Crew piano
    text = text.replace(
        '<img src="images/mark-ratcliffe-crew-loading-piano-eastbourne.jpg" width="480" alt="Photo of trained Mark Ratcliffe Moving removals staff loading a piano" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-crew-loading-piano-eastbourne-p-500.jpeg 500w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-800.jpeg 800w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-1080.jpeg 1080w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-1600.jpeg 1600w, images/mark-ratcliffe-crew-loading-piano-eastbourne.jpg 1920w" class="lb-image" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-crew-loading-piano-eastbourne.webp"><img src="images/mark-ratcliffe-crew-loading-piano-eastbourne.jpg" width="480" height="480" alt="Trained Mark Ratcliffe Moving crew carefully loading an upright piano during an Eastbourne removal" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-crew-loading-piano-eastbourne-p-500.jpeg 500w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-800.jpeg 800w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-1080.jpeg 1080w, images/mark-ratcliffe-crew-loading-piano-eastbourne-p-1600.jpeg 1600w, images/mark-ratcliffe-crew-loading-piano-eastbourne.jpg 1920w" class="lb-image" decoding="async" loading="lazy"></picture>'
    )

    # #4 Sleeper cab
    text = text.replace(
        '<img src="images/mark-ratcliffe-sleeper-cab-removal-lorry.jpg" width="480" alt="photo of Mark Ratcliffe sleeper moving van, Eastbourne" class="lb-image" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-sleeper-cab-removal-lorry.webp"><img src="images/mark-ratcliffe-sleeper-cab-removal-lorry.jpg" width="480" height="270" alt="Mark Ratcliffe Moving sleeper-cab removal lorry used for long-distance and overseas moves" class="lb-image" decoding="async" loading="lazy"></picture>'
    )

    # #5 Duplicate body logo — decorative
    text = text.replace(
        '<img src="images/Mark-Ratcliffe.svg" height="150" alt="" decoding="async" loading="lazy">',
        '<img src="images/Mark-Ratcliffe.svg" width="200" height="150" alt="" role="presentation" aria-hidden="true" decoding="async" loading="lazy">'
    )

    # #6 FB-Pic badge — fix lightbox/thumbnail mismatch. Use Member hat image (BAR) as visible thumbnail
    text = text.replace(
        '<img src="images/FB-Pic.jpg" width="76" sizes="76px" srcset="images/FB-Pic-p-500.jpg 500w, images/FB-Pic.jpg 702w" alt="" class="badge-image" decoding="async" loading="lazy">',
        '<img src="images/Member-hat-with-number.png" width="76" height="82" alt="Member of the British Association of Removers (BAR)" class="badge-image" decoding="async" loading="lazy">'
    )

    # #7 BS 8564 — alt + height
    text = text.replace(
        '<img src="images/bs-8564-2-removals-storage-accreditation.png" width="110" alt="" class="badge-image" decoding="async" loading="lazy">',
        '<img src="images/bs-8564-2-removals-storage-accreditation.png" width="110" height="180" alt="BS 8564 quality accreditation for removals and storage" class="badge-image" decoding="async" loading="lazy">'
    )

    # #8 APG
    text = text.replace(
        '<img src="images/apg-approved-payment-guarantee-uk-domestic.png" width="110" sizes="110px" srcset="images/apg-approved-payment-guarantee-uk-domestic-p-500.png 500w, images/apg-approved-payment-guarantee-uk-domestic.png 600w" alt="" class="badge-image" decoding="async" loading="lazy">',
        '<img src="images/apg-approved-payment-guarantee-uk-domestic.png" width="110" height="130" alt="APG Approved Payment Guarantee badge — UK domestic removals" sizes="110px" srcset="images/apg-approved-payment-guarantee-uk-domestic-p-500.png 500w, images/apg-approved-payment-guarantee-uk-domestic.png 600w" class="badge-image" decoding="async" loading="lazy">'
    )

    # #9 IMA — drop oversized srcset variants that no longer make sense (source is now ~500w)
    text = text.replace(
        '<img src="images/ima-international-movers-association-logo.png" width="115" sizes="115px" srcset="images/ima-international-movers-association-logo-p-500.png 500w, images/ima-international-movers-association-logo-p-800.png 800w, images/ima-international-movers-association-logo-p-1080.png 1080w, images/ima-international-movers-association-logo-p-1600.png 1600w, images/ima-international-movers-association-logo-p-2000.png 2000w, images/ima-international-movers-association-logo.png 3064w" alt="" class="badge-image" decoding="async" loading="lazy">',
        '<img src="images/ima-international-movers-association-logo.png" width="115" height="81" alt="International Movers Association (IMA) member badge" class="badge-image" decoding="async" loading="lazy">'
    )

    # #10 UK Thai
    text = text.replace(
        '<img src="images/UK---Thai-Movers-Logo.png" width="350" sizes="350px" srcset="images/UK---Thai-Movers-Logo-p-500.png 500w, images/UK---Thai-Movers-Logo-p-800.png 800w, images/UK---Thai-Movers-Logo-p-1080.png 1080w, images/UK---Thai-Movers-Logo.png 1200w" alt="" class="badge-image" decoding="async" loading="lazy">',
        '<img src="images/UK---Thai-Movers-Logo.png" width="350" height="100" alt="UK and Thai Movers Group — specialist UK-to-Thailand removals partner" sizes="350px" srcset="images/UK---Thai-Movers-Logo-p-500.png 500w, images/UK---Thai-Movers-Logo-p-800.png 800w, images/UK---Thai-Movers-Logo-p-1080.png 1080w, images/UK---Thai-Movers-Logo.png 1200w" class="badge-image" decoding="async" loading="lazy">'
    )

    # #11 Filler floated photo — give it real alt + height + webp
    text = text.replace(
        '<div><img src="images/mark-ratcliffe-wrapped-furniture-sussex.jpg" loading="lazy" alt=""></div>',
        '<div><picture><source type="image/webp" srcset="images/mark-ratcliffe-wrapped-furniture-sussex.webp"><img src="images/mark-ratcliffe-wrapped-furniture-sussex.jpg" width="600" height="450" alt="Pad-wrapped sideboard ready for a Sussex home move with Mark Ratcliffe Moving" decoding="async" loading="lazy"></picture></div>'
    )

    # #12 Founder portrait — critical E-E-A-T
    text = text.replace(
        '<img src="images/mark-ratcliffe-founder-portrait.jpg" loading="lazy" alt="" class="mark-image">',
        '<img src="images/mark-ratcliffe-founder-portrait.jpg" width="300" height="214" alt="Mark Ratcliffe, founder of Mark Ratcliffe Moving and Storage in Eastbourne — over 40 years experience in UK and international removals" itemprop="image" decoding="async" loading="lazy" class="mark-image">'
    )

    # #13–17 — 5x van.svg bullets: make decorative
    text = text.replace(
        '<img src="images/van-mark-ratcliffe.svg" alt="Domestic Removals Eastbourne, Sussex" width="75" decoding="async" loading="lazy">',
        '<img src="images/van-mark-ratcliffe.svg" alt="" role="presentation" aria-hidden="true" width="75" height="40" decoding="async" loading="lazy">'
    )  # default replace_all not enabled; do it explicitly
    # ensure all 5 are replaced
    text = re.sub(
        r'<img src="images/van-mark-ratcliffe\.svg" alt="Domestic Removals Eastbourne, Sussex" width="75" decoding="async" loading="lazy">',
        '<img src="images/van-mark-ratcliffe.svg" alt="" role="presentation" aria-hidden="true" width="75" height="40" decoding="async" loading="lazy">',
        text
    )

    # #18 truck.svg — already empty alt; add aria-hidden
    text = text.replace(
        '<img src="images/truck.svg" loading="lazy" width="75" alt="" class="small-margin-right">',
        '<img src="images/truck.svg" loading="lazy" width="75" height="50" alt="" role="presentation" aria-hidden="true" class="small-margin-right">'
    )

    # #19 Vintage Bedford 1
    text = text.replace(
        '<img src="images/mark-ratcliffe-1963-vintage-bedford-removal-van.jpg" width="480" alt="photo of all vand and vehicles in the Mark Ratcliffe Moving fleet" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-500.jpeg 500w, images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-800.jpeg 800w, images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-1080.jpeg 1080w, images/mark-ratcliffe-1963-vintage-bedford-removal-van.jpg 1200w" class="lb-image van" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-1963-vintage-bedford-removal-van.webp"><img src="images/mark-ratcliffe-1963-vintage-bedford-removal-van.jpg" width="480" height="480" alt="1963 vintage Bedford removal van from the Mark Ratcliffe Moving fleet" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-500.jpeg 500w, images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-800.jpeg 800w, images/mark-ratcliffe-1963-vintage-bedford-removal-van-p-1080.jpeg 1080w, images/mark-ratcliffe-1963-vintage-bedford-removal-van.jpg 1200w" class="lb-image van" decoding="async" loading="lazy"></picture>'
    )

    # #20 Modern lorry
    text = text.replace(
        '<img src="images/mark-ratcliffe-modern-removal-lorry-eastbourne.jpg" width="480" alt="photo of all vand and vehicles in the Mark Ratcliffe Moving fleet" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-500.jpeg 500w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-800.jpeg 800w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-1080.jpeg 1080w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-1600.jpeg 1600w, images/mark-ratcliffe-modern-removal-lorry-eastbourne.jpg 1800w" class="lb-image van" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp"><img src="images/mark-ratcliffe-modern-removal-lorry-eastbourne.jpg" width="480" height="360" alt="Modern Mark Ratcliffe Moving removal lorry parked at the Eastbourne depot" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-500.jpeg 500w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-800.jpeg 800w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-1080.jpeg 1080w, images/mark-ratcliffe-modern-removal-lorry-eastbourne-p-1600.jpeg 1600w, images/mark-ratcliffe-modern-removal-lorry-eastbourne.jpg 1800w" class="lb-image van" decoding="async" loading="lazy"></picture>'
    )

    # #21 Vintage restored
    text = text.replace(
        '<img src="images/mark-ratcliffe-1963-vintage-van-restored.jpg" width="480" alt="photo of all vand and vehicles in the Mark Ratcliffe Moving fleet" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-1963-vintage-van-restored-p-500.jpeg 500w, images/mark-ratcliffe-1963-vintage-van-restored-p-800.jpeg 800w, images/mark-ratcliffe-1963-vintage-van-restored-p-1080.jpeg 1080w, images/mark-ratcliffe-1963-vintage-van-restored.jpg 1200w" class="lb-image van" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-1963-vintage-van-restored.webp"><img src="images/mark-ratcliffe-1963-vintage-van-restored.jpg" width="480" height="480" alt="Restored 1963 vintage removal van celebrating 40 years of Mark Ratcliffe Moving" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-1963-vintage-van-restored-p-500.jpeg 500w, images/mark-ratcliffe-1963-vintage-van-restored-p-800.jpeg 800w, images/mark-ratcliffe-1963-vintage-van-restored-p-1080.jpeg 1080w, images/mark-ratcliffe-1963-vintage-van-restored.jpg 1200w" class="lb-image van" decoding="async" loading="lazy"></picture>'
    )

    # #22 Fleet line-up
    text = text.replace(
        '<img src="images/mark-ratcliffe-removal-fleet-vehicles-sussex.jpg" width="480" alt="photo of all vans and vehicles in the Mark Ratcliffe Moving fleet" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-500.jpeg 500w, images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-800.jpeg 800w, images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-1080.jpeg 1080w, images/mark-ratcliffe-removal-fleet-vehicles-sussex.jpg 1536w" class="lb-image van" decoding="async" loading="lazy">',
        '<picture><source type="image/webp" srcset="images/mark-ratcliffe-removal-fleet-vehicles-sussex.webp"><img src="images/mark-ratcliffe-removal-fleet-vehicles-sussex.jpg" width="480" height="340" alt="Mark Ratcliffe Moving removal fleet lined up at the Sussex depot" sizes="(max-width: 479px) 100vw, 480px" srcset="images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-500.jpeg 500w, images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-800.jpeg 800w, images/mark-ratcliffe-removal-fleet-vehicles-sussex-p-1080.jpeg 1080w, images/mark-ratcliffe-removal-fleet-vehicles-sussex.jpg 1536w" class="lb-image van" decoding="async" loading="lazy"></picture>'
    )

    # #23 chat.svg — decorative + aria-hidden
    text = text.replace(
        '<img src="images/chat.svg" width="75" alt="" decoding="async" loading="lazy">',
        '<img src="images/chat.svg" width="75" height="60" alt="" role="presentation" aria-hidden="true" decoding="async" loading="lazy">'
    )

    # #24 facebook.svg footer
    text = text.replace(
        '<img src="images/facebook.svg" width="35" alt="Facebook icon" class="hover-enlarge" decoding="async" loading="lazy">',
        '<img src="images/facebook.svg" width="35" height="35" alt="Follow Mark Ratcliffe Moving on Facebook" class="hover-enlarge" decoding="async" loading="lazy">'
    )

    # #25 FHIO footer
    text = text.replace(
        '<img src="images/FHIO-Logo-01.png" loading="lazy" sizes="100vw" srcset="images/FHIO-Logo-01-p-500.png 500w, images/FHIO-Logo-01-p-800.png 800w, images/FHIO-Logo-01-p-1080.png 1080w, images/FHIO-Logo-01-p-1600.png 1600w, images/FHIO-Logo-01.png 1708w" alt="" class="fhio-image">',
        '<img src="images/FHIO-Logo-01.png" width="300" height="100" loading="lazy" alt="Foundation of Independent Home Improvers (FHIO) accredited member" class="fhio-image">'
    )

    INDEX.write_text(text, encoding="utf-8")

def main():
    renamed = rename_jpeg_variants()
    print(f"Renamed {len(renamed)} .jpeg variants.")
    html_files = list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html"))
    update_html_refs(html_files, renamed)
    print("HTML references updated.")
    fix_index()
    print("index.html image fixes applied.")

if __name__ == "__main__":
    main()
