"""
ARC -- architecture and lineage conventions.

Every rule here is ``Tier.ARCHITECTURE``, so the engine suppresses it when
provenance indicates lift-and-shift conversion; suppressed suggestions are
counted and summarised as a single modernisation note rather than deleted.

**Model and column names are deliberately not audited.** Judging a name needs
the original object name, and a dbt project records that nowhere
machine-readable (the migration header is a comment, never reaching
``manifest.json``; identifier shape is unlabelled and platform-dependent; no
``meta``/crosswalk field exists). ARC002 and ARC008 guessed at this anyway and
were removed -- do not reintroduce them behind a config flag; the problem is
the missing fact, not the default. Revisit only if provenance ever becomes
declared (a ``meta`` key, a crosswalk).
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
    Tier,
    make_suggestion,
    plural,
    rule,
)
from dbt_quality.core.sqlutil import span
from dbt_quality.discovery import LAYER_ALIASES

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "ARC"

ARC_UNKNOWN_LAYER = "SSC-EWI-DBTARC0001"
# ARC002 (model name convention) and ARC008 (filename case) were removed
# deliberately -- see the module docstring. The IDs are not reused, so a finding
# from an older run cannot be silently reinterpreted as a different rule.
ARC_SOURCE_OUTSIDE_STAGING = "SSC-EWI-DBTARC0003"
ARC_DUPLICATE_STAGING = "SSC-EWI-DBTARC0004"
ARC_LAYER_CROSSING = "SSC-EWI-DBTARC0005"
ARC_STAGING_LOGIC = "SSC-EWI-DBTARC0006"
ARC_DUPLICATE_TAGS = "SSC-EWI-DBTARC0007"

LAYER_ORDER = {"bronze": 0, "silver": 1, "gold": 2}

AGGREGATE_PATTERN = re.compile(
    r"\b(sum|count|avg|min|max|median|listagg)\s*\(", re.IGNORECASE
)
JOIN_PATTERN = re.compile(r"\bjoin\b", re.IGNORECASE)


@rule(
    ARC_UNKNOWN_LAYER,
    "Model outside a recognised layer folder",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Layer folders make materialization, tagging, and schema routing "
        "configurable in one place. A model outside them inherits no layer "
        "configuration."
    ),
)
def unknown_layer(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.layer:
        return
    location = "/".join(model.segments) if model.segments else ""
    yield make_suggestion(
        ARC_UNKNOWN_LAYER,
        (
            f"This model sits in `models/{location}`, which is not a recognised "
            "layer folder, so it inherits no layer configuration."
            if location
            else "This model sits directly in `models/` rather than a layer folder, "
            "so it inherits no layer configuration."
        ),
        file=model.relative_path,
        evidence=f"path segments: {location or 'models/ root'}",
        remediation=(
            "Move it into the layer matching its role: `bronze/` for source-aligned "
            "staging, `silver/` for business-logic intermediates, `gold/` for "
            "consumer-facing marts. Recognised aliases are "
            f"{', '.join(sorted(set(LAYER_ALIASES)))}."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    ARC_SOURCE_OUTSIDE_STAGING,
    "source() used outside the staging layer",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Confining `source()` to staging gives every raw table one entry point. "
        "A schema change upstream is then fixed in one file."
    ),
)
def source_outside_staging(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    if model.layer in ("bronze", "") or not model.sources:
        return
    labels = [f"{s[0]}.{s[1]}" for s in model.sources]
    match = re.search(r"\bsource\s*\(", model.raw)
    yield make_suggestion(
        ARC_SOURCE_OUTSIDE_STAGING,
        f"This {model.layer.title()} model calls `source()` on "
        f"{', '.join(f'`{label}`' for label in labels)} directly, "
        "bypassing the staging layer.",
        file=model.relative_path,
        **(span(model.raw, match.start(), match.end()) if match else {}),
        evidence=", ".join(labels),
        remediation=(
            "Add a dedicated staging model for each source table and `ref()` it "
            "here. Staging is where renaming, casting, and light cleaning belong."
        ),
        effort=Effort.MEDIUM,
        sources=labels,
    )


@rule(
    ARC_DUPLICATE_STAGING,
    "Source table has more than one staging model",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "One staging model per source table keeps casting and renaming decisions "
        "in one place. Two staging models over the same table will eventually "
        "disagree."
    ),
)
def duplicate_staging(project: ProjectContext) -> Iterator[Suggestion]:
    by_source: dict[tuple[str, str], list[ModelFile]] = defaultdict(list)
    for model in project.models:
        if model.layer != "bronze":
            continue
        for source in model.sources:
            by_source[source].append(model)

    for source, models in sorted(by_source.items(), key=lambda kv: kv[0]):
        if len(models) < 2:
            continue
        names = sorted(m.name for m in models)
        yield make_suggestion(
            ARC_DUPLICATE_STAGING,
            f"Source `{source[0]}.{source[1]}` has {len(names)} staging models:"
            f" {', '.join(names)}.",
            file=models[0].relative_path,
            evidence=f"{source[0]}.{source[1]} -> {', '.join(names)}",
            remediation=(
                "Keep one staging model as the single entry point and `ref()` "
                "it from the others. If consumers need different shapes, those "
                "differences belong in silver, not in parallel staging models."
            ),
            effort=Effort.MEDIUM,
            models=names,
        )


@rule(
    ARC_LAYER_CROSSING,
    "Dependency flows against the layer order",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    tier=Tier.ARCHITECTURE,
    requires_manifest=True,
    rationale=(
        "Data flows bronze to silver to gold. A backward edge breaks the "
        "dependency order and makes cycles possible."
    ),
)
def layer_crossing(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.layer not in LAYER_ORDER:
        return
    own = LAYER_ORDER[model.layer]
    for parent_name in project.graph.parent_names(model.name):
        parent = project.model_by_name(parent_name)
        if parent is None or parent.layer not in LAYER_ORDER:
            continue
        parent_rank = LAYER_ORDER[parent.layer]
        if parent_rank <= own:
            continue
        yield make_suggestion(
            ARC_LAYER_CROSSING,
            f"This {model.layer.title()} model depends on `{parent_name}` "
            f"in the downstream {parent.layer} layer.",
            file=model.relative_path,
            evidence=f"{parent.layer}.{parent_name} -> {model.layer}.{model.name}",
            remediation=(
                "Invert the dependency: move the shared logic into the earlier "
                f"layer so both can read it, or move `{model.name}` into "
                f"`{parent.layer}/` if it belongs downstream."
            ),
            effort=Effort.HIGH,
        )


@rule(
    ARC_STAGING_LOGIC,
    "Staging model contains joins or aggregation",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Staging is a one-to-one projection of a single source table. "
        "Joins and aggregation in staging hide business logic from the "
        "silver layer and couple the model to multiple sources."
    ),
)
def staging_logic(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    if model.layer != "bronze" or model.is_python:
        return
    issues: list[str] = []
    if JOIN_PATTERN.search(model.stripped):
        issues.append("a join")
    if re.search(
        r"\bgroup\s+by\b", model.stripped, re.IGNORECASE
    ) and AGGREGATE_PATTERN.search(model.stripped):
        issues.append("an aggregation")
    if not issues:
        return
    yield make_suggestion(
        ARC_STAGING_LOGIC,
        "This staging model contains " + " and ".join(issues) + ".",
        file=model.relative_path,
        evidence=", ".join(issues),
        remediation=(
            "Keep staging to a one-to-one projection of its source: rename "
            "columns and cast types. Move joins and aggregation into a silver "
            "`int_` model where consumers expect to find them."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    ARC_DUPLICATE_TAGS,
    "Nested folder repeats a parent's tags",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    tier=Tier.ARCHITECTURE,
    rationale=(
        "Tags in `dbt_project.yml` accumulate down the tree. Repeating a "
        "parent tag in a child adds nothing and creates two places to edit."
    ),
)
def duplicate_tags(project: ProjectContext) -> Iterator[Suggestion]:
    def walk(node: Any, path: list[str], inherited: set[str]) -> Iterator[Suggestion]:
        if not isinstance(node, dict):
            return
        own = node.get("+tags") or node.get("tags") or []
        own_set = {str(t) for t in (own if isinstance(own, list) else [own])}
        redundant = own_set & inherited
        if redundant:
            location = "/".join(path) or "<project root>"
            yield make_suggestion(
                ARC_DUPLICATE_TAGS,
                f"`{location}` re-declares "
                f"{plural(len(redundant), 'tag')} it already inherits from its "
                f"parent: {', '.join(f'`{t}`' for t in sorted(redundant))}.",
                file="dbt_project.yml",
                yaml_keys=("models", *path, "tags"),
                evidence=f"{location} +tags: {sorted(own_set)}",
                remediation=(
                    f"Remove {', '.join(sorted(redundant))} from `{location}`. "
                    "Tags accumulate down the tree, so the parent declaration "
                    "already applies here."
                ),
                effort=Effort.LOW,
            )
        for key, value in node.items():
            if not key.startswith("+"):
                yield from walk(value, [*path, str(key)], inherited | own_set)

    yield from walk(project.project_yml.get("models") or {}, [], set())
