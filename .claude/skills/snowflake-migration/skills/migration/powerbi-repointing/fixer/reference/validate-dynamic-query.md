# Validating Dynamic SQL Queries

Instructions for validating dynamically constructed SQL queries (e.g., from PowerQuery/M, application code, or templated SQL) against Snowflake.

## Prerequisites

**IMPORTANT**: SQL validation requires a database context in your Snowflake connection.

- This should have been configured in **Step 0.5** of the workflow
- If no database was configured and the user chose to proceed without validation, **skip this entire validation process**
- The skill will still translate queries, but syntax errors may only be discovered at runtime

## Overview

Dynamic queries built via string concatenation often contain syntax errors that are only discovered at runtime. Use compile-only validation to safely check SQL syntax without executing against live data.

**IMPORTANT - What Compile-Only Validation Does:**
- ✅ Checks SQL syntax is valid
- ✅ Verifies object references (tables, schemas) exist
- ✅ Validates column names
- ❌ Does NOT execute any queries
- ❌ Does NOT access or read any data
- ❌ Does NOT create audit log entries for data access

## Step-by-Step Process

### Step 1: Extract the SQL Template

Identify the SQL query being constructed. For PowerQuery/M, look for `Value.NativeQuery()` calls:

```powerquery
Value.NativeQuery(
    ...,
    "SELECT ... FROM TABLE WHERE col = '" & Parameter & "'",
    ...
)
```

Extract the SQL string and note all dynamic parameters (variables being concatenated).

### Step 2: Substitute Sample Values

Replace dynamic parameters with realistic sample values:

| Parameter Type | Example Substitution |
|----------------|---------------------|
| String | `'CA'`, `'active'` |
| Number | `10`, `100.50` |
| Date | `'2024-01-01'` |
| Boolean | `TRUE`, `FALSE` |

**Example:**

Original (M language):
```
"SELECT * FROM CUSTOMER SAMPLE BERNOULLI (" & Number.ToText(SamplePct) & ") WHERE STATE = '" & StateCode & "'"
```

Substituted SQL:
```sql
SELECT * FROM CUSTOMER SAMPLE BERNOULLI (10) WHERE STATE = 'CA'
```

### Step 3: Validate Using Compile-Only Mode

Execute the query with compile-only validation. This checks syntax and object references without:
- Consuming compute resources
- Accessing any data
- Requiring a running warehouse
- Creating audit log entries for data access

```sql
-- Use compile-only validation (syntax check only, no execution)
SELECT * FROM CUSTOMER SAMPLE BERNOULLI (10) WHERE STATE = 'CA'
```

### Step 4: Interpret Results

| Result | Meaning | Action |
|--------|---------|--------|
| Compilation successful | SQL syntax is valid | Proceed to Step 5 |
| Syntax error | Invalid SQL structure | Fix the error and re-validate |
| Object does not exist | Table/schema not found | Expected if validating against different environment; syntax is likely valid |
| Column not found | Invalid column reference | Check column names in source schema |

**Important:** An "object does not exist" error after fixing syntax errors typically means the syntax is valid but the objects don't exist in the current connection's context. This is acceptable for syntax validation.

### Step 5: Provide Corrected Query

If errors were found and fixed, provide:

1. **The specific error** identified
2. **The correction** made
3. **The full corrected query** in the original language/format

## Common Snowflake SQL Syntax Issues

### Table Alias with SAMPLE Clause

**Invalid:**
```sql
FROM TABLE_NAME SAMPLE BERNOULLI (10) T
```

**Valid:**
```sql
FROM TABLE_NAME AS T SAMPLE BERNOULLI (10)
```

The alias must come BEFORE the SAMPLE clause.

### String Concatenation Quoting

Ensure string parameters are properly quoted in the concatenation:

**Invalid:**
```
"WHERE name = " & NameVar
```

**Valid:**
```
"WHERE name = '" & NameVar & "'"
```

### Newline Characters

In PowerQuery/M, `#(lf)` represents a line feed. Ensure these don't break SQL syntax when the query is assembled.

## Validation Safety Comparison

| Method | Compute Used | Data Accessed | Side Effects |
|--------|--------------|---------------|--------------|
| Compile-only | None | None | None |
| EXPLAIN | Minimal | None | Query plan logged |
| LIMIT 0 | Minimal | Metadata only | Query logged |
| Full execution | Full | Yes | Full audit trail |

**Always prefer compile-only validation for syntax checking.**

## Example Validation Session

**Input:** PowerQuery/M with embedded SQL
```powerquery
let
    Source = Value.NativeQuery(
        Snowflake.Databases(...){[Name=DB]}[Data],
        "SELECT c.ID FROM SCHEMA.TABLE SAMPLE BERNOULLI (" & Number.ToText(Pct) & ") C",
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Extracted SQL with substitution:**
```sql
SELECT c.ID FROM SCHEMA.TABLE SAMPLE BERNOULLI (10) C
```

**Validation result:** Syntax error - unexpected 'C' after SAMPLE clause

**Corrected SQL:**
```sql
SELECT c.ID FROM SCHEMA.TABLE AS C SAMPLE BERNOULLI (10)
```

**Corrected PowerQuery/M:**
```powerquery
let
    Source = Value.NativeQuery(
        Snowflake.Databases(...){[Name=DB]}[Data],
        "SELECT c.ID FROM SCHEMA.TABLE AS C SAMPLE BERNOULLI (" & Number.ToText(Pct) & ")",
        null,
        [EnableFolding=true]
    )
in
    Source
```
