"""Critic module: validates correctness and consistency of conversion checker output."""

from __future__ import annotations

import re

# Audit patterns that should never appear as MISSING_IN_DBT
_AUDIT_PATTERNS = re.compile(
    r"^(CURRENT_TIMESTAMP|CURRENT_USER|USER|SYSDATE|CURRENT_DATE)", re.IGNORECASE
)

# Housekeeping SQL patterns (platform-specific, not real logic).
# The named procedures are real routines from the source estates this checker was
# built against; they stay because that is what the pattern has to match to
# recognise statistics/audit maintenance as noise rather than dropped logic.
_HOUSEKEEPING_RE = re.compile(
    r"(COLLECT.STATS|RUN_CREV_AUDITS|COLLECT_STATS_WRAP)", re.IGNORECASE
)


def run_critic_checks(result: dict, unresolved: list[dict]) -> list[dict]:
    """Run all critic checks on a single workflow's result + unresolved.

    Returns list of {check, status, detail} dicts.
    """
    checks = []
    checks.append(_check_evidence_completeness(result))
    checks.append(_check_verdict_matches_sections(result))
    checks.append(_check_unresolved_coverage(unresolved))
    checks.append(_check_source_pre_hook_overlap(result))
    checks.append(_check_cast_equivalence(result))
    checks.append(_check_audit_column_leakage(result))
    checks.append(_check_delete_strategy_overlap(result, unresolved))
    checks.append(_check_housekeeping_noise(unresolved))
    checks.append(_check_unresolved_reason_actionable(unresolved))
    checks.append(_check_all_sections_evaluated(result))
    checks.append(_check_transform_logic_coverage(result))
    checks.append(_check_pre_sql_actually_compared(result))
    return checks


def _check_evidence_completeness(result: dict) -> dict:
    """A1: Non-SKIP sections should have evidence with line > 0."""
    issues = []
    for section_name in ["source_tables", "target_table", "load_strategy", "column_list"]:
        section = result.get(section_name)
        if not section or section.get("status") == "SKIP":
            continue
        evidence = section.get("evidence", [])
        if not evidence:
            issues.append(f"{section_name}: no evidence")
            continue
        for ev in evidence:
            line = ev.get("xml_line") or ev.get("dbt_line") or 0
            if isinstance(line, str) and "-" in line:
                continue  # range like "37-64" is valid
            if isinstance(line, int) and line == 0:
                issues.append(f"{section_name}: evidence line=0")
                break

    status = "FAIL" if issues else "PASS"
    if not issues:
        checked = [s for s in ["source_tables", "target_table", "load_strategy", "column_list"]
                   if result.get(s) and result[s].get("status") != "SKIP"]
        detail = f"All {len(checked)} non-SKIP sections have evidence with valid line numbers"
    else:
        detail = issues
    return {"check": "evidence_completeness", "status": status, "detail": detail}


def _check_verdict_matches_sections(result: dict) -> dict:
    """A2: Verdict should be consistent with section statuses."""
    verdict = result.get("verdict", "")
    critical = ["source_tables", "target_table", "load_strategy"]
    non_critical = ["column_list", "pre_hooks", "post_hooks"]

    critical_statuses = []
    for s in critical:
        sec = result.get(s)
        if sec and sec.get("status") not in (None, "SKIP"):
            critical_statuses.append(sec["status"])

    non_critical_statuses = []
    for s in non_critical:
        sec = result.get(s)
        if sec and sec.get("status") not in (None, "SKIP"):
            non_critical_statuses.append(sec["status"])

    has_critical_fail = any(s == "FAIL" for s in critical_statuses)
    has_non_critical_fail = any(s == "FAIL" for s in non_critical_statuses)

    expected = "PASS"
    if has_critical_fail:
        expected = "FAIL"
    elif has_non_critical_fail:
        expected = "PARTIAL"

    if verdict != expected:
        return {"check": "verdict_matches_sections", "status": "FAIL",
                "detail": f"verdict={verdict} but expected={expected}"}
    return {"check": "verdict_matches_sections", "status": "PASS",
            "detail": f"Verdict '{verdict}' is consistent with section statuses"}


def _check_unresolved_coverage(unresolved: list[dict]) -> dict:
    """A4: Unresolved items should have non-empty SQL on at least one side."""
    if not unresolved:
        return {"check": "unresolved_coverage", "status": "PASS",
                "detail": "No unresolved items to check"}

    bad = []
    for i, u in enumerate(unresolved):
        if not u.get("infa_sql", "").strip() and not u.get("dbt_sql", "").strip():
            bad.append(f"item {i}: both infa_sql and dbt_sql empty")

    status = "FAIL" if bad else "PASS"
    detail = bad if bad else f"All {len(unresolved)} unresolved items have SQL on at least one side"
    return {"check": "unresolved_coverage", "status": status, "detail": detail}


