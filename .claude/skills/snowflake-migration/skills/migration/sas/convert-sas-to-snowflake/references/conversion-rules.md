# Critical Conversion Rules

## When to Load

Load at **Steps 5-6** (code generation and self-check). These rules govern semantic correctness of the converted SQL.

---

### Rule: No Programmatic Delegation (NEVER Generate Converter Scripts)
- **NEVER** generate a Python, bash, Node.js, or any other script to perform SAS-to-SQL conversion programmatically
- **NEVER** delegate file conversion to a subagent with instructions to write a converter/parser program
- **NEVER** use regex-based find-and-replace as a substitute for semantic understanding of SAS logic
- The LLM MUST read each SAS file, understand its procedural semantics, and write the Snowflake SQL directly
- Regex parsers CANNOT correctly handle: missing value comparison semantics, MERGE vs JOIN distinctions, RETAIN with conditional resets, BY-group processing order dependencies, or conditional OUTPUT behavior
- For large batches (50+ files): process files in groups of 10-20 per context window, writing completed .sql files to disk between groups. Use `conversion_state.json` to track progress across windows. This is slower but produces correct output.
- The only acceptable use of Python in this workflow is for post-conversion utilities (e.g., generating `conversion_report.docx` via python-docx)

### Rule: Output Completeness (NEVER Truncate)
- **NEVER** summarize repeated logic with "similar pattern", "same as above", "repeat for other tables", or "adjusted joins/filters"
- **NEVER** replace logic with pseudocode or placeholders
- If a block has many column derivations, output EVERY derivation
- If PROC SQL creates multiple tables, generate EACH CREATE TABLE fully
- If a macro has multiple branches, convert EVERY branch
- Prefer **completeness and explicitness** over brevity
- **Filter Dataset Preservation:** If SAS defines a dataset and uses it as a filter (via IN() subquery, INNER JOIN, WHERE ... IN (SELECT ... FROM dataset), or macro variable populated from that dataset), the converted SQL MUST:
  1. Create/populate the equivalent of that filter dataset (as a CTE, temp table, or subquery)
  2. Apply the same filtering relationship in the main query
  3. NEVER silently drop a filtering dataset or its associated WHERE/JOIN condition
- Common pattern: SAS creates a small lookup/filter table (e.g., `REGION_LIST` with specific REGION_IDs), then uses those IDs in a WHERE clause like `WHERE T1.REGION_ID IN (&REGION_ID.)`. The converted SQL must preserve BOTH the filter dataset creation AND its application as a WHERE/JOIN filter.
- If a macro variable is populated via `SELECT ... INTO :var` from a filter dataset, the converted SQL must preserve that filter logic (as a subquery, CTE, session variable, or equivalent)
- During Step 6 self-check: for each dataset created in the SAS source, verify it is either: (a) present as output, or (b) consumed as a filter/join in the converted SQL. If it exists in SAS but is absent from the conversion, it is a logic omission.

### Rule: Missing Value Semantics
- SAS numeric missing (`.`) → `NULL`
- SAS `missing(.A)` through `missing(.Z)` → flag `MANUAL_REVIEW_REQUIRED`
- SAS treats missing as **less than** any value in comparisons; SQL NULLs propagate differently
- Review WHERE/IF/CASE/JOIN conditions involving missing values — behavior may differ
- Convert `MISSING()`, `NMISS()`, `CMISS()` explicitly
- Preserve defaulting logic built from missing-value checks
- Use `NULLS FIRST` in ORDER BY when SAS sort order depends on missing values sorting low
- When SAS checks `IF var NOT IN ('x','X')`, the SQL equivalent **MUST** also handle NULLs explicitly with `OR var IS NULL`, because SQL `NOT IN` evaluates to NULL (not TRUE) when `var` is NULL — SAS treats missing as not-in-list (TRUE). Pattern: `WHERE var NOT IN ('x','X') OR var IS NULL`

