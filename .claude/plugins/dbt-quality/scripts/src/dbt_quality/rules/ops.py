"""
OPS -- operational hygiene and observability.

Configuration that determines whether anyone finds out when the project breaks.
Low severity, but cheap to fix, and the contradictory-config case (OPS001) is a
genuine trap: the package is installed, the hook is wired, and the whole thing is
disabled by a flag elsewhere -- so the project looks instrumented and records
nothing.
"""

from __future__ import annotations

import re
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
    rule,
)
from dbt_quality.core.sqlutil import span

if TYPE_CHECKING:
    from dbt_quality.discovery import ProjectContext

CATEGORY = "OPS"

OPS_ARTIFACTS_CONTRADICTION = "SSC-EWI-DBTOPS0001"
OPS_CREDENTIALS = "SSC-EWI-DBTOPS0002"
OPS_EVALUATOR_CONFIG = "SSC-EWI-DBTOPS0003"
OPS_RUN_NOT_BUILD = "SSC-EWI-DBTOPS0004"

SECRET_PATTERN = re.compile(
    r"^\s*(password|private_key_passphrase|token|secret|access_key)\s*:\s*(?!\s*$)(?!\{\{)(?!\$)\S",
    re.MULTILINE | re.IGNORECASE,
)


def _find_flag(node: Any, key: str) -> Any:
    """Locate a config key anywhere in a nested tree, returning its value."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k.lstrip("+") == key:
                return v
            found = _find_flag(v, key)
            if found is not None:
                return found
    return None


@rule(
    OPS_ARTIFACTS_CONTRADICTION,
    "Run-artifact logging is wired but disabled",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.WARNING,
    severity=Severity.MEDIUM,
    rationale=(
        "An `on-run-end` upload hook alongside `+enabled: false` on the same "
        "package means the artifact models are never built. The hook runs against "
        "tables that do not exist, so the project appears instrumented but records "
        "nothing."
    ),
)
def artifacts_contradiction(project: ProjectContext) -> Iterator[Suggestion]:
    declared = {
        str(p.get("package", "")).split("/")[-1]
        for p in (project.packages.get("packages") or [])
        if isinstance(p, dict)
    }
    if "dbt_artifacts" not in declared:
        return

    on_run_end = project.project_yml.get("on-run-end") or []
    hooks = on_run_end if isinstance(on_run_end, list) else [on_run_end]
    has_hook = any("dbt_artifacts" in str(h) for h in hooks)
    enabled = _find_flag(project.project_yml.get("models") or {}, "enabled")
    artifacts_node = (project.project_yml.get("models") or {}).get("dbt_artifacts")
    artifacts_enabled = (
        _find_flag(artifacts_node, "enabled")
        if isinstance(artifacts_node, dict)
        else None
    )

    if has_hook and artifacts_enabled is False:
        yield make_suggestion(
            OPS_ARTIFACTS_CONTRADICTION,
            "`dbt_artifacts` models are disabled while the `on-run-end` upload "
            "hook is active.",
            file="dbt_project.yml",
            evidence="on-run-end references dbt_artifacts; models.dbt_artifacts.+enabled: false",
            remediation=(
                "To capture run history, set `+enabled: true` under "
                "`models: dbt_artifacts:` and run `dbt build --select "
                "package:dbt_artifacts` once to create the tables. "
                "To disable entirely, remove the `on-run-end` hook."
            ),
            effort=Effort.LOW,
        )
        return

    if not has_hook:
        yield make_suggestion(
            OPS_ARTIFACTS_CONTRADICTION,
            "`dbt_artifacts` is installed but has no `on-run-end` upload hook.",
            level=Level.INFORMATION,
            file="dbt_project.yml",
            evidence=f"packages include dbt_artifacts; on-run-end: {hooks or 'absent'}",
            remediation=(
                "Add the hook to `dbt_project.yml`:\n\n"
                "```yaml\n"
                "on-run-end:\n"
                '  - "{{ dbt_artifacts.upload_results(results) }}"\n'
                "```\n\n"
                "Gate on `target.name == 'prod'` to limit uploads to production runs."
            ),
            effort=Effort.LOW,
        )
    _ = enabled  # retained for clarity: project-wide enabled is not itself a defect


@rule(
    OPS_CREDENTIALS,
    "Literal credential in configuration",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.ERROR,
    severity=Severity.CRITICAL,
    rationale=(
        "A credential in a tracked file is exposed to everyone with repository access "
        "and stays in git history after removal."
    ),
)
def credentials(project: ProjectContext) -> Iterator[Suggestion]:
    for name in ("profiles.yml", "profiles.yaml", "dbt_project.yml"):
        path = project.root / name
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        match = SECRET_PATTERN.search(content)
        if not match:
            continue
        yield make_suggestion(
            OPS_CREDENTIALS,
            f"`{name}` contains a literal `{match.group(1)}` value.",
            file=name,
            **span(content, match.start(1), match.end(1)),
            evidence=f"{match.group(1)}: <redacted>",
            remediation=(
                "Replace the literal value with an environment variable: "
                "`password: \"{{ env_var('SNOWFLAKE_PASSWORD') }}\"`."
                " Alternatively, use key-pair authentication with a named "
                "connection in `~/.snowflake/connections.toml`."
                " Rotate the credential now; git history retains it."
            ),
            effort=Effort.MEDIUM,
        )


@rule(
    OPS_EVALUATOR_CONFIG,
    "dbt_project_evaluator not configured for dbt_constraints",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.LOW,
    rationale=(
        "`dbt_project_evaluator` only recognises the built-in uniqueness tests by "
        "default. In a project that uses `dbt_constraints`, it reports missing "
        "primary keys on models that do have them, and the false positives train "
        "people to ignore it."
    ),
)
def evaluator_config(project: ProjectContext) -> Iterator[Suggestion]:
    declared = {
        str(p.get("package", "")).split("/")[-1]
        for p in (project.packages.get("packages") or [])
        if isinstance(p, dict)
    }
    if "dbt_project_evaluator" not in declared:
        return
    variables = project.project_yml.get("vars") or {}
    evaluator_vars = variables.get("dbt_project_evaluator") or {}
    if isinstance(evaluator_vars, dict) and evaluator_vars.get(
        "primary_key_test_macros"
    ):
        return
    if "primary_key_test_macros" in str(variables):
        return
    yield make_suggestion(
        OPS_EVALUATOR_CONFIG,
        "`dbt_project_evaluator` is installed but `primary_key_test_macros` is "
        "not configured in `vars`.",
        file="dbt_project.yml",
        evidence="vars.dbt_project_evaluator.primary_key_test_macros absent",
        remediation=(
            "Set `primary_key_test_macros` under `vars: dbt_project_evaluator:` "
            "in `dbt_project.yml`:\n\n"
            "```yaml\n"
            "vars:\n"
            "  dbt_project_evaluator:\n"
            "    primary_key_test_macros:\n"
            '      [["dbt_constraints.test_primary_key"],\n'
            '       ["dbt_constraints.test_unique_key", "dbt.test_not_null"],\n'
            '       ["dbt.test_unique", "dbt.test_not_null"]]\n'
            "```"
        ),
        effort=Effort.LOW,
    )


@rule(
    OPS_RUN_NOT_BUILD,
    "Automation runs dbt run instead of dbt build",
    category=CATEGORY,
    scope=Scope.PROJECT,
    kind=Kind.EWI,
    level=Level.INFORMATION,
    severity=Severity.MEDIUM,
    rationale=(
        "`dbt run` executes models without tests. Splitting run and test means a "
        "failing test is discovered after downstream models have already consumed "
        "bad data; `dbt build` interleaves them so a failure stops its dependents."
    ),
)
def run_not_build(project: ProjectContext) -> Iterator[Suggestion]:
    candidates = [
        *project.root.glob("*.yml"),
        *project.root.glob("*.yaml"),
        *project.root.glob(".github/workflows/*.yml"),
        *project.root.glob(".github/workflows/*.yaml"),
        *project.root.glob("*.sh"),
        *project.root.glob("Makefile"),
    ]
    for path in candidates:
        if not path.is_file() or path.name in (
            "dbt_project.yml",
            "packages.yml",
            "profiles.yml",
        ):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not re.search(r"\bdbt\s+run\b", content):
            continue
        if not re.search(r"\bdbt\s+test\b", content):
            continue
        match = re.search(r"\bdbt\s+run\b", content)
        try:
            relative = str(path.relative_to(project.root))
        except ValueError:
            relative = str(path)
        yield make_suggestion(
            OPS_RUN_NOT_BUILD,
            f"`{path.name}` runs `dbt run` and `dbt test` as separate steps.",
            file=relative,
            **(span(content, match.start(), match.end()) if match else {}),
            evidence=match.group(0) if match else "dbt run",
            remediation=(
                "Replace both with `dbt build`. It interleaves models and tests "
                "and halts dependents on failure, so bad data does not propagate."
            ),
            effort=Effort.LOW,
        )
