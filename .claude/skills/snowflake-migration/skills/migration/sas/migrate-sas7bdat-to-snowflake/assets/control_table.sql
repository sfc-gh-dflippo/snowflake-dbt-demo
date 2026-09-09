-- control_table.sql
-- Audit + incremental-load control table. One row per (file, load attempt).
-- Used by LOAD_SAS7BDAT for:
--   * audit (what loaded, when, how many rows, errors)
--   * idempotency / incremental (skip files already loaded successfully whose
--     size + last_modified are unchanged)
-- Replace <DB>, <SCHEMA> before running.

CREATE TABLE IF NOT EXISTS <DB>.<SCHEMA>.SAS_LOAD_CONTROL (
    relative_path       STRING        NOT NULL,   -- path within the stage, e.g. 'sales/orders.sas7bdat'
    target_table        STRING        NOT NULL,   -- fully-qualified table the file was loaded into
    file_size           NUMBER,                   -- bytes, from DIRECTORY()
    last_modified       TIMESTAMP_NTZ,            -- from DIRECTORY() (for humans)
    last_modified_epoch NUMBER,                   -- absolute epoch seconds; used for incremental match (tz-safe)
    write_mode          STRING,                   -- 'append' or 'overwrite' used for this load
    load_status     STRING        NOT NULL,   -- 'SUCCESS' | 'FAILED' | 'SKIPPED'
    rows_loaded     NUMBER,
    error_msg       STRING,
    load_ts         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Convenience view: the latest successful load per file (used for incremental skip).
CREATE OR REPLACE VIEW <DB>.<SCHEMA>.SAS_LOAD_CONTROL_LATEST AS
SELECT relative_path, file_size, last_modified, last_modified_epoch, target_table, rows_loaded, load_ts
FROM (
    SELECT c.*,
           ROW_NUMBER() OVER (PARTITION BY relative_path ORDER BY load_ts DESC) AS rn
    FROM <DB>.<SCHEMA>.SAS_LOAD_CONTROL c
    WHERE load_status = 'SUCCESS'
)
WHERE rn = 1;
