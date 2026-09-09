# SSC-EWI-0021 - OUTPUT Clause Not Supported

Snowflake does not support the SQL Server OUTPUT clause. Choose the right fix based on whether the captured data is actually used.

## Decision Tree

```
Is the OUTPUT data queried or used downstream?
├── NO → Remove OUTPUT clause entirely (Case 1)
└── YES → What data is needed?
    ├── Row count only → Use SQLROWCOUNT (Case 2)
    ├── Generated IDs for single row → Query after insert (Case 3)
    ├── Generated IDs for batch/loop → Use batch tracking pattern (Case 4)
    └── Change history → Use Streams (Case 5)
```

## Fix Process

1. **Search for usage** - Find if the OUTPUT target (`@TableVar`, `#TempTable`) is queried after the DML
2. **Choose pattern** - Use decision tree above
3. **Apply fix** - Transform code using the appropriate pattern
4. **Remove marker** - Delete the `!!!RESOLVE EWI!!!` line
5. **Verify** - Check that downstream code still receives the data it needs

---

## Case 1: OUTPUT Not Used (Most Common)

If the captured data is never queried, remove the OUTPUT clause and its target.

### Before
```sql
INSERT INTO target_table (col1, col2)
OUTPUT inserted.id INTO @CapturedRows
SELECT col1, col2 FROM source_table;
-- @CapturedRows is never used
```

### After
```sql
INSERT INTO target_table (col1, col2)
SELECT col1, col2 FROM source_table;
```

**Verification:** Search for `@CapturedRows` - if no SELECT/usage found, safe to remove.

---

## Case 2: Row Count Only

Replace with `SQLROWCOUNT`.

### Before
```sql
INSERT INTO target OUTPUT inserted.id INTO @ids SELECT col1 FROM source;
SET @count = (SELECT COUNT(*) FROM @ids);
```

### After
```sql
INSERT INTO target SELECT col1 FROM source;
LET count := SQLROWCOUNT;
```

---

## Case 3: Single Row - Query After Insert

For single-row inserts needing the generated ID, query using known keys.

### Before
```sql
INSERT INTO orders (customer_id, order_date)
OUTPUT inserted.order_id INTO @NewOrderId
VALUES (@cust_id, GETDATE());
```

### After
```sql
INSERT INTO orders (customer_id, order_date)
VALUES (:cust_id, CURRENT_TIMESTAMP());

LET new_order_id := (
    SELECT order_id FROM orders 
    WHERE customer_id = :cust_id 
    ORDER BY order_date DESC
    LIMIT 1
);
```

---

## Case 4: Batch Processing - Track with Temp Table

**Use this pattern when:** Processing rows in a loop/batch and need to link source rows to generated target IDs.

### Pattern

```sql
-- 1. Capture which source rows are being processed
CREATE OR REPLACE TEMPORARY TABLE T_BatchRows AS
SELECT source_key_columns
FROM source_table
WHERE filter_conditions
LIMIT :batch_size;

-- 2. Perform the DML
INSERT INTO target_table (cols...)
SELECT cols...
FROM source_table src
INNER JOIN T_BatchRows br ON br.key = src.key;

-- 3. Update source with generated IDs by joining on composite key
UPDATE source_table src
SET result_id_column = tgt.generated_id
FROM target_table tgt
INNER JOIN T_BatchRows br ON br.key = src.key
WHERE tgt.composite_key_col1 = src.composite_key_col1
  AND tgt.composite_key_col2 = src.composite_key_col2;

-- 4. Cleanup
DROP TABLE IF EXISTS T_BatchRows;
```

### Complete Example

**Before (Invalid - OUTPUT in batch loop):**
```sql
WHILE (@RowsThisBatch > 0)
BEGIN
    INSERT INTO BudgetLineItem (HeaderID, AccountID, Amount)
    OUTPUT inserted.LineItemID, inserted.AccountID
    INTO @InsertedRows (LineItemID, AccountID)
    SELECT :HeaderID, AccountID, Amount
    FROM Staging WHERE IsProcessed = 0
    ORDER BY RowID
    OFFSET 0 ROWS FETCH NEXT @BatchSize ROWS ONLY;
    
    SET @RowsThisBatch = @@ROWCOUNT;
    
    -- Update staging with result IDs
    UPDATE Staging SET ResultID = ir.LineItemID
    FROM @InsertedRows ir WHERE Staging.AccountID = ir.AccountID;
END
```

