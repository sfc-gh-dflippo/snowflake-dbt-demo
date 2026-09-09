---
name: assessment
description: Analyzes workloads to be migrated to Snowflake using SnowConvert assessment reports. Routes to specialized sub-skills for high-quality assessments. Use this skill when user wants to do an assessment of their code or ETL workload, waves generation, object exclusion, effort estimates, anti-patterns, discovery (SQL Server), sql dynamic and/or ETL analysis (SSIS)
version: 0.1.0
license: Proprietary. See License-Skills for complete terms
---

# Assessment

## On Entry

Tell the user:
> **Migration Assessment** — I'll analyze your converted code to generate a migration plan: dependency waves, object categorization, dynamic SQL patterns, and a summary report. This helps us prioritize what to migrate first.

End-to-end migration assessment. The user only needs to point at the source — this skill detects the project state and, if needed, drives the migration setup (connect → init → register → convert) so that the SnowConvert reports the assessment depends on are produced automatically. The user is **never** asked for CSV paths, registry paths, or output directories.

**One exception:** SQL Server **Discovery** uses Extended Events (`.xel`)
files, which the conversion pipeline does not produce. Step 4 first explains
what Discovery adds, then lets the user skip it, provide `.xel` path(s)
now, or take the capture SQL and provide the files on a later assessment run.
The files stay in place; never copy them into the project.

> "I want to assess my workload" → the user provides a source → assessment runs end-to-end. Nothing else is requested.

## Step 0: Configure Session

Call the `configure` MCP tool with `project_dir` (use the current directory, or ask the user if ambiguous). Assessment needs no Snowflake connection — `scai assessment` runs entirely off the local project — so don't ask for one here; the setup machine asks after assessment, only if the user goes on to object migration. Other settings are filled in by sub-skills as the workflow progresses.

## Step 1: Verify Prerequisites

If you arrived here directly (not through the setup state machine), call `progress_setup()` first. If it returns a `next_task` other than `runAssessment` (or `completed: true` with assessment already done), follow the engine — finish that setup step, then re-enter assessment when `progress_setup()` routes here.

## Step 2: Auto-Detect SnowConvert Outputs

Resolve all inputs from `project_dir`. Do not prompt the user.

| Input | Resolution |
|-------|------------|
| SCAI project root | `project_dir` (contains `.scai/` and the registry — required by `scai assessment waves`) |
| SnowConvert reports dir | `<project_dir>/reports/SnowConvert/` |
| Issues CSV | `<project_dir>/reports/SnowConvert/Issues.*.csv` (latest timestamp) |
| ETL Elements / Issues CSVs | `<project_dir>/reports/SnowConvert/ETL.Elements.*.csv` and `ETL.Issues.*.csv` (only if present — drives whether SSIS analysis is included) |
| Assessment output dir | `<project_dir>/assessment/` (created by `scai assessment waves`; fall back to creating if missing for other sub-skills) |

Selection rules:
- **Wave generation is always driven by `scai assessment waves`** — it reads the registry from the current project folder and writes `<project_dir>/assessment/waves_analysis_*.json`. There is no CSV fallback for wave creation.
- The multi-tab HTML report (`scai assessment report`) takes `--project-dir` (the scai project root) and auto-discovers everything it needs: `registry/`, `reports/`, `assessment/waves_analysis_*.json`, `workload-insights-*.json`, and the exclusion / dynamic-SQL JSONs. The registry is **required** — without it the report cannot enrich the waves JSON (which emits UUIDs) with canonical names, categories, file paths, and conversion status.
- If the registry or reports are missing after a successful-looking convert, re-run `../convert/SKILL.md` once and stop if it still produces nothing.

## Step 3: Confirm Scope (single, short)

Show one compact confirmation that lists what will run. This is the **only** confirmation between source-question and execution.

```
I will run:
1. Waves (dependency analysis + deployment partitioning)
2. Anti-Patterns  (SQL Server only)
3. Effort Estimates  (SQL Server and Redshift only)
4. Dynamic SQL Patterns
5. Discovery  (SQL Server only — capture files are optional, asked next)
6. ETL/SSIS Assessment  (only if present)
7. Informatica Assessment  (only if present)
8. HTML Report

Proceed with all, or pick a subset?
```

Wait for "yes" or a subset selection, then run. Do not re-prompt for files or directories at any later point.

**Note:** "Proceed with all" is **not** the last prompt. The next step (Step 4) collects every input the in-scope sub-skills need so they can run as non-interactive sub-agents. After Step 4 the assessment becomes hands-off until results are surfaced in Step 8.

## Step 4: Gather Sub-Skill Inputs (single batch)

Collect **every** answer the in-scope sub-skills need **before** dispatching anything. Sub-agents run non-interactively. Hold the answers in an in-message `assessment_inputs` block in your working context (do not write it to disk) — it is the source of truth for the context blocks emitted in Step 5.

For sub-skills excluded by the Step 3 scope answer, skip the corresponding inputs and do not dispatch in Step 5.

### 5.1 Waves inputs (always required when waves is in scope)

Ask the three Required User Interactions from `waves-generator/SKILL.md` here, in this order:

1. **Partition size** — "The default wave size is 40-80 objects. Keep the defaults, or set custom min/max?" Record `partition_min_size` (int) and `partition_max_size` (int).
2. **Prioritization** — "Any objects to push into the earliest waves? Provide patterns like `*Payroll*` or `dbo.Customer`, or say no." Record `prioritization_globs` (list of strings; empty if none).
3. **Wave ordering** — "Default is category-based (TABLE → VIEW → FUNCTIONS/PROCEDURES → ETL). Switch to dependency-based?" Record `wave_ordering` (`category` or `dependency`).

### 5.2 Dynamic SQL review (when in scope)

Ask once:

> "Are you interested in Dynamic SQL code analysis? Each occurrence will be reviewed individually — pattern, complexity, migration considerations. (yes / no)"

Map the answer to `dynamic_sql.review_mode`:
- `yes` → `auto-review-all` — generate, then loop and update each occurrence
- `no` → `generate-only` — generate the JSON for report visibility only; no per-occurrence review

### 5.3 ETL/SSIS review (when ETL is detected)

When ETL/SSIS is in scope and `ETL.*.csv` files are present, **always generate** the JSON — it gives the user visibility into their packages: component counts, control flow / data flow DAGs, and a baseline migration view in the report. Do not ask about that step.

Beyond the baseline, ask once whether to run the deeper AI package analysis:

> "I detected SSIS packages in this project. The assessment will give you visibility into them — component counts, control/data flow DAGs, and a baseline migration view in the report.
>
> Optionally, I can run an AI-driven per-package analysis that adds package classification (Ingestion / Transformation / Export / Orchestration / Hybrid), an AI HTML summary, and effort estimates. It takes more time, but runs in the background as a sub-agent in parallel with the other assessments — it doesn't block anything else. Run the AI analysis? (yes / no)"

Map the answer to `etl.review_mode`:
- `yes` → `auto-review-all` — generate, then per-package AI classification + AI HTML summary
- `no` → `generate-only` — generate the JSON for report visibility only; no AI analysis

Capture `etl_replatform_sources_path` from `migration_status` if available (otherwise leave blank for sub-agent auto-detection).

### 5.3b Informatica PowerCenter target (when Informatica is in scope)

When Informatica PowerCenter sources are detected (use MCP `migration_status` to check project config), ask **once**:

> "Which conversion target for Informatica PowerCenter?
> 1. **dbt** — mappings convert to dbt models orchestrated by Snowflake Tasks
> 2. **scripting** — mappings convert to Snowflake stored procedures (Snowflake Scripting)
>
> Choose 1 or 2:"

This prompt is **MANDATORY** — do not skip or default. Record `informatica.target` as `"dbt"` or `"scripting"`.


### 5.4 Object exclusion (no inputs)

No prompts. Note the sub-skill is in scope.

### 5.5 Effort estimate (no inputs)

No prompts. Note the sub-skill is in scope.

### 5.6 Anti-patterns (SQL Server only, no inputs)

No prompts. In scope **only when the project's source dialect is SQL Server** — `scai assessment anti-patterns` self-gates and aborts (error `ASM0024`) on other dialects. For non-SQL-Server projects, treat it as out of scope and synthesize a `"skipped"` result in Step 6.

### 5.7 Discovery (SQL Server only)

In scope **only when the project's source dialect is SQL Server**. The command
self-gates with `ASM0034` on other dialects. For non-SQL-Server projects, ask
nothing here and synthesize a `"skipped"` result in Step 6.

On SQL Server, **always ask** — never search for `.xel` files and never answer
for the user. Only the answer below takes Discovery out of scope.

First say this, as one short paragraph:

> **Discovery** summarizes the SQL activity recorded by a SQL Server Extended Events capture: execution volume, duration mix, statement types, applications and users, long-running executions, and errors. It is not derived from converted source. To include it, give me the local path to the `.xel` file(s) from a capture that records the events this report needs. This is optional — you can skip it, provide the paths now, or take the starter SQL that sets up the capture and provide the files on a later assessment run.

Then ask this. Keep the disclaimer and all three choices in the question:

> Disclaimer: captured Extended Events data, including statement text, is used for reporting only. Statement text is read only to classify query type; it is not stored in the artifact or shown in the report.
>
> How do you want to handle Discovery?
>
> 1. Skip for this run
> 2. I have the `.xel`
> 3. Give me the SQL, I'll provide the files later

Map answers to `workload_insights.mode`: `skip` | `have_extract` | `later`.

**1 — `skip`.** Record empty `input_paths`, paste no SQL, and continue gathering
the remaining inputs.

**2 — `have_extract`.** Ask for one or more absolute `.xel` paths. A folder or
glob is acceptable only when it resolves to the capture rollover files. Any
filename works. Record the resolved absolute files in `input_paths`. Do not
copy, rename, or move them under the project. Do not ask for a database name or
capture duration. If no usable path is supplied, ask for one or let the user
switch to `skip` / `later`; never dispatch with an empty list.

**3 — `later`.** This is `skip` **plus the SQL**. Record empty `input_paths`,
and from here on treat Discovery exactly as if the user had chosen `skip`: it
is out of scope for this run.

Do not ask for a database name or number of days. **In this same turn**, show
the guidance below **verbatim** — both lists, every bullet, with the reason
each setting matters — then paste
`workload-insights/references/create-extended-events-session.sql` unchanged.
Do not summarize it, merge the lists, or drop the explanations: this is the same
review copy the HTML report shows, and the user is about to run this on a
production instance.

The SQL is delivered **now, during input gathering** — never deferred. Do not
add a plan or task step such as "provide the capture SQL", do not schedule it
after the HTML report, and do not mention it again in Step 8 or on completion
beyond the normal `skipped` row. Capture takes days; the assessment must not
model it as pending work.

> Disclaimer: captured Extended Events data, including statement text, is used for reporting only. Statement text is read only to classify query type; it is not stored in the artifact or shown in the report.
>
> **Review the capture before running it.** SQL Server keeps no history of past
> queries, so nothing can be reported until a capture is running. This starter
> script creates a **SQL Server Extended Events** session for one database, but
> leaves it stopped. While it runs, it records each completed user statement
> and stored-procedure call that meets the duration filter — duration, CPU,
> reads, writes, rows, application, and user — plus errors at severity 11 or
> higher. Statement text is used only to classify the query type. Review every
> value, replace `YourDatabase` in all three predicates, and uncomment
> `STATE = START` only when you are ready to begin. The three events
> and their `ACTION` lists must stay or the report loses columns.
>
> **A DBA should own this capture.** Have a DBA set the values, confirm it is
> safe to run on this instance, and start it. Watch the server once it is
> running — CPU, disk space, and waits — and stop the session if anything
> degrades.
>
> This capture uses CPU and disk. It is reasonable on a typical host with the
> defaults below, but it is not free and can compete with the database if the
> settings are too aggressive. Do not switch `EVENT_RETENTION_MODE` to
> `NO_EVENT_LOSS` — that can stall user queries.
>
> **You can change these to fit the capture:**
>
> - **Session name** — default is `WorkloadReport_XE`. Change it if another
>   session already uses that name; keep the same name in the create, start,
>   and stop statements.
> - **Duration threshold** — default is 0.5 seconds
>   (`[duration] >= 500000`, in microseconds). Raise it to write less; lowering
>   it captures more and costs more CPU and disk.
> - **Filters** — default is one database, no system work, no SSMS/telemetry,
>   and errors at severity 11 or higher. Tighten or loosen as needed. Removing
>   the database predicate traces the whole instance and is usually too wide.
>
> **Set these carefully — they affect the database:**
>
> - **`filename`** — replace `<dedicated volume>` with a path on a volume that
>   has space and is not a data or log disk. SQL Server appends its own suffix
>   and `.xel`.
> - **`max_file_size`** (200 MB) and **`max_rollover_files`** (5) — together
>   they cap disk at 1 GB. Confirm more than that is free before starting.
>   Smaller caps use less disk; larger caps keep more history.
> - **`MAX_MEMORY`** (8,192 KB) — how much RAM the session may hold. Raising it
>   buffers more events; leaving it low keeps it from competing with the buffer
>   pool.
> - **`MAX_DISPATCH_LATENCY`** (30 seconds) — how soon events flush to disk.
>   Lower it to write sooner; higher it to batch more.
> - **`STARTUP_STATE`** (OFF) — the session does not return after a service
>   restart. Set it ON only if you want it to resume automatically, and still
>   stop it when the capture window ends.
> - **`MEMORY_PARTITION_MODE`** — not set, which is right for a typical host.
>   On a busy many-core server, set `PER_CPU` (commented in the script) to
>   reduce contention when many queries finish at once, and raise `MAX_MEMORY`
>   to 16–32 MB first. Leaving 8,192 KB with `PER_CPU` drops more events.

After the SQL, tell the user:

- `CREATE` leaves the session stopped. Uncomment and run the commented
  `STATE = START` statement when capture should begin; nothing is recorded
  before that.
- Leave it running under representative traffic. Around 30 days is a useful
  target, but a shorter window still works.
- Copy every rollover `.xel` file, then **stop the session** with the
  commented `STATE = STOP` statement. Leaving it running continues to use
  CPU and disk.
- Re-run assessment later, choose **I have the `.xel`**, and provide the files.
- The current assessment continues now and does not wait for the capture.

Do not dispatch `workload-insights` in `later` mode. Continue straight to the
next input in Step 4, then dispatch the remaining sub-skills in Step 5 as
usual. In Step 6 synthesize the `"skipped"` result described in §6.6 so Step 8 has its
row, and generate the HTML report in Step 7 exactly as for `skip` — the
Discovery tab renders its empty state.

### 5.8 Snapshot the inputs

Lay out the resolved values in your working context like this (text only — do not write to disk):

```
assessment_inputs:
  project_dir: <abs>
  output_dir_assessment: <project_dir>/assessment
  waves:
    partition_min_size: <int>
    partition_max_size: <int>
    prioritization_globs: [<glob>, ...]
    wave_ordering: category | dependency
  exclusion: {}
  effort_estimate: {}
  anti_patterns: {}
  workload_insights:
    mode: have_extract | skip | later
    input_paths: [<abs .xel path>, ...]
  dynamic_sql:
    review_mode: generate-only | auto-review-all | skip
    output_dir: <project_dir>/assessment/json
  etl:
    review_mode: generate-only | auto-review-all | skip
    output_dir: <project_dir>/assessment/ssis
    etl_replatform_sources_path: <abs or empty>
  informatica:
    target: dbt | scripting
```

After Step 4 completes, do **not** prompt the user again until Step 8.

## Step 5: Parallel Sub-Agent Dispatch

In a **single message**, fire one Task tool call per in-scope sub-skill. Do not dispatch sequentially. After dispatching, end your turn — sub-agents run on their own and return results back to this conversation.

Each Task call uses the prompt template for its sub-skill below. Substitute every `<placeholder>` with the value from the `assessment_inputs` snapshot in Step 4. Use absolute paths only.

> **Important:** Do **not** dispatch any sub-skill that is out of scope (per Step 3) or whose `review_mode` is `skip`. The parent synthesizes a `"skipped"` result for those in Step 6.

### 6.1 waves-runner prompt

```
Read and follow plugin/skills/migration/assessment/waves-generator/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>
- partition_min_size: <int>
- partition_max_size: <int>
- prioritization_globs: <list or empty>
- wave_ordering: category | dependency
- output_dir: <project_dir>/assessment

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for waves generation.
2. Run `scai assessment waves` from <project_dir>, passing every required
   input as a flag derived from partition_min_size, partition_max_size,
   prioritization_globs (one --prioritize per glob), and wave_ordering
   (--no-category-waves only when wave_ordering = dependency). If the CLI
   still requests TTY input, fail fast and report the missing flag — do not
   block on stdin.
3. Locate the timestamped waves_analysis_*.json the CLI wrote.

Report back JSON only:
{
  "sub_skill": "waves-generator",
  "status": "ok" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line counts: partitions, sccs, objects>",
  "error": "<message>" | null
}
```

### 6.2 exclusion-runner prompt

```
Read and follow plugin/skills/migration/assessment/object_exclusion_detection/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for object exclusion.
2. Run `scai assessment object-exclusion` from <project_dir>.
3. Locate the timestamped object_exclusion_analysis_*.json the CLI wrote under <project_dir>/artifacts/assessment.

Report back JSON only:
{
  "sub_skill": "object-exclusion-detection",
  "status": "ok" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line counts: temp/staging, deprecated, testing, duplicates>",
  "error": "<message>" | null
}
```

### 6.2b effort-estimate-runner prompt

```
Read and follow plugin/skills/migration/assessment/effort-estimate/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for effort estimate analysis.
2. Run `scai assessment effort-estimate` from <project_dir>.
3. Locate the timestamped effort-estimates-*.json the CLI wrote under
   <project_dir>/artifacts/assessment/. If the CLI aborts because the
   source dialect is unsupported (error ASM0031), report status "skipped"
   with that reason — do NOT treat it as an error.

Report back JSON only:
{
  "sub_skill": "effort-estimate",
  "status": "ok" | "skipped" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line: ddl_objects, total_estimated_hours>",
  "error": "<message>" | null
}
```

### 6.3 dynamic-sql-runner prompt

```
Read and follow plugin/skills/migration/assessment/analyzing-sql-dynamic-patterns/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>
- output_dir: <project_dir>/assessment/json
- review_mode: generate-only | auto-review-all

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for dynamic-SQL analysis.
2. Run:
     scai assessment sql-dynamic generate \
       --project-dir <project_dir> \
       --output <output_dir>/sql_dynamic_analysis.json
3. If review_mode = auto-review-all, follow the skill's per-occurrence
   review loop until `stats` shows zero PENDING records. Each update is a
   single-record call with its own analysis (no batching, no copy/paste).
4. Locate the analysis JSON.

Report back JSON only:
{
  "sub_skill": "analyzing-sql-dynamic-patterns",
  "status": "ok" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line: total occurrences, REVIEWED, PENDING>",
  "error": "<message>" | null
}
```

### 6.4 etl-runner prompt

```
Read and follow plugin/skills/migration/assessment/etl-assessment/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>
- output_dir: <project_dir>/assessment/ssis
- etl_replatform_sources_path: <abs or empty>
- review_mode: generate-only | auto-review-all

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for SSIS analysis.
2. Locate ETL.Elements.*.csv and ETL.Issues.*.csv under
   <project_dir>/reports/SnowConvert/. If etl_replatform_sources_path is
   empty, auto-detect per the skill's Step 1.
3. Run (from the project root):
     scai assessment etl generate
   This writes etl_assessment_analysis_<timestamp>.json and dag_model_<timestamp>.json
   to <output_dir>.
4. Render DAG HTMLs from the newest dag_model_*.json (conditional, per the skill's Step 2).
5. If review_mode = auto-review-all, follow the skill's Step 3 + Step 4
   to classify each package and produce ai_ssis_summary.html
6. Locate etl_assessment_analysis_<timestamp>.json under <output_dir>.

Report back JSON only:
{
  "sub_skill": "etl-assessment",
  "status": "ok" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line: total packages, classified, pending>",
  "error": "<message>" | null
}
```

### 6.4b informatica-runner prompt

```
Read and follow plugin/skills/migration/assessment/informatica-assessment/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>
- output_dir: <project_dir>/assessment/informatica
- informatica_target: dbt | scripting
- review_mode: generate-only | auto-review-all

Steps:
1. Call configure() with project_dir above and etl_informatica_target=<informatica_target>.
   Snowflake credentials are not needed for Informatica analysis.
2. Locate ETL.Elements.*.csv and ETL.Issues.*.csv under
   <project_dir>/reports/SnowConvert/.
3. Run the skill's Step 2 (generate JSON) and Step 3 (analyze workflows)
   following informatica-assessment/SKILL.md instructions.
   Use informatica_target to frame all analysis in the correct mode.
4. If review_mode = auto-review-all, analyze each workflow per Step 3
   and produce the AI summary per Step 4.
5. Locate informatica_assessment_analysis_<timestamp>.json under <output_dir>.

Report back JSON only:
{
  "sub_skill": "informatica-assessment",
  "status": "ok" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line: total workflows, classified, pending, target=dbt|scripting>",
  "error": "<message>" | null
}
```

### 6.5 anti-patterns-runner prompt

Dispatch **only when the project's source dialect is SQL Server** (otherwise synthesize a `"skipped"` result in Step 6).

```
Read and follow plugin/skills/migration/assessment/anti-patterns/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>

Steps:
1. Call configure() with project_dir above. Snowflake credentials are not needed for anti-patterns analysis.
2. Run `scai assessment anti-patterns` from <project_dir>. It writes
   artifacts/assessment/anti-patterns-<timestamp>.json under the project root.
   If the CLI aborts because the project is not SQL Server (error ASM0024),
   report status "skipped" with that reason — do NOT treat it as an error.
3. Locate the timestamped anti-patterns-*.json under
   <project_dir>/artifacts/assessment/.

Report back JSON only:
{
  "sub_skill": "anti-patterns",
  "status": "ok" | "skipped" | "error",
  "output_json": "<abs_path>" | null,
  "summary": "<one-line: buckets, distinct flags, code units affected>",
  "error": "<message>" | null
}
```

### 6.6 workload-insights-runner prompt

Dispatch **only** when all three hold: the project's source dialect is SQL
Server, `workload_insights.mode == have_extract`, and
`workload_insights.input_paths` is non-empty. In every other case (other
dialect, `skip`, `later`, or no paths), do not dispatch; synthesize a
`"skipped"` result in Step 6. For `later`, use
`summary: "capture SQL provided; re-run assessment with the .xel files"` — the
SQL was already delivered in Step 4, so this is a closed row, not pending work.
For `skip`, use `summary: "skipped by user"`.

```
Read and follow plugin/skills/migration/assessment/workload-insights/SKILL.md.
You are running in sub-agent mode — do NOT ask the user any questions.

Context (from parent):
- project_dir: <abs_path>
- input_paths: <abs .xel paths>

Steps:
1. Call configure() with project_dir. Snowflake credentials are not needed.
2. Run `scai assessment workload-insights --input <path> [--input <path>…]`
   from project_dir, adding exactly one `--input <path>` per context path.
3. Locate the timestamped `workload-insights-*.json` under
   `<project_dir>/artifacts/assessment/`.
4. Return JSON only `{sub_skill, status, output_json, summary, error}`.
   `ASM0034` means `skipped`. Do not rewrite any JSON fields and do not copy
   the `.xel` files into the project.
```

A large-file or long-running parse message on stdout is not a failure. Exit
code 0 and a written artifact means `"ok"`; include the message in `summary`.

### 6.7 Common rules for every dispatch

1. **One message, multiple Task calls.** Send all in-scope dispatches in a single tool-use turn so the framework can run them in parallel.
2. **Absolute paths only** in every context block.
3. **Sub-agent calls `configure()` itself** — do not assume MCP state is inherited.
4. **Each sub-agent writes only its own output JSON** — no edits to the registry, source SQL, or other sub-agents' artifacts.
5. **JSON return only** — free-form text in the report is harder to consume reliably.

End your turn after the dispatch message.

## Step 6: Wait + Verify Outputs

Each Task return contains a single JSON object: `{sub_skill, status, output_json, summary, error}`. Collect all returns. **A failing sub-agent does not block the others.**

For every dispatched sub-skill, validate:

| Check | Action on failure |
|---|---|
| Task returned a JSON object | Mark sub-skill as failed with `error: "no response"` |
| `status == "ok"` (or `"skipped"` for skip dispatches) | Mark as failed with the returned `error` text |
| `output_json` path exists on disk | Mark as failed with `error: "claimed JSON not found"` |
| `output_json` file is non-empty (size > 0) | Mark as failed with `error: "JSON empty"` (do NOT schema-validate) |

For sub-skills excluded by the Step 3 scope (or set to `review_mode: skip` in Step 4), synthesize `{status: "skipped", output_json: null, summary: "<reason>"}` so Step 8 has a complete row for every sub-skill.

Build a `results` table indexed by sub-skill name (`waves-generator`, `object-exclusion-detection`, `effort-estimate`, `anti-patterns`, `analyzing-sql-dynamic-patterns`, `workload-insights`, `etl-assessment`, `informatica-assessment`). Carry it into Step 7 and Step 8.

## Step 7: Generate Unified HTML Report

**First, resolve the report name.** A generated report gets shared outside the team, so it has to
say which customer or project it belongs to. Check whether this project already has a name:

```bash
uv run --project plugin/skills/migration/assessment \
  python plugin/skills/migration/assessment/scripts/metadata_tools.py \
  --project-dir "<project_dir>" --show-assessment-name
```

It prints three lines:

```
assessmentName: (unset)
projectName:    beverage
resolved:       beverage
```

- `assessmentName` is anything other than `(unset)` → **do not ask.** Go straight to the generator.
- Otherwise ask once, offering `projectName` as the default:

  > **What would you like to name this assessment report?** This will be visible in the report
  > (e.g., Customer or Project name) `[default: beverage]`

  Then store the answer:

```bash
uv run --project plugin/skills/migration/assessment \
  python plugin/skills/migration/assessment/scripts/metadata_tools.py \
  --project-dir "<project_dir>" --set-assessment-name "<answer>"
```

**Name rules:**
1. If `--set-assessment-name` exits non-zero, warn and continue anyway — the report still renders
   from `projectName`.

**Then run `scai assessment report`** with `--project-dir` and **pass flags for ssis or informatica if they apply** from the `results` table:

```bash
scai assessment report \
  --project-dir "<project_dir>" \
  --output "<project_dir>/assessment/multi_report.html" \
  [--ssis-json "<path>" if etl-assessment succeeded] \
  [--informatica-json "<path>" if informatica-assessment succeeded]
```

**Rules:**
1. Always pass `--project-dir` — it auto-discovers waves, exclusion, dynamic-SQL, anti-patterns, `workload-insights` JSON, registry, and reports directories
2. **Explicitly pass `--ssis-json`** if the `etl-assessment` sub-skill in the `results` table has `status == "ok"` and a valid `output_json` path
3. **Explicitly pass `--informatica-json`** if the `informatica-assessment` sub-skill in the `results` table has `status == "ok"` and a valid `output_json` path
4. Do **not** write custom HTML

If the report command fails, record the failure and proceed to Step 8 anyway — the user still needs the status table.

## Step 8: Surface Results + Retry

Print a status table from the `results` collected in Step 6, one line per sub-skill, in this order: `waves-generator`, `object-exclusion-detection`, `effort-estimate`, `anti-patterns`, `analyzing-sql-dynamic-patterns`, `workload-insights`, `etl-assessment`.

Format:

```
waves-generator                  ok      <output_json basename>   (<summary>)
object-exclusion-detection       ok      <output_json basename>   (<summary>)
effort-estimate                  ok      <output_json basename>   (<summary>)
anti-patterns                    ok      <output_json basename>   (<summary>)
analyzing-sql-dynamic-patterns   FAIL    <error message>
workload-insights                skip    <reason>
etl-assessment                   skip    <reason>

Multi-tab report:  <abs path to multi_report.html>   (or "FAILED — see error above")
```

If any sub-skill failed, ask:

> "Retry failed sub-skills? Successful JSONs will be reused — only the failed runs re-fire. (yes / no)"

On `yes`: re-fire **only** the failed sub-skills using the same single-message Task fan-out as Step 5. Reuse the `assessment_inputs` snapshot from Step 4 — do not re-prompt the user. After the retries return, re-run Step 6 verification, regenerate the report (Step 7), and re-print the status table.

Each retry produces a fresh timestamped JSON; old runs are not deleted (this supports diffs across runs).

After retries complete (or if no retry was requested), proceed to [On Completion](#on-completion).

## Prerequisites

Handled automatically by Steps 0–3. The skill assumes:
- `scai` CLI is installed and available on `PATH` — used by `setup`, `convert`, and `scai assessment waves`.
- Python 3.11+ and `uv` are available for the HTML report generator and the remaining assessment scripts (install `uv` per https://docs.astral.sh/uv/getting-started/installation/ — `brew install uv` on macOS, `winget install astral-sh.uv` on Windows, or `pip install uv` anywhere).

## Example Prompts

Help users get the best results by understanding what they can ask:

### Starting an Assessment
- "Run a quick assessment of my migration"
- "I need a comprehensive assessment with all analyses"
- "Generate deployment waves for my SQL migration"

### Customizing Wave Generation
- "I want a maximum of N objects per wave"
- "Create smaller waves with 20-30 objects each"
- "Prioritize all Payroll-related objects in Wave 1"
- "Put all Customer* objects in the earliest waves"
- "Use dependency-based ordering instead of category-based"

### Iterative Refinement (After Initial Results)
- "Show me which objects have circular dependencies"
- "Regenerate waves with smaller batch sizes"
- "What objects are blocking the migration?"

### Working with Reports
- "Generate the HTML report"
- "Show me a summary of the assessment"
- "How many objects are flagged for exclusion?"
- "What's the breakdown by schema?"

### Specific Analyses
- "Identify temporary and staging objects"
- "Find deprecated objects that can be excluded"
- "Analyze Dynamic SQL patterns in my codebase"
- "Assess my SSIS packages for migration complexity"

## Critical Rules

**Follow instructions of each sub-skill:** Read the sub-skill first before executing any command.

**NO CUSTOM SCRIPTS:** Only execute existing scripts within sub-skills. Do not create automation, batch processing tools, or bash loops.

**🚫 NEVER WRITE CUSTOM HTML REPORTS:** When delivering results to users, you MUST use `scai assessment report`. Do NOT write HTML manually under any circumstances. See [Report Generation](#report-generation) section.

**USER CONFIRMATION:** Stop at mandatory checkpoints in sub-skills for user input.

**DATA-DRIVEN:** All assessments based on SnowConvert registry (JSON), CSV outputs and source code.

## Intent Detection & Routing

Detect user intent and load the appropriate sub-skill:

**Deployment Waves** - Analyze dependencies and create deployment sequence:
- Triggers: "deployment waves", "migration waves", "dependency analysis", "deployment sequence", "wave planning"
- Load: `waves-generator/SKILL.md`

**Object Exclusion** - Identify objects to exclude from migration:
- Triggers: "temporary objects", "staging objects", "deprecated", "exclude objects", "test objects", "cleanup"
- Load: `object_exclusion_detection/SKILL.md`

**Effort Estimates** - Generate migration effort estimates from SnowConvert reports:
- Triggers: "effort estimate", "effort estimates", "migration effort", "FDE hours", "how long will migration take"
- Load: `effort-estimate/SKILL.md`

**Anti-Patterns** - Surface migration converns from existing SnowConvert findings (SQL Server only):
- Triggers: "anti-patterns", "anti patterns", "risk analysis", "performance risks", "collation risks", "semantic risks", "architecture blockers"
- Load: `anti-patterns/SKILL.md`

**Dynamic SQL Analysis** - Classify and score Dynamic SQL patterns:
- Triggers: "dynamic sql", "sql dynamic patterns"
- Supports: SQL Server, Redshift, Oracle, and Teradata migrations
- Load: `analyzing-sql-dynamic-patterns/SKILL.md`

**Discovery** - Summarize SQL Server activity recorded by Extended Events:
- Triggers: "discovery", "workload insights", "query logs", "extended events", "xel"
- Needs one or more `.xel` files produced by the starter capture session. No
  files yet → route through this parent skill's Step 4 §5.7 so it can offer
  skip / files / later and show the review guidance and session SQL.
- Load `workload-insights/SKILL.md` only after §5.7 has collected non-empty
  `.xel` paths and the runner is dispatched. The sub-skill is non-interactive.

**ETL/SSIS Assessment** - Analyze SSIS packages for migration complexity:
- Triggers: "ssis", "etl packages", "ssis analysis"
- Load: `etl-assessment/SKILL.md`

**Informatica Power Center Assessment** - Analyze Informatica workflows/mappings for migration complexity:
- Triggers: "informatica", "power center", "powercenter", "informatica assessment", "informatica analysis"
- Load: `informatica-assessment/SKILL.md`

**Data Migration & Validation readiness** - Explain how the workload's data moves to Snowflake and how it gets validated:
- Triggers: "data migration", "data validation", "move the data", "data type coverage", "unsupported types", "table inventory", "validation divergence", "topology"
- No sub-skill to load and no `scai assessment` command: the multi-report's **Data Migration & Validation** tab already answers this. It is computed from the Code Unit Registry by `scripts/snowconvert_reports/data_migration_readiness.py` (with `data_types_scan.py` for types found in captured DDL and `type_coverage.py` for per-dialect coverage), and rendered by `scripts/data_migration_report/`.
- Reviewed inventory SQL exists only for SQL Server and Redshift (`scripts/data_migration_report/sql/`). Other dialects get a gather checklist — do not invent queries for them.

**Testing readiness** - Explain what can be tested today and what each object still needs first:
- Triggers: "testing", "test readiness", "can I test", "output testing", "what's ready to test", "testing ladder"
- No sub-skill to load and no `scai assessment` command: the multi-report's **Testing** tab already answers this. It is computed from the Code Unit Registry by `scripts/snowconvert_reports/testing_readiness.py` and rendered by `scripts/testing_report/`.
- Both readiness ladders state a no-source-code precondition. ETL units terminate at `stabilization`, all other code units at `testing` — never read `testing.status` for an ETL unit.

**Multiple Assessments** - Load all applicable sub-skills if request requires comprehensive analysis.

## Running Scripts
When running any scripts in any of the above skills, make sure to do all of the following:

- **Wave generation** is executed via `scai assessment waves`. It must be run from inside the SCAI project directory so that it can read the registry.
- **Multi-tab HTML report** is executed via `scai assessment report`.
- **All other Python scripts** in this skill and its sub-skills (ETL analysis, etc.) must be run with `uv run --project <DIRECTORY THIS SKILL.md file is in> python <DIRECTORY THIS SKILL.md file is in>/scripts/script_name.py`.
- Do not `cd` into another directory to run Python scripts, but run them from whatever directory you're already in. When `scai assessment waves` needs the project directory, `cd` into it only for that single invocation.

**WHY:** This maintains your current working context and prevents path confusion. When using `uv run --project`, you must provide absolute paths for BOTH the `--project` flag AND the script itself. Just run the script the way the skill says. Do not question it by running --help or reading the script.

<!-- DEPRECATED in favor of Steps 5-9 (sub-agent dispatch). Will be removed one release after sub-agent rollout stabilizes. See dev/assessment-subagent-dispatch-design.md §11.2 Phase 3.

## Assessment Integration

### Complete Migration Assessment Workflow

The user has already confirmed scope in **Step 4**. Do **not** re-prompt for confirmation here — execute the agreed sequence directly.

**Sequence:**

1. **Waves Generation** (First)
   - **MANDATORY:** Load `waves-generator/SKILL.md` and complete its **Required User Interactions** (partition size, prioritization, wave-ordering strategy) before running the command. These prompts are required even on the end-to-end path — do **not** skip them.
   - Then run `scai assessment waves` from inside the SCAI project directory, passing `--min-size`, `--max-size`, `--prioritize`, `--no-category-waves` derived from the user's answers.
   - The command builds the dependency graph from the registry, validates §15 invariants, and writes `<project_dir>/assessment/waves_analysis_<timestamp>.json`
   - Generate wave-based migration plan

2. **Object Exclusion Analysis** (Second)
   - Identify objects that don't need migration
   - Reduce scope before dependency analysis
   - Generate cleanup recommendations

3. **Dynamic SQL Pattern Analysis** (Third)
   - Classify Dynamic SQL patterns
   - Identify migration complexity and blockers

4. **ETL/SSIS Assessment** (Fourth - if applicable)
   - Analyze SSIS packages individually
   - Understand control flow and data flow pipelines
   - Classify packages and estimate migration effort

5. **Generate Multi-Tab Report** (FINAL - REQUIRED)
   - Use `scai assessment report` - see [Report Generation](#report-generation) section
   - Pass all available JSON outputs from previous steps
   - 🚫 Do NOT write custom HTML - the script handles all formatting

-->

## Tools

### `scai assessment report`

**Description**: Generates unified multi-tab HTML report combining Object Exclusion, Dynamic SQL Analysis, Waves, and SSIS Assessment reports.

**Location**: `scai assessment report`

**When to use**: After completing any requested assessment(s) (1, 2, 3, or all) to deliver results in a consistent format, or whenever the user requests a combined HTML report.

<!-- DEPRECATED in favor of Steps 5-9 (sub-agent dispatch). Will be removed one release after sub-agent rollout stabilizes. See dev/assessment-subagent-dispatch-design.md §11.2 Phase 3.

## Completing the Assessment Analysis

### ⚠️ MANDATORY STOPPING POINT: After Initial Assessment

After generating the initial assessment (Object Exclusion, Dynamic SQL JSON, Waves, SSIS), you **MUST** ask the user about completing each analysis that has pending items:

#### Dynamic SQL Analysis Completion

```
Assessment data has been generated. The Dynamic SQL analysis contains X occurrences 
that are currently in PENDING status and need individual review.

Would you like to complete the Dynamic SQL analysis?
- This involves reviewing each Dynamic SQL occurrence individually
- Each occurrence will be classified, scored for complexity, and documented
- Estimated time: varies based on occurrence count and code complexity

Options:
1. Yes - Complete the full analysis (review all Dynamic SQL occurrences)
2. No - Stop here with the current data (report will show PENDING status)
```

**If user selects Yes:**
- Load the `analyzing-sql-dynamic-patterns/SKILL.md` sub-skill
- Follow the workflow to review each occurrence
- Update each record with: status=REVIEWED, category, complexity, notes
- Continue until `stats` command shows 0 PENDING records
- Then proceed to the next analysis or report generation

**If user selects No:**
- Report will show Dynamic SQL occurrences with PENDING status
- User can complete the analysis later

#### SSIS/ETL Analysis Completion

If SSIS packages are present, also ask:

```
The SSIS/ETL analysis contains X packages that are currently unclassified 
and need individual review.

Would you like to complete the SSIS analysis?
- This involves reviewing each SSIS package individually
- Each package will be classified (Ingestion, Transformation, Export, etc.)
- AI analysis and migration effort estimates will be documented

Options:
1. Yes - Complete the full SSIS analysis (review all packages)
2. No - Stop here with the current data (report will show unclassified packages)
```

**If user selects Yes:**
- Load the `etl-assessment/SKILL.md` sub-skill
- Use `pending` command to list unclassified packages
- Use `package <path>` to view package details
- Use `update <path> --ai-status DONE --classification <type> --ai-analysis "<notes>" --effort <hours>` to classify each package
- Classification options: Ingestion, Transformation, Export, Orchestration, Hybrid
- Continue until `stats` command shows "No pending packages found"
- Then proceed to report generation

**If user selects No:**
- Report will show SSIS packages as unclassified
- User can complete the analysis later

**IMPORTANT:** Do NOT skip these checkpoints. The assessment is not complete until all Dynamic SQL occurrences AND all SSIS packages have been reviewed OR the user explicitly chooses to defer each.

-->

## Report Generation

<!-- DEPRECATED in favor of Steps 5-9 (sub-agent dispatch). Will be removed one release after sub-agent rollout stabilizes. See dev/assessment-subagent-dispatch-design.md §11.2 Phase 3.

### ⚠️ CRITICAL: Multi-Tab HTML Report Generator

**⚠️ MANDATORY: Check for Incomplete Analysis Before Report Generation**

Before generating the report, you **MUST** check for incomplete analysis and warn the user:

1. **Check Dynamic SQL status:**
   ```bash
   scai assessment sql-dynamic stats <path/to/sql_dynamic_analysis.json>
   ```

2. **Check SSIS status** using the scai assessment etl command:
   ```bash
   scai assessment etl stats
   ```
   
   Note: The `stats` command reads the JSON produced by `scai assessment etl generate` and auto-detects the file from project context.

**If there are PENDING Dynamic SQL records OR unclassified SSIS packages**, present this warning:

```
⚠️ WARNING: Incomplete Analysis Detected

The assessment contains unanalyzed items:
- Dynamic SQL: X of Y occurrences are PENDING (not reviewed)
- SSIS/ETL: X of Y packages are unclassified

Generating the report now will show these items as incomplete/unanalyzed.

Options:
1. Generate report anyway (items will show as PENDING/Unclassified)
2. Complete the analysis first (recommended for final deliverables)

Which option would you like?
```

Wait for user response before proceeding.

**⚠️ MANDATORY STOPPING POINT**: After checking analysis status, confirm with user:

```
I will generate a multi-tab HTML report including:
- Object Exclusion Report (if available)
- Dynamic SQL Analysis Report (if available) [X/Y reviewed]
- Waves Deployment Report (if available)
- SSIS Assessment Report (if available) [X/Y classified]

Output file size: typically 5-10MB due to interactive content.

Proceed with report generation? (Yes/No)
```

Wait for approval.

-->

**MANDATORY:** When users request an assessment report (even if it’s only one sub-assessment), a migration report, or a combined HTML report—or when you have completed the requested assessment(s) and are ready to deliver results—you **MUST** use `scai assessment report`. This is the **ONLY** approved method for generating consolidated assessment reports.

**DO NOT:**
- Write custom HTML reports manually
- Use individual sub-skill report generators in isolation
- Create new report generation scripts

**Usage (recommended — single `--project-dir` argument):**
```bash
scai assessment report \
  --project-dir "path/to/<projectRoot>" \
  --output "path/to/<projectRoot>/assessment/multi_report.html"
```

When `--project-dir` is provided, the command auto-discovers:

- `<projectRoot>/registry/` — registry JSONs (REQUIRED for object enrichment: names, categories, files, status, missing-deps, direct dep counts)
- `<projectRoot>/reports/` — SnowConvert CSVs (for EWI/FDM/PRF counts and severity)
- `<projectRoot>/artifacts/assessment/object_exclusion_analysis_*.json` — exclusion JSON (latest timestamp)
- `<projectRoot>/artifacts/assessment/workload-insights-*.json` — Discovery JSON (latest timestamp)
- `<projectRoot>/assessment/json/sql_dynamic_analysis.json` — dynamic-SQL JSON
- `<projectRoot>/assessment/waves_analysis_*.json` — waves JSON (latest timestamp)

Explicit per-source flags (below) override auto-discovery. The individual flags are only needed when you want to mix-and-match sources from non-standard locations.

**Usage with explicit paths (advanced):**
```bash
scai assessment report \
  --project-dir "path/to/<projectRoot>" \
  --waves-json "path/to/waves_analysis_TIMESTAMP.json" \
  --exclusion-json "path/to/object_exclusion.json" \
  --dynamic-sql-json "path/to/sql_dynamic_analysis.json" \
  --workload-insights-json "path/to/workload-insights-TIMESTAMP.json" \
  --snowconvert-reports-dir "path/to/reports" \
  --ssis-json "path/to/ssis/etl_assessment_analysis.json" \
  --output "path/to/multi_report.html"
```

**IMPORTANT:** Always pass `--project-dir` even when providing explicit flags — the registry at `<projectRoot>/registry/` is required to enrich the waves JSON (which now emits UUIDs; canonical names, categories, file paths, and status come from the registry). Without `--project-dir` (or an equivalent `--registry-dir`), the dependencies table will show UUIDs and every row will have category "UNKNOWN".

**Parameters:**
- `--project-dir` **(recommended)**: Path to the scai project root. Auto-discovers registry, SnowConvert reports, and assessment artifacts. Use this alone in the common case.
- `--waves-json`: Path to waves analysis JSON file (output from `scai assessment waves`, e.g. `waves_analysis_<timestamp>.json`). Auto-discovered from `<projectRoot>/assessment/` when `--project-dir` is provided.
- `--registry-dir`: Path to SnowConvert registry directory containing `*.json` entries. Auto-discovered from `<projectRoot>/registry/` when `--project-dir` is provided.
- `--exclusion-json`: Path to object exclusion JSON file. Auto-discovered.
- `--dynamic-sql-json`: Path to dynamic SQL analysis JSON file. Auto-discovered.
- `--workload-insights-json`: Path to the Discovery JSON (`workload-insights-*.json`) produced from
  Extended Events. Auto-discovered from `<projectRoot>/artifacts/assessment/`.
- `--snowconvert-reports-dir`: Path to SnowConvert Reports directory containing `TopLevelCodeUnits.*.csv` and `ObjectReferences.*.csv`. Auto-discovered.
- `--ssis-json`: Path to SSIS assessment JSON file (etl_assessment_analysis.json from ETL assessment). **MUST be explicitly passed when the etl-assessment sub-skill succeeds.**
- `--informatica-json`: Path to Informatica Power Center assessment JSON file (informatica_assessment_analysis.json from Informatica assessment). **MUST be explicitly passed when the informatica-assessment sub-skill succeeds.**
- `--output`: Output HTML file path (required)

**Note:** At least one data source parameter must be provided. If only partial assessment was completed, provide only the available data sources.

**SSIS Report Generation:** When SSIS packages are analyzed using the ETL assessment sub-skill, you **MUST explicitly pass `--ssis-json`** with the path to `etl_assessment_analysis.json` returned by the sub-skill in Step 7.

**Informatica Report Generation:** When Informatica workflows are analyzed using the Informatica assessment sub-skill, you **MUST explicitly pass `--informatica-json`** with the path to `informatica_assessment_analysis.json` returned by the sub-skill in Step 7.

## Report Styling

When generating HTML reports, see `STYLES.md` for styling specifications.

## Success Criteria

An assessment is complete when:
- All requested analyses have completed without errors
- For Dynamic SQL: All occurrences have status `REVIEWED` (no `PENDING` records)
- Reports generated successfully with all requested data sources ** using `scai assessment report` (NOT custom HTML) **
- User has reviewed and approved findings

### Pre-Completion Checklist

Before marking assessment as complete, verify:

```
□ Did I use `scai assessment report` for the final report?
□ Did I pass all available JSON files to the command?
□ Did I avoid writing any custom HTML?
```

If any answer is "No", go back and use the correct script.

## Sub-Skill Documentation

- `waves-generator/SKILL.md` - Algorithm details, partition creation
- `object_exclusion_detection/SKILL.md` - Pattern definitions, naming conventions
- `effort-estimate/SKILL.md` - Complexity-banded effort hours from SnowConvert reports (SQL Server, Redshift)
- `anti-patterns/SKILL.md` - Curated SnowConvert issue-code catalog → customer-facing risk buckets (SQL Server only)
- `workload-insights/SKILL.md` - Extended Events `.xel` files → captured
  workload volume, duration mix, apps/users, long-running executions, and
  errors (SQL Server only); `references/` holds the starter session SQL the
  parent pastes.
- `analyzing-sql-dynamic-patterns/SKILL.md` - Pattern classification, complexity scoring
- `etl-assessment/SKILL.md` - SSIS package analysis, control flow, data flow pipelines

The **Data Migration & Validation** and **Testing** tabs have no sub-skill and nothing to dispatch: both are computed inside the report generator from the `--registry-dir` it already requires, so they render in every report without a runner, a CLI command, or an artifact of their own. Their logic lives in `scripts/snowconvert_reports/{data_migration_readiness,data_types_scan,type_coverage,testing_readiness,conversion_status}.py`; their customer-facing copy lives in `scripts/data_migration_report/content.py` and `scripts/testing_report/content.py`, which are the files to read (or change) when answering a wording question.

## On Completion

Present the closing message with: **opening line** (`migration_status.in_scope` objects in `wave_count` waves), **summary table** (Register, Convert, ETL conversion, Waves, Object exclusion, Dynamic SQL, SSIS/Informatica analysis, Missing objects — pull from `migration_status` and Code Unit Registry), **key findings** (2–4 bullets interpreting the data: heavy staging footprint ≥30%, unresolved external refs, conversion friction, ETL risk, circular dependencies — only when triggers fire), **report path** (platform-specific open command for `<project_dir>/assessment/multi_report.html`), and **next-steps menu**:

> What would you like to do?
> 1. **Review the report** — open HTML or ask any questions
> 2. **Modify the assessment** — re-run with changed parameters
> 3. **Move on to migration setup** — set up the Snowflake target, testing configuration, and data infrastructure setup

Mark option **(1)** as `(recommended)` when `missing > 0`, otherwise **(3)**. Wait for response.

If `configure` reported a dashboard URL at session start, add one line before the menu:
> The dashboard at `<url>` shows the same picture live as you migrate.

Skip it if no URL came back (the user opted out, or the port was busy) — never guess one.

On **(3)**, the user has just answered the setup machine's `continueToMigration`
gate, so **submit it rather than letting the gate ask again**:

```
progress_setup(answers={"continue_to_migration": "true"})
```

Act on that response as `setup/SKILL.md` describes — it walks git, the Snowflake
target and the testing choice. Calling a bare `progress_setup()` here instead
makes the machine put the same question to the user a second time. The same
applies later: if the user reviews the report and *then* says to move on, submit
the answer with that call. Do not load `../migrate-objects/SKILL.md` directly
from here; it has no Snowflake target configured yet.
