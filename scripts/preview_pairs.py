#!/usr/bin/env python3
"""Create a side-by-side infrared and visible/RGB preview panel."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PAIR_SPECS = [
    ("202304131130_test01_filtered", "infrared", "visual", "frame_0300_obj_7_truck_bus.png"),
    (
        "filtered_dataset_20210418_test01",
        "person/ir",
        "person/rgb",
        "20210418_test01_pair_00010_avi[000011]_mp4[000011]_obj1_person.png",
    ),
    (
        "filtered_dataset_202304131400",
        "vehicle/ir",
        "vehicle/rgb",
        "202304131400_pair_00020_avi[000021]_mp4[000021]_obj5_vehicle.png",
    ),
    (
        "filtered_dataset_202304141211_test02",
        "vehicle/ir",
        "vehicle/rgb",
        "202304141211_test02_pair_03190_avi[003399]_mp4[002835]_obj2_vehicle.png",
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
        tile = ImageOps.contain(image.convert("RGB"), size)
    canvas = Image.new("RGB", size, (248, 248, 248))
    x = (size[0] - tile.width) // 2
    y = (size[1] - tile.height) // 2
    canvas.paste(tile, (x, y))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_root", type=Path, help="Dataset source root.")
    parser.add_argument("--output", type=Path, default=Path("samples") / "preview" / "paired_examples.png")
    parser.add_argument("--tile-width", type=int, default=220)
    parser.add_argument("--tile-height", type=int, default=150)
    args = parser.parse_args()

    pairs = [first_pair(args.dataset_root, *spec) for spec in PAIR_SPECS]
    margin = 24
    label_h = 34
    gap = 14
    row_gap = 22
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
