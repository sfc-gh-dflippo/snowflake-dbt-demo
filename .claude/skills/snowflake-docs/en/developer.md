---
auto_generated: true
description: Write applications that extend Snowflake, act as a client, or act as
  an integrating component.
last_scraped: '2026-01-14T16:54:22.040930+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer
title: Develop Apps and Extensions
---

1. [Overview](developer.md)
2. Builders
3. [Snowflake DevOps](developer-guide/builders/devops.md)
4. [Observability](developer-guide/builders/observability.md)
5. Snowpark Library
6. [Snowpark API](developer-guide/snowpark/index.md)
7. [Spark workloads on Snowflake](developer-guide/snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](developer-guide/snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](developer-guide/snowpark-container-services/overview.md)
12. [Functions and procedures](developer-guide/extensibility.md)
13. [Logging, Tracing, and Metrics](developer-guide/logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](developer-guide/snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](developer-guide/snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](developer-guide/sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](developer-guide/streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](developer-guide/streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](developer-guide/streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](developer-guide/streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](developer-guide/streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](developer-guide/streamlit/object-management/billing.md)
      - [Security considerations](developer-guide/streamlit/object-management/security.md)
      - [Privilege requirements](developer-guide/streamlit/object-management/privileges.md)
      - [Understanding owner's rights](developer-guide/streamlit/object-management/owners-rights.md)
      - [PrivateLink](developer-guide/streamlit/object-management/privatelink.md)
      - [Logging and tracing](developer-guide/streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](developer-guide/streamlit/app-development/runtime-environments.md)
      - [Dependency management](developer-guide/streamlit/app-development/dependency-management.md)
      - [File organization](developer-guide/streamlit/app-development/file-organization.md)
      - [Secrets and configuration](developer-guide/streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](developer-guide/streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](developer-guide/streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](developer-guide/streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](developer-guide/streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](developer-guide/streamlit/features/git-integration.md)
      - [External access](developer-guide/streamlit/features/external-access.md)
      - [Row access policies](developer-guide/streamlit/features/row-access.md)
      - [Sleep timer](developer-guide/streamlit/features/sleep-timer.md)
    - [Limitations and library changes](developer-guide/streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](developer-guide/streamlit/troubleshooting.md)
    - [Release notes](release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](developer-guide/native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](developer-guide/declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](developer-guide/native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](developer-guide/snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](developer-guide/snowflake-cli/index.md)
30. [Git](developer-guide/git/git-overview.md)
31. Drivers
32. [Overview](developer-guide/drivers.md)
33. [Considerations when drivers reuse sessions](developer-guide/driver-connections.md)
34. [Scala versions](developer-guide/scala-version-differences.md)
35. Reference
36. [API Reference](api-reference.md)

# Develop Apps and Extensions

Write applications that extend Snowflake, act as a client, or act as an integrating component.

SNOWPARK API

## Run Python, Java, and Scala Code in Snowpark

Using Snowpark libraries and code execution environments, you can run Python and other programming languages next to your data in Snowflake.

#### Build

Enable all data users to bring their work to a single platform with native support for Python, Java, Scala, and more.

#### Secure

Apply consistent controls trusted by over 500 of the Forbes Global 2000 across all workloads.

#### Optimize

Benefit from the Snowflake Data Cloud with super price/performance and near-zero maintenance.

Get to know Snowpark API

Snowpark is the set of libraries and code execution environments that run Python and other programming languages next to your data in Snowflake. Snowpark can be used to build data pipelines, ML models, apps, and other data processing tasks.

[Learn more](developer-guide/snowpark/index.md)

![Snowpark example code](/images/snowpark-code-example-banner.svg)

### Code in Snowpark with multiple languages

Run custom Python, Java, or Scala code directly in Snowflake with Snowpark user-defined functions (UDFs) and stored procedures. There are no separate clusters to manage, scale, or operate.

PythonJavaScala

```
from snowflake.snowpark import Session  
from snowflake.snowpark.functions import col  
  
# Create a new session, using the connection properties specified in a file.  
new_session = Session.builder.configs(connection_parameters).create()  
  
# Create a DataFrame that contains the id, name, and serial_number  
# columns in the “sample_product_data” table.  
df = session.table("sample_product_data").select(  
col("id"), col("name"), col("name"), col("serial_number")  
)  
  
# Show the results   
df.show()
```

[Developer Guide](/developer-guide/snowpark/python/index)[API Reference](/developer-guide/snowpark/reference/python/index.html)

### Try Snowpark

Use the following quickstart tutorials to get a hands-on introduction to Snowpark

[TUTORIAL

Getting Started with Data Engineering and ML using Snowpark for Python

Follow this step-by-step guide to transform raw data into an interactive application using Python with Snowpark and Streamlit.](https://quickstarts.snowflake.com/guide/getting_started_with_dataengineering_ml_using_snowpark_python/index.html)

[TUTORIAL

Data Engineering Pipelines with Snowpark Python

Learn how to build end-to-end data engineering pipelines using Snowpark with Python.](https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python)

[TUTORIAL

Getting Started with Snowflake ML

Build an end-to-end ML workflow — from feature engineering to model training and batch inference — using Snowflake ML.](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/index.html)

Snowflake AI and ML

## Build ML models and run AI workflows in Snowflake

Snowflake offers two broad categories of features based on generative artificial intelligence (AI) and machine learning (ML).

### Run Snowflake Cortex AI next to your data

Understand unstructured data, answer freeform questions, generate accurate text-to-SQL responses, and provide intelligent assistance using large language models (LLMs).

[User Guide

Snowflake Cortex LLM Functions

Access industry-leading large language models (LLMs) that are fully hosted and managed by Snowflake.](user-guide/snowflake-cortex/llm-functions.md)

[User Guide

Snowflake Copilot

Simplify data analysis while maintaining robust data governance using an LLM-powered assistant.](user-guide/snowflake-copilot.md)

[User Guide

Cortex Agents

Orchestrate tasks across both structured and unstructured data sources to analyze data and deliver insights.](user-guide/snowflake-cortex/cortex-agents.md)

[User Guide

Cortex Search

Build enterprise search and retrieval-augmented generation (RAG) applications on unstructured text data.](user-guide/snowflake-cortex/cortex-search/cortex-search-overview.md)

### Build end-to-end Machine Learning workflows

Pre-process data and train, manage, and deploy machine learning models, all within Snowflake.

[Developer Guide

Model development

Transform data and train models. Run your ML pipeline within security and governance frameworks.](developer-guide/snowflake-ml/modeling.md)

[Developer Guide

Model Registry

Securely manage models and their metadata in Snowflake regardless of origin.](developer-guide/snowflake-ml/model-registry/overview.md)

[Developer Guide

Feature Store

Make creating, storing, and managing features for machine learning workloads easier and more efficient.](developer-guide/snowflake-ml/feature-store/overview.md)

[Developer Guide

Datasets

Immutable, versioned snapshots of data ready to be fed to popular machine learning frameworks.](developer-guide/snowflake-ml/dataset.md)

[Developer Guide

Data Connectors

Provide Snowflake data to PyTorch and Tensorflow in their own formats.](developer-guide/snowflake-ml/framework-connectors.md)

[API Reference

Snowflake ML Python

The Python API for Snowflake ML modeling and ML Ops features.](developer-guide/snowflake-ml/snowpark-ml.md)

Snowflake Python APIs

## Manage Snowflake resources, apps, and data pipelines

Create and manage Snowflake resources across data engineering, Snowpark, Snowflake ML, and application workloads using a unified, first-class Python API.

[Developer Guide

Snowflake Python APIs overview

Learn about the Snowflake Python APIs and how to get started.](developer-guide/snowflake-python-api/snowflake-python-overview.md)

[Tutorial

Getting started with the Snowflake Python APIs

Learn the fundamentals for creating and managing Snowflake resources using the Snowflake Python APIs.](developer-guide/snowflake-python-api/overview-tutorials.md)

[API Reference

Snowflake Python APIs reference

Reference for the Snowflake Python APIs.](developer-guide/snowflake-python-api/reference/latest/index.md)

NATIVE APPS FRAMEWORK

## Build secure data applications

Expand the capabilities of other Snowflake features by sharing data and related business logic with other Snowflake accounts.

[Tutorial

Developing an Application with the Native Apps Framework

Follow this step-by-step tutorial to create a secure data application using the Native Apps Framework.](developer-guide/native-apps/tutorials/getting-started-tutorial.md)

[Developer Guide

About the Native Apps Framework

Learn about the building blocks of the Native Apps Framework, including key terms and components.](developer-guide/native-apps/native-apps-about.md)

[Developer Guide

Native Apps Framework Workflows

Understand the end-to-end workflows for developing, publishing, and using applications.](developer-guide/native-apps/native-apps-workflow.md)

[SQL Reference

Native Apps Framework Commands

View the SQL commands used to create and use database objects supported by the Native Apps Framework.](sql-reference/commands-native-apps.md)

SNOWPARK CONTAINER SERVICES

## Deploy, manage, and scale containerized applications

Build atop a fully-managed service that comes with Snowflake security, configuration, and operational best practices built in.

[Developer Guide

Snowpark Container Services Overview

Learn about Snowpark Container Services, including how it works and how to get started.](developer-guide/snowpark-container-services/overview.md)

[Tutorial

Introductory tutorials

Learn the basics of creating a Snowpark Container Services service.](developer-guide/snowpark-container-services/overview-tutorials.md)

[Tutorial

Advanced tutorials

Learn advanced concepts such as service-to-service communications.](developer-guide/snowpark-container-services/overview-advanced-tutorials.md)

STREAMLIT IN SNOWFLAKE

## Develop custom web apps for machine learning and data science

Securely build, deploy, and share Streamlit apps on Snowflake’s data cloud.

[Developer Guide

About Streamlit in Snowflake

Learn about deploying Streamlit apps by using Streamlit in Snowflake.](developer-guide/streamlit/about-streamlit.md)

[Developer Guide

Example - Accessing Snowflake data from Streamlit in Snowflake

Learn how to securely access Snowflake data from a Streamlit app.](developer-guide/streamlit/getting-started/overview.md)

[Developer Guide

Developing a Streamlit app by using Snowsight

Learn how to quickly create, use, and share a Streamlit app in Snowsight.](developer-guide/streamlit/getting-started/create-streamlit-ui.md)

FUNCTIONS AND PROCEDURES

## Extend Snowflake Capabilities

Enhance and extend Snowflake by writing procedures and user-defined functions. In both cases, you write the logic in one of the supported programming languages.

[Developer Guide

Stored Procedures or UDFs

Understand key differences between procedures and UDFs.](developer-guide/stored-procedures-vs-udfs.md)

[Developer Guide

Stored Procedures

Perform scheduled or on-demand operations by executing code or SQL statements.](developer-guide/stored-procedure/stored-procedures-overview.md)

[Developer Guide

User-Defined Functions (UDFs)

Run logic to calculate and return data for batch processing and integrating custom logic into SQL.](developer-guide/udf/udf-overview.md)

[Developer Guide

Design Guidelines

General guidelines on security, conventions, and more.](developer-guide/udf-stored-procedure-guidelines.md)

[Developer Guide

Packaging Handler Code

Build a JAR file that contains the handler and its dependencies. Reference the handler JAR on a stage.](developer-guide/udf-stored-procedure-building.md)

[Developer Guide

Writing External Functions

Writing external functions you can use to invoke code on other systems.](sql-reference/external-functions.md)

[Developer Guide

Logging and Tracing

Capture log and trace messages in an event table that you can query for analysis later.](developer-guide/logging-tracing/logging-tracing-overview.md)

[Developer Guide

External Network Access

A guide for accessing network locations external to Snowflake.](developer-guide/external-network-access/external-network-access-overview.md)

KAFKA AND SPARK CONNECTORS

## Integrate with Other Systems

Snowflake includes connectors with APIs for integrating with systems outside Snowflake.

[User Guide

Snowflake Ecosystem

Integrate Snowflake with many other systems for exchanging data, performing analysis, and more.](user-guide/ecosystem.md)

[User Guide

Apache Kafka

Send events from the Kafka event streaming platform to Snowflake.](user-guide/kafka-connector-overview.md)

[User Guide

Apache Spark

Integrate the Apache Spark analytics engine in Spark workloads for data processing directly on Snowflake.](user-guide/spark-connector-overview.md)

DRIVERS

## Build a Client App with Drivers and APIs

Integrate Snowflake operations into a client app. In addition to the Snowpark API, you can also use language and platform specific drivers.

### Drivers

Drivers allow you to connect from your code or apps to Snowflake. Using languages such as C#, Go, and Python, you can write applications that perform operations on Snowflake.

[Go Snowflake Driver](/developer-guide/golang/go-driver)[JDBC Driver](/developer-guide/jdbc/jdbc)[.NET Driver](/developer-guide/dotnet/dotnet-driver)[Node.js Driver](/developer-guide/node-js/nodejs-driver)[ODBC Driver](/developer-guide/odbc/odbc)[PHP PDO Driver](/developer-guide/php-pdo/php-pdo-driver)[Python Connector](/developer-guide/python-connector/python-connector)

### RESTful API

Using the Snowflake RESTful SQL API, you can access and update data over HTTPS and REST. For example, you can submit SQL statements, create and execute stored procedures, provision users, and so on.

In the SQL REST API, you submit a SQL statement for execution in the body of a POST request. You then check execution status and fetch results with GET requests.

[DEVELOPER GUIDE

Snowflake SQL REST API

Get started with the Snowflake SQL REST API.](developer-guide/sql-api/index.md)

TOOLS

## Develop more efficiently

Work with Snowflake using tools that integrate well with your existing workflow.

### Work with Snowflake from the command line

Use the command line to create, manage, update, and view apps running on Snowflake across workloads.

[DEVELOPER GUIDE

Introducing Snowflake CLI

Learn about Snowflake CLI benefits and how it differs from SnowSQL.](developer-guide/snowflake-cli-v2/introduction/introduction.md)

[DEVELOPER GUIDE

Installing Snowflake CLI

Install Snowflake CLI using common package managers.](developer-guide/snowflake-cli-v2/installation/installation.md)

[REFERENCE

Snowflake CLI command reference

Explore commands for connecting, managing apps, objects, and other Snowflake features.](developer-guide/snowflake-cli-v2/command-reference/overview.md)

### Use Git from Snowflake

Execute and use Git repository code directly from Snowflake.

[DEVELOPER GUIDE

Using a Git repository in Snowflake

Integrate your Git repository with Snowflake and fetch repository files to a repository stage that is a Git client with a full clone of the repository.](developer-guide/git/git-overview.md)

[DEVELOPER GUIDE

Setting up Snowflake to use Git

Set up Snowflake to securely interact with your Git repository.](developer-guide/git/git-setting-up.md)

[DEVELOPER GUIDE

Git operations in Snowflake

Perform common Git operations from within Snowflake, including fetching files, viewing branches or tags, and executing repository code.](developer-guide/git/git-operations.md)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.