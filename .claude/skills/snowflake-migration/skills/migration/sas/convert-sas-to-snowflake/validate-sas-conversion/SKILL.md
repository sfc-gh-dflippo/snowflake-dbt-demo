---
name: validate-sas-conversion
parent_skill: sas
description: |
  Preview. Validate a completed SAS to Snowflake conversion by comparing expected SAS output
  against actual converted SQL output using synthetic test data. Performs
  dual-execution comparison: LLM traces original SAS logic to produce baseline, then
  runs converted SQL on Snowflake and compares outputs cell-by-cell.
  Triggers: validate conversion, verify sas migration, test conversion, compare sas output.
license: Proprietary. See License-Skills for complete terms
---

# Validate SAS to Snowflake Conversion

Dual-execution comparison framework: LLM traces SAS logic to produce expected baselines, then executes converted SQL on Snowflake and compares.

## Execution Model

| Component | Engine | Snowflake? |
|-----------|--------|------------|
| Synthetic data generation | LLM + SQL | Yes (temp tables) |
| SAS logic trace (expected baseline) | LLM | No |
| Converted SQL execution | Snowflake | Yes |
| Output comparison | SQL MINUS/EXCEPT | Yes |
| Artifact persistence | CSV + SQL files to disk | No |

**Snowflake is used for execution** with explicit credit confirmation per Snowflake Interaction Policy.

## When to Load

[convert-sas-to-snowflake] Step 8: After user opts to validate conversion, or when user explicitly requests validation of existing converted code.

## Arguments

- `$CONVERTED_CODE` - Path to converted `.sql` file or SQL code to validate
- `$ORIGINAL_SAS` - Path to original SAS code (REQUIRED for baseline generation)

## Rules

1. **Never modify the converted code** - Create test wrapper/harness separately
2. **Original SAS code is REQUIRED** - Cannot generate baseline without it
3. **Schema inference** - Derive from SQL CREATE statements, SELECT columns, or original SAS
4. **Persist all test artifacts** - Save synthetic data, expected baselines, actual results, and validation reports to disk subfolders (see Artifact Persistence below)
5. **Load reference files** - Read `references/synthetic-data-rules.md` and `references/comparison-rules.md` before generating data or comparing
6. **Snowflake execution** - All SQL execution runs on Snowflake with explicit credit confirmation per Snowflake Interaction Policy.

## Artifact Persistence

All test artifacts MUST be persisted to disk in the conversion output directory. This enables reproducibility, audit trails, and inclusion in the conversion report.

### Directory Structure

Create the following subfolder structure relative to the conversion output directory (same directory as the generated `.sql` files):

```
<output_dir>/
├── extract.sql                          # converted code
├── transform.sql                        # converted code
├── tests/
│   ├── extract/
│   │   ├── synthetic_data/
│   │   │   ├── customers.csv            # pandas DataFrame exported as CSV
│   │   │   ├── customers.sql            # SQL reference (CREATE + INSERT, not executed)
│   │   │   ├── orders.csv               # pandas DataFrame exported as CSV
│   │   │   ├── orders.sql               # SQL reference (CREATE + INSERT, not executed)
│   │   │   └── _manifest.md             # table names, row counts, key coverage summary
│   │   ├── expected/
│   │   │   ├── expected_output.csv      # expected baseline from SAS logic trace
│   │   │   └── expected_output.sql      # SQL reference (not executed)
│   │   ├── actual/
│   │   │   ├── actual_output.csv        # Snowflake execution result
│   │   │   └── actual_summary.csv       # one file per actual output table
│   │   └── validation_report.md         # per-script validation report (Phase 5 output)
│   ├── transform/
│   │   ├── synthetic_data/
│   │   │   └── ...
│   │   ├── expected/
│   │   │   └── ...
│   │   ├── actual/
│   │   │   └── ...
│   │   └── validation_report.md
│   └── _test_summary.md                 # cross-file test summary
├── conversion_report.md                 # final conversion report
└── conversion_report.docx               # DOCX copy of conversion report
```

### Persistence Rules

