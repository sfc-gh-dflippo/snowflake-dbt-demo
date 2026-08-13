"""
Core types for the dbt audit: severity, tier, findings, and the rule registry.

Mirrors the conventions established in ``.claude/hooks/dbt-validation``
(``core/base.py``) so the two tools speak the same language:

- Three severity levels, of which only ERROR is build-blocking.
- Rule IDs are module-local string constants declared in each rule pack --
  there is no central ID table to edit when adding a rule.

Adds two concepts the hook does not need:

- **Tier** -- separates rules that are always valid (UNIVERSAL) from rules that
  encode a greenfield architectural ideal (ARCHITECTURE). ARCHITECTURE rules are
  suppressed for lift-and-shift migrations, where a medallion layout was never
  the goal. See ``provenance.py``.
- **Scope** -- lets a rule run per-model, per-project, or once across the whole
  portfolio, so project fragmentation can be judged across many dbt projects.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

# =============================================================================
# Constants
# =============================================================================


class Severity:
    """
    Severity levels for audit findings.

    - ERROR: broken or wrong -- will fail, silently corrupt data, or block a build
    - WARNING: should be addressed -- correctness or maintainability risk
    - RECOMMENDATION: best-practice improvement -- nice to have
    """

    ERROR: str = "error"
    WARNING: str = "warning"
    RECOMMENDATION: str = "recommendation"


#: Ordering used for sorting and for "worst severity" roll-ups.
SEVERITY_RANK: dict[str, int] = {
    Severity.ERROR: 0,
    Severity.WARNING: 1,
    Severity.RECOMMENDATION: 2,
}


class Tier:
    """
    Whether a rule survives a lift-and-shift migration.

    - UNIVERSAL: always applies. A truncate-and-load is wrong whether a human
      wrote it or a converter emitted it.
    - ARCHITECTURE: encodes a greenfield ideal (medallion folders, layer naming,
      layer-crossing lineage). Suppressed when provenance indicates the project
      was mechanically converted from Informatica/SSIS, because the customer
      never chose that layout. Reported once as a modernisation note instead.
    - MIGRATION: only meaningful *because* the project was converted -- e.g.
      unresolved conversion markers. Never suppressed; these are real defects.
    """

    UNIVERSAL: str = "universal"
    ARCHITECTURE: str = "architecture"
    MIGRATION: str = "migration"


class Scope:
    """What a rule function is called with."""

    MODEL: str = "model"  # once per model file
    PROJECT: str = "project"  # once per dbt project
    PORTFOLIO: str = "portfolio"  # once across all discovered projects


#: Effort hint used to rank remediation. Impact-over-effort ordering means a
#: cheap fix to a serious problem is surfaced before an expensive one.
class Effort:
    LOW: str = "low"
    MEDIUM: str = "medium"
    HIGH: str = "high"


EFFORT_RANK: dict[str, int] = {Effort.LOW: 1, Effort.MEDIUM: 2, Effort.HIGH: 3}


# =============================================================================
# Findings
# =============================================================================


@dataclass
class Finding:
    """
    A single audit finding.

    ``evidence`` is the concrete thing observed -- a SQL fragment, a config key,
    a count. It exists so a reader can verify the finding without re-deriving
    it, and so the HTML report can quote rather than paraphrase.
    """

    rule_id: str
    title: str
    severity: str
    tier: str
    category: str
    message: str
    project: str = ""
    file: str = ""
    line: int | None = None
    evidence: str = ""
    remediation: str = ""
    effort: str = Effort.MEDIUM
    #: Free-form extra context (related files, counts, other call sites).
    context: dict[str, Any] = field(default_factory=dict)
    #: Set when a rule fired but was muted by migration provenance.
    suppressed: bool = False
    suppressed_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "tier": self.tier,
            "category": self.category,
            "message": self.message,
            "project": self.project,
            "file": self.file,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "effort": self.effort,
        }
        if self.line is not None:
            out["line"] = self.line
        if self.context:
            out["context"] = self.context
        if self.suppressed:
            out["suppressed"] = True
            out["suppressed_reason"] = self.suppressed_reason
        return out


# =============================================================================
# Rule registry
# =============================================================================


@dataclass
class Rule:
    """Metadata plus the callable that implements one check."""

    rule_id: str
    title: str
    tier: str
    category: str
    scope: str
    fn: Callable[..., Iterator[Finding]]
    default_severity: str = Severity.WARNING
    requires_manifest: bool = False
    #: One-line statement of the best practice this rule protects, for the
    #: report's "why this matters" text and for the rule-catalog reference.
    rationale: str = ""


#: Populated at import time by the ``@rule`` decorator.
REGISTRY: dict[str, Rule] = {}


def rule(
    rule_id: str,
    title: str,
    *,
    tier: str = Tier.UNIVERSAL,
    category: str = "",
    scope: str = Scope.MODEL,
    severity: str = Severity.WARNING,
    requires_manifest: bool = False,
    rationale: str = "",
) -> Callable[[Callable[..., Iterator[Finding]]], Callable[..., Iterator[Finding]]]:
    """
    Register a rule implementation.

    The decorated function is a generator yielding ``Finding`` objects, and is
    called with arguments determined by ``scope``:

    - ``Scope.MODEL``     -> ``fn(model, project)``
    - ``Scope.PROJECT``   -> ``fn(project)``
    - ``Scope.PORTFOLIO`` -> ``fn(portfolio)``

    Yielding nothing means the check passed.
    """

    def decorator(
        fn: Callable[..., Iterator[Finding]],
    ) -> Callable[..., Iterator[Finding]]:
        if rule_id in REGISTRY:
            raise ValueError(f"Duplicate rule id: {rule_id}")
        REGISTRY[rule_id] = Rule(
            rule_id=rule_id,
            title=title,
            tier=tier,
            category=category or rule_id[:3],
            scope=scope,
            fn=fn,
            default_severity=severity,
            requires_manifest=requires_manifest,
            rationale=rationale,
        )
        return fn

    return decorator


def make_finding(
    rule_id: str,
    message: str,
    *,
    severity: str | None = None,
    file: str = "",
    line: int | None = None,
    evidence: str = "",
    remediation: str = "",
    effort: str = Effort.MEDIUM,
    project: str = "",
    **context: Any,
) -> Finding:
    """
    Build a ``Finding`` from a registered rule, inheriting its metadata.

    Rules call this rather than constructing ``Finding`` directly so title,
    tier, and category stay in one place (the registration) and cannot drift.
    """
    meta = REGISTRY[rule_id]
    return Finding(
        rule_id=rule_id,
        title=meta.title,
        severity=severity or meta.default_severity,
        tier=meta.tier,
        category=meta.category,
        message=message,
        project=project,
        file=file,
        line=line,
        evidence=evidence,
        remediation=remediation,
        effort=effort,
        context=context,
    )
