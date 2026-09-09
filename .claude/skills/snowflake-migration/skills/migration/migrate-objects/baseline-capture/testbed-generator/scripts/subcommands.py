"""Typed wrappers over the `scai testbed` mine-phase subcommands.

The CLI is the single source of truth for testbed state; this module reads only
the machine-readable `--json` envelope and never touches the opaque state.bin.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, NamedTuple

TESTBED_SUFFIX = ".testbed.json"


def _env_timeout(default: int = 3600) -> int:
    # Generous by design: catches a hung scai without tripping on a slow but
    # progressing whole-workload scan. A non-numeric SCAI_TESTBED_TIMEOUT must
    # degrade to the default, not raise ValueError at import before any driver runs.
    try:
        return int(os.environ.get("SCAI_TESTBED_TIMEOUT", default))
    except ValueError:
        return default


DEFAULT_TIMEOUT_SECONDS = _env_timeout()

# argv is everything after the `scai` program name; cwd is required by `init`;
# stdin feeds Console.In — propose-enrichments reads the whole envelope from it.
CliRunner = Callable[[list[str], str | None, str | None], subprocess.CompletedProcess]


@dataclass(frozen=True)
class TestbedError:
    code: str
    message: str = ""
    suggestion: str = ""


@dataclass(frozen=True)
class Envelope:
    success: bool
    result: dict | None
    error: TestbedError | None


def default_runner(scai_bin: str | None = None,
                   timeout: float | None = DEFAULT_TIMEOUT_SECONDS) -> CliRunner:
    program = scai_bin or os.environ.get("SCAI", "scai")

    def _run(argv: list[str], cwd: str | None = None,
             stdin: str | None = None) -> subprocess.CompletedProcess:
        # The failures that strike before scai can emit a parseable envelope — an
        # unlaunchable binary, a hang past the bound, and I/O that is not valid UTF-8 —
        # become a non-zero CompletedProcess so _envelope reports EXEC instead of
        # raising or blocking the whole skill forever.
        try:
            # encoding= is not optional here. text=True alone decodes stdout/stderr with
            # locale.getencoding(), and this call is the main ingress for mined identities: scai
            # writes its --json envelope as UTF-8 (Program.cs pins Console.OutputEncoding) and that
            # envelope (list-unsolved, propose-enrichments) carries object/column names verbatim.
            # On a cp1252 host — only five undefined byte values — those bytes decode to mojibake
            # without raising, so a golden literal false-REJECTs as absent from its own
            # source_evidence span. Pin the codec instead of inheriting the shell's. The same
            # keyword pins the stdin encode too, which is contract rather than repair: today's only
            # caller hands propose-enrichments json.dumps output, already escaped to pure ASCII by
            # ensure_ascii, so no locale codec can fail on it.
            return subprocess.run(
                [program, *argv], input=stdin, capture_output=True, text=True,
                encoding="utf-8", cwd=cwd, timeout=timeout)
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(
                [program, *argv], 124, "", f"scai timed out after {timeout}s: {' '.join(argv)}")
        except UnicodeError as exc:
            # Pinning the codec converts a silent mis-decode into a raise; keep that raise inside
            # the seam. UnicodeDecodeError/UnicodeEncodeError subclass ValueError, not OSError, so
            # without this arm they escape as a traceback out of the driver. Loud EXEC beats both
            # mojibake (indistinguishable from an object genuinely named that) and a crash.
            return subprocess.CompletedProcess(
                [program, *argv], 125, "", f"scai I/O was not valid UTF-8: {exc}")
        except OSError as exc:
            return subprocess.CompletedProcess(
                [program, *argv], 127, "", f"could not execute scai ({program}): {exc}")

    return _run


def parse_envelope(stdout: str) -> Envelope:
    doc = json.loads(stdout)
    err = doc.get("error")
    return Envelope(
        success=bool(doc.get("success")),
        result=doc.get("result"),
        error=TestbedError(err["code"], err.get("message", ""), err.get("suggestion", ""))
        if err else None,
    )


class TestbedCli:
    def __init__(self, runner: CliRunner):
        self._run = runner

    def init(self, project_dir: str) -> Envelope:
        # init infers artifacts/workspace from the project, so cwd must be the project.
        return self._envelope(self._run(["testbed", "init", "--json"], project_dir))

    def compile(self, project_dir: str) -> Envelope:
        # compile is RequiresProject=true and infers its paths from the project,
        # so cwd must be the project (like init). It takes no artifacts path.
        return self._envelope(self._run(["testbed", "compile", "--json"], project_dir))

    def propose_enrichments(self, project_dir: str, envelope_json: str) -> Envelope:
        # RequiresProject=true: cwd is the project (like init/compile). The command reads the whole
        # envelope from stdin (Console.In.ReadToEnd); reject codes come back in the stdout envelope.
        return self._envelope(
            self._run(["testbed", "propose-enrichments", "--json"], project_dir, envelope_json))

    def validate(self, project_dir: str) -> Envelope:
        # validate is RequiresProject=true and reads the mined state to report
        # readiness (fk gaps / type conflicts / unsatisfied constraints), so cwd
        # must be the project (like compile). It takes no artifacts path.
        return self._envelope(self._run(["testbed", "validate", "--json"], project_dir))

    def generate(self, project_dir: str,
                 rows: int | None = None, seed: int | None = None) -> Envelope:
        # generate is RequiresProject=true; output is derived per-object (each table's CSV
        # into its own artifacts folder, manifest beside state.bin), so there is no --out.
        # rows/seed are optional generator knobs.
        argv = ["testbed", "generate"]
        if rows is not None:
            argv += ["--rows", str(rows)]
        if seed is not None:
            argv += ["--seed", str(seed)]
        argv.append("--json")
        return self._envelope(self._run(argv, project_dir))

    def inspect_branches(self, project_dir: str, stem: str | None = None) -> Envelope:
        # RequiresProject=true and resolves Workspace from the project (like compile/validate),
        # so cwd is the project; the command declares no artifacts-path option. Omitting the
        # identity projects every branch-carrying object from a single state.bin load — what
        # spares the drill-down one process (and one deserialization) per procedure.
        argv = ["testbed", "inspect-branches"]
        if stem is not None:
            argv.append(stem)
        argv.append("--json")
        return self._envelope(self._run(argv, project_dir))

    def list_unsolved(self, project_dir: str) -> Envelope:
        # Whole-workload scan; RequiresProject=true, resolves Workspace from the project (cwd)
        # like compile/validate. Per-object list-unsolved (a `stem` arg) has no caller yet;
        # it's a one-line add back the day per-object scanning is needed.
        argv = ["testbed", "list-unsolved", "--json"]
        return self._envelope(self._run(argv, project_dir))

    @staticmethod
    def _envelope(cp: subprocess.CompletedProcess) -> Envelope:
        # In --json mode the testbed commands write the envelope (success OR error) to stdout.
        try:
            return parse_envelope(cp.stdout)
        except (json.JSONDecodeError, KeyError, TypeError):
            detail = (cp.stderr or cp.stdout or "").strip()[:500]
            return Envelope(False, None, TestbedError("EXEC", detail or "no parseable envelope"))


class ArtifactRef(NamedTuple):
    """One mined artifact. `stem` is the bare filename — the view/quarantine key; `object_name` is
    the identity inspect-branches reports each projected object under (FQN or code_unit_id);
    `object_type` is the engine's authoritative `"TABLE"`/`"PROCEDURE"` stamp (`""` when the artifact
    omits it), which the drill-down dispatches on: a known non-procedure folds in with no branches,
    while a procedure — or an untyped artifact, which init may still resolve to a procedure via the
    CUR registry — is expected in the whole-workload projection."""
    stem: str
    object_name: str
    object_type: str


def enumerate_artifacts(artifacts_path: str) -> list[ArtifactRef]:
    """One ArtifactRef per artifacts/**/testbed/*.testbed.json, sorted by stem.

    The whole-workload inspect-branches projection reports each object under the exact FQN or
    code_unit_id it was mined as (never the bare filename), so each stem is paired with that
    identity for the join back: procedures — and current-layout tables — carry it as `object`,
    legacy-layout tables as `table`. An unreadable or identity-less artifact falls back to its stem
    with no type; since a missing type may still be a registry-typed procedure, the drill-down
    expects it in the projection (recording PENDING if it never appears) rather than silently
    folding it in as an empty-branch entry."""
    return sorted(
        (_artifact_ref(p, p.name[: -len(TESTBED_SUFFIX)])
         for p in Path(artifacts_path).glob(f"**/testbed/*{TESTBED_SUFFIX}")),
        key=lambda ref: ref.stem,
    )


def _artifact_ref(path: Path, stem: str) -> ArtifactRef:
    try:
        # The engine writes these artifacts as UTF-8. Decoding with the platform locale instead
        # (cp1252 on a Windows runner) raises UnicodeDecodeError, which is a ValueError and so is
        # caught below as if the file were unreadable — silently collapsing a non-ASCII identity
        # to the bare stem. The stem then never matches an `object` the CLI echoes, so a real
        # procedure becomes an unresolvable PENDING. Pin the encoding to the one it was written in.
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ArtifactRef(stem, stem, "")
    if not isinstance(doc, dict):
        return ArtifactRef(stem, stem, "")
    identity = doc.get("object") or doc.get("table")
    object_name = identity if isinstance(identity, str) and identity else stem
    object_type = doc.get("object_type")
    return ArtifactRef(stem, object_name, object_type if isinstance(object_type, str) else "")
