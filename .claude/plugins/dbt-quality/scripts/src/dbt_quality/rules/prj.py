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

import ast
import re
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING

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
from dbt_quality.core.sqlutil import span, strip_comments_and_strings
from dbt_quality.provenance import PLACEHOLDER_VALUES

if TYPE_CHECKING:
    from dbt_quality.discovery import PortfolioContext, ProjectContext

CATEGORY = "PRJ"

PRJ_MICRO_PROJECT = "SSC-EWI-DBTPRJ0001"
PRJ_CONSOLIDATION = "SSC-EWI-DBTPRJ0002"
PRJ_DUPLICATED_CONFIG = "SSC-EWI-DBTPRJ0003"
PRJ_PROFILES_COMMITTED = "SSC-EWI-DBTPRJ0004"
PRJ_PLACEHOLDER_CONFIG = "SSC-EWI-DBTPRJ0005"
PRJ_TASK_ORCHESTRATION = "SSC-EWI-DBTPRJ0006"
PRJ_MISSING_PACKAGES = "SSC-EWI-DBTPRJ0007"
PRJ_ARTIFACTS_COMMITTED = "SSC-EWI-DBTPRJ0008"

EXECUTE_DBT_PATTERN = re.compile(r"\bEXECUTE\s+DBT\s+PROJECT\b", re.IGNORECASE)

#: Packages this project's own guidance treats as baseline.
EXPECTED_PACKAGES = {
    "dbt_constraints": "Snowflake-Labs/dbt_constraints",
    "dbt_semantic_view": "Snowflake-Labs/dbt_semantic_view",
}

COMMITTED_ARTIFACT_DIRS = ("target", "logs", "dbt_packages")


def _fmt_ver(raw: str) -> str:
    """Render a version specifier (possibly a Python list repr) as plain text."""
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return ",".join(str(x) for x in parsed)
    except (ValueError, SyntaxError):
        pass
    return raw


# =============================================================================
# Fragmentation
# =============================================================================


@rule(
    PRJ_MICRO_PROJECT,
    "Project below model threshold",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "A dbt project is the unit of lineage, testing, and documentation. "
        "Splitting a few models into their own project loses cross-project "
        "`ref()` lineage and multiplies the config and package surface to maintain."
    ),
)
def micro_project(portfolio: PortfolioContext) -> Iterator[Suggestion]:
    threshold = portfolio.config.micro_project_threshold
    if len(portfolio.projects) < 2:
        # A single small project is a new or intentionally scoped repo, not
        # fragmentation. Fragmentation is a property of the estate.
        return

    for project in portfolio.projects:
        count = project.model_count
        if count > threshold:
            continue
        # Fewer models means less justification for a separate project, which is
        # a difference in consequence rather than confidence.
        severity = Severity.MEDIUM if count <= 2 else Severity.LOW
        yield make_suggestion(
            PRJ_MICRO_PROJECT,
            f"Project `{project.name}` has {count} model{'' if count == 1 else 's'}, "
            f"below the {threshold}-model threshold for a standalone project.",
            severity=severity,
            project=project.name,
            file=f"{project.relative_root}/dbt_project.yml",
            evidence=f"{count} model(s) in {project.relative_root}",
            remediation=(
                "Merge these models into a sibling project. "
                "A single project provides `ref()` lineage and one `dbt build` "
                "across the whole flow. "
                "Keep separate projects only where ownership or release trains differ."
            ),
            effort=Effort.HIGH,
            model_count=count,
        )


@rule(
    PRJ_CONSOLIDATION,
    "Sibling projects share source tables",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "Projects sharing sources have no lineage between them. "
        "dbt cannot order them or detect conflicts; the dependency lives "
        "in whatever schedules them."
    ),
)
def consolidation_candidates(portfolio: PortfolioContext) -> Iterator[Suggestion]:
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
        yield make_suggestion(
            PRJ_CONSOLIDATION,
            f"{len(names)} projects ({', '.join(names)}) read the same "
            f"{plural(len(sources), 'source')} ({', '.join(source_labels)}"
            + (" ..." if len(sources) > 5 else "")
            + ") with no `ref()` lineage between them.",
            file="<portfolio>",
            evidence=f"shared sources: {', '.join(source_labels)}",
            remediation=(
                f"Consolidate these {len(names)} projects into one "
                f"containing all {total_models} models. "
                "Define each source once and let `ref()` express the ordering. "
                "If they must stay separate, keep source definitions identical "
                "to avoid silent inconsistency."
            ),
            effort=Effort.HIGH,
            projects=names,
        )


