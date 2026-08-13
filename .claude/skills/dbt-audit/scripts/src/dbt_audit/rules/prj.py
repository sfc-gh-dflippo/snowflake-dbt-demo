"""
PRJ -- project structure and fragmentation.

Portfolio-scoped rules that look across every discovered dbt project rather than
inside one. The motivating case is a customer with a separate dbt project holding
one or two models each -- often the output of a per-data-flow conversion, where a
Snowflake Task graph replaces dbt's DAG.

That shape costs real capability: no cross-project ``ref()`` lineage, no single
``dbt build``, no project-wide tests or docs, and dependency order duplicated
into ``AFTER`` clauses that dbt cannot validate. All UNIVERSAL -- fragmentation
is a problem regardless of how it arose, and consolidating is the remedy either
way.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule
from dbt_audit.core.sqlutil import find_line_number, strip_comments_and_strings
from dbt_audit.provenance import PLACEHOLDER_VALUES

if TYPE_CHECKING:
    from dbt_audit.discovery import PortfolioContext, ProjectContext

CATEGORY = "PRJ"

PRJ_MICRO_PROJECT = "PRJ001"
PRJ_CONSOLIDATION = "PRJ002"
PRJ_DUPLICATED_CONFIG = "PRJ003"
PRJ_PROFILES_COMMITTED = "PRJ004"
PRJ_PLACEHOLDER_CONFIG = "PRJ005"
PRJ_TASK_ORCHESTRATION = "PRJ006"
PRJ_MISSING_PACKAGES = "PRJ007"
PRJ_ARTIFACTS_COMMITTED = "PRJ008"

EXECUTE_DBT_PATTERN = re.compile(r"\bEXECUTE\s+DBT\s+PROJECT\b", re.IGNORECASE)

#: Packages this project's own guidance treats as baseline.
EXPECTED_PACKAGES = {
    "dbt_utils": "dbt-labs/dbt_utils",
    "dbt_constraints": "Snowflake-Labs/dbt_constraints",
}

COMMITTED_ARTIFACT_DIRS = ("target", "logs", "dbt_packages")


# =============================================================================
# Fragmentation
# =============================================================================


@rule(
    PRJ_MICRO_PROJECT,
    "dbt project contains very few models",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    severity=Severity.WARNING,
    rationale=(
        "A dbt project is the unit of lineage, testing and documentation. Splitting a "
        "handful of models into their own project forfeits all three at the boundary, "
        "and multiplies the config, package and profile surface to maintain."
    ),
)
def micro_project(portfolio: PortfolioContext) -> Iterator[Finding]:
    threshold = portfolio.config.micro_project_threshold
    if len(portfolio.projects) < 2:
        # A single small project is a new or intentionally scoped repo, not
        # fragmentation. Fragmentation is a property of the estate.
        return

    for project in portfolio.projects:
        count = project.model_count
        if count > threshold:
            continue
        severity = Severity.WARNING if count <= 2 else Severity.RECOMMENDATION
        yield make_finding(
            PRJ_MICRO_PROJECT,
            f"Project `{project.name}` contains {count} model"
            f"{'' if count == 1 else 's'}, below the {threshold}-model threshold.",
            severity=severity,
            project=project.name,
            file=f"{project.relative_root}/dbt_project.yml",
            evidence=f"{count} model(s) in {project.relative_root}",
            remediation=(
                "Merge these models into a single project alongside their peers. One "
                "project gives you `ref()` lineage across the whole flow, a single "
                "`dbt build` that orders everything correctly, project-wide tests, and "
                "one set of docs. Keep separate projects only where there is a genuine "
                "ownership or release boundary."
            ),
            effort=Effort.HIGH,
            model_count=count,
        )


@rule(
    PRJ_CONSOLIDATION,
    "Multiple projects read the same sources",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    severity=Severity.WARNING,
    rationale=(
        "Projects sharing sources are working the same data with no lineage between "
        "them. dbt cannot order them, detect a conflict, or show the combined graph -- "
        "so the real dependency lives in whatever schedules them."
    ),
)
def consolidation_candidates(portfolio: PortfolioContext) -> Iterator[Finding]:
    if len(portfolio.projects) < 2:
        return

    by_source: dict[tuple[str, str], set[str]] = defaultdict(set)
    for project in portfolio.projects:
        for model in project.models:
            for source in model.sources:
                by_source[source].add(project.name)

    shared: dict[frozenset[str], list[tuple[str, str]]] = defaultdict(list)
    for source, project_names in by_source.items():
        if len(project_names) > 1:
            shared[frozenset(project_names)].append(source)

    for project_names, sources in shared.items():
        names = sorted(project_names)
        source_labels = [f"{s[0]}.{s[1]}" for s in sorted(sources)][:5]
        total_models = sum(
            p.model_count for p in portfolio.projects if p.name in project_names
        )
        yield make_finding(
            PRJ_CONSOLIDATION,
            f"{len(names)} projects ({', '.join(names)}) read the same source "
            f"table(s): {', '.join(source_labels)}"
            + (" ..." if len(sources) > 5 else "")
            + ". There is no lineage between them.",
            file="<portfolio>",
            evidence=f"shared sources: {', '.join(source_labels)}",
            remediation=(
                f"Consolidate these {len(names)} projects into one containing all "
                f"{total_models} models. Define each source once, let `ref()` express "
                "the ordering that is currently implicit in the scheduler, and run a "
                "single `dbt build`. If they must stay separate, at minimum ensure the "
                "shared source definitions are identical -- divergent freshness or "
                "quoting config on the same table is a silent inconsistency."
            ),
            effort=Effort.HIGH,
            projects=names,
        )


@rule(
    PRJ_TASK_ORCHESTRATION,
    "Projects chained by Snowflake Tasks instead of dbt lineage",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    severity=Severity.WARNING,
    rationale=(
        "EXECUTE DBT PROJECT inside a Task graph moves dependency ordering out of dbt. "
        "dbt can no longer validate the order, and a model added to one project will "
        "not automatically run before its consumer in another."
    ),
)
def task_orchestration(portfolio: PortfolioContext) -> Iterator[Finding]:
    hits: list[tuple[str, str, int]] = []
    for project in portfolio.projects:
        for path, raw in project.loose_sql:
            stripped = strip_comments_and_strings(raw)
            for match in EXECUTE_DBT_PATTERN.finditer(stripped):
                try:
                    relative = str(path.relative_to(portfolio.root))
                except ValueError:
                    relative = str(path)
                hits.append(
                    (project.name, relative, find_line_number(stripped, match.start()))
                )

    if len(hits) < 2:
        return

    files = sorted({path for _project, path, _line in hits})
    project_name, path, line = hits[0]
    yield make_finding(
        PRJ_TASK_ORCHESTRATION,
        f"{len(hits)} `EXECUTE DBT PROJECT` invocations across {len(files)} "
        "orchestration script(s) chain separate dbt projects through a Task graph.",
        project=project_name,
        file=path,
        line=line,
        evidence=f"EXECUTE DBT PROJECT found in: {', '.join(files[:5])}",
        remediation=(
            "Move the dependency into dbt. Once the models live in one project, "
            "`ref()` expresses the ordering and a single `dbt build` runs the whole "
            "graph in the correct sequence -- with the Task reduced to one scheduled "
            "trigger. Keep Tasks for scheduling, not for ordering."
        ),
        effort=Effort.HIGH,
        occurrence_count=len(hits),
    )


@rule(
    PRJ_DUPLICATED_CONFIG,
    "Project configuration duplicated across sibling projects",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "Near-identical config in many projects has to be updated in many places. In "
        "practice it is updated in one and drifts everywhere else."
    ),
)
def duplicated_config(portfolio: PortfolioContext) -> Iterator[Finding]:
    if len(portfolio.projects) < 3:
        return

    versions: dict[str, set[str]] = defaultdict(set)
    for project in portfolio.projects:
        for package in project.packages.get("packages") or []:
            if isinstance(package, dict) and package.get("package"):
                versions[str(package["package"])].add(
                    str(package.get("version", "unpinned"))
                )

    drifted = {name: sorted(vers) for name, vers in versions.items() if len(vers) > 1}

    yield make_finding(
        PRJ_DUPLICATED_CONFIG,
        f"{len(portfolio.projects)} projects each carry their own `dbt_project.yml` "
        "and `packages.yml`"
        + (
            f", and {len(drifted)} package(s) are already pinned to different "
            f"versions across them: "
            + "; ".join(f"{n} ({', '.join(v)})" for n, v in list(drifted.items())[:3])
            if drifted
            else "."
        ),
        file="<portfolio>",
        evidence=f"{len(portfolio.projects)} dbt_project.yml files under {portfolio.root.name}",
        remediation=(
            "Consolidate into one project so there is one config, one package set and "
            "one place to upgrade. Where multiple projects are genuinely required, "
            "pin package versions identically and keep the shared config in a single "
            "reviewed file."
        ),
        effort=Effort.HIGH,
        version_drift=drifted,
    )


# =============================================================================
# Per-project hygiene
# =============================================================================


@rule(
    PRJ_PROFILES_COMMITTED,
    "profiles.yml committed inside the project",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "profiles.yml holds connection and credential configuration. Committing it "
        "risks leaking secrets and pins every developer to one account."
    ),
)
def profiles_committed(project: ProjectContext) -> Iterator[Finding]:
    for name in ("profiles.yml", "profiles.yaml"):
        path = project.root / name
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = ""
        has_secret = bool(
            re.search(
                r"^\s*(password|private_key_passphrase|token)\s*:\s*\S",
                content,
                re.MULTILINE,
            )
        )
        yield make_finding(
            PRJ_PROFILES_COMMITTED,
            f"`{name}` is present in the project directory"
            + (" and contains a literal credential value." if has_secret else "."),
            severity=Severity.ERROR if has_secret else Severity.WARNING,
            file=name,
            evidence=f"{name} found at project root",
            remediation=(
                "Move it to `~/.dbt/profiles.yml` and add the path to `.gitignore`. "
                "Keep a redacted `profiles.yml.sample` in the repo for onboarding. If a "
                "credential was committed, rotate it -- git history retains it."
            ),
            effort=Effort.LOW,
        )


@rule(
    PRJ_PLACEHOLDER_CONFIG,
    "Unresolved placeholder values in project configuration",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "A placeholder means the project cannot parse or cannot resolve a relation. "
        "Nothing downstream -- tests, docs, lineage -- can be trusted until it is set."
    ),
)
def placeholder_config(project: ProjectContext) -> Iterator[Finding]:
    haystack = {
        "dbt_project.yml": str(project.project_yml),
        "packages.yml": str(project.packages),
    }
    for filename, text in haystack.items():
        found = sorted({p for p in PLACEHOLDER_VALUES if p in text})
        if not found:
            continue
        yield make_finding(
            PRJ_PLACEHOLDER_CONFIG,
            f"`{filename}` still contains converter placeholder value(s): {', '.join(found)}.",
            file=filename,
            evidence=", ".join(found),
            remediation=(
                "Replace each placeholder with the real project, profile, database or "
                "schema name. Note that some conversion tooling ships "
                "`sc_override_*_db`/`_schema` vars with placeholder defaults and "
                "expects them supplied via `--vars` at run time -- check whether the "
                "value belongs in the file or in the invocation before deleting it, "
                "because removing the var silently drops the override behaviour."
            ),
            effort=Effort.LOW,
        )


@rule(
    PRJ_MISSING_PACKAGES,
    "Baseline packages absent or version-drifted",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "dbt_constraints turns key assumptions into enforced database constraints and "
        "dbt_utils removes hand-rolled equivalents. Both are baseline in this estate."
    ),
)
def missing_packages(project: ProjectContext) -> Iterator[Finding]:
    if project.model_count == 0:
        return
    declared = {
        str(p.get("package", "")).split("/")[-1]
        for p in (project.packages.get("packages") or [])
        if isinstance(p, dict)
    }
    missing = [
        canonical
        for short, canonical in EXPECTED_PACKAGES.items()
        if short not in declared
    ]
    if not missing:
        return
    yield make_finding(
        PRJ_MISSING_PACKAGES,
        f"`packages.yml` does not declare: {', '.join(missing)}.",
        file="packages.yml",
        evidence=f"declared: {', '.join(sorted(declared)) or 'none'}",
        remediation=(
            "Add the missing packages and run `dbt deps`:\n\n"
            "```yaml\n"
            "packages:\n"
            "  - package: dbt-labs/dbt_utils\n"
            '    version: [">=1.0.0", "<2.0.0"]\n'
            "  - package: Snowflake-Labs/dbt_constraints\n"
            '    version: [">=1.0.0", "<2.0.0"]\n'
            "```\n\n"
            "dbt_constraints in particular converts the primary and foreign keys you "
            "already assume into constraints Snowflake enforces."
        ),
        effort=Effort.LOW,
        missing=missing,
    )


@rule(
    PRJ_ARTIFACTS_COMMITTED,
    "Build artifacts present in the project tree",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "target/ and dbt_packages/ are regenerated on every run. Committing them "
        "creates noisy diffs and can ship a stale manifest that misleads tooling."
    ),
)
def artifacts_committed(project: ProjectContext) -> Iterator[Finding]:
    gitignore = project.root / ".gitignore"
    ignored_text = ""
    if gitignore.is_file():
        try:
            ignored_text = gitignore.read_text(encoding="utf-8", errors="replace")
        except OSError:
            ignored_text = ""

    present = [
        name
        for name in COMMITTED_ARTIFACT_DIRS
        if (project.root / name).is_dir() and name not in ignored_text
    ]
    if not present:
        return
    yield make_finding(
        PRJ_ARTIFACTS_COMMITTED,
        f"Generated director{'y' if len(present) == 1 else 'ies'} "
        f"{', '.join(present)} present with no matching `.gitignore` entry.",
        file=".gitignore",
        evidence=f"unignored: {', '.join(present)}",
        remediation=(
            "Add to `.gitignore`:\n\n"
            "```\n" + "\n".join(f"{name}/" for name in present) + "\n```\n\n"
            "Then `git rm -r --cached` any that are already tracked."
        ),
        effort=Effort.LOW,
    )
