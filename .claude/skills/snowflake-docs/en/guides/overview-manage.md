---
auto_generated: true
description: The following topics describe how to manage Snowflake organizations and
  accounts.
last_scraped: '2026-01-14T16:54:23.158363+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-manage
title: Working with organizations and accounts | Snowflake Documentation
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

    * Organizations
    * [Introduction](../user-guide/organizations.md)
    * [Organization administrators](../user-guide/organization-administrators.md)
    * [Organization account](../user-guide/organization-accounts.md)
    * [Organization users](../user-guide/organization-users.md)
    * [Managing accounts](../user-guide/organizations-manage-accounts.md)
    * Accounts
    * [Connecting to your accounts](../user-guide/organizations-connect.md)
    * [Account identifiers](../user-guide/admin-account-identifier.md)
    * [Trial accounts](../user-guide/admin-trial-account.md)
    * [Parameter management](../user-guide/admin-account-management.md)
    * [User management](../user-guide/admin-user-management.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Organizations & Accounts

# Working with organizations and accounts[¶](#working-with-organizations-and-accounts "Link to this heading")

The following topics describe how to manage Snowflake organizations and accounts.

## Organizations[¶](#organizations "Link to this heading")

[Introduction to organizations](user-guide/organizations)
:   Learn about organizations, which link the accounts owned by your business entity. You can find the name of your organization, list the
    accounts in your organization, and change the name of your organization.

[Organization administrators](user-guide/organization-administrators)
:   Learn about the system roles that administrators use to perform organization-level tasks.

[Organization users](user-guide/organization-users)
:   Learn about using organization users for users who need access to multiple accounts within the organization.

[Managing accounts in your organization](user-guide/organizations-manage-accounts)
:   Manage the lifecycle of an account such as creating it and deleting it. Also, manage the general characteristics of an account like
    its Snowflake edition.

[Connecting to your accounts](user-guide/organizations-connect)
:   Connect to accounts in your organization from SnowSQL, connectors, drivers, and through Snowsight.

## Organization accounts[¶](#organization-accounts "Link to this heading")

[Organization accounts](user-guide/organization-accounts)
:   Learn how organization administrators of multi-account organizations use an organization account. Also, use premium views in the
    ORGANIZATION\_USAGE schema to track usage across the organization.

## Accounts[¶](#accounts "Link to this heading")

[Account identifiers](user-guide/admin-account-identifier)
:   Learn how to use account identifiers to specify the account that you are using (e.g. to connect to the account, use
    Snowsight, etc.).

[Trial accounts](user-guide/admin-trial-account)
:   Sign up for a trial account, convert that account to a paid account, and cancel the trial account.

[Parameter management](user-guide/admin-account-management)
:   View and alter parameters for your account.

[User management](user-guide/admin-user-management)
:   Create, modify, view, and drop users in your account.

[Behavior change management](release-notes/bcr-bundles/managing-behavior-change-releases)
:   Enable, disable, and check the status of behavior changes.

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

1. [Organizations](#organizations)
2. [Organization accounts](#organization-accounts)
3. [Accounts](#accounts)