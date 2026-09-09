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
Informatica Report Content Generator for Multi-Tab Report

Generates HTML content for Informatica Power Center assessment tab,
matching the SSIS report design with 4 sections:
  1. AI Summary
  2. Key Metrics
  3. Workflow Classification
  4. Component Conversion Breakdown

Uses the native multi-tab design system CSS classes:
  .metric-grid, .metric-card, .metric-label, .metric-value, .metric-description
  .exclusion-table (blue header tables)
  .section (white card containers)

Only injects scoped overrides for elements not covered globally:
  h2 blue underline, row hover/alternating, tooltip, info-box, warning-box
"""

import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .informatica_dag_service import InformaticaDagService




def generate_informatica_html_content(
    informatica_json_path: Path, output_html_path: Path = None, source_dir: Optional[Path] = None
) -> Tuple[str, str, str]:
    """Generate HTML content for Informatica tab in the multi-tab report.

    Args:
        informatica_json_path: Path to informatica_assessment_analysis.json
        output_html_path: Path where the main HTML file will be saved (optional)
        source_dir: Ignored (kept for API compatibility)

    Returns:
        Tuple of (html_content, javascript_code, css_content)
    """
    try:
        with open(informatica_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        workflows = data.get("workflows", [])
        conversion_mode = summary.get("conversion_mode", "dbt")

        # Generate detail pages if output_html_path is provided
        if output_html_path:
            mappings_dir = output_html_path.parent / "informatica_mappings"
            mappings_dir.mkdir(parents=True, exist_ok=True)
            _generate_workflow_detail_pages(
                workflows, mappings_dir, output_html_path.name
            )

        # Build the main content sections (matching SSIS order)
        ai_summary_html = _generate_ai_summary_section(data, informatica_json_path)
        metrics_html = _generate_metrics_section(summary, workflows)
        classification_html = _generate_workflow_classification(workflows, output_html_path, conversion_mode)
        breakdown_html = _generate_component_breakdown(workflows)

        mode_badge = _generate_mode_badge(conversion_mode)

        html_content = f"""
        <div id="informatica-report">
            <h1 style="font-size: 1.875rem; font-weight: 800; color: #102E46; margin-bottom: 0.5rem;">
                Informatica Power Center Assessment {mode_badge}
            </h1>
            <p style="color: #64748B; font-size: 1rem; margin-bottom: 2rem;">
                Comprehensive analysis of Informatica PowerCenter workflows and mappings
                identified for migration to Snowflake.
            </p>

            {ai_summary_html}
            {metrics_html}
            {classification_html}
            {breakdown_html}
        </div>
        """

        js_code = _generate_javascript()
        css_content = _generate_css()

        return html_content, js_code, css_content

    except FileNotFoundError:
        error_html = f"""
        <div id="informatica-report">
            <h2>Informatica Power Center Assessment</h2>
            <div class="warning-box">
                <p style="color: #991B1B; margin: 0;">
                    <strong>Error:</strong> Informatica JSON file not found: {html.escape(str(informatica_json_path))}
                </p>
            </div>
        </div>
        """
        return error_html, "", ""
    except Exception as e:
        error_html = f"""
        <div id="informatica-report">
            <h2>Informatica Power Center Assessment</h2>
            <div class="warning-box">
                <p style="color: #991B1B; margin: 0;">
                    <strong>Error loading Informatica data:</strong> {html.escape(str(e))}
                </p>
            </div>
        </div>
        """
        return error_html, "", ""


def _strip_document_wrapper(html_content: str) -> str:
    """Strip full HTML document tags and headings, returning only body content.

    Handles AI summary files that may be full documents (<!DOCTYPE>, <html>,
    <head>, <body>) or fragments. Strips all heading tags (h1, h2, h3) since
    the report generator provides its own section headings.
    """
    import re as _re

    content = html_content.strip()

    # Remove DOCTYPE
    content = _re.sub(r'<!DOCTYPE[^>]*>', '', content, flags=_re.IGNORECASE)

    # Remove <html> and </html>
    content = _re.sub(r'</?html[^>]*>', '', content, flags=_re.IGNORECASE)

    # Remove <head>...</head> entirely
    content = _re.sub(r'<head[^>]*>.*?</head>', '', content,
                      flags=_re.IGNORECASE | _re.DOTALL)

    # Remove <body> and </body> tags (keep content between them)
    content = _re.sub(r'</?body[^>]*>', '', content, flags=_re.IGNORECASE)

    # Remove ALL heading tags (h1-h2) — the report provides its own headings
    content = _re.sub(r'<h[1-2][^>]*>.*?</h[1-2]>', '', content,
                      flags=_re.IGNORECASE | _re.DOTALL)

    return content.strip()


def _generate_mode_badge(conversion_mode: str) -> str:
    """Generate an inline badge showing the conversion target mode."""
    if conversion_mode == "scripting":
        return (
            '<span style="display: inline-block; vertical-align: middle; '
            'background: #F3E8FF; color: #7C3AED; padding: 0.25rem 0.75rem; '
            'border-radius: 9999px; font-size: 0.8rem; font-weight: 600; '
            'margin-left: 0.75rem;">Target: Snowflake Scripting (Stored Procedures)</span>'
        )
    return (
        '<span style="display: inline-block; vertical-align: middle; '
        'background: #DBEAFE; color: #1D4ED8; padding: 0.25rem 0.75rem; '
        'border-radius: 9999px; font-size: 0.8rem; font-weight: 600; '
        'margin-left: 0.75rem;">Target: Snowflake dbt</span>'
    )


def _generate_ai_summary_section(data: Dict, json_path: Path) -> str:
    """Generate AI Summary section.

    Priority:
    1. If an LLM-generated ai_informatica_summary.html exists (referenced by
       data["summary"]["ai_summary"]), load and embed it.
    2. Otherwise, produce a deterministic fallback from JSON data.
    """
    # --- Try loading LLM-generated summary ---
    summary_rel_path = data.get("summary", {}).get("ai_summary", "")
    if summary_rel_path:
        candidate = (json_path.parent / summary_rel_path).resolve()
        if candidate.exists():
            try:
                raw_html = candidate.read_text(encoding="utf-8").strip()
                cleaned = _strip_document_wrapper(raw_html)
                if cleaned:
                    return f"""
        <section id="informatica-executive-summary">
            <h2>AI Summary</h2>
            {cleaned}
        </section>
        """
            except Exception:
                pass  # Fall through to auto-generated fallback

    # --- Fallback: rich auto-generated summary from JSON data ---
    return _build_rich_summary_fallback(data)


def _build_rich_summary_fallback(data: Dict) -> str:
    """Build a full 7-section AI Summary from JSON data alone."""
    summary = data.get("summary", {})
    workflows = data.get("workflows", [])
    conversion_mode = summary.get("conversion_mode", "dbt")

    total_workflows = summary.get("total_workflows", 0)
    total_mappings = summary.get("total_mappings", 0)
    total_components = summary.get("total_components", 0)
    total_ewis = summary.get("total_ewis", 0)
    total_fdms = summary.get("total_fdms", 0)

    # --- Compute derived data ---
    classification_counts: Dict[str, int] = {}
    complexity_counts: Dict[str, int] = {}
    custom_transform_count = 0
    source_db_types: Dict[str, int] = {}
    target_db_types: Dict[str, int] = {}
    total_not_supported = 0
    not_supported_types: List[str] = []
    largest_wf_name = ""
    largest_wf_components = 0

    for wf in workflows:
        ai = wf.get("ai_analysis") or {}
        c = ai.get("classification", "Unclassified") or "Unclassified"
        classification_counts[c] = classification_counts.get(c, 0) + 1

        metrics = wf.get("metrics", {})
        cx = metrics.get("workflow_complexity", {}).get("complexity", "Unknown")
        complexity_counts[cx] = complexity_counts.get(cx, 0) + 1

        if wf.get("flags", {}).get("has_custom_transforms"):
            custom_transform_count += 1

        wf_components = metrics.get("total_components", 0)
        if wf_components > largest_wf_components:
            largest_wf_components = wf_components
            largest_wf_name = wf.get("name", "Unknown")

        ns = metrics.get("not_supported_elements", {})
        ns_count = ns.get("total_count", 0)
        total_not_supported += ns_count
        for ct in ns.get("component_types", []):
            if ct not in not_supported_types:
                not_supported_types.append(ct)

        for src in wf.get("source_definitions", []):
            _acc_db_type(src, source_db_types)
        for tgt in wf.get("target_definitions", []):
            _acc_db_type(tgt, target_db_types)

    # Success rate
    status_totals = summary.get("status_totals", {})
    total_status = sum(status_totals.values()) if status_totals else 0
    success_count = status_totals.get("Success", 0)
    success_rate = round((success_count / total_status) * 100, 1) if total_status > 0 else 0

    # Mode-specific labels
    if conversion_mode == "scripting":
        target_label = "Snowflake Scripting (Stored Procedures)"
        target_short = "stored procedures"
        target_tasks = "Snowflake Tasks with CALL statements"
        target_transform = "Stored procedures + Snowflake Tasks"
        target_config = "Snowflake Tasks with inline SQL"
    else:
        target_label = "Snowflake dbt"
        target_short = "dbt models"
        target_tasks = "Snowflake Tasks calling dbt"
        target_transform = "dbt models + Snowflake Tasks"
        target_config = "Snowflake Tasks orchestrating dbt runs"

    # --- Section 1: Workload Overview ---
    complexity_desc_parts = []
    easy_total = complexity_counts.get("Very Easy", 0) + complexity_counts.get("Easy", 0)
    if easy_total > 0 and total_workflows > 0:
        complexity_desc_parts.append(
            f"{round(easy_total / total_workflows * 100)}% Easy/Very Easy"
        )
    medium = complexity_counts.get("Medium", 0)
    if medium > 0 and total_workflows > 0:
        complexity_desc_parts.append(
            f"{round(medium / total_workflows * 100)}% Medium"
        )
    hard_total = complexity_counts.get("Complex", 0) + complexity_counts.get("Very Complex", 0)
    if hard_total > 0 and total_workflows > 0:
        complexity_desc_parts.append(
            f"{round(hard_total / total_workflows * 100)}% Complex"
        )
    complexity_desc = ", ".join(complexity_desc_parts) if complexity_desc_parts else "not assessed"

    sec1 = f"""
  <div style="background: #f0f9ff; border-left: 4px solid #29B5E8; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
    <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Workload Overview</h3>
    <p style="font-size: 0.9rem; color: #334155; line-height: 1.7; margin: 0;">
      This Informatica PowerCenter workload comprises <strong>{total_workflows} workflows</strong> containing <strong>{total_mappings} mappings</strong> and <strong>{total_components:,} total components</strong>. Complexity distribution: {complexity_desc}. Conversion success rate: <strong>{success_rate}%</strong> ({success_count:,} of {total_status:,} components).
    </p>
  </div>"""

    # --- Section 2: Classification Breakdown ---
    class_rows = ""
    ordered_classes = sorted(classification_counts.items(), key=lambda x: -x[1])
    class_colors = {
        "Data Transformation": "#F59E0B",
        "Configuration & Control": "#22C55E",
        "Ingestion": "#29B5E8",
        "Mixed: Ingestion + Transformation": "#8B5CF6",
        "Unclassified": "#9CA3AF",
    }
    class_targets = {
        "Data Transformation": target_transform,
        "Configuration & Control": target_config,
        "Ingestion": "External stages, COPY INTO, Snowpipe",
        "Mixed: Ingestion + Transformation": f"Ingestion layer + {target_short}",
        "Unclassified": "Pending AI classification",
    }
    row_bg = False
    for label, count in ordered_classes:
        pct = round((count / total_workflows) * 100, 1) if total_workflows else 0
        color = class_colors.get(label, "#9CA3AF")
        target = class_targets.get(label, target_transform)
        bg = ' background: #fafafa;' if row_bg else ''
        class_rows += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;{bg}">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: {color}; border-radius: 3px; margin-right: 8px;"></span>{html.escape(label)}</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">{count}</td>
          <td style="text-align: center; padding: 10px 14px;">{pct}%</td>
          <td style="padding: 10px 14px; color: #475569;">{html.escape(target)}</td>
        </tr>"""
        row_bg = not row_bg

    sec2 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Workflow Classification Breakdown</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Classification</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Workflows</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">% of Total</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Snowflake Target</th>
        </tr>
      </thead>
      <tbody>{class_rows}
      </tbody>
    </table>
  </div>"""

    # --- Section 3: Sources & Destinations ---
    src_rows = ""
    for db, count in sorted(source_db_types.items(), key=lambda x: -x[1]):
        locality = "External" if db in ("Flat File", "ODBC", "FTP") else "Internal"
        src_rows += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">{html.escape(db)} ({locality})</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">{count:,} references</td>
        </tr>"""

    tgt_rows = ""
    for db, count in sorted(target_db_types.items(), key=lambda x: -x[1]):
        locality = "External" if db in ("Flat File", "ODBC", "FTP") else "Internal"
        tgt_rows += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">{html.escape(db)} ({locality})</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">{count:,} references</td>
        </tr>"""

    sec3 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Sources &amp; Destinations</h3>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem;">
      <h4 style="font-size: 0.85rem; font-weight: 600; color: #11567F; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.03em;">Sources</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8125rem;">{src_rows}
      </table>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem;">
      <h4 style="font-size: 0.85rem; font-weight: 600; color: #11567F; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.03em;">Destinations</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8125rem;">{tgt_rows}
      </table>
    </div>
  </div>"""

    # --- Section 4: Connector Types ---
    pill_colors = {
        "Teradata": "#29B5E8", "Oracle": "#11567F", "Flat File": "#22C55E",
        "DB2": "#8A999E", "ODBC": "#6366F1", "Sybase": "#EC4899",
        "Informix": "#F97316", "SQL Server": "#3B82F6",
    }
    all_db_types = set(source_db_types.keys()) | set(target_db_types.keys())
    pills_html = ""
    for db in sorted(all_db_types, key=lambda d: -(source_db_types.get(d, 0) + target_db_types.get(d, 0))):
        color = pill_colors.get(db, "#64748b")
        pills_html += f'    <span style="display: inline-block; background: {color}; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">{html.escape(db)}</span>\n'

    dominant = sorted(all_db_types, key=lambda d: -(source_db_types.get(d, 0) + target_db_types.get(d, 0)))
    dominant_name = dominant[0] if dominant else "Unknown"
    dominant_count = source_db_types.get(dominant_name, 0) + target_db_types.get(dominant_name, 0)
    connector_desc = f"{dominant_name} dominates with {dominant_count:,} total connection references."
    if "Flat File" in all_db_types:
        ff_count = source_db_types.get("Flat File", 0) + target_db_types.get("Flat File", 0)
        connector_desc += f" Flat file connections ({ff_count:,} refs) handle file-based data exchange."
    connector_desc += f" Migration requires replacing source connections with Snowflake native tables and {target_short}."

    sec4 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Connector &amp; Session Types</h3>
  <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
{pills_html}  </div>
  <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 1.5rem; line-height: 1.6;">
    {connector_desc}
  </p>"""

    # --- Section 5: Complexity Drivers ---
    if success_rate >= 95:
        rate_color, rate_bg = "#16a34a", "#f0fdf4"
    elif success_rate >= 80:
        rate_color, rate_bg = "#c2410c", "#fff7ed"
    else:
        rate_color, rate_bg = "#dc2626", "#fef2f2"

    ns_detail = ", ".join(not_supported_types) if not_supported_types else "None"

    sec5 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Complexity Drivers</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Complexity Factor</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Impact</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Details</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">EWI Issues</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fef2f2; color: #dc2626; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">{total_ewis}</span></td>
          <td style="padding: 10px 14px; color: #475569;">Conversion warnings requiring manual review</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">FDM Differences</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fff7ed; color: #c2410c; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">{total_fdms}</span></td>
          <td style="padding: 10px 14px; color: #475569;">Functional differences between Informatica and Snowflake behavior requiring UAT validation</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">Not Supported Components</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fef2f2; color: #dc2626; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">{total_not_supported}</span></td>
          <td style="padding: 10px 14px; color: #475569;">{html.escape(ns_detail)} — requires manual rewrite</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">Conversion Success Rate</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: {rate_bg}; color: {rate_color}; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">{success_rate}%</span></td>
          <td style="padding: 10px 14px; color: #475569;">{success_count:,} of {total_status:,} components converted successfully</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">Largest Workflow</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fff7ed; color: #c2410c; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">{largest_wf_components} components</span></td>
          <td style="padding: 10px 14px; color: #475569;">{html.escape(largest_wf_name)}</td>
        </tr>
      </tbody>
    </table>
  </div>"""

    # --- Section 6: Recommended Migration Approach ---
    approach_rows = ""
    row_bg = False
    for label, count in ordered_classes:
        if label == "Unclassified":
            strategy = "Pending classification"
            considerations = "Run AI analysis (Step 3) to classify workflows"
        elif label == "Data Transformation":
            strategy = f"<strong>{target_transform}</strong>"
            considerations = f"{success_rate}% auto-conversion rate; mappings convert to {target_short}"
        elif label == "Configuration & Control":
            strategy = f"<strong>{target_config}</strong>"
            considerations = f"Lightweight orchestration; replace with Snowflake Task DAGs"
        elif label == "Ingestion":
            strategy = "<strong>External stages + COPY INTO</strong>"
            considerations = "Replace external source connections with Snowflake ingestion patterns"
        else:
            strategy = f"<strong>Ingestion + {target_short}</strong>"
            considerations = "Decompose into separate ingestion and transformation layers"
        bg = ' background: #fafafa;' if row_bg else ''
        approach_rows += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;{bg}">
          <td style="padding: 10px 14px; font-weight: 500;">{html.escape(label)}</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">{count}</td>
          <td style="padding: 10px 14px; color: #475569;">{strategy}</td>
          <td style="padding: 10px 14px; color: #475569;">{considerations}</td>
        </tr>"""
        row_bg = not row_bg

    sec6 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Recommended Migration Approach</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Classification</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Count</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Migration Strategy</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Key Considerations</th>
        </tr>
      </thead>
      <tbody>{approach_rows}
      </tbody>
    </table>
  </div>"""

    # --- Section 7: Key Risks ---
    risk_cards = []
    if total_not_supported > 0:
        risk_cards.append(("red", "Not Supported Components",
                           f"{total_not_supported} component(s) not supported in {target_label} mode ({ns_detail}). Requires manual rewrite."))
    if custom_transform_count > 0:
        risk_cards.append(("red", "Custom Transformations",
                           f"{custom_transform_count} workflow(s) contain Java/C++ Custom Transformations requiring complete manual rewrite to {target_short}."))
    if total_fdms > 50:
        risk_cards.append(("amber", f"FDM Validation ({total_fdms} instances)",
                           f"Functional Difference Markers indicate behavioral gaps between Informatica and Snowflake. Each FDM requires validation during UAT to ensure business logic equivalence in the migrated {target_short}."))
    if "Flat File" in all_db_types:
        ff_total = source_db_types.get("Flat File", 0) + target_db_types.get("Flat File", 0)
        if ff_total > 0:
            risk_cards.append(("amber", "Flat File Ingestion Replacement",
                               f"{ff_total:,} flat file connection references require redesigning ingestion to use Snowflake external stages and COPY INTO."))
    if total_ewis > 0 and len(risk_cards) < 4:
        risk_cards.append(("amber", f"EWI Conversion Issues ({total_ewis})",
                           f"{total_ewis} Early Warning Issues identified during conversion requiring manual review and resolution."))
    if success_rate >= 95 and len(risk_cards) < 4:
        risk_cards.append(("green", "High Conversion Confidence",
                           f"{success_rate}% success rate with only {total_ewis} EWIs across {total_workflows} workflows. Single-mapping workflows simplify migration — each maps cleanly to one {target_short.rstrip('s') if target_short.endswith('s') else target_short}."))
    elif success_rate < 80 and len(risk_cards) < 4:
        risk_cards.append(("red", "Low Conversion Rate",
                           f"Only {success_rate}% conversion success rate indicates significant manual effort needed for migration."))

    risk_cards = risk_cards[:4]
    card_styles = {
        "red": ("background: #fef2f2; border-left: 4px solid #ef4444;", "#991b1b", "#7f1d1d"),
        "amber": ("background: #fff7ed; border-left: 4px solid #f59e0b;", "#92400e", "#78350f"),
        "green": ("background: #f0fdf4; border-left: 4px solid #22c55e;", "#166534", "#14532d"),
    }
    cards_html = ""
    for severity, title, desc in risk_cards:
        style, title_color, desc_color = card_styles[severity]
        cards_html += f"""
    <div style="{style} border-radius: 8px; padding: 1rem 1.25rem;">
      <div style="font-weight: 600; color: {title_color}; font-size: 0.9rem; margin-bottom: 0.4rem;">{html.escape(title)}</div>
      <div style="font-size: 0.825rem; color: {desc_color}; line-height: 1.6;">{html.escape(desc)}</div>
    </div>"""

    sec7 = f"""
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Key Risks</h3>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem;">{cards_html}
  </div>"""

    return f"""
        <section id="informatica-executive-summary">
            <h2>AI Summary</h2>
            <section id="ai-summary" class="section">
  <p style="color: #64748b; font-size: 0.875rem; margin-bottom: 1.5rem;">High-level, decision-ready overview of the Informatica PowerCenter workload for data engineers and solution architects preparing a migration to Snowflake.</p>
{sec1}
{sec2}
{sec3}
{sec4}
{sec5}
{sec6}
{sec7}
</section>
        </section>
        """


