---
name: object-exclusion-detection
description: Identify database objects that can be excluded from migration (temporary/staging, deprecated/legacy, testing, duplicates, version conflicts) by running the SCAI assessment object-exclusion command.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Object Exclusion Detection

Run `scai assessment object-exclusion` in the SCAI project.

## Sub-Agent Mode

When invoked from a parent skill (e.g., `assessment/SKILL.md`) as a sub-agent, the parent provides a context block with the fields below. This sub-skill takes no user prompts in either mode, so the only behavioral change in sub-agent mode is the JSON return contract.

| Field | Required | Notes |
|---|---|---|
| `project_dir` | yes | absolute path to the SCAI project root |

**On entry:** call the `configure` MCP tool with `project_dir` from the context block.

Run `scai assessment object-exclusion` from `project_dir`.

**On completion**, return **JSON only**:

```json
{
  "sub_skill": "object-exclusion-detection",
  "status": "ok",
  "output_json": "<abs path to object_exclusion_analysis_*.json>",
  "summary": "<one-line: temp/staging, deprecated, testing, duplicates counts>",
  "error": null
}
```

On failure: `"status": "error"`, `"output_json": null`, `"error": "<message>"`.

## Output

`scai assessment object-exclusion` writes one file:

```
<project_dir>/artifacts/assessment/object_exclusion_analysis_YYYYMMDD_HHMMSS.json
```

Hand that path back to the parent skill as `--exclusion-json`. Don't parse or rewrite it.

For the summary line, read `summary` from the JSON:

```json
{
  "summary": {
    "total_objects_found": 0,
    "temp_staging_objects_count": 0,
    "deprecated_legacy_objects_count": 0,
    "testing_objects_count": 0,
    "duplicate_objects_count": 0,
    "objects_with_multiple_versions": 0
  }
}
```

Per-category detail may live in the registry instead of the JSON (`detail_location: "registry"` vs `"json"`) — irrelevant to this skill, the parent report generator handles both.

## What It Detects

Temp/staging, deprecated/legacy, testing objects, duplicates, version conflicts, and potentially misclassified objects — pattern matching is entirely internal to SCAI, nothing to configure here.

## Related

- Parent: `../SKILL.md` (consumes the artifact via `--exclusion-json`)
- SCAI built-in help: `scai assessment object-exclusion --help`
