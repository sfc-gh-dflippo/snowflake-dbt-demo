# Orchestration Assertion Patterns

SQL assertion templates for each orchestration element type. All assertions return `'PASS'` or `'FAIL: <reason>'` as a single-row result. Every assertion MUST include a traceable comment: `-- (Trace: <source element> → <logic> → <expected>)`. The platform profile's `traceability_format` defines the exact comment format for the active platform.

In these templates, `<TEST_DB>` refers to the user-provided `<DATABASE>.<SCHEMA>` from `session_status.json`'s `test_environment` config.

## Execute SQL Task Assertions (DML)

For tasks that perform INSERT, MERGE, UPDATE, or DELETE.

### Row count

```sql
-- Assert: <table> should have N rows after INSERT
-- (Trace: T-SQL inserts from source with WHERE <condition>;
--         source has 3 rows, 2 match condition → expect 2 rows)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table) = 2
    THEN 'PASS' ELSE 'FAIL: expected 2 rows in target_table, got ' ||
         (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table)
END AS test_row_count;
```

### Column value

```sql
-- Assert: status column should be 'Active' for active=1 rows
-- (Trace: T-SQL CASE WHEN active = 1 THEN 'Active' ELSE 'Inactive' END;
--         seed row id=1 has active=1 → expect status='Active')
SELECT CASE
    WHEN status = 'Active'
    THEN 'PASS' ELSE 'FAIL: expected status=Active for id=1, got ' || NVL(status, 'NULL')
END AS test_active_status
FROM <TEST_DB>.staging.target_table
WHERE id = 1;
```

### NULL handling

```sql
-- Assert: NVL should replace NULL created_date with default
-- (Trace: T-SQL ISNULL(created_date, '1900-01-01');
--         seed row id=2 has created_date=NULL → expect '1900-01-01')
SELECT CASE
    WHEN created_date = '1900-01-01'::DATE
    THEN 'PASS' ELSE 'FAIL: expected default date for NULL input, got ' || NVL(TO_VARCHAR(created_date), 'NULL')
END AS test_null_date_handling
FROM <TEST_DB>.staging.target_table
WHERE id = 2;
```

### TRUNCATE + INSERT pattern

```sql
-- Assert: table should be truncated then repopulated (common ETL pattern)
-- (Trace: T-SQL first TRUNCATEs target, then INSERTs filtered rows;
--         only rows matching condition should exist)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table) = 2
    THEN 'PASS' ELSE 'FAIL: expected exactly 2 rows after TRUNCATE+INSERT'
END AS test_truncate_insert;
```

## Script Task Assertions (Variable Assignment)

For tasks that assign variables via `UpdateControlVariable`.

### Variable value

```sql
-- Assert: ScriptTask should set <variable> to expected computed value
-- (Trace: C# Main() calls Dts.Variables["User::<variable>"].Value = <expression>;
--         converted to UpdateControlVariable('User::<variable>', <snowflake_expression>))
SELECT CASE
    WHEN variable_value = TO_VARIANT(<expected_value>)
    THEN 'PASS' ELSE 'FAIL: <variable> should be ' || <expected_value> ||
         ', got ' || NVL(TO_VARCHAR(variable_value), 'NULL')
END AS test_variable_value
FROM <TEST_DB>.public.control_variables
WHERE variable_name = 'User::<variable>';
```

### Variable existence

```sql
-- Assert: variable should exist after ScriptTask execution
-- (Trace: C# writes to User::<variable> → UpdateControlVariable should create/update the row)
SELECT CASE
    WHEN COUNT(*) = 1
    THEN 'PASS' ELSE 'FAIL: expected User::<variable> variable to exist'
END AS test_variable_exists
FROM <TEST_DB>.public.control_variables
WHERE variable_name = 'User::<variable>';
```

## ForEach Loop Assertions

For containers that iterate over collections.

### Cumulative iteration effects

```sql
-- Assert: loop should process all items (cumulative row count)
-- (Trace: DTSX ForEachLoop iterates over 3 file records;
--         each iteration INSERTs to audit_log → expect 3 audit rows)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.dbo.audit_log) = 3
    THEN 'PASS' ELSE 'FAIL: expected 3 audit_log rows from loop, got ' ||
         (SELECT COUNT(*) FROM <TEST_DB>.dbo.audit_log)
END AS test_loop_iteration_count;
```

## Conditional Execution Assertions

For tasks with variable-controlled branching.

### Branch execution verification

```sql
-- Assert: conditional block should execute only when variable matches condition
-- (Trace: DTSX PrecedenceConstraint expression: @[User::<variable>] == "<value>";
--         control_variables seeded with <variable>='<value>' → this branch should execute)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.<target_table>) > 0
    THEN 'PASS' ELSE 'FAIL: conditional branch should have executed (<variable>=<value>)'
END AS test_conditional_branch;
```

