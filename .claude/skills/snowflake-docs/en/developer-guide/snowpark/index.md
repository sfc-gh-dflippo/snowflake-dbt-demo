---
auto_generated: true
description: The Snowpark API provides an intuitive library for querying and processing
  data at scale in Snowflake. Using a library for any of three languages, you can
  build applications that process data in Snowf
last_scraped: '2026-01-14T16:54:39.928181+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/index
title: Snowpark API | Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](index.md)

   * [Java](java/index.md)
   * [Python](python/index.md)
   * [Scala](scala/index.md)
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
27. [Snowflake Scripting Developer Guide](../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)Snowpark API

# Snowpark API[¶](#snowpark-api "Link to this heading")

The Snowpark API provides an intuitive library for querying and processing data at scale in Snowflake. Using a library for any of three
languages, you can build applications that process data in Snowflake without moving data to the system where your application code runs,
and process at scale as part of the elastic and serverless Snowflake engine.

Snowflake currently provides Snowpark libraries for three languages: Java, Python, and Scala.

## Quickstarts[¶](#quickstarts "Link to this heading")

You can use the following Quickstarts to get a hands-on introduction to Snowpark.

* [Machine Learning with Snowpark Python](https://quickstarts.snowflake.com/guide/getting_started_snowpark_machine_learning/index.html)
* [Data Engineering Pipelines with Snowpark Python](https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python/index.html)
* [Getting Started With Snowpark for Python and Streamlit](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html)
* [An Image Recognition App in Snowflake using Snowpark Python, PyTorch, Streamlit and OpenAI](https://quickstarts.snowflake.com/guide/image_recognition_snowpark_pytorch_streamlit_openai/index.html)
* [Getting Started With Snowpark Scala](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_scala/index.html)

## Developer Guides[¶](#developer-guides "Link to this heading")

You can use Snowpark libraries for the languages listed in the following table:

| Language | Developer Guide | API Reference |
| --- | --- | --- |
| Java | [Snowpark Developer Guide for Java](java/index) | [Snowpark Library for Java API Reference](/developer-guide/snowpark/reference/java/index.html) |
| Python | [Snowpark Developer Guide for Python](python/index) | [Snowpark Library for Python API Reference](/developer-guide/snowpark/reference/python/latest/index) |
| Scala | [Snowpark Developer Guide for Scala](scala/index) | [Snowpark Library for Scala API Reference](/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/index.html) |

## Download[¶](#download "Link to this heading")

You can download the Snowpark library for any of the three supported languages. For downloads, see
[Snowpark Client Download](https://developers.snowflake.com/snowpark/) (Snowflake Developer Center).

## Key Features[¶](#key-features "Link to this heading")

Snowpark has several features that distinguish it from other client libraries, as described in the following sections.

### Benefits When Compared with the Spark Connector[¶](#benefits-when-compared-with-the-spark-connector "Link to this heading")

In comparison to using the [Snowflake Connector for Spark](../../user-guide/spark-connector), developing with Snowpark includes the following benefits:

* Support for interacting with data within Snowflake using libraries and patterns purpose built for different languages without compromising
  on performance or functionality.
* Support for authoring Snowpark code using local tools such as Jupyter, VS Code, or IntelliJ.
* Support for pushdown for all operations, including Snowflake UDFs. This means Snowpark pushes down all data transformation and
  heavy lifting to the Snowflake data cloud, enabling you to efficiently work with data of any size.
* No requirement for a separate cluster outside of Snowflake for computations. All of the computations are done within
  Snowflake. Scale and compute management are handled by Snowflake.

### Ability to Build SQL Statements with Native Constructs[¶](#ability-to-build-sql-statements-with-native-constructs "Link to this heading")

The Snowpark API provides programming language constructs for building SQL statements. For example, the API provides a
`select` method that you can use to specify the column names to return, rather than writing
`'select column_name'` as a string.

Although you can still use a string to specify the SQL statement to execute, you benefit from features like
[intelligent code completion](https://en.wikipedia.org/wiki/Intelligent_code_completion) and type checking when you use the
native language constructs provided by Snowpark.

#### Example[¶](#example "Link to this heading")

Python code in the following example performs a select operation on the `sample_product_data` table, specifying the columns
`id`, `name`, and `serial_number`.

```
>>> # Import the col function from the functions module.
>>> from snowflake.snowpark.functions import col

>>> # Create a DataFrame that contains the id, name, and serial_number
>>> # columns in the "sample_product_data" table.
>>> df = session.table("sample_product_data").select(col("id"), col("name"), col("serial_number"))
>>> df.show()
```

Copy

### Reduced Data Transfer[¶](#reduced-data-transfer "Link to this heading")

Snowpark operations are executed lazily on the server, meaning that you can use the library to delay running data transformation until as
late in the pipeline as possible while batching up many operations into a single operation. This reduces the amount of data transferred
between your client and the Snowflake database. It also improves performance.

The core abstraction in Snowpark is the DataFrame, which represents a set of data and provides methods to operate on that data.
In your client code, you construct a DataFrame object and set it up to retrieve the data that you want to use (for example, the
columns containing the data, the filter to apply to rows, etc.).

The data isn’t retrieved when you construct the DataFrame object. Instead, when you are ready to retrieve the data,
you can perform an action that evaluates the DataFrame objects and sends the corresponding SQL statements to the Snowflake
database for execution.

#### Example[¶](#id1 "Link to this heading")

Python code in the following example sets up a query against a table. It calls the `collect` method to execute the query and retrieve
results.

```
>>> # Create a DataFrame with the "id" and "name" columns from the "sample_product_data" table.
>>> # This does not execute the query.
>>> df = session.table("sample_product_data").select(col("id"), col("name"))

>>> # Send the query to the server for execution and
>>> # return a list of Rows containing the results.
>>> results = df.collect()
```

Copy

### Ability to Create UDFs Inline[¶](#ability-to-create-udfs-inline "Link to this heading")

You can create user-defined functions (UDFs) inline in a Snowpark app. Snowpark can push your code to the server, where the code can
operate on the data at scale. This is useful for looping or batch functionality where creating as a UDF will allow Snowflake to parallelize
and apply the codeful logic at scale within Snowflake.

You can write functions in the same language that you use to write your client code (for example, by using anonymous functions
in Scala or by using lambda functions in Python). To use these functions to process data in the Snowflake database, you define
and call user-defined functions (UDFs) in your custom code.

Snowpark automatically pushes the custom code for UDFs to the Snowflake engine. When you call the UDF in your client code,
your custom code is executed on the server (where the data is). You don’t need to transfer the data to your client in order to
execute the function on the data.

#### Example[¶](#id2 "Link to this heading")

Python code in the following example creates a UDF called `my_udf` and assigns it to the `add_one` variable.

```
>>> from snowflake.snowpark.types import IntegerType
>>> add_one = udf(lambda x: x+1, return_type=IntegerType(), input_types=[IntegerType()], name="my_udf", replace=True)
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

On this page

1. [Quickstarts](#quickstarts)
2. [Developer Guides](#developer-guides)
3. [Download](#download)
4. [Key Features](#key-features)

Related content

1. [Snowpark Developer Guide for Scala](/developer-guide/snowpark/scala/index)
2. [Snowpark Developer Guide for Java](/developer-guide/snowpark/java/index)
3. [Snowpark Developer Guide for Python](/developer-guide/snowpark/python/index)

Related info

* [Snowpark Library for Scala and Java release notes](../../release-notes/clients-drivers/snowpark-scala-java)
* [Getting Started With Snowpark in Scala](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_scala/index.html) (Snowflake Quickstarts)