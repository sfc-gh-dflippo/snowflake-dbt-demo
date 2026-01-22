---
auto_generated: true
description: You can write stored procedures to extend the system with procedural
  code. With a procedure, you can use branching, looping, and other programmatic constructs.
  You can reuse a procedure multiple times
last_scraped: '2026-01-14T16:56:19.099771+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/stored-procedures-overview
title: Stored procedures overview | Snowflake Documentation
---

1. [Overview](../developer.md)
2. Builders
3. [Snowflake DevOps](../developer-guide/builders/devops.md)
4. [Observability](../developer-guide/builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../developer-guide/snowpark/index.md)
7. [Spark workloads on Snowflake](../developer-guide/snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../developer-guide/snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../developer-guide/snowpark-container-services/overview.md)
12. [Functions and procedures](../developer-guide/extensibility.md)

    * [Function or procedure?](../developer-guide/stored-procedures-vs-udfs.md)
    * [Guidelines](../developer-guide/udf-stored-procedure-guidelines.md)
    * [Stored procedures](../developer-guide/stored-procedure/stored-procedures-overview.md)

      + [Usage](../developer-guide/stored-procedure/stored-procedures-usage.md)
      + [Caller and owner rights](../developer-guide/stored-procedure/stored-procedures-rights.md)
      + [Creating](../developer-guide/stored-procedure/stored-procedures-creating.md)
      + [Calling](../developer-guide/stored-procedure/stored-procedures-calling.md)
      + [Selecting from](../developer-guide/stored-procedure/stored-procedures-selecting-from.md)
      + [Passing in references](../developer-guide/stored-procedure/stored-procedures-calling-references.md)
      + Handler writing
      + [Java](../developer-guide/stored-procedure/java/procedure-java-overview.md)
      + [Javascript](../developer-guide/stored-procedure/stored-procedures-javascript.md)
      + [Python](../developer-guide/stored-procedure/python/procedure-python-overview.md)
      + [Scala](../developer-guide/stored-procedure/scala/procedure-scala-overview.md)
      + [Snowflake Scripting](../developer-guide/stored-procedure/stored-procedures-snowflake-scripting.md)
    * [User-defined functions](../developer-guide/udf/udf-overview.md)
    * [Packaging handler code](../developer-guide/udf-stored-procedure-building.md)
    * [External network access](../developer-guide/external-network-access/external-network-access-overview.md)
13. [Logging, Tracing, and Metrics](../developer-guide/logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../developer-guide/snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../developer-guide/snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../developer-guide/sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../developer-guide/streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../developer-guide/streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../developer-guide/streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../developer-guide/streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../developer-guide/streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../developer-guide/streamlit/object-management/billing.md)
      - [Security considerations](../developer-guide/streamlit/object-management/security.md)
      - [Privilege requirements](../developer-guide/streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../developer-guide/streamlit/object-management/owners-rights.md)
      - [PrivateLink](../developer-guide/streamlit/object-management/privatelink.md)
      - [Logging and tracing](../developer-guide/streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../developer-guide/streamlit/app-development/runtime-environments.md)
      - [Dependency management](../developer-guide/streamlit/app-development/dependency-management.md)
      - [File organization](../developer-guide/streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../developer-guide/streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../developer-guide/streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../developer-guide/streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../developer-guide/streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../developer-guide/streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../developer-guide/streamlit/features/git-integration.md)
      - [External access](../developer-guide/streamlit/features/external-access.md)
      - [Row access policies](../developer-guide/streamlit/features/row-access.md)
      - [Sleep timer](../developer-guide/streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../developer-guide/streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../developer-guide/streamlit/troubleshooting.md)
    - [Release notes](../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../developer-guide/declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../developer-guide/native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](external-functions.md)
