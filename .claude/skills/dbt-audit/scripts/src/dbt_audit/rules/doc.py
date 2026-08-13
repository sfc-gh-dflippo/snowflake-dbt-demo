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

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule

if TYPE_CHECKING:
    from dbt_audit.discovery import ModelFile, ProjectContext

CATEGORY = "DOC"

DOC_NO_MODEL_DESCRIPTION = "DOC001"
DOC_COLUMN_COVERAGE = "DOC002"
DOC_NO_SOURCE_DESCRIPTION = "DOC003"
DOC_NO_PERSIST_DOCS = "DOC004"
DOC_NO_EXPOSURES = "DOC005"


@rule(
    DOC_NO_MODEL_DESCRIPTION,
    "Model has no description",
    category=CATEGORY,
    scope=Scope.MODEL,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "The description is what a consumer reads in the catalog to decide whether this "
        "is the right table. Without it they guess from the name, or ask."
    ),
)
def no_model_description(
    model: ModelFile, project: ProjectContext
) -> Iterator[Finding]:
    model_def = project.schema_def(model.name)
    if not model_def:
        return  # TST010 covers the missing entry
    if str(model_def.get("description", "")).strip():
        return
    severity = Severity.WARNING if model.layer == "gold" else Severity.RECOMMENDATION
    yield make_finding(
        DOC_NO_MODEL_DESCRIPTION,
        "Model has a schema entry but no description.",
        severity=severity,
        file=project.schema_sources.get(model.name, model.relative_path),
        evidence=f"{model.name}: description absent",
        remediation=(
            "Describe what one row represents, its grain, and how often it refreshes. "
            "That is what a consumer needs before trusting it:\n\n"
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
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Column meaning is where ambiguity actually lives -- whether an amount is gross "
        "or net, whether a date is the event or the load. A model description cannot "
        "carry that."
    ),
)
def column_coverage(model: ModelFile, project: ProjectContext) -> Iterator[Finding]:
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
    yield make_finding(
        DOC_COLUMN_COVERAGE,
        f"{documented} of {len(columns)} columns documented ({ratio:.0%}), below the "
        f"{threshold:.0%} threshold.",
        file=project.schema_sources.get(model.name, model.relative_path),
        evidence=f"undocumented: {', '.join(undocumented[:8])}"
        + (" ..." if len(undocumented) > 8 else ""),
        remediation=(
            "Document the columns whose meaning is not obvious from the name first -- "
            "amounts, dates, flags and codes. For descriptions shared across models, "
            "define them once in a `docs` block and reference with "
            "`description: \"{{ doc('column_name') }}\"`."
        ),
        effort=Effort.MEDIUM,
        undocumented=undocumented,
    )


@rule(
    DOC_NO_SOURCE_DESCRIPTION,
    "Source or source table has no description",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Sources are the project's contract with the outside world. Where the data comes "
        "from and how often it lands belongs next to the definition."
    ),
)
def no_source_description(project: ProjectContext) -> Iterator[Finding]:
    for source in project.source_defs:
        name = str(source.get("name", "unknown"))
        if not str(source.get("description", "")).strip():
            yield make_finding(
                DOC_NO_SOURCE_DESCRIPTION,
                f"Source `{name}` has no description.",
                file="models/",
                evidence=f"source {name}: description absent",
                remediation=(
                    "Record the upstream system, its owner, and the expected landing "
                    "cadence. Add a `freshness:` block at the same time so staleness is "
                    "detected rather than assumed."
                ),
                effort=Effort.LOW,
            )
        undescribed = [
            str(t.get("name"))
            for t in (source.get("tables") or [])
            if isinstance(t, dict) and not str(t.get("description", "")).strip()
        ]
        if undescribed:
            yield make_finding(
                DOC_NO_SOURCE_DESCRIPTION,
                f"Source `{name}` has {len(undescribed)} table(s) without a "
                f"description: {', '.join(undescribed[:6])}"
                + (" ..." if len(undescribed) > 6 else ""),
                file="models/",
                evidence=", ".join(undescribed[:6]),
                remediation=(
                    "Describe each source table so its grain is stated once, at the boundary."
                ),
                effort=Effort.LOW,
            )


@rule(
    DOC_NO_PERSIST_DOCS,
    "persist_docs not configured",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Without persist_docs, descriptions live only in dbt's own docs site. With it, "
        "they become Snowflake COMMENTs that BI tools, catalogs and anyone running "
        "DESCRIBE TABLE can see."
    ),
)
def no_persist_docs(project: ProjectContext) -> Iterator[Finding]:
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
    yield make_finding(
        DOC_NO_PERSIST_DOCS,
        f"{documented} model(s) carry descriptions, but `persist_docs` is not enabled, "
        "so none of them reach Snowflake metadata.",
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
            "Documentation already written then becomes visible to every consumer, not "
            "only to people who open the dbt docs site."
        ),
        effort=Effort.LOW,
        documented_models=documented,
    )


def _has_persist_docs(node: Any) -> bool:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("+persist_docs", "persist_docs") and value:
                return True
            if _has_persist_docs(value):
                return True
    return False


@rule(
    DOC_NO_EXPOSURES,
    "No exposures declared",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Exposures record which dashboards and applications depend on which models. "
        "Without them, nobody can answer 'what breaks if I change this' before changing "
        "it."
    ),
)
def no_exposures(project: ProjectContext) -> Iterator[Finding]:
    if project.model_count < 10:
        return
    has_exposures = any(
        "exposures" in path.read_text(encoding="utf-8", errors="replace")
        for path in project.root.rglob("*.yml")
        if path.is_file()
        and "target" not in path.parts
        and "dbt_packages" not in path.parts
    )
    if has_exposures:
        return
    yield make_finding(
        DOC_NO_EXPOSURES,
        f"Project has {project.model_count} models and declares no exposures, so "
        "downstream consumers are not represented in the lineage graph.",
        file="models/",
        evidence="no exposures: block found in any YAML",
        remediation=(
            "Declare the dashboards and applications that read the gold layer:\n\n"
            "```yaml\n"
            "exposures:\n"
            "  - name: executive_dashboard\n"
            "    type: dashboard\n"
            "    owner: {name: Analytics, email: analytics@example.com}\n"
            "    depends_on: [ref('fct_orders'), ref('dim_customers')]\n"
            "```\n\n"
            "Impact analysis before a change then becomes a lineage query rather than "
            "an email thread."
        ),
        effort=Effort.MEDIUM,
    )
