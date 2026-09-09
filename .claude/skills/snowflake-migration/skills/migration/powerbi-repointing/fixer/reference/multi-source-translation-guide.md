# Multi-Source Connection Translation Guide

This guide covers translating PowerQuery expressions that contain **multiple database connections** to Snowflake.

## Pattern Detection

Look for these indicators of multiple source connections:

1. **Multiple connector calls** in the same `let...in` block:
   - `Source = Teradata.Database(...)`
   - `Source_2 = Teradata.Database(...)`

2. **Conditional logic** selecting between sources:
   - `if paramName = "1" then Source else Source_2`
   - `SelectedSource = if condition then Source else Source_2`

3. **Conditional transformations** referencing specific sources:
   - `if param = "1" then Table.TransformColumnTypes(Source,...) else Table.TransformColumnTypes(Source_2,...)`

## Translation Rules

### Rule 1: Translate ALL Database Connectors

Every database connector call must be translated to Snowflake:

| Source Connector | Target Connector |
|-----------------|------------------|
| `Teradata.Database()` | `Value.NativeQuery(Snowflake.Databases(...))` |
| `Sql.Database()` | `Value.NativeQuery(Snowflake.Databases(...))` |
| `Oracle.Database()` | `Value.NativeQuery(Snowflake.Databases(...))` |

### Rule 2: Preserve Variable Names

Keep all original variable names exactly as they appear:
- `Source` stays `Source`
- `Source_2` stays `Source_2`
- `RowsToReturn` stays `RowsToReturn`

### Rule 3: Preserve Conditional Logic

All `if...then...else` statements must remain unchanged:
```m
RowsToReturn = if paramP = "1" then Source else Source_2
```

### Rule 4: Apply SQL Syntax Translation to EACH Query

Each query string must have dialect-specific translations applied independently.

---

## Complete Translation Example

### Before (Teradata with Multiple Sources)

```m
let
    Source = Teradata.Database("teradata.example.com", [Query="SELECT TOP 100 cust_id, first_name, last_name, income, state_code, TO_DATE('1900/01/01','YYYY/MM/DD') AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='M'"]),
    Source_2 = Teradata.Database("teradata.example.com", [Query="SELECT cust_id, first_name, last_name, income, state_code, CURRENT_DATE AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='F'"]),
    SelectedSource = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = Table.TransformColumnTypes(SelectedSource, {{"report_date", type date}, {"income", type number}})
in
    #"Changed Type"
```

### After (Snowflake - ALL Connections Translated)

```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role=SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT cust_id, first_name, last_name, income, state_code, TO_DATE('1900-01-01') AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='M' LIMIT 100",
        null,
        [EnableFolding=true]
    ),
    Source_2 = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role=SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT cust_id, first_name, last_name, income, state_code, CURRENT_DATE AS report_date FROM sales_db.customers WHERE state_code='" & pStateCode & "' AND gender='F'",
        null,
        [EnableFolding=true]
    ),
    SelectedSource = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = Table.TransformColumnTypes(SelectedSource, {{"report_date", type date}, {"income", type number}})
in
    #"Changed Type"
```

### SQL Translations Applied

| Original (Teradata) | Translated (Snowflake) |
|--------------------|------------------------|
| `SELECT TOP 100 ...` | `SELECT ... LIMIT 100` |
| `TO_DATE('1900/01/01','YYYY/MM/DD')` | `TO_DATE('1900-01-01')` |

---

## Complex Example with UNION ALL

### Before (Teradata)

```m
let
    Source = Teradata.Database("teradata.example.com", [HierarchicalNavigation=true, Query="SELECT TOP 10 * FROM (SELECT c.cust_id, c.first_name, TO_DATE('1900/01/01','YYYY/MM/DD') AS Calendar_Date FROM sales_db.customers c WHERE c.status = 1 GROUP BY 1,2,3 UNION ALL SELECT c.cust_id, c.first_name, CURRENT_DATE AS Calendar_Date FROM sales_db.customers c WHERE c.status = 2 GROUP BY 1,2,3) a"]),
    Source_2 = Teradata.Database("teradata.example.com", [HierarchicalNavigation=true, Query="SELECT c.cust_id, c.first_name, CURRENT_DATE AS Calendar_Date FROM sales_db.customers c WHERE c.age >= 21 GROUP BY 1,2,3"]),
    RowsToReturn = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = if pSourceSelector = "1" then Table.TransformColumnTypes(Source, {{"Calendar_Date", type date}}) else Table.TransformColumnTypes(Source_2, {{"Calendar_Date", type date}})
in
    #"Changed Type"
```

### After (Snowflake)

```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role=SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT * FROM (SELECT c.cust_id, c.first_name, TO_DATE('1900-01-01') AS Calendar_Date FROM sales_db.customers c WHERE c.status = 1 GROUP BY 1,2,3 UNION ALL SELECT c.cust_id, c.first_name, CURRENT_DATE AS Calendar_Date FROM sales_db.customers c WHERE c.status = 2 GROUP BY 1,2,3) a LIMIT 10",
        null,
        [EnableFolding=true]
    ),
    Source_2 = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role=SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT c.cust_id, c.first_name, CURRENT_DATE AS Calendar_Date FROM sales_db.customers c WHERE c.age >= 21 GROUP BY 1,2,3",
        null,
        [EnableFolding=true]
    ),
    RowsToReturn = if pSourceSelector = "1" then Source else Source_2,
    #"Changed Type" = if pSourceSelector = "1" then Table.TransformColumnTypes(Source, {{"Calendar_Date", type date}}) else Table.TransformColumnTypes(Source_2, {{"Calendar_Date", type date}})
in
    #"Changed Type"
```

---

## Validation Checklist for Multi-Source

After translating, verify:

- [ ] **ALL** database connector calls are translated (count Source, Source_2, etc.)
- [ ] Each uses `Value.NativeQuery(Snowflake.Databases(...))`
- [ ] Each has `SF_SERVER_LINK`, `SF_WAREHOUSE_NAME`, `SF_DB_NAME` parameters
- [ ] Each has `[Role=SF_ROLE, Implementation="2.0"]`
- [ ] Each has `[EnableFolding=true]`
- [ ] All variable names preserved exactly
- [ ] All conditional logic (`if...then...else`) preserved
- [ ] SQL syntax translated in EACH query string
- [ ] `TOP N` moved to `LIMIT N` at end of query
- [ ] Date functions converted (TO_DATE format, ADD_MONTHS → DATEADD)

---

## Common Mistakes to Avoid

1. **Only translating `Source`** - Must translate ALL sources (Source, Source_2, Source_3, etc.)
2. **Changing variable names** - Keep `Source_2` as `Source_2`, not `SecondSource`
3. **Removing conditional logic** - The `if...then...else` must stay exactly as-is
4. **Missing SQL translations in one query** - Each query needs independent translation
5. **Forgetting `LIMIT` placement** - `TOP N` at start becomes `LIMIT N` at end

---

## See Also

- `llm-translation-guide.md` - Complete SQL dialect translation rules
- `teradata-m-query-pattern-samples.md` - Patterns 16 and 17 for multi-source examples
