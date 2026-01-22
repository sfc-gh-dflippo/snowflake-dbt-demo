---
auto_generated: true
description: To download the installation package for a Snowflake client, connector,
  driver, or library, use the download pages in the Snowflake Developer Center.
last_scraped: '2026-01-14T16:57:43.750352+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-client-repository
title: Downloading Snowflake Clients, Connectors, Drivers, and Libraries | Snowflake
  Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)

   * User interface
   * [Snowsight](ui-snowsight.md)
   * Command-line clients
   * [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
   * [SnowSQL](snowsql.md)
   * Extensions for code editors
   * [Visual Studio Code SQL extension](vscode-ext.md)
   * Infrastructure as code
   * [Snowflake Terraform provider](terraform.md)
   * Drivers and libraries
   * [API reference](../api-reference.md)
   * Downloads and configuration
   * [Download clients, drivers, and libraries](snowflake-client-repository.md)
   * [Configure clients, drivers, libraries, and applications to connect to Snowflake](gen-conn-config.md)
   * [Troubleshoot Snowflake client connectivity](client-connectivity-troubleshooting/overview.md)
   * Additional information about clients

     * [View the client version used in a query](snowflake-client-version-check.md)
     * [Limits on query text size](query-size-limits.md)
     * [SQL statements supported for preparation](sql-prepare.md)
   * Third-party software
   * [Ecosystem](ecosystem.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)Download clients, drivers, and libraries

# Downloading Snowflake Clients, Connectors, Drivers, and Libraries[¶](#downloading-snowflake-clients-connectors-drivers-and-libraries "Link to this heading")

To download the installation package for a Snowflake client, connector, driver, or library, use the
[download pages in the Snowflake Developer Center](#label-client-download-developer-center).

If you want to write a script to download clients over HTTP (e.g. using [curl](https://curl.se/)), you can download SnowSQL, the ODBC Driver,
the Snowpark Library, and SnowCD directly from the [Snowflake Client Repository](#label-client-download-repository).

See [Drivers](../developer-guide/drivers) and [Using Snowflake with Kafka and Spark](connectors) for documentation for the drivers and
connectors, respectively. For other developer documentation,
see [Develop Apps and Extensions](https://docs.snowflake.com/developer).

## Snowflake Developer Center Download Pages[¶](#snowflake-developer-center-download-pages "Link to this heading")

To download a Snowflake client, use the following download pages in the [Snowflake Developer Center](https://developers.snowflake.com/):

| Client / Connector / Driver / Library | Download Page |
| --- | --- |
| [Snowflake CLI](../developer-guide/snowflake-cli/index) | [Snowflake CLI Download](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html) |
| [ODBC Driver](../developer-guide/odbc/odbc) | [ODBC Download](https://developers.snowflake.com/odbc/) |
| [Snowpark API](../developer-guide/snowpark/index) | [Snowpark Client Download](https://developers.snowflake.com/snowpark/) |
| [Drivers](../developer-guide/drivers) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) |
| [Scala and Java connectors](connectors) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) |
| [SnowCD](snowcd) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) |
| [Snowpark ML](../developer-guide/snowflake-ml/overview) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) |

## Snowflake Client Repository[¶](#snowflake-client-repository "Link to this heading")

To download SnowSQL, the ODBC Driver, the Snowpark Library, or SnowCD over HTTP programmatically (e.g. using [curl](https://curl.se/)), use the
Snowflake Client Repository. The Snowflake Client Repository serves the packages for these clients through CDN (Content Delivery
Network) using the following endpoints:

> * <https://sfc-repo.azure.snowflakecomputing.com/index.html> (mirror on Azure Blob)

If the endpoint is not specified explicitly, the client upgrader (e.g., the SnowSQL auto-upgrader) uses the AWS endpoint. For instructions on specifying the endpoint, see the installation documentation for the client.

Note

Users can download Snowflake clients from either endpoint regardless of which cloud provider hosts their Snowflake account.

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

1. [Snowflake Developer Center Download Pages](#snowflake-developer-center-download-pages)
2. [Snowflake Client Repository](#snowflake-client-repository)