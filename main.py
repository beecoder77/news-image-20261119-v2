"""Ship the finished front page to the make.fun output folder.

The artwork itself lives next to this script as ``entry.png``.  This
module's only job is to place an exact copy of that file where the
judge expects it and then prove the copy is a usable PNG: right
magic bytes, small enough, and no bigger than the allowed canvas.
Everything here is plain standard library, and nothing about the
run depends on the clock or the network, so repeated runs produce
identical bytes.
"""

import os
import struct
import sys
from pathlib import Path

# The eight bytes every PNG file starts with.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# Limits from the competition kit, in bytes and pixels.
BYTE_LIMIT = 1_048_576
EDGE_LIMIT = 1024


def fail(reason):
    """Report a problem on stderr and stop with a failing status."""
    print(f"entrypoint failed: {reason}", file=sys.stderr)
    return 1


def canvas_size(blob):
    """Pull (width, height) out of a PNG's IHDR chunk.

    The chunk layout is fixed: an 8-byte signature, then a 4-byte
    length, the four letters ``IHDR``, and then width and height as
    two big-endian unsigned 32-bit numbers.
    """
    if len(blob) < 24:
        raise ValueError("file is too short to hold a PNG header")
    if blob[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR, not a normal PNG")
    wide, tall = struct.unpack(">II", blob[16:24])
    return wide, tall


def run():
    here = Path(__file__).resolve().parent
    artwork = here / "entry.png"

    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / "entry.png"

    try:
        picture_bytes = artwork.read_bytes()
    except OSError as exc:
        return fail(f"could not read {artwork}: {exc}")

    try:
        destination.write_bytes(picture_bytes)
    except OSError as exc:
        return fail(f"could not write {destination}: {exc}")

    try:
        delivered = destination.read_bytes()
    except OSError as exc:
        return fail(f"could not read back {destination}: {exc}")

    if delivered != picture_bytes:
        return fail("output bytes differ from the source artwork")

    if len(delivered) > BYTE_LIMIT:
        return fail(
            f"output is {len(delivered)} bytes, over the "
            f"{BYTE_LIMIT} byte limit"
        )

    if delivered[:8] != PNG_MAGIC:
        return fail("output does not start with the PNG signature")

    try:
        wide, tall = canvas_size(delivered)
    except ValueError as exc:
        return fail(str(exc))

    if wide > EDGE_LIMIT or tall > EDGE_LIMIT:
        return fail(
            f"canvas is {wide}x{tall}, over the {EDGE_LIMIT}x{EDGE_LIMIT} limit"
        )

    print(f"Wrote {destination} ({len(delivered)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
