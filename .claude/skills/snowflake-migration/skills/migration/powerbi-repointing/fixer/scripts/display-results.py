#!/usr/bin/env python3
"""
Display conversion results after processing a PBIT file.
Usage: python display_results.py
"""

import json
import os
import sys
import tempfile

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
CONVERSION_RESULTS_JSON = os.path.join(_BASE_DIR, "conversion_results.json")
REASSEMBLE_RESULTS_JSON = os.path.join(_BASE_DIR, "reassemble_results.json")


def display_results():
    """Display conversion and reassembly results."""
    
    try:
        # Load conversion results
        with open(CONVERSION_RESULTS_JSON, 'r', encoding='utf-8') as f:
            results = json.load(f)

        # Load reassembly results
        with open(REASSEMBLE_RESULTS_JSON, 'r', encoding='utf-8') as f:
            reassemble = json.load(f)
        
        # Display formatted results
        print(f"Converted: {results['converted_count']}, Failed: {len(results['failed_queries'])}")
        print(f"Updated: {reassemble['original_path']}")
        print(f"Backup: {reassemble['backup_path']}")
        
        # Return appropriate exit code
        return 0 if results['success'] else 1
        
    except FileNotFoundError as e:
        print(f"Error: Results file not found - {e}")
        return 1
    except Exception as e:
        print(f"Error reading results: {e}")
        return 1


def main():
    sys.exit(display_results())


if __name__ == '__main__':
    main()
