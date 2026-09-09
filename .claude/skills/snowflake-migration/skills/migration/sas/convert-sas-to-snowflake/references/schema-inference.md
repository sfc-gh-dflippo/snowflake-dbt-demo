# Schema Inference Rules: SAS to Snowflake Type Mapping

Rules for inferring Snowflake DDL from SAS code constructs. Used by Step 7a (Schema Inference) to auto-generate source table DDL when no real data exists in Snowflake.

---

## SAS Format to Snowflake Type Mapping

### Numeric Formats

| SAS Format / Informat | Snowflake Type | Notes |
|----------------------|----------------|-------|
| `BEST.` / `BESTn.` | `NUMBER(n,0)` | Default integer; `BEST12.` → `NUMBER(12,0)` |
| `n.` (bare numeric, e.g., `8.`) | `NUMBER(n,0)` | SAS width = total digits |
| `n.d` (e.g., `12.2`) | `NUMBER(n,d)` | Width.Decimals → precision,scale |
| `COMMAn.d` | `NUMBER(n,d)` | Display format; same storage as n.d |
| `DOLLARn.d` | `NUMBER(n,d)` | Currency display; same storage |
| `PERCENTn.d` | `NUMBER(n,d)` | Percentage display; same storage |
| `Ew.d` (scientific) | `FLOAT` | Scientific notation → floating point |
| `(no format specified, numeric)` | `FLOAT` | Default for unformatted numerics |

### Character Formats

| SAS Format / Informat | Snowflake Type | Notes |
|----------------------|----------------|-------|
| `$n.` (e.g., `$50.`) | `VARCHAR(n)` | SAS char width → VARCHAR length |
| `$CHARn.` | `VARCHAR(n)` | Preserves leading/trailing blanks |
| `$VARYINGn.` | `VARCHAR(n)` | Variable-length character |
| `$UPCASEn.` | `VARCHAR(n)` | Uppercase format; apply UPPER() in transform |
| `$HEXn.` | `VARCHAR(n)` | Hex representation |
| `(no format specified, character)` | `VARCHAR(256)` | Default for unformatted characters |

### Date / Time Formats

| SAS Format / Informat | Snowflake Type | Notes |
|----------------------|----------------|-------|
| `MMDDYYn.` / `MMDDYY10.` | `DATE` | MM/DD/YYYY |
| `YYMMDDn.` / `YYMMDD10.` | `DATE` | YYYY-MM-DD |
| `DATEn.` / `DATE9.` | `DATE` | DDMonYYYY (e.g., 01JAN2024) |
| `DDMMYYn.` | `DATE` | DD/MM/YYYY |
| `MONYY.` / `MONYY7.` | `DATE` | MonYYYY (e.g., JAN2024) |
| `JULIAN.` / `JULIANn.` | `DATE` | Julian date |
| `DATETIME.` / `DATETIMEn.` | `TIMESTAMP_NTZ` | SAS datetime (seconds since 1960-01-01) |
| `TIME.` / `TIMEn.` | `TIME` | SAS time (seconds since midnight) |
| `DTDATE.` | `DATE` | Date portion of datetime |
| `ANYDTDTE.` / `ANYDTDTM.` | `DATE` / `TIMESTAMP_NTZ` | Auto-detect date/datetime |
| `YYMMN.` / `YYMMN6.` | `VARCHAR(6)` | Period key: YYYYMM (not a date — preserve as string) |
| `(no format, but used in date functions)` | `DATE` | If column appears in INTCK/INTNX/DATEPART |

---

## PROC IMPORT Inference Rules

When parsing `PROC IMPORT` statements:

| PROC IMPORT Attribute | Inference Rule |
|----------------------|----------------|
| `DBMS=XLSX` / `DBMS=XLS` | Excel source; table name = SHEET= value or OUT= dataset name |
| `DBMS=CSV` | CSV source; all columns default to `VARCHAR(256)` unless refined by subsequent DATA step |
| `DBMS=DLM` | Delimited file; use DELIMITER= to identify separator |
| `GETNAMES=YES` | Column names come from first row (cannot infer types without data) |
| `GETNAMES=NO` | Columns are positional: VAR1, VAR2, ...; all VARCHAR(256) |
| `DATAROW=n` | Data starts at row n; header at row n-1 if GETNAMES=YES |
| `SHEET="name"` | Table name candidate = sanitized sheet name |
| `OUT=lib.dataset` | Output table name; lib maps to Snowflake schema |
| `RANGE="A1:Z100"` | Limits column/row range; infer column count from range |

