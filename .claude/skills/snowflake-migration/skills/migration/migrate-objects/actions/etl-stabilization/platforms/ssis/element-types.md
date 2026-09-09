# SSIS Element Type Reference

Quick reference for understanding what each SSIS element type does and how it maps to Snowflake. Read this when encountering an unfamiliar element type in the `---- Start` tags or assessment data.

## Contents
- Control Flow Tasks (SQL execution, script tasks, file operations, mail)
- Control Flow Containers (loops, sequence grouping)
- Data Flow Components (sources, destinations, transformations, joins)
- Other Elements (precedence constraints, event handlers, package root)

---

## Control Flow Tasks

### Microsoft.ExecuteSQLTask
Runs SQL statements or stored procedures. Operations include truncating tables, creating/altering/dropping objects, running stored procedures, and saving query results into variables. In Snowflake: procedural SQL within a `CREATE TASK` or `CREATE PROCEDURE`.

### Microsoft.ExecutePackageTask
Runs other SSIS packages as part of a workflow. Enables modular design and reuse. In Snowflake: nested `CALL` statements to stored procedures, or separate tasks with `AFTER` dependencies. Variable bindings between parent and child may need manual configuration using session variables or task parameters.

### Microsoft.ScriptTask
Custom C#/VB.NET code for operations not available through built-in tasks. See `SSC-EWI-SSIS0004.md` for detailed conversion guidance including variable assignment patterns, script purpose classification, and boilerplate stripping.

### Microsoft.SendMailTask
Sends email notifications. In Snowflake: `SYSTEM$SEND_EMAIL` via Notification Integrations. Custom SMTP servers cannot be specified.

### Microsoft.FileSystemTask
File move/copy/delete/rename operations on the filesystem. In Snowflake: stage operations (`COPY INTO`, `REMOVE`, `GET`, `PUT`) for stage-based files. On-premise file operations require external orchestration.

### Microsoft.FtpTask
FTP file transfers. In Snowflake: external stages + `COPY INTO` or SnowPipe for automated ingestion.

### Microsoft.ExecuteProcess
Runs external executables. In Snowflake: external orchestration (Airflow, etc.) or Snowpark stored procedures.

### Microsoft.BulkInsertTask
Bulk data loading from files. In Snowflake: `COPY INTO` from stages.

---

## Control Flow Containers

### STOCK:FOREACHLOOP (ForEach Loop Container)
Iterates over a collection (files, recordsets, objects). Variables can be mapped to collection values per iteration. In Snowflake: cursor-based iteration (`FOR row IN cursor DO ... END FOR`) or refactored to set-based operations. File enumerators need Snowflake stage mapping (see `SSC-EWI-SSIS0014.md`).

### STOCK:FORLOOP (For Loop Container)
Repeating workflow with init/eval/iterate expressions (like a programming for-loop). In Snowflake: `WHILE` loop or set-based refactoring.

### Sequence Container
Groups tasks for logical organization and shared variable scope. In Snowflake: converted inline within the parent task body (see `SSC-FDM-SSIS0003.md`). No separate Snowflake construct — contents are expanded in-place.

---

## Data Flow Components

### Microsoft.Pipeline (Data Flow Task)
The entire data flow pipeline — sources → transformations → destinations. In Snowflake: `EXECUTE DBT PROJECT` (when converted to dbt) or `INSERT/SELECT`, `MERGE`, stored procedures with transformation steps.

### Microsoft.OLEDBSource
Extracts data from OLE DB databases (SQL Server, Oracle, etc.). In Snowflake: becomes the source table/query in `FROM` clauses or CTEs within dbt staging models.

### Microsoft.OLEDBDestination
Loads data into OLE DB databases. Supports standard insert and fast-load (bulk). In Snowflake: `INSERT`, `MERGE`, or `COPY INTO` targeting destination tables within dbt mart models.

### Microsoft.DerivedColumn
Creates new column values by applying expressions. In Snowflake: `SELECT` expressions with calculated columns (casts, concatenation, CASE, etc.) within dbt intermediate models.

### Microsoft.Lookup
Joins against a reference table to enrich rows. Returns first matching row. In Snowflake: `JOIN` with `QUALIFY ROW_NUMBER()` for deterministic first-match. See `SSC-FDM-SSIS0001.md` for the ORDER BY NULL pattern.

### Microsoft.ConditionalSplit
Routes rows to different outputs based on boolean conditions. In Snowflake: `CASE WHEN` expressions or separate dbt models with `WHERE` filters for each output path.

### Microsoft.MergeJoin
Sorted join of two inputs. In Snowflake: standard SQL `JOIN`. See `SSC-FDM-SSIS0004.md` for ORDER BY considerations.

### Microsoft.Merge
Combines two sorted inputs into one sorted output. In Snowflake: `UNION ALL` with `ORDER BY`. See `SSC-FDM-SSIS0002.md`.

### Microsoft.UnionAll
Combines multiple inputs without sorting. In Snowflake: `UNION ALL` (direct equivalent).

### Microsoft.Multicast
Sends rows to multiple outputs (copies data). In Snowflake: multiple `INSERT` statements or dbt models reading from the same source.

### Microsoft.RowCount
Counts rows passing through. In Snowflake: `COUNT(*)` or `SQLROWCOUNT` after DML.

### Microsoft.DataConversion
Type casting of columns. In Snowflake: `CAST()` or `::` operator in `SELECT` expressions.

### Microsoft.SortTransform
Sorts data by specified columns. In Snowflake: `ORDER BY` clause.

---

## Other Elements

### PrecedenceConstraint
Defines execution order and conditional branching between tasks. Evaluates: execution result (Success/Failure/Completion), boolean expressions, or both. In Snowflake: sequential execution order via `AFTER` clauses on tasks, `IF/ELSE` conditional blocks, or `BEGIN/EXCEPTION` for success/failure branching.

### EventHandler
Responds to events during execution (OnError, OnPreExecute, OnPostExecute, OnTaskFailed). In Snowflake: `BEGIN/EXCEPTION` blocks for error handlers, `SYSTEM$SEND_EMAIL` for notifications. See `SSC-FDM-SSIS0006.md`.

### Package
The top-level SSIS package container. In Snowflake: the root `CREATE TASK` that initializes variables from `CONFIG` and chains child tasks via `AFTER` dependencies.