25. [Kafka and Spark Connectors](../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../developer-guide/snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
30. [Git](../developer-guide/git/git-overview.md)
31. Drivers
32. [Overview](../developer-guide/drivers.md)
33. [Considerations when drivers reuse sessions](../developer-guide/driver-connections.md)
34. [Scala versions](../developer-guide/scala-version-differences.md)
35. Reference
36. [API Reference](../api-reference.md)

[Developer](../developer.md)[Functions and procedures](../developer-guide/extensibility.md)Stored procedures

# Stored procedures overview[¶](#stored-procedures-overview "Link to this heading")

You can write stored procedures to extend the system with procedural code. With a procedure, you can use branching, looping, and other
programmatic constructs. You can reuse a procedure multiple times by calling it from other code.

With a stored procedure, you can:

* Automate tasks that require multiple database operations performed frequently.
* Dynamically create and execute database operations.
* Execute code with the privileges of the role that owns the procedure, rather than with the privileges of the role that runs the procedure.

  This allows the stored procedure owner to delegate the power to perform specified operations to users who otherwise could not do so.
  However, there are limitations on these owner’s rights stored procedures.

For example, imagine that you want to clean up a database by deleting data older than a specified date. You can execute the delete operation
multiple times in your code, each time deleting data from a specific table. You can put all of those statements in a single stored
procedure, then pass a parameter that specifies the cut-off date.

With the procedure deployed, you can call it to clean up the database. As your database changes, you can update the procedure to clean
up additional tables; if there are multiple users who use the new cleanup command, they can call one procedure, rather than remember
every table name and clean up each table individually.

A stored procedure is like a UDF, but the two differ in important ways. For more information, see
[Choosing whether to write a stored procedure or a user-defined function](../stored-procedures-vs-udfs).

A procedure is just one way to extend Snowflake. For others, see the following:

* [User-defined functions overview](../udf/udf-overview)
* [Writing external functions](../../sql-reference/external-functions)
* [Snowpark API](../snowpark/index)

## Supported languages and tools[¶](#supported-languages-and-tools "Link to this heading")

You can create and manage stored procedures (and other Snowflake entities) by using any of multiple tools, depending on how you prefer to work.

| Language | Approach | Support |
| --- | --- | --- |
| **SQL**  With handler in Java, JavaScript, Python, Scala, or SQL Scripting | Write SQL code in Snowflake to create and manage Snowflake entities. Write the procedure’s logic in one of the supported handler languages. | [Java](java/procedure-java-overview)  [JavaScript](stored-procedures-javascript)  [Python](python/procedure-python-overview)  [Scala](scala/procedure-scala-overview)  [SQL Scripting](stored-procedures-snowflake-scripting) |
| **Java, Python, or Scala**  [Snowpark API](../snowpark/index) | On the client, write code for operations that are pushed to Snowflake for processing. | [Java](../snowpark/java/creating-sprocs)  [Python](../snowpark/python/creating-sprocs)  [Scala](../snowpark/scala/creating-sprocs) |
| **Command-line interface**  [Snowflake CLI](../snowflake-cli/index) | Use the command line to create and manage Snowflake entities, specifying properties as properties of JSON objects. | [Managing Snowflake objects](../snowflake-cli/objects/manage-objects) |
| **Python**  [Snowflake Python API](../snowflake-python-api/snowflake-python-overview) | On the client, write code that executes management operations on Snowflake. | [Managing stored procedures](../snowflake-python-api/snowflake-python-managing-functions-procedures.html#label-snowflake-python-procedures) |
| **REST**  [Snowflake REST API](../snowflake-rest-api/snowflake-rest-api) | Make requests of RESTful endpoints to create and manage Snowflake entities. | [Manage procedures](../snowflake-rest-api/procedure/procedure-introduction) |

You write a procedure’s logic — its handler — in one of the [supported languages](#label-stored-procedures-handler-languages). Once
you have a handler, you can [create a procedure](stored-procedures-creating) with a CREATE PROCEDURE command, then
[call the procedure](stored-procedures-calling) with a CALL statement.

From a stored procedure, you can return a single value or (where supported with the handler language) tabular data. For more information
about supported return types, see [CREATE PROCEDURE](../../sql-reference/sql/create-procedure).

When choosing a language, consider also the handler locations supported. Not all languages support referring to the handler on a stage
(the handler code must instead be in-line). For more information, see [Keeping handler code in-line or on a stage](../inline-or-staged).

| Language | Handler Location |
| --- | --- |
| Java | In-line or staged |
| JavaScript | In-line |
| Python | In-line or staged |
| Scala | In-line or staged |
| Snowflake Scripting | In-line |

## Temporary procedures[¶](#temporary-procedures "Link to this heading")

You can create a procedure that is discarded after you use it. You might find this useful when you don’t
need the procedure to be available in a durable way, such as for multiple sessions or to multiple users.

In addition, creating a procedure in one of the following ways doesn’t require the CREATE PROCEDURE privilege, so these approaches are more broadly available to users:

* Create a temporary stored procedure that persists for only the current session, then is dropped.

  The following Snowflake tools support creating a temporary procedure:

  + [CREATE PROCEDURE](../../sql-reference/sql/create-procedure) with the TEMP or TEMPORARY parameter
  + The Snowpark API for [Java](../snowpark/java/creating-sprocs.html#label-snowpark-java-stored-proc-create-temp), [Python](../snowpark/python/creating-sprocs.html#label-snowpark-python-snowpark-sproc-named),
    or [Scala](../snowpark/scala/creating-sprocs.html#label-snowpark-scala-stored-proc-create-temp)
* Create an anonymous procedure that you call immediately, and which is dropped immediately.

  + To create a procedure and immediately call it in a single SQL statement, use the [CALL (with anonymous procedure)](../../sql-reference/sql/call-with) syntax.

## Stored procedure example[¶](#stored-procedure-example "Link to this heading")

Code in the following example creates a stored procedure called `myproc` with a Python handler called `run`.

```
CREATE OR REPLACE PROCEDURE myproc(from_table STRING, to_table STRING, count INT)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
as
$$
def run(session, from_table, to_table, count):
  session.table(from_table).limit(count).write.save_as_table(to_table)
  return "SUCCESS"
$$;
```

Copy

Code in the following example calls the stored procedure `myproc`.

```
CALL myproc('table_a', 'table_b', 5);
```

Copy

## Guidelines and constraints[¶](#guidelines-and-constraints "Link to this heading")

Tips:
:   For tips on writing stored procedures, see [Working with stored procedures](stored-procedures-usage).

Snowflake constraints:
:   You can ensure stability within the Snowflake environment by developing within Snowflake constraints. For more information, see
    [Designing Handlers that Stay Within Snowflake-Imposed Constraints](../udf-stored-procedure-constraints).

Naming:
:   Be sure to name procedures in a way that avoids collisions with other procedures. For more information, see
    [Naming and overloading procedures and UDFs](../udf-stored-procedure-naming-conventions).

Arguments:
:   Specify the arguments for your stored procedure and indicate which arguments are optional. For more information, see
    [Defining arguments for UDFs and stored procedures](../udf-stored-procedure-arguments).

Data type mappings:
:   For each handler language, there’s a separate set of mappings between the language’s data types and the SQL types used for arguments and
    return values. For more about the mappings for each language, see [Data Type Mappings Between SQL and Handler Languages](../udf-stored-procedure-data-type-mapping).

## Handler writing[¶](#handler-writing "Link to this heading")

Handler languages:
:   For language-specific content on writing a handler, see [Supported languages and tools](#label-stored-procedures-handler-languages).

External network access:
:   You can access external network locations with
    [external network access](../external-network-access/external-network-access-overview). You can create secure
    access to specific network locations external to Snowflake, then use that access from within the handler code.

Logging and tracing:
:   You can record code activity by [capturing log messages and trace events](../logging-tracing/logging-tracing-overview),
    storing the data in a database you can query later.

## Security[¶](#security "Link to this heading")

Whether you choose to have a stored procedure run with caller’s rights or owner’s rights can impact the information it has access to and
the tasks it may be allowed to perform. For more information, see [Understanding caller’s rights and owner’s rights stored procedures](stored-procedures-rights).

Stored procedures share certain security concerns with user-defined functions (UDFs). For more information, see the following:

* You can help a procedure’s handler code execute securely by following the best practices described in
  [Security Practices for UDFs and Procedures](../udf-stored-procedure-security-practices)
* Ensure that sensitive information is concealed from users who should not have access to it. For more information, see
  [Protecting Sensitive Information with Secure UDFs and Stored Procedures](../secure-udf-procedure)

## Handler code deployment[¶](#handler-code-deployment "Link to this heading")

When creating a procedure, you can specify its handler – which implements the procedure’s logic – as code in-line with the CREATE
PROCEDURE statement or as code external to the statement, such as compiled code packaged and copied to a stage.

For more information, see [Keeping handler code in-line or on a stage](../inline-or-staged).

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

1. [Supported languages and tools](#supported-languages-and-tools)
2. [Temporary procedures](#temporary-procedures)
3. [Stored procedure example](#stored-procedure-example)
4. [Guidelines and constraints](#guidelines-and-constraints)
5. [Handler writing](#handler-writing)
6. [Security](#security)
7. [Handler code deployment](#handler-code-deployment)

Related content

1. [Choosing whether to write a stored procedure or a user-defined function](/developer-guide/stored-procedure/../stored-procedures-vs-udfs)
2. [Extending Snowflake with Functions and Procedures](/developer-guide/stored-procedure/../extensibility)