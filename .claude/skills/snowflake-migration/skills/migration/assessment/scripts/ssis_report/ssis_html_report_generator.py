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
SSIS Assessment HTML Report Generator

Generates a standalone HTML report from ETL assessment analysis data.
"""

import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import unquote

_scripts_dir = str(Path(__file__).resolve().parent.parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from snowconvert_reports.console_utils import DONE, WARN  # noqa: E402


def sanitize_filename(name: str) -> str:
    """Sanitize a package name for use as a filename."""
    name = unquote(name)
    name = re.sub(r'\.dtsx$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[^\w]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name


def format_display_name(name: str) -> str:
    """Convert a name to a readable display name."""
    name = unquote(name)
    name = re.sub(r'\.dtsx$', '', name, flags=re.IGNORECASE)
    return name


class HTMLReportGenerator:
    """Generates standalone HTML assessment reports."""
    
    # Snowflake Official Colors
    COLORS = {
        'sf_blue': '#29B5E8',
        'sf_dark_blue': '#11567F',
        'sf_deep_blue': '#003545',
        'sf_navy': '#102E46',
        'sf_orange': '#FF9F36',
        'sf_cyan': '#71D3DC',
        'sf_purple': '#7D44CF',
        'sf_pink': '#D45B90',
        'sf_gray': '#8A999E',
        'sf_dark_gray': '#24323D',
        'success': '#22C55E',
        'warning': '#F59E0B',
        'danger': '#EF4444',
    }
    
    def __init__(self, json_path: str, executive_summary_path: str = None, ai_estimation_enabled: bool = False):
        """
        Initialize the report generator.
        
        Args:
            json_path: Path to etl_assessment_analysis.json (contains AI analysis)
            executive_summary_path: Optional path to executive summary text file
            ai_estimation_enabled: Whether to show AI effort estimation (default: False)
        """
        self.json_path = Path(json_path)
        self.executive_summary_path = Path(executive_summary_path) if executive_summary_path else None
        self.ai_estimation_enabled = ai_estimation_enabled
        
        # Load data - AI analysis is now included in the main JSON
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Packages with AI analysis are in the main data structure
        self.packages = self.data.get('packages', [])
        
        # Load executive summary if provided
        self.executive_summary = None
        if self.executive_summary_path and self.executive_summary_path.exists():
            with open(self.executive_summary_path, 'r', encoding='utf-8') as f:
                self.executive_summary = f.read().strip()
    
    def generate_css(self) -> str:
        """Generate inline CSS styles."""
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #000000;
            background-color: #FFFFFF;
        }}
        
        .sidebar {{
            width: 280px;
            background: {self.COLORS['sf_navy']};
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            padding: 2rem 0;
        }}
        
        .sidebar-header {{
            padding: 0 1.5rem 2rem;
            border-bottom: 1px solid {self.COLORS['sf_dark_blue']};
            margin-bottom: 1rem;
        }}
        
        .sidebar-title {{
            color: #FFFFFF;
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .sidebar-subtitle {{
            color: {self.COLORS['sf_gray']};
            font-size: 0.875rem;
        }}
        
        .nav-link {{
            display: block;
            padding: 0.75rem 1.5rem;
            color: #FFFFFF;
            text-decoration: none;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .nav-link:hover {{
            background: {self.COLORS['sf_dark_blue']};
            border-left-color: {self.COLORS['sf_blue']};
        }}
        
        .nav-link.active {{
            background: {self.COLORS['sf_dark_blue']};
            border-left-color: {self.COLORS['sf_blue']};
            color: {self.COLORS['sf_blue']};
        }}
        
        .content {{
            margin-left: 280px;
            padding: 2rem;
            max-width: 1400px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {self.COLORS['sf_dark_blue']};
            margin-bottom: 1rem;
        }}
        
        h2 {{
            font-size: 2rem;
            font-weight: bold;
            color: {self.COLORS['sf_dark_blue']};
            margin: 2rem 0 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {self.COLORS['sf_blue']};
        }}
        
        h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: {self.COLORS['sf_dark_blue']};
            margin: 1.5rem 0 1rem;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .metric-card {{
            background: white;
            border: 1px solid {self.COLORS['sf_gray']};
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .metric-label {{
            font-size: 0.875rem;
            color: {self.COLORS['sf_gray']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {self.COLORS['sf_blue']};
        }}
        
        .metric-description {{
            font-size: 0.875rem;
            color: {self.COLORS['sf_gray']};
            margin-top: 0.5rem;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        thead {{
            background: {self.COLORS['sf_blue']};
            color: white;
        }}
        
        th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid {self.COLORS['sf_gray']};
        }}
        
        tbody tr:hover {{
            background: #E5F6FD;
        }}
        
        tbody tr:nth-child(even) {{
            background: #F9FAFB;
        }}
        
        tbody tr:nth-child(even):hover {{
            background: #E5F6FD;
        }}
        
        .chart-container {{
            background: white;
            border: 1px solid {self.COLORS['sf_gray']};
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            height: auto;
            min-height: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .bar-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .bar-label {{
            min-width: 100px;
            font-weight: 600;
            color: {self.COLORS['sf_dark_blue']};
        }}
        
        .bar-background {{
            flex: 1;
            height: 40px;
            background: #F3F4F6;
            border-radius: 4px;
            position: relative;
            overflow: hidden;
        }}
        
        .bar-fill {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            transition: width 0.3s ease;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-success {{
            background: {self.COLORS['success']};
            color: white;
        }}
        
        .badge-warning {{
            background: {self.COLORS['warning']};
            color: white;
        }}
        
        .badge-danger {{
            background: {self.COLORS['danger']};
            color: white;
        }}
        
        .badge-info {{
            background: {self.COLORS['sf_blue']};
            color: white;
        }}
        
        .section {{
            margin-bottom: 3rem;
        }}
        
        .info-box {{
            background: #F0F9FF;
            border-left: 4px solid {self.COLORS['sf_blue']};
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            border-radius: 4px;
        }}
        
        .warning-box {{
            background: #FEF3C7;
            border-left: 4px solid {self.COLORS['warning']};
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            border-radius: 4px;
        }}
        
        /* Package row tooltip styles */
        .package-row {{
            position: relative;
        }}
        
        .package-row .ai-tooltip {{
            visibility: hidden;
            opacity: 0;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: 100%;
            width: 450px;
            max-width: 90vw;
            background: #1e293b;
            color: #f1f5f9;
            padding: 1rem;
            border-radius: 8px;
            font-size: 0.8rem;
            line-height: 1.5;
            z-index: 1000;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            transition: opacity 0.2s ease, visibility 0.2s ease;
            pointer-events: none;
            white-space: pre-wrap;
            text-align: left;
        }}
        
        .package-row .ai-tooltip::after {{
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 8px solid transparent;
            border-top-color: #1e293b;
        }}
        
        .package-row:hover .ai-tooltip {{
            visibility: visible;
            opacity: 1;
        }}
        
        .ai-tooltip-header {{
            font-weight: 600;
            color: {self.COLORS['sf_blue']};
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #334155;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .ai-tooltip-content {{
            color: #cbd5e1;
        }}
        
        .ai-tooltip-pending {{
            color: #94a3b8;
            font-style: italic;
            text-align: center;
            padding: 0.5rem;
        }}
        """
    
    def generate_header(self) -> str:
        """Generate HTML header with title and navigation."""
        return f"""
        <nav class="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">SSIS Assessment</div>
                <div class="sidebar-subtitle">Migration Analysis</div>
            </div>
            <a href="#executive-summary" class="nav-link">AI Summary</a>
            <a href="#metrics" class="nav-link">Key Metrics</a>
            <a href="#package-summary" class="nav-link">Package Classification</a>
            <a href="#not-supported" class="nav-link">Component Breakdown</a>
        </nav>
        
        <main class="content">
            <div style="margin-bottom: 32px;">
                <h1 style="font-size: 1.875rem; font-weight: 800; color: #102E46; margin-bottom: 12px;">
                    SSIS Assessment Report
                </h1>
                <p style="color: #64748B; font-size: 1.1rem;">
                    Comprehensive analysis of SSIS packages identified for migration including component analysis and conversion readiness metrics.
                </p>
            </div>
        """
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        summary = self.data.get('summary', {})
        
        if self.executive_summary:
            return f"""
            {self.executive_summary}
            """
        else:
            # Default summary if no AI-generated summary provided
            return f"""
        <section id="executive-summary" class="section">
            <h2>AI Summary</h2>
            <p>This report provides a comprehensive analysis of {summary.get('packages', 0)} SSIS packages 
            identified for migration to Snowflake. The assessment includes detailed component analysis, 
            conversion readiness metrics, and AI-powered migration recommendations.</p>
        </section>
        """
    
    def generate_metrics_section(self) -> str:
        """Generate key metrics cards."""
        summary = self.data.get('summary', {})
        
        # Calculate AI analyzed packages count
        analyzed_count = 0
        for package in self.packages:
            ai_analysis = package.get('ai_analysis', {})
            analysis_text = ai_analysis.get('analysis', '').strip()
            if analysis_text:
                analyzed_count += 1
        
        # Conditionally include AI Effort card
        ai_effort_card = ""
        if self.ai_estimation_enabled:
            ai_effort_card = f"""
                <div class="metric-card">
                    <div class="metric-label">Estimated AI Effort</div>
                    <div class="metric-value">{summary.get('estimated effort hours', 0):,}</div>
                    <div class="metric-description">AI migration hours estimate</div>
                </div>
            """
        
        return f"""
        <section id="metrics" class="section">
            <h2>Key Metrics</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Packages</div>
                    <div class="metric-value">{summary.get('packages', 0)}</div>
                    <div class="metric-description">SSIS packages found</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">AI Analyzed Packages</div>
                    <div class="metric-value">{analyzed_count}</div>
                    <div class="metric-description">Packages analyzed with AI</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Total Components</div>
                    <div class="metric-value">{summary.get('total components', 0):,}</div>
                    <div class="metric-description">Control flow + data flow components</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Connection Managers</div>
                    <div class="metric-value">{summary.get('connection managers', 0)}</div>
                    <div class="metric-description">Database and file connections</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Data Flows</div>
                    <div class="metric-value">{summary.get('data flows', 0):,}</div>
                    <div class="metric-description">ETL transformation pipelines</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Control Flows</div>
                    <div class="metric-value">{summary.get('control flow components', 0):,}</div>
                    <div class="metric-description">Workflow and orchestration tasks</div>
                </div>
                {ai_effort_card}
            </div>
        </section>
        """
    
    def generate_not_supported_section(self) -> str:
        """Generate comprehensive component breakdown section showing all conversion statuses."""
        packages = self.data.get('packages', [])
        
        # Count components by (subtype, type) and status
        component_breakdown = {}  # {(subtype, type): {'Success': count, 'Partial': count, 'NotSupported': count}}
        
        for package in packages:
            # Count from control flow components
            control_flow = package.get('control_flow_components', [])
            for component in control_flow:
                subtype = component.get('subtype', 'Unknown')
                status = component.get('status', 'Unknown')
                key = (subtype, 'Control Flow')
                
                if key not in component_breakdown:
                    component_breakdown[key] = {'Success': 0, 'Partial': 0, 'NotSupported': 0}
                
                if status in ['Success', 'Partial', 'NotSupported']:
                    component_breakdown[key][status] += 1
            
            # Count from data flow components (within each data flow)
            data_flows = package.get('data_flows', [])
            for df in data_flows:
                df_components = df.get('components', [])
                for component in df_components:
                    subtype = component.get('subtype', 'Unknown')
                    status = component.get('status', 'Unknown')
                    key = (subtype, 'Data Flow')
                    
                    if key not in component_breakdown:
                        component_breakdown[key] = {'Success': 0, 'Partial': 0, 'NotSupported': 0}
                    
                    if status in ['Success', 'Partial', 'NotSupported']:
                        component_breakdown[key][status] += 1
        
        # Sort by total count descending
        sorted_components = sorted(
            component_breakdown.items(),
            key=lambda x: sum(x[1].values()),
            reverse=True
        )
        
        # Generate table rows
        rows_html = ""
        for (subtype, comp_type), counts in sorted_components:
            total = counts['Success'] + counts['Partial'] + counts['NotSupported']
            success_pct = (counts['Success'] / total * 100) if total > 0 else 0
            partial_pct = (counts['Partial'] / total * 100) if total > 0 else 0
            not_supported_pct = (counts['NotSupported'] / total * 100) if total > 0 else 0
            
            rows_html += f"""
            <tr class="component-row" data-component-name="{subtype.lower()}" data-component-type="{comp_type.lower()}">
                <td><code style="font-size: 0.85rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px;">{subtype}</code></td>
                <td style="text-align: center;"><span style="display: inline-block; background: #f3f4f6; font-weight: 500; font-size: 0.85rem; padding: 0.25rem 0.5rem; border-radius: 4px;">{comp_type}</span></td>
                <td style="text-align: center; font-weight: 600;">{total}</td>
                <td style="text-align: center; color: #10b981; font-weight: 600;">{counts['Success']}</td>
                <td style="text-align: center; color: #f59e0b; font-weight: 600;">{counts['Partial']}</td>
                <td style="text-align: center; color: #ef4444; font-weight: 600;">{counts['NotSupported']}</td>
                <td>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="flex: 1; display: flex; height: 24px; border-radius: 4px; overflow: hidden; background: #f3f4f6;">
                            <div style="width: {success_pct}%; background: #10b981;" title="Success: {success_pct:.1f}%"></div>
                            <div style="width: {partial_pct}%; background: #f59e0b;" title="Partial: {partial_pct:.1f}%"></div>
                            <div style="width: {not_supported_pct}%; background: #ef4444;" title="Not Supported: {not_supported_pct:.1f}%"></div>
                        </div>
                        <span style="font-size: 0.75rem; color: #6b7280; min-width: 45px;">{success_pct:.0f}%</span>
                    </div>
                </td>
            </tr>
            """
        
        # Calculate totals
        total_success = sum(counts['Success'] for _, counts in component_breakdown.items())
        total_partial = sum(counts['Partial'] for _, counts in component_breakdown.items())
        total_not_supported = sum(counts['NotSupported'] for _, counts in component_breakdown.items())
        grand_total = total_success + total_partial + total_not_supported
        
        success_pct = (total_success / grand_total * 100) if grand_total > 0 else 0
        partial_pct = (total_partial / grand_total * 100) if grand_total > 0 else 0
        not_supported_pct = (total_not_supported / grand_total * 100) if grand_total > 0 else 0
        
        return f"""
        <section id="not-supported" class="section">
            <h2>Component Conversion Breakdown</h2>
            <div class="info-box" style="background: linear-gradient(to right, #f0f9ff, #e0f2fe); border-left: 4px solid {self.COLORS['sf_blue']};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <strong style="font-size: 1.1rem;">Overall Conversion Status</strong>
                        <p style="margin: 0.5rem 0 0 0; color: #475569;">Comprehensive breakdown of all {grand_total:,} components by conversion readiness</p>
                    </div>
                    <div style="display: flex; gap: 1.5rem;">
                        <div style="text-align: center;">
                            <div style="font-size: 1.75rem; font-weight: bold; color: #10b981;">{success_pct:.1f}%</div>
                            <div style="font-size: 0.75rem; color: #059669; text-transform: uppercase;">Success</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.75rem; font-weight: bold; color: #f59e0b;">{partial_pct:.1f}%</div>
                            <div style="font-size: 0.75rem; color: #d97706; text-transform: uppercase;">Partial</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.75rem; font-weight: bold; color: #ef4444;">{not_supported_pct:.1f}%</div>
                            <div style="font-size: 0.75rem; color: #dc2626; text-transform: uppercase;">Not Supported</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 1.5rem;">
                <div style="display: flex; gap: 0.75rem; margin-bottom: 1rem;">
                    <input type="text" id="componentSearch" placeholder="Search components by name..." 
                           style="flex: 1; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; font-size: 0.95rem;"
                           onkeyup="filterComponents()">
                    <select id="typeFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; font-size: 0.95rem; min-width: 180px;" onchange="filterComponents()">
                        <option value="">All Types</option>
                        <option value="data flow">Data Flow</option>
                        <option value="control flow">Control Flow</option>
                    </select>
                </div>
                <div id="componentCount" style="margin-bottom: 0.75rem; color: #6b7280; font-size: 0.875rem;"></div>
            </div>
            
            <table id="componentTable">
                <thead>
                    <tr>
                        <th style="width: 28%;">Component</th>
                        <th style="width: 12%; text-align: center;">Type</th>
                        <th style="width: 8%; text-align: center;">Total</th>
                        <th style="width: 8%; text-align: center;">Success</th>
                        <th style="width: 8%; text-align: center;">Partial</th>
                        <th style="width: 10%; text-align: center;">Not Supported</th>
                        <th style="width: 26%;">Conversion Rate</th>
                    </tr>
                </thead>
                <tbody id="componentTableBody">
                    {rows_html if rows_html else '<tr><td colspan="7" style="text-align: center; color: #6b7280; padding: 2rem;">No component data available.</td></tr>'}
                </tbody>
            </table>
        </section>
        """
    
    def generate_package_summary(self, output_folder: Optional[Path] = None) -> str:
        """Generate package summary table from JSON with links to detail pages."""
        # Calculate classification and complexity distribution
        classification_counts = {}
        complexity_counts = {}
        total_packages = len(self.packages)
        analyzed_count = 0
        pending_count = 0
        
        rows_html = ""
        
        for idx, package in enumerate(self.packages, 1):
            # Get AI analysis data from nested structure
            ai_analysis = package.get('ai_analysis', {})
            classification = ai_analysis.get('classification', 'Unclassified')
            if not classification:  # Handle empty string
                classification = 'Unclassified'
            flags = package.get('flags', {})
            has_scripts = flags.get('has_scripts', False)
            effort = ai_analysis.get('estimated_effort_hours', 'N/A')
            package_name = package.get('name', 'N/A')
            package_path = package.get('path', 'N/A')
            
            # Count analyzed vs pending packages
            analysis_text = ai_analysis.get('analysis', '').strip()
            if analysis_text:
                analyzed_count += 1
            else:
                pending_count += 1
            
            # Get complexity from JSON - only show if package is classified (has AI analysis)
            package_json = self.get_package_data_from_json(package_path)
            complexity = '—'  # Default to dash for unclassified
            if package_json and classification != 'Unclassified':
                complexity = package_json.get('metrics', {}).get('package_complexity', {}).get('complexity', '—')
            
            # Count classifications
            classification_counts[classification] = classification_counts.get(classification, 0) + 1
            
            # Count complexity
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
            
            # Complexity text color - green for easy, yellow for moderate, red for complex
            if complexity in ['Very Easy', 'Easy']:
                complexity_color = '#16a34a'  # Green
            elif complexity == 'Medium':
                complexity_color = '#ca8a04'  # Yellow
            elif complexity in ['Complex', 'Very Complex']:
                complexity_color = '#dc2626'  # Red
            else:
                complexity_color = '#9ca3af'  # Light gray for unclassified/dash
            
            # Indicators/badges column
            indicators_html = ''
            if has_scripts:
                indicators_html = '<span style="display: inline-block; padding: 0.125rem 0.375rem; background: #f3f4f6; color: #374151; border-radius: 3px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;">Scripts</span>'
            
            # Create link to detail page if output folder provided
            display_name = format_display_name(package_name)
            if output_folder:
                detail_filename = f"packages/package_{sanitize_filename(package_name)}.html"
                package_name_html = f'<a href="{detail_filename}" target="_blank" style="text-decoration: none;"><span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500; color: #1f2937;">{display_name} ↗</span></a>'
            else:
                package_name_html = f'<span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">{display_name}</span>'
            
            # Conditionally include effort column
            effort_cell = f'<td style="text-align: center; font-weight: 500;">{effort}</td>' if self.ai_estimation_enabled else ''
            
            # Get AI analysis text for tooltip
            ai_analysis_text = ai_analysis.get('analysis', '').strip()
            
            # Create tooltip content
            if ai_analysis_text:
                # Escape HTML and limit length for tooltip
                tooltip_text = html.escape(ai_analysis_text)
                # Truncate if too long (max 500 chars for tooltip readability)
                if len(tooltip_text) > 500:
                    tooltip_text = tooltip_text[:497] + '...'
                tooltip_html = f'''<div class="ai-tooltip">
                    <div class="ai-tooltip-header">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 16v-4M12 8h.01"/>
                        </svg>
                        AI Analysis
                    </div>
                    <div class="ai-tooltip-content">{tooltip_text}</div>
                </div>'''
            else:
                tooltip_html = '''<div class="ai-tooltip">
                    <div class="ai-tooltip-pending">AI analysis pending</div>
                </div>'''
            
            rows_html += f"""
            <tr class="package-row" data-classification="{classification}" data-complexity="{complexity}" data-name="{package_name.lower()}" data-path="{package_path.lower()}">
                <td style="position: relative;">{package_name_html}{tooltip_html}</td>
                <td><span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">{classification}</span></td>
                <td style="text-align: center;"><span style="display: inline-block; background: #f3f4f6; color: {complexity_color}; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">{complexity}</span></td>
                <td style="text-align: center;">{indicators_html if indicators_html else '<span style="color: #d1d5db;">—</span>'}</td>
                {effort_cell}
            </tr>
            """
        
        # Generate classification and complexity distribution charts (dual donut)
        classification_dist_html = self._generate_classification_and_complexity_charts(classification_counts, complexity_counts, total_packages)
        
        # Generate analysis status summary
        analysis_status_html = ""
        if pending_count > 0:
            analysis_status_html = f"""
            <div class="info-box" style="background-color: #fff3cd; border-left: 4px solid #ffc107; margin-top: 1rem;">
                <strong>Analysis Status:</strong> {analyzed_count} of {total_packages} packages analyzed. 
                {pending_count} package{'s' if pending_count != 1 else ''} pending AI analysis.
            </div>
            """
        else:
            analysis_status_html = f"""
            <div class="info-box" style="background-color: #d1e7dd; border-left: 4px solid #198754; margin-top: 1rem;">
                <strong>Analysis Status:</strong> All {analyzed_count} packages have been analyzed.
            </div>
            """
        
        return f"""
        <section id="package-summary" class="section">
            <h2>Package Classification</h2>
            {analysis_status_html}
            
            <div class="info-box" style="background-color: #f8fafc; border-left: 4px solid #29B5E8; margin-top: 1rem;">
                <strong>Classification Guide:</strong>
                <ul style="margin: 0.5rem 0 0 1.25rem; line-height: 1.6;">
                    <li><strong>Ingestion:</strong> Packages that extract data from external sources (files, APIs, FTP, external databases) into the data platform. These packages are not candidates for dbt on Snowflake since dbt cannot connect to external sources; use alternatives like Snowflake Openflow, Snowpipe, or Fivetran.</li>
                    <li><strong>Data Transformation:</strong> Packages that transform data between internal database layers. Good candidates to migrate with SnowConvert AI to dbt projects on Snowflake, with control flow elements converting to Snowflake Tasks and Snowflake Scripting.</li>
                    <li><strong>Mixed: Ingestion + Transformation:</strong> Packages that both ingest data from external sources and apply transformations within the same workflow. Decompose into separate Snowflake ingestion (Snowpipe/Tasks) and dbt transformation layers.</li>
                    <li><strong>Configuration &amp; Control:</strong> Packages focused on orchestration, metadata management, or system operations rather than moving business data. Often contain foreach loops, file tasks, script tasks, and execute package tasks. Migrate to Snowflake Tasks and Snowflake Scripting, or re-architect based on use case.</li>
                    <li><strong>Unclassified:</strong> Pending AI analysis.</li>
                </ul>
            </div>

            {classification_dist_html}
            
            <div style="margin: 1.5rem 0;">
                <input type="text" id="packageSearch" placeholder="Search by package name..." 
                       style="width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; margin-bottom: 0.75rem; font-size: 0.95rem;">
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    <select id="classificationFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; flex: 1; min-width: 200px;">
                        <option value="">All Classifications</option>
                        <option value="Ingestion">Ingestion</option>
                        <option value="Data Transformation">Data Transformation</option>
                        <option value="Mixed: Ingestion + Transformation">Mixed: Ingestion + Transformation</option>
                        <option value="Configuration & Control">Configuration & Control</option>
                    </select>
                    <select id="complexityFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; flex: 1; min-width: 200px;">
                        <option value="">All Complexity Levels</option>
                        <option value="Very Easy">Very Easy</option>
                        <option value="Easy">Easy</option>
                        <option value="Medium">Medium</option>
                        <option value="Complex">Complex</option>
                        <option value="Very Complex">Very Complex</option>
                    </select>
                    <button onclick="resetPackageFilters()" style="padding: 0.75rem 1.5rem; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-weight: 600;">
                        Reset Filters
                    </button>
                </div>
                <div id="packageCount" style="margin-top: 0.75rem; color: #6b7280; font-size: 0.875rem;"></div>
            </div>
            
            <table id="packageTable">
                <thead>
                    <tr>
                        <th style="width: {'32%' if not self.ai_estimation_enabled else '30%'};">Package Name</th>
                        <th style="width: {'28%' if not self.ai_estimation_enabled else '24%'};">Classification</th>
                        <th style="width: {'20%' if not self.ai_estimation_enabled else '16%'}; text-align: center;">Complexity</th>
                        <th style="width: {'20%' if not self.ai_estimation_enabled else '15%'}; text-align: center;">Indicators</th>
                        {'<th style="width: 15%; text-align: center;">AI Effort (hrs)</th>' if self.ai_estimation_enabled else ''}
                    </tr>
                </thead>
                <tbody id="packageTableBody">
                    {rows_html}
                </tbody>
            </table>
        </section>
        """
    
    def _generate_donut_chart_svg(self, data: Dict[str, int], colors: Dict[str, str], size: int = 160, hole_ratio: float = 0.6) -> str:
        """Generate an SVG donut chart.
        
        Args:
            data: Dictionary of {label: count}
            colors: Dictionary of {label: color}
            size: Size of the SVG in pixels
            hole_ratio: Ratio of the inner hole (0.0 to 1.0)
        
        Returns:
            SVG string for the donut chart
        """
        import math
        
        total = sum(data.values())
        if total == 0:
            # Empty state
            return f'''
                <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
                    <circle cx="{size/2}" cy="{size/2}" r="{size/2 - 5}" fill="#f3f4f6" stroke="#e5e7eb" stroke-width="2"/>
                    <text x="{size/2}" y="{size/2}" text-anchor="middle" dominant-baseline="middle" fill="#9ca3af" font-size="12">No data</text>
                </svg>
            '''
        
        center = size / 2
        radius = (size / 2) - 5
        inner_radius = radius * hole_ratio
        
        paths = []
        start_angle = -90  # Start from top
        
        for label, count in data.items():
            if count == 0:
                continue
                
            percentage = count / total
            angle = percentage * 360
            end_angle = start_angle + angle
            
            # Convert angles to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate arc points
            x1_outer = center + radius * math.cos(start_rad)
            y1_outer = center + radius * math.sin(start_rad)
            x2_outer = center + radius * math.cos(end_rad)
            y2_outer = center + radius * math.sin(end_rad)
            
            x1_inner = center + inner_radius * math.cos(end_rad)
            y1_inner = center + inner_radius * math.sin(end_rad)
            x2_inner = center + inner_radius * math.cos(start_rad)
            y2_inner = center + inner_radius * math.sin(start_rad)
            
            # Large arc flag
            large_arc = 1 if angle > 180 else 0
            
            color = colors.get(label, '#9ca3af')
            
            # Create path for arc segment
            path = f'''
                <path d="M {x1_outer} {y1_outer} 
                         A {radius} {radius} 0 {large_arc} 1 {x2_outer} {y2_outer}
                         L {x1_inner} {y1_inner}
                         A {inner_radius} {inner_radius} 0 {large_arc} 0 {x2_inner} {y2_inner}
                         Z"
                      fill="{color}" stroke="white" stroke-width="2"/>
            '''
            paths.append(path)
            
            start_angle = end_angle
        
        paths_html = ''.join(paths)
        
        return f'''
            <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display: block;">
                {paths_html}
                <circle cx="{center}" cy="{center}" r="{inner_radius - 2}" fill="white"/>
                <text x="{center}" y="{center - 8}" text-anchor="middle" dominant-baseline="middle" fill="#1f2937" font-size="20" font-weight="bold">{total}</text>
                <text x="{center}" y="{center + 10}" text-anchor="middle" dominant-baseline="middle" fill="#6b7280" font-size="11">packages</text>
            </svg>
        '''
    
    def _generate_donut_legend(self, data: Dict[str, int], colors: Dict[str, str], total: int, descriptions: Dict[str, str] = None) -> str:
        """Generate legend for donut chart.
        
        Args:
            data: Dictionary of {label: count}
            colors: Dictionary of {label: color}
            total: Total count for percentage calculation
            descriptions: Optional dictionary of {label: description} for detailed legends
        """
        legend_items = []
        for label, count in data.items():
            if count == 0:
                continue
            percentage = (count / total * 100) if total > 0 else 0
            color = colors.get(label, '#9ca3af')
            
            # Check if we have a description for this label
            description = descriptions.get(label, '') if descriptions else ''
            
            if description:
                # Detailed legend with description
                legend_items.append(f'''
                    <div style="display: flex; gap: 0.5rem; font-size: 0.8rem; padding: 0.375rem 0;">
                        <span style="width: 12px; height: 12px; background: {color}; border-radius: 3px; flex-shrink: 0; margin-top: 2px;"></span>
                        <div style="flex: 1;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: #1f2937; font-weight: 600;">{label}</span>
                                <span style="color: #6b7280; font-weight: 500; margin-left: 0.5rem;">{count} ({percentage:.0f}%)</span>
                            </div>
                            <div style="color: #64748b; font-size: 0.7rem; line-height: 1.3; margin-top: 2px;">{description}</div>
                        </div>
                    </div>
                ''')
            else:
                # Simple legend without description
                legend_items.append(f'''
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem;">
                        <span style="width: 12px; height: 12px; background: {color}; border-radius: 3px; flex-shrink: 0;"></span>
                        <span style="color: #374151; flex: 1;">{label}</span>
                        <span style="color: #6b7280; font-weight: 500;">{count} ({percentage:.0f}%)</span>
                    </div>
                ''')
        
        return f'''
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                {''.join(legend_items)}
            </div>
        '''
    
    def _generate_classification_and_complexity_charts(self, classification_counts: Dict, complexity_counts: Dict, total: int) -> str:
        """Generate dual donut charts for classification and complexity distribution."""
        classification_colors = {
            'Ingestion': self.COLORS['sf_blue'],
            'Data Transformation': self.COLORS['warning'],
            'Mixed: Ingestion + Transformation': '#8B5CF6',
            'Configuration & Control': self.COLORS['success'],
            'Unclassified': self.COLORS['sf_gray']
        }
        
        complexity_colors = {
            'Very Easy': '#22c55e',
            'Easy': '#4ade80',
            'Medium': '#facc15',
            'Complex': '#f97316',
            'Very Complex': '#ef4444',
            '—': '#d1d5db'
        }
        
        # Order the data for consistent display
        ordered_classification = {}
        for key in ['Ingestion', 'Data Transformation', 'Mixed: Ingestion + Transformation', 'Configuration & Control', 'Unclassified']:
            if classification_counts.get(key, 0) > 0:
                ordered_classification[key] = classification_counts.get(key, 0)
        
        ordered_complexity = {}
        for key in ['Very Easy', 'Easy', 'Medium', 'Complex', 'Very Complex', '—']:
            if complexity_counts.get(key, 0) > 0:
                ordered_complexity[key] = complexity_counts.get(key, 0)
        
        # Generate SVG donut charts
        classification_donut = self._generate_donut_chart_svg(ordered_classification, classification_colors, size=150)
        complexity_donut = self._generate_donut_chart_svg(ordered_complexity, complexity_colors, size=150)
        
        # Generate simple legends (no descriptions - Classification Guide info-box provides details)
        classification_legend = self._generate_donut_legend(ordered_classification, classification_colors, total)
        complexity_legend = self._generate_donut_legend(ordered_complexity, complexity_colors, total)
        
        return f"""
        <div style="margin: 1.5rem 0;">
            <h3 style="margin-bottom: 1rem; color: #1f2937;">Package Distribution</h3>
            <div class="chart-container" style="padding: 1.5rem 2rem;">
                <div style="display: flex; justify-content: space-evenly; align-items: stretch; flex-wrap: wrap; gap: 2rem;">
                    <!-- Classification Donut -->
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 1; min-width: 320px; max-width: 450px;">
                        <div style="font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">By Classification</div>
                        <div style="display: flex; align-items: center; gap: 1.5rem;">
                            <div style="flex-shrink: 0;">{classification_donut}</div>
                            <div style="flex: 1; min-width: 160px;">{classification_legend}</div>
                        </div>
                    </div>
                    
                    <!-- Vertical Divider -->
                    <div style="width: 1px; background: linear-gradient(180deg, transparent 0%, #e2e8f0 15%, #e2e8f0 85%, transparent 100%); align-self: stretch; min-height: 120px;"></div>
                    
                    <!-- Complexity Donut -->
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 1; min-width: 320px; max-width: 450px;">
                        <div style="font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">By Complexity</div>
                        <div style="display: flex; align-items: center; gap: 1.5rem;">
                            <div style="flex-shrink: 0;">{complexity_donut}</div>
                            <div style="flex: 1; min-width: 160px;">{complexity_legend}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_classification_distribution(self, classification_counts: Dict, total: int) -> str:
        """Generate classification distribution chart - now redirects to dual donut charts."""
        # This method is kept for backwards compatibility but now uses donut charts
        # Complexity counts are passed as empty since this is the old method signature
        return self._generate_classification_and_complexity_charts(classification_counts, {}, total)
    
    def get_package_data_from_json(self, package_path: str) -> Optional[Dict]:
        """Get package data from JSON by path."""
        packages = self.data.get('packages', [])
        for pkg in packages:
            if pkg.get('path') == package_path:
                return pkg
        return None
    
    def _parse_connection_manager_info(self, additional_info: str) -> str:
        """Parse connection manager additional_info JSON to extract creationName."""
        try:
            import json
            info = json.loads(additional_info)
            creation_name = info.get('creationName', '')
            # Simplify long .NET type names
            if 'ADO.NET:' in creation_name:
                parts = creation_name.split(':')
                if len(parts) > 1:
                    type_parts = parts[1].split(',')
                    return f"ADO.NET ({type_parts[0].split('.')[-1]})"
            return creation_name if creation_name else 'Unknown'
        except:
            return 'Unknown'
    
    def _get_component_status_from_subtype(self, subtype: str, metrics: Dict) -> str:
        """Determine component status based on not_supported_elements."""
        not_supported = metrics.get('not_supported_elements', {}).get('component_types', [])
        if subtype in not_supported:
            return 'NotSupported'
        # Check if it's in the status_summary
        status_summary = metrics.get('status_summary', {})
        # This is a simplification - in reality we'd need more logic
        # For now, assume if not in not_supported, it's either Success or Partial
        if 'Event' in subtype:
            return 'Partial'
        return 'Success'
    
    def _generate_progress_bar(self, success_rate: float, partial_rate: float, not_supported_rate: float,
                                success_count: int, partial_count: int, not_supported_count: int) -> str:
        """Generate a progress bar showing conversion rates."""
        # Don't show percentage if less than 5%
        success_label = f"{success_rate:.1f}%" if success_rate >= 5 else ""
        partial_label = f"{partial_rate:.1f}%" if partial_rate >= 5 else ""
        not_supported_label = f"{not_supported_rate:.1f}%" if not_supported_rate >= 5 else ""
        
        return f"""
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.875rem;">
                <span><strong>Success:</strong> {success_count} ({success_rate:.1f}%)</span>
                <span><strong>Partial:</strong> {partial_count} ({partial_rate:.1f}%)</span>
                <span><strong>Not Supported:</strong> {not_supported_count} ({not_supported_rate:.1f}%)</span>
            </div>
            <div style="display: flex; height: 30px; border-radius: 4px; overflow: hidden; background: #e5e7eb;">
                <div style="width: {success_rate}%; background: #10b981; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75rem; font-weight: bold;">{success_label}</div>
                <div style="width: {partial_rate}%; background: #f59e0b; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75rem; font-weight: bold;">{partial_label}</div>
                <div style="width: {not_supported_rate}%; background: #ef4444; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75rem; font-weight: bold;">{not_supported_label}</div>
            </div>
        </div>
        """
    
    def _generate_subtype_table(self, subtype_summary: Dict) -> str:
        """Generate table showing component subtypes without status."""
        if not subtype_summary:
            return "<p>No component breakdown available.</p>"
        
        rows = ""
        for subtype, count in sorted(subtype_summary.items(), key=lambda x: x[1], reverse=True):
            rows += f"""
            <tr>
                <td><code style="font-size: 0.85rem;">{subtype}</code></td>
                <td style="text-align: center; font-weight: 600;">{count}</td>
            </tr>
            """
        
        return f"""
        <table>
            <thead>
                <tr>
                    <th>Component Type</th>
                    <th style="width: 120px; text-align: center;">Count</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
    
    def _generate_package_not_supported_section(self, not_supported_elements: Dict) -> str:
        """Generate not supported section for package detail page with chip-based display."""
        component_types = not_supported_elements.get('component_types', [])
        total_count = not_supported_elements.get('total_count', 0)
        
        # Don't show section if no unsupported components
        if not component_types or total_count == 0:
            return ""
        
        chips_html = ""
        for comp_type in component_types:
            chips_html += f'''
                <span style="display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem; 
                             background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; font-size: 0.8rem;">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                    <code style="color: #991b1b;">{comp_type}</code>
                </span>
            '''
        
        return f'''
            <div class="detail-card" style="margin-top: 1rem; border-color: #fecaca;">
                <div class="detail-card-header" onclick="toggleDetailCard('not-supported-content', this)" style="background: #fef2f2; border-bottom-color: #fecaca;">
                    <div class="detail-card-title" style="color: #991b1b;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
                            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                        </svg>
                        Not Supported Components
                        <span style="background: #fee2e2; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #991b1b; font-weight: 500;">{total_count}</span>
                    </div>
                    <span class="toggle-icon" style="color: #f87171; font-size: 0.875rem;">▶</span>
                </div>
                <div id="not-supported-content" class="detail-card-content" style="display: none;">
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        {chips_html}
                    </div>
                    <p style="margin: 1rem 0 0 0; font-size: 0.8rem; color: #6b7280;">
                        These components require manual migration or alternative approaches.
                    </p>
                </div>
            </div>
        '''
    
    def _generate_package_connection_managers(self, connection_managers: list, total_cm: int) -> str:
        """Generate connection managers section for package detail page with styled N/A state."""
        if not connection_managers or total_cm == 0:
            return '''
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; 
                            padding: 2rem; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1;">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" style="margin-bottom: 0.5rem;">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="8" y1="12" x2="16" y2="12"/>
                    </svg>
                    <div style="font-size: 0.9rem; font-weight: 500; color: #64748b;">No Connection Managers</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">
                        This package uses inherited or external connections
                    </div>
                </div>
            '''
        
        cm_items = ""
        for cm in connection_managers:
            name = cm.get('full_name', 'Unknown')
            additional_info = cm.get('additional_info', '')
            cm_type = self._parse_connection_manager_info(additional_info)
            
            # Connection type icon color based on type
            icon_color = '#3b82f6'
            if 'OLEDB' in cm_type.upper():
                icon_color = '#f59e0b'
            elif 'ADO' in cm_type.upper():
                icon_color = '#8b5cf6'
            elif 'FILE' in cm_type.upper() or 'FLAT' in cm_type.upper():
                icon_color = '#10b981'
            
            cm_items += f'''
                <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem; 
                            background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, {icon_color}22, {icon_color}11); 
                                border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{icon_color}" stroke-width="2">
                            <ellipse cx="12" cy="5" rx="9" ry="3"/>
                            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                        </svg>
                    </div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 600; color: #1e293b; font-size: 0.875rem; word-break: break-word;">{name}</div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.125rem;">
                            <code style="background: #e2e8f0; padding: 0.125rem 0.375rem; border-radius: 4px; font-size: 0.7rem;">{cm_type}</code>
                        </div>
                    </div>
                </div>
            '''
        
        return f'''
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                {cm_items}
            </div>
        '''
    
    def _generate_data_flows_section(self, data_flows: list, total_df: int, dag_base_path: str = "..") -> str:
        """Generate data flows section with DAG links for package detail page."""
        if not data_flows or total_df == 0:
            return '''
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; 
                            padding: 2rem; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1;">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" style="margin-bottom: 0.5rem;">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="8" y1="12" x2="16" y2="12"/>
                    </svg>
                    <div style="font-size: 0.9rem; font-weight: 500; color: #64748b;">No Data Flows</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">
                        This package does not contain data flow pipelines
                    </div>
                </div>
            '''
        
        df_items = ""
        for df in data_flows:
            df_name = df.get('name', 'Data Flow')
            dag_file = df.get('dag_file', '')
            df_metrics = df.get('metrics', {})
            
            # Get metrics
            total_components = df_metrics.get('total_components', 0)
            conversion_rates = df_metrics.get('conversion_rates', {})
            success_rate = conversion_rates.get('success_rate', 0)
            
            # Status color
            if success_rate >= 90:
                status_color = '#16a34a'
                status_bg = '#dcfce7'
            elif success_rate >= 70:
                status_color = '#ca8a04'
                status_bg = '#fef9c3'
            else:
                status_color = '#dc2626'
                status_bg = '#fee2e2'
            
            # DAG link
            dag_link = ""
            if dag_file:
                dag_link = f'''
                    <a href="{dag_base_path}/{dag_file}" target="_blank" 
                       style="display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.5rem 0.875rem; 
                              background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; 
                              text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.8rem;
                              box-shadow: 0 2px 4px rgba(59, 130, 246, 0.25); transition: all 0.2s; flex-shrink: 0;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="3"></circle>
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
                        </svg>
                        View DAG
                    </a>
                '''
            
            df_items += f'''
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.875rem 1rem; 
                            background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 600; color: #1e293b; font-size: 0.875rem; margin-bottom: 0.25rem; word-break: break-word;">{df_name}</div>
                        <div style="display: flex; align-items: center; gap: 0.75rem; font-size: 0.75rem; color: #64748b;">
                            <span>{total_components} components</span>
                            <span style="background: {status_bg}; color: {status_color}; padding: 0.125rem 0.5rem; border-radius: 99px; font-weight: 600;">{success_rate:.0f}% success</span>
                        </div>
                    </div>
                    {dag_link}
                </div>
            '''
        
        return f'''
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                {df_items}
            </div>
        '''
    
    def generate_package_detail_page(self, package_csv_row: Dict, package_json_data: Dict, main_report_filename: str = "index.html", dag_base_path: str = "..") -> str:
        """Generate individual package detail HTML page with improved UI structure.
        
        Args:
            package_csv_row: Package data dictionary from the analysis.
            package_json_data: Package JSON data with metrics and components.
            main_report_filename: Filename of the main report for the back link (default: index.html).
            dag_base_path: Relative path from the packages/ directory to the directory containing the dags/ folder.
        """
        package_name = package_csv_row.get('name', 'Unknown')
        display_name = format_display_name(package_name)
        package_path = package_csv_row.get('path', '')
        display_path = unquote(package_path)
        
        # Get AI analysis from nested structure
        ai_analysis_obj = package_csv_row.get('ai_analysis', {})
        classification = ai_analysis_obj.get('classification', 'Unclassified')
        if not classification:  # Handle empty string
            classification = 'Unclassified'
        flags = package_csv_row.get('flags', {})
        has_scripts = flags.get('has_scripts', False)
        effort = ai_analysis_obj.get('estimated_effort_hours', 'N/A')
        ai_analysis = ai_analysis_obj.get('analysis', '')
        
        metrics = package_json_data.get('metrics', {})
        complexity_data = metrics.get('package_complexity', {})
        complexity = complexity_data.get('complexity', '—') if classification != 'Unclassified' else '—'
        connection_managers = package_json_data.get('connection_managers', [])
        data_flows = package_json_data.get('data_flows', [])
        control_flow_dag_file = package_json_data.get('control_flow_dag_file', '')
        
        # Metrics
        total_components = metrics.get('total_components', 0)
        total_cm = metrics.get('total_connection_managers', 0)
        total_df = metrics.get('total_data_flows', 0)
        total_df_components = metrics.get('total_data_flow_components', 0)
        total_cf_components = metrics.get('total_control_flow_components', 0)
        
        # Conversion rates
        conversion_rates = metrics.get('conversion_rates', {})
        success_rate = conversion_rates.get('success_rate', 0)
        partial_rate = conversion_rates.get('partial_rate', 0)
        not_supported_rate = conversion_rates.get('not_supported_rate', 0)
        
        # Status summary
        status_summary = metrics.get('status_summary', {})
        success_count = status_summary.get('Success', 0)
        partial_count = status_summary.get('Partial', 0)
        not_supported_count = status_summary.get('NotSupported', 0)
        
        # Classification styling
        classification_styles = {
            'Ingestion': {'bg': '#dbeafe', 'color': '#1e40af', 'border': '#3b82f6'},
            'Data Transformation': {'bg': '#fef3c7', 'color': '#92400e', 'border': '#f59e0b'},
            'Mixed: Ingestion + Transformation': {'bg': '#ede9fe', 'color': '#5b21b6', 'border': '#8B5CF6'},
            'Configuration & Control': {'bg': '#d1fae5', 'color': '#065f46', 'border': '#10b981'},
            'Unclassified': {'bg': '#f3f4f6', 'color': '#6b7280', 'border': '#9ca3af'}
        }
        class_style = classification_styles.get(classification, classification_styles['Unclassified'])
        
        # Complexity styling
        complexity_styles = {
            'Very Easy': {'bg': '#d1fae5', 'color': '#065f46'},
            'Easy': {'bg': '#d1fae5', 'color': '#065f46'},
            'Medium': {'bg': '#fef3c7', 'color': '#92400e'},
            'Complex': {'bg': '#fee2e2', 'color': '#991b1b'},
            'Very Complex': {'bg': '#fee2e2', 'color': '#991b1b'},
            '—': {'bg': '#f3f4f6', 'color': '#6b7280'}
        }
        comp_style = complexity_styles.get(complexity, complexity_styles['—'])
        
        # Control flow DAG button
        dag_button_html = ""
        if control_flow_dag_file:
            dag_button_html = f'''
                <a href="{dag_base_path}/{control_flow_dag_file}" target="_blank" 
                   style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1rem; 
                          background: linear-gradient(135deg, #8B5CF6, #7C3AED); color: white; 
                          text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 0.875rem;
                          box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3); transition: all 0.2s;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
                    </svg>
                    View Control Flow DAG
                </a>
            '''
        
        # Script indicator
        script_indicator = ""
        if has_scripts:
            script_indicator = '''
                <div style="display: flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem; 
                            background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
                        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                    <span style="font-size: 0.75rem; font-weight: 600; color: #dc2626; text-transform: uppercase;">Contains Scripts</span>
                </div>
            '''
        
        # Subtype summary table
        subtype_summary = metrics.get('subtype_summary', {})
        subtype_table_html = self._generate_subtype_table(subtype_summary)
        
        # Not supported elements
        not_supported_elements = metrics.get('not_supported_elements', {})
        not_supported_html = self._generate_package_not_supported_section(not_supported_elements)
        
        # Connection managers
        cm_html = self._generate_package_connection_managers(connection_managers, total_cm)
        
        # Data flows
        df_html = self._generate_data_flows_section(data_flows, total_df, dag_base_path=dag_base_path)
        
        # AI Analysis section - only show if there's actual analysis
        ai_analysis_content = ""
        if ai_analysis and ai_analysis.strip():
            ai_analysis_content = f'''
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; line-height: 1.7;">
                    <p style="margin: 0; color: #334155; white-space: pre-wrap;">{ai_analysis}</p>
                </div>
            '''
        else:
            ai_analysis_content = '''
                <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 2rem; text-align: center;">
                    <div style="color: #94a3b8; font-size: 0.875rem;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin: 0 auto 0.5rem; display: block; opacity: 0.5;">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 16v-4M12 8h.01"/>
                        </svg>
                        AI analysis pending
                    </div>
                </div>
            '''
        
        # Generate sidebar navigation
        sidebar_nav = f"""
        <div class="sidebar" style="position: fixed; left: 0; top: 0; width: 260px; height: 100vh; background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); color: white; padding: 1.5rem; overflow-y: auto; z-index: 1000; box-shadow: 4px 0 24px rgba(0,0,0,0.15);">
            <div style="margin-bottom: 2rem;">
                <a href="../{main_report_filename}" style="color: white; text-decoration: none; font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; transition: all 0.2s;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 12H5M12 19l-7-7 7-7"/>
                    </svg>
                    Back to Main Report
                </a>
            </div>
            <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(148, 163, 184, 0.2);">
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 0.5rem;">Package</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #f1f5f9; word-break: break-word;">{display_name}</div>
            </div>
            <nav style="display: flex; flex-direction: column; gap: 0.25rem;">
                <a href="#header" class="nav-link" style="display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 0.875rem; color: #cbd5e1; text-decoration: none; border-radius: 6px; font-size: 0.875rem; transition: all 0.15s;">
                    <span style="width: 6px; height: 6px; background: #3b82f6; border-radius: 50%;"></span>
                    Overview
                </a>
                <a href="#ai-analysis" class="nav-link" style="display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 0.875rem; color: #cbd5e1; text-decoration: none; border-radius: 6px; font-size: 0.875rem; transition: all 0.15s;">
                    <span style="width: 6px; height: 6px; background: #8b5cf6; border-radius: 50%;"></span>
                    AI Analysis
                </a>
                <a href="#details" class="nav-link" style="display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 0.875rem; color: #cbd5e1; text-decoration: none; border-radius: 6px; font-size: 0.875rem; transition: all 0.15s;">
                    <span style="width: 6px; height: 6px; background: #10b981; border-radius: 50%;"></span>
                    Package Details
                </a>
            </nav>
        </div>
        """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_name} - Package Detail</title>
    <style>
        {self.generate_css()}
        
        .nav-link:hover {{ background: rgba(59, 130, 246, 0.15) !important; color: #60a5fa !important; }}
        .nav-link.active {{ background: rgba(59, 130, 246, 0.2) !important; color: #60a5fa !important; }}
        
        .detail-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            transition: box-shadow 0.2s;
        }}
        .detail-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .detail-card-header {{
            padding: 1rem 1.25rem;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }}
        .detail-card-header:hover {{
            background: #f1f5f9;
        }}
        .detail-card-title {{
            font-weight: 600;
            color: #1e293b;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .detail-card-content {{
            padding: 1.25rem;
        }}
        
        .stat-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            text-align: center;
            transition: all 0.2s;
        }}
        .stat-card:hover {{
            border-color: #cbd5e1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        .stat-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.2;
        }}
        .stat-label {{
            font-size: 0.75rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.375rem;
        }}
        .stat-na {{
            color: #94a3b8;
            font-size: 1.25rem;
        }}
    </style>
