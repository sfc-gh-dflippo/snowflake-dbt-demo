#!/usr/bin/env python3
"""Verify the reassembled PBIT file is a valid ZIP archive."""

import os
import sys
import zipfile


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify-output.py <pbit_path>")
        sys.exit(1)

    pbit_path = sys.argv[1]
    if not os.path.exists(pbit_path):
        print(f"Error: PBIT file not found: {pbit_path}")
        sys.exit(1)

    if not zipfile.is_zipfile(pbit_path):
        print(f"FAILED: {pbit_path} is not a valid ZIP/PBIT file")
        sys.exit(1)

    with zipfile.ZipFile(pbit_path, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            print(f"FAILED: Corrupt entry in PBIT: {bad}")
            sys.exit(1)
        entries = zf.namelist()

    has_datamodel = "DataModelSchema" in entries
    print(f"Valid PBIT: {pbit_path}")
    print(f"  Entries: {len(entries)}")
    print(f"  DataModelSchema: {'present' if has_datamodel else 'MISSING'}")

    if not has_datamodel:
        print("WARNING: DataModelSchema not found in PBIT")
        sys.exit(1)


if __name__ == "__main__":
    main()
