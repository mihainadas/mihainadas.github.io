"""Regenerate the default social preview with Pillow and an installed TrueType font."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", required=True, help="Path to an installed sans-serif font")
    args = parser.parse_args()
    image = Image.new("RGB", (1200, 630), "#f7f4ec")
    draw = ImageDraw.Draw(image)
    ink, muted, accent = "#171b1c", "#4e5855", "#855708"
    font = lambda size: ImageFont.truetype(args.font, size)
    draw.text((72, 62), "Mihai Nadăș / field notes", fill=accent, font=font(30))
    draw.line((72, 133, 1128, 133), fill="#b8b1a2", width=2)
    draw.text((72, 198), "Staying close to", fill=ink, font=font(72))
    draw.text((72, 286), "the implementation.", fill=ink, font=font(72))
    draw.text((76, 452), "Engineering · AI research · Applied papers", fill=muted, font=font(29))
    draw.text((76, 544), "mihainadas.github.io", fill=accent, font=font(25))
    image.save(Path(__file__).resolve().parents[1] / "assets" / "social-card.png", optimize=True)


if __name__ == "__main__":
    main()
