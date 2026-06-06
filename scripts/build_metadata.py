#!/usr/bin/env python3
"""Build manifest, per-file checksums, and aggregate statistics."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_parts(relative_path: Path) -> tuple[str, str, str]:
    parts = relative_path.parts
    subset = parts[0]

    if len(parts) >= 3 and parts[1] in {"infrared", "visual"}:
        category = ""
        modality = parts[1]
    elif len(parts) >= 4:
        category = parts[1]
        modality = parts[2]
    else:
        category = ""
        modality = ""

    return subset, category, modality


def build(source: Path, output: Path) -> None:
    images = sorted(source.rglob("*.png"))
    if not images:
        raise SystemExit(f"No PNG files found under {source}")

    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.csv"
    checksums_path = output / "file_checksums.sha256"
    statistics_path = output / "statistics.json"

    total_bytes = 0
    subset_counts: Counter[str] = Counter()
    modality_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    subset_detail: dict[str, Counter[str]] = defaultdict(Counter)

    with manifest_path.open("w", newline="", encoding="utf-8") as manifest_handle, checksums_path.open(
        "w", encoding="utf-8"
    ) as checksum_handle:
        writer = csv.DictWriter(
            manifest_handle,
            fieldnames=[
                "path",
                "subset",
                "category",
                "modality",
                "filename",
                "width",
                "height",
                "mode",
                "bytes",
                "sha256",
            ],
        )
        writer.writeheader()

        for path in images:
            rel = path.relative_to(source).as_posix()
            subset, category, modality = classify_parts(Path(rel))
            size = path.stat().st_size
            digest = sha256(path)

            with Image.open(path) as image:
                width, height = image.size
                mode = image.mode

            writer.writerow(
                {
                    "path": rel,
                    "subset": subset,
                    "category": category,
                    "modality": modality,
                    "filename": path.name,
                    "width": width,
                    "height": height,
                    "mode": mode,
                    "bytes": size,
                    "sha256": digest,
                }
            )
            checksum_handle.write(f"{digest}  {rel}\n")

            total_bytes += size
            subset_counts[subset] += 1
            if modality:
                modality_counts[modality] += 1
                subset_detail[subset][modality] += 1
            if category:
                category_counts[category] += 1

    statistics = {
        "source_root": source.name,
        "image_format": "PNG",
        "total_images": len(images),
        "total_bytes": total_bytes,
        "total_mib": round(total_bytes / (1024 * 1024), 2),
        "subsets": dict(sorted(subset_counts.items())),
        "modalities": dict(sorted(modality_counts.items())),
        "categories": dict(sorted(category_counts.items())),
        "subset_modalities": {key: dict(sorted(value.items())) for key, value in sorted(subset_detail.items())},
    }
    statistics_path.write_text(json.dumps(statistics, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {manifest_path}")
    print(f"Wrote {checksums_path}")
    print(f"Wrote {statistics_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Dataset source root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "metadata",
        help="Metadata output directory.",
    )
    args = parser.parse_args()
    build(args.source, args.output)


if __name__ == "__main__":
    main()
