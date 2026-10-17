"""Trim the raw lockup renders, add clear space, size to 2000 px wide.

Run after make_lockups.mjs. Clear space on every side is ~12% of the
lockup height (about the llama's head width). Raw renders are deleted.
"""
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "llama/logos"
W = 2000

for raw in sorted(OUT.glob("raw-lockup-*.png")):
    im = Image.open(raw).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    pad = round(im.height * 0.12)
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    canvas.alpha_composite(im, (pad, pad))
    canvas = canvas.resize((W, round(canvas.height * W / canvas.width)), Image.LANCZOS)
    name = raw.name.replace("raw-lockup-", "llama-lockup-").replace(".png", f"-{W}w.png")
    canvas.save(OUT / name)
    raw.unlink()
    print(name, canvas.size)