</head>
<body>
    {sidebar_nav}
    
    <div class="content" style="margin-left: 280px; max-width: 1100px; padding: 2rem 2.5rem;">
        
        <!-- HEADER SECTION -->
        <section id="header" style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <h1 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem 0; line-height: 1.3;">{display_name}</h1>
                    <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                        <code style="background: #f1f5f9; padding: 0.375rem 0.75rem; border-radius: 6px; font-size: 0.8rem; color: #475569; border: 1px solid #e2e8f0;">{display_path}</code>
                        {script_indicator}
                    </div>
                </div>
                <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
                    {dag_button_html}
                </div>
            </div>
            
            <!-- Classification & Complexity Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: {class_style['bg']}; border: 1px solid {class_style['border']}; border-radius: 10px; padding: 1rem 1.25rem;">
                    <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: {class_style['color']}; opacity: 0.8; margin-bottom: 0.375rem;">Classification</div>
                    <div style="font-size: 1rem; font-weight: 600; color: {class_style['color']};">{classification}</div>
                </div>
                <div style="background: {comp_style['bg']}; border: 1px solid {'#d1d5db' if complexity == '—' else comp_style['bg']}; border-radius: 10px; padding: 1rem 1.25rem;">
                    <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: {comp_style['color']}; opacity: 0.8; margin-bottom: 0.375rem;">Complexity</div>
                    <div style="font-size: 1rem; font-weight: 600; color: {comp_style['color']};">{complexity}</div>
                </div>
                {'<div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 1rem 1.25rem;"><div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #1e40af; opacity: 0.8; margin-bottom: 0.375rem;">AI Effort Estimate</div><div style="font-size: 1rem; font-weight: 600; color: #1e40af;">' + str(effort) + ' hours</div></div>' if self.ai_estimation_enabled else ''}
            </div>
        </section>
        
        <!-- QUICK STATS BAR -->
        <section style="margin-bottom: 2rem;">
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem;">
                <div class="stat-card">
                    <div class="stat-value">{total_components}</div>
                    <div class="stat-label">Total Components</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_df}</div>
                    <div class="stat-label">Data Flows</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_cf_components}</div>
                    <div class="stat-label">Control Flow</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value {'stat-na' if total_cm == 0 else ''}">{total_cm if total_cm > 0 else 'N/A'}</div>
                    <div class="stat-label">Connections</div>
                </div>
                <div class="stat-card" style="border-color: {'#bbf7d0' if success_rate >= 90 else '#fde68a' if success_rate >= 70 else '#fecaca'};">
                    <div class="stat-value" style="color: {'#16a34a' if success_rate >= 90 else '#ca8a04' if success_rate >= 70 else '#dc2626'};">{success_rate:.0f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </section>
        
        <!-- AI ANALYSIS SECTION -->
        <section id="ai-analysis" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2">
                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #1e293b;">AI Analysis</h2>
            </div>
            {ai_analysis_content}
            
            <!-- Conversion Progress Bar -->
            <div style="margin-top: 1.25rem; background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="font-size: 0.875rem; font-weight: 600; color: #475569;">Conversion Status</span>
                    <div style="display: flex; gap: 1.5rem; font-size: 0.8rem;">
                        <span style="color: #16a34a;"><strong>{success_count}</strong> Success</span>
                        <span style="color: #ca8a04;"><strong>{partial_count}</strong> Partial</span>
                        <span style="color: #dc2626;"><strong>{not_supported_count}</strong> Not Supported</span>
                    </div>
                </div>
                <div style="display: flex; height: 10px; border-radius: 5px; overflow: hidden; background: #f1f5f9;">
                    <div style="width: {success_rate}%; background: linear-gradient(90deg, #22c55e, #16a34a);"></div>
                    <div style="width: {partial_rate}%; background: linear-gradient(90deg, #fbbf24, #f59e0b);"></div>
                    <div style="width: {not_supported_rate}%; background: linear-gradient(90deg, #f87171, #ef4444);"></div>
                </div>
            </div>
            
            <!-- Not Supported Elements (collapsed by default) -->
            {not_supported_html}
        </section>
        
        <!-- PACKAGE DETAILS GRID -->
        <section id="details" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                </svg>
                <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #1e293b;">Package Details</h2>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <!-- Connection Managers -->
                <div class="detail-card">
                    <div class="detail-card-header" onclick="toggleDetailCard('cm-content', this)">
                        <div class="detail-card-title">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2">
                                <path d="M18 20V10M18 10l-6-6-6 6M6 20V10"/>
                            </svg>
                            Connection Managers
                            <span style="background: #f1f5f9; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #64748b; font-weight: 500;">{total_cm if total_cm > 0 else 'N/A'}</span>
                        </div>
                        <span class="toggle-icon" style="color: #94a3b8; font-size: 0.875rem;">▶</span>
                    </div>
                    <div id="cm-content" class="detail-card-content" style="display: none;">
                        {cm_html}
                    </div>
                </div>
                
                <!-- Component Breakdown -->
                <div class="detail-card">
                    <div class="detail-card-header" onclick="toggleDetailCard('breakdown-content', this)">
                        <div class="detail-card-title">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2">
                                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                                <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                            </svg>
                            Component Breakdown
                        </div>
                        <span class="toggle-icon" style="color: #94a3b8; font-size: 0.875rem;">▶</span>
                    </div>
                    <div id="breakdown-content" class="detail-card-content" style="display: none;">
                        {subtype_table_html}
                    </div>
                </div>
            </div>
            
            <!-- Data Flows (full width) -->
            <div class="detail-card" style="margin-top: 1rem;">
                <div class="detail-card-header" onclick="toggleDetailCard('df-content', this)">
                    <div class="detail-card-title">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
                            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                        </svg>
                        Data Flows
                        <span style="background: #dbeafe; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #1e40af; font-weight: 500;">{total_df if total_df > 0 else 'N/A'}</span>
                    </div>
                    <span class="toggle-icon" style="color: #94a3b8; font-size: 0.875rem;">▶</span>
                </div>
                <div id="df-content" class="detail-card-content" style="display: none;">
                    {df_html}
                </div>
            </div>
        </section>
    </div>
    
    <script>
        // Toggle detail card sections
        function toggleDetailCard(contentId, header) {{
            const content = document.getElementById(contentId);
            const icon = header.querySelector('.toggle-icon');
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                icon.textContent = '▼';
            }} else {{
                content.style.display = 'none';
                icon.textContent = '▶';
            }}
        }}
        
        // Smooth scroll for navigation links
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    
    def generate_html(self, output_folder: Optional[Path] = None) -> str:
        """Generate complete HTML report."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSIS Assessment Report</title>
    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    {self.generate_header()}
    {self.generate_executive_summary()}
    {self.generate_metrics_section()}
    {self.generate_package_summary(output_folder)}
    {self.generate_not_supported_section()}
    
    </main>
    
    <script>
        // Smooth scroll for navigation links
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    
                    // Update active state
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                }}
            }});
        }});
        
        // Set initial active state
        document.querySelector('.nav-link').classList.add('active');
        
        // Package Search and Filter Functionality
        function filterPackages() {{
            const searchTerm = document.getElementById('packageSearch')?.value.toLowerCase() || '';
            const classificationFilter = document.getElementById('classificationFilter')?.value || '';
            const complexityFilter = document.getElementById('complexityFilter')?.value || '';
            
            const rows = document.querySelectorAll('.package-row');
            let visibleCount = 0;
            
            rows.forEach(row => {{
                const name = row.getAttribute('data-name') || '';
                const classification = row.getAttribute('data-classification') || '';
                const complexity = row.getAttribute('data-complexity') || '';
                
                const matchesSearch = name.includes(searchTerm);
                const matchesClassification = !classificationFilter || classification === classificationFilter;
                const matchesComplexity = !complexityFilter || complexity === complexityFilter;
                
                if (matchesSearch && matchesClassification && matchesComplexity) {{
                    row.style.display = '';
                    visibleCount++;
                }} else {{
                    row.style.display = 'none';
                }}
            }});
            
            // Update count display
            const totalCount = rows.length;
            const countElement = document.getElementById('packageCount');
            if (countElement) {{
                countElement.textContent = `Showing ${{visibleCount}} of ${{totalCount}} packages`;
            }}
        }}
        
        function resetPackageFilters() {{
            document.getElementById('packageSearch').value = '';
            document.getElementById('classificationFilter').value = '';
            document.getElementById('complexityFilter').value = '';
            filterPackages();
        }}
        
        // Component Search and Filter Functionality
        function filterComponents() {{
            const searchTerm = document.getElementById('componentSearch').value.toLowerCase();
            const typeFilter = document.getElementById('typeFilter').value.toLowerCase();
            const rows = document.querySelectorAll('.component-row');
            let visibleCount = 0;
            
            rows.forEach(row => {{
                const componentName = row.getAttribute('data-component-name');
                const componentType = row.getAttribute('data-component-type');
                
                const matchesSearch = componentName.includes(searchTerm);
                const matchesType = !typeFilter || componentType === typeFilter;
                
                if (matchesSearch && matchesType) {{
                    row.style.display = '';
                    visibleCount++;
                }} else {{
                    row.style.display = 'none';
                }}
            }});
            
            const totalCount = rows.length;
            const countElement = document.getElementById('componentCount');
            if (countElement) {{
                countElement.textContent = `Showing ${{visibleCount}} of ${{totalCount}} component types`;
            }}
        }}
        
        // Attach event listeners
        document.getElementById('packageSearch')?.addEventListener('input', filterPackages);
        document.getElementById('classificationFilter')?.addEventListener('change', filterPackages);
        document.getElementById('complexityFilter')?.addEventListener('change', filterPackages);
        document.getElementById('componentSearch')?.addEventListener('keyup', filterComponents);
        document.getElementById('typeFilter')?.addEventListener('change', filterComponents);
        
        // Initialize count displays
        window.addEventListener('load', function() {{
            filterPackages();
            filterComponents();
        }});
    </script>
</body>
</html>
"""
    
    def save_report(self, output_folder: str, generate_package_pages: bool = True):
        """Save the HTML report and optionally individual package pages."""
        output_dir = Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create packages subfolder if generating package pages
        if generate_package_pages:
            packages_dir = output_dir / "packages"
            packages_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate main report
        main_report_path = output_dir / "index.html"
        html_content = self.generate_html(output_dir if generate_package_pages else None)
        
        with open(main_report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"{DONE} Main report generated: {main_report_path}")
        print(f"   Analyzed {len(self.packages)} packages")
        
        # Generate individual package pages
        if generate_package_pages:
            packages_dir = output_dir / "packages"
            package_count = 0
            # `dag_base_path` is interpolated into HTML href= attributes, which
            # require forward slashes regardless of OS.
            dag_base_path = os.path.relpath(
                self.json_path.parent.resolve(),
                packages_dir.resolve()
            ).replace(os.sep, '/')
            
            for package_csv_row in self.packages:
                package_path = package_csv_row.get('path', '')
                package_name = package_csv_row.get('name', '')
                
                # Get package data from JSON
                package_json_data = self.get_package_data_from_json(package_path)
                if not package_json_data:
                    print(f"{WARN} Warning: Package data not found in JSON: {package_path}")
                    continue
                
                # Generate package detail page
                package_html = self.generate_package_detail_page(package_csv_row, package_json_data, dag_base_path=dag_base_path)
                
                # Save package page in packages subfolder
                package_filename = f"package_{sanitize_filename(package_name)}.html"
                package_file_path = packages_dir / package_filename
                
                with open(package_file_path, 'w', encoding='utf-8') as f:
                    f.write(package_html)
                
                package_count += 1
            
            print(f"{DONE} Generated {package_count} package detail pages in: {packages_dir}")

        print(f"   Total report size: {len(html_content):,} characters")