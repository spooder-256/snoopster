"""Turn a GIF into frames.json (coloured ASCII). Run once on your computer:

    pip install pillow
    python convert.py source.gif frames.json [columns]
"""
import json
import sys

from PIL import Image, ImageSequence

CW, CH = 8, 14                 # character cell size used by the page (px)
RAMP = " .:-=+*#%@"            # dark -> bright
BOOST = 1.3                    # colours pop more on a black background


def convert(src, out, cols=110):
    im = Image.open(src)
    w, h = im.size
    rows = round(cols * h / w * CW / CH)
    frames, delays = [], []
    for fr in ImageSequence.Iterator(im):
        delays.append(fr.info.get("duration", 70) or 70)
        rgb = fr.convert("RGB").resize((cols, rows), Image.BOX)
        text, colour = [], []
        for y in range(rows):
            line = ""
            for x in range(cols):
                r, g, b = rgb.getpixel((x, y))
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                line += RAMP[min(len(RAMP) - 1, int(lum ** 0.8 * len(RAMP)))]
                colour.append("".join("%x" % min(15, int(min(255, v * BOOST) / 17)) for v in (r, g, b)))
            text.append(line)
        frames.append({"t": "\n".join(text), "c": "".join(colour)})
    with open(out, "w") as f:
        json.dump({"cols": cols, "rows": rows, "cw": CW, "ch": CH, "delays": delays, "frames": frames}, f, separators=(",", ":"))
    print(f"{len(frames)} frames, {cols}x{rows} characters -> {out}")


if __name__ == "__main__":
    a = sys.argv
    convert(a[1] if len(a) > 1 else "source.gif", a[2] if len(a) > 2 else "frames.json", int(a[3]) if len(a) > 3 else 110)
