---
auto_generated: true
description: Instructions on performing various Snowflake operations
last_scraped: '2026-01-14T16:54:20.125133+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides
title: User Guides
---

1. [Overview](README.md)
2. [Snowflake Horizon Catalog](../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](overview-connecting.md)
6. [Virtual warehouses](../user-guide/warehouses.md)
7. [Databases, Tables, & Views](overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](overview-loading-data.md)
    - [Dynamic Tables](../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](overview-unloading-data.md)
12. [Storage Lifecycle Policies](../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](overview-sharing.md)
19. [Snowflake AI & ML](overview-ai-features.md)
21. [Snowflake Postgres](../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](overview-alerts.md)
25. [Security](overview-secure.md)
26. [Data Governance](overview-govern.md)
27. [Privacy](overview-privacy.md)
29. [Organizations & Accounts](overview-manage.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

# User Guides

Instructions on performing various Snowflake operations

## Connecting to Snowflake

Snowflake provides a variety of mechanisms for connecting to Snowflake and executing database commands. Choose between the web interface or the command line tool to connect to your Snowflake account. Learn how to use connectors to integrate third-party data into Snowflake.

[See all](overview-connecting.md)

Web Interface

Snowsight distills Snowflake’s powerful SQL support into a unified, easy-to-use experience. Use Snowsight to perform your critical Snowflake operations.

[Learn more](../user-guide/ui-snowsight.md)

Command Line

Detailed instructions for installing, configuring, and using the Snowflake command-line client, snowsql.

[Learn more](../user-guide/snowsql.md)

Connectors

The Snowflake Connectors provide native integration of third-party applications and database systems in Snowflake. The connectors provide instant access to current data without the need to manually integrate against API endpoints.

[Learn more](https://other-docs.snowflake.com/en/connectors)

## Snowflake Fundamentals

Learn the basics of warehouses, tables, and views in Snowflake.

## Snowflake Warehouses

Learn how to set up and use virtual data warehouses to process the SQL statements that you execute.

[Overview of Warehouses](../user-guide/warehouses-overview.md)

[Multi-cluster Warehouses](../user-guide/warehouses-multicluster.md)

[Warehouse Considerations](../user-guide/warehouses-considerations.md)

[Working with Warehouses](../user-guide/warehouses-tasks.md)

[Using the Query Acceleration Service](../user-guide/query-acceleration-service.md)

[See all](../user-guide/warehouses.md)

## Basics of Snowflake Tables and Views

Learn how to design and create tables and views for your data.

[Understanding Snowflake Table Structures](../user-guide/tables-micro-partitions.md)

[Table Design Considerations](../user-guide/table-considerations.md)

[Overview of Views](../user-guide/views-introduction.md)

[Working with Secure Views](../user-guide/views-secure.md)

[Cloning Considerations](../user-guide/object-clone.md)

[Table Storage Considerations](../user-guide/tables-storage-considerations.md)

[See all](overview-db.md)

## Basics of Data Types

Learn about Snowflake data types and their uses

[Introduction to Snowflake Data Types](../sql-reference/intro-summary-data-types.md)

[Numeric Data Types](../sql-reference/data-types-numeric.md)

[String and Binary Data Types](../sql-reference/data-types-text.md)

[Logical Data Types](../sql-reference/data-types-logical.md)

[Date & Time Data Types](../sql-reference/data-types-datetime.md)

[Geospatial Data Types](../sql-reference/data-types-geospatial.md)

[See all](../sql-reference-data-types.md)

## Getting data in to Snowflake

Snowflake provides several different methods to load data in to Snowflake, such as by using Snowpipe, loading from cloud storage, or uploading files using Snowsight.

[![](/images/guides/GettingDataIntoSnowflake1Light.svg)

Understanding Data Loading

Data can be loaded into Snowflake in a number of ways. Learn about data loading concepts, different tasks, tools, and techniques to quickly and easily load data into Snowflake.](/en/guides-overview-loading-data)

[![](/images/guides/GettingDataIntoSnowflake2Light.svg)

Bulk Data Loading

Learn to use the COPY command to load data on-demand directly from an AWS S3 bucket, Google Cloud Share, or a Microsoft Azure storage container into Snowflake.](/en/user-guide/data-load-local-file-system)

[![](/images/guides/GettingDataIntoSnowflake3Light.svg)

Snowpipe

Use Snowflake Snowpipe to load data automatically as it arrives.](/en/user-guide/data-load-snowpipe-intro)

## Working with data

Queries and other standard database features are just the beginning when you work with your data in Snowflake. You also use machine learning functions to analyze data in Snowflake.

[See all](overview-db.md)

Queries

Snowflake supports standard SQL, including a subset of ANSI SQL:1999 and the SQL:2003 analytic extensions. Learn how to use queries to interact with Snowflake using simple queries, joins, and more.

[Learn more](overview-queries.md)

Views, Materialized Views, & Dynamic Tables

Views are just the beginning of how you can examine data. Snowflake provides a number of mechanism for joining data including Materialized Views and Dynamic Tables.

[Learn more](../user-guide/overview-view-mview-dts.md)

Streams and Tasks

Streams and tasks make executing complex task based solutions simple and easy. Streams allow you to track changes to database objects and tasks provide a mechanism to then execute SQL when those events occur.

[Learn more](../user-guide/streams-intro.md)

ML Functions

ML Functions are Snowflake’s intelligent, fully-managed service that enables organizations to quickly analyze data within Snowflake.

[Learn more](overview-ai-features.md)

## Collaborating

Share data and applications with other Snowflake users. Discover and publish listings of data products on the Snowflake Marketplace, share data products privately, or use a direct share to quickly share data with someone in the same region.

[What are listings?

With listings, you can provide data and other information to other Snowflake users, and you can access data and other information shared by Snowflake providers.](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about)

[Becoming a listing provider

Becoming a provider of listings in Snowflake makes it easier to manage sharing from your account to other Snowflake accounts.](https://other-docs.snowflake.com/en/collaboration/provider-becoming)

[Becoming a listing consumer

Get access to data products shared privately or on the Snowflake Marketplace by becoming a consumer of listings.](https://other-docs.snowflake.com/en/collaboration/consumer-becoming)

## More Guides

## Alerts and Notifications

[Setting Up Alerts Based on Data in Snowflake](../user-guide/alerts.md)

[Sending Email Notifications](../user-guide/email-stored-procedures.md)

[See all](overview-alerts.md)

## Security

[Authentication](../user-guide/admin-security-fed-auth-overview.md)

[Access Control](../user-guide/security-access-control-overview.md)

[Encryption key management](../user-guide/security-encryption-manage.md)

[Encryption](../user-guide/security-encryption-end-to-end.md)

[Networking](../user-guide/network-policies.md)

[See all](overview-secure.md)

## Governance and Compliance

[Data Lineage and Dependencies](../user-guide/access-history.md)

[Data Access Policies](../user-guide/security-column-intro.md)

[Data Sensitivity](../user-guide/object-tagging.md)

[Classification](../user-guide/governance-classify-concepts.md)

[Compliance](../user-guide/intro-compliance.md)

[See all](overview-govern.md)

## Privacy

[Aggregation Policies](../user-guide/aggregation-policies.md)

[Projection Policies](../user-guide/projection-policies.md)

[See all](overview-privacy.md)

## Organizations and Accounts

[Organizations](../user-guide/organizations.md)

[Account identifiers](../user-guide/admin-account-identifier.md)

[See all](overview-manage.md)

## Business Continuity & Data Recovery

[Replication & Failover](../user-guide/account-replication-intro.md)

[Client Redirect](../user-guide/client-redirect.md)

[Time Travel](../user-guide/data-time-travel.md)

[Fail-safe](../user-guide/data-failsafe.md)

[See all](../user-guide/replication-intro.md)

## Performance and Cost

[Cost Management](overview-cost.md)

[Query Performance](overview-performance.md)

[See all](overview-performance.md)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.