@rule(
    PRJ_TASK_ORCHESTRATION,
    "dbt projects chained via Snowflake Tasks",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "`EXECUTE DBT PROJECT` inside a Task graph moves dependency ordering "
        "out of dbt. Models in one project do not automatically run before "
        "consumers in another."
    ),
)
def task_orchestration(portfolio: PortfolioContext) -> Iterator[Suggestion]:
    hits: list[tuple[str, str, dict]] = []
    for project in portfolio.projects:
        for path, raw in project.loose_sql:
            stripped = strip_comments_and_strings(raw)
            for match in EXECUTE_DBT_PATTERN.finditer(stripped):
                try:
                    relative = str(path.relative_to(portfolio.root))
                except ValueError:
                    relative = str(path)
                hits.append(
                    (project.name, relative, span(stripped, match.start(), match.end()))
                )

    if len(hits) < 2:
        return

    files = sorted({path for _project, path, _line in hits})
    project_name, path, pos = hits[0]
    yield make_suggestion(
        PRJ_TASK_ORCHESTRATION,
        f"{len(hits)} `EXECUTE DBT PROJECT` invocations across "
        f"{plural(len(files), 'orchestration script')} "
        f"{'chains' if len(files) == 1 else 'chain'} separate "
        "dbt projects through a Task graph.",
        project=project_name,
        file=path,
        **pos,
        evidence=f"EXECUTE DBT PROJECT found in: {', '.join(files[:5])}",
        remediation=(
            "Merge the projects so `ref()` expresses the ordering. "
            "A single `dbt build` runs the whole graph in sequence. "
            "Reduce the Task to a scheduled trigger; "
            "keep Tasks for scheduling, not ordering."
        ),
        effort=Effort.HIGH,
        occurrence_count=len(hits),
    )


