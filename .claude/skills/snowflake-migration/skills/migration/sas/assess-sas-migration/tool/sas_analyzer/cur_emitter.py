"""Populate the Code Unit Registry (CUR) from SAS source and converted SQL.

Skill-side, JSON-only bridge: writes one ``<id>.json`` per converted object into
``<project_root>/registry/`` so the existing ``scai test`` harness can seed and
validate SAS conversions. Does NOT register a SnowConvert dialect or touch the
.NET CodeUnitRegistry engine. See ``sas/references/cur-schema.md`` for the
contract and ``sas/INTEGRATION.md`` for the boundary.

Granularity is one unit per converted object (one per SAS file in 1:1 mode).
Blocks (from ``parser.py``) classify objectType and derive the signature;
``dependency.py`` supplies the file-level dependency edges.

Stdlib-only and deterministic: unit ids are UUIDv5 of ``source.canonicalName``,
so re-runs are idempotent and the converted-attach pass re-finds the same unit.
"""

import hashlib
import json
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .parser import SASParser, SASScript, BlockType
from .dependency import DependencyTracker
from .constants import iter_countable_blocks, is_boilerplate_macro

# Stable namespace for deterministic unit ids (do not change — ids would churn).
_CUR_NAMESPACE = uuid.UUID("b6d7e1a2-9c34-5f60-8a71-2c3d4e5f6a7b")

_SOURCE_SCHEMA = "SAS"
_SOURCE_PLATFORM = "sas"
_SOURCE_FORMAT = "sas"
_TARGET_FORMAT = "snowflakeSQL"
_CONVERTER_VERSION = "sas-skill"
_SCHEMA_VERSION = 1

# tier (conversion_state files.*.tier) -> provisional objectType.
_TIER_OBJECT_TYPE = {
    "2-SP": "procedure",
    "1-SQL": "table",
}
_SKIP_TIERS = frozenset({"3-PYSPARK"})

_CREATE_OBJECT_RE = re.compile(
    r"(?is)\bCREATE\s+(?:OR\s+REPLACE\s+)?(PROCEDURE|FUNCTION|TABLE|VIEW)\b"
)
_MACRO_HEADER_RE = re.compile(r"(?is)%MACRO\s+(\w+)\s*\(([^)]*)\)")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def canonical_name(name: str) -> str:
    """``SAS.<NAME>`` — the source-side identity used to derive the unit id."""
    return f"{_SOURCE_SCHEMA}.{name.upper()}"


def unit_id(name: str) -> str:
    """Deterministic UUIDv5 for a unit, keyed on its canonical name."""
    return str(uuid.uuid5(_CUR_NAMESPACE, canonical_name(name)))


def object_type_from_sql(sql_text: str) -> Optional[str]:
    """Authoritative objectType from converted SQL, or None if undetermined."""
    match = _CREATE_OBJECT_RE.search(sql_text)
    return match.group(1).lower() if match else None


def _object_type_from_blocks(script: SASScript) -> str:
    """Heuristic objectType when neither converted SQL nor a tier is known.

    A file with executable macro logic or control flow converts to a stored
    procedure; a file that only builds tables is a table.
    """
    for block in iter_countable_blocks(script):
        if block.block_type == BlockType.MACRO_DEF and not is_boilerplate_macro(block):
            return "procedure"
        if block.block_type == BlockType.DATA_STEP:
            body = block.content.lower()
            if "%do" in body or block.metadata.get("has_first_last") or block.metadata.get("has_retain"):
                return "procedure"
    return "table"


def macro_arguments(content: str) -> List[Dict]:
    """Extract ``%MACRO name(p1, p2=default)`` params as CUR signature args."""
    match = _MACRO_HEADER_RE.search(content)
    if not match:
        return []
    args: List[Dict] = []
    for raw in match.group(2).split(","):
        param = raw.split("=", 1)[0].strip()
        if not param:
            continue
        args.append(
            {
                "name": param,
                "type": "VARCHAR",
                "targetName": param,
                "targetType": "VARCHAR",
                "direction": "in",
                "required": "=" not in raw,
                "isCursor": False,
            }
        )
    return args


def _split_target_schema(target_schema: Optional[str]):
    """``DB.SCHEMA`` -> (db, schema); tolerate a bare schema or None."""
    if not target_schema:
        return None, None
    parts = target_schema.split(".")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, parts[0]


