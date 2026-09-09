-- directory_table_setup.sql
-- Enable and refresh the directory table on an EXISTING stage so the loader can
-- enumerate files with DIRECTORY(@stage). This skill does NOT create the stage.
-- Replace <DB>, <SCHEMA>, <STAGE> before running.

-- 1. Inspect the stage. Check the "directory" row in the output: if enable=false,
--    run the ALTER below. For external stages, confirm STORAGE_INTEGRATION is set.
DESCRIBE STAGE <DB>.<SCHEMA>.<STAGE>;

-- 2. Enable the directory table (safe to run if already enabled).
ALTER STAGE <DB>.<SCHEMA>.<STAGE> SET DIRECTORY = (ENABLE = TRUE);

-- 3. Refresh so the directory table reflects current files.
--    (Auto-refresh via cloud notifications can be configured separately; a manual
--     REFRESH is enough for one-time loads and is also run by the ongoing Task.)
ALTER STAGE <DB>.<SCHEMA>.<STAGE> REFRESH;

-- 4. Confirm the .sas7bdat files are visible. Expect one row per file, with the
--    subfolder embedded in relative_path (e.g. 'sales/orders.sas7bdat').
SELECT relative_path, size, last_modified
FROM DIRECTORY(@<DB>.<SCHEMA>.<STAGE>)
WHERE relative_path ILIKE '%.sas7bdat'
ORDER BY relative_path;
