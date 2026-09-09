# SSC-EWI-SSIS0004 — Control Flow Element Cannot Be Converted

An SSIS control flow element (FileSystemTask, FTP Task, Script Task, third-party component, etc.) has no direct Snowflake equivalent. The `!!!RESOLVE EWI!!!` marker **breaks compilation**. The original SSIS XML is preserved as comments for reference.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Marker type | `!!!RESOLVE EWI!!!` (compilation-breaking) |
| Breaks compilation? | **Yes** |
| Frequency | Moderate (once per unconvertible control flow element) |
| Common action | Remove marker, keep SSIS XML comments, add needs-user recommendation |

## Identification

Look for the marker:
```
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT <ElementType> CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
```

Followed by the original SSIS XML commented out:
```sql
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT Microsoft.FileSystemTask CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<Executable ExecutableType="Microsoft.FileSystemTask" refId="Package\Foreach Loop Container\File System Task" ...>
--  <EventHandlers />
--</Executable>
 ;
```

The trailing `;` after the commented XML is a placeholder statement that SnowConvert inserts to maintain syntactic structure.

## Decision Tree

1. **What type of control flow element is it?**
   - Identify the `ExecutableType` from the marker or the commented XML.
   - Use the element-type table below to determine the recommended approach.

2. **Does the element perform file operations (move, copy, delete)?**
   - `Microsoft.FileSystemTask` — file move/copy/delete/rename operations
   - **Action:** Replace with Snowflake stage operations if files are stage-based, or mark as needs-user for on-premise file operations.

3. **Does the element perform network transfers (FTP, SFTP)?**
   - `Microsoft.FtpTask` or third-party SFTP tasks (e.g., `ZappySys.SecureFtpTask`)
   - **Action:** Mark as needs-user. Suggest external data loading approach (SnowPipe, external stages).

4. **Is it a Script Task or custom component?**
   - Contains arbitrary .NET code or third-party logic.
   - **Action:** Mark as needs-user. Suggest Snowpark UDF or stored procedure if logic is simple.

5. **Is it a third-party component?**
   - `ZappySys.*`, `CozyRoc.*`, or other non-Microsoft executable types.
   - **Action:** Mark as needs-user. These require manual replacement.

## Element Type Reference

| SSIS Element Type | Snowflake Approach | Auto-fixable? |
|-------------------|--------------------|---------------|
| `Microsoft.FileSystemTask` | Stage operations (`COPY`, `REMOVE`) | Partially |
| `Microsoft.FtpTask` | External stage + SnowPipe | No |
| `ZappySys.SecureFtpTask` | External stage + SnowPipe | No |
| `Microsoft.ScriptTask` | Stored procedure, SQL variable logic, or Snowpark UDF | **Partially — see ScriptTask section** |
| `Microsoft.SendMailTask` | External notification service | No |
| `Microsoft.ExecuteProcess` | External orchestration | No |

---

## ScriptTask Conversion (Microsoft.ScriptTask)

ScriptTask is the most complex unconvertible element because it contains arbitrary C#/VB.NET code. However, many ScriptTasks perform operations that CAN be converted to Snowflake SQL. Analyze the script logic before marking as needs-user.

### Step 1: Extract the Relevant Code

ScriptTask XML contains a full C# project with many files. Only `ScriptMain.cs` matters — it contains the `Main()` method with the actual business logic. Ignore: `AssemblyInfo.cs`, `Settings.settings`, `Resources.resx`, `*.Designer.cs`, `.csproj` XML. These are boilerplate and can be 50-100x larger than the actual logic.

Look for this pattern in the commented XML:
```
--  <ProjectItem Name="ScriptMain.cs">
--    ... actual C# code ...
--  </ProjectItem>
```

### Step 2: Classify the Script's Purpose

| Script Purpose | Snowflake Equivalent | Approach |
|---------------|---------------------|----------|
| Logging / monitoring (writing to log files, calculating durations, setting status flags) | Snowflake provides native observability: `QUERY_HISTORY`, `TASK_HISTORY`, `EVENT TABLE`, `SYSTEM$LOG()` | Eliminate the script. If custom logging is needed, use `INSERT` into a logging table or `SYSTEM$LOG_INFO` / `SYSTEM$LOG_ERROR` |
| Variable computation / conditional logic (calculating values, evaluating conditions, setting package variables) | SQL variable assignments, `CASE` expressions, `IF/ELSE` blocks | Convert to SQL inside the stored procedure |
| File system operations (checking file existence, moving/renaming) | Stage operations: `LIST @stage`, directory tables, `GET`/`PUT`, `METADATA$FILENAME` | Replace with stage operations, or use Snowpark for complex file orchestration |
| Web service / API calls | External functions, external network access integrations | Move to external orchestrator or Snowflake external function |
| Data transformation logic | SQL expressions, SQL UDFs, Snowpark UDFs | Refactor into SQL |

