"""
TST -- testing and constraint coverage.

The key-test vocabulary and the composite-key handling here mirror
``dbt_validation.yaml.validator`` deliberately. That module already solved two
problems this pack would otherwise re-introduce:

1. A primary key can be declared at *model* level (for composite keys) rather
   than on a column, via ``column_name`` / ``column_names`` / ``fk_column_name``
   / ``fk_column_names``. A column-only scan reports every composite key as
   untested.
2. dbt 1.10.5+ nests test arguments under an ``arguments:`` key, so the older
   flat lookup silently stops matching.

Both are handled in ``_model_level_key_covers``. The vocabulary is duplicated
rather than imported because the hook is a separate installable package; the
constants are stable and short, and coupling the audit to the hook's import path
would make the audit unrunnable wherever the hook is not installed.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "TST"

TST_NO_TESTS_AT_ALL = "TST001"
TST_NO_KEY_TEST = "TST002"
TST_DIM_NO_PK = "TST003"
TST_FACT_NO_FK = "TST004"
TST_PREFER_CONSTRAINTS = "TST005"
TST_COVERAGE = "TST006"
TST_SINGULAR_AS_GENERIC = "TST007"
TST_NO_STORE_FAILURES = "TST008"
TST_SNAPSHOT_CONFIG = "TST009"
TST_ORPHAN_MODEL = "TST010"

PRIMARY_KEY_TESTS = ("dbt_constraints.primary_key", "primary_key")
UNIQUE_KEY_TESTS = ("dbt_constraints.unique_key", "unique_key", "unique")
FOREIGN_KEY_TESTS = ("dbt_constraints.foreign_key", "foreign_key", "relationships")
KEY_CONSTRAINT_TESTS = PRIMARY_KEY_TESTS + UNIQUE_KEY_TESTS + FOREIGN_KEY_TESTS

KEY_COLUMN_PATTERN = re.compile(r"(.*_id|.*_key|id|.*_sk|fk_.*|.*_fk)$", re.IGNORECASE)
DIM_PATTERN = re.compile(r"^(dim|dimension)[_]", re.IGNORECASE)
FACT_PATTERN = re.compile(r"^(fct|fact)[_]", re.IGNORECASE)


def _test_name(test: Any) -> str | None:
    if isinstance(test, str):
        return test
    if isinstance(test, dict) and test:
        return str(next(iter(test)))
    return None


def _tests_of(node: dict[str, Any]) -> list[Any]:
    """Both spellings; dbt accepts ``tests:`` and ``data_tests:``."""
    return list(node.get("tests") or node.get("data_tests") or [])


def _column_has_key_test(column: dict[str, Any]) -> bool:
    has_unique = has_not_null = False
    for test in _tests_of(column):
        name = _test_name(test)
        if name is None:
            continue
        if name in PRIMARY_KEY_TESTS or name in (
            "dbt_constraints.unique_key",
            "unique_key",
        ):
            return True
        if name in FOREIGN_KEY_TESTS:
            return True
        if name == "unique":
            has_unique = True
        elif name == "not_null":
            has_not_null = True
    return has_unique and has_not_null


def _model_level_key_covers(model_def: dict[str, Any], column_name: str) -> bool:
    """Whether a model-level key test references this column (composite keys)."""
    for test in _tests_of(model_def):
        if not isinstance(test, dict) or not test:
            continue
        name = str(next(iter(test)))
        if name not in KEY_CONSTRAINT_TESTS:
            continue
        config = test.get(name)
        if not isinstance(config, dict):
            continue
        # dbt 1.10.5+ wraps test args in `arguments:`.
        if "arguments" in config and isinstance(config["arguments"], dict):
            config = config["arguments"]
        for single in ("column_name", "fk_column_name"):
            if str(config.get(single, "")).lower() == column_name.lower():
                return True
        for multi in ("column_names", "fk_column_names"):
            values = config.get(multi) or []
            if isinstance(values, list) and column_name.lower() in [
                str(v).lower() for v in values
            ]:
                return True
    return False


def _has_any_key_test(model_def: dict[str, Any]) -> bool:
    """Whether the model has a PK/UK anywhere -- column level or model level."""
    for test in _tests_of(model_def):
        name = _test_name(test)
        if name in PRIMARY_KEY_TESTS or name in UNIQUE_KEY_TESTS:
            return True
    for column in model_def.get("columns") or []:
        if isinstance(column, dict) and _column_has_key_test(column):
            return True
    return False


# =============================================================================
# Coverage
# =============================================================================


@rule(
    TST_NO_TESTS_AT_ALL,
    "Project defines no tests",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "Without tests, a build succeeding says only that the SQL parsed. Nothing "
        "asserts the data is correct, so a silent upstream change ships unnoticed."
    ),
)
def no_tests_at_all(project: ProjectContext) -> Iterator[Finding]:
    if project.model_count == 0:
        return
    yaml_tests = sum(
        len(_tests_of(model_def))
        + sum(
            len(_tests_of(c))
            for c in (model_def.get("columns") or [])
            if isinstance(c, dict)
        )
        for model_def in project.schema_models.values()
    )
    if yaml_tests or project.singular_tests:
        return
    yield make_finding(
        TST_NO_TESTS_AT_ALL,
        f"Project has {project.model_count} models and no tests of any kind.",
        file="models/",
        evidence="no tests in schema YAML; no files under tests/",
        remediation=(
            "Start with primary keys, which catch the most damaging class of bug "
            "(unexpected fan-out from a join):\n\n"
            "```yaml\n"
            "models:\n"
            "  - name: dim_customers\n"
            "    columns:\n"
            "      - name: customer_id\n"
            "        tests:\n"
            "          - dbt_constraints.primary_key\n"
            "```\n\n"
            "Then add foreign keys from facts to dimensions. Run with `dbt build`, not "
            "`dbt run`, so tests execute as part of the build."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    TST_NO_KEY_TEST,
    "Model has no primary or unique key test",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "A key test is the cheapest guard against the most common dbt defect: a join "
        "that fans out and silently multiplies rows. Nothing else catches it."
    ),
)
def no_key_test(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    model_def = project.schema_def(model.name)
    if not model_def:
        return  # TST010 reports the missing YAML entry itself
    if _has_any_key_test(model_def):
        return
    # Staging passthroughs inherit their grain from the source; still worth a
    # test, but a recommendation rather than a warning.
    severity = Severity.RECOMMENDATION if model.layer == "bronze" else Severity.WARNING
    candidates = [
        str(c.get("name"))
        for c in (model_def.get("columns") or [])
        if isinstance(c, dict) and KEY_COLUMN_PATTERN.fullmatch(str(c.get("name", "")))
    ]
    suggestion = candidates[0] if candidates else "<key_column>"
    yield make_finding(
        TST_NO_KEY_TEST,
        "Model has no primary-key or unique-key test, so nothing asserts its grain.",
        severity=severity,
        file=model.relative_path,
        evidence=f"schema entry in {project.schema_sources.get(model.name, 'schema yml')}",
        remediation=(
            "Add a key test on the column that defines one row:\n\n"
            "```yaml\n"
            f"  - name: {model.name}\n"
            "    columns:\n"
            f"      - name: {suggestion}\n"
            "        tests:\n"
            "          - dbt_constraints.primary_key\n"
            "```\n\n"
            "For a composite grain, declare it at model level with "
            "`column_names: [col_a, col_b]`."
        ),
        effort=Effort.LOW,
        candidate_columns=candidates,
    )


@rule(
    TST_DIM_NO_PK,
    "Dimension without a dbt_constraints primary key",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "dbt_constraints creates a real Snowflake constraint, which documents the grain "
        "in database metadata, is visible to BI tools, and lets the optimiser use it."
    ),
)
def dim_no_pk(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not DIM_PATTERN.match(model.name):
        return
    model_def = project.schema_def(model.name)
    if not model_def:
        return
    declared = {
        _test_name(t)
        for t in _tests_of(model_def)
        + [
            t
            for c in (model_def.get("columns") or [])
            if isinstance(c, dict)
            for t in _tests_of(c)
        ]
    }
    if "dbt_constraints.primary_key" in declared:
        return
    if declared & set(PRIMARY_KEY_TESTS) or {"unique", "not_null"} <= declared:
        yield make_finding(
            TST_DIM_NO_PK,
            "Dimension has a uniqueness test but not `dbt_constraints.primary_key`, so "
            "no constraint is created in Snowflake.",
            severity=Severity.RECOMMENDATION,
            file=model.relative_path,
            evidence=f"tests present: {', '.join(sorted(n for n in declared if n))}",
            remediation=(
                "Swap the `unique` + `not_null` pair for "
                "`dbt_constraints.primary_key`. It performs the same validation and "
                "additionally creates the database constraint."
            ),
            effort=Effort.LOW,
        )
        return
    yield make_finding(
        TST_DIM_NO_PK,
        "Dimension has no primary-key test at all.",
        file=model.relative_path,
        evidence=f"tests present: {', '.join(sorted(n for n in declared if n)) or 'none'}",
        remediation=(
            "Add `dbt_constraints.primary_key` on the dimension's surrogate or natural "
            "key. Facts joining to this dimension depend on that key being unique."
        ),
        effort=Effort.LOW,
    )


@rule(
    TST_FACT_NO_FK,
    "Fact table without foreign-key tests",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "An untested foreign key is how orphaned facts reach a dashboard: rows that "
        "join to nothing, quietly dropped by an inner join or shown as blank."
    ),
)
def fact_no_fk(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not FACT_PATTERN.match(model.name):
        return
    model_def = project.schema_def(model.name)
    if not model_def:
        return

    columns = [c for c in (model_def.get("columns") or []) if isinstance(c, dict)]
    key_columns = [
        str(c.get("name"))
        for c in columns
        if KEY_COLUMN_PATTERN.fullmatch(str(c.get("name", "")))
    ]
    if not key_columns:
        return

    untested: list[str] = []
    for column in columns:
        name = str(column.get("name", ""))
        if name not in key_columns:
            continue
        has_fk = any(_test_name(t) in FOREIGN_KEY_TESTS for t in _tests_of(column))
        is_pk = any(_test_name(t) in PRIMARY_KEY_TESTS for t in _tests_of(column))
        if has_fk or is_pk or _model_level_key_covers(model_def, name):
            continue
        untested.append(name)

    if not untested:
        return
    yield make_finding(
        TST_FACT_NO_FK,
        f"Fact table has key column(s) with no foreign-key test: {', '.join(untested)}.",
        file=model.relative_path,
        evidence=f"untested key columns: {', '.join(untested)}",
        remediation=(
            "Add a foreign-key test per dimension reference:\n\n"
            "```yaml\n"
            f"      - name: {untested[0]}\n"
            "        tests:\n"
            "          - dbt_constraints.foreign_key:\n"
            "              pk_table_name: ref('dim_customers')\n"
            "              pk_column_name: customer_id\n"
            "```\n\n"
            "If unmatched rows are expected, resolve them to a ghost key (-1) in the "
            "model so the relationship still holds."
        ),
        effort=Effort.MEDIUM,
        untested_columns=untested,
    )


@rule(
    TST_PREFER_CONSTRAINTS,
    "Built-in tests where dbt_constraints would enforce the rule",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "unique + not_null validates during a run; dbt_constraints additionally creates "
        "the constraint in Snowflake, so the rule is documented in metadata and "
        "available to the optimiser and to BI tools."
    ),
)
def prefer_constraints(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    model_def = project.schema_def(model.name)
    for column in model_def.get("columns") or []:
        if not isinstance(column, dict):
            continue
        names = {_test_name(t) for t in _tests_of(column)}
        column_name = str(column.get("name", ""))
        if {"unique", "not_null"} <= names:
            yield make_finding(
                TST_PREFER_CONSTRAINTS,
                f"Column `{column_name}` uses `unique` + `not_null` where "
                "`dbt_constraints.primary_key` would also create a database constraint.",
                file=model.relative_path,
                evidence=f"{column_name}: unique + not_null",
                remediation=(
                    f"Replace both tests on `{column_name}` with a single "
                    "`- dbt_constraints.primary_key`."
                ),
                effort=Effort.LOW,
                column=column_name,
            )
        elif "relationships" in names:
            yield make_finding(
                TST_PREFER_CONSTRAINTS,
                f"Column `{column_name}` uses `relationships` where "
                "`dbt_constraints.foreign_key` would also create the constraint.",
                file=model.relative_path,
                evidence=f"{column_name}: relationships",
                remediation=(
                    "Switch to `dbt_constraints.foreign_key` with `pk_table_name` and "
                    "`pk_column_name`."
                ),
                effort=Effort.LOW,
                column=column_name,
            )


@rule(
    TST_COVERAGE,
    "Test coverage below threshold",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale=(
        "Coverage is a blunt measure, but a project where most models assert nothing "
        "about their grain has no early warning system."
    ),
)
def coverage(project: ProjectContext) -> Iterator[Finding]:
    if project.model_count < 5:
        return
    tested = sum(
        1
        for model in project.models
        if _has_any_key_test(project.schema_def(model.name))
    )
    ratio = tested / project.model_count
    if ratio >= 0.6:
        return
    yield make_finding(
        TST_COVERAGE,
        f"Only {tested} of {project.model_count} models ({ratio:.0%}) have a key test.",
        file="models/",
        evidence=f"{tested}/{project.model_count} models with PK/UK tests",
        remediation=(
            "Work outward from the gold layer, where errors are most visible to "
            "consumers: add `dbt_constraints.primary_key` to every dimension and fact "
            "first, then foreign keys, then work back through silver. Enable "
            "`+store_failures: true` so failures are inspectable rather than just "
            "counted."
        ),
        effort=Effort.HIGH,
        tested=tested,
        total=project.model_count,
    )


@rule(
    TST_ORPHAN_MODEL,
    "Model or schema entry without its counterpart",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    rationale=(
        "A model with no schema entry cannot be tested or documented. A schema entry "
        "with no model produces a parse error or silently describes nothing."
    ),
)
def orphan_model(project: ProjectContext) -> Iterator[Finding]:
    model_names = {model.name for model in project.models}

    for model in project.models:
        if model.name in project.schema_models:
            continue
        yield make_finding(
            TST_ORPHAN_MODEL,
            "Model has no entry in any schema YAML, so it has no tests and no documentation.",
            file=model.relative_path,
            evidence=f"{model.name} absent from all schema files",
            remediation=(
                "Add it to the `_models.yml` beside it with a description, its "
                "columns, and at minimum a primary-key test."
            ),
            effort=Effort.LOW,
        )

    for name, source_file in project.schema_sources.items():
        if name in model_names:
            continue
        yield make_finding(
            TST_ORPHAN_MODEL,
            f"Schema YAML declares model `{name}`, but no matching model file exists.",
            severity=Severity.ERROR,
            file=source_file,
            evidence=f"{name} declared in {source_file}",
            remediation=(
                "Delete the stale entry, or restore the model file if it was removed "
                "by mistake. dbt raises an error for a documented model it cannot find."
            ),
            effort=Effort.LOW,
        )


@rule(
    TST_NO_STORE_FAILURES,
    "store_failures not enabled",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Without store_failures a failing test reports a row count. With it, the "
        "offending rows land in a table you can query, which is the difference between "
        "knowing something broke and knowing what broke."
    ),
)
def no_store_failures(project: ProjectContext) -> Iterator[Finding]:
    tests_config = project.project_yml.get("tests") or {}
    if _nested_flag(tests_config, "+store_failures") or _nested_flag(
        tests_config, "store_failures"
    ):
        return
    if project.model_count == 0:
        return
    yield make_finding(
        TST_NO_STORE_FAILURES,
        "`store_failures` is not enabled, so test failures report only a count.",
        file="dbt_project.yml",
        evidence="no +store_failures under tests:",
        remediation=(
            "Enable it so failures are inspectable:\n\n"
            "```yaml\n"
            "tests:\n"
            f"  {project.name}:\n"
            "    +store_failures: true\n"
            "    +schema: test_failures\n"
            "```"
        ),
        effort=Effort.LOW,
    )


def _nested_flag(node: Any, key: str) -> bool:
    """Whether a key is set truthy anywhere in a nested config tree."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key and v:
                return True
            if _nested_flag(v, key):
                return True
    return False


