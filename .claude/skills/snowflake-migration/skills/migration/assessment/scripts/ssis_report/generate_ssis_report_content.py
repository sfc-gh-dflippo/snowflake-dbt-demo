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
SSIS Report Content Generator for Multi-Tab Report

Generates HTML content for SSIS assessment using the local ssis_html_report_generator.
"""

import os
import sys
import json
from pathlib import Path
from typing import Tuple

_scripts_dir = str(Path(__file__).resolve().parent.parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports.console_utils import DONE  # noqa: E402

# Import the local SSIS HTML report generator
from .ssis_html_report_generator import HTMLReportGenerator, sanitize_filename


def generate_ssis_html_content(ssis_json_path: Path, output_html_path: Path = None) -> Tuple[str, str, str]:
    """
    Generate HTML content for SSIS tab using the same generator as standalone reports.
    
    Args:
        ssis_json_path: Path to SSIS assessment JSON file
        output_html_path: Path where the main HTML file will be saved (optional, for package page generation)
        
    Returns:
        Tuple of (html_content, javascript_code, css_content)
    """
    try:
        # Resolve AI summary path from JSON summary (optional)
        summary_html_path = None
        try:
            data = json.loads(ssis_json_path.read_text(encoding="utf-8"))
            summary_path = data.get("summary", {}).get("ai_summary", "")
            if summary_path:
                candidate = (ssis_json_path.parent / summary_path).resolve()
                if candidate.exists():
                    summary_html_path = candidate
                else:
                    print(f"Warning: ai_summary path not found: {candidate}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not load ai_summary from JSON: {e}", file=sys.stderr)

        # Create HTMLReportGenerator instance
        generator = HTMLReportGenerator(
            json_path=str(ssis_json_path),
            executive_summary_path=str(summary_html_path) if summary_html_path else None,
            ai_estimation_enabled=False
        )
        
        # Determine output folder for package pages
        # If output_html_path is provided, create packages folder alongside it
        if output_html_path:
            output_dir = output_html_path.parent
            main_report_filename = output_html_path.name
            packages_dir = output_dir / "packages"
            packages_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate individual package pages
            package_count = 0
            # `dag_base_path` is interpolated into HTML href= attributes, which
            # require forward slashes regardless of OS.
            dag_base_path = os.path.relpath(
                ssis_json_path.parent.resolve(),
                packages_dir.resolve()
            ).replace(os.sep, '/')
            for package_csv_row in generator.packages:
                package_path = package_csv_row.get('path', '')
                package_name = package_csv_row.get('name', '')
                
                # Get package data from JSON
                package_json_data = generator.get_package_data_from_json(package_path)
                if not package_json_data:
                    continue
                
                # Generate package detail page with correct back link
                package_html = generator.generate_package_detail_page(package_csv_row, package_json_data, main_report_filename=main_report_filename, dag_base_path=dag_base_path)
                
                # Save package page in packages subfolder
                package_filename = f"package_{sanitize_filename(package_name)}.html"
                package_file_path = packages_dir / package_filename
                
                with open(package_file_path, 'w', encoding='utf-8') as f:
                    f.write(package_html)
                
                package_count += 1
            
            print(f"{DONE} Generated {package_count} SSIS package detail pages in: {packages_dir}")
            output_folder = str(output_dir)
        else:
            output_folder = None
        
        # Get the EXACT CSS from the standalone generator
        css_content = generator.generate_css()
        
        # Scope CSS by prefixing all selectors with #ssis-report
        # This ensures SSIS styles take precedence over multi-tab CSS
        import re
        
        def scope_css(css_text, scope_id):
            """Add scope_id before each CSS selector"""
            lines = []
            in_selector = True
            current_selector = []
            
            for line in css_text.split('\n'):
                stripped = line.strip()
                
                # Skip empty lines and preserve them
                if not stripped:
                    lines.append(line)
                    continue
                
                # Check if this is a property line (contains : but not in a selector context)
                if stripped and '{' in stripped:
                    # This is a selector line
                    if stripped.startswith('@') or stripped.startswith('*'):
                        # Don't scope @media, @keyframes, * selectors
                        lines.append(line)
                    else:
                        # Scope the selector
                        selector = stripped.replace('{', '').strip()
                        scoped_selector = f"{scope_id} {selector}" if selector else scope_id
                        lines.append(f"        {scoped_selector} {{")
                elif stripped and not any(c in stripped for c in ['{', '}', ':']):
                    # Might be a multi-line selector
                    lines.append(line)
                else:
                    # Property or closing brace
                    lines.append(line)
            
            return '\n'.join(lines)
        
        scoped_css = scope_css(css_content, '#ssis-report')
        
        # Add !important to critical grid and card properties to ensure they override multi-tab CSS
        scoped_css = scoped_css.replace(
            'display: grid;',
            'display: grid !important;'
        ).replace(
            'grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));',
            'grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) !important;'
        )
        
        # Fix metric-card display - multi-tab CSS has .metric-card { display: inline-flex }
        # We need to ensure cards behave as block elements within the grid
        scoped_css = scoped_css.replace(
            '#ssis-report .metric-card {',
            '#ssis-report .metric-card {\n            display: block !important;'
        )
        
        # Generate the same sections as the standalone report
        # but without the full page structure (no sidebar, no wrapping HTML)
        executive_summary = generator.generate_executive_summary()
        metrics_section = generator.generate_metrics_section()
        not_supported_section = generator.generate_not_supported_section()
        # Pass output_folder to generate package pages if output path is provided
        package_summary = generator.generate_package_summary(output_folder=output_folder)
        
        # Combine all sections with the EXACT same structure as standalone
        # CSS is returned separately so it can be injected into the main <head>
        # Section order: AI Summary -> Key Metrics -> Package Classification -> Component Breakdown
        html_content = f"""
        <div id="ssis-report">
            <h1>SSIS Assessment Report</h1>
        
            {executive_summary}
            {metrics_section}
            {package_summary}
            {not_supported_section}
        </div>
        """
        
        # Package and component search/filter JS (needed for multi-tab report)
        # Expose functions globally because the HTML uses onclick handlers.
        js_code = """
        (function() {
            function filterComponents() {
                const searchTerm = document.getElementById('componentSearch')?.value.toLowerCase() || '';
                const typeFilter = document.getElementById('typeFilter')?.value.toLowerCase() || '';
                const rows = document.querySelectorAll('.component-row');
                let visibleCount = 0;
                
                rows.forEach(row => {
                    const componentName = row.getAttribute('data-component-name') || '';
                    const componentType = row.getAttribute('data-component-type') || '';
                    
                    const matchesSearch = componentName.includes(searchTerm);
                    const matchesType = !typeFilter || componentType === typeFilter;
                    
                    if (matchesSearch && matchesType) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                const totalCount = rows.length;
                const countElement = document.getElementById('componentCount');
                if (countElement) {
                    countElement.textContent = `Showing ${visibleCount} of ${totalCount} component types`;
                }
            }

            function filterPackages() {
                const searchTerm = document.getElementById('packageSearch')?.value.toLowerCase() || '';
                const classificationFilter = document.getElementById('classificationFilter')?.value || '';
                const complexityFilter = document.getElementById('complexityFilter')?.value || '';

                const rows = document.querySelectorAll('.package-row');
                let visibleCount = 0;

                rows.forEach(row => {
                    const name = row.getAttribute('data-name') || '';
                    const classification = row.getAttribute('data-classification') || '';
                    const complexity = row.getAttribute('data-complexity') || '';

                    const matchesSearch = name.includes(searchTerm);
                    const matchesClassification = !classificationFilter || classification === classificationFilter;
                    const matchesComplexity = !complexityFilter || complexity === complexityFilter;

                    if (matchesSearch && matchesClassification && matchesComplexity) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });

                const totalCount = rows.length;
                const countElement = document.getElementById('packageCount');
                if (countElement) {
                    countElement.textContent = `Showing ${visibleCount} of ${totalCount} packages`;
                }
            }

            function resetPackageFilters() {
                const search = document.getElementById('packageSearch');
                const classification = document.getElementById('classificationFilter');
                const complexity = document.getElementById('complexityFilter');

                if (search) search.value = '';
                if (classification) classification.value = '';
                if (complexity) complexity.value = '';
                filterPackages();
            }

            // Expose globally for onclick handlers
            window.filterComponents = filterComponents;
            window.filterPackages = filterPackages;
            window.resetPackageFilters = resetPackageFilters;

            // Attach event listeners for component filter
            document.getElementById('componentSearch')?.addEventListener('keyup', filterComponents);
            document.getElementById('typeFilter')?.addEventListener('change', filterComponents);

            // Attach event listeners for package filter
            document.getElementById('packageSearch')?.addEventListener('input', filterPackages);
            document.getElementById('classificationFilter')?.addEventListener('change', filterPackages);
            document.getElementById('complexityFilter')?.addEventListener('change', filterPackages);

            // Initialize count displays
            window.addEventListener('load', function() {
                filterComponents();
                filterPackages();
            });
        })();
        """
        
        return html_content, js_code, scoped_css
        
    except FileNotFoundError as e:
        error_html = f"""
        <div class="ssis-content">
            <h2 class="text-3xl font-bold text-sf-dark-blue mb-6 border-b-2 border-sf-blue pb-2">
                SSIS Assessment Report
            </h2>
            <div class="info-box" style="background-color: #fef2f2; border-color: #EF4444;">
                <p style="color: #991B1B; margin: 0;">
                    <strong>Error:</strong> SSIS JSON file not found: {ssis_json_path}
                </p>
            </div>
        </div>
        """
        return error_html, "", ""
    except Exception as e:
        error_html = f"""
        <div class="ssis-content">
            <h2 class="text-3xl font-bold text-sf-dark-blue mb-6 border-b-2 border-sf-blue pb-2">
                SSIS Assessment Report
            </h2>
            <div class="info-box" style="background-color: #fef2f2; border-color: #EF4444;">
                <p style="color: #991B1B; margin: 0;">
                    <strong>Error loading SSIS data:</strong> {str(e)}
                </p>
            </div>
        </div>
        """
        return error_html, "", ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_ssis_report_content.py <ssis_json_path>")
        sys.exit(1)
    
    json_path = Path(sys.argv[1])
    html, js, css = generate_ssis_html_content(json_path)
    print("HTML Content Generated Successfully")
    print(f"HTML Length: {len(html)} characters")
    print(f"JS Length: {len(js)} characters")
    print(f"CSS Length: {len(css)} characters")
