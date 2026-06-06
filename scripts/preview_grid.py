#!/usr/bin/env python3
"""Create a preview image grid from a local extracted dataset directory."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from PIL import Image, ImageOps


def make_grid(paths: list[Path], output: Path, tile_size: int, columns: int) -> None:
    rows = (len(paths) + columns - 1) // columns
    grid = Image.new("RGB", (columns * tile_size, rows * tile_size), "white")

    for index, path in enumerate(paths):
        with Image.open(path) as image:
            tile = ImageOps.contain(image.convert("RGBA"), (tile_size, tile_size))
        canvas = Image.new("RGBA", (tile_size, tile_size), (255, 255, 255, 255))
        x = (index % columns) * tile_size + (tile_size - tile.width) // 2
        y = (index // columns) * tile_size + (tile_size - tile.height) // 2
        canvas.alpha_composite(tile, ((tile_size - tile.width) // 2, (tile_size - tile.height) // 2))
        grid.paste(canvas.convert("RGB"), ((index % columns) * tile_size, (index // columns) * tile_size))

    output.parent.mkdir(parents=True, exist_ok=True)
    grid.save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_root", type=Path, help="Extracted dataset root.")
    parser.add_argument("--output", type=Path, default=Path("samples") / "preview_grid.png")
    parser.add_argument("--count", type=int, default=36)
    parser.add_argument("--tile-size", type=int, default=128)
    parser.add_argument("--columns", type=int, default=6)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--object-only",
        action="store_true",
        help="Use only extracted person/vehicle primitive directories.",
    )
    parser.add_argument(
        "--ir-only",
        action="store_true",
        help="Use only infrared extracted primitive directories.",
    )
    args = parser.parse_args()

    if args.ir_only:
        images = []
        for pattern in ("person/ir/*.png", "vehicle/ir/*.png"):
            images.extend(args.dataset_root.rglob(pattern))
        images = sorted(images)
    elif args.object_only:
        images = []
        for pattern in ("person/ir/*.png", "person/rgb/*.png", "vehicle/ir/*.png", "vehicle/rgb/*.png"):
            images.extend(args.dataset_root.rglob(pattern))
        images = sorted(images)
    else:
        images = sorted(args.dataset_root.rglob("*.png"))
    if not images:
        raise SystemExit(f"No PNG images found under {args.dataset_root}")

    random.seed(args.seed)
    selected = random.sample(images, min(args.count, len(images)))
    make_grid(selected, args.output, args.tile_size, args.columns)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
