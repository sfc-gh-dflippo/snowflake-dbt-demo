"""CLI interface for the conversion checker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .comparator import compare_workflow
from .dbt_parser import parse_dbt_model
from .infa_parser import parse_infa_xml
from .manifest import build_manifest, get_testable_workflows, load_manifest, save_manifest
from .reporter import save_json_report

import yaml


# ──────────────────────────────────────────────────────────────
# Reference resolution (sources, vars)
# ──────────────────────────────────────────────────────────────

_SOURCE_RE = re.compile(
    r"\{\{\s*source\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}"
)
_VAR_RE = re.compile(r"\{\{\s*var\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}")
_SAFE_WF_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _resolve_env_var(val: str) -> str:
    """Resolve {{ env_var('X', 'DEFAULT') }} to DEFAULT."""
    result = re.sub(
        r"\{\{\s*env_var\s*\(\s*['\"][^'\"]+['\"]\s*,\s*['\"]([^'\"]*)['\"]?\s*\)\s*\}\}",
        r"\1", val,
    )
    result = re.sub(r"\{\{.*?\}\}", "", result)
    return result.strip()


def _load_all_sources(dbt_project_dir: Path) -> dict[str, dict[str, str]]:
    """Load all source YAML files into {source_name: {table: FQN}}."""
    source_files = [
        dbt_project_dir / "models" / "SOURCES" / "snowflake_sources.yml",
        dbt_project_dir / "models" / "SOURCES" / "external_sources.yml",
        dbt_project_dir / "models" / "SOURCES" / "snowflake_references.yml",
    ]
    lookup: dict[str, dict[str, str]] = {}
    for sources_path in source_files:
        if not sources_path.exists():
            continue
        with open(sources_path) as f:
            data = yaml.safe_load(f)
        for source in data.get("sources", []):
            source_name = source["name"]
            db = _resolve_env_var(source.get("database", ""))
            schema = _resolve_env_var(source.get("schema", source_name))
            table_map: dict[str, str] = {}
            for t in source.get("tables", []):
                tname = t["name"]
                fqn = f"{db}.{schema}.{tname}" if db else f"{schema}.{tname}"
                table_map[tname] = fqn
            if source_name in lookup:
                lookup[source_name].update(table_map)
            else:
                lookup[source_name] = table_map
    return lookup


def _load_all_vars(dbt_project_dir: Path) -> dict[str, str]:
    """Load vars from dbt_project.yml."""
    project_path = dbt_project_dir / "dbt_project.yml"
    if not project_path.exists():
        return {}
    with open(project_path) as f:
        data = yaml.safe_load(f)
    resolved: dict[str, str] = {}
    for k, v in data.get("vars", {}).items():
        val = re.sub(r"\{\{.*?\}\}", "", str(v)).strip().strip("'\"")
        resolved[k] = val
    return resolved


def _resolve_refs_for_workflow(
    dbt_path: Path,
    sources_lookup: dict[str, dict[str, str]],
    vars_lookup: dict[str, str],
) -> dict:
    """Resolve all source() and var() references for a workflow's models."""
    wf_dir = dbt_path.parent
    all_sql_files = list(wf_dir.glob("*.sql"))

    resolved_sources: dict[str, str] = {}
    resolved_vars: dict[str, str] = {}

    for sql_file in all_sql_files:
        content = sql_file.read_text(encoding="utf-8", errors="replace")
        for source_name, table_name in _SOURCE_RE.findall(content):
            key = f"source('{source_name}', '{table_name}')"
            if source_name in sources_lookup:
                resolved_sources[key] = sources_lookup[source_name].get(
                    table_name, f"UNRESOLVED:{source_name}.{table_name}")
            else:
                resolved_sources[key] = f"UNRESOLVED:{source_name}.{table_name}"
        for var_name in _VAR_RE.findall(content):
            if var_name in vars_lookup:
                resolved_vars[var_name] = vars_lookup[var_name]
            else:
                resolved_vars[var_name] = f"UNRESOLVED:{var_name}"

    return {"resolved_sources": resolved_sources, "resolved_vars": resolved_vars}


