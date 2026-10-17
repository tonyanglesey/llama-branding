"""Build transparent llama marks + avatars from the flat white-bg export.

The mark is one flat color on white, so each pixel is a blend:
  p = a*C + (1-a)*255   ->   a = (255 - p) / (255 - C)
Solved on the blue channel (largest C-to-white range), which keeps the
anti-aliased edges. Then the mark is repainted with an exact brand color.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "logos/logo-1024-white-bg.png"
OUT = ROOT / "llama/logos"
TRIM = Path(__file__).with_name("llama-mark-trim.png")  # high-res input for make_lockups.mjs (gitignored)

OLIVE = (0x7D, 0x99, 0x44)
WHITE = (255, 255, 255)
BLACK = (0x0A, 0x0A, 0x0B)  # site near-black, not pure #000

src = Image.open(SRC).convert("RGB")
sampled_b = 0x61  # blue of the exported fill (#8ba161)
blue = src.getchannel("B")
alpha = blue.point(lambda b: max(0, min(255, round((255 - b) * 255 / (255 - sampled_b)))))
alpha = alpha.point(lambda v: 0 if v < 6 else v)  # drop compression speckle near white
bbox = alpha.getbbox()
alpha = alpha.crop(bbox)


def mark(color):
    img = Image.new("RGBA", alpha.size, color + (0,))
    img.putalpha(alpha)
    return img


def place(img, size, fill_ratio, bg=None):
    """Center img on a square canvas, its longest side = fill_ratio * size."""
    s = fill_ratio * size / max(img.size)
    m = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (bg + (255,)) if bg else (0, 0, 0, 0))
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


OUT.mkdir(parents=True, exist_ok=True)
mark(OLIVE).save(TRIM)

# Transparent marks: 80% fill leaves ~10% clear space each side.
for name, color in [("olive", OLIVE), ("white", WHITE), ("black", BLACK)]:
    place(mark(color), 1024, 0.80).save(OUT / f"llama-mark-{name}-1024.png")

# Profile pictures: 62% fill so a circle crop never clips the ears/feet.
place(mark(OLIVE), 1024, 0.62, bg=BLACK).save(OUT / "llama-avatar-olive-on-black-1024.png")
place(mark(OLIVE), 1024, 0.62, bg=WHITE).save(OUT / "llama-avatar-olive-on-white-1024.png")

print("bbox", bbox, "trim", alpha.size)
for p in sorted(OUT.glob("llama-*.png")):
    print(p.name)