| Artifact | Format | When to Write | Contents |
|----------|--------|---------------|----------|
| Synthetic data | `.csv` + `.sql` | Phase 2.4 (after generating DataFrames) | CSV for local testing; SQL for reference/future Snowflake use |
| Manifest | `_manifest.md` | Phase 2.4 | Table list, row counts, key coverage, edge case checklist |
| Expected baseline | `.csv` + `.sql` | Phase 3A.3 (after LLM trace) | CSV for comparison; SQL for reference |
| Actual results | `.csv` | Phase 3B.2 (after Snowflake execution) | CSV export of Snowflake result |
| Validation report | `.md` | Phase 5 (after comparison) | Full diff report for this script |
| Test summary | `_test_summary.md` | After all scripts validated | Cross-file pass/fail summary |

### Writing Synthetic Data Files

For each input table, write BOTH a `.csv` (for local testing) and a `.sql` (for reference):

```python
import pandas as pd

customers_df = pd.DataFrame({
    'ID': [1, 2, 2, 3, 4, 5],
    'NAME': ['Alice', 'Bob', 'Bob Jr', 'Carol', 'Dave', None],
    'REGION': ['EAST', 'WEST', 'WEST', 'EAST', 'SOUTH', None]
})

customers_df.to_csv('tests/<script>/synthetic_data/customers.csv', index=False)
```

Also write a `.sql` reference file (NOT executed against Snowflake):

```sql
-- Synthetic data for: customers
-- Generated for: extract.sas validation
-- Rows: 6
-- Key coverage: JOIN keys (3 matching, 1 left-only, 1 right-only, 1 duplicate)
-- NOTE: This SQL is for REFERENCE ONLY. Testing runs on Snowflake.

CREATE OR REPLACE TEMPORARY TABLE customers (
  id NUMBER,
  name VARCHAR,
  region VARCHAR
);

INSERT INTO customers VALUES
  (1, 'Alice', 'EAST'),
  (2, 'Bob', 'WEST'),
  (2, 'Bob Jr', 'WEST'),
  (3, 'Carol', 'EAST'),
  (4, 'Dave', 'SOUTH'),
  (5, NULL, NULL);
```

---

## Workflow

### Phase 1: Analyze Dependencies

#### 1.1 Identify Input Tables

Parse BOTH the converted Snowflake code AND the original SAS code to find:

**From converted SQL:**
```sql
SELECT ... FROM table_name
JOIN table_name
IDENTIFIER(:param)
```

**From original SAS:**
```sas
SET dataset_name;
MERGE dataset1 dataset2;
PROC SQL; SELECT ... FROM table;
```

**For each table, capture:**
- Table name (as used in both SAS and Snowflake code)
- Columns referenced (SELECT, WHERE, JOIN, BY, GROUP BY)
- Data types (from CAST, LENGTH, FORMAT, or usage context)
- Role: input-only, output-only, or intermediate (created by one block, read by another)

#### 1.2 Identify Output Tables

Determine which tables the code creates as final output:
- `CREATE TABLE output_name AS ...`
- `INSERT INTO output_name ...`
- SAS: `DATA output_name;`
- Exclude intermediate/temp tables used only between blocks

#### 1.3 Determine Test Mode

Since all testing runs locally, there is no need to check Snowflake for table existence. All input data will be synthetic.

```
LOCAL VALIDATION MODE

All testing runs on Snowflake with synthetic data.
Credit impact: Moderate (execution against test data).

Input tables to generate (synthetic):
  - TABLE1 (inferred: col1 VARCHAR, col2 NUMBER)
  - TABLE2 (inferred: id NUMBER, name VARCHAR)

Proceed with synthetic data generation? [Yes] / [No - Abort]
```

**STOP**: Wait for user confirmation.

---

### Phase 2: Generate Smart Synthetic Data

**REQUIRED**: Read `references/synthetic-data-rules.md` before generating any data.

#### 2.1 Infer Schema

**From SQL code:**
```sql
-- SELECT col1, col2, col1 + col2 AS total FROM t
-- Inference: col1 NUMBER, col2 NUMBER

-- WHERE name = 'value' AND date_col > '2024-01-01'
-- Inference: name VARCHAR, date_col DATE

-- JOIN t2 ON t1.id = t2.id
-- Inference: id column, likely NUMBER
```

