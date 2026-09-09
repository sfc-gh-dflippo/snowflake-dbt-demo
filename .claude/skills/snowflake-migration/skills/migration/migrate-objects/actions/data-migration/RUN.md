# Migrate data (per-object)

Guide for the `migrateData` task — migrate the batch of tables the machine handed you (`where = id IN (...)`). The shared orchestrator + worker are already up (brought up once via `data_infrastructure(mode="up")`; see `../../../data-infrastructure/SKILL.md`). This step is **pure dispatch**, not infrastructure setup.

## 1. Choose the approach (once per batch, if not already set)

The migration approach was chosen during setup and is persisted for all
objects. Do not re-ask or change it here. If it is unexpectedly missing, or
the user asks to change it (for example full → incremental watermark), return
the request to the main agent. The main agent must route through
[`../../../data-infrastructure/SKILL.md`](../../../data-infrastructure/SKILL.md),
which owns any setup delegation, persist the change once, and then redispatch
this task.

## 2. Generate the workflow

Call `migrate_data(mode="setup", where=<the batch's object filter>)`. It writes a workflow YAML and returns `edit_hints` plus any `partition_key_findings`. Review the file and apply row filters (`whereClauseCriteria`) or a partition column when the hints call for it. Pass `force_regenerate=true` only to discard prior edits and regenerate.

## 3. Dispatch

Call `migrate_data(mode="run", workflow_path=<path from setup>)`. This is **pure dispatch** against the already-running infrastructure — there are no infra flags to pass. If the response says infrastructure is not up, return the remediation to the main agent. Do not call `data_infrastructure` from this subagent; the main agent resumes the persisted setup and redispatches the task.

The response carries a `monitor` block (a `job_id` and a ready-made `watch_command`).

## 4. Track it

Arm the `monitor.watch_command` with the Monitor tool. Its terminal event's
`detail.completion` is the authoritative result and supplies the final
verdict, counts, and failures. Use `job_status(job_id)` only for an on-demand
status or lost-watch recovery; use `details=true` for deeper failure
diagnostics. For the full monitoring / reporting / teardown walkthrough,
load `SKILL.md` (Steps 5–7) in this folder.

## When it finishes

The machine reads live `DATA_MIGRATION.TABLE_PROGRESS` — do not stamp the registry. Present the migration summary (`SKILL.md` Step 6), and offer to tear the shared infrastructure down when the wave is done — unless you were dispatched for a single object, in which case leave it alone: `data_infrastructure(mode="down")` stops the worker every other slot is using, so that offer belongs to whoever owns the wave.

If the job **failed**, do not re-run it and do not change Snowflake with `sql_execute`. Call `migration_status(mode="next_task")`. A failed load is `error=sql` and the machine owns the next step. A judgment you made in the converted file (meanings vs compile) is a `note` after the fix, not a live `ALTER` and not a re-dispatch of the same workflow.
