#!/usr/bin/env python3
"""Convert all raster images to WebP, update HTML refs, remove old files.
Preserves SVG, favicon.png, webclip.png.
"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
IMG_DIR = ROOT / "images"
PRESERVE = {"favicon.png", "webclip.png"}  # icons referenced by <link>

def convert_all():
    """Run cwebp on every JPG/JPEG/PNG (except preserved icons)."""
    converted = []   # list of (old_basename, new_basename)
    for f in IMG_DIR.iterdir():
        if not f.is_file():
            continue
        if f.name in PRESERVE:
            continue
        ext = f.suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png"):
            continue
        new_name = f.stem + ".webp"
        new_path = IMG_DIR / new_name
        if new_path.exists():
            converted.append((f.name, new_name))
            continue
        # cwebp -q 82 (good balance); for PNG with alpha, near-lossless is better
        if ext == ".png":
            # Try near-lossless for logos/badges with transparency
            subprocess.run(
                ["cwebp", "-q", "85", "-alpha_q", "100", "-quiet", str(f), "-o", str(new_path)],
                check=False
            )
        else:
            subprocess.run(
                ["cwebp", "-q", "82", "-quiet", str(f), "-o", str(new_path)],
                check=False
            )
        if new_path.exists():
            converted.append((f.name, new_name))
    return converted

def update_html(converted):
    """In every HTML file: rewrite all references from old → new, remove <picture> wrappers that are now redundant."""
    rename_map = dict(converted)
    html_files = list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html"))
    n = 0
    refs = 0
    for fp in html_files:
        text = fp.read_text(encoding="utf-8")
        new_text = text
        for old, new in rename_map.items():
            if old in new_text:
                refs += new_text.count(old)
                new_text = new_text.replace(old, new)
        # Unwrap <picture>…<source webp><img …></picture> blocks since src is now webp
        # Pattern: <picture><source type="image/webp" srcset="X.webp"><img ... src="X.webp" ...></picture>
        # After replacement, the source.srcset and img.src both end in .webp — collapse.
        unwrap = re.compile(
            r'<picture>\s*<source\s+type="image/webp"\s+srcset="[^"]+\.webp">\s*(<img[^>]+>)\s*</picture>',
            re.I
        )
        new_text = unwrap.sub(r"\1", new_text)
        if new_text != text:
            fp.write_text(new_text, encoding="utf-8")
            n += 1
    print(f"Updated {refs} references across {n} HTML files.")

def remove_old_rasters(converted):
    """Remove the original JPG/JPEG/PNG files that now have a WebP equivalent and aren't referenced anywhere."""
    html_files = list(ROOT.glob("*.html")) + list((ROOT / "areas-covered").glob("*.html"))
    # Build big concat of HTML content for ref check
    all_text = "\n".join(fp.read_text(encoding="utf-8") for fp in html_files)
    removed = 0
    for old, _new in converted:
        if old in PRESERVE:
            continue
        # Check no HTML still references the old name
        if old in all_text:
            continue
        p = IMG_DIR / old
        if p.exists():
            p.unlink()
            removed += 1
    print(f"Removed {removed} orphan raster files.")

def main():
    converted = convert_all()
    print(f"Converted {len(converted)} files to WebP.")
    update_html(converted)
    remove_old_rasters(converted)

if __name__ == "__main__":
    main()