**From original SAS (if provided):**
```sas
LENGTH name $50 amount 8 date_col 8;
/* Inference: name VARCHAR(50), amount NUMBER, date_col DATE */

FORMAT date_col DATE9.;
/* Confirms: date_col is a DATE */
```

**Type inference rules:**

| Pattern | Inferred Type |
|---------|--------------|
| `col = 'string'` | VARCHAR |
| `col > 0`, `col + n` | NUMBER |
| `col > '2024-01-01'` | DATE |
| `CAST(col AS INT)` | NUMBER |
| `TO_DATE(col)` | DATE |
| `LENGTH(col)` | VARCHAR |
| SAS `LENGTH x 8` | NUMBER |
| SAS `LENGTH x $n` | VARCHAR(n) |
| SAS `FORMAT x DATE9.` | DATE |

#### 2.2 Generate Join-Aware Synthetic Data

Follow `references/synthetic-data-rules.md` strictly. For every JOIN/MERGE:

1. **Matching keys** in both tables (at least 3 shared key values)
2. **Left-only key** (present in left table, absent in right)
3. **Right-only key** (present in right table, absent in left)
4. **Duplicate key** (same key value with multiple rows on one side)
5. **Many-to-many key** (duplicate on BOTH sides -- if SAS MERGE is involved)

#### 2.3 Include SAS Edge Cases

Every table MUST include:
- At least one row with NULL in numeric columns (SAS missing `.`)
- At least one row with NULL or empty string in character columns
- At least one zero value (zero is NOT missing in SAS)
- At least one negative number
- Boundary dates if date logic is present (year-start, year-end)

For BY-group processing: at least one group with 3+ rows (to test FIRST./LAST.)
For RETAIN/LAG: at least 2 partitions with 4+ rows each.

#### 2.4 Create Test Data Locally and Persist to Disk

Generate pandas DataFrames for each input table. Write to disk as both `.csv` (for local testing) and `.sql` (for reference/future Snowflake use).

```python
import pandas as pd

customers_df = pd.DataFrame({
    'ID': [1, 2, 2, 3, 4, 5],
    'NAME': ['Alice', 'Bob', 'Bob Jr', 'Carol', 'Dave', None],
    'REGION': ['EAST', 'WEST', 'WEST', 'EAST', 'SOUTH', None]
})

customers_df.to_csv('tests/<script>/synthetic_data/customers.csv', index=False)
```

**Persist**: Write each DataFrame to `tests/<script_name>/synthetic_data/<table_name>.csv`.
Also write `.sql` reference files (NOT executed).
Write `tests/<script_name>/synthetic_data/_manifest.md` with table inventory and key coverage.

**STOP**: Show user the test data and confirm before proceeding.

```
Test data generated LOCALLY (no Snowflake):
  - CUSTOMERS (6 rows): id, name, region
  - ORDERS (7 rows): order_id, customer_id, amount, order_date

Key coverage:
  - JOIN keys: 3 matching, 1 left-only, 1 right-only, 1 duplicate
  - NULL rows: 1 per table
  - Boundary values: zero amount, negative amount, year-end date

Saved to: tests/extract/synthetic_data/
  - customers.csv, customers.sql
  - orders.csv, orders.sql
  - _manifest.md

Ready to generate expected baseline and execute converted code locally?
```

---

**Load `references/validation-execution.md`** for Phases 3A (Expected Baseline Generation), 3B (Snowflake Execution), and 4 (Expected vs Actual Comparison).

---

### Phase 5: Structured Diff Report

#### 5.1 Full Comparison Report

**Persist**: Write the full report below to `tests/<script_name>/validation_report.md`.