def _validate_workflow_name(name: str) -> None:
    if not _SAFE_WF_RE.fullmatch(name):
        print(f"Error: workflow name contains unsafe characters: {name!r}", file=sys.stderr)
        sys.exit(1)


def _cmd_manifest(args: argparse.Namespace) -> None:
    """Build workflow manifest."""
    mapping_csv = Path(args.mapping_csv)
    xml_dir = Path(args.xml_dir)
    dbt_dir = Path(args.dbt_dir)
    output = Path(args.output)

    manifest = build_manifest(mapping_csv, xml_dir, dbt_dir)
    save_manifest(manifest, output)

    testable = get_testable_workflows(manifest)
    has_xml = sum(1 for v in manifest.values() if v.get("xml_path"))
    has_dbt = sum(1 for v in manifest.values() if v.get("dbt_path"))
    print(f"Manifest built: {len(manifest)} workflows")
    print(f"  Has XML: {has_xml}")
    print(f"  Has DBT: {has_dbt}")
    print(f"  Testable (both): {len(testable)}")
    print(f"Saved to: {output}")


def _cmd_check(args: argparse.Namespace) -> None:
    """Run conversion checks."""
    manifest = load_manifest(Path(args.manifest))
    output_base = Path(args.report) if args.report else None

    # Locate the dbt project root by walking up from a model path until a
    # dbt_project.yml appears — sources.yml and vars are resolved relative to it.
    dbt_project_dir = None
    for info in manifest.values():
        if info.get("dbt_path"):
            p = Path(info["dbt_path"])
            for parent in p.parents:
                if (parent / "dbt_project.yml").exists():
                    dbt_project_dir = parent
                    break
            if dbt_project_dir:
                break

    # Load source/var lookups once
    sources_lookup = _load_all_sources(dbt_project_dir) if dbt_project_dir else {}
    vars_lookup = _load_all_vars(dbt_project_dir) if dbt_project_dir else {}

    # Reject workflow names with path-unsafe characters before any path construction.
    _validate_workflow_name(args.workflow)

    wf_key = args.workflow.lower()
    if wf_key not in manifest:
        print(f"Error: workflow '{args.workflow}' not in manifest", file=sys.stderr)
        sys.exit(1)

    info = manifest[wf_key]
    xml_path = info.get("xml_path")
    dbt_path = info.get("dbt_path")
    candidates = info.get("dbt_candidates") or []

    # An ambiguous primary is a hard stop, not a guess. The `_wf` directory holds one
    # model per Informatica pipeline and the primary is frequently not the one named
    # after the directory, so any automatic choice here compares the wrong file and
    # every finding downstream is about the wrong model. Emitting the candidates as an
    # artifact and failing makes the stop something a caller cannot reason past --
    # prose in the skill can be, and has been, argued around.
    if not dbt_path and candidates:
        out = (output_base if output_base is None or output_base.suffix == ""
               else output_base.parent)
        if out is not None:
            target = out / wf_key / "work"
            target.mkdir(parents=True, exist_ok=True)
            if not target.resolve().is_relative_to(out.resolve()):
                print("Error: output path escapes report directory", file=sys.stderr)
                sys.exit(1)
            (target / "primary_ambiguous.json").write_text(
                json.dumps({
                    "workflow": wf_key,
                    "reason": "The dbt _wf directory holds more than one model; "
                              "the primary cannot be derived from the directory name.",
                    "candidates": candidates,
                    "resolution": "Re-run with the primary named explicitly in the "
                                  "manifest's dbt_path for this workflow.",
                }, indent=2) + "\n",
                encoding="utf-8")
        print(f"Error: {wf_key} has {len(candidates)} candidate models and no primary "
              f"named in the manifest. Candidates:", file=sys.stderr)
        for c in candidates:
            print(f"  {c}", file=sys.stderr)
        print("Name the primary in the manifest's dbt_path and re-run.", file=sys.stderr)
        sys.exit(2)

    # One explicitly-requested workflow that cannot be checked is a failure, not
    # something to skip past: the caller is blocked on this single result, and a
    # silent skip leaves them looking for a check.json that was never written.
    if not xml_path or not dbt_path:
        missing = "XML" if not xml_path else "DBT model"
        print(f"Error: {wf_key} has no {missing} path in the manifest", file=sys.stderr)
        sys.exit(1)

    xml_p = Path(xml_path)
    dbt_p = Path(dbt_path)

    if not xml_p.exists():
        print(f"Error: XML not found: {xml_path}", file=sys.stderr)
        sys.exit(1)
    if not dbt_p.exists():
        print(f"Error: DBT model not found: {dbt_path}", file=sys.stderr)
        sys.exit(1)

    infa = parse_infa_xml(xml_p, args.workflow)
    if infa is None:
        print(f"Error: could not parse XML: {xml_path}", file=sys.stderr)
        sys.exit(1)

    dbt = parse_dbt_model(dbt_p, sources_lookup, vars_lookup)
    result = compare_workflow(infa, dbt, xml_path=str(xml_p), dbt_path=str(dbt_p),
                              sources_lookup=sources_lookup, vars_lookup=vars_lookup)

    icon = {"PASS": "✓", "FAIL": "✗", "PARTIAL": "~"}.get(result.verdict, "?")
    print(f"  {icon} {wf_key}: {result.verdict}")

    if not output_base:
        return

    out_dir = output_base if output_base.suffix == "" else output_base.parent
    # Use validated wf_key (from --workflow CLI arg), not result.workflow (raw XML NAME),
    # to prevent path traversal via a crafted WORKFLOW NAME attribute.
    wf_dir = out_dir / wf_key
    # Everything the run produces on the way to an answer goes in work/. Only
    # final_verdict.json, written by the skill at the end, sits at wf_dir level, so a
    # reader sees the verdict and has to opt in to the evidence behind it.
    work_dir = wf_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    if not work_dir.resolve().is_relative_to(out_dir.resolve()):
        print("Error: output path escapes report directory", file=sys.stderr)
        sys.exit(1)

    # work/check.json — kept as a single-element array so critic.py and any
    # downstream consumer of the existing artifact shape keep working.
    save_json_report([result], work_dir / "check.json")

    # work/unresolved.json
    if result.unresolved:
        unresolved_items = [
            {"section": u.section, "reason": u.reason,
             "infa_sql": u.infa_sql, "dbt_sql": u.dbt_sql}
            for u in result.unresolved
        ]
        (work_dir / "unresolved.json").write_text(
            json.dumps(unresolved_items, indent=2), encoding="utf-8")

    # wf_foo/siblings.json
    if result.sibling_context:
        from dataclasses import asdict as _asdict
        (work_dir / "siblings.json").write_text(
            json.dumps(_asdict(result.sibling_context), indent=2), encoding="utf-8")

    # wf_foo/dbt_primary.sql and wf_foo/dbt_siblings.json — Jinja pre-resolved.
    # Informatica's N pipelines decompose into N models in one _wf directory, so
    # logic "missing" from the primary often lives in a sibling's body, pre_hook or
    # post_hook. Emitting every sibling with source()/var()/ref() already resolved
    # means the adjudication step reads concrete identifiers instead of re-deriving
    # them, and cannot miss a sibling it never thought to open.
    if dbt_p.exists() and (sources_lookup or vars_lookup):
        from .dbt_parser import resolve_jinja

        raw_primary = dbt_p.read_text(encoding="utf-8", errors="replace")
        (work_dir / "dbt_primary.sql").write_text(
            resolve_jinja(raw_primary, sources_lookup, vars_lookup), encoding="utf-8")

        siblings_sql = []
        for sql_file in sorted(dbt_p.parent.glob("*.sql")):
            if sql_file.name == dbt_p.name:
                continue
            raw_sib = sql_file.read_text(encoding="utf-8", errors="replace")
            siblings_sql.append({
                "name": sql_file.stem,
                "sql": resolve_jinja(raw_sib, sources_lookup, vars_lookup),
            })
        if siblings_sql:
            (work_dir / "dbt_siblings.json").write_text(
                json.dumps(siblings_sql, indent=2), encoding="utf-8")

    print(f"\nResults saved to: {work_dir}/")
    if result.unresolved:
        print(f"Unresolved sections for LLM: {len(result.unresolved)} items")


