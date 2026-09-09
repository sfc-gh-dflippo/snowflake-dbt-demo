---
name: effort-estimate
description: Generates migration effort estimates by running `scai assessment effort-estimate`, which writes JSON for the assessment multi-report. Supports SQL Server and Redshift.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Effort Estimates

Thin wrapper over `scai assessment effort-estimate`. SCAI reads SnowConvert reports, bands every object by complexity, prices each band against the dialect's rate card, and writes one timestamped JSON the parent assessment multi-report consumes.

- **Supported dialects:** SQL Server, Redshift. Any other dialect aborts with `ASM0031` — report `skipped`, not an error.

## Run

```bash
scai assessment effort-estimate
```

Writes `<project_dir>/artifacts/assessment/effort-estimates-YYYYMMDD_HHMMSS.json`. Return that path to the parent; the multi-report auto-discovers it from `--project-dir`. Never parse or rewrite the file.

## Sub-agent contract

On entry, call `configure` with `project_dir` from the parent's context block. Take no user prompts. On completion return **JSON only**:

```json
{
  "sub_skill": "effort-estimate",
  "status": "ok",
  "output_json": "<abs path to effort-estimates-*.json>",
  "summary": "<one-line: ddl_objects, total_estimated_hours>",
  "error": null
}
```

- Unsupported dialect (`ASM0031`): `status` `"skipped"`, `output_json` `null`, `error` `null`.
- Any other failure: `status` `"error"`, `output_json` `null`, `error` `"<message>"`.
