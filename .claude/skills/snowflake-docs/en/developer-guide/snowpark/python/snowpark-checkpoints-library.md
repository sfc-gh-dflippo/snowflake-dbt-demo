---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:54:55.556483+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/python/snowpark-checkpoints-library
title: Snowpark Checkpoints | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../index.md)

   * [Java](../java/index.md)
   * [Python](index.md)

     + [Setting Up a Development Environment](setup.md)
     + [Creating a Session](creating-session.md)
     + [Snowpark DataFrames](working-with-dataframes.md)

       - [Writing Snowpark Code in Python Worksheets](python-worksheets.md)
       - [Using Snowpark to Read Data](reading-data.md)
       - [Creating User Defined Functions](creating-udfs.md)
       - [Creating User Defined Table Functions](creating-udtfs.md)
       - [Creating User Defined Aggregate Functions](creating-udafs.md)
       - [Creating Stored Procedures for DataFrames](creating-sprocs.md)
       - [Profiling Procedure Handlers](profiling-procedure-handlers.md)
       - [Calling Functions and Stored Procedures](calling-functions.md)
       - [Training Machine Learning Models with Snowpark Python](python-snowpark-training-ml.md)
       - [Writing Tests for Snowpark Python](testing-python-snowpark.md)
       - [Local Testing Framework](testing-locally.md)
       - [Tutorial: Testing Python Snowpark](tutorials/testing-tutorial.md)
       - [Troubleshooting](troubleshooting.md)
       - [Snowpark Checkpoints](snowpark-checkpoints-library.md)

         * [Setting up Snowpark Checkpoints](checkpoints-setup-snowpark-checkpoints.md)
         * [Using Checkpoints](checkpoints-using-checkpoints.md)
         * [Snowpark Checkpoints API Reference](../../snowpark-checkpoints-api/reference/latest/index.md)
     + [pandas on Snowflake](pandas-on-snowflake.md)
     + [Python API Reference](../reference/python/latest/index.md)
   * [Scala](../scala/index.md)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)
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

[Developer](../../../developer.md)[Snowpark API](../index.md)[Python](index.md)[Snowpark DataFrames](working-with-dataframes.md)Snowpark Checkpoints

# Snowpark Checkpoints[¶](#snowpark-checkpoints "Link to this heading")

[![Snowflake logo in black (no text)](../../../_images/logo-snowflake-black.png)](../../../_images/logo-snowflake-black.png) [Preview Feature](../../../release-notes/preview-features) — Open

Available to all accounts.

Snowpark Checkpoints is a testing library that validates code migrated from [Apache PySpark](https://spark.apache.org/) to Snowpark Python. It compares the outputs of DataFrame operations across both platforms, ensuring that Snowpark implementations produce results that are functionally equivalent to their PySpark counterparts. It strives to maintain data integrity and analytical consistency throughout the migration process.

![Checkpoints SMA extension](../../../_images/checkpoints-extend.png)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.