### Rule: DATA Step Row-by-Row Semantics
- Treat DATA step as **row-by-row procedural execution**, not simple set-based SQL
- Preserve implicit OUTPUT at end of iteration (when no explicit OUTPUT statement)
- Preserve explicit OUTPUT, DELETE, RETURN, and STOP behavior exactly
- Preserve `_N_` semantics when used → `ROW_NUMBER() OVER (ORDER BY 1)`
- If one input row can create zero, one, or multiple output rows, preserve that behavior
- Preserve ordering dependencies that influence retained values or lag behavior

### Rule: BY-Group Processing
- BY-group processing REQUIRES explicit ordering equivalent to SAS sort order
- If SAS assumes a prior PROC SORT, preserve that ordering dependency
- Do NOT assume input order is stable unless SAS explicitly sorted
- Preserve group resets, running totals by group, and first/last-row logic
- Preserve duplicate handling within BY groups

### Rule: RETAIN / LAG / Sum Statement
- SAS sum statement `x + y;` (with trailing semicolon, no equals sign) **differs from assignment** — it adds y to x's retained value and treats missing as 0
- Convert `x + y;` sum statement to: `COALESCE(x, 0) + COALESCE(y, 0)` with RETAIN semantics
- Preserve LAG behavior exactly; LAG in SAS always reads from the **input queue** regardless of WHERE
- Preserve multiple retained variables with interdependent updates
- If RETAIN or LAG depends on sorted groups, preserve same partitioning and order

### Rule: MERGE vs JOIN Semantics
- SAS MERGE is **NOT** automatically equivalent to a SQL JOIN
- Detect one-to-many and many-to-many row multiplication risk
- Preserve IN= dataset flag behavior explicitly
- Preserve source precedence when multiple datasets contribute overlapping columns
- Preserve row survival rules when unmatched keys exist
- Do NOT silently deduplicate unless SAS explicitly does so
- For UPDATE/MODIFY semantics: preserve in-place update intent

### Rule: WORK / Temp Tables
- SAS WORK datasets → `CREATE OR REPLACE TEMPORARY TABLE` (no schema prefix)
- **NEVER** qualify temp tables with DATABASE.SCHEMA — use bare name only
- **ALWAYS** preserve the `TEMPORARY` keyword on rewrites
- Temporary tables persist for the Snowflake session — available to ALL subsequent blocks
- Do NOT recreate temp tables that were already created upstream

### Rule: Block Separation of Concerns
- Each converted block MUST correspond exactly to its SAS block
- A DATA step block MUST NOT also perform the logic of a subsequent PROC SORT
- A PROC SORT block MUST only dedup/sort, not recreate the table from source
- Temp tables created upstream will still exist when downstream blocks execute
- A temp table created in block N may be consumed by block N+2 or later — not just N+1

### Rule: Snowflake Scripting Syntax
- Variable assignment: use `SELECT col INTO :var FROM table` — **NEVER** `LET var := (SELECT ...)`
- Use `:var` prefix only inside SQL statements (SELECT, INSERT, UPDATE, WHERE, SET)
- Do NOT use `:var` in IF conditions, assignments, concatenations, or RETURN statements
- For RAISE: **ONLY** named exceptions declared in DECLARE section — **NEVER** `RAISE USING MESSAGE`
- For cursors in FOR loop: do NOT use explicit OPEN/CLOSE (FOR opens/closes automatically)

### Rule: PROC SORT with NODUPKEY
- When using ROW_NUMBER() for deduplication, the outer SELECT **MUST use an explicit column list**
- **NEVER** use `SELECT *` if it would leak the helper column (rn) into the output table
- If source is TEMPORARY TABLE, the deduplicated output MUST also be TEMPORARY

### Rule: Cross-Block Variable Persistence
- Snowflake Scripting variables in DECLARE...BEGIN...END **DO NOT persist** after block ends
- If a variable from block N is needed by block N+1, persist as session variable:
  `EXECUTE IMMEDIATE 'SET VAR_NAME = ''' || REPLACE(v_local_var, '''', '''''') || '''';`
