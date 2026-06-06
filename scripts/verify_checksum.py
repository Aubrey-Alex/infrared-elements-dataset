#!/usr/bin/env python3
"""Verify a downloaded dataset archive against metadata/checksums.sha256."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_expected(checksums_path: Path, filename: str) -> str:
    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        digest, name = line.split(maxsplit=1)
        if Path(name).name == filename:
            return digest.lower()
    raise SystemExit(f"No checksum entry found for {filename!r} in {checksums_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path, help="Path to the downloaded zip archive.")
    parser.add_argument(
        "--checksums",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "metadata" / "checksums.sha256",
        help="Path to checksums.sha256.",
    )
    args = parser.parse_args()

    actual = sha256(args.archive)
    expected = load_expected(args.checksums, args.archive.name)

    if actual != expected:
        raise SystemExit(f"Checksum mismatch\nexpected: {expected}\nactual:   {actual}")

    print(f"OK: {args.archive} matches SHA256 {actual}")


if __name__ == "__main__":
    main()
