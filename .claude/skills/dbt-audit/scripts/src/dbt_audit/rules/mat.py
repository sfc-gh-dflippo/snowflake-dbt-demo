"""
MAT -- materialization fitness.

Whether each model's materialization matches how it is actually used. Most of
these need the dependency graph (how many models reference this one), so they
declare ``requires_manifest=True`` and are reported as skipped rather than
passing when no manifest is available.

Mixed tiers. Fan-out, pass-through chains and clustering are UNIVERSAL --
they are about cost and correctness. Redundant config and missing folder defaults
are ARCHITECTURE, because they describe project conventions a converted project
never adopted.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbt_audit.core.base import (
    Effort,
    Finding,
    Scope,
    Severity,
    Tier,
    make_finding,
    rule,
)
from dbt_audit.core.sqlutil import extract_ctes, significant_lines

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "MAT"

MAT_EPHEMERAL_FANOUT = "MAT001"
MAT_SINGLE_USE_MODEL = "MAT002"
MAT_PASSTHROUGH_CHAIN = "MAT003"
MAT_CLUSTERING = "MAT004"
MAT_VIEW_COMPLEXITY = "MAT005"
MAT_REDUNDANT_CONFIG = "MAT006"
MAT_NO_FOLDER_DEFAULT = "MAT007"
MAT_PYTHON_MODEL = "MAT008"

FACT_NAME_PATTERN = re.compile(r"^(fct|fact)_", re.IGNORECASE)
DIM_NAME_PATTERN = re.compile(r"^(dim|dimension)_", re.IGNORECASE)


@rule(
    MAT_EPHEMERAL_FANOUT,
    "Ephemeral or view model referenced by many models",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    requires_manifest=True,
    rationale=(
        "An ephemeral model is inlined into every consumer, so its logic is executed "
        "once per consumer. Past a few consumers, materializing it as a table computes "
        "the work once and lets Snowflake reuse the result."
    ),
)
def ephemeral_fanout(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    materialization = model.materialization
    if materialization not in ("ephemeral", "view"):
        return
    children = project.graph.child_names(model.name)
    model_children = [c for c in children if project.model_by_name(c) is not None]
    threshold = project.config.ephemeral_fanout_threshold
    if len(model_children) < threshold:
        return
    yield make_finding(
        MAT_EPHEMERAL_FANOUT,
        f"`{materialization}` model is referenced by {len(model_children)} models "
        f"({', '.join(sorted(model_children)[:5])}"
        + (" ..." if len(model_children) > 5 else "")
        + f"), so its logic runs {len(model_children)} times per build.",
        file=model.relative_path,
        evidence=f"materialized='{materialization}', {len(model_children)} downstream models",
        remediation=(
            "Change to `materialized='table'` so the work happens once and every "
            "consumer reads the stored result. Ephemeral is the right choice for logic "
            "with one or two consumers, where avoiding a relation is worth recomputing."
        ),
        effort=Effort.LOW,
        downstream=sorted(model_children),
    )


@rule(
    MAT_SINGLE_USE_MODEL,
    "Intermediate model with a single consumer",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    requires_manifest=True,
    rationale=(
        "A model exists so more than one thing can use it, or so it can be tested and "
        "documented as a unit. An intermediate model with one consumer and no tests is "
        "usually a CTE that was promoted to a file for no gain."
    ),
)
def single_use_model(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.layer not in ("silver", ""):
        return
    if model.is_python:
        return
    children = [
        c for c in project.graph.child_names(model.name) if project.model_by_name(c)
    ]
    if len(children) != 1:
        return
    # A tested, documented model is a deliberate contract even with one consumer.
    schema_def = project.schema_def(model.name)
    if schema_def.get("description") and (
        schema_def.get("tests")
        or schema_def.get("data_tests")
        or schema_def.get("columns")
    ):
        return
    yield make_finding(
        MAT_SINGLE_USE_MODEL,
        f"Model is referenced only by `{children[0]}` and has no tests or description, "
        "so it adds a DAG node without adding a contract.",
        file=model.relative_path,
        evidence=f"1 consumer ({children[0]}), no tests or description",
        remediation=(
            f"Either fold this logic into `{children[0]}` as a named CTE, or -- if the "
            "step deserves to be a model -- give it a description and a primary-key "
            "test so it functions as a real interface. Making it `ephemeral` is a "
            "middle path: it keeps the name and the DAG edge without creating a "
            "relation."
        ),
        effort=Effort.MEDIUM,
        consumer=children[0],
    )


@rule(
    MAT_PASSTHROUGH_CHAIN,
    "Chain of single-consumer pass-through models",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.WARNING,
    requires_manifest=True,
    rationale=(
        "A linear chain where each model feeds exactly one next model is one "
        "transformation split across many files. It is the signature of "
        "one-model-per-ETL-transformation generation, and it multiplies relations, "
        "build time and review surface for a single logical step."
    ),
)
def passthrough_chain(project: ProjectContext) -> Iterator[Finding]:
    threshold = project.config.passthrough_chain_threshold
    graph = project.graph
    model_names = {m.name for m in project.models}

    def single_child(name: str) -> str | None:
        children = [c for c in graph.child_names(name) if c in model_names]
        return children[0] if len(children) == 1 else None

    visited: set[str] = set()
    for model in project.models:
        if model.name in visited:
            continue
        # Only start from a chain head: no model parent, or a parent that fans out.
        parents = [p for p in graph.parent_names(model.name) if p in model_names]
        if len(parents) == 1 and single_child(parents[0]) == model.name:
            continue

        chain = [model.name]
        current = model.name
        while True:
            nxt = single_child(current)
            if nxt is None or nxt in chain:
                break
            parents_of_next = [p for p in graph.parent_names(nxt) if p in model_names]
            if len(parents_of_next) != 1:
                break
            chain.append(nxt)
            current = nxt

        if len(chain) < threshold:
            continue
        visited.update(chain)
        head = project.model_by_name(chain[0])
        yield make_finding(
            MAT_PASSTHROUGH_CHAIN,
            f"{len(chain)} models form a linear chain where each feeds exactly one "
            f"successor: {' -> '.join(chain)}. That is one transformation spread across "
            f"{len(chain)} files.",
            file=head.relative_path if head else "",
            evidence=" -> ".join(chain),
            remediation=(
                "Collapse the chain into a single model with one CTE per step. The "
                "steps keep their names and remain individually readable, but there is "
                "one relation, one set of tests, and one node to build. Split it again "
                "only where a step genuinely gains a second consumer."
            ),
            effort=Effort.HIGH,
            chain=chain,
        )


@rule(
    MAT_CLUSTERING,
    "Clustering key missing or over-specified",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Snowflake prunes micro-partitions using the clustering key. Large fact tables "
        "without one scan more than they need; more than about four columns dilutes "
        "clustering and raises maintenance cost."
    ),
)
def clustering(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.materialization not in ("table", "incremental"):
        return
    cluster_by = model.effective_config.get("cluster_by")
    maximum = project.config.max_cluster_columns

    if cluster_by:
        columns = cluster_by if isinstance(cluster_by, list) else [cluster_by]
        if len(columns) > maximum:
            yield make_finding(
                MAT_CLUSTERING,
                f"`cluster_by` specifies {len(columns)} columns; beyond {maximum} the "
                "clustering depth per column degrades and reclustering costs rise.",
                severity=Severity.WARNING,
                file=model.relative_path,
                evidence=f"cluster_by={columns}",
                remediation=(
                    f"Reduce to at most {maximum} columns, ordered from lowest to "
                    "highest cardinality, and choose them from the predicates queries "
                    "actually filter on. Verify with "
                    "`select system$clustering_information('<table>', '(col1, col2)')`."
                ),
                effort=Effort.LOW,
            )
        return

    if FACT_NAME_PATTERN.match(model.name) or model.is_incremental:
        yield make_finding(
            MAT_CLUSTERING,
            "Fact or incremental table has no `cluster_by`, so queries filtering on "
            "date or key columns cannot prune micro-partitions.",
            file=model.relative_path,
            evidence=f"materialized='{model.materialization}', no cluster_by",
            remediation=(
                "Add a clustering key matching the dominant filter pattern, typically "
                "the date column first:\n\n"
                "```sql\n"
                "{{ config(materialized='incremental', cluster_by=['order_date']) }}\n"
                "```\n\n"
                "Clustering only pays for itself above roughly a terabyte or on tables "
                "queried with selective filters -- check table size before adding it."
            ),
            effort=Effort.LOW,
        )


@rule(
    MAT_VIEW_COMPLEXITY,
    "Complex logic materialized as a view",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    requires_manifest=True,
    rationale=(
        "A view re-executes its full logic on every query. For a heavily-referenced "
        "model with substantial transformation, that cost is paid by every consumer, "
        "every time."
    ),
)
def view_complexity(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.materialization != "view" or model.is_python:
        return
    cte_count = len(extract_ctes(model.stripped))
    lines = significant_lines(model.stripped)
    children = [
        c for c in project.graph.child_names(model.name) if project.model_by_name(c)
    ]
    if cte_count < 3 and lines < 60:
        return
    if len(children) < 2:
        return
    yield make_finding(
        MAT_VIEW_COMPLEXITY,
        f"View contains {cte_count} CTEs across {lines} lines and is referenced by "
        f"{len(children)} models, so the full transformation re-runs for each consumer.",
        file=model.relative_path,
        evidence=f"materialized='view', {cte_count} CTEs, {len(children)} consumers",
        remediation=(
            "Materialize as `table` so the transformation runs once per build, or as "
            "`incremental` if it is large and rows arrive over time. Keep `view` for "
            "thin projections where freshness matters more than query cost."
        ),
        effort=Effort.LOW,
    )


@rule(
    MAT_PYTHON_MODEL,
    "Python model configuration issue",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.WARNING,
    rationale=(
        "Python models run on Snowpark and cost more to execute and debug than SQL. "
        "They are worth it for ML and library-dependent work, not for transformations "
        "SQL expresses directly."
    ),
)
def python_model(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if not model.is_python:
        return
    if "packages" not in model.raw and re.search(r"\bimport\s+\w+", model.raw):
        yield make_finding(
            MAT_PYTHON_MODEL,
            "Python model imports libraries but declares no `packages` list, so the "
            "imports may not resolve in Snowpark.",
            file=model.relative_path,
            evidence="import statement present; no packages= in dbt.config",
            remediation=(
                "Declare the dependencies explicitly:\n\n"
                "```python\n"
                "def model(dbt, session):\n"
                "    dbt.config(materialized='table', packages=['pandas', 'scikit-learn'])\n"
                "```"
            ),
            effort=Effort.LOW,
        )

    analytical = re.search(
        r"\b(sklearn|scikit|scipy|statsmodels|xgboost|lightgbm|prophet|torch|"
        r"tensorflow|numpy\.linalg)\b",
        model.raw,
    )
    if not analytical:
        yield make_finding(
            MAT_PYTHON_MODEL,
            "Python model does not use any analytical or ML library, so the "
            "transformation is likely expressible in SQL at lower cost.",
            severity=Severity.RECOMMENDATION,
            file=model.relative_path,
            evidence="no ML/statistical library imported",
            remediation=(
                "Rewrite as a SQL model unless the Python is doing something SQL "
                "cannot -- model training or scoring, a statistical routine, or a "
                "library-specific parser. SQL models are cheaper to run, easier to "
                "test, and visible in the compiled artifact."
            ),
            effort=Effort.MEDIUM,
        )


# =============================================================================
# Configuration conventions (ARCHITECTURE tier -- suppressed for migrations)
# =============================================================================


@rule(
    MAT_REDUNDANT_CONFIG,
    "Model config repeats the folder default",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Restating an inherited default adds a line that must be kept in sync. When "
        "the folder default changes, models that repeated it silently keep the old "
        "value."
    ),
)
def redundant_config(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    redundant = [
        key
        for key, value in model.own_config.items()
        if key in model.folder_config and model.folder_config[key] == value
    ]
    if not redundant:
        return
    yield make_finding(
        MAT_REDUNDANT_CONFIG,
        f"Model config restates value(s) already inherited from `dbt_project.yml`: "
        f"{', '.join(sorted(redundant))}.",
        file=model.relative_path,
        evidence=", ".join(f"{k}={model.own_config[k]!r}" for k in sorted(redundant)),
        remediation=(
            "Remove the redundant keys from the model's `config()` block and let the "
            "folder default apply. Keep model-level config only where it genuinely "
            "overrides the default."
        ),
        effort=Effort.LOW,
    )


@rule(
    MAT_NO_FOLDER_DEFAULT,
    "Layer folder has no materialization default",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Setting materialization per layer in dbt_project.yml states the architecture "
        "in one reviewable place, instead of leaving it implicit across many files."
    ),
)
def no_folder_default(project: ProjectContext) -> Iterator[Finding]:
    layers_present = {m.segments[0] for m in project.models if m.segments}
    if not layers_present:
        return

    models_tree = project.project_yml.get("models") or {}
    node = models_tree.get(project.name)
    if not isinstance(node, dict):
        candidates = [
            v
            for k, v in models_tree.items()
            if not k.startswith("+") and isinstance(v, dict)
        ]
        node = candidates[0] if len(candidates) == 1 else {}

    unconfigured = sorted(
        layer
        for layer in layers_present
        if not (
            isinstance(node.get(layer), dict)
            and any(k.startswith("+materialized") for k in node[layer])
        )
        and not any(k.startswith("+materialized") for k in node)
    )
    if not unconfigured:
        return
    yield make_finding(
        MAT_NO_FOLDER_DEFAULT,
        f"Folder(s) {', '.join(unconfigured)} have no `+materialized` default in "
        "`dbt_project.yml`, so materialization is decided model by model.",
        file="dbt_project.yml",
        evidence=f"no +materialized for: {', '.join(unconfigured)}",
        remediation=(
            "Declare the intent per layer:\n\n"
            "```yaml\n"
            "models:\n"
            f"  {project.name}:\n"
            "    bronze:\n"
            "      +materialized: ephemeral\n"
            "    silver:\n"
            "      +materialized: ephemeral\n"
            "    gold:\n"
            "      +materialized: table\n"
            "```\n\n"
            "Individual models then override only where they differ."
        ),
        effort=Effort.LOW,
    )
