# SAS PROC Steps to Snowflake Conversion

## When to Load

Load when SAS code contains: `PROC SORT`, `PROC MEANS`, `PROC SUMMARY`, `PROC FREQ`, `PROC TRANSPOSE`, `PROC RANK`, `PROC APPEND`, `PROC CONTENTS`, `PROC PRINT`, `PROC TABULATE`, `PROC UNIVARIATE`, `PROC COMPARE`, `PROC IMPORT`, `PROC EXPORT`, or `PROC FORMAT`.

---

## PROC SORT

**SAS:**
```sas
PROC SORT DATA=input OUT=sorted;
  BY descending amount customer_id;
RUN;
```

**Snowflake:**
```sql
CREATE TABLE sorted AS
SELECT * FROM input
ORDER BY amount DESC, customer_id;
```

**With NODUPKEY (remove duplicates):**
```sas
PROC SORT DATA=input OUT=deduped NODUPKEY;
  BY customer_id;
RUN;
```

**Snowflake (CRITICAL: use explicit column list, NOT SELECT *):**
```sql
-- CORRECT: explicit column list excludes helper column
CREATE TABLE deduped AS
SELECT col1, col2, col3, customer_id
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY 1) AS rn
  FROM input
)
WHERE rn = 1;

-- WRONG: SELECT * leaks the rn column into output
-- SELECT * FROM (...) WHERE rn = 1;  -- DO NOT DO THIS
```

**NODUPKEY with TEMPORARY source:**
If the source is a TEMPORARY TABLE, the deduplicated output MUST also be TEMPORARY:
```sql
CREATE OR REPLACE TEMPORARY TABLE deduped AS
SELECT col1, col2 FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY 1) AS rn
  FROM temp_input
) WHERE rn = 1;
```

**PROC SORT stability:** SAS PROC SORT is stable (preserves original order for ties). If downstream logic depends on first/last row selection within ties, add deterministic ORDER BY columns.

**NODUPKEY dedup rules:**
- Do NOT add deduplication unless SAS explicitly uses NODUPKEY or NODUPREC
- Preserve sort stability assumptions where later logic depends on first/last row selection

**NODUPKEY BY _ALL_ → prefer SELECT DISTINCT:**
When SAS dedups on ALL columns (`PROC SORT NODUPKEY; BY _ALL_;`), every duplicate row is identical — there is no "which row to keep" decision. Use `SELECT DISTINCT`, which is simpler and faster than ROW_NUMBER():
```sql
-- SAS: PROC SORT DATA=mydata NODUPKEY; BY _ALL_; RUN;
CREATE OR REPLACE TEMPORARY TABLE mydata AS SELECT DISTINCT * FROM mydata;
```
Use ROW_NUMBER() (above) only when BY is a **subset** of columns, where you must choose which row survives each group.

## SAS INDEX → CLUSTER BY

SAS dataset indexes have no direct Snowflake equivalent. Convert index definitions to `CLUSTER BY` (or a documented comment), never silently drop them.

```sql
-- SAS: PROC SQL; CREATE INDEX idx ON tbl(col1, col2);
-- SAS: DATA tbl(INDEX=(idx=(col1 col2)));
-- SAS: PROC DATASETS; MODIFY tbl; INDEX CREATE col1;
-- Snowflake:
ALTER TABLE tbl CLUSTER BY (col1, col2);
```

**Rules:**
- Single-column index → `CLUSTER BY (col)`; composite → `CLUSTER BY (col1, col2, ...)`.
- CLUSTER BY benefits large tables (~1TB+ or frequent range/filter queries). For small or TEMPORARY tables, emit a comment instead of clustering:
  `-- CLUSTER BY (col) omitted — table is small/temporary; add if query performance requires it`
- UNIQUE index → clustering does NOT enforce uniqueness. Add a comment:
  `-- NOTE: SAS had UNIQUE index on (col); consider ALTER TABLE t ADD CONSTRAINT uq UNIQUE (col) NOT ENFORCED;`

## PROC MEANS / PROC SUMMARY

