#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261119 bounty (v2 entry).

Writes the finished front page for Thursday 19 November 2026 to
$MAKEFUN_OUTPUT_DIR/entry.png. The image was drawn in-session by
build_image.py (Pillow, local build tool) from 40 verified stories:
a dense newspaper front page rebuilt around a drawn world map with
numbered markers keyed to the 8 biggest stories.

This entrypoint is stdlib-only and deterministic: it copies the same
bytes on every run, with no network access and no timestamps.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if size > 1048576:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
