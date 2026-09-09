# Validation Execution: Phases 3A, 3B, and 4

## When to Load

Load this file at Step 7 (Phase 2: SAS Logic Trace — runs as part of Local LLM Tracing Validation) and Step 9 (Phase 4: Snowflake Execution and comparison). Referenced from SKILL.md Step 7b and `workflows/steps-8-10-post-conversion.md` Step 9.

---

### Phase 3A: Generate Expected Baseline (SAS Logic Trace)

This is the core validation capability. Manually trace the original SAS code against the synthetic data to produce expected output.

#### 3A.1 Read Inputs

1. Read the original SAS code (block by block)
2. Read the synthetic data from the pandas DataFrames (or from CSV files):

```python
customers_df = pd.read_csv('tests/<script>/synthetic_data/customers.csv')
orders_df = pd.read_csv('tests/<script>/synthetic_data/orders.csv')
```

#### 3A.2 Trace SAS Logic Row-by-Row

For each SAS block that produces an output table:

**DATA Step tracing rules:**
1. Initialize the PDV (Program Data Vector) with all variables
2. Process each input row according to SET/MERGE/INPUT statement
3. Apply SAS missing value semantics:
   - Missing numeric (`.`) is less than ANY number (including negative)
   - Missing + value = missing (SAS sum statement `x + y;` is the exception -- it treats missing as 0)
   - IF condition with missing: `IF x > 0` is FALSE when x is missing
4. Track RETAIN values across iterations (do NOT reset to missing)
5. Apply FIRST./LAST. flags based on BY-group boundaries
6. Execute OUTPUT/DELETE/RETURN/STOP behavior
7. At end of DATA step iteration, implicit OUTPUT if no explicit OUTPUT statement

**PROC SQL tracing rules:**
1. Execute the SQL logic mentally against the synthetic data
2. Follow standard SQL semantics (not SAS DATA step semantics)
3. NULL handling follows SQL rules (NULL in comparison = unknown)

**MERGE tracing rules:**
1. Both datasets MUST be sorted by BY variables
2. MERGE is NOT a SQL JOIN -- it interleaves records within BY-groups
3. One-to-one: matched rows combine, unmatched rows fill with missing
4. One-to-many: the single row is repeated for each row in the many-side
5. Many-to-many: SAS processes row-by-row within the BY-group (NOT a Cartesian product)
6. IN= flags: track which dataset contributed each row

#### 3A.3 Produce Expected Output (Local)

For each output table, present the expected result as a table:

```
Expected output for OUTPUT_TABLE (traced from SAS logic):

| ID | NAME   | TOTAL_AMOUNT | REGION |
|----|--------|-------------|--------|
| 1  | Alice  | 350.50      | EAST   |
| 2  | Bob    | 65.00       | WEST   |
| 3  | Carol  | 0           | EAST   |
| 4  | Dave   | NULL        | SOUTH  |
```

Then create as a pandas DataFrame and persist:

```python
expected_output = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'NAME': ['Alice', 'Bob', 'Carol', 'Dave'],
    'TOTAL_AMOUNT': [350.50, 65.00, 0, None],
    'REGION': ['EAST', 'WEST', 'EAST', 'SOUTH']
})
expected_output.to_csv('tests/<script>/expected/expected_output.csv', index=False)
```

Also write a `.sql` reference file (NOT executed):
```sql
-- Expected baseline for: OUTPUT_TABLE
-- Traced from SAS logic on synthetic data
-- NOTE: This SQL is for REFERENCE ONLY. Testing runs locally.

CREATE OR REPLACE TEMPORARY TABLE expected_output (
  ID NUMBER, NAME VARCHAR, TOTAL_AMOUNT NUMBER(10,2), REGION VARCHAR
);
INSERT INTO expected_output VALUES
  (1, 'Alice', 350.50, 'EAST'),
  (2, 'Bob', 65.00, 'WEST'),
  (3, 'Carol', 0, 'EAST'),
  (4, 'Dave', NULL, 'SOUTH');
```

**Persist**: Write CSV to `tests/<script_name>/expected/expected_<output_name>.csv`.
Write SQL reference to `tests/<script_name>/expected/expected_<output_name>.sql`.

**STOP**: Show user the expected output for review. Ask:
```
Does this expected output look correct based on the original SAS logic?
1. Yes, proceed with Snowflake compilation and execution
2. No, let me correct the expected values
3. Skip baseline comparison (smoke test only)
```

If user selects option 3, fall back to smoke-test-only mode (basic checks, no comparison).

---

### Phase 3B: Execute Converted SQL on Snowflake

**REQUIRED**: Read `references/snowflake-execution.md` before executing.

#### 3B.1 Run the Conversion on Snowflake

Execute converted SQL against synthetic data on Snowflake using `snowflake_sql_execute`.

1. Create temporary tables from `source_table_ddl.sql`
2. Load synthetic data from `synthetic_data.sql`
3. Execute each converted SQL file in dependency order
4. Capture output tables

