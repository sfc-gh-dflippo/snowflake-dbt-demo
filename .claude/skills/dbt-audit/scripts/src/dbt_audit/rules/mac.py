"""
MAC -- macro discipline, in both directions.

Over-use and under-use are both failures, and they need opposite remedies, so
this pack measures both. Over-abstraction shows up as macros that wrap a single
expression, macros called from exactly one place, macros that emit whole SELECT
statements, and models whose bodies are mostly Jinja. Under-abstraction shows up
as the same multi-line SQL repeated across several models.

Note: this repo's skills contain no prescriptive macro guidance -- the thresholds
here are authored for this audit rather than extracted from existing docs, which
is why they are all configurable in ``.dbt-audit.yml``.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule
from dbt_audit.core.sqlutil import (
    extract_macro_calls,
    find_line_number,
    significant_lines,
    strip_all,
)

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "MAC"

MAC_RATIO = "MAC001"
MAC_SINGLE_CALLER = "MAC002"
MAC_UNUSED = "MAC003"
MAC_TRIVIAL = "MAC004"
MAC_EMITS_QUERY = "MAC005"
MAC_HARDCODED_RELATION = "MAC006"
MAC_DEEP_NESTING = "MAC007"
MAC_JINJA_HEAVY = "MAC008"
MAC_REIMPLEMENTS_UTIL = "MAC009"
MAC_MISSING_ABSTRACTION = "MAC010"
MAC_IN_MODELS_DIR = "MAC011"
MAC_NAME_MISMATCH = "MAC012"

#: dbt_utils / dbt_constraints equivalents that teams commonly hand-roll.
UTIL_REIMPLEMENTATIONS: list[tuple[str, str, str]] = [
    (
        r"md5\s*\(\s*concat",
        "dbt_utils.generate_surrogate_key",
        "hand-rolled surrogate key hashing",
    ),
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
    (
        r"sum\s*\(\s*case\s+when.*then\s+1\s+else\s+0\s+end\s*\)",
        "dbt_utils.pivot",
        "hand-rolled pivot",
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
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Macros move logic out of SQL and out of the compiled artifact a reviewer "
        "reads. A project with nearly as many macros as models is usually abstracting "
        "ahead of need, which raises the cost of understanding any single model."
    ),
)
def macro_ratio(project: ProjectContext) -> Iterator[Finding]:
    macro_count = sum(len(f.macros) for f in project.macros)
    model_count = project.model_count
    if model_count == 0 or macro_count == 0:
        return
    ratio = macro_count / model_count
    if ratio < project.config.macro_model_ratio:
        return
    yield make_finding(
        MAC_RATIO,
        f"Project defines {macro_count} macros for {model_count} models "
        f"(ratio {ratio:.2f}), above the {project.config.macro_model_ratio:.2f} "
        "threshold for likely over-abstraction.",
        file="macros/",
        evidence=f"{macro_count} macros / {model_count} models",
        remediation=(
            "Review the macro inventory against the single-caller and trivial-wrapper "
            "findings in this report. Inline anything used once, delete anything "
            "unused, and keep macros for logic that is genuinely parameterised or "
            "repeated. Prefer an ephemeral model over a macro when the shared thing is "
            "a query rather than an expression -- it keeps lineage visible."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    MAC_SINGLE_CALLER,
    "Macro is called from only one place",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "A macro exists to serve more than one caller. With one caller it only adds a "
        "file to open, and the logic is no longer visible where it is used."
    ),
)
def single_caller(project: ProjectContext) -> Iterator[Finding]:
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
            yield make_finding(
                MAC_SINGLE_CALLER,
                f"Macro `{name}` is called from exactly one place ({caller_path}:{caller_line}).",
                file=macro_file.relative_path,
                line=macro["line"],
                evidence=f"{{% macro {name}({', '.join(macro['args'])}) %}}",
                remediation=(
                    f"Inline the body at its single call site in `{caller_path}` and "
                    "delete the macro, so the logic is readable where it is used. Keep "
                    "the macro only if a second caller is imminent."
                ),
                effort=Effort.LOW,
                caller=caller_path,
            )


@rule(
    MAC_UNUSED,
    "Macro is never called",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale="Dead code still has to be read, reviewed and kept compiling.",
)
def unused_macro(project: ProjectContext) -> Iterator[Finding]:
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
            yield make_finding(
                MAC_UNUSED,
                f"Macro `{name}` has no call sites anywhere in the project.",
                file=macro_file.relative_path,
                line=macro["line"],
                evidence=f"{{% macro {name}({', '.join(macro['args'])}) %}}",
                remediation=(
                    "Delete it. If it is invoked dynamically (via `context` lookup or "
                    "from outside this project), add a comment saying so -- otherwise "
                    "the next reader will delete it anyway."
                ),
                effort=Effort.LOW,
            )


@rule(
    MAC_TRIVIAL,
    "Macro wraps a single expression with no logic",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "A macro containing one expression and no branching adds indirection without "
        "encapsulating a decision. The SQL was clearer inline."
    ),
)
def trivial_macro(project: ProjectContext) -> Iterator[Finding]:
    for macro_file in project.macros:
        for macro in macro_file.macros:
            body = macro["body"].strip()
            if not body or LOGIC_MARKERS.search(body):
                continue
            if significant_lines(body) > 2:
                continue
            if len(strip_all(body).strip()) > 120:
                continue
            yield make_finding(
                MAC_TRIVIAL,
                f"Macro `{macro['name']}` wraps a single short expression with no "
                "conditional or loop.",
                file=macro_file.relative_path,
                line=macro["line"],
                evidence=re.sub(r"\s+", " ", body)[:140],
                remediation=(
                    "Inline the expression. A macro earns its indirection when it "
                    "encapsulates a choice (dialect dispatch, conditional logic, a "
                    "loop over columns) or when the expression is long enough that "
                    "naming it genuinely aids reading."
                ),
                effort=Effort.LOW,
            )


@rule(
    MAC_EMITS_QUERY,
    "Macro generates a whole query instead of an expression",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale=(
        "When a macro emits SELECT ... FROM, the model's real logic lives outside the "
        "model file. Reviewers reading the model see a macro call; lineage tools see "
        "whatever the macro happened to interpolate."
    ),
)
def macro_emits_query(project: ProjectContext) -> Iterator[Finding]:
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
            yield make_finding(
                MAC_EMITS_QUERY,
                f"Macro `{macro['name']}` emits a full SELECT ... FROM query, moving "
                "model logic out of the model.",
                file=macro_file.relative_path,
                line=macro["line"],
                evidence=re.sub(r"\s+", " ", body.strip())[:180],
                remediation=(
                    "If the query is shared, make it an ephemeral model instead -- it "
                    "gains a name in the DAG, can be tested, and appears in docs. "
                    "Reserve macros for expressions, predicates and column lists."
                ),
                effort=Effort.MEDIUM,
            )


@rule(
    MAC_HARDCODED_RELATION,
    "Macro hardcodes a relation name",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "A literal relation inside a macro bypasses ref(), so the dependency is "
        "invisible to dbt and the reference does not follow the target environment."
    ),
)
def macro_hardcoded_relation(project: ProjectContext) -> Iterator[Finding]:
    for macro_file in project.macros:
        for macro in macro_file.macros:
            stripped = strip_all(macro["body"])
            for match in RELATION_LITERAL_PATTERN.finditer(stripped):
                reference = match.group(2)
                if reference.lower().startswith(
                    ("information_schema.", "snowflake.", "table.")
                ):
                    continue
                yield make_finding(
                    MAC_HARDCODED_RELATION,
                    f"Macro `{macro['name']}` reads `{reference}` as a literal "
                    "relation rather than taking a ref or relation argument.",
                    file=macro_file.relative_path,
                    line=macro["line"] + find_line_number(stripped, match.start()) - 1,
                    evidence=match.group(0).strip(),
                    remediation=(
                        "Pass the relation in as an argument -- "
                        f"`{{{{ {macro['name']}(ref('the_model')) }}}}` -- so the "
                        "caller's ref() creates the lineage edge and the relation "
                        "resolves per target."
                    ),
                    effort=Effort.MEDIUM,
                )


@rule(
    MAC_DEEP_NESTING,
    "Macro call chain is deeply nested",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale=(
        "Each macro hop is a file a debugger has to open. Three or more hops from a "
        "model to the actual SQL makes compiled output the only practical way to see "
        "what runs."
    ),
)
def deep_nesting(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            MAC_DEEP_NESTING,
            f"Macro `{name}` calls through {levels} further macro level(s): "
            f"{' -> '.join([name, *chain])}.",
            file=path,
            line=int(macro["line"]),
            evidence=" -> ".join([name, *chain]),
            remediation=(
                "Flatten the chain. Collapse thin intermediate macros into their "
                "caller so a reader reaches the SQL in one hop, and keep only the "
                "layers that each encapsulate a distinct decision."
            ),
            effort=Effort.MEDIUM,
            chain=[name, *chain],
        )


@rule(
    MAC_JINJA_HEAVY,
    "Model body is mostly Jinja rather than SQL",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "When a model is mostly macro calls, neither a reviewer nor a data consumer "
        "can tell what it produces without compiling it."
    ),
)
def jinja_heavy(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
    yield make_finding(
        MAC_JINJA_HEAVY,
        f"Roughly {jinja_lines} of {significant_lines(body)} body lines are Jinja, "
        f"with {len(user_calls)} project macro call(s). The SQL this model runs is not "
        "visible in the file.",
        file=model.relative_path,
        evidence=", ".join(sorted({c["name"] for c in user_calls})[:6]),
        remediation=(
            "Bring the core transformation back into SQL and keep macros at the edges "
            "(a shared predicate, a column list, an audit column block). If the "
            "generation is genuinely dynamic, add a comment showing a representative "
            "compiled output so reviewers can read intent without running dbt."
        ),
        effort=Effort.HIGH,
    )


@rule(
    MAC_REIMPLEMENTS_UTIL,
    "Hand-rolled equivalent of a dbt_utils macro",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "dbt_utils implementations are cross-adapter, tested, and understood by other "
        "engineers. A local equivalent has to be maintained and is usually subtly "
        "different on NULLs or types."
    ),
)
def reimplements_util(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.is_python:
        return
    for pattern, replacement, description in UTIL_REIMPLEMENTATIONS:
        match = re.search(pattern, model.stripped, re.IGNORECASE | re.DOTALL)
        if not match:
            continue
        yield make_finding(
            MAC_REIMPLEMENTS_UTIL,
            f"Model contains a {description}; `{replacement}` covers this case.",
            file=model.relative_path,
            line=find_line_number(model.stripped, match.start()),
            evidence=re.sub(r"\s+", " ", match.group(0))[:140],
            remediation=(
                f"Replace with `{{{{ {replacement}(...) }}}}`. It handles NULL and type "
                "edge cases consistently and removes local code to maintain."
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
    severity=Severity.WARNING,
    rationale=(
        "The same block copied into several models means a fix has to be applied "
        "several times, and eventually will not be."
    ),
)
def missing_abstraction(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            MAC_MISSING_ABSTRACTION,
            f"An identical {window_size}-line SQL block appears in "
            f"{len(distinct_files)} models: {', '.join(distinct_files[:5])}"
            + (" ..." if len(distinct_files) > 5 else "")
            + ".",
            file=path,
            line=line,
            evidence=key[:200],
            remediation=(
                "Extract it. Use a macro if it is an expression or column list that "
                "appears in differently-shaped queries; use an ephemeral model if it "
                "is a self-contained query over refs, so the shared step keeps its "
                "place in the DAG."
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
    severity=Severity.WARNING,
    rationale=(
        "dbt discovers macros from macro-paths. One defined inside a model file is "
        "scoped confusingly and easy to define twice."
    ),
)
def macro_in_models(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    for match in re.finditer(
        r"\{%-?\s*macro\s+([A-Za-z_]\w*)", model.raw, re.IGNORECASE
    ):
        yield make_finding(
            MAC_IN_MODELS_DIR,
            f"Macro `{match.group(1)}` is defined inside a model file.",
            file=model.relative_path,
            line=find_line_number(model.raw, match.start()),
            evidence=match.group(0).strip(),
            remediation=(
                f"Move it to `macros/{match.group(1)}.sql`. Keep model files to the "
                "query they produce."
            ),
            effort=Effort.LOW,
        )


@rule(
    MAC_NAME_MISMATCH,
    "Macro file name does not match the macro it defines",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "One macro per file, named for the macro, is how people find a macro from a "
        "call site without grepping."
    ),
)
def name_mismatch(project: ProjectContext) -> Iterator[Finding]:
    for macro_file in project.macros:
        if len(macro_file.macros) != 1:
            continue
        macro = macro_file.macros[0]
        stem = macro_file.path.stem
        if stem == macro["name"]:
            continue
        yield make_finding(
            MAC_NAME_MISMATCH,
            f"File `{macro_file.path.name}` defines a single macro named `{macro['name']}`.",
            file=macro_file.relative_path,
            line=macro["line"],
            evidence=f"{macro_file.path.name} -> {macro['name']}()",
            remediation=f"Rename the file to `{macro['name']}.sql`.",
            effort=Effort.LOW,
        )
