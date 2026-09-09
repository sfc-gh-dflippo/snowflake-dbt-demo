---
name: migrate-objects
description: Deploy and validate all object types (tables, views, functions, procedures) in dependency order. Triggers: deploy objects, migrate objects, deploy tables, deploy views, migrate functions, migrate procedures.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Migrate Objects

## Prerequisite: Support Level Check

Check `support` from the `configure()` response.

If `support` is `basic`, load [BASIC_SUPPORT.md](BASIC_SUPPORT.md) and **STOP**. Do not continue with the steps below.

## On Entry **IMPORTANT DO NOT SKIP**

Tell the user:
> **Phase 2: Migrate Objects.** Now we'll deploy your objects to Snowflake according to your wave plan (if you created one in assessments). Each object goes through a deploy-test-fix loop.

## Step 1: Confirm setup is finished

The Snowflake target (connection + database) and the testing path are
configured by the **`setup` state machine**, not here — they're the last
steps of setup, gated behind the post-assessment `continueToMigration`
prompt. A user who stopped at assessment has none of them yet.

Call `progress_setup()`.

- **`completed: true`** → setup is finished; continue to Step 2.
- **Anything else** (a `next_task` / `next_prompt` came back) → setup isn't
  done. Load `../setup/SKILL.md` and drive it to completion, then come
  back. Don't ask for a connection, database, or testing preference
  yourself — the machine owns those questions and persists the answers.

This is also the path for a user who answered "Not now" at the gate and has
since changed their mind: the prompt is re-offered, and answering "Yes"
walks them through the Snowflake target and testing setup.

## Advancing and reporting

This rule is the same for **every** task in the loop below — deploy, test, capture, seed, fix, validate:

1. **Do the task's work** as its skill describes.
2. **Ask what's next.** Re-pull `migration_status(mode="my_objects_summary")` (or `migration_status(mode="next_task", object_id="<id>")` for one object). The machine advances you when it can see the work is done — a tool wrote the registry field, the object exists in Snowflake, or the expected file exists.
3. **Call `transition_status` to report or override:**
   - a **failure** you can't fix — `transition_status(status='advance', task='<task>', outcome='failed', error='<sql|infra>')`;
   - an outcome the system **can't observe** and you had to judge — e.g. "all tests passed" ([migrate-object/RUN_TESTS.md](migrate-object/RUN_TESTS.md)), view parity ([migrate-object/VALIDATE_VIEW.md](migrate-object/VALIDATE_VIEW.md)), ETL stabilization ([migrate-etl/SKILL.md](migrate-etl/SKILL.md));
   - an **override** — `bypass` a precondition, `reset` an errored task, or `skip`.

