---
auto_generated: true
description: There are many ways to share data from your Snowflake account with users
  in other Snowflake accounts, including collaborating with other parties in a secure
  environment.
last_scraped: '2026-01-14T16:54:25.046323+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-sharing
title: Data sharing and collaboration in Snowflake | Snowflake Documentation
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

    * Data Clean Rooms

      * [About clean rooms](../user-guide/cleanrooms/introduction.md)
      * Get started

        * [Introduction](../user-guide/cleanrooms/getting-started.md)
        * [Tutorials, samples, and videos](../user-guide/cleanrooms/tutorials-and-samples.md)
        * [Understanding cost](../user-guide/cleanrooms/cleanroom-cost.md)
        * [Glossary](../user-guide/cleanrooms/dcr-glossary.md)
      * Key concepts

        * [Create, join, drop clean rooms](../user-guide/cleanrooms/manage-clean-rooms.md)
        * [Table policies](../user-guide/cleanrooms/policies.md)
        * [Multistep flows](../user-guide/cleanrooms/multistep-flows.md)
      * Features

        * [Activating results](../user-guide/cleanrooms/activation.md)
        * [Cross-Cloud Auto-Fulfillment](../user-guide/cleanrooms/enabling-laf.md)
        * [Custom functions](../user-guide/cleanrooms/demo-flows/custom-code.md)
        * [Custom SQL queries](../user-guide/cleanrooms/web-app-sql-template.md)
        * [Custom templates](../user-guide/cleanrooms/demo-flows/custom-templates.md)
        * [Differential privacy](../user-guide/cleanrooms/differential-privacy.md)
        * [Managed accounts](../user-guide/cleanrooms/managed-accounts.md)
        * [Security scans](../user-guide/cleanrooms/scan-custom-template.md)
        * [Snowpark in clean rooms](../user-guide/cleanrooms/demo-flows/snowpark.md)
      * Use cases

        * [Consumer-run analysis](../user-guide/cleanrooms/demo-flows/basic-flow-data-analysis.md)
        * [Inventory forecasting](../user-guide/cleanrooms/inventory-forecasting-template.md)
        * [Last touch attribution](../user-guide/cleanrooms/last-touch-template.md)
        * [Lookalike audience modeling](../user-guide/cleanrooms/lookalike-audience-modeling-template.md)
        * [Machine learning](../user-guide/cleanrooms/demo-flows/machine-learning.md)
        * [Multi-provider analysis](../user-guide/cleanrooms/demo-flows/multiprovider.md)
        * [Overlap and segmentation](../user-guide/cleanrooms/demo-flows/basic-flow-overlap.md)
        * [Provider-run analysis](../user-guide/cleanrooms/demo-flows/provider-run-analysis.md)
      * Developers

        * [Clean rooms developer guide](../user-guide/cleanrooms/developer-introduction.md)
        * [Clean rooms API tutorial](../user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic.md)
        * [Provider API reference](../user-guide/cleanrooms/provider.md)
        * [Consumer API reference](../user-guide/cleanrooms/consumer.md)
        * [Custom template reference](../user-guide/cleanrooms/custom-templates.md)
        * [Clean room versioning](../user-guide/cleanrooms/dcr-versions.md)
        * [Template chains](../user-guide/cleanrooms/developer-template-chains.md)
      * Administrators

        * [Installing the clean rooms environment](../user-guide/cleanrooms/installing-dcr.md)
        * [Uninstalling the clean rooms environment](../user-guide/cleanrooms/uninstalling-clean-rooms.md)
        * [Managing users and access](../user-guide/cleanrooms/manage-dcr-users.md)
        * [Registering data](../user-guide/cleanrooms/register-data.md)
        * [Other administrator tasks](../user-guide/cleanrooms/admin-tasks.md)
        * [Installed objects](../user-guide/cleanrooms/installation-details.md)
        * [Update to Snowflake authentication](../user-guide/cleanrooms/update-to-oauth.md)
      * Clean rooms UI

        * [UI overview](../user-guide/cleanrooms/web-app-introduction.md)
        * [UI tour](../user-guide/cleanrooms/ui-tour.md)
        * [UI single-account tutorial](../user-guide/cleanrooms/tutorials/cleanroom-web-app-single-account-tutorial.md)
        * [UI two-account tutorial](../user-guide/cleanrooms/tutorials/cleanroom-web-app-tutorial.md)
        * [Run an analysis in the UI](../user-guide/cleanrooms/web-app-working.md)
        * [Schedule an analysis](../user-guide/cleanrooms/schedule-analysis.md)
      * [Troubleshooting guide](../user-guide/cleanrooms/troubleshooting.md)
      * Third-party connectors

        * Cloud data connectors

          * [Amazon S3](../user-guide/cleanrooms/external-data-aws.md)
          * [Azure Blob Storage](../user-guide/cleanrooms/external-data-azure.md)
          * [Google Cloud Storage](../user-guide/cleanrooms/external-data-gcp.md)
          * [Troubleshooting External Data](../user-guide/cleanrooms/external-data-troubleshoot.md)
        * [Activation connectors](../user-guide/cleanrooms/connector-activation.md)
        * [Identity & data provider connectors](../user-guide/cleanrooms/connector-identity.md)
        * [Third-party clean room connectors](../user-guide/cleanrooms/connector-clean-room.md)
    * [Shares](../user-guide/data-sharing-intro.md)
    * Reader Accounts

      * [Configure a reader account](../user-guide/data-sharing-reader-config.md)
      * [Manage reader accounts](../user-guide/data-sharing-reader-create.md)
    * VPS & Collaboration

      * [About VPS Collaboration](../collaboration/virtual-private-snowflake/about-vps-collaboration.md)
      * [Enabling VPS Private Listings](../collaboration/virtual-private-snowflake/vps-enable-collaboration.md)
      * [Consuming VPS Private Listings](../collaboration/virtual-private-snowflake/vps-collaboration-for-consumers.md)
      * [Providing VPS Private Listings](../collaboration/virtual-private-snowflake/vps-collaboration-for-providers.md)
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

