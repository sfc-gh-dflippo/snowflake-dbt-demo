"""
Command-line interface.

Two commands:

- ``manifest-status`` -- report, per project, whether ``target/manifest.json``
  exists and is current, and which checks are unavailable without it. Cheap and
  read-only; the skill runs this first so it can offer to run ``dbt parse`` before
  the audit rather than producing a report with gaps.
- ``audit`` -- run the rules and write ``findings.json``.

Output conventions follow ``dbt_validation.cli``: Rich tables to stderr so stdout
stays clean for piping, a ``--simple`` flag for non-colour environments, and a
non-zero exit only for errors, never for warnings or recommendations.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dbt_audit.core.base import REGISTRY, Severity
from dbt_audit.discovery import build_portfolio, find_projects
from dbt_audit.engine import run_audit
from dbt_audit.scoring import CATEGORY_LABELS, build_report, grade

app = typer.Typer(
    add_completion=False,
    help="Audit dbt projects for anti-patterns and produce a quality assessment.",
    no_args_is_help=True,
)

SEVERITY_STYLE = {
    Severity.ERROR: "bold red",
    Severity.WARNING: "yellow",
    Severity.RECOMMENDATION: "cyan",
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
        Path | None, typer.Option("--out", "-o", help="Write findings JSON here.")
    ] = None,
    stdout: Annotated[
        bool, typer.Option("--stdout", help="Emit findings JSON on stdout.")
    ] = False,
    category: Annotated[
        list[str] | None,
        typer.Option("--category", "-c", help="Limit to categories, e.g. INC."),
    ] = None,
    min_severity: Annotated[
        str, typer.Option("--min-severity", help="error | warning | recommendation")
    ] = "recommendation",
    fail_on_error: Annotated[
        bool,
        typer.Option(
            "--fail-on-error", help="Exit 1 if any error-severity finding is found."
        ),
    ] = False,
    simple: Annotated[
        bool, typer.Option("--simple", help="Plain output, no colour.")
    ] = False,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Suppress the console summary.")
    ] = False,
) -> None:
    """Run the audit and write findings.json."""
    console = _console(simple)
    root = root.resolve()

    if not find_projects(root):
        console.print(f"[bold red]No dbt_project.yml found under {root}[/]")
        raise typer.Exit(code=1)

    portfolio = build_portfolio(root)
    result = run_audit(portfolio)
    report = build_report(result, str(root))

    # Filters apply to the emitted findings list, not to scoring -- a score that
    # changed with the display filter would not be comparable between runs.
    if category:
        wanted = {c.upper() for c in category}
        report["findings"] = [f for f in report["findings"] if f["category"] in wanted]
    order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.RECOMMENDATION: 2}
    threshold = order.get(min_severity.lower(), 2)
    report["findings"] = [
        f for f in report["findings"] if order.get(f["severity"], 2) <= threshold
    ]

    payload = json.dumps(report, indent=2)
    destination = out or (root / "dbt-audit-findings.json")
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

    table = Table(title="dbt quality assessment")
    table.add_column("Category")
    table.add_column("Score", justify="right")
    table.add_column("Error", justify="right")
    table.add_column("Warn", justify="right")
    table.add_column("Rec", justify="right")

    for entry in report["summary"]["categories"]:
        if entry["total"] == 0:
            continue
        table.add_row(
            entry["label"],
            f"{entry['score']:.0f} ({entry['grade']})",
            str(entry["error"]) if entry["error"] else "-",
            str(entry["warning"]) if entry["warning"] else "-",
            str(entry["recommendation"]) if entry["recommendation"] else "-",
        )
    console.print(table)

    lines = [
        f"Overall: [bold]{summary['score']:.0f}/100 ({grade(summary['score'])})[/]",
        f"Projects: {summary['project_count']}   Models: {summary['model_count']}",
        f"Findings: {counts['error']} error, {counts['warning']} warning, "
        f"{counts['recommendation']} recommendation",
        f"Manifest coverage: {summary['manifest_coverage']}   "
        f"Rules skipped: {summary['rules_skipped']}",
    ]
    if counts.get("suppressed"):
        lines.append(
            f"Suppressed (lift-and-shift): {counts['suppressed']} architecture finding(s)"
        )
    if destination is not None:
        lines.append(f"\nFindings written to {destination}")
    console.print(Panel("\n".join(lines), title="Summary"))

    top = report["remediation"][:5]
    if top:
        priority = Table(title="Highest-leverage remediation")
        priority.add_column("Rule")
        priority.add_column("Finding")
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
    table.add_column("Severity")
    table.add_column("Manifest")
    table.add_column("Title")
    for meta in sorted(REGISTRY.values(), key=lambda m: m.rule_id):
        table.add_row(
            meta.rule_id,
            CATEGORY_LABELS.get(meta.category, meta.category),
            meta.tier,
            meta.default_severity,
            "yes" if meta.requires_manifest else "-",
            meta.title,
        )
    console.print(table)


def main() -> None:
    """Entry point for the ``dbt-audit`` script."""
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
