#!/usr/bin/env python3
"""Extract a PBIT file (ZIP archive) to the working directory."""

import os
import sys
import tempfile
import zipfile

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
WORK_DIR = os.path.join(_BASE_DIR, "work")


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract-pbit.py <pbit_path>")
        sys.exit(1)

    pbit_path = sys.argv[1]
    if not os.path.exists(pbit_path):
        print(f"Error: PBIT file not found: {pbit_path}")
        sys.exit(1)

    os.makedirs(WORK_DIR, exist_ok=True)

    with zipfile.ZipFile(pbit_path, "r") as zf:
        for member in zf.namelist():
            target = os.path.realpath(os.path.join(WORK_DIR, member))
            if not target.startswith(os.path.realpath(WORK_DIR)):
                print(f"Error: ZIP entry escapes target directory: {member}")
                sys.exit(1)
        zf.extractall(WORK_DIR)

    print(f"Extracted: {pbit_path} -> {WORK_DIR}")
    extracted = os.listdir(WORK_DIR)
    print(f"Contents: {', '.join(sorted(extracted))}")


if __name__ == "__main__":
    main()
