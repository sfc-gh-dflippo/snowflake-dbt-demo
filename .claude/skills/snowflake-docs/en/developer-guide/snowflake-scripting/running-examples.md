---
auto_generated: true
description: This topic explains how to run the Snowflake Scripting examples in Snowflake
  CLI, SnowSQL, and the Python Connector.
last_scraped: '2026-01-14T16:58:07.144745+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-scripting/running-examples
title: Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector |
  Snowflake Documentation
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

[Developer](../../developer.md)[Snowflake Scripting Developer Guide](index.md)Using Snowflake Scripting in Snowflake CLI, SnowSQL, or the Python Connector

# Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector[¶](#using-snowflake-scripting-in-sf-cli-snowsql-and-python-connector "Link to this heading")

This topic explains how to run the Snowflake Scripting examples in [Snowflake CLI](../snowflake-cli/index), [SnowSQL](../../user-guide/snowsql), and the [Python Connector](../python-connector/python-connector).

Note

If you are using other clients and interfaces, such as [Snowflake CLI](../snowflake-cli/index) or the
[JDBC driver](../jdbc/jdbc), you can skip this topic and refer to
[Snowflake Scripting blocks](blocks).

## Introduction[¶](#introduction "Link to this heading")

Currently, the following interfaces do not correctly parse Snowflake Scripting blocks:

* [Snowflake CLI](../snowflake-cli/index)
* [SnowSQL](../../user-guide/snowsql)
* The `execute_stream()` and `execute_string()` methods in
  [Python Connector](../python-connector/python-connector) code

  Note

  The other Python Connector methods parse Snowflake Scripting blocks correctly.

Entering and running a Snowflake Scripting block can result in the following error:

```
SQL compilation error: syntax error line 2 at position 25 unexpected '<EOF>'
```

Copy

To work around this, use delimiters around the start and end of a Snowflake Scripting block if you are using
these interfaces.

The following sections explain how to do this:

* [Using string constant delimiters around a block in a stored procedure](#label-snowscript-stored-procedure-delimiter-workaround)
* [Passing a block as a string literal to EXECUTE IMMEDIATE](#label-snowscript-anonymous-block-delimiter-workaround)

## Using string constant delimiters around a block in a stored procedure[¶](#using-string-constant-delimiters-around-a-block-in-a-stored-procedure "Link to this heading")

If you are creating a stored procedure, enclose the Snowflake Scripting block in
[single quotes or double dollar signs](../../sql-reference/data-types-text.html#label-quoted-string-constants). For example:

```
CREATE OR REPLACE PROCEDURE myprocedure()
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
    -- Snowflake Scripting code
    DECLARE
      radius_of_circle FLOAT;
      area_of_circle FLOAT;
    BEGIN
      radius_of_circle := 3;
      area_of_circle := pi() * radius_of_circle * radius_of_circle;
      RETURN area_of_circle;
    END;
  $$
  ;
```

Copy

Note

When specifying the scripting block directly on the Snowflake CLI command line, the `$$` delimiters might not work for some shells because they interpret that delimiter as something else. For example, the bash and zsh shells interpret it as the process ID (PID). To address this limitation, you can use the following alternatives:

* If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
* You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f <filename>` command.

## Passing a block as a string literal to EXECUTE IMMEDIATE[¶](#passing-a-block-as-a-string-literal-to-execute-immediate "Link to this heading")

If you are writing an [anonymous block](blocks.html#label-snowscript-block-anonymous), pass the block as a string literal to the
[EXECUTE IMMEDIATE](../../sql-reference/sql/execute-immediate) command. To delimit the string literal, use
[single quotes or double dollar signs](../../sql-reference/data-types-text.html#label-quoted-string-constants).

For example:

```
EXECUTE IMMEDIATE $$
-- Snowflake Scripting code
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := pi() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
$$
;
```

Copy

As an alternative, you can define a [session variable](../../sql-reference/session-variables) that is a string literal
containing the block, and you can pass that session variable to the EXECUTE IMMEDIATE command. For example:

```
SET stmt =
$$
DECLARE
    radius_of_circle FLOAT;
    area_of_circle FLOAT;
BEGIN
    radius_of_circle := 3;
    area_of_circle := pi() * radius_of_circle * radius_of_circle;
    RETURN area_of_circle;
END;
$$
;

EXECUTE IMMEDIATE $stmt;
```

Copy

Note

When specifying the scripting block directly on the Snowflake CLI command line, the `$$` delimiters might not work for some shells because they interpret that delimiter as something else. For example, the bash and zsh shells interpret it as the process ID (PID). To address this limitation, you can use the following alternatives:

* If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
* You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f <filename>` command.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Introduction](#introduction)
2. [Using string constant delimiters around a block in a stored procedure](#using-string-constant-delimiters-around-a-block-in-a-stored-procedure)
3. [Passing a block as a string literal to EXECUTE IMMEDIATE](#passing-a-block-as-a-string-literal-to-execute-immediate)