def _check_source_pre_hook_overlap(result: dict) -> dict:
    """B5: Sources 'missing in DBT' that are actually produced by pre_hooks."""
    src = result.get("source_tables")
    if not src or src.get("status") != "FAIL":
        return {"check": "source_pre_hook_overlap", "status": "PASS",
                "detail": "source_tables did not FAIL; no overlap to check"}

    missing = set(s.upper() for s in src.get("missing_in_dbt", []))
    if not missing:
        return {"check": "source_pre_hook_overlap", "status": "PASS",
                "detail": "No missing sources to check against pre_hooks"}

    # Check if any missing table is an INSERT target in pre_hooks
    pre_hooks = result.get("pre_hooks", {})
    all_hook_sql = " ".join(pre_hooks.get("infa_sql", []) + pre_hooks.get("dbt_sql", []))
    all_hook_upper = all_hook_sql.upper()

    false_positives = []
    for table in missing:
        if re.search(rf"INSERT\s+INTO\s+[^\s]*{re.escape(table)}", all_hook_upper):
            false_positives.append(table)

    if false_positives:
        return {"check": "source_pre_hook_overlap", "status": "FAIL",
                "detail": f"False positive sources (produced by pre_hooks): {false_positives}"}
    return {"check": "source_pre_hook_overlap", "status": "PASS",
            "detail": f"Checked {len(missing)} missing sources; none produced by pre_hooks"}


def _check_cast_equivalence(result: dict) -> dict:
    """B6: DIFFERENT columns where only difference is a CAST wrapper."""
    tl = result.get("transform_logic")
    if not tl or not tl.get("columns"):
        return {"check": "cast_equivalence", "status": "PASS",
                "detail": "No transform columns to check for CAST-only differences"}

    false_positives = []
    for col in tl["columns"]:
        if col.get("status") != "DIFFERENT":
            continue
        infa = col.get("infa_expr", "").strip()
        dbt = col.get("dbt_expr", "").strip()
        # Check if DBT is just CAST(infa_expr AS type)
        cast_match = re.match(
            rf"CAST\(\s*{re.escape(infa)}\s+AS\s+\w+(?:\(\d+(?:,\s*\d+)?\))?\s*\)",
            dbt, re.IGNORECASE
        )
        if cast_match:
            false_positives.append(col["column"])
            continue
        # Check reverse
        cast_match = re.match(
            rf"CAST\(\s*{re.escape(dbt)}\s+AS\s+\w+(?:\(\d+(?:,\s*\d+)?\))?\s*\)",
            infa, re.IGNORECASE
        )
        if cast_match:
            false_positives.append(col["column"])

    if false_positives:
        return {"check": "cast_equivalence", "status": "FAIL",
                "detail": f"CAST-only differences (likely equivalent): {false_positives}"}
    diff_count = sum(1 for c in tl["columns"] if c.get("status") == "DIFFERENT")
    if diff_count:
        return {"check": "cast_equivalence", "status": "PASS",
                "detail": f"Checked {diff_count} DIFFERENT columns; none are CAST-only differences"}
    return {"check": "cast_equivalence", "status": "PASS",
            "detail": "No DIFFERENT columns to check"}


def _check_audit_column_leakage(result: dict) -> dict:
    """B7: MISSING_IN_DBT columns that are audit patterns."""
    tl = result.get("transform_logic")
    if not tl or not tl.get("columns"):
        return {"check": "audit_column_leakage", "status": "PASS",
                "detail": "No transform columns to check for audit leakage"}

    leaked = []
    for col in tl["columns"]:
        if col.get("status") != "MISSING_IN_DBT":
            continue
        name = col.get("column", "")
        expr = col.get("infa_expr", "")
        if _AUDIT_PATTERNS.match(name) or _AUDIT_PATTERNS.match(expr):
            leaked.append(name)

    if leaked:
        return {"check": "audit_column_leakage", "status": "FAIL",
                "detail": f"Audit columns not excluded: {leaked}"}
    missing_count = sum(1 for c in tl["columns"] if c.get("status") == "MISSING_IN_DBT")
    if missing_count:
        return {"check": "audit_column_leakage", "status": "PASS",
                "detail": f"Checked {missing_count} MISSING_IN_DBT columns; none are audit patterns"}
    return {"check": "audit_column_leakage", "status": "PASS",
            "detail": "No MISSING_IN_DBT columns to check"}


def _check_delete_strategy_overlap(result: dict, unresolved: list[dict]) -> dict:
    """B8: DELETE in unresolved that's handled by load strategy."""
    strategy = result.get("load_strategy", {}).get("infa_strategy", "")
    if "DELETE" not in strategy.upper():
        return {"check": "delete_strategy_overlap", "status": "PASS",
                "detail": "INFA strategy is not DELETE-based; no overlap possible"}

    # Check if unresolved has "No matching DELETE on INFA side"
    for u in unresolved:
        if "DELETE" in u.get("reason", "").upper() and "INFA" in u.get("reason", ""):
            return {"check": "delete_strategy_overlap", "status": "FAIL",
                    "detail": "DBT DELETE in pre_hook is likely handled by INFA DELETE+INSERT strategy"}

    return {"check": "delete_strategy_overlap", "status": "PASS",
            "detail": "INFA uses DELETE strategy; no conflicting DELETE in unresolved items"}


