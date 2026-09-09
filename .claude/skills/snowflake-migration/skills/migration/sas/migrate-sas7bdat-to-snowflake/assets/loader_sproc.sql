-- loader_sproc.sql
-- Server-side engine that bulk-loads .sas7bdat files from a stage into tables.
-- Runs ENTIRELY in Snowflake: reads staged files with SnowflakeFile, parses with
-- pandas.read_sas, writes with Snowpark. Shared by one-time (CALL once) and ongoing
-- (Task calls with incremental=TRUE) flows.
--
-- Mapping: each stage subfolder -> one table (files appended); each root-level file
-- -> its own table. Table name = normalized, uppercased folder/file stem.
--
-- Replace <DB>, <SCHEMA> before running.

CREATE OR REPLACE PROCEDURE <DB>.<SCHEMA>.LOAD_SAS7BDAT(
    STAGE           STRING,   -- e.g. '@DB.SCHEMA.MY_STAGE'
    TARGET_SCHEMA   STRING,   -- e.g. 'DB.SCHEMA' where tables are created
    WRITE_MODE      STRING,   -- default write mode: 'append' or 'overwrite'
    TABLE_OVERRIDES STRING,   -- JSON map of per-table mode, e.g. '{"ORDERS":"overwrite"}', or NULL
    INCREMENTAL     BOOLEAN,  -- TRUE = skip files already loaded (unchanged size+last_modified)
    ENCODING        STRING    -- text encoding for SAS strings, e.g. 'latin-1' (safe default), 'utf-8', 'cp1252'
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'pandas')
HANDLER = 'run'
AS
$$
import io
import json
import re
import pandas as pd
from snowflake.snowpark.files import SnowflakeFile

# SAS format names (uppercased, no width/decimals) that represent pure DATE vs TIME.
# pandas.read_sas already converts recognized DATE and DATETIME formats to datetime64,
# so we only downcast pure-date columns to date and convert time-of-day columns.
DATE_FORMATS = {"DATE", "YYMMDD", "MMDDYY", "DDMMYY", "YYMMDDD", "WEEKDATE",
                "WORDDATE", "MONYY", "JULIAN", "E8601DA", "B8601DA"}
TIME_FORMATS = {"TIME", "HHMM", "TIMEAMPM", "E8601TM", "B8601TM"}


def _norm_ident(name: str) -> str:
    """Normalize a SAS name/stem into a safe, uppercased Snowflake identifier."""
    s = re.sub(r"[^0-9a-zA-Z_]", "_", (name or "").strip())
    if not s:
        s = "COL"
    if s[0].isdigit():
        s = "_" + s
    return s.upper()[:255]


def _table_for(relative_path: str) -> str:
    """Subfolder -> table name; root file -> file stem as table name."""
    parts = relative_path.split("/")
    if len(parts) > 1 and parts[-2] != "":
        return _norm_ident(parts[-2])           # deepest subfolder
    stem = parts[-1].rsplit(".", 1)[0]           # strip .sas7bdat
    return _norm_ident(stem)


def _base_fmt(fmt) -> str:
    if not fmt:
        return ""
    if isinstance(fmt, bytes):
        fmt = fmt.decode("latin-1", "ignore")
    return re.sub(r"[0-9.]+$", "", str(fmt)).upper()


def _read_sas(buf, encoding):
    """Return (dataframe, {col: label}). Applies Standard date/time fidelity."""
    reader = pd.read_sas(buf, format="sas7bdat", encoding=encoding, iterator=True)
    labels, date_cols, time_cols = {}, [], []
    for c in reader.columns:
        cname = c.name.decode(encoding, "ignore") if isinstance(c.name, bytes) else c.name
        clabel = c.label.decode(encoding, "ignore") if isinstance(c.label, bytes) else c.label
        if clabel:
            labels[cname] = clabel
        bf = _base_fmt(getattr(c, "format", ""))
        if bf in DATE_FORMATS:
            date_cols.append(cname)
        elif bf in TIME_FORMATS:
            time_cols.append(cname)
    df = reader.read()
    reader.close()
    # pandas already produced datetime64 for recognized date/datetime formats.
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
    for col in time_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            # SAS time = seconds since midnight
            df[col] = pd.to_datetime(df[col], unit="s", errors="coerce").dt.time
    return df, labels


