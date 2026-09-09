# Testing the skill end-to-end

Use real public `.sas7bdat` samples (there is no reliable OSS writer for sas7bdat, so
download rather than generate). Files run through the same server-side engine users hit.

## 1. Get sample files

Small, public `.sas7bdat` files with mixed numeric/string/date columns live in the
pandas and pyreadstat test suites. Download a handful (verify URLs resolve; raw GitHub
paths can move between branches):

```bash
mkdir -p /tmp/sas_samples/sales /tmp/sas_samples/hr
# pandas test data (dates, numerics, strings)
curl -fsSL -o /tmp/sas_samples/sales/airline.sas7bdat \
  https://github.com/pandas-dev/pandas/raw/main/pandas/tests/io/sas/data/airline.sas7bdat
curl -fsSL -o /tmp/sas_samples/sales/productsales.sas7bdat \
  https://github.com/pandas-dev/pandas/raw/main/pandas/tests/io/sas/data/productsales.sas7bdat
curl -fsSL -o /tmp/sas_samples/hr/datetime.sas7bdat \
  https://github.com/pandas-dev/pandas/raw/main/pandas/tests/io/sas/data/datetime.sas7bdat
# a root-level file (becomes its own table)
curl -fsSL -o /tmp/sas_samples/cars.sas7bdat \
  https://github.com/pandas-dev/pandas/raw/main/pandas/tests/io/sas/data/cars.sas7bdat
```

Layout produced (2 subfolders + 1 root file):
```
/tmp/sas_samples/
  sales/airline.sas7bdat        -> table SALES
  sales/productsales.sas7bdat   -> table SALES (appended)
  hr/datetime.sas7bdat          -> table HR
  cars.sas7bdat                 -> table CARS
```

## 2. Stage the files (internal test stage)

```sql
CREATE DATABASE IF NOT EXISTS SAS_LOAD_TEST;
CREATE SCHEMA  IF NOT EXISTS SAS_LOAD_TEST.PUBLIC;
CREATE STAGE   IF NOT EXISTS SAS_LOAD_TEST.PUBLIC.SAS_STAGE
    DIRECTORY = (ENABLE = TRUE);
```
PUT preserves the subfolder in the path when you point at each folder:
```bash
snow sql -q "PUT file:///tmp/sas_samples/sales/*.sas7bdat @SAS_LOAD_TEST.PUBLIC.SAS_STAGE/sales AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
snow sql -q "PUT file:///tmp/sas_samples/hr/*.sas7bdat    @SAS_LOAD_TEST.PUBLIC.SAS_STAGE/hr    AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
snow sql -q "PUT file:///tmp/sas_samples/cars.sas7bdat    @SAS_LOAD_TEST.PUBLIC.SAS_STAGE       AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
```
`AUTO_COMPRESS=FALSE` matters — the loader matches `%.sas7bdat`, not `.sas7bdat.gz`.
Then `ALTER STAGE SAS_LOAD_TEST.PUBLIC.SAS_STAGE REFRESH;` and confirm files show in
`DIRECTORY(@SAS_LOAD_TEST.PUBLIC.SAS_STAGE)`.

## 3. Deploy + one-time load

Run `assets/control_table.sql` and `assets/loader_sproc.sql` (DB=SAS_LOAD_TEST,
SCHEMA=PUBLIC), then:
```sql
CALL SAS_LOAD_TEST.PUBLIC.LOAD_SAS7BDAT(
  '@SAS_LOAD_TEST.PUBLIC.SAS_STAGE', 'SAS_LOAD_TEST.PUBLIC',
  'append', NULL, FALSE, 'latin-1');
```

## 4. Verification queries

```sql
-- Tables created (expect SALES, HR, CARS)
SHOW TABLES IN SCHEMA SAS_LOAD_TEST.PUBLIC;

-- Per-file audit + row counts
SELECT relative_path, target_table, load_status, rows_loaded, error_msg
FROM SAS_LOAD_TEST.PUBLIC.SAS_LOAD_CONTROL ORDER BY load_ts;

-- SALES got BOTH files appended: control rows_loaded should sum to the table count
SELECT (SELECT COUNT(*) FROM SAS_LOAD_TEST.PUBLIC.SALES) AS table_rows,
       (SELECT SUM(rows_loaded) FROM SAS_LOAD_TEST.PUBLIC.SAS_LOAD_CONTROL
        WHERE target_table='SAS_LOAD_TEST.PUBLIC.SALES' AND load_status='SUCCESS') AS control_rows;

-- Date/type conversion + column comments (labels)
DESCRIBE TABLE SAS_LOAD_TEST.PUBLIC.HR;   -- date/datetime cols should be DATE/TIMESTAMP
SELECT * FROM SAS_LOAD_TEST.PUBLIC.HR LIMIT 5;
```
Checklist: correct table set; `table_rows == control_rows`; date columns are DATE/
TIMESTAMP (not numbers); comments present on labeled columns; no `FAILED` rows.

## 5. Ongoing / incremental proof

Deploy `assets/task_setup.sql` (Variant 1), then:
```sql
EXECUTE TASK SAS_LOAD_TEST.PUBLIC.LOAD_SAS7BDAT_TASK;   -- should SKIP everything already loaded
```
Add a new file, refresh, run again — only the new file should show `SUCCESS`, the rest
`SKIPPED`:
```sql
-- (PUT one more file into @.../sales, then)
ALTER STAGE SAS_LOAD_TEST.PUBLIC.SAS_STAGE REFRESH;
EXECUTE TASK SAS_LOAD_TEST.PUBLIC.LOAD_SAS7BDAT_TASK;
SELECT relative_path, load_status, rows_loaded FROM SAS_LOAD_TEST.PUBLIC.SAS_LOAD_CONTROL
ORDER BY load_ts DESC LIMIT 10;
```

## 6. Cleanup

```sql
DROP DATABASE IF EXISTS SAS_LOAD_TEST;
```
