#!/usr/bin/env python3
"""Snapshot a unit directory into <unit>/stabilization/original.

Usage: python backup_unit.py <unit_dir>

Skips the stabilization/ sub-tree so the snapshot doesn't recurse into itself.
"""

import shutil
import sys
from pathlib import Path

from path_resolver import original_backup_dir, stabilization_root

STABILIZATION_FOLDER = "stabilization"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: backup_unit.py <unit_dir>", file=sys.stderr)
        return 2

    src = Path(sys.argv[1]).resolve()
    if not src.is_dir():
        print(f"Error: {src} is not a directory", file=sys.stderr)
        return 1

    dst = original_backup_dir(src)
    if dst.exists():
        # Fresh snapshot every time — the dest is a known scratch area.
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(STABILIZATION_FOLDER),
        dirs_exist_ok=True,
    )
    print(f"Snapshot saved to: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
