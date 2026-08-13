"""
MAC -- macro discipline, in both directions.

Over-use and under-use are both failures, and they need opposite remedies, so
this pack measures both. Over-abstraction shows up as macros that wrap a single
expression, macros called from exactly one place, macros that emit whole SELECT
statements, and models whose bodies are mostly Jinja. Under-abstraction shows up
as the same multi-line SQL repeated across several models.

Note: this repo's skills contain no prescriptive macro guidance -- the thresholds
here are authored for this audit rather than extracted from existing docs, which
is why they are all configurable in ``.dbt-quality.yml``.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING

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
    extract_macro_calls,
    match_paren,
    significant_lines,
    span,
    strip_all,
)

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "MAC"

MAC_RATIO = "SSC-EWI-DBTMAC0001"
MAC_SINGLE_CALLER = "SSC-EWI-DBTMAC0002"
MAC_UNUSED = "SSC-EWI-DBTMAC0003"
MAC_TRIVIAL = "SSC-EWI-DBTMAC0004"
MAC_EMITS_QUERY = "SSC-EWI-DBTMAC0005"
MAC_HARDCODED_RELATION = "SSC-EWI-DBTMAC0006"
MAC_DEEP_NESTING = "SSC-EWI-DBTMAC0007"
MAC_JINJA_HEAVY = "SSC-EWI-DBTMAC0008"
MAC_HASHED_FK = "SSC-EWI-DBTMAC0009"
MAC_MISSING_ABSTRACTION = "SSC-EWI-DBTMAC0010"
MAC_IN_MODELS_DIR = "SSC-EWI-DBTMAC0011"
MAC_NAME_MISMATCH = "SSC-EWI-DBTMAC0012"

#: Every Snowflake scalar hash function yields broad values that hinder pruning
#: when used for relationship keys. Hash-diffs over non-key attributes are valid.
_SNOWFLAKE_HASH_FUNCTION_PATTERN = re.compile(
    r"\b(?:hash|md5(?:_binary)?|sha1(?:_binary)?|sha2(?:_binary)?)\s*\(",
    re.IGNORECASE,
)
_FOREIGN_KEY_FIELD_PATTERN = re.compile(r"\b[\w$]*(?:_id|_key)\b", re.IGNORECASE)

#: dbt_utils equivalents that teams commonly hand-roll (excluding hash and pivot).
UTIL_REIMPLEMENTATIONS: list[tuple[str, str, str]] = [
    (
        r"\bdate\w*\s+between\s+.*\bseq4\s*\(",
        "dbt_utils.date_spine",
        "hand-rolled date spine",
    ),
    (
        r"\bgenerator\s*\(\s*rowcount",
        "dbt_utils.date_spine",
        "hand-rolled row generator for a date series",
    ),
]

#: A macro body containing these is doing real work, not merely wrapping.
LOGIC_MARKERS = re.compile(r"\{%-?\s*(if|for|set|do|call)\b", re.IGNORECASE)

#: Macro emitting a full query shape rather than an expression or predicate.
QUERY_EMITTING_PATTERN = re.compile(r"\bselect\b[\s\S]{0,400}?\bfrom\b", re.IGNORECASE)

RELATION_LITERAL_PATTERN = re.compile(
    r"\b(from|join)\s+((?!\{\{|\{%)[A-Za-z_][\w$]*(?:\.[A-Za-z_][\w$]*){1,2})\b",
    re.IGNORECASE,
)


def _all_call_sites(project: ProjectContext) -> dict[str, list[tuple[str, int]]]:
    """
    Map macro name -> [(file, line)] across models, macros, and project config.

    Call sites in other macros count, otherwise a helper called only by another
    macro reads as dead. Hooks in ``dbt_project.yml`` count too, since that is
    where operational macros are usually invoked.
    """
    sites: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for model in project.models:
        for call in model.macro_calls:
            sites[call["bare"]].append((model.relative_path, call["line"]))

    for macro_file in project.macros:
        for call in extract_macro_calls(macro_file.raw):
            sites[call["bare"]].append((macro_file.relative_path, call["line"]))

    # dbt_project.yml hooks and any other string values referencing a macro.
    project_text = str(project.project_yml)
    for call in extract_macro_calls(project_text):
        sites[call["bare"]].append(("dbt_project.yml", 0))

    for _path, raw in project.snapshot_files:
        for call in extract_macro_calls(raw):
            sites[call["bare"]].append(("snapshots", call["line"]))

    return sites


def _self_calls(macro_file_raw: str, macro_name: str) -> int:
    """How many times a macro's own file calls it (recursion, or sibling defs)."""
    return len(
        [c for c in extract_macro_calls(macro_file_raw) if c["bare"] == macro_name]
    )