class CurEmitter:
    """Writes and updates CUR entries under a project root (== SAS output_dir)."""

    def __init__(self, project_root: Path):
        self.root = Path(project_root)
        self.registry_dir = self.root / "registry"
        self.source_dir = self.root / "source"
        self.snowflake_dir = self.root / "snowflake"

    # -- filesystem ---------------------------------------------------------

    def scaffold(self) -> None:
        for sub in (".scai", "registry", "source", "snowflake", "artifacts"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    def _entry_path(self, uid: str) -> Path:
        return self.registry_dir / f"{uid}.json"

    def _read_entry(self, uid: str) -> Optional[Dict]:
        path = self._entry_path(uid)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def _write_entry(self, entry: Dict) -> None:
        path = self._entry_path(entry["id"])
        path.write_text(json.dumps(entry, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # -- source registration (Skill A) --------------------------------------

    def register_sources(
        self,
        sas_files: List[Path],
        source_root: Optional[Path] = None,
        target_schema: Optional[str] = None,
    ) -> List[Dict]:
        """Parse ``.sas`` files, build file-level units, write source-side JSON.

        Returns the list of written entries. Deterministic: identical inputs
        produce identical files (idempotent re-runs).
        """
        self.scaffold()
        parser = SASParser()
        tracker = DependencyTracker()

        scripts: Dict[str, SASScript] = {}
        contents: Dict[str, str] = {}
        analyses: Dict[str, Dict] = {}
        file_by_name: Dict[str, Path] = {}
        for sas_file in sorted(sas_files):
            content = sas_file.read_text(encoding="utf-8", errors="replace")
            script = parser.parse(content, filename=sas_file.name)
            name = sas_file.stem
            scripts[name] = script
            contents[name] = content
            analyses[sas_file.name] = tracker.analyze_file(script)
            file_by_name[name] = sas_file
            parser = SASParser()  # reset per-file libname/macro-var state

        edges = tracker.build_cross_file_graph(analyses)["edges"]
        depends_on, required_by = self._edges_to_deps(edges, file_by_name)
        ranks = self._topological_ranks(file_by_name.keys(), depends_on)

        db, schema = _split_target_schema(target_schema)
        entries: List[Dict] = []
        for name, script in scripts.items():
            src_file = file_by_name[name]
            rel = self._copy_into(src_file, self.source_dir, source_root)
            obj_type = _object_type_from_blocks(script)
            entry = self._build_entry(
                name=name,
                obj_type=obj_type,
                source_path=f"source/{rel}",
                source_checksum=_md5(src_file),
                db=db,
                schema=schema,
                signature_args=macro_arguments(contents[name]),
                depends_on=depends_on.get(name, []),
                required_by=required_by.get(name, []),
                topological_rank=ranks.get(name, 0),
            )
            self._write_entry(entry)
            entries.append(entry)
        return entries

    # -- converted attach (Skill B) -----------------------------------------

    def attach_converted_from_state(self, conversion_state: Dict) -> List[Dict]:
        """Attach converted ``.sql`` + objectType from a ``conversion_state.json`` dict.

        Only files whose ``status == 'complete'`` and whose tier is a SQL object
        are attached; ``3-PYSPARK`` units are left source-only (not SQL-testable).
        Skips (without error) any file that has no registered source unit yet.
        """
        db, schema = _split_target_schema(
            conversion_state.get("metadata", {}).get("target_schema")
        )
        updated: List[Dict] = []
        for filename, info in sorted(conversion_state.get("files", {}).items()):
            if info.get("status") != "complete":
                continue
            tier = info.get("tier")
            if tier in _SKIP_TIERS:
                continue
            name = Path(filename).stem
            entry = self._read_entry(unit_id(name))
            if entry is None:
                continue
            output_file = info.get("output_file")
            if not output_file:
                continue
            converted_src = self._resolve_output_file(output_file)
            if converted_src is None:
                continue
            rel = self._copy_into(converted_src, self.snowflake_dir, converted_src.parent)
            self._apply_converted(entry, rel, _md5(converted_src), tier, db, schema)
            self._apply_state_dependencies(entry, info.get("dependencies", {}))
            self._write_entry(entry)
            updated.append(entry)
        return updated

    def _apply_converted(self, entry, rel, checksum, tier, db, schema) -> None:
        converted_sql = (self.snowflake_dir / rel).read_text(encoding="utf-8", errors="replace")
        obj_type = object_type_from_sql(converted_sql) or _TIER_OBJECT_TYPE.get(tier, "table")
        entry["source"]["objectType"] = obj_type
        entry["target"]["objectType"] = obj_type
        entry["files"]["converted"] = {"path": f"snowflake/{rel}", "checksum": checksum}
        if db is not None:
            entry["target"]["database"] = db
        if schema is not None:
            entry["target"]["schema"] = schema
        entry["target"]["canonicalName"] = ".".join(
            p for p in (entry["target"].get("database"), entry["target"].get("schema"), entry["target"]["name"]) if p
        )
        entry["files"]["artifacts"] = {
            "path": f"artifacts/{entry['target'].get('database', 'DB')}/"
            f"{entry['target'].get('schema', 'SCHEMA')}/{obj_type}/{entry['source']['name'].lower()}"
        }
        entry["codeStatus"]["conversion"] = {
            "status": "completed",
            "converterVersion": _CONVERTER_VERSION,
            "updatedAt": _now_iso(),
        }
        entry["updatedAt"] = _now_iso()

    def _apply_state_dependencies(self, entry, deps: Dict) -> None:
        """Merge creates/reads from conversion_state into dependency edges.

        Only used to fill edges that source registration could not resolve (e.g.
        when Skill B runs without a prior full-corpus source pass). Existing
        edges are preserved.
        """
        # conversion_state dependencies are dataset names, not unit ids; without
        # the full corpus we cannot resolve them to ids here, so this is a no-op
        # placeholder that keeps the structure stable. Cross-file edges are set
        # authoritatively by register_sources.
        entry["dependencies"].setdefault("dependsOn", [])
        entry["dependencies"].setdefault("requiredBy", [])
        entry["dependencies"].setdefault("hasTransitiveMissingDependencies", False)

    # -- helpers ------------------------------------------------------------

    def _build_entry(
        self, name, obj_type, source_path, source_checksum, db, schema,
        signature_args, depends_on, required_by, topological_rank,
    ) -> Dict:
        target_name = name
        target_canonical = ".".join(p for p in (db, schema, target_name) if p) or target_name
        target: Dict = {
            "canonicalName": target_canonical,
            "name": target_name,
            "objectType": obj_type,
            "format": _TARGET_FORMAT,
        }
        if db is not None:
            target["database"] = db
        if schema is not None:
            target["schema"] = schema
        now = _now_iso()
        return {
            "id": unit_id(name),
            "schemaVersion": _SCHEMA_VERSION,
            "kind": "databaseObject",
            "inScope": True,
            "isMissing": False,
            "source": {
                "canonicalName": canonical_name(name),
                "name": name,
                "objectType": obj_type,
                "schema": _SOURCE_SCHEMA,
                "platform": _SOURCE_PLATFORM,
                "format": _SOURCE_FORMAT,
            },
            "target": target,
            "files": {
                "source": {"path": source_path, "checksum": source_checksum},
                "artifacts": {"path": f"artifacts/{db or 'DB'}/{schema or 'SCHEMA'}/{obj_type}/{name.lower()}"},
            },
            "dependencies": {
                "dependsOn": depends_on,
                "requiredBy": required_by,
                "hasTransitiveMissingDependencies": False,
            },
            "codeStatus": {
                "registration": {"status": "completed", "sourceId": "", "updatedAt": now},
                "assessment": {"status": "completed"},
            },
            "signature": {"parameters": {"arguments": signature_args}},
            "extensions": {},
            "planning": {"topologicalRank": topological_rank},
            "updatedAt": now,
        }

    @staticmethod
    def _edges_to_deps(edges, file_by_name):
        """edge {from: creator_file, to: reader_file, via: dataset} -> id edges.

        Keyed by file stem. ``from`` values are ``.sas`` filenames; map to stems.
        """
        name_by_filename = {f.name: stem for stem, f in file_by_name.items()}
        depends_on: Dict[str, List[Dict]] = {}
        required_by: Dict[str, List[str]] = {}
        for edge in edges:
            creator = name_by_filename.get(edge["from"])
            reader = name_by_filename.get(edge["to"])
            if creator is None or reader is None or creator == reader:
                continue
            depends_on.setdefault(reader, []).append(
                {"id": unit_id(creator), "isMissing": False, "relationTypes": [f"READS {edge['via']}"]}
            )
            required_by.setdefault(creator, []).append(unit_id(reader))
        return depends_on, required_by

    @staticmethod
    def _topological_ranks(names, depends_on):
        """Longest-path rank from roots; cycle-safe (returns 0 on cycle)."""
        dep_names: Dict[str, List[str]] = {}
        id_to_name = {unit_id(n): n for n in names}
        for name in names:
            dep_names[name] = [
                id_to_name[d["id"]] for d in depends_on.get(name, []) if d["id"] in id_to_name
            ]
        ranks: Dict[str, int] = {}

        def rank_of(node, stack):
            if node in ranks:
                return ranks[node]
            if node in stack:
                return 0
            stack.add(node)
            deps = dep_names.get(node, [])
            value = 0 if not deps else 1 + max(rank_of(d, stack) for d in deps)
            stack.discard(node)
            ranks[node] = value
            return value

        for name in names:
            rank_of(name, set())
        return ranks

    def _copy_into(self, src: Path, dest_dir: Path, base: Optional[Path]) -> str:
        """Copy ``src`` under ``dest_dir`` preserving its path relative to ``base``.

        Returns the path relative to ``dest_dir`` (used to build the CUR entry's
        root-relative ``files.*.path``). Idempotent.
        """
        src = Path(src)
        if base is not None:
            try:
                rel = src.relative_to(base)
            except ValueError:
                rel = Path(src.name)
        else:
            rel = Path(src.name)
        target = dest_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.resolve() != src.resolve():
            shutil.copyfile(src, target)
        return str(rel)

    def _resolve_output_file(self, output_file: str) -> Optional[Path]:
        """Locate a conversion_state ``output_file`` relative to the project root."""
        candidate = Path(output_file)
        if candidate.is_absolute() and candidate.exists():
            return candidate
        for base in (self.root, self.snowflake_dir):
            resolved = base / output_file
            if resolved.exists():
                return resolved
        # Fall back to a basename search under the project root.
        matches = list(self.root.rglob(Path(output_file).name))
        return matches[0] if matches else None
