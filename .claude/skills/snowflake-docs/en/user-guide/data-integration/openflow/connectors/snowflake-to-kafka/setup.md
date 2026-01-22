---
auto_generated: true
description: Preview Feature
last_scraped: '2026-01-14T16:57:42.685624+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/setup
title: Set up the Openflow Connector for Snowflake to Kafka | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../about.md)

      * [Set up and access Openflow](../../setup-openflow-roles-login.md)
      * [About Openflow - BYOC Deployments](../../about-byoc.md)
      * [About Openflow - Snowflake Deployments](../../about-spcs.md)
      * Connect your data sources using Openflow connectors

        * [About Openflow connectors](../about-openflow-connectors.md)
        * [About SAP® and Snowflake](../about-sap-snowflake.md)
        * Openflow Connector for Amazon Ads

          * [About the connector](../amazon-ads/about.md)
          * [Set up the connector](../amazon-ads/setup.md)
        * Openflow Connector for Box

          * [About the connector](../box/about.md)
          * [Set up the connector](../box/setup.md)
        * Openflow Connector for Google Ads

          * [About the connector](../google-ads/about.md)
          * [Set up the connector](../google-ads/setup.md)
        * Openflow Connector for Google Drive

          * [About the connector](../google-drive/about.md)
          * [Set up the connector](../google-drive/setup.md)
        * Openflow Connector for Google Sheets

          * [About the connector](../google-sheets/about.md)
          * [Set up the connector](../google-sheets/setup.md)
        * Openflow Connector for Jira Cloud

          * [About the connector](../jira-cloud/about.md)
          * [Set up the connector](../jira-cloud/setup.md)
        * Openflow Connector for Kafka

          * [About the connector](../kafka/about.md)
          * [Set up the connector (core)](../kafka/setup.md)")
          * [Performance tuning](../kafka/performance-tuning.md)
        * Openflow Connector for Kinesis Data Streams

          * [About the connector](../kinesis/about.md)
          * [Set up the connector](../kinesis/setup.md)
        * Openflow Connector for LinkedIn Ads

          * [About the connector](../linkedin-ads/about.md)
          * [Set up the connector](../linkedin-ads/setup.md)
        * Openflow Connector for Meta Ads

          * [About the connector](../meta-ads/about.md)
          * [Set up the connector](../meta-ads/setup.md)
        * Openflow Connector for Microsoft Dataverse

          * [About the connector](../dataverse/about.md)
          * [Set up the connector](../dataverse/setup.md)
        * Openflow Connector for MySQL

          * [About the connector](../mysql/about.md)
          * [Set up the connector](../mysql/setup.md)
          * [Set up incremental replication without snapshots](../mysql/incremental-replication.md)
          * [Maintenance](../mysql/maintenance.md)
        * Openflow Connector for PostgreSQL

          * [About the connector](../postgres/about.md)
          * [Set up the connector](../postgres/setup.md)
          * [Set up incremental replication without snapshots](../postgres/incremental-replication.md)
          * [Maintenance](../postgres/maintenance.md)
        * Openflow Connector for SharePoint

          * [About the connector](../sharepoint/about.md)
          * [Set up the connector](../sharepoint/setup.md)
        * Openflow Connector for Slack

          * [About the connector](../slack/about.md)
          * [Set up the connector](../slack/setup.md)
        * Openflow Connector for Snowflake to Kafka

          * [About the connector](about.md)
          * [Set up the connector](setup.md)
        * Openflow Connector for SQL Server

          * [About the connector](../sql-server/about.md)
          * [Set up the connector](../sql-server/setup.md)
          * [Set up incremental replication without snapshots](../sql-server/incremental-replication.md)
          * [Maintenance](../sql-server/maintenance.md)
        * Openflow Connector for Workday

          * [About the connector](../workday/about.md)
          * [Set up the connector](../workday/setup.md)
      * [Manage Openflow](../../manage.md)
      * [Monitor Openflow](../../monitor.md)
      * [Troubleshoot Openflow](../../troubleshoot.md)
      * [Processors](../../processors/index.md)
      * [Controller services](../../controllers/index.md)
      * [Version history](../../version-history.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../dynamic-tables-about.md)
    - [Streams and Tasks](../../../../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../migrations/README.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)Data Integration[Snowflake Openflow](../../about.md)Connect your data sources using Openflow connectorsOpenflow Connector for Snowflake to KafkaSet up the connector

# Set up the Openflow Connector for Snowflake to Kafka[¶](#set-up-the-sf-kafka "Link to this heading")

[![Snowflake logo in black (no text)](../../../../../_images/logo-snowflake-black.png)](../../../../../_images/logo-snowflake-black.png) [Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Snowflake Openflow on BYOC deployments](../../about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](../../../../intro-regions.html#label-na-general-regions)).

[Openflow Snowflake deployments](../../about-spcs) are available to all accounts in AWS and Azure Commercial Regions.

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Snowflake to Kafka.

## Prerequisites[¶](#prerequisites "Link to this heading")

1. Ensure that you have reviewed [About Openflow Connector for Snowflake to Kafka](about).
2. Ensure that you have [Set up Openflow - BYOC](../../setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](../../setup-openflow-spcs).
3. Create a Snowflake stream that will be queried for the changes.
4. Create a Kafka topic that will receive CDC messages from the Snowflake stream.

## Set up Snowflake account[¶](#set-up-snowflake-account "Link to this heading")

As a Snowflake account administrator, perform the following tasks:

1. Create the database, source table, and the stream object that the connector will use for reading CDC events. For example:

   ```
   create database stream_db;
   use database stream_db;
   create table stream_source (user_id varchar, data varchar);
   create stream stream_on_table on table stream_source;
   ```

   Copy
2. Create a new role or use an existing role, and grant the SELECT privilege on the stream
   and the source object for the stream. The connector will also need the USAGE privilege on the database and
   schema containing the stream and source object for the stream. For example:

   ```
   create role stream_reader;
   grant usage on database stream_db to role stream_reader;
   grant usage on schema stream_db.public to role stream_reader;
   grant select on stream_source to role stream_reader;
   grant select on stream_on_table to role stream_reader;
   ```

   Copy
3. Create a new Snowflake service user with the type as [SERVICE](../../../../../sql-reference/sql/create-user.html#label-user-type-property). For example:

   ```
   create user stream_user type = service;
   ```

   Copy
4. Grant the Snowflake service user the role you created in the previous steps. For example:

   ```
   grant role stream_reader to user stream_user;
   ```

   Copy
5. Configure with [key-pair auth](../../../../key-pair-auth) for the Snowflake SERVICE user from step 3.
6. Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, for example, AWS, Azure, and Hashicorp,
   and store the public and private keys in the secret store. However, note that the private key generated in step 4 can be used
   directly as a configuration parameter for the connector configuration. In such a case, the private key is stored in Openflow runtime configuration.

   Note

   If for any reason, you do not wish to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you the
      EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right.
      Navigate to Controller Settings » Parameter Provider and then fetch your parameter values.
   3. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
7. Designate a warehouse for the connector to use. One connector can replicate single table to a single Kafka Topic.
   For this kind of processing, you can select the smallest warehouse.

## Set up the connector[¶](#set-up-the-connector "Link to this heading")

As a data engineer, perform the following tasks to install and configure a connector:

1. Navigate to the Openflow Overview page. In the Featured connectors section, select View more connectors.
2. On the Openflow connectors page, find and choose the connector depending on what kind of Kafka broker instance the connector should communicate with.

   * mTLS version: Choose this connector if you are using the SSL (mutual TLS) security protocol, or if you are using
     the SASL\_SSL protocol and connecting to the broker that is using self-signed certificates.
   * SASL version: Choose this connector if you are using any other security protocol
3. Select Add to runtime.
4. In the Select runtime dialog, select your runtime from the Available runtimes drop-down list.
5. Select Add.
6. Authenticate to the deployment with your Snowflake account credentials and select Allow when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
7. Authenticate to the runtime with your Snowflake account credentials.

   The Openflow canvas appears with the connector process group added to it.
8. Right-click on the imported process group and select Parameters.
9. Populate the required parameter values as described in [Flow parameters](#flow-parameters).

### Flow parameters[¶](#flow-parameters "Link to this heading")

This section describes the flow parameters that you can configure based on the following parameter contexts:

* [Kafka Sink Source Parameters](#kafka-sink-source-parameters)
* [Kafka Sink Destination Parameters](#kafka-sink-destination-parameters)
* [Kafka Sink Ingestion Parameters](#kafka-sink-ingestion-parameters)

#### Kafka Sink Source Parameters[¶](#kafka-sink-source-parameters "Link to this heading")

| Parameter | Description | Required |
| --- | --- | --- |
| Snowflake Account Identifier | When using:   * **Session Token Authentication Strategy**: Must be blank. * **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name] where data will be persisted. | Yes |
| Snowflake Authentication Strategy | When using:   * **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_SESSION\_TOKEN.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [runtime roles](../../setup-openflow-byoc.html#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_SESSION\_TOKEN. * **BYOC:** Alternatively BYOC can use KEY\_PAIR as the value for authentication strategy. | Yes |
| Source Database | Source database. This database should contain the Snowflake Stream object that will be consumed. | Yes |
| Snowflake Private Key Password | When using:   * **Session Token Authentication Strategy**: Must be blank. * **KEY\_PAIR**: Provide the password associated with the Snowflake Private Key File. | No |
| Snowflake Role | When using   * **Session Token Authentication Strategy**: Use your Snowflake Role.   You can find your Snowflake Role in the Openflow UI, by navigating to View Details for your Runtime. * **KEY\_PAIR** Authentication Strategy: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   * **Session Token Authentication Strategy**: Must be blank. * **KEY\_PAIR**: Provide the user name used to connect to the Snowflake instance. | Yes |
| Snowflake Private Key | Leave this blank when using Session Token for your Authentication Strategy. When using KEY\_PAIR, provide the RSA private key used for authentication. The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either Snowflake Private Key File or Snowflake Private Key must be defined. | Yes |
| Snowflake Private Key File | Leave this blank when using Session Token for your Authentication Strategy. When using KEY\_PAIR, upload the file that contains the RSA Private Key used for authentication to Snowflake, formatted according to PKCS8 standards and having standard PEM headers and footers. The header line begins with `-----BEGIN PRIVATE`. Select the Reference asset checkbox to upload the private key file. | No |
| Source Schema | The source schema. This schema should contain Snowflake Stream object that will be consumed. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries | Yes |

#### Kafka Sink Destination Parameters[¶](#kafka-sink-destination-parameters "Link to this heading")

| Parameter | Description | Required |
| --- | --- | --- |
| Kafka Bootstrap Servers | A comma-separated list of Kafka brokers to send data to. | Yes |
| Kafka SASL Mechanism | SASL mechanism used for authentication. Corresponds to the Kafka Client `sasl.mechanism` property. Possible values:   * `PLAIN` * `SCRAM-SHA-256` * `SCRAM-SHA-512` * `AWS_MSK_IAM` | Yes |
| Kafka SASL Username | The username to authenticate to Kafka | Yes |
| Kafka SASL Password | The password to authenticate to Kafka | Yes |
| Kafka Security Protocol | Security protocol used to communicate with brokers. Corresponds to the Kafka Client `security.protocol` property. Possible values:   * `PLAINTEXT` * `SASL_PLAINTEXT` * `SASL_SSL` * `SSL` | Yes |
| Kafka Topic | The Kafka topic, where CDCs from Snowflake Stream will be sent | Yes |
| Kafka Message Key Field | Specify the database column name that will be used as the Kafka message key. If not specified, the message key will not be set. If specified, the value of this column will be used as a message key. The value of this parameter is case-sensitive. | No |
| Kafka Keystore Filename | A full path to a keystore storing a client key and certificate for mTLS authentication method. Required for mTLS authentication and when the security protocol is SSL. | No |
| Kafka Keystore Type | The type of keystore. Required for mTLS authentication. Possible values:   * `PKCS12` * `JKS` * `BCFKS` | No |
| Kafka Keystore Password | The password used to secure keystore file. | No |
| Kafka Key Password | A password for the private key stored in the keystore. Required for mTLS authentication. | No |
| Kafka Truststore Filename | A full path to a truststore storing broker certificates. The client will use the certificate from this truststore to verify broker identity. | No |
| Kafka Truststore Type | The type of truststore file. Possible values:   * `PKCS12` * `JKS` * `BCFKS` | No |
| Kafka Truststore Password | A password for the truststore file. | No |

#### Kafka Sink Ingestion Parameters[¶](#kafka-sink-ingestion-parameters "Link to this heading")

| Parameter | Description | Required |
| --- | --- | --- |
| Snowflake FQN Stream Name | Fully qualified Snowflake stream name. | Yes |

## Run the flow[¶](#run-the-flow "Link to this heading")

1. Right-click on the plane and select Enable all Controller Services.
2. Right-click on the imported process group and select Start. The connector starts the data ingestion.

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

1. [Prerequisites](#prerequisites)
2. [Set up Snowflake account](#set-up-snowflake-account)
3. [Set up the connector](#set-up-the-connector)
4. [Run the flow](#run-the-flow)

Related content

1. [About Openflow](/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/../../about)
2. [Manage Openflow](/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/../../manage)
3. [Openflow connectors](/user-guide/data-integration/openflow/connectors/snowflake-to-kafka/../about-openflow-connectors)