**SAS:**
```sas
PROC MEANS DATA=sales N MEAN STD MIN MAX SUM;
  CLASS region product;
  VAR revenue quantity;
  OUTPUT OUT=summary 
    N=n_revenue n_quantity
    MEAN=avg_revenue avg_quantity
    SUM=total_revenue total_quantity;
RUN;
```

**Snowflake (with GROUPING SETS for all CLASS combinations):**
```sql
CREATE TABLE summary AS
SELECT 
  region,
  product,
  COUNT(revenue) AS n_revenue,
  COUNT(quantity) AS n_quantity,
  AVG(revenue) AS avg_revenue,
  AVG(quantity) AS avg_quantity,
  SUM(revenue) AS total_revenue,
  SUM(quantity) AS total_quantity,
  STDDEV(revenue) AS std_revenue,
  MIN(revenue) AS min_revenue,
  MAX(revenue) AS max_revenue
FROM sales
GROUP BY GROUPING SETS (
  (region, product),
  (region),
  (product),
  ()
);
```

**With NWAY option (most detailed level only — no subtotals):**
```sas
PROC SUMMARY DATA=sales NWAY;
  CLASS region product;
  VAR revenue;
  OUTPUT OUT=summary SUM=total;
RUN;
```

**Snowflake (NWAY = simple GROUP BY, no GROUPING SETS):**
```sql
CREATE TABLE summary AS
SELECT 
  region,
  product,
  SUM(revenue) AS total,
  COUNT(*) AS _FREQ_
FROM sales
GROUP BY region, product;
```

**CLASS vs BY semantics:**
- `CLASS` = creates all combinations including subtotals (use GROUPING SETS)
- `CLASS` with `NWAY` = only the most detailed level (use simple GROUP BY)
- `BY` = separate analysis per BY group (same as PARTITION BY in output)
- Preserve missing-group handling: SAS excludes missing CLASS values by default unless `MISSING` option is specified

**Simple aggregation:**
```sas
PROC MEANS DATA=sales SUM;
  VAR amount;
RUN;
```

**Snowflake:**
```sql
SELECT SUM(amount) AS amount_sum FROM sales;
```

## PROC FREQ

**SAS:**
```sas
PROC FREQ DATA=customers;
  TABLES region * status / NOCUM NOPERCENT;
RUN;
```

**Snowflake:**
```sql
SELECT 
  region,
  status,
  COUNT(*) AS frequency,
  COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS percent
FROM customers
GROUP BY region, status
ORDER BY region, status;
```

**One-way frequency:**
```sas
PROC FREQ DATA=customers;
  TABLES status;
RUN;
```

**Snowflake:**
```sql
SELECT 
  status,
  COUNT(*) AS frequency,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percent,
  SUM(COUNT(*)) OVER (ORDER BY status) AS cumulative_freq
FROM customers
GROUP BY status
ORDER BY status;
```

## PROC TRANSPOSE

**SAS (long to wide):**
```sas
PROC TRANSPOSE DATA=long OUT=wide PREFIX=month_;
  BY customer_id;
  ID month;
  VAR sales;
RUN;
```

**Snowflake (PIVOT):**
```sql
SELECT * FROM long
PIVOT (
  SUM(sales) FOR month IN ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
) AS p (customer_id, month_JAN, month_FEB, month_MAR, month_APR, 
        month_MAY, month_JUN, month_JUL, month_AUG, month_SEP, 
        month_OCT, month_NOV, month_DEC);
```

**SAS (wide to long):**
```sas
PROC TRANSPOSE DATA=wide OUT=long NAME=quarter;
  BY customer_id;
  VAR q1 q2 q3 q4;
RUN;
```

**Snowflake (UNPIVOT):**
```sql
SELECT * FROM wide
UNPIVOT (
  value FOR quarter IN (q1, q2, q3, q4)
);
```

**PROC TRANSPOSE with PREFIX/SUFFIX/DELIMITER:**
- PREFIX= → column name prefix in output (use AS alias in PIVOT)
- SUFFIX= → column name suffix in output
- DELIMITER= → separator between ID value and prefix
- Preserve output column naming rules explicitly

**Dynamic PROC TRANSPOSE (unknown ID values):**
When the ID column values are not known at conversion time, use a stored procedure with EXECUTE IMMEDIATE to build dynamic PIVOT SQL, or flag MANUAL_REVIEW_REQUIRED.

