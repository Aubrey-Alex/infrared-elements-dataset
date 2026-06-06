#!/usr/bin/env python3
"""Create a side-by-side preview panel for extracted object primitives."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PAIR_SPECS = [
    (
        "filtered_dataset_20210418_test02",
        "person/ir",
        "person/rgb",
        "20210418_test02_pair_00417_avi[000461]_mp4[000348]_obj2_person.png",
    ),
    (
        "filtered_dataset_20210418_test02",
        "person/ir",
        "person/rgb",
        "20210418_test02_pair_00429_avi[000473]_mp4[000358]_obj3_person.png",
    ),
    (
        "filtered_dataset_20210418_test01",
        "vehicle/ir",
        "vehicle/rgb",
        "20210418_test01_pair_00028_avi[000029]_mp4[000024]_obj5_vehicle.png",
    ),
    (
        "filtered_dataset_202304131400",
        "vehicle/ir",
        "vehicle/rgb",
        "202304131400_pair_00200_avi[000201]_mp4[000201]_obj5_vehicle.png",
    ),
]


def first_pair(dataset_root: Path, subset: str, left_dir: str, right_dir: str, preferred: str) -> tuple[Path, Path]:
    left_root = dataset_root / subset / left_dir
    right_root = dataset_root / subset / right_dir
    preferred_left = left_root / preferred
    preferred_right = right_root / preferred
    if preferred_left.exists() and preferred_right.exists():
        return preferred_left, preferred_right

    for left in sorted(left_root.glob("*.png")):
        right = right_root / left.name
        if right.exists():
            return left, right

    raise SystemExit(f"No paired PNG files found for {subset}: {left_dir} and {right_dir}")


def fit_tile(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        tile = ImageOps.contain(image.convert("RGBA"), size)
    canvas = Image.new("RGBA", size, (255, 255, 255, 255))
    x = (size[0] - tile.width) // 2
    y = (size[1] - tile.height) // 2
    canvas.alpha_composite(tile, (x, y))
    return canvas.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_root", type=Path, help="Dataset source root.")
    parser.add_argument("--output", type=Path, default=Path("samples") / "preview" / "paired_examples.png")
    parser.add_argument("--tile-width", type=int, default=150)
    parser.add_argument("--tile-height", type=int, default=170)
    args = parser.parse_args()

    pairs = [first_pair(args.dataset_root, *spec) for spec in PAIR_SPECS]
    margin = 20
    label_h = 28
    gap = 18
    row_gap = 18
    tile_size = (args.tile_width, args.tile_height)
    width = margin * 2 + args.tile_width * 2 + gap
    height = margin * 2 + label_h + len(pairs) * args.tile_height + (len(pairs) - 1) * row_gap

    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((margin, margin), "Infrared / IR", fill=(30, 30, 30), font=font)
    draw.text((margin + args.tile_width + gap, margin), "Visible / RGB", fill=(30, 30, 30), font=font)

    y = margin + label_h
    for left, right in pairs:
        image.paste(fit_tile(left, tile_size), (margin, y))
        image.paste(fit_tile(right, tile_size), (margin + args.tile_width + gap, y))
        y += args.tile_height + row_gap

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
