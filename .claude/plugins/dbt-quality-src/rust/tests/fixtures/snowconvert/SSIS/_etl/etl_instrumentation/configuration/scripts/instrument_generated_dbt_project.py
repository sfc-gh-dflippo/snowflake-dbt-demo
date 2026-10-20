#!/usr/bin/env python3
#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved
#
"""
Script to update dbt_project.yml files to add post-hook macros for execution metrics tracking.

This script:
1. Reads a dbt_project.yml file
2. Extracts the refId from the header comment (format: ### dbt project for '<refId>')
3. For each model type (except 'marts'):
   - Changes +materialized to 'table'
   - Adds a +post-hook with the m_register_post_exec_metrics macro
4. Writes the updated configuration back to the file

Use --revert to remove the post-hooks and optionally restore original materialization settings.
"""

import argparse
from typing import Union
import re
import sys
from pathlib import Path

try:
   import yaml
except ImportError:
    print("Error: yaml module not found. Please install it using 'pip install pyyaml'.")
    sys.exit(1)

class IndentedListDumper(yaml.SafeDumper):
    """Custom YAML dumper that indents list items properly."""
    
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow=flow, indentless=False)


def extract_ref_id(file_content: str) -> Union[str, None]:
    """
    Extract the refId from the header comment.
    Expected format: ### dbt project for '<refId>'
    """
    pattern = r"###\s*dbt project for\s*['\"]([^'\"]+)['\"]"
    match = re.search(pattern, file_content)
    if match:
        return match.group(1)
    return None


def extract_header_comment(file_content: str) -> str:
    """Extract the header comment lines from the file content."""
    lines = file_content.split('\n')
    header_lines = []
    for line in lines:
        if line.startswith('#'):
            header_lines.append(line)
        else:
            break
    return '\n'.join(header_lines) + '\n' if header_lines else ''


def update_models_section(config: dict, ref_id: str, package_name: str) -> dict:
    """
    Update the models section to add post-hooks for non-mart models.
    
    Args:
        config: The parsed YAML configuration
        ref_id: The reference ID extracted from the header comment
        package_name: The package name parameter
    
    Returns:
        The updated configuration dictionary
    """
    
    ref_id = ref_id.replace('\\', '\\\\\\\\')
    if 'models' not in config:
        print("Warning: No 'models' section found in the configuration.")
        return config
    
    models_section = config['models']
    
    # Iterate through project names in models section
    for project_name, project_config in models_section.items():
        if not isinstance(project_config, dict):
            continue
        
        # Iterate through model types (staging, intermediate, marts, etc.)
        for model_type, model_config in project_config.items():
            # Skip 'marts' models
            if model_type.lower() == 'marts':
                continue
            
            if not isinstance(model_config, dict):
                continue
            
            # Change materialized to 'table'
            if '+materialized' in model_config:
                model_config['+materialized'] = 'table'
            
            # Add post-hook with the macro invocation
            post_hook = f"{{{{ m_register_post_exec_metrics(this.name,'{ref_id}', '{package_name}') }}}}"
            model_config['+post-hook'] = [post_hook]
    
    return config


# Default materialization values for revert operation
DEFAULT_MATERIALIZATIONS = {
    'staging': 'view',
    'intermediate': 'ephemeral',
}


def revert_models_section(config: dict, materialization_overrides: dict = None) -> dict:
    """
    Revert the models section by removing post-hooks and optionally restoring materialization.
    
    Args:
        config: The parsed YAML configuration
        materialization_overrides: Optional dict mapping model types to materialization values
    
    Returns:
        The reverted configuration dictionary
    """
    if 'models' not in config:
        print("Warning: No 'models' section found in the configuration.")
        return config
    
    materializations = DEFAULT_MATERIALIZATIONS.copy()
    if materialization_overrides:
        materializations.update(materialization_overrides)
    
    models_section = config['models']
    
    # Iterate through project names in models section
    for project_name, project_config in models_section.items():
        if not isinstance(project_config, dict):
            continue
        
        # Iterate through model types (staging, intermediate, marts, etc.)
        for model_type, model_config in project_config.items():
            # Skip 'marts' models
            if model_type.lower() == 'marts':
                continue
            
            if not isinstance(model_config, dict):
                continue
            
            # Remove post-hook if present
            if '+post-hook' in model_config:
                del model_config['+post-hook']
                print(f"  Removed +post-hook from {model_type}")
            
            # Restore materialization if specified
            model_type_lower = model_type.lower()
            if model_type_lower in materializations and '+materialized' in model_config:
                old_value = model_config['+materialized']
                new_value = materializations[model_type_lower]
                model_config['+materialized'] = new_value
                print(f"  Restored {model_type} +materialized: {old_value} -> {new_value}")
    
    return config


