"""Mine-phase driver for the Synthetic Testbed Generator orchestration skill.

v0 sequences the workload-scoped mine phase:
    init  ->  list-unsolved (whole workload)  ->  write the categorized view.
Resume recomputes the frontier from on-disk artifacts (state.bin + the view),
never from a progress log. No enrich, no materialize (post-v0).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from subcommands import TestbedCli, default_runner, enumerate_artifacts  # noqa: E402
from recovery import RecoveryClass, classify  # noqa: E402
from manifest import Manifest, classify_rejections  # noqa: E402
from assembler import (  # noqa: E402
    load_fragments, assemble, structural_coverage_warnings, value_conflict_warnings, AssemblyError)
from critic_index import load_index  # noqa: E402
from critic_backbone import run_backbone, build_critique_request, reads_column_facts, CheckStatus  # noqa: E402
from critic_gate import parse_verdict, apply_gate, GateAction  # noqa: E402

STATE_REL = ".scai/testbed/state.bin"  # written by init (opaque; driver never touches)
VIEW_REL = "testbed/mine/unsolved-view.json"  # non-hidden: it's the state-machine completion predicate
COMPILE_VIEW_REL = "testbed/compile/clusters-view.json"  # non-hidden: the compile-phase completion predicate
VALIDATE_VIEW_REL = "testbed/validate/readiness-view.json"  # non-hidden: the validate-phase completion predicate
GENERATE_VIEW_REL = "testbed/generate/summary-view.json"  # non-hidden: the TERMINAL completion predicate
ENRICH_VIEW_REL = "testbed/enrich/enrichment-view.json"  # completion predicate: present <=> ready
ENRICH_REPORT_REL = "testbed/enrich/enrichment-report.json"  # not-ready / reject diagnostics
FRAGMENTS_DIR_REL = "testbed/enrich/fragments"
CRITIQUE_REQUEST_REL = "testbed/enrich/critic/critique-request.json"
CRITIC_VERDICT_REL = "testbed/enrich/critic/verdict.json"
CRITIC_PROMPT_TYPE = "critic"  # the max_rejections_per_type bucket critic re-author rounds draw down
QUARANTINE_REL = ".scai/testbed/quarantine"
MAX_QUARANTINE_ATTEMPTS = 20
# PENDING key for a malformed whole-workload entry that carries no identity to attribute it to.
WORKLOAD_PENDING_KEY = "inspect-branches"
# The validate report's issue buckets, in CLI declaration order. Every consumer enumerates this instead
# of naming buckets inline: `counts` is copied wholesale so a new CLI tally rides through free, but an
# array is persisted only if a writer names it — a new bucket would otherwise default to unlisted.
ISSUE_BUCKETS = ("fk_gaps", "type_conflicts", "unsatisfied_constraints", "overlaps")


def _present(project_dir: str, rel: str) -> bool:
    return (Path(project_dir) / rel).exists()


def _as_dict(result) -> dict:
    # A success envelope can still carry a null/non-dict `result` (the CLI drops empty
    # payloads), so normalize before the view writers' .get() calls — which would else
    # AttributeError on None, mirroring the guard _collect_branches already applies.
    return result if isinstance(result, dict) else {}


def _write_json(path: Path, obj: dict) -> None:
    # Atomic write: the views are task-completion predicates checked by a
    # filesystemProxy glob, so a crash mid-write must not leave a truncated file
    # that still satisfies the glob. Mirror manifest.save: write a temp sibling,
    # then os.replace (atomic on POSIX).
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    # Explicit utf-8, matching every reader of these views. Not a live crash fix: json.dumps
    # escapes non-ASCII, so this payload is pure ASCII and writes identically under any
    # ASCII-superset locale codec. The pin declares the views' encoding at the call site instead of
    # inheriting the host's, which is what the readers below (and the guard test) rely on.
    tmp.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _categorize(constraints: list[dict]) -> dict:
    by_kind: dict[str, list] = {}
    for c in constraints:
        by_kind.setdefault(c.get("kind", "unknown"), []).append(c)
    return {k: {"count": len(v), "constraints": v} for k, v in sorted(by_kind.items())}


def _write_mine_view(project_dir: str, result: dict, branches: list, manifest: Manifest) -> dict:
    result = _as_dict(result)
    constraints = result.get("constraints", [])
    view = {
        "schema_version": 1,
        "json_schema_version": result.get("json_schema_version"),
        "total": len(constraints),
        "by_kind": _categorize(constraints),
        "branches": branches,
        "pending": manifest.pending,
    }
    p = Path(project_dir) / VIEW_REL
    _write_json(p, view)
    return view


def _branch_ids(obj, raw, manifest):
    """(branch_count, unsolved_branch_ids) for one object's `branches` payload.

    A *successful* envelope can still carry malformed branch data — a null/non-list `branches`, a
    non-dict branch element, or an unsolved branch with no branch_id. Each is treated the same way:
    the offending object (or branch) is recorded PENDING so the unsolved work stays traceable in
    both the view and the run.json ledger — never silently dropped, never aborting."""
    if isinstance(raw, list):
        branches = raw
    else:
        # Absent/null/non-list branches can't be enumerated (len(None) would abort).
        branches = []
        manifest.record_pending(
            obj, f"malformed inspect-branches result: 'branches' is not a list ({type(raw).__name__})")
    unsolved = []
    for b in branches:
        if not isinstance(b, dict):
            # A non-dict element would AttributeError on b.get(); keep it traceable.
            manifest.record_pending(obj, "malformed branch: not a JSON object")
            continue
        if b.get("solution_status") != "unsolved":
            continue
        bid = b.get("branch_id")
        if bid is None:
            # Unsolved work with no id: record PENDING rather than silently
            # dropping it — the contract is "record PENDING and skip", not "skip".
            manifest.record_pending(obj, "unsolved branch missing branch_id")
            continue
        unsolved.append(bid)
    return len(branches), unsolved


def _workload_failure(env):
    """Why the whole-workload envelope is unusable, or None when it carries an `objects` list."""
    if not env.success:
        return f"{env.error.code}: {env.error.message}"
    if not isinstance(env.result, dict):
        return "malformed inspect-branches result: not a JSON object"
    objects = env.result.get("objects")
    if not isinstance(objects, list):
        return ("malformed inspect-branches result: 'objects' is not a list "
                f"({type(objects).__name__})")
    return None


def _collect_branches(project_dir, artifacts_path, cli, manifest):
    """Whole-workload inspect-branches drill-down over the surviving artifacts.
    Runs after list-unsolved (which already quarantined any malformed artifact).

    One no-<object> call projects every branch-carrying object from a single state.bin load, so the
    drill-down costs one process for the workload rather than one per procedure. A *known*
    non-procedure (TABLE/VIEW/…) folds in a branch_count:0 entry directly — it is not in the
    procedure state, so the projection never mentions it. An artifact whose type is absent (which
    init may still resolve to a procedure via the CUR registry) is expected in that projection:
    treating it as a non-procedure would silently zero-branch a real procedure.

    Unlike the per-object form, a failed call is NOT isolable — it costs every candidate its
    drill-down — so each is recorded PENDING individually, keyed by stem. A candidate the projection
    never mentions (an untyped artifact that was really a table, say) is recorded PENDING the same
    way: traceable, never a silent branch_count 0.

    PENDING records accumulate on the manifest and the caller persists the ledger once
    after the drill-down: a kill mid-drill-down leaves no view, so resume re-runs the
    whole drill-down from scratch — per-record saves would only add O(n^2) rewrites."""
    refs = enumerate_artifacts(artifacts_path)
    # Everything except a KNOWN non-procedure: inspect-branches (BranchInspector) projects only
    # branch sources, and a missing type ("") may still be a registry-typed procedure, so the CLI
    # stays authoritative rather than us zero-branching it here.
    expected = [ref for ref in refs if not (ref.object_type and ref.object_type != "PROCEDURE")]
    drilled = {}

    if expected:
        env = cli.inspect_branches(project_dir)
        reason = _workload_failure(env)
        if reason is not None:
            for ref in expected:
                manifest.record_pending(ref.stem, reason)
        else:
            # state.bin is authoritative for what exists; the stem stays the view/quarantine key, so
            # each entry is joined back onto the mined identity the CLI echoes in `object`.
            stem_by_identity = {ref.object_name: ref.stem for ref in expected}
            for entry in env.result["objects"]:
                if not isinstance(entry, dict):
                    manifest.record_pending(
                        WORKLOAD_PENDING_KEY, "malformed workload entry: not a JSON object")
                    continue
                obj = entry.get("object")
                if not isinstance(obj, str) or not obj:
                    manifest.record_pending(
                        WORKLOAD_PENDING_KEY, "malformed workload entry: no 'object' identity")
                    continue
                count, unsolved = _branch_ids(obj, entry.get("branches"), manifest)
                stem = stem_by_identity.get(obj, obj)
                drilled[stem] = {
                    "object": obj,
                    "stem": stem,
                    "branch_count": count,  # a procedure with no unsolved branches legitimately has 0
                    "unsolved_branches": unsolved,
                }
            for ref in expected:
                if ref.stem not in drilled:
                    manifest.record_pending(
                        ref.stem, "inspect-branches projected no branches for this artifact")

    # Emitted in enumerate_artifacts order (sorted by stem) so the view stays stable regardless of
    # the order the CLI returns objects in.
    out = []
    for ref in refs:
        if ref.object_type and ref.object_type != "PROCEDURE":
            out.append({"object": ref.object_name, "stem": ref.stem,
                        "branch_count": 0, "unsolved_branches": []})
        elif ref.stem in drilled:
            out.append(drilled[ref.stem])
    return out


def _mine_summary(view: dict) -> str:
    kinds = ", ".join(f"{k}={v['count']}" for k, v in view["by_kind"].items()) or "none"
    return (f"mine complete: {view['total']} unsolved constraints ({kinds}); "
            f"{len(view['branches'])} objects inspected")


def _write_compile_view(project_dir: str, result: dict, manifest: Manifest) -> dict:
    # Counts-only: cluster membership stays inside the opaque state.bin and is only
    # surfaceable once `generate` lands. state_path is dropped so no absolute path
    # leaks into the deliverable.
    result = _as_dict(result)
    view = {
        "schema_version": 1,
        "json_schema_version": result.get("json_schema_version"),
        "clusters": result.get("clusters", 0),
        "coupled_objects": result.get("coupled_objects", 0),
        "singleton_objects": result.get("singleton_objects", 0),
        "largest_cluster": result.get("largest_cluster", 0),
        "pending": manifest.pending,
    }
    p = Path(project_dir) / COMPILE_VIEW_REL
    _write_json(p, view)
    return view


def _compile_summary(view: dict) -> str:
    return (f"compile complete: {view['clusters']} clusters "
            f"({view['coupled_objects']} coupled, {view['singleton_objects']} singletons, "
            f"largest={view['largest_cluster']})")


def _write_readiness_view(project_dir: str, result: dict, manifest: Manifest) -> dict:
    result = _as_dict(result)
    view = {
        "schema_version": 1,
        "json_schema_version": result.get("json_schema_version"),
        "ready": result.get("ready", False),
        "counts": result.get("counts", {}),
        **{bucket: result.get(bucket, []) for bucket in ISSUE_BUCKETS},
        "pending": manifest.pending,
    }
    p = Path(project_dir) / VALIDATE_VIEW_REL
    _write_json(p, view)
    return view


def _validate_summary(view: dict) -> str:
    c = view["counts"]
    status = "ready" if view["ready"] else "not ready"
    # Every bucket gets a term, so the terms can never sum below the blocking count the line
    # announces. They are listed after the tallies rather than parenthesised onto `advisory`: the
    # terms span both severities, so "0 advisory (2 overlaps)" would read as an advisory breakdown
    # while naming the very issues that block the run.
    buckets = ", ".join(f"{c.get(bucket, 0)} {bucket.replace('_', ' ')}" for bucket in ISSUE_BUCKETS)
    return (f"validate complete: {status}; {c.get('blocking', 0)} blocking, "
            f"{c.get('advisory', 0)} advisory; by bucket: {buckets}")


def _write_summary_view(project_dir: str, result: dict,
                        readiness_overridden: bool, manifest: Manifest) -> dict:
    # Zero ints and null strings are dropped by the CLI envelope writer, so the
    # driver re-defaults them here (csv_files/tables/rows_written -> 0, manifest_path
    # /note -> None, warnings -> []). out_path comes straight from the CLI (it derives the
    # location); readiness_overridden + pending are driver-injected.
    result = _as_dict(result)
    view = {
        "schema_version": 1,
        "json_schema_version": result.get("json_schema_version"),
        "out_path": result.get("out_path"),
        "tables": result.get("tables", 0),
        "rows_written": result.get("rows_written", 0),
        "csv_files": result.get("csv_files", 0),
        "manifest_path": result.get("manifest_path"),
        "note": result.get("note"),
        # Non-fatal generation diagnostics (e.g. a declared width too narrow for row_count distinct
        # keys). The CLI omits the key when clean; surface it so width collisions reach the agent.
        "warnings": result.get("warnings") or [],
        "readiness_overridden": readiness_overridden,
        "pending": manifest.pending,
    }
    p = Path(project_dir) / GENERATE_VIEW_REL
    _write_json(p, view)
    return view


def _generate_summary(view: dict) -> str:
    override = " (readiness overridden)" if view.get("readiness_overridden") else ""
    note = f"; {view['note']}" if view.get("note") else ""
    warnings = view.get("warnings") or []
    warn = f"; {len(warnings)} warning(s)" if warnings else ""
    return (f"generate complete: {view['tables']} tables, {view['rows_written']} rows "
            f"across {view['csv_files']} CSV files{override}{warn}{note}")


def _fail(env, station: str) -> tuple[int, str]:
    error = env.error
    return 1, f"{station} failed [{error.code}] {error.message} ({classify(error.code).value})"


def run_mine(project_dir: str, artifacts_path: str | None, cli: TestbedCli) -> tuple[int, str]:
    project_dir = str(project_dir)
    artifacts_path = artifacts_path or str(Path(project_dir) / "artifacts")
    manifest = Manifest.load(project_dir)

    if _present(project_dir, VIEW_REL):
        return 0, "mine already complete (unsolved view present)"

    # init only if state absent; both init and list-unsolved abort atomically on a
    # malformed artifact (C5), so both run under the same quarantine-and-retry loop.
    if not _present(project_dir, STATE_REL):
        _, fail = _run_with_quarantine(
            "init", lambda: cli.init(project_dir), project_dir, artifacts_path, manifest)
        if fail is not None:
            return fail

    env, fail = _run_with_quarantine(
        "list-unsolved", lambda: cli.list_unsolved(project_dir),
        project_dir, artifacts_path, manifest)
    if fail is not None:
        return fail

    # per-object branch drill-down over the survivors (list-unsolved already
    # quarantined any malformed artifact). A per-object failure is isolable:
    # record PENDING and skip, never abort the mine.
    branches = _collect_branches(project_dir, artifacts_path, cli, manifest)
    view = _write_mine_view(project_dir, env.result, branches, manifest)
    manifest.mark_mine_complete()
    manifest.save(project_dir)
    return 0, _mine_summary(view)


def run_compile(project_dir: str, cli: TestbedCli) -> tuple[int, str]:
    # Compile reads only the opaque state.bin (written by init/mine); it never reads
    # the mine view, so the phases resume independently. Idempotent: the view being
    # present is the completion predicate.
    project_dir = str(project_dir)
    manifest = Manifest.load(project_dir)

    if _present(project_dir, COMPILE_VIEW_REL):
        return 0, "compile already complete (clusters view present)"

    env = cli.compile(project_dir)
    if not env.success:
        return _fail(env, "compile")  # TBD0002 -> input_config (run mine first); TBD0003/4/5 -> escalate

    view = _write_compile_view(project_dir, env.result, manifest)
    manifest.mark_compile_complete()
    manifest.save(project_dir)
    return 0, _compile_summary(view)


def run_validate(project_dir: str, cli: TestbedCli) -> tuple[int, str]:
    # Validate reads the mined state and reports readiness; it never mutates state.
    # Idempotent: the readiness view being present is the completion predicate.
    # ready==false is STILL success — the issues are carried in the view, not the rc.
    project_dir = str(project_dir)
    manifest = Manifest.load(project_dir)

    if _present(project_dir, VALIDATE_VIEW_REL):
        return 0, "validate already complete (readiness view present)"

    env = cli.validate(project_dir)
    if not env.success:
        return _fail(env, "validate")  # TBD0002 -> input_config (run mine first); TBD0003/4/5 -> escalate

    view = _write_readiness_view(project_dir, env.result, manifest)
    manifest.mark_validate_complete()
    manifest.save(project_dir)
    return 0, _validate_summary(view)


def _readiness_gate(project_dir: str, ignore_readiness: bool) -> tuple[bool, str, bool]:
    # Guard generate on the validate readiness view: it must exist, parse, and report
    # ready — unless the caller overrides. Returns (ok, block_message, overridden): when
    # ok the message is empty and `overridden` flags a forced not-ready run.
    readiness_path = Path(project_dir) / VALIDATE_VIEW_REL
    if not readiness_path.exists():
        return False, "generate blocked: run validate first", False
    try:
        readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        # Predicate files are atomic-written, but a crash mid-write (or a hand-edit) can still
        # truncate one — mid-codepoint (UnicodeDecodeError), malformed (JSONDecodeError), or racing
        # a reader (OSError); surface it as a clean block like every other driver failure, not a traceback.
        return False, "generate blocked: readiness view unreadable; re-run validate", False
    ready = bool(readiness.get("ready", False))
    if not ready and not ignore_readiness:
        # `counts` can be present-but-null in a hand-edited view; `or {}` guards the None
        # that a plain .get("counts", {}) default would let through into .get("blocking").
        blocking = (readiness.get("counts") or {}).get("blocking", 0)
        return False, (f"generate blocked: {blocking} blocking issue(s); "
                       "re-run with --ignore-readiness to override"), False
    return True, "", not ready


def run_generate(project_dir: str, cli: TestbedCli,
                 rows: int | None = None, seed: int | None = None,
                 ignore_readiness: bool = False) -> tuple[int, str]:
    # Generate consumes the compiled clusters + validated readiness and writes each
    # table's CSV into its own artifacts folder plus a manifest beside state.bin (the
    # CLI derives those paths — no output dir is passed). Idempotent: the summary view
    # is the TERMINAL completion predicate. A readiness gate guards it: generate must
    # not run before validate, nor against a not-ready workspace unless the caller
    # explicitly overrides.
    project_dir = str(project_dir)
    manifest = Manifest.load(project_dir)

    if _present(project_dir, GENERATE_VIEW_REL):
        return 0, "generate already complete (summary view present)"

    ok, block_message, readiness_overridden = _readiness_gate(project_dir, ignore_readiness)
    if not ok:
        return 1, block_message

    env = cli.generate(project_dir, rows, seed)
    if not env.success:
        return _fail(env, "generate")  # TBD0012 -> input_config (run compile first); TBD0003/4/5 -> escalate

    view = _write_summary_view(project_dir, env.result, readiness_overridden, manifest)
    manifest.mark_generate_complete()
    manifest.save(project_dir)
    return 0, _generate_summary(view)


def _read_json(project_dir, rel):
    p = Path(project_dir) / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        # Mirror _readiness_gate: a truncated/unreadable predicate (crash mid-write, permissions,
        # partial write) degrades to None rather than raising straight out of the driver --
        # including the mid-codepoint truncation, which raises UnicodeDecodeError (a ValueError,
        # so it escapes OSError). The explicit utf-8 is what makes the degrade reachable at all:
        # on the locale default a non-UTF-8 host decodes an accented view to mojibake without
        # raising, so nothing degrades and the driver reads names that were never written.
        return None


def _blocking_issues(report):
    # Gate on each issue's own severity, not counts.blocking: the tally can disagree with
    # the issues actually present, and it's the per-issue remediation the agent must act on.
    out = []
    for bucket in ISSUE_BUCKETS:
        for issue in report.get(bucket, []):
            if issue.get("severity") == "blocking":
                out.append({"bucket": bucket, "id": issue.get("id"),
                            "remediation": issue.get("remediation", {}), "detail": issue.get("detail", "")})
    return out


def _clear_stale_report(project_dir):
    # On ready, delete any prior not-ready/reject report so the view and diagnostics can't disagree.
    p = Path(project_dir) / ENRICH_REPORT_REL
    if p.exists():
        p.unlink()


def _commit_enrich_ready(project_dir, manifest, report, applied, warnings, note):
    # The single enrich success-commit path, shared by run_enrich and the CAS-retry loop so the two
    # can't drift when the view schema changes. Order matters: mark complete FIRST so the enrichment
    # block embedded in the view carries ready=True — it's a live reference to manifest.enrichment, so
    # writing the view before mark_enrich_complete() would persist enrichment.ready=false alongside the
    # top-level ready=true, leaving two disagreeing signals in one artifact. Then persist the view (the
    # completion predicate), drop any prior not-ready/reject report, and save the ledger.
    manifest.mark_enrich_complete()
    _write_json(Path(project_dir) / ENRICH_VIEW_REL,
                {"schema_version": 1, "ready": True, "counts": report.get("counts", {}),
                 "applied": applied, "warnings": warnings, "enrichment": manifest.enrichment})
    _clear_stale_report(project_dir)
    _clear_critic_state(project_dir)
    manifest.save(project_dir)
    return 0, note


def _enrich_stop(project_dir, manifest, kind, report, warnings, msg):
    payload = {"schema_version": 1, "ready": False, "stop_kind": kind, "warnings": warnings, **report,
               "enrichment": manifest.enrichment}
    _write_json(Path(project_dir) / ENRICH_REPORT_REL, payload)
    manifest.save(project_dir)
    return 1, msg


def _stop_not_ready(project_dir, manifest, report, warnings, max_iterations, iterate_msg) -> tuple[int, str]:
    # The shared not-ready tail for both the main path and the CAS-retry-win branch (they had a
    # verbatim copy each, same change-driver as _commit_enrich_ready): record the iteration, then
    # bound it — iterations persist across re-invocations, so a spent budget stops as budget-exhausted
    # rather than emitting yet another unbounded iterate. Only iterate_msg differs between the two
    # callers (the budget-exhausted arm is identical), so it is the single varying parameter.
    manifest.record_iteration()
    if manifest.iteration_budget_exhausted(max_iterations):
        return _enrich_stop(project_dir, manifest, "budget-exhausted",
                            {"reason": "iteration_budget", "code": "iterate",
                             "counts": report.get("counts", {})}, warnings,
                            "enrich iteration budget exhausted; fix fragments and re-run with --reset-budget")
    return _enrich_stop(project_dir, manifest, "iterate",
                        {"reason": "not_ready", "counts": report.get("counts", {}),
                         "blocking": _blocking_issues(report)}, warnings, iterate_msg)


MAX_SAME_ENVELOPE_RETRIES = 2


def _prompt_type_for(env) -> str:
    # v1: bucket the per-type rejection budget under the reject error code. The envelope surfaces the
    # offending field only in free text (message/suggestion), so a field->prompt_type derivation is a
    # follow-up; until then every malformed-field reject (TBD0014) shares one budget bucket.
    return env.error.code if env.error else "unknown"


def _enrich_handle_reject(project_dir, manifest, env, warnings, *, cap, cli, envelope, max_iterations):
    # Single dispatch on the recovery class of the reject code — one mechanism, no second gate.
    cls = classify(env.error.code)

    if cls is RecoveryClass.RETRY:  # TBD0016: concurrent state change — retry the SAME envelope
        payload = json.dumps(envelope, sort_keys=True)
        for _ in range(MAX_SAME_ENVELOPE_RETRIES):
            manifest.record_retry()
            retried = cli.propose_enrichments(project_dir, payload)
            if retried.success:
                report = cli.validate(project_dir).result or {}
                if report.get("ready") is True:
                    return _commit_enrich_ready(
                        project_dir, manifest, report, (retried.result or {}).get("applied", []),
                        warnings, "enrich complete: ready (after CAS retry)")
                return _stop_not_ready(project_dir, manifest, report, warnings, max_iterations,
                                       "enrich not ready after CAS retry; see enrichment-report.json")
            # A retry that fails with a non-retryable code is a different failure: stop looping and
            # dispatch on THAT code below. Recompute cls so the REPROMPT / structural branches see the
            # retry's class, not the stale RETRY — else a retry that comes back TBD0014/TBD0015 skips
            # its intended branch and wrongly falls through to the structural documented-stop.
            retried_cls = classify(retried.error.code)
            if retried_cls is not RecoveryClass.RETRY:
                env, cls = retried, retried_cls
                break
        else:
            return _enrich_stop(project_dir, manifest, "documented-stop",
                                {"reason": "cas_retry_exhausted", "code": env.error.code}, warnings,
                                "enrich stopped: state kept changing under retry (TBD0016)")

    if cls is RecoveryClass.REPROMPT:  # TBD0014: malformed field — re-prompt the offending fragment
        prompt_type = _prompt_type_for(env)
        manifest.record_rejection(prompt_type)
        if manifest.rejection_budget_exhausted(prompt_type, cap):
            return _enrich_stop(project_dir, manifest, "budget-exhausted",
                                {"reason": "rejection_budget", "prompt_type": prompt_type,
                                 "code": env.error.code, "detail": env.error.message}, warnings,
                                f"enrich budget exhausted for '{prompt_type}'; fix the fragment and re-run with --reset-budget")
        return _enrich_stop(project_dir, manifest, "reject",
                            {"reason": "propose_rejected", "prompt_type": prompt_type,
                             "code": env.error.code, "detail": env.error.message}, warnings,
                            f"enrich reject [{env.error.code}]: re-prompt '{prompt_type}'; see enrichment-report.json")

    # TBD0015 (cycle) and anything else -> documented structural stop, no naive re-prompt.
    return _enrich_stop(project_dir, manifest, "documented-stop",
                        {"reason": "structural_reject", "code": env.error.code, "detail": env.error.message},
                        warnings, f"enrich stopped [{env.error.code}]: {env.error.message}")


def _envelope_sig(envelope) -> str:
    # Ties a verdict fragment to the exact envelope it critiqued: if the agent re-authors any fragment,
    # the sig changes and the stale verdict is ignored (Invocation A re-runs on the new envelope).
    return hashlib.sha256(json.dumps(envelope, sort_keys=True).encode()).hexdigest()[:16]


def _clear_critic_state(project_dir) -> None:
    for rel in (CRITIC_VERDICT_REL, CRITIQUE_REQUEST_REL):
        p = Path(project_dir) / rel
        if p.exists():
            p.unlink()


def _critic_backbone_stop(project_dir, manifest, envelope, index, warnings, sig, *, cap):
    # Backbone policy, for an envelope with no fresh verdict. A FAIL never reaches the critic: a
    # re-proposed rejected value escalates, otherwise it spends the reject budget. An all-clear writes
    # the critique request and stops for the critic's second invocation.
    checks = run_backbone(envelope, index)
    fails = [c for c in checks if c.status == CheckStatus.FAIL]
    if fails:
        # Same helper the gate's REJECT arm consumes, so "repeat rejection -> escalate as a cycle,
        # else record it" is decided in one place for both shapes of rejection.
        cycle, recorded = classify_rejections(
            ((f.identity.get("table"), f.identity.get("column"), f.identity.get("literal"))
             for f in fails),
            manifest.value_previously_rejected)
        for table, column, value in recorded:
            manifest.record_rejected_value(table, column, value)
        citations = [{"identity": f.identity, "citation": f.citation} for f in fails]
        if cycle:
            return _enrich_stop(project_dir, manifest, "documented-stop",
                                {"reason": "value_cycle", "citations": citations}, warnings,
                                "critic backbone: a previously-rejected value was re-proposed; escalating for human review")
        manifest.record_rejection(CRITIC_PROMPT_TYPE)
        if manifest.rejection_budget_exhausted(CRITIC_PROMPT_TYPE, cap):
            return _enrich_stop(project_dir, manifest, "budget-exhausted",
                                {"reason": "critic_budget", "prompt_type": CRITIC_PROMPT_TYPE,
                                 "citations": citations}, warnings,
                                "critic reject budget exhausted; fix fragments and re-run with --reset-budget")
        return _enrich_stop(project_dir, manifest, "reject",
                            {"reason": "critic_backbone", "prompt_type": CRITIC_PROMPT_TYPE,
                             "citations": citations}, warnings,
                            "critic backbone rejected an entry; re-prompt the fragment; see enrichment-report.json")
    request = build_critique_request(checks)
    request["envelope_sig"] = sig
    _write_json(Path(project_dir) / CRITIQUE_REQUEST_REL, request)
    return _enrich_stop(project_dir, manifest, "critique",
                        {"reason": "await_critic", "critique_request": CRITIQUE_REQUEST_REL,
                         "entries": len(request["entries"])}, warnings,
                        "critic backbone passed; run the critic prompt, write verdict.json, then re-run enrich")


def _critic_gate_stop(project_dir, manifest, verdict, index, warnings, *, cap):
    # Gate policy, for a verdict matching the current envelope. Returns None only on accept_all;
    # reject/revise spend the reject budget, and every other action is a documented stop.
    decision = apply_gate(verdict, index, manifest.value_previously_rejected)
    for table, column, value in decision.record_values:
        manifest.record_rejected_value(table, column, value)
    if decision.action == GateAction.ACCEPT_ALL:
        return None
    if decision.action in (GateAction.REJECT, GateAction.REVISE):
        manifest.record_rejection(CRITIC_PROMPT_TYPE)
        if manifest.rejection_budget_exhausted(CRITIC_PROMPT_TYPE, cap):
            # decision.report carries "reason": f"critic_{action}", so override it AFTER the spread:
            # a budget-exhausted stop must report critic_budget (as the backbone-reject arm does),
            # not the underlying critic_revise/critic_reject action.
            return _enrich_stop(project_dir, manifest, "budget-exhausted",
                                {**decision.report, "prompt_type": CRITIC_PROMPT_TYPE, "reason": "critic_budget"},
                                warnings, "critic revise/reject budget exhausted; fix fragments and re-run with --reset-budget")
        stop_kind = "reject" if decision.action == GateAction.REJECT else "iterate"
        return _enrich_stop(project_dir, manifest, stop_kind,
                            {"prompt_type": CRITIC_PROMPT_TYPE, **decision.report}, warnings, decision.message)
    return _enrich_stop(project_dir, manifest, "documented-stop",
                        {"prompt_type": CRITIC_PROMPT_TYPE, **decision.report}, warnings, decision.message)


def _run_critic_station(project_dir, artifacts_path, manifest, envelope, unsolved, warnings, *, cap):
    # Two-invocation bridge. Returns None to proceed to propose, else a terminal (rc, msg) stop.
    sig = _envelope_sig(envelope)
    verdict_path = Path(project_dir) / CRITIC_VERDICT_REL
    verdict = None
    if verdict_path.exists():
        # A present verdict.json that can't be read or parsed is malformed, not "stale/absent":
        # surface it rather than silently re-critiquing over a truncated/corrupt handoff (never
        # auto-apply an un-critiqued envelope). An absent file leaves verdict None -> backbone below.
        def _malformed(detail):
            return _enrich_stop(project_dir, manifest, "documented-stop",
                                {"reason": "critic_verdict_malformed", "detail": detail}, warnings,
                                "critic verdict.json malformed; a human must review "
                                "(never auto-apply an un-critiqued envelope)")
        try:
            raw = verdict_path.read_text(encoding="utf-8")
        # read_text raises UnicodeDecodeError on a handoff written mid-codepoint, which is a ValueError
        # and so escapes OSError -- crashing the run instead of reaching the documented stop above. The
        # explicit utf-8 is load-bearing for that: on the locale default a non-UTF-8 host mis-decodes
        # the handoff to mojibake without raising, so a real critique parses as different text.
        except (OSError, ValueError) as exc:
            return _malformed(f"verdict.json unreadable: {exc}")
        verdict = parse_verdict(raw)
        if not verdict.ok:
            return _malformed(verdict.error)

    # A re-authored fragment changes the sig, so a stale-but-valid verdict falls through to a fresh
    # backbone run. Build the read-only facts index once here and share it across both branches -- before
    # the accept-all fast path, or a run whose only diagnostics are index warnings reports none of them.
    fresh = verdict is not None and verdict.envelope_sig == sig
    index = load_index(artifacts_path, unsolved)
    warnings.extend(f"critic index skipped unreadable artifact {s}" for s in index.skipped)
    warnings.extend(
        f"critic index: {a}; entries naming it bare cannot be resolved to one table and are routed "
        "to the critic instead of checked deterministically" for a in index.ambiguities)
    # A qualified row the index could not attribute to any captured table. Reported for the same reason
    # `ambiguities` is: its evidence stops counting toward every other schema's cells, and without this
    # line nothing explains why (a qualified name is not ambiguous, so `ambiguities` stays empty).
    warnings.extend(f"critic index: {u}" for u in index.unattributed)
    # Both index-health diagnostics are recorded before the fast path below, for the same reason the
    # index is built there: a run whose only diagnostics are these would otherwise report none of them.
    no_root = not Path(artifacts_path).is_dir()
    if no_root:
        warnings.append(f"critic artifacts root {artifacts_path} is not a directory; column-existence "
                        "checks have no facts to read")
    elif not index.tables:
        # Warning, not a stop: a purely procedural envelope over a procedural-only artifact root is
        # legitimate, so hard-stopping here would be a false positive. It is still worth naming, since
        # it is the reason every column entry rejects rather than any property of the entries.
        warnings.append(f"critic index resolved zero TABLE artifacts under {artifacts_path}; "
                        "column-existence checks cannot pass and every column entry will be rejected")
    if fresh and not verdict.verdicts:
        return None

    # An absent root plus at least one entry that would be graded against the column facts. Both halves
    # are load-bearing, and the finding is only the conjunction: the harm is a manufactured verdict, not a
    # missing directory. With no facts every column reads as non-existent, so a fact-reading entry draws a
    # guaranteed-true-shaped FAIL worded identically to a genuinely missing column, and the gate would
    # adjudicate its citations against nothing.
    #
    # `reads_column_facts` is what keeps this from over-reaching. An envelope of only uncovered arrays
    # reads no facts at all -- the backbone's `_uncovered` inspects the entry's own keys and FLAGs -- so it
    # is graded identically with or without a root, and stopping it would contradict the reason the
    # present-but-tableless root above is only a warning: a purely procedural envelope with nothing to look
    # up is a legitimate steady state, and it stays one when the lookup target is absent rather than merely
    # empty. Such an envelope keeps its critique handoff, and the warning recorded above is what tells the
    # operator the root was missing.
    #
    # A documented-stop rather than a reject because a misconfigured root is not an entry defect: it spends
    # no reject budget and writes no rejected-value memo, so fixing the flag is enough to re-run without
    # --reset-budget. (Absent is a misconfiguration, never a steady state: the mine phase creates the
    # default root, and --artifacts-path is per-phase, so `mine --artifacts-path /elsewhere` plus a plain
    # `enrich` lands here.) It sits below the accept-all fast path deliberately -- an already-accepted
    # verdict consumes no facts either, so stopping it there would be a false positive for the same reason.
    if no_root and reads_column_facts(envelope):
        return _enrich_stop(project_dir, manifest, "documented-stop",
                            {"reason": "critic_no_artifacts", "artifacts_path": str(artifacts_path)},
                            warnings,
                            f"critic artifacts root {artifacts_path} is not a directory; pass "
                            "--artifacts-path (it is not inherited from the mine phase)")

    if not fresh:
        return _critic_backbone_stop(project_dir, manifest, envelope, index, warnings, sig, cap=cap)

    return _critic_gate_stop(project_dir, manifest, verdict, index, warnings, cap=cap)


def run_enrich(project_dir, cli, *, artifacts_path=None, max_rejections_per_type=3, max_iterations=3,
               reset_budget=False) -> tuple[int, str]:
    # Enrich assembles the LLM prompt fragments into one envelope, proposes it to the CLI, then
    # validates readiness. Idempotent: the enrichment view is the completion predicate. state.bin
    # stays opaque — the driver reads only fragments + the machine-readable envelopes.
    project_dir = str(project_dir)
    artifacts_path = artifacts_path or str(Path(project_dir) / "artifacts")
    if _present(project_dir, ENRICH_VIEW_REL):
        return 0, "enrich already complete (enrichment view present)"

    manifest = Manifest.load(project_dir)
    if reset_budget:
        manifest.reset_enrich_budget()

    unsolved = _read_json(project_dir, VIEW_REL) or {}
    warnings: list[str] = []
    try:
        # load_fragments raises AssemblyError on a malformed fragment (not just assemble), so a
        # bad fragment JSON shares this one reject path instead of a raw JSONDecodeError escaping
        # the station as a traceback. warnings defaults to [] until fragments are loaded.
        fragments = load_fragments(str(Path(project_dir) / FRAGMENTS_DIR_REL))
        manifest.record_fragments(len(fragments))
        warnings = structural_coverage_warnings(fragments, unsolved) + value_conflict_warnings(fragments)
        envelope = assemble(fragments)
    except AssemblyError as e:
        return _enrich_stop(project_dir, manifest, "reject",
                            report={"reason": "assembly_rejected", "prompt_type": e.prompt_type, "detail": e.message},
                            warnings=warnings, msg=f"enrich rejected: {e.message}")

    gate_stop = _run_critic_station(project_dir, artifacts_path, manifest, envelope, unsolved, warnings,
                                    cap=max_rejections_per_type)
    if gate_stop is not None:
        return gate_stop

    env = cli.propose_enrichments(project_dir, json.dumps(envelope, sort_keys=True))
    if not env.success:
        return _enrich_handle_reject(project_dir, manifest, env, warnings,
                                     cap=max_rejections_per_type, cli=cli, envelope=envelope,
                                     max_iterations=max_iterations)

    report = cli.validate(project_dir).result or {}
    if report.get("ready") is True:
        return _commit_enrich_ready(
            project_dir, manifest, report, (env.result or {}).get("applied", []),
            warnings, f"enrich complete: ready ({len(fragments)} fragments)")

    return _stop_not_ready(
        project_dir, manifest, report, warnings, max_iterations,
        f"enrich not ready: {report.get('counts', {}).get('blocking', '?')} blocking; see enrichment-report.json")


def _run_with_quarantine(station, invoke, project_dir, artifacts_path, manifest):
    """Run a station; on a malformed-artifact abort (C5), quarantine the offending
    artifact, record PENDING, and retry over the remainder. Returns (Envelope, None)
    on success, or (None, (exit_code, message)) on an unrecoverable failure."""
    for _ in range(MAX_QUARANTINE_ATTEMPTS):
        env = invoke()
        if env.success:
            return env, None
        if classify(env.error.code) is RecoveryClass.DATA_QUARANTINE:
            offending = _offending_artifact(env.error, artifacts_path)
            if offending is None or not offending.exists():
                return None, _fail(env, station)  # cannot isolate -> escalate
            _quarantine(project_dir, offending)
            manifest.record_pending(offending.name, f"{env.error.code}: {env.error.message}")
            manifest.save(project_dir)
            continue
        return None, _fail(env, station)
    return None, (1, f"{station} exceeded quarantine attempts")


_ARTIFACT_RE = re.compile(r"'([^']*\.testbed\.json)'")


def _offending_artifact(error, artifacts_path):
    # Contract: TBD0009/TBD0011 quote the offending artifact path in single quotes.
    # Parse the first quoted *.testbed.json out of the message/suggestion; fall back to None.
    root = Path(artifacts_path).resolve()
    for text in (error.message, error.suggestion):
        m = _ARTIFACT_RE.search(text or "")
        if m:
            p = Path(m.group(1))
            # The path is parsed from CLI error text, so refuse to quarantine
            # anything that resolves outside the artifacts tree.
            candidate = (p if p.is_absolute() else root / p).resolve()
            return candidate if candidate.is_relative_to(root) else None
    return None


def _quarantine(project_dir, artifact_path: Path) -> None:
    # Prefix with the stem directory name to avoid collisions when two malformed
    # artifacts share the same basename (e.g. artifacts/a/testbed/data.testbed.json
    # vs artifacts/b/testbed/data.testbed.json).
    stem_dir = artifact_path.parent.parent.name
    dest = Path(project_dir) / QUARANTINE_REL / f"{stem_dir}__{artifact_path.name}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.replace(dest)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="run_pipeline")
    sub = parser.add_subparsers(dest="phase", required=True)
    mine = sub.add_parser("mine", help="run the workload-scoped mine phase")
    mine.add_argument("--project-dir", required=True)
    mine.add_argument("--artifacts-path", default=None)
    mine.add_argument("--scai", default=None, help="override the scai binary")
    val = sub.add_parser("validate", help="run the workload-scoped validate phase")
    val.add_argument("--project-dir", required=True)
    val.add_argument("--scai", default=None, help="override the scai binary")
    comp = sub.add_parser("compile", help="run the workload-scoped compile phase")
    comp.add_argument("--project-dir", required=True)
    comp.add_argument("--scai", default=None, help="override the scai binary")
    gen = sub.add_parser("generate", help="run the workload-scoped generate phase")
    gen.add_argument("--project-dir", required=True)
    gen.add_argument("--rows", type=int, default=None)
    gen.add_argument("--seed", type=int, default=None)
    gen.add_argument("--ignore-readiness", action="store_true",
                     help="proceed even when validate reports the workspace not ready")
    gen.add_argument("--scai", default=None, help="override the scai binary")
    enr = sub.add_parser("enrich", help="run the enrichment orchestration phase")
    enr.add_argument("--project-dir", required=True)
    enr.add_argument("--scai", default=None, help="override the scai binary")
    enr.add_argument("--artifacts-path", default=None,
                     help="per-object testbed JSON root the critic reads (default: <project>/artifacts)")
    enr.add_argument("--reset-budget", action="store_true", help="clear the retry/iterate budget (fresh human run)")
    enr.add_argument("--max-rejections-per-type", type=int, default=3,
                     help="re-prompt reject cap before stopping. v1 buckets every malformed-field reject "
                          "(TBD0014) under one key, so this is effectively a single budget until per-field "
                          "prompt-type derivation lands")
    enr.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args(argv)

    cli = TestbedCli(default_runner(args.scai))
    if args.phase == "compile":
        rc, msg = run_compile(args.project_dir, cli)
    elif args.phase == "validate":
        rc, msg = run_validate(args.project_dir, cli)
    elif args.phase == "generate":
        rc, msg = run_generate(args.project_dir, cli, args.rows, args.seed,
                               args.ignore_readiness)
    elif args.phase == "enrich":
        rc, msg = run_enrich(args.project_dir, cli, artifacts_path=args.artifacts_path,
                             max_rejections_per_type=args.max_rejections_per_type,
                             max_iterations=args.max_iterations, reset_budget=args.reset_budget)
    else:
        rc, msg = run_mine(args.project_dir, args.artifacts_path, cli)
    print(msg)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