**After (Valid - Batch tracking pattern):**
```sql
WHILE (:ROWSTHISBATCH > 0) LOOP
    -- 1. Capture batch rows
    CREATE OR REPLACE TEMPORARY TABLE T_BatchRows AS
    SELECT RowID, AccountID, CostCenterID, PeriodID
    FROM Staging
    WHERE IsProcessed = 0
    ORDER BY RowID
    LIMIT :BATCHSIZE;

    -- 2. Insert using join
    INSERT INTO BudgetLineItem (HeaderID, AccountID, CostCenterID, PeriodID, Amount)
    SELECT :HEADERID, stg.AccountID, stg.CostCenterID, stg.PeriodID, stg.Amount
    FROM Staging stg
    INNER JOIN T_BatchRows br ON br.RowID = stg.RowID;
    
    ROWSTHISBATCH := SQLROWCOUNT;

    -- 3. Update staging with generated IDs
    UPDATE Staging stg
    SET ResultID = bli.LineItemID
    FROM BudgetLineItem bli
    INNER JOIN T_BatchRows br ON br.RowID = stg.RowID
    WHERE bli.HeaderID = :HEADERID
      AND bli.AccountID = stg.AccountID
      AND bli.CostCenterID = stg.CostCenterID
      AND bli.PeriodID = stg.PeriodID;

    -- 4. Mark processed and cleanup
    UPDATE Staging SET IsProcessed = 1 WHERE RowID IN (SELECT RowID FROM T_BatchRows);
    DROP TABLE IF EXISTS T_BatchRows;
END LOOP;

-- Final cleanup (in case of early exit)
DROP TABLE IF EXISTS T_BatchRows;
```

**Verification:** After fix, query `Staging.ResultID` - should contain the generated `LineItemID` values.

---

## Case 5: MERGE with Tracking

Same pattern applies to MERGE statements.

### Before
```sql
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET target.val = source.val
WHEN NOT MATCHED THEN INSERT (id, val) VALUES (source.id, source.val)
OUTPUT $action, inserted.id INTO @MergeResults;
```

### After
```sql
-- Capture source rows being processed
CREATE OR REPLACE TEMPORARY TABLE T_BatchRows AS
SELECT id FROM source;

MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN UPDATE SET target.val = source.val
WHEN NOT MATCHED THEN INSERT (id, val) VALUES (source.id, source.val);

LET rows_affected := SQLROWCOUNT;

-- Link back if needed
UPDATE source_tracking src
SET target_id = tgt.id
FROM target tgt
INNER JOIN T_BatchRows br ON br.id = src.id
WHERE tgt.id = src.id;

DROP TABLE IF EXISTS T_BatchRows;
```

---

## Case 6: Streams (Long-term Tracking)

For ongoing change tracking, use Snowflake Streams.

```sql
-- Setup (once)
CREATE OR REPLACE STREAM target_stream ON TABLE target_table;

-- After DML, query the stream
SELECT METADATA$ACTION, METADATA$ISUPDATE, * FROM target_stream;
```

---

## Quick Reference

| Need | Solution |
|------|----------|
| Nothing (OUTPUT unused) | Remove OUTPUT clause |
| Row count | `SQLROWCOUNT` |
| Single generated ID | Query after insert with known keys |
| Batch IDs in loop | Temp table + join pattern |
| Change history | Streams |

## Resources

- [Snowflake Streams](https://docs.snowflake.com/en/user-guide/streams)
- [SQLROWCOUNT](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/resultsets#sqlrowcount)
- [MERGE Statement](https://docs.snowflake.com/en/sql-reference/sql/merge)
- [SQL Server OUTPUT Clause](https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql)
