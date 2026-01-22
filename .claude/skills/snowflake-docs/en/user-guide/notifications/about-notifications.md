---
auto_generated: true
description: You can configure Snowflake to send notifications to a queue provided
  by a Cloud service (Amazon SNS, Google Cloud PubSub, or Azure Event Grid), an email
  address, or a webhook. For details, see the fo
last_scraped: '2026-01-14T16:57:44.627202+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/notifications/about-notifications
title: Notifications in Snowflake | Snowflake Documentation
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
21. [Snowflake Postgres](../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)

    * [Snowflake Alerts](../alerts.md)
    * [Notifications](about-notifications.md)

      + [Sending a notification to a cloud provider queue](queue-notifications.md)
      + [Sending an email notification](email-notifications.md)
      + [Sending a webhook notification](webhook-notifications.md)
      + [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send a notification](snowflake-notifications.md)
      + [Using SYSTEM$SEND\_EMAIL to send an email notification](email-stored-procedures.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Alerts & Notifications](../../guides/overview-alerts.md)Notifications

# Notifications in Snowflake[¶](#notifications-in-snowflake "Link to this heading")

You can configure Snowflake to send notifications to a queue provided by a Cloud service (Amazon SNS, Google Cloud PubSub, or
Azure Event Grid), an email address, or a webhook. For details, see the following sections:

* [Sending notifications to cloud provider queues (Amazon SNS, Google Cloud PubSub, and Azure Event Grid)](queue-notifications)
* [Sending email notifications](email-notifications)
* [Sending webhook notifications](webhook-notifications)

## Viewing the history of notifications[¶](#viewing-the-history-of-notifications "Link to this heading")

To view the history of notifications, call the Information Schema [NOTIFICATION\_HISTORY](../../sql-reference/functions/notification_history) table
function.

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

1. [Viewing the history of notifications](#viewing-the-history-of-notifications)

Related content

1. [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications)
2. [Snowpipe error notifications](/user-guide/notifications/../data-load-snowpipe-errors)
3. [Enabling notifications for tasks](/user-guide/notifications/../tasks-errors)