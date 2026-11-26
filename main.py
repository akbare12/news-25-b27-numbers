"""news-25-b27-numbers: copy the rendered front page to the output dir.

Stdlib only (os / shutil / sys). The image itself is rendered at build
time by gen.py (Pillow) and committed to this repo as entry.png; this
script only copies it into MAKEFUN_OUTPUT_DIR so the grader, which runs
with the standard library only, never needs Pillow.

Rules enforced here before copying:
  * entry.png must exist next to this file
  * entry.png must be at most 1024 x 1024 px and at most 1 MiB
    (checked by reading the PNG header with the stdlib only)
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG file using only the stdlib."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        raise ValueError("file too short to be a PNG")
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError("missing PNG IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1

    try:
        width, height = png_size(src)
    except ValueError as exc:
        print("entry.png failed PNG check: %s" % exc, file=sys.stderr)
        return 1

    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png is %dx%d, over the 1024x1024 limit"
              % (width, height), file=sys.stderr)
        return 1

    print("entry.png: %dx%d, %d bytes" % (width, height, size))
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote %s" % dst)

    if os.path.getsize(dst) != size:
        print("output size mismatch after copy", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
