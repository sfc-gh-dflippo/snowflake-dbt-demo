---
auto_generated: true
description: After a DML command is executed (excluding the TRUNCATE TABLE command),
  Snowflake Scripting sets the following global variables. You can use these variables
  to determine if the last DML statement affe
last_scraped: '2026-01-14T16:55:53.172788+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/dml-status
title: Determining the number of rows affected by DML commands | Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../snowpark-container-services/overview.md)
12. [Functions and procedures](../extensibility.md)
13. [Logging, Tracing, and Metrics](../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../streamlit/object-management/billing.md)
      - [Security considerations](../streamlit/object-management/security.md)
      - [Privilege requirements](../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../streamlit/app-development/dependency-management.md)
      - [File organization](../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../streamlit/features/git-integration.md)
      - [External access](../streamlit/features/external-access.md)
      - [Row access policies](../streamlit/features/row-access.md)
      - [Sleep timer](../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../streamlit/troubleshooting.md)
    - [Release notes](../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](index.md)

    * [Blocks](blocks.md)
    * [Variables](variables.md)
    * [Returning a value](return.md)
    * [Conditional logic](branch.md)
    * [Loops](loops.md)
    * [Cursors](cursors.md)
    * [RESULTSETs](resultsets.md)
    * [Asynchronous child jobs](asynchronous-child-jobs.md)
    * [Exceptions](exceptions.md)
    * [Affected rows](dml-status.md)
    * [Getting a query ID](query-id.md)
    * [Examples for common use cases of Snowflake Scripting](use-cases.md)
    * [Using Snowflake Scripting in Snowflake CLI, SnowSQL, or the Python Connector](running-examples.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)Affected rows

# Determining the number of rows affected by DML commands[¶](#determining-the-number-of-rows-affected-by-dml-commands "Link to this heading")

After a [DML command](../../sql-reference/sql-dml) is executed (excluding the [TRUNCATE TABLE](../../sql-reference/sql/truncate-table)
command), Snowflake Scripting sets the following global variables. You can use these variables to determine if the last DML
statement affected any rows.

| Variable | Description |
| --- | --- |
| `SQLROWCOUNT` | Number of rows affected by the last DML statement.  This is equivalent to [`getNumRowsAffected()`](../stored-procedure/stored-procedures-api.html#getNumRowsAffected "getNumRowsAffected") in JavaScript stored procedures. |
| `SQLFOUND` | `true` if the last DML statement affected one or more rows. |
| `SQLNOTFOUND` | `true` if the last DML statement affected zero rows. |

Note

The [2025\_01 behavior change bundle](../../release-notes/bcr-bundles/2025_01_bundle) changes the behavior
of these variables. When the bundle is enabled, the variables return NULL when a non-DML statement is executed
after the last DML statement in a Snowflake Scripting block or stored procedure. The bundle is enabled by
default. For more information about the behavior change, see [Snowflake Scripting: Changes to global variables](../../release-notes/bcr-bundles/2025_01/bcr-1850).

If the bundle is disabled, you can [enable it in your account](../../release-notes/bcr-bundles/managing-behavior-change-releases.html#label-manage-bcr-enable-bundle) by
executing the following statement:

```
SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_01');
```

Copy

To disable the bundle, execute the following statement:

```
SELECT SYSTEM$DISABLE_BEHAVIOR_CHANGE_BUNDLE('2025_01');
```

Copy

The examples in this section use the following table:

```
CREATE OR REPLACE TABLE my_values (value NUMBER);
```

Copy

The following example uses the `SQLROWCOUNT` variable to return the number of rows affected by the last
DML statement (the INSERT statement).

```
BEGIN
  LET sql_row_count_var INT := 0;
  INSERT INTO my_values VALUES (1), (2), (3);
  sql_row_count_var := SQLROWCOUNT;
  SELECT * from my_values;
  RETURN sql_row_count_var;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
BEGIN
  LET sql_row_count_var INT := 0;
  INSERT INTO my_values VALUES (1), (2), (3);
  sql_row_count_var := SQLROWCOUNT;
  SELECT * from my_values;
  RETURN sql_row_count_var;
END;
$$;
```

Copy

```
+-----------------+
| anonymous block |
|-----------------|
|               3 |
+-----------------+
```

The following example uses the `SQLFOUND` and `SQLNOTFOUND` variables to return the number of rows affected by the
last DML statement (the UPDATE statement).

```
BEGIN
  LET sql_row_count_var INT := 0;
  LET sql_found_var BOOLEAN := NULL;
  LET sql_notfound_var BOOLEAN := NULL;
  IF ((SELECT MAX(value) FROM my_values) > 2) THEN
    UPDATE my_values SET value = 4 WHERE value < 3;
    sql_row_count_var := SQLROWCOUNT;
    sql_found_var := SQLFOUND;
    sql_notfound_var := SQLNOTFOUND;
  END IF;
  SELECT * from my_values;
  IF (sql_found_var = true) THEN
    RETURN 'Updated ' || sql_row_count_var || ' rows.';
  ELSEIF (sql_notfound_var = true) THEN
    RETURN 'No rows updated.';
  ELSE
    RETURN 'No DML statements executed.';
  END IF;
END;
```

Copy

Note: If you use [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](../python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](running-examples)):

```
EXECUTE IMMEDIATE $$
BEGIN
  LET sql_row_count_var INT := 0;
  LET sql_found_var BOOLEAN := NULL;
  LET sql_notfound_var BOOLEAN := NULL;
  IF ((SELECT MAX(value) FROM my_values) > 2) THEN
    UPDATE my_values SET value = 4 WHERE value < 3;
    sql_row_count_var := SQLROWCOUNT;
    sql_found_var := SQLFOUND;
    sql_notfound_var := SQLNOTFOUND;
  END IF;
  SELECT * from my_values;
  IF (sql_found_var = true) THEN
    RETURN 'Updated ' || sql_row_count_var || ' rows.';
  ELSEIF (sql_notfound_var = true) THEN
    RETURN 'No rows updated.';
  ELSE
    RETURN 'No DML statements executed.';
  END IF;
END;
$$;
```

Copy

When the anonymous block runs, the `SQLFOUND` variable is `true` because the UPDATE statement updates two rows.

```
+-----------------+
| anonymous block |
|-----------------|
| Updated 2 rows. |
+-----------------+
```

Query the table to see the current values:

```
SELECT * FROM my_values;
```

Copy

```
+-------+
| VALUE |
|-------|
|     4 |
|     4 |
|     3 |
+-------+
```

Run the same anonymous block again, and the results are the following:

* The UPDATE statement is executed because there is a value in the table that is greater than `2`. That is,
  the IF condition is satisfied.
* The `SQLNOTFOUND` variable is `true` because no rows are updated. The UPDATE statement doesn’t update
  any rows because none of the values in the table are less than `3` (specified in the WHERE clause).

The query returns the following output:

```
+------------------+
| anonymous block  |
|------------------|
| No rows updated. |
+------------------+
```

Now, update the table to set all of the values to `1`:

```
UPDATE my_values SET value = 1;

SELECT * FROM my_values;
```

Copy

```
+-------+
| VALUE |
|-------|
|     1 |
|     1 |
|     1 |
+-------+
```

Run the same anonymous block again, and the UPDATE statement isn’t executed because none of the values
in the table are greater than `2`. That is, the IF condition isn’t satisfied, so the UPDATE statement
doesn’t execute.

```
+-----------------------------+
| anonymous block             |
|-----------------------------|
| No DML statements executed. |
+-----------------------------+
```

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.