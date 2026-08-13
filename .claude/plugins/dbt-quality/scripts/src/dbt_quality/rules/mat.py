"""
MAT -- materialization fitness.

Whether each model's materialization matches how it is actually used. Most of
these need the dependency graph (how many models reference this one), so they
declare ``requires_manifest=True`` and are reported as skipped rather than
passing when no manifest is available.

Mixed tiers. Fan-out and clustering are UNIVERSAL -- they are about cost and
correctness. Redundant config and missing folder defaults are ARCHITECTURE,
because they describe project conventions a converted project never adopted.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbt_quality.core.base import (
    Effort,
    Kind,
    Level,
    Scope,
    Severity,
    Suggestion,
    Tier,
    make_suggestion,
    plural,
    rule,
)

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "MAT"

MAT_EPHEMERAL_FANOUT = "SSC-PRF-DBTMAT0001"
MAT_SINGLE_USE_MODEL = "SSC-PRF-DBTMAT0002"
MAT_CLUSTERING = "SSC-PRF-DBTMAT0004"
MAT_REDUNDANT_CONFIG = "SSC-EWI-DBTMAT0006"
MAT_NO_FOLDER_DEFAULT = "SSC-EWI-DBTMAT0007"


@rule(
    MAT_EPHEMERAL_FANOUT,
    "Ephemeral or view model with many consumers",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    requires_manifest=True,
    rationale=(
        "An `ephemeral` or `view` model runs its logic once per consumer. "
        "Past a few consumers, a `table` runs the work once and every "
        "consumer reads the stored result."
    ),
)
def ephemeral_fanout(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    materialization = model.materialization
    if materialization not in ("ephemeral", "view"):
        return
    children = project.graph.child_names(model.name)
    model_children = [c for c in children if project.model_by_name(c) is not None]
    threshold = project.config.ephemeral_fanout_threshold
    if len(model_children) < threshold:
        return
    yield make_suggestion(
        MAT_EPHEMERAL_FANOUT,
        f"This `{materialization}` model runs its logic "
        f"{len(model_children)} times per build, once per consumer "
        f"({', '.join(sorted(model_children)[:5])}"
        + (" ..." if len(model_children) > 5 else "")
        + ").",
        file=model.relative_path,
        evidence=f"materialized='{materialization}', {len(model_children)} downstream models",
        remediation=(
            "Change `materialized` to `'table'` so the logic runs once and "
            "each consumer reads the stored result. `ephemeral` works well "
            "with one or two consumers where the transformation is cheap."
        ),
        effort=Effort.LOW,
        downstream=sorted(model_children),
    )


@rule(
    MAT_SINGLE_USE_MODEL,
    "Intermediate model with a single consumer",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    requires_manifest=True,
    rationale=(
        "An intermediate model with one consumer and no tests is usually a "
        "CTE promoted to a file for no gain. A model warrants its own file "
        "when referenced by multiple consumers or when it serves as a "
        "tested, documented interface."
    ),
)
def single_use_model(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
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
    yield make_suggestion(
        MAT_SINGLE_USE_MODEL,
        f"This model is referenced only by `{children[0]}` "
        "and has no tests or description.",
        file=model.relative_path,
        evidence=f"1 consumer ({children[0]}), no tests or description",
        remediation=(
            f"Fold the logic into `{children[0]}` as a named CTE, or add a "
            "description and a primary-key test to define it as an interface. "
            "Use `ephemeral` to preserve the DAG name without creating a relation."
        ),
        effort=Effort.MEDIUM,
        consumer=children[0],
    )


@rule(
    MAT_CLUSTERING,
    "Clustering key over-specified",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.PRF,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Snowflake prunes micro-partitions using the clustering key. "
        "More than about four columns dilutes the benefit and raises "
        "maintenance cost."
    ),
)
def clustering(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.materialization not in ("table", "incremental"):
        return
    cluster_by = model.effective_config.get("cluster_by")
    maximum = project.config.max_cluster_columns

    if cluster_by:
        columns = cluster_by if isinstance(cluster_by, list) else [cluster_by]
        if len(columns) > maximum:
            yield make_suggestion(
                MAT_CLUSTERING,
                f"`cluster_by` lists {len(columns)} columns; "
                f"pruning benefit diminishes past {maximum}.",
                level=Level.INFORMATION,
                file=model.relative_path,
                evidence=f"cluster_by={columns}",
                remediation=(
                    "Run `system$clustering_information()` on the table and review "
                    "average depth and total overlap. Identify which columns appear "
                    "in filter predicates; only those belong in the clustering key."
                ),
                effort=Effort.LOW,
            )


# =============================================================================
# Configuration conventions (ARCHITECTURE tier -- suppressed for migrations)
# =============================================================================


@rule(
    MAT_REDUNDANT_CONFIG,
    "Model config repeats the folder default",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Restating an inherited default adds a line that must be kept in sync. "
        "When the folder default changes, models that repeated it silently "
        "keep the old value."
    ),
)
def redundant_config(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    redundant = [
        key
        for key, value in model.own_config.items()
        if key in model.folder_config and model.folder_config[key] == value
    ]
    if not redundant:
        return
    yield make_suggestion(
        MAT_REDUNDANT_CONFIG,
        f"{plural(len(redundant), 'config key')} "
        f"{', '.join(sorted(redundant))} "
        f"{'repeats' if len(redundant) == 1 else 'repeat'} "
        "the `dbt_project.yml` folder default.",
        file=model.relative_path,
        evidence=", ".join(f"{k}={model.own_config[k]!r}" for k in sorted(redundant)),
        remediation=(
            "Remove the redundant keys from the model's `config()` block and let the "
            "folder default apply. Keep model-level config only where it overrides "
            "the default."
        ),
        effort=Effort.LOW,
    )


@rule(
    MAT_NO_FOLDER_DEFAULT,
    "Layer folder has no materialization default",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Setting `+materialized` per layer in `dbt_project.yml` states "
        "materialization in one place instead of leaving it model-by-model."
    ),
)
def no_folder_default(project: ProjectContext) -> Iterator[Suggestion]:
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
    yield make_suggestion(
        MAT_NO_FOLDER_DEFAULT,
        f"{plural(len(unconfigured), 'folder')} "
        f"{'has' if len(unconfigured) == 1 else 'have'} no `+materialized` "
        f"default in `dbt_project.yml`: {', '.join(unconfigured)}.",
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