def process_dbt_project_file(file_path: str, package_name: str = '', output_path: str = None) -> bool:
    """
    Process a dbt_project.yml file to add execution metrics hooks.
    
    Args:
        file_path: Path to the dbt_project.yml file
        package_name: Optional package name parameter
        output_path: Optional output path (defaults to overwriting input file)
    
    Returns:
        True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # Extract header comment and refId
    header_comment = extract_header_comment(file_content)
    ref_id = extract_ref_id(file_content)
    
    if ref_id is None:
        print("Error: Could not extract refId from header comment.")
        print("Expected format: ### dbt project for '<refId>'")
        return False
    
    print(f"Extracted refId: {ref_id}")
    
    # Parse YAML content (skip header comments for parsing)
    yaml_content = file_content
    if header_comment:
        yaml_content = file_content[len(header_comment):]
    
    try:
        config = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return False
    
    if config is None:
        print("Error: Empty or invalid YAML configuration.")
        return False
    
    # Update the models section
    updated_config = update_models_section(config, ref_id, package_name)
    
    # Write the updated configuration
    output_file = Path(output_path) if output_path else file_path
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header comment first
        if header_comment:
            f.write(header_comment)
        
        # Write updated YAML with proper indentation
        yaml.dump(
            updated_config,
            f,
            Dumper=IndentedListDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000,  # Prevent line wrapping
            indent=2
        )
    
    print(f"Successfully updated: {output_file}")
    return True


def revert_dbt_project_file(file_path: str, output_path: str = None, 
                            materialization_overrides: dict = None) -> bool:
    """
    Revert a dbt_project.yml file by removing execution metrics hooks.
    
    Args:
        file_path: Path to the dbt_project.yml file
        output_path: Optional output path (defaults to overwriting input file)
        materialization_overrides: Optional dict mapping model types to materialization values
    
    Returns:
        True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # Extract header comment
    header_comment = extract_header_comment(file_content)
    
    # Parse YAML content (skip header comments for parsing)
    yaml_content = file_content
    if header_comment:
        yaml_content = file_content[len(header_comment):]
    
    try:
        config = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return False
    
    if config is None:
        print("Error: Empty or invalid YAML configuration.")
        return False
    
    print("Reverting dbt project configuration...")
    
    # Revert the models section
    reverted_config = revert_models_section(config, materialization_overrides)
    
    # Write the reverted configuration
    output_file = Path(output_path) if output_path else file_path
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header comment first
        if header_comment:
            f.write(header_comment)
        
        # Write reverted YAML with proper indentation
        yaml.dump(
            reverted_config,
            f,
            Dumper=IndentedListDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000,  # Prevent line wrapping
            indent=2
        )
    
    print(f"Successfully reverted: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Update dbt_project.yml to add post-hook macros for execution metrics tracking.'
    )
    parser.add_argument(
        'file_path',
        help='Path to the dbt_project.yml file'
    )
    parser.add_argument(
        '--package-name',
        default='',
        help='Optional package name parameter for the macro (default: empty string)'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: overwrite input file)'
    )
    parser.add_argument(
        '--revert',
        action='store_true',
        help='Revert the file by removing post-hooks and restoring materialization'
    )
    parser.add_argument(
        '--staging-materialized',
        default=None,
        help='Materialization value for staging models when reverting (default: view)'
    )
    parser.add_argument(
        '--intermediate-materialized',
        default=None,
        help='Materialization value for intermediate models when reverting (default: ephemeral)'
    )
    
    args = parser.parse_args()
    
    if args.revert:
        # Build materialization overrides from arguments
        materialization_overrides = {}
        if args.staging_materialized:
            materialization_overrides['staging'] = args.staging_materialized
        if args.intermediate_materialized:
            materialization_overrides['intermediate'] = args.intermediate_materialized
        
        success = revert_dbt_project_file(
            file_path=args.file_path,
            output_path=args.output,
            materialization_overrides=materialization_overrides if materialization_overrides else None
        )
    else:
        success = process_dbt_project_file(
            file_path=args.file_path,
            package_name=args.package_name,
            output_path=args.output
        )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