## Assertion Numbering

When a statement has many elements with independent assertions, number them clearly:

```sql
-- ASSERT 1 of 4: Row count for insert operation
SELECT CASE ... END AS assert_01_row_count;

-- ASSERT 2 of 4: Column value transformation
SELECT CASE ... END AS assert_02_column_value;

-- ASSERT 3 of 4: Variable assignment
SELECT CASE ... END AS assert_03_variable_assignment;

-- ASSERT 4 of 4: NULL handling
SELECT CASE ... END AS assert_04_null_handling;
```

## Negative Assertion Patterns

Every positive assertion should be paired with a negative assertion verifying the absence of pre-fix or stale state. This prevents false passes where both old and new data coexist.

### No stale rows

```sql
-- Assert: no rows should remain with old/unconverted value
-- (Trace: T-SQL converts status from 0/1 to 'Inactive'/'Active';
--         after conversion, no rows should have numeric status)
SELECT CASE
    WHEN COUNT(*) = 0
    THEN 'PASS' ELSE 'FAIL: ' || COUNT(*) || ' stale rows with numeric status remain'
END AS test_no_stale_status
FROM <TEST_DB>.staging.target_table
WHERE TRY_CAST(status AS INTEGER) IS NOT NULL;
```

### Exact row count (not >= 1)

```sql
-- Assert: exactly N rows should exist (not "at least 1")
-- (Trace: source has 3 rows, 2 match filter → expect exactly 2, not >= 1)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table) = 2
    THEN 'PASS' ELSE 'FAIL: expected exactly 2 rows, got ' ||
         (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table)
END AS test_exact_row_count;
```

### No unexpected column values

```sql
-- Assert: column should NOT contain pre-fix value
-- (Trace: T-SQL sets default_date = '1900-01-01' for NULLs;
--         after fix, no rows should have NULL created_date)
SELECT CASE
    WHEN COUNT(*) = 0
    THEN 'PASS' ELSE 'FAIL: ' || COUNT(*) || ' rows still have NULL created_date'
END AS test_no_null_dates
FROM <TEST_DB>.staging.target_table
WHERE created_date IS NULL;
```

### Variable overwritten (old value absent)

```sql
-- Assert: old variable value should no longer exist
-- (Trace: ScriptTask overwrites <variable> from seed value to computed value;
--         after execution, value should NOT be the seed value)
SELECT CASE
    WHEN variable_value != TO_VARIANT('<seed_value>')
    THEN 'PASS' ELSE 'FAIL: <variable> still has seed value, was not updated'
END AS test_variable_overwritten
FROM <TEST_DB>.public.control_variables
WHERE variable_name = '<variable_name>';
```

## Positive + Negative Pairs

Always write assertions in pairs. Example for an INSERT operation:

```sql
-- POSITIVE: expected rows exist
-- ASSERT 1 of 2: target_table should have 2 rows after INSERT
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table) = 2
    THEN 'PASS' ELSE 'FAIL: expected 2 rows, got ' ||
         (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table)
END AS assert_01_row_count;

-- NEGATIVE: stale/unexpected rows absent
-- ASSERT 2 of 2: no rows should have status='PENDING' (pre-fix state)
SELECT CASE
    WHEN (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table WHERE status = 'PENDING') = 0
    THEN 'PASS' ELSE 'FAIL: ' ||
         (SELECT COUNT(*) FROM <TEST_DB>.staging.target_table WHERE status = 'PENDING') ||
         ' rows still have pre-fix status PENDING'
END AS assert_02_no_stale_status;
```

## Batched Assertion Format

All assertions for a single element MUST be combined into a single UNION ALL query.
Each SELECT returns one row: `assert_name:PASS` or `assert_name:FAIL: details`.

Template:
```sql
-- === ASSERT: {element_name} (batched) ===
SELECT 'assert_01_{description}:' ||
    CASE WHEN ({assertion_query})
    THEN 'PASS'
    ELSE 'FAIL: expected {expected}, got ' || COALESCE(CAST({actual} AS VARCHAR), 'NULL')
    END AS result
UNION ALL
SELECT 'assert_02_{description}:' ||
    CASE WHEN ({assertion_query})
    THEN 'PASS'
    ELSE 'FAIL: expected {expected}, got ' || COALESCE(CAST({actual} AS VARCHAR), 'NULL')
    END
-- ... continue for all assertions
;
```

Rules:
- One `snowflake_sql_execute` call per element's assertion block
- Assert names must be unique and descriptive (e.g., `assert_01_package_status_is_E`)
- Always include failure details in FAIL branch
- Use COALESCE for NULL handling in failure messages
