"""
ARC -- architecture and lineage conventions.

Every rule here is ``Tier.ARCHITECTURE``, which means the engine suppresses it
when provenance indicates lift-and-shift conversion. That is the point of the
tier: a converted project never chose a medallion layout or ``stg_``/``dim_``
naming, so reporting dozens of naming violations against generated code buries
the findings that matter. Suppressed findings are counted and summarised as a
single modernisation note instead of being deleted, so the option is still
visible.

Naming enforcement is mode-driven because this repo's own guidance conflicts:
``dbt-architecture`` mandates layer prefixes while ``dbt-modeling``'s
Name-Retention Policy explicitly forbids them in favour of original source object
names. The default ``auto`` infers the project's own dominant convention and
flags deviation from that, rather than imposing either standard.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from dbt_audit.core.base import (
    Effort,
    Finding,
    Scope,
    Severity,
    Tier,
    make_finding,
    rule,
)
from dbt_audit.core.sqlutil import find_line_number
from dbt_audit.discovery import LAYER_ALIASES, dominant_naming_convention

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "ARC"

ARC_UNKNOWN_LAYER = "ARC001"
ARC_NAMING = "ARC002"
ARC_SOURCE_OUTSIDE_STAGING = "ARC003"
ARC_DUPLICATE_STAGING = "ARC004"
ARC_LAYER_CROSSING = "ARC005"
ARC_STAGING_LOGIC = "ARC006"
ARC_DUPLICATE_TAGS = "ARC007"
ARC_FILENAME_CASE = "ARC008"

LAYER_ORDER = {"bronze": 0, "silver": 1, "gold": 2}

LAYER_PREFIXES = {
    "bronze": re.compile(r"^stg_", re.IGNORECASE),
    "silver": re.compile(r"^(int_|lookup_)", re.IGNORECASE),
    "gold": re.compile(r"^(dim_|fct_|mart_|agg_)", re.IGNORECASE),
}
EXPECTED_PREFIX_HINT = {
    "bronze": "stg_<source>__<entity>",
    "silver": "int_<entity>__<description>",
    "gold": "dim_<entity> or fct_<process>",
}

AGGREGATE_PATTERN = re.compile(
    r"\b(sum|count|avg|min|max|median|listagg)\s*\(", re.IGNORECASE
)
JOIN_PATTERN = re.compile(r"\bjoin\b", re.IGNORECASE)


@rule(
    ARC_UNKNOWN_LAYER,
    "Model outside a recognised layer folder",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Layer folders are what make materialization, tagging and schema routing "
        "configurable in one place. A model outside them inherits nothing and its role "
        "is not evident from its location."
    ),
)
def unknown_layer(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.layer:
        return
    location = "/".join(model.segments) if model.segments else "models/ root"
    yield make_finding(
        ARC_UNKNOWN_LAYER,
        f"Model sits in `{location}`, which maps to no recognised layer, so it "
        "inherits no layer configuration.",
        file=model.relative_path,
        evidence=f"path segments: {location}",
        remediation=(
            "Move it into the layer matching its role: `bronze/` for source-aligned "
            "staging, `silver/` for business-logic intermediates, `gold/` for "
            "consumer-facing marts. Recognised aliases are "
            f"{', '.join(sorted(set(LAYER_ALIASES)))}."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    ARC_NAMING,
    "Model name does not follow the project's convention",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "A consistent convention lets a reader infer a model's layer and grain from its "
        "name alone. Which convention matters less than applying one consistently."
    ),
)
def naming(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    mode = project.config.naming_mode
    if mode == "off" or not model.layer:
        return
    if mode == "auto":
        mode = dominant_naming_convention(project)
        if mode != "medallion":
            # No clear convention, or the project deliberately retains source
            # names. Either way there is nothing to enforce.
            return
    if mode == "retain-original":
        if LAYER_PREFIXES.get(model.layer, re.compile(r"$^")).match(model.name):
            yield make_finding(
                ARC_NAMING,
                f"`{model.name}` carries a layer prefix, but this project retains "
                "original source object names.",
                file=model.relative_path,
                evidence=model.name,
                remediation=(
                    "Rename to the original source object name and express the layer "
                    "through the folder. Use `alias` if the warehouse name must differ "
                    "from the file name."
                ),
                effort=Effort.MEDIUM,
            )
        return

    pattern = LAYER_PREFIXES.get(model.layer)
    if pattern is None or pattern.match(model.name):
        return
    yield make_finding(
        ARC_NAMING,
        f"`{model.name}` is in the {model.layer} layer but does not use the expected "
        f"`{EXPECTED_PREFIX_HINT[model.layer]}` form, which most models here follow.",
        file=model.relative_path,
        evidence=f"{model.name} in {model.layer}/",
        remediation=(
            f"Rename to the `{EXPECTED_PREFIX_HINT[model.layer]}` form. Update every "
            "`ref()` to it in the same change -- `dbt build` will fail fast on a missed "
            "one, and `dbt ls --select +<model>` lists the consumers to update."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    ARC_FILENAME_CASE,
    "Model filename is not snake_case",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Model file names become relation names. Mixed case forces quoted identifiers "
        "downstream and makes `ref()` fragile on case-sensitive filesystems."
    ),
)
def filename_case(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    issues: list[str] = []
    if model.name != model.name.lower():
        issues.append("contains uppercase characters")
    if "__" in model.name and not re.match(r"^(stg|int)_", model.name, re.IGNORECASE):
        issues.append("uses a double underscore outside the stg_/int_ convention")
    if not issues:
        return
    yield make_finding(
        ARC_FILENAME_CASE,
        f"Model file name `{model.name}` " + " and ".join(issues) + ".",
        file=model.relative_path,
        evidence=model.name,
        remediation=(
            f"Rename to `{re.sub(r'_+', '_', model.name.lower())}`. Reserve the double "
            "underscore for the `stg_<source>__<entity>` separator, where it "
            "distinguishes source from entity."
        ),
        effort=Effort.LOW,
    )


@rule(
    ARC_SOURCE_OUTSIDE_STAGING,
    "source() used outside the staging layer",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.WARNING,
    rationale=(
        "Confining source() to staging gives every raw table exactly one entry point. "
        "Reading a source from silver or gold means a schema change upstream has to be "
        "fixed in several places instead of one."
    ),
)
def source_outside_staging(
    model: ModelFile, project: ProjectContext
) -> Iterator[Finding]:
    if model.layer in ("bronze", "") or not model.sources:
        return
    labels = [f"{s[0]}.{s[1]}" for s in model.sources]
    match = re.search(r"\bsource\s*\(", model.raw)
    yield make_finding(
        ARC_SOURCE_OUTSIDE_STAGING,
        f"{model.layer.title()} model reads source table(s) directly: {', '.join(labels)}.",
        file=model.relative_path,
        line=find_line_number(model.raw, match.start()) if match else None,
        evidence=", ".join(labels),
        remediation=(
            "Add a staging model for each source table and reference that instead. "
            "Staging is where renaming, casting and light cleaning belong, so an "
            "upstream change is absorbed in one file."
        ),
        effort=Effort.MEDIUM,
        sources=labels,
    )


@rule(
    ARC_DUPLICATE_STAGING,
    "Source table has more than one staging model",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.ARCHITECTURE,
    severity=Severity.WARNING,
    rationale=(
        "One staging model per source table keeps casting and renaming decisions in one "
        "place. Two staging models over the same table will eventually disagree."
    ),
)
def duplicate_staging(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            ARC_DUPLICATE_STAGING,
            f"Source `{source[0]}.{source[1]}` is staged by {len(names)} models: "
            f"{', '.join(names)}.",
            file=models[0].relative_path,
            evidence=f"{source[0]}.{source[1]} -> {', '.join(names)}",
            remediation=(
                "Keep one staging model as the single entry point and have the others "
                "ref() it. If they exist because consumers need different shapes, those "
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
    tier=Tier.ARCHITECTURE,
    severity=Severity.WARNING,
    requires_manifest=True,
    rationale=(
        "Data should flow bronze to silver to gold. A backward edge means the layers no "
        "longer describe the dependency order, and a cycle becomes possible."
    ),
)
def layer_crossing(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            ARC_LAYER_CROSSING,
            f"{model.layer.title()} model depends on `{parent_name}` in the "
            f"{parent.layer} layer, which is downstream of it.",
            file=model.relative_path,
            evidence=f"{parent.layer}.{parent_name} -> {model.layer}.{model.name}",
            remediation=(
                "Invert the dependency. Either move the shared logic into the earlier "
                f"layer so both can read it, or move `{model.name}` into "
                f"`{parent.layer}/` if it genuinely belongs downstream."
            ),
            effort=Effort.HIGH,
        )


@rule(
    ARC_STAGING_LOGIC,
    "Staging model contains joins or aggregation",
    category=CATEGORY,
    scope=Scope.MODEL,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Staging exists to present one source table cleanly: renamed, cast, lightly "
        "filtered. Business logic there is invisible to anyone looking in silver for it, "
        "and it couples the staging model to more than one source."
    ),
)
def staging_logic(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
    if model.layer != "bronze" or model.is_python:
        return
    issues: list[str] = []
    if JOIN_PATTERN.search(model.stripped):
        issues.append("a JOIN")
    if re.search(
        r"\bgroup\s+by\b", model.stripped, re.IGNORECASE
    ) and AGGREGATE_PATTERN.search(model.stripped):
        issues.append("an aggregation")
    if len(model.sources) + len(model.refs) > 1:
        issues.append(f"{len(model.sources) + len(model.refs)} upstream references")
    if not issues:
        return
    yield make_finding(
        ARC_STAGING_LOGIC,
        "Staging model contains " + ", ".join(issues) + ".",
        file=model.relative_path,
        evidence=", ".join(issues),
        remediation=(
            "Keep staging to a one-to-one projection of its source: rename columns, cast "
            "types, and drop obvious bad rows. Move joins and aggregation into a silver "
            "`int_` model where consumers expect to find them."
        ),
        effort=Effort.MEDIUM,
    )


@rule(
    ARC_DUPLICATE_TAGS,
    "Nested folder repeats a parent's tags",
    category=CATEGORY,
    scope=Scope.PROJECT,
    tier=Tier.ARCHITECTURE,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Tags in dbt_project.yml are additive down the tree. Repeating a parent tag in a "
        "child adds nothing and creates two places to edit when the tag changes."
    ),
)
def duplicate_tags(project: ProjectContext) -> Iterator[Finding]:
    def walk(node: Any, path: list[str], inherited: set[str]) -> Iterator[Finding]:
        if not isinstance(node, dict):
            return
        own = node.get("+tags") or node.get("tags") or []
        own_set = {str(t) for t in (own if isinstance(own, list) else [own])}
        redundant = own_set & inherited
        if redundant:
            location = "/".join(path) or "<project root>"
            yield make_finding(
                ARC_DUPLICATE_TAGS,
                f"`{location}` re-declares tag(s) already inherited from its parent: "
                f"{', '.join(sorted(redundant))}.",
                file="dbt_project.yml",
                evidence=f"{location} +tags: {sorted(own_set)}",
                remediation=(
                    f"Remove {', '.join(sorted(redundant))} from `{location}`. Tags "
                    "accumulate down the tree, so the parent declaration already "
                    "applies here."
                ),
                effort=Effort.LOW,
            )
        for key, value in node.items():
            if not key.startswith("+"):
                yield from walk(value, [*path, str(key)], inherited | own_set)

    yield from walk(project.project_yml.get("models") or {}, [], set())
