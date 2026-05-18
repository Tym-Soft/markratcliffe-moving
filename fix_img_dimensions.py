#!/usr/bin/env python3
"""Add explicit width/height attributes to every <img> that's missing them.
Reads actual pixel dimensions from each image file.
"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"
IMG_DIR = ROOT / "images"

# Cache image dimensions
_dims_cache = {}
def get_dimensions(name):
    if name in _dims_cache:
        return _dims_cache[name]
    fp = IMG_DIR / name
    if not fp.exists():
        return None
    ext = fp.suffix.lower()
    w, h = None, None
    if ext == ".svg":
        # Read viewBox/width/height attrs
        text = fp.read_text(errors='ignore')[:2000]
        m = re.search(r'viewBox="[\d.\s-]*?(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)"', text)
        if m:
            w, h = int(float(m.group(1))), int(float(m.group(2)))
    elif ext in (".webp", ".jpg", ".jpeg", ".png"):
        try:
            r = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(fp)],
                               capture_output=True, text=True, timeout=5)
            for line in r.stdout.splitlines():
                if 'pixelWidth' in line: w = int(line.split(':')[-1].strip())
                if 'pixelHeight' in line: h = int(line.split(':')[-1].strip())
        except Exception:
            pass
    _dims_cache[name] = (w, h) if w and h else None
    return _dims_cache[name]


def fix_file(fp):
    text = fp.read_text(encoding='utf-8')
    orig = text
    # Match every <img ...>
    def replace(m):
        attrs = m.group(0)
        # Skip if both width and height already present
        if re.search(r'\bwidth=', attrs) and re.search(r'\bheight=', attrs):
            return attrs
        src_m = re.search(r'src="images/([^"]+)"', attrs)
        if not src_m:
            return attrs
        name = src_m.group(1).split('?')[0]
        dims = get_dimensions(name)
        if not dims:
            return attrs
        w, h = dims
        # If width attr present without height, append height
        if re.search(r'\bwidth="\d+', attrs):
            # Calculate height proportional to specified width
            wm = re.search(r'\bwidth="(\d+)"', attrs)
            if wm:
                specified_w = int(wm.group(1))
                scaled_h = int(h * specified_w / w)
                # Insert height attribute after width
                attrs = re.sub(r'(\bwidth="\d+")', r'\1 height="' + str(scaled_h) + '"', attrs, count=1)
                return attrs
        # Neither attribute present — add both
        attrs = attrs[:-1] + f' width="{w}" height="{h}">'
        return attrs

    text = re.sub(r'<img\b[^>]+>', replace, text)
    if text != orig:
        fp.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for fp in ROOT.rglob('*.html'):
        if fix_file(fp):
            n += 1
    print(f'Added missing img dimensions to {n} files.')


if __name__ == '__main__':
    main()