@rule(
    TST_SINGULAR_AS_GENERIC,
    "Singular test that should be a generic test",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "A singular test applies to one place. The same assertion written as a generic "
        "test can be attached to every model that needs it, and shows up in the schema "
        "YAML where reviewers look."
    ),
)
def singular_as_generic(project: ProjectContext) -> Iterator[Finding]:
    for path, raw in project.singular_tests:
        if "{% test" in raw or "{%- test" in raw:
            continue  # already a generic test definition
        body = raw.strip()
        # A single-table null/uniqueness check is exactly what a generic test does.
        simple = (
            len(re.findall(r"\bfrom\b", body, re.IGNORECASE)) == 1
            and len(re.findall(r"\bjoin\b", body, re.IGNORECASE)) == 0
            and re.search(
                r"\bis\s+null\b|\bcount\s*\(\s*\*\s*\)|\bhaving\b", body, re.IGNORECASE
            )
        )
        if not simple:
            continue
        try:
            relative = str(path.relative_to(project.root))
        except ValueError:
            relative = str(path)
        yield make_finding(
            TST_SINGULAR_AS_GENERIC,
            f"`{path.name}` is a single-table null or count assertion, which the "
            "built-in generic tests already express.",
            file=relative,
            evidence=re.sub(r"\s+", " ", body)[:160],
            remediation=(
                "Replace it with a generic test in schema YAML (`not_null`, `unique`, "
                "`accepted_values`, `dbt_utils.accepted_range`). If the logic is "
                "genuinely reusable but not built in, define it as "
                "`tests/generic/<name>.sql` wrapped in `{% test %}` so it can be "
                "attached by name."
            ),
            effort=Effort.LOW,
        )


