#!/usr/bin/env python3
"""CLI wrapper for the SAS -> Code Unit Registry emitter.

Two modes, mirroring the two skills:

  # Skill A — register source .sas files as CUR units
  python emit_cur.py source --sas <dir_or_file> --project-root <output_dir> \
      [--source-root <dir>] [--target-schema DB.SCHEMA]

  # Skill B — attach converted .sql + objectType from conversion_state.json
  python emit_cur.py converted --project-root <output_dir> \
      [--state <path/to/conversion_state.json>]

The project root is the SAS conversion <output_dir>. It gains a .scai/ marker and
sibling registry/, source/, snowflake/, artifacts/ dirs so `scai test` can seed
and validate the units. See ../sas_analyzer/cur_emitter.py and
../../references/cur-schema.md.
"""

import argparse
import json
import sys
from pathlib import Path

from sas_analyzer.cur_emitter import CurEmitter


def _find_sas_files(source: str):
    path = Path(source)
    if path.is_file() and path.suffix.lower() == ".sas":
        return [path]
    if path.is_dir():
        return sorted(path.rglob("*.sas"))
    print(f"Error: '{source}' is not a .sas file or directory.", file=sys.stderr)
    sys.exit(1)


def _cmd_source(args) -> int:
    sas_files = _find_sas_files(args.sas)
    if not sas_files:
        print("No .sas files found.", file=sys.stderr)
        return 1
    emitter = CurEmitter(Path(args.project_root))
    source_root = Path(args.source_root) if args.source_root else None
    entries = emitter.register_sources(sas_files, source_root=source_root, target_schema=args.target_schema)
    print(f"Registered {len(entries)} source unit(s) into {emitter.registry_dir}")
    for entry in entries:
        print(f"  {entry['source']['objectType']:<10} {entry['source']['name']}  ({entry['id']})")
    return 0


def _cmd_converted(args) -> int:
    root = Path(args.project_root)
    state_path = Path(args.state) if args.state else root / "conversion_state.json"
    if not state_path.exists():
        print(f"Error: conversion_state.json not found at {state_path}", file=sys.stderr)
        return 1
    conversion_state = json.loads(state_path.read_text(encoding="utf-8"))
    emitter = CurEmitter(root)
    updated = emitter.attach_converted_from_state(conversion_state)
    print(f"Attached converted SQL to {len(updated)} unit(s) in {emitter.registry_dir}")
    for entry in updated:
        converted = entry.get("files", {}).get("converted", {}).get("path", "?")
        print(f"  {entry['target']['objectType']:<10} {entry['source']['name']}  -> {converted}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="SAS -> Code Unit Registry emitter")
    sub = ap.add_subparsers(dest="mode", required=True)

    src = sub.add_parser("source", help="Register .sas files as source-side CUR units")
    src.add_argument("--sas", required=True, help="Path to .sas file or directory")
    src.add_argument("--project-root", required=True, help="SAS conversion output_dir (CUR project root)")
    src.add_argument("--source-root", help="Base dir for computing relative source paths (default: --sas dir)")
    src.add_argument("--target-schema", help="Target DB.SCHEMA for the converted objects")
    src.set_defaults(func=_cmd_source)

    conv = sub.add_parser("converted", help="Attach converted .sql from conversion_state.json")
    conv.add_argument("--project-root", required=True, help="SAS conversion output_dir (CUR project root)")
    conv.add_argument("--state", help="Path to conversion_state.json (default: <project-root>/conversion_state.json)")
    conv.set_defaults(func=_cmd_converted)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
