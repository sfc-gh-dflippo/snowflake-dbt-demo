#!/usr/bin/env python3
"""
Prepare unsupported PowerQuery expressions for LLM translation.
This script extracts queries that need translation from both DataModelSchema
and UnappliedChanges files, and prepares them for LLM processing.

Usage: python prepare_queries_for_llm.py <datamodel_path> <pbit_info_json>
"""

import json
import os
import sys
import tempfile

from _console import OK, FAIL

_BASE_DIR = os.path.join(
    os.environ.get("SCAI_PROJECT_DIR", tempfile.gettempdir()),
    "artifacts", "pbit",
)
QUERIES_FOR_TRANSLATION_JSON = os.path.join(_BASE_DIR, "queries_for_translation.json")
TRANSLATED_QUERIES_JSON = os.path.join(_BASE_DIR, "translated_queries.json")


def is_parameter_definition(query_text):
    """Check if the query text is a parameter definition (should not be translated)."""
    return 'IsParameterQuery=true' in query_text


def prepare_queries_from_datamodel(datamodel_path, pbit_info):
    """Extract unsupported queries from DataModelSchema."""
    
    # Read DataModelSchema
    with open(datamodel_path, 'r', encoding='utf-16-le') as f:
        data = json.loads(f.read())
    
    queries_for_translation = []
    
    for query_info in pbit_info['unsupported_queries']:
        query_name = query_info['query_name']
        print(f"\n  Preparing query for LLM: {query_name}")
        
        # Find the query in model.tables[]
        query_table = None
        for table in data['model']['tables']:
            if table['name'] == query_name:
                query_table = table
                break
        
        if not query_table:
            print(f"  {FAIL} ERROR: Query '{query_name}' not found in DataModelSchema")
            continue

        # Get current expression
        partitions = query_table.get('partitions', [])
        if not partitions or 'source' not in partitions[0] or 'expression' not in partitions[0]['source']:
            print(f"  {FAIL} ERROR: Query '{query_name}' has no valid partition/source/expression")
            continue
        expression = partitions[0]['source']['expression']
        query_text = ''.join(expression) if isinstance(expression, list) else expression
        
        # Extract column names (top-level columns expected by Power BI)
        # These may differ from SQL column names due to Power Query transformations
        column_names = []
        if 'columns' in query_table:
            column_names = [col['name'] for col in query_table['columns']]
        
        # Prepare query for LLM translation
        query_for_llm = {
            'query_name': query_name,
            'source_file': 'DataModelSchema',
            'original_expression': expression,
            'original_text': query_text,
            'expected_columns': column_names,
            'translation_status': 'pending',
            'translated_expression': None
        }
        
        queries_for_translation.append(query_for_llm)
        print(f"  {OK} Query prepared: {query_name} ({len(column_names)} columns) [DataModelSchema]")
    
    return queries_for_translation


def prepare_queries_from_unapplied_changes(work_dir, pbit_info):
    """Extract unsupported queries from UnappliedChanges file (if it exists)."""
    
    unapplied_changes_path = os.path.join(work_dir, 'UnappliedChanges')
    
    if not os.path.exists(unapplied_changes_path):
        print("\n  UnappliedChanges file not found (skipping)")
        return []
    
    print("\n  Processing UnappliedChanges file...")
    
    # Read UnappliedChanges (UTF-16 LE encoded JSON)
    with open(unapplied_changes_path, 'r', encoding='utf-16-le') as f:
        data = json.loads(f.read())
    
    # Get list of unsupported query names from inventory
    unsupported_query_names = {q['query_name'] for q in pbit_info['unsupported_queries']}
    
    queries_for_translation = []
    
    for query in data.get('queries', []):
        query_name = query.get('name', '')
        query_text_list = query.get('text', [])
        query_text = ''.join(query_text_list)
        
        # Skip parameter definitions - they should remain unchanged
        if is_parameter_definition(query_text):
            continue
        
        # Check if this query is in the assessment's unsupported list (same query names in both files)
        if query_name in unsupported_query_names:
            print(f"\n  Preparing query for LLM: {query_name} [UnappliedChanges]")
            
            # Prepare query for LLM translation
            query_for_llm = {
                'query_name': query_name,
                'source_file': 'UnappliedChanges',
                'original_expression': query_text_list,
                'original_text': query_text,
                'expected_columns': [],  # UnappliedChanges doesn't have column definitions
                'translation_status': 'pending',
                'translated_expression': None
            }
            
            queries_for_translation.append(query_for_llm)
            print(f"  {OK} Query prepared: {query_name} [UnappliedChanges]")
    
    return queries_for_translation


def prepare_queries_for_llm(datamodel_path, pbit_info_json):
    """Extract unsupported queries and prepare them for LLM translation."""
    
    # Load PBIT file info
    with open(pbit_info_json, 'r', encoding='utf-8') as f:
        pbit_info = json.load(f)
    
    work_dir = os.path.dirname(datamodel_path)
    
    # Prepare queries from DataModelSchema
    queries_from_datamodel = prepare_queries_from_datamodel(datamodel_path, pbit_info)
    
    # Prepare queries from UnappliedChanges (if exists)
    queries_from_unapplied = prepare_queries_from_unapplied_changes(work_dir, pbit_info)
    
    # Combine all queries
    queries_for_translation = queries_from_datamodel + queries_from_unapplied
    
    # Save queries for LLM processing
    os.makedirs(os.path.dirname(QUERIES_FOR_TRANSLATION_JSON), exist_ok=True)
    with open(QUERIES_FOR_TRANSLATION_JSON, 'w', encoding='utf-8') as f:
        json.dump(queries_for_translation, f, indent=2)
    
    datamodel_count = len(queries_from_datamodel)
    unapplied_count = len(queries_from_unapplied)
    
    print(f"\n{OK} Prepared {len(queries_for_translation)} queries for LLM translation")
    print(f"  - DataModelSchema: {datamodel_count} queries")
    print(f"  - UnappliedChanges: {unapplied_count} queries")
    print(f"  Output: {QUERIES_FOR_TRANSLATION_JSON}")
    print(f"\nNext step: Process each query with LLM to translate PowerQuery expressions")
    print(f"  - Translate Sql.Database() to Snowflake.Databases()")
    print(f"  - Handle string concatenation with parameters")
    print(f"  - Apply SQL syntax translations")
    print(f"  - Use expected_columns to add Table.RenameColumns if casing differs")
    print(f"  - Save translations to {TRANSLATED_QUERIES_JSON}")
    
    return len(queries_for_translation)


def main():
    if len(sys.argv) != 3:
        print("Usage: python prepare_queries_for_llm.py <datamodel_path> <pbit_info_json>")
        sys.exit(1)
    
    datamodel_path = sys.argv[1]
    pbit_info_json = sys.argv[2]
    
    count = prepare_queries_for_llm(datamodel_path, pbit_info_json)
    
    if count > 0:
        sys.exit(0)
    else:
        print(f"\n{FAIL} No queries to prepare")
        sys.exit(1)


if __name__ == '__main__':
    main()
