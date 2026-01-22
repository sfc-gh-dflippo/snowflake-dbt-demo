---
auto_generated: true
description: Sets parameters that change the behavior for the current session.
last_scraped: '2026-01-14T16:55:35.758805+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/alter-session
title: ALTER SESSION | Snowflake Documentation
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

     + Parameters
     + [ALTER SESSION](alter-session.md)
     + [SHOW PARAMETERS](show-parameters.md)
     + Context
     + [USE ROLE](use-role.md)
     + [USE SECONDARY ROLES](use-secondary-roles.md)
     + [USE WAREHOUSE](use-warehouse.md)
     + [USE DATABASE](use-database.md)
     + [USE SCHEMA](use-schema.md)
     + Variables
     + [SET](set.md)
     + [UNSET](unset.md)
     + [SHOW VARIABLES](show-variables.md)
     + Queries
     + [EXPLAIN](explain.md)
     + [DESCRIBE RESULT](desc-result.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Sessions](../commands-session.md)ALTER SESSION

# ALTER SESSION[¶](#alter-session "Link to this heading")

Sets parameters that change the behavior for the current session.

See also:
:   [SHOW PARAMETERS](show-parameters)

## Syntax[¶](#syntax "Link to this heading")

```
ALTER SESSION SET sessionParams

ALTER SESSION UNSET <param_name> [ , <param_name> , ... ]
```

Copy

Where:

> ```
> sessionParams ::=
>   ABORT_DETACHED_QUERY = TRUE | FALSE
>   ACTIVE_PYTHON_PROFILER = 'LINE' | 'MEMORY'
>   AUTOCOMMIT = TRUE | FALSE
>   BINARY_INPUT_FORMAT = <string>
>   BINARY_OUTPUT_FORMAT = <string>
>   DATE_INPUT_FORMAT = <string>
>   DATE_OUTPUT_FORMAT = <string>
>   ERROR_ON_NONDETERMINISTIC_MERGE = TRUE | FALSE
>   ERROR_ON_NONDETERMINISTIC_UPDATE = TRUE | FALSE
>   GEOGRAPHY_OUTPUT_FORMAT = 'GeoJSON' | 'WKT' | 'WKB' | 'EWKT' | 'EWKB'
>   HYBRID_TABLE_LOCK_TIMEOUT = <num>
>   JSON_INDENT = <num>
>   LOG_LEVEL = <string>
>   LOCK_TIMEOUT = <num>
>   PYTHON_PROFILER_TARGET_STAGE = <string>
>   PYTHON_PROFILER_MODULES = <string>
>   QUERY_TAG = <string>
>   ROWS_PER_RESULTSET = <num>
>   S3_STAGE_VPCE_DNS_NAME = <string>
>   SEARCH_PATH = <string>
>   SIMULATED_DATA_SHARING_CONSUMER = <string>
>   STATEMENT_TIMEOUT_IN_SECONDS = <num>
>   STRICT_JSON_OUTPUT = TRUE | FALSE
>   TIMESTAMP_DAY_IS_ALWAYS_24H = TRUE | FALSE
>   TIMESTAMP_INPUT_FORMAT = <string>
>   TIMESTAMP_LTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_NTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_OUTPUT_FORMAT = <string>
>   TIMESTAMP_TYPE_MAPPING = <string>
>   TIMESTAMP_TZ_OUTPUT_FORMAT = <string>
>   TIMEZONE = <string>
>   TIME_INPUT_FORMAT = <string>
>   TIME_OUTPUT_FORMAT = <string>
>   TRACE_LEVEL = <string>
>   TRANSACTION_DEFAULT_ISOLATION_LEVEL = <string>
>   TWO_DIGIT_CENTURY_START = <num>
>   UNSUPPORTED_DDL_ACTION = <string>
>   USE_CACHED_RESULT = TRUE | FALSE
>   WEEK_OF_YEAR_POLICY = <num>
>   WEEK_START = <num>
> ```
>
> Copy

Note

For readability, the complete list of session parameters that can be set is not included here. For a complete list of all session parameters,
with their descriptions, as well as account and object parameters, see [Parameters](../parameters).

## Parameters[¶](#parameters "Link to this heading")

`SET ...`
:   Specifies one (or more) parameters to set for the session (separated by blank spaces, commas, or new lines).

    For descriptions of each of the parameters you can set for a session, see [Parameters](../parameters).

`UNSET ...`
:   Specifies one (or more) parameters to unset for the session, which resets them to the defaults.

    You can reset multiple parameters with a single ALTER statement; however, each property must be separated by a comma. When resetting
    a property, specify only the name; specifying a value for the property will return an error.

## Usage notes[¶](#usage-notes "Link to this heading")

* Parameters are typed. The supported types are BOOLEAN, NUMBER, and STRING.
* To see the current parameter values for the session, use [SHOW PARAMETERS](show-parameters).

## Examples[¶](#examples "Link to this heading")

Set the lock timeout for statements executed in the session to 1 hour (3600 seconds):

> ```
> ALTER SESSION SET LOCK_TIMEOUT = 3600;
> ```
>
> Copy

Set the lock timeout for statements executed in the session back to the default:

> ```
> ALTER SESSION UNSET LOCK_TIMEOUT;
> ```
>
> Copy

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
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Examples](#examples)