# =============================================================================
# Over-use
# =============================================================================


@rule(
    MAC_RATIO,
    "High macro-to-model ratio",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Macros remove logic from the compiled artifact a reviewer reads. "
        "A high macro-to-model ratio signals over-abstraction that raises "
        "the cost of reading individual models."
    ),
)
def macro_ratio(project: ProjectContext) -> Iterator[Suggestion]:
    macro_count = sum(len(f.macros) for f in project.macros)
    model_count = project.model_count
    if model_count == 0 or macro_count == 0:
        return
    ratio = macro_count / model_count
    if ratio < project.config.macro_model_ratio:
        return
    yield make_suggestion(
        MAC_RATIO,
        f"{macro_count} macros for {model_count} models "
        f"(ratio {ratio:.2f}) exceeds the "
        f"{project.config.macro_model_ratio:.2f} threshold.",
        file="macros/",
        evidence=f"{macro_count} macros / {model_count} models",
        remediation=(
            "Inline single-caller macros and delete unused ones. "
            "Keep macros for logic that is parameterized or shared across "
            "multiple call sites. "
            "Prefer an ephemeral model when the shared piece is a query, "
            "so it stays in the DAG."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    MAC_SINGLE_CALLER,
    "Macro is called from only one place",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A macro with one caller adds a file to navigate without serving "
        "more than one consumer. The logic is no longer visible at its use site."
    ),
)
def single_caller(project: ProjectContext) -> Iterator[Suggestion]:
    sites = _all_call_sites(project)
    for macro_file in project.macros:
        for macro in macro_file.macros:
            name = macro["name"]
            external = [
                (path, line)
                for path, line in sites.get(name, [])
                if path != macro_file.relative_path
            ]
            if len(external) != 1:
                continue
            # A macro with real branching may justifiably have one caller today.
            if (
                LOGIC_MARKERS.search(macro["body"])
                and significant_lines(macro["body"]) > 10
            ):
                continue
            caller_path, caller_line = external[0]
            yield make_suggestion(
                MAC_SINGLE_CALLER,
                f"`{name}` has exactly one external caller: "
                f"`{caller_path}:{caller_line}`.",
                file=macro_file.relative_path,
                **span(macro_file.raw, macro["start"], macro["end"]),
                evidence=f"{{% macro {name}({', '.join(macro['args'])}) %}}",
                remediation=(
                    f"Inline the body at `{caller_path}` and delete the macro. "
                    "Keep it only if a second caller is expected soon."
                ),
                effort=Effort.LOW,
                caller=caller_path,
            )


@rule(
    MAC_UNUSED,
    "Macro is never called",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale="Dead code still has to be read, reviewed, and kept compiling.",
)
def unused_macro(project: ProjectContext) -> Iterator[Suggestion]:
    sites = _all_call_sites(project)
    for macro_file in project.macros:
        for macro in macro_file.macros:
            name = macro["name"]
            # Adapter-dispatch overrides and dbt hook macros are invoked by dbt
            # itself, never by name in user code, so they are never "unused".
            if re.match(
                r"^(snowflake__|default__|dbt_|generate_(schema|database|alias)_name$|"
                r"get_custom_|test_|ref$|source$)",
                name,
            ):
                continue
            if sites.get(name):
                continue
            yield make_suggestion(
                MAC_UNUSED,
                f"`{name}` has no detected callers in this project.",
                file=macro_file.relative_path,
                **span(macro_file.raw, macro["start"], macro["end"]),
                evidence=f"{{% macro {name}({', '.join(macro['args'])}) %}}",
                remediation=(
                    "Delete the macro. "
                    "If it is called dynamically (via `context` lookup or from "
                    "outside this project), add a comment explaining that, "
                    "or the next reader will remove it."
                ),
                effort=Effort.LOW,
            )


@rule(
    MAC_TRIVIAL,
    "Macro wraps a trivial expression",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A single-expression macro with no branching adds a file to open "
        "without encapsulating a decision. The inline SQL is clearer."
    ),
)
def trivial_macro(project: ProjectContext) -> Iterator[Suggestion]:
    for macro_file in project.macros:
        for macro in macro_file.macros:
            body = macro["body"].strip()
            if not body or LOGIC_MARKERS.search(body):
                continue
            if significant_lines(body) > 2:
                continue
            if len(strip_all(body).strip()) > 120:
                continue
            yield make_suggestion(
                MAC_TRIVIAL,
                f"`{macro['name']}` wraps a single short expression "
                "with no branching or conditional logic.",
                file=macro_file.relative_path,
                **span(macro_file.raw, macro["start"], macro["end"]),
                evidence=re.sub(r"\s+", " ", body)[:140],
                remediation=(
                    "Inline the expression. "
                    "A macro is worth keeping when it encapsulates a choice "
                    "(dialect dispatch, conditional logic, a column loop) "
                    "or when the expression is long enough that naming it "
                    "aids reading."
                ),
                effort=Effort.LOW,
            )


@rule(
    MAC_EMITS_QUERY,
    "Macro emits a full query",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "When a macro emits `select ... from`, the model's core logic lives "
        "outside the model file. "
        "Lineage tools see only the macro call, not what it produces."
    ),
)
def macro_emits_query(project: ProjectContext) -> Iterator[Suggestion]:
    for macro_file in project.macros:
        for macro in macro_file.macros:
            body = macro["body"]
            if not QUERY_EMITTING_PATTERN.search(strip_all(body)):
                continue
            # Materializations and operational macros legitimately emit SQL.
            if re.match(
                r"^(snowflake__|default__|create_|drop_|grant_|apply_|refresh_)",
                macro["name"],
            ):
                continue
            yield make_suggestion(
                MAC_EMITS_QUERY,
                f"`{macro['name']}` emits a full `select ... from` query, "
                "hiding the model's core logic outside the model file.",
                file=macro_file.relative_path,
                **span(macro_file.raw, macro["start"], macro["end"]),
                evidence=re.sub(r"\s+", " ", body.strip())[:180],
                remediation=(
                    "Convert the query to an ephemeral model so it gains a "
                    "name in the DAG and can be tested. "
                    "Reserve macros for expressions, predicates, and column lists."
                ),
                effort=Effort.MEDIUM,
            )


@rule(
    MAC_HARDCODED_RELATION,
    "Macro hardcodes a relation name",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "A literal relation inside a macro bypasses `ref()`, hiding the "
        "dependency from dbt and preventing target-environment resolution."
    ),
)
def macro_hardcoded_relation(project: ProjectContext) -> Iterator[Suggestion]:
    for macro_file in project.macros:
        for macro in macro_file.macros:
            stripped = strip_all(macro["body"])
            for match in RELATION_LITERAL_PATTERN.finditer(stripped):
                reference = match.group(2)
                if reference.lower().startswith(
                    ("information_schema.", "snowflake.", "table.")
                ):
                    continue
                yield make_suggestion(
                    MAC_HARDCODED_RELATION,
                    f"`{reference}` in `{macro['name']}` is a literal "
                    "relation name, bypassing `ref()` and hiding the "
                    "dependency from dbt.",
                    file=macro_file.relative_path,
                    **span(
                        macro_file.raw,
                        macro["body_start"] + match.start(),
                        macro["body_start"] + match.end(),
                    ),
                    evidence=match.group(0).strip(),
                    remediation=(
                        f"Pass the relation as an argument: "
                        f"`{{{{ {macro['name']}(ref('the_model')) }}}}`. "
                        "The caller's `ref()` creates the lineage edge and "
                        "resolves the relation per target. "
                        "If the table is an external system with no dbt model, "
                        "add a comment to that effect."
                    ),
                    effort=Effort.MEDIUM,
                )