**One-row-per-group vs multi-row-per-group:**
- If VAR lists multiple variables but no ID: produces one row per BY group with one column per VAR
- If VAR and ID both present: produces one row per BY group with columns named from ID values

## PROC RANK

**SAS:**
```sas
PROC RANK DATA=sales OUT=ranked GROUPS=10;
  VAR revenue;
  RANKS revenue_decile;
RUN;
```

**Snowflake:**
```sql
CREATE TABLE ranked AS
SELECT *,
  NTILE(10) OVER (ORDER BY revenue) AS revenue_decile
FROM sales;
```

**Simple rank:**
```sas
PROC RANK DATA=sales OUT=ranked;
  VAR revenue;
  RANKS revenue_rank;
RUN;
```

**Snowflake:**
```sql
SELECT *,
  RANK() OVER (ORDER BY revenue) AS revenue_rank
FROM sales;
```

## PROC APPEND

**SAS:**
```sas
PROC APPEND BASE=master DATA=new_data FORCE;
RUN;
```

**Snowflake:**
```sql
INSERT INTO master
SELECT * FROM new_data;
```

## PROC DATASETS (DELETE)

**SAS:**
```sas
PROC DATASETS LIBRARY=work NOLIST;
  DELETE temp1 temp2 temp3;
QUIT;
```

**Snowflake:**
```sql
DROP TABLE IF EXISTS temp1;
DROP TABLE IF EXISTS temp2;
DROP TABLE IF EXISTS temp3;
```

## PROC CONTENTS

**SAS:**
```sas
PROC CONTENTS DATA=mytable;
RUN;
```

**Snowflake:**
```sql
DESCRIBE TABLE mytable;
-- or
SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'MYTABLE';
```

## PROC PRINT

**SAS:**
```sas
PROC PRINT DATA=sales (OBS=10);
  VAR customer_id amount date;
RUN;
```

**Snowflake:**
```sql
SELECT customer_id, amount, date
FROM sales
LIMIT 10;
```

## PROC TABULATE

**SAS:**
```sas
PROC TABULATE DATA=sales;
  CLASS region year;
  VAR revenue;
  TABLE region, year * revenue * (SUM MEAN);
RUN;
```

**Snowflake:**
```sql
SELECT 
  region,
  year,
  SUM(revenue) AS sum_revenue,
  AVG(revenue) AS mean_revenue
FROM sales
GROUP BY region, year
ORDER BY region, year;
```

## PROC UNIVARIATE

**SAS:**
```sas
PROC UNIVARIATE DATA=sales;
  VAR amount;
  OUTPUT OUT=stats 
    N=n MEAN=mean STD=std 
    MIN=min MAX=max 
    P25=p25 MEDIAN=median P75=p75;
RUN;
```

**Snowflake:**
```sql
CREATE TABLE stats AS
SELECT 
  COUNT(amount) AS n,
  AVG(amount) AS mean,
  STDDEV(amount) AS std,
  MIN(amount) AS min,
  MAX(amount) AS max,
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) AS p25,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY amount) AS median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) AS p75
FROM sales;
```

## PROC COMPARE

**SAS:**
```sas
PROC COMPARE BASE=old COMPARE=new;
  ID customer_id;
RUN;
```

**Snowflake:**
```sql
-- Find differences
SELECT 'In OLD only' AS status, o.* 
FROM old o
LEFT JOIN new n ON o.customer_id = n.customer_id
WHERE n.customer_id IS NULL

UNION ALL

SELECT 'In NEW only' AS status, n.* 
FROM new n
LEFT JOIN old o ON n.customer_id = o.customer_id
WHERE o.customer_id IS NULL

UNION ALL

SELECT 'Different values' AS status, o.*
FROM old o
INNER JOIN new n ON o.customer_id = n.customer_id
WHERE o.amount != n.amount OR o.status != n.status;
```

## PROC IMPORT / PROC EXPORT

**SAS (CSV import):**
```sas
PROC IMPORT DATAFILE='/path/to/file.csv'
  OUT=mydata DBMS=CSV REPLACE;
  GETNAMES=YES;
RUN;
```

