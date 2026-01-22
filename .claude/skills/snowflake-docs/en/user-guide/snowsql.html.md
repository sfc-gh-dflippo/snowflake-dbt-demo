---
auto_generated: true
description: Note
last_scraped: '2026-01-14T16:55:38.762370+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowsql.html
title: SnowSQL (CLI client) | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)

   * User interface
   * [Snowsight](ui-snowsight.md)
   * Command-line clients
   * [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
   * [SnowSQL](snowsql.md)

     + [Installing](snowsql-install-config.md)
     + [Configuring](snowsql-config.md)
     + [Connecting](snowsql-start.md)
     + [Using](snowsql-use.md)
     + [Migrating to Snowflake CLI](snowsql-migrate.md)
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

[Guides](../guides/README.md)[Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)SnowSQL

# SnowSQL (CLI client)[¶](#snowsql-cli-client "Link to this heading")

Note

[Snowflake CLI](../developer-guide/snowflake-cli/index) is an open-source command-line tool explicitly designed for developer-centric workloads in addition to SQL operations. Snowflake CLI is a more modern, robust, and efficient CLI client than legacy SnowSQL. Snowflake CLI not only lets you execute SQL commands, but also lets you execute commands for other Snowflake products like Streamlit in Snowflake, Snowpark Container Services, and Snowflake Native App Framework. Snowflake will only add new features and enhancements to Snowflake CLI. Consequently, Snowflake recommends that you begin transitioning from SnowSQL to Snowflake CLI.

To help you with the transition from SnowSQL to Snowflake CLI, see [Migrating from SnowSQL to Snowflake CLI](snowsql-migrate).

As of July 2025, Snowflake will provide support based on the minor releases for SnowSQL, as follows:

> | SnowSQL version | Initial release date | Support end date |
> | --- | --- | --- |
> | 1.2.x | February 02, 2023 | December 19, 2025 |
> | 1.3.x | May 02, 2024 | May 02, 2026 |
> | 1.4.x | May 22, 2025 | May 22, 2027 |

SnowSQL is a legacy command-line client for connecting to Snowflake to execute SQL queries and perform all DDL and DML operations, including loading data into and unloading data out of database tables.

SnowSQL (`snowsql` executable) can be run as an interactive shell or in batch mode through `stdin` or using the `-f` option.

SnowSQL is an example of an application developed using the [Snowflake Connector for Python](../developer-guide/python-connector/python-connector); however, the connector is not a prerequisite for installing SnowSQL. All required software for installing SnowSQL
is bundled in the installers.

Snowflake provides platform-specific versions of SnowSQL for download for the following platforms:

| Operating System | Supported Versions |
| --- | --- |
| Linux | CentOS 7, 8 |
|  | Red Hat Enterprise Linux (RHEL) 7, 8 |
|  | Ubuntu 16.04, 18.04, 20.04 or later |
| macOS | 10.14 or later |
| Microsoft Windows | Microsoft Windows 8 or later |
|  | Microsoft Windows Server 2012, 2016, 2019, 2022 |

## Related videos[¶](#related-videos "Link to this heading")

> Snowflake 101 | SnowSQL

**Next Topics:**

* [Installing SnowSQL](snowsql-install-config)
* [Configuring SnowSQL](snowsql-config)
* [Connecting through SnowSQL](snowsql-start)
* [Using SnowSQL](snowsql-use)

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

1. [Related videos](#related-videos)

Related content

1. [SnowSQL Change Log (Prior to January 2022)](/user-guide/../release-notes/client-change-log-snowsql)
2. [Client versions & support policy](/user-guide/../release-notes/requirements)

Related info

For a tutorial on using SnowSQL, see the following page:

* [Getting Started with SnowSQL](https://quickstarts.snowflake.com/guide/getting_started_with_snowsql/index.html) (Snowflake Quickstarts)