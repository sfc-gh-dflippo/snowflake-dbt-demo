# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
"""Adapter that exposes `waves_analysis_*.json` (camelCase, schemaVersion 1)
in the snake_case shapes the HTML generators consume.

The input schema mirrors what `scai assessment waves` emits today:
camelCase keys, `schemaVersion: 1`, nested `graphSummary.connectivity` /
`graphSummary.statistics`, top-level `missingCodeUnits`, etc. Registry-sourced
enrichment fields (`name`, `category`, `conversionStatus`, `fileName`,
`missingDependencies`, …) are overlaid by the `waves_from_registry` synthesizer
before the adapter reads the file.

All public methods return dict shapes with snake_case keys because the HTML
templates and `generate_multi_report.py` / `generate_html_report.py` still
index into the legacy names. That output contract is stable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


class WavesJsonAdapter:
    def __init__(self, json_path: str | Path) -> None:
        self._path = Path(json_path)
        if not self._path.exists():
            raise FileNotFoundError(f"Waves JSON not found: {self._path}")
        try:
            with self._path.open("r", encoding="utf-8") as fh:
                self._data: dict[str, Any] = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Malformed waves JSON at {self._path}: {exc}"
            ) from exc
        self._memo: dict[str, Any] = {}

    def _cache(self, key: str, fn: Callable[[], Any]) -> Any:
        if key not in self._memo:
            self._memo[key] = fn()
        return self._memo[key]

    @staticmethod
    def _derive_is_root(obj: dict[str, Any]) -> bool:
        if "isRoot" in obj:
            return bool(obj.get("isRoot"))
        return int(obj.get("totalDirectDependencies", 0) or 0) == 0

    @staticmethod
    def _derive_is_leaf(obj: dict[str, Any]) -> bool:
        if "isLeaf" in obj:
            return bool(obj.get("isLeaf"))
        return int(obj.get("totalDirectDependents", 0) or 0) == 0

    def total_objects(self) -> int:
        return len(self._data.get("objects", []))

    def total_waves(self) -> int:
        return len(self._data.get("partitions", []))

    def objects_by_type(self) -> dict[str, int]:
        def build() -> dict[str, int]:
            counts: dict[str, int] = {}
            for obj in self._data.get("objects", []):
                cat = obj.get("category") or "UNKNOWN"
                counts[cat] = counts.get(cat, 0) + 1
            return counts
        return self._cache("objects_by_type", build)

    def conversion_status_counts(self) -> dict[str, int]:
        def build() -> dict[str, int]:
            counts: dict[str, int] = {}
            for obj in self._data.get("objects", []):
                status = obj.get("conversionStatus") or "Unknown"
                counts[status] = counts.get(status, 0) + 1
            return counts
        return self._cache("conversion_status_counts", build)

    def temporal_tables_count(self) -> int:
        def build() -> int:
            count = 0
            for obj in self._data.get("objects", []):
                name = obj.get("name", "") or ""
                bare = name.replace("[", "").replace("]", "").rsplit(".", 1)[-1]
                if bare.startswith("#"):
                    count += 1
            return count
        return self._cache("temporal_tables_count", build)

    def external_tables_count(self) -> int:
        def build() -> int:
            return sum(
                1 for obj in self._data.get("objects", [])
                if (obj.get("category") or "").upper() == "EXTERNAL TABLE"
            )
        return self._cache("external_tables_count", build)

    def graph_summary(self) -> dict[str, Any]:
        def build() -> dict[str, Any]:
            raw = self._data.get("graphSummary", {}) or {}
            conn = raw.get("connectivity", {}) or {}
            stats = raw.get("statistics", {}) or {}
            return {
                "total_nodes": raw.get("nodes", 0),
                "total_edges": raw.get("edges", 0),
                "avg_dependencies": raw.get("averageDependenciesPerNode", 0.0),
                "weakly_connected_components": conn.get("weaklyConnectedCodeUnits", 0),
                "strongly_connected_components": conn.get("stronglyConnectedCodeUnits", 0),
                "cyclic_dependencies": conn.get("cyclicDependenciesCount", 0),
                "root_nodes": stats.get("codeUnitsWithoutDependencies", 0),
                "leaf_nodes": stats.get("codeUnitsWithoutDependents", 0),
                "max_dependencies": stats.get("maxDependenciesPerCodeUnit", 0),
                "max_dependents": stats.get("maxDependentsPerCodeUnit", 0),
            }
        return self._cache("graph_summary", build)

    def cycles(self) -> list[dict[str, Any]]:
        def build() -> list[dict[str, Any]]:
            return [
                {
                    "cycle_num": c.get("sccId"),
                    "node_count": c.get("size", len(c.get("nodes") or [])),
                    "nodes": list(c.get("nodes") or []),
                }
                for c in self._data.get("cycles", []) or []
            ]
        return self._cache("cycles", build)

    def excluded_edges(self) -> dict[str, Any]:
        def build() -> dict[str, Any]:
            raw = self._data.get("missingCodeUnits", {}) or {}
            total_refs = int(raw.get("totalReferences", 0) or 0)
            total_missing = int(raw.get("totalCount", 0) or 0)
            relations = raw.get("relationTypes", {}) or {}
            return {
                "total_excluded": total_refs,
                "undefined_caller": 0,
                "undefined_referenced": total_missing,
                "both_undefined": 0,
                "exclusion_reasons": [],
                "relation_types": [
                    {"type": k, "count": v} for k, v in relations.items()
                ],
                "top_undefined_referenced": [
                    {
                        "object": cu.get("canonicalName") or cu.get("id", ""),
                        "count": int(cu.get("requiredByCount", 0) or 0),
                    }
                    for cu in (raw.get("codeUnits") or [])
                    if isinstance(cu, dict)
                ],
            }
        return self._cache("excluded_edges", build)

    def partition_membership(self) -> dict[str, dict[str, Any]]:
        def build() -> dict[str, dict[str, Any]]:
            membership: dict[str, dict[str, Any]] = {}
            for obj in self._data.get("objects", []):
                oid = obj.get("id")
                if not oid:
                    continue
                membership[oid] = {
                    "partition": obj.get("partitionNumber"),
                    "is_root": self._derive_is_root(obj),
                    "is_leaf": self._derive_is_leaf(obj),
                    "is_picked_scc": bool(obj.get("isWaveSeed", False)),
                    "category": obj.get("category", ""),
                    "file_name": obj.get("fileName", ""),
                    "technology": obj.get("technology", ""),
                    "conversion_status": obj.get("conversionStatus", ""),
                    "subtype": obj.get("subtype", ""),
                    "partition_type": obj.get("partitionType", ""),
                }
            return membership
        return self._cache("partition_membership", build)

    def dependency_counts(self) -> dict[str, dict[str, int]]:
        def build() -> dict[str, dict[str, int]]:
            counts: dict[str, dict[str, int]] = {}
            for obj in self._data.get("objects", []):
                oid = obj.get("id")
                if not oid:
                    continue
                counts[oid] = {
                    "direct_dependencies": int(obj.get("totalDirectDependencies", 0) or 0),
                    "direct_dependents": int(obj.get("totalDirectDependents", 0) or 0),
                    "total_dependencies": int(obj.get("totalDependencies", 0) or 0),
                    "total_dependents": int(obj.get("totalDependents", 0) or 0),
                }
            return counts
        return self._cache("dependency_counts", build)

    def missing_dependencies(self) -> dict[str, dict[str, Any]]:
        def build() -> dict[str, dict[str, Any]]:
            result: dict[str, dict[str, Any]] = {}
            for obj in self._data.get("objects", []):
                oid = obj.get("id")
                if not oid:
                    continue
                missing_count = int(obj.get("missingCount", 0) or 0)
                raw_deps = obj.get("missingDependencies") or []
                deps: list[dict[str, Any]] = []
                for d in raw_deps:
                    if not isinstance(d, dict):
                        continue
                    deps.append({
                        "referenced": d.get("referenced", ""),
                        "relation_type": d.get("relationType", d.get("relation_type", "")),
                        "line": d.get("line", ""),
                        "file": d.get("file", obj.get("fileName", "")),
                    })
                result[oid] = {
                    "object_name": obj.get("name", oid),
                    "object_category": obj.get("category", ""),
                    "object_file": obj.get("fileName", ""),
                    "has_missing_dependencies": missing_count > 0,
                    "missing_count": missing_count,
                    "missing_dependencies": deps,
                }
            return result
        return self._cache("missing_dependencies", build)

    def missing_object_refs(self) -> dict[str, Any]:
        def build() -> dict[str, Any]:
            missing: set[str] = set()
            dependents: dict[str, list[dict[str, Any]]] = {}
            for obj in self._data.get("objects", []):
                caller = obj.get("id")
                if not caller:
                    continue
                for d in obj.get("missingDependencies", []) or []:
                    if not isinstance(d, dict):
                        continue
                    ref = d.get("referenced")
                    if not ref:
                        continue
                    missing.add(ref)
                    dependents.setdefault(ref, []).append({
                        "caller": caller,
                        "relation_type": d.get("relationType", d.get("relation_type", "")),
                        "line": d.get("line", ""),
                        "file_name": d.get("file", obj.get("fileName", "")),
                    })
            metadata = self._data.get("metadata", {}) or {}
            return {
                "missing_objects": missing,
                "dependents": dependents,
                "details": [],
                "data_source": metadata.get("missingDependenciesSource", "json"),
                "warning": None,
            }
        return self._cache("missing_object_refs", build)

    def wave_deployment_order(self) -> dict[str, dict[str, Any]]:
        def build() -> dict[str, dict[str, Any]]:
            by_id = {
                obj["id"]: obj
                for obj in self._data.get("objects", [])
                if obj.get("id")
            }
            result: dict[str, dict[str, Any]] = {}
            for p in self._data.get("partitions", []) or []:
                num = p.get("partitionNumber")
                order = list(p.get("deploymentOrder", []) or [])
                detail: list[dict[str, Any]] = []
                for idx, oid in enumerate(order):
                    obj = by_id.get(oid, {})
                    detail.append({
                        "name": obj.get("name", oid),
                        "category": obj.get("category", ""),
                        "is_root": self._derive_is_root(obj) if obj else False,
                        "is_leaf": self._derive_is_leaf(obj) if obj else False,
                        "deployment_position": idx + 1,
                    })
                result[str(num)] = {
                    "wave_number": str(num),
                    "deployment_order": order,
                    "total_objects": p.get("size", len(order)),
                    "objects_detail": detail,
                }
            return result
        return self._cache("wave_deployment_order", build)

    def warnings(self) -> list[str]:
        metadata = self._data.get("metadata", {}) or {}
        return list(metadata.get("warnings", []) or [])
