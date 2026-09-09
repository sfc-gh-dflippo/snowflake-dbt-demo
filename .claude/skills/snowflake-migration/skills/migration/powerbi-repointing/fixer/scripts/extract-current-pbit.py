#!/usr/bin/env python3
"""
Extract current PBIT file info from inventory for processing.
Usage: python extract_current_pbit.py <pbit_filename>
"""

import json
import os
import sys
import tempfile

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
CURRENT_PBIT_JSON = os.path.join(_BASE_DIR, "current_pbit.json")
INVENTORY_JSON = os.path.join(_BASE_DIR, "pbit_inventory.json")


def extract_current_pbit(pbit_filename):
    """Extract current PBIT info from inventory."""
    
    # Load inventory
    with open(INVENTORY_JSON, 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    # Find matching PBIT file
    current = None
    for item in inventory:
        if item['pbit_file'] == pbit_filename:
            current = item
            break
    
    if not current:
        print(f"Error: PBIT file '{pbit_filename}' not found in inventory")
        sys.exit(1)
    
    # Save to temporary file for processing
    with open(CURRENT_PBIT_JSON, 'w', encoding='utf-8') as f:
        json.dump(current, f, indent=2)
    
    print(f"Extracted info for: {pbit_filename}")
    print(f"Unsupported queries: {len(current['unsupported_queries'])}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_current_pbit.py <pbit_filename>")
        sys.exit(1)
    
    pbit_filename = sys.argv[1]
    extract_current_pbit(pbit_filename)


if __name__ == '__main__':
    main()
