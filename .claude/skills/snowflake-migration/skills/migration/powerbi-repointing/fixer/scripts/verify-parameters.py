#!/usr/bin/env python3
"""
Verify SF_* parameters exist in PBIT DataModelSchema and UnappliedChanges.
If SF_ROLE is not present, it will be auto-injected.
Usage: python verify_parameters.py <datamodel_path>
"""

import json
import os
import sys

from _console import OK


# SF_ROLE parameter definition for DataModelSchema (model.expressions[])
# NOTE: Uses null default (not empty string) so the parameter is null when not provided.
# This allows direct use of SF_ROLE in [Role = SF_ROLE] without conditional logic.
SF_ROLE_DATAMODEL_DEFINITION = {
    "name": "SF_ROLE",
    "description": "Optional Snowflake role to use for the connection. Leave null to use your default role.",
    "kind": "m",
    "expression": "null meta [IsParameterQuery=true, Type=\"Any\", IsParameterQueryRequired=false]",
    "lineageTag": "33a7ccce-7ab5-49f3-8766-ef3dc7a10469",
    "annotations": [
        {"name": "PBI_NavigationStepName", "value": "Navigation"},
        {"name": "PBI_ResultType", "value": "Any"}
    ]
}

# SF_ROLE parameter definition for UnappliedChanges (queries[])
# NOTE: Uses null default (not empty string) so the parameter is null when not provided.
SF_ROLE_UNAPPLIED_DEFINITION = {
    "name": "SF_ROLE",
    "lineageTag": "33a7ccce-7ab5-49f3-8766-ef3dc7a10469",
    "description": "Optional Snowflake role to use for the connection. Leave null to use your default role.",
    "navigationStepName": "Navigation",
    "text": ["null meta [IsParameterQuery=true, Type=\"Any\", IsParameterQueryRequired=false]"],
    "loadAsTableDisabled": True,
    "resultType": "Any"
}


def verify_parameters_in_datamodel(datamodel_path):
    """Verify that required SF_* parameters exist in DataModelSchema.
    Auto-injects SF_ROLE if not present."""
    
    # Read from isolated working directory (once per PBIT file)
    with open(datamodel_path, 'r', encoding='utf-16-le') as f:
        data = json.loads(f.read())
    
    # CRITICAL: Verify SF_* parameters exist in model.expressions[]
    # These parameters may be EMPTY (no value assigned) - this is INTENTIONAL
    # Users will fill these values when opening the report in Power BI
    sf_server_link_exists = False
    sf_warehouse_name_exists = False
    sf_db_name_exists = False
    sf_role_exists = False

    for expr in data.get('model', {}).get('expressions', []):
        if expr['name'] == 'SF_SERVER_LINK':
            sf_server_link_exists = True
            param_value = expr.get('expression', '').strip('" ')
            print(f"  SF_SERVER_LINK parameter found (value: {param_value if param_value else 'EMPTY - will be filled by user'})")
        elif expr['name'] == 'SF_WAREHOUSE_NAME':
            sf_warehouse_name_exists = True
            param_value = expr.get('expression', '').strip('" ')
            print(f"  SF_WAREHOUSE_NAME parameter found (value: {param_value if param_value else 'EMPTY - will be filled by user'})")
        elif expr['name'] == 'SF_DB_NAME':
            sf_db_name_exists = True
            param_value = expr.get('expression', '').strip('" ')
            print(f"  SF_DB_NAME parameter found (value: {param_value if param_value else 'EMPTY - will be filled by user'})")
        elif expr['name'] == 'SF_ROLE':
            sf_role_exists = True
            param_value = expr.get('expression', '').strip('" ')
            print(f"  SF_ROLE parameter found (value: {param_value if param_value and param_value != 'null' else 'NULL - optional, uses default role'})")
    
    # Validate that all required parameter DEFINITIONS exist (even if empty)
    if not all([sf_server_link_exists, sf_warehouse_name_exists, sf_db_name_exists]):
        print("\nERROR: Missing required SF_* parameter definitions in DataModelSchema")
        print(f"  SF_SERVER_LINK exists: {sf_server_link_exists}")
        print(f"  SF_WAREHOUSE_NAME exists: {sf_warehouse_name_exists}")
        print(f"  SF_DB_NAME exists: {sf_db_name_exists}")
        return False, False
    
    # Auto-inject SF_ROLE if not present
    sf_role_injected = False
    if not sf_role_exists:
        print(f"  SF_ROLE parameter NOT found - auto-injecting...")
        if 'expressions' not in data['model']:
            data['model']['expressions'] = []
        data['model']['expressions'].append(SF_ROLE_DATAMODEL_DEFINITION)
        sf_role_injected = True
        
        # Write updated DataModelSchema back
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        with open(datamodel_path, 'wb') as f:
            f.write(json_str.encode('utf-16-le'))
        print(f"  {OK} SF_ROLE parameter injected into DataModelSchema")
    
    return True, sf_role_injected