- Reference downstream as `$VAR_NAME`

### Rule: Validation Checks Must Be Data-Driven
- When SAS validates values against a dimension/lookup table (e.g., `IF Status_Code NOT IN (SELECT ... FROM dim_table)`), the converted SQL **MUST** preserve the table-based lookup
- **NEVER** replace a SAS dimension-table lookup with a hardcoded value list (e.g., `NOT IN ('A','B','C')`)
- Hardcoded lists become stale when dimension members change — they are a silent correctness regression
- Pattern: SAS `IF var NOT IN (dimension values)` → SQL `LEFT JOIN dimension_table WHERE match IS NULL`
- If the dimension table reference is unclear, flag as MANUAL_REVIEW_REQUIRED rather than hardcoding values

### Rule: Validation Reference Table Preservation
- When SAS validation checks anti-join against a **master/reference table** (e.g., `Ref.CUSTOMER_MASTER`, `Ref.PRODUCT_MASTER`, `Ref.ACCOUNT_MASTER`), the converted SQL **MUST** anti-join against the **same semantic equivalent** — not a derived, subset, or working table
- A master hierarchy table (e.g., `CUSTOMER_MASTER`) and a working/derived table (e.g., `CUSTOMER_SUBSET`) are **NOT interchangeable** — the master is the authoritative source; the derived table is a user-entered subset
- **Referential checks** ("does this key exist in the master?") must use anti-join against the master table
- **Value checks** ("is this value null/zero/invalid?") may use simple WHERE on the target table
- **NEVER** downgrade a referential check to a value check — checking `WHERE Rate IS NULL` is NOT equivalent to checking `WHERE key NOT IN (SELECT key FROM rate_table)` because the latter catches entirely missing rows
- During Step 6 self-check, verify: for each anti-join validation, the reference table in the converted SQL matches the reference table in the SAS source — not a derived/subset alternative

### Rule: Validation Check Source Completeness
- When converting SAS validation scripts (anti-join checks, existence checks, referential integrity), **preserve ALL source tables** referenced in the original SAS check
- If SAS validates Key_ID against tables A, B, and C, the converted SQL must also validate against A, B, and C — not just A
- Dropping a validation source is equivalent to removing a quality gate — it is a silent correctness regression
- During Step 6 self-check, verify: every source table in the SAS validation block appears in the converted SQL validation query

### Rule: Output Column Completeness
- The converted SQL must produce the **same columns** as the SAS output dataset
- If the SAS DATA step or PROC SQL outputs columns A through Z, the converted CREATE TABLE must include A through Z
- **NEVER silently drop output columns** — even if they appear redundant or derivable
- If a column cannot be translated (e.g., depends on unavailable external data), include it with a NULL placeholder and MANUAL_REVIEW_REQUIRED comment
- During Step 6 self-check, verify: column count of converted output >= column count of SAS output

### Rule: Consolidation Must Preserve All Output Tables
- When consolidating multiple SAS scripts into fewer SQL files (Optimize & Consolidate mode), the **total set of output tables** across all consolidated files **MUST equal** the total set from the unconsolidated conversion
- Before declaring consolidation complete, cross-check:
  1. List every CREATE TABLE / INSERT INTO target from the unconsolidated version
  2. List every CREATE TABLE / INSERT INTO target from the consolidated version
  3. Any target in (1) but not in (2) is a **dropped output** — this is a P1 bug
- If a SAS script's logic is merged into another file, the merged file MUST contain ALL output tables from the original script
- **NEVER silently drop a SAS script's output tables during consolidation**
- Consolidation **MUST NOT change which reference table** a validation check validates against — if SAS check N anti-joins against `Ref.CUSTOMER_MASTER`, the consolidated SQL must also anti-join against `CUSTOMER_MASTER` (or its schema-qualified equivalent), not a derived table like `CUSTOMER_SUBSET`

