# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

"""Informatica DAG Service — Interactive Cytoscape.js DAG visualizations.

Generates interactive HTML DAG pages for Informatica workflows and mappings,
matching the SSIS report DAG format with:
- Cytoscape.js + dagre layout
- Zoom/Fit/Layout controls
- Clickable nodes for navigation between workflow and mapping DAGs
- Node highlighting and SQL tooltips

Edge data is read from the 'successors' field in component additional_info
(produced by SnowConvert's ETL.Elements.csv report), avoiding slow XML parsing.
"""

import json
from html import escape
from pathlib import Path
from typing import Dict, List, Optional


class InformaticaDagService:
    """Service for generating interactive DAG visualizations for Informatica."""

    # ==========================================================================
    # Node Color Mapping
    # ==========================================================================

    @staticmethod
    def get_node_color(status: str) -> Dict[str, str]:
        """Get node color based on conversion status."""
        s = (status or "").upper()
        if s == "SUCCESS":
            return {"background": "#DCFCE7", "border": "#22C55E"}
        elif s == "PARTIAL":
            return {"background": "#FEF3C7", "border": "#F59E0B"}
        elif s == "NOTSUPPORTED":
            return {"background": "#FEE2E2", "border": "#EF4444"}
        else:
            return {"background": "#F3F4F6", "border": "#6B7280"}

    # ==========================================================================
    # Edge Extraction from Component Data (successors in additional_info)
    # ==========================================================================

    @classmethod
    def extract_edges_from_components(cls, components: List[Dict]) -> List[Dict[str, str]]:
        """Extract edges from 'successors' in component additional_info.

        Reads the successors field produced by SnowConvert's ETL.Elements.csv report.
        Returns list of {from: short_name, to: successor_name} deduplicated.
        """
        edges = []
        seen = set()

        # Build a set of valid node IDs (short names) for edge validation
        valid_nodes = set()
        for comp in components:
            full_name = comp.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            if short_name:
                valid_nodes.add(short_name)

        for comp in components:
            full_name = comp.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            if not short_name:
                continue

            # Parse additional_info JSON
            additional_info_str = comp.get("additional_info", "")
            if not additional_info_str:
                continue

            try:
                additional_info = json.loads(additional_info_str) if isinstance(additional_info_str, str) else additional_info_str
            except (json.JSONDecodeError, TypeError):
                continue

            successors = additional_info.get("successors", [])
            for successor in successors:
                # Successor may be a full name or short name
                successor_short = successor.split(".")[-1] if "." in successor else successor
                if successor_short and successor_short in valid_nodes:
                    key = (short_name, successor_short)
                    if key not in seen:
                        seen.add(key)
                        edges.append({"from": short_name, "to": successor_short})

        return edges

    @classmethod
    def extract_workflow_edges_from_tasks(cls, tasks: List[Dict]) -> List[Dict[str, str]]:
        """Extract workflow task edges from 'successors' in additional_info.

        Returns list of {from: task_short_name, to: task_short_name}.
        """
        edges = []
        seen = set()

        # Build a set of valid node IDs (short names)
        valid_nodes = set()
        for task in tasks:
            full_name = task.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            if short_name:
                valid_nodes.add(short_name)

        for task in tasks:
            full_name = task.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            if not short_name:
                continue

            additional_info_str = task.get("additional_info", "")
            if not additional_info_str:
                continue

            try:
                additional_info = json.loads(additional_info_str) if isinstance(additional_info_str, str) else additional_info_str
            except (json.JSONDecodeError, TypeError):
                continue

            successors = additional_info.get("successors", [])
            for successor in successors:
                successor_short = successor.split(".")[-1] if "." in successor else successor
                if successor_short and successor_short in valid_nodes:
                    key = (short_name, successor_short)
                    if key not in seen:
                        seen.add(key)
                        edges.append({"from": short_name, "to": successor_short})

        return edges

    # ==========================================================================
    # Fallback Edge Inference (when XML not available)
    # ==========================================================================

    @classmethod
    def infer_mapping_edges(cls, components: List[Dict]) -> List[Dict[str, str]]:
        """Infer data flow edges from component types when XML is unavailable.

        Heuristic: Sources → Source Qualifiers → Transforms → Targets
        Components are connected in sequence within their category tier.
        """
        # Classify components by role
        sources = []
        source_qualifiers = []
        transforms = []
        targets = []

        source_types = {"Source Definition"}
        sq_types = {"Source Qualifier"}
        target_types = {"Target Definition"}

        for comp in components:
            subtype = comp.get("subtype", "")
            name = comp.get("full_name", "").split(".")[-1] if comp.get("full_name") else ""
            if subtype in source_types:
                sources.append(name)
            elif subtype in sq_types:
                source_qualifiers.append(name)
            elif subtype in target_types:
                targets.append(name)
            else:
                transforms.append(name)

        edges = []
        # Sources → Source Qualifiers (or first transform if no SQ)
        next_tier = source_qualifiers or transforms or targets
        for src in sources:
            for nxt in next_tier[:1]:  # Connect to first of next tier
                edges.append({"from": src, "to": nxt})

        # Source Qualifiers → Transforms
        if source_qualifiers and transforms:
            for sq in source_qualifiers:
                edges.append({"from": sq, "to": transforms[0]})

        # Chain transforms
        for i in range(len(transforms) - 1):
            edges.append({"from": transforms[i], "to": transforms[i + 1]})

        # Last transform → Targets
        last_transform = transforms[-1] if transforms else (source_qualifiers[-1] if source_qualifiers else (sources[-1] if sources else None))
        if last_transform:
            for tgt in targets:
                edges.append({"from": last_transform, "to": tgt})

        return edges

    @classmethod
    def infer_workflow_edges(cls, tasks: List[Dict]) -> List[Dict[str, str]]:
        """Infer workflow task edges when XML is unavailable (sequential chain)."""
        edges = []
        task_names = []
        for t in tasks:
            name = t.get("full_name", "").split(".")[-1] if t.get("full_name") else ""
            if name:
                task_names.append(name)

        for i in range(len(task_names) - 1):
            edges.append({"from": task_names[i], "to": task_names[i + 1]})

        return edges

    # ==========================================================================
    # Cytoscape.js HTML Generation
    # ==========================================================================

    @classmethod
    def generate_dag_html(
        cls,
        title: str,
        subtitle: str,
        nodes: List[Dict],
        edges: List[Dict],
        dag_type: str = "data_flow",
        clickable_links: Optional[Dict[str, str]] = None,
        back_link: Optional[str] = None,
        back_link_title: Optional[str] = None,
        node_metadata: Optional[Dict[str, Dict]] = None,
    ) -> str:
        """Generate interactive DAG HTML using Cytoscape.js.

        Args:
            title: Main title
            subtitle: Subtitle (path info)
            nodes: List of {id, label, status, color:{background, border}, parent?}
            edges: List of {from, to}
            dag_type: 'data_flow' or 'control_flow'
            clickable_links: Dict mapping node ID → URL for navigation
            back_link: URL for back button
            back_link_title: Label for back button
        """
        clickable_links = clickable_links or {}
        node_metadata = node_metadata or {}

        # Serialize metadata for JS
        metadata_json = json.dumps(node_metadata)
        cy_elements = []
        for node in nodes:
            node_id = node["id"]
            is_clickable = node_id in clickable_links
            link_url = clickable_links.get(node_id, "")

            cy_node = {
                "data": {
                    "id": node_id,
                    "label": node["label"],
                    "status": node.get("status", "Unknown"),
                    "subtype": node.get("subtype", "Unknown"),
                    "bgColor": node["color"]["background"],
                    "borderColor": node["color"]["border"],
                    "isClickable": is_clickable,
                    "linkUrl": link_url,
                }
            }
            if node.get("parent"):
                cy_node["data"]["parent"] = node["parent"]
            cy_elements.append(cy_node)

        for edge in edges:
            cy_elements.append(
                {
                    "data": {
                        "id": f"{edge['from']}_to_{edge['to']}",
                        "source": edge["from"],
                        "target": edge["to"],
                    }
                }
            )

        elements_json = json.dumps(cy_elements)

        # Header gradient based on type
        header_gradient = (
            "linear-gradient(135deg, #3B82F6, #2563EB)"
            if dag_type == "data_flow"
            else "linear-gradient(135deg, #8B5CF6, #7C3AED)"
        )

        # Back button
        back_button_html = ""
        if back_link:
            back_title = back_link_title or "Back to Workflow"
            back_button_html = f"""
    <a href="{back_link}" class="back-btn">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 12H5M12 19l-7-7 7-7"/>
      </svg>
      {escape(back_title)}
    </a>"""

        # Clickable hint
        hint_text = ""
        if clickable_links:
            hint_text = "Click highlighted nodes to view Mapping DAG"

        return f"""<!DOCTYPE html>
<html>
<head>
  <title>{escape(title)}</title>
  <script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js" onerror="document.getElementById('cy-error').style.display='flex'"></script>
  <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js" onerror="document.getElementById('cy-error').style.display='flex'"></script>
  <script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js" onerror="document.getElementById('cy-error').style.display='flex'"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #F9FAFB; min-height: 100vh; }}
    .header {{
      background: {header_gradient};
      color: white;
      padding: 20px 24px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .header h1 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 4px; }}
    .header p {{ font-size: 0.875rem; opacity: 0.9; }}
    .controls {{
      padding: 12px 24px;
      background: white;
      border-bottom: 1px solid #E5E7EB;
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .controls button {{
      padding: 6px 16px;
      background: #6B7280;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.875rem;
    }}
    .controls button:hover {{ background: #4B5563; }}
    #cy {{
      height: calc(100vh - 180px);
      background: white;
      margin: 16px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .legend {{
      display: flex;
      gap: 20px;
      padding: 12px 24px;
      background: white;
      justify-content: center;
      flex-wrap: wrap;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      color: #4B5563;
    }}
    .legend-color {{
      width: 16px;
      height: 16px;
      border-radius: 4px;
      border: 2px solid;
    }}
    .legend-success {{ background: #DCFCE7; border-color: #22C55E; }}
    .legend-partial {{ background: #FEF3C7; border-color: #F59E0B; }}
    .legend-notsupported {{ background: #FEE2E2; border-color: #EF4444; }}
    .legend-unknown {{ background: #F3F4F6; border-color: #6B7280; }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: rgba(255,255,255,0.2);
      color: white;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      transition: background 0.2s;
      margin-bottom: 8px;
    }}
    .back-btn:hover {{ background: rgba(255,255,255,0.3); }}
    .clickable-hint {{
      font-size: 0.75rem;
      color: #6B7280;
      margin-left: auto;
    }}
    #info-panel {{
      position: fixed;
      width: 320px;
      background: #1e293b;
      color: #f1f5f9;
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      display: none;
      z-index: 100;
      font-size: 0.8125rem;
      pointer-events: none;
    }}
    #info-panel.visible {{ display: block; }}
    .info-header {{
      padding: 12px 16px;
      border-bottom: 1px solid #334155;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .info-header h3 {{ font-size: 0.875rem; font-weight: 600; margin: 0; }}
    .info-body {{ padding: 12px 16px; }}
    .info-row {{
      margin-bottom: 10px;
    }}
    .info-label {{
      font-size: 0.6875rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      margin-bottom: 3px;
    }}
    .info-value {{
      color: #e2e8f0;
    }}
    .info-badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
    .info-sql {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 8px 10px;
      font-family: 'SF Mono', 'Fira Code', monospace;
      font-size: 0.75rem;
      white-space: pre-wrap;
      word-break: break-all;
      color: #a5f3fc;
    }}
    .info-expr-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .info-expr-list li {{
      padding: 4px 0;
      border-bottom: 1px solid #334155;
      font-family: 'SF Mono', monospace;
      font-size: 0.6875rem;
      color: #d4d4d8;
    }}
    .info-expr-list li:last-child {{ border-bottom: none; }}
    .info-expr-name {{ color: #67e8f9; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="header">{back_button_html}
    <h1>{escape(title)}</h1>
    <p>{escape(subtitle)}</p>
  </div>

  <div class="controls">
    <button id="fitBtn">Fit to Screen</button>
    <button id="zoomInBtn">Zoom In</button>
    <button id="zoomOutBtn">Zoom Out</button>
    <button id="layoutLRBtn" style="background: #3B82F6;">\u2190 \u2192 Left to Right</button>
    <button id="layoutTBBtn">\u2193 Top to Bottom</button>
    <span class="clickable-hint" id="clickHint">{hint_text}</span>
  </div>

  <div id="cy"></div>
  <div id="info-panel">
    <div class="info-header">
      <h3 id="info-title">Node Details</h3>
    </div>
    <div class="info-body" id="info-body"></div>
  </div>
  <div id="cy-error" style="display:none; height: calc(100vh - 180px); margin: 16px; border-radius: 8px; background: #FEF2F2; border: 1px solid #FECACA; align-items: center; justify-content: center; flex-direction: column; gap: 12px;">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
    <p style="color: #991B1B; font-size: 1rem; font-weight: 600;">DAG visualization unavailable</p>
    <p style="color: #7F1D1D; font-size: 0.875rem; max-width: 400px; text-align: center;">Unable to load Cytoscape.js library from CDN. Please ensure internet connectivity and try refreshing the page.</p>
  </div>

  <div class="legend">
    <div class="legend-item"><div class="legend-color legend-success"></div> Success (Supported)</div>
    <div class="legend-item"><div class="legend-color legend-partial"></div> Partial (Needs Review)</div>
    <div class="legend-item"><div class="legend-color legend-notsupported"></div> Not Supported</div>
    <div class="legend-item"><div class="legend-color legend-unknown"></div> Unknown</div>
  </div>

  <script>
    if (typeof cytoscape === 'undefined') {{
      document.getElementById('cy').style.display = 'none';
      document.getElementById('cy-error').style.display = 'flex';
    }} else {{
    const elements = {elements_json};
    const nodeMetadata = {metadata_json};

    const cy = cytoscape({{
      container: document.getElementById('cy'),
      elements: elements,
      style: [
        {{
          selector: 'node',
          style: {{
            'label': 'data(label)',
            'text-wrap': 'wrap',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '11px',
            'font-family': 'system-ui, sans-serif',
            'background-color': 'data(bgColor)',
            'border-color': 'data(borderColor)',
            'border-width': 2,
            'padding': '10px',
            'shape': 'roundrectangle',
            'width': 'label',
            'height': 'label'
          }}
        }},
        {{
          selector: 'edge',
          style: {{
            'width': 2,
            'line-color': '#6B7280',
            'target-arrow-color': '#6B7280',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'arrow-scale': 1.2
          }}
        }},
        {{
          selector: 'node:selected',
          style: {{
            'border-width': 4,
            'border-color': '#3B82F6'
          }}
        }},
        {{
          selector: '.highlighted',
          style: {{
            'border-width': 4,
            'border-color': '#3B82F6',
            'line-color': '#3B82F6',
            'target-arrow-color': '#3B82F6'
          }}
        }},
        {{
          selector: 'node[?isClickable]',
          style: {{
            'border-width': 3,
            'border-style': 'solid',
            'cursor': 'pointer'
          }}
        }},
        {{
          selector: 'node[?isClickable]:hover',
          style: {{
            'border-color': '#2563EB',
            'overlay-color': '#3B82F6',
            'overlay-opacity': 0.1
          }}
        }}
      ],
      layout: {{ name: 'preset' }}
    }});

    // Compute levels based on topological order
    function computeLevels() {{
      const nodes = cy.nodes();
      const edges = cy.edges();
      const successors = {{}};
      const predecessors = {{}};
      const indegree = {{}};

      nodes.forEach(n => {{
        const id = n.id();
        successors[id] = [];
        predecessors[id] = [];
        indegree[id] = 0;
      }});

      edges.forEach(e => {{
        const src = e.data('source');
        const tgt = e.data('target');
        if (successors[src] && predecessors[tgt]) {{
          successors[src].push(tgt);
          predecessors[tgt].push(src);
          indegree[tgt]++;
        }}
      }});

      const level = {{}};
      const order = {{}};
      const queue = [];

      nodes.forEach(n => {{
        const id = n.id();
        if (indegree[id] === 0) {{
          level[id] = 0;
          queue.push(id);
        }}
      }});

      let orderIdx = 0;
      const processed = new Set();

      while (queue.length > 0) {{
        queue.sort((a, b) => (level[a] || 0) - (level[b] || 0));
        const current = queue.shift();
        if (processed.has(current)) continue;
        processed.add(current);
        order[current] = orderIdx++;

        for (const next of (successors[current] || [])) {{
          const newLevel = (level[current] || 0) + 1;
          level[next] = Math.max(level[next] || 0, newLevel);
          indegree[next]--;
          if (indegree[next] === 0) queue.push(next);
        }}
      }}

      nodes.forEach(n => {{
        const id = n.id();
        if (!processed.has(id)) {{
          level[id] = 0;
          order[id] = orderIdx++;
        }}
      }});

      const levelGroups = {{}};
      nodes.forEach(n => {{
        const id = n.id();
        const lvl = level[id] || 0;
        if (!levelGroups[lvl]) levelGroups[lvl] = [];
        levelGroups[lvl].push({{ id, order: order[id], node: n }});
      }});

      Object.keys(levelGroups).forEach(lvl => {{
        levelGroups[lvl].sort((a, b) => a.order - b.order);
      }});

      return {{ levelGroups, levels: Object.keys(levelGroups).map(Number).sort((a, b) => a - b) }};
    }}

    function computePositionsLR() {{
      const {{ levelGroups, levels }} = computeLevels();
      const levelWidth = 250;
      const nodeHeight = 120;
      const startX = 100;
      const startY = 100;
      const positions = {{}};

      levels.forEach(lvl => {{
        const group = levelGroups[lvl];
        const x = startX + lvl * levelWidth;
        group.forEach((item, idx) => {{
          positions[item.id] = {{ x, y: startY + idx * nodeHeight }};
        }});
      }});
      return positions;
    }}

    function computePositionsTB() {{
      const {{ levelGroups, levels }} = computeLevels();
      const levelHeight = 150;
      const nodeWidth = 200;
      const startX = 100;
      const startY = 100;
      const positions = {{}};

      levels.forEach(lvl => {{
        const group = levelGroups[lvl];
        const y = startY + lvl * levelHeight;
        group.forEach((item, idx) => {{
          positions[item.id] = {{ x: startX + idx * nodeWidth, y }};
        }});
      }});
      return positions;
    }}

    function runLayout(direction) {{
      const positions = direction === 'TB' ? computePositionsTB() : computePositionsLR();
      cy.nodes().forEach(n => {{
        const pos = positions[n.id()];
        if (pos) n.position(pos);
      }});
      cy.fit(50);

      const lrBtn = document.getElementById('layoutLRBtn');
      const tbBtn = document.getElementById('layoutTBBtn');
      if (direction === 'TB') {{
        tbBtn.style.background = '#3B82F6';
        lrBtn.style.background = '#6B7280';
      }} else {{
        lrBtn.style.background = '#3B82F6';
        tbBtn.style.background = '#6B7280';
      }}
    }}

    runLayout('LR');

    // Controls
    document.getElementById('fitBtn').addEventListener('click', () => cy.fit(50));
    document.getElementById('zoomInBtn').addEventListener('click', () => cy.zoom(cy.zoom() * 1.2));
    document.getElementById('zoomOutBtn').addEventListener('click', () => cy.zoom(cy.zoom() / 1.2));
    document.getElementById('layoutLRBtn').addEventListener('click', () => runLayout('LR'));
    document.getElementById('layoutTBBtn').addEventListener('click', () => runLayout('TB'));

    // Highlight on click (non-clickable nodes)
    cy.on('tap', 'node[!isClickable]', function(evt) {{
      cy.elements().removeClass('highlighted');
      evt.target.addClass('highlighted');
      evt.target.neighborhood().addClass('highlighted');
    }});

    // Navigate on clickable node
    cy.on('tap', 'node[?isClickable]', function(evt) {{
      const linkUrl = evt.target.data('linkUrl');
      if (linkUrl) window.location.href = linkUrl;
    }});

    cy.on('tap', function(evt) {{
      if (evt.target === cy) {{
        cy.elements().removeClass('highlighted');
      }}
    }});

    // Show info panel on HOVER (matching SSIS tooltip behavior)
    cy.on('mouseover', 'node', function(evt) {{
      showInfoPanel(evt.target);
    }});
    cy.on('mouseout', 'node', function(evt) {{
      document.getElementById('info-panel').classList.remove('visible');
    }});

    // Info panel logic
    function showInfoPanel(node) {{
      const id = node.id();
      const subtype = node.data('subtype') || 'Unknown';
      const status = node.data('status') || 'Unknown';
      const meta = nodeMetadata[id] || {{}};
      const panel = document.getElementById('info-panel');
      const body = document.getElementById('info-body');
      const title = document.getElementById('info-title');

      title.textContent = id;

      // Position panel near the node
      const pos = node.renderedPosition();
      const cyContainer = document.getElementById('cy');
      const cyRect = cyContainer.getBoundingClientRect();
      const panelWidth = 320;
      const panelHeight = 250;

      let left = cyRect.left + pos.x + 20;
      let top = cyRect.top + pos.y - panelHeight / 2;

      // Keep within viewport
      if (left + panelWidth > window.innerWidth) {{
        left = cyRect.left + pos.x - panelWidth - 20;
      }}
      if (top < 10) top = 10;
      if (top + panelHeight > window.innerHeight) {{
        top = window.innerHeight - panelHeight - 10;
      }}

      panel.style.left = left + 'px';
      panel.style.top = top + 'px';

      // Status badge colors
      const statusColors = {{
        'Success': {{bg: '#dcfce7', color: '#166534'}},
        'Partial': {{bg: '#fef3c7', color: '#92400e'}},
        'NotSupported': {{bg: '#fee2e2', color: '#991b1b'}},
      }};
      const sc = statusColors[status] || {{bg: '#f3f4f6', color: '#6b7280'}};

      let html = `
        <div class="info-row">
          <div class="info-label">Type</div>
          <div class="info-value">${{subtype}}</div>
        </div>
        <div class="info-row">
          <div class="info-label">Status</div>
          <div class="info-value"><span class="info-badge" style="background:${{sc.bg}};color:${{sc.color}}">${{status}}</span></div>
        </div>
      `;

      // SQL Query (truncate to 200 chars for tooltip readability)
      const sqlQuery = meta.sql_query || '';
      if (sqlQuery) {{
        const truncSql = sqlQuery.length > 200 ? sqlQuery.substring(0, 200) + '...' : sqlQuery;
        html += `
          <div class="info-row">
            <div class="info-label">SQL Query</div>
            <div class="info-sql">${{truncSql}}</div>
          </div>
        `;
      }}

      // Pre SQL / Post SQL (truncate)
      const preSql = meta.pre_sql || '';
      const postSql = meta.post_sql || '';
      if (preSql) {{
        const t = preSql.length > 150 ? preSql.substring(0, 150) + '...' : preSql;
        html += `<div class="info-row"><div class="info-label">Pre SQL</div><div class="info-sql">${{t}}</div></div>`;
      }}
      if (postSql) {{
        const t = postSql.length > 150 ? postSql.substring(0, 150) + '...' : postSql;
        html += `<div class="info-row"><div class="info-label">Post SQL</div><div class="info-sql">${{t}}</div></div>`;
      }}

      // Source Filter / User Defined Join
      const sourceFilter = meta.source_filter || '';
      const userJoin = meta.user_defined_join || '';
      if (sourceFilter) {{
        html += `<div class="info-row"><div class="info-label">Source Filter</div><div class="info-sql">${{sourceFilter}}</div></div>`;
      }}
      if (userJoin) {{
        html += `<div class="info-row"><div class="info-label">User Defined Join</div><div class="info-sql">${{userJoin}}</div></div>`;
      }}

      // Expressions (show max 4 for compact tooltip)
      const expressions = meta.expressions || [];
      if (expressions.length > 0) {{
        const exprItems = expressions.slice(0, 4).map(e => {{
          const expr = e.expression.length > 60 ? e.expression.substring(0, 60) + '...' : e.expression;
          return `<li><span class="info-expr-name">${{e.name}}</span> = ${{expr}}</li>`;
        }}).join('');
        const moreNote = expressions.length > 4 ? `<li style="color:#94a3b8;font-style:italic">... and ${{expressions.length - 4}} more</li>` : '';
        html += `
          <div class="info-row">
            <div class="info-label">Expressions (${{expressions.length}})</div>
            <ul class="info-expr-list">${{exprItems}}${{moreNote}}</ul>
          </div>
        `;
      }}

      // If no metadata at all
      if (!sqlQuery && !preSql && !postSql && !sourceFilter && !userJoin && expressions.length === 0) {{
        html += `<div class="info-row"><div class="info-value" style="color:#94a3b8;font-style:italic;">No SQL or expression data available for this component.</div></div>`;
      }}

      body.innerHTML = html;
      panel.classList.add('visible');
    }}

    // Cursor for clickable nodes
    cy.on('mouseover', 'node[?isClickable]', function() {{
      document.body.style.cursor = 'pointer';
    }});
    cy.on('mouseout', 'node[?isClickable]', function() {{
      document.body.style.cursor = 'default';
    }});
    }} // end else (cytoscape available)
  </script>
</body>
</html>"""

    # ==========================================================================
    # High-Level DAG Generation
    # ==========================================================================

    @classmethod
    def generate_mapping_dag(
        cls,
        mapping: Dict,
        workflow_name: str,
        output_path: Path,
        xml_path: Optional[str] = None,
        workflow_dag_link: Optional[str] = None,
    ) -> Optional[Path]:
        """Generate interactive DAG HTML for a mapping.

        Args:
            mapping: Mapping dict with 'name', 'components', 'dag_file'
            workflow_name: Parent workflow name
            output_path: Full output path for the DAG HTML file
            xml_path: Ignored (kept for API compatibility)
            workflow_dag_link: Optional link back to workflow DAG
        """
        components = mapping.get("components", [])
        if not components:
            return None

        mapping_name = mapping.get("name", "Unknown")

        # Build nodes
        nodes = []
        # Use short name (last segment of full_name) as node ID for edge matching
        for comp in components:
            full_name = comp.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            subtype = comp.get("subtype", "Unknown")
            status = comp.get("status", "Unknown")
            label = f"{short_name}\n[{subtype}]"
            color = cls.get_node_color(status)
            nodes.append(
                {
                    "id": short_name,
                    "label": label,
                    "subtype": subtype,
                    "status": status,
                    "color": color,
                }
            )

        # Build edges from successors in additional_info (produced by SnowConvert)
        edges = cls.extract_edges_from_components(components)
        if not edges:
            # Fallback to heuristic inference if no successors available
            edges = cls.infer_mapping_edges(components)

        html_content = cls.generate_dag_html(
            title=f"Mapping DAG - {mapping_name}",
            subtitle=f"Workflow: {workflow_name}",
            nodes=nodes,
            edges=edges,
            dag_type="data_flow",
            back_link=workflow_dag_link,
            back_link_title="Back to Workflow DAG",
            node_metadata={},
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path

    @classmethod
    def generate_workflow_dag(
        cls,
        workflow: Dict,
        output_path: Path,
        xml_path: Optional[str] = None,
        mapping_dag_links: Optional[Dict[str, str]] = None,
    ) -> Optional[Path]:
        """Generate interactive DAG HTML for a workflow's task flow.

        Args:
            workflow: Workflow dict with 'workflow_tasks', 'name'
            output_path: Full output path for the DAG HTML file
            xml_path: Ignored (kept for API compatibility)
            mapping_dag_links: Dict mapping task names → mapping DAG URLs
        """
        tasks = workflow.get("workflow_tasks", [])
        if not tasks:
            return None

        workflow_name = workflow.get("name", "Unknown")

        # Build nodes
        nodes = []
        for task in tasks:
            full_name = task.get("full_name", "")
            short_name = full_name.split(".")[-1] if "." in full_name else full_name
            subtype = task.get("subtype", "Unknown")
            status = task.get("status", "Unknown")
            label = f"{short_name}\n[{subtype}]"
            color = cls.get_node_color(status)
            nodes.append(
                {
                    "id": short_name,
                    "label": label,
                    "subtype": subtype,
                    "status": status,
                    "color": color,
                }
            )

        # Build edges from successors in additional_info (produced by SnowConvert)
        edges = cls.extract_workflow_edges_from_tasks(tasks)
        if not edges:
            # Fallback to heuristic inference if no successors available
            edges = cls.infer_workflow_edges(tasks)

        html_content = cls.generate_dag_html(
            title=f"Workflow DAG - {workflow_name}",
            subtitle=f"Control flow task orchestration",
            nodes=nodes,
            edges=edges,
            dag_type="control_flow",
            clickable_links=mapping_dag_links,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path