def _cmd_critic(args: argparse.Namespace) -> None:
    """Run critic checks on a workflow's checker output."""
    from .critic import run_critic_checks

    _validate_workflow_name(args.workflow)

    reports_dir = Path(args.reports_dir)
    wf = args.workflow.lower()
    wf_dir = reports_dir / wf

    # Artifacts live in work/ so that only final_verdict.json surfaces at wf_dir level.
    # Report directories produced before that change keep them flat, so fall back rather
    # than failing on an older tree.
    work_dir = wf_dir / "work"
    if not (work_dir / "check.json").exists() and (wf_dir / "check.json").exists():
        work_dir = wf_dir

    result_path = work_dir / "check.json"
    unresolved_path = work_dir / "unresolved.json"

    if not result_path.exists():
        print(f"ERROR: {result_path} not found")
        return

    with open(result_path) as f:
        raw = json.load(f)
        result = raw[0] if isinstance(raw, list) else raw

    unresolved = []
    if unresolved_path.exists():
        with open(unresolved_path) as f:
            unresolved = json.load(f)

    checks = run_critic_checks(result, unresolved)

    # Summary
    passed = sum(1 for c in checks if c["status"] == "PASS")
    failed = sum(1 for c in checks if c["status"] == "FAIL")

    output = {
        "workflow": wf,
        "summary": {"passed": passed, "failed": failed, "total": len(checks)},
        "checks": checks,
    }

    out_path = work_dir / "critic.json"
    if not out_path.resolve().is_relative_to(reports_dir.resolve()):
        print("Error: output path escapes reports directory", file=sys.stderr)
        sys.exit(1)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Critic: {passed}/{len(checks)} passed, {failed} issues found")
    print(f"Output: {out_path}")

    if failed:
        for c in checks:
            if c["status"] == "FAIL":
                print(f"  FAIL: {c['check']} — {c['detail']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="conversion_checker",
        description="INFA vs DBT static conversion comparison tool",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # manifest subcommand
    p_manifest = subparsers.add_parser("manifest", help="Build workflow manifest")
    p_manifest.add_argument("--mapping-csv", required=True,
                            help="CSV with 'Informatica Workflow Name' and 'DBT Model Name' columns")
    p_manifest.add_argument("--xml-dir", required=True, help="Path to XML directory")
    p_manifest.add_argument("--dbt-dir", required=True, help="Path to the dbt models root")
    p_manifest.add_argument("--output", required=True, help="Output manifest JSON path")

    # check subcommand
    p_check = subparsers.add_parser("check", help="Run conversion checks")
    p_check.add_argument("--manifest", required=True, help="Path to manifest JSON")
    p_check.add_argument("--report", help="Output report base path")
    p_check.add_argument("--workflow", required=True, help="Workflow to check")

    # critic subcommand
    p_critic = subparsers.add_parser("critic", help="Run critic checks on checker output")
    p_critic.add_argument("--workflow", required=True, help="Workflow name (e.g. wf_MT_CX_CENTRALIZED_COGS)")
    p_critic.add_argument("--reports-dir", required=True, help="Directory containing result/unresolved files")

    args = parser.parse_args()

    if args.command == "manifest":
        _cmd_manifest(args)
    elif args.command == "check":
        _cmd_check(args)
    elif args.command == "critic":
        _cmd_critic(args)
