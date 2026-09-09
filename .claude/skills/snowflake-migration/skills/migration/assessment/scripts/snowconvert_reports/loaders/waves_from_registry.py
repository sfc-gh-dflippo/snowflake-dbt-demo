# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
"""Synthesize a waves-JSON-compatible dict from the registry.

Every in-scope registry entry becomes a row in `objects[]`, including entries
marked `isMissing: true` or with `objectType == "other"` (which usually means a
referenced target that has no source file). Only `objectType == "schema"` is
skipped (current registry bug, to be fixed upstream). This mirrors what
`scai assessment waves` itself emits — no filtering at the synthesizer layer.

Intrinsic per-object data (name, category, file, status, direct deps, issues)
is pulled from the registry. Algorithmic fields produced by `scai assessment
waves` (partition assignment, is_picked_scc, transitive counts, cycles,
excluded_edges) are mocked until the new waves JSON producer is wired in:

- `partition_number`: 1 for every object (single mock wave)
- `partition_type`: "regular"
- `is_picked_scc`: False
- `total_dependencies` / `total_dependents`: equal to the direct counts
- `cycles`, `excluded_edges.edges`: empty

The output shape matches `WavesJsonAdapter`'s expected input, so the rest of
the report pipeline is untouched.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..conversion_status import is_etl as _is_etl
from ..conversion_status import map_conversion_status as _map_conversion_status
from .registry_loader import (
    build_id_to_name_map,
    load_registry_entries,
)

# Empty — schemas and `other`/missing entries are all valid code units for
# the dependency graph. Extra exclusions (e.g. UDF helpers) are handled
# separately via path-based checks so the filter set stays clean.
SKIP_OBJECT_TYPES: set[str] = set()

# Snowflake-side helper UDFs live under this path prefix in `files.converted`.
# They have no source counterpart and should not appear in the dependency graph.
UDF_HELPER_PATH_MARKER = "UDF Helpers"

MOCK_PARTITION_NUMBER = 1
MOCK_PARTITION_TYPE = "regular"


def _is_udf_helper(entry: dict) -> bool:
    """True when the entry is a Snowflake-side UDF helper (no real source)."""
    converted = (
        entry.get("files", {}).get("converted", {}).get("path", "") or ""
    )
    return UDF_HELPER_PATH_MARKER in converted


def _is_non_toplevel_other(entry: dict) -> bool:
    """True when the entry is ``objectType=other`` but NOT a missing reference.

    These are internal / non-code-unit registry rows (synonyms, indexes, etc.)
    that shouldn't appear as first-class rows. ``other``-typed entries that
    are ``isMissing=true`` stay — they represent real missing references.

    ETL units (``kind == "etl"``) also have ``objectType: other`` at the
    source block; they are exempt from this filter and surface as their own
    category.
    """
    if _is_etl(entry):
        return False
    obj_type = (_source_or_target(entry).get("objectType") or "").lower()
    return obj_type == "other" and not entry.get("isMissing", False)


def _bracket(ident: str) -> str:
    ident = (ident or "").strip()
    if not ident:
        return "[]"
    if ident.startswith("[") and ident.endswith("]"):
        return ident
    return f"[{ident}]"


def _source_or_target(entry: dict) -> dict:
    """Return the entry's `source` block, falling back to `target` when absent.

    Target-only entries are typically Snowflake-side helpers (e.g. UDF shims)
    that have no source-side counterpart but still need to appear in the
    dependency graph as first-class code units.
    """
    source = entry.get("source") or {}
    if source:
        return source
    return entry.get("target") or {}


def _canonical_name(entry: dict) -> str:
    """Build a bracketed ``[db].[schema].[name]`` identifier.

    We ignore ``source.canonicalName`` on purpose: some registry entries
    (especially ``isMissing`` ones like ``Dash.U.value``) store it unbracketed,
    which causes downstream deduplication against ``build_id_to_name_map`` to
    fail. Reconstructing from the parts guarantees the bracketed form used
    everywhere else in the pipeline.

    ETL units (``kind == "etl"``) have no ``source.database/schema/name``;
    their natural identifier is ``files.source.path`` (e.g. the ``.dtsx`` /
    ``.xml`` definition file).
    """
    if _is_etl(entry):
        path = (
            entry.get("files", {}).get("source", {}).get("path", "") or ""
        ).strip()
        return path or (entry.get("id") or "")
    source = _source_or_target(entry)
    parts = [
        _bracket(v)
        for v in (source.get("database", ""), source.get("schema", ""), source.get("name", ""))
        if v and v.strip() and v.strip("[]")
    ]
    return ".".join(parts) if parts else ""


def _aggregate_etl_dependencies(entry: dict) -> tuple[list[dict], list[dict]]:
    """Flatten ``parts[*].dependencies`` into a single (depends_on, required_by) pair.

    ETL registry entries carry empty top-level ``dependencies`` — the real
    dependency edges live one level down inside ``parts[*].dependencies``.
    Each part can reference different SQL objects (Execute SQL Tasks point at
    procedures and tables; Pipeline / Data Flow parts point at staging
    tables, etc.), so aggregating across all parts gives the correct
    code-unit-level view for the dependency graph and the report table.

    Deduplicate by dependency ``id``: a single staging table referenced by
    multiple Execute SQL Tasks must count as one edge, not N. Each merged
    dep keeps a stable ``relationTypes`` list (deduped, preserving order).
    """
    seen_deps: dict[str, dict] = {}
    seen_req: dict[str, dict] = {}
    for part in entry.get("parts") or []:
        if not isinstance(part, dict):
            continue
        deps = part.get("dependencies") or {}
        for dep in deps.get("dependsOn") or []:
            if not isinstance(dep, dict):
                continue
            dep_id = dep.get("id") or ""
            if not dep_id:
                continue
            existing = seen_deps.get(dep_id)
            if existing:
                rel_set = {*(existing.get("relationTypes") or [])}
                for r in dep.get("relationTypes") or []:
                    if r not in rel_set:
                        existing.setdefault("relationTypes", []).append(r)
                        rel_set.add(r)
                # If any part says missing, the aggregate is missing
                if dep.get("isMissing"):
                    existing["isMissing"] = True
            else:
                seen_deps[dep_id] = {
                    "id": dep_id,
                    "isMissing": bool(dep.get("isMissing")),
                    "relationTypes": list(dep.get("relationTypes") or []),
                }
        for req in deps.get("requiredBy") or []:
            if not isinstance(req, dict):
                continue
            rid = req.get("id") or ""
            if rid and rid not in seen_req:
                seen_req[rid] = dict(req)
    return list(seen_deps.values()), list(seen_req.values())


def _relation_type(dep: dict) -> str:
    types = dep.get("relationTypes") or []
    if not types:
        return ""
    if len(types) == 1:
        return types[0]
    return ", ".join(types)


def _build_object(
    entry: dict,
    id_map: dict[str, str],
) -> dict[str, Any]:
    source = _source_or_target(entry)
    is_etl = _is_etl(entry)

    if is_etl:
        # Edges live one level down for ETL; flatten and dedupe across parts
        # so the dependency table sees the staging tables / procedures the
        # SSIS / Informatica package actually reads from and writes to.
        depends_on, required_by = _aggregate_etl_dependencies(entry)
    else:
        deps = entry.get("dependencies", {}) or {}
        depends_on = deps.get("dependsOn", []) or []
        required_by = deps.get("requiredBy", []) or []

    files = entry.get("files", {}) or {}
    # Prefer the source-side path; fall back to converted path for target-only
    # entries (Snowflake UDF helpers and similar) that have no source file.
    file_name = (
        files.get("source", {}).get("path", "")
        or files.get("converted", {}).get("path", "")
        or ""
    )

    name = _canonical_name(entry)
    obj_id = name or (entry.get("id") or "")
    if is_etl:
        # First-class ETL row in the dependency table; surface the platform
        # (SSIS, Informatica, ...) as the subtype so users can distinguish
        # the engine without leaving the table.
        category = "ETL"
        subtype = (source.get("platform") or "").upper()
    else:
        category = (source.get("objectType") or "").upper() or "UNKNOWN"
        subtype = ""

    missing_dependencies: list[dict[str, Any]] = []
    for dep in depends_on:
        if not isinstance(dep, dict) or not dep.get("isMissing"):
            continue
        dep_id = dep.get("id") or ""
        missing_dependencies.append(
            {
                "referenced": id_map.get(dep_id, dep_id),
                "relationType": _relation_type(dep),
                "line": "0",
                "file": file_name,
            }
        )

    direct_dependencies = sum(
        1
        for d in depends_on
        if isinstance(d, dict)
    )
    direct_dependents = sum(
        1
        for r in required_by
        if r
    )

    return {
        "id": obj_id,
        "name": name,
        "category": category,
        "subtype": subtype,
        "technology": "",
        "fileName": file_name,
        "conversionStatus": _map_conversion_status(entry),
        "partitionNumber": MOCK_PARTITION_NUMBER,
        "partitionType": MOCK_PARTITION_TYPE,
        "isRoot": len(required_by) == 0,
        "isLeaf": len(depends_on) == 0,
        "isWaveSeed": False,
        "totalDirectDependencies": direct_dependencies,
        "totalDirectDependents": direct_dependents,
        "totalDependencies": direct_dependencies,
        "totalDependents": direct_dependents,
        "missingCount": len(missing_dependencies),
        "missingDependencies": missing_dependencies,
    }


def synthesize_waves_json(registry_dir: Path | str) -> dict[str, Any]:
    """Build a waves-JSON-compatible dict from the registry on disk.

    Emits the camelCase / `schemaVersion: 1` shape consumed by
    `WavesJsonAdapter`. Includes every in-scope registry entry
    (including ``isMissing`` rows and ``objectType: other`` entries).
    Skips ``objectType: schema`` only.
    """
    registry_dir = Path(registry_dir)
    entries = load_registry_entries(registry_dir)
    id_map = build_id_to_name_map(entries)

    valid_entries = [
        e
        for e in entries
        if e.get("inScope")
        and (_source_or_target(e).get("objectType") or "").lower() not in SKIP_OBJECT_TYPES
        and not _is_udf_helper(e)
        and not _is_non_toplevel_other(e)
    ]

    valid_entries.sort(
        key=lambda e: (
            e.get("planning", {}).get("topologicalRank", 0),
            _canonical_name(e),
        )
    )

    objects = [_build_object(e, id_map) for e in valid_entries]

    deployment_order = [o["id"] for o in objects]

    total_nodes = len(objects)
    total_edges = sum(o["totalDirectDependencies"] for o in objects)
    root_nodes = sum(1 for o in objects if o["isRoot"])
    leaf_nodes = sum(1 for o in objects if o["isLeaf"])
    max_dependencies = max((o["totalDirectDependencies"] for o in objects), default=0)
    max_dependents = max((o["totalDirectDependents"] for o in objects), default=0)
    avg_deps = (total_edges / total_nodes) if total_nodes else 0.0

    return {
        "schemaVersion": 1,
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ).replace("+00:00", "Z"),
            "tool": {
                "name": "waves_from_registry",
                "version": "0.3.0",
                "subcommand": "synthesize",
            },
            "sourceMode": "registry-mock",
            "missingDependenciesSource": "registry",
            "warnings": [
                "Partition assignments are mocked (all objects placed in wave 1). "
                "Replace with output of `scai assessment waves` when available."
            ],
        },
        "graphSummary": {
            "nodes": total_nodes,
            "edges": total_edges,
            "averageDependenciesPerNode": round(avg_deps, 2),
            "connectivity": {
                "weaklyConnectedCodeUnits": 0,
                "stronglyConnectedCodeUnits": total_nodes,
                "cyclicDependenciesCount": 0,
            },
            "statistics": {
                "codeUnitsWithoutDependencies": root_nodes,
                "codeUnitsWithoutDependents": leaf_nodes,
                "maxDependenciesPerCodeUnit": max_dependencies,
                "maxDependentsPerCodeUnit": max_dependents,
            },
        },
        "cycles": [],
        "objects": objects,
        "partitions": [
            {
                "partitionNumber": MOCK_PARTITION_NUMBER,
                "partitionType": MOCK_PARTITION_TYPE,
                "size": total_nodes,
                "deploymentOrder": deployment_order,
            }
        ],
        "missingCodeUnits": {
            "totalCount": 0,
            "totalReferences": 0,
            "relationTypes": {},
            "codeUnits": [],
        },
    }


def write_synthesized_waves_json(
    registry_dir: Path | str, out_path: Path | str
) -> Path:
    """Synthesize a waves JSON and write it to disk. Returns the path."""
    data = synthesize_waves_json(registry_dir)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    return out_path


# ---------------------------------------------------------------------------
# Overlay: merge the real `scai assessment waves` output onto the synthesizer
# ---------------------------------------------------------------------------
#
# Expects the real waves JSON to follow `schemaVersion: 1` (integer), the
# current contract emitted by `scai assessment waves`. All keys are
# camelCase: `isWaveSeed`, `missingCodeUnits`, `weaklyConnectedCodeUnits`,
# `statistics.maxDependenciesPerCodeUnit`, `totalDirectDependencies`, etc.
#
# The overlay translates these names to the snake_case internal names used
# by WavesJsonAdapter and the HTML generator (which predate this schema),
# so callers and downstream code stay unchanged.


def overlay_real_waves_json(
    synth: dict[str, Any],
    real_waves_path: Path | str,
    registry_dir: Path | str,
) -> dict[str, Any]:
    """Overlay the C# waves-analysis output onto a registry-synthesized dict.

    - ``objects[*]`` algorithmic fields are copied from the real waves JSON,
      matched on the registry's UUID.
    - ``partitions[]``, ``cycles[]``, and ``missingCodeUnits`` are taken from
      the real JSON. UUIDs in ``deploymentOrder`` / ``cycles[].nodes`` are
      translated to canonical names via ``build_id_to_name_map``. UUIDs that
      don't correspond to a synthesized object are dropped.
    - ``graphSummary.connectivity`` and ``graphSummary.statistics`` are taken
      from the real JSON; ``nodes`` / ``edges`` stay synthesizer-derived so
      they reflect our filtered object set.
    - ``metadata.tool`` and ``metadata.parameters`` are preserved for
      traceability under ``metadata.waves_*`` keys.

    Returns the mutated ``synth`` dict (same instance).
    """
    real_waves_path = Path(real_waves_path)
    with real_waves_path.open(encoding="utf-8") as fh:
        real = json.load(fh)

    # Accept only the current producer contract: schemaVersion == 1 (camelCase).
    schema_version = real.get("schemaVersion")
    if schema_version != 1:
        raise ValueError(
            f"Unsupported waves JSON schemaVersion={schema_version!r} at "
            f"{real_waves_path}. Expected 1 (camelCase schema). Re-run "
            f"`scai assessment waves` to regenerate with the current schema."
        )

    entries = load_registry_entries(registry_dir)
    uuid_to_name = build_id_to_name_map(entries)

    # Only UUIDs whose canonical name is present as a synthesized object are
    # allowed through — this drops UDF helpers and any future filtered types.
    synth_names = {o["name"] for o in synth.get("objects", [])}

    def _resolve(uuid: str) -> str | None:
        name = uuid_to_name.get(uuid)
        if name and name in synth_names:
            return name
        return None

    # --- overlay per-object algorithmic fields ---
    real_by_uuid = {o.get("id"): o for o in real.get("objects", []) if o.get("id")}
    name_to_uuid = {v: k for k, v in uuid_to_name.items()}

    overlaid = 0
    for obj in synth.get("objects", []):
        uuid = name_to_uuid.get(obj.get("name"))
        if not uuid:
            continue
        real_obj = real_by_uuid.get(uuid)
        if not real_obj:
            continue
        # Copy algorithmic fields through in camelCase (adapter reads them verbatim)
        for key in (
            "partitionNumber",
            "partitionType",
            "isWaveSeed",
            "rank",
            "totalDependencies",
            "totalDependents",
            "totalDirectDependencies",
            "totalDirectDependents",
        ):
            if key in real_obj:
                obj[key] = real_obj[key]
        overlaid += 1

    # --- partitions: translate UUIDs, drop unresolved entries ---
    new_partitions = []
    for p in real.get("partitions", []):
        translated = []
        for uuid in p.get("deploymentOrder", []):
            name = _resolve(uuid)
            if name:
                translated.append(name)
        if translated:
            new_partitions.append({
                "partitionNumber": p.get("partitionNumber"),
                "partitionType": p.get("partitionType", ""),
                "size": len(translated),
                "deploymentOrder": translated,
            })
    if new_partitions:
        synth["partitions"] = new_partitions

    # --- cycles: translate and drop unresolved ---
    new_cycles = []
    for c in real.get("cycles", []):
        nodes = [n for n in (_resolve(u) for u in c.get("nodes", [])) if n]
        if nodes:
            new_cycles.append({
                "sccId": c.get("sccId"),
                "size": c.get("size", len(nodes)),
                "nodes": nodes,
            })
    synth["cycles"] = new_cycles

    # --- graphSummary: copy connectivity/statistics verbatim (camelCase) ---
    real_gs = real.get("graphSummary", {}) or {}
    gs = synth.setdefault("graphSummary", {})
    if real_gs.get("connectivity"):
        gs["connectivity"] = dict(real_gs["connectivity"])
    if real_gs.get("statistics"):
        gs["statistics"] = dict(real_gs["statistics"])

    # --- missingCodeUnits: copy through unchanged ---
    mcu = real.get("missingCodeUnits")
    if isinstance(mcu, dict):
        synth["missingCodeUnits"] = {
            "totalCount": int(mcu.get("totalCount", 0) or 0),
            "totalReferences": int(mcu.get("totalReferences", 0) or 0),
            "relationTypes": dict(mcu.get("relationTypes", {}) or {}),
            "codeUnits": [
                {
                    "id": cu.get("id", ""),
                    "canonicalName": cu.get("canonicalName", cu.get("id", "")),
                    "requiredByCount": int(cu.get("requiredByCount", 0) or 0),
                    "relationTypes": dict(cu.get("relationTypes", {}) or {}),
                }
                for cu in (mcu.get("codeUnits") or [])
                if isinstance(cu, dict)
            ],
        }

    # --- metadata traceability (camelCase) ---
    real_meta = real.get("metadata", {}) or {}
    meta = synth.setdefault("metadata", {})
    if "tool" in real_meta:
        meta["wavesTool"] = real_meta["tool"]
    if "parameters" in real_meta:
        meta["wavesParameters"] = real_meta["parameters"]
    if "generatedAt" in real_meta:
        meta["wavesGeneratedAt"] = real_meta["generatedAt"]
    meta["sourceMode"] = "registry+waves"
    meta["warnings"] = [
        f"Merged {overlaid}/{len(synth.get('objects', []))} objects with real waves JSON ({real_waves_path.name})."
    ]

    return synth


def write_merged_waves_json(
    registry_dir: Path | str,
    real_waves_path: Path | str,
    out_path: Path | str,
) -> Path:
    """Synthesize from registry, overlay real waves JSON, write the result."""
    data = synthesize_waves_json(registry_dir)
    overlay_real_waves_json(data, real_waves_path, registry_dir)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    return out_path