### Rule: Tier Consistency in Consolidation
- When consolidating files in Optimize & Consolidate mode, **do not downgrade a file's tier** unless consolidation genuinely eliminates the need for procedural control flow
- If a SAS file has 3+ sequential dependent DML statements (e.g., DELETE → INSERT → UPDATE on related tables), it MUST remain Tier 2 with SP wrapping — even if each individual statement is simple SQL
- SP wrapping provides: transaction scope, error handling via EXCEPTION, orchestration via CALL, and row-count reporting via RETURN

### Rule: No Invented Elements (Anti-Hallucination)
- **NEVER** introduce variables, parameters, columns, macro variables, or filter values that do not exist in the source SAS code
- The converted SQL must be a FAITHFUL translation — not an "improved" or "augmented" version
- If a variable name appears in the output SQL, it MUST trace back to the source SAS (as a column, macro parameter, macro variable, or SAS variable)
- If a WHERE clause or filter condition appears in the output, it MUST correspond to a condition in the source SAS
- Specifically prohibited:
  - Adding parameters to macros/procedures that aren't in the SAS `%MACRO` definition
  - Adding WHERE clauses or JOIN conditions not present in the SAS source
  - Inventing column names based on assumed data patterns
  - Adding "helper" filters that seem logical but aren't in the source
  - Adding variables to make the code "more flexible" when the SAS source is hardcoded
- During Step 6 self-check: for each variable/parameter in the output, verify it has a source in the input SAS — if it doesn't, it is a hallucination and must be removed
- Specifically: if a file's logic involves a DELETE-then-INSERT-then-UPDATE chain where later statements depend on earlier ones succeeding, flat Tier 1 SQL is insufficient — wrap in a stored procedure with CALL at the bottom

### Rule: BOOLEAN Flag/Indicator Column Detection
- SAS commonly stores flags as character `'Y'`/`'N'`, but the migrated Snowflake column may be a native `BOOLEAN`
- When converting `WHERE flag = 'Y'` / `flag = 'N'` (or `IF`/`CASE` on such a column):
  - If the target column is known `BOOLEAN`: emit `WHERE flag = TRUE` / `flag = FALSE`
  - If the target column is known `VARCHAR`: keep `WHERE flag = 'Y'` / `'N'`
  - If the type is **unknown** and the column name ends in `_IND` or `_FLAG`: prefer `BOOLEAN` (TRUE/FALSE) and add a comment: `-- NOTE: verify column type (BOOLEAN vs VARCHAR) for <col>`
- **NEVER** blindly copy SAS `'Y'`/`'N'` comparisons without considering a BOOLEAN target — a string compare against a BOOLEAN column errors or silently matches nothing

### Rule: Loop / Delimited-String NULL Guards
- When converting a SAS loop that iterates over a delimited string (e.g., `%DO` over a comma list, or cursor over `SPLIT_PART`), guard against NULL/empty before iterating:
  ```sql
  IF (v_list IS NOT NULL AND TRIM(v_list) <> '') THEN
    -- loop body; also skip blank items: IF (TRIM(v_item) <> '') THEN ...
  END IF;
  ```
- When building an iteration list from a control/config table, filter out null/empty keys: `WHERE key_col IS NOT NULL AND TRIM(key_col) <> ''`
- This prevents malformed dynamic SQL (empty `IN ()` clauses, broken concatenation) and wasted iterations on empty data

---

## Migrated-Source Type Traps

These three rules address a common failure class: SAS treats data types permissively, and source engines (Teradata, Oracle, DB2, SQL Server) often coerced types implicitly. When those tables land in Snowflake — which is **strict** about types — otherwise-faithful conversions silently return wrong results (0 rows) or raise errors. Apply these whenever a converted query touches a table that was migrated from a non-Snowflake source.

