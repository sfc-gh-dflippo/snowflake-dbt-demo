"""
DOC -- documentation coverage.

Low-severity throughout: missing documentation does not break a build. It does
determine whether anyone other than the author can use the output, which is why
it is audited rather than ignored.

``persist_docs`` is included even though no skill in this repo mentions it,
because it is live configuration here and it is the difference between docs that
exist in dbt and docs that reach Snowflake metadata where BI tools can read them.
"""

from __future__ import annotations

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

if TYPE_CHECKING:
    from dbt_quality.discovery import ModelFile, ProjectContext

CATEGORY = "DOC"

DOC_NO_MODEL_DESCRIPTION = "SSC-EWI-DBTDOC0001"
DOC_COLUMN_COVERAGE = "SSC-EWI-DBTDOC0002"
DOC_NO_SOURCE_DESCRIPTION = "SSC-EWI-DBTDOC0003"
DOC_NO_PERSIST_DOCS = "SSC-EWI-DBTDOC0004"
#: DOC0005 (no exposures declared) was removed. The ID is retired, not reused.


@rule(
    DOC_NO_MODEL_DESCRIPTION,
    "Model missing description",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "The description is what a consumer reads in the catalog to "
        "decide whether this is the right table."
    ),
)
def no_model_description(
    model: ModelFile, project: ProjectContext
) -> Iterator[Suggestion]:
    model_def = project.schema_def(model.name)
    if not model_def:
        return  # TST010 covers the missing entry
    if str(model_def.get("description", "")).strip():
        return
    # A missing description costs more on a gold model with external consumers
    # than on an internal passthrough -- a difference in consequence, not in
    # confidence, so it varies severity rather than level.
    severity = Severity.MEDIUM if model.layer == "gold" else Severity.LOW
    yield make_suggestion(
        DOC_NO_MODEL_DESCRIPTION,
        f"`{model.name}` has no description in the schema YAML.",
        severity=severity,
        file=project.schema_sources.get(model.name, model.relative_path),
        evidence=f"{model.name}: description absent",
        remediation=(
            "Add a description stating what one row represents, "
            "the grain, and the refresh cadence:\n\n"
            "```yaml\n"
            f"  - name: {model.name}\n"
            "    description: |\n"
            "      One row per <entity>. Refreshed daily.\n"
            "      Use this as the source of truth for <purpose>.\n"
            "```"
        ),
        effort=Effort.LOW,
    )


@rule(
    DOC_COLUMN_COVERAGE,
    "Column documentation below threshold",
    category=CATEGORY,
    scope=Scope.MODEL,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Column meaning is where ambiguity lives. Whether an "
        "amount is gross or net, or a date is the event or the "
        "load, cannot be inferred from a model description."
    ),
)
def column_coverage(model: ModelFile, project: ProjectContext) -> Iterator[Suggestion]:
    model_def = project.schema_def(model.name)
    columns = [c for c in (model_def.get("columns") or []) if isinstance(c, dict)]
    if len(columns) < 3:
        return
    documented = sum(1 for c in columns if str(c.get("description", "")).strip())
    ratio = documented / len(columns)
    threshold = project.config.column_doc_coverage
    if ratio >= threshold:
        return
    undocumented = [
        str(c.get("name")) for c in columns if not str(c.get("description", "")).strip()
    ]
    yield make_suggestion(
        DOC_COLUMN_COVERAGE,
        f"{documented} of {len(columns)} columns documented "
        f"({ratio:.0%}), below the {threshold:.0%} threshold.",
        file=project.schema_sources.get(model.name, model.relative_path),
        evidence=f"undocumented: {', '.join(undocumented[:8])}"
        + (" ..." if len(undocumented) > 8 else ""),
        remediation=(
            "Document columns whose meaning is not obvious from "
            "the name first: amounts, dates, flags, and codes. "
            "For shared definitions, use a `docs` block and "
            "reference with "
            "`description: \"{{ doc('column_name') }}\"`."
        ),
        effort=Effort.MEDIUM,
        undocumented=undocumented,
    )


@rule(
    DOC_NO_SOURCE_DESCRIPTION,
    "Source or source table missing description",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Sources are the project's contract with the outside "
        "world. Where data comes from and how often it lands "
        "belongs next to the definition."
    ),
)
def no_source_description(project: ProjectContext) -> Iterator[Suggestion]:
    for source in project.source_defs:
        name = str(source.get("name", "unknown"))
        if not str(source.get("description", "")).strip():
            yield make_suggestion(
                DOC_NO_SOURCE_DESCRIPTION,
                f"Source `{name}` has no description.",
                file="models/",
                evidence=f"source {name}: description absent",
                remediation=(
                    "Record the upstream system, its owner, and "
                    "the expected landing cadence. Add a "
                    "`freshness:` block so staleness is detected "
                    "rather than assumed."
                ),
                effort=Effort.LOW,
            )
        undescribed = [
            str(t.get("name"))
            for t in (source.get("tables") or [])
            if isinstance(t, dict) and not str(t.get("description", "")).strip()
        ]
        if undescribed:
            yield make_suggestion(
                DOC_NO_SOURCE_DESCRIPTION,
                f"{plural(len(undescribed), 'table')} in source "
                f"`{name}` "
                f"{'lacks' if len(undescribed) == 1 else 'lack'} descriptions: "
                f"{', '.join(undescribed[:6])}"
                + (" ..." if len(undescribed) > 6 else "")
                + ".",
                file="models/",
                evidence=", ".join(undescribed[:6]),
                remediation=(
                    "Describe each source table so its grain is "
                    "stated once, at the boundary."
                ),
                effort=Effort.LOW,
            )


@rule(
    DOC_NO_PERSIST_DOCS,
    "persist_docs not configured",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Without `persist_docs`, descriptions live only in the "
        "dbt docs site. With it, they become Snowflake COMMENTs "
        "visible to BI tools and `describe table`."
    ),
)
def no_persist_docs(project: ProjectContext) -> Iterator[Suggestion]:
    if project.model_count == 0:
        return
    if _has_persist_docs(project.project_yml.get("models")):
        return
    documented = sum(
        1
        for d in project.schema_models.values()
        if str(d.get("description", "")).strip()
    )
    if documented == 0:
        return  # nothing to persist yet; DOC001 is the prior fix
    yield make_suggestion(
        DOC_NO_PERSIST_DOCS,
        f"{plural(documented, 'model')} "
        f"{'has' if documented == 1 else 'have'} descriptions that are not "
        "persisted as Snowflake COMMENTs.",
        file="dbt_project.yml",
        evidence="no +persist_docs under models:",
        remediation=(
            "Push descriptions into the database:\n\n"
            "```yaml\n"
            "models:\n"
            f"  {project.name}:\n"
            "    +persist_docs:\n"
            "      relation: true\n"
            "      columns: true\n"
            "```\n\n"
            "Descriptions then appear in every consumer tool, "
            "not only the dbt docs site."
        ),
        effort=Effort.LOW,
        documented_models=documented,
    )


def _has_persist_docs(node: Any) -> bool:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("+persist_docs", "persist_docs"):
                # A mapping with relation:false and columns:false is not enabled.
                if isinstance(value, dict):
                    if any(value.values()):
                        return True
                elif value:
                    return True
            elif _has_persist_docs(value):
                return True
    return False
