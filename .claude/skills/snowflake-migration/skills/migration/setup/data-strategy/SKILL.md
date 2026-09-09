---
name: data-strategy
description: Capture the data migration + validation strategy (migration type, sync strategy, extraction strategy, target table type; validation type + sync strategy) by driving the data-migration-setup and data-validation-setup wizards to completion.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Capture Data Strategy

Capture the project's **data migration and validation strategy** by driving the existing
`data-migration-setup` and `data-validation-setup` wizards to completion. This skill only **drives**
those two wizards — it asks no new questions of its own (the questions live in those machines) and makes
no assumptions about who invoked it. Deciding *whether* to capture the strategy is the caller's job; when
this skill runs, it runs the wizards.

For a Snowflake-source validation-only project, skip Step 1 and run only the
validation wizard in Step 2. Snowflake is already the source and target, so
data migration is not available.

## Step 1 — Migration strategy (non-Snowflake sources only)

Drive the `data-migration-setup` machine to completion: call `progress_setup(mode="data_migration")` in a
loop until the response's `completed` is `true` — ask each response's `next_prompt` (plus any `then_ask`,
in the same turn) and send the answers back with `progress_setup(mode="data_migration", answers={...})`.

If the strategy was already chosen (e.g. a prior migration set it lazily), the first call returns
`completed: true` immediately — do not re-prompt.

## Step 2 — Validation strategy

Then drive the `data-validation-setup` machine the same way: `progress_setup(mode="data_validation")` in
a loop until `completed`. An already-chosen strategy returns `completed: true` at once.

The choices persist to `plugin.yml` as `data_migration_type`, `data_migration_sync_strategy`,
`data_migration_extraction_strategy`, `data_migration_target_table_type` (Redshift), `data_validation_type`,
and `data_validation_sync_strategy`.

## Changing an existing choice

Only the main/setup agent changes persisted strategy. A per-object
`migrateData` / `validateData` subagent must return the request to its parent
instead of re-running setup or changing infrastructure.

When the user explicitly asks for a different strategy, confirm the new choice
once and apply it through the corresponding setup tool. For example, changing
an existing full load to incremental watermark means calling
`migrate_data(mode="setup", migration_type="incremental",
sync_strategy="watermark", force_regenerate=true, where=...)`, then reviewing
the regenerated workflow and setting its real `watermarkColumn` (plus
`primaryKeyColumns` / `trackModifications` when required for an already
populated target). Explicit setup arguments persist the new defaults in
`plugin.yml`; subsequent object dispatches reuse them without asking again.

If the change also affects placement or worker prerequisites, return through
[`../../data-infrastructure/SKILL.md`](../../data-infrastructure/SKILL.md)
before resuming dispatch.

> Infrastructure readiness (compute pool / orchestrator service) is **not** covered here — that is the
> shared `../../data-infrastructure/SKILL.md`. This skill only captures the data strategy.

Return control to the caller.
