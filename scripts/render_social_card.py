"""Regenerate the editorial social preview with Pillow and TrueType fonts."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", required=True, help="Path to an installed sans-serif font")
    parser.add_argument("--display-font", help="Path to the Newsreader regular TrueType source")
    parser.add_argument("--italic-font", help="Path to the Newsreader italic TrueType source")
    args = parser.parse_args()
    image = Image.new("RGB", (1200, 630), "#f7f4ec")
    draw = ImageDraw.Draw(image)
    ink, muted, accent = "#171b1c", "#4e5855", "#ac3b25"
    def font(size: int):
        result = ImageFont.truetype(args.font, size)
        try:
            axes = result.get_variation_axes()
        except OSError:
            return result
        result.set_variation_by_axes([
            500 if axis["name"] == b"Weight" else axis["default"] for axis in axes
        ])
        return result
    display = lambda size: ImageFont.truetype(args.display_font or args.font, size)
    italic = lambda size: ImageFont.truetype(args.italic_font or args.display_font or args.font, size)
    artwork = Path(__file__).resolve().parents[1] / "assets/editorial/structure-1440.webp"
    with Image.open(artwork) as source:
        image.paste(ImageOps.fit(source, (490, 630), centering=(0.56, 0.5)), (710, 0))
    draw.rectangle((0, 0, 1200, 4), fill=ink)
    draw.text((60, 55), "Mihai Nadăș / field notes", fill=accent, font=font(25))
    draw.line((60, 111, 650, 111), fill="#b8b1a2", width=1)
    draw.text((60, 166), "Staying close", fill=ink, font=display(78))
    draw.text((60, 251), "to the", fill=ink, font=display(78))
    draw.text((60, 336), "implementation.", fill=accent, font=italic(78))
    draw.text((62, 475), "Engineering · AI research", fill=muted, font=font(23))
    draw.text((62, 514), "Applied papers", fill=muted, font=font(23))
    draw.text((62, 568), "mihainadas.github.io", fill=accent, font=font(20))
    image.save(Path(__file__).resolve().parents[1] / "assets" / "social-card.png", optimize=True)


if __name__ == "__main__":
    main()
