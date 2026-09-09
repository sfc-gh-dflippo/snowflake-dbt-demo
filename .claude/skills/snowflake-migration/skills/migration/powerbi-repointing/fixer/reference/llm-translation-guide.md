# LLM Translation Guide for PowerQuery Expressions

## Table of Contents

- [Overview](#overview)
- [Why LLM Translation?](#why-llm-translation)
- [Translation Process](#translation-process)
- [Translation Rules](#translation-rules)
- [Complete Examples](#complete-examples)
- [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)
- [Validation Checklist](#validation-checklist)
- [Edge Cases](#edge-cases)
- [Testing Your Translation](#testing-your-translation)


## Overview

This guide explains how to translate unsupported PowerQuery expressions from various SQL dialects (SQL Server, Oracle, Teradata, etc.) to Snowflake using LLM knowledge.

**Important**: 
- This guide uses the correct Snowflake connector pattern with `Value.NativeQuery()` and `Implementation="2.0"` as documented in the [official Microsoft Power Query Snowflake connector documentation](https://learn.microsoft.com/en-us/power-query/connectors/snowflake).
- The source SQL dialect should be identified from `Reports/SnowConvert/Assessment.<timestamp>.csv` in the SnowConvert output folder.
- Apply dialect-specific SQL syntax translations based on the identified source database.

## Why LLM Translation?

**Problem**: SnowConvert cannot translate PowerQuery expressions with complex string concatenation, such as:

```m
Sql.Database("server", "database", 
    [Query="SELECT " & ColumnNameParam & " FROM [MYTBL] WHERE SALARY > " & MinSalary])
```

Or from other SQL dialects like Oracle:

```m
Oracle.Database("server", 
    [Query="SELECT * FROM EMPLOYEES WHERE ROWNUM <= " & MaxRows & " AND HIRE_DATE >= SYSDATE - " & DaysBack])
```

**Challenges**:
- Dynamic query construction with `&` concatenation
- Multiple parameters injected into query string
- Conditional logic building queries
- Source dialect-specific syntax (SQL Server brackets `[]`, Oracle `ROWNUM`, Teradata `QUALIFY`, etc.)
- Various SQL syntax differences between source and Snowflake
- **Column name casing differences** between source connectors and Snowflake

**Solution**: Use LLM to understand and translate the entire PowerQuery expression while:
- Preserving logic and parameter usage
- Identifying source SQL dialect patterns
- Applying dialect-specific SQL syntax translations to Snowflake
- Handling column name casing to ensure compatibility
- Using the provided `expected_columns` field to apply column renames when necessary

## Translation Process

### Input Format

The LLM receives queries in this format (`artifacts/pbit/queries_for_translation.json`):

```json
[
  {
    "query_name": "QueryName",
    "original_expression": ["let", "    Source = Sql.Database(...)", "in", "    Source"],
    "original_text": "let\n    Source = Sql.Database(...)\nin\n    Source",
    "expected_columns": ["Cust_ID", "FIRST_NAME", "LAST_NAME"],
    "translation_status": "pending",
    "translated_expression": null
  }
]
```

**Key Fields**:
- `query_name`: The name of the Power BI query/table
- `original_expression`: Array format of the PowerQuery expression
- `original_text`: String format of the PowerQuery expression
- `expected_columns`: **List of top-level column names expected by Power BI** (from `model.tables[].columns[].name` in DataModelSchema)
- `translation_status`: Current status (`pending`, `completed`, etc.)
- `translated_expression`: The translated expression (initially `null`)

### Output Format

The LLM produces translations in this format (`artifacts/pbit/translated_queries.json`):

```json
[
  {
    "query_name": "QueryName",
    "original_expression": ["let", "    Source = Sql.Database(...)", "in", "    Source"],
    "original_text": "let\n    Source = Sql.Database(...)\nin\n    Source",
    "expected_columns": ["Cust_ID", "FIRST_NAME", "LAST_NAME"],
    "translation_status": "completed",
    "translated_expression": "let\n        Source = Value.NativeQuery(Snowflake.Databases(...))\n    in\n        Source"
  }
]
```

**Important**: The `expected_columns` field is preserved in the output to maintain context.

**CRITICAL - Expression Format**: 
- The `translated_expression` MUST be a **STRING** with embedded newlines (`\n`), NOT a list/array
- This matches the format that SnowConvert uses for converted queries
- Example: `"let\n        Source = ...\n    in\n        Source"` (single string)
- Do NOT use: `["let", "    Source = ...", "in", "    Source"]` (array format)

### Validation Checklist 

Before saving translated expression, verify:

- [ ] Use the instructions in [validation instructions](validate-dynamic-query.md) to validate the syntax of the translated query. ** DO THIS ** (Note: Skip this step if no database was configured in Step 0.5 - user was warned that validation would be skipped)
- [ ] Source SQL dialect identified (SQL Server, Oracle, Teradata, etc.)
- [ ] Source connector replaced with `Value.NativeQuery(Snowflake.Databases(...))`
- [ ] Uses `SF_SERVER_LINK` parameter (NOT with `.snowflakecomputing.com` suffix)
- [ ] Uses `SF_WAREHOUSE_NAME` parameter
- [ ] Uses `SF_ROLE` parameter with validation: `[Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]`
- [ ] Uses `{[Name=SF_DB_NAME]}[Data]` to access database
- [ ] Includes `[Implementation="2.0"]` in Snowflake.Databases options
- [ ] Includes `[EnableFolding=true]` in Value.NativeQuery
- [ ] Dialect-specific SQL syntax translated correctly (e.g., SQL Server `TOP` → `LIMIT`, Oracle `ROWNUM` → `LIMIT`, Oracle `NVL` → `IFNULL`)
- [ ] Source-specific identifiers handled (SQL Server brackets removed, Oracle FROM DUAL removed, etc.)
- [ ] All `&` concatenation operators preserved
- [ ] All Power BI parameters preserved (ColumnParam, TableParam, etc.)
- [ ] PowerQuery structure unchanged (let...in, variable names)
- [ ] **Column names checked**: Compare `expected_columns` from input JSON with Snowflake output (UPPERCASE)
- [ ] **Table.RenameColumns added** if any column names in `expected_columns` have casing mismatches with Snowflake UPPERCASE
- [ ] **Final return variable updated** to `RenamedColumns` if renaming was added
- [ ] `translation_status` set to `"completed"`

#

## Translation Rules

### 0. Identify Source SQL Dialect

**Rule**: Before translating, identify the source SQL dialect from the SnowConvert migration.

**How to Identify**:
1. **From SnowConvert Assessment File** (preferred):
   - File location: `<OUTPUT_FOLDER>/Reports/SnowConvert/Assessment.<timestamp>.csv`
   - Look for line: `SourceLanguage,<dialect name>`
   - Examples: `SourceLanguage,Transact`, `SourceLanguage,Oracle`, `SourceLanguage,Teradata`

2. **From Query Patterns** (if assessment file not found):
   - `[TABLE]` brackets → SQL Server
   - `ROWNUM`, `DUAL`, `NVL()` → Oracle
   - `QUALIFY`, `SEL` → Teradata
   - Connection function: `Sql.Database()` → SQL Server, `Oracle.Database()` → Oracle

**Important**: The source dialect determines which SQL syntax translations to apply.

### 1. Connector Replacement

**Rule**: Replace source database connector with `Value.NativeQuery()` using `Snowflake.Databases()` connector and parameter references.

**Before (SQL Server)**:
```m
Sql.Database("myserver", "mydb", [Query="..."])
```

**Before (Oracle)**:
```m
Oracle.Database("myserver", [Query="..."])
```

**Before (Teradata)**:
```m
Teradata.Database("myserver", [Query="..."])
```

**After (All become Snowflake)**:
```m
Value.NativeQuery(
    Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
    "...",
    null,
    [EnableFolding=true]
)
```

**Key Points**:
- Replace ANY source connector with the Snowflake pattern
- Use `Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"])` (NOT `SF_SERVER_LINK & ".snowflakecomputing.com"`)
- Access the database using `{[Name=SF_DB_NAME]}[Data]`
- Wrap in `Value.NativeQuery()` function
- SQL query is the second parameter (as a string, can include concatenation)
- Include `[EnableFolding=true]` for query optimization

**Note on Oracle Connector**:
- Use `Oracle.Database()` (NOT `OracleACI.Database()`)
- Server parameter is just the hostname (port and service can be specified in connection options if needed)
- See [Oracle.Database documentation](https://learn.microsoft.com/en-us/powerquery-m/oracle-database) for details

**Note on Teradata Connector**:
- Use `Teradata.Database()` 
- Server parameter is the hostname (port can be specified with colon separator if needed, e.g., "server:1025")
- See [Teradata.Database documentation](https://learn.microsoft.com/en-us/powerquery-m/teradata-database) for details

### 2. Preserve Parameter Concatenation

**Rule**: Keep all `&` concatenation operators and parameter references intact in the query string.

**Before**:
```m
[Query="SELECT " & ColumnParam & " FROM " & TableParam]
```

**After**:
```m
Value.NativeQuery(
    Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
    "SELECT " & ColumnParam & " FROM " & TableParam,
    null,
    [EnableFolding=true]
)
```

**Important**: Do NOT try to evaluate or replace parameters. They are Power BI report parameters.

### 3. SQL Syntax Translation

Apply these SQL syntax changes WITHIN the Query string based on the source dialect:

**SQL Server → Snowflake:**

| SQL Server | Snowflake | Example |
|------------|-----------|---------|
| `[TABLE]` | `TABLE` | `[EMPLOYEES]` → `EMPLOYEES` |
| `[SCHEMA].[TABLE]` | `SCHEMA.TABLE` | `[DBO].[SALES]` → `DBO.SALES` |
| `TOP N` | `LIMIT N` | `SELECT TOP 100` → `SELECT ... LIMIT 100` |
| `ISNULL(x,y)` | `IFNULL(x,y)` | `ISNULL(col, 0)` → `IFNULL(col, 0)` |
| `GETDATE()` | `CURRENT_TIMESTAMP()` | `GETDATE()` → `CURRENT_TIMESTAMP()` |
| `LEN(x)` | `LENGTH(x)` | `LEN(name)` → `LENGTH(name)` |
| `CONVERT(VARCHAR, x)` | `TO_VARCHAR(x)` | `CONVERT(VARCHAR, date)` → `TO_VARCHAR(date)` |
| `DATEADD(day, n, d)` | `DATEADD(day, n, d)` | (Same syntax) |

**Oracle → Snowflake:**

| Oracle | Snowflake | Example |
|--------|-----------|---------|
| `SYSDATE` | `CURRENT_TIMESTAMP()` | `WHERE date >= SYSDATE` → `WHERE date >= CURRENT_TIMESTAMP()` |
| `NVL(x,y)` | `IFNULL(x,y)` | `NVL(salary, 0)` → `IFNULL(salary, 0)` |
| `ROWNUM <= N` | `LIMIT N` | `WHERE ROWNUM <= 100` → `LIMIT 100` (move to end) |
| `TO_CHAR(x, 'fmt')` | `TO_VARCHAR(x, 'fmt')` | `TO_CHAR(date, 'YYYY')` → `TO_VARCHAR(date, 'YYYY')` |
| `DECODE(x,a,b,c)` | `CASE WHEN x=a THEN b ELSE c END` | Full CASE expression |
| `FROM DUAL` | Remove `FROM DUAL` | `SELECT 1 FROM DUAL` → `SELECT 1` |
| `\|\| (concat)` | `\|\|` or `CONCAT()` | (Same or use CONCAT) |

**Teradata → Snowflake:**

| Teradata | Snowflake | Example |
|----------|-----------|---------|
| `QUALIFY ROW_NUMBER() <= N` | Subquery with `LIMIT N` | Restructure query |
| `SEL` | `SELECT` | `SEL *` → `SELECT *` |
| `.NEXTVAL` | `<sequence>.NEXTVAL` | `seq.NEXTVAL` (same) |
| `CAST(x AS VARCHAR(n))` | `CAST(x AS VARCHAR(n))` | (Same syntax) |

**Important**: Apply these transformations ONLY to SQL within the Query string, NOT to PowerQuery syntax.

### 4. Handle Complex Concatenation

**Example 1**: Multiple parameter injection

**Before**:
```m
let
    Source = Sql.Database("server", "db", 
        [Query="SELECT " & Columns & " FROM [" & Schema & "].[" & Table & "] WHERE " & Filter])
in
    Source
```

**After**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT " & Columns & " FROM " & Schema & "." & Table & " WHERE " & Filter,
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Note**: Brackets removed around schema/table in concatenation.

**Example 2**: Conditional query building

**Before**:
```m
let
    BaseQuery = "SELECT * FROM [DBO].[SALES]",
    FilterClause = if HasFilter then " WHERE Date >= '" & StartDate & "'" else "",
    Source = Sql.Database("server", "db", [Query=BaseQuery & FilterClause])
in
    Source
```

**After**:
```m
let
    BaseQuery = "SELECT * FROM DBO.SALES",
    FilterClause = if HasFilter then " WHERE Date >= '" & StartDate & "'" else "",
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        BaseQuery & FilterClause,
        null,
        [EnableFolding=true]
    )
in
    Source
```

### 5. Column Name Casing (Table.RenameColumns)

**Rule**: The Snowflake connector returns all column names in UPPERCASE. If the Power BI report expects different casing, you MUST add a `Table.RenameColumns` step to ensure compatibility.

**Why This Matters**:
- Source connectors (Teradata, SQL Server, Oracle) may return column names in mixed case or the original casing
- Snowflake always returns column names in UPPERCASE
- Power BI reports reference columns by the names defined in `model.tables[].columns[].name`
- If the expected column name doesn't match what Snowflake returns, the report will fail

**Using the `expected_columns` Field**:

The input JSON includes an `expected_columns` field that contains the exact column names Power BI expects. Use this field to:

1. **Determine what Snowflake will return**: Snowflake returns the UPPERCASE version of SQL column aliases
2. **Compare with expected names**: Check each name in `expected_columns` against the UPPERCASE version
3. **Identify mismatches**: Any difference in casing requires a `Table.RenameColumns` step

**Step-by-Step Process**:

```
For each column in expected_columns:
  1. Get the expected name (e.g., "Cust_ID")
  2. Determine Snowflake output (UPPERCASE of SQL alias, e.g., "CUST_ID")
  3. If expected ≠ Snowflake output:
     - Add to rename list: {"CUST_ID", "Cust_ID"}
```

**How to Identify Expected Column Names**:

The expected column names are provided in the `expected_columns` field of the input JSON. These come from `model.tables[].columns[].name` in the DataModelSchema and represent the exact column names that Power BI expects.

**Example - Using Expected Column Names from JSON**:

Given this input query:
```json
{
  "query_name": "genquery",
  "original_expression": [...],
  "original_text": "let\n    Source = Teradata.Database(...)\nin\n    Source",
  "expected_columns": ["Cust_ID", "FIRST_NAME", "LAST_NAME"],
  "translation_status": "pending",
  "translated_expression": null
}
```

Compare the expected columns with what Snowflake will return:

| Expected Name (from `expected_columns`) | Snowflake Returns | Match? | Action |
|-----------------------------------------|-------------------|--------|--------|
| `Cust_ID` | `CUST_ID` | ❌ | Rename needed |
| `FIRST_NAME` | `FIRST_NAME` | ✓ | No action |
| `LAST_NAME` | `LAST_NAME` | ✓ | No action |

**How to Apply Table.RenameColumns**:

If there are mismatches, add a `Table.RenameColumns` step after the `Source` step:

```m
Table.RenameColumns(Source, {{"SNOWFLAKE_NAME", "Expected_Name"}, {"SNOWFLAKE_NAME2", "Expected_Name2"}})
```

**Complete Example with Column Renaming**:

**Before (Teradata)**:
```m
let
    Source = Teradata.Database(TeradataServer,
     [HierarchicalNavigation=true, Query="SELECT TOP " & Number.ToText(SamplePct) &
      " PERCENT c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME, c.LAST_NAME as LAST_NAME 
      FROM VAL.CUSTOMER C WHERE c.STATE_CODE = '" & StateCode & "'"])
in
    Source
```

**Expected columns from schema**: `Cust_ID`, `FIRST_NAME`, `LAST_NAME`

**After (Snowflake with Column Renaming)**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME, c.LAST_NAME as LAST_NAME 
         FROM VAL.CUSTOMER SAMPLE (" & Number.ToText(SamplePct) & ") C 
         WHERE c.STATE_CODE = '" & StateCode & "'",
        null,
        [EnableFolding=true]
    ),
    RenamedColumns = Table.RenameColumns(Source, {{"CUST_ID", "Cust_ID"}})
in
    RenamedColumns
```

**Key Points**:
- The `Table.RenameColumns` step is added AFTER the `Source` step
- The mapping is `{{"SNOWFLAKE_UPPERCASE_NAME", "Expected_Name_From_Schema"}}`
- The final `in` clause returns `RenamedColumns` instead of `Source`
- Only include columns that need renaming (where casing differs)
- If ALL columns match (all uppercase), no `Table.RenameColumns` is needed

**JSON Array Format with Column Renaming**:
```json
"expression": [
    "let",
    "    Source = Value.NativeQuery(",
    "        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Implementation=\"2.0\"]){[Name=SF_DB_NAME]}[Data],",
    "        \"SELECT c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME FROM VAL.CUSTOMER C\",",
    "        null,",
    "        [EnableFolding=true]",
    "    ),",
    "    RenamedColumns = Table.RenameColumns(Source, {{\"CUST_ID\", \"Cust_ID\"}})",
    "in",
    "    RenamedColumns"
]
```

## Complete Examples

### Example 1: Simple Query with Parameters

**Input**:
```m
let
    Source = Sql.Database("MYSERVER", "MYDB", 
        [Query="SELECT TOP 1000 * FROM [DBO].[EMPLOYEES] WHERE SALARY > " & MinSalary])
in
    Source
```

**Output**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT * FROM DBO.EMPLOYEES WHERE SALARY > " & MinSalary & " LIMIT 1000",
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Changes Applied**:
- Connector replacement with `Value.NativeQuery`
- `[DBO].[EMPLOYEES]` → `DBO.EMPLOYEES`
- `TOP 1000` → `LIMIT 1000` (moved to end)
- Preserved `& MinSalary` concatenation
- Added `[EnableFolding=true]` for optimization

### Example 2: Oracle Query with Parameters

**Input**:
```m
let
    Source = Oracle.Database("orcl.company.com", 
        [Query="SELECT * FROM EMPLOYEES WHERE ROWNUM <= " & MaxRows & " AND HIRE_DATE >= SYSDATE - " & DaysBack & " AND NVL(SALARY, 0) > 0 ORDER BY EMPLOYEE_ID"])
in
    Source
```

**Output**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT * FROM EMPLOYEES WHERE HIRE_DATE >= CURRENT_TIMESTAMP() - " & DaysBack & " AND IFNULL(SALARY, 0) > 0 ORDER BY EMPLOYEE_ID LIMIT " & MaxRows,
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Changes Applied**:
- `Oracle.Database` → `Value.NativeQuery` with `Snowflake.Databases`
- Hard-coded server → SF_* parameters
- `ROWNUM <= N` → `LIMIT N` (moved to end, preserved parameter)
- `SYSDATE` → `CURRENT_TIMESTAMP()`
- `NVL` → `IFNULL`
- Preserved all `&` concatenations (MaxRows, DaysBack)
- Added `[EnableFolding=true]` for optimization

### Example 3: Teradata Query with QUALIFY

**Input**:
```m
let
    Source = Teradata.Database("tdserver.company.com", 
        [Query="SEL Employee_ID, Salary, ROW_NUMBER() OVER (ORDER BY Salary DESC) AS Rank 
                FROM Employees 
                WHERE Hire_Date >= CURRENT_DATE - " & DaysBack & " 
                QUALIFY ROW_NUMBER() OVER (ORDER BY Salary DESC) <= " & TopN])
in
    Source
```

**Output**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT Employee_ID, Salary, ROW_NUMBER() OVER (ORDER BY Salary DESC) AS Rank 
         FROM (
             SELECT * 
             FROM Employees 
             WHERE Hire_Date >= CURRENT_DATE - " & DaysBack & "
         ) 
         QUALIFY ROW_NUMBER() OVER (ORDER BY Salary DESC) <= " & TopN,
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Changes Applied**:
- `Teradata.Database` → `Value.NativeQuery` with `Snowflake.Databases`
- Hard-coded server → SF_* parameters
- `SEL` → `SELECT` (Teradata abbreviation)
- `QUALIFY` preserved (Snowflake supports QUALIFY)
- `CURRENT_DATE` works in both Teradata and Snowflake
- Preserved all `&` concatenations (DaysBack, TopN)
- Added `[EnableFolding=true]` for optimization

### Example 4: Complex Multi-Part Query (SQL Server)

**Input**:
```m
let
    Source = Sql.Database("SERVER", "DB",
        [Query="SELECT " & ColumnList & " FROM [" & SchemaParam & "].[" & TableParam & "] 
                WHERE [Date] >= '" & StartDate & "' 
                AND LEN([Name]) > 0 
                AND [Status] = 'Active'
                ORDER BY [Date] DESC"])
in
    Source
```

**Output**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT " & ColumnList & " FROM " & SchemaParam & "." & TableParam & " 
                WHERE Date >= '" & StartDate & "' 
                AND LENGTH(Name) > 0 
                AND Status = 'Active'
                ORDER BY Date DESC",
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Changes Applied**:
- Connector replacement
- Brackets removed: `[Schema].[Table]` → concatenation without brackets
- `LEN` → `LENGTH`
- All `[ColumnName]` → `ColumnName` (brackets removed)
- Preserved all `&` concatenations
- Added `Value.NativeQuery` wrapper

### Example 5: Dynamic Table Selection (SQL Server)

**Input**:
```m
let
    TableName = "SALES_" & Year,
    Query = "SELECT * FROM [DBO].[" & TableName & "] WHERE ISNULL([Amount], 0) > 0",
    Source = Sql.Database("SERVER", "DB", [Query=Query])
in
    Source
```

**Output**:
```m
let
    TableName = "SALES_" & Year,
    Query = "SELECT * FROM DBO." & TableName & " WHERE IFNULL(Amount, 0) > 0",
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        Query,
        null,
        [EnableFolding=true]
    )
in
    Source
```

**Changes Applied**:
- Connector replacement with `Value.NativeQuery`
- `[DBO].[" & TableName & "]` → `DBO." & TableName` (brackets removed from concatenation)
- `ISNULL` → `IFNULL`
- `[Amount]` → `Amount`
- Query variable can be passed directly to `Value.NativeQuery`

### Example 6: Teradata Query with Column Renaming

**Input JSON**:
```json
{
  "query_name": "genquery",
  "original_expression": [
    "let",
    "    Source = Teradata.Database(TeradataServer,",
    "     [HierarchicalNavigation=true, Query=\"SELECT TOP \" & Number.ToText(SamplePct) &",
    "      \" PERCENT  c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME, c.LAST_NAME as LAST_NAME, c.STATE_CODE as STATE_CODE, c.GENDER as GENDER, c.CITY_NAME as CITY_NAME",
    "      FROM VAL.CUSTOMER C",
    "      WHERE c.STATE_CODE = '\" & StateCode & \"'",
    "      AND c.GENDER = '\" & Gender & \"'\" ])",
    "in",
    "    Source"
  ],
  "original_text": "let\n    Source = Teradata.Database(TeradataServer,\n     [HierarchicalNavigation=true, Query=\"SELECT TOP \" & Number.ToText(SamplePct) &\n      \" PERCENT  c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME, c.LAST_NAME as LAST_NAME, c.STATE_CODE as STATE_CODE, c.GENDER as GENDER, c.CITY_NAME as CITY_NAME \n      FROM VAL.CUSTOMER C \n      WHERE c.STATE_CODE = '\" & StateCode & \"' \n      AND c.GENDER = '\" & Gender & \"'\" ])\nin\n    Source",
  "expected_columns": ["Cust_ID", "FIRST_NAME", "LAST_NAME", "STATE_CODE", "GENDER", "CITY_NAME"],
  "translation_status": "pending",
  "translated_expression": null
}
```

**Column Analysis** (using `expected_columns`):
| Expected Name | Snowflake Returns | Match? |
|---------------|-------------------|--------|
| `Cust_ID` | `CUST_ID` | ❌ |
| `FIRST_NAME` | `FIRST_NAME` | ✓ |
| `LAST_NAME` | `LAST_NAME` | ✓ |
| `STATE_CODE` | `STATE_CODE` | ✓ |
| `GENDER` | `GENDER` | ✓ |
| `CITY_NAME` | `CITY_NAME` | ✓ |

**Output (translated_expression)**:
```m
let
    Source = Value.NativeQuery(
        Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
        "SELECT c.CUST_ID as CUST_ID, c.FIRST_NAME as FIRST_NAME, c.LAST_NAME as LAST_NAME, c.STATE_CODE as STATE_CODE, c.GENDER as GENDER, c.CITY_NAME as CITY_NAME #(lf)FROM VAL.CUSTOMER SAMPLE (" & Number.ToText(SamplePct) & ") C #(lf)WHERE c.STATE_CODE = '" & StateCode & "' #(lf)AND c.GENDER = '" & Gender & "'",
        null,
        [EnableFolding=true]
    ),
    RenamedColumns = Table.RenameColumns(Source, {{"CUST_ID", "Cust_ID"}})
in
    RenamedColumns
```

**Changes Applied**:
- `Teradata.Database` → `Value.NativeQuery` with `Snowflake.Databases`
- `TOP N PERCENT` → `SAMPLE (N)` (Snowflake sampling syntax)
- Added `Table.RenameColumns` to fix `CUST_ID` → `Cust_ID` casing
- Changed final return from `Source` to `RenamedColumns`
- Preserved all parameter concatenations

## Common Pitfalls to Avoid

### ❌ DON'T: Use old connector format
```m
// WRONG - Old format
Source = Snowflake.Databases("myaccount.snowflakecomputing.com", "MYWAREHOUSE", [Database="MYDB", Query="..."])
```

### ✅ DO: Use Value.NativeQuery with parameter references
```m
// CORRECT - New format with parameters
Source = Value.NativeQuery(
    Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME, [Role = if SF_ROLE = "" then null else SF_ROLE, Implementation="2.0"]){[Name=SF_DB_NAME]}[Data],
    "...",
    null,
    [EnableFolding=true]
)
```

### ❌ DON'T: Evaluate or replace Power BI parameters
```m
// WRONG - Don't try to resolve ColumnParam
Value.NativeQuery(..., "SELECT ID, NAME, SALARY FROM TABLE", ...)  // Missing parameter concatenation
```

### ✅ DO: Preserve parameter concatenation
```m
// CORRECT
Value.NativeQuery(..., "SELECT " & ColumnParam & " FROM TABLE", ...)
```

### ❌ DON'T: Change PowerQuery syntax
```m
// WRONG
let
    Result = Snowflake.Databases(...)
in
    Result  // Changed variable name
```

### ✅ DO: Keep PowerQuery structure
```m
// CORRECT
let
    Source = Snowflake.Databases(...)
in
    Source  // Same variable name
```

### ❌ DON'T: Ignore column name casing differences
```m
// WRONG - Schema expects "Cust_ID" but Snowflake returns "CUST_ID"
let
    Source = Value.NativeQuery(...)
in
    Source  // Missing Table.RenameColumns
```

### ✅ DO: Add Table.RenameColumns when casing differs
```m
// CORRECT - Rename columns to match expected names from schema
let
    Source = Value.NativeQuery(...),
    RenamedColumns = Table.RenameColumns(Source, {{"CUST_ID", "Cust_ID"}})
in
    RenamedColumns
```

## Validation Checklist  

Use the checklist described in "Translation Process -> Validation Checklist".

## Edge Cases

### Multi-line Query Strings

When Query string spans multiple lines in concatenation:

```m
// Input
[Query="SELECT * " &
       "FROM TABLE " &
       "WHERE Col > " & Value]

// Output
[Query="SELECT * " &
       "FROM TABLE " &
       "WHERE Col > " & Value]
```

Keep the same structure.

### Nested Concatenation

```m
// Input
[Query="SELECT * FROM [" & Schema & "].[" & Table & "_" & Suffix & "]"]

// Output  
[Query="SELECT * FROM " & Schema & "." & Table & "_" & Suffix]
```

Remove brackets but preserve all concatenation logic.

### Comments in Query

```m
// Input
[Query="SELECT * FROM [TABLE] -- Comment"]

// Output
[Query="SELECT * FROM TABLE -- Comment"]
```

Preserve comments.

### Multiple Column Renames

When multiple columns need renaming:

```m
// Input columns from schema: Cust_ID, First_Name, Last_Name
// Snowflake returns: CUST_ID, FIRST_NAME, LAST_NAME

let
    Source = Value.NativeQuery(...),
    RenamedColumns = Table.RenameColumns(Source, {
        {"CUST_ID", "Cust_ID"}, 
        {"FIRST_NAME", "First_Name"}, 
        {"LAST_NAME", "Last_Name"}
    })
in
    RenamedColumns
```

### No Column Renames Needed

When all expected column names are already uppercase:

```m
// Input columns from schema: CUST_ID, FIRST_NAME, LAST_NAME
// Snowflake returns: CUST_ID, FIRST_NAME, LAST_NAME
// All match - no Table.RenameColumns needed

let
    Source = Value.NativeQuery(...)
in
    Source
```

### Power Query Column Transformations

**Important**: The `expected_columns` field shows the **final** column names after all Power Query transformations. If the Power Query expression adds, removes, or renames columns after fetching from the database, the `expected_columns` will reflect those changes.

**Example - Columns Added by Power Query**:
```json
{
  "query_name": "EnhancedCustomers",
  "expected_columns": ["CUST_ID", "FULL_NAME", "IS_ACTIVE"],
  "original_text": "let\n    Source = Sql.Database(...),\n    AddedFullName = Table.AddColumn(Source, \"FULL_NAME\", each [FIRST_NAME] & \" \" & [LAST_NAME]),\n    AddedIsActive = Table.AddColumn(AddedFullName, \"IS_ACTIVE\", each true)\nin\n    AddedIsActive"
}
```

In this case:
- SQL query returns: `CUST_ID`, `FIRST_NAME`, `LAST_NAME`
- Power Query adds: `FULL_NAME`, `IS_ACTIVE`
- `expected_columns` shows final output: `CUST_ID`, `FULL_NAME`, `IS_ACTIVE`

**When translating**: Focus on ensuring the SQL columns match what's needed for the Power Query transformations. The `expected_columns` helps you understand what the final output should be, but you still need to preserve any column transformations in the Power Query expression.

## Testing Your Translation

Mental checklist for each translation:

1. Is the source SQL dialect identified? (SQL Server, Oracle, Teradata, etc.)
2. Would this connect to Snowflake? (Value.NativeQuery with Snowflake.Databases and SF_* params)
3. Are Power BI parameters still dynamic? (& concatenation preserved in query string)
4. Is the SQL valid Snowflake syntax? (dialect-specific syntax translated correctly)
5. Would Power BI prompt for SF_* values? (using parameters, not hard-coded)
6. Is the structure identical to input? (same let...in, variable names)
7. Is `[Implementation="2.0"]` included? (uses new Snowflake connector)
8. Is `[EnableFolding=true]` included? (enables query optimization)
9. **Are column names checked against `expected_columns`?** (compare with Snowflake UPPERCASE output)
10. **Is Table.RenameColumns added if needed?** (for casing mismatches found in `expected_columns`)

---

**Remember**: The goal is to translate the connection and SQL syntax from the SOURCE DIALECT to Snowflake while preserving ALL PowerQuery logic and parameter usage, AND ensuring column names match the expected casing from the Power BI schema.

**Reference**: [Power Query Snowflake connector documentation](https://learn.microsoft.com/en-us/power-query/connectors/snowflake)
