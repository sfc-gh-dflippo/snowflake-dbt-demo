---
auto_generated: true
description: You can write user-defined functions (UDFs) to extend the system to perform
  operations that are not available through the built-in system-defined functions
  provided by Snowflake. Once you create a UDF
last_scraped: '2026-01-14T16:55:23.214539+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/user-defined-functions.html
title: User-defined functions overview | Snowflake Documentation
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
    * [User-defined functions](../developer-guide/udf/udf-overview.md)

      + [Privileges](../developer-guide/udf/udf-access-control.md)
      + [Creating](../developer-guide/udf/udf-creating-sql.md)
      + [Executing](../developer-guide/udf/udf-calling-sql.md)
      + [Viewing in Snowsight](../user-guide/ui-snowsight-data-databases-function.md)
      + Handler writing
      + [Java](../developer-guide/udf/java/udf-java-introduction.md)
      + [Javascript](../developer-guide/udf/javascript/udf-javascript-introduction.md)
      + [Python](../developer-guide/udf/python/udf-python-introduction.md)
      + [Scala](../developer-guide/udf/scala/udf-scala-introduction.md)
      + [SQL](../developer-guide/udf/sql/udf-sql-introduction.md)
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

[Developer](../developer.md)[Functions and procedures](../developer-guide/extensibility.md)User-defined functions

# User-defined functions overview[¶](#user-defined-functions-overview "Link to this heading")

You can write user-defined functions (UDFs) to extend the system to perform operations that are not available through the
[built-in system-defined functions](../../sql-reference/intro-summary-operators-functions) provided by Snowflake. Once you create a UDF,
you can reuse it multiple times. A function always returns a value explicitly by specifying an expression, so it’s a good choice for
calculating and return a value.

You can use UDFs to extend built-in functions or to encapsulate calculations that are standard for your organization. UDFs you create
can be called in a way similar to built-in functions.

