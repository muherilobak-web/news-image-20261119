#!/usr/bin/env python3
"""Entry program for news-image-20261119.

Copies the front-page image this repository holds (entry.png) to the
output directory, byte for byte. Standard library only, no network, no
randomness, no timestamps: two runs write identical bytes.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        sys.exit("entry.png not found next to main.py")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # A pure copy must be byte-identical: same size is the cheap check.
    if os.path.getsize(dst) != os.path.getsize(src):
        sys.exit("copied entry.png differs in size from the source")
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
