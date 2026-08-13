"""
Scoring and the findings.json contract.

Two decisions worth stating, because both affect how a customer reads the grade:

1. **Suppressed findings are excluded from the score, not zeroed.** A converted
   project is not penalised for architecture it never chose, but the report says
   how many findings were suppressed and why, so the grade cannot be mistaken for
   "no architectural debt".

2. **Remediation is ranked by impact over effort**, not by severity alone. A
   one-line fix to a serious problem should be addressed before a multi-week
   refactor of a moderate one, and a severity-only sort hides that.

The score is deliberately a blunt instrument: it exists to direct attention, and
the findings list is the actual product.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dbt_audit.core.base import EFFORT_RANK, REGISTRY, Finding, Severity
from dbt_audit.engine import AuditResult

SCHEMA_VERSION = "1.0"

#: Per-finding penalty by severity. Deducted from 100, weighted by category.
SEVERITY_PENALTY: dict[str, float] = {
    Severity.ERROR: 10.0,
    Severity.WARNING: 4.0,
    Severity.RECOMMENDATION: 1.0,
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

#: Findings are converted to a size-normalised density, then mapped to a score by
#: a hyperbolic curve: score = 100 / (1 + density / tolerance).
#:
#: A curve rather than subtraction because subtraction saturates -- any project
#: with a few dozen findings floors at zero, which makes a bad project and a
#: catastrophic one indistinguishable. The curve stays monotonic and informative
#: across the whole range, and a clean project still scores near 100.
#:
#: Tolerance is the density at which the score reaches 50.
OVERALL_TOLERANCE = 15.0
CATEGORY_TOLERANCE = 2.5

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


def grade(score: float) -> str:
    """Letter grade for a 0-100 score."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


@dataclass
class CategoryScore:
    category: str
    label: str
    score: float
    error: int = 0
    warning: int = 0
    recommendation: int = 0

    @property
    def total(self) -> int:
        return self.error + self.warning + self.recommendation

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "label": self.label,
            "score": round(self.score, 1),
            "grade": grade(self.score),
            "error": self.error,
            "warning": self.warning,
            "recommendation": self.recommendation,
            "total": self.total,
        }


@dataclass
class Scorecard:
    score: float = 100.0
    categories: list[CategoryScore] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 1),
            "grade": grade(self.score),
            "counts": self.counts,
            "categories": [c.to_dict() for c in self.categories],
        }


def score_findings(findings: list[Finding], model_count: int) -> Scorecard:
    """
    Score a set of findings, normalised by project size.

    Normalisation matters: 20 findings in a 10-model project is a different
    situation from 20 in a 500-model project, and an un-normalised count would
    always rank the large project worst.
    """
    card = Scorecard()
    active = [f for f in findings if not f.suppressed]
    card.counts = {
        "error": sum(1 for f in active if f.severity == Severity.ERROR),
        "warning": sum(1 for f in active if f.severity == Severity.WARNING),
        "recommendation": sum(
            1 for f in active if f.severity == Severity.RECOMMENDATION
        ),
        "suppressed": sum(1 for f in findings if f.suppressed),
        "total": len(active),
    }

    # Floor the divisor so a two-model project is not scored on a knife edge.
    scale = max(model_count, 5)
    by_category: dict[str, list[Finding]] = defaultdict(list)
    for finding in active:
        by_category[finding.category].append(finding)

    weighted_density = 0.0
    for category in sorted(set(CATEGORY_WEIGHT) | set(by_category)):
        items = by_category.get(category, [])
        counts = Counter(f.severity for f in items)
        points = sum(SEVERITY_PENALTY.get(sev, 1.0) * n for sev, n in counts.items())
        density = points / scale
        weighted_density += density * CATEGORY_WEIGHT.get(category, 1.0)
        card.categories.append(
            CategoryScore(
                category=category,
                label=CATEGORY_LABELS.get(category, category),
                score=100.0 / (1.0 + density / CATEGORY_TOLERANCE),
                error=counts.get(Severity.ERROR, 0),
                warning=counts.get(Severity.WARNING, 0),
                recommendation=counts.get(Severity.RECOMMENDATION, 0),
            )
        )

    card.score = 100.0 / (1.0 + weighted_density / OVERALL_TOLERANCE)
    return card


def rank_remediation(findings: list[Finding], limit: int = 20) -> list[dict[str, Any]]:
    """
    Group findings by rule and rank by impact over effort.

    Grouping matters as much as ranking: "43 models lack a primary-key test" is
    one piece of work, and presenting it as 43 separate items makes the report
    unreadable and the effort look larger than it is.
    """
    groups: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        if not finding.suppressed:
            groups[finding.rule_id].append(finding)

    ranked: list[dict[str, Any]] = []
    for rule_id, items in groups.items():
        worst = min(items, key=lambda f: SEVERITY_PENALTY.get(f.severity, 0) * -1)
        severity_weight = SEVERITY_PENALTY.get(worst.severity, 1.0)
        category_weight = CATEGORY_WEIGHT.get(worst.category, 1.0)
        effort = min(EFFORT_RANK.get(f.effort, 2) for f in items)
        # Count is dampened with a log-like curve so one very common low-severity
        # rule cannot outrank a critical one.
        impact = severity_weight * category_weight * (1 + min(len(items), 25) / 25)
        ranked.append(
            {
                "rule_id": rule_id,
                "title": (
                    REGISTRY[rule_id].title if rule_id in REGISTRY else worst.title
                ),
                "rationale": REGISTRY[rule_id].rationale if rule_id in REGISTRY else "",
                "category": worst.category,
                "category_label": CATEGORY_LABELS.get(worst.category, worst.category),
                "severity": worst.severity,
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
    Assemble the findings.json payload the HTML report step consumes.

    This dict is the contract between the analyzer and the report. Adding a key is
    safe; renaming or removing one is a breaking change and requires a
    ``schema_version`` bump.
    """
    total_models = sum(int(p["model_count"]) for p in result.projects)
    overall = score_findings(result.findings, total_models)

    per_project: list[dict[str, Any]] = []
    for project in result.projects:
        name = project["name"]
        project_findings = [f for f in result.findings if f.project == name]
        card = score_findings(project_findings, int(project["model_count"]))
        per_project.append({**project, "scorecard": card.to_dict()})

    manifest_available = [p for p in result.projects if p["manifest"]]
    suppressed = [f for f in result.findings if f.suppressed]
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
        "remediation": rank_remediation(result.findings),
        "findings": [f.to_dict() for f in result.findings],
        "suppressed": {
            "count": len(suppressed),
            "by_rule": dict(suppressed_by_rule),
            "reason": suppressed[0].suppressed_reason if suppressed else "",
            "note": (
                (
                    "Architecture-tier findings were withheld because these models are "
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
                "default_severity": meta.default_severity,
                "requires_manifest": meta.requires_manifest,
                "rationale": meta.rationale,
            }
            for meta in sorted(REGISTRY.values(), key=lambda m: m.rule_id)
        ],
    }