**When column types cannot be determined from PROC IMPORT alone**, check for subsequent DATA step or PROC SQL that reads the imported table — those often apply explicit FORMAT/INFORMAT statements or WHERE conditions that reveal types.

---

## INFILE / INPUT Statement Inference Rules

Parse the INPUT statement following INFILE to extract column definitions:

### Column-Pointer INPUT

```sas
INPUT @1 ACCT_NUM $20. @21 BALANCE 12.2 @33 OPEN_DATE MMDDYY10.;
```

| Component | Inference |
|-----------|-----------|
| `@n` | Column position (absolute pointer) — skip for DDL |
| `varname $n.` | `VARCHAR(n)` |
| `varname n.d` | `NUMBER(n,d)` |
| `varname informat.` | Apply Date/Time mapping table above |

### List INPUT (space-delimited)

```sas
INPUT ACCT_NUM $ BALANCE OPEN_DATE :MMDDYY10.;
```

| Component | Inference |
|-----------|-----------|
| `varname $` | `VARCHAR(256)` (no width → default) |
| `varname` (no $) | `FLOAT` (no format → numeric default) |
| `varname :informat.` | Apply format mapping with colon modifier |

### Named INPUT

```sas
INPUT ACCT_NUM= BALANCE= OPEN_DATE=;
```

All columns `VARCHAR(256)` unless subsequent FORMAT/INFORMAT statement clarifies types.

---

## PROC SQL CREATE TABLE Inference

Direct DDL extraction — these map cleanly:

| SAS SQL Type | Snowflake Type |
|-------------|----------------|
| `CHAR(n)` / `CHARACTER(n)` | `VARCHAR(n)` |
| `VARCHAR(n)` | `VARCHAR(n)` |
| `INTEGER` / `INT` | `INTEGER` |
| `SMALLINT` | `SMALLINT` |
| `FLOAT` / `REAL` / `DOUBLE` | `FLOAT` |
| `NUMERIC(p,s)` / `DECIMAL(p,s)` | `NUMBER(p,s)` |
| `DATE` | `DATE` |
| `TIMESTAMP` | `TIMESTAMP_NTZ` |

---

## Fallback Rules

When type cannot be inferred from any SAS construct:

| Scenario | Default Type |
|----------|-------------|
| Column name contains `_ID`, `_KEY`, `_NUM`, `_CODE` | `VARCHAR(50)` |
| Column name contains `_AMT`, `_BAL`, `_RATE`, `_PCT` | `NUMBER(18,4)` |
| Column name contains `_DT`, `_DATE` | `DATE` |
| Column name contains `_TS`, `_TIMESTAMP`, `_DTTM` | `TIMESTAMP_NTZ` |
| Column name contains `_DESC`, `_NAME`, `_LABEL` | `VARCHAR(500)` |
| Column name contains `_FLAG`, `_IND` | `VARCHAR(1)` |
| Column referenced only in WHERE with numeric comparison | `FLOAT` |
| Column referenced only in WHERE with string comparison | `VARCHAR(256)` |
| No heuristic matches | `VARIANT` |

---

## Output Format

Generate one DDL file per pipeline phase (or one consolidated file), with comments tracing each table back to its SAS source:

```sql
-- ============================================================
-- Auto-generated source table DDL
-- Inferred from SAS code: Phase 1 (01 through 50)
-- Generated by: /convert-sas-to-snowflake Step 7a
-- ============================================================

-- Source: 01_import_excel_data.sas (PROC IMPORT, SHEET="Customers")
CREATE TABLE IF NOT EXISTS TARGET_SCHEMA.WK_CUSTOMER_DIM (
  CUSTOMER_ID VARCHAR(50),    -- inferred: _ID suffix
  CUSTOMER_NAME VARCHAR(500), -- inferred: _NAME suffix
  REGION VARCHAR(50),         -- inferred: no format, char context
  AMOUNT_A NUMBER(12,2),      -- inferred: subsequent FORMAT 12.2
  AMOUNT_B NUMBER(12,2),      -- inferred: subsequent FORMAT 12.2
  DISCOUNT_RATE NUMBER(18,4), -- inferred: _RATE suffix
  UNIT_RATE NUMBER(18,4),     -- inferred: _RATE suffix
  EFFECTIVE_DATE DATE          -- inferred: _DATE suffix
);
```
