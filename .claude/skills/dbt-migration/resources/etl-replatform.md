# ETL Replatform (SSIS Migration)

SnowConvert AI's ETL Replatform feature converts SSIS (SQL Server Integration Services) packages to
modern cloud-native architecture on Snowflake using dbt and Snowflake Tasks.

## Conversion Mapping

| SSIS Component           | Snowflake Target                               |
| ------------------------ | ---------------------------------------------- |
| Data Flow Tasks          | dbt projects                                   |
| Control Flow logic       | Snowflake TASKs or stored procedures           |
| SSIS Variables           | control_variables table + UDFs + dbt variables |
| Sequence/Loop Containers | Inline conversion within parent TASK/procedure |

## Output Structure

```text
Output/ETL/
├── etl_configuration/           # Shared infrastructure
│   ├── tables/                  # control_variables_table.sql
│   ├── functions/               # GetControlVariableUDF.sql
│   └── procedures/              # UpdateControlVariable.sql
├── {PackageName}/
│   ├── {PackageName}.sql        # Orchestration (TASK or PROCEDURE)
│   └── {DataFlowTaskName}/      # dbt project per Data Flow Task
│       ├── dbt_project.yml
│       ├── profiles.yml
│       └── models/
│           ├── sources.yml
│           ├── staging/         # stg_raw__{component}.sql
│           ├── intermediate/    # int_{component}.sql
│           └── marts/           # {destination}.sql
```

## dbt Project Layers

| Layer         | Materialization      | Purpose                                |
| ------------- | -------------------- | -------------------------------------- |
| staging/      | View                 | Clean, type-safe access to source data |
| intermediate/ | Ephemeral            | Transformation logic (not persisted)   |
| marts/        | Incremental or Table | Final business-ready data models       |

## Prerequisites

- SnowConvert AI
- DTSX files extracted from ISPAC (ISPAC not directly supported)
- SSIS package version 8 or later
- Source dependencies accessible in Snowflake (for running migrated project)

## Migration Steps

1. Select path to DDL scripts (for data type identification)
2. Click the Replatform card in SnowConvert AI
3. Browse to SSIS project folder containing DTSX files
4. Review migration reports and fix identified issues
5. Fill placeholders in `sources.yml`, `profiles.yml`, `dbt_project.yml`
6. Deploy dbt project using Snowflake CLI or Workspace
7. Run orchestration (EXECUTE TASK or CALL procedure)

## Deployment Options

**Snowflake CLI:**

```bash
snow dbt deploy --schema schema_name --database database_name --force package_name
```

**Snowflake Workspace:** Navigate to Workspaces > Add new > Upload Folder, then Connect > Deploy dbt
project

## Orchestration Patterns

- **Standard packages**: Converted to Snowflake TASK objects with AFTER dependencies
- **Reusable packages** (called by ExecutePackage): Converted to stored procedures for synchronous
  execution

## Documentation

- [ETL Migration Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/etl-migration-replatform)
- [SSIS Translation Reference](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/ssis/README)
- [dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)