You write a UDF’s logic – its handler – in one of the [supported languages](#label-udf-supported-languages). Once you have a handler,
you can [create a UDF](udf-creating-sql) using any of several tools included in Snowflake, then
[execute the UDF](udf-calling-sql).

A UDF is like a stored procedure, but the two differ in important ways. For more information, see
[Choosing whether to write a stored procedure or a user-defined function](../stored-procedures-vs-udfs).

A UDF is just one way to extend Snowflake. For others, see the following:

* [Stored procedures overview](../stored-procedure/stored-procedures-overview)
* [Writing external functions](../../sql-reference/external-functions)
* [Snowpark API](../snowpark/index)

## User-defined function variations[¶](#user-defined-function-variations "Link to this heading")

You can write a UDF in one of several variations, depending on the input and output requirements your function must meet.

| Variation | Description |
| --- | --- |
| User-defined function (UDF) | Also known as a *scalar function*, returns one output row for each input row. The returned row consists of a single column/value. |
| User-defined aggregate function (UDAF) | Operates on values across multiple rows to perform mathematical calculations such as sum, average, counting, finding minimum or maximum values, standard deviation, and estimation, as well as some non-mathematical operations. |
| User-defined table function (UDTF) | Returns a tabular value for each input row. |
| Vectorized user-defined function (UDF) | Receive batches of input rows as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html) or [Series](https://pandas.pydata.org/docs/reference/series.html). |
| Vectorized user-defined table function (UDTF) | Receive batches of input rows as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and return tabular results. |

## Supported languages and tools[¶](#supported-languages-and-tools "Link to this heading")

You can [create](udf-creating-sql) and manage UDFs (and other Snowflake entities) by using any of multiple
tools, depending on how you prefer to work.

| Language | Approach | Support |
| --- | --- | --- |
| **SQL**  With handler in Java, JavaScript, Python, Scala, or SQL | Write SQL code in Snowflake to create and manage Snowflake entities. Write the function’s logic in one of the supported handler languages. | Java:  [UDF](java/udf-java-introduction), [UDTF](java/udf-java-tabular-functions)  JavaScript:  [UDF](javascript/udf-javascript-introduction), [UDTF](javascript/udf-javascript-tabular-functions)  Python:  [UDF](python/udf-python-introduction), [UDAF](python/udf-python-aggregate-functions), [UDTF](python/udf-python-tabular-functions), [Vectorized UDF](python/udf-python-batch), [Vectorized UDTF](python/udf-python-tabular-vectorized)  Scala:  [UDF](scala/udf-scala-introduction)  SQL:  [UDF](sql/udf-sql-introduction), [UDTF](sql/udf-sql-tabular-functions) |
| **Java, Python, or Scala**  [Snowpark API](../snowpark/index) | On the client, write code for operations that are pushed to Snowflake for processing. | Java:  [UDF](../snowpark/java/creating-udfs), [UDTF](../snowpark/java/creating-udfs.html#label-snowpark-java-udtf)  Python:  [UDF](../snowpark/python/creating-udfs), [UDAF](../snowpark/python/creating-udafs), [UDTF](../snowpark/python/creating-udtfs), [Vectorized UDF or UDTF](../snowpark/python/creating-udfs.html#label-snowpark-python-udf-vectorized)  Scala:  [UDF](../snowpark/scala/creating-udfs), [UDTF](../snowpark/scala/creating-udfs.html#label-snowpark-udtf) |
| **Command-line Interface**  [Snowflake CLI](../snowflake-cli/index) | Use the command line to create and manage Snowflake entities, specifying properties as properties of JSON objects. | [Managing Snowflake objects](../snowflake-cli/objects/manage-objects) |
| **Python**  [Snowflake Python API](../snowflake-python-api/snowflake-python-overview) | On the client, Execute commands to create the function with Python, writing the function’s handler in one of the supported handler languages. | [Managing user-defined functions (UDFs)](../snowflake-python-api/snowflake-python-managing-functions-procedures.html#label-snowflake-python-udfs) |
| **REST**  [Snowflake REST API](../snowflake-rest-api/snowflake-rest-api) | Make requests of RESTful endpoints to create and manage Snowflake entities. | [Manage user-defined functions](../snowflake-rest-api/user-defined-function/user-defined-function-introduction) |

When choosing a language, consider also the following:

* **Handler locations supported.** Not all languages support referring to the handler on a stage (the handler code must instead be in-line).
  For more information, see [Keeping handler code in-line or on a stage](../inline-or-staged).
* **Whether the handler results in a UDF that’s sharable.** A sharable UDF can be used with the Snowflake
  [Secure Data Sharing](../../user-guide/data-sharing-intro) feature.

| Language | Handler Location | Sharable |
| --- | --- | --- |
| Java | In-line or staged | No [[1]](#id5) |
| JavaScript | In-line | Yes |
| Python | In-line or staged | No [[2]](#id6) |
| Scala | In-line or staged | No [[3]](#id7) |
| SQL | In-line | Yes |

[[1](#id2)]

For more information about limits on sharing Java UDFs, see [General limitations](java/udf-java-limitations.html#label-limitations-on-java-udfs).


[[2](#id3)]

For more information about limits on sharing Python UDFs, see [General limitations](python/udf-python-limitations.html#label-limitations-on-python-udfs).


[[3](#id4)]

For more information about limits on sharing Scala UDFs, see [Scala UDF limitations](scala/udf-scala-limitations).

## Considerations[¶](#considerations "Link to this heading")

* If a query calls a UDF to access staged files, the operation fails with a user error if the SQL statement also queries a view that
  calls any UDF or UDTF, regardless of whether the function in the view accesses staged files or not.
* UDTFs can process multiple files in parallel; however, UDFs currently process files serially. As a workaround,
  group rows in a subquery using the [GROUP BY](../../sql-reference/constructs/group-by) clause. See [Process a CSV with a UDTF](../../user-guide/unstructured-data-java.html#label-unstructured-udtf-examples)
  for an example.
* Currently, if staged files referenced in a query are modified or deleted while the query is running, the function call fails with an
  error.
* If you specify the [CURRENT\_DATABASE](../../sql-reference/functions/current_database) or [CURRENT\_SCHEMA](../../sql-reference/functions/current_schema) function in the
  handler code of the UDF, the function returns the database or schema that contains the UDF, not the database or schema in use for
  the session.

## UDF example[¶](#udf-example "Link to this heading")

Code in the following example creates a UDF called `addone` with a handler written in Python. The handler function is
`addone_py`. This UDF returns an `int`.

```
CREATE OR REPLACE FUNCTION addone(i INT)
  RETURNS INT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  HANDLER = 'addone_py'
AS $$
def addone_py(i):
 return i+1
$$;
```

Copy

Code in the following example executes the `addone` UDF.

```
SELECT addone(3);
```

Copy

## Guidelines and constraints[¶](#guidelines-and-constraints "Link to this heading")

Snowflake constraints:
:   You can ensure stability within the Snowflake environment by developing within Snowflake constraints. For
    more information, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](../udf-stored-procedure-constraints).

Naming:
:   Be sure to name functions in a way that avoids collisions with other functions. For more information, see
    [Naming and overloading procedures and UDFs](../udf-stored-procedure-naming-conventions).

Arguments:
:   Specify the arguments and indicate which arguments are optional. For more information, see
    [Defining arguments for UDFs and stored procedures](../udf-stored-procedure-arguments).

Data type mappings:
:   For each handler language, there’s a separate set of mappings between the language’s data types and the SQL types
    used for arguments and return values. For more about the mappings for each language, see [Data Type Mappings Between SQL and Handler Languages](../udf-stored-procedure-data-type-mapping).

## Handler writing[¶](#handler-writing "Link to this heading")

Handler languages:
:   For language-specific content on writing a handler, see [Supported languages and tools](#label-udf-supported-languages).

External network access:
:   You can access external network locations with
    [external network access](../external-network-access/external-network-access-overview). You can create secure
    access to specific network locations external to Snowflake, then use that access from within the handler code.

Logging, tracing, and metrics:
:   You can record code activity by
    [capturing log messages, trace events, and metrics data](../logging-tracing/logging-tracing-overview),
    storing the data in a database you can query later.

## Security[¶](#security "Link to this heading")

You can grant privileges on objects needed for them to perform specific SQL actions with a UDF or UDTF. For more information, see
[Granting privileges for user-defined functions](udf-access-control)

Functions share certain security concerns with stored procedures. For more information, see the following:

* You can help a procedure’s handler code execute securely by following the best practices described in
  [Security Practices for UDFs and Procedures](../udf-stored-procedure-security-practices)
* Ensure that sensitive information is concealed from users who should not have access to it. For more information, see
  [Protecting Sensitive Information with Secure UDFs and Stored Procedures](../secure-udf-procedure)

## Handler code deployment[¶](#handler-code-deployment "Link to this heading")

When creating a function, you can specify its handler – which implements the function’s logic – as code in-line with the function
definition or as code external to the definition, such as code packaged and copied to a stage.

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

1. [User-defined function variations](#user-defined-function-variations)
2. [Supported languages and tools](#supported-languages-and-tools)
3. [Considerations](#considerations)
4. [UDF example](#udf-example)
5. [Guidelines and constraints](#guidelines-and-constraints)
6. [Handler writing](#handler-writing)
7. [Security](#security)
8. [Handler code deployment](#handler-code-deployment)

Related content

1. [Choosing whether to write a stored procedure or a user-defined function](/developer-guide/udf/../stored-procedures-vs-udfs)
2. [Extending Snowflake with Functions and Procedures](/developer-guide/udf/../extensibility)