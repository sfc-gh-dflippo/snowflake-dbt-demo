#!/usr/bin/env python3
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Data Loading Module for HTML Wave Migration Report Generator

Contains all data loading and parsing functions for dependency analysis outputs.
"""
import sys
from pathlib import Path

# Add shared library to path
_scripts_dir = str(Path(__file__).resolve().parent.parent.parent / 'scripts')
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports.na_utils import NA_VALUES as _NA_VALUES 


def load_issues_estimation(json_path):
    """Load issues estimation data from JSON file."""
    from snowconvert_reports import load_issues_estimation_json
    issue_map_typed, severity_map_typed = load_issues_estimation_json(json_path)
    issue_map = {code: {'code': e.code, 'severity': e.severity, 'manual_effort': e.manual_effort, 'friendly_name': e.friendly_name}
                 for code, e in issue_map_typed.items()}
    severity_map = {s.severity: s.manual_effort for s in severity_map_typed.values()}
    return issue_map, severity_map


def load_toplevel_code_units(csv_path):
    """Load TopLevelCodeUnits CSV with object metadata.
    Uses CodeUnitId (fully qualified name) as the primary key for matching with partition_membership.
    """
    from snowconvert_reports import load_code_units
    units = load_code_units(csv_path)
    objects_data = {}
    for u in units:
        if u.code_unit_id:
            obj_data = {
                'category': u.category,
                'file_name': u.file_name,
                'code_unit': u.code_unit,
                'has_missing_dependencies': u.has_missing_dependencies,
                'deployment_order': u.deployment_order,
                'conversion_status': u.conversion_status,
                'lines_of_code': str(u.lines_of_code),
                'ewi_count': u.ewi_count,
                'fdm_count': u.fdm_count,
                'prf_count': u.prf_count,
                'highest_ewi_severity': u.highest_ewi_severity,
            }
            objects_data[u.code_unit_id] = obj_data
            if u.code_unit_name:
                objects_data[u.code_unit_name] = obj_data
    return objects_data


def load_toplevel_objects_estimation(csv_path):
    """Load TopLevelObjectsEstimation report with per-object effort data and EWI counts."""
    from snowconvert_reports import load_object_estimations
    estimations = load_object_estimations(csv_path)
    return {e.object_id: {
        'manual_effort_minutes': e.manual_effort_minutes,
        'conversion_status': e.conversion_status,
        'ewis_number': e.ewis_number,
        'highest_ewi_severity': e.highest_ewi_severity,
    } for e in estimations}


def find_estimation_reports(reports_dir):
    """Find estimation report files with NA or timestamp patterns."""
    from snowconvert_reports import ReportFinder
    finder = ReportFinder(reports_dir)
    estimation_files = {}
    mapping = {
        'toplevel_estimation': finder.find_toplevel_objects_estimation,
        'issues_aggregate': finder.find_issues_aggregate,
        'effort_formula': finder.find_effort_formula,
    }
    for key, find_fn in mapping.items():
        path = find_fn()
        if path:
            estimation_files[key] = path
    return estimation_files


def load_estimation_grand_totals(estimation_files):
    """Load grand totals from estimation reports for display in HTML."""
    from snowconvert_reports import load_object_estimations
    from snowconvert_reports.loaders.csv_reader import read_csv_rows

    grand_totals = {}

    if 'toplevel_estimation' in estimation_files:
        try:
            estimations = load_object_estimations(estimation_files['toplevel_estimation'])
            total_objects = len(estimations)
            total_manual_minutes = sum(e.manual_effort_minutes for e in estimations)
            success_count = sum(1 for e in estimations if e.conversion_status == 'Success')

            grand_totals['toplevel'] = {
                'total_objects': total_objects,
                'total_manual_hours': total_manual_minutes / 60.0,
                'success_count': success_count,
                'success_rate': (success_count / total_objects * 100) if total_objects > 0 else 0
            }
        except Exception as e:
            print(f"Error loading toplevel estimation totals: {e}")

    if 'issues_aggregate' in estimation_files:
        try:
            severity_breakdown = {}
            total_issues = 0
            total_issue_minutes = 0.0

            for row in read_csv_rows(estimation_files['issues_aggregate']):
                severity = row.get('Highest EWI Severity', '')
                count = int(row.get('Object Count', '0') or '0')
                manual_effort = row.get('Manual Effort', '0')

                try:
                    effort_minutes = float(manual_effort) if manual_effort else 0.0
                except ValueError:
                    effort_minutes = 0.0

                total_issues += count
                total_issue_minutes += effort_minutes

                if severity:
                    severity_breakdown[severity] = {
                        'count': count,
                        'manual_hours': effort_minutes / 60.0
                    }

            grand_totals['issues_aggregate'] = {
                'total_issues': total_issues,
                'total_manual_hours': total_issue_minutes / 60.0,
                'severity_breakdown': severity_breakdown
            }
        except Exception as e:
            print(f"Error loading issues aggregate totals: {e}")

    if 'effort_formula' in estimation_files:
        try:
            code_unit_breakdown = {}

            for row in read_csv_rows(estimation_files['effort_formula']):
                code_unit = row.get('Code Unit Type', '')
                count = int(row.get('Code Unit Count', '0') or '0')
                manual_effort = row.get('Manual Effort', '0')

                try:
                    effort_minutes = float(manual_effort) if manual_effort else 0.0
                except ValueError:
                    effort_minutes = 0.0

                if code_unit:
                    code_unit_breakdown[code_unit] = {
                        'count': count,
                        'manual_hours': effort_minutes / 60.0
                    }

            grand_totals['effort_formula'] = {
                'code_unit_breakdown': code_unit_breakdown
            }
        except Exception as e:
            print(f"Error loading effort formula totals: {e}")

    return grand_totals


def estimate_hours_for_object(obj_name, objects_data, severity_map, estimation_data=None, conversion_status_override=None):
    """Estimate hours based on conversion status and issues.

    Uses estimation reports if provided, otherwise falls back to severity baseline.
    """
    obj_info = objects_data.get(obj_name, {})
    conversion_status = conversion_status_override if conversion_status_override is not None else obj_info.get('conversion_status', 'Unknown')

    if estimation_data and obj_name in estimation_data:
        return estimation_data[obj_name].get('manual_effort_minutes', 0.0) / 60.0

    if conversion_status == 'Success':
        return 0.0

    return severity_map.get('Medium', 16.5) / 60.0


def load_object_references_as_dicts(reports_dir):
    """Load ObjectReferences CSV as a list of {'caller', 'referenced'} dicts."""
    from snowconvert_reports import ReportFinder, load_object_references

    finder = ReportFinder(reports_dir)
    csv_path = finder.find_object_references()
    if not csv_path:
        return []

    refs = load_object_references(csv_path)
    return [
        {'caller': r.caller_full_name, 'referenced': r.referenced_full_name}
        for r in refs
        if r.caller_full_name and r.referenced_full_name
        and r.caller_full_name not in _NA_VALUES and r.referenced_full_name not in _NA_VALUES
    ]


def _accumulate_missing_refs(caller_referenced_pairs):
    """Build missing-refs result dict from (caller, referenced, relation_type, line, file_name) tuples."""
    missing_objects = set()
    dependents = {}
    details = []

    for caller, referenced, relation_type, line, file_name in caller_referenced_pairs:
        if not referenced or not caller or caller in _NA_VALUES or referenced in _NA_VALUES:
            continue

        missing_objects.add(referenced)
        dependents.setdefault(referenced, []).append({
            'caller': caller, 'relation_type': relation_type, 'line': line, 'file_name': file_name
        })
        details.append({
            'missing_object': referenced, 'dependent': caller,
            'relation_type': relation_type, 'line': line, 'file_name': file_name
        })

    return {'missing_objects': missing_objects, 'dependents': dependents, 'details': details}


def load_missing_object_references_from_registry(registry_dir):
    """Load missing object references from SnowConvert registry JSON files.

    Returns dict with keys:
        - missing_objects: set of missing object names
        - dependents: dict mapping missing object -> list of dependents
        - details: list of dependency details
        - data_source: 'registry'
        - warning: None (or error message on failure)
    """
    import re
    from snowconvert_reports import load_missing_references_from_registry

    _NA_SEG_RE = re.compile(r'\[N/A\]\.')
    _NA_VALS = {"N/A", "n/a", "NA", "na", ""}

    def _clean(val):
        if not val:
            return ""
        return _NA_SEG_RE.sub('', str(val).strip())

    refs = load_missing_references_from_registry(Path(registry_dir))

    def _iter():
        for r in refs:
            caller = _clean(r.caller_full_name)
            referenced = _clean(r.referenced_full_name)
            yield caller, referenced, r.relation_type, r.line, r.file_name

    result = _accumulate_missing_refs(_iter())
    result['data_source'] = 'registry'
    result['warning'] = None
    return result


def load_missing_refs(registry_dir=None, reports_dir=None):
    """Load missing object references from registry only.

    Returns dict with keys:
        - missing_objects: set of missing object names
        - dependents: dict mapping missing object -> list of dependents
        - details: list of dependency details
        - data_source: 'registry' or 'none'
        - warning: error message if registry not available, None otherwise
    """
    if not registry_dir:
        return {
            'missing_objects': set(),
            'dependents': {},
            'details': [],
            'data_source': 'none',
            'warning': 'No registry directory provided. Missing dependencies analysis requires --registry-dir.',
        }

    try:
        result = load_missing_object_references_from_registry(registry_dir)
        # Registry loaded successfully - return result (even if 0 missing deps)
        return result
    except Exception as exc:
        import sys as _sys
        print(f"Error loading missing refs from registry: {exc}", file=_sys.stderr)
        return {
            'missing_objects': set(),
            'dependents': {},
            'details': [],
            'data_source': 'none',
            'warning': f'Failed to load missing dependencies from registry: {exc}',
        }