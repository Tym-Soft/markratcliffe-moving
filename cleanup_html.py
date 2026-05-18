#!/usr/bin/env python3
"""Strip dead/unused HTML across the site:
 - Empty elfsight widget containers (script already removed)
 - SHARE: + w-embed wrapper if it only contained elfsight
 - "Copyright" Webflow comment label
 - Developer notes (HTML comments I left while building)
 - Strip leading/trailing whitespace
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "www.markratcliffemoving.co.uk"


def clean_file(fp: Path) -> dict:
    text = fp.read_text(encoding="utf-8")
    orig = text
    changes = []

    # 1) Remove the entire "SHARE: ... elfsight" block. Pattern is:
    #    <div>SHARE:</div>\n  <div class="w-embed w-script">...elfsight-app...</div>
    # Some original pages also include this as a list item; match the whole share unit.
    share_pattern = re.compile(
        r'<div>SHARE:</div>\s*<div class="w-embed w-script">\s*<div class="elfsight-app[^"]*"[^>]*></div>\s*</div>',
        re.S
    )
    if share_pattern.search(text):
        text = share_pattern.sub('', text)
        changes.append("strip-share-elfsight")

    # 2) Standalone empty elfsight div (no share label)
    elfsight_solo = re.compile(
        r'<div class="elfsight-app[^"]*"[^>]*></div>\s*',
        re.S
    )
    if elfsight_solo.search(text):
        text = elfsight_solo.sub('', text)
        changes.append("strip-elfsight-div")

    # 3) Empty w-embed w-script wrappers left behind
    empty_embed = re.compile(
        r'<div class="w-embed w-script">\s*</div>\s*',
        re.S
    )
    if empty_embed.search(text):
        text = empty_embed.sub('', text)
        changes.append("strip-empty-embed")

    # 4) Webflow "Copyright" comment label
    if "<!--  Copyright  -->" in text:
        text = text.replace("<!--  Copyright  -->", "")
        changes.append("strip-copyright-comment")

    # 5) Developer notes I left during builds
    dev_comments = [
        "<!-- Why our removal service is different -->",
    ]
    for c in dev_comments:
        if c in text:
            text = text.replace(c, "")
            changes.append("strip-dev-comment")

    # 6) Collapse runs of 3+ blank lines to a max of 1
    text2 = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', text)
    if text2 != text:
        text = text2
        changes.append("collapse-blank-lines")

    if text != orig:
        fp.write_text(text, encoding="utf-8")
    return {"file": str(fp.relative_to(ROOT)), "changes": changes}


def main():
    files = list(ROOT.rglob("*.html"))
    stats = {}
    changed = 0
    for fp in files:
        r = clean_file(fp)
        if r["changes"]:
            changed += 1
            for c in r["changes"]:
                stats[c] = stats.get(c, 0) + 1
    print(f"Cleaned {changed} of {len(files)} files.")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
