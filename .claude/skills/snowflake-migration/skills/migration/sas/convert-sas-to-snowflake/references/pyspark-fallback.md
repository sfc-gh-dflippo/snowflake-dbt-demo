# PySpark Fallback - TIER 3 (LAST RESORT)

⚠️ **CRITICAL**: Only use PySpark when SQL and Stored Procedures CANNOT accomplish the task.

**⚠️ These patterns are SQL-translatable and MUST NOT use PySpark:**
- ARRAY iteration → SQL CASE expressions, GREATEST/LEAST
- RETAIN → SQL SUM() OVER window function
- FIRST./LAST. → SQL ROW_NUMBER(), QUALIFY
- KEY= lookup → SQL LEFT JOIN
- MERGE with IN= → SQL FULL OUTER JOIN + CASE
- %DO loops → SQL GENERATOR + CROSS JOIN
- Complex branching (>5 IF) → Stored Procedure

See SKILL.md SQL-First Classification for these patterns.

## When to Load

Load ONLY when block is classified as TIER 3 (PySpark) after exhausting SQL and Stored Procedure options.

---

## Before Using PySpark - Checklist

**Ask yourself:**

- [ ] Can this be done with window functions? (LAG, LEAD, SUM OVER, ROW_NUMBER)
- [ ] Can this be done with CTEs and CASE statements?
- [ ] Can this be done with a stored procedure using DECLARE/BEGIN/END?
- [ ] Is this truly a pattern that requires Python runtime?

**If any checkbox is YES → Do NOT use PySpark. Use SQL or Stored Procedure.**

---

## Valid PySpark Use Cases (ONLY These)

| Pattern | Why PySpark Required | SQL/SP Alternative? |
|---------|---------------------|---------------------|
| HASH objects | In-memory key-value store not in Snowflake | ❌ No direct equivalent |
| DO UNTIL/WHILE with external state | Runtime condition evaluation | ❌ Cannot evaluate at runtime |
| CALL EXECUTE | Dynamic code generation | ❌ Limited dynamic SQL |
| External file I/O | Non-Snowflake files | ❌ COPY INTO limited |
| Complex ARRAY with carried state | Per-element iteration with memory | ❌ No array iteration |

---

## Snowpark Connect (SCOS) Setup

```python
# Cell 1: Setup (SCOS)
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Create Spark session via Snowpark Connect
from pyspark.sql import SparkSession
spark = SparkSession.builder.remote(session.connection).getOrCreate()

print(f"Connected via Snowpark Connect")
TARGET_SCHEMA = "DATABASE.SCHEMA"
```

---

## Pattern: HASH Object Processing

**SAS (No SQL equivalent):**
```sas
DATA enriched;
  IF _N_ = 1 THEN DO;
    DECLARE HASH lookup(dataset: 'codes');
    lookup.DEFINEKEY('code');
    lookup.DEFINEDATA('description');
    lookup.DEFINEDONE();
  END;
  SET transactions;
  rc = lookup.FIND();
  IF rc = 0 THEN code_desc = description;
  ELSE code_desc = 'UNKNOWN';
RUN;
```

**PySpark (broadcast join):**
```python
from pyspark.sql import functions as F
from pyspark.sql.functions import broadcast

codes_df = spark.table(f"{TARGET_SCHEMA}.codes")
transactions_df = spark.table(f"{TARGET_SCHEMA}.transactions")

enriched = transactions_df.join(
    broadcast(codes_df),
    transactions_df.code == codes_df.code,
    "left"
).withColumn(
    "code_desc",
    F.coalesce(F.col("description"), F.lit("UNKNOWN"))
).drop(codes_df.code)

enriched.write.mode("overwrite").saveAsTable(f"{TARGET_SCHEMA}.enriched")
```

---

## Pattern: DO UNTIL/WHILE with External State

**SAS (Runtime iteration):**
```sas
DATA result;
  SET input;
  RETAIN running 0;
  DO UNTIL (running > threshold OR _N_ > 1000);
    running = running + increment;
    /* Complex external condition check */
  END;
RUN;
```

**PySpark:**
```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

df = spark.table(f"{TARGET_SCHEMA}.input")

# Implement iterative logic
running = 0
threshold = 1000
results = []

for row in df.collect():
    running += row['increment']
    if running > threshold:
        break
    results.append(row)

result_df = spark.createDataFrame(results)
result_df.write.mode("overwrite").saveAsTable(f"{TARGET_SCHEMA}.result")
```

---

## SAS Function Helpers (When PySpark Required)

```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, when, coalesce
from pyspark.sql.window import Window

def intck(interval, start_date, end_date):
    """SAS INTCK equivalent"""
    interval_upper = interval.upper()
    if interval_upper == 'YEAR':
        return F.year(end_date) - F.year(start_date)
    elif interval_upper == 'MONTH':
        return F.months_between(end_date, start_date).cast('int')
    elif interval_upper == 'DAY':
        return F.datediff(end_date, start_date)
    return F.datediff(end_date, start_date)

def intnx(interval, start_date, n):
    """SAS INTNX equivalent"""
    interval_upper = interval.upper()
    if interval_upper == 'YEAR':
        return F.add_months(start_date, n * 12)
    elif interval_upper == 'MONTH':
        return F.add_months(start_date, n)
    elif interval_upper == 'DAY':
        return F.date_add(start_date, n)
    return F.date_add(start_date, n)
```

---

## Confidence Levels for PySpark

| Pattern | Confidence | Notes |
|---------|------------|-------|
| Broadcast join (HASH) | HIGH | Well-supported |
| Simple iteration | MEDIUM | Verify row ordering |
| CALL EXECUTE replacement | LOW | May need manual review |
| Complex state management | LOW | Test thoroughly |

---

## Output Format

When generating PySpark notebooks:

```markdown
## Notebook: <script_name>_pyspark.ipynb

### Cell 1: Setup (SCOS Connection)
[Snowpark Connect setup]

### Cell 2: Helper Functions
[Only if needed]

### Cell 3: TIER 3 Block - <reason>
# Original SAS: <sas_code>
# Reason for PySpark: <why_sql_insufficient>
[PySpark implementation]

### Cell 4: Verification
[Query output table to verify]
```

---

## Remember

1. **SQL first** - Window functions solve most SAS patterns
2. **Stored Procedures second** - Complex state management
3. **PySpark last** - Only for genuine edge cases
4. **Document why** - Always explain why PySpark was necessary
