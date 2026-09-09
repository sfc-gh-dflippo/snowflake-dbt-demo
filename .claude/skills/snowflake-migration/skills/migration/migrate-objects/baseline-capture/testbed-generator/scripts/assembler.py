"""Assemble LLM enrichment prompt fragments into one EnrichmentEnvelope.

Each prompt emits a *partial* envelope keyed by its destination array; assembly is a per-array
deep-merge, never a transform. column_enrichments collapses by (table, column); every other array
is independent. flag_for_llm must be resolved Skill-side before it reaches here (design §5.2).
"""
from __future__ import annotations

import json
from pathlib import Path

STRUCTURAL_ARRAYS = ["fk_chains", "correlated_groups", "temporal_alignment", "anti_join_tables"]
VALUE_ARRAYS = ["column_enrichments", "branch_values", "predicate_fills"]
# Arrays merged as independent lists (concat + byte-identical dedupe), NOT collapsed by (table, column).
# branch_values joins the structural arrays here: two branch arms on one column carrying different enums
# must reach the backend as separate entries so its Decision-5 conflict detector can reject them —
# pre-unioning would launder that contradiction. predicate_fills joins for the same reason, but its identity
# is fill_id rather than (table, column): two fills keyed to DIFFERENT branches on one column are legal, and
# the backend adjudicates them on (branch_id, table, column). Only column_enrichments collapses (to fuse the
# complementary enum / must_include / null_fraction_override fields the per-type prompt fragments contribute).
_INDEPENDENT_ARRAYS = ["branch_values", "predicate_fills", *STRUCTURAL_ARRAYS]

# Which structural array a mine `by_kind` gap maps to (SKILL.md §Enrich mapping). enum_domain/check are value-only.
_KIND_TO_STRUCTURAL = {"fk": "fk_chains", "join_edge": "fk_chains", "branch_predicate": "correlated_groups"}


class AssemblyError(Exception):
    def __init__(self, prompt_type: str, message: str):
        super().__init__(message)
        self.prompt_type = prompt_type
        self.message = message


def load_fragments(fragments_dir: str) -> list[dict]:
    root = Path(fragments_dir)
    if not root.is_dir():
        return []
    fragments: list[dict] = []
    for p in sorted(root.glob("*.json")):
        try:
            frag = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            # A malformed fragment is a re-promptable reject, not a station crash: name the offending
            # fragment (via prompt_type) so run_enrich emits stop_kind "reject" and the agent knows
            # which prompt to re-run — mirroring assemble()'s flag_for_llm handling.
            raise AssemblyError(p.stem, f"fragment '{p.name}' is not valid JSON: {e}") from e
        except (OSError, UnicodeDecodeError) as e:
            # Unreadable (removed between glob and read, permissions, or a fragment written mid-
            # codepoint): same reject class, not a traceback out of the station — but named honestly
            # as an I/O failure, not bad JSON. UnicodeDecodeError is a ValueError, so it escapes
            # both arms above unless named here; the explicit utf-8 read is what can raise it,
            # instead of the locale default silently decoding a fragment to mojibake.
            raise AssemblyError(p.stem, f"fragment '{p.name}' could not be read: {e}") from e
        if not isinstance(frag, dict):
            # Valid JSON but not an object (a bare array/scalar) can't be merged; reject it here so
            # assemble() and _merge_column_entry can trust every fragment is an object.
            raise AssemblyError(p.stem, f"fragment '{p.name}' is not a JSON object")
        fragments.append(frag)
    return fragments


def assemble(fragments: list[dict]) -> dict:
    for frag in fragments:
        if "flag_for_llm" in frag:
            # The C# parser rejects a root flag_for_llm anyway; catching it here saves a subprocess and
            # names the offending prompt so the agent re-prompts the right fragment.
            raise AssemblyError("flag_for_llm",
                                "'flag_for_llm' leaked into a fragment; resolve it into one of the 10 supported types.")

    columns: dict[tuple[str, str], dict] = {}
    independent: dict[str, list] = {name: [] for name in _INDEPENDENT_ARRAYS}
    seen: dict[str, set] = {name: set() for name in _INDEPENDENT_ARRAYS}

    for frag in fragments:
        for entry in frag.get("column_enrichments", []) or []:
            _merge_column_entry(columns, entry, "column_enrichments")
        # branch_values keeps the (table, column) identity guard, but is NOT collapsed: each arm is an
        # independent entry, deduped only when byte-identical (like the structural arrays).
        for entry in frag.get("branch_values", []) or []:
            _require_column_identity(entry, "branch_values")
            _append_unique(independent["branch_values"], seen["branch_values"], entry)
        # predicate_fills needs its OWN collection loop, not just membership in the list constants above:
        # assemble() reads exactly the sources enumerated here, VALUE_ARRAYS is consumed only by
        # structural_coverage_warnings, and _INDEPENDENT_ARRAYS merely chooses dedupe-vs-collapse for arrays
        # already collected. Registering the name without a loop silently drops every fragment — the live
        # proof being temporal_window_bindings, which appears in none of the three lists and never reaches
        # the backend today. Identity is fill_id, not (table, column), so _require_column_identity does not
        # apply (a non-coverable entry legitimately carries neither column nor value).
        for entry in frag.get("predicate_fills", []) or []:
            if not isinstance(entry, dict) or "fill_id" not in entry or "branch_id" not in entry:
                raise AssemblyError(
                    "predicate_fills",
                    f"predicate_fills entry is malformed (needs 'fill_id' and 'branch_id'): {entry!r}")
            _append_unique(independent["predicate_fills"], seen["predicate_fills"], entry)
        for name in STRUCTURAL_ARRAYS:
            for entry in frag.get(name, []) or []:
                _append_unique(independent[name], seen[name], entry)

    env: dict = {}
    col_list = [columns[k] for k in sorted(columns)]
    if col_list:
        env["column_enrichments"] = col_list
    for name in _INDEPENDENT_ARRAYS:
        if independent[name]:
            env[name] = _sorted_json(independent[name])
    return env