### Rule: Type-Safe JOIN/Comparison on Migrated Keys
- The **same logical key** can have **different physical types** across tables from different source systems (e.g., an ID is `NUMBER` in one table and `VARCHAR` in another).
- When joining or comparing key columns, cast **both sides to the same type** (`::VARCHAR` is the safe default for identifiers) whenever:
  1. The column is an identifier/key (an `*_ID`, `*_GUID`, `*_SK`, customer/account/order key, etc.), **and**
  2. The two tables originate from **different source systems or schemas**, **and**
  3. There is any possibility of a `NUMBER` vs `VARCHAR` mismatch.
  ```sql
  -- CORRECT: cast both sides
  ... ON A.CUSTOMER_ID::VARCHAR = B.CUSTOMER_ID::VARCHAR
  WHERE HDR.ACCOUNT_KEY::VARCHAR = DTL.ACCOUNT_KEY::VARCHAR
  -- WRONG: raw compare fails silently (0 rows) if one side is NUMBER, other VARCHAR
  ... ON A.CUSTOMER_ID = B.CUSTOMER_ID
  ```
- **Why:** Teradata/Oracle perform permissive implicit conversion; Snowflake does not. A mismatched-type join yields zero rows or a "Numeric value is not recognized" error.
- Alternative for repeated joins: pre-cast into a clean temp table (`SELECT DISTINCT key::VARCHAR AS key ... WHERE key IS NOT NULL`) and join to that.

### Rule: Numeric Aggregation on Migrated VARCHAR Columns
- Migration tools sometimes store numeric measures as `VARCHAR` (to preserve precision). A direct `SUM()`/`AVG()`/`MIN()`/`MAX()` on such a column raises "Numeric value is not recognized".
- Wrap aggregations with `TRY_TO_DOUBLE` (or `TRY_TO_NUMBER`) — plus `COALESCE(..., 0)` to match SAS's "missing + missing = 0 in SUM" behavior — when the source table was migrated **and** the column type cannot be confirmed numeric **and** the name suggests a measure (`*_AMT`, `*_CNT`, `*_QTY`, `*_DAYS`, `*_COST`, `*_CHRG`, `PAID_*`, `SPLY_*`).
  ```sql
  -- CORRECT
  COALESCE(SUM(TRY_TO_DOUBLE(CPVAL.PAID_AMT::VARCHAR)), 0) AS TOT_PAID
  -- WRONG (errors if PAID_AMT is VARCHAR)
  COALESCE(SUM(CPVAL.PAID_AMT), 0) AS TOT_PAID
  ```
- `TRY_TO_*` returns NULL (not an error) for non-numeric text, so bad rows are skipped rather than aborting the query.

### Rule: VARCHAR Date-Column Range Comparison
- When SAS compares a date column against a date range (e.g., `PAID_DT >= &DTS`), determine whether the **target Snowflake column** is a native `DATE`/`TIMESTAMP` or a `VARCHAR` holding a date string.
- If the column is (or may be) `VARCHAR`, wrap the **column itself** in `TO_DATE(col, fmt)` — not just the comparison value:
  ```sql
  -- CORRECT (column stored as 'DDMONYYYY')
  WHERE TO_DATE(DTL.CLM_LN_PAID_DT, 'DDMONYYYY') >= TO_DATE($DTS, 'YYYY-MM-DD')
    AND TO_DATE(DTL.CLM_LN_PAID_DT, 'DDMONYYYY') <= TO_DATE($DTE, 'YYYY-MM-DD')
  -- WRONG: string comparison, meaningless as a date ('15JAN2024' >= '2024-01-01' is alphabetic)
  WHERE DTL.CLM_LN_PAID_DT >= $DTS
  ```
- Detection heuristics: SAS uses `INPUT(col, date_fmt.)` before comparing → column is VARCHAR; source DDL shows `CHAR`/`VARCHAR`; a `*_DT` column from a Teradata/DB2-migrated fact table → assume VARCHAR `DDMONYYYY` unless context says otherwise.
- When unsure, wrapping the column in `TO_DATE()` is safe for both native `DATE` and `VARCHAR` columns.
