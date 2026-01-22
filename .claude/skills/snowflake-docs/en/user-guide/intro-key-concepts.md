---
auto_generated: true
description: Snowflake is powered by an advanced data platform that is provided to
  you as a self-managed service. Snowflake’s data platform brings together data storage,
  processing, and analytic solutions that are
last_scraped: '2026-01-14T16:54:50.792447+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/intro-key-concepts
title: Snowflake key concepts and architecture | Snowflake Documentation
---

1. [Overview](getting-started.md)
2. [Get started for users](../getting-started-for-users.md)

   * [Before you begin](setup.md)
   * [Sign in](connecting.md)
   * [Key concepts and architecture](intro-key-concepts.md)
   * [Snowsight tour](ui-snowsight-quick-tour.md)
   * [Data lifecycle](data-lifecycle.md)
3. [Tutorials](../learn-tutorials.md)
4. [Concepts for administrators](../concepts-for-administrators.md)
5. [Sample data](sample-data.md)
6. [Contacting support](contacting-support.md)

[Get started](getting-started.md)[Get started for users](../getting-started-for-users.md)Key concepts and architecture

# Snowflake key concepts and architecture[¶](#snowflake-key-concepts-and-architecture "Link to this heading")

Snowflake is powered by an advanced data platform that is provided to you as a self-managed
service. Snowflake’s data platform brings together data storage, processing, and analytic solutions
that are faster, easier to use, and far more flexible than traditional offerings.

Snowflake combines a completely new SQL query engine with an innovative architecture that is
natively designed for the cloud. It offers full enterprise analytic database functionality,
and unique features and capabilities.

## Data platform as a self-managed service[¶](#data-platform-as-a-self-managed-service "Link to this heading")

As a *self-managed service*, Snowflake has the following advantages:

* There is no hardware (virtual or physical) for you to select, install, configure, or manage.
* There is virtually no software for you to install, configure, or manage.
* Ongoing maintenance, management, upgrades, and tuning are handled by Snowflake.

Snowflake uses public cloud infrastructure to host virtual compute instances and persistent data storage.
Snowflake manages software updates and infrastructure so you don’t have to. You can’t install and run Snowflake
locally or on private cloud infrastructures, whether on-premises or hosted.

## Snowflake architecture[¶](#snowflake-architecture "Link to this heading")

Snowflake’s architecture is a hybrid of traditional shared-disk and shared-nothing database architectures.
Similar to shared-disk architectures, Snowflake uses a central data repository for persisted data that is
accessible from all compute nodes in the platform. But similar to shared-nothing architectures, Snowflake
processes queries using massively parallel processing (MPP) compute clusters, where each node in the cluster
stores a portion of the entire data set locally. This hybrid architecture, which is shown in the following diagram,
offers the data management simplicity of a shared-disk architecture, but with the performance and scale-out benefits
of a shared-nothing architecture:

![Snowflake architecture overview](../_images/architecture-overview.png)

Snowflake’s unique architecture has the following key layers:

