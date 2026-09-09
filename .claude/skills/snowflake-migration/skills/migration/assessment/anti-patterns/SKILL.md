---
name: anti-patterns
description: Flags migration anti-patterns (performance, architecture/security, behavior) by running `scai assessment anti-patterns`, which buckets SnowConvert's recorded issue codes and writes JSON for the assessment multi-report. Supports SQL Server and Redshift.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Anti-Patterns

Thin wrapper over `scai assessment anti-patterns`. SCAI reads the project's Code Unit Registry, matches the already-recorded issue codes against a curated per-dialect catalog, and writes one timestamped JSON the parent assessment multi-report consumes.

- **Supported dialects:** SQL Server, Redshift. Any other dialect aborts with `ASM0024` — report `skipped`, not an error.

## Run

```bash
scai assessment anti-patterns
```

Writes `<project_dir>/artifacts/assessment/anti-patterns-YYYYMMDD_HHMMSS.json`. Return that path to the parent; the multi-report auto-discovers it from `--project-dir`. Never parse or rewrite the file.

## Sub-agent contract

On entry, call `configure` with `project_dir` from the parent's context block. Take no user prompts. On completion return **JSON only**:

```json
{
  "sub_skill": "anti-patterns",
  "status": "ok",
  "output_json": "<abs path to anti-patterns-*.json>",
  "summary": "<one-line: buckets, distinct flags, code units affected>",
  "error": null
}
```

- Unsupported dialect (`ASM0024`): `status` `"skipped"`, `output_json` `null`, `error` `null`.
- Any other failure: `status` `"error"`, `output_json` `null`, `error` `"<message>"`.