[Guides](README.md)Collaboration

# Data sharing and collaboration in Snowflake[¶](#data-sharing-and-collaboration-in-snowflake "Link to this heading")

There are many ways to share data from your Snowflake account with users in other Snowflake accounts, including collaborating with other
parties in a secure environment.

## Why share data with Snowflake[¶](#why-share-data-with-snowflake "Link to this heading")

When you use Snowflake to share data as a provider, you can manage who has access to your data, and avoid challenges
keeping your data synchronized across different people and groups.

As a data consumer, you can reduce the data transformations you need to perform because the data stays in Snowflake, making it easy to join
datasets shared with you with your own data.

If you share your data using listings, you can include metadata with your data share, such as a title and description, and usage examples to
help consumers use the data quickly. In addition to the benefits for consumers, as a provider you get access to usage data, automatically
replicate your data to other regions, and can even decide to charge for access to your data or offer some datasets publicly
on the Snowflake Marketplace.

## Options for sharing[¶](#options-for-sharing "Link to this heading")

Listings let you share data with people in any Snowflake region, across clouds, without performing manual replication tasks.
If you use listings, you can provide additional metadata for the data that you share, view customer data usage, and for listings
offered publicly on the Snowflake Marketplace, gauge consumer interest in your listings.

If you don’t want to share data using a listing, you can use a direct share instead, see [Secure data sharing](user-guide/data-sharing-intro) and [Non-secure data sharing](user-guide/data-sharing-views). No matter which option you choose, you can share with people
who don’t have Snowflake accounts by using [Reader Accounts](user-guide/data-sharing-reader-create).

| Data Sharing Mechanism | Share With Whom? | Auto-fulfill Across Clouds? | Optionally Charge for Data? | Optionally Offer Data Publicly? | Get Consumer Usage Metrics? |
| --- | --- | --- | --- | --- | --- |
| [Listing](#label-about-listings) | One or more accounts in any region | Yes | Yes | Yes | Yes |
| [Direct share](#label-about-direct-share) | One or more accounts in your region | No | No | No | No |

If you want to manage a group of accounts, and control who can publish and consume listings in that group, consider using a [Data Exchange](#label-about-data-exchange).

## Listing[¶](#listing "Link to this heading")

You can offer a listing privately to specific accounts, or publicly on the Snowflake Marketplace. For more about the Snowflake Marketplace, see
[About Snowflake Marketplace](collaboration/collaboration-marketplace-about).

After you accept the provider and consumer terms, you can start sharing and consuming data shared with you with a listing.
For more information, see [About listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about).

Note

To learn more about sharing listings to or from [Virtual Private Snowflake (VPS)](user-guide/intro-editions.html#label-snowflake-editions-vps),
see [About collaboration in VPS environments](collaboration/virtual-private-snowflake/about-vps-collaboration).

## Direct share[¶](#direct-share "Link to this heading")

Use a direct share to share data with one or more accounts in the same Snowflake region.
You don’t need to copy or move data shared with a direct share.

If you want to convert a direct share with active consumers to a listing, see [Convert a direct share to a listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing#convert-a-direct-share-to-a-private-listing).

For more information, see [Share secure database objects](user-guide/data-sharing-gs).

## Data Exchange[¶](#data-exchange "Link to this heading")

If creating listings that you offer privately to specific accounts isn’t an option, you can use a data exchange to share data with
a selected group of accounts that you invite.

You must request that a data exchange be provisioned and configured for your account, then you can invite members to the exchange
and specify whether they can consume data, provide data, or both.

For more information, see [About Data Exchange](user-guide/data-exchange).

## Collaborating with shared data in a secure environment[¶](#collaborating-with-shared-data-in-a-secure-environment "Link to this heading")

When you use listings, direct shares, and Data Exchange to share data with another party, they can directly access the data. If you want to
share data with other parties, but want to control how that data is accessed, you can use a Snowflake Data Clean Room to collaborate. The
provider who is sharing their data in a clean room defines what analyses can be run against the shared data, which allows the consumer to
gather insights from the data without having unrestricted access to it.

For more information, see [About Snowflake Data Clean Rooms](user-guide/cleanrooms/introduction).

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

1. [Why share data with Snowflake](#why-share-data-with-snowflake)
2. [Options for sharing](#options-for-sharing)
3. [Listing](#listing)
4. [Direct share](#direct-share)
5. [Data Exchange](#data-exchange)
6. [Collaborating with shared data in a secure environment](#collaborating-with-shared-data-in-a-secure-environment)

Related content

1. [Snowflake Marketplace and Listings](/user-guide/data-marketplace)
2. [About Secure Data Sharing](/user-guide/data-sharing-intro)
3. [Share data in non-secured views](/user-guide/data-sharing-views)
4. [About Data Exchange](/user-guide/data-exchange)
5. [Snowflake Data Clean Rooms](https://other-docs.snowflake.com/en/cleanrooms/introduction)