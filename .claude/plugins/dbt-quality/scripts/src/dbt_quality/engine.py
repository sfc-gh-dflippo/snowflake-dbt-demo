"""
The audit runner.

Dispatches registered rules by scope, applies migration-tier suppression, and
records which rules could not run so the report can distinguish "checked and
clean" from "not checked".
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dbt_quality import rules as _rules  # noqa: F401  -- import registers all packs
from dbt_quality.core.anchors import resolve_position
from dbt_quality.core.base import REGISTRY, Scope, Suggestion, Tier
from dbt_quality.discovery import PortfolioContext, ProjectContext
from dbt_quality.provenance import classify


@dataclass
class SkippedRule:
    """A rule that did not run, and why -- surfaced in the report appendix."""

    rule_id: str
    title: str
    reason: str


@dataclass
class AuditResult:
    """Everything one audit run produced."""

    suggestions: list[Suggestion] = field(default_factory=list)
    skipped: list[SkippedRule] = field(default_factory=list)
    #: Per-project metadata for the report header.
    projects: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def active_suggestions(self) -> list[Suggestion]:
        """Suggestions that count toward the score (suppressed ones excluded)."""
        return [f for f in self.suggestions if not f.suppressed]


def _safe_iter(fn: Any, *args: Any) -> Iterator[Suggestion]:
    """
    Run one rule, converting an exception into a diagnostic rather than
    aborting the whole audit.

    A rule crashing on unusual SQL must not cost the user every other suggestion,
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
                SkippedRule(rule_id, meta.title, "disabled in .dbt-quality.yml")
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

    result.suggestions.sort(key=_finding_sort_key)
    return result


def run_single_file(portfolio: PortfolioContext, target: Path) -> AuditResult:
    """
    Run only the model-scoped rules that apply to one file.

    Used by the editor hook, where the unit of work is a file just written rather
    than a project. The project context is still built in full -- a model cannot be
    judged without its ``dbt_project.yml`` folder defaults and its schema YAML entry
    -- but rules are then dispatched for the single target model.

    Project- and portfolio-scoped rules are reported as **skipped**, not passed.
    Several of them are unanswerable from one file by nature: ``SQL001`` decides
    between a CTE and an ephemeral model by fingerprinting the same subquery across
    every model, and fragmentation is a property of the estate. Reporting them as
    clean would assert something this invocation never checked.
    """
    result = AuditResult()
    config = portfolio.config
    disabled = set(config.disabled_rules)

    resolved = target.resolve()
    located: tuple[ProjectContext, Any] | None = None
    for project in portfolio.projects:
        project.provenance = classify(project)
        for model in project.models:
            if model.path.resolve() == resolved:
                located = (project, model)
                break
        if located:
            break

    if located is None:
        # Out of scope: not a model in any discovered project. Silent success, so
        # the hook stays quiet on the many files that are not dbt models.
        return result

    project, model = located
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
                SkippedRule(rule_id, meta.title, "disabled in .dbt-quality.yml")
            )
            continue
        if meta.scope != Scope.MODEL:
            result.skipped.append(
                SkippedRule(
                    rule_id,
                    meta.title,
                    f"{meta.scope}-scoped: needs the whole project, run `dbt-audit`",
                )
            )
            continue
        if meta.requires_manifest and not project.graph.available:
            result.skipped.append(
                SkippedRule(rule_id, meta.title, "needs target/manifest.json")
            )
            continue
        _collect(result, meta, _safe_iter(meta.fn, model, project), project)

    result.suggestions.sort(key=_finding_sort_key)
    return result


def _collect(
    result: AuditResult,
    meta: Any,
    suggestions: Iterator[Suggestion],
    project: ProjectContext | None,
) -> None:
    """Attach project attribution, apply suppression, and record the suggestions."""
    try:
        produced = list(suggestions)
    except RuntimeError as exc:
        result.errors.append(f"rule {meta.rule_id} failed: {exc}")
        result.skipped.append(
            SkippedRule(meta.rule_id, meta.title, f"rule error: {exc}")
        )
        return

    for suggestion in produced:
        if project is not None and not suggestion.project:
            suggestion.project = project.name
        # Resolve an anchor for any rule that did not supply one, so no suggestion
        # ever ships without a line. The linter depends on this invariant. The
        # column stays None when it cannot be justified -- see resolve_position.
        suggestion.line, suggestion.column = resolve_position(suggestion, project)
        _apply_suppression(suggestion, project)
        result.suggestions.append(suggestion)


def _apply_suppression(suggestion: Suggestion, project: ProjectContext | None) -> None:
    """
    Mute ARCHITECTURE suggestions on converted code.

    Only the ARCHITECTURE tier is suppressible. UNIVERSAL suggestions describe
    things that are wrong regardless of how the code came to exist, and
    MIGRATION suggestions exist precisely because the code was converted.
    """
    if suggestion.tier != Tier.ARCHITECTURE:
        return
    if project is None or project.provenance is None:
        return
    verdict = project.provenance
    if not verdict.is_migration:
        return
    if verdict.covers(suggestion.file) or not suggestion.file:
        suggestion.suppressed = True
        suggestion.suppressed_reason = verdict.suppression_reason()


def _finding_sort_key(suggestion: Suggestion) -> tuple[Any, ...]:
    from dbt_quality.core.base import LEVEL_RANK

    return (
        LEVEL_RANK.get(suggestion.level, 9),
        suggestion.category,
        suggestion.rule_id,
        suggestion.project,
        suggestion.file,
        suggestion.line or 0,
    )