**Snowflake:**
```sql
COPY INTO mydata
FROM @my_stage/file.csv
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);
```

**SAS (Excel XLSX import):**
```sas
PROC IMPORT DATAFILE='/path/to/workbook.xlsx'
  OUT=mydata DBMS=XLSX REPLACE;
  SHEET='SheetName';
  GETNAMES=YES;
RUN;
```

**⚠️ Snowflake does NOT support native XLSX in `COPY INTO` / `INFER_SCHEMA`.** Do NOT generate `COPY INTO ... FILE_FORMAT = (TYPE = 'XLSX')` or `INFER_SCHEMA(... .xlsx)` — those fail at runtime. XLSX read/write requires Python (`openpyxl`/`pandas`). Per the SQL-first tiering, this is a **SQL-wrapped Python** case (NOT Tier 3): generate a Python stored procedure with a clean `CALL` interface so the user still executes only SQL.

**Snowflake (XLSX import — stored procedure + CALL, fully parameterized, no hardcoded db/schema/stage):**
```sql
CREATE OR REPLACE PROCEDURE SP_IMPORT_XLSX(
  STAGE_FILE   VARCHAR,   -- e.g. '@my_stage/workbook.xlsx'
  SHEET_NAME   VARCHAR,
  TARGET_TABLE VARCHAR,   -- bare name for temp, or DB.SCHEMA.TABLE for permanent
  IS_TEMP      BOOLEAN DEFAULT FALSE
)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'openpyxl', 'pandas')
HANDLER = 'run'
EXECUTE AS CALLER
AS
$$
def run(session, stage_file, sheet_name, target_table, is_temp):
    import pandas as pd, os
    filename = stage_file.split('/')[-1]
    session.file.get(stage_file, '/tmp')
    df = pd.read_excel(f'/tmp/{filename}', sheet_name=sheet_name, engine='openpyxl', dtype=str)
    df.columns = [c.strip().upper().replace(' ', '_') for c in df.columns]
    df = df.where(pd.notnull(df), other=None)
    session.create_dataframe(df).write.save_as_table(
        target_table, mode='overwrite', table_type=('temporary' if is_temp else None))
    n = session.sql(f"SELECT COUNT(*) FROM {target_table}").collect()[0][0]
    if os.path.exists(f'/tmp/{filename}'): os.remove(f'/tmp/{filename}')
    return f'Loaded {n} rows into {target_table} from sheet {sheet_name}'
$$;

CALL SP_IMPORT_XLSX('@my_stage/workbook.xlsx', 'SheetName', 'MYDATA', FALSE);
```

**Excel import notes:**
- Stage the `.xlsx` file first: `PUT file:///path/to/workbook.xlsx @my_stage/`
- SAS `GETNAMES=YES` (default) → first row is headers (pandas default).
- SAS WORK target → pass `IS_TEMP = TRUE`.
- **Multi-sheet**: one procedure definition, one `CALL` per sheet with different `SHEET_NAME`/`TARGET_TABLE`.
- Flag `MANUAL_REVIEW_REQUIRED` only when merged cells / cell formulas affect business logic.

**SAS (CSV export):**
```sas
PROC EXPORT DATA=mydata
  OUTFILE='/path/to/output.csv' DBMS=CSV REPLACE;
RUN;
```

**Snowflake (CSV/pipe export stays native SQL — no Python needed):**
```sql
COPY INTO @my_stage/output.csv
FROM mydata
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' HEADER = TRUE)
SINGLE = TRUE OVERWRITE = TRUE MAX_FILE_SIZE = 5368709120;
```
- `REPLACE` → `OVERWRITE = TRUE`; `PUTNAMES=NO` → `HEADER = FALSE`; `DELIMITER='|'` → `FIELD_DELIMITER = '|'`.

**SAS (XLSX export):**
```sas
PROC EXPORT DATA=mydata OUTFILE='/path/out.xlsx' DBMS=XLSX REPLACE; SHEET='Sheet1'; RUN;
```

