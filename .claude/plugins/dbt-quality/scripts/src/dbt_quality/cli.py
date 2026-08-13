"""
Command-line interface.

Two commands:

- ``manifest-status`` -- report, per project, whether ``target/manifest.json``
  exists and is current, and which checks are unavailable without it. Cheap and
  read-only; the skill runs this first so it can offer to run ``dbt parse`` before
  the audit rather than producing a report with gaps.
- ``audit`` -- run the rules and write ``suggestions.json``.

Output conventions follow ``dbt_validation.cli``: Rich tables to stderr so stdout
stays clean for piping, a ``--simple`` flag for non-colour environments, and a
non-zero exit only for errors, never for warnings or information suggestions.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dbt_quality.core.base import LEVEL_RANK, LINT_TOKENS, REGISTRY, Level
from dbt_quality.discovery import build_portfolio, find_projects
from dbt_quality.engine import run_audit, run_single_file
from dbt_quality.scoring import CATEGORY_LABELS, build_report

app = typer.Typer(
    add_completion=False,
    help="Audit dbt projects for anti-patterns and produce a quality assessment.",
    no_args_is_help=True,
)

LEVEL_STYLE = {
    Level.ERROR: "bold red",
    Level.WARNING: "yellow",
    Level.INFORMATION: "cyan",
}


def _console(simple: bool) -> Console:
    # stderr keeps stdout free for `--stdout` JSON piping.
    return Console(stderr=True, no_color=simple, soft_wrap=simple)


@app.command("manifest-status")
def manifest_status(
    root: Annotated[
        Path, typer.Argument(help="dbt project, or a directory containing several.")
    ] = Path("."),
    simple: Annotated[
        bool, typer.Option("--simple", help="Plain output, no colour.")
    ] = False,
) -> None:
    """
    Report manifest availability per project, and what it unlocks.

    Run this before ``audit`` to decide whether to run ``dbt parse`` first. Graph
    checks (fan-out, pass-through chains, layer crossing, single-consumer models)
    cannot run without a manifest and are reported as skipped rather than passing.
    """
    console = _console(simple)
    root = root.resolve()
    projects = find_projects(root)

    if not projects:
        console.print(f"[bold red]No dbt_project.yml found under {root}[/]")
        raise typer.Exit(code=1)

    graph_rules = sorted(r.rule_id for r in REGISTRY.values() if r.requires_manifest)

    table = Table(title=f"Manifest status ({len(projects)} project(s))")
    table.add_column("Project")
    table.add_column("Manifest")
    table.add_column("State")
    table.add_column("dbt parse needed")

    needs_parse: list[str] = []
    for project_root in projects:
        manifest = project_root / "target" / "manifest.json"
        rel = str(project_root.relative_to(root)) or "."
        if not manifest.is_file():
            table.add_row(rel, "missing", "-", "yes")
            needs_parse.append(rel)
            continue
        newest = max(
            (
                p.stat().st_mtime
                for p in project_root.rglob("models/**/*.sql")
                if p.is_file()
            ),
            default=0.0,
        )
        stale = manifest.stat().st_mtime < newest
        table.add_row(
            rel,
            "present",
            "stale" if stale else "current",
            "recommended" if stale else "no",
        )
        if stale:
            needs_parse.append(rel)

    console.print(table)
    if needs_parse:
        console.print(
            Panel(
                f"{len(graph_rules)} graph-dependent check(s) will be skipped for: "
                f"{', '.join(needs_parse)}\n"
                f"Rules affected: {', '.join(graph_rules)}\n\n"
                "Run `dbt parse` in each project to enable them. `dbt parse` does not "
                "execute models and needs no warehouse compute, but it does need a "
                "valid profile.",
                title="Recommendation",
            )
        )
    else:
        console.print(
            "[green]All projects have a current manifest; all checks available.[/]"
        )

    # stdout carries the machine-readable answer for the calling agent.
    print(
        json.dumps({"needs_parse": needs_parse, "graph_rules": graph_rules}, indent=2)
    )


@app.command("audit")
def audit(
    root: Annotated[
        Path, typer.Argument(help="dbt project, or a directory containing several.")
    ] = Path("."),
    out: Annotated[
        Path | None, typer.Option("--out", "-o", help="Write suggestions JSON here.")
    ] = None,
    stdout: Annotated[
        bool, typer.Option("--stdout", help="Emit suggestions JSON on stdout.")
    ] = False,
    category: Annotated[
        list[str] | None,
        typer.Option("--category", "-c", help="Limit to categories, e.g. INC."),
    ] = None,
    min_level: Annotated[
        str, typer.Option("--min-level", help="error | warning | information")
    ] = "information",
    fail_on_error: Annotated[
        bool,
        typer.Option(
            "--fail-on-error", help="Exit 1 if any error-level suggestion is found."
        ),
    ] = False,
    simple: Annotated[
        bool, typer.Option("--simple", help="Plain output, no colour.")
    ] = False,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress the console summary.")
    ] = False,
) -> None:
    """Run the audit and write suggestions.json."""
    console = _console(simple)
    root = root.resolve()

    if not find_projects(root):
        console.print(f"[bold red]No dbt_project.yml found under {root}[/]")
        raise typer.Exit(code=1)

    portfolio = build_portfolio(root)
    result = run_audit(portfolio)
    report = build_report(result, str(root))

    # Filters apply to the emitted suggestions list, not to scoring -- a score that
    # changed with the display filter would not be comparable between runs.
    if category:
        wanted = {c.upper() for c in category}
        report["suggestions"] = [
            f for f in report["suggestions"] if f["category"] in wanted
        ]
    threshold = LEVEL_RANK.get(min_level.lower(), 2)
    report["suggestions"] = [
        f for f in report["suggestions"] if LEVEL_RANK.get(f["level"], 2) <= threshold
    ]

    payload = json.dumps(report, indent=2)
    destination = out or (root / "dbt-audit-suggestions.json")
    if stdout:
        print(payload)
    else:
        destination.write_text(payload, encoding="utf-8")

    if not quiet:
        _print_summary(console, report, destination if not stdout else None)

    if fail_on_error and report["summary"]["counts"]["error"]:
        raise typer.Exit(code=1)


def _print_summary(console: Console, report: dict, destination: Path | None) -> None:
    summary = report["summary"]
    counts = summary["counts"]

    table = Table(title="dbt quality suggestions")
    table.add_column("Category")
    table.add_column("Error", justify="right")
    table.add_column("Warning", justify="right")
    table.add_column("Information", justify="right")
    table.add_column("Per model", justify="right")

    for entry in report["summary"]["categories"]:
        if entry["total"] == 0:
            continue
        table.add_row(
            entry["label"],
            str(entry["error"]) if entry["error"] else "-",
            str(entry["warning"]) if entry["warning"] else "-",
            str(entry["information"]) if entry["information"] else "-",
            f"{entry['per_model']:.2f}",
        )
    console.print(table)

    lines = [
        f"Projects: {summary['project_count']}   Models: {summary['model_count']}",
        f"Suggestions: [bold]{counts['total']}[/] — {counts['error']} error, "
        f"{counts['warning']} warning, {counts['information']} information",
        f"Severity: {counts['critical']} critical, {counts['high']} high, "
        f"{counts['medium']} medium, {counts['low']} low",
        f"Per model: {summary['per_model']:.2f}",
        f"Manifest coverage: {summary['manifest_coverage']}   "
        f"Rules skipped: {summary['rules_skipped']}",
    ]
    if counts.get("suppressed"):
        lines.append(
            f"Suppressed (lift-and-shift): {counts['suppressed']} "
            "architecture suggestion(s)"
        )
    if destination is not None:
        lines.append(f"\nSuggestions written to {destination}")
    console.print(Panel("\n".join(lines), title="Summary"))

    top = report["remediation"][:5]
    if top:
        priority = Table(title="Highest-leverage remediation")
        priority.add_column("Rule")
        priority.add_column("Suggestion")
        priority.add_column("Count", justify="right")
        priority.add_column("Effort")
        for item in top:
            priority.add_row(
                item["rule_id"],
                item["title"],
                str(item["count"]),
                item["effort"],
            )
        console.print(priority)


@app.command("lint")
def lint(
    root: Annotated[
        Path, typer.Argument(help="dbt project, or a directory containing several.")
    ] = Path("."),
    output_format: Annotated[
        str, typer.Option("--format", help="text | json")
    ] = "text",
    min_level: Annotated[
        str, typer.Option("--min-level", help="error | warning | information")
    ] = "information",
    strict: Annotated[
        bool,
        typer.Option("--strict", help="Exit 1 if any error-level suggestion is found."),
    ] = False,
) -> None:
    """
    Emit suggestions in a linter format an editor can parse.

    One line per suggestion, because a ``problemMatcher`` regex is applied per line
    -- a multi-line message cannot be matched, so messages are collapsed to a single
    line here rather than wrapped.

    Paths are relative to ``root`` so a matcher configured with
    ``fileLocation: ["relative", "${workspaceFolder}"]`` resolves them.

    Exits 0 even when suggestions are found. A suggestion is not a failure, and a
    lint task that reports failure trains people to ignore it. ``--strict`` opts in
    to exit 1 on any ``error``-level suggestion, for a pipeline that wants a gate.
    """
    console = _console(simple=True)
    if not find_projects(root):
        console.print(f"[yellow]No dbt_project.yml found under {root}[/]")
        raise typer.Exit(code=0)

    portfolio = build_portfolio(root)
    result = run_audit(portfolio)

    threshold = LEVEL_RANK.get(min_level.lower(), 2)
    active = [
        s
        for s in result.suggestions
        if not s.suppressed and LEVEL_RANK.get(s.level, 2) <= threshold
    ]

    if output_format.lower() == "json":
        print(
            json.dumps(
                [_lint_record(s, root) for s in active],
                indent=2,
            )
        )
    else:
        for suggestion in active:
            print(_lint_line(suggestion, root))

    if strict and any(s.level == Level.ERROR for s in active):
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


def _lint_relative(suggestion: Any, root: Path) -> str:
    """
    Path relative to the lint root, which is what a problem matcher resolves.

    Project-scoped rules sometimes name a directory (``models/``) or nothing at all,
    because the observation is about the project rather than a file. An editor cannot
    open a directory as a diagnostic target, so those are redirected to
    ``dbt_project.yml`` -- the file that actually configures the thing being
    described.
    """
    resolved = root.resolve()

    def _relative_to_root(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(resolved))
        except ValueError:
            return str(path)

    def _project_fallback() -> str:
        for project in find_projects(root):
            candidate = project / "dbt_project.yml"
            if candidate.is_file():
                return _relative_to_root(candidate)
        return "dbt_project.yml"

    if not suggestion.file:
        return _project_fallback()

    candidate = Path(suggestion.file)
    if candidate.is_absolute():
        return (
            _relative_to_root(candidate) if candidate.is_file() else _project_fallback()
        )

    # Suggestions carry paths relative to their own project, which may itself sit
    # below the lint root in a multi-project tree.
    for project in find_projects(root):
        full = project / suggestion.file
        if full.is_file():
            return _relative_to_root(full)
    if (resolved / suggestion.file).is_file():
        return suggestion.file
    return _project_fallback()


#: Longest fix hint appended to a lint line. The full remediation, including any
#: code block, stays in the JSON report -- a Problems-panel row is a pointer, not a
#: place to paste SQL.
LINT_HINT_LIMIT = 140

CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)


def _one_line(text: str) -> str:
    """Collapse to a single line; a problem matcher cannot span lines."""
    return " ".join(text.split())


def _fix_hint(remediation: str) -> str:
    """
    First sentence of the remediation, with code blocks removed.

    Fenced examples are the most useful part of a remediation and the least useful
    thing to inline into a single-line diagnostic -- flattened, a ```sql block turns
    into an unreadable run of tokens. They are stripped here and remain in the JSON.
    """
    text = _one_line(CODE_FENCE.sub("", remediation))
    if not text:
        return ""
    sentence = text.split(". ")[0].rstrip(". ")
    if len(sentence) > LINT_HINT_LIMIT:
        sentence = sentence[: LINT_HINT_LIMIT - 1].rstrip() + "\u2026"
    return sentence


def _lint_line(suggestion: Any, root: Path) -> str:
    """
    ``path:line:col:endLine:endCol: level: [RULE] message -> fix``

    The severity token is the mapped ``LINT_TOKENS`` value rather than our own level
    name, because a matcher only recognises error/warning/info. The level name is
    not lost -- it is carried in the JSON and in the report.

    The end position falls back to the start, so the field count is constant and
    the matcher regex needs no optional groups. Appending the end rather than
    changing the existing separator keeps a stale ``tasks.json`` working: its
    regex still matches file, line and column and simply ignores the range.
    """
    token = LINT_TOKENS.get(suggestion.level, "info")
    line = suggestion.line or 1
    column = suggestion.column or 1
    parts = [
        f"{_lint_relative(suggestion, root)}:{line}:{column}:"
        f"{suggestion.end_line or line}:{suggestion.end_column or column}:"
        f" {token}: [{suggestion.rule_id}]",
        _one_line(suggestion.message),
    ]
    hint = _fix_hint(suggestion.remediation)
    if hint:
        parts.append(f"-> {hint}.")
    return " ".join(parts)


def _lint_record(suggestion: Any, root: Path) -> dict[str, Any]:
    line = suggestion.line or 1
    column = suggestion.column or 1
    return {
        "file": _lint_relative(suggestion, root),
        "line": line,
        "column": column,
        "end_line": suggestion.end_line or line,
        "end_column": suggestion.end_column or column,
        "severity": LINT_TOKENS.get(suggestion.level, "info"),
        "level": suggestion.level,
        "code": suggestion.rule_id,
        "message": _one_line(suggestion.message),
        "remediation": _one_line(suggestion.remediation),
    }


@app.command("rules")
def rules(
    simple: Annotated[
        bool, typer.Option("--simple", help="Plain output, no colour.")
    ] = False,
) -> None:
    """List the registered rules and their tiers."""
    console = _console(simple)
    table = Table(title=f"{len(REGISTRY)} registered rules")
    table.add_column("ID")
    table.add_column("Category")
    table.add_column("Tier")
    table.add_column("Level")
    table.add_column("Manifest")
    table.add_column("Title")
    for meta in sorted(REGISTRY.values(), key=lambda m: m.rule_id):
        table.add_row(
            meta.rule_id,
            CATEGORY_LABELS.get(meta.category, meta.category),
            meta.tier,
            meta.default_level,
            "yes" if meta.requires_manifest else "-",
            meta.title,
        )
    console.print(table)


# =============================================================================
# Single-file validation (dbt-validate, and the editor hook)
# =============================================================================

validate_app = typer.Typer(
    add_completion=False,
    help="Validate a single dbt model file.",
)


def _resolve_hook_path(raw: str) -> str:
    """
    Accept the path shapes an editor hook actually passes.

    ``$FILE_PATH`` normally arrives already expanded by the shell, but when the hook
    command is quoted such that the shell does not expand it, the literal string
    ``$FILE_PATH`` is passed through instead. Both are handled, matching the
    behaviour of the tool this replaces.
    """
    if raw.startswith("$"):
        return os.environ.get(raw[1:], raw)
    return raw


@validate_app.command()
def validate(
    path: Annotated[
        str,
        typer.Argument(help="Path to a dbt model file.", envvar="FILE_PATH"),
    ],
    simple: Annotated[
        bool, typer.Option("--simple", help="Plain output, no colour.")
    ] = False,
    strict: Annotated[
        bool,
        typer.Option("--strict", help="Exit 1 on any error-level suggestion."),
    ] = False,
) -> None:
    """
    Validate one model file and report suggestions.

    Exits 0 for anything not a dbt model, including a path that does not exist, so
    it is safe to wire to an editor hook that fires on every write.
    """
    console = _console(simple)
    target = Path(_resolve_hook_path(path))

    if not target.is_file() or target.suffix.lower() not in (".sql", ".py"):
        raise typer.Exit(code=0)

    # Find the enclosing dbt project by walking up, rather than assuming the
    # current working directory is the project root -- a hook's CWD is not ours.
    project_root: Path | None = None
    for candidate in [target.resolve().parent, *target.resolve().parents]:
        if (candidate / "dbt_project.yml").is_file():
            project_root = candidate
            break
    if project_root is None:
        raise typer.Exit(code=0)

    portfolio = build_portfolio(project_root)
    result = run_single_file(portfolio, target)

    active = [f for f in result.suggestions if not f.suppressed]
    if not active:
        raise typer.Exit(code=0)

    table = Table(title=f"{target.name}")
    table.add_column("Level")
    table.add_column("Rule")
    table.add_column("Line", justify="right")
    table.add_column("Suggestion")
    for suggestion in active:
        table.add_row(
            suggestion.level,
            suggestion.rule_id,
            str(suggestion.line) if suggestion.line else "-",
            suggestion.message,
        )
    console.print(table)

    if strict and any(f.level == Level.ERROR for f in active):
        raise typer.Exit(code=1)
    # Nothing blocks a save. An Error prints loudly, but a validation hook that fails
    # mid-refactor gets switched off, after which it protects nothing. Gate on errors
    # in CI instead, with `dbt-lint --strict`.
    raise typer.Exit(code=0)


def main() -> None:
    """Entry point for the ``dbt-audit`` script."""
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)


def validate_main() -> None:
    """
    Entry point for the ``dbt-validate`` script and the editor hook.

    A separate Typer app rather than a subcommand of ``app``, so the hook can call
    it with a bare path and no subcommand name.
    """
    try:
        validate_app()
    except KeyboardInterrupt:
        sys.exit(130)


lint_app = typer.Typer(
    add_completion=False,
    help="Emit dbt quality suggestions in a linter format.",
)
lint_app.command()(lint)


def lint_main() -> None:
    """
    Entry point for the ``dbt-lint`` script and the editor task.

    Wrapped in its own single-command app so the task definition can pass a bare
    path, keeping ``tasks.json`` readable.
    """
    try:
        lint_app()
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
