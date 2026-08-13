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

from dbt_audit.core.base import Effort, Finding, Scope, Severity, make_finding, rule

if TYPE_CHECKING:
    from dbt_audit.discovery import ProjectContext

CATEGORY = "OPS"

OPS_ARTIFACTS_CONTRADICTION = "OPS001"
OPS_CREDENTIALS = "OPS002"
OPS_EVALUATOR_CONFIG = "OPS003"
OPS_RUN_NOT_BUILD = "OPS004"

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
    severity=Severity.WARNING,
    rationale=(
        "An on-run-end upload hook alongside an `enabled: false` flag on the same "
        "package means the models that store the results are never built. The hook runs, "
        "finds no destination, and the project looks instrumented while recording "
        "nothing."
    ),
)
def artifacts_contradiction(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            OPS_ARTIFACTS_CONTRADICTION,
            "`dbt_artifacts` has an active `on-run-end` upload hook but its models are "
            "set to `+enabled: false`, so there is nowhere for the results to land.",
            file="dbt_project.yml",
            evidence="on-run-end references dbt_artifacts; models.dbt_artifacts.+enabled: false",
            remediation=(
                "Pick one. To collect run history, set `+enabled: true` under "
                "`models: dbt_artifacts:` and run `dbt build --select "
                "package:dbt_artifacts` once to create the tables. To opt out entirely, "
                "remove the `on-run-end` hook as well so the intent is unambiguous."
            ),
            effort=Effort.LOW,
        )
        return

    if not has_hook:
        yield make_finding(
            OPS_ARTIFACTS_CONTRADICTION,
            "`dbt_artifacts` is installed but no `on-run-end` hook uploads results, so "
            "no run history is captured.",
            severity=Severity.RECOMMENDATION,
            file="dbt_project.yml",
            evidence=f"packages include dbt_artifacts; on-run-end: {hooks or 'absent'}",
            remediation=(
                "Wire up the upload:\n\n"
                "```yaml\n"
                "on-run-end:\n"
                '  - "{{ dbt_artifacts.upload_results(results) }}"\n'
                "```\n\n"
                "Gate it on `target.name == 'prod'` if you only want production history. "
                "Without this the package is inert."
            ),
            effort=Effort.LOW,
        )
    _ = enabled  # retained for clarity: project-wide enabled is not itself a defect


@rule(
    OPS_CREDENTIALS,
    "Literal credential in configuration",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.ERROR,
    rationale=(
        "A credential in a tracked file is exposed to everyone with repository access "
        "and stays in git history after removal."
    ),
)
def credentials(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            OPS_CREDENTIALS,
            f"`{name}` contains a literal value for `{match.group(1)}`.",
            file=name,
            line=content[: match.start()].count("\n") + 1,
            evidence=f"{match.group(1)}: <redacted>",
            remediation=(
                "Replace with an environment variable -- "
                "`password: \"{{ env_var('SNOWFLAKE_PASSWORD') }}\"` -- or move to "
                "key-pair authentication. Prefer a named connection in "
                "`~/.snowflake/connections.toml` referenced by connection name, which "
                "keeps the secret out of the project entirely. Rotate the exposed "
                "credential; git history retains it."
            ),
            effort=Effort.MEDIUM,
        )


@rule(
    OPS_EVALUATOR_CONFIG,
    "dbt_project_evaluator not configured for dbt_constraints",
    category=CATEGORY,
    scope=Scope.PROJECT,
    severity=Severity.RECOMMENDATION,
    rationale=(
        "dbt_project_evaluator only recognises the built-in uniqueness tests by default. "
        "In a project that uses dbt_constraints, it reports missing primary keys on "
        "models that do have them, and the false positives train people to ignore it."
    ),
)
def evaluator_config(project: ProjectContext) -> Iterator[Finding]:
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
    yield make_finding(
        OPS_EVALUATOR_CONFIG,
        "`dbt_project_evaluator` is installed without `primary_key_test_macros`, so it "
        "will not recognise `dbt_constraints` tests and will report false key gaps.",
        file="dbt_project.yml",
        evidence="vars.dbt_project_evaluator.primary_key_test_macros absent",
        remediation=(
            "Teach it the project's test vocabulary:\n\n"
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
    severity=Severity.WARNING,
    rationale=(
        "`dbt run` executes models without tests. Splitting run and test means a failing "
        "test is discovered after downstream models have already consumed bad data; "
        "`dbt build` interleaves them so a failure stops its dependents."
    ),
)
def run_not_build(project: ProjectContext) -> Iterator[Finding]:
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
        yield make_finding(
            OPS_RUN_NOT_BUILD,
            f"`{path.name}` invokes `dbt run` and `dbt test` as separate steps.",
            file=relative,
            line=content[: match.start()].count("\n") + 1 if match else None,
            evidence=match.group(0) if match else "dbt run",
            remediation=(
                "Replace both with a single `dbt build`. It runs each model and its tests "
                "together and skips dependents of a failed test, so bad data does not "
                "propagate while the pipeline continues."
            ),
            effort=Effort.LOW,
        )
