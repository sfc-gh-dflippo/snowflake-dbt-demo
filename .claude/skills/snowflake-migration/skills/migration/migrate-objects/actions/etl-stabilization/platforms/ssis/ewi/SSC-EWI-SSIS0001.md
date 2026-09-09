# SSC-EWI-SSIS0001 — SSIS Component Not Supported

An SSIS **data flow component** has no SnowConvert translation, so the converter emitted a stub: a
`!!!RESOLVE EWI!!!` marker plus the component's original XML as comments. The marker **breaks
compilation**, and the component's behaviour is absent from the generated model — so resolving this means
reconstructing what the component did, not just deleting a line.

In real customer packages this is the most frequent compilation-breaking SSIS marker, and the most common
cause is a **third-party / custom component** (a vendor connector or a Script Component) rather than a
stock Microsoft transform. Those two cases have very different resolutions, so identify which you have
before editing anything.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Logic present in output? | **No** — only as commented XML |
| Frequency | **High** relative to other SSIS markers; clusters when one component is reused across data flows |
| Common action | Identify the component from `componentClassID`, then rebuild in SQL or escalate as needs-user |

## Identification

```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--
--<component DTSID="" CreationName="" componentClassID="Microsoft.ManagedComponentHost"
--   refId="Package\Load Reference Data\ExampleVendor CloudSheets Source"
--   name="ExampleVendor CloudSheets Source"
--   description="Extracts data from a hosted spreadsheet service." ...>
--  <properties>
--    <property name="AccessMode" ...>0</property>
--    <property name="TableOrView" ...>[ReferenceCrosswalks_CategoryDescriptions]</property>
--    <property name="UserComponentTypeName" ...>ExampleVendor.SSIS.CloudSheets.CloudSheetsSource</property>
--  </properties>
```

The marker text is generic. The commented `<component>` element tells you everything:

| Attribute / property | What it tells you |
|---|---|
| `componentClassID` | The component type. `Microsoft.ManagedComponentHost` means a **managed/third-party** component — look at `UserComponentTypeName` for the real identity. |
| `name` / `description` | Human-readable purpose, often naming the vendor and system. |
| `refId` | Which package and data flow task it belongs to (`Package\<Data Flow Task>\<Component>`). |
| `UserComponentTypeName` | The concrete third-party class (for example `<Vendor>.SSIS.<System>.<Name>Source`). |
| `<property>` entries | The configuration: `SQLStatement`, `TableOrView`, `AccessMode`, parameter mappings. |
| `<inputColumns>` / `<outputColumns>` | The column contract downstream components expect. |

## Decision Tree

1. **Is it a source, a transform, or a destination?** The component name and its input/output columns tell
   you. A component with only output columns is a source; only input columns is a destination.
2. **Is it a third-party or custom component?** (`componentClassID="Microsoft.ManagedComponentHost"`, a
   `UserComponentTypeName` with a vendor namespace, or a Script Component.) If so, the data comes from or
   goes to a system outside Snowflake — go to Pattern 3. **This cannot be solved by writing SQL**, because
   the data does not exist in the warehouse yet.
3. **Is it a stock transform Snowflake can express?** Use the table below and rebuild it in SQL
   (Pattern 1).
4. **Is it a Script Component with row-level .NET logic?** Read the embedded script from the properties,
   and reproduce the logic in SQL if it is expressible; otherwise escalate.
5. **Preserve the column contract.** Whatever you build must expose the component's `outputColumns` with
   the same names and compatible types, or the downstream model breaks.

## Component Type Reference

| SSIS component | Snowflake / dbt approach | Reconstructable? |
|---|---|---|
| Derived Column | Expression list in the `SELECT` | Yes |
| Conditional Split | One CTE / model per output, each with the branch condition | Yes |
| Lookup | `LEFT JOIN` (match all rows) — mind no-match rows | Yes |
| Aggregate | `GROUP BY` + aggregates | Yes |
| Sort (with "remove duplicates") | `ORDER BY`, `SELECT DISTINCT`, or `QUALIFY ROW_NUMBER()...=1` | Yes |
| Union All / Merge | `UNION ALL` | Yes |
| Merge Join | `JOIN` of the corresponding type | Yes |
| Pivot / Unpivot | `PIVOT` / `UNPIVOT` | Yes |
| Row Count | Drop it; the count becomes a variable/metric, not data | Usually |
| Script Component (row logic) | SQL expression, or a Snowpark UDF | Sometimes |
| Third-party source/destination (commercial connector packs, cloud SaaS sources, REST endpoints, hosted spreadsheets) | Land the data in Snowflake by other means, then `source()` it | **No** — needs-user |
| Fuzzy Lookup / Grouping | `JAROWINKLER_SIMILARITY` + windowed best-match selection | Sometimes |

## Fix Patterns

### Pattern 1: Stock transform — rebuild in SQL

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0001 - SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
--<component name="Split By Region" componentClassID="Microsoft.ConditionalSplit" ...>
--  <outputs>
--    <output name="West" ...><property name="Expression">Region == "West"</property></output>
--    <output name="Other" isErrorOut="false" ... />
--  </outputs>

-- After: one model (or CTE) per branch, SSIS expression translated to SQL
SELECT * FROM {{ ref('stg_raw__customers') }} WHERE REGION = 'West'
```

Remember SSIS expression syntax is not SQL: `==` becomes `=`, `!=` becomes `<>`, `&&`/`||` become
`AND`/`OR`, and string comparisons are case-sensitive in SSIS but follow Snowflake's collation here.

### Pattern 2: Lookup — preserve no-match behaviour

```sql
-- After
SELECT c.*, r.REGION_NAME
FROM {{ ref('stg_raw__customers') }} c
LEFT JOIN {{ source('raw', 'REGION_LOOKUP') }} r
    ON c.REGION_CODE = r.REGION_CODE
```

Use `LEFT JOIN` when the SSIS Lookup redirects or ignores no-match rows, and an inner `JOIN` only when the
package genuinely fails/drops them. Choosing the wrong one silently changes row counts and compiles fine.

### Pattern 3: Third-party source — escalate, do not fake it

```sql
-- After (marker removed so the model parses; the data dependency is explicit)
-- NEEDS-USER: This model replaced the SSIS component "ExampleVendor CloudSheets Source"
-- (ExampleVendor.SSIS.CloudSheets.CloudSheetsSource), which read the hosted spreadsheet
-- [ReferenceCrosswalks_CategoryDescriptions] directly from the SSIS runtime.
-- Snowflake cannot reach that system from SQL, so the data must be landed first
-- (external ingestion, a stage load, or a scheduled export into a raw table).
-- Once landed, point this model at it via source(), preserving the output columns declared
-- in the commented XML. Not stubbed with constants on purpose.
SELECT * FROM {{ source('raw', 'CLOUDSHEETS_CATEGORY_DESCRIPTIONS') }}
```

Declare the expected table in `sources.yml` so the project's lineage is honest about the dependency
instead of hiding it. Flag the model needs-user with the vendor component name and the system it read.

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` line — it breaks compilation.
- Removing the marker alone is **not** a fix: the component's behaviour is missing from the output.
- **Read `componentClassID` and `UserComponentTypeName` first.** Third-party connectors are a data-landing
  problem, not a SQL problem, and no amount of SQL will resolve them.
- Preserve the component's output column names and types — downstream models depend on them.
- Never substitute constants, empty sets or `NULL` for a component you cannot reproduce; escalate instead.
- The same vendor component often appears in several data flows of one package; resolve every occurrence
  the same way.
- Validate against source-derived expected results — a rebuilt component that compiles can still have the
  wrong join type, grain or branch conditions.