@rule(
    TST_SNAPSHOT_CONFIG,
    "Snapshot configuration incomplete",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "A snapshot with a missing strategy key silently fails to track changes, and "
        "the history gap is not recoverable after the fact."
    ),
)
def snapshot_config(project: ProjectContext) -> Iterator[Finding]:
    for path, raw in project.snapshot_files:
        if "{% snapshot" not in raw and "{%- snapshot" not in raw:
            continue
        try:
            relative = str(path.relative_to(project.root))
        except ValueError:
            relative = str(path)

        missing: list[str] = []
        if not re.search(r"\bunique_key\s*=", raw):
            missing.append("unique_key")
        strategy_match = re.search(r"\bstrategy\s*=\s*['\"](\w+)['\"]", raw)
        if not strategy_match:
            missing.append("strategy")
        else:
            strategy = strategy_match.group(1).lower()
            if strategy == "timestamp" and not re.search(r"\bupdated_at\s*=", raw):
                missing.append("updated_at (required by the timestamp strategy)")
            if strategy == "check" and not re.search(r"\bcheck_cols\s*=", raw):
                missing.append("check_cols (required by the check strategy)")
        if not missing:
            continue
        yield make_finding(
            TST_SNAPSHOT_CONFIG,
            f"Snapshot `{path.stem}` is missing required config: {', '.join(missing)}.",
            file=relative,
            evidence=", ".join(missing),
            remediation=(
                "Complete the snapshot config:\n\n"
                "```sql\n"
                "{{ config(\n"
                "    unique_key='customer_id',\n"
                "    strategy='timestamp',\n"
                "    updated_at='updated_at',\n"
                "    invalidate_hard_deletes=True\n"
                ") }}\n"
                "```\n\n"
                "Prefer the timestamp strategy when the source has a reliable "
                "modification timestamp; use `check` with an explicit `check_cols` "
                "list only when it does not."
            ),
            effort=Effort.LOW,
        )