```
════════════════════════════════════════════════════════════════════
VALIDATION REPORT: SAS vs SNOWFLAKE COMPARISON (LOCAL)
════════════════════════════════════════════════════════════════════

Source: <original_sas_file>
Target: <converted_sql_file>
Test Data: Synthetic (5-8 rows per table)
Execution Engine: Snowflake (synthetic test data)

INPUT TABLES:
  - CUSTOMERS (6 rows)
  - ORDERS (7 rows)

────────────────────────────────────────────────────────────────────
OUTPUT TABLE: SUMMARY
────────────────────────────────────────────────────────────────────
  Schema:    PASS  (4/4 columns match)
  Row Count: PASS  (expected: 4, actual: 4)
  Values:    PASS  (0 mismatches)
  Result:    PASS

────────────────────────────────────────────────────────────────────
OUTPUT TABLE: DETAIL
────────────────────────────────────────────────────────────────────
  Schema:    PASS  (6/6 columns match)
  Row Count: FAIL  (expected: 5, actual: 7)
             Likely cause: JOIN produced extra rows (many-to-many?)
  Values:    FAIL  (3 mismatches)
  Result:    FAIL

  Mismatches:
  ┌─────┬──────────────┬──────────────┬──────────────┬────────────────────────┐
  │ Row │ Column       │ Expected     │ Actual       │ Likely Cause           │
  ├─────┼──────────────┼──────────────┼──────────────┼────────────────────────┤
  │ 2   │ TOTAL_AMOUNT │ 150.00       │ 150.50       │ Float precision        │
  │ 3   │ STATUS       │ NULL         │ ''           │ Missing vs empty str   │
  │ 5   │ REGION       │ SOUTH        │ NULL         │ Missing value handling │
  └─────┴──────────────┴──────────────┴──────────────┴────────────────────────┘

════════════════════════════════════════════════════════════════════
OVERALL: 1 of 2 output tables PASSED
════════════════════════════════════════════════════════════════════

Suggested Fixes:
1. Row count mismatch in DETAIL: Check if SAS MERGE BY should be
   translated as LEFT JOIN with QUALIFY ROW_NUMBER() = 1 instead
   of plain JOIN
2. NULL vs empty string: Add NULLIF('', '') or CASE expression
   for character missing values
3. Float precision: Consider ROUND(amount, 2) if currency column
```

#### 5.2 Smoke-Test-Only Report (when baseline was skipped)

If user opted out of baseline comparison in Phase 3A:

```
════════════════════════════════════════════════════════════════════
VALIDATION REPORT: SAS CONVERSION (SMOKE TEST - LOCAL)
════════════════════════════════════════════════════════════════════

Converted Code: <filename.sql>
Execution Engine: Snowflake
Execution Status: SUCCESS

Test Data Generated:
  - CUSTOMERS (6 rows)
  - ORDERS (7 rows)

Output DataFrames Created:
  - SUMMARY (4 rows)
  - DETAIL (7 rows)

Basic Checks:
  Row counts:      Non-zero
  Key uniqueness:  No unexpected duplicates
  NULL counts:     Within expected range
  Join explosion:  Not detected

Sample Output (SUMMARY):
┌────┬──────┬──────────────┬────────┐
│ ID │ NAME │ TOTAL_AMOUNT │ REGION │
├────┼──────┼──────────────┼────────┤
│ 1  │ Alice│ 350.50       │ EAST   │
│ 2  │ Bob  │ 65.00        │ WEST   │
└────┴──────┴──────────────┴────────┘

NOTE: No baseline comparison performed. Only execution success verified.
════════════════════════════════════════════════════════════════════
```

---

### Phase 6: Write Test Summary and Cleanup

#### 6.0 Write Cross-File Test Summary

After all scripts have been validated, write `tests/_test_summary.md`:

```markdown
# Test Summary

| Script | Synthetic Data | Expected Baseline | Execution | Comparison | Result |
|--------|---------------|-------------------|-----------|------------|--------|
| extract.sas | tests/extract/synthetic_data/ | tests/extract/expected/ | tests/extract/actual/ | PASS | PASS |
| transform.sas | tests/transform/synthetic_data/ | tests/transform/expected/ | tests/transform/actual/ | FAIL | FAIL |
```

#### 6.1 Cleanup

Local testing artifacts (DataFrames) are ephemeral -- they are garbage collected when the Python process ends. No Snowflake temp tables to clean up.

Disk artifacts persist at `tests/<script>/` for audit and reproducibility:
  - `synthetic_data/*.csv`, `*.sql`
  - `expected/*.csv`, `*.sql`
  - `actual/*.csv`
  - `validation_report.md`

```
Validation complete (ran locally -- no Snowflake credits consumed).

Disk artifacts saved to: tests/
  (synthetic data, expected baselines, actual results, validation reports)

Options:
  1. Keep all disk artifacts (default, recommended for audit trail)
  2. Delete disk artifacts
```

