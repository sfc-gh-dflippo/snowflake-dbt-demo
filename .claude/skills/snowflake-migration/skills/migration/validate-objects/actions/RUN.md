# Validate data (per-object)

Guide for the `validateData` task — validate the batch of tables the machine handed you (`where = id IN (...)`). The shared orchestrator + worker are already up (brought up once via `data_infrastructure(mode="up")`). This step is **pure dispatch**, not infrastructure setup.

## 1. Choose validation scope (once per batch, if not already set)

Validation type / sync strategy were chosen during setup and persist across
objects. Do not ask or run setup here. If they are missing, or the user asks
to change them, return the request to the main agent so it can update setup
once through [`../../data-infrastructure/SKILL.md`](../../data-infrastructure/SKILL.md),
which owns any setup delegation.

## 2. Generate the workflow

Call `validate_data(mode="setup", where=<the batch's object filter>)`. It writes a validation workflow YAML and returns `edit_hints`. Review and edit the toggles (schema / metrics / row validation, continue-on-failure) if needed before running.

## 3. Dispatch

Call `validate_data(mode="run", workflow_path=<path from setup>)` — **pure
dispatch** against the already-running infrastructure. If the response says
infrastructure is not up, stop and return that remediation to the main agent.
Do not call `data_infrastructure` from this subagent; the main agent resumes
the persisted setup and redispatches the task. Use
`validate_data(mode="revalidate", workflow_name=<finished parent>)` to retry
only failed partitions of a finished run.

The response carries a `monitor` block (a `job_id` and a ready-made `watch_command`).

## 4. Track it

Arm the `monitor.watch_command` with the Monitor tool. Its terminal event's
`detail.completion` is the authoritative result and supplies the final
verdict, counts, and failures. Use `job_status(job_id)` only for an on-demand
status or lost-watch recovery; use `details=true` for deeper failure
diagnostics. For the full monitoring / reporting / teardown walkthrough,
load `validate_tables.md` (Steps 4–6) in this folder.

## When it finishes

The machine reads live `DATA_VALIDATION.TABLE_PROGRESS_DETAIL` — do not stamp the registry. Present the error-first validation report (`validate_tables.md` Step 5) and offer re-validation when eligible.

Offer re-validation only after the report identifies a changed input or a transient
condition that has cleared. A repeatable source/target row mismatch, schema drift,
or invalid identifier / compilation error in generated validation SQL is
deterministic: park it with the exact evidence and required repair instead of
dispatching the same workflow again.
