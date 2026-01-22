---
auto_generated: true
description: This topic covers Scalar JavaScript UDFs (user-defined function).
last_scraped: '2026-01-14T16:56:40.810370+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-scalar-functions
title: Scalar JavaScript UDFs | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../../snowpark/index.md)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)

    * [Function or procedure?](../../stored-procedures-vs-udfs.md)
    * [Guidelines](../../udf-stored-procedure-guidelines.md)
    * [Stored procedures](../../stored-procedure/stored-procedures-overview.md)
    * [User-defined functions](../udf-overview.md)

      + [Privileges](../udf-access-control.md)
      + [Creating](../udf-creating-sql.md)
      + [Executing](../udf-calling-sql.md)
      + [Viewing in Snowsight](../../../user-guide/ui-snowsight-data-databases-function.md)
      + Handler writing
      + [Java](../java/udf-java-introduction.md)
      + [Javascript](udf-javascript-introduction.md)

        - [Limitations](udf-javascript-limitations.md)
        - [Scalar functions](udf-javascript-scalar-functions.md)
        - [Table functions](udf-javascript-tabular-functions.md)
        - [Troubleshooting](udf-javascript-troubleshooting.md)
      + [Python](../python/udf-python-introduction.md)
      + [Scala](../scala/udf-scala-introduction.md)
      + [SQL](../sql/udf-sql-introduction.md)
    * [Packaging handler code](../../udf-stored-procedure-building.md)
    * [External network access](../../external-network-access/external-network-access-overview.md)
13. [Logging, Tracing, and Metrics](../../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../../streamlit/object-management/billing.md)
      - [Security considerations](../../streamlit/object-management/security.md)
      - [Privilege requirements](../../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../../streamlit/app-development/dependency-management.md)
      - [File organization](../../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../../streamlit/features/git-integration.md)
      - [External access](../../streamlit/features/external-access.md)
      - [Row access policies](../../streamlit/features/row-access.md)
      - [Sleep timer](../../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../../streamlit/troubleshooting.md)
    - [Release notes](../../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../../snowflake-cli/index.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Functions and procedures](../../extensibility.md)[User-defined functions](../udf-overview.md)[Javascript](udf-javascript-introduction.md)Scalar functions

# Scalar JavaScript UDFs[¶](#scalar-javascript-udfs "Link to this heading")

This topic covers Scalar JavaScript UDFs (user-defined function).

## Introduction[¶](#introduction "Link to this heading")

A scalar JavaScript UDF returns one output row for each input row. The output row must contain only one column/value.

A basic example is in [Introduction to JavaScript UDFs](udf-javascript-introduction). Additional examples are below.

Note

Scalar functions (UDFs) have a limit of 500 input arguments.

## Examples[¶](#examples "Link to this heading")

This section contains examples of scalar JavaScript UDFs.

### Recursion[¶](#recursion "Link to this heading")

The following example shows that a JavaScript UDF can call itself (i.e. it can use recursion).

Create a recursive UDF:

```
CREATE OR REPLACE FUNCTION RECURSION_TEST (STR VARCHAR)
  RETURNS VARCHAR
  LANGUAGE JAVASCRIPT
  AS $$
  return (STR.length <= 1 ? STR : STR.substring(0,1) + '_' + RECURSION_TEST(STR.substring(1)));
  $$
  ;
```

Copy

Call the recursive UDF:

```
SELECT RECURSION_TEST('ABC');
+-----------------------+
| RECURSION_TEST('ABC') |
|-----------------------|
| A_B_C                 |
+-----------------------+
```

Copy

### Custom exception[¶](#custom-exception "Link to this heading")

The following example shows a JavaScript UDF that throws a custom exception.

Create the function:

```
CREATE FUNCTION validate_ID(ID FLOAT)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS $$
    try {
        if (ID < 0) {
            throw "ID cannot be negative!";
        } else {
            return "ID validated.";
        }
    } catch (err) {
        return "Error: " + err;
    }
$$;
```

Copy

Create a table with valid and invalid values:

```
CREATE TABLE employees (ID INTEGER);
INSERT INTO employees (ID) VALUES 
    (1),
    (-1);
```

Copy

Call the function:

```
SELECT ID, validate_ID(ID) FROM employees ORDER BY ID;
+----+-------------------------------+
| ID | VALIDATE_ID(ID)               |
|----+-------------------------------|
| -1 | Error: ID cannot be negative! |
|  1 | ID validated.                 |
+----+-------------------------------+
```

Copy

## Troubleshooting[¶](#troubleshooting "Link to this heading")

See [Troubleshooting JavaScript UDFs](udf-javascript-troubleshooting).

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
2. [Examples](#examples)
3. [Troubleshooting](#troubleshooting)

Related content

1. [User-defined functions overview](/developer-guide/udf/javascript/../udf-overview)
2. [Tabular JavaScript UDFs (UDTFs)](/developer-guide/udf/javascript/udf-javascript-tabular-functions)
3. [Introduction to Java UDFs](/developer-guide/udf/javascript/../java/udf-java-introduction)
4. [Scalar SQL UDFs](/developer-guide/udf/javascript/../sql/udf-sql-scalar-functions)