def _acc_db_type(definition: Dict, accumulator: Dict[str, int]) -> None:
    """Accumulate databaseType from a source/target definition's additional_info."""
    info = definition.get("additional_info", "")
    if not info:
        return
    try:
        parsed = json.loads(info)
        db_type = parsed.get("databaseType", "")
        if db_type:
            accumulator[db_type] = accumulator.get(db_type, 0) + 1
    except (json.JSONDecodeError, TypeError):
        pass


def _generate_metrics_section(summary: Dict, workflows: List[Dict]) -> str:
    """Generate key metrics cards using native .metric-grid/.metric-card classes."""
    total_workflows = summary.get("total_workflows", 0)
    total_mappings = summary.get("total_mappings", 0)
    total_components = summary.get("total_components", 0)
    total_ewis = summary.get("total_ewis", 0)
    total_fdms = summary.get("total_fdms", 0)

    # Calculate AI analyzed count
    analyzed_count = sum(
        1 for wf in workflows
        if (wf.get("ai_analysis") or {}).get("status") == "DONE"
    )

    status_totals = summary.get("status_totals", {})
    success_count = status_totals.get("Success", 0)
    total_exec = sum(status_totals.values()) if status_totals else 0
    success_rate = round((success_count / total_exec) * 100, 1) if total_exec > 0 else 0

    # Determine success rate color
    if success_rate >= 70:
        rate_color = "#10b981"
    elif success_rate >= 40:
        rate_color = "#f59e0b"
    else:
        rate_color = "#ef4444"

    return f"""
    <section id="informatica-metrics">
        <h2>Key Metrics</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Workflows</div>
                <div class="metric-value">{total_workflows}</div>
                <div class="metric-description">XML files analyzed</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">AI Analyzed</div>
                <div class="metric-value">{analyzed_count}</div>
                <div class="metric-description">Workflows analyzed with AI</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Mappings</div>
                <div class="metric-value">{total_mappings}</div>
                <div class="metric-description">Data flow pipelines</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Components</div>
                <div class="metric-value">{total_components:,}</div>
                <div class="metric-description">Transformations and tasks</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Conversion Rate</div>
                <div class="metric-value" style="color: {rate_color};">{success_rate}%</div>
                <div class="metric-description">Successful conversions</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">EWIs</div>
                <div class="metric-value" style="color: #ef4444;">{total_ewis:,}</div>
                <div class="metric-description">Conversion issues found</div>
            </div>
        </div>
    </section>
    """