The outcome and error vocabulary is defined once in [../extensibility/TASKS.md](../extensibility/TASKS.md#outcome-vocabulary).

## Autonomous mode

If the user asks to run the wave unattended — "autonomous", "auto-pilot", "just
migrate everything", "run objects in parallel" — load
[autonomous/SKILL.md](autonomous/SKILL.md) instead of the loop below and follow
it. That skill claims work itself and dispatches one subagent per ready task
group, up to a parallelism the user picks, escalating only when one gets stuck.

Everything below is the interactive loop: one batch at a time, the user picks
every group and every claim. It stays the default — do not offer autonomous mode
as a menu item in 2b, and do not switch to it unless the user asks.

## Step 2: Object Loop

**IMPORTANT** Ask the user to `/compact` between work units to free up context. **IMPORTANT**

### 2a. Pull status

> **Entry call — always.** Whenever you enter this skill, you must **first** call `migration_status(mode="my_objects_summary")`.

Cache the response — it drives the render in 2b and the drill-down `id`s in 2c.

If `groups` is empty, `blocked_groups` is empty, and `errored_count` and `done_count` are both 0, the user has no active claims. Tell them so and go to Step 2c → **"User picked `claimObjects`"** to pick up new work.

### 2b. Render

> **Finish before claiming new work.** Done objects sitting unmerged keep your branch ahead of `main`, which forces every teammate to rebase against stale state (or worse, duplicate the work you've already finished). Whenever `done_count > 0`, you must steer the user toward `finishObjects` before offering any new claims.

Show **only** the following status lines, all derived from the cached summary response. Skip any line whose count is zero or whose group is empty — do not write "(no errored bucket)" or "(none)" placeholders, and do not mention buckets that don't apply.

> **Use `group.user_label` verbatim.** Every group entry carries a server-controlled `user_label` (e.g. `"Generate test cases from source database"`). Render it exactly as returned. **Do not paraphrase, shorten, or substitute the camelCase `group.task` identifier** — those identifiers (`generateTestCases`, `captureBaseline`, `extractRules`, ...) are opaque to end users and must not appear in your output.

- One line per `group`: `<group.count> <group.object_type>s ready: <group.user_label>`. If `group.reason` contains a parenthetical like `(claimed in another session)`, include it after the count — e.g. `1 table (claimed in another session) ready: Deploy`.
- One line per `blocked_groups` entry: `<count> <object_type>s blocked at "<blocked_group.user_label>" (waiting on dependencies)` — only if `blocked_groups` is non-empty. Same rule: include any session parenthetical from the reason after the count. Don't list individual deps here; that comes from the drill-down in 2c.
- `<done_count> objects ready to finish (merge)` — only if `done_count > 0`.
- `<errored_count> objects errored` — only if `errored_count > 0`.

Then ask the user to pick a next action. **Only list actions you are actually offering** — never include an absent option just to acknowledge it. Build the action menu like this:

1. One numbered item per task group, labelled `<group.user_label> for the <group.count> <group.object_type>(s)` — e.g. `Deploy for the 5 tables`, `Generate test cases from source database for the 1 function`. Use `group.user_label` verbatim.
2. One numbered item per `blocked_groups` entry, labelled `Resolve blocked <object_type>s waiting on "<blocked_group.user_label>" (see deps)` — only if `blocked_groups` is non-empty.
3. `finishObjects` — only if `done_count > 0`.
4. `claimObjects` — only if `done_count == 0` (when `done_count > 0`, omit this entirely; the user must merge first). The exception: if the user *explicitly overrides* on a later turn ("I know, claim anyway", "skip the merge for now"), proceed to claim and flag the unmerged done objects in your reply.
5. The errored bucket — only if `errored_count > 0`.

**Wait for the user's response — do not proceed to 2c until they choose.**

### 2c. Dispatch

**User picked a task group** → take the matching `group.id` from the cached summary and call:

```
migration_status(mode="my_objects_details", group=<group.id>)
```

When `object_type == "etl"`, the group is an ETL stabilization batch — load [migrate-etl/SKILL.md](migrate-etl/SKILL.md) and follow it. SQL object types (`table`, `view`, `procedure`, `function`, `bteq`) follow the loop already described by `instructions` (BTEQ scripts skip deploy).

VERY IMPORTANT: **Wait for user input before acting.** Once the user confirms which objects to operate on, follow the `instructions` field on the response.

**User picked `claimObjects`** → load [actions/claim_objects.md](actions/claim_objects.md).

**User picked `finishObjects`** → load [actions/finish_objects.md](actions/finish_objects.md).

**User picked a blocked group** → call `migration_status(mode="my_objects_details", group="<blocked_id>")`.

> **Differentiate "missing" deps from "not-yet-completed" deps.** Walk every `objects[i].blocked_on[]` entry and look at `reason`:
>
> - `reason == "missing"` → the dep is **not in the project at all** (the resolver also classifies orphan deps with no registry entry as missing). Present a per-object resolution menu:
>
>   1. **Register the missing dep** — extract DDL from the source database (or import a local SQL file) and add it to the project. Load `../register-code-units/SKILL.md` for the matching dep `object_type`. After registration completes, re-run the blocked group; the dep should now resolve.
>   2. **Stub the missing dep in Snowflake** — create a placeholder object (empty table / no-op procedure / view returning the right column shape) so the dependent unit can deploy. Use this when the source isn't available but the shape is known. Capture what was stubbed in `extensions.notes` on the registry entry so the team has a record.
>   3. **Mark this object out of scope** — when the dependent shouldn't migrate at all because its missing dep is genuinely deprecated. Run `update_registry(field="inScope", status="false", objects="<object_id>")`.
>   4. **Bypass the precondition** — **last resort, not a peer of the options above.** Do not offer it proactively; use it only when the user has already mitigated the dep externally (e.g. it lives in another database that's already in Snowflake) and explicitly insists on proceeding without registering. A `reason` is required and the bypass is surfaced distinctly downstream (never as a satisfied precondition). Use `transition_status(status="bypass", task="<blocking_task>", where="id IN ('<object_id>')", reason="<why the dep is safe to skip>")`. This is logged and reversible.
>
>   **Wait for the user to pick one option per object** before acting. Do not auto-pick — "missing" usually surfaces a real data-modeling decision the user needs to make.
>
> - any other `reason` (e.g. `"deploy not completed"`, `"migrateData not completed"`) → the dep exists in the project but its prerequisite task hasn't finished yet. No prompt needed; the dep will resolve itself once the user finishes the upstream group. Tell the user which upstream group is blocking and offer to switch to it.

**User picked the errored bucket** → call `migration_status(mode="my_objects_details", group="errored")` to fetch `ErroredObject` entries and present them. **Wait for the user to pick which errored object(s) to address** before attempting any resolution; resolution depends on each `task`/`reason`.

### Resolving errored long-running tasks (`migrateData`, `validateData`, `runTests`)

When a long-running task fails and the failure is
**transient** (Snowflake connection drop, source timeout, cancelled
run), don't try to fix anything — just retry. After confirming with
the user, call:

```
transition_status(status="reset", task="<errored task>", where="id IN ('<id1>', '<id2>')")
```

This clears the registry stamp behind the task so the next walk
re-emits the task as Pending. The agent (or user) re-runs the task
the same way as before. For non-transient failures (schema drift,
missing target tables, etc.) the agent should diagnose and fix the
root cause first; reset is only for "try again now that the
environment is healthy."

`reset` is also useful when the user manually fixed something
out-of-band and wants the resolver to re-evaluate — for example,
they corrected a column type in Snowflake and want `validateData` to
re-run.

### After `migrateData` (data migration run)

When the current task is **`migrateData`** and you call `migrate_data(mode="run")` (from FSM instructions or this skill), you **must** complete poll and report before marking work done:

1. Load [actions/data-migration/SKILL.md](actions/data-migration/SKILL.md) **Steps 5–7** if you have not already (background Monitor or poll fallback with `job_status`, present the error-first migration report, offer teardown).
2. Do not return to the object loop or claim the next task until the user has seen the summary.

### After `validateData` (data validation run)

When the current task is **`validateData`** and you call `validate_data(mode="run")` (from FSM instructions or the validate-objects skill), you **must** complete poll and report before marking work done:

1. Load [../validate-objects/actions/validate_tables.md](../validate-objects/actions/validate_tables.md) **Steps 4–6** if you have not already (background Monitor or poll fallback with `job_status`, present the error-first validation report, offer re-validation when eligible, then teardown).
2. Do not return to the object loop or claim the next task until the user has seen the summary.

## Step 3: Report

Call `migration_status()` and present a completion summary to the user:
> **Wave `<N>` complete.** `<deployed_count>` objects deployed, `<tested_count>` tested and passing, `<failed_count>` still failing. `<data_migrated_count>` tables with data migrated.

If all waves are done:
> **Migration complete.** All objects have been deployed to Snowflake and validated.

When all waves are done **and** any wave used data migration or data validation (i.e. SPCS infrastructure was provisioned), unconditionally load [../data-infrastructure/teardown/SKILL.md](../data-infrastructure/teardown/SKILL.md) to suspend the orchestrator + compute pool and prompt the user to stop the local worker. Skip this if the project never configured a `compute_pool` (no SPCS infrastructure was used).

If the wave is complete, the next `configure()` call will auto-advance to the next wave.