---

## Fallback Escalation: Constructs Requiring Special Handling

Some Snowflake-specific constructs may require additional setup:

**Constructs that need stored procedure execution context:**
- Snowflake Scripting (`DECLARE ... BEGIN ... END`, stored procedures)
- `IDENTIFIER()` dynamic references
- Session variables (`$VAR_NAME`)

**When a construct requires special handling:**
1. Ensure stored procedures are created before execution
2. Set session variables via `SET` before running the SQL
3. Present any execution plan to user for confirmation

---

## Stopping Points

- Phase 1.3: After determining test mode - user confirms synthetic data generation
- Phase 2.4: After generating test data locally - confirm data looks correct
- Phase 3A.3: After generating expected output - user reviews baseline
- Phase 3B.3: On execution error or Snowflake fallback - present options, wait for guidance
- Phase 5: After report - present results
- Phase 6.1: Disk artifact cleanup choice

## Success Criteria

- All input tables identified and generated as pandas DataFrames
- Expected baseline generated from SAS logic trace and user-reviewed
- Converted code executes successfully on Snowflake
- All output tables have matching schema (column names, types, order)
- All output tables have matching row counts
- All output tables have matching values (within tolerance rules)
- Structured diff report produced with root cause classification
- All test artifacts persisted to tests/<script>/ subfolders (CSV + SQL reference)
- Cross-file test summary written to tests/_test_summary.md
- No unnecessary Snowflake credits consumed (uses temporary objects, auto-dropped)

---

## Quick Validation Example

**Original SAS:**
```sas
DATA output;
  MERGE customers(IN=a) orders(IN=b);
  BY id;
  IF a;
  total = amount;
  IF total = . THEN total = 0;
RUN;
```

**Converted SQL:**
```sql
CREATE OR REPLACE TABLE output AS
SELECT c.id, c.name, COALESCE(o.amount, 0) AS total
FROM customers c
LEFT JOIN orders o ON c.id = o.id;
```

**Synthetic Data (pandas):**
```python
customers_df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', None]})
orders_df = pd.DataFrame({'id': [1, 1, 4], 'amount': [100, 50, 200]})
```

**Phase 3A - Expected (SAS trace):**
SAS MERGE BY id with IN=a (keep only customers):
- id=1: Alice + amount=100 (first match), total=100 -> OUTPUT
- id=1: Alice + amount=50 (second match, SAS overwrites), total=50 -> OUTPUT
- id=2: Bob + missing amount, total=. -> IF total=. THEN total=0 -> total=0 -> OUTPUT
- id=3: NULL name + no match, total=. -> total=0 -> OUTPUT
- id=4: NOT in customers (a=0), skip

Expected:
| ID | NAME  | TOTAL |
|----|-------|-------|
| 1  | Alice | 100   |
| 1  | Alice | 50    |
| 2  | Bob   | 0     |
| 3  | NULL  | 0     |

**Phase 3B - Actual (Snowflake):**
Execute on Snowflake:
```sql
CREATE OR REPLACE TEMPORARY TABLE customers (id NUMBER, name VARCHAR);
INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob'), (3, NULL);

CREATE OR REPLACE TEMPORARY TABLE orders (id NUMBER, amount NUMBER);
INSERT INTO orders VALUES (1, 100), (1, 50), (4, 200);

CREATE OR REPLACE TABLE output AS
SELECT c.id, c.name, COALESCE(o.amount, 0) AS total
FROM customers c
LEFT JOIN orders o ON c.id = o.id;
```
LEFT JOIN produces:
| ID | NAME  | TOTAL |
|----|-------|-------|
| 1  | Alice | 100   |
| 1  | Alice | 50    |
| 2  | Bob   | 0     |
| 3  | NULL  | 0     |

**Phase 4 - Comparison (pandas):**
Schema: PASS, Rows: PASS (4=4), Values: PASS

**Note:** If the converted SQL had used INNER JOIN instead of LEFT JOIN, id=2 and id=3 would be missing from actual output -- the comparison would catch this as a row count mismatch (expected: 4, actual: 2) and flag "Incorrect JOIN type."