@rule(
    PRJ_DUPLICATED_CONFIG,
    "Project config duplicated across siblings",
    category=CATEGORY,
    scope=Scope.PORTFOLIO,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "Near-identical config in many projects must be updated everywhere. "
        "In practice it is updated in one and drifts in the rest."
    ),
)
def duplicated_config(portfolio: PortfolioContext) -> Iterator[Suggestion]:
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

    yield make_suggestion(
        PRJ_DUPLICATED_CONFIG,
        f"These {len(portfolio.projects)} projects each carry duplicate "
        "`dbt_project.yml` and `packages.yml`"
        + (
            ". "
            + plural(len(drifted), "package")
            + (" is" if len(drifted) == 1 else " are")
            + " already at different versions: "
            + "; ".join(
                f"{n} ({' vs '.join(_fmt_ver(v) for v in vers)})"
                for n, vers in list(drifted.items())[:3]
            )
            + "."
            if drifted
            else "."
        ),
        file="<portfolio>",
        evidence=f"{len(portfolio.projects)} dbt_project.yml files under {portfolio.root.name}",
        remediation=(
            "Consolidate into one project to unify config and packages. "
            "Where separate projects are required, pin package versions "
            "identically across all of them."
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
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.CRITICAL,
    rationale=(
        "`profiles.yml` holds connection and credential configuration. "
        "Committing it risks leaking secrets and pins every developer "
        "to one account."
    ),
)
def profiles_committed(project: ProjectContext) -> Iterator[Suggestion]:
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
        yield make_suggestion(
            PRJ_PROFILES_COMMITTED,
            f"`{name}` is present in the project directory"
            + (" and contains a literal credential value." if has_secret else "."),
            level=Level.ERROR if has_secret else Level.WARNING,
            file=name,
            evidence=f"{name} found at project root",
            remediation=(
                "Move it to `~/.dbt/profiles.yml` and add the path to `.gitignore`. "
                "Keep a redacted `profiles.yml.sample` in the repo for onboarding. "
                "If a credential was committed, rotate it; git history retains it."
            ),
            effort=Effort.LOW,
        )


@rule(
    PRJ_PLACEHOLDER_CONFIG,
    "Converter placeholders in project config",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.HIGH,
    rationale=(
        "A placeholder means the project cannot resolve a relation. "
        "Tests, docs, and lineage are unreliable until each is replaced."
    ),
)
def placeholder_config(project: ProjectContext) -> Iterator[Suggestion]:
    haystack = {
        "dbt_project.yml": str(project.project_yml),
        "packages.yml": str(project.packages),
    }
    for filename, text in haystack.items():
        found = sorted({p for p in PLACEHOLDER_VALUES if p in text})
        if not found:
            continue
        yield make_suggestion(
            PRJ_PLACEHOLDER_CONFIG,
            f"`{filename}` contains converter placeholder "
            f"{plural(len(found), 'value')}: {', '.join(found)}.",
            file=filename,
            evidence=", ".join(found),
            remediation=(
                "Replace each placeholder with the real project, profile, "
                "database, or schema name. "
                "Some conversion tooling ships `sc_override_*_db`/`_schema` "
                "vars with placeholder defaults, expecting the real value via "
                "`--vars` at run time. "
                "Before deleting a var, verify it belongs in the file "
                "and not in the run-time invocation; removing it silently "
                "drops the override."
            ),
            effort=Effort.LOW,
        )


@rule(
    PRJ_MISSING_PACKAGES,
    "Required baseline packages not declared",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "`dbt_constraints` turns assumed primary and foreign keys into "
        "enforced database constraints. `dbt_semantic_view` exposes "
        "dbt models as Snowflake semantic views for Cortex Analyst. "
        "Both are baseline in this estate."
    ),
)
def missing_packages(project: ProjectContext) -> Iterator[Suggestion]:
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
    yield make_suggestion(
        PRJ_MISSING_PACKAGES,
        f"`packages.yml` does not declare: {', '.join(missing)}.",
        file="packages.yml",
        evidence=f"declared: {', '.join(sorted(declared)) or 'none'}",
        remediation=(
            "Add the missing packages and run `dbt deps`:\n\n"
            "```yaml\n"
            "packages:\n"
            "  - package: Snowflake-Labs/dbt_constraints\n"
            '    version: [">=1.0.0", "<2.0.0"]\n'
            "  - package: Snowflake-Labs/dbt_semantic_view\n"
            '    version: [">=1.0.0", "<2.0.0"]\n'
            "```\n\n"
            "`dbt_constraints` converts assumed primary and foreign keys "
            "into Snowflake-enforced constraints. "
            "`dbt_semantic_view` exposes dbt models as Snowflake semantic "
            "views for Cortex Analyst."
        ),
        effort=Effort.LOW,
        missing=missing,
    )


@rule(
    PRJ_ARTIFACTS_COMMITTED,
    "Build artifact directories not in .gitignore",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "`target/` and `dbt_packages/` are regenerated on every run. "
        "Committing them creates noisy diffs and can ship a stale manifest "
        "that misleads tooling."
    ),
)
def artifacts_committed(project: ProjectContext) -> Iterator[Suggestion]:
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
    yield make_suggestion(
        PRJ_ARTIFACTS_COMMITTED,
        f"Generated director{'y' if len(present) == 1 else 'ies'} "
        f"{', '.join(present)} {'is' if len(present) == 1 else 'are'} "
        "tracked but not in `.gitignore`.",
        file=".gitignore",
        evidence=f"unignored: {', '.join(present)}",
        remediation=(
            "Add to `.gitignore`:\n\n"
            "```\n" + "\n".join(f"{name}/" for name in present) + "\n```\n\n"
            "Then `git rm -r --cached` any that are already tracked."
        ),
        effort=Effort.LOW,
    )
