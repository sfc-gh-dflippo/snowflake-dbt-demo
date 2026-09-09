---
name: setup
description: Set up a migration project — connect to source, initialize, extract objects, convert, and assess. Covers steps 1-5 of the migration lifecycle.
license: Proprietary. See License-Skills for complete terms
---

# Migration Setup

## On Entry

Tell the user:
> **Phase 1: Setup** — I'll walk you through connecting to your source database, initializing the project, registering your objects, converting them to Snowflake SQL, and generating an assessment report. Once you've seen the assessment I'll ask whether you want to go on to migrating objects.

For a Snowflake source, use this instead:
> **Snowflake Validation Setup** — I'll initialize a Snowflake-source project,
> configure the Snowflake target and orchestrator, and capture your validation
> strategy. Snowflake-source projects skip code conversion, assessment,
> deployment, data migration, testing setup, and the Data Exchange Worker.

## Flow

Setup is driven by the **`setup` state machine** — the resolver picks
the next step automatically. The flow:

1. Call `progress_setup()`. The response carries the following keys
   when relevant — fields that would otherwise be the no-op default
   (`completed: false`, `blocked: false`, etc.) are omitted to keep
   responses small:
   - `next_task` — id of the task the resolver landed on
   - `next_skill` — sub-skill path to load (omitted when the task is
     handled inline via `next_prompt`)
   - `next_skill_md` — when present, the **full body** of the skill at
     `next_skill`. Execute it directly without calling Read. Only
     emitted for skills small enough to inline; for larger ones (or
     any skill not in the inline set), `next_skill` is the path and
     you Read it normally.
   - `next_prompt` — present when the task is an inline question (see
     step 3 below)
   - `then_ask` — further questions to ask in the **same turn**, in
     order (see step 3)
   - `planned_steps` — remaining task ids in order
   - `completed: true` — only when the machine reached its terminal
     state; absence means "not done, keep looping"
   - `blocked: true` (+ `blocked_on`), `errored: true` (+
     `error_reason`), `committed: [...]`, `project_initialized: false`
     — emitted only when actionable
2. If `completed` is `true`, jump to **On Completion** below.
3. If `next_prompt` is non-null, the engine wants you to ask the user a
   question directly — no sub-skill load required. Surface the prompt
   exactly as the engine returned it via `ask_user_question` (`multiSelect = false`):
   - `next_prompt.question` is the question text.
   - `next_prompt.options` is the list of `{label, value, description?}`
     entries to render. Use `label` as the user-facing choice; **never**
     show `value` to the user.
   - **If `then_ask` is present, ask every question in one
     `ask_user_question` call** — `next_prompt` first, then each entry of
     `then_ask` in the order given, one question per entry,
     `multiSelect = false` on each. Don't ask them one call at a time.
     They are queued precisely because the machine reaches all of them
     whatever the user answers, so nothing you learn from one can make a
     later one wrong. The queue is capped so a whole run always fits in a
     single call; never split it.
   - Send every answer you collected in **one** call:
     `progress_setup(answers={"<write_to>": "<chosen value>", ...})` —
     keys are each prompt's `write_to`, values the chosen option's
     `value` verbatim (a string, even for a number or a boolean). That
     records the answers *and* returns the next step, so for **questions**
     it replaces both the separate `configure(...)` call and the follow-up
     `progress_setup()`. Go to step 2 with its response.
   - A prompt whose chosen option carries `then` is the other case —
     that answer leads somewhere specific, so you can start on it in the
     same turn (such a prompt never has `then_ask`):
     - `then.completed` → setup is done; jump to **On Completion**.
     - `then.skill` → that is the step the answer leads to. Send the
       answer with `progress_setup(answers={...})`; its response carries
       `next_skill_md` for that very step, so execute it from there
       rather than Reading the file. `then` gives you the route early —
       what to tell the user, and what's coming — while the body arrives
       once, for the branch actually taken.
     - a `then` with only `task` → that step is already satisfied; send
       the answer and act on whatever the response names.
     If that response names the same `next_task` you just acted on, the
     step did not complete — do **not** run its skill again. Re-running it
     re-asks questions the user just answered; instead do what that skill
     says to do when it can't finish (e.g.
     `progress_setup(skip="<task>")`).

   If the user has **already** answered one of these questions in
   conversation — "move on to migration", "I'll use SQL Server" — don't
   ask it again. Put it straight in `answers` on your next call. An
   answer for a step that is already settled is harmless: the walk still
   decides what runs next, so a premature or unnecessary answer costs
   nothing.

   `answers` is for **questions the engine asked you**. Values a
   *sub-skill* tells you to set — `project_dir_confirmed`,
   `source_connection`, `git_main_branch`, `snowflake_database` — go
   through `configure(...)` as that skill instructs; that is what it is
   for, and those steps are not prompts. Folding one into `answers`
   anyway is tolerated rather than an error, but it is not the path.
4. Otherwise (no prompt): if `next_skill_md` is set, **execute its
   instructions directly in this same turn** — no Read needed.
   Otherwise **load the skill at `next_skill` immediately** (Read it,
   then execute in the same turn). The sub-skill is responsible for
   asking the user any question it needs. Do not surface "Next step
   pending: X — let me know" prose and wait — that's a wasted
   round-trip; the user already said "continue" upstream. When the
   sub-skill returns, go back to step 1.

Note: `progress_setup()` also handles git commits automatically — when a
task with `commitOnComplete` completes, the tool commits and pushes
project files. You do not need to run git commands manually.

Tasks the machine routes through, in order:

| Task id                          | How the agent handles it                                          |
|----------------------------------|-------------------------------------------------------------------|
| `validateEmptyDir`               | sub-skill: `setup/validate-empty-dir.md`                          |
| `confirmProjectDir`              | sub-skill: `setup/confirm-project-dir.md`                         |
| `enableGit`                      | skipped for a fresh (non-git) directory — git is on by default; otherwise inline prompt |
| `configureGit`                   | sub-skill: `setup/git.md` (existing repos only; fresh dirs auto-init) |
| `recommendSafeTools`             | inline prompt — arrives with the next two queued in `then_ask`     |
| `chooseSourceDialect`            | inline prompt (queued)                                            |
| Snowflake branch                 | `configureSnowflakeTarget` → `setupDataInfrastructure` → `dataStrategy` |
| `chooseEntryMode`                | inline prompt (queued; nothing queues after it — it routes by dialect) |
| `midwayEntry`                    | sub-skill: `setup/midway-entry.md`                                |
| `chooseCodeSource`               | inline prompt (`next_prompt`) — extract vs. local files; each answer carries its `then` |
| `configureSourceConnectionExtract`      | sub-skill: `setup/configure-source-connection.md` (extract path only) |
| `registerCode`                   | sub-skill: `register-code-units/SKILL.md`                         |
| `convertCode`                    | sub-skill: `convert/SKILL.md`                                     |
| `runAssessment`                  | sub-skill: `assessment/SKILL.md`                                  |
| `continueToMigration`            | inline prompt (`next_prompt`) — the post-assessment gate; each answer carries its `then` |
| `configureSnowflakeTarget`       | sub-skill: `setup/configure-snowflake-target.md`                  |
| `configureSourceConnectionTesting` | sub-skill: `setup/configure-source-connection.md` (source-data testing path only) |
| `configureTesting`               | sub-skill: `setup/configure-testing.md`                           |
| `generateTestbed`                | sub-skill: `migrate-objects/baseline-capture/testbed-generator/SKILL.md` (synthetic testing path only) |
| `configureSourceConnectionData`  | sub-skill: `setup/configure-source-connection.md` (data infrastructure path only) |
| `setupDataInfrastructure`        | sub-skill: `data-infrastructure/SKILL.md`                         |
| `dataStrategy`                   | sub-skill: `setup/data-strategy/SKILL.md`                         |

Conversion and assessment come first on purpose: neither needs a Snowflake
target, so a user reaches their assessment report without picking a
connection or database. Git is enabled by default right after the project
directory is confirmed — before dialect and code registration — so milestone
commits can land as each step completes. A fresh directory that is not
already a git repo is initialized on `main` automatically, without asking.
An existing repository stops at `configureGit` until the user confirms
branch and remote settings.

Object migration setup (Snowflake target, testing, data infrastructure) is
gated behind the `continueToMigration` prompt. Answer "Not now" and the
machine finishes at assessment; nothing is persisted for that answer, so the
gate is offered again on the next run. Pass `configure(git_enabled=false)`
(or answer Skip if the `enableGit` prompt still appears, for an existing
repo) to run assessment-only with no repository — milestone commits are skipped.

The `assessment` skill's closing menu asks the same thing the gate asks, so
on "Move on to migration" it submits
`progress_setup(answers={"continue_to_migration": "true"})` instead of a bare
call. A bare call there would put the question a second time.

The testing choice also decides the last step: **synthetic** walks into
`generateTestbed` (synthetic tests need generated data), while
**source-data** ends setup right after `configureTesting`.

If `progress_setup()` returns an unexpected `next_task` not listed above,
surface the raw response to the user and stop — do not invent a skill
path.

## Skipping an optional step

To skip an optional setup step for this run, call
`progress_setup(mode="setup", skip="runAssessment")`. The response
resolves the next step exactly as a normal call would (for the last step,
`completed: true`) — act on it directly. Nothing is persisted, so the step
is offered again later; for a permanent opt-out use
`configure(tasks={"runAssessment": {"enabled": false}})`.

Trust `progress_setup()` / related MCP return values for what is done vs
pending — do not invent completion from chat history.

## Sub-Skills Reference

| Stage | Sub-skill | Location |
|-------|-----------|----------|
| 1 | sql-server-connection | `../connection/sql-server-connection/SKILL.md` |
| 1 | redshift-connection | `../connection/redshift-connection/SKILL.md` |
| 1 | oracle-connection | `../connection/oracle-connection/SKILL.md` |
| 1 | teradata-connection | `../connection/teradata-connection/SKILL.md` |
| 1 | postgresql-connection | `../connection/postgresql-connection/SKILL.md` |
| 1 | db2-connection | `../connection/db2-connection/SKILL.md` |
| 1 | bigquery-connection | `../connection/bigquery-connection/SKILL.md` |
| 1 | snowflake-connection (source and target for validation-only projects) | `../connection/snowflake-connection/SKILL.md` |
| — | midway-entry (existing project with pre-converted code; SQL Server/Redshift only) | `./midway-entry.md` |
| 3 | register-code-units | `../register-code-units/SKILL.md` |
| 4 | convert | `../convert/SKILL.md` |
| 4 | code-conversion-only | `../code-conversion-only/SKILL.md` |
| 5 | snowconvert-assessment | `../assessment/SKILL.md` |
| — | configure-snowflake-target (post-assessment: connection + database) | `./configure-snowflake-target.md` |
| — | configure-testing (post-assessment: source-data vs synthetic) | `./configure-testing.md` |
| — | data-infrastructure-setup | `../data-infrastructure/SKILL.md` |
| — | data-strategy | `./data-strategy/SKILL.md` |
| — | data-migration-setup | `../migrate-objects/actions/data-migration/SKILL.md` |
| — | data-validation-setup | `./data-validation/SKILL.md` |
| — | data-infrastructure-teardown | `../data-infrastructure/teardown/SKILL.md` |
| — | discover-extras (custom assets the engine doesn't generate — FiveTran, SSAS, Oracle PACKAGE, scripts) | `./discover-extras/SKILL.md` |

## Rules

1. **Follow sub-skill instructions** — Complete each sub-skill fully before returning
2. **Confirm transitions** — Ask user before moving to next stage

## On Completion

When the setup machine reaches `setupComplete`, the closing message depends
on how the user answered the `continueToMigration` gate.

**If they chose "Not now"** (no Snowflake target configured) — close out
here without nudging them toward migration:
> **Assessment complete** — connected to <source_type>, <N> objects
> registered, code converted, and your assessment report is ready. Every
> step was committed to git.
>
> Whenever you want to go on to deploying objects to Snowflake, just say
> so — I'll pick up right here and set up the Snowflake target then.

Then ask what else you can help with, and stop. Do **not** load
`../migrate-objects/SKILL.md`.

**If they opted in** and the Snowflake target and testing path are set:
> **Setup complete** — Your migration project is configured: connected to <source_type>, <N> objects registered, code converted, assessment generated, and your Snowflake target (`<snowflake_database>`) and testing path are set. Ready to start migrating objects.
>
> Every step along the way was committed to git. This is a good time
> to share the project with your team — the next phase (object
> migration) is designed to be multi-user, with multiple engineers
> working through waves in parallel.

Then return to the parent migration skill.
