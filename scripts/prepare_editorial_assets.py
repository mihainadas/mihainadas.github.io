"""Encode editorial artwork as responsive WebP; keep image content unchanged."""

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("name", choices=("structure", "signal"))
    args = parser.parse_args()
    destination = Path(__file__).resolve().parents[1] / "assets" / "editorial"
    destination.mkdir(parents=True, exist_ok=True)
    with Image.open(args.source) as original:
        for width in (480, 960, 1440):
            size = (width, round(original.height * width / original.width))
            image = original.convert("RGB").resize(size, Image.Resampling.LANCZOS)
            path = destination / f"{args.name}-{width}.webp"
            image.save(path, "WEBP", quality=82, method=6)
            print(f"{path.name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