def _append_unique(bucket: list, seen: set, entry) -> None:
    # O(1) byte-identical dedupe: a signature set replaces the prior `entry not in bucket` linear
    # scan, so concatenating a large fk_chains / correlated_groups array is no longer O(n²).
    sig = json.dumps(entry, sort_keys=True)
    if sig not in seen:
        seen.add(sig)
        bucket.append(entry)


def _require_column_identity(entry: dict, array: str) -> None:
    # A valid-JSON fragment can still carry a malformed entry: a non-object, or one missing the
    # (table, column) identity. Reject it as an AssemblyError named by its array so run_enrich
    # degrades to a re-promptable reject instead of a KeyError/AttributeError out of the station.
    if not isinstance(entry, dict) or "table" not in entry or "column" not in entry:
        raise AssemblyError(array, f"{array} entry is malformed (needs 'table' and 'column'): {entry!r}")


def _merge_column_entry(acc: dict, entry: dict, array: str) -> None:
    _require_column_identity(entry, array)
    key = (entry["table"], entry["column"])
    cur = acc.get(key)
    if cur is None:
        acc[key] = {"table": entry["table"], "column": entry["column"]}
        cur = acc[key]
    for list_field in ("inferred_enum", "must_include"):
        if entry.get(list_field):
            merged = set(cur.get(list_field, [])) | set(entry[list_field])
            cur[list_field] = sorted(merged)
    if entry.get("null_fraction_override") is not None:
        cur["null_fraction_override"] = entry["null_fraction_override"]
    if entry.get("source_evidence") and "source_evidence" not in cur:
        cur["source_evidence"] = entry["source_evidence"]


def _sorted_json(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda d: json.dumps(d, sort_keys=True))


def value_conflict_warnings(fragments: list[dict]) -> list[str]:
    # column_enrichments collapses by (table, column) with last-writer-wins for null_fraction_override,
    # so two fragments disagreeing on the value silently pick one. The backend hard-rejects that split
    # (EnrichmentConflictDetector `nfo|` key), but it never sees the conflict once the assembler has
    # collapsed the entries — surface the disagreement here (mirrors structural_coverage_warnings).
    by_col: dict[tuple, set] = {}
    for frag in fragments:
        for entry in frag.get("column_enrichments", []) or []:
            if not isinstance(entry, dict) or entry.get("null_fraction_override") is None:
                continue
            by_col.setdefault((entry.get("table"), entry.get("column")), set()).add(entry["null_fraction_override"])
    warnings: list[str] = []
    for (table, column), values in sorted(by_col.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        if len(values) > 1:
            shown = ", ".join(str(v) for v in sorted(values, key=str))
            warnings.append(
                f"conflicting null_fraction_override for {table}.{column}: {shown} "
                f"(assembler keeps the last; the backend rejects the disagreement)")
    return warnings


def structural_coverage_warnings(fragments: list[dict], unsolved_view: dict) -> list[str]:
    has_value = any(any(frag.get(a) for a in VALUE_ARRAYS) for frag in fragments)
    if not has_value:
        return []
    present = {name for frag in fragments for name in STRUCTURAL_ARRAYS if frag.get(name)}
    warnings: list[str] = []
    by_kind = unsolved_view.get("by_kind", {})
    for kind, arr in _KIND_TO_STRUCTURAL.items():
        if by_kind.get(kind, {}).get("count", 0) > 0 and arr not in present:
            warnings.append(
                f"value fragments present but no '{arr}' fragment for unsolved '{kind}' gaps "
                f"(structural pass may be incomplete)")
    return warnings