**Snowflake (XLSX export — stored procedure + CALL; never raw `COPY INTO ... XLSX`):**
```sql
CREATE OR REPLACE PROCEDURE SP_EXPORT_XLSX(
  SOURCE_QUERY VARCHAR,   -- e.g. 'SELECT * FROM MYDATA WHERE region = ''EAST'''
  FILE_NAME    VARCHAR,
  SHEET_NAME   VARCHAR DEFAULT 'Sheet1',
  STAGE_PATH   VARCHAR DEFAULT '@~/'  -- pass the target stage from conversion context
)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'openpyxl', 'pandas')
HANDLER = 'run'
EXECUTE AS CALLER
AS
$$
def run(session, source_query, file_name, sheet_name, stage_path):
    import pandas as pd, os
    df = session.sql(source_query).to_pandas()
    local_path = f'/tmp/{file_name}'
    if os.path.exists(local_path):
        with pd.ExcelWriter(local_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as w:
            df.to_excel(w, sheet_name=sheet_name, index=False)
    else:
        df.to_excel(local_path, sheet_name=sheet_name, index=False, engine='openpyxl')
    session.file.put(local_path, stage_path, auto_compress=False, overwrite=True)
    os.remove(local_path)
    return f'Exported {len(df)} rows to {stage_path}/{file_name} sheet {sheet_name}'
$$;

CALL SP_EXPORT_XLSX('SELECT * FROM MYDATA', 'out.xlsx', 'Sheet1', '@my_stage');
```
- Multi-sheet to one workbook: call once per sheet against the SAME `FILE_NAME`; `if_sheet_exists='replace'` keeps re-runs idempotent.
- SAS `DATA=lib.tbl(WHERE=(...))` → fold the filter into `SOURCE_QUERY`.

## PROC REPORT

**SAS:**
```sas
PROC REPORT DATA=sales NOWD;
  COLUMNS region product revenue;
  DEFINE region / GROUP;
  DEFINE product / GROUP;
  DEFINE revenue / ANALYSIS SUM;
  COMPUTE AFTER region;
    LINE 'Subtotal for ' region $20.;
  ENDCOMP;
RUN;
```

**Snowflake (GROUP BY with ROLLUP for subtotals):**
```sql
SELECT
  region,
  product,
  SUM(revenue) AS revenue
FROM sales
GROUP BY ROLLUP(region, product)
ORDER BY region, product;
```

**PROC REPORT notes:**
- PROC REPORT is primarily a **reporting/display** procedure. If it does NOT create an output dataset (no `OUT=`), the conversion may be a no-op (display-only).
- If `OUT=` is present, convert to `CREATE TABLE AS SELECT` with appropriate GROUP BY.
- COMPUTE blocks with LINE statements are display formatting only — omit from SQL conversion.
- COMPUTE blocks with calculated columns → SQL expressions in SELECT.

## Statistical PROCs (TIER 3)

**The following PROCs require Python, not SQL. See `references/python-datascience.md` for conversion patterns:**

| SAS PROC | Python Equivalent | Reference |
|----------|-------------------|-----------|
| PROC REG | `statsmodels.OLS()` | `references/python-datascience.md` |
| PROC GLM | `statsmodels.GLM()` | `references/python-datascience.md` |
| PROC LOGISTIC | `sklearn.LogisticRegression()` | `references/python-datascience.md` |
| PROC CLUSTER | `sklearn.AgglomerativeClustering()` | `references/python-datascience.md` |
| PROC FACTOR | `sklearn.FactorAnalysis()` | `references/python-datascience.md` |
| PROC PHREG | `lifelines.CoxPHFitter()` | Manual review required |
| PROC LIFETEST | `lifelines.KaplanMeierFitter()` | Manual review required |
| PROC MIXED | `statsmodels.MixedLM()` | Manual review required |
| PROC NLIN | `scipy.optimize.curve_fit()` | Manual review required |
| PROC SURVEYSELECT | `sklearn.model_selection` | Manual review required |

Flag these as MANUAL_REVIEW_REQUIRED if no Python conversion is provided.

## PROC FORMAT

**SAS (simple value format):**
```sas
PROC FORMAT;
  VALUE status_fmt
    1 = 'Active'
    2 = 'Inactive'
    3 = 'Pending';
RUN;
```

