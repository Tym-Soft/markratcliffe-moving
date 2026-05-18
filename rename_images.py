#!/usr/bin/env python3
"""Rename images for SEO and update every reference site-wide."""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
IMG_DIR = ROOT / "images"

# old_name -> new_name (basename only)
RENAMES = {
    "272763708_1997416893773723_7179548589196086698_n.jpg": "pad-wrapped-furniture-eastbourne-removals.jpg",
    "20200701_154903.jpg": "mark-ratcliffe-crew-loading-piano-eastbourne.jpg",
    "mrm-sleeper.jpg": "mark-ratcliffe-sleeper-cab-removal-lorry.jpg",
    "271945446_1989902067858539_1023122096450257812_n.jpg": "mark-ratcliffe-wrapped-furniture-sussex.jpg",
    "mark_ratckiffe.jpg": "mark-ratcliffe-founder-portrait.jpg",
    "20211023_180112.jpg": "mark-ratcliffe-modern-removal-lorry-eastbourne.jpg",
    "1963-Vintage-Moving-Van-1.jpg": "mark-ratcliffe-1963-vintage-bedford-removal-van.jpg",
    "1963-Vintage-Moving-Van-3.jpg": "mark-ratcliffe-1963-vintage-van-restored.jpg",
    "271863336_1988393178009428_8288437399475883358_n.jpg": "mark-ratcliffe-removal-fleet-vehicles-sussex.jpg",
    "APG-Final-Logo2020_UK-Domestic-Clear-BG.png": "apg-approved-payment-guarantee-uk-domestic.png",
    "IMA-Logo-FA-01_1.png": "ima-international-movers-association-logo.png",
    "BS-8564-2-1.png": "bs-8564-2-removals-storage-accreditation.png",
}

# Build srcset variants we need to redirect too
def expand_with_variants(name: str):
    stem, dot, ext = name.rpartition(".")
    variants = [name]
    for tag in ("-p-500", "-p-800", "-p-1080", "-p-1600", "-p-2000"):
        variants.append(f"{stem}{tag}.{ext}")
    return variants

def main():
    # Rename files
    renamed = []
    for old, new in RENAMES.items():
        for old_variant in expand_with_variants(old):
            old_p = IMG_DIR / old_variant
            if old_p.exists():
                new_variant = old_variant.replace(old.rsplit(".",1)[0], new.rsplit(".",1)[0])
                new_p = IMG_DIR / new_variant
                old_p.rename(new_p)
                renamed.append((old_variant, new_variant))

    print(f"Renamed {len(renamed)} files.")

    # Update references in every HTML file
    html_files = list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html"))
    files_changed = 0
    refs_updated = 0
    for fp in html_files:
        text = fp.read_text(encoding="utf-8")
        new_text = text
        for old_variant, new_variant in renamed:
            if old_variant in new_text:
                count = new_text.count(old_variant)
                new_text = new_text.replace(old_variant, new_variant)
                refs_updated += count
        if new_text != text:
            fp.write_text(new_text, encoding="utf-8")
            files_changed += 1

    print(f"Updated {refs_updated} references across {files_changed} HTML files.")

if __name__ == "__main__":
    main()
