# SSC-FDM-0007 — Missing Dependent Object

SnowConvert detected that a SQL statement references a database object (table, view, stored procedure, or function) that was not found within the converted project scope. The FDM comment is informational — it does NOT break compilation.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | Inline FDM comment (not `!!!RESOLVE EWI!!!`) |
| Breaks compilation? | **No** |
| Frequency | Very high (~10,000 occurrences in large projects) |
| Most common action | No code change needed |

## Identification

Look for the marker:
```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "schema.ObjectName" **
```

Or with multiple objects:
```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "dbo.BQI_PROJECT", "[dbo].[ESQAM_ETL_STATS]" **
```

The marker appears as a SQL comment on the line immediately before the statement that references the missing object(s). The code after the comment is syntactically valid SQL.

## Decision Tree

1. **Is the object a source table or view that will exist in Snowflake at runtime?**
   - Examples: `dbo.BQI_PROJECT`, `Staging.TGB_Data`, `dwh.v_Dim_Vehicle`
   - These are production tables/views that will be migrated or already exist.
   - **Action:** No code change. Mark as informational.

2. **Is the object a staging table created by a prior task in the task graph?**
   - Examples: `stg.PatientStatus_Leaf`, temporary tables populated by earlier steps
   - The table will exist when this task runs because the task graph order ensures it.
   - **Action:** No code change. Mark as informational.

3. **Is the object a stored procedure or function?**
   - Examples: `stg.udp_PatientStatus_Leaf`, `CWSBIReporting.Metrics.Duplicate_Claim`
   - Check if SnowConvert generated it in another converted file within the project.
   - **Action:** If found elsewhere in converted output, no code change. If not found, mark as needs-user.

4. **Is the object a logging/audit table (e.g., `ESQAM_ETL_STATS`, `SSIS_log`)?**
   - These tables track ETL execution metrics and may need to be created in Snowflake.
   - **Action:** No code change to the referencing SQL. Note that the table must be created separately.

5. **Does the object genuinely not exist and cannot be inferred?**
   - Examples: `ErrorTable` with no definition found anywhere
   - **Action:** Ask user. Options: comment out the statement, create a stub table, or map to an alternative.

## Fix Patterns

### Pattern 1: Source table exists at runtime — no change needed

```sql
-- Before (no change needed)
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "dbo.BQI_PROJECT", "[dbo].[ESQAM_ETL_STATS]" **
truncate TABLE dbo.BQI_PROJECT;
UPDATE QIS.dbo.ESQAM_ETL_STATS
   SET LoadStartTimestamp = CURRENT_TIMESTAMP() :: TIMESTAMP
   WHERE tableName = 'BQI_PROJECT';

-- After (identical — keep the FDM comment, no code change)
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "dbo.BQI_PROJECT", "[dbo].[ESQAM_ETL_STATS]" **
truncate TABLE dbo.BQI_PROJECT;
UPDATE QIS.dbo.ESQAM_ETL_STATS
   SET LoadStartTimestamp = CURRENT_TIMESTAMP() :: TIMESTAMP
   WHERE tableName = 'BQI_PROJECT';
```

### Pattern 2: Stored procedure exists elsewhere in converted output

```sql
-- Before
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "stg.udp_PatientStatus_Leaf" **
CALL stg.udp_PatientStatus_Leaf(:Package_paramVersionName, :Package_paramLogFlag, :User_varBatchTagAppend);

-- After (no code change — procedure is defined in another converted file)
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "stg.udp_PatientStatus_Leaf" **
CALL stg.udp_PatientStatus_Leaf(:Package_paramVersionName, :Package_paramLogFlag, :User_varBatchTagAppend);
```

### Pattern 3: Object genuinely missing — comment out with user note

```sql
-- Before
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "ErrorTable" **
insert INTO ErrorTable (PackageName, StepName, ErrorDescription)
VALUES (:System_ErrorDescription, :System_PackageName, :System_SourceName);

-- After (commented out, awaiting user decision)
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "ErrorTable" **
-- NEEDS-USER: Table "ErrorTable" not found in converted output. Create the table or provide an alternative.
-- insert INTO ErrorTable (PackageName, StepName, ErrorDescription)
-- VALUES (:System_ErrorDescription, :System_PackageName, :System_SourceName);
```

## Key Points

- This is the **most common** marker. The vast majority of instances are informational and require no code change.
- Do **NOT** remove the FDM comment. It documents a dependency for future reference.
- Focus on **runtime correctness**, not marker elimination. The goal is ensuring the SQL will execute, not removing comments.
- When multiple objects are listed in one marker, evaluate each independently.
- Search the rest of the converted output before concluding an object is genuinely missing.
