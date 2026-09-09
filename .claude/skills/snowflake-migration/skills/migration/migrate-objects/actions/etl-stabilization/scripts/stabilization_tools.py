#!/usr/bin/env python3
# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""stabilization_tools — the deterministic block tools for ETL stabilization, as one subcommand CLI.

The mechanical operations the stabilization loop calls (locate a block by marker,
splice a validated replacement, extract EWI/RESOLVE spans, resolve an EWI fix guide,
map a task/CALL error back to a block) are deterministic and share the same CLI shape
(read a marked ``.sql``, emit JSON or plain text, return a structured exit code). They
live here as subcommands of a single CLI — mirroring ``track_status.py`` — rather than
as separate scripts, so the scaffolding is written and tested once.

Usage:
    python stabilization_tools.py <command> [args...]
    python stabilization_tools.py <command> --help

Commands:
    block-locate        locate a materialized block by its marker (span + byte range + body)
    ewi-extract         list EWI/FDM markers with code/description/offset, grouped by block
    ewi-guide-resolve   resolve an EWI/FDM code to its fix-guide markdown path
    block-replace       splice a validated replacement into a block, marker-integrity checked
    task-error-locate   map a task/CALL error back to the failing statement + block
    stub-detect         find unrepaired all-NULL placeholder projections (marker-independent)

Exit codes are per-command; the shared conventions are:
    0  ok
    1  file/target not found, or other handled error
    2  usage error (argparse)
    3  a write would violate marker integrity (nothing written)
    4  the request is ambiguous (e.g. a block name occurs in more than one statement)
    5  nothing matched (task-error-locate found no statement/block)
    6  an unrepaired placeholder stub is still present (stub-detect)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from scan_unit import (
    RE_CREATE,
    RE_END_TAG,
    RE_START_TAG,
    extract_ewis,
    locate_blocks,
    parse_orchestration,
)

# ── shared CLI helpers ──────────────────────────────────────────────────────

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INTEGRITY = 3
EXIT_AMBIGUOUS = 4
EXIT_NO_MATCH = 5
EXIT_STUB_PRESENT = 6


def emit_json(obj) -> None:
    """Print ``obj`` as indented, UTF-8-faithful JSON (the shared --json shape)."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def err(msg: str, code: int = EXIT_ERROR) -> int:
    """Print ``Error: <msg>`` to stderr and return the exit code (callers ``return err(...)``)."""
    print(f"Error: {msg}", file=sys.stderr)
    return code


def require_sql_file(arg: str) -> Path | None:
    """Return ``arg`` as a Path if it is an existing file, else None (caller emits the error)."""
    p = Path(arg)
    return p if p.is_file() else None


# ── block-locate ────────────────────────────────────────────────────────────

_LOCATE_INDEX_FIELDS = (
    "statement", "statement_type", "name",
    "start_line", "end_line", "line_count", "byte_start", "byte_end",
)


def _locate_select(blocks: list[dict], name: str, statement: str | None) -> list[dict]:
    matches = [b for b in blocks if b["name"] == name]
    if statement is not None:
        matches = [b for b in matches if b["statement"] == statement]
    return matches


def cmd_block_locate(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py block-locate",
        description="Locate a block within a converted ETL procedure by its marker.",
    )
    parser.add_argument("sql_file", help="path to the converted procedure .sql")
    parser.add_argument("--block", help="block FullName to locate (from ---- Start block '<FullName>')")
    parser.add_argument("--statement", help="disambiguate when the block name occurs in more than one statement")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--body-only", action="store_true", help="print only the block body (for piping)")
    parser.add_argument("--list", action="store_true", help="list every block (name + span) and exit")
    args = parser.parse_args(argv)

    sql_path = require_sql_file(args.sql_file)
    if sql_path is None:
        return err(f"'{args.sql_file}' is not a file")

    blocks = locate_blocks(sql_path)

    if args.list or not args.block:
        index = [{k: b[k] for k in _LOCATE_INDEX_FIELDS} for b in blocks]
        if args.json:
            emit_json(index)
        elif not index:
            print("(no blocks found)")
        else:
            for b in index:
                print(f"{b['start_line']:>6}-{b['end_line']:<6} [{b['statement']}] {b['name']}")
        return EXIT_OK

    matches = _locate_select(blocks, args.block, args.statement)
    if not matches:
        where = f" in statement '{args.statement}'" if args.statement else ""
        return err(f"block '{args.block}' not found{where}")
    if len(matches) > 1:
        stmts = ", ".join(sorted({m["statement"] for m in matches}))
        return err(
            f"block '{args.block}' is ambiguous across statements: {stmts}; pass --statement "
            f"(a name duplicated within a single statement cannot be disambiguated)",
            code=EXIT_AMBIGUOUS,
        )

    block = matches[0]
    if args.body_only:
        sys.stdout.write(block["body"])
        return EXIT_OK
    if args.json:
        emit_json(block)
    else:
        print(f"block     : {block['name']}")
        print(f"statement : {block['statement']} ({block['statement_type']})")
        print(f"lines     : {block['start_line']}-{block['end_line']}  ({block['line_count']} lines)")
        print(f"bytes     : {block['byte_start']}-{block['byte_end']}")
        print("---- body ----")
        sys.stdout.write(block["body"])
        if not block["body"].endswith("\n"):
            sys.stdout.write("\n")
    return EXIT_OK


# ── ewi-extract ─────────────────────────────────────────────────────────────

_EWI_OUTSIDE = "(outside blocks)"


def cmd_ewi_extract(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py ewi-extract",
        description="List EWI/FDM markers with location and containing block.",
    )
    parser.add_argument("sql_file", help="path to the converted procedure .sql")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--grouped", action="store_true", help="group markers by block")
    parser.add_argument("--code", help="filter to a single EWI/FDM code")
    parser.add_argument("--kind", choices=["EWI", "FDM"], help="filter to EWI or FDM only")
    args = parser.parse_args(argv)

    sql_path = require_sql_file(args.sql_file)
    if sql_path is None:
        return err(f"'{args.sql_file}' is not a file")

    markers = extract_ewis(sql_path)
    if args.code:
        markers = [m for m in markers if m["code"] == args.code]
    if args.kind:
        markers = [m for m in markers if m["kind"] == args.kind]

    if args.json:
        if args.grouped:
            grouped: dict[str, list[dict]] = {}
            for m in markers:
                grouped.setdefault(m["block"] or _EWI_OUTSIDE, []).append(m)
            emit_json(grouped)
        else:
            emit_json(markers)
        return EXIT_OK

    if not markers:
        print("(no EWI/FDM markers)")
        return EXIT_OK

    if args.grouped:
        order: list[str] = []
        by_block: dict[str, list[dict]] = {}
        for m in markers:
            key = m["block"] or _EWI_OUTSIDE
            if key not in by_block:
                by_block[key] = []
                order.append(key)
            by_block[key].append(m)
        for key in order:
            print(f"[{key}]")
            for m in by_block[key]:
                print(f"  {m['line']:>5}  {m['kind']}  {m['code']} - {m['description']}")
    else:
        for m in markers:
            print(f"{m['line']:>5}  {m['kind']}  {m['code']}  [{m['block'] or '-'}]  {m['description']}")
    return EXIT_OK


# ── ewi-guide-resolve ─────────────────────────────────────────────────────────

_SKILL_DIR = Path(__file__).resolve().parent.parent


def resolve_ewi_guide(
    code: str, platform: str | None = None, skill_dir: str | Path | None = None
) -> tuple[Path | None, list[Path]]:
    """Return ``(path, candidates)``: ``path`` is the first existing guide for ``code``
    (platform-specific first, then the shared reference guide), or None if none exists.
    ``candidates`` is the list of paths tried, in order.
    """
    # Guard against path traversal: code comes from marker text and both code and
    # platform are interpolated straight into the guide path.
    for label, value in (("code", code), ("platform", platform)):
        if value and ("/" in value or "\\" in value or "\x00" in value or value in (".", "..")):
            raise ValueError(f"invalid {label} '{value}': must not contain path separators")

    root = Path(skill_dir) if skill_dir else _SKILL_DIR
    candidates: list[Path] = []
    if platform:
        candidates.append(root / "platforms" / platform / "ewi" / f"{code}.md")
    candidates.append(root / "reference" / "ewi" / f"{code}.md")
    for candidate in candidates:
        if candidate.is_file():
            return candidate, candidates
    return None, candidates


def cmd_ewi_guide_resolve(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py ewi-guide-resolve",
        description="Resolve an EWI/FDM code to its fix-guide markdown.",
    )
    parser.add_argument("code", help="the EWI/FDM code, e.g. SSC-EWI-SSIS0003")
    parser.add_argument("--platform", help="platform id (ssis, informatica, ...) — checked before the shared guides")
    parser.add_argument("--skill-dir", help="override the stabilization skill root (default: this script's skill root)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    try:
        path, candidates = resolve_ewi_guide(args.code, args.platform, args.skill_dir)
    except ValueError as e:
        return err(str(e))

    if args.json:
        emit_json({
            "code": args.code,
            "platform": args.platform,
            "found": path is not None,
            "path": str(path) if path else None,
            "candidates": [str(c) for c in candidates],
        })
        return EXIT_OK if path else EXIT_ERROR

    if path:
        print(path)
        return EXIT_OK
    where = f" (platform={args.platform})" if args.platform else ""
    tried = ", ".join(str(c) for c in candidates)
    return err(f"No guide for '{args.code}'{where}; tried: {tried}")


# ── block-replace ─────────────────────────────────────────────────────────────


class BlockReplaceError(Exception):
    """Base error for block-replace."""


class BlockNotFound(BlockReplaceError):
    pass


class AmbiguousBlock(BlockReplaceError):
    pass


class IntegrityError(BlockReplaceError):
    pass


def _structure_signature(text: str) -> tuple[list[str], list[str], int]:
    """Structural fingerprint the splice must preserve: Start-marker names and
    End-marker names (both in file order) plus the CREATE OR REPLACE count.
    Computed identically for the original and the result, so the comparison is
    apples-to-apples (no readlines-vs-splitlines skew)."""
    starts: list[str] = []
    ends: list[str] = []
    creates = 0
    for raw in text.splitlines():
        ln = raw.strip()
        sm = RE_START_TAG.match(ln)
        if sm:
            starts.append(sm.group(1))
        em = RE_END_TAG.match(ln)
        if em:
            ends.append(em.group(1))
        if RE_CREATE.match(ln):
            creates += 1
    return starts, ends, creates


def block_replace(
    sql_path: Path, name: str, replacement: str, statement: str | None = None
) -> str:
    """Return the file contents with block ``name`` replaced by ``replacement``.

    The block is located by its ``---- Start``/``---- End`` marker pair; the span
    runs from the Start marker line through the matching End marker line. The
    replacement is normalized to whole lines terminated with the file's own line
    ending, so it can never fuse with the line that follows the block.

    Raises:
      BlockNotFound / AmbiguousBlock -- the block can't be uniquely located.
      BlockReplaceError -- the block has no matching ``---- End`` marker
        (block-replace requires End-delimited blocks; it will not guess a span).
      IntegrityError -- the result would change the file's Start-marker names/order,
        End-marker names/order, or CREATE OR REPLACE count. Nothing is written.
    """
    with open(sql_path, encoding="utf-8", newline="") as f:
        lines = f.readlines()
    content = "".join(lines)

    matches = [
        b
        for b in locate_blocks(sql_path)
        if b["name"] == name and (statement is None or b["statement"] == statement)
    ]
    if not matches:
        where = f" in statement '{statement}'" if statement else ""
        raise BlockNotFound(f"block '{name}' not found{where}")
    if len(matches) > 1:
        stmts = ", ".join(sorted({m["statement"] for m in matches}))
        raise AmbiguousBlock(
            f"block '{name}' is ambiguous across statements: {stmts}; pass --statement "
            f"(a name duplicated within a single statement cannot be disambiguated)"
        )
    target = matches[0]

    start_idx = target["start_line"] - 1  # 0-based index of the Start marker line
    # Require the matching End marker: block-replace only operates on End-delimited
    # blocks, so it never silently absorbs trailing statement lines (END; / $$;).
    span_end = None
    for i in range(start_idx + 1, target["end_line"]):
        end_match = RE_END_TAG.match(lines[i].strip())
        if end_match and end_match.group(1) == name:
            span_end = i + 1  # include the End marker line
            break
    if span_end is None:
        raise BlockReplaceError(
            f"block '{name}' has no matching '---- End' marker; block-replace requires "
            f"End-delimited blocks and will not guess a span"
        )

    # Normalize the replacement to whole lines terminated with the file's own line
    # ending (taken from the End-marker line): guarantees a trailing terminator so
    # the block's last line can't fuse with the following line, and keeps endings
    # consistent (LF / CRLF).
    end_line = lines[span_end - 1]
    line_ending = "\r\n" if end_line.endswith("\r\n") else ("\r" if end_line.endswith("\r") else "\n")
    normalized = "".join(seg + line_ending for seg in replacement.splitlines())

    new_content = "".join(lines[:start_idx]) + normalized + "".join(lines[span_end:])

    orig_sig = _structure_signature(content)
    new_sig = _structure_signature(new_content)
    if new_sig != orig_sig:
        raise IntegrityError(
            "structure integrity violated (nothing written): "
            f"start markers {orig_sig[0]} -> {new_sig[0]}; "
            f"end markers {orig_sig[1]} -> {new_sig[1]}; "
            f"CREATE count {orig_sig[2]} -> {new_sig[2]}"
        )

    return new_content


def cmd_block_replace(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py block-replace",
        description="Deterministically splice a fixed block back into a procedure, with marker integrity check.",
    )
    parser.add_argument("sql_file", help="path to the converted procedure .sql")
    parser.add_argument("--block", required=True, help="the block FullName to replace")
    parser.add_argument("--statement", help="disambiguate when the block name occurs in more than one statement")
    parser.add_argument("--replacement-file", help="file with the replacement block text (default: read stdin)")
    parser.add_argument("--in-place", action="store_true", help="overwrite <sql_file> (default: write new content to stdout)")
    args = parser.parse_args(argv)

    sql_path = require_sql_file(args.sql_file)
    if sql_path is None:
        return err(f"'{args.sql_file}' is not a file")

    if args.replacement_file:
        try:
            replacement = Path(args.replacement_file).read_text(encoding="utf-8")
        except OSError as e:
            return err(f"cannot read --replacement-file '{args.replacement_file}': {e}")
    else:
        replacement = sys.stdin.read()

    try:
        new_content = block_replace(sql_path, args.block, replacement, args.statement)
    except BlockNotFound as e:
        return err(str(e))
    except AmbiguousBlock as e:
        return err(str(e), code=EXIT_AMBIGUOUS)
    except IntegrityError as e:
        return err(f"{e} (nothing written)", code=EXIT_INTEGRITY)
    except BlockReplaceError as e:
        return err(str(e))

    if args.in_place:
        sql_path.write_text(new_content, encoding="utf-8", newline="")
        print(f"Replaced block '{args.block}' in {sql_path}", file=sys.stderr)
    else:
        sys.stdout.write(new_content)
    return EXIT_OK


# ── task-error-locate ─────────────────────────────────────────────────────────

_RE_LINE = re.compile(r"\bline\s+(\d+)", re.IGNORECASE)

# Keywords that precede an object name in a task-run / CALL error. The free-text name
# scan is anchored to one of these so a short, generic statement name (load / run /
# update / main / data) can't spuriously match unrelated prose ("failed to load file ...").
_NAME_CONTEXT_KEYWORDS = "task|procedure|proc|function|call"


def _name_in_error(normalized_name: str, error_text: str) -> bool:
    """True when the normalized statement name ``normalized_name`` appears in ``error_text`` anchored to
    a task/CALL keyword (optionally through a ``db.schema`` qualifier and/or quotes) - e.g.
    ``Task PUBLIC.T_FACT`` / ``procedure LOAD`` / ``CALL public.load_fact()`` - rather than as
    a bare substring of unrelated prose."""
    pattern = (
        rf"(?i)\b(?:{_NAME_CONTEXT_KEYWORDS})\b[\s\"']*"
        rf"(?:[\w$]+[\s\"']*\.[\s\"']*)*"
        rf"\"?{re.escape(normalized_name)}\"?\b"
    )
    return re.search(pattern, error_text) is not None


def _norm(name: str) -> str:
    """Normalize a task/proc name for matching: strip quotes, drop an argument
    list, lowercase, keep the last dotted component (``db.schema.NAME`` -> ``name``)."""
    base = re.sub(r"\s*\(.*\)\s*$", "", name.strip())  # drop "(...)" arg list
    base = base.split(".")[-1]                              # last dotted component
    return base.strip().strip('"').lower()


def _statements(sql_path: Path) -> list[dict]:
    """Statements with computed 1-based inclusive line spans (start..end): each
    runs from its CREATE line to the line before the next statement (last to EOF)."""
    stmts = parse_orchestration(sql_path)
    with open(sql_path, encoding="utf-8", newline="") as f:
        total = len(f.readlines())
    out = []
    for i, s in enumerate(stmts):
        end = stmts[i + 1]["line"] - 1 if i + 1 < len(stmts) else total
        out.append({"name": s["name"], "type": s["type"], "start_line": s["line"], "end_line": end})
    return out


def _hit(stmt: dict, block: dict | None) -> dict:
    return {
        "statement": stmt["name"],
        "statement_type": stmt["type"],
        "block": block["name"] if block else None,
        "start_line": block["start_line"] if block else stmt["start_line"],
        "end_line": block["end_line"] if block else stmt["end_line"],
    }


def locate_error(
    sql_path: Path,
    task: str | None = None,
    line: int | None = None,
    error_text: str | None = None,
) -> list[dict]:
    """Return the failing statement(s)+block(s) implied by the given signals, in
    resolution order (line-derived hits first, then name-derived), de-duplicated.

    A ``--task`` name matches on its last dotted component, so it resolves EVERY statement
    with that name across schemas (e.g. both ``public.load_dim`` and ``staging.load_dim`` for
    ``load_dim``) - all candidates are surfaced, not one guessed. The free-text scan of
    ``error_text`` for known statement names is anchored to a task/CALL keyword (see
    ``_name_in_error``) so short generic names don't match unrelated prose."""
    stmts = _statements(sql_path)
    blocks = locate_blocks(sql_path)

    def stmt_by_name(name):
        return next((s for s in stmts if s["name"] == name), None)

    def stmt_of_line(line_no):
        return next((s for s in stmts if s["start_line"] <= line_no <= s["end_line"]), None)

    def block_of_line(line_no):
        return next((b for b in blocks if b["start_line"] <= line_no <= b["end_line"]), None)

    hits: list[dict] = []
    seen: set = set()

    def add(stmt, block):
        if stmt is None:
            return
        key = (stmt["name"], block["name"] if block else None)
        if key not in seen:
            seen.add(key)
            hits.append(_hit(stmt, block))

    # 1. line numbers (explicit + parsed from the error text)
    line_nums = [line] if line is not None else []
    if error_text:
        line_nums += [int(m.group(1)) for m in _RE_LINE.finditer(error_text)]
    for line_no in line_nums:
        b = block_of_line(line_no)
        add(stmt_by_name(b["statement"]) if b else stmt_of_line(line_no), b)

    # 2. task/proc names (explicit + any known statement name found in the error text)
    wants = [_norm(task)] if task else []
    if error_text:
        # Anchored to a task/CALL keyword to avoid short-name false positives (see _name_in_error).
        for s in stmts:
            normalized_name = _norm(s["name"])
            if normalized_name and _name_in_error(normalized_name, error_text):
                wants.append(normalized_name)
    for want in wants:
        if not want:
            continue
        for s in stmts:
            if _norm(s["name"]) == want:
                s_blocks = [b for b in blocks if b["statement"] == s["name"]]
                if s_blocks:
                    for b in s_blocks:
                        add(s, b)
                else:
                    add(s, None)

    return hits


