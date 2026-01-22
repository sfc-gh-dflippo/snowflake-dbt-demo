---
auto_generated: true
description: Feature — Generally Available
last_scraped: '2026-01-14T16:57:42.936862+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-integration/openflow/connectors/mysql/about
title: About Openflow Connector for MySQL | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../about.md)

      * [Set up and access Openflow](../../setup-openflow-roles-login.md)
      * [About Openflow - BYOC Deployments](../../about-byoc.md)
      * [About Openflow - Snowflake Deployments](../../about-spcs.md)
      * Connect your data sources using Openflow connectors

        * [About Openflow connectors](../about-openflow-connectors.md)
        * [About SAP® and Snowflake](../about-sap-snowflake.md)
        * Openflow Connector for Amazon Ads

          * [About the connector](../amazon-ads/about.md)
          * [Set up the connector](../amazon-ads/setup.md)
        * Openflow Connector for Box

          * [About the connector](../box/about.md)
          * [Set up the connector](../box/setup.md)
        * Openflow Connector for Google Ads

          * [About the connector](../google-ads/about.md)
          * [Set up the connector](../google-ads/setup.md)
        * Openflow Connector for Google Drive

          * [About the connector](../google-drive/about.md)
          * [Set up the connector](../google-drive/setup.md)
        * Openflow Connector for Google Sheets

          * [About the connector](../google-sheets/about.md)
          * [Set up the connector](../google-sheets/setup.md)
        * Openflow Connector for Jira Cloud

          * [About the connector](../jira-cloud/about.md)
          * [Set up the connector](../jira-cloud/setup.md)
        * Openflow Connector for Kafka

          * [About the connector](../kafka/about.md)
          * [Set up the connector (core)](../kafka/setup.md)")
          * [Performance tuning](../kafka/performance-tuning.md)
        * Openflow Connector for Kinesis Data Streams

          * [About the connector](../kinesis/about.md)
          * [Set up the connector](../kinesis/setup.md)
        * Openflow Connector for LinkedIn Ads

          * [About the connector](../linkedin-ads/about.md)
          * [Set up the connector](../linkedin-ads/setup.md)
        * Openflow Connector for Meta Ads

          * [About the connector](../meta-ads/about.md)
          * [Set up the connector](../meta-ads/setup.md)
        * Openflow Connector for Microsoft Dataverse

          * [About the connector](../dataverse/about.md)
          * [Set up the connector](../dataverse/setup.md)
        * Openflow Connector for MySQL

          * [About the connector](about.md)
          * [Set up the connector](setup.md)
          * [Set up incremental replication without snapshots](incremental-replication.md)
          * [Maintenance](maintenance.md)
        * Openflow Connector for PostgreSQL

          * [About the connector](../postgres/about.md)
          * [Set up the connector](../postgres/setup.md)
          * [Set up incremental replication without snapshots](../postgres/incremental-replication.md)
          * [Maintenance](../postgres/maintenance.md)
        * Openflow Connector for SharePoint

          * [About the connector](../sharepoint/about.md)
          * [Set up the connector](../sharepoint/setup.md)
        * Openflow Connector for Slack

          * [About the connector](../slack/about.md)
          * [Set up the connector](../slack/setup.md)
        * Openflow Connector for Snowflake to Kafka

          * [About the connector](../snowflake-to-kafka/about.md)
          * [Set up the connector](../snowflake-to-kafka/setup.md)
        * Openflow Connector for SQL Server

          * [About the connector](../sql-server/about.md)
          * [Set up the connector](../sql-server/setup.md)
          * [Set up incremental replication without snapshots](../sql-server/incremental-replication.md)
          * [Maintenance](../sql-server/maintenance.md)
        * Openflow Connector for Workday

          * [About the connector](../workday/about.md)
          * [Set up the connector](../workday/setup.md)
      * [Manage Openflow](../../manage.md)
      * [Monitor Openflow](../../monitor.md)
      * [Troubleshoot Openflow](../../troubleshoot.md)
      * [Processors](../../processors/index.md)
      * [Controller services](../../controllers/index.md)
      * [Version history](../../version-history.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../dynamic-tables-about.md)
    - [Streams and Tasks](../../../../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../migrations/README.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)Data Integration[Snowflake Openflow](../../about.md)Connect your data sources using Openflow connectorsOpenflow Connector for MySQLAbout the connector

# About Openflow Connector for MySQL[¶](#about-mysql "Link to this heading")

