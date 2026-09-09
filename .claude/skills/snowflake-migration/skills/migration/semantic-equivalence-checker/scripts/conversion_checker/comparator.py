"""Stage 1 structural comparison: INFA workflow vs DBT model."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import sqlglot
from sqlglot import exp as _exp

from .dbt_parser import parse_dbt_model
from .models import (
    CheckResult,
    ColumnCheck,
    DbtModel,
    HookCheck,
    InfaWorkflow,
    PipelineCoverage,
    SiblingContext,
    SiblingModel,
    SourceCheck,
    StrategyCheck,
    TargetCheck,
    TransformCheck,
    UnresolvedSection,
)
from .transform_checker import (
    compare_column_expressions,
    compare_filters,
    compare_hook_statements,
    compare_joins,
    extract_column_expressions,
)
from .sql_tables import extract_tables_from_sql


def _normalize_name(name: str) -> str:
    """Strip DB/schema prefixes and uppercase."""
    return name.split(".")[-1].upper().strip()


def _find_line(file_path: str, pattern: str, case_insensitive: bool = True) -> int:
    """Find the first line number matching pattern in a file. Returns 0 if not found."""
    try:
        flags = re.IGNORECASE if case_insensitive else 0
        with open(file_path, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line, flags):
                    return i
    except (OSError, UnicodeDecodeError):
        pass
    return 0


def _find_line_range(file_path: str, start_pattern: str, end_pattern: str) -> str:
    """Find line range (start-end) for a block. Returns 'start-end' or 'start'."""
    start = _find_line(file_path, start_pattern)
    if not start:
        return "0"
    end = 0
    try:
        with open(file_path, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                if i > start and re.search(end_pattern, line, re.IGNORECASE):
                    end = i
                    break
    except (OSError, UnicodeDecodeError):
        pass
    return f"{start}-{end}" if end else str(start)


def _xml_ev(xml_path: str, pattern: str, desc: str) -> dict:
    """Evidence from XML file."""
    return {"xml_line": _find_line(xml_path, pattern), "text": desc}


def _xml_ev_range(xml_path: str, start_pat: str, end_pat: str, desc: str) -> dict:
    """Evidence from XML file with line range."""
    return {"xml_line": _find_line_range(xml_path, start_pat, end_pat), "text": desc}


def _dbt_ev(dbt_path: str, pattern: str, desc: str) -> dict:
    """Evidence from DBT file."""
    return {"dbt_line": _find_line(dbt_path, pattern), "text": desc}


def _dbt_ev_range(dbt_path: str, start_pat: str, end_pat: str, desc: str) -> dict:
    """Evidence from DBT file with line range."""
    return {"dbt_line": _find_line_range(dbt_path, start_pat, end_pat), "text": desc}


def _check_sources(infa: InfaWorkflow, dbt: DbtModel) -> SourceCheck:
    """Compare source tables between INFA and DBT.

    When SQ Override is present, extracts sources from the SQL (the actual TD-side
    query) instead of SOURCE instances (which include Oracle EL artifacts).
    Falls back to SOURCE instances (minus self-read) when no SQ Override exists.
    """
    target_normalized = _normalize_name(infa.target_table)

    # Determine INFA sources: prefer SQ Override SQL (TD-side truth)
    if infa.sq_overrides:
        # Union sources from ALL pipelines
        infa_set: set[str] = set()
        for sq in infa.sq_overrides:
            sq_tables = extract_tables_from_sql(sq)
            infa_set.update(t[1] for t in sq_tables)
        infa_set.discard(target_normalized)
    elif infa.sq_override:
        sq_tables = extract_tables_from_sql(infa.sq_override)
        infa_set = {t[1] for t in sq_tables}
        infa_set.discard(target_normalized)
    else:
        # Fallback: use SOURCE instances minus self-read
        infa_set = {_normalize_name(s) for s in infa.source_tables}
        infa_set.discard(target_normalized)

    dbt_set = {_normalize_name(s) for s in dbt.source_tables}

    # Exclude tables that are INSERT targets in pre_hooks (they're intermediate staging)
    pre_hook_targets = set()
    for hook in (dbt.pre_hooks or []):
        clean = hook.replace("{{", "").replace("}}", "").replace("'", "")
        try:
            parsed = sqlglot.parse_one(clean, read="snowflake")
            table_node = parsed.find(_exp.Table)
            if table_node and isinstance(parsed, (_exp.Insert,)):
                pre_hook_targets.add(table_node.name.upper())
            elif table_node:
                # Check if it's an INSERT even if sqlglot classified differently
                if clean.strip().upper().startswith("INSERT"):
                    pre_hook_targets.add(table_node.name.upper())
        except Exception:
            # Regex fallback for unparseable hooks (Jinja remnants etc)
            m = re.search(r"(?i)INSERT\s+INTO\s+.+?\.(\w+)(?:\s|\(|$)", clean)
            if not m:
                m = re.search(r"(?i)INSERT\s+INTO\s+(\w+)", clean)
            if m:
                pre_hook_targets.add(m.group(1).upper())

    missing = sorted((infa_set - dbt_set) - pre_hook_targets)
    extra = sorted(dbt_set - infa_set)

    status = "PASS" if not missing and not extra else "FAIL"
    return SourceCheck(
        status=status,
        infa_sources=sorted(infa_set),
        dbt_sources=sorted(dbt_set),
        missing_in_dbt=missing,
        extra_in_dbt=extra,
    )


_OOD_INSERT_RE = re.compile(
    r"INSERT\s+INTO\s+(?:\{\{[^}]*\}\}\s*\.)?(\w+(?:\.\w+)*)",
    re.IGNORECASE,
)


def _extract_ood_insert_target(hooks: list[str]) -> str | None:
    """Extract INSERT INTO target from OOD post_hooks (ignores {{this}})."""
    for hook in hooks:
        m = _OOD_INSERT_RE.search(hook)
        if m and re.search(r"\{\{\s*this\s*\}\}", hook):
            # Take last dotted component as table name
            target = m.group(1).split(".")[-1]
            if target.upper() != "THIS":
                return target
    return None


def _check_target(infa: InfaWorkflow, dbt: DbtModel) -> TargetCheck:
    """Compare target table, detecting OOD TEMP→INSERT pattern."""
    infa_target = _normalize_name(infa.target_table)
    dbt_target = _normalize_name(dbt.target_table)

    match = infa_target == dbt_target
    # OOD pattern: dbt creates TEMP table, post_hook INSERT INTO <real_target>
    if not match and dbt.post_hooks:
        effective = _extract_ood_insert_target(dbt.post_hooks)
        if effective:
            dbt_target = _normalize_name(effective)
            match = infa_target == dbt_target

    status = "PASS" if match else "FAIL"
    return TargetCheck(
        status=status,
        infa_target=infa_target,
        dbt_target=dbt_target,
        match=match,
    )


def _check_strategy(infa: InfaWorkflow, dbt: DbtModel) -> StrategyCheck:
    """Compare load strategy."""
    infa_strat = infa.target_load_type.upper()

    # Map DBT config to comparable strategy
    if dbt.materialization == "incremental":
        dbt_strat = (dbt.incremental_strategy or "append").upper()
        # Normalize
        dbt_strat_map = {
            "DELETE+INSERT": "DELETE+INSERT",
            "INSERT_OVERWRITE": "DELETE+INSERT",
            "MERGE": "UPDATE",
            "APPEND": "INSERT",
        }
        dbt_strat = dbt_strat_map.get(dbt_strat, dbt_strat)
    elif dbt.materialization == "table":
        # materialized='table' = full rebuild (drop+create+insert)
        # Semantically equivalent to both INFA INSERT (full load) and DELETE+INSERT
        dbt_strat = "FULL_REBUILD"
    elif dbt.materialization == "view":
        dbt_strat = "VIEW"
    else:
        dbt_strat = dbt.materialization.upper()

    # FULL_REBUILD matches INSERT (full load) and DELETE+INSERT (truncate+load)
    if dbt_strat == "FULL_REBUILD":
        match = infa_strat in ("INSERT", "DELETE+INSERT")
    else:
        match = infa_strat == dbt_strat
    status = "PASS" if match else "FAIL"
    return StrategyCheck(
        status=status,
        infa_strategy=infa_strat,
        dbt_strategy=dbt_strat,
        match=match,
    )


def _check_hooks(infa_sql: list[str], dbt_sql: list[str], label: str) -> tuple[HookCheck, list[dict]]:
    """Compare pre/post hook SQL with content comparison.

    Returns (HookCheck, unresolved_sections) tuple.
    """
    # Both empty = equivalent
    if not infa_sql and not dbt_sql:
        return HookCheck(status="PASS", infa_sql=infa_sql, dbt_sql=dbt_sql, equivalent=True), []

    # Presence check — if INFA has hooks but DBT doesn't (or vice versa)
    if bool(infa_sql) != bool(dbt_sql):
        return HookCheck(status="FAIL", infa_sql=infa_sql, dbt_sql=dbt_sql, equivalent=False), []

    # Both have hooks — do content comparison
    equivalent, matched_pairs, unresolved = compare_hook_statements(infa_sql, dbt_sql)

    has_fail = any(p["status"] == "DIFFERENT" for p in matched_pairs)
    status = "FAIL" if has_fail else ("PASS" if equivalent else "PARTIAL")

    return HookCheck(status=status, infa_sql=infa_sql, dbt_sql=dbt_sql, equivalent=equivalent), unresolved


def _check_columns(infa: InfaWorkflow, dbt: DbtModel) -> ColumnCheck:
    """Compare column lists."""
    infa_cols = {c.upper() for c in infa.columns_written}
    dbt_cols = {c.upper() for c in dbt.columns_selected}

    # If we couldn't extract INFA columns, skip
    if not infa_cols:
        return ColumnCheck(status="SKIP", missing_in_dbt=[], extra_in_dbt=[])

    # Audit columns: INFA uses EDW_* prefix, DBT uses EDWSF_* prefix.
    # These are known equivalent pairs during conversion — exclude both sides.
    infa_audit_cols = {"EDW_CREATE_DTM", "EDW_CREATE_USER", "EDW_UPDATE_DTM", "EDW_UPDATE_USER",
                       "EDW_CREATE_DATETIME", "EDW_UPDATE_DATETIME"}
    dbt_audit_cols = {"EDWSF_CREATE_DTM", "EDWSF_CREATE_USER", "EDWSF_UPDATE_DTM",
                      "EDWSF_UPDATE_USER", "EDWSF_BATCH_ID", "EDWSF_SOURCE_DELETED_FLAG"}

    infa_cols_filtered = infa_cols - infa_audit_cols
    dbt_cols_filtered = dbt_cols - dbt_audit_cols

    missing = sorted(infa_cols_filtered - dbt_cols_filtered)
    extra = sorted(dbt_cols_filtered - infa_cols_filtered)

    status = "PASS" if not missing else "FAIL"
    return ColumnCheck(status=status, missing_in_dbt=missing, extra_in_dbt=extra)


def _check_pipelines(infa: InfaWorkflow) -> PipelineCoverage | None:
    """Extract pipeline variant information from multi-pipeline workflows."""
    overrides = infa.sq_overrides
    if len(overrides) <= 1:
        return None

    # Extract variant constants: look for string literals assigned AS column in each pipeline
    variants: list[str] = []
    for sq in overrides:
        matches = re.findall(r"'([^']+)'\s+AS\s+\w+", sq, re.IGNORECASE)
        for m in matches:
            if m.upper() not in ("GOODS", "REVENUE", "UNKNOWN") and m not in variants:
                variants.append(m)
                break  # one variant per pipeline

    return PipelineCoverage(count=len(overrides), variants=variants)


def _check_transforms(infa: InfaWorkflow, dbt: DbtModel) -> TransformCheck | None:
    """Stage 2: Compare transformation expressions column-by-column.

    Uses SQ Override SQL for INFA side, raw DBT SQL for DBT side.
    Returns None if SQ Override is not available (can't compare).
    """
    if not infa.sq_override:
        return None

    # Extract INFA column expressions from SQ Override
    infa_cols = extract_column_expressions(infa.sq_override)
    if not infa_cols:
        return TransformCheck(status="SKIP", evidence=[{"text": "Could not parse INFA SQ Override"}])

    # Extract DBT column expressions from raw SQL
    dbt_sql = dbt.raw_sql
    if not dbt_sql:
        return TransformCheck(status="SKIP", evidence=[{"text": "No DBT SQL available"}])

    # Strip Jinja before parsing as SQL
    from .dbt_parser import _strip_jinja
    dbt_sql = _strip_jinja(dbt_sql)
    # Remove the config placeholder (may follow a leading comment)
    dbt_sql = re.sub(r"'__JINJA__'\s*", "", dbt_sql, count=1).strip()

    dbt_cols = extract_column_expressions(dbt_sql, dialect="snowflake")
    if not dbt_cols:
        return TransformCheck(status="SKIP", evidence=[{"text": "Could not parse DBT SQL"}])

    return compare_column_expressions(infa_cols, dbt_cols)


# ──────────────────────────────────────────────────────────────
# Sibling context extraction
# ──────────────────────────────────────────────────────────────

def extract_sibling_context(
    dbt_path: str,
    sources_lookup: dict[str, dict[str, str]] | None = None,
    vars_lookup: dict[str, str] | None = None,
) -> SiblingContext | None:
    """Extract sibling models, upstream columns, and variables from the _wf directory.

    Parses all .sql files in the same directory as dbt_path (excluding the primary model)
    and returns structured metadata the LLM can use to resolve external references.
    """
    dbt_file = Path(dbt_path)
    if not dbt_file.exists():
        return None

    wf_dir = dbt_file.parent
    primary_name = dbt_file.stem

    # Parse all sibling models
    siblings: list[SiblingModel] = []
    sibling_models: dict[str, DbtModel] = {}

    for sql_file in sorted(wf_dir.glob("*.sql")):
        if sql_file.stem == primary_name:
            continue
        try:
            model = parse_dbt_model(sql_file, sources_lookup, vars_lookup)
            sibling_models[model.name] = model
            siblings.append(SiblingModel(
                name=model.name,
                file_path=sql_file.name,
                materialization=model.materialization,
                pre_hooks=model.pre_hooks,
                post_hooks=model.post_hooks,
                refs=[r for r in model.source_tables if r.upper() != model.name.upper()],
                columns_selected=model.columns_selected,
            ))
        except Exception as e:
            import sys
            print(f"  WARN: sibling parse failed {sql_file.name}: {e}", file=sys.stderr)
            continue

    if not siblings:
        return None

    # Build upstream_columns: for each ref() in the primary model, get the sibling's output columns
    primary_model = parse_dbt_model(dbt_file, sources_lookup, vars_lookup)
    upstream_columns: dict[str, list[str]] = {}
    for ref_name in primary_model.source_tables:
        ref_upper = ref_name.upper()
        for sib_name, sib_model in sibling_models.items():
            if sib_name.upper() == ref_upper and sib_model.columns_selected:
                upstream_columns[ref_name] = sib_model.columns_selected
                break

    return SiblingContext(
        primary_model=dbt_file.name,
        siblings=siblings,
        upstream_columns=upstream_columns,
        variables={},
    )


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────

def compare_workflow(
    infa: InfaWorkflow,
    dbt: DbtModel,
    xml_path: str = "",
    dbt_path: str = "",
    sources_lookup: dict[str, dict[str, str]] | None = None,
    vars_lookup: dict[str, str] | None = None,
) -> CheckResult:
    """Run all Stage 1 structural checks for a single workflow.

    Args:
        infa: Parsed INFA workflow
        dbt: Parsed DBT model
        xml_path: Path to the source XML file (for evidence)
        dbt_path: Path to the DBT model file (for evidence)
        sources_lookup: Optional resolved source definitions for sibling context
        vars_lookup: Optional resolved var definitions for sibling context
    """
    xml_file = xml_path or ""
    dbt_file = dbt_path or dbt.file_path

    source_check = _check_sources(infa, dbt)
    target_check = _check_target(infa, dbt)
    strategy_check = _check_strategy(infa, dbt)
    pre_hook_check, pre_unresolved = _check_hooks(infa.pre_sql, dbt.pre_hooks, "pre")
    post_hook_check, post_unresolved = _check_hooks(infa.post_sql, dbt.post_hooks, "post")
    column_check = _check_columns(infa, dbt)
    transform_check = _check_transforms(infa, dbt)
    pipeline_check = _check_pipelines(infa)

    # Add evidence to transform columns
    if transform_check and transform_check.columns and (xml_file or dbt_file):
        for col in transform_check.columns:
            col_name = col.column
            if xml_file and col.infa_expr:
                col.evidence.append(
                    _xml_ev(xml_file,
                            f'(?i)AS\\s+{re.escape(col_name)}\\b',
                            f"INFA: {col.infa_expr} AS {col_name}"))
            if dbt_file and col.dbt_expr:
                col.evidence.append(
                    _dbt_ev(dbt_file,
                            f'(?i)AS\\s+{re.escape(col_name)}\\b',
                            f"DBT: {col.dbt_expr} AS {col_name}"))

    # Add evidence line numbers
    if xml_file:
        # Source evidence: point to where we extracted sources from
        if infa.sq_override:
            source_check.evidence.append(
                _xml_ev(xml_file, r'NAME\s*=\s*"Sql Query".*VALUE\s*=\s*"[^"]',
                        f"INFA SQ Override sources: {source_check.infa_sources}"))
        else:
            for src in infa.source_tables[:3]:
                source_check.evidence.append(
                    _xml_ev(xml_file, f'TRANSFORMATION_NAME\\s*=\\s*"[^"]*{re.escape(src)}[^"]*".*TYPE\\s*=\\s*"SOURCE"',
                            f"INFA source: {src}"))
        target_check.evidence.append(
            _xml_ev(xml_file, f'TRANSFORMATION_NAME\\s*=\\s*"[^"]*{re.escape(infa.target_table)}[^"]*".*TYPE\\s*=\\s*"TARGET"',
                    f"INFA target: {infa.target_table}"))
        if infa.pre_sql:
            pre_hook_check.evidence.append(
                _xml_ev(xml_file, r'NAME\s*=\s*"Pre SQL".*VALUE\s*=\s*"[^"]',
                        f"INFA Pre SQL ({len(infa.pre_sql)} stmts)"))
        if infa.post_sql:
            post_hook_check.evidence.append(
                _xml_ev(xml_file, r'NAME\s*=\s*"Post SQL".*VALUE\s*=\s*"[^"]',
                        f"INFA Post SQL ({len(infa.post_sql)} stmts)"))
        if infa.sq_override:
            strategy_check.evidence.append(
                _xml_ev(xml_file, r'NAME\s*=\s*"Treat source rows as"',
                        f"INFA load type: {infa.target_load_type}"))
        if not strategy_check.evidence or strategy_check.evidence[-1].get("xml_line") == 0:
            # Fallback: try Target Load Type attribute
            if strategy_check.evidence and strategy_check.evidence[-1].get("xml_line") == 0:
                strategy_check.evidence.pop()
            strategy_check.evidence.append(
                _xml_ev(xml_file, r'NAME\s*=\s*"Target Load Type"',
                        f"INFA load type: {infa.target_load_type}"))
        column_check.evidence.append(
            _xml_ev_range(xml_file, r'<TARGET\b.*NAME\s*=\s*"', r'</TARGET>',
                          f"INFA TARGET columns ({len(infa.columns_written)} fields)"))

    if dbt_file:
        for src in dbt.source_tables[:3]:
            source_check.evidence.append(
                _dbt_ev(dbt_file, f"(?i)(?:source|ref)\\([^)]*['\"]{ re.escape(src)}['\"]",
                        f"DBT ref: {src}"))
        strat_ev = _dbt_ev(dbt_file, r"incremental_strategy\s*=",
                           f"DBT strategy: {dbt.materialization}/{dbt.incremental_strategy}")
        if strat_ev.get("dbt_line") == 0:
            # Fallback: find materialized= line for non-incremental models
            strat_ev = _dbt_ev(dbt_file, r"materialized\s*=",
                               f"DBT strategy: {dbt.materialization}/{dbt.incremental_strategy}")
        strategy_check.evidence.append(strat_ev)
        target_check.evidence.append(
            _dbt_ev(dbt_file, r"materialized\s*=",
                    f"DBT target: {dbt.target_table}"))
        if dbt.pre_hooks:
            pre_hook_check.evidence.append(
                _dbt_ev(dbt_file, r"pre_hook\s*=", "DBT pre_hook"))
        if dbt.post_hooks:
            post_hook_check.evidence.append(
                _dbt_ev(dbt_file, r"post_hook\s*=", "DBT post_hook"))
        column_check.evidence.append(
            _dbt_ev_range(dbt_file, r"^\s*SELECT\b", r"^\s*FROM\b",
                          f"DBT SELECT ({len(dbt.columns_selected)} cols)"))

    # Determine verdict
    critical_checks = [source_check.status, target_check.status, strategy_check.status]
    if any(s == "FAIL" for s in critical_checks):
        verdict = "FAIL"
    elif any(s == "FAIL" for s in [column_check.status,
                                     pre_hook_check.status, post_hook_check.status]):
        verdict = "PARTIAL"
    elif transform_check and transform_check.status == "FAIL":
        verdict = "PARTIAL"
    else:
        verdict = "PASS"

    # Collect unresolved sections for LLM
    all_unresolved = [
        UnresolvedSection(section="pre_sql", reason=u["reason"],
                          infa_sql=u.get("infa_sql", ""), dbt_sql=u.get("dbt_sql", ""))
        for u in pre_unresolved
    ] + [
        UnresolvedSection(section="post_sql", reason=u["reason"],
                          infa_sql=u.get("infa_sql", ""), dbt_sql=u.get("dbt_sql", ""))
        for u in post_unresolved
    ]

    # Extract sibling context for multi-model workflows
    sibling_ctx = extract_sibling_context(dbt_file, sources_lookup, vars_lookup) if dbt_file else None

    return CheckResult(
        workflow=infa.name.lower(),
        verdict=verdict,
        xml_path=xml_file,
        dbt_path=dbt_file,
        source_tables=source_check,
        target_table=target_check,
        load_strategy=strategy_check,
        pre_hooks=pre_hook_check,
        post_hooks=post_hook_check,
        column_list=column_check,
        transform_logic=transform_check,
        semantic_equivalence=None,
        pipeline_coverage=pipeline_check,
        sibling_context=sibling_ctx,
        unresolved=all_unresolved,
    )
