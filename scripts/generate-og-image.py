"""One-off: generate social preview PNG (X does not use SVG for cards)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = Path(__file__).resolve().parent.parent / "og-image.png"


def main() -> None:
    img = Image.new("RGB", (W, H), "#0f1115")
    draw = ImageDraw.Draw(img)

    # Simple gradient-like bands (no dependency on aggdraw)
    for y in range(H):
        t = y / (H - 1)
        r = int(15 + t * 8)
        g = int(17 + t * 10)
        b = int(21 + t * 12)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    margin = 80
    draw.rounded_rectangle(
        [margin, margin, W - margin, H - margin],
        radius=28,
        outline="#4f8cff",
        width=4,
    )
    inner = margin + 24
    draw.rounded_rectangle(
        [inner, inner, W - inner, H - inner],
        radius=20,
        fill="#111722",
    )

    # Play / film strip motif (left)
    ix, iy = 150, 200
    for j in range(3):
        draw.rounded_rectangle(
            [ix, iy + j * 50, ix + 26, iy + 26 + j * 50],
            radius=6,
            fill="#4f8cff",
        )
    draw.polygon(
        [(230, 200), (390, 280), (230, 360)],
        fill="#7bd389",
    )

    try:
        title_font = ImageFont.truetype("segoeui.ttf", 72)
        sub_font = ImageFont.truetype("segoeui.ttf", 32)
    except OSError:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    title = "Video Toolkit"
    sub1 = "In-browser video processing"
    sub2 = "No uploads — runs locally in your browser"

    draw.text((450, 210), title, fill="#e6e6e6", font=title_font)
    draw.text((450, 300), sub1, fill="#9aa3ad", font=sub_font)
    draw.text((450, 350), sub2, fill="#9aa3ad", font=sub_font)

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