def verify_parameters_in_unapplied_changes(work_dir):
    """Verify SF_* parameters in UnappliedChanges file (if it exists).
    Auto-injects SF_ROLE if not present."""
    
    unapplied_changes_path = os.path.join(work_dir, 'UnappliedChanges')
    
    if not os.path.exists(unapplied_changes_path):
        print("\n  UnappliedChanges file not found (optional file)")
        return True, False  # Not an error - file is optional
    
    print("\n  Checking UnappliedChanges file...")
    
    # Read UnappliedChanges (UTF-16 LE encoded JSON)
    with open(unapplied_changes_path, 'r', encoding='utf-16-le') as f:
        data = json.loads(f.read())
    
    # Check for SF_* parameters in queries[] array
    # These are parameter definitions that should remain unchanged
    sf_server_link_exists = False
    sf_warehouse_name_exists = False
    sf_db_name_exists = False
    sf_role_exists = False
    
    for query in data.get('queries', []):
        query_name = query.get('name', '')
        query_text = ''.join(query.get('text', []))
        
        # Check if this is a parameter definition
        if 'IsParameterQuery=true' in query_text:
            if query_name == 'SF_SERVER_LINK':
                sf_server_link_exists = True
                print(f"    SF_SERVER_LINK parameter found in UnappliedChanges")
            elif query_name == 'SF_WAREHOUSE_NAME':
                sf_warehouse_name_exists = True
                print(f"    SF_WAREHOUSE_NAME parameter found in UnappliedChanges")
            elif query_name == 'SF_DB_NAME':
                sf_db_name_exists = True
                print(f"    SF_DB_NAME parameter found in UnappliedChanges")
            elif query_name == 'SF_ROLE':
                sf_role_exists = True
                print(f"    SF_ROLE parameter found in UnappliedChanges")
    
    if sf_server_link_exists or sf_warehouse_name_exists or sf_db_name_exists:
        print(f"  {OK} SF_* parameters found in UnappliedChanges (will remain unchanged)")
    
    # Auto-inject SF_ROLE if not present
    sf_role_injected = False
    if not sf_role_exists:
        print(f"    SF_ROLE parameter NOT found in UnappliedChanges - auto-injecting...")
        if 'queries' not in data:
            data['queries'] = []
        data['queries'].append(SF_ROLE_UNAPPLIED_DEFINITION)
        sf_role_injected = True
        
        # Write updated UnappliedChanges back
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        with open(unapplied_changes_path, 'wb') as f:
            f.write(json_str.encode('utf-16-le'))
        print(f"  {OK} SF_ROLE parameter injected into UnappliedChanges")
    
    return True, sf_role_injected


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_parameters.py <datamodel_path>")
        sys.exit(1)
    
    datamodel_path = sys.argv[1]
    work_dir = os.path.dirname(datamodel_path)
    
    # Verify parameters in DataModelSchema
    datamodel_ok, datamodel_role_injected = verify_parameters_in_datamodel(datamodel_path)
    if not datamodel_ok:
        sys.exit(1)
    
    # Verify parameters in UnappliedChanges (if exists)
    unapplied_ok, unapplied_role_injected = verify_parameters_in_unapplied_changes(work_dir)
    if not unapplied_ok:
        sys.exit(1)
    
    print(f"\n{OK} All SF_* parameters exist in PBIT")
    if datamodel_role_injected or unapplied_role_injected:
        print("  SF_ROLE parameter was auto-injected (defaults to null - uses user's default Snowflake role)")
    print("Note: Empty parameter values are intentional - users will fill them when opening the report")
    sys.exit(0)


if __name__ == '__main__':
    main()
