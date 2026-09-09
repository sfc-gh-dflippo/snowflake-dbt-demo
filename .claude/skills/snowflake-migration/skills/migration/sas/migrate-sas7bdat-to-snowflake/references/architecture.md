# Architecture & server-side details

How the `LOAD_SAS7BDAT` engine works, and the decisions behind it. Read this before
deploying or debugging.

## Why server-side `pandas.read_sas`

All execution must stay inside Snowflake, so the parser must be a package available in
the Snowflake Anaconda channel and free of external C dependencies at runtime:

- **`pandas.read_sas(..., format='sas7bdat')`** — pure-Python, ships in Snowflake
  Anaconda. **This is the engine.** It reads `.sas7bdat` and auto-converts columns
  whose SAS format is a recognized date/datetime format to `datetime64`.
- **`pyreadstat`** — faster and more robust (C/ReadStat), but **not** in the Snowflake
  Anaconda channel. Only usable server-side via the PyPI **Artifact Repository**
  (needs an external access integration to fetch the wheel). Keep as a fallback for
  files `pandas.read_sas` cannot parse — see "pyreadstat fallback" below.

## Reading a staged file inside the proc

Files are enumerated from the stage's **directory table**:
```sql
SELECT relative_path, size, last_modified FROM DIRECTORY(@stage)
WHERE relative_path ILIKE '%.sas7bdat';
```
Each file is read with a scoped URL + `SnowflakeFile` (the documented way to read
arbitrary staged files from a Python handler):
```python
url = session.sql("SELECT BUILD_SCOPED_FILE_URL(@stage, ?)", params=[rel_path]).collect()[0][0]
with SnowflakeFile.open(url, "rb") as f:
    buf = io.BytesIO(f.read())          # whole file into proc memory
df = pd.read_sas(buf, format="sas7bdat", encoding=encoding)
```
The whole file is read into memory because the SAS7BDAT reader needs a seekable
buffer. That makes per-file memory ~= file size; size the warehouse accordingly.

## The write path

The proc uses `session.create_dataframe(df).write.mode(...).save_as_table(fqtn)`:
- `mode="overwrite"` recreates the table with this run's data; `mode="append"` adds.
- `create_dataframe` from pandas infers Snowpark types (datetime64 → TIMESTAMP_NTZ,
  date → DATE, float/int → NUMBER/FLOAT, str → VARCHAR).
- Chosen over `session.write_pandas(auto_create_table=True)` because it gives cleaner
  control of append/overwrite and avoids identifier-quoting surprises. If you hit a
  `create_dataframe` limitation on a very wide/large frame, `write_pandas` is the
  alternate — both stage data through a temp internal stage inside the proc.

**Per-table mode within a run:** the first file written to an *overwrite* table
replaces it; subsequent files for that same table append (so a folder with 3 files in
overwrite mode ends up with all 3 files' rows, not just the last).

## SAS type model (what maps to what)

A `.sas7bdat` dataset has only **two physical column types**: **numeric** (8-byte
double) and **character**. There is no binary/BLOB/varbinary type in SAS datasets, so
nothing "binary" exists to load. Dates, datetimes, and times are just numeric values
carrying a display *format* (SAS epoch = 1960-01-01). Verified mappings:

| SAS column | Format example | Snowflake type |
|------------|----------------|----------------|
| numeric | (none) | `FLOAT` |
| numeric | `DATE`, `YYMMDD`, `E8601DA` | `DATE` |
| numeric | `DATETIME`, `E8601DT` | `TIMESTAMP_NTZ` (fractional seconds preserved) |
| numeric | `TIME`, `HHMM` | `TIME` (seconds since midnight) |
| character | — | `TEXT` (VARCHAR) |

Notes proven in testing: the *same* underlying number with **no** date format stays
`FLOAT` (it is not guessed into a date); out-of-range dates (e.g. `9999-12-29`) load
correctly because `pandas.read_sas` returns them as Python `date`/`datetime` objects
rather than overflowing `datetime64`; wide tables (hundreds of columns) load fine.

## Metadata fidelity: names, labels, dates (Standard)


- **Dates/datetimes:** `pandas.read_sas` already converts recognized date/datetime
  formats to `datetime64`. The proc additionally downcasts pure **date-format** columns
  to `date` (so they land as Snowflake `DATE`, not midnight timestamps) and converts
  **time-of-day** columns (seconds since midnight) to `time`. SAS epoch is
  1960-01-01; pandas handles the offset internally.
- **Column names:** normalized to uppercase, non-alphanumerics → `_`, leading digit
  prefixed with `_`.
- **Labels:** SAS column labels are read from the `SAS7BDATReader.columns` metadata and
  applied as Snowflake column comments (`COMMENT ON COLUMN ...`) when a table is
  created/overwritten.

## Encoding

`pandas.read_sas` needs to know how to decode byte strings. The proc defaults to
`latin-1`, which never raises on decode (every byte maps to a char) — a safe universal
default. If you see mojibake, pass the file's true encoding (`utf-8`, `cp1252`,
`wlatin1`→`cp1252`, etc.). Encoding is a proc argument, so no redeploy is needed.

## Large files, memory, and warehouses

- Per-file memory ≈ file size (read fully into `BytesIO`) plus the pandas frame.
- For files above a few hundred MB, use a **Snowpark-optimized warehouse** (more
  memory per node) for the proc/Task.
- The proc processes files sequentially; total runtime scales with total bytes.

## Directory-table refresh (automatic)

`DIRECTORY(@stage)` only returns files that the directory table knows about, and it is
not always current. So the proc runs `ALTER STAGE <stage> REFRESH` at the **start of
every call** (best-effort: wrapped in try/except so a missing refresh privilege or a
cloud-auto-refresh stage doesn't fail the load). This means both one-time and scheduled
loads always see newly-arrived files without a separate refresh step. The directory
table must still be *enabled* once on the stage (Step 0 / `directory_table_setup.sql`).

Exception: the **stream-triggered** Task variant evaluates its `WHEN SYSTEM$STREAM_HAS_DATA`
gate before the proc runs, so the proc's refresh is too late to feed the stream — that
variant needs stage auto-refresh or a predecessor refresh task.

## Incremental logic (ongoing)

With `incremental=TRUE`, before loading a file the proc checks
`SAS_LOAD_CONTROL_LATEST` for the same `relative_path` with identical `size` +
`last_modified`. Match → log `SKIPPED` and move on. This makes scheduled runs cheap
and idempotent. A changed file (new size/mtime) re-loads; in append mode that adds
rows again, so use overwrite mode for tables whose source files are edited in place.

## Schema drift (limitation)

Appending files with differing column sets into one table can fail (Snowpark append
requires a compatible schema). For datasets where files share a schema this is a
non-issue. If a folder mixes schemas, split it, use overwrite, or pre-align columns.

## pyreadstat fallback (optional, advanced)

If a specific file won't parse with `pandas.read_sas`, you can enable `pyreadstat`
server-side via the PyPI Artifact Repository:
1. Create an external access integration allowing egress to the PyPI endpoints.
2. Create an `ARTIFACT REPOSITORY` and reference `pyreadstat` in the proc's
   `PACKAGES`/`ARTIFACT_REPOSITORY` clause.
3. In the handler, write the `BytesIO` to a temp path and call
   `pyreadstat.read_sas7bdat(path)` (it returns `(df, meta)`; `meta.column_labels`
   holds labels, `meta.original_variable_types`/`meta.variable_value_labels` add
   fidelity). This still executes inside Snowflake.
Keep this off by default — it adds network + object setup. Only reach for it on files
that genuinely fail the default parser.