@rule(
    MAC_DEEP_NESTING,
    "Macro call chain is deeply nested",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Each macro hop is a file to open while tracing execution. "
        "A chain of three or more makes compiled output the only practical "
        "way to see what runs."
    ),
)
def deep_nesting(project: ProjectContext) -> Iterator[Suggestion]:
    defined: dict[str, tuple[str, dict[str, object]]] = {}
    for macro_file in project.macros:
        for macro in macro_file.macros:
            defined[macro["name"]] = (macro_file.relative_path, macro)

    def depth(name: str, seen: frozenset[str]) -> tuple[int, list[str]]:
        if name in seen or name not in defined:
            return 0, []
        _path, macro = defined[name]
        best, best_chain = 0, []
        for call in extract_macro_calls(str(macro["body"])):
            child = call["bare"]
            if child not in defined:
                continue
            child_depth, child_chain = depth(child, seen | {name})
            if child_depth + 1 > best:
                best, best_chain = child_depth + 1, [child, *child_chain]
        return best, best_chain

    for name, (path, macro) in sorted(defined.items()):
        levels, chain = depth(name, frozenset())
        if levels < 2:
            continue
        yield make_suggestion(
            MAC_DEEP_NESTING,
            f"`{name}` has a {levels}-level macro call chain: "
            f"{' -> '.join([name, *chain])}.",
            file=path,
            line=int(macro["line"]),
            evidence=" -> ".join([name, *chain]),
            remediation=(
                "Collapse thin pass-through macros into their caller so the "
                "SQL is reachable in fewer hops. "
                "Keep layers only when each encapsulates a distinct decision, "
                "such as dialect dispatch."
            ),
            effort=Effort.MEDIUM,
            chain=[name, *chain],
        )


@rule(
    MAC_JINJA_HEAVY,
    "Model body is mostly Jinja rather than SQL",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "When a model is mostly macro calls, readers cannot tell what SQL "
        "it produces without compiling it."
    ),
)
def jinja_heavy(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.is_python:
        return
    total = significant_lines(model.raw)
    if total < 5:
        return
    # Exclude the config block from the Jinja count; it is not logic.
    body = re.sub(r"\{\{-?\s*config\s*\([\s\S]*?\)\s*-?\}\}", "", model.raw)
    sql_only = strip_all(body)
    sql_lines = significant_lines(sql_only)
    jinja_lines = max(0, significant_lines(body) - sql_lines)
    user_calls = [c for c in model.macro_calls if not c["name"].startswith("dbt_")]
    if jinja_lines / max(1, significant_lines(body)) < 0.5 or len(user_calls) < 2:
        return
    yield make_suggestion(
        MAC_JINJA_HEAVY,
        f"{jinja_lines} of {significant_lines(body)} body lines are Jinja "
        f"across {plural(len(user_calls), 'project macro call', 'project macro calls')}, "
        "hiding the model's SQL from readers.",
        file=model.relative_path,
        evidence=", ".join(sorted({c["name"] for c in user_calls})[:6]),
        remediation=(
            "Move the core transformation back into SQL and keep macros at "
            "the edges: shared predicates, column lists, or audit-column blocks. "
            "If the generation is dynamic, add a comment with a representative "
            "compiled output so readers understand intent without running dbt."
        ),
        effort=Effort.HIGH,
    )


@rule(
    MAC_HASHED_FK,
    "Hashed foreign-key fields impair Snowflake join pruning",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Hash values have broad micro-partition ranges. "
        "Joining on a hashed relationship field reduces pruning compared "
        "with the original columns or a concatenated key."
    ),
)
def reimplements_util(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    if model.is_python:
        return
    # Hashing an FK-shaped field hurts Snowflake pruning; a hash-diff without
    # relationship fields is deliberately ignored.
    for hash_match in _SNOWFLAKE_HASH_FUNCTION_PATTERN.finditer(model.stripped):
        open_paren = model.stripped.find("(", hash_match.start())
        close_paren = match_paren(model.stripped, open_paren)
        if close_paren == -1:
            continue
        hash_expression = model.stripped[hash_match.start() : close_paren + 1]
        if not _FOREIGN_KEY_FIELD_PATTERN.search(hash_expression):
            continue
        yield make_suggestion(
            MAC_HASHED_FK,
            "Hashing foreign-key fields for a join key impairs "
            "Snowflake micro-partition pruning.",
            file=model.relative_path,
            **span(model.raw, hash_match.start(), close_paren + 1),
            evidence=re.sub(r"\s+", " ", hash_expression)[:140],
            remediation=(
                "Join on the original foreign-key columns or use the "
                "project's concatenated natural-key strategy. "
                "Add a `dbt_constraints` relationships test. "
                "Reserve hash-diff patterns for non-key change detection."
            ),
            effort=Effort.LOW,
        )


# =============================================================================
# Under-use
# =============================================================================


@rule(
    MAC_MISSING_ABSTRACTION,
    "Repeated SQL block that should be a macro",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "The same block copied into several models means a fix has to be "
        "applied several times, and eventually will not be."
    ),
)
def missing_abstraction(project: ProjectContext) -> Iterator[Suggestion]:
    """
    Find identical multi-line statement windows repeated across models.

    Complements SQL002 (which compares whole CTE bodies) by catching repetition
    that is not CTE-shaped -- a shared CASE expression, a standard audit-column
    block, a repeated set of window functions.
    """
    threshold = project.config.duplicate_block_threshold
    window_size = project.config.duplicate_block_min_lines
    blocks: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for model in project.models:
        if model.is_python:
            continue
        lines = [line.strip() for line in model.stripped.splitlines()]
        meaningful = [(i, line) for i, line in enumerate(lines, start=1) if line]
        for start in range(len(meaningful) - window_size + 1):
            window = meaningful[start : start + window_size]
            text = " ".join(line for _n, line in window)
            if len(text) < 80:
                continue
            key = re.sub(r"\s+", " ", text).lower()
            blocks[key].append((model.relative_path, window[0][0]))

    for key, hits in blocks.items():
        distinct_files = sorted({path for path, _line in hits})
        if len(distinct_files) < threshold:
            continue
        path, line = hits[0]
        yield make_suggestion(
            MAC_MISSING_ABSTRACTION,
            f"An identical {window_size}-line SQL block appears in "
            f"{len(distinct_files)} models ({', '.join(distinct_files[:5])}"
            + (" ..." if len(distinct_files) > 5 else "")
            + ").",
            file=path,
            line=line,
            evidence=key[:200],
            remediation=(
                "Extract the block. "
                "Use a macro for shared expressions or column lists. "
                "Use an ephemeral model for a self-contained query over "
                "`ref()` calls, so the shared step stays in the DAG."
            ),
            effort=Effort.MEDIUM,
            repeated_in=distinct_files,
        )


