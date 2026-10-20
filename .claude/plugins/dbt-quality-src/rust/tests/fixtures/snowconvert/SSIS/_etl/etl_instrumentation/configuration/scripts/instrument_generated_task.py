#!/usr/bin/env python3
#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved
#
"""
Script to instrument Snowflake SQL code generated from SSIS packages.

This script:
1. Locates control flow task boundaries marked by special comments
2. Inserts CALL PUBLIC.COLLECT_TABLE_METRICS() calls at the end of each task/block
3. Supports --revert to remove the instrumentation

Task markers:
- Start of task: ---- Start '<refid>'
- Start of block: ---- Start block '<block refid>'
- End of block: ---- End block '<block refid>'
"""

import argparse
import re
import sys
from pathlib import Path


# Regex patterns for parsing task markers
PATTERN_START_BLOCK = re.compile(r"^(\s*)----\s*Start\s+block\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)
PATTERN_END_BLOCK = re.compile(r"^(\s*)----\s*End\s+block\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)
PATTERN_START_TASK = re.compile(r"^(\s*)----\s*Start\s+['\"]([^'\"]+)['\"]", re.IGNORECASE)

# Pattern for the metrics call we insert
METRICS_CALL_PATTERN = re.compile(r"^\s*CALL\s+PUBLIC\.COLLECT_TABLE_METRICS\s*\(", re.IGNORECASE)


def parse_line(line: str) -> tuple:
    """
    Parse a line to identify if it's a task marker.
    
    Returns:
        tuple: (marker_type, indent, refid) or (None, None, None)
        marker_type: 'start_block', 'end_block', 'start_task', or None
    """
    # Check for start block (must check before start_task since it's more specific)
    match = PATTERN_START_BLOCK.match(line)
    if match:
        return ('start_block', match.group(1), match.group(2))
    
    # Check for end block
    match = PATTERN_END_BLOCK.match(line)
    if match:
        return ('end_block', match.group(1), match.group(2))
    
    # Check for start task (non-block)
    match = PATTERN_START_TASK.match(line)
    if match:
        return ('start_task', match.group(1), match.group(2))
    
    return (None, None, None)


def generate_metrics_call(refid: str, package_name: str, indent: str) -> str:
    """Generate the metrics collection call."""
    refid = refid.replace('\\','\\\\')
    return f"{indent}CALL PUBLIC.COLLECT_TABLE_METRICS('{refid}', '{package_name}');\n"


def instrument_sql(content: str, package_name: str = '') -> str:
    """
    Instrument SQL content with metrics collection calls.
    
    Args:
        content: The SQL file content
        package_name: Optional package name parameter
    
    Returns:
        The instrumented SQL content
    """
    # Preserve original ending
    ends_with_newline = content.endswith('\n')
    
    lines = content.split('\n')
    # Remove empty last element if content ended with newline
    if ends_with_newline and lines and lines[-1] == '':
        lines = lines[:-1]
    
    result_lines = []
    
    # Stack to track open tasks that need closing
    # Each entry: {'type': 'block'|'task', 'refid': str, 'indent': str}
    open_tasks = []
    
    for line in lines:
        marker_type, indent, refid = parse_line(line)
        
        if marker_type == 'start_block':
            # Close any pending non-block task before this block starts
            if open_tasks and open_tasks[-1]['type'] == 'task':
                task = open_tasks.pop()
                result_lines.append(generate_metrics_call(task['refid'], package_name, task['indent']).rstrip('\n'))
            
            # Push this block onto the stack
            open_tasks.append({'type': 'block', 'refid': refid, 'indent': indent})
            result_lines.append(line)
            
        elif marker_type == 'end_block':
            # Close any pending non-block task within this block
            if open_tasks and open_tasks[-1]['type'] == 'task':
                task = open_tasks.pop()
                result_lines.append(generate_metrics_call(task['refid'], package_name, task['indent']).rstrip('\n'))
            
            # Insert metrics call for the block before end marker
            if open_tasks and open_tasks[-1]['type'] == 'block':
                block = open_tasks.pop()
                result_lines.append(generate_metrics_call(block['refid'], package_name, indent).rstrip('\n'))
            
            result_lines.append(line)
            
        elif marker_type == 'start_task':
            # Close any pending non-block task
            if open_tasks and open_tasks[-1]['type'] == 'task':
                task = open_tasks.pop()
                result_lines.append(generate_metrics_call(task['refid'], package_name, task['indent']).rstrip('\n'))
            
            # Push this task onto the stack
            open_tasks.append({'type': 'task', 'refid': refid, 'indent': indent})
            result_lines.append(line)
            
        else:
            result_lines.append(line)
    
    # Handle any remaining open tasks at end of file
    while open_tasks:
        task = open_tasks.pop()
        result_lines.append(generate_metrics_call(task['refid'], package_name, task['indent']).rstrip('\n'))
    
    result = '\n'.join(result_lines)
    if ends_with_newline:
        result += '\n'
    
    return result


def revert_sql(content: str) -> str:
    """
    Remove instrumentation calls from SQL content.
    
    Args:
        content: The instrumented SQL file content
    
    Returns:
        The SQL content with metrics calls removed
    """
    # Preserve original ending
    ends_with_newline = content.endswith('\n')
    
    lines = content.split('\n')
    # Remove empty last element if content ended with newline
    if ends_with_newline and lines and lines[-1] == '':
        lines = lines[:-1]
    
    result_lines = []
    
    for line in lines:
        # Skip lines that are metrics calls
        if METRICS_CALL_PATTERN.match(line):
            continue
        result_lines.append(line)
    
    result = '\n'.join(result_lines)
    if ends_with_newline:
        result += '\n'
    
    return result


def process_file(file_path: str, package_name: str = '', output_path: str = None, 
                 revert: bool = False) -> bool:
    """
    Process a SQL file to add or remove instrumentation.
    
    Args:
        file_path: Path to the SQL file
        package_name: Optional package name parameter
        output_path: Optional output path (defaults to overwriting input file)
        revert: If True, remove instrumentation instead of adding it
    
    Returns:
        True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if revert:
        print(f"Reverting instrumentation from: {file_path}")
        result = revert_sql(content)
    else:
        print(f"Instrumenting: {file_path}")
        result = instrument_sql(content, package_name)
    
    # Write the result
    output_file = Path(output_path) if output_path else file_path
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Successfully {'reverted' if revert else 'instrumented'}: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Instrument Snowflake SQL code with metrics collection calls.'
    )
    parser.add_argument(
        'file_path',
        help='Path to the SQL file to instrument'
    )
    parser.add_argument(
        '--package-name',
        default='',
        help='Optional package name parameter for the metrics call (default: empty string)'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: overwrite input file)'
    )
    parser.add_argument(
        '--revert',
        action='store_true',
        help='Remove instrumentation calls instead of adding them'
    )
    
    args = parser.parse_args()
    
    success = process_file(
        file_path=args.file_path,
        package_name=args.package_name,
        output_path=args.output,
        revert=args.revert
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

