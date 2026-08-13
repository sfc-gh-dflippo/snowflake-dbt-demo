"""
SQL -- query construction and shape.

The centrepiece is SQL001: a derived-table subquery in FROM/JOIN position, where
the *recommendation depends on reuse*. The same fragment appearing in two or more
models should become an ephemeral model so there is one definition; a fragment
used once should become a CTE in place, because promoting it to a model adds a
node to the DAG for no reuse benefit.

That decision needs a whole-project view, so the reuse-sensitive rules are
project-scoped and fingerprint normalised SQL across every model.

False positives are the main risk in this pack. Guards applied throughout:
comments, string literals and Jinja statement blocks are stripped before
matching; only FROM/JOIN subqueries are considered (never scalar subqueries,
EXISTS or IN); and the sanctioned incremental watermark
``(select max(c) from {{ this }})`` is exempt -- without that exemption every
correctly written incremental model would be flagged.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from dbt_quality.core.base import (
    Effort,
    Kind,
    Level,
    Scope,
    Severity,
    Suggestion,
    make_suggestion,
    plural,
    rule,
)
from dbt_quality.core.sqlutil import (
    extract_ctes,
    find_derived_subqueries,
    fingerprint,
    match_paren,
    normalize_sql,
    raw_span,
    significant_lines,
    span,
)

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "SQL"

SQL_SUBQUERY = "SSC-EWI-DBTSQL0001"
SQL_DUPLICATE_BLOCK = "SSC-EWI-DBTSQL0002"
SQL_NESTED_SUBQUERY = "SSC-EWI-DBTSQL0003"
SQL_WINDOW_WRAPPER = "SSC-EWI-DBTSQL0004"
SQL_SELECT_STAR = "SSC-EWI-DBTSQL0005"
SQL_HARDCODED_REF = "SSC-EWI-DBTSQL0006"
SQL_IMPLICIT_JOIN = "SSC-EWI-DBTSQL0007"
SQL_NONDETERMINISTIC = "SSC-FDM-DBTSQL0008"
SQL_GENERIC_CTE = "SSC-EWI-DBTSQL0009"
SQL_UNUSED_CTE = "SSC-EWI-DBTSQL0010"
SQL_NO_CTE_STRUCTURE = "SSC-EWI-DBTSQL0011"
SQL_UNION_DEDUP = "SSC-EWI-DBTSQL0012"
SQL_DISTINCT = "SSC-EWI-DBTSQL0013"

#: Minimum normalised length for a subquery to be worth reporting. Very short
#: derived tables (a two-column inline VALUES list, a trivial dedup) are noise.
MIN_SUBQUERY_LENGTH = 60

GENERIC_CTE_PATTERN = re.compile(
    r"^(cte|tmp|temp|tbl|t|q|a|b|x|y|s|d|sub|src\d*)\d*$", re.IGNORECASE
)

HARDCODED_TABLE_PATTERN = re.compile(
    r"\b(from|join)\s+((?!\{\{)[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*){1,2})\b",
    re.IGNORECASE,
)

# Snowflake system references that cannot be replaced with ref()/source().
HARDCODED_EXEMPT_PATTERN = re.compile(
    r"^snowflake\.(account_usage|organization_usage)"
    r"|\.information_schema\b"
    r"|^information_schema\b",
    re.IGNORECASE,
)

WINDOW_FUNCTION_PATTERN = re.compile(
    r"\b(row_number|rank|dense_rank|ntile|lag|lead|first_value|last_value)\s*\(",
    re.IGNORECASE,
)

NONDETERMINISTIC_ORDER_PATTERN = re.compile(
    r"order\s+by\s*\(\s*select\s+null\s*\)|order\s+by\s+(?:1|null)\s*\)",
    re.IGNORECASE,
)

IMPLICIT_JOIN_PATTERN = re.compile(
    r"\bfrom\s+(?:\{\{[^}]*\}\}|[A-Za-z_][\w.$]*)(?:\s+(?:as\s+)?[A-Za-z_]\w*)?\s*,\s*"
    r"(?:\{\{|[A-Za-z_])",
    re.IGNORECASE,
)

UNION_DEDUP_PATTERN = re.compile(r"\bunion\b(?!\s+all\b)", re.IGNORECASE)
SELECT_DISTINCT_PATTERN = re.compile(r"\bselect\s+distinct\b", re.IGNORECASE)

#: Layers where SELECT * is idiomatic -- a staging model passing a source
#: through, or an import CTE. Flagging those would fight our own guidance.
SELECT_STAR_EXEMPT_LAYERS = {"bronze"}


def _relative(model: ModelFile) -> str:
    return model.relative_path


# =============================================================================
# Subquery vs CTE vs ephemeral
# =============================================================================


@rule(
    SQL_SUBQUERY,
    "Derived-table subquery in FROM or JOIN",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A subquery in FROM/JOIN position hides a named step. As a CTE it becomes "
        "readable and individually testable; when the same logic appears in more than "
        "one model it belongs in an ephemeral model so there is a single definition "
        "and dbt tracks the dependency."
    ),
)
def derived_subquery(project: ProjectContext) -> Iterator[Suggestion]:
    # Fingerprint every FROM/JOIN subquery across the project so the
    # recommendation can distinguish reused logic from one-off nesting.
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for model in project.models:
        if model.is_python:
            continue
        for subquery in find_derived_subqueries(model.stripped):
            body = subquery["body"]
            if len(normalize_sql(body)) < MIN_SUBQUERY_LENGTH:
                continue
            occurrences[fingerprint(body)].append({"model": model, **subquery})

    for digest, hits in sorted(occurrences.items()):
        distinct_models = sorted({hit["model"].name for hit in hits})
        reused = len(distinct_models) > 1

        for hit in hits:
            model: ModelFile = hit["model"]
            # Offsets align between stripped and raw, so quote the original text.
            snippet = raw_span(
                model.raw, hit["start"], hit["start"] + len(hit["body"]) + 20, limit=200
            )

            if reused:
                others = [name for name in distinct_models if name != model.name]
                message = (
                    f"The same subquery body appears in {len(distinct_models)} models: "
                    f"{', '.join(distinct_models)}."
                )
                remediation = (
                    "Extract this into an ephemeral model so there is one definition "
                    "and dbt tracks the dependency:\n\n"
                    "```sql\n"
                    "-- models/silver/int_<describe_the_logic>.sql\n"
                    "{{ config(materialized='ephemeral') }}\n"
                    "<the subquery body>\n"
                    "```\n\n"
                    "Then replace each subquery with "
                    "`{{ ref('int_<describe_the_logic>') }}`. Ephemeral materializes "
                    "as a CTE at compile time, adding no extra relation. Upgrade to "
                    "`table` when referenced by three or more models."
                )
                yield make_suggestion(
                    SQL_SUBQUERY,
                    message,
                    file=_relative(model),
                    **span(model.stripped, hit["start"], hit["end"]),
                    evidence=f"{hit['keyword']} ( {snippet} )",
                    remediation=remediation,
                    effort=Effort.MEDIUM,
                    project=project.name,
                    fingerprint=digest,
                    also_in=others,
                    reuse_count=len(distinct_models),
                )
            else:
                yield make_suggestion(
                    SQL_SUBQUERY,
                    "This subquery appears only in this model.",
                    level=Level.INFORMATION,
                    file=_relative(model),
                    **span(model.stripped, hit["start"], hit["end"]),
                    evidence=f"{hit['keyword']} ( {snippet} )",
                    remediation=(
                        "Lift it into a named CTE so the step is self-describing:\n\n"
                        "```sql\n"
                        "with <descriptive_name> as (\n"
                        "    <the subquery body>\n"
                        ")\n"
                        "select ... from <descriptive_name>\n"
                        "```\n\n"
                        "Name it for what it produces, not for its position. Only "
                        "promote it to an ephemeral model if a second model needs the "
                        "same logic."
                    ),
                    effort=Effort.LOW,
                    project=project.name,
                    fingerprint=digest,
                    reuse_count=1,
                )


@rule(
    SQL_DUPLICATE_BLOCK,
    "Identical SQL block repeated across models",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Copy-pasted logic is the most common source of metric drift: one copy gets "
        "fixed and the others do not. A shared ephemeral model or macro applies the "
        "fix everywhere."
    ),
)
def duplicate_block(project: ProjectContext) -> Iterator[Suggestion]:
    """
    Detect repeated CTE bodies across models.

    Uses CTE bodies rather than arbitrary line windows because a CTE is already a
    unit the author chose to name, which makes the extraction suggestion concrete
    and keeps the false-positive rate low.
    """
    threshold = project.config.duplicate_block_threshold
    min_lines = project.config.duplicate_block_min_lines
    groups: dict[str, list[tuple[ModelFile, dict[str, Any]]]] = defaultdict(list)

    for model in project.models:
        if model.is_python:
            continue
        for cte in extract_ctes(model.stripped):
            if significant_lines(cte["body"]) < min_lines:
                continue
            groups[fingerprint(cte["body"])].append((model, cte))

    for digest, hits in sorted(groups.items()):
        model_names = sorted({model.name for model, _ in hits})
        if len(model_names) < 2:
            continue

        target = "a macro" if len(model_names) >= threshold else "an ephemeral model"
        for model, cte in hits:
            yield make_suggestion(
                SQL_DUPLICATE_BLOCK,
                f"CTE `{cte['name']}` is byte-identical to a CTE in "
                f"{plural(len(model_names) - 1, 'other model', 'other models')}: "
                f"{', '.join(n for n in model_names if n != model.name)}.",
                file=_relative(model),
                **span(model.stripped, cte["start"], cte["end"]),
                evidence=raw_span(
                    model.stripped, cte["start"], cte["start"] + len(cte["body"])
                ),
                remediation=(
                    f"Extract the shared logic into {target}. Use an ephemeral model "
                    "when the block is a self-contained query over refs; use a macro "
                    "when it is a parameterised expression or column list reused in "
                    "different query shapes."
                ),
                effort=Effort.MEDIUM,
                project=project.name,
                fingerprint=digest,
                repeated_in=model_names,
            )


@rule(
    SQL_NESTED_SUBQUERY,
    "Deeply nested subqueries",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Nesting has to be read inside-out. A flat sequence of CTEs reads top-down and "
        "each step can be inspected on its own during debugging."
    ),
)
def nested_subquery(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for subquery in find_derived_subqueries(model.stripped):
        if subquery["depth"] < 2:
            continue
        yield make_suggestion(
            SQL_NESTED_SUBQUERY,
            f"This subquery has {subquery['depth']} nested `select` levels; "
            "sequential CTEs read top-down.",
            file=_relative(model),
            **span(model.stripped, subquery["start"], subquery["end"]),
            evidence=raw_span(
                model.raw,
                subquery["start"],
                subquery["start"] + len(subquery["body"]) + 20,
            ),
            remediation=(
                "Flatten the nesting into sequential CTEs, one per logical step, so "
                "the model reads in execution order. Each CTE can then be selected "
                "from directly while debugging."
            ),
            effort=Effort.MEDIUM,
        )


@rule(
    SQL_WINDOW_WRAPPER,
    "Window function in subquery instead of QUALIFY",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Snowflake's QUALIFY filters on a window result directly, removing the wrapper "
        "select that exists only to expose the window column."
    ),
)
def window_wrapper(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python or re.search(r"\bqualify\b", model.stripped, re.IGNORECASE):
        return
    for subquery in find_derived_subqueries(model.stripped):
        body = subquery["body"]
        window_match = WINDOW_FUNCTION_PATTERN.search(body)
        if not window_match:
            continue
        # The wrapper must filter on something after the subquery closes.
        open_index = model.stripped.index("(", subquery["start"])
        close_index = match_paren(model.stripped, open_index)
        if close_index == -1:
            continue
        tail = model.stripped[close_index : close_index + 400]
        if not re.search(r"\bwhere\b", tail, re.IGNORECASE):
            continue
        yield make_suggestion(
            SQL_WINDOW_WRAPPER,
            f"`{window_match.group(1).lower()}()` is computed in a subquery filtered "
            "by an outer `where`; `qualify` does this in one step.",
            file=_relative(model),
            **span(model.stripped, subquery["start"], subquery["end"]),
            evidence=raw_span(model.raw, subquery["start"], close_index + 1, limit=180),
            remediation=(
                "Replace the wrapper with QUALIFY:\n\n"
                "```sql\n"
                "select ...\n"
                "from {{ ref('upstream') }}\n"
                "qualify row_number() over (\n"
                "    partition by customer_id order by updated_at desc\n"
                ") = 1\n"
                "```\n\n"
                "Make sure the `ORDER BY` is deterministic: a tie leaves row choice "
                "arbitrary."
            ),
            effort=Effort.LOW,
        )


# =============================================================================
# Reference hygiene and query shape
# =============================================================================


@rule(
    SQL_SELECT_STAR,
    "SELECT * outside the staging layer",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "SELECT * makes the output schema depend on upstream column order and silently "
        "propagates new columns. Downstream contracts and tests then describe a shape "
        "nothing pins."
    ),
)
def select_star(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python or model.layer in SELECT_STAR_EXEMPT_LAYERS:
        return
    for match in re.finditer(r"\bselect\s+\*", model.stripped, re.IGNORECASE):
        # `select * from cte` as a final passthrough is the documented CTE
        # pattern, so only flag a star that reads from a ref/source directly.
        tail = model.stripped[match.end() : match.end() + 120]
        if not re.search(r"\bfrom\s+\{\{", tail):
            continue
        yield make_suggestion(
            SQL_SELECT_STAR,
            "`select *` reads from a `ref` or `source`, so the output schema changes "
            "whenever upstream columns change.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end() + 80),
            remediation=(
                "List the columns explicitly. For a wide passthrough where that is "
                "impractical, use `{{ dbt_utils.star(from=ref('upstream'), "
                "except=['col_to_drop']) }}` so the expansion is at least resolved at "
                "compile time and visible in the compiled SQL."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_HARDCODED_REF,
    "Hardcoded table reference instead of ref() or source()",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.HIGH,
    rationale=(
        "A literal database.schema.table is invisible to dbt: no lineage edge, no "
        "build ordering, and the reference points at one environment regardless of "
        "target."
    ),
)
def hardcoded_ref(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    # CTE names declared in this file are legitimate FROM targets.
    local_names = {cte["name"].lower() for cte in extract_ctes(model.stripped)}
    for match in HARDCODED_TABLE_PATTERN.finditer(model.stripped):
        reference = match.group(2)
        if reference.split(".")[0].lower() in local_names:
            continue
        # A trailing alias like `from x.y z` still counts; but skip obvious
        # Snowflake pseudo-references such as table(...) or lateral flatten.
        if reference.lower().startswith(("table.", "lateral.", "values.")):
            continue
        if HARDCODED_EXEMPT_PATTERN.search(reference):
            continue
        yield make_suggestion(
            SQL_HARDCODED_REF,
            f"`{reference}` is a literal table reference; "
            "dbt cannot track it in lineage or resolve it per target.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Use `{{ ref('model_name') }}` if a dbt model produces it, or declare "
                "it in a `sources:` block and use "
                "`{{ source('source_name', 'table_name') }}`. Both give dbt lineage "
                "and let the relation resolve differently in dev and prod."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_IMPLICIT_JOIN,
    "Implicit comma join",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Comma joins put the join condition in the WHERE clause, where omitting it "
        "silently produces a cross join instead of a syntax error."
    ),
)
def implicit_join(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for match in IMPLICIT_JOIN_PATTERN.finditer(model.stripped):
        yield make_suggestion(
            SQL_IMPLICIT_JOIN,
            "Comma-separated `from` clause; a missing predicate silently produces "
            "a cross join.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Use explicit `JOIN ... ON` syntax so the join condition sits with "
                "the join. Write `CROSS JOIN` deliberately when a cartesian product "
                "is intended."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_UNION_DEDUP,
    "UNION without ALL deduplicates rows",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "UNION removes duplicate rows and performs duplicate-elimination work. "
        "UNION ALL preserves every row and avoids that work when duplicates are "
        "meaningful or impossible."
    ),
)
def union_dedup(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for match in UNION_DEDUP_PATTERN.finditer(model.stripped):
        yield make_suggestion(
            SQL_UNION_DEDUP,
            "`union` performs duplicate-elimination work on every row; "
            "`union all` skips that cost.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Use `union all` when both inputs should be retained. Keep `union` "
                "only when distinct combined rows are the intended business result."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_DISTINCT,
    "SELECT DISTINCT masking a grain problem",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "SELECT DISTINCT removes duplicate projected rows and performs "
        "duplicate-elimination work. It can mask an upstream join or grain issue "
        "that should be understood explicitly."
    ),
)
def select_distinct(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for match in SELECT_DISTINCT_PATTERN.finditer(model.stripped):
        yield make_suggestion(
            SQL_DISTINCT,
            "`select distinct` performs duplicate-elimination work and may hide "
            "an upstream grain problem that `qualify` would make explicit.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Keep `distinct` when all projected rows must be deduplicated and no "
                "row-selection rule exists. Otherwise, fix the upstream grain or use "
                "`qualify row_number() over "
                "(partition by business_key order by updated_at desc) = 1` with the "
                "correct key and deterministic ordering."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_NONDETERMINISTIC,
    "Non-deterministic row selection",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.FDM,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "ORDER BY (SELECT null) or ORDER BY 1 inside a dedup window picks an arbitrary "
        "row. The model looks deterministic, passes tests, and returns different data "
        "between runs."
    ),
)
def nondeterministic(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for match in NONDETERMINISTIC_ORDER_PATTERN.finditer(model.stripped):
        window = model.stripped[max(0, match.start() - 200) : match.end()]
        if not WINDOW_FUNCTION_PATTERN.search(window):
            continue
        yield make_suggestion(
            SQL_NONDETERMINISTIC,
            "The window `order by` is a placeholder; "
            "which row survives deduplication is arbitrary between runs.",
            file=_relative(model),
            **span(model.stripped, match.start(), match.end()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Supply a real ordering that breaks ties deterministically. "
                "Use the updated-at timestamp plus the primary key as a tiebreaker:\n\n"
                "```sql\n"
                "qualify row_number() over (\n"
                "    partition by customer_id\n"
                "    order by updated_at desc, source_row_id\n"
                ") = 1\n"
                "```\n\n"
                "If this is converted code, the placeholder was left for a human to "
                "resolve and the correct column has to come from the source system."
            ),
            effort=Effort.MEDIUM,
        )


# =============================================================================
# CTE hygiene
# =============================================================================


@rule(
    SQL_GENERIC_CTE,
    "Uninformative CTE name",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A CTE's name is the only documentation of what that step does. `t1` forces "
        "every reader to reconstruct the intent from the body."
    ),
)
def generic_cte(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    for cte in extract_ctes(model.stripped):
        if not GENERIC_CTE_PATTERN.match(cte["name"]):
            continue
        yield make_suggestion(
            SQL_GENERIC_CTE,
            f"CTE `{cte['name']}` has a generic name; "
            "rename it for what the step produces.",
            file=_relative(model),
            **span(model.stripped, cte["start"], cte["end"]),
            evidence=f"{cte['name']} as (...)",
            remediation=(
                "Rename it after what it produces: `orders_with_customer`, "
                "`deduplicated_events`, `daily_totals`. Import CTEs can take the "
                "upstream name."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_UNUSED_CTE,
    "Unreferenced CTE",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "An unreferenced CTE is dead code that still has to be read and maintained, "
        "and often marks a refactor that was left half-finished."
    ),
)
def unused_cte(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    ctes = extract_ctes(model.stripped)
    if not ctes:
        return
    for cte in ctes:
        # Count references outside this CTE's own body (self-reference in a
        # recursive CTE is legitimate and must not count as external use).
        body_start = model.stripped.index("(", cte["start"])
        body_end = match_paren(model.stripped, body_start)
        outside = model.stripped[: cte["start"]] + model.stripped[body_end + 1 :]
        if re.search(rf"\b{re.escape(cte['name'])}\b", outside, re.IGNORECASE):
            continue
        yield make_suggestion(
            SQL_UNUSED_CTE,
            f"CTE `{cte['name']}` is defined but never referenced in this model.",
            file=_relative(model),
            **span(model.stripped, cte["start"], cte["end"]),
            evidence=f"{cte['name']} as (...)",
            remediation=(
                "Delete it if it is leftover, or wire it into the final select if the "
                "omission is a bug. An unused import CTE usually means a join was "
                "dropped by accident."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_NO_CTE_STRUCTURE,
    "Flat model without named CTEs",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Named CTEs give each transformation step a name and let a reader follow the "
        "model top-down. A single flat SELECT doing several things at once has to be "
        "unpicked mentally, and no step can be selected from in isolation while "
        "debugging."
    ),
)
def no_cte_structure(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    """
    Carried over from the retired dbt-validation ``SQL002``.

    Kept deliberately narrow. A trivial passthrough does not benefit from a CTE, so
    the rule only fires on a model doing enough work to have steps worth naming --
    a join, an aggregate, or a window function. Staging is exempt because a
    one-to-one projection of a source is meant to be flat.
    """
    if model.is_python or model.layer == "bronze":
        return
    if model.materialization == "ephemeral":
        # An ephemeral model is itself inlined as a CTE by the consumer.
        return
    if extract_ctes(model.stripped):
        return
    # `where false` is the placeholder-model idiom; it has no logic to structure.
    if re.search(r"\bwhere\s+false\b", model.stripped, re.IGNORECASE):
        return

    complexity = [
        label
        for label, pattern in (
            ("a join", r"\bjoin\b"),
            ("an aggregate", r"\b(sum|count|avg|min|max|median|listagg)\s*\("),
            ("a window function", r"\bover\s*\("),
            ("a set operation", r"\b(union|intersect|except)\b"),
        )
        if re.search(pattern, model.stripped, re.IGNORECASE)
    ]
    if not complexity:
        return

    yield make_suggestion(
        SQL_NO_CTE_STRUCTURE,
        f"This model contains {' and '.join(complexity)} but no named CTEs.",
        file=_relative(model),
        evidence=", ".join(complexity),
        remediation=(
            "Break the query into named CTEs, one per step, ending with a final "
            "select:\n\n"
            "```sql\n"
            "with orders as (\n"
            "    select * from {{ ref('stg_orders') }}\n"
            "),\n"
            "daily_totals as (\n"
            "    select order_date, sum(amount) as total_amount\n"
            "    from orders\n"
            "    group by order_date\n"
            ")\n"
            "select * from daily_totals\n"
            "```\n\n"
            "Name each CTE for what it produces. While debugging you can then select "
            "from any single step."
        ),
        effort=Effort.LOW,
    )