def _check_housekeeping_noise(unresolved: list[dict]) -> dict:
    """C10: Housekeeping statements in unresolved are noise."""
    noise = []
    for i, u in enumerate(unresolved):
        sql = (u.get("infa_sql", "") + " " + u.get("dbt_sql", "")).strip()
        if _HOUSEKEEPING_RE.search(sql):
            noise.append(f"item {i}: {u.get('reason', '')}")

    if noise:
        return {"check": "housekeeping_noise", "status": "FAIL",
                "detail": f"Platform housekeeping in unresolved (should auto-skip): {noise}"}
    if unresolved:
        return {"check": "housekeeping_noise", "status": "PASS",
                "detail": f"Checked {len(unresolved)} unresolved items; none contain housekeeping noise"}
    return {"check": "housekeeping_noise", "status": "PASS",
            "detail": "No unresolved items to check for housekeeping noise"}


def _check_unresolved_reason_actionable(unresolved: list[dict]) -> dict:
    """C9: Unresolved reasons should be specific, not generic."""
    vague = []
    vague_patterns = ["Parse error", "Unknown", "Failed"]
    for i, u in enumerate(unresolved):
        reason = u.get("reason", "")
        for p in vague_patterns:
            if p.lower() in reason.lower() and len(reason) < 50:
                vague.append(f"item {i}: '{reason}'")
                break

    if vague:
        return {"check": "unresolved_reason_actionable", "status": "FAIL",
                "detail": f"Vague reasons (not actionable for LLM): {vague}"}
    if unresolved:
        return {"check": "unresolved_reason_actionable", "status": "PASS",
                "detail": f"All {len(unresolved)} unresolved reasons are specific and actionable"}
    return {"check": "unresolved_reason_actionable", "status": "PASS",
            "detail": "No unresolved items to check"}


def _check_all_sections_evaluated(result: dict) -> dict:
    """D12: Core sections should be non-null."""
    required = ["source_tables", "target_table", "load_strategy", "pre_hooks", "post_hooks", "column_list"]
    missing = [s for s in required if result.get(s) is None]

    if missing:
        return {"check": "all_sections_evaluated", "status": "FAIL",
                "detail": f"Missing sections: {missing}"}
    return {"check": "all_sections_evaluated", "status": "PASS",
            "detail": f"All {len(required)} core sections present: {', '.join(required)}"}


def _check_transform_logic_coverage(result: dict) -> dict:
    """D13: If INFA has sq_override, transform_logic should not be null."""
    # We can infer sq_override presence from source_tables evidence mentioning "SQ Override"
    src_ev = (result.get("source_tables") or {}).get("evidence", [])
    has_sq = any("SQ Override" in str(e.get("text", "")) for e in src_ev)

    if has_sq and result.get("transform_logic") is None:
        return {"check": "transform_logic_coverage", "status": "FAIL",
                "detail": "INFA has SQ Override but transform_logic is null"}
    if has_sq:
        return {"check": "transform_logic_coverage", "status": "PASS",
                "detail": "INFA has SQ Override and transform_logic is populated"}
    return {"check": "transform_logic_coverage", "status": "PASS",
            "detail": "No SQ Override detected; transform_logic coverage not required"}


def _check_pre_sql_actually_compared(result: dict) -> dict:
    """D14: If both sides have pre_sql, content should be compared (not just presence)."""
    ph = result.get("pre_hooks", {})
    if not ph:
        return {"check": "pre_sql_actually_compared", "status": "PASS",
                "detail": "No pre_hooks section present"}

    infa_sql = ph.get("infa_sql", [])
    dbt_sql = ph.get("dbt_sql", [])

    if infa_sql and dbt_sql and ph.get("status") == "PASS" and ph.get("equivalent") is True:
        # Check if this is a genuine content comparison or just presence check
        # If both have multiple statements but equivalent=True with no evidence of matching, suspicious
        if len(infa_sql) > 1 and len(dbt_sql) > 1 and not ph.get("evidence"):
            return {"check": "pre_sql_actually_compared", "status": "FAIL",
                    "detail": "Both sides have pre_sql but no evidence of content comparison"}

    if infa_sql and dbt_sql:
        return {"check": "pre_sql_actually_compared", "status": "PASS",
                "detail": f"Pre-hooks compared: {len(infa_sql)} INFA stmt(s) vs {len(dbt_sql)} DBT stmt(s)"}
    return {"check": "pre_sql_actually_compared", "status": "PASS",
            "detail": "Pre-hooks present on only one side or empty; no content comparison needed"}
