#!/usr/bin/env python3
"""
Re-encode any image in /images/ that is over 200 KB so it drops under
the threshold. Uses cwebp for .webp files (quality 75, max width
1600px) and pngquant for .png files (compression 65–80).

JPEGs are left alone; sips can be used manually for those if needed.

Idempotent — pages that are already under 200 KB are skipped.
"""

from __future__ import annotations
import glob, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

THRESHOLD_BYTES = 200 * 1024
MAX_WIDTH       = 1600
WEBP_QUALITY    = 75


def file_kb(path: str) -> int:
    return os.path.getsize(path) // 1024


def get_webp_width(path: str) -> int | None:
    """Use sips on macOS to read pixel width."""
    try:
        out = subprocess.check_output(['sips', '--getProperty', 'pixelWidth', path],
                                      stderr=subprocess.DEVNULL).decode()
    except Exception:
        return None
    for line in out.splitlines():
        if 'pixelWidth' in line:
            return int(line.split(':')[1].strip())
    return None


def compress_webp(path: str) -> tuple[int, int]:
    """Returns (before_kb, after_kb)."""
    before = file_kb(path)
    width = get_webp_width(path) or 0
    args = ['cwebp', '-q', str(WEBP_QUALITY), '-m', '6', '-mt', '-quiet']
    if width and width > MAX_WIDTH:
        args += ['-resize', str(MAX_WIDTH), '0']
    # cwebp can't read .webp directly — convert through PNG via dwebp first
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as png:
        png_path = png.name
    try:
        subprocess.run(['dwebp', '-quiet', path, '-o', png_path], check=True)
        tmp_out = path + '.tmp.webp'
        subprocess.run(args + [png_path, '-o', tmp_out], check=True)
        new_size = os.path.getsize(tmp_out)
        if new_size < os.path.getsize(path):
            os.replace(tmp_out, path)
        else:
            os.unlink(tmp_out)
    finally:
        if os.path.exists(png_path):
            os.unlink(png_path)
    return before, file_kb(path)


def compress_png(path: str) -> tuple[int, int]:
    before = file_kb(path)
    subprocess.run(['pngquant', '--quality=65-80', '--ext=.png', '--force',
                    '--skip-if-larger', '--strip', path], check=False)
    return before, file_kb(path)


def main() -> int:
    paths = sorted(glob.glob('images/*'))
    large = [p for p in paths if os.path.isfile(p) and os.path.getsize(p) > THRESHOLD_BYTES]
    if not large:
        print('No images >200 KB.')
        return 0
    print(f'Found {len(large)} images >200 KB. Compressing...\n')
    total_before = total_after = 0
    for p in large:
        ext = os.path.splitext(p)[1].lower()
        try:
            if ext == '.webp':
                before, after = compress_webp(p)
            elif ext == '.png':
                before, after = compress_png(p)
            else:
                continue
        except subprocess.CalledProcessError as e:
            print(f'  FAIL {p}: {e}')
            continue
        total_before += before
        total_after += after
        marker = '✓' if after <= 200 else '⚠'
        print(f'  {marker}  {p}  {before}K → {after}K')
    print()
    print(f'Total: {total_before}K → {total_after}K  (saved {total_before-total_after}K)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