# =============================================================================
# Placement
# =============================================================================


@rule(
    MAC_IN_MODELS_DIR,
    "Macro defined inside the models directory",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "dbt discovers macros from `macro-paths`, not from model directories. "
        "A macro in a model file may not be found by dbt and is easy to "
        "define twice."
    ),
)
def macro_in_models(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    for match in re.finditer(
        r"\{%-?\s*macro\s+([A-Za-z_]\w*)", model.raw, re.IGNORECASE
    ):
        yield make_suggestion(
            MAC_IN_MODELS_DIR,
            f"`{match.group(1)}` is defined inside the models directory, "
            "outside the configured `macro-paths`.",
            file=model.relative_path,
            **span(model.raw, match.start(1), match.end(1)),
            evidence=match.group(0).strip(),
            remediation=(
                f"Move it to `macros/{match.group(1)}.sql`. "
                "Keep model files to the query they produce."
            ),
            effort=Effort.LOW,
        )


@rule(
    MAC_NAME_MISMATCH,
    "Macro filename does not match macro name",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A file named for its macro lets readers navigate from a call site "
        "to the definition without grepping."
    ),
)
def name_mismatch(project: ProjectContext) -> Iterator[Suggestion]:
    for macro_file in project.macros:
        if len(macro_file.macros) != 1:
            continue
        macro = macro_file.macros[0]
        stem = macro_file.path.stem
        if stem == macro["name"]:
            continue
        yield make_suggestion(
            MAC_NAME_MISMATCH,
            f"`{macro_file.path.name}` contains `{macro['name']}`, "
            "so callers cannot find the macro by its file name.",
            file=macro_file.relative_path,
            **span(macro_file.raw, macro["start"], macro["end"]),
            evidence=f"{macro_file.path.name} -> {macro['name']}()",
            remediation=f"Rename the file to `{macro['name']}.sql`.",
            effort=Effort.LOW,
        )
