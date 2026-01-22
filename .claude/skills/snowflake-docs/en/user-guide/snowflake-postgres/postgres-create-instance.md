---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:57:51.521068+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-postgres/postgres-create-instance
title: Creating a Snowflake Postgres Instance | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](about.md)

    * [Creating instances](postgres-create-instance.md)
    * [Connecting](connecting-to-snowflakepg.md)
    * [Managing instances](managing-instances.md)
    * Monitoring
    * [Evaluate cost](postgres-cost.md)
    * [Insights](insights.md)
    * [Logging](postgres-logging.md)
    * Security and networking
    * [Networking](postgres-network.md)
    * [Tri-Secret Secure](postgres-tss.md)
    * Reference
    * [Instance sizes](postgres-instance-sizes.md)
    * [Extensions](postgres-extensions.md)
    * [Server settings](postgres-server-settings.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Snowflake Postgres](about.md)Creating instances

# Creating a Snowflake Postgres Instance[¶](#creating-a-snowflake-postgres-instance "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

## Overview[¶](#overview "Link to this heading")

You can create Snowflake Postgres instances by using either Snowsight or
by executing Snowflake SQL statements. The size of the instance, the storage size, and the Postgres major versions are
configurable when creating an instance. Network policies can also be applied to
instances at creation time.

## Privileges[¶](#privileges "Link to this heading")

To create Snowflake Postgres instances, you must use a role that has been granted
the CREATE POSTGRES INSTANCE privilege on the account. By default, this
privilege is granted to the ACCOUNTADMIN role.

To grant this privilege to other roles, a user with the ACCOUNTADMIN role
can run the [GRANT <privileges> … TO ROLE](../../sql-reference/sql/grant-privilege) command:

```
GRANT CREATE POSTGRES INSTANCE ON ACCOUNT TO your_role;
```

Copy

## Creating a Postgres instance[¶](#creating-a-postgres-instance "Link to this heading")

SnowsightSQL

You can create a Postgres instance by using the Create menu or by using the Create button in the Postgres Instances page.

**Using the main Create menu:**

1. At the top of the navigation menu, select [![Add a dashboard tile](../../_images/snowsight-dashboards-add-tile-icon.png)](../../_images/snowsight-dashboards-add-tile-icon.png) (Create).
2. Select Postgres Instance.
3. Configure your instance.
4. Select Create.

**Using the Create button on the Postgres instances page:**

1. In the navigation menu, select Postgres.
2. In the Postgres Instances page, select the Create button at the top right.
3. Choose your instance configuration.
4. Select Create.

[![Create a Snowflake Postgres instance](../../_images/new-snowflake-postgres-instance.png)](../../_images/new-snowflake-postgres-instance.png)

When you create an instance, the connection details are displayed, including the hostname and credentials needed to connect to
the instance. Save these credentials in a secure location; they will not be shown again. You can regenerate credentials later if
needed.

If you did not select a network policy, you will have the option to configure network settings from the instance details page.
See [Snowflake Postgres networking](postgres-network) for more details.

[![Snowflake Postgres connection reveal](../../_images/snowflake-postgres-snowsight-connection.png)](../../_images/snowflake-postgres-snowsight-connection.png)

Use the CREATE POSTGRES INSTANCE command to create a new Postgres instance. The syntax of this command is shown below:

```
CREATE POSTGRES INSTANCE <name>
  COMPUTE_FAMILY = '<compute_family>'
  STORAGE_SIZE_GB = <storage_gb>
  AUTHENTICATION_AUTHORITY = POSTGRES
  [ POSTGRES_VERSION = { 16 | 17 } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ HIGH_AVAILABILITY = { TRUE | FALSE } ]
  [ POSTGRES_SETTINGS = '<json_string>' ]
  [ COMMENT = '<string_literal>' ];
```

Copy

For the command parameters:

> `COMPUTE_FAMILY = compute_family`
> :   Specifies the name of an instance size from the [Snowflake Postgres Instance Sizes](postgres-instance-sizes) tables.
>
> `STORAGE_SIZE_GB = storage_gb`
> :   Specifies storage size in GB. Must be between 10 and 65,535.
>
> `AUTHENTICATION_AUTHORITY = POSTGRES`
> :   Determines how you authenticate to your instance. Currently, the only available option is `POSTGRES`, but other
>     authentication methods, including `SNOWFLAKE`, might be supported in the future.
>
> `POSTGRES_VERSION = { 16 | 17 }`
> :   Specifies the version of Postgres to use.
>
>     Default: The latest Postgres version.
>
> `NETWORK_POLICY = 'network_policy'`
> :   Specifies the [network policy](postgres-network) to use for the instance. To specify this parameter, you must have been granted the USAGE privilege on the NETWORK\_POLICY object.
>
>     Default: No network policy is applied. A network policy will need to be configured before the instance can be reached. See [Snowflake Postgres networking](postgres-network) for more information.
>
> `HIGH_AVAILABILITY = { TRUE | FALSE }`
> :   Specifies whether to enable high availability for the instance.
>
>     Default: `FALSE`
>
> `POSTGRES_SETTINGS = 'json_string'`
> :   Allows you to optionally set Postgres configuration parameters on your instance in JSON format. See [Snowflake Postgres Server Settings](postgres-server-settings) for a list of available Postgres parameters.
>
>     ```
>     '{"component:name" = "value", ...}'
>     ```
>
>     Copy
>
>     Default: No custom Postgres configuration parameters are set.
>
> `COMMENT = 'string_literal'`
> :   Specifies a comment for the Postgres instance.
>
>     Default: `NULL`

When you create the instance, one row with the following columns is returned:

* `status`
* `host`
* `access_roles`
* `default_database`

The `access_roles` column contains the user name and password for both the `snowflake_admin` and `application` roles. Save these details in a secure location because they cannot be retrieved later.

Creating a new instance will take some time to complete. The instance will display its current
state as it is building. See the list of [instance states](managing-instances.html#instance-states) for
details about the states you will see while instances are being created.

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

1. [Overview](#overview)
2. [Privileges](#privileges)
3. [Creating a Postgres instance](#creating-a-postgres-instance)