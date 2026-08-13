"""
The audit runner.

Dispatches registered rules by scope, applies migration-tier suppression, and
records which rules could not run so the report can distinguish "checked and
clean" from "not checked".
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from dbt_audit import rules as _rules  # noqa: F401  -- import registers all packs
from dbt_audit.core.base import REGISTRY, Finding, Scope, Tier
from dbt_audit.discovery import PortfolioContext, ProjectContext
from dbt_audit.provenance import classify


@dataclass
class SkippedRule:
    """A rule that did not run, and why -- surfaced in the report appendix."""

    rule_id: str
    title: str
    reason: str


@dataclass
class AuditResult:
    """Everything one audit run produced."""

    findings: list[Finding] = field(default_factory=list)
    skipped: list[SkippedRule] = field(default_factory=list)
    #: Per-project metadata for the report header.
    projects: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def active_findings(self) -> list[Finding]:
        """Findings that count toward the score (suppressed ones excluded)."""
        return [f for f in self.findings if not f.suppressed]


def _safe_iter(fn: Any, *args: Any) -> Iterator[Finding]:
    """
    Run one rule, converting an exception into a diagnostic rather than
    aborting the whole audit.

    A rule crashing on unusual SQL must not cost the user every other finding,
    so failures are contained per-rule. The exception is re-surfaced as an error
    in the result so a broken rule cannot hide behind a clean report.
    """
    try:
        yield from fn(*args)
    except Exception as exc:  # noqa: BLE001 -- deliberate containment boundary
        raise RuntimeError(str(exc)) from exc


def run_audit(portfolio: PortfolioContext) -> AuditResult:
    """Execute every enabled rule against a discovered portfolio."""
    result = AuditResult()
    config = portfolio.config
    disabled = set(config.disabled_rules)

    for project in portfolio.projects:
        project.provenance = classify(project)
        result.errors.extend(project.read_errors)
        result.projects.append(
            {
                "name": project.name,
                "path": project.relative_root,
                "model_count": project.model_count,
                "macro_count": sum(len(m.macros) for m in project.macros),
                "manifest": project.graph.available,
                "manifest_stale": project.graph.stale,
                "provenance": {
                    "is_migration": project.provenance.is_migration,
                    "confidence": project.provenance.confidence,
                    "source_platform": project.provenance.source_platform,
                    "signals": project.provenance.signals,
                },
            }
        )

    for rule_id, meta in sorted(REGISTRY.items()):
        if rule_id in disabled:
            result.skipped.append(
                SkippedRule(rule_id, meta.title, "disabled in .dbt-audit.yml")
            )
            continue

        if meta.scope == Scope.PORTFOLIO:
            _collect(result, meta, _safe_iter(meta.fn, portfolio), None)
            continue

        for project in portfolio.projects:
            if meta.requires_manifest and not project.graph.available:
                result.skipped.append(
                    SkippedRule(
                        rule_id,
                        meta.title,
                        f"{project.name}: needs target/manifest.json (run `dbt parse`)",
                    )
                )
                continue

            if meta.scope == Scope.PROJECT:
                _collect(result, meta, _safe_iter(meta.fn, project), project)
            else:
                for model in project.models:
                    _collect(result, meta, _safe_iter(meta.fn, model, project), project)

    result.findings.sort(key=_finding_sort_key)
    return result


def _collect(
    result: AuditResult,
    meta: Any,
    findings: Iterator[Finding],
    project: ProjectContext | None,
) -> None:
    """Attach project attribution, apply suppression, and record the findings."""
    try:
        produced = list(findings)
    except RuntimeError as exc:
        result.errors.append(f"rule {meta.rule_id} failed: {exc}")
        result.skipped.append(
            SkippedRule(meta.rule_id, meta.title, f"rule error: {exc}")
        )
        return

    for finding in produced:
        if project is not None and not finding.project:
            finding.project = project.name
        _apply_suppression(finding, project)
        result.findings.append(finding)


def _apply_suppression(finding: Finding, project: ProjectContext | None) -> None:
    """
    Mute ARCHITECTURE findings on converted code.

    Only the ARCHITECTURE tier is suppressible. UNIVERSAL findings describe
    things that are wrong regardless of how the code came to exist, and
    MIGRATION findings exist precisely because the code was converted.
    """
    if finding.tier != Tier.ARCHITECTURE:
        return
    if project is None or project.provenance is None:
        return
    verdict = project.provenance
    if not verdict.is_migration:
        return
    if verdict.covers(finding.file) or not finding.file:
        finding.suppressed = True
        finding.suppressed_reason = verdict.suppression_reason()


def _finding_sort_key(finding: Finding) -> tuple[Any, ...]:
    from dbt_audit.core.base import SEVERITY_RANK

    return (
        SEVERITY_RANK.get(finding.severity, 9),
        finding.category,
        finding.rule_id,
        finding.project,
        finding.file,
        finding.line or 0,
    )
