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

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule
from dbt_audit.core.sqlutil import (
    extract_ctes,
    find_derived_subqueries,
    find_line_number,
    fingerprint,
    match_paren,
    normalize_sql,
    raw_span,
    significant_lines,
)

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "SQL"

SQL_SUBQUERY = "SQL001"
SQL_DUPLICATE_BLOCK = "SQL002"
SQL_NESTED_SUBQUERY = "SQL003"
SQL_WINDOW_WRAPPER = "SQL004"
SQL_SELECT_STAR = "SQL005"
SQL_HARDCODED_REF = "SQL006"
SQL_IMPLICIT_JOIN = "SQL007"
SQL_NONDETERMINISTIC = "SQL008"
SQL_GENERIC_CTE = "SQL009"
SQL_UNUSED_CTE = "SQL010"

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
    "Derived-table subquery should be a CTE or an ephemeral model",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale=(
        "A subquery in FROM/JOIN position hides a named step. As a CTE it becomes "
        "readable and individually testable; when the same logic appears in more than "
        "one model it belongs in an ephemeral model so there is a single definition and "
        "dbt tracks the dependency."
    ),
)
def derived_subquery(project: ProjectContext) -> Iterator[Finding]:
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
            line = find_line_number(model.stripped, hit["start"])
            # Offsets align between stripped and raw, so quote the original text.
            snippet = raw_span(
                model.raw, hit["start"], hit["start"] + len(hit["body"]) + 20, limit=200
            )

            if reused:
                others = [name for name in distinct_models if name != model.name]
                message = (
                    f"Identical subquery logic appears in {len(distinct_models)} models "
                    f"({', '.join(distinct_models)}). Duplicated logic drifts apart."
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
                    "`{{ ref('int_<describe_the_logic>') }}`. Ephemeral keeps it "
                    "inlined as a CTE at compile time, so there is no extra relation. "
                    "If it ends up referenced by three or more models, promote it to "
                    "`table` so the work is done once."
                )
                yield make_finding(
                    SQL_SUBQUERY,
                    message,
                    file=_relative(model),
                    line=line,
                    evidence=f"{hit['keyword']} ( {snippet} )",
                    remediation=remediation,
                    effort=Effort.MEDIUM,
                    project=project.name,
                    fingerprint=digest,
                    also_in=others,
                    reuse_count=len(distinct_models),
                )
            else:
                yield make_finding(
                    SQL_SUBQUERY,
                    "Subquery in FROM/JOIN position hides an unnamed transformation "
                    "step. It is used only here, so a CTE is the right home for it.",
                    severity=Severity.RECOMMENDATION,
                    file=_relative(model),
                    line=line,
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
    severity=Severity.WARNING,
    rationale=(
        "Copy-pasted logic is the most common source of metric drift: one copy gets "
        "fixed and the others do not. A shared definition -- ephemeral model or macro "
        "-- makes the fix apply everywhere."
    ),
)
def duplicate_block(project: ProjectContext) -> Iterator[Finding]:
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
            yield make_finding(
                SQL_DUPLICATE_BLOCK,
                f"CTE `{cte['name']}` is byte-identical (after normalisation) to a CTE "
                f"in {len(model_names) - 1} other model(s): "
                f"{', '.join(n for n in model_names if n != model.name)}.",
                file=_relative(model),
                line=find_line_number(model.stripped, cte["start"]),
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
    severity=Severity.WARNING,
    rationale=(
        "Nesting has to be read inside-out. A flat sequence of CTEs reads top-down and "
        "each step can be inspected on its own during debugging."
    ),
)
def nested_subquery(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python:
        return
    for subquery in find_derived_subqueries(model.stripped):
        if subquery["depth"] < 2:
            continue
        yield make_finding(
            SQL_NESTED_SUBQUERY,
            f"Subquery contains {subquery['depth']} nested SELECT levels, which has to "
            "be read inside-out.",
            file=_relative(model),
            line=find_line_number(model.stripped, subquery["start"]),
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
    "Window function filtered by a wrapping subquery instead of QUALIFY",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Snowflake's QUALIFY filters on a window result directly, removing the wrapper "
        "select that exists only to expose the window column."
    ),
)
def window_wrapper(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            SQL_WINDOW_WRAPPER,
            f"`{window_match.group(1).lower()}()` is computed in a subquery and then "
            "filtered by the enclosing WHERE. Snowflake can do this in one step.",
            file=_relative(model),
            line=find_line_number(model.stripped, subquery["start"]),
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
                "Make sure the ORDER BY is deterministic -- a tie leaves row choice "
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
    severity=Severity.RECOMMENDATION,
    rationale=(
        "SELECT * makes the output schema depend on upstream column order and silently "
        "propagates new columns. Downstream contracts and tests then describe a shape "
        "nothing pins."
    ),
)
def select_star(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python or model.layer in SELECT_STAR_EXEMPT_LAYERS:
        return
    for match in re.finditer(r"\bselect\s+\*", model.stripped, re.IGNORECASE):
        # `select * from cte` as a final passthrough is the documented CTE
        # pattern, so only flag a star that reads from a ref/source directly.
        tail = model.stripped[match.end() : match.end() + 120]
        if not re.search(r"\bfrom\s+\{\{", tail):
            continue
        yield make_finding(
            SQL_SELECT_STAR,
            "`SELECT *` reads directly from a ref or source, so this model's output "
            "schema changes whenever the upstream one does.",
            file=_relative(model),
            line=find_line_number(model.stripped, match.start()),
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
    severity=Severity.ERROR,
    rationale=(
        "A literal database.schema.table is invisible to dbt: no lineage edge, no "
        "build ordering, and the reference points at one environment regardless of "
        "target."
    ),
)
def hardcoded_ref(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            SQL_HARDCODED_REF,
            f"`{reference}` is a literal table reference, so dbt cannot see the "
            "dependency or resolve the relation per target.",
            file=_relative(model),
            line=find_line_number(model.stripped, match.start()),
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
    severity=Severity.WARNING,
    rationale=(
        "Comma joins put the join condition in the WHERE clause, where omitting it "
        "silently produces a cross join instead of a syntax error."
    ),
)
def implicit_join(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python:
        return
    for match in IMPLICIT_JOIN_PATTERN.finditer(model.stripped):
        yield make_finding(
            SQL_IMPLICIT_JOIN,
            "Comma-separated FROM list is an implicit join; a missing predicate here "
            "becomes a silent cross join.",
            file=_relative(model),
            line=find_line_number(model.stripped, match.start()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Use explicit JOIN ... ON syntax so the join condition sits with the "
                "join. Write `CROSS JOIN` deliberately when a cartesian product is "
                "actually intended."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_NONDETERMINISTIC,
    "Non-deterministic row selection",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.ERROR,
    rationale=(
        "ORDER BY (SELECT null) or ORDER BY 1 inside a dedup window picks an arbitrary "
        "row. The model looks deterministic, passes tests, and returns different data "
        "between runs."
    ),
)
def nondeterministic(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python:
        return
    for match in NONDETERMINISTIC_ORDER_PATTERN.finditer(model.stripped):
        window = model.stripped[max(0, match.start() - 200) : match.end()]
        if not WINDOW_FUNCTION_PATTERN.search(window):
            continue
        yield make_finding(
            SQL_NONDETERMINISTIC,
            "Window ordering is a placeholder, so which row survives deduplication is "
            "arbitrary and can change between runs.",
            file=_relative(model),
            line=find_line_number(model.stripped, match.start()),
            evidence=raw_span(model.raw, match.start(), match.end()),
            remediation=(
                "Supply a real ordering that breaks ties deterministically -- usually "
                "the record's updated-at timestamp plus the primary key as a final "
                "tiebreaker:\n\n"
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
    severity=Severity.RECOMMENDATION,
    rationale=(
        "A CTE's name is the only documentation of what that step does. `t1` forces "
        "every reader to reconstruct the intent from the body."
    ),
)
def generic_cte(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python:
        return
    for cte in extract_ctes(model.stripped):
        if not GENERIC_CTE_PATTERN.match(cte["name"]):
            continue
        yield make_finding(
            SQL_GENERIC_CTE,
            f"CTE `{cte['name']}` is named for its position rather than its content.",
            file=_relative(model),
            line=find_line_number(model.stripped, cte["start"]),
            evidence=f"{cte['name']} as (...)",
            remediation=(
                "Rename it after what it produces -- `orders_with_customer`, "
                "`deduplicated_events`, `daily_totals`. Import CTEs can simply take "
                "the upstream name."
            ),
            effort=Effort.LOW,
        )


@rule(
    SQL_UNUSED_CTE,
    "CTE is defined but never referenced",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "An unreferenced CTE is dead code that still has to be read and maintained, "
        "and often marks a refactor that was left half-finished."
    ),
)
def unused_cte(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            SQL_UNUSED_CTE,
            f"CTE `{cte['name']}` is defined but never selected from.",
            file=_relative(model),
            line=find_line_number(model.stripped, cte["start"]),
            evidence=f"{cte['name']} as (...)",
            remediation=(
                "Delete it if it is leftover, or wire it into the final select if the "
                "omission is a bug. An unused import CTE usually means a join was "
                "dropped by accident."
            ),
            effort=Effort.LOW,
        )
