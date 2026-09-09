## Batch Output Format

Each orchestration batch agent writes a structured artifact at `{UNIT}/stabilization/phases/phase_{N}/batch_{B}.md`. This is the **only** output channel for batch results — the orchestrator reads these artifacts to update tracking and apply fixes.

> **Placeholder:** `{B}` is the full phase-qualified batch ID (e.g., `B1.1`, `B1.2`). Schema names use the flat format `ETL_FIX_P{N}_B{M}` (e.g., `ETL_FIX_P1_B1`) where `{M}` is the batch number without phase prefix.

```markdown
# Batch {B} — Phase {N}

## Elements

### {element_name}

- **Status**: test-passed | test-failed | skipped | needs-user | auto-fixed-needs-review | failed
- **Reason**: (required for skipped, needs-user, auto-fixed-needs-review, failed)
- **Test file**: `{UNIT}/stabilization/tests/orchestration/{task_procedure_name}/{element_name}.sql`
- **Replacement tag**: `---- Start block: {exact_tag_from_orch_sql}`
- **Replacement SQL**:
\```sql
-- Production-ready SQL body (original DB/schema references, NOT test-env references)
-- This replaces everything between the Start and End tags in the orch SQL
{production_sql}
\```

### {next_element_name}
...
```

**Incremental write model:** Batch artifacts are written one element section at a time — the agent appends each `###` section immediately after completing that element. **Partial artifacts are valid** — if a batch agent stops early due to context pressure, the orchestrator reads whatever elements are present and treats missing elements as unprocessed (available for retry). Do not assume a batch artifact is complete just because it exists.

**Rules for batch artifacts:**
- One `###` section per element assigned to this batch
- Every assigned element MUST appear in a fully-completed artifact — but partial artifacts (missing elements) are expected during recovery flows
- `Replacement SQL` is required for `test-passed`, `auto-fixed-needs-review`, and `skipped:disabled-in-source` statuses, and conditionally for `no-fix-needed` when the element still has EWI markers that must be cleared
- `Replacement SQL` must use the **original** database/schema references from the orch SQL file, not the test schema (`ETL_FIX_P{N}_B{M}`)
- **Replacement tag**: The EXACT tag line from the orch SQL — either `---- Start block '<name>'` for containers or `---- Start '<name>'` for non-containers. Must match verbatim.
- `Test file` path is required for all statuses except `skipped` and `failed`

## Learning Artifact Format

Each batch agent writes a per-batch learning file at `{UNIT}/stabilization/phases/phase_{N}/learnings_batch_{B}.md`. These are merged into `{UNIT}/stabilization/tracking/fix_log.md` at phase end by the orchestrator (single-writer).

```markdown
# Learnings — Batch {B}, Phase {N}

## {element_name}: {one-line summary of fix}

- **EWI/FDM**: {code} — {title}
- **Marker status**: NO_MARKER | MARKER_BROKEN | MARKER_PLUS_BUG | EWI_MARKED | FDM_MARKED | EWI_CRASH
- **Classification**: engine-defect | conversion-improvement | intentional-decline | context-dependent
  (Intentional `!!!RESOLVE EWI!!!` declines use marker `EWI_MARKED` + classification `intentional-decline` — do not invent a separate marker code.)
- **Root cause**: {what the converter did wrong or couldn't handle}
- **Fix pattern**: {the SQL transformation applied}
- **Fix instances**: (one row per file the fix touched — anchors let a consumer pull arbitrary context on demand)

| File (repo-relative) | Anchor (fixed) | Original ref | Source XML |
|---|---|---|---|
| {models/.../foo.sql} | {block tag / macro / model + line hint} | {stabilization/original/.../foo.sql + line hint, or `new-file`} | {source.XML :: TRANSFORMATION NAME} |

- **Before** (short inline excerpt for humans — full context recoverable via `Original ref`):
\```sql
{original snippet}
\```
- **After** (short inline excerpt — full context recoverable via `Anchor (fixed)`):
\```sql
{fixed snippet}
\```
- **Reusable**: yes | no — {why}

## {next_element_name}: ...
```

**Rules:**
- Only include entries for elements where a fix was actually applied (`test-passed` or `auto-fixed-needs-review`)
- `Reusable: yes` means this pattern can be applied to similar EWI/FDM codes in future phases
- **`Fix instances` is required**: list every file the fix touched with a stable anchor. Prefer symbol/tag anchors (`---- Start block '<name>'`, macro name, model name) as primary and line numbers only as a hint, since line numbers drift across later phases. `Original ref` points into the `stabilization/original/` backup (or `new-file` when the fix created the artifact). This is what lets downstream consumers (e.g. bug reports) expand context instead of re-deriving it by diffing trees.
- **`Classification` is required and must be honest about intent.** Use `intentional-decline` when the converter *correctly* emitted a declined-conversion signal (the `!!!RESOLVE EWI!!!` breaking wrapper, or a supported EWI/FDM) and the fix was manual resolution — this is **not** an engine defect. Use `engine-defect` only for wrong output with no/broken signal. Use `conversion-improvement` when a better deterministic conversion is possible. Never log an intentional `!!!RESOLVE EWI!!!` decline as `engine-defect`.
- Keep the inline Before/After excerpts short (relevant lines only) — full surrounding context is reachable through the anchors, so the log stays lean and doesn't drift.
- If no fixes were applied (all elements skipped or passed without changes), write an empty learnings file with a note: `No fixes applied in this batch.`