### Step 3: Handle SSIS Variable Assignments

**CRITICAL**: When the C# code sets an SSIS user variable, you MUST convert it to a `CALL` to the `UpdateControlVariable` procedure.

```csharp
// C# (in ScriptMain.cs)
Dts.Variables["User::SomeName"].Value = someValue;
// or
Dts.Variables["SomeName"].Value = someValue;
```

Converts to:
```sql
CALL public.UpdateControlVariable('User_SomeName', '<SCOPE>', TO_VARIANT(someValue));
```

Where:
- `User_SomeName` — variable name with `::` replaced by `_`
- `<SCOPE>` — the package name. Find it in existing `UpdateControlVariable` calls in the same task, or use the package name from the task context
- `someValue` — the computed value converted to a SQL expression

**Example:**
```csharp
// C#: Calculate package duration and store it
Dts.Variables["PackageDuration"].Value = DateTime.Now.Subtract(startTime).TotalSeconds.ToString();
```
```sql
-- Snowflake SQL equivalent:
CALL public.UpdateControlVariable('User_PackageDuration', 'MyPackageName', TO_VARIANT(DATEDIFF('second', :System_StartTime, CURRENT_TIMESTAMP())::VARCHAR));
```

### Step 4: Clean Up After Successful Conversion

When the ScriptTask logic has been successfully converted to SQL, **remove all the commented SSIS XML metadata** from the fixed code. Only leave a short summary comment (1-2 lines) describing what the original ScriptTask did. The verbose XML is no longer needed once the logic is faithfully reproduced in SQL.

```sql
-- Good: clean result after successful conversion
-- Converted from ScriptTask: calculates package duration and stores it in User_PackageDuration
CALL public.UpdateControlVariable('User_PackageDuration', 'MyPackageName', TO_VARIANT(DATEDIFF('second', :System_StartTime, CURRENT_TIMESTAMP())::VARCHAR));
```

```sql
-- Bad: leaving hundreds of lines of SSIS XML after a successful conversion
-- Converted from ScriptTask: calculates package duration
CALL public.UpdateControlVariable('User_PackageDuration', 'MyPackageName', TO_VARIANT(DATEDIFF('second', :System_StartTime, CURRENT_TIMESTAMP())::VARCHAR));
--<Executable ExecutableType="Microsoft.ScriptTask" ...>
--  <ScriptProject ...>
--    ... 50+ lines of C# project boilerplate, AssemblyInfo, etc. ...
--  </ScriptProject>
--</Executable>
```

**Exception**: If the conversion is only partial (some logic could not be translated), keep the relevant portions of the XML as reference for the user and add a `NEEDS-USER` comment for the unconverted parts.

### Step 5: Handle Acceptable Infrastructure Errors

After converting a ScriptTask to SQL, the code may reference infrastructure that doesn't exist in the target environment (e.g., `UpdateControlVariable` procedure, logging tables). If the conversion is logically correct but fails because the infrastructure is missing, treat this as **success** — the conversion is right, the infrastructure just needs to be deployed separately.

### Step 6: Disabled ScriptTasks

If the original SSIS ScriptTask was **disabled** (check `DTS:Disabled="True"` in the XML attributes), the element can typically be safely removed or commented out entirely. Note this in the fix log.

---

## Fix Patterns

### Pattern 1: FileSystemTask — stage-based file move

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT Microsoft.FileSystemTask CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<Executable ExecutableType="Microsoft.FileSystemTask" refId="Package\Foreach Loop Container\File System Task" ...>
--  <EventHandlers />
--</Executable>
 ;

-- After (stage-based replacement)
-- NEEDS-USER: Original SSIS FileSystemTask moved files between directories.
-- If source files are in a Snowflake stage, use:
--   COPY INTO @archive_stage FROM @source_stage;
--   REMOVE @source_stage/filename;
-- Original SSIS XML preserved below for reference:
--<Executable ExecutableType="Microsoft.FileSystemTask" refId="Package\Foreach Loop Container\File System Task" ...>
--  <EventHandlers />
--</Executable>
```

### Pattern 2: Third-party FTP/SFTP task

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT ZappySys.SecureFtpTask CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<Executable ExecutableType="ZappySys.SecureFtpTask" refId="Package\ZS Secure FTP Task" ...>
--  <EventHandlers />
--</Executable>
 ;

-- After (marker removed, needs-user recommendation added)
-- NEEDS-USER: Original SSIS task used ZappySys.SecureFtpTask for SFTP file transfer.
-- Recommended Snowflake approach:
--   1. Create an external stage pointing to the SFTP/cloud storage location
--   2. Use COPY INTO to load data from the stage
--   3. Set up SnowPipe for automated ingestion if needed
-- Original SSIS XML preserved below for reference:
--<Executable ExecutableType="ZappySys.SecureFtpTask" refId="Package\ZS Secure FTP Task" ...>
--  <EventHandlers />
--</Executable>
```

### Pattern 3: ScriptTask — convert C# logic to SQL

When the ScriptTask contains simple logic (variable computation, logging), convert it directly. Follow the ScriptTask Conversion section above. On successful conversion, remove all the SSIS XML metadata and leave only a brief summary of what the original code did.

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT Microsoft.ScriptTask CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<Executable ExecutableType="Microsoft.ScriptTask" ...>
--  <ScriptProject ...>
--    <ProjectItem Name="ScriptMain.cs">
--      // public void Main() {
--      //   Dts.Variables["PackageDuration"].Value = DateTime.Now.Subtract(startTime).TotalSeconds.ToString();
--      //   Dts.TaskResult = (int)ScriptResults.Success;
--      // }
--    </ProjectItem>
--  </ScriptProject>
--</Executable>
 ;

-- After (converted to SQL, SSIS XML removed, only summary remains)
-- Converted from ScriptTask: calculates package execution duration and stores it in User_PackageDuration
CALL public.UpdateControlVariable('User_PackageDuration', 'MyPackageName', TO_VARIANT(DATEDIFF('second', :System_StartTime, CURRENT_TIMESTAMP())::VARCHAR));
```

### Pattern 4: Minimal fix — remove marker, keep placeholder

When the element type is unknown or complex, the safest approach is to remove only the compilation-breaking marker:

```sql
-- Before (breaks compilation)
!!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT Microsoft.ExecuteProcess CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
--<Executable ExecutableType="Microsoft.ExecuteProcess" ...>
--  ...original SSIS XML...
--</Executable>
 ;

-- After (compiles, but needs manual implementation)
-- NEEDS-USER: SSIS Microsoft.ExecuteProcess element requires manual replacement.
-- See commented SSIS XML below for original behavior.
--<Executable ExecutableType="Microsoft.ExecuteProcess" ...>
--  ...original SSIS XML...
--</Executable>
```

## Context: Where These Appear

These markers typically appear inside task bodies, often within loop constructs (Foreach Loop Container). A single task graph file can contain multiple instances:

```sql
CREATE OR REPLACE TASK public.package_foreach_loop_container
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.tgbsftp
AS
BEGIN
   -- ... loop setup ...
   FOR row IN cursor DO
      !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - ... ***/!!!
      --<Executable ...>
      --</Executable>
       ;
   END FOR;
END;
```

After fixing, the task body must remain syntactically valid. If the element was the only statement inside a loop or block, ensure the block still has at least one valid statement (use `NULL;` as a no-op if needed).

## Key Points

- **Must** remove the `!!!RESOLVE EWI!!!` marker line — it breaks compilation.
- **For ScriptTask**: If the C# logic is successfully converted to SQL, **remove all the commented SSIS XML** and leave only a 1-2 line summary comment describing what the original ScriptTask did. The XML metadata is only useful when the conversion is incomplete or the element is marked as needs-user.
- **For other element types** (FileSystemTask, FTP, third-party): **Keep** the commented SSIS XML — it documents the original behavior for the user since these are typically marked as needs-user.
- Ensure the surrounding block (loop, task body) remains syntactically valid after removing the marker.
- The trailing ` ;` (space + semicolon) after the commented XML is intentional — keep it as a no-op statement placeholder when the element is not replaced with actual SQL.