def _generate_donut_chart_svg(data: Dict[str, int], colors: Dict[str, str], size: int = 150, hole_ratio: float = 0.6, center_label: str = "workflows") -> str:
    """Generate an SVG donut chart (matching SSIS pattern)."""
    import math

    total = sum(data.values())
    if total == 0:
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

        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        x1_outer = center + radius * math.cos(start_rad)
        y1_outer = center + radius * math.sin(start_rad)
        x2_outer = center + radius * math.cos(end_rad)
        y2_outer = center + radius * math.sin(end_rad)

        x1_inner = center + inner_radius * math.cos(end_rad)
        y1_inner = center + inner_radius * math.sin(end_rad)
        x2_inner = center + inner_radius * math.cos(start_rad)
        y2_inner = center + inner_radius * math.sin(start_rad)

        large_arc = 1 if angle > 180 else 0
        color = colors.get(label, '#9ca3af')

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
            <text x="{center}" y="{center + 10}" text-anchor="middle" dominant-baseline="middle" fill="#6b7280" font-size="11">{center_label}</text>
        </svg>
    '''


def _generate_donut_legend(data: Dict[str, int], colors: Dict[str, str], total: int) -> str:
    """Generate legend HTML for donut chart (matching SSIS pattern)."""
    legend_items = []
    for label, count in data.items():
        if count == 0:
            continue
        percentage = (count / total * 100) if total > 0 else 0
        color = colors.get(label, '#9ca3af')
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


def _generate_classification_and_complexity_charts(classification_counts: Dict[str, int], complexity_counts: Dict[str, int], total: int) -> str:
    """Generate dual donut charts for classification and complexity distribution (matching SSIS)."""
    classification_colors = {
        'Ingestion': '#29B5E8',
        'Data Transformation': '#F59E0B',
        'Mixed: Ingestion + Transformation': '#8B5CF6',
        'Configuration & Control': '#10b981',
        'Unclassified': '#9ca3af'
    }

    complexity_colors = {
        'Very Easy': '#22c55e',
        'Easy': '#4ade80',
        'Medium': '#facc15',
        'Complex': '#f97316',
        'Very Complex': '#ef4444',
        '\u2014': '#d1d5db'
    }

    # Order data for consistent display
    ordered_classification = {}
    for key in ['Ingestion', 'Data Transformation', 'Mixed: Ingestion + Transformation', 'Configuration & Control', 'Unclassified']:
        if classification_counts.get(key, 0) > 0:
            ordered_classification[key] = classification_counts[key]

    ordered_complexity = {}
    for key in ['Very Easy', 'Easy', 'Medium', 'Complex', 'Very Complex', '\u2014']:
        if complexity_counts.get(key, 0) > 0:
            ordered_complexity[key] = complexity_counts[key]

    # Generate SVG donuts
    classification_donut = _generate_donut_chart_svg(ordered_classification, classification_colors, size=150, center_label="workflows")
    complexity_donut = _generate_donut_chart_svg(ordered_complexity, complexity_colors, size=150, center_label="workflows")

    # Generate legends
    classification_legend = _generate_donut_legend(ordered_classification, classification_colors, total)
    complexity_legend = _generate_donut_legend(ordered_complexity, complexity_colors, total)

    return f"""
    <div style="margin: 1.5rem 0;">
        <h3 style="margin-bottom: 1rem; color: #1f2937;">Workflow Distribution</h3>
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


def _generate_workflow_classification(workflows: List[Dict], output_html_path: Path = None, conversion_mode: str = "dbt") -> str:
    """Generate Workflow Classification section (equivalent to SSIS Package Classification).

    Shows workflow classification distribution, analysis status, and a filterable
    workflow table with clickable links to detail pages.
    """
    if not workflows:
        return """
        <section id="informatica-workflow-classification">
            <h2>Workflow Classification</h2>
            <div class="info-box">
                <p style="margin: 0; color: #64748B;">No Informatica workflows were detected in the assessment data.</p>
            </div>
        </section>
        """

    # Count classifications and complexity
    classification_counts: Dict[str, int] = {}
    complexity_counts: Dict[str, int] = {}
    analyzed_count = 0
    pending_count = 0

    rows_html = ""
    for wf in workflows:
        name = html.escape(wf.get("name", "Unknown"))
        path = wf.get("path", "")
        metrics = wf.get("metrics", {})
        flags = wf.get("flags", {})
        ai_analysis = wf.get("ai_analysis") or {}

        classification = ai_analysis.get("classification", "Unclassified") or "Unclassified"
        complexity = metrics.get("workflow_complexity", {}).get("complexity", "\u2014")
        if classification == "Unclassified":
            complexity = "\u2014"

        analysis_text = ai_analysis.get("analysis", "").strip()
        if analysis_text and conversion_mode == "scripting":
            analysis_text = analysis_text.replace("(dbt)", "(scripting)")
        elif analysis_text and conversion_mode == "dbt":
            analysis_text = analysis_text.replace("(scripting)", "(dbt)")
        if analysis_text:
            analyzed_count += 1
        else:
            pending_count += 1

        # Count distributions
        classification_counts[classification] = classification_counts.get(classification, 0) + 1
        complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1

        # Complexity color
        if complexity in ["Very Easy", "Easy"]:
            complexity_color = "#16a34a"
        elif complexity == "Medium":
            complexity_color = "#ca8a04"
        elif complexity in ["Complex", "Very Complex"]:
            complexity_color = "#dc2626"
        else:
            complexity_color = "#9ca3af"

        # Indicators/badges
        indicators_html = ""
        if flags.get("has_custom_transforms"):
            indicators_html += '<span style="display: inline-block; padding: 0.125rem 0.375rem; background: #FEF2F2; color: #DC2626; border-radius: 3px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; margin-right: 4px;">Custom</span>'
        if flags.get("has_sql_override"):
            indicators_html += '<span style="display: inline-block; padding: 0.125rem 0.375rem; background: #FFFBEB; color: #D97706; border-radius: 3px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;">SQL Override</span>'

        # Workflow name link (using <a href target="_blank"> like SSIS)
        if output_html_path:
            safe_name = _safe_filename(wf.get("name", "unknown"))
            detail_filename = f"informatica_mappings/workflow_{safe_name}.html"
            name_html = f'<a href="{detail_filename}" target="_blank" style="text-decoration: none;"><span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500; color: #1f2937;">{name} \u2197</span></a>'
        else:
            name_html = f'<span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500; color: #1f2937;">{name}</span>'

        # AI analysis tooltip (dark background, positioned above — matching SSIS)
        if analysis_text:
            tooltip_text = html.escape(analysis_text)
            if len(tooltip_text) > 500:
                tooltip_text = tooltip_text[:497] + '...'
            tooltip_html = f'''<div class="ai-tooltip">
                    <div class="ai-tooltip-header">\U0001f916 AI Analysis</div>
                    <div class="ai-tooltip-content">{tooltip_text}</div>
                </div>'''
        else:
            tooltip_html = '''<div class="ai-tooltip">
                    <div class="ai-tooltip-pending">\u23F3 AI analysis pending</div>
                </div>'''

        rows_html += f"""
            <tr class="workflow-row" data-classification="{html.escape(classification)}" data-complexity="{html.escape(complexity)}" data-name="{html.escape(name.lower())}">
                <td style="position: relative;">{name_html}{tooltip_html}</td>
                <td><span style="display: inline-block; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">{html.escape(classification)}</span></td>
                <td style="text-align: center;"><span style="display: inline-block; background: #f3f4f6; color: {complexity_color}; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">{html.escape(complexity)}</span></td>
                <td style="text-align: center;">{indicators_html if indicators_html else '<span style="color: #d1d5db;">&mdash;</span>'}</td>
            </tr>
            """

    # Analysis status banner
    total_workflows = len(workflows)
    if pending_count > 0:
        analysis_status_html = f"""
            <div class="warning-box">
                <strong>Analysis Status:</strong> {analyzed_count} of {total_workflows} workflows analyzed.
                {pending_count} workflow{'s' if pending_count != 1 else ''} pending AI analysis.
            </div>
            """
    else:
        analysis_status_html = f"""
            <div class="info-box" style="background: #D1FAE5; border-left-color: #10b981;">
                <strong>Analysis Status:</strong> All {analyzed_count} workflows have been analyzed.
            </div>
            """

    # Classification guide — adapt target references based on conversion_mode
    if conversion_mode == "scripting":
        data_transform_target = "stored procedures on Snowflake, with sessions converting to Snowflake Tasks using CALL statements"
        mixed_target = "Snowflake ingestion and stored procedure transformation layers"
    else:
        data_transform_target = "dbt projects on Snowflake, with sessions converting to Snowflake Tasks"
        mixed_target = "Snowflake ingestion and dbt transformation layers"

    classification_guide_html = f"""
            <div class="info-box">
                <strong>Classification Guide:</strong>
                <ul style="margin: 0.5rem 0 0 1.25rem; line-height: 1.6;">
                    <li><strong>Ingestion:</strong> Workflows that extract data from external sources (flat files, APIs, external databases) into the data platform. Consider Snowflake Openflow, Snowpipe, or Fivetran as alternatives.</li>
                    <li><strong>Data Transformation:</strong> Workflows that transform data between internal layers. Good candidates to migrate with SnowConvert AI to {data_transform_target}.</li>
                    <li><strong>Mixed: Ingestion + Transformation:</strong> Workflows combining external data ingestion with internal transformations. Decompose into separate {mixed_target}.</li>
                    <li><strong>Configuration &amp; Control:</strong> Workflows focused on orchestration, timer-based scheduling, or system operations. Migrate to Snowflake Tasks and Snowflake Scripting.</li>
                    <li><strong>Unclassified:</strong> Pending AI analysis.</li>
                </ul>
            </div>
    """

    # Dual donut charts for classification and complexity distribution
    charts_html = _generate_classification_and_complexity_charts(classification_counts, complexity_counts, total_workflows)

    return f"""
    <section id="informatica-workflow-classification">
        <h2>Workflow Classification</h2>
        {analysis_status_html}
        {classification_guide_html}
        {charts_html}

        <div style="margin: 1.5rem 0;">
            <input type="text" id="informaticaWorkflowSearch" placeholder="Search by workflow name..."
                   style="width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; margin-bottom: 0.75rem; font-size: 0.95rem;">
            <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                <select id="informaticaClassificationFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; flex: 1; min-width: 200px;">
                    <option value="">All Classifications</option>
                    <option value="Ingestion">Ingestion</option>
                    <option value="Data Transformation">Data Transformation</option>
                    <option value="Mixed: Ingestion + Transformation">Mixed: Ingestion + Transformation</option>
                    <option value="Configuration & Control">Configuration &amp; Control</option>
                </select>
                <select id="informaticaComplexityFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; flex: 1; min-width: 200px;">
                    <option value="">All Complexity Levels</option>
                    <option value="Very Easy">Very Easy</option>
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Complex">Complex</option>
                    <option value="Very Complex">Very Complex</option>
                </select>
                <button onclick="resetInformaticaFilters()" style="padding: 0.75rem 1.5rem; border: 1px solid #d1d5db; border-radius: 4px; background: white; cursor: pointer; font-weight: 600;">
                    Reset Filters
                </button>
            </div>
            <div id="informaticaWorkflowCount" style="margin-top: 0.75rem; color: #6b7280; font-size: 0.875rem;"></div>
        </div>

        <table id="informaticaWorkflowTable">
            <thead>
                <tr>
                    <th style="width: 35%;">Workflow Name</th>
                    <th style="width: 28%;">Classification</th>
                    <th style="width: 20%; text-align: center;">Complexity</th>
                    <th style="width: 17%; text-align: center;">Indicators</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </section>
    """


def _generate_component_breakdown(workflows: List[Dict]) -> str:
    """Generate Component Conversion Breakdown (equivalent to SSIS not-supported section).

    Aggregates all components by (subtype, category) with Success/Partial/NotSupported counts.
    """
    # Count components by (subtype, category) and status
    component_breakdown: Dict[tuple, Dict[str, int]] = {}

    for wf in workflows:
        # Workflow tasks (Control Flow equivalent)
        for task in wf.get("workflow_tasks", []):
            subtype = task.get("subtype", "Unknown")
            status = task.get("status", "Unknown")
            key = (subtype, "Workflow Task")

            if key not in component_breakdown:
                component_breakdown[key] = {"Success": 0, "Partial": 0, "NotSupported": 0}

            if status in ["Success", "Partial", "NotSupported"]:
                component_breakdown[key][status] += 1

        # Mapping components (Data Flow equivalent) — classify by Informatica semantics
        for mapping in wf.get("mappings", []):
            for component in mapping.get("components", []):
                subtype = component.get("subtype", "Unknown")
                status = component.get("status", "Unknown")
                # Classify: Source Definition → Source, Target Definition → Target, else → Transformation
                if subtype == "Source Definition":
                    comp_type = "Source"
                elif subtype == "Target Definition":
                    comp_type = "Target"
                else:
                    comp_type = "Transformation"
                key = (subtype, comp_type)

                if key not in component_breakdown:
                    component_breakdown[key] = {"Success": 0, "Partial": 0, "NotSupported": 0}

                if status in ["Success", "Partial", "NotSupported"]:
                    component_breakdown[key][status] += 1

        # Source definitions (folder-level)
        for src in wf.get("source_definitions", []):
            subtype = src.get("subtype", "Source Definition")
            status = src.get("status", "N/A")
            key = (subtype, "Source")

            if key not in component_breakdown:
                component_breakdown[key] = {"Success": 0, "Partial": 0, "NotSupported": 0}

            if status in ["Success", "Partial", "NotSupported"]:
                component_breakdown[key][status] += 1

        # Target definitions (folder-level)
        for tgt in wf.get("target_definitions", []):
            subtype = tgt.get("subtype", "Target Definition")
            status = tgt.get("status", "N/A")
            key = (subtype, "Target")

            if key not in component_breakdown:
                component_breakdown[key] = {"Success": 0, "Partial": 0, "NotSupported": 0}

            if status in ["Success", "Partial", "NotSupported"]:
                component_breakdown[key][status] += 1

    if not component_breakdown:
        return """
        <section id="informatica-component-breakdown">
            <h2>Component Conversion Breakdown</h2>
            <div class="info-box">
                <p style="margin: 0; color: #64748B;">No components with conversion status were found in the assessment data.</p>
            </div>
        </section>
        """

    # Sort by total count descending
    sorted_components = sorted(
        component_breakdown.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True,
    )

    # Generate table rows
    rows_html = ""
    for (subtype, comp_type), counts in sorted_components:
        total = counts["Success"] + counts["Partial"] + counts["NotSupported"]
        if total == 0:
            continue
        success_pct = (counts["Success"] / total * 100) if total > 0 else 0
        partial_pct = (counts["Partial"] / total * 100) if total > 0 else 0
        not_supported_pct = (counts["NotSupported"] / total * 100) if total > 0 else 0

        rows_html += f"""
            <tr class="component-row" data-component-name="{html.escape(subtype.lower())}" data-component-type="{html.escape(comp_type.lower())}">
                <td><code style="font-size: 0.85rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px;">{html.escape(subtype)}</code></td>
                <td style="text-align: center;"><span style="display: inline-block; background: #f3f4f6; font-weight: 500; font-size: 0.85rem; padding: 0.25rem 0.5rem; border-radius: 4px;">{html.escape(comp_type)}</span></td>
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
    total_success = sum(counts["Success"] for _, counts in component_breakdown.items())
    total_partial = sum(counts["Partial"] for _, counts in component_breakdown.items())
    total_not_supported = sum(counts["NotSupported"] for _, counts in component_breakdown.items())
    grand_total = total_success + total_partial + total_not_supported

    success_pct = (total_success / grand_total * 100) if grand_total > 0 else 0
    partial_pct = (total_partial / grand_total * 100) if grand_total > 0 else 0
    not_supported_pct = (total_not_supported / grand_total * 100) if grand_total > 0 else 0

    return f"""
    <section id="informatica-component-breakdown">
        <h2>Component Conversion Breakdown</h2>
        <div class="info-box" style="background: linear-gradient(to right, #f0f9ff, #e0f2fe);">
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
                <input type="text" id="informaticaComponentSearch" placeholder="Search components by name..."
                       style="flex: 1; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; font-size: 0.95rem;">
                <select id="informaticaTypeFilter" style="padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 4px; font-size: 0.95rem; min-width: 180px;">
                    <option value="">All Types</option>
                    <option value="transformation">Transformation</option>
                    <option value="source">Source</option>
                    <option value="target">Target</option>
                    <option value="workflow task">Workflow Task</option>
                </select>
            </div>
            <div id="informaticaComponentCount" style="margin-bottom: 0.75rem; color: #6b7280; font-size: 0.875rem;"></div>
        </div>

        <table class="exclusion-table" id="informaticaComponentTable">
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
            <tbody>
                {rows_html if rows_html else '<tr><td colspan="7" style="text-align: center; color: #6b7280; padding: 2rem;">No component data available.</td></tr>'}
            </tbody>
        </table>
    </section>
    """


def _generate_workflow_detail_pages(
    workflows: List[Dict], output_dir: Path, main_report_filename: str,
) -> None:
    """Generate individual HTML detail pages for each workflow."""
    # output_dir is the informatica_mappings/ subdir; parent is main output dir
    dag_root = output_dir.parent
    dag_service = InformaticaDagService

    # Generate DAG HTML files for each workflow and mapping
    for wf in workflows:
        name = wf.get("name", "unknown")
        workflow_dag_file = wf.get("workflow_dag_file", "")
        workflow_tasks = wf.get("workflow_tasks", [])
        mappings = wf.get("mappings", [])

        # Generate mapping DAGs first (to build clickable links for workflow DAG)
        mapping_dag_links = {}
        for m in mappings:
            m_dag_file = m.get("dag_file", "")
            if m_dag_file and m.get("components"):
                # Workflow DAG link back from mapping DAG
                workflow_dag_link_from_mapping = f"../{workflow_dag_file}" if workflow_dag_file else None
                dag_service.generate_mapping_dag(
                    mapping=m,
                    workflow_name=name,
                    output_path=dag_root / m_dag_file,
                    workflow_dag_link=workflow_dag_link_from_mapping,
                )

        # Build clickable navigation: Session tasks → their Mapping DAGs
        # Naming convention: Session task "s_<mapping_name>" → mapping "<mapping_name>"
        mapping_name_to_dag = {}
        for m in mappings:
            m_name = m.get("name", "")
            m_dag = m.get("dag_file", "")
            if m_name and m_dag:
                mapping_name_to_dag[m_name] = m_dag

        for task in workflow_tasks:
            full_name = task.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            subtype = (task.get("subtype", "") or "").lower()
            if subtype == "session":
                # Strip "s_" prefix to get mapping name
                candidate = short_name[2:] if short_name.startswith("s_") else short_name
                if candidate in mapping_name_to_dag:
                    mapping_dag_links[short_name] = f"../{mapping_name_to_dag[candidate]}"

        # Generate workflow-level DAG (from workflow tasks)
        if workflow_dag_file and workflow_tasks:
            dag_service.generate_workflow_dag(
                workflow=wf,
                output_path=dag_root / workflow_dag_file,
                mapping_dag_links=mapping_dag_links if mapping_dag_links else None,
            )

    print(f"  Generated DAG files in: {dag_root / 'dags'}")

    for wf in workflows:
        name = wf.get("name", "unknown")
        safe_name = _safe_filename(name)
        detail_html = _build_workflow_detail_html(wf, main_report_filename, dag_base_path="..", dag_root=dag_root)

        detail_path = output_dir / f"workflow_{safe_name}.html"
        with open(detail_path, "w", encoding="utf-8") as f:
            f.write(detail_html)

    print(f"  Generated {len(workflows)} Informatica workflow detail pages in: {output_dir}")


def _build_workflow_detail_html(wf: Dict, main_report_filename: str, dag_base_path: str = "..", dag_root: Path = None) -> str:
    """Build a standalone HTML page for one workflow's details.

    Matches the SSIS package detail page design:
    - Dark sidebar navigation
    - Hero header with classification/complexity badges + DAG button
    - Quick stats bar
    - AI Analysis section with conversion progress bar
    - Collapsible detail cards (Workflow Tasks, Mappings with DAG links, Sources/Targets)
    """
    name = html.escape(wf.get("name", "Unknown"))
    path = html.escape(wf.get("path", ""))
    metrics = wf.get("metrics", {})
    flags = wf.get("flags", {})
    ai_analysis = wf.get("ai_analysis") or {}
    mappings = wf.get("mappings", [])
    source_defs = wf.get("source_definitions", [])
    target_defs = wf.get("target_definitions", [])
    workflow_tasks = wf.get("workflow_tasks", [])
    workflow_dag_file = wf.get("workflow_dag_file", "")

    rates = metrics.get("conversion_rates", {})
    complexity_data = metrics.get("workflow_complexity", {})
    classification = ai_analysis.get("classification", "Unclassified") or "Unclassified"
    complexity = complexity_data.get("complexity", "\u2014") if classification != "Unclassified" else "\u2014"
    analysis_text = ai_analysis.get("analysis", "").strip()

    # Metrics
    total_components = metrics.get("total_components", 0)
    total_mappings = metrics.get("total_mappings", 0)
    success_rate = rates.get("success_rate", 0)
    partial_rate = rates.get("partial_rate", 0)
    not_supported_rate = rates.get("not_supported_rate", 0)

    # Status counts
    status_summary = metrics.get("status_summary", {})
    success_count = status_summary.get("Success", 0)
    partial_count = status_summary.get("Partial", 0)
    not_supported_count = status_summary.get("NotSupported", 0)

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
    }
    comp_style = complexity_styles.get(complexity, {'bg': '#f3f4f6', 'color': '#6b7280'})

    # Workflow DAG button — show in header for ALL detail pages
    # Priority: workflow DAG > first mapping DAG
    dag_button_html = ""
    dag_button_file = ""
    dag_button_label = ""
    if workflow_dag_file and dag_root and (dag_root / workflow_dag_file).exists():
        dag_button_file = workflow_dag_file
        dag_button_label = "View Workflow DAG"
    elif mappings:
        # Fall back to first mapping's DAG file
        for m in mappings:
            m_dag = m.get("dag_file", "")
            if m_dag and dag_root and (dag_root / m_dag).exists():
                dag_button_file = m_dag
                dag_button_label = "View Mapping DAG"
                break

    if dag_button_file:
        dag_button_html = f'''
            <a href="{dag_base_path}/{dag_button_file}" target="_blank"
               style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1rem;
                      background: linear-gradient(135deg, #8B5CF6, #7C3AED); color: white;
                      text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 0.875rem;
                      box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3); transition: all 0.2s;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
                </svg>
                {dag_button_label}
            </a>
        '''

    # Flag indicators
    flags_indicators = ""
    if flags.get("has_custom_transforms"):
        flags_indicators += '''
            <div style="display: flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem;
                        background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px;">
                <span style="font-size: 0.75rem; font-weight: 600; color: #dc2626; text-transform: uppercase;">Custom Transforms</span>
            </div>
        '''
    if flags.get("has_sql_override"):
        flags_indicators += '''
            <div style="display: flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem;
                        background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px;">
                <span style="font-size: 0.75rem; font-weight: 600; color: #d97706; text-transform: uppercase;">SQL Override</span>
            </div>
        '''

    # AI Analysis content
    ai_analysis_content = ""
    if analysis_text:
        ai_analysis_content = f'''
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; line-height: 1.7;">
                <p style="margin: 0; color: #334155; white-space: pre-wrap;">{html.escape(analysis_text)}</p>
            </div>
        '''
    else:
        ai_analysis_content = '''
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 2rem; text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem;">AI analysis pending</div>
            </div>
        '''

    # Conversion progress bar
    progress_bar_html = f'''
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
    '''

    # Workflow tasks HTML
    tasks_html = ""
    if workflow_tasks:
        task_rows = ""
        for task in workflow_tasks:
            t_name = html.escape(task.get("full_name", "").split(".")[-1] if task.get("full_name") else "")
            t_subtype = html.escape(task.get("subtype", ""))
            t_status = task.get("status", "N/A")
            t_ewis = task.get("issue_counts", {}).get("ewis", 0)
            status_color = "#10b981" if t_status == "Success" else "#ef4444" if t_status == "NotSupported" else "#64748B"
            task_rows += f'''
                <tr>
                    <td style="font-weight: 500;">{t_name}</td>
                    <td style="text-align: center;"><code style="background: #f1f5f9; padding: 0.125rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">{t_subtype}</code></td>
                    <td style="text-align: center; color: {status_color}; font-weight: 600;">{html.escape(t_status)}</td>
                    <td style="text-align: center; color: {"#ef4444" if t_ewis > 0 else "#64748b"};">{t_ewis}</td>
                </tr>
            '''
        tasks_html = f'''
            <table>
                <thead><tr><th>Task Name</th><th style="text-align: center;">Type</th><th style="text-align: center;">Status</th><th style="text-align: center;">EWIs</th></tr></thead>
                <tbody>{task_rows}</tbody>
            </table>
        '''
    else:
        tasks_html = '''
            <div style="padding: 2rem; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1; text-align: center;">
                <div style="font-size: 0.9rem; color: #64748b;">No workflow tasks</div>
            </div>
        '''

    # Mappings HTML with DAG links
    mappings_html = ""
    if mappings:
        mapping_items = ""
        for m in mappings:
            m_name = html.escape(m.get("name", ""))
            m_metrics = m.get("metrics", {})
            m_rates = m_metrics.get("conversion_rates", {})
            m_components = m_metrics.get("total_components", 0)
            m_success = m_rates.get("success_rate", 0)
            m_ewis = m_metrics.get("issue_counts", {}).get("total_ewis", 0)
            m_dag_file = m.get("dag_file", "")

            # Status color for success rate
            if m_success >= 90:
                s_color = '#16a34a'
                s_bg = '#dcfce7'
            elif m_success >= 70:
                s_color = '#ca8a04'
                s_bg = '#fef9c3'
            else:
                s_color = '#dc2626'
                s_bg = '#fee2e2'

            # DAG link for this mapping — only show if file exists on disk
            dag_link = ""
            if m_dag_file and dag_root and (dag_root / m_dag_file).exists():
                dag_link = f'''
                    <a href="{dag_base_path}/{m_dag_file}" target="_blank"
                       style="display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.5rem 0.875rem;
                              background: linear-gradient(135deg, #3B82F6, #2563EB); color: white;
                              text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.8rem;
                              box-shadow: 0 2px 4px rgba(59, 130, 246, 0.25); flex-shrink: 0;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="3"></circle>
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
                        </svg>
                        View DAG
                    </a>
                '''

            mapping_items += f'''
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.875rem 1rem;
                            background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 600; color: #1e293b; font-size: 0.875rem; margin-bottom: 0.25rem;">{m_name}</div>
                        <div style="display: flex; align-items: center; gap: 0.75rem; font-size: 0.75rem; color: #64748b;">
                            <span>{m_components} components</span>
                            <span style="background: {s_bg}; color: {s_color}; padding: 0.125rem 0.5rem; border-radius: 99px; font-weight: 600;">{m_success:.0f}% success</span>
                            {f'<span style="color: #ef4444;">{m_ewis} EWIs</span>' if m_ewis > 0 else ''}
                        </div>
                    </div>
                    {dag_link}
                </div>
            '''
        mappings_html = f'<div style="display: flex; flex-direction: column; gap: 0.5rem;">{mapping_items}</div>'
    else:
        mappings_html = '''
            <div style="padding: 2rem; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1; text-align: center;">
                <div style="font-size: 0.9rem; color: #64748b;">No mappings</div>
            </div>
        '''

    # Not Supported Components (collect from all mappings)
    not_supported_types = set()
    for m in mappings:
        ns = m.get("metrics", {}).get("not_supported_components", {})
        for comp_type in ns.get("component_types", []):
            not_supported_types.add(comp_type)
    for task in workflow_tasks:
        if task.get("status") == "NotSupported":
            not_supported_types.add(task.get("subtype", "Unknown"))

    not_supported_html = ""
    if not_supported_types:
        chips = ""
        for comp_type in sorted(not_supported_types):
            chips += f'''
                <span style="display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem;
                             background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; font-size: 0.8rem;">
                    <code style="color: #991b1b;">{html.escape(comp_type)}</code>
                </span>
            '''
        not_supported_html = f'''
            <div class="detail-card" style="margin-top: 1rem; border-color: #fecaca;">
                <div class="detail-card-header" onclick="toggleDetailCard('not-supported-content', this)" style="background: #fef2f2; border-bottom-color: #fecaca;">
                    <div class="detail-card-title" style="color: #991b1b;">
                        Not Supported Components
                        <span style="background: #fee2e2; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #991b1b; font-weight: 500;">{len(not_supported_types)}</span>
                    </div>
                    <span class="toggle-icon">&#9654;</span>
                </div>
                <div id="not-supported-content" class="detail-card-content" style="display: none;">
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">{chips}</div>
                    <p style="margin: 1rem 0 0 0; font-size: 0.8rem; color: #6b7280;">These components require manual migration or alternative approaches.</p>
                </div>
            </div>
        '''

    # Component Breakdown — aggregate subtypes from mappings + workflow tasks
    subtype_counts: Dict[str, int] = {}
    for m in mappings:
        for comp in m.get("components", []):
            st = comp.get("subtype", "Unknown")
            subtype_counts[st] = subtype_counts.get(st, 0) + 1
    for task in workflow_tasks:
        st = task.get("subtype", "Unknown")
        subtype_counts[st] = subtype_counts.get(st, 0) + 1

    component_breakdown_html = ""
    if subtype_counts:
        breakdown_rows = ""
        for subtype, count in sorted(subtype_counts.items(), key=lambda x: x[1], reverse=True):
            breakdown_rows += f'''
                <tr>
                    <td><code style="font-size: 0.85rem;">{html.escape(subtype)}</code></td>
                    <td style="text-align: center; font-weight: 600;">{count}</td>
                </tr>
            '''
        component_breakdown_html = f'''
            <table>
                <thead>
                    <tr>
                        <th>Component Type</th>
                        <th style="width: 120px; text-align: center;">Count</th>
                    </tr>
                </thead>
                <tbody>
                    {breakdown_rows}
                </tbody>
            </table>
        '''
    else:
        component_breakdown_html = '<p style="color: #94a3b8; font-size: 0.875rem; text-align: center; padding: 1.5rem 0;">No component breakdown available.</p>'

    # Sources & Targets
    sources_list = ""
    for src in source_defs:
        sources_list += f'<div style="padding: 0.5rem 0.75rem; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.85rem;">{html.escape(src.get("full_name", ""))}</div>'
    targets_list = ""
    for tgt in target_defs:
        targets_list += f'<div style="padding: 0.5rem 0.75rem; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.85rem;">{html.escape(tgt.get("full_name", ""))}</div>'

    # Success rate color
    rate_color = '#16a34a' if success_rate >= 90 else '#ca8a04' if success_rate >= 70 else '#dc2626'
    rate_border = '#bbf7d0' if success_rate >= 90 else '#fde68a' if success_rate >= 70 else '#fecaca'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Workflow Detail</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #F8FAFC; color: #1E293B; line-height: 1.6; }}
        .sidebar {{ position: fixed; left: 0; top: 0; width: 260px; height: 100vh; background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); color: white; padding: 1.5rem; overflow-y: auto; z-index: 1000; box-shadow: 4px 0 24px rgba(0,0,0,0.15); }}
        .content {{ margin-left: 280px; max-width: 1100px; padding: 2rem 2.5rem; }}
        .nav-link {{ display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 0.875rem; color: #cbd5e1; text-decoration: none; border-radius: 6px; font-size: 0.875rem; transition: all 0.15s; }}
        .nav-link:hover {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; }}
        .detail-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; transition: box-shadow 0.2s; }}
        .detail-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .detail-card-header {{ padding: 1rem 1.25rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; }}
        .detail-card-header:hover {{ background: #f1f5f9; }}
        .detail-card-title {{ font-weight: 600; color: #1e293b; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; }}
        .detail-card-content {{ padding: 1.25rem; }}
        .stat-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.25rem; text-align: center; transition: all 0.2s; }}
        .stat-card:hover {{ border-color: #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .stat-value {{ font-size: 1.75rem; font-weight: 700; color: #0f172a; line-height: 1.2; }}
        .stat-label {{ font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.375rem; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        thead {{ background: #29B5E8; color: white; }}
        th {{ padding: 0.75rem 1rem; text-align: left; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #e2e8f0; font-size: 0.875rem; }}
        tbody tr:hover {{ background: #E5F6FD; }}
        tbody tr:nth-child(even) {{ background: #F9FAFB; }}
        tbody tr:nth-child(even):hover {{ background: #E5F6FD; }}
        .toggle-icon {{ color: #94a3b8; font-size: 0.875rem; }}
    </style>
</head>
<body>
    <!-- SIDEBAR NAVIGATION -->
    <div class="sidebar">
        <div style="margin-bottom: 2rem;">
            <a href="../{html.escape(main_report_filename)}" style="color: white; text-decoration: none; font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                Back to Main Report
            </a>
        </div>
        <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(148, 163, 184, 0.2);">
            <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 0.5rem;">Workflow</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #f1f5f9; word-break: break-word;">{name}</div>
        </div>
        <nav style="display: flex; flex-direction: column; gap: 0.25rem;">
            <a href="#header" class="nav-link"><span style="width: 6px; height: 6px; background: #3b82f6; border-radius: 50%;"></span> Overview</a>
            <a href="#ai-analysis" class="nav-link"><span style="width: 6px; height: 6px; background: #8b5cf6; border-radius: 50%;"></span> AI Analysis</a>
            <a href="#details" class="nav-link"><span style="width: 6px; height: 6px; background: #10b981; border-radius: 50%;"></span> Workflow Details</a>
        </nav>
    </div>

    <!-- MAIN CONTENT -->
    <div class="content">
        <!-- HEADER SECTION -->
        <section id="header" style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <h1 style="font-size: 1.75rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem 0;">{name}</h1>
                    <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                        <code style="background: #f1f5f9; padding: 0.375rem 0.75rem; border-radius: 6px; font-size: 0.8rem; color: #475569; border: 1px solid #e2e8f0;">{path}</code>
                        {flags_indicators}
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
                    <div style="font-size: 1rem; font-weight: 600; color: {class_style['color']};">{html.escape(classification)}</div>
                </div>
                <div style="background: {comp_style['bg']}; border: 1px solid {comp_style.get('bg', '#d1d5db')}; border-radius: 10px; padding: 1rem 1.25rem;">
                    <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: {comp_style['color']}; opacity: 0.8; margin-bottom: 0.375rem;">Complexity</div>
                    <div style="font-size: 1rem; font-weight: 600; color: {comp_style['color']};">{html.escape(complexity)}</div>
                </div>
            </div>
        </section>

        <!-- QUICK STATS BAR -->
        <section style="margin-bottom: 2rem;">
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem;">
                <div class="stat-card">
                    <div class="stat-value">{total_components}</div>
                    <div class="stat-label">Components</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_mappings}</div>
                    <div class="stat-label">Mappings</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(workflow_tasks)}</div>
                    <div class="stat-label">Tasks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(source_defs) + len(target_defs)}</div>
                    <div class="stat-label">Sources/Targets</div>
                </div>
                <div class="stat-card" style="border-color: {rate_border};">
                    <div class="stat-value" style="color: {rate_color};">{success_rate:.0f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </section>

        <!-- AI ANALYSIS SECTION -->
        <section id="ai-analysis" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #1e293b; border: none; padding: 0;">AI Analysis</h2>
            </div>
            {ai_analysis_content}
            {progress_bar_html}
            {not_supported_html}
        </section>

        <!-- WORKFLOW DETAILS -->
        <section id="details" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #1e293b; border: none; padding: 0;">Workflow Details</h2>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <!-- Component Breakdown -->
                <div class="detail-card">
                    <div class="detail-card-header" onclick="toggleDetailCard('breakdown-content', this)">
                        <div class="detail-card-title">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2">
                                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                                <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                            </svg>
                            Component Breakdown
                            <span style="background: #f1f5f9; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #64748b; font-weight: 500;">{total_components}</span>
                        </div>
                        <span class="toggle-icon">&#9654;</span>
                    </div>
                    <div id="breakdown-content" class="detail-card-content" style="display: none;">
                        {component_breakdown_html}
                    </div>
                </div>

                <!-- Workflow Tasks -->
                <div class="detail-card">
                    <div class="detail-card-header" onclick="toggleDetailCard('tasks-content', this)">
                        <div class="detail-card-title">
                            Workflow Tasks
                            <span style="background: #f1f5f9; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #64748b; font-weight: 500;">{len(workflow_tasks)}</span>
                        </div>
                        <span class="toggle-icon">&#9654;</span>
                    </div>
                    <div id="tasks-content" class="detail-card-content" style="display: none;">
                        {tasks_html}
                    </div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <!-- Sources & Targets -->
                <div class="detail-card">
                    <div class="detail-card-header" onclick="toggleDetailCard('sources-content', this)">
                        <div class="detail-card-title">
                            Sources &amp; Targets
                            <span style="background: #f1f5f9; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #64748b; font-weight: 500;">{len(source_defs) + len(target_defs)}</span>
                        </div>
                        <span class="toggle-icon">&#9654;</span>
                    </div>
                    <div id="sources-content" class="detail-card-content" style="display: none;">
                        {f'<div style="margin-bottom: 1rem;"><div style="font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem;">Sources ({len(source_defs)})</div><div style="display: flex; flex-direction: column; gap: 0.375rem;">{sources_list}</div></div>' if source_defs else '<div style="margin-bottom: 1rem; color: #94a3b8; font-size: 0.85rem;">No sources</div>'}
                        {f'<div><div style="font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem;">Targets ({len(target_defs)})</div><div style="display: flex; flex-direction: column; gap: 0.375rem;">{targets_list}</div></div>' if target_defs else '<div style="color: #94a3b8; font-size: 0.85rem;">No targets</div>'}
                    </div>
                </div>
            </div>

            <!-- Mappings (full width) -->
            <div class="detail-card" style="margin-top: 1rem;">
                <div class="detail-card-header" onclick="toggleDetailCard('mappings-content', this)">
                    <div class="detail-card-title">
                        Mappings
                        <span style="background: #dbeafe; padding: 0.125rem 0.5rem; border-radius: 99px; font-size: 0.75rem; color: #1e40af; font-weight: 500;">{len(mappings)}</span>
                    </div>
                    <span class="toggle-icon">&#9654;</span>
                </div>
                <div id="mappings-content" class="detail-card-content" style="display: none;">
                    {mappings_html}
                </div>
            </div>
        </section>
    </div>

    <script>
        function toggleDetailCard(contentId, header) {{
            const content = document.getElementById(contentId);
            const icon = header.querySelector('.toggle-icon');
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                icon.innerHTML = '&#9660;';
            }} else {{
                content.style.display = 'none';
                icon.innerHTML = '&#9654;';
            }}
        }}

        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    document.querySelectorAll('.nav-link').forEach(l => l.style.background = '');
                    this.style.background = 'rgba(59, 130, 246, 0.2)';
                }}
            }});
        }});
    </script>
</body>
</html>"""


def _generate_javascript() -> str:
    """Generate JavaScript for Informatica tab interactivity.

    Functions are prefixed with 'informatica' to avoid collisions with SSIS JS.
    Targets .workflow-row and .component-row within #informatica-report.
    """
    return """
    (function() {
        function filterInformaticaWorkflows() {
            const searchTerm = document.getElementById('informaticaWorkflowSearch')?.value.toLowerCase() || '';
            const classificationFilter = document.getElementById('informaticaClassificationFilter')?.value || '';
            const complexityFilter = document.getElementById('informaticaComplexityFilter')?.value || '';

            const rows = document.querySelectorAll('#informatica-report .workflow-row');
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
            const countElement = document.getElementById('informaticaWorkflowCount');
            if (countElement) {
                countElement.textContent = `Showing ${visibleCount} of ${totalCount} workflows`;
            }
        }

        function resetInformaticaFilters() {
            const search = document.getElementById('informaticaWorkflowSearch');
            const classification = document.getElementById('informaticaClassificationFilter');
            const complexity = document.getElementById('informaticaComplexityFilter');

            if (search) search.value = '';
            if (classification) classification.value = '';
            if (complexity) complexity.value = '';
            filterInformaticaWorkflows();
        }

        function filterInformaticaComponents() {
            const searchTerm = document.getElementById('informaticaComponentSearch')?.value.toLowerCase() || '';
            const typeFilter = document.getElementById('informaticaTypeFilter')?.value.toLowerCase() || '';
            const rows = document.querySelectorAll('#informatica-report .component-row');
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
            const countElement = document.getElementById('informaticaComponentCount');
            if (countElement) {
                countElement.textContent = `Showing ${visibleCount} of ${totalCount} component types`;
            }
        }

        // Expose globally for onclick handlers
        window.filterInformaticaWorkflows = filterInformaticaWorkflows;
        window.resetInformaticaFilters = resetInformaticaFilters;
        window.filterInformaticaComponents = filterInformaticaComponents;

        // Attach event listeners
        document.getElementById('informaticaWorkflowSearch')?.addEventListener('input', filterInformaticaWorkflows);
        document.getElementById('informaticaClassificationFilter')?.addEventListener('change', filterInformaticaWorkflows);
        document.getElementById('informaticaComplexityFilter')?.addEventListener('change', filterInformaticaWorkflows);
        document.getElementById('informaticaComponentSearch')?.addEventListener('keyup', filterInformaticaComponents);
        document.getElementById('informaticaTypeFilter')?.addEventListener('change', filterInformaticaComponents);

        // Initialize count displays
        window.addEventListener('load', function() {
            filterInformaticaWorkflows();
            filterInformaticaComponents();
        });
    })();
    """


def _generate_css() -> str:
    """Generate scoped CSS for Informatica tab.

    Only overrides what is NOT provided by the global multi-tab CSS:
    - h2 blue underline (section headings)
    - Row hover/alternating colors for workflow and component tables
    - Dark tooltip (matching SSIS design)
    - Info/warning boxes
    - Overrides for .metric-card cursor and .exclusion-table td white-space

    The following are provided globally and NOT duplicated here:
    - .metric-grid, .metric-card, .metric-label, .metric-value, .metric-description
    - .exclusion-table, .exclusion-table thead, .exclusion-table th, .exclusion-table td
    """
    return """
    /* Section heading style — matches SSIS h2 design */
    #informatica-report h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #102E46;
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #29B5E8;
    }

    /* Override cursor from global metric-card (help -> default) */
    #informatica-report .metric-card {
        cursor: default;
    }

    /* Chart container — matches SSIS .chart-container */
    #informatica-report .chart-container {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Workflow classification table — no overflow anywhere so tooltip is never clipped */
    #informaticaWorkflowTable {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    #informaticaWorkflowTable thead th:first-child {
        border-top-left-radius: 8px;
    }
    #informaticaWorkflowTable thead th:last-child {
        border-top-right-radius: 8px;
    }
    #informaticaWorkflowTable thead {
        background: #29B5E8;
        color: white;
    }
    #informaticaWorkflowTable th {
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    #informaticaWorkflowTable td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E2E8F0;
        font-size: 0.85rem;
    }
    #informaticaWorkflowTable tbody tr:nth-child(even) {
        background: #F9FAFB;
    }
    #informaticaWorkflowTable tbody tr:hover {
        background: #E5F6FD;
    }
    #informaticaWorkflowTable tbody tr:nth-child(even):hover {
        background: #E5F6FD;
    }

    /* Workflow row — positioned for tooltip (same as SSIS .package-row) */
    #informaticaWorkflowTable .workflow-row {
        position: relative;
    }

    /* Component row styles (alternating + hover) */
    #informatica-report .component-row:nth-child(even) {
        background: #F9FAFB;
    }
    #informatica-report .component-row:hover {
        background: #E5F6FD !important;
    }

    /* Info box - blue left border */
    #informatica-report .info-box {
        background: #F0F9FF;
        border-left: 4px solid #29B5E8;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        border-radius: 4px;
    }

    /* Warning box - amber left border */
    #informatica-report .warning-box {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        border-radius: 4px;
    }

    /* Dark tooltip — identical to SSIS .package-row .ai-tooltip */
    #informaticaWorkflowTable .workflow-row .ai-tooltip {
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
        text-align: left;
    }

    /* Tooltip arrow pointing down */
    #informaticaWorkflowTable .workflow-row .ai-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 8px solid transparent;
        border-top-color: #1e293b;
    }

    /* Show tooltip on row hover */
    #informaticaWorkflowTable .workflow-row:hover .ai-tooltip {
        visibility: visible;
        opacity: 1;
    }

    /* Tooltip header */
    #informaticaWorkflowTable .ai-tooltip-header {
        font-weight: 600;
        color: #29B5E8;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #334155;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Tooltip content */
    #informaticaWorkflowTable .ai-tooltip-content {
        color: #cbd5e1;
    }

    /* Tooltip pending state */
    #informaticaWorkflowTable .ai-tooltip-pending {
        color: #94a3b8;
        font-style: italic;
        text-align: center;
        padding: 0.5rem;
    }
    """


def _safe_filename(name: str) -> str:
    """Convert name to filesystem-safe string."""
    result = re.sub(r"[^\w]", "_", name)
    result = re.sub(r"_+", "_", result)
    return result.strip("_").lower()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_informatica_report_content.py <informatica_json_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    content_html, js, css = generate_informatica_html_content(json_path)
    print("HTML Content Generated Successfully")
    print(f"HTML Length: {len(content_html)} characters")
    print(f"JS Length: {len(js)} characters")
    print(f"CSS Length: {len(css)} characters")
