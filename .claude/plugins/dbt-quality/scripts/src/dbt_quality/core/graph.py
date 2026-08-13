"""
Adapter over ``target/manifest.json``.

The audit never runs dbt itself -- it must be safe to point at an unfamiliar
repo with no warehouse credentials and no write access to ``target/``. So the
graph is optional: rules that need it declare ``requires_manifest=True`` and are
reported as *skipped* rather than silently passing when it is absent.

That distinction matters. "No layer-crossing dependencies found" and "we could
not check for layer-crossing dependencies" are very different statements to put
in front of a customer, and conflating them would overstate a project's health.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Graph:
    """
    Node and edge view of a dbt project derived from its manifest.

    ``available`` is False when no manifest was found, in which case every
    accessor returns an empty result and manifest-dependent rules are skipped.
    """

    available: bool = False
    stale: bool = False
    path: Path | None = None
    #: node unique_id -> node dict
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: model name -> unique_id
    by_name: dict[str, str] = field(default_factory=dict)
    #: unique_id -> list of child unique_ids
    children: dict[str, list[str]] = field(default_factory=dict)
    #: source unique_id -> list of child unique_ids
    source_children: dict[str, list[str]] = field(default_factory=dict)

    def child_count(self, model_name: str) -> int:
        """How many nodes reference this model. 0 when the graph is unavailable."""
        uid = self.by_name.get(model_name)
        if uid is None:
            return 0
        return len(self.children.get(uid, []))

    def child_names(self, model_name: str) -> list[str]:
        uid = self.by_name.get(model_name)
        if uid is None:
            return []
        return [
            self.nodes.get(c, {}).get("name", c) for c in self.children.get(uid, [])
        ]

    def parent_names(self, model_name: str) -> list[str]:
        uid = self.by_name.get(model_name)
        if uid is None:
            return []
        node = self.nodes.get(uid, {})
        parents = node.get("depends_on", {}).get("nodes", [])
        return [
            self.nodes.get(p, {}).get("name", p)
            for p in parents
            if p.startswith("model.")
        ]

    def node(self, model_name: str) -> dict[str, Any]:
        uid = self.by_name.get(model_name)
        return self.nodes.get(uid, {}) if uid else {}

    def description(self, model_name: str) -> str:
        return str(self.node(model_name).get("description", ""))

    def materialization(self, model_name: str) -> str:
        return str(self.node(model_name).get("config", {}).get("materialized", ""))

    def fqn_layer(self, model_name: str) -> str:
        """Second FQN element, which for this project layout is the layer folder."""
        fqn = self.node(model_name).get("fqn", [])
        return fqn[1] if len(fqn) > 1 else ""

    def depends_on_sources(self, model_name: str) -> list[str]:
        uid = self.by_name.get(model_name)
        if uid is None:
            return []
        parents = self.nodes.get(uid, {}).get("depends_on", {}).get("nodes", [])
        return [p for p in parents if p.startswith("source.")]

    def test_nodes_for(self, model_name: str) -> list[dict[str, Any]]:
        """Test nodes attached to a model, from the manifest's child edges."""
        uid = self.by_name.get(model_name)
        if uid is None:
            return []
        out: list[dict[str, Any]] = []
        for child in self.children.get(uid, []):
            if child.startswith("test."):
                out.append(self.nodes.get(child, {}))
        return out


def load_graph(project_root: Path, newest_source_mtime: float | None = None) -> Graph:
    """
    Load ``target/manifest.json`` if present.

    ``stale`` is set when any model file is newer than the manifest, which is
    the common case where someone parsed once weeks ago. A stale graph is still
    used -- partial lineage beats none -- but the report says so, because a
    model added since the parse would otherwise look like it has no children.
    """
    manifest_path = project_root / "target" / "manifest.json"
    if not manifest_path.is_file():
        return Graph(available=False)

    try:
        with manifest_path.open(encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return Graph(available=False)

    graph = Graph(available=True, path=manifest_path)

    if newest_source_mtime is not None:
        graph.stale = manifest_path.stat().st_mtime < newest_source_mtime

    graph.nodes = dict(raw.get("nodes", {}))
    graph.nodes.update(raw.get("sources", {}))

    for uid, node in graph.nodes.items():
        if uid.startswith("model."):
            graph.by_name[str(node.get("name", ""))] = uid

    # Prefer the manifest's own child_map when present; otherwise invert
    # depends_on. child_map is absent from partial parses.
    child_map = raw.get("child_map")
    if isinstance(child_map, dict) and child_map:
        for uid, kids in child_map.items():
            if uid.startswith("source."):
                graph.source_children[uid] = list(kids)
            else:
                graph.children[uid] = list(kids)
    else:
        for uid, node in graph.nodes.items():
            for parent in node.get("depends_on", {}).get("nodes", []):
                if parent.startswith("source."):
                    graph.source_children.setdefault(parent, []).append(uid)
                else:
                    graph.children.setdefault(parent, []).append(uid)

    return graph