def cmd_task_error_locate(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py task-error-locate",
        description="Map a task/CALL error to the failing statement + block.",
    )
    parser.add_argument("sql_file", help="path to the converted procedure/orchestration .sql")
    parser.add_argument("--task", help="failing task/proc name (e.g. TASK_HISTORY.NAME or the CALL target)")
    parser.add_argument("--line", type=int, help="a 1-based line number carried by the error")
    parser.add_argument("--error-file", help="file with the raw error text (default: read stdin if no --task/--line)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    sql_path = require_sql_file(args.sql_file)
    if sql_path is None:
        return err(f"'{args.sql_file}' is not a file")

    error_text = None
    if args.error_file:
        try:
            error_text = Path(args.error_file).read_text(encoding="utf-8")
        except OSError as e:
            return err(f"cannot read --error-file '{args.error_file}': {e}")
    elif args.task is None and args.line is None:
        error_text = sys.stdin.read()

    hits = locate_error(sql_path, task=args.task, line=args.line, error_text=error_text)

    if args.json:
        emit_json(hits)
    elif not hits:
        print("(no matching statement/block)")
    else:
        for h in hits:
            print(f"{h['start_line']:>5}-{h['end_line']:<5} [{h['statement']}] {h['block'] or '-'}")
    return EXIT_OK if hits else EXIT_NO_MATCH


# ── stub-detect ─────────────────────────────────────────────────────────────
# An unconverted transformation is emitted as a placeholder whose projection is
# entirely NULL literals (`null AS col`), wrapped in a RESOLVE-EWI marker. The
# placeholder is a COMPLETE projection feeding a real INSERT, so deleting the
# marker alone leaves SQL that compiles and silently writes NULL rows — a fix
# that passes a compile check while destroying the data contract.
#
# This detector is deliberately marker-INDEPENDENT: it reads the projection, not
# the marker, so a "repair" that only strips `!!!RESOLVE EWI!!!` is still
# reported. A real reconstruction projects real expressions and clears.

_RE_NULL_PROJECTION = re.compile(r"^null\s+AS\s+[\w$\"]+\s*,?$", re.IGNORECASE)
_RE_PROJECTION_ALIAS = re.compile(r"\bAS\s+([\w$\"]+)\s*,?$", re.IGNORECASE)
_STUB_STOP_PREFIXES = ("FROM", ")", ";", "WITH", "SELECT", "INSERT", "----", "!!!", "--")


def detect_null_stubs(sql_path: Path) -> list[dict]:
    """Return every all-NULL placeholder projection in ``sql_path``.

    A hit is a bare ``SELECT`` whose entire projection list is ``null AS <col>``
    items. Each hit carries its containing block (when the file is marked) and
    the enclosing CTE name, so the caller can point the fixer at the exact node.
    """
    with open(sql_path, encoding="utf-8", newline="") as f:
        lines = f.readlines()

    try:
        blocks = locate_blocks(sql_path)
    except Exception:  # noqa: BLE001 - an unmarked file is still scannable
        blocks = []

    def block_of(line_no: int) -> str | None:
        for b in blocks:
            if b["start_line"] <= line_no <= b["end_line"]:
                return b["name"]
        return None

    def cte_of(idx: int) -> str | None:
        # nearest preceding `<name> AS (` opener, walking back over the captured
        # source-XML comment lines the placeholder carries; stop if we leave the CTE.
        for k in range(idx - 1, -1, -1):
            s = lines[k].strip()
            if s in (")", ");", ";") or s.upper().startswith("INSERT"):
                return None
            m = re.match(r"^([\w$]+)\s+AS\s*\(?\s*$", s, re.IGNORECASE)
            if m and m.group(1).upper() != "AS":
                return m.group(1)
        return None

    hits: list[dict] = []
    for i, raw in enumerate(lines):
        if raw.strip().upper() != "SELECT":
            continue
        items: list[str] = []
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            if not s or s.upper().startswith(_STUB_STOP_PREFIXES):
                break
            items.append(s)
            j += 1
        if not items or not all(_RE_NULL_PROJECTION.match(it) for it in items):
            continue
        columns = [m.group(1) for m in (_RE_PROJECTION_ALIAS.search(it) for it in items) if m]
        hits.append({
            "block": block_of(i + 1),
            "cte": cte_of(i),
            "start_line": i + 1,
            "end_line": j,
            "column_count": len(items),
            "columns": columns,
        })
    return hits


def cmd_stub_detect(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        prog="stabilization_tools.py stub-detect",
        description="Find unrepaired all-NULL placeholder projections (independent of EWI markers).",
    )
    parser.add_argument("sql_file", help="path to the converted procedure .sql")
    parser.add_argument("--block", help="only report stubs inside this block")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    sql_path = require_sql_file(args.sql_file)
    if sql_path is None:
        return err(f"'{args.sql_file}' is not a file")

    hits = detect_null_stubs(sql_path)
    if args.block:
        hits = [h for h in hits if h["block"] == args.block]

    if args.json:
        emit_json(hits)
    elif not hits:
        print("(no all-NULL placeholder projections)")
    else:
        for h in hits:
            where = h["cte"] or h["block"] or "-"
            print(f"{h['start_line']:>5}-{h['end_line']:<5} {where}  {h['column_count']} NULL column(s): {', '.join(h['columns'])}")
    return EXIT_STUB_PRESENT if hits else EXIT_OK


# ── dispatcher ──────────────────────────────────────────────────────────────

_COMMANDS = {
    "block-locate": cmd_block_locate,
    "ewi-extract": cmd_ewi_extract,
    "ewi-guide-resolve": cmd_ewi_guide_resolve,
    "block-replace": cmd_block_replace,
    "task-error-locate": cmd_task_error_locate,
    "stub-detect": cmd_stub_detect,
}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__, file=sys.stderr)
        return EXIT_ERROR
    command, rest = argv[0], argv[1:]
    if command in ("-h", "--help"):
        print(__doc__)
        return EXIT_OK
    handler = _COMMANDS.get(command)
    if handler is None:
        print(f"Error: unknown command '{command}'. Run 'stabilization_tools.py --help' for the command list.", file=sys.stderr)
        return EXIT_ERROR
    return handler(rest)


if __name__ == "__main__":
    sys.exit(main())
