---
auto_generated: true
description: This topic provides the URL and account identifier formats that you use
  to connect to the Snowflake accounts in your organization.
last_scraped: '2026-01-14T16:57:51.198668+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/organizations-connect
title: Connecting to your accounts | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
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

    * Organizations
    * [Introduction](organizations.md)
    * [Organization administrators](organization-administrators.md)
    * [Organization account](organization-accounts.md)
    * [Organization users](organization-users.md)
    * [Managing accounts](organizations-manage-accounts.md)
    * Accounts
    * [Connecting to your accounts](organizations-connect.md)
    * [Account identifiers](admin-account-identifier.md)
    * [Trial accounts](admin-trial-account.md)
    * [Parameter management](admin-account-management.md)
    * [User management](admin-user-management.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Organizations & Accounts](../guides/overview-manage.md)Connecting to your accounts

# Connecting to your accounts[¶](#connecting-to-your-accounts "Link to this heading")

This topic provides the URL and [account identifier](admin-account-identifier) formats that you use to connect to the
Snowflake accounts in your organization.

Note

If you are an organization administrator and want to delete old URLs for an account that has changed, see [Managing account URLs](organizations-manage-accounts-urls).

## Connecting to the Snowflake web interface[¶](#connecting-to-the-snowflake-web-interface "Link to this heading")

To connect to Snowsight using your web browser, see [Signing in to Snowsight](ui-snowsight-gs.html#label-snowsight-getting-started-sign-in).

## Connecting with a URL[¶](#connecting-with-a-url "Link to this heading")

Snowflake supports multiple URL formats when connecting to a Snowflake account without a browser. For example, an identity provider
might use a direct URL to communicate with Snowflake.

* The **account name** format uses the name of the account and its [organization](organizations) to identify the account.
  To find the name of your organization and account, see [Finding the organization and account name for an account](admin-account-identifier.html#label-account-name-find).
* The **connection name** format, which replaces the account name with the name of a connection, is required when using the
  [Client Redirect](client-redirect) feature. To find the name of your connection, execute the
  [SHOW CONNECTIONS](../sql-reference/sql/show-connections) command.
* The legacy **account locator** format is currently supported, but its use is discouraged.

### Standard account URLs[¶](#standard-account-urls "Link to this heading")

The standard URL format can be used in most cases where a Snowflake account URL is required, including:

> * SSO connections ([except Okta](#label-okta-url))
> * SCIM base URL ([except Okta](#label-okta-url))
> * OAuth connections with third-party identity providers ([except Okta](#label-okta-url))
> * OAuth base URL for a Snowflake Authorization Server

The standard URL formats are:

> * Account name: `https://<orgname>-<account_name>.snowflakecomputing.com`
> * Connection name: `https://<orgname>-<connectionname>.snowflakecomputing.com`
> * Account locator (legacy): `https://<accountlocator>.<region>.<cloud>.snowflakecomputing.com`

### Private connectivity URLs[¶](#private-connectivity-urls "Link to this heading")

When connecting to Snowflake using private connectivity to the Snowflake service (e.g. AWS PrivateLink), the string `privatelink` must be
appended to the [account identifier](admin-account-identifier) in the Snowflake account URL.

> * Account Name: `https://<orgname>-<account_name>.privatelink.snowflakecomputing.com`
> * Connection Name: `https://<orgname>-<connectionname>.privatelink.snowflakecomputing.com`
> * Account Locator (legacy): `https://<account_locator>.<region>.privatelink.snowflakecomputing.com`

Note that using private connectivity requires updating DNS records to include the private connectivity URL. For more information, see:

> * [AWS PrivateLink CNAME Records](admin-security-privatelink.html#label-aws-pl-additional-cname-records).
> * Azure Private Link DNS setup in the [configuration procedure](privatelink-azure.html#label-azure-pl-config-procedure).
> * Google Cloud Private Service Connect DNS setup in [Step 8](private-service-connect-google.html#label-gcp-psc-config).

### Okta URLs[¶](#okta-urls "Link to this heading")

When using Okta for SSO, SCIM, or OAuth, you must use a special account name format if the account name contains an underscore. Because
Okta does not support underscores in URLs, the underscore in the account name must be converted to a hyphen.

> * Account name: `https://<orgname>-<account-name>.snowflakecomputing.com`
> * Connection name: Use the standard URL
> * Account locator (legacy): Use the standard URL

## Connecting from clients, connectors, and drivers[¶](#connecting-from-clients-connectors-and-drivers "Link to this heading")

See [Configuring a client, driver, library, or third-party application to connect to Snowflake](gen-conn-config).

## Backwards compatibility[¶](#backwards-compatibility "Link to this heading")

Using the legacy account locator in an account identifier or account URL is still supported, though discouraged.

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

1. [Connecting to the Snowflake web interface](#connecting-to-the-snowflake-web-interface)
2. [Connecting with a URL](#connecting-with-a-url)
3. [Connecting from clients, connectors, and drivers](#connecting-from-clients-connectors-and-drivers)
4. [Backwards compatibility](#backwards-compatibility)

Related content

1. [Account identifiers](/user-guide/admin-account-identifier)
2. [Redirecting client connections](/user-guide/client-redirect)