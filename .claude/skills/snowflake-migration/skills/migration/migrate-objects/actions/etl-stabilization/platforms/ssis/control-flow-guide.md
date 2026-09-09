# DTSX XML Navigation Guide — Control Flow

The DTSX file is XML that describes the entire SSIS package. This guide covers **control flow** navigation (for data flow navigation used by dbt-test-gen, see `../dbt-test-gen/SKILL.md`).

## Contents

- Namespaces
- Package Structure — Executable Hierarchy
- Execute SQL Task — Extracting SQL and Parameters
- Script Task — Variable Bindings and Source Code
- ForEach Loop Container — Enumerator Configuration
- Event Handlers
- Connection Managers
- Common DTS:DataType Codes

## Namespaces

DTSX files use several XML namespaces:

- `DTS` — `www.microsoft.com/SqlServer/Dts` (package metadata, executables, variables, precedence constraints)
- `SQLTask` — `www.microsoft.com/sqlserver/dts/tasks/sqltask` (Execute SQL Task configuration)

## Package Structure — Executable Hierarchy

```
DTS:Executable (root package)
  ├─ @DTS:ObjectName              ← package display name
  ├─ DTS:Variables
  │    └─ DTS:Variable            ← package-level variables
  │         ├─ @DTS:ObjectName    ← variable name
  │         ├─ @DTS:Namespace     ← "User" or "System"
  │         ├─ @DTS:DataType      ← type code (2=Int16, 3=Int32, 8=String, 11=Boolean, 7=Date, 20=Int64)
  │         ├─ @DTS:Expression    ← expression (if computed variable)
  │         └─ DTS:VariableValue  ← default value (text content)
  ├─ DTS:Executables
  │    └─ DTS:Executable (task or container)
  │         ├─ @DTS:ExecutableType  ← task type identifier
  │         ├─ @DTS:ObjectName      ← task display name
  │         ├─ @DTS:Disabled        ← "True" if disabled
  │         ├─ DTS:Variables        ← task-scoped variables
  │         ├─ DTS:ObjectData       ← task-specific configuration
  │         ├─ DTS:Executables      ← child tasks (for containers)
  │         └─ DTS:EventHandlers    ← event handlers attached to this task
  └─ DTS:PrecedenceConstraints
       └─ DTS:PrecedenceConstraint
            ├─ @DTS:From           ← source executable DTSID
            ├─ @DTS:To             ← target executable DTSID
            ├─ @DTS:Value          ← 0=Success, 1=Failure, 2=Completion
            ├─ @DTS:Expression     ← boolean expression (optional)
            └─ @DTS:LogicalAnd     ← "True" if AND with result, "False" if OR
```

## Execute SQL Task — Extracting SQL and Parameters

```
DTS:Executable[@DTS:ExecutableType="Microsoft.ExecuteSQLTask"]
  └─ DTS:ObjectData
       └─ SQLTask:SqlTaskData
            ├─ @SQLTask:SqlStatementSource  ← the original T-SQL query text
            ├─ @SQLTask:ResultType          ← "ResultSetType_None", "ResultSetType_Rowset", "ResultSetType_SingleRow"
            ├─ @SQLTask:Connection          ← connection manager reference
            └─ SQLTask:ParameterBinding     ← parameter-to-variable mappings
                 ├─ @SQLTask:ParameterName  ← parameter ordinal or name
                 ├─ @SQLTask:DtsVariableName ← SSIS variable bound to this parameter
                 └─ @SQLTask:ParameterDirection ← "Input", "Output", "ReturnValue"
```

The `SqlStatementSource` contains the full T-SQL query. This is the primary source of truth for test assertions — it reveals what tables are read, what transformations are applied, and what the output should look like.

Parameter bindings map `@ParameterName` placeholders in the SQL to SSIS variables. In the Snowflake conversion, these become `:Variable_Name` bind variables or `GetControlVariableUDF` calls.

## Script Task — Variable Bindings and Source Code

```
DTS:Executable[@DTS:ExecutableType="Microsoft.ScriptTask"]
  └─ DTS:ObjectData
       └─ ScriptProject
            ├─ ReadOnlyVariables   ← comma-separated list of variables the script reads
            ├─ ReadWriteVariables  ← comma-separated list of variables the script writes
            └─ ProjectItem[@Name="ScriptMain.cs"]
                 └─ (CDATA section with C# source code)
```

The `ReadWriteVariables` list identifies which variables the script modifies — these are the variables to assert on after execution. The C# source (when available) reveals the transformation logic:
- `Dts.Variables["User::VarName"].Value = ...` → `UpdateControlVariable('User::VarName', ...)`
- Common patterns: date calculations, string formatting, conditional assignments

## ForEach Loop Container — Enumerator Configuration

```
DTS:Executable[@DTS:ExecutableType="STOCK:FOREACHLOOP"]
  ├─ DTS:ForEachEnumerator
  │    ├─ @DTS:ObjectName          ← enumerator display name
  │    └─ DTS:ObjectData
  │         └─ (enumerator-specific configuration)
  │              SSIS:ForEachFileEnumerator   ← file enumerator
  │              SSIS:ForEachADOEnumerator    ← ADO recordset enumerator
  ├─ DTS:ForEachVariableMappings
  │    └─ DTS:ForEachVariableMapping
  │         ├─ @DTS:VariableName   ← variable populated per iteration
  │         └─ @DTS:ValueIndex     ← index in the enumerator output
  └─ DTS:Executables               ← loop body (child tasks)
```

The enumerator type determines how to mock the iteration:
- **File Enumerator** → stage listing (often untestable in V1 — document as coverage gap)
- **ADO Enumerator** → result set from a prior query (mock with synthetic rows in a temporary table)
- **Variable Enumerator** → iterate over variable values (populate via control_variables)

## Event Handlers

```
DTS:EventHandlers
  └─ DTS:EventHandler
       ├─ @DTS:EventName           ← "OnError", "OnPreExecute", "OnPostExecute", "OnTaskFailed"
       └─ DTS:Executables          ← handler tasks (same structure as control flow tasks)
```

In Snowflake, `OnError` handlers should map to `BEGIN/EXCEPTION` blocks. `OnPreExecute`/`OnPostExecute` are often redundant (Snowflake has `TASK_HISTORY()`). `OnWarning`/`OnInformation` are typically informational and skipped.

## Connection Managers

```
DTS:ConnectionManagers
  └─ DTS:ConnectionManager
       ├─ @DTS:ObjectName          ← connection display name
       ├─ @DTS:CreationName        ← provider type (e.g., "OLEDB", "FLATFILE")
       └─ DTS:ObjectData
            └─ DTS:ConnectionManager
                 └─ @DTS:ConnectionString  ← full connection string with server, database, catalog
```

Connection strings reveal the original database names and servers. These help identify which database references in the converted SQL need rewriting in the ACT section.

## Common DTS:DataType Codes

| Code | SSIS Type | Snowflake Equivalent |
|------|-----------|---------------------|
| 2 | DT_I2 (Int16) | NUMBER(5,0) |
| 3 | DT_I4 (Int32) | NUMBER(10,0) |
| 7 | DT_DATE (Date) | DATE |
| 8 | DT_BSTR / DT_WSTR (String) | VARCHAR |
| 11 | DT_BOOL (Boolean) | BOOLEAN |
| 13 | DT_DBTIMESTAMP (DateTime) | TIMESTAMP_NTZ |
| 20 | DT_I8 (Int64) | NUMBER(19,0) |