[![Snowflake logo in black (no text)](../../../../../_images/logo-snowflake-black.png)](../../../../../_images/logo-snowflake-black.png) Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Snowflake Openflow on BYOC deployments](../../about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](../../../../intro-regions.html#label-na-general-regions)).

[Openflow Snowflake deployments](../../about-spcs) are available to all accounts in AWS and Azure Commercial Regions.

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for MySQL,
its workflow, and limitations.

The Openflow Connector for MySQL connects a MySQL database instance to Snowflake and replicates data from selected tables in near real-time or on a specified schedule.
The connector also creates a log of all data changes, which is available along with the current state of the replicated tables.

Use this connector if you’re looking to do the following:

* CDC replication of MySQL tables into Snowflake for comprehensive, centralized reporting

## How tables are replicated[¶](#how-tables-are-replicated "Link to this heading")

The tables are replicated in the following stages:

1. Schema introspection: The connector discovers the columns in the source table, including the column names and types,
   then validates them against Snowflake’s and the connector’s [Limitations](#limitations). Validation failures cause
   this stage to fail, and the cycle completes. After successful completion of this stage, the connector creates an empty destination table.
2. Snapshot load: The connector copies all data available in the
   source table into the destination table. If this stage fails, then
   no more data is replicated. After successful completion, the data from the source table is available in the destination table.
3. Incremental load: The connector tracks
   changes in the source table and applies those changes to the destination table.
   This process continues until the table is removed from replication. Failure at this stage
   permanently stops replication of the source table, until the issue is resolved.

   Note

   This connector can be configured to immediately start replicating incremental changes for newly added tables,
   bypassing the snapshot load phase. This option is often useful when reinstalling the connector
   in an account where previously replicated data exists and you want to continue replication without having to re-snapshot tables.

   For details on the bypassing snapshot load and using the incremental load process, see [Incremental replication](incremental-replication).

Important

Interim failures, such as connection errors, do not prevent tables from being replicated.
Permanent failures, such as unsupported data types, do prevent tables from being replicated.
If a permanent failure prevents a table from being replicated, remove the table from the list of replicated tables.
After you address the problem that caused the failure, you can add the table back to the list of replicated tables.

## Workflow[¶](#workflow "Link to this heading")

1. A **MySQL database administrator** performs the following tasks:

   > * Configure MySQL replication settings
   > * Create credentials for the connector
   > * (Optionally) Provide the SSL certificate.
2. A **Snowflake account administrator** performs the following tasks:

   1. Creates a service user for the connector, a warehouse for the connector, and a destination database for the replicated data.
   2. Installs the connector.
   3. Specifies the required parameters for the flow template.
   4. Runs the flow. The connector performs the following tasks when run in Openflow:

      1. Creates a schema for journal tables.
      2. Creates the schemas and destination tables matching the source tables configured for replication.
      3. Starts replicating the tables. For details on the replication process, see [How tables are replicated](#how-tables-are-replicated).

## Supported MySQL versions[¶](#supported-mysql-versions "Link to this heading")

The following table lists the tested and officially supported MySQL versions.

|  | 8.0 | 8.4 |
| --- | --- | --- |
| [Standard](https://www.mysql.com/) | Yes | Yes |
| [AWS RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html) | Yes |  |
| [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/Welcome.html) | Yes, as Version 3 |  |
| [GCP Cloud SQL](https://cloud.google.com/sql/mysql?hl=en) | Yes | Yes |
| [Azure Database](https://azure.microsoft.com/en-us/products/mysql/) | Yes | Yes |

## Openflow requirements[¶](#openflow-requirements "Link to this heading")

* The runtime size must be at least Medium. Use a bigger runtime when replicating large data volumes, especially when row sizes are large.
* The connector does not support multi-node Openflow runtimes. Configure the runtime for this connector with Min nodes and Max nodes set to `1`.

## Limitations[¶](#limitations "Link to this heading")

* The connector supports MySQL version 8 or later.
* The connector supports only username and password authentication with MySQL.
* Only database tables containing primary keys can be replicated.
* The connector does not replicate tables with data that exceeds [Snowflake’s type limitations](../../../../../sql-reference/intro-summary-data-types).
* The connector does not replicate columns of types GEOMETRY, GEOMETRYCOLLECTION, LINESTRING, MULTILINESTRING, MULTIPOINT, MULTIPOLYGON, POINT, and POLYGON.
* The connector has the [Group Replication Limitations of MySQL](https://dev.mysql.com/doc/refman/8.4/en/group-replication-limitations.html#group-replication-limitations-transaction-size).
  This means that a single transaction must fit into a binary log message of size no more than 4 GB.
* The connector does not support replicating tables from a reader instance in Amazon Aurora as Aurora reader instances do not maintain their own binary logs.
* The connector supports source table schema changes with the exception of changing primary key definitions and
  changing the precision or the scale of a numeric column.
* The connector does not support re-adding a column after it is dropped.

Note

Limitations affecting certain table columns can be bypassed by excluding these specific columns from replication.

## Next steps[¶](#next-steps "Link to this heading")

[Set up the Openflow Connector for MySQL](setup)

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

1. [How tables are replicated](#how-tables-are-replicated)
2. [Workflow](#workflow)
3. [Supported MySQL versions](#supported-mysql-versions)
4. [Openflow requirements](#openflow-requirements)
5. [Limitations](#limitations)
6. [Next steps](#next-steps)

Related content

1. [About Openflow](/user-guide/data-integration/openflow/connectors/mysql/../../about)
2. [Manage Openflow](/user-guide/data-integration/openflow/connectors/mysql/../../manage)
3. [Openflow connectors](/user-guide/data-integration/openflow/connectors/mysql/../about-openflow-connectors)
4. [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup)