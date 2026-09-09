# Checkpoint Logging (`checkpoint_log.jsonl`)

## When to Load

Load once, early (Step 1), and keep the append rule in context for the whole conversion. This file is lightweight — it defines an append-only audit trail that complements `conversion_state.json`.

---

## Purpose

`conversion_state.json` is a **current-state snapshot** — it is overwritten at every transition, so it cannot answer "what happened, and when?" across a multi-session conversion.

`checkpoint_log.jsonl` is the **immutable audit trail** — one JSON object per line, appended (never overwritten) at every checkpoint. It enables:
- Reconstructing exactly what passed/failed/skipped across context windows and sessions
- Debugging a stalled or failed conversion without replaying it
- Auditing credit-consuming operations (when each Snowflake phase ran)

The two files are complementary and BOTH required:

| File | Role | Write mode |
|------|------|-----------|
| `conversion_state.json` | Current state (resume point, per-file status, gates) | Overwrite |
| `checkpoint_log.jsonl` | Historical event log (audit trail) | Append-only |

**Location:** `<output_dir>/checkpoint_log.jsonl`

---

## Line Schema

Each line is a single complete JSON object (JSON Lines format — no array wrapper, no trailing commas):

```json
{"ts": "2026-06-23T10:15:30Z", "step": "6a", "gate": "step_6a_artifacts", "status": "PASSED", "artifacts_written": ["customers_clean.sql"], "rows_affected": null, "notes": "12 .sql files verified on disk"}
```

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `ts` | string (ISO 8601 UTC) | Yes | When the checkpoint occurred |
| `step` | string | Yes | Workflow step or phase (e.g. `"1"`, `"3"`, `"6a"`, `"phase_2"`, `"phase_5"`) |
| `gate` | string or null | Yes | Gate name if this checkpoint corresponds to a gate (e.g. `"phase_3_snowflake_compile"`), else null |
| `status` | string | Yes | `STARTED` \| `PASSED` \| `FAILED` \| `BLOCKED` \| `SKIPPED` \| `INFO` |
| `artifacts_written` | string[] | No | Files written/updated at this checkpoint (basenames) |
| `rows_affected` | integer or null | No | Row count when relevant (e.g. synthetic inserts, execution output) |
| `notes` | string | No | Short human-readable context (keep < 200 chars) |

---

## Append Rule (BLOCKING — append BEFORE advancing)

At every point where the workflow writes `conversion_state.json` (see the transition table in `references/state-tracker-schema.md`), also append ONE line to `checkpoint_log.jsonl` **before** beginning the next step.

Order of operations at any checkpoint:
1. Complete the step's work (artifacts on disk)
2. Update `conversion_state.json` (current-state snapshot)
3. Append a line to `checkpoint_log.jsonl` (audit trail)
4. Only then advance to the next step

If `checkpoint_log.jsonl` does not exist yet, create it with the first line. Never rewrite existing lines — append only.

---

## Append Helper

Use the Bash tool to append (do NOT read-modify-write the whole file — that defeats append-only and risks corruption):

```python
import json, os
from datetime import datetime, timezone

def append_checkpoint(output_dir, step, status, gate=None, artifacts=None, rows=None, notes=None):
    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "step": step,
        "gate": gate,
        "status": status,
        "artifacts_written": artifacts or [],
        "rows_affected": rows,
        "notes": notes or ""
    }
    path = os.path.join(output_dir, "checkpoint_log.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

---

## Checkpoints to Log (minimum)

| Step / Phase | status values to emit |
|--------------|----------------------|
| Step 1 (input gathered) | `STARTED` (conversion begins) |
| Step 2.5 (source resolution) | `PASSED` or `SKIPPED` |
| Step 3 (classification) | `PASSED` |
| Step 5 (conversion) | `INFO` per batch, `PASSED` when all converted |
| Step 6 (self-check) | `PASSED` |
| Step 6a (artifact gate) | `PASSED` or `BLOCKED` |
| Phase 1 (synthetic data) | `STARTED`, then `PASSED`/`BLOCKED` |
| Phase 2 (LLM trace) | `STARTED`, then `PASSED`/`SKIPPED`/`BLOCKED` |
| Phase 3 (compilation) | `STARTED`, then `PASSED`/`SKIPPED`/`BLOCKED` |
| Phase 4 (Tier 2/3 execution) | `STARTED`, then `PASSED`/`SKIPPED`/`BLOCKED` |
| Phase 5 (E2E orchestration) | `STARTED`, then `PASSED`/`SKIPPED`/`BLOCKED` |
| Step 10 (report) | `PASSED` |
| Complete | `PASSED` with notes "conversion complete" |

For credit-consuming phases (3, 4, 5), also log an `INFO` line capturing the user's consent decision (e.g. `notes: "Tier-2 gate: user approved"`).

At Step 3, the `PASSED` line should carry an assessment note capturing baseline consumption and
reconciliation, e.g. `notes: "assessment consumed=true matched=8 mismatched=1 stale=false"` (or
`notes: "assessment consumed=false reason=not_found"` when none was discovered).

---

## Reading the Log (resume / audit)

On resume, the log is informational only — `conversion_state.json` remains the authoritative resume point. Use the log to:
- Show the user a timeline: `tail` the file and render each line as `[ts] step status — notes`
- Confirm a credit phase actually ran (search for the phase's `PASSED` line)
- Diagnose where a prior session stopped (last line = last completed checkpoint)