**Snowflake (use CASE or lookup table):**
```sql
-- Inline CASE (for simple, few values)
SELECT *,
  CASE status
    WHEN 1 THEN 'Active'
    WHEN 2 THEN 'Inactive'
    WHEN 3 THEN 'Pending'
  END AS status_desc
FROM mytable;

-- Lookup table (for reusable or complex formats)
CREATE TABLE status_lookup (code INT, description STRING);
INSERT INTO status_lookup VALUES (1, 'Active'), (2, 'Inactive'), (3, 'Pending');

SELECT t.*, l.description AS status_desc
FROM mytable t
LEFT JOIN status_lookup l ON t.status = l.code;
```

> **Materialize as a queryable TEMPORARY table when a downstream block uses the format.**
> If any later block applies the format via a `PUT()`, `LEFT JOIN`, or CASE-based lookup, create the lookup as a **`CREATE OR REPLACE TEMPORARY TABLE`** (bare name, no schema prefix) — not an in-memory structure (a Python dict, when producing Python, is **not** queryable by downstream SQL). A session-scoped temp table is visible to all later blocks in the same session and can be joined directly.

**SAS (range-based format):**
```sas
PROC FORMAT;
  VALUE age_grp
    LOW - 17 = 'Youth'
    18 - 64 = 'Adult'
    65 - HIGH = 'Senior';
RUN;
```

**Snowflake:**
```sql
CASE 
  WHEN age <= 17 THEN 'Youth'
  WHEN age BETWEEN 18 AND 64 THEN 'Adult'
  WHEN age >= 65 THEN 'Senior'
END AS age_group
```

**SAS (CNTLIN= data-driven format):**
```sas
PROC FORMAT CNTLIN=format_dataset;
RUN;
```

**Snowflake (create lookup table from the format dataset):**
```sql
CREATE OR REPLACE TABLE LKP_MY_FORMAT AS
SELECT 
  START AS code_start,
  END AS code_end,
  LABEL AS description,
  TYPE AS format_type
FROM format_dataset;

-- Usage: JOIN with range conditions
SELECT t.*, l.description
FROM mytable t
LEFT JOIN LKP_MY_FORMAT l 
  ON t.value >= l.code_start AND t.value <= l.code_end;
```

**PROC FORMAT with OTHER= (default):**
- Always include an `ELSE` clause in CASE expressions to handle the OTHER= default
- Preserve inclusive/exclusive range semantics from SAS format definitions

**SAS PUT() with format → Snowflake equivalent:**
```sql
-- SAS: new_col = PUT(status, status_fmt.);
-- Snowflake:
CASE status WHEN 1 THEN 'Active' WHEN 2 THEN 'Inactive' ELSE 'Unknown' END AS new_col
-- OR with lookup table:
l.description AS new_col
```

## Quick Reference Table

| SAS PROC | Snowflake Equivalent |
|----------|---------------------|
| PROC SORT | ORDER BY / QUALIFY ROW_NUMBER() |
| PROC MEANS | GROUP BY with aggregates |
| PROC SUMMARY | GROUP BY with GROUPING SETS |
| PROC FREQ | GROUP BY with COUNT(*) |
| PROC TRANSPOSE | PIVOT / UNPIVOT |
| PROC RANK | RANK() / NTILE() window functions |
| PROC APPEND | INSERT INTO ... SELECT |
| PROC DATASETS DELETE | DROP TABLE |
| PROC CONTENTS | DESCRIBE TABLE |
| PROC PRINT | SELECT ... LIMIT |
| PROC UNIVARIATE | Aggregate + PERCENTILE_CONT |
| PROC COMPARE | EXCEPT / anti-join patterns |
| PROC IMPORT (CSV) | COPY INTO |
| PROC IMPORT (XLSX) | Python stored proc + CALL (openpyxl) — NOT COPY INTO |
| PROC EXPORT (CSV/pipe) | COPY INTO @stage (native SQL) |
| PROC EXPORT (XLSX) | Python stored proc + CALL (openpyxl) — NOT COPY INTO |
| PROC FORMAT | CASE expression / lookup table |
| PROC REPORT | GROUP BY + ROLLUP (or display-only no-op) |
| PROC REG/GLM/etc. | Python (see references/python-datascience.md) |
