#!/usr/bin/env python3
"""Download the release archive for Infrared Elements Dataset."""

from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path


DEFAULT_URL = (
    "https://github.com/Aubrey-Alex/infrared-elements-dataset/releases/download/"
    "v1.0.0/infrared-elements-v1.0.0.zip"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL, help="Release asset URL.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data") / "infrared-elements-v1.0.0.zip",
        help="Output archive path.",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {args.url}")
    print(f"Writing {args.output}")
    urllib.request.urlretrieve(args.url, args.output)
    print("Done")


if __name__ == "__main__":
    main()
