# Conversion State Tracker Schema (`conversion_state.json`)

## When to Load

Load on **resume** (when `conversion_state.json` exists and needs interpretation) or when writing state for the first time. Not needed in context for routine step execution — the step-specific instructions reference which fields to write.

---

## Full Schema

```json
{
  "metadata": {
    "output_dir": "<path>",
    "target_schema": "DATABASE.SCHEMA",
    "migration_mode": "1:1",
    "created_at": "<ISO timestamp>",
    "last_updated": "<ISO timestamp>",
    "current_step": "5",
    "total_files": 5,
    "validation_scope": "full",
    "pre_approved_compilation": false,
    "pre_approved_validation": null,
    "sp_permission": null
  },
  "source_mappings": {
    "LIBNAME_NAME": {
      "engine": "sqlsvr",
      "original_dsn": "DSN_NAME",
      "original_schema": "dbo",
      "target_database": "SNOWFLAKE_DB",
      "target_schema": "SNOWFLAKE_SCHEMA",
      "tables": ["table1", "table2"]
    }
  },
  "assessment": {
    "consumed": true,
    "source_path": "<abs path to the assessment.json used>",
    "generated_at": "<assessment metadata.generated_at>",
    "consumed_at": "<ISO timestamp>",
    "stale": false,
    "reconciliation": {
      "files_compared": 9,
      "files_matched": 8,
      "files_mismatched": 1,
      "mismatches": [
        {"file": "b.sas", "field": "primary_tier", "assessment": "TIER_2_SP", "convert": "TIER_1_SQL"},
        {"file": "b.sas", "field": "blocks", "assessment": 22, "convert": 20}
      ]
    }
  },
  "files": {
    "script_name.sas": {
      "status": "converted",
      "tier": "1-SQL",
      "output_file": "script_name.sql",
      "blocks": 3,
      "dependencies": {"creates": ["TABLE_A"], "reads": ["TABLE_B", "TABLE_C"]},
      "classification_complete": true,
      "conversion_complete": true,
      "self_check_passed": false,
      "compilation_status": "PENDING",
      "compilation_errors": [],
      "compilation_fix_attempts": 0,
      "validation_status": "PENDING",
      "validation_mismatches": []
    }
  },
  "gates": {
    "step_2_5_source_resolution": "PENDING",
    "step_6a_artifacts": "PENDING",
    "step_7a_test_artifacts": "PENDING",
    "phase_5_e2e_orchestration": "PENDING",
    "step_10_final_artifacts": "PENDING"
  },
  "trace_progress": {
    "total_files_in_scope": 15,
    "files_traced": [],
    "files_remaining": [],
    "current_batch": 0,
    "batch_size": 5,
    "concerns_found": []
  },
  "compilation_env": null,
  "summary": {
    "classified": 0,
    "converted": 0,
    "self_checked": 0,
    "compiled_pass": 0,
    "compiled_fail": 0,
    "validated_pass": 0,
    "validated_fail": 0,
    "pending_validation": 0
  }
}
```

---

## `assessment` object

Written in Step 3 to record whether a prior `assess-sas-migration` run was auto-discovered and
consumed as a baseline, and how this conversion's block counts/tiers reconcile against it.

- **When found & consumed:** `consumed: true` with `source_path` (which `assessment.json` was used),
  `generated_at`, `consumed_at`, `stale` (true if the assessment predates the newest source edit),
  and a `reconciliation` object (`files_compared`, `files_matched`, `files_mismatched`, and a
  `mismatches` list of `{file, field, assessment, convert}` where `field` ∈ `blocks` / `primary_tier`
  / `tier_distribution`). Mismatches are informational — they never block conversion.
- **When none found:** `{"consumed": false, "reason": "not_found", "searched_paths": [...]}`
  (or `reason: "unreadable"` if a candidate existed but failed to parse). Conversion proceeds with
  fresh classification and no prompt.

---

## Companion Audit Trail — `checkpoint_log.jsonl`

`conversion_state.json` is the **current-state snapshot** (overwritten each transition). It is paired with `checkpoint_log.jsonl`, the **append-only audit trail** (one JSON line per checkpoint, never overwritten). BOTH are required artifacts. See `references/checkpoint-logging.md` for the line schema and append helper.

At every transition in the table below, the workflow MUST: (1) update `conversion_state.json`, then (2) append one line to `checkpoint_log.jsonl` — before advancing.

---

## Enforcement Rule — State Writes are BLOCKING PREREQUISITES

`conversion_state.json` is NOT optional. It MUST be written/updated at each transition point below. The NEXT step CANNOT begin until the state file reflects the current step's completion. If the file is missing or stale, write it before proceeding. At each transition, also append a checkpoint line to `checkpoint_log.jsonl`.

| Transition | Prerequisite (state file must show) | Checkpoint line appended |
|---|---|---|
| Step 1 → Step 2 | File exists with metadata (output_dir, target_schema, migration_mode, `current_step: "1"`) | `step:"1" status:"STARTED"` |
| Step 2.5 → Step 3 | `gates.step_2_5_source_resolution: "PASSED"` or `"SKIPPED"` (no external sources) — `source_mappings` populated if external sources found | `step:"2.5" status:"PASSED"\|"SKIPPED"` |
| Step 3 → Step 4 | All files have `status: "classified"`, dependencies populated; `assessment` object written (consumed+reconciliation, or `consumed: false`) | `step:"3" status:"PASSED"` |
| Step 5 → Step 6 | All files have `status: "converted"` | `step:"5" status:"PASSED"` |
| Step 6 → Step 6a | All files have `self_check_passed: true` | `step:"6" status:"PASSED"` |
| Step 6a → Step 7 | `gates.step_6a_artifacts: "PASSED"` | `step:"6a" gate:"step_6a_artifacts" status:"PASSED"` |
| Step 7a → Step 7b | `gates.step_7a_test_artifacts: "PASSED"` | `step:"phase_1" status:"PASSED"` |
| Step 7b → Step 7c | `trace_progress.files_remaining` is empty (all priority files traced) | `step:"phase_2" status:"PASSED"\|"SKIPPED"` |
| Step 7 → Step 8 | `current_step: "7"` | — |
| Step 8 → Step 8 compile | Target schema exists OR `compilation_env` is set (auto-created via Step 8-pre) | `step:"phase_3" status:"STARTED"` |
| Step 8 → Step 9 | All files have `compilation_status` set (SUCCESS, FAILED, or SKIPPED) | `step:"phase_3" gate:"phase_3_snowflake_compile" status:"PASSED"\|"SKIPPED"` |
| Step 9 → Phase 5 | Phase 4 gate shows PASSED or SKIPPED | `step:"phase_4" gate:"phase_4_snowflake_execute" status:"PASSED"\|"SKIPPED"` |
| Phase 5 → Step 10 | `gates.phase_5_e2e_orchestration: "PASSED"` or `"SKIPPED"` | `step:"phase_5" gate:"phase_5_e2e_orchestration" status:"PASSED"\|"SKIPPED"` |
| Step 10 → Complete | `gates.step_10_final_artifacts: "PASSED"`, `current_step: "complete"` | `step:"10" status:"PASSED"`, then `step:"complete" status:"PASSED"` |

**If the state file does not satisfy the prerequisite for the next step:**
1. Write/update it immediately
2. Verify the write succeeded (re-read the file)
3. Append the corresponding checkpoint line to `checkpoint_log.jsonl`
4. Only then proceed to the next step

This rule applies in BOTH interactive and batch modes. Context pressure does NOT exempt state writes.

---

## Resume Behavior (Step 1 Pre-Check)

- If `conversion_state.json` exists, read it and display:
  ```
  Prior conversion found. Status: [summary counts]. Last step: [current_step].
  Resume from step [current_step + 1]? / Restart fresh (overwrites)?
  ```
- If resume: skip all completed files/steps, continue from `current_step`
- If restart: delete state file and begin from Step 1

---

## File Status Progression

```
classified → converted → self_checked → compiled → validated → complete
```

---

## Valid `current_step` Values

| Value | Meaning |
|-------|---------|
| `"1"` | Step 1 complete (metadata captured) |
| `"2.5"` | External source resolution complete |
| `"3"` | Classification complete |
| `"5"` | Conversion in progress or complete |
| `"6"` | Self-check complete |
| `"7"` | Validation (tracing) complete |
| `"8"` | Compilation in progress |
| `"9"` | Snowflake execution in progress |
| `"10-in-progress"` | Report generation started |
| `"10"` | Report generation complete |
| `"complete"` | All gates passed, all artifacts verified |
