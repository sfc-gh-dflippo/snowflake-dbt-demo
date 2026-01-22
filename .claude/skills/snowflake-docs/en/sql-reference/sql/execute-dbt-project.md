---
auto_generated: true
description: Executes the specified dbt project object or the dbt project in a Snowflake
  workspace using the dbt command and command-line options specified.
last_scraped: '2026-01-14T16:57:10.364857+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/execute-dbt-project
title: EXECUTE DBT PROJECT | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)

     + [CREATE DBT PROJECT](create-dbt-project.md)
     + [ALTER DBT PROJECT](alter-dbt-project.md)
     + [EXECUTE DBT PROJECT](execute-dbt-project.md)
     + [DESCRIBE DBT PROJECT](desc-dbt-project.md)
     + [DROP DBT PROJECT](drop-dbt-project.md)
     + [SHOW DBT PROJECTS](show-dbt-projects.md)
     + [SHOW VERSIONS IN DBT PROJECT](show-versions-in-dbt-project.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)EXECUTE DBT PROJECT

# EXECUTE DBT PROJECT[¶](#execute-dbt-project "Link to this heading")

Executes the specified [dbt project object](../../user-guide/data-engineering/dbt-projects-on-snowflake) or the dbt project in a Snowflake workspace using the dbt command and command-line options specified.

See also:
:   [CREATE DBT PROJECT](create-dbt-project), [ALTER DBT PROJECT](alter-dbt-project), [DESCRIBE DBT PROJECT](desc-dbt-project), [DROP DBT PROJECT](drop-dbt-project), [SHOW DBT PROJECTS](show-dbt-projects)

## Syntax[¶](#syntax "Link to this heading")

Executes the dbt project object with the specified name.

```
EXECUTE DBT PROJECT [ IF EXISTS ] <name>
  [ ARGS = '[ <dbt_command> ] [ --<dbt_cli_option> <option_value_1> [ ... ] ] [ ... ]' ]
```

Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

Executes the dbt project that is saved in a workspace with the specified workspace name. The user who owns the workspace must be the user who runs this command variant.

```
EXECUTE DBT PROJECT [ IF EXISTS ] [ FROM WORKSPACE <name> ]
  [ ARGS = '[ <dbt_command> ] [ --<dbt_cli_option> <option_value_1> [ ... ] [ ... ] ]' ]
  [ PROJECT_ROOT = '<subdirectory_path>' ]
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   When executing a dbt project object, specifies the name of the dbt project object to execute.

    When executing a dbt project by using the FROM WORKSPACE option, specifies the name of the workspace for dbt Projects on Snowflake. The workspace name is always specified in reference to the `public` schema in the user’s personal database, which is indicated by `user$`.

    We recommend enclosing the workspace name in double quotes because workspace names are case-sensitive and can contain special characters.

    The following example shows a workspace name reference:

    `user$.public."My dbt Project Workspace"`

## Optional parameters[¶](#optional-parameters "Link to this heading")

`ARGS = '[ dbt_command ] [ --dbt_cli_option option_value_1 [ ... ] [ ... ] ]'`
:   Specifies the [dbt command](https://docs.getdbt.com/reference/dbt-commands) and supported [command-line options](https://docs.getdbt.com/reference/global-configs/about-global-configs#available-flags) to run when the dbt project executes. This is a literal string that must conform to the syntax and requirements of dbt CLI commands.

    If no value is specified, the dbt project executes with the [dbt command](https://docs.getdbt.com/reference/dbt-commands) and [command-line options](https://docs.getdbt.com/reference/global-configs/about-global-configs#available-flags) specified in the [dbt project object definition](create-dbt-project). If you specify dbt CLI options without specifying a dbt command, the dbt `run` command executes by default.

    Default: No value

`PROJECT_ROOT = 'subdirectory_path'`
:   Specifies the subdirectory path to the `dbt_project.yml` file within the dbt project object or workspace. This parameter is only supported when executing a dbt project by using the FROM WORKSPACE option.

    If no value is specified, the dbt project executes with the `dbt_project.yml` file in the root directory of the dbt project object.

    If no `dbt_project.yml` file exists in the root directory or in the PROJECT\_ROOT subdirectory, an error occurs.

    Default: No value

## Output[¶](#output "Link to this heading")

| Column | Description |
| --- | --- |
| `0|1 Success` | `TRUE` if the dbt project executed successfully; otherwise, `FALSE`. If the dbt project fails to execute, an exception message is returned. |
| `EXCEPTION` | Any exception message returned by the dbt project execution. If the dbt project executes successfully, the string `None` is returned. |
| `STDOUT` | The standard output returned by the dbt project execution. |
| `OUTPUT_ARCHIVE_URL` | The URL of the output archive that contains output files of the dbt project execution. This includes log files and artifacts that dbt writes to the `/target` directory. For more information, see [About dbt artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts) in dbt documentation. Selecting this link directly results in an error; however, you can use this URL to retrieve dbt project files and output. For more information, see [Access dbt artifacts and logs programmatically](../../user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability.html#label-dbt-projects-artifacts-and-logs). |

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE | dbt project |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

Note

The dbt command specified in EXECUTE DBT PROJECT runs with the privileges of the `role` specified in the `outputs` block of the projects `profiles.yml` file. Operations are further restricted to only those privileges granted to the Snowflake user calling EXECUTE DBT PROJECT. Both the user and the role specified must have the required privileges to use the `warehouse`, perform operations on the `database` and `schema` specified in the project’s `profiles.yml` file, and perform operations on any other Snowflake objects that the dbt model specifies.

## Examples[¶](#examples "Link to this heading")

* [Default run command with target and models specified](#label-execute-dbt-project-default-run-example)
* [Explicit test command with target and models specified](#label-execute-dbt-project-test-example)
* [Explicit run command with downstream models specified](#label-execute-dbt-project-explicit-run-example)
* [Run and test dbt projects using production tasks](#label-execute-dbt-project-tasks-example)

### Default run command with target and models specified[¶](#default-run-command-with-target-and-models-specified "Link to this heading")

Execute a dbt `run` targeting the `dev` profile in the `dbt_project.yml` file in the root directory of the dbt project object and selecting three models from the project DAG. No `run` command is explicitly specified and is executed by default.

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = '--select simple_customers combined_bookings prepped_data --target dev';
```

Copy

### Explicit test command with target and models specified[¶](#explicit-test-command-with-target-and-models-specified "Link to this heading")

Execute a dbt `test` command targeting the `prod` profile in the `dbt_project.yml` file in the root directory of the dbt project object and selecting three models from the project DAG.

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = '--select simple_customers combined_bookings prepped_data --target prod';
```

Copy

### Explicit run command with downstream models specified[¶](#explicit-run-command-with-downstream-models-specified "Link to this heading")

Execute a dbt `run` command targeting the `dev` profile in the `dbt_project.yml` file and selecting all models downstream of the `simple_customers` model using the dbt `+` notation.

```
EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project
  ARGS = 'run --select simple_customers+ --target dev';
```

Copy

### Run and test dbt projects using production tasks[¶](#run-and-test-dbt-projects-using-production-tasks "Link to this heading")

Create a task for a production dbt target that executes a dbt `run` command on a six-hour interval. Then create a task that executes the dbt `test` command after each dbt `run` task completes. The EXECUTE DBT PROJECT command for each task targets the `prod` profile in the `dbt_project.yml` file in the root directory of the dbt project object.

```
CREATE OR ALTER TASK my_database.my_schema.run_dbt_project
  WAREHOUSE = my_warehouse
  SCHEDULE = '6 hours'
AS
  EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project args='run --target prod';


CREATE OR ALTER TASK change_this.public.test_dbt_project
        WAREHOUSE = my_warehouse
        AFTER run_dbt_project
AS
  EXECUTE DBT PROJECT my_database.my_schema.my_dbt_project args='test --target prod';
```

Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Variant syntax](#variant-syntax)
3. [Required parameters](#required-parameters)
4. [Optional parameters](#optional-parameters)
5. [Output](#output)
6. [Access control requirements](#access-control-requirements)
7. [Examples](#examples)

Related content

1. [dbt Projects on Snowflake](/sql-reference/sql/../../user-guide/data-engineering/dbt-projects-on-snowflake)