#### 3B.2 Capture Actual Output

Query each output table and capture results for comparison against expected baselines.

#### 3B.3 Handle Errors

**If execution error:**
1. Capture full error message
2. **STOP** - Present error to user
3. Do NOT attempt automatic fixes

```
SNOWFLAKE EXECUTION FAILED

Error: [error message]

The converted code failed during Snowflake execution.
This may indicate:
- Missing table dependencies
- Column name mismatches
- Type conversion errors

Options:
1. Review the error and adjust test data
2. Examine the original SAS code
3. Abort validation
```

**STOP**: Wait for user guidance. Do NOT auto-retry.

---

### Phase 4: Compare Expected vs Actual (Local)

**REQUIRED**: Read `references/comparison-rules.md` before executing comparisons.

For each output table, execute three levels of comparison using pandas:

#### 4.1 Schema Comparison

```python
def compare_schemas(expected_df, actual_df):
    expected_cols = list(expected_df.columns)
    actual_cols = list(actual_df.columns)

    results = {
        'column_count_match': len(expected_cols) == len(actual_cols),
        'column_names_match': [c.upper() for c in expected_cols] == [c.upper() for c in actual_cols],
        'expected_columns': expected_cols,
        'actual_columns': actual_cols,
        'missing_in_actual': [c for c in expected_cols if c.upper() not in [a.upper() for a in actual_cols]],
        'extra_in_actual': [c for c in actual_cols if c.upper() not in [e.upper() for e in expected_cols]],
    }
    return results
```

Check:
- Column count matches
- Column names match (case-insensitive)
- Column order matches
- Column types are compatible (per comparison-rules.md type compatibility matrix)

#### 4.2 Row Count Comparison

```python
expected_rows = len(expected_df)
actual_rows = len(actual_df)
```

If counts differ, classify the likely cause:
- actual > expected: possible many-to-many join explosion or missing DISTINCT
- actual < expected: possible incorrect INNER JOIN (should be LEFT/FULL) or extra WHERE filter
- actual = 0: execution produced no output (likely error in logic)

#### 4.3 Value Comparison

**Step 1: Exact match check (fast path)**

```python
import numpy as np

def dataframes_match(expected_df, actual_df, key_cols=None):
    if key_cols:
        expected_sorted = expected_df.sort_values(key_cols).reset_index(drop=True)
        actual_sorted = actual_df.sort_values(key_cols).reset_index(drop=True)
    else:
        expected_sorted = expected_df.reset_index(drop=True)
        actual_sorted = actual_df.reset_index(drop=True)

    try:
        pd.testing.assert_frame_equal(
            expected_sorted, actual_sorted,
            check_dtype=False,
            check_exact=False,
            atol=1e-10,
            rtol=1e-5
        )
        return True, []
    except AssertionError:
        return False, get_column_diffs(expected_sorted, actual_sorted)
```

If match = True AND row counts match, the table PASSES. Skip detailed comparison.

**Step 2: If mismatches found, do column-level diff**

```python
def get_column_diffs(expected_df, actual_df):
    mismatches = []
    for col in expected_df.columns:
        if col not in actual_df.columns:
            mismatches.append({'column': col, 'type': 'missing_column'})
            continue
        for idx in range(min(len(expected_df), len(actual_df))):
            e_val = expected_df[col].iloc[idx]
            a_val = actual_df[col].iloc[idx]
            if not values_equivalent(e_val, a_val):
                mismatches.append({
                    'row': idx + 1,
                    'column': col,
                    'expected': e_val,
                    'actual': a_val,
                    'cause': classify_mismatch(e_val, a_val)
                })
    return mismatches

def values_equivalent(e_val, a_val):
    if pd.isna(e_val) and pd.isna(a_val):
        return True
    if pd.isna(e_val) and a_val == '':
        return True
    if e_val == '' and pd.isna(a_val):
        return True
    try:
        if abs(float(e_val) - float(a_val)) < 1e-10:
            return True
    except (ValueError, TypeError):
        pass
    return str(e_val).strip() == str(a_val).strip()
```

#### 4.4 Classify Mismatches

For each mismatch found, classify using the table in comparison-rules.md:

| Mismatch Pattern | Likely Root Cause |
|------------------|-------------------|
| NULL vs non-NULL | Missing value handling error |
| NULL vs empty string | Character missing value conversion |
| Row count actual > expected | Many-to-many join |
| Row count actual < expected | Incorrect JOIN type or extra filter |
| Numeric diff < 0.01 | Float precision (likely acceptable) |
| Numeric diff > 0.01 | Wrong aggregation or missing COALESCE |
| Date off by 1 | INTNX alignment parameter |
| Values shifted by N rows | Window function frame error |
| Duplicate rows | Missing DISTINCT or QUALIFY |
| Column missing | KEEP/DROP/RENAME not translated |
