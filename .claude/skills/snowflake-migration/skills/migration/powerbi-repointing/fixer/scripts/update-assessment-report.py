#!/usr/bin/env python3
"""
Update assessment report with skill results.
Copies the ETLAndBiRepointing report to output folder and updates query statuses:
- "Unsupported" -> "AI Repointed" if the query was successfully translated
- "Unsupported" remains if translation failed

Usage: python update-assessment-report.py <assessment_csv> <translated_queries_json> <output_folder>
"""

import csv
import json
import os
import sys
import tempfile

from _console import OK
from pathlib import Path

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
ASSESSMENT_UPDATE_SUMMARY_JSON = os.path.join(_BASE_DIR, "assessment_update_summary.json")


def update_assessment_report(assessment_csv, translated_queries_json, output_folder):
    """Update assessment report with translation results."""
    
    # Load translation results
    with open(translated_queries_json, 'r', encoding='utf-8') as f:
        translated_queries = json.load(f)
    
    # Build a set of successfully translated query names
    successfully_translated = set()
    failed_queries = set()
    
    for query in translated_queries:
        query_name = query['query_name']
        status = query.get('translation_status', 'pending')
        
        if status == 'completed':
            successfully_translated.add(query_name)
        else:
            failed_queries.add(query_name)
    
    print(f"  Successfully translated: {len(successfully_translated)} queries")
    if failed_queries:
        print(f"  Failed translations: {len(failed_queries)} queries")
    
    # Read original assessment report
    with open(assessment_csv, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # Update statuses
    updated_count = 0
    for row in rows:
        query_name = row.get('FullName', '')
        current_status = row.get('Status', '')
        
        # Only update "Unsupported" queries that were successfully translated
        if current_status == 'Unsupported' and query_name in successfully_translated:
            row['Status'] = 'AI Repointed'
            row['ContainsSQL'] = 'Yes'
            row['PendingWork'] = 'No'
            row['Pending Work Description'] = 'Query successfully translated to Snowflake by SCAI PowerBI Fixer.'
            updated_count += 1
            print(f"  {OK} Updated: {query_name} -> AI Repointed")
    
    # Write updated report to output folder
    output_csv = os.path.join(output_folder, os.path.basename(assessment_csv))
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n{OK} Assessment report updated: {updated_count} queries marked as 'AI Repointed'")
    print(f"  Output: {output_csv}")
    
    # Save summary for reference
    summary = {
        'original_assessment': assessment_csv,
        'output_assessment': output_csv,
        'successfully_translated': list(successfully_translated),
        'failed_queries': list(failed_queries),
        'updated_count': updated_count
    }
    
    summary_path = ASSESSMENT_UPDATE_SUMMARY_JSON
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    return updated_count


def main():
    if len(sys.argv) != 4:
        print("Usage: python update-assessment-report.py <assessment_csv> <translated_queries_json> <output_folder>")
        sys.exit(1)
    
    assessment_csv = sys.argv[1]
    translated_queries_json = sys.argv[2]
    output_folder = sys.argv[3]
    
    if not os.path.exists(assessment_csv):
        print(f"Error: Assessment report not found: {assessment_csv}")
        sys.exit(1)
    
    if not os.path.exists(translated_queries_json):
        print(f"Error: Translated queries file not found: {translated_queries_json}")
        sys.exit(1)
    
    # Create output folder if needed
    os.makedirs(output_folder, exist_ok=True)
    
    update_assessment_report(assessment_csv, translated_queries_json, output_folder)


if __name__ == '__main__':
    main()
