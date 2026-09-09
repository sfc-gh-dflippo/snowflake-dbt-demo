# SSC-EWI-SSIS0014 — ForEach File Enumerator Stage Mapping Required

A ForEach File Enumerator's folder path requires manual mapping to a Snowflake stage. The `!!!RESOLVE EWI!!!` marker **breaks compilation**. SSIS enumerates files on a local/network file system; Snowflake uses stages for file access.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Low (once per ForEach File Enumerator) |
| Common action | Replace file system path with Snowflake stage reference |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - FOREACH FILE ENUMERATOR FOLDER PATH REQUIRES MANUAL MAPPING TO SNOWFLAKE STAGE. ***/!!!
```

It appears inside a loop that originally iterated over files in a directory:

```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - FOREACH FILE ENUMERATOR FOLDER PATH REQUIRES MANUAL MAPPING TO SNOWFLAKE STAGE. ***/!!!
-- Original path: \\server\share\data\incoming\
FOR file_row IN (SELECT ???) DO
   -- ... file processing logic ...
END FOR;
```

## Fix Patterns

### Pattern 1: Replace with LIST @stage query

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - FOREACH FILE ENUMERATOR FOLDER PATH REQUIRES MANUAL MAPPING TO SNOWFLAKE STAGE. ***/!!!
-- Original path: \\server\share\data\incoming\
FOR file_row IN (SELECT ???) DO
   COPY INTO raw_data FROM ???;
END FOR;

-- After (uses Snowflake stage)
-- NEEDS-USER: Map original path \\server\share\data\incoming\ to a Snowflake stage.
-- Create stage: CREATE STAGE IF NOT EXISTS @my_stage URL='s3://bucket/incoming/';
FOR file_row IN (
   SELECT "name" AS file_name
   FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
   AFTER (EXECUTE IMMEDIATE 'LIST @my_stage/incoming/ PATTERN=''.*\\.csv''')
) DO
   COPY INTO raw_data FROM @my_stage/incoming/
      FILES = (file_row.file_name)
      FILE_FORMAT = (TYPE = 'CSV');
END FOR;
```

### Pattern 2: Simple single-directory load (no loop needed)

When all files in the directory are loaded identically, the loop can be replaced with a single COPY INTO:

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0014 - FOREACH FILE ENUMERATOR FOLDER PATH REQUIRES MANUAL MAPPING TO SNOWFLAKE STAGE. ***/!!!
-- Original path: C:\ETL\DataFiles\
FOR file_row IN (...) DO
   COPY INTO target_table FROM ???;
END FOR;

-- After (simplified — no loop needed)
-- NEEDS-USER: Verify stage @data_stage points to the correct location.
COPY INTO target_table
FROM @data_stage/DataFiles/
FILE_FORMAT = (TYPE = 'CSV')
PATTERN = '.*\.csv';
```

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker line — it breaks compilation.
- The original file system path (UNC or local) is typically in the commented SSIS XML or the marker comment. Document it for the user.
- Mark as **needs-user** — stage creation and path mapping require environment-specific knowledge.
- If the SSIS package used a variable for the folder path, the stage path may also need to be parameterized.
- Consider whether the loop is even necessary — Snowflake's `COPY INTO` with `PATTERN` can process multiple files in one statement.