def run(session, stage, target_schema, write_mode, table_overrides, incremental, encoding):
    stage = stage.strip()
    if not stage.startswith("@"):
        stage = "@" + stage
    encoding = (encoding or "latin-1").strip()
    default_mode = (write_mode or "append").strip().lower()
    overrides = {k.upper(): v.lower() for k, v in (json.loads(table_overrides) if table_overrides else {}).items()}
    ctrl = f"{target_schema}.SAS_LOAD_CONTROL"

    # Refresh the stage's directory table so DIRECTORY() reflects the current files.
    # This runs every call so BOTH one-time and scheduled/ongoing loads always see new
    # arrivals (otherwise an incremental Task would never notice new files). Best-effort:
    # if the caller lacks refresh privilege, or the stage uses cloud auto-refresh, we log
    # and continue rather than fail the load.
    try:
        session.sql(f"ALTER STAGE {stage[1:]} REFRESH").collect()
    except Exception:
        pass

    # Total .sas7bdat files on the stage (for the skipped count).
    total = session.sql(
        f"SELECT COUNT(*) FROM DIRECTORY({stage}) WHERE relative_path ILIKE '%.sas7bdat'"
    ).collect()[0][0]

    # Enumerate files to load. For incremental runs, anti-join against the control
    # view so already-loaded, unchanged files (same path + size + last_modified) are
    # excluded. The comparison is done in SQL so both sides normalize to TIMESTAMP_NTZ
    # in the same session timezone (a Python str() compare fails: DIRECTORY returns
    # tz-aware LTZ, the control table stores naive NTZ).
    if incremental:
        enum_sql = (
            f"SELECT d.relative_path, d.size, d.last_modified, DATE_PART(EPOCH_SECOND, d.last_modified) "
            f"FROM DIRECTORY({stage}) d "
            f"LEFT JOIN {target_schema}.SAS_LOAD_CONTROL_LATEST c "
            f"  ON c.relative_path = d.relative_path AND c.file_size = d.size "
            f"  AND c.last_modified_epoch = DATE_PART(EPOCH_SECOND, d.last_modified) "
            f"WHERE d.relative_path ILIKE '%.sas7bdat' AND c.relative_path IS NULL "
            f"ORDER BY d.relative_path"
        )
        try:
            files = session.sql(enum_sql).collect()
        except Exception:
            # Control view may not exist yet (first run) -> load everything.
            files = session.sql(
                f"SELECT relative_path, size, last_modified, DATE_PART(EPOCH_SECOND, last_modified) "
                f"FROM DIRECTORY({stage}) WHERE relative_path ILIKE '%.sas7bdat' ORDER BY relative_path"
            ).collect()
    else:
        files = session.sql(
            f"SELECT relative_path, size, last_modified, DATE_PART(EPOCH_SECOND, last_modified) "
            f"FROM DIRECTORY({stage}) WHERE relative_path ILIKE '%.sas7bdat' ORDER BY relative_path"
        ).collect()

    overwritten_this_run = set()   # tables already replaced this run (so 2nd+ file appends)
    summary = {"files": total, "skipped": total - len(files),
               "loaded": 0, "failed": 0, "rows": 0, "tables": {}}

    for row in files:
        rel_path, size, last_mod, lm_epoch = row[0], row[1], row[2], row[3]
        table = _table_for(rel_path)
        fqtn = f"{target_schema}.{table}"

        try:
            # Read the staged file server-side into memory, then parse.
            url = session.sql(f"SELECT BUILD_SCOPED_FILE_URL({stage}, ?)", params=[rel_path]).collect()[0][0]
            with SnowflakeFile.open(url, "rb") as f:
                buf = io.BytesIO(f.read())
            df, labels = _read_sas(buf, encoding)
            df.columns = [_norm_ident(c) for c in df.columns]
            labels = {_norm_ident(k): v for k, v in labels.items()}

            # Decide mode: override > default; first file into an overwrite table replaces,
            # later files into the same table append.
            mode = overrides.get(table, default_mode)
            if mode == "overwrite" and table not in overwritten_this_run:
                eff_mode = "overwrite"
                overwritten_this_run.add(table)
            else:
                eff_mode = "append"

            created = eff_mode == "overwrite" or not session.sql(
                f"SHOW TABLES LIKE '{table}' IN SCHEMA {target_schema}"
            ).collect()

            session.create_dataframe(df).write.mode(eff_mode).save_as_table(fqtn)

            # Set SAS labels as column comments (only when table (re)created, to avoid churn).
            if created and labels:
                for col, lbl in labels.items():
                    safe = str(lbl).replace("'", "''")
                    try:
                        session.sql(f'COMMENT ON COLUMN {fqtn}."{col}" IS \'{safe}\'').collect()
                    except Exception:
                        pass

            n = len(df)
            summary["loaded"] += 1
            summary["rows"] += n
            summary["tables"][table] = summary["tables"].get(table, 0) + n
            session.sql(
                f"INSERT INTO {ctrl}(relative_path,target_table,file_size,last_modified,last_modified_epoch,write_mode,load_status,rows_loaded) "
                f"SELECT ?,?,?,?,?,?,?,?",
                params=[rel_path, fqtn, size, last_mod, lm_epoch, eff_mode, "SUCCESS", n],
            ).collect()
        except Exception as e:
            summary["failed"] += 1
            msg = str(e)[:1000].replace("'", "''")
            session.sql(
                f"INSERT INTO {ctrl}(relative_path,target_table,file_size,last_modified,last_modified_epoch,write_mode,load_status,rows_loaded,error_msg) "
                f"SELECT ?,?,?,?,?,?,?,?,?",
                params=[rel_path, fqtn, size, last_mod, lm_epoch, default_mode, "FAILED", 0, msg],
            ).collect()

    return json.dumps(summary)
$$;
