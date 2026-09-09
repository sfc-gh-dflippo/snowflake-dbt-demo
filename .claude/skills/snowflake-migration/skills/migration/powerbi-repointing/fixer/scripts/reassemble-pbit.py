#!/usr/bin/env python3
"""
Reassemble PBIT file from working directory and replace original.
Usage: python reassemble_pbit.py <original_pbit_path> <work_dir>
"""

import json
import os
import shutil
import sys
import tempfile
import zipfile

from _console import OK

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
REASSEMBLE_RESULTS_JSON = os.path.join(_BASE_DIR, "reassemble_results.json")


def reassemble_pbit(original_path, work_dir):
    """Reassemble PBIT and replace SnowConvert output with backup."""
    
    # Back up original SnowConvert output (optional but recommended)
    backup_path = original_path + '.backup'
    if not os.path.exists(backup_path):
        shutil.copyfile(original_path, backup_path)
        print(f"  Backup created: {backup_path}")
    else:
        print(f"  Using existing backup: {backup_path}")
    
    # Replace SnowConvert output with updated version
    with zipfile.ZipFile(original_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(work_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, work_dir)
                zipf.write(file_path, arcname)
    
    print(f"{OK} Updated: {original_path}")
    
    return backup_path


def main():
    if len(sys.argv) != 3:
        print("Usage: python reassemble_pbit.py <original_pbit_path> <work_dir>")
        sys.exit(1)
    
    original_path = sys.argv[1]
    work_dir = sys.argv[2]
    
    if not os.path.exists(original_path):
        print(f"Error: Original PBIT not found: {original_path}")
        sys.exit(1)
    
    if not os.path.exists(work_dir):
        print(f"Error: Work directory not found: {work_dir}")
        sys.exit(1)
    
    backup_path = reassemble_pbit(original_path, work_dir)
    
    with open(REASSEMBLE_RESULTS_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'original_path': original_path,
            'backup_path': backup_path
        }, f, indent=2)


if __name__ == '__main__':
    main()
