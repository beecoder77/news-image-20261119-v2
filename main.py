"""Front-page delivery for the 19 November news-image entry.

The finished page already exists in this folder as entry.png. This
small program only carries those exact bytes to the folder the
platform asks for, then reads the copy back and checks it matches,
so the picture that gets submitted is bit-for-bit the one we built.
"""

import pathlib
import struct

PNG_MARK = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
HEADER_LEN = 24


def front_page_path():
    """Where the finished picture lives, next to this program."""
    return pathlib.Path(__file__).resolve().parent / "entry.png"


def output_folder():
    """Folder named by the platform, falling back to ./out."""
    wanted = pathlib.os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    return pathlib.Path(wanted)


def check_picture(payload):
    """Refuse anything that is not a small, well-formed PNG."""
    if not payload.startswith(PNG_MARK):
        raise SystemExit("error: entry.png does not start with the PNG signature")
    if len(payload) > MAX_BYTES:
        raise SystemExit(f"error: entry.png is {len(payload)} bytes, over the 1048576 byte limit")
    if len(payload) < HEADER_LEN or payload[12:16] != b"IHDR":
        raise SystemExit("error: entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", payload[16:24])
    if width == 0 or height == 0:
        raise SystemExit("error: entry.png has a zero dimension")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"error: entry.png is {width}x{height}, over the 1024x1024 limit")


def deliver():
    """Copy the picture, verify the copy, and confirm in one line."""
    origin = front_page_path()
    try:
        payload = origin.read_bytes()
    except FileNotFoundError:
        raise SystemExit("error: entry.png is missing beside main.py") from None
    except OSError as trouble:
        raise SystemExit(f"error: cannot read entry.png: {trouble}") from None
    check_picture(payload)
    folder = output_folder()
    try:
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / "entry.png"
        target.write_bytes(payload)
        echoed = target.read_bytes()
    except OSError as trouble:
        raise SystemExit(f"error: cannot write output: {trouble}") from None
    if echoed != payload:
        raise SystemExit("error: output bytes do not match entry.png")
    print(f"Wrote {target} ({len(payload)} bytes)")
    return 0


raise SystemExit(deliver())
