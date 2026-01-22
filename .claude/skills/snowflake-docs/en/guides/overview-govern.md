---
auto_generated: true
description: Snowflake provides industry-leading features that ensure the highest
  levels of governance for your account and users, as well as all the data you store
  and access in Snowflake.
last_scraped: '2026-01-14T16:54:17.649191+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-govern
title: Data Governance in Snowflake | Snowflake Documentation
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

    * Data quality monitoring

      * [Data profile](../user-guide/data-quality-profile.md)
      * [Introduction to DMFs](../user-guide/data-quality-intro.md)
      * [Tutorial: Getting started with DMFs](../user-guide/tutorials/data-quality-tutorial-start.md)
      * [System DMFs](../user-guide/data-quality-system-dmfs.md)
      * [Custom DMFs](../user-guide/data-quality-custom-dmfs.md)
      * [Use DMFs for quality checks](../user-guide/data-quality-working.md)
      * [Monitor quality checks in Snowsight](../user-guide/data-quality-ui-monitor.md)
      * [Notifications for failed quality checks](../user-guide/data-quality-notifications.md)
      * [View DMF results using SQL](../user-guide/data-quality-results.md)
      * [Remediate data quality issues](../user-guide/data-quality-fixing.md)
      * [Track use of DMFs](../user-guide/data-quality-monitor.md)
      * [Access control](../user-guide/data-quality-access-control.md)
    * Object tagging

      * [Introduction](../user-guide/object-tagging/introduction.md)
      * [Tag inheritance](../user-guide/object-tagging/inheritance.md)
      * [Automatic propagation](../user-guide/object-tagging/propagation.md)
      * [Work with object tags](../user-guide/object-tagging/work.md)
      * [Monitor object tags](../user-guide/object-tagging/monitor.md)
      * [Interaction with other features](../user-guide/object-tagging/interaction.md)
    * Sensitive data classification

      * [Introduction](../user-guide/classify-intro.md)
      * [Tutorial: Automatically classify and tag sensitive data](../user-guide/tutorials/sensitive-data-auto-classification.md)
      * [Custom classification](../user-guide/classify-custom.md)
      * [Automatic classification](../user-guide/classify-auto.md)
      * [Manual classification](../user-guide/classify-using.md)
      * [Legacy APIs](../user-guide/classify-classic.md)
    * Data access policies

      * Aggregation Policies

        * [Introduction](../user-guide/aggregation-policies.md)
        * [Entity-Level Privacy](../user-guide/aggregation-policies-entity-privacy.md)
      * Masking Policies

        * [Introduction](../user-guide/security-column-intro.md)
        * [Dynamic Data Masking](../user-guide/security-column-ddm-intro.md)
        * [External Tokenization](../user-guide/security-column-ext-token-intro.md)
        * [Tag-based Masking](../user-guide/tag-based-masking-policies.md)
        * [Advanced](../user-guide/security-column-advanced.md)
      * [Join Policies](../user-guide/join-policies.md)
      * [Projection Policies](../user-guide/projection-policies.md)
      * Row Access Policies

        * [Introduction](../user-guide/security-row-intro.md)
        * [Using Row Access Policies](../user-guide/security-row-using.md)
    * [Data lineage](../user-guide/ui-snowsight-lineage.md)
    * [Access history](../user-guide/access-history.md)
    * [Object dependencies](../user-guide/object-dependencies.md)
27. [Privacy](overview-privacy.md)
29. [Organizations & Accounts](overview-manage.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Data Governance

# Data Governance in Snowflake[¶](#data-governance-in-snowflake "Link to this heading")

Snowflake provides industry-leading features that ensure the highest levels of governance for your account and users, as well as all the data you store and access in Snowflake.

[Data Quality Monitoring and data metric functions](user-guide/data-quality-intro)
:   Allows the monitoring of the state and integrity of your data using system data metric functions and user-defined data metric functions.

[Column-level Security](user-guide/security-column-intro)
:   Allows the application of a masking policy to a column within a table or view.

[Row-level Security](user-guide/security-row-intro)
:   Allows the application of a row access policy to a table or view to determine which rows are visible in the query result.

[Introduction to object tagging](user-guide/object-tagging/introduction)
:   Allows the tracking of sensitive data for compliance, discovery, protection, and resource usage.

[Tag-based masking policies](user-guide/tag-based-masking-policies)
:   Allows protecting column data by assigning a masking policy to a tag and then setting the tag on a database object or the Snowflake
    account.

[Sensitive data classification](user-guide/classify-intro)
:   Allows categorizing potentially personal and/or sensitive data to support compliance and privacy regulations.

[Access History](user-guide/access-history)
:   Allows the auditing of the user access history through the Account Usage [ACCESS\_HISTORY view](sql-reference/account-usage/access_history).

[Object Dependencies](user-guide/object-dependencies)
:   Allows the auditing of how one object references another object by its metadata (e.g. creating a view depends on a table name and column
    names) through the Account Usage [OBJECT\_DEPENDENCIES](sql-reference/account-usage/object_dependencies) view.

Data Governance area in Snowsight
:   Allows using the Governance & security » Tags & policies area to monitor and report on the usage of policies and tags with
    tables, views, and columns using two different interfaces: Dashboard and Tagged Objects. For details, see:

    * [Use Snowsight to set tags](user-guide/object-tagging/work.html#label-object-tagging-assign-ui)
    * [Monitor tags with Snowsight](user-guide/object-tagging/monitor.html#label-object-tagging-snowsight)
    * [Monitor masking policies with Snowsight](user-guide/security-column-intro.html#label-security-column-intro-snowsight)
    * [Monitor row access policies with Snowsight](user-guide/security-row-intro.html#label-security-row-intro-snowsight)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.