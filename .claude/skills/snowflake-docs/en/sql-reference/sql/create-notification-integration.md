---
auto_generated: true
description: Creates a new notification integration in the account or replaces an
  existing integration. A notification integration is a Snowflake object that provides
  an interface between Snowflake and third-party
last_scraped: '2026-01-14T16:56:03.121405+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-notification-integration
title: CREATE NOTIFICATION INTEGRATION | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)

     + General
     + [CREATE INTEGRATION](create-integration.md)
     + [ALTER INTEGRATION](alter-integration.md)
     + [SHOW INTEGRATIONS](show-integrations.md)
     + [DESCRIBE INTEGRATION](desc-integration.md)
     + [DROP INTEGRATION](drop-integration.md)
     + API
     + [CREATE API INTEGRATION](create-api-integration.md)
     + [ALTER API INTEGRATION](alter-api-integration.md)
     + Catalog
     + [CREATE CATALOG INTEGRATION](create-catalog-integration.md)
     + [ALTER CATALOG INTEGRATION](alter-catalog-integration.md)
     + [DROP CATALOG INTEGRATION](drop-catalog-integration.md)
     + [SHOW CATALOG INTEGRATIONS](show-catalog-integrations.md)
     + [DESCRIBE CATALOG INTEGRATION](desc-catalog-integration.md)
     + External access
     + [CREATE EXTERNAL ACCESS INTEGRATION](create-external-access-integration.md)
     + [ALTER EXTERNAL ACCESS INTEGRATION](alter-external-access-integration.md)
     + Notification
     + [CREATE NOTIFICATION INTEGRATION](create-notification-integration.md)

       - [Azure Event Grid topics (inbound)](create-notification-integration-queue-inbound-azure.md)")
       - [Google Pub/Sub topics (inbound)](create-notification-integration-queue-inbound-gcp.md)")
       - [Amazon SNS topics (outbound)](create-notification-integration-queue-outbound-aws.md)")
       - [Azure Event Grid topics (outbound)](create-notification-integration-queue-outbound-azure.md)")
       - [Google Pub/Sub topics (outbound)](create-notification-integration-queue-outbound-gcp.md)")
       - [Email](create-notification-integration-email.md)
       - [Webhooks](create-notification-integration-webhooks.md)
     + [ALTER NOTIFICATION INTEGRATION](alter-notification-integration.md)
     + [DESCRIBE NOTIFICATION INTEGRATION](desc-notification-integration.md)
     + [SHOW NOTIFICATION INTEGRATIONS](show-notification-integrations.md)
     + Security
     + [CREATE SECURITY INTEGRATION](create-security-integration.md)
     + [ALTER SECURITY INTEGRATION](alter-security-integration.md)
     + [SHOW DELEGATED AUTHORIZATIONS](show-delegated-authorizations.md)
     + Storage
     + [CREATE STORAGE INTEGRATION](create-storage-integration.md)
     + [ALTER STORAGE INTEGRATION](alter-storage-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Integrations](../commands-integration.md)CREATE NOTIFICATION INTEGRATION

# CREATE NOTIFICATION INTEGRATION[¶](#create-notification-integration "Link to this heading")

Creates a new notification integration in the account or replaces an existing integration. A notification integration is a
Snowflake object that provides an interface between Snowflake and third-party messaging services (third-party cloud message
queuing services, email services, webhooks, etc.).

The syntax of the command depends on the type of the messaging service and whether the message is inbound or outbound. The
following topics explain the syntax for creating notification integrations for different use cases:

* [CREATE NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](create-notification-integration-queue-inbound-azure)
* [CREATE NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](create-notification-integration-queue-inbound-gcp)
* [CREATE NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)](create-notification-integration-queue-outbound-aws)
* [CREATE NOTIFICATION INTEGRATION (outbound to an Azure Event Grid topic)](create-notification-integration-queue-outbound-azure)
* [CREATE NOTIFICATION INTEGRATION (outbound to a Google Pub/Sub topic)](create-notification-integration-queue-outbound-gcp)
* [CREATE NOTIFICATION INTEGRATION (email)](create-notification-integration-email)
* [CREATE NOTIFICATION INTEGRATION (webhooks)](create-notification-integration-webhooks)

See also:
:   [ALTER NOTIFICATION INTEGRATION](alter-notification-integration) , [DESCRIBE INTEGRATION](desc-integration) , [DROP INTEGRATION](drop-integration) , [SHOW INTEGRATIONS](show-integrations)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces