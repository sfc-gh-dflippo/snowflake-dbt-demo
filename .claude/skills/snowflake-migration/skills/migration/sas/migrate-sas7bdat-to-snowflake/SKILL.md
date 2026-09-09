---
name: migrate-sas7bdat-to-snowflake
parent_skill: sas
description: "Preview. Bulk-load .sas7bdat files from a Snowflake stage into tables, entirely server-side. Use whenever the user wants to ingest, load, or migrate SAS datasets (.sas7bdat) sitting in cloud storage / a stage into Snowflake, whether a one-time load or an ongoing scheduled pipeline. Triggers: load sas7bdat, bulk load sas, ingest sas files from stage, sas7bdat to snowflake, migrate sas datasets, schedule sas load, sas directory table."
license: Proprietary. See License-Skills for complete terms
---

# Migrate .sas7bdat Files from Stage to Snowflake

> © Snowflake Inc. This skill and its contents are the proprietary intellectual property of Snowflake Inc.

Load one or many `.sas7bdat` files that already sit on a Snowflake stage into tables.
**All parsing and loading runs inside Snowflake** (a Python stored procedure using
`pandas.read_sas` + `SnowflakeFile`). Nothing is parsed on the client.

## Mental model

- The stage may contain subfolders. **Each subfolder = one target table** (all
  `.sas7bdat` files directly inside it are appended into that table). Files at the
  **stage root (no subfolder) = one table each.**
- A single **engine stored procedure** does all the work. A **one-time load** just
  `CALL`s it once. An **ongoing load** wraps that same proc in a scheduled **Task**
  and uses a **control table** to load only new/changed files.
- The proc **refreshes the stage's directory table itself** at the start of every run,
  so both one-time and scheduled loads always see newly-arrived files. (First-time
  setup still enables the directory table; see Step 0.)

## Prerequisites

- The stage already exists and points at the `.sas7bdat` files. (This skill verifies
  it; it does not create the stage.)
- Role can `CREATE TABLE`, `CREATE PROCEDURE`, and (ongoing only) `CREATE TASK` +
  `EXECUTE TASK` in the target schema, plus `USAGE` + `READ` on the stage.
- A warehouse is available. For large files (>~500 MB) prefer a Snowpark-optimized
  warehouse — see `references/architecture.md`.

## Setup (always do first)

**Load** `references/architecture.md` — it holds the exact server-side read pattern,
SAS date/encoding handling, memory/chunking, and warehouse guidance you will need
while deploying.

### Step 0: Confirm stage and directory table

1. **Ask** the user for the stage name and target database/schema/warehouse.

2. **Verify** the stage and check whether a directory table is enabled (the engine
   enumerates files with `DIRECTORY(@stage)`, which requires one):
   ```sql
   DESCRIBE STAGE <stage>;
   ```
   Look at the `directory` property. If files sit on an external stage, also confirm a
   storage integration is in use.

3. **Ask** the user before changing the stage:
   ```
   The engine lists files with DIRECTORY(@stage), which needs a directory table.
   - Directory table enabled? (yes / no / unknown)
   - Storage integration backing this stage (external stages)? (name / n/a)
   May I enable the directory table and refresh it? (yes / no)
   ```

   **If approved and not enabled**, apply `assets/directory_table_setup.sql`
   (edit the stage name first), then confirm files are visible:
   ```sql
   SELECT relative_path, size, last_modified
   FROM DIRECTORY(@<stage>)
   WHERE relative_path ILIKE '%.sas7bdat'
   ORDER BY relative_path;
   ```

**⚠️ STOPPING POINT:** Do not proceed until the query above returns the expected
`.sas7bdat` files. If it returns nothing, the directory table is stale
(`ALTER STAGE <stage> REFRESH;`) or the path/stage is wrong.

### Step 1: Preview the file → table mapping

From the `DIRECTORY()` result, compute the plan and **show it to the user**:

- subfolder `foo/` with files `a.sas7bdat`, `b.sas7bdat` → table `FOO` (2 files appended)
- root file `customers.sas7bdat` → table `CUSTOMERS` (1 file)

Table names are the normalized, uppercased folder/file stem (invalid chars → `_`).
Present the mapping as a table so the user can catch surprises before anything loads.

### Step 2: Route — one-time or ongoing?

**Ask** the user:
```
Is this a ONE-TIME load, or an ONGOING (scheduled) pipeline?
1. One-time  — load what's on the stage now, then stop.
2. Ongoing   — set up a control table + scheduled Task to keep loading new files.
```

| Choice | Go to |
|--------|-------|
| One-time | **Section A** |
| Ongoing | **Section B** |

---

## Section A: One-time load

### A1. Deploy the engine

1. **Edit** `assets/control_table.sql` and `assets/loader_sproc.sql` placeholders
   (`<DB>`, `<SCHEMA>`) and run them. The control table is used even for one-time
   loads (it gives you an audit row per file and makes re-runs idempotent).

2. Verify the proc compiled: `SHOW PROCEDURES LIKE 'LOAD_SAS7BDAT%' IN SCHEMA <DB>.<SCHEMA>;`

### A2. Ask write mode per table

**Ask** the user, defaulting to append:
```
For each target table, load in APPEND or OVERWRITE mode? (default: append)
Reply "append all", "overwrite all", or list exceptions (e.g. "overwrite FOO").
```
Pass this as the `write_mode` argument (a single default) plus optional per-table
overrides (a JSON map) — see the proc signature in `assets/loader_sproc.sql`.

### A3. Run the load

```sql
CALL <DB>.<SCHEMA>.LOAD_SAS7BDAT(
  '@<DB>.<SCHEMA>.<STAGE>',   -- stage
  '<DB>.<SCHEMA>',            -- target schema for tables
  'append',                   -- default write mode
  NULL,                       -- per-table overrides (JSON) e.g. '{"ORDERS":"overwrite"}' or NULL
  FALSE,                      -- incremental? FALSE = load everything now
  'latin-1'                   -- encoding for SAS strings (latin-1 is a safe default)
);
```

The proc returns a summary (files processed, tables written, rows, errors) and writes
one row per file to the control table.

### A4. Verify

Run the verification queries in `references/testing.md` ("Verification queries"):
table list, row counts vs. the control table, a `DESCRIBE TABLE` to confirm date/type
conversion, and column comments (SAS labels). Report results to the user.

**Halt:** One-time load complete. If the user later wants scheduling, go to Section B.

---

## Section B: Ongoing scheduled load

### B1. Deploy engine + control table

Same as A1 (run `assets/control_table.sql` + `assets/loader_sproc.sql`). The control
table is mandatory here: incremental runs skip files whose `relative_path` +
`size` + `last_modified` already loaded successfully.

### B2. Choose the trigger

**Ask** the user:
```
How should the Task run?
1. Time-based  — a CRON/interval schedule (simplest). e.g. every hour.
2. Stream-triggered — only runs when new files land on the stage
   (a stream on the directory table). More efficient for sparse arrivals.
```

### B3. Ask write mode + schedule

- Write mode default (append recommended for ongoing) + any per-table overrides.
- Warehouse for the Task, and schedule (CRON expr / interval) if time-based.

### B4. Deploy the Task

**Edit** `assets/task_setup.sql` (stage, schema, warehouse, schedule, chosen trigger
variant) and run it. It creates the Task calling `LOAD_SAS7BDAT(..., incremental=TRUE)`.
The proc refreshes the stage's directory table at the start of each run, so the
time-based variant needs no separate refresh task. The **stream-triggered** variant is
the exception: its `WHEN SYSTEM$STREAM_HAS_DATA` gate is evaluated before the proc runs,
so it needs stage auto-refresh or a small predecessor refresh task to feed the stream
(see notes in `assets/task_setup.sql`).

Then resume it:
```sql
ALTER TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK RESUME;
```

### B5. Validate the pipeline

1. Kick a manual run: `EXECUTE TASK <DB>.<SCHEMA>.LOAD_SAS7BDAT_TASK;`
2. Check history: `SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY()) ORDER BY scheduled_time DESC;`
3. Confirm tables + control-table rows (verification queries in `references/testing.md`).
4. Prove incrementality: add one new file to the stage, `ALTER STAGE <stage> REFRESH;`,
   run the Task again, and confirm only the new file loaded.

**Halt:** Ongoing pipeline live. Remind the user the Task consumes credits on its
schedule and can be suspended with `ALTER TASK ... SUSPEND`.

---

## Testing this skill (for the skill author / first run)

Follow `references/testing.md` to download real public `.sas7bdat` samples, PUT them
into an internal test stage (two subfolders + one root file), and run Sections A and B
end-to-end.

## Stopping Points

- ✋ Step 0: before altering the stage (directory table) — needs user approval
- ✋ Step 1: after showing the file→table mapping — user confirms
- ✋ Step 2: one-time vs ongoing routing
- ✋ A2 / B3: write mode (append vs overwrite) per table

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `DIRECTORY(@stage)` returns 0 rows | Directory table not enabled (Step 0). The proc auto-refreshes each run, but the directory table must first be enabled on the stage. |
| Proc errors reading a file | Encoding — pass a different `encoding` (e.g. `latin-1`, `utf-8`, `cp1252`). See `references/architecture.md`. |
| Date columns arrive as numbers | SAS format wasn't a recognized date format; see the date-handling section in `references/architecture.md`. |
| Proc runs out of memory on a big file | Use a Snowpark-optimized warehouse and/or lower the chunk size; see architecture notes. |
| `pandas.read_sas` fails on a specific file | Try the optional `pyreadstat` via Artifact Repository fallback (architecture.md). |
| Duplicate rows after re-run | Re-ran in append without incremental; use `incremental=TRUE` (ongoing) or overwrite mode. |

## Output

A deployed `LOAD_SAS7BDAT` stored procedure + control table, target tables (one per
subfolder, one per root file), and — for ongoing — a scheduled/stream-triggered Task.
