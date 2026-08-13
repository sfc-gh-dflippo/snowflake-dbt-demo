"""
Scoring and the suggestions.json contract.

Two decisions worth stating, because both affect how a customer reads the grade:

1. **Suppressed suggestions are excluded from the score, not zeroed.** A converted
   project is not penalised for architecture it never chose, but the report says
   how many suggestions were suppressed and why, so the grade cannot be mistaken for
   "no architectural debt".

2. **Remediation is ranked by impact over effort**, not by level alone. A
   one-line fix to a serious problem should be addressed before a multi-week
   refactor of a moderate one, and a level-only sort hides that.

The score is deliberately a blunt instrument: it exists to direct attention, and
the suggestions list is the actual product.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dbt_quality.core.base import (
    EFFORT_RANK,
    REGISTRY,
    Level,
    Severity,
    Suggestion,
)
from dbt_quality.engine import AuditResult

SCHEMA_VERSION = "3.0"

#: Per-suggestion weight by level, used to rank remediation.
LEVEL_PENALTY: dict[str, float] = {
    Level.ERROR: 10.0,
    Level.WARNING: 4.0,
    Level.INFORMATION: 1.0,
}

#: Category weight. Correctness categories cost more than stylistic ones, so a
#: project with clean load mechanics and patchy docs outscores the reverse.
CATEGORY_WEIGHT: dict[str, float] = {
    "INC": 1.5,  # wrong load behaviour corrupts data
    "MIG": 1.4,  # unresolved conversion debt blocks compilation
    "TST": 1.2,  # no early warning system
    "SQL": 1.0,
    "PRJ": 1.0,
    "MAT": 0.9,
    "MAC": 0.7,
    "ARC": 0.6,
    "OPS": 0.6,
    "DOC": 0.4,  # matters, but breaks nothing
}


CATEGORY_LABELS: dict[str, str] = {
    "PRJ": "Project structure & fragmentation",
    "INC": "Load patterns & incremental",
    "SQL": "Query construction",
    "MAC": "Macro discipline",
    "MAT": "Materialization fitness",
    "TST": "Testing & constraints",
    "DOC": "Documentation",
    "ARC": "Architecture & lineage",
    "MIG": "Migration debt",
    "OPS": "Operational hygiene",
}


@dataclass
class CategoryCount:
    """Per-category suggestion counts, plus a size-normalised rate."""

    category: str
    label: str
    error: int = 0
    warning: int = 0
    information: int = 0
    model_count: int = 0

    @property
    def total(self) -> int:
        return self.error + self.warning + self.information

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "label": self.label,
            "error": self.error,
            "warning": self.warning,
            "information": self.information,
            "total": self.total,
            "per_model": _per_model(self.total, self.model_count),
        }


@dataclass
class Tally:
    """Counts of suggestions overall and by category."""

    categories: list[CategoryCount] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    model_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "counts": self.counts,
            "per_model": _per_model(self.counts.get("total", 0), self.model_count),
            "categories": [c.to_dict() for c in self.categories],
        }


def _per_model(total: int, model_count: int) -> float:
    """
    Suggestions per model.

    Reported alongside the raw counts because counts alone are not comparable
    across projects of different sizes -- 20 suggestions in a 10-model project is a
    different situation from 20 in a 500-model one. This is what replaced the old
    normalised score, and it is the number to watch across runs.
    """
    if model_count <= 0:
        return 0.0
    return round(total / model_count, 2)


def tally_suggestions(suggestions: list[Suggestion], model_count: int) -> Tally:
    """
    Count suggestions overall and per category.

    There is deliberately no score and no letter grade. A grade asserts a verdict on
    the project, and this engine does not have the context to justify one: most rules
    test a heuristic whose applicability only the reader can settle, so aggregating
    them into "F" states something the engine cannot know. Counts and a per-model
    rate say exactly what was observed and nothing more.
    """
    active = [f for f in suggestions if not f.suppressed]
    tally = Tally(model_count=model_count)
    tally.counts = {
        "error": sum(1 for f in active if f.level == Level.ERROR),
        "warning": sum(1 for f in active if f.level == Level.WARNING),
        "information": sum(1 for f in active if f.level == Level.INFORMATION),
        # Severity is a second, independent axis: level is how confident we are that
        # something is wrong, severity is the consequence if it is. Both are counted
        # because a project can have few errors and still carry critical exposure.
        "critical": sum(1 for f in active if f.severity == Severity.CRITICAL),
        "high": sum(1 for f in active if f.severity == Severity.HIGH),
        "medium": sum(1 for f in active if f.severity == Severity.MEDIUM),
        "low": sum(1 for f in active if f.severity == Severity.LOW),
        "suppressed": sum(1 for f in suggestions if f.suppressed),
        "total": len(active),
    }

    by_category: dict[str, list[Suggestion]] = defaultdict(list)
    for suggestion in active:
        by_category[suggestion.category].append(suggestion)

    for category in sorted(set(CATEGORY_WEIGHT) | set(by_category)):
        counts = Counter(f.level for f in by_category.get(category, []))
        tally.categories.append(
            CategoryCount(
                category=category,
                label=CATEGORY_LABELS.get(category, category),
                error=counts.get(Level.ERROR, 0),
                warning=counts.get(Level.WARNING, 0),
                information=counts.get(Level.INFORMATION, 0),
                model_count=model_count,
            )
        )
    return tally


def rank_remediation(
    suggestions: list[Suggestion], limit: int = 20
) -> list[dict[str, Any]]:
    """
    Group suggestions by rule and rank by impact over effort.

    Grouping matters as much as ranking: "43 models lack a primary-key test" is
    one piece of work, and presenting it as 43 separate items makes the report
    unreadable and the effort look larger than it is.
    """
    groups: dict[str, list[Suggestion]] = defaultdict(list)
    for suggestion in suggestions:
        if not suggestion.suppressed:
            groups[suggestion.rule_id].append(suggestion)

    ranked: list[dict[str, Any]] = []
    for rule_id, items in groups.items():
        worst = min(items, key=lambda f: LEVEL_PENALTY.get(f.level, 0) * -1)
        level_weight = LEVEL_PENALTY.get(worst.level, 1.0)
        category_weight = CATEGORY_WEIGHT.get(worst.category, 1.0)
        effort = min(EFFORT_RANK.get(f.effort, 2) for f in items)
        # Count is dampened with a log-like curve so one very common low-level
        # rule cannot outrank a critical one.
        impact = level_weight * category_weight * (1 + min(len(items), 25) / 25)
        ranked.append(
            {
                "rule_id": rule_id,
                "title": (
                    REGISTRY[rule_id].title if rule_id in REGISTRY else worst.title
                ),
                "rationale": REGISTRY[rule_id].rationale if rule_id in REGISTRY else "",
                "category": worst.category,
                "category_label": CATEGORY_LABELS.get(worst.category, worst.category),
                "level": worst.level,
                "tier": worst.tier,
                "effort": worst.effort,
                "count": len(items),
                "priority": round(impact / effort, 3),
                "remediation": worst.remediation,
                "affected_files": sorted({f.file for f in items if f.file})[:10],
                "example": {
                    "file": worst.file,
                    "line": worst.line,
                    "message": worst.message,
                    "evidence": worst.evidence,
                },
            }
        )

    ranked.sort(key=lambda item: (-item["priority"], item["rule_id"]))
    return ranked[:limit]


def build_report(result: AuditResult, root: str) -> dict[str, Any]:
    """
    Assemble the suggestions.json payload the HTML report step consumes.

    This dict is the contract between the analyzer and the report. Adding a key is
    safe; renaming or removing one is a breaking change and requires a
    ``schema_version`` bump -- as happened when ``findings`` became ``suggestions``
    and ``score``/``grade`` were dropped in favour of counts.
    """
    total_models = sum(int(p["model_count"]) for p in result.projects)
    overall = tally_suggestions(result.suggestions, total_models)

    per_project: list[dict[str, Any]] = []
    for project in result.projects:
        name = project["name"]
        project_suggestions = [f for f in result.suggestions if f.project == name]
        tally = tally_suggestions(project_suggestions, int(project["model_count"]))
        per_project.append({**project, "tally": tally.to_dict()})

    manifest_available = [p for p in result.projects if p["manifest"]]
    suppressed = [f for f in result.suggestions if f.suppressed]
    suppressed_by_rule = Counter(f.rule_id for f in suppressed)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated": datetime.now(UTC).isoformat(timespec="seconds"),
        "root": root,
        "summary": {
            "project_count": len(result.projects),
            "model_count": total_models,
            "manifest_coverage": f"{len(manifest_available)}/{len(result.projects)}",
            "rules_registered": len(REGISTRY),
            "rules_skipped": len(result.skipped),
            **overall.to_dict(),
        },
        "projects": per_project,
        "remediation": rank_remediation(result.suggestions),
        "suggestions": [f.to_dict() for f in result.suggestions],
        "suppressed": {
            "count": len(suppressed),
            "by_rule": dict(suppressed_by_rule),
            "reason": suppressed[0].suppressed_reason if suppressed else "",
            "note": (
                (
                    "Architecture-tier suggestions were withheld because these models are "
                    "mechanically converted lift-and-shift output. They are opportunities "
                    "for a later modernisation pass, not defects introduced by this team, "
                    "and they do not affect the score."
                )
                if suppressed
                else ""
            ),
        },
        "skipped_checks": [
            {"rule_id": s.rule_id, "title": s.title, "reason": s.reason}
            for s in result.skipped
        ],
        "errors": result.errors,
        "rule_catalog": [
            {
                "rule_id": meta.rule_id,
                "title": meta.title,
                "category": meta.category,
                "category_label": CATEGORY_LABELS.get(meta.category, meta.category),
                "tier": meta.tier,
                "default_level": meta.default_level,
                "requires_manifest": meta.requires_manifest,
                "rationale": meta.rationale,
            }
            for meta in sorted(REGISTRY.values(), key=lambda m: m.rule_id)
        ],
    }
