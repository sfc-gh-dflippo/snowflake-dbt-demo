#!/usr/bin/env python3
"""
PostToolUse hook: run the project audit after dbt updates the manifest.

There is no native file-changed hook event, so this fires on tool calls and gates
itself twice before doing real work:

1. **Was dbt actually invoked?** Matches a dbt executable command in Bash. Anything
   else costs one regex and returns.
2. **Did the manifest advance?** ``target/manifest.json`` must exist *and* be newer
   than the recorded stamp. Missing or unchanged is a silent skip -- no audit, no
   output, and no nagging to run ``dbt parse``.

Gating on the manifest rather than on a list of dbt subcommands means
``dbt debug``, ``dbt deps`` and a failed run produce nothing without needing to be
enumerated, because none of them leaves a newer manifest.

The audit runs through ``uv run --script``, so the PEP 723 header on
``scripts/audit.py`` supplies its dependencies and nothing needs installing. This
wrapper uses only the standard library.

Always advisory: writes plain (non-JSON) text to stdout to report suggestions --
the hook runner maps non-JSON stdout to ``additionalContext`` automatically,
unlike the JSON ``hookSpecificOutput.additionalContext`` form, which does not
reach the agent for ``PostToolUse``. Writes ``{"continue": true}`` and exits 0
when there is nothing to report. An audit is a report, and a report should
never fail somebody's command.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AUDIT = PLUGIN_ROOT / "scripts" / "audit.py"

#: Match a shell command that invokes dbt and will rewrite ``target/manifest.json``.
#:
#: The hook fires on every bash call -- ``matcher`` in hooks.json is tested
#: against the tool name, not the command -- so this regex is the only filter.
#: It requires a manifest-producing subcommand, which keeps ``dbt debug``,
#: ``dbt deps``, ``dbt --version`` and prose mentions from starting an audit.
#: dbt must start a shell command (optionally through ``uv run``), preventing
#: strings such as ``echo dbt build`` and commit messages from invoking an audit.
#: Flags between the executable and the subcommand are tolerated, so
#: ``dbt --profiles-dir ~/.dbt run`` still matches.
DBT_INVOCATION = re.compile(
    r"(?:^|[|;&])\s*(?:(?:[A-Za-z_][\w]*=\S+)\s+)*"
    r"(?:(?:uv|poetry|pipenv)\s+run\s+)?(?<![\w-])dbt(?![\w-])[^|;&]*?"
    r"(?<![\w-])(run|build|compile|parse|seed|snapshot|test|docs)(?![\w-])"
)

STATE_DIR = Path.home() / ".cache" / "dbt-quality"
MAX_PROJECTS_REPORTED = 2
TIMEOUT_SECONDS = 180


def _continue(context: str = "") -> None:
    """Emit the hook response, optionally injecting advisory context."""
    sys.stdout.write(context if context else '{"continue": true}')


def _invoked_dbt(payload: dict) -> bool:
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command")
    return isinstance(command, str) and bool(DBT_INVOCATION.search(command))


def _find_projects(root: Path, limit: int = 40) -> list[Path]:
    """Directories under root holding a dbt_project.yml, skipping vendored trees."""
    skip = {"dbt_packages", "target", "node_modules", ".git", ".venv", "venv"}
    found: list[Path] = []
    stack = [root]
    while stack and len(found) < limit:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except (OSError, PermissionError):
            continue
        for entry in entries:
            if entry.is_dir():
                if entry.name not in skip and not entry.name.startswith("."):
                    stack.append(entry)
            elif entry.name == "dbt_project.yml":
                found.append(current)
    return found


def _manifest_advanced(project_root: Path) -> bool:
    """
    True when the manifest exists and is newer than the last audited stamp.

    The stamp lives outside the project, so auditing never writes into the user's
    repository, and is keyed on the project path so sibling projects are tracked
    independently.
    """
    manifest = project_root / "target" / "manifest.json"
    if not manifest.is_file():
        return False
    try:
        mtime = manifest.stat().st_mtime
    except OSError:
        return False

    key = re.sub(r"[^A-Za-z0-9]+", "_", str(project_root.resolve())).strip("_")
    stamp = STATE_DIR / f"{key}.stamp"
    try:
        if stamp.is_file():
            previous = float(stamp.read_text(encoding="utf-8").strip() or 0)
            if previous >= mtime:
                return False
    except (OSError, ValueError):
        pass  # unreadable stamp: treat as never audited

    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        stamp.write_text(str(mtime), encoding="utf-8")
    except OSError:
        # Cannot record, so decline rather than re-auditing on every later call.
        return False
    return True


def _summarise(report: dict, project_root: Path) -> str:
    summary = report.get("summary", {})
    counts = summary.get("counts", {})
    lines = [
        f"dbt quality suggestions -- {project_root.name}",
        f"  {counts.get('total', 0)} suggestion(s) across "
        f"{summary.get('model_count')} models "
        f"({summary.get('per_model', 0)} per model)",
        f"  {counts.get('error', 0)} error, {counts.get('warning', 0)} warning, "
        f"{counts.get('information', 0)} information",
        f"  severity: {counts.get('critical', 0)} critical, "
        f"{counts.get('high', 0)} high, {counts.get('medium', 0)} medium, "
        f"{counts.get('low', 0)} low",
    ]
    for item in (report.get("remediation") or [])[:3]:
        lines.append(
            f"  - {item['rule_id']} {item['title']} "
            f"({item['count']}x, {item['effort']} effort)"
        )
    if counts.get("suppressed"):
        lines.append(
            f"  {counts['suppressed']} architecture suggestion(s) suppressed "
            "(lift-and-shift provenance detected)"
        )
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        _continue()
        return 0

    if not _invoked_dbt(payload):
        _continue()
        return 0

    uv = shutil.which("uv")
    if uv is None or not AUDIT.is_file():
        _continue()
        return 0

    cwd = Path(payload.get("cwd") or Path.cwd())
    projects = [p for p in _find_projects(cwd) if _manifest_advanced(p)]
    if not projects:
        _continue()
        return 0

    summaries: list[str] = []
    for project_root in projects[:MAX_PROJECTS_REPORTED]:
        try:
            completed = subprocess.run(  # noqa: S603 -- fixed argv, no shell
                [
                    uv,
                    "run",
                    "--script",
                    str(AUDIT),
                    "audit",
                    str(project_root),
                    "--stdout",
                    "--quiet",
                ],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
            report = json.loads(completed.stdout)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError):
            continue
        summaries.append(_summarise(report, project_root))

    if not summaries:
        _continue()
        return 0

    context = "\n\n".join(summaries)
    context += "\n\nUse the dbt-audit skill for the full report and remediation."
    _continue(context)
    return 0


if __name__ == "__main__":
    sys.exit(main())