* [Database storage](#label-intro-key-concepts-storage)
* [Compute](#label-intro-key-concepts-compute)
* [Cloud services](#label-intro-key-concepts-cloud-services)

### Database storage[¶](#database-storage "Link to this heading")

Snowflake supports the following kinds of data:

* *Structured data* — such as rows and columns in a table — follows a strict tabular schema.
* *Semi-structured data* — such as a JSON file or an XML file — has a flexible schema.
* *Unstructured data* — such as a document, image, or audio file — has no inherent schema.

Snowflake supports several types of tables for data storage, including the following table types:

* [Snowflake tables](#label-intro-key-concepts-storage-snowflake-tables)
* [Apache Iceberg™ tables](#label-intro-key-concepts-storage-iceberg-tables)
* [Hybrid tables](#label-intro-key-concepts-storage-hybrid-tables)

#### Snowflake tables[¶](#snowflake-tables "Link to this heading")

When data is loaded into a Snowflake table, Snowflake reorganizes that data into its internally optimized,
compressed, columnar format. Snowflake stores this optimized data in cloud storage. Snowflake tables
are ideal for data warehouses.

Snowflake manages all aspects of how this data is stored — including the organization, file size,
structure, compression, metadata, and statistics. All data in Snowflake tables is automatically divided
into *micro-partitions*, which are contiguous units of storage. Micro-partitions improve efficiency and
provide other benefits.

You can use Snowflake tables to store structured and semi-structured data. You can also use the
[FILE data type](../sql-reference/data-types-unstructured.html#label-data-types-file) for unstructured data.

For more information about Snowflake tables, see [Understanding Snowflake Table Structures](tables-micro-partitions).

#### Apache Iceberg™ tables[¶](#iceberg-tm-tables "Link to this heading")

Apache Iceberg™ tables for Snowflake combine the performance and query semantics of typical
Snowflake tables with external cloud storage that you manage. They are
ideal for existing data lakes and data lakehouses that you can’t, or choose not to, store in Snowflake.

Iceberg tables store their data and metadata files in an external cloud storage location; for example,
Amazon S3, Google Cloud Storage, or Microsoft Azure Storage. The external storage isn’t part of Snowflake.

You can use Iceberg tables to store structured and semi-structured data.

For more information, see [Apache Iceberg™ tables](tables-iceberg).

#### Hybrid tables[¶](#hybrid-tables "Link to this heading")

Hybrid tables are optimized for low latency and high throughput by using index-based random reads and writes.
Hybrid tables support row locking and enforce unique and referential integrity constraints, which are
critical for transactional workloads. You can use a hybrid table along with other Snowflake
tables and features for [Unistore workloads](https://www.snowflake.com/en/data-cloud/workloads/unistore/)
that bring transactional and analytical data together in a single platform.

You can use hybrid tables to store structured and semi-structured data.

For more information, see [Hybrid tables](tables-hybrid).

### Compute[¶](#compute "Link to this heading")

A *virtual warehouse* is a cluster of compute resources in Snowflake. Virtual warehouses process
SQL statements and, using [Snowpark](../developer-guide/snowpark/index), run code in languages,
such as Java, Python, and Scala. With
[Snowpark Connect for Spark](../developer-guide/snowpark-connect/snowpark-connect-overview), you
can also run Apache Spark™ workloads on virtual warehouses.

Each virtual warehouse is an independent compute cluster that doesn’t share compute resources with other
virtual warehouses. As a result, each virtual warehouse has no effect on the performance of other virtual
warehouses.

For more information, see [Virtual warehouses](warehouses).

### Cloud services[¶](#cloud-services "Link to this heading")

The cloud services layer is a collection of services that coordinate activities across Snowflake. These services
tie together all of the different components of Snowflake in order to process user requests, from sign-in to query
dispatch. The cloud services layer also runs on compute instances that are provisioned by Snowflake from the cloud
provider.

Services managed in this layer include the following:

* [Security, authentication, and access control](../guides-overview-secure)
* [Snowflake Horizon Catalog](snowflake-horizon)
* [Infrastructure management with cloud platforms](intro-cloud-platforms)
* Metadata management, including the [SNOWFLAKE database](../sql-reference/snowflake-db) and the [Snowflake Information Schema](../sql-reference/info-schema)
* [Query parsing and optimization](../guides-overview-performance)
* [Regulatory compliance](intro-compliance)

## Integrated features for your workloads[¶](#integrated-features-for-your-workloads "Link to this heading")

Instead of moving data to different systems so that different teams can complete specific operations and tasks,
you can bring all of your workloads directly to their data with an integrated set of features.

These features support the following broad areas of data integration and development:

* [Data engineering](#label-intro-key-concepts-cloud-services-data-engineering)
* [Analytics](#label-intro-key-concepts-cloud-services-analytics)
* [AI and ML](#label-intro-key-concepts-cloud-services-ai)
* [Applications and collaboration](#label-intro-key-concepts-cloud-services-applications-and-collaboration)

### Data engineering[¶](#data-engineering "Link to this heading")

Snowflake separates storage and compute, which simplifies some traditional challenges of data engineering,
such as infrastructure management and performance tuning. Data engineers can focus on implementing pipelines that
ingest, transform, and deliver data.

Snowflake provides several ways to ingest data, including the following options:

* [COPY INTO <table>](../sql-reference/sql/copy-into-table) command — Loads data from files to a table.
* [Snowpipe](data-load-snowpipe-intro) — Loads data from files as soon as they are available in a stage.
* [Snowpipe Streaming](snowpipe-streaming/data-load-snowpipe-streaming-overview) — Loads row-level data continuously and with
  low latency, using the Snowflake SDKs or a REST API, directly into Snowflake tables and Snowflake-managed Iceberg tables,
  instead of loading data from files.
* [Openflow connectors](data-integration/openflow/connectors/about-openflow-connectors) — Ingest data from specific sources
  by using connectors built on Apache NiFi, such as Microsoft Sharepoint and Google Drive.
* [Snowflake Connectors](https://other-docs.snowflake.com/connectors.html) — Connect from external applications and systems and stream data into Snowflake.

Snowflake also provides several ways to transform data, including the following options:

* [Dynamic tables](dynamic-tables-about) — Define tables that automatically refresh based on target freshness and a query
  that performs data transformations.
* [Streams and tasks](data-pipelines-intro) — Capture changes made to base objects with streams and
  define tasks to perform data transformations.
* [Snowpark](../developer-guide/snowpark/index) — Perform more complex transformations by using programming languages,
  such as Python, Java, and Scala.
* [dbt](data-engineering/dbt-projects-on-snowflake) — Use an open-source data transformation
  tool and framework to define, test, and deploy SQL transformations.

In addition, [SnowConvert AI](../migrations/snowconvert-docs/overview) can ingest and transform data, and
[Snowpark Migration Accelerator](../migrations/sma-docs/general/introduction) can convert code from various platforms
to Snowflake.

For more information, see [Overview of data loading](data-load-overview).

### Analytics[¶](#analytics "Link to this heading")

With Snowflake, you can scale workloads dynamically based on demand, access different types of data — including structured,
semi-structured, and unstructured — and share data easily. These features let you analyze data stored in Snowflake
to extract meaningful insights, patterns, and trends for analytical use cases, such as business intelligence or predictive
modeling.

Snowflake provides several ways to analyze data, including the following options:

* System functions and SQL constructs — Perform calculations and statistical analysis with the following Snowflake system
  functions and SQL constructs:

  + [Aggregate functions](../sql-reference/functions-aggregation) — Summarize data by performing calculations on a set of related rows
    and returning a single value.
  + [Window functions](../sql-reference/functions-window) — Perform calculations on a set of related rows in partitions for
    rolling operations on subsets of the rows in each partition, such as calculating running totals or moving averages.
  + [Common table expressions (CTEs)](queries-cte) — Improve the readability and reusability of
    complex queries, which might perform multiple steps of data transformation.
* [Cortex AI Functions](snowflake-cortex/aisql) — Run unstructured analytics on text and images
  with large language models (LLMs) from OpenAI, Anthropic, Meta, Mistral AI, and DeepSeek.
* [Semantic views](views-semantic/overview) — Store semantic business concepts directly in the database to
  define business metrics and model business entities and their relationships.

### AI and ML[¶](#ai-and-ml "Link to this heading")

Snowflake simplifies the use of artificial intelligence (AI) and machine learning (ML) capabilities so you can
perform AI and ML feature engineering, training, and inference with your Snowflake data. Models can access your most
up-to-date data in a secure environment. With Snowflake, you can avoid the cost and complexity of moving your data to a
separate platform for AI and ML tasks.

Snowflake offers AI and ML capabilities in two broad suites of features:

* Snowflake Cortex — AI features that use LLMs to understand unstructured data, answer freeform
  questions, and provide intelligent assistance. [Cortex AI functions](snowflake-cortex/aisql.html#label-cortex-llm-ai-function) can automate routine tasks, such
  as simple summaries and quick translations.
* Snowflake ML — Features that you can use to build your own models. [ML functions](../guides-overview-ml-functions)
  give you automated predictions and insights into your data by using ML.
  [Snowflake ML](../developer-guide/snowflake-ml/overview) is a unified environment for ML development.

For more information, see [Snowflake AI and ML](../guides-overview-ai-features).

### Applications and collaboration[¶](#applications-and-collaboration "Link to this heading")

Snowflake offers many ways to build applications and share them with your teams, partners, and customers. When
you use Snowflake to share data, you control access to the data, and avoid the challenges of keeping it synchronized
in different places.

The following list shows some of the tools and services you can use to build, deploy, and manage applications in Snowflake:

* [Streamlit](../developer-guide/streamlit/about-streamlit) — Use an open-source Python library to create and
  share custom web apps with an interactive user interface (UI) for ML and data science.
* [Snowpark Container Services](../developer-guide/snowpark-container-services/overview) — Deploy, manage, and scale
  containerized applications from directly inside Snowflake.
* [Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about) — Build applications that
  expand the capabilities of other Snowflake features by sharing data and related business logic with other Snowflake
  accounts. The business logic of an application might include a Streamlit app, stored procedures, and functions
  written by using Snowpark API, JavaScript, and SQL. A Snowflake Native App can also run container workloads with
  Snowpark Container Services.

Snowflake includes support for the following kinds of collaboration:

* [Secure Data Sharing](data-sharing-intro) — Share selected objects in a database in your
  account with other Snowflake accounts.
* [Listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about) — Provide data and
  other information to other Snowflake users, or access data and other information shared by Snowflake providers.
  You can explore, access, and provide listings to consumers privately and on the [Snowflake Marketplace](https://other-docs.snowflake.com/collaboration/collaboration-marketplace-about).
* [Data Clean Rooms](cleanrooms/introduction) — Define what analyses can be run against the shared data,
  which allows the consumer to gather insights from the data without having unrestricted access to it.

## Snowgrid[¶](#snowgrid "Link to this heading")

Snowgrid is Snowflake’s cross-region, cross-cloud technology layer. With Snowgrid, you can achieve the following
goals:

* Connect a data ecosystem across different cloud regions and providers — such as, Amazon Web Services (AWS),
  Microsoft Azure, and Google Cloud — by using
  [listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about) and other
  [collaboration features](../guides-overview-sharing).
* Apply consistent
  [security and governance policies across clouds and regions](secure-data-sharing-across-regions-platforms).
* Enable disaster recovery and business continuity capabilities across regions by using
  [replication](replication-intro).

For more information, see [Snowgrid](https://www.snowflake.com/en/product/features/cross-cloud-snowgrid/).

## Connecting to Snowflake[¶](#connecting-to-snowflake "Link to this heading")

Snowflake supports multiple ways for you to connect to the service:

* [Snowsight](ui-snowsight-quick-tour), a web-based UI that you can use to access all aspects of managing
  and using Snowflake can be accessed.
* Command-line clients that you can also use to access all aspects of managing and using Snowflake; for example,
  [Snowflake CLI](../developer-guide/snowflake-cli/index).
* Native APIs that you can use to create and manage Snowflake resources programmatically; for example,
  [Snowflake Python APIs](../developer-guide/snowflake-python-api/snowflake-python-overview) and
  [Snowflake REST APIs](../developer-guide/snowflake-rest-api/snowflake-rest-api).
* [Drivers](../developer-guide/drivers) that other applications can use to connect to Snowflake; for example, JDBC
  and ODBC.
* Native <connectors> that you can use to develop applications for
  connecting to Snowflake; for example, Apache Kafka and Apache Spark.
* [Third-party technologies](ecosystem-all) that you can use to connect applications to Snowflake;
  for example, extract, transform, load (ETL) tools such as Informatica, and business intelligence (BI) tools such as
  ThoughtSpot.

For more information, see [Sign in to Snowflake](connecting).

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

1. [Data platform as a self-managed service](#data-platform-as-a-self-managed-service)
2. [Snowflake architecture](#snowflake-architecture)
3. [Database storage](#database-storage)
4. [Compute](#compute)
5. [Cloud services](#cloud-services)
6. [Integrated features for your workloads](#integrated-features-for-your-workloads)
7. [Data engineering](#data-engineering)
8. [Analytics](#analytics)
9. [AI and ML](#ai-and-ml)
10. [Applications and collaboration](#applications-and-collaboration)
11. [Snowgrid](#snowgrid)
12. [Connecting to Snowflake](#connecting-to-snowflake)