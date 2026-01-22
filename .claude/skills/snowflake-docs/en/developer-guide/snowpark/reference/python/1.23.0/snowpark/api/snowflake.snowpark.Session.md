---
auto_generated: true
description: 'Bases: object'
last_scraped: '2026-01-14T16:54:51.510119+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.Session
title: snowflake.snowpark.Session | Snowflake Documentation
---

1.44.0 (latest)1.43.01.42.01.41.01.40.01.39.11.39.01.38.01.37.01.35.01.34.01.33.01.32.01.31.01.30.01.29.11.29.01.28.01.27.01.26.01.25.01.24.01.23.01.22.11.21.11.21.01.20.01.19.01.18.01.17.01.16.01.15.01.14.01.13.01.12.11.12.01.11.11.10.01.9.01.8.01.7.01.6.11.5.01.4.01.3.01.2.01.1.0

1. [Overview](../../index.md)
2. [Snowpark Session](../session.md)

   * [Session](snowflake.snowpark.Session.md)
   * [Session.SessionBuilder.app\_name](snowflake.snowpark.Session.SessionBuilder.app_name.md)
   * [Session.SessionBuilder.config](snowflake.snowpark.Session.SessionBuilder.config.md)
   * [Session.SessionBuilder.configs](snowflake.snowpark.Session.SessionBuilder.configs.md)
   * [Session.SessionBuilder.create](snowflake.snowpark.Session.SessionBuilder.create.md)
   * [Session.SessionBuilder.getOrCreate](snowflake.snowpark.Session.SessionBuilder.getOrCreate.md)
   * [Session.add\_import](snowflake.snowpark.Session.add_import.md)
   * [Session.add\_packages](snowflake.snowpark.Session.add_packages.md)
   * [Session.add\_requirements](snowflake.snowpark.Session.add_requirements.md)
   * [Session.append\_query\_tag](snowflake.snowpark.Session.append_query_tag.md)
   * [Session.call](snowflake.snowpark.Session.call.md)
   * [Session.cancel\_all](snowflake.snowpark.Session.cancel_all.md)
   * [Session.clear\_imports](snowflake.snowpark.Session.clear_imports.md)
   * [Session.clear\_packages](snowflake.snowpark.Session.clear_packages.md)
   * [Session.close](snowflake.snowpark.Session.close.md)
   * [Session.createDataFrame](snowflake.snowpark.Session.createDataFrame.md)
   * [Session.create\_async\_job](snowflake.snowpark.Session.create_async_job.md)
   * [Session.create\_dataframe](snowflake.snowpark.Session.create_dataframe.md)
   * [Session.flatten](snowflake.snowpark.Session.flatten.md)
   * [Session.generator](snowflake.snowpark.Session.generator.md)
   * [Session.get\_current\_account](snowflake.snowpark.Session.get_current_account.md)
   * [Session.get\_current\_database](snowflake.snowpark.Session.get_current_database.md)
   * [Session.get\_current\_role](snowflake.snowpark.Session.get_current_role.md)
   * [Session.get\_current\_schema](snowflake.snowpark.Session.get_current_schema.md)
   * [Session.get\_current\_user](snowflake.snowpark.Session.get_current_user.md)
   * [Session.get\_current\_warehouse](snowflake.snowpark.Session.get_current_warehouse.md)
   * [Session.get\_fully\_qualified\_current\_schema](snowflake.snowpark.Session.get_fully_qualified_current_schema.md)
   * [Session.get\_fully\_qualified\_name\_if\_possible](snowflake.snowpark.Session.get_fully_qualified_name_if_possible.md)
   * [Session.get\_imports](snowflake.snowpark.Session.get_imports.md)
   * [Session.get\_packages](snowflake.snowpark.Session.get_packages.md)
   * [Session.get\_session\_stage](snowflake.snowpark.Session.get_session_stage.md)
   * [Session.query\_history](snowflake.snowpark.Session.query_history.md)
   * [Session.stored\_procedure\_profiler](snowflake.snowpark.Session.stored_procedure_profiler.md)
   * [Session.range](snowflake.snowpark.Session.range.md)
   * [Session.remove\_import](snowflake.snowpark.Session.remove_import.md)
   * [Session.remove\_package](snowflake.snowpark.Session.remove_package.md)
   * [Session.replicate\_local\_environment](snowflake.snowpark.Session.replicate_local_environment.md)
   * [Session.sql](snowflake.snowpark.Session.sql.md)
   * [Session.table](snowflake.snowpark.Session.table.md)
   * [Session.table\_function](snowflake.snowpark.Session.table_function.md)
   * [Session.update\_query\_tag](snowflake.snowpark.Session.update_query_tag.md)
   * [Session.use\_database](snowflake.snowpark.Session.use_database.md)
   * [Session.use\_role](snowflake.snowpark.Session.use_role.md)
   * [Session.use\_schema](snowflake.snowpark.Session.use_schema.md)
   * [Session.use\_secondary\_roles](snowflake.snowpark.Session.use_secondary_roles.md)
   * [Session.use\_warehouse](snowflake.snowpark.Session.use_warehouse.md)
   * [Session.write\_pandas](snowflake.snowpark.Session.write_pandas.md)
   * [Session.builder](snowflake.snowpark.Session.builder.md)
   * [Session.custom\_package\_usage\_config](snowflake.snowpark.Session.custom_package_usage_config.md)
   * [Session.file](snowflake.snowpark.Session.file.md)
   * [Session.query\_tag](snowflake.snowpark.Session.query_tag.md)
   * [Session.lineage](snowflake.snowpark.Session.lineage.md)
   * [Session.read](snowflake.snowpark.Session.read.md)
   * [Session.sproc](snowflake.snowpark.Session.sproc.md)
   * [Session.sql\_simplifier\_enabled](snowflake.snowpark.Session.sql_simplifier_enabled.md)
   * [Session.telemetry\_enabled](snowflake.snowpark.Session.telemetry_enabled.md)
   * [Session.udaf](snowflake.snowpark.Session.udaf.md)
   * [Session.udf](snowflake.snowpark.Session.udf.md)
   * [Session.udtf](snowflake.snowpark.Session.udtf.md)
   * [Session.session\_id](snowflake.snowpark.Session.session_id.md)
   * [Session.connection](snowflake.snowpark.Session.connection.md)
3. [Snowpark APIs](../index.md)
4. [Snowpark pandas API](../../modin/index.md)

[Developer](../../../../../../../developer.md)[Snowpark API](../../../../../index.md)[Python](../../../../../python/index.md)[Python API Reference](../../index.md)[Snowpark Session](../session.md)Session

You are viewing documentation about an older version (1.23.0).  [View latest version](../../../1.44.0/index.md)

# snowflake.snowpark.Session[¶](#snowflake-snowpark-session "Permalink to this heading")

*class* snowflake.snowpark.Session(*conn: Union[ServerConnection, MockServerConnection]*, *options: Optional[Dict[str, Any]] = None*)[[source]](https://github.com/snowflakedb/snowpark-python/blob/v1.23.0/src/snowflake/snowpark/session.py#L300-L3543)[¶](#snowflake.snowpark.Session "Permalink to this definition")
:   Bases: `object`

    Establishes a connection with a Snowflake database and provides methods for creating DataFrames
    and accessing objects for working with files in stages.

    When you create a [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") object, you provide connection parameters to establish a
    connection with a Snowflake database (e.g. an account, a user name, etc.). You can
    specify these settings in a dict that associates connection parameters names with values.
    The Snowpark library uses [the Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html)
    to connect to Snowflake. Refer to
    [Connecting to Snowflake using the Python Connector](https://docs.snowflake.com/en/user-guide/python-connector-example.html#connecting-to-snowflake)
    for the details of [Connection Parameters](https://docs.snowflake.com/en/user-guide/python-connector-api.html#connect).

    To create a [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") object from a `dict` of connection parameters:

    ```
    >>> connection_parameters = {
    ...     "user": "<user_name>",
    ...     "password": "<password>",
    ...     "account": "<account_name>",
    ...     "role": "<role_name>",
    ...     "warehouse": "<warehouse_name>",
    ...     "database": "<database_name>",
    ...     "schema": "<schema_name>",
    ... }
    >>> session = Session.builder.configs(connection_parameters).create()
    ```

    Copy

    To create a [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") object from an existing Python Connector connection:

    ```
    >>> session = Session.builder.configs({"connection": <your python connector connection>}).create()
    ```

    Copy

    [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") contains functions to construct a [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame") like [`table()`](snowflake.snowpark.Session.table.html#snowflake.snowpark.Session.table "snowflake.snowpark.Session.table"),
    [`sql()`](snowflake.snowpark.Session.sql.html#snowflake.snowpark.Session.sql "snowflake.snowpark.Session.sql") and [`read`](snowflake.snowpark.Session.read.html#snowflake.snowpark.Session.read "snowflake.snowpark.Session.read"), etc.

    A [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") object is not thread-safe.

    Methods

    |  |  |
    | --- | --- |
    | [`add_import`](snowflake.snowpark.Session.add_import.html#snowflake.snowpark.Session.add_import "snowflake.snowpark.Session.add_import")(path[, import\_path, chunk\_size, ...]) | Registers a remote file in stage or a local file as an import of a user-defined function (UDF). |
    | [`add_packages`](snowflake.snowpark.Session.add_packages.html#snowflake.snowpark.Session.add_packages "snowflake.snowpark.Session.add_packages")(\*packages) | Adds third-party packages as dependencies of a user-defined function (UDF). |
    | [`add_requirements`](snowflake.snowpark.Session.add_requirements.html#snowflake.snowpark.Session.add_requirements "snowflake.snowpark.Session.add_requirements")(file\_path) | Adds a [requirement file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) that contains a list of packages as dependencies of a user-defined function (UDF). |
    | [`append_query_tag`](snowflake.snowpark.Session.append_query_tag.html#snowflake.snowpark.Session.append_query_tag "snowflake.snowpark.Session.append_query_tag")(tag[, separator]) | Appends a tag to the current query tag. |
    | [`call`](snowflake.snowpark.Session.call.html#snowflake.snowpark.Session.call "snowflake.snowpark.Session.call")(sproc\_name, \*args[, statement\_params, ...]) | Calls a stored procedure by name. |
    | [`cancel_all`](snowflake.snowpark.Session.cancel_all.html#snowflake.snowpark.Session.cancel_all "snowflake.snowpark.Session.cancel_all")() | Cancel all action methods that are running currently. |
    | [`clear_imports`](snowflake.snowpark.Session.clear_imports.html#snowflake.snowpark.Session.clear_imports "snowflake.snowpark.Session.clear_imports")() | Clears all files in a stage or local files from the imports of a user-defined function (UDF). |
    | [`clear_packages`](snowflake.snowpark.Session.clear_packages.html#snowflake.snowpark.Session.clear_packages "snowflake.snowpark.Session.clear_packages")() | Clears all third-party packages of a user-defined function (UDF). |
    | [`close`](snowflake.snowpark.Session.close.html#snowflake.snowpark.Session.close "snowflake.snowpark.Session.close")() | Close this session. |
    | [`createDataFrame`](snowflake.snowpark.Session.createDataFrame.html#snowflake.snowpark.Session.createDataFrame "snowflake.snowpark.Session.createDataFrame")(data[, schema]) | Creates a new DataFrame containing the specified values from the local data. |
    | [`create_async_job`](snowflake.snowpark.Session.create_async_job.html#snowflake.snowpark.Session.create_async_job "snowflake.snowpark.Session.create_async_job")(query\_id) | Creates an [`AsyncJob`](snowflake.snowpark.AsyncJob.html#snowflake.snowpark.AsyncJob "snowflake.snowpark.AsyncJob") from a query ID. |
    | [`create_dataframe`](snowflake.snowpark.Session.create_dataframe.html#snowflake.snowpark.Session.create_dataframe "snowflake.snowpark.Session.create_dataframe")(data[, schema]) | Creates a new DataFrame containing the specified values from the local data. |
    | [`flatten`](snowflake.snowpark.Session.flatten.html#snowflake.snowpark.Session.flatten "snowflake.snowpark.Session.flatten")(input[, path, outer, recursive, mode]) | Creates a new [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame") by flattening compound values into multiple rows. |
    | [`generator`](snowflake.snowpark.Session.generator.html#snowflake.snowpark.Session.generator "snowflake.snowpark.Session.generator")(\*columns[, rowcount, timelimit]) | Creates a new DataFrame using the Generator table function. |
    | [`get_current_account`](snowflake.snowpark.Session.get_current_account.html#snowflake.snowpark.Session.get_current_account "snowflake.snowpark.Session.get_current_account")() | Returns the name of the current account for the Python connector session attached to this session. |
    | [`get_current_database`](snowflake.snowpark.Session.get_current_database.html#snowflake.snowpark.Session.get_current_database "snowflake.snowpark.Session.get_current_database")() | Returns the name of the current database for the Python connector session attached to this session. |
    | [`get_current_role`](snowflake.snowpark.Session.get_current_role.html#snowflake.snowpark.Session.get_current_role "snowflake.snowpark.Session.get_current_role")() | Returns the name of the primary role in use for the current session. |
    | [`get_current_schema`](snowflake.snowpark.Session.get_current_schema.html#snowflake.snowpark.Session.get_current_schema "snowflake.snowpark.Session.get_current_schema")() | Returns the name of the current schema for the Python connector session attached to this session. |
    | [`get_current_user`](snowflake.snowpark.Session.get_current_user.html#snowflake.snowpark.Session.get_current_user "snowflake.snowpark.Session.get_current_user")() | Returns the name of the user in the connection to Snowflake attached to this session. |
    | [`get_current_warehouse`](snowflake.snowpark.Session.get_current_warehouse.html#snowflake.snowpark.Session.get_current_warehouse "snowflake.snowpark.Session.get_current_warehouse")() | Returns the name of the warehouse in use for the current session. |
    | [`get_fully_qualified_current_schema`](snowflake.snowpark.Session.get_fully_qualified_current_schema.html#snowflake.snowpark.Session.get_fully_qualified_current_schema "snowflake.snowpark.Session.get_fully_qualified_current_schema")() | Returns the fully qualified name of the current schema for the session. |
    | [`get_fully_qualified_name_if_possible`](snowflake.snowpark.Session.get_fully_qualified_name_if_possible.html#snowflake.snowpark.Session.get_fully_qualified_name_if_possible "snowflake.snowpark.Session.get_fully_qualified_name_if_possible")(name) | Returns the fully qualified object name if current database/schema exists, otherwise returns the object name |
    | [`get_imports`](snowflake.snowpark.Session.get_imports.html#snowflake.snowpark.Session.get_imports "snowflake.snowpark.Session.get_imports")() | Returns a list of imports added for user defined functions (UDFs). |
    | [`get_packages`](snowflake.snowpark.Session.get_packages.html#snowflake.snowpark.Session.get_packages "snowflake.snowpark.Session.get_packages")() | Returns a `dict` of packages added for user-defined functions (UDFs). |
    | [`get_session_stage`](snowflake.snowpark.Session.get_session_stage.html#snowflake.snowpark.Session.get_session_stage "snowflake.snowpark.Session.get_session_stage")([statement\_params]) | Returns the name of the temporary stage created by the Snowpark library for uploading and storing temporary artifacts for this session. |
    | [`query_history`](snowflake.snowpark.Session.query_history.html#snowflake.snowpark.Session.query_history "snowflake.snowpark.Session.query_history")([include\_describe, ...]) | Create an instance of [`QueryHistory`](snowflake.snowpark.QueryHistory.html#snowflake.snowpark.QueryHistory "snowflake.snowpark.QueryHistory") as a context manager to record queries that are pushed down to the Snowflake database. |
    | [`range`](snowflake.snowpark.Session.range.html#snowflake.snowpark.Session.range "snowflake.snowpark.Session.range")(start[, end, step]) | Creates a new DataFrame from a range of numbers. |
    | [`remove_import`](snowflake.snowpark.Session.remove_import.html#snowflake.snowpark.Session.remove_import "snowflake.snowpark.Session.remove_import")(path) | Removes a file in stage or local file from the imports of a user-defined function (UDF). |
    | [`remove_package`](snowflake.snowpark.Session.remove_package.html#snowflake.snowpark.Session.remove_package "snowflake.snowpark.Session.remove_package")(package) | Removes a third-party package from the dependency list of a user-defined function (UDF). |
    | [`replicate_local_environment`](snowflake.snowpark.Session.replicate_local_environment.html#snowflake.snowpark.Session.replicate_local_environment "snowflake.snowpark.Session.replicate_local_environment")([...]) | Adds all third-party packages in your local environment as dependencies of a user-defined function (UDF). |
    | [`sql`](snowflake.snowpark.Session.sql.html#snowflake.snowpark.Session.sql "snowflake.snowpark.Session.sql")(query[, params]) | Returns a new DataFrame representing the results of a SQL query. |
    | [`table`](snowflake.snowpark.Session.table.html#snowflake.snowpark.Session.table "snowflake.snowpark.Session.table")(name) | Returns a Table that points the specified table. |
    | [`table_function`](snowflake.snowpark.Session.table_function.html#snowflake.snowpark.Session.table_function "snowflake.snowpark.Session.table_function")(func\_name, \*func\_arguments, ...) | Creates a new DataFrame from the given snowflake SQL table function. |
    | [`update_query_tag`](snowflake.snowpark.Session.update_query_tag.html#snowflake.snowpark.Session.update_query_tag "snowflake.snowpark.Session.update_query_tag")(tag) | Updates a query tag that is a json encoded string. |
    | [`use_database`](snowflake.snowpark.Session.use_database.html#snowflake.snowpark.Session.use_database "snowflake.snowpark.Session.use_database")(database) | Specifies the active/current database for the session. |
    | [`use_role`](snowflake.snowpark.Session.use_role.html#snowflake.snowpark.Session.use_role "snowflake.snowpark.Session.use_role")(role) | Specifies the active/current primary role for the session. |
    | [`use_schema`](snowflake.snowpark.Session.use_schema.html#snowflake.snowpark.Session.use_schema "snowflake.snowpark.Session.use_schema")(schema) | Specifies the active/current schema for the session. |
    | [`use_secondary_roles`](snowflake.snowpark.Session.use_secondary_roles.html#snowflake.snowpark.Session.use_secondary_roles "snowflake.snowpark.Session.use_secondary_roles")(roles) | Specifies the active/current secondary roles for the session. |
    | [`use_warehouse`](snowflake.snowpark.Session.use_warehouse.html#snowflake.snowpark.Session.use_warehouse "snowflake.snowpark.Session.use_warehouse")(warehouse) | Specifies the active/current warehouse for the session. |
    | [`write_pandas`](snowflake.snowpark.Session.write_pandas.html#snowflake.snowpark.Session.write_pandas "snowflake.snowpark.Session.write_pandas")(df, table\_name, \*[, database, ...]) | Writes a pandas DataFrame to a table in Snowflake and returns a Snowpark [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame") object referring to the table where the pandas DataFrame was written to. |

    Attributes

    |  |  |
    | --- | --- |
    | `auto_clean_up_temp_table_enabled` | When setting this parameter to `True`, Snowpark will automatically clean up temporary tables created by [`DataFrame.cache_result()`](snowflake.snowpark.DataFrame.cache_result.html#snowflake.snowpark.DataFrame.cache_result "snowflake.snowpark.DataFrame.cache_result") in the current session when the DataFrame is no longer referenced (i.e., gets garbage collected). |
    | [`builder`](snowflake.snowpark.Session.builder.html#snowflake.snowpark.Session.builder "snowflake.snowpark.Session.builder") | Returns a builder you can use to set configuration properties and create a [`Session`](#snowflake.snowpark.Session "snowflake.snowpark.Session") object. |
    | `conf` |  |
    | [`connection`](snowflake.snowpark.Session.connection.html#snowflake.snowpark.Session.connection "snowflake.snowpark.Session.connection") | Returns a `SnowflakeConnection` object that allows you to access the connection between the current session and Snowflake server. |
    | `cte_optimization_enabled` | Set to `True` to enable the CTE optimization (defaults to `False`). |
    | [`custom_package_usage_config`](snowflake.snowpark.Session.custom_package_usage_config.html#snowflake.snowpark.Session.custom_package_usage_config "snowflake.snowpark.Session.custom_package_usage_config") | Get or set configuration parameters related to usage of custom Python packages in Snowflake. |
    | `eliminate_numeric_sql_value_cast_enabled` |  |
    | [`file`](snowflake.snowpark.Session.file.html#snowflake.snowpark.Session.file "snowflake.snowpark.Session.file") | Returns a [`FileOperation`](snowflake.snowpark.FileOperation.html#snowflake.snowpark.FileOperation "snowflake.snowpark.FileOperation") object that you can use to perform file operations on stages. |
    | `large_query_breakdown_complexity_bounds` |  |
    | `large_query_breakdown_enabled` |  |
    | [`lineage`](snowflake.snowpark.Session.lineage.html#snowflake.snowpark.Session.lineage "snowflake.snowpark.Session.lineage") | Returns a `Lineage` object that you can use to explore lineage of snowflake entities. |
    | [`query_tag`](snowflake.snowpark.Session.query_tag.html#snowflake.snowpark.Session.query_tag "snowflake.snowpark.Session.query_tag") | The query tag for this session. |
    | [`read`](snowflake.snowpark.Session.read.html#snowflake.snowpark.Session.read "snowflake.snowpark.Session.read") | Returns a [`DataFrameReader`](snowflake.snowpark.DataFrameReader.html#snowflake.snowpark.DataFrameReader "snowflake.snowpark.DataFrameReader") that you can use to read data from various supported sources (e.g. |
    | [`session_id`](snowflake.snowpark.Session.session_id.html#snowflake.snowpark.Session.session_id "snowflake.snowpark.Session.session_id") | Returns an integer that represents the session ID of this session. |
    | [`sproc`](snowflake.snowpark.Session.sproc.html#snowflake.snowpark.Session.sproc "snowflake.snowpark.Session.sproc") | Returns a [`stored_procedure.StoredProcedureRegistration`](snowflake.snowpark.stored_procedure.StoredProcedureRegistration.html#snowflake.snowpark.stored_procedure.StoredProcedureRegistration "snowflake.snowpark.stored_procedure.StoredProcedureRegistration") object that you can use to register stored procedures. |
    | [`sql_simplifier_enabled`](snowflake.snowpark.Session.sql_simplifier_enabled.html#snowflake.snowpark.Session.sql_simplifier_enabled "snowflake.snowpark.Session.sql_simplifier_enabled") | Set to `True` to use the SQL simplifier (defaults to `True`). |
    | [`stored_procedure_profiler`](snowflake.snowpark.Session.stored_procedure_profiler.html#snowflake.snowpark.Session.stored_procedure_profiler "snowflake.snowpark.Session.stored_procedure_profiler") | Returns a `stored_procedure_profiler.StoredProcedureProfiler` object that you can use to profile stored procedures. |
    | [`telemetry_enabled`](snowflake.snowpark.Session.telemetry_enabled.html#snowflake.snowpark.Session.telemetry_enabled "snowflake.snowpark.Session.telemetry_enabled") | Controls whether or not the Snowpark client sends usage telemetry to Snowflake. |
    | [`udaf`](snowflake.snowpark.Session.udaf.html#snowflake.snowpark.Session.udaf "snowflake.snowpark.Session.udaf") | Returns a [`udaf.UDAFRegistration`](snowflake.snowpark.udaf.UDAFRegistration.html#snowflake.snowpark.udaf.UDAFRegistration "snowflake.snowpark.udaf.UDAFRegistration") object that you can use to register UDAFs. |
    | [`udf`](snowflake.snowpark.Session.udf.html#snowflake.snowpark.Session.udf "snowflake.snowpark.Session.udf") | Returns a [`udf.UDFRegistration`](snowflake.snowpark.udf.UDFRegistration.html#snowflake.snowpark.udf.UDFRegistration "snowflake.snowpark.udf.UDFRegistration") object that you can use to register UDFs. |
    | [`udtf`](snowflake.snowpark.Session.udtf.html#snowflake.snowpark.Session.udtf "snowflake.snowpark.Session.udtf") | Returns a [`udtf.UDTFRegistration`](snowflake.snowpark.udtf.UDTFRegistration.html#snowflake.snowpark.udtf.UDTFRegistration "snowflake.snowpark.udtf.UDTFRegistration") object that you can use to register UDTFs. |

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.