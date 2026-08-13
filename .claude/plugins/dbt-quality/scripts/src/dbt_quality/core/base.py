"""
Core types for the dbt audit: levels, tiers, suggestions, and the rule registry.

- Three orthogonal axes on every suggestion: ``kind`` (EWI/FDM/PRF, the issue
  family), ``level`` (error/warning/information, confidence), and ``severity``
  (critical/high/medium/low, blast radius if the rule is right). None of them is
  build-blocking, because a suggestion is not a defect.
- Rule codes follow SnowConvert's own convention, ``SSC-{KIND}-DBT{CAT}{NNNN}``,
  adopted for consistency since this engine is maintained by the SnowConvert team.
- Rule IDs are module-local string constants declared in each rule pack --
  there is no central ID table to edit when adding a rule.

Two further concepts:

- **Tier** -- separates rules that are always valid (UNIVERSAL) from rules that
  encode a greenfield architectural ideal (ARCHITECTURE). ARCHITECTURE rules are
  suppressed for lift-and-shift migrations, where a medallion layout was never
  the goal. See ``provenance.py``.
- **Scope** -- lets a rule run per-model, per-project, or once across the whole
  portfolio, so project fragmentation can be judged across many dbt projects.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

# =============================================================================
# Constants
# =============================================================================


class Kind:
    """
    Which family of issue a rule belongs to, mirroring SnowConvert.

    - EWI: a conversion or quality issue
    - FDM: a functional difference -- the model's results differ from what the
      source system produced, or a declared behavioural difference
    - PRF: a performance or cost concern

    The kind appears in the rule code (``SSC-FDM-DBTSQL0008``), so it is visible
    wherever the code is, without needing to look the rule up.
    """

    EWI: str = "EWI"
    FDM: str = "FDM"
    PRF: str = "PRF"


class Level:
    """
    How confident the engine is that something is actually wrong -- the E/W/I of
    SnowConvert's "Error, Warning, and Information".

    - ERROR: no legitimate condition makes this correct. The project is broken,
      will not compile, silently produces nothing, or exposes a secret.
    - WARNING: a real problem in nearly all cases, with narrow exceptions.
    - INFORMATION: genuinely context-dependent -- only the reader can settle
      whether it applies. **This is the default.**

    Most rules here test a heuristic whose applicability the engine cannot
    establish: an incremental model with no ``unique_key`` is correct when the load
    is append-only, and a flat query is correct when it is short. Those are
    ``INFORMATION``.

    The invariant that ties this to the message text: every message states a fact,
    and the level decides *which kind* of fact. An ``ERROR`` names the defect. An
    ``INFORMATION`` names only the observation, and leaves the verdict to the
    reader. A rule may not hedge ("check whether ...") to signal low confidence,
    nor assert a defect it cannot establish -- the level carries the confidence, so
    the prose does not have to.
    """

    ERROR: str = "error"
    WARNING: str = "warning"
    INFORMATION: str = "information"


class Severity:
    """
    How bad the consequence is *if* the issue is real. SnowConvert carries this
    alongside the E/W/I kind, and the two are deliberately orthogonal here.

    - CRITICAL: secret exposure, data loss or corruption, or a model that builds
      successfully while silently producing nothing
    - HIGH: wrong results
    - MEDIUM: avoidable cost, or maintainability that will bite
    - LOW: style and consistency

    Why both axes: ``level`` is confidence, ``severity`` is blast radius. A rule can
    be ``INFORMATION`` (only the reader can tell whether it applies) and yet
    ``CRITICAL`` (if it does apply, data is lost). One axis cannot express that, and
    collapsing them would force a choice between crying wolf and under-reporting.
    """

    CRITICAL: str = "critical"
    HIGH: str = "high"
    MEDIUM: str = "medium"
    LOW: str = "low"


#: Ordering used for sorting and for "most pressing level" roll-ups.
LEVEL_RANK: dict[str, int] = {
    Level.ERROR: 0,
    Level.WARNING: 1,
    Level.INFORMATION: 2,
}

#: Ordering for severity, independent of level.
SEVERITY_RANK: dict[str, int] = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.MEDIUM: 2,
    Severity.LOW: 3,
}

#: Level -> the severity token a VS Code problem matcher can parse.
#:
#: A matcher recognises only ``error``, ``warning`` and ``info``, so the mapping is
#: forced. Unlike the previous vocabulary, ``error`` is now reachable -- because
#: ``Level.ERROR`` means genuinely wrong rather than merely worth checking.
LINT_TOKENS: dict[str, str] = {
    Level.ERROR: "error",
    Level.WARNING: "warning",
    Level.INFORMATION: "info",
}

#: Rule code format, following SnowConvert: ``SSC-{KIND}-DBT{CATEGORY}{NNNN}``.
#:
#: ``SSC`` is SnowConvert's own prefix, adopted for consistency with its
#: documentation. ``DBT`` reserves a domain inside that namespace for this engine --
#: SnowConvert already emits dbt-related codes under its own domains (for example
#: ``SSC-EWI-SSIS0033``), so the ``DBT`` segment is what distinguishes a suggestion
#: from this tool from a conversion issue emitted during a migration.
#:
#: The category is the three letters after ``DBT``. It is parsed from here rather
#: than sliced off the front of the ID, which would yield ``"SSC"`` for every rule.
CODE_PATTERN = re.compile(r"^SSC-(EWI|FDM|PRF)-DBT([A-Z]{3})(\d{4})$")


def parse_code(rule_id: str) -> tuple[str, str, int]:
    """
    Split a rule code into its kind, category and number.

    Raises on a malformed code rather than returning a default. A silently wrong
    category would mis-file every suggestion in the report without any error, which
    is far more expensive to notice than a failure at import time.
    """
    match = CODE_PATTERN.match(rule_id)
    if match is None:
        raise ValueError(
            f"rule id {rule_id!r} does not match SSC-{{EWI|FDM|PRF}}-DBT<CAT><NNNN>"
        )
    kind, category, number = match.groups()
    return kind, category, int(number)


def build_code(kind: str, category: str, number: int) -> str:
    """Assemble a rule code. The inverse of :func:`parse_code`."""
    return f"SSC-{kind}-DBT{category}{number:04d}"


def plural(count: int, singular: str, many: str = "") -> str:
    """
    Count a noun without the ``model(s)`` tic: ``1 model``, ``3 models``.

    Messages interpolate a real count, so the parenthetical plural is never
    needed. Pass ``many`` for an irregular plural. Verb agreement stays at the
    call site, since only the sentence knows which verb follows.
    """
    return f"{count} {singular if count == 1 else many or singular + 's'}"


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
# Suggestions
# =============================================================================


@dataclass
class Suggestion:
    """
    A single audit suggestion.

    ``evidence`` is the concrete thing observed -- a SQL fragment, a config key,
    a count. It exists so a reader can verify the finding without re-deriving
    it, and so the HTML report can quote rather than paraphrase.
    """

    rule_id: str
    title: str
    kind: str
    level: str
    severity: str
    tier: str
    category: str
    message: str
    project: str = ""
    file: str = ""
    line: int | None = None
    #: 1-based column, only set when a rule matched a real character offset.
    column: int | None = None
    #: End of the matched span. ``end_column`` is exclusive -- it points one past
    #: the last character, matching VS Code's ``endColumn``. Only set alongside
    #: ``column``, and under the current clamp ``end_line`` always equals ``line``.
    end_line: int | None = None
    end_column: int | None = None
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
            "kind": self.kind,
            "level": self.level,
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
        if self.column:
            out["column"] = self.column
        if self.end_line:
            out["end_line"] = self.end_line
        if self.end_column:
            out["end_column"] = self.end_column
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
    fn: Callable[..., Iterator[Suggestion]]
    kind: str = Kind.EWI
    default_level: str = Level.INFORMATION
    default_severity: str = Severity.MEDIUM
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
    kind: str = Kind.EWI,
    level: str = Level.INFORMATION,
    severity: str = Severity.MEDIUM,
    requires_manifest: bool = False,
    rationale: str = "",
) -> Callable[
    [Callable[..., Iterator[Suggestion]]], Callable[..., Iterator[Suggestion]]
]:
    """
    Register a rule implementation.

    The decorated function is a generator yielding ``Suggestion`` objects, and is
    called with arguments determined by ``scope``:

    - ``Scope.MODEL``     -> ``fn(model, project)``
    - ``Scope.PROJECT``   -> ``fn(project)``
    - ``Scope.PORTFOLIO`` -> ``fn(portfolio)``

    Yielding nothing means the check passed.
    """

    def decorator(
        fn: Callable[..., Iterator[Suggestion]],
    ) -> Callable[..., Iterator[Suggestion]]:
        if rule_id in REGISTRY:
            raise ValueError(f"Duplicate rule id: {rule_id}")
        # Validate the code and take the category from its domain segment. Never
        # slice the front of the ID: that is "SSC" for every rule, which would
        # silently collapse all ten categories into one without raising.
        parsed_kind, parsed_category, _ = parse_code(rule_id)
        if kind != parsed_kind:
            raise ValueError(
                f"{rule_id}: kind={kind!r} contradicts the code's {parsed_kind!r}"
            )
        REGISTRY[rule_id] = Rule(
            rule_id=rule_id,
            title=title,
            tier=tier,
            category=category or parsed_category,
            scope=scope,
            fn=fn,
            kind=kind,
            default_level=level,
            default_severity=severity,
            requires_manifest=requires_manifest,
            rationale=rationale,
        )
        return fn

    return decorator


def make_suggestion(
    rule_id: str,
    message: str,
    *,
    level: str | None = None,
    severity: str | None = None,
    file: str = "",
    line: int | None = None,
    column: int | None = None,
    end_line: int | None = None,
    end_column: int | None = None,
    evidence: str = "",
    remediation: str = "",
    effort: str = Effort.MEDIUM,
    project: str = "",
    **context: Any,
) -> Suggestion:
    """
    Build a ``Suggestion`` from a registered rule, inheriting its metadata.

    Rules call this rather than constructing ``Suggestion`` directly so title,
    tier, and category stay in one place (the registration) and cannot drift.

    Every keyword here must appear in the ``Suggestion(...)`` call below. A
    parameter accepted here and not forwarded is silently swallowed: ``column``
    was declared and never forwarded, so every diagnostic reported column 1 and
    the ``if self.column`` branch in ``to_dict`` was unreachable. Anything not
    named explicitly lands in ``**context`` instead, which is why the SQL column
    name is passed as ``column_name`` -- ``column`` here is a character offset.
    """
    meta = REGISTRY[rule_id]
    return Suggestion(
        rule_id=rule_id,
        title=meta.title,
        kind=meta.kind,
        level=level or meta.default_level,
        severity=severity or meta.default_severity,
        tier=meta.tier,
        category=meta.category,
        message=message,
        project=project,
        file=file,
        line=line,
        column=column,
        end_line=end_line,
        end_column=end_column,
        evidence=evidence,
        remediation=remediation,
        effort=effort,
        context=context,
    )
