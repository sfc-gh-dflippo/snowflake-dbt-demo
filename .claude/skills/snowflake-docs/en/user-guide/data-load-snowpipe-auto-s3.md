---
auto_generated: true
description: This topic provides instructions for triggering Snowpipe data loads from
  external stages on S3 automatically using Amazon SQS (Simple Queue Service) notifications
  for an S3 bucket.
last_scraped: '2026-01-14T16:54:49.696322+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-s3
title: Automating Snowpipe for Amazon S3 | Snowflake Documentation
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

      * [Overview](data-load-overview.md)
      * [Feature summary](intro-summary-loading.md)
      * [Considerations](data-load-considerations.md)
      * [Preparing to load data](data-load-prepare.md)
      * [Staging files using Snowsight](data-load-local-file-system-stage-ui.md)
      * [Loading data using the web interface](data-load-web-ui.md)
      * [Monitor data loading activity](data-load-monitor.md)
      * Bulk Loading
      * [Local File System](data-load-local-file-system.md)
      * [Amazon S3](data-load-s3.md)
      * [Google Cloud Storage](data-load-gcs.md)
      * [Microsoft Azure](data-load-azure.md)
      * [Troubleshooting](data-load-bulk-ts.md)
      * Snowpipe
      * [Overview](data-load-snowpipe-intro.md)
      * [Auto Ingest](data-load-snowpipe-auto.md)

        + [Automating for Amazon S3](data-load-snowpipe-auto-s3.md)
        + [Automating for Google Cloud Storage](data-load-snowpipe-auto-gcs.md)
        + [Automating for Microsoft Azure](data-load-snowpipe-auto-azure.md)
      * [REST Endpoints](data-load-snowpipe-rest-overview.md)
      * [Error Notifications](data-load-snowpipe-errors.md)
      * [Troubleshooting](data-load-snowpipe-ts.md)
      * [Managing](data-load-snowpipe-manage.md)
      * [Monitoring Events for Snowpipe](data-load-snowpipe-monitor-events.md)
      * [Managing Snowpipe in Snowsight](data-load-snowpipe-snowsight.md)
      * [Snowpipe Costs](data-load-snowpipe-billing.md)
      * Snowpipe Streaming
      * [Overview](snowpipe-streaming/data-load-snowpipe-streaming-overview.md)
      * [High-performance Architecture](snowpipe-streaming/snowpipe-streaming-high-performance-overview.md)
      * [Classic Architecture](snowpipe-streaming/snowpipe-streaming-classic-overview.md)
      * Semi-Structured Data
      * [Introduction](semistructured-intro.md)
      * [Supported Formats](semistructured-data-formats.md)
      * [Considerations](semistructured-considerations.md)
      * Unstructured Data
      * [Introduction](unstructured-intro.md)
      * [Directory Tables](data-load-dirtables.md)
      * [REST API](data-load-unstructured-rest-api.md)
      * [Processing with UDF and Procedure Handlers](unstructured-data-java.md)
      * [Sharing](unstructured-data-sharing.md)
      * [Troubleshooting](unstructured-ts.md)
      * [Loading Unstructured Data with Document AI](data-load-unstructured-data.md)
      * Accessing Data in Other Storage
      * [Amazon S3-compatible Storage](data-load-s3-compatible-storage.md)
      * Querying and Transforming Data
      * [Querying Data in Staged Files](querying-stage.md)
      * [Querying Metadata for Staged Files](querying-metadata.md)
      * [Transforming Data During Load](data-load-transform.md)
      * [Evolving Table Schema Automatically](data-load-schema-evolution.md)
      * Integrate Snowflake into external applications
      * Snowflake Connector for Microsoft Power Apps

        * [About the connector](../connectors/microsoft/powerapps/about.md)
        * [Tasks](../connectors/microsoft/powerapps/tasks.md)
      * Loading data from third-party systems
      * [Loading data using Native Applications](https://other-docs.snowflake.com/en/connectors "Loading data using Native Applications")
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

[Guides](../guides/README.md)Data engineering[Data loading](../guides/overview-loading-data.md)[Auto Ingest](data-load-snowpipe-auto.md)Automating for Amazon S3

# Automating Snowpipe for Amazon S3[¶](#automating-snowpipe-for-amazon-s3 "Link to this heading")

This topic provides instructions for triggering Snowpipe data loads from external stages on S3 automatically using [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket.

Snowflake recommends that you only send supported events for Snowpipe to reduce costs, event noise, and latency.

## Cloud platform support[¶](#cloud-platform-support "Link to this heading")

Triggering automated Snowpipe data loads using S3 event messages is supported by Snowflake accounts hosted on [all supported cloud platforms](intro-cloud-platforms).

## Network traffic[¶](#network-traffic "Link to this heading")

Note to [Virtual Private Snowflake (VPS)](intro-editions) and [AWS PrivateLink](admin-security-privatelink) customers:

Automating Snowpipe using Amazon SQS notifications works well. However, although AWS cloud storage within a VPC (including VPS) can communicate with its own messaging services (Amazon SQS, Amazon Simple Notification Service), this traffic flows between servers on Amazon’s secure network outside of the VPC; therefore, this traffic is not protected by the VPC.

## Configuring secure access to Cloud Storage[¶](#configuring-secure-access-to-cloud-storage "Link to this heading")

Note

If you have already configured secure access to the S3 bucket that stores your data files, you can skip this section.

This section describes how to use storage integrations to allow Snowflake to read data from and write data to an Amazon S3 bucket referenced in an external (i.e. S3) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as secret keys or access tokens. Integration objects store an AWS identity and access management (IAM) user ID. An administrator in your organization grants the integration IAM user permissions in the AWS account.

An integration can also list buckets (and optional paths) that limit the locations users can specify when creating external stages that use the integration.

Note

* Completing the instructions in this section requires permissions in AWS to create and manage IAM policies and roles. If you are not an AWS administrator, ask your AWS administrator to perform these tasks.
* Note that currently, accessing S3 storage in [government regions](intro-regions.html#label-us-gov-regions)
  using a storage integration is limited to Snowflake accounts hosted on AWS in the same government
  region. Accessing your S3 storage from an account hosted outside of the government region using
  direct credentials is supported.

The following diagram shows the integration flow for a S3 stage:

[![Amazon S3 Stage Integration Flow](../_images/storage-integration-s3.png)](../_images/storage-integration-s3.png)

1. An external (i.e. S3) stage references a storage integration object in its definition.
2. Snowflake automatically associates the storage integration with a S3 IAM user created for your account. Snowflake creates a single IAM user that is referenced by all S3 storage integrations in your Snowflake account.
3. An AWS administrator in your organization grants permissions to the IAM user to access the bucket referenced in the stage definition. Note that many external stage objects can reference different buckets and paths and use the same storage integration for authentication.

When a user loads or unloads data from or to a stage, Snowflake verifies the permissions granted to the IAM user on the bucket before allowing or denying access.

Note

We highly recommend this option, which avoids the need to supply IAM credentials when accessing cloud storage. See [Configuring secure access to Amazon S3](data-load-s3-config) for additional storage access options.

### Step 1: Configure access permissions for the S3 bucket[¶](#step-1-configure-access-permissions-for-the-s3-bucket "Link to this heading")

#### AWS access control requirements[¶](#aws-access-control-requirements "Link to this heading")

Snowflake requires the following permissions on an S3 bucket and folder to be able to access files in the folder (and sub-folders):

* `s3:GetBucketLocation`
* `s3:GetObject`
* `s3:GetObjectVersion`
* `s3:ListBucket`

As a best practice, Snowflake recommends creating an IAM policy for Snowflake access to the S3 bucket. You can then attach the policy to
the role and use the security credentials generated by AWS for the role to access files in the bucket.

#### Creating an IAM policy[¶](#creating-an-iam-policy "Link to this heading")

The following step-by-step instructions describe how to configure access permissions for Snowflake in your AWS Management Console to access
your S3 bucket.

1. Log into the AWS Management Console.
2. From the home dashboard, search for and select IAM.
3. From the left-hand navigation pane, select Account settings.
4. Under Security Token Service (STS) in the Endpoints list, find the Snowflake
   [region](intro-regions) where your account is located. If the STS status is inactive,
   move the toggle to Active.
5. From the left-hand navigation pane, select Policies.
6. Select Create Policy.
7. For Policy editor, select JSON.
8. Add a policy document that will allow Snowflake to access the S3 bucket and folder.

   The following policy (in JSON format) provides Snowflake with the required permissions to load or unload data using a single bucket and
   folder path.

   Copy and paste the text into the policy editor:

   Note

   * Make sure to replace `bucket` and `prefix` with your actual bucket name and folder path prefix.
   * The Amazon Resource Names (ARN) for buckets in
     [government regions](intro-regions.html#label-us-gov-regions) have a `arn:aws-us-gov:s3:::` prefix.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                 "s3:GetObject",
                 "s3:GetObjectVersion"
               ],
               "Resource": "arn:aws:s3:::<bucket>/<prefix>/*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "s3:ListBucket",
                   "s3:GetBucketLocation"
               ],
               "Resource": "arn:aws:s3:::<bucket>",
               "Condition": {
                   "StringLike": {
                       "s3:prefix": [
                           "<prefix>/*"
                       ]
                   }
               }
           }
       ]
   }
   ```

   Copy

   Note

   Setting the `"s3:prefix":` condition to either `["*"]` or `["<path>/*"]` grants access to all prefixes in the
   specified bucket or path in the bucket, respectively.

   Note that AWS policies support a variety of different security use cases.
9. Select Next.
10. Enter a Policy name (for example, `snowflake_access`) and an optional Description.
11. Select Create policy.

### Step 2: Create the IAM role in AWS[¶](#step-2-create-the-iam-role-in-aws "Link to this heading")

To configure access permissions for Snowflake in the AWS Management Console, do the following:

1. From the left-hand navigation pane in the Identity and Access Management (IAM) Dashboard, select Roles.
2. Select Create role.
3. Select AWS account as the trusted entity type.
4. Select Another AWS account

   > [![Select trusted entity page in AWS Management Console](../_images/iam-role-select-trusted-entity.png)](../_images/iam-role-select-trusted-entity.png)
5. In the Account ID field, enter your own AWS account ID temporarily. Later, you modify the trust relationship and grant
   access to Snowflake.
6. Select the Require external ID option. An external ID is used to grant access to your AWS resources
   (such as S3 buckets) to a third party like Snowflake.

   Enter a placeholder ID such as `0000`.
   In a later step, you will modify the trust relationship for your IAM role and specify the external ID for your storage integration.
7. Select Next.
8. Select the policy you created in [Step 1: Configure access permissions for the S3 bucket](#step-1-configure-access-permissions-for-the-s3-bucket) (in this topic).
9. Select Next.

   > [![Review Page in AWS Management Console](../_images/iam-role-review.png)](../_images/iam-role-review.png)
10. Enter a name and description for the role, then select Create role.

    You have now created an IAM policy for a bucket, created an IAM role, and attached the policy to the role.
11. On the role summary page, locate and record the Role ARN value. In the next step, you will create a Snowflake integration that
    references this role.

Note

Snowflake caches the temporary credentials for a period that cannot exceed the 60-minute expiration time. If you revoke access from
Snowflake, users might be able to list files and access data from the cloud storage location until the cache expires.

### Step 3: Create a cloud storage integration in Snowflake[¶](#step-3-create-a-cloud-storage-integration-in-snowflake "Link to this heading")

Create a storage integration using the [CREATE STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration) command. A storage integration is a Snowflake
object that stores a generated identity and access management (IAM) user for your S3 cloud storage, along with an optional set of allowed
or blocked storage locations (that is, buckets). Cloud provider administrators in your organization grant permissions on the storage locations
to the generated user. This option allows users to avoid supplying credentials when creating stages or loading data.

A single storage integration can support multiple external (that is, S3) stages. The URL in the stage definition must align with the S3
buckets (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this
SQL command.

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<iam_role>'
  STORAGE_ALLOWED_LOCATIONS = ('<protocol>://<bucket>/<path>/', '<protocol>://<bucket>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('<protocol>://<bucket>/<path>/', '<protocol>://<bucket>/<path>/') ]
```

Copy

Where:

* `integration_name` is the name of the new integration.
* `iam_role` is the Amazon Resource Name (ARN) of the role you created in [Step 2: Create the IAM role in AWS](#step-2-create-the-iam-role-in-aws) (in this topic).
* `protocol` is one of the following:

  + `s3` refers to S3 storage in public AWS regions outside of China.
  + `s3china` refers to S3 storage in public AWS regions in China.
  + `s3gov` refers to S3 storage in [government regions](intro-regions.html#label-us-gov-regions).
* `bucket` is the name of a S3 bucket that stores your data files (for example, `mybucket`). The required STORAGE\_ALLOWED\_LOCATIONS
  parameter and optional STORAGE\_BLOCKED\_LOCATIONS parameter restrict or block access to these buckets, respectively, when stages that
  reference this integration are created or modified.
* `path` is an optional path that can be used to provide granular control over objects in the bucket.

The following example creates an integration that allows access to all buckets in the account but blocks access to the defined `sensitivedata` folders.

Additional external stages that also use this integration can reference the allowed buckets and paths:

```
CREATE STORAGE INTEGRATION s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
  STORAGE_ALLOWED_LOCATIONS = ('*')
  STORAGE_BLOCKED_LOCATIONS = ('s3://mybucket1/mypath1/sensitivedata/', 's3://mybucket2/mypath2/sensitivedata/');
```

Copy

Note

Optionally, use the [STORAGE\_AWS\_EXTERNAL\_ID](../sql-reference/sql/create-storage-integration.html#label-create-storage-integration-aws-ext-id) parameter to specify
your own external ID. You might choose this option
to use the same external ID across multiple external volumes and/or storage integrations.

### Step 4: Retrieve the AWS IAM user for your Snowflake account[¶](#step-4-retrieve-the-aws-iam-user-for-your-snowflake-account "Link to this heading")

1. To retrieve the ARN for the IAM user that was created automatically for your Snowflake account, use the [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration).

   ```
   DESC INTEGRATION <integration_name>;
   ```

   Copy

   Where:

   * `integration_name` is the name of the integration you created in [Step 3: Create a Cloud Storage Integration in Snowflake](#step-3-create-a-cloud-storage-integration-in-snowflake)
     (in this topic).

   For example:

   ```
   DESC INTEGRATION s3_int;
   ```

   Copy

   ```
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------+
   | property                  | property_type | property_value                                                                 | property_default |
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------|
   | ENABLED                   | Boolean       | true                                                                           | false            |
   | STORAGE_ALLOWED_LOCATIONS | List          | s3://mybucket1/mypath1/,s3://mybucket2/mypath2/                                | []               |
   | STORAGE_BLOCKED_LOCATIONS | List          | s3://mybucket1/mypath1/sensitivedata/,s3://mybucket2/mypath2/sensitivedata/    | []               |
   | STORAGE_AWS_IAM_USER_ARN  | String        | arn:aws:iam::123456789001:user/abc1-b-self1234                                 |                  |
   | STORAGE_AWS_ROLE_ARN      | String        | arn:aws:iam::001234567890:role/myrole                                          |                  |
   | STORAGE_AWS_EXTERNAL_ID   | String        | MYACCOUNT_SFCRole=2_a123456/s0aBCDEfGHIJklmNoPq=                               |                  |
   +---------------------------+---------------+--------------------------------------------------------------------------------+------------------+
   ```
2. Record the values for the following properties:

   | Property | Description |
   | --- | --- |
   | `STORAGE_AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account; for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. All S3 storage integrations in your account use that IAM user. |
   | `STORAGE_AWS_EXTERNAL_ID` | The external ID that Snowflake uses to establish a trust relationship with AWS. If you didn’t specify an external ID (`STORAGE_AWS_EXTERNAL_ID`) when you created the storage integration, Snowflake generates an ID for you to use. |

   You provide these values in the next section.

### Step 5: Grant the IAM user permissions to access bucket objects[¶](#step-5-grant-the-iam-user-permissions-to-access-bucket-objects "Link to this heading")

The following step-by-step instructions describe how to configure IAM access permissions for Snowflake in your AWS Management Console so that you can use a S3 bucket to load and unload data:

1. Sign in to the AWS Management Console.
2. Select IAM.
3. From the left-hand navigation pane, select Roles.
4. Select the role you created in [Step 2: Create the IAM role in AWS](#step-2-create-the-iam-role-in-aws) (in this topic).
5. Select the Trust relationships tab.
6. Select Edit trust policy.
7. Modify the policy document with the DESC STORAGE INTEGRATION output values you recorded in
   [Step 4: Retrieve the AWS IAM user for your Snowflake account](#step-4-retrieve-the-aws-iam-user-for-your-snowflake-account) (in this topic):

   **Policy document for IAM role**

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "",
         "Effect": "Allow",
         "Principal": {
           "AWS": "<snowflake_user_arn>"
         },
         "Action": "sts:AssumeRole",
         "Condition": {
           "StringEquals": {
             "sts:ExternalId": "<snowflake_external_id>"
           }
         }
       }
     ]
   }
   ```

   Copy

   Where:

   > * `snowflake_user_arn` is the STORAGE\_AWS\_IAM\_USER\_ARN value you recorded.
   > * `snowflake_external_id` is the STORAGE\_AWS\_EXTERNAL\_ID value you recorded.
   >
   >   In this example, the `snowflake_external_id` value is `MYACCOUNT_SFCRole=2_a123456/s0aBCDEfGHIJklmNoPq=`.
   >
   >   Note
   >
   >   For security reasons, if you create a new storage integration (or recreate an existing storage integration using the CREATE OR
   >   REPLACE STORAGE INTEGRATION syntax) without specifying an external ID, the new integration has a *different* external ID and
   >   can’t resolve the trust relationship unless you update the trust policy.
8. Select Update policy to save your changes.

Note

Snowflake caches the temporary credentials for a period that cannot exceed the 60-minute expiration time. If you revoke access from
Snowflake, users might be able to list files and load data from the cloud storage location until the cache expires.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](../sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

## Determining the correct option[¶](#determining-the-correct-option "Link to this heading")

Before proceeding, determine whether an S3 event notification exists for the target path (or “prefix,” in AWS terminology) in your S3 bucket where your data files are located. AWS rules prohibit creating conflicting notifications for the same path.

The following options for automating Snowpipe using Amazon SQS are supported:

* **Option 1. New S3 event notification:** Create an event notification for the target path in your S3 bucket. The event notification informs Snowpipe via an SQS queue when files are ready to load.

  Important

  If a conflicting event notification exists for your S3 bucket, use Option 2 instead.
* **Option 2. Existing event notification:** Configure [Amazon Simple Notification Service (SNS)](https://aws.amazon.com/sns/) as a broadcaster to share notifications for a given path with multiple endpoints (or “subscribers,” e.g. SQS queues or AWS Lambda workloads), including the Snowflake SQS queue for Snowpipe automation. An S3 event notification published by SNS informs Snowpipe via an SQS queue when files are ready to load.

  Note

  We recommend this option if you plan to use [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history). You can also migrate from option 1 to
  option 2 after you create a replication or failover group. For more information, see [Migrate to Amazon Simple Notification Service (SNS)](account-replication-stages-pipes-load-history.html#label-account-replication-stages-pipes-load-history-migrate-to-sns).
* **Option 3. Setting up Amazon EventBridge for automating Snowpipe:** Similar to option 2, you can also enable [Amazon EventBridge](https://aws.amazon.com/eventbridge/) for S3 buckets and create rules to send notifications to SNS topics.

## Option 1: Creating a new S3 event notification to automate Snowpipe[¶](#option-1-creating-a-new-s3-event-notification-to-automate-snowpipe "Link to this heading")

This section describes the most common option for triggering Snowpipe data loads automatically using [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket. The steps explain how to create an event notification for the target path (or “prefix,” in AWS terminology) in your S3 bucket where your data files are stored.

> Important
>
> If a conflicting event notification exists for your S3 bucket, use [Option 2: Configuring Amazon SNS to Automate Snowpipe Using SQS Notifications](#option-2-configuring-amazon-sns-to-automate-snowpipe-using-sqs-notifications) (in this topic) instead. AWS rules prohibit creating conflicting notifications for the same target path.

The following diagram shows the Snowpipe auto-ingest process flow:

[![Snowpipe Auto-ingest Process Flow](../_images/data-load-snowpipe-s3-sqs.png)](../_images/data-load-snowpipe-s3-sqs.png)

1. Data files are loaded in a stage.
2. An S3 event notification informs Snowpipe via an SQS queue that files are ready to load. Snowpipe copies the files into a queue.
3. A Snowflake-provided virtual warehouse loads data from the queued files into the target table based on parameters defined in the specified pipe.

Note

The instructions in this topic assume a target table already exists in the Snowflake database where your data will be loaded.

### Step 1: Create a stage (if needed)[¶](#step-1-create-a-stage-if-needed "Link to this heading")

Create an external stage that references your S3 bucket using the [CREATE STAGE](../sql-reference/sql/create-stage) command. Snowpipe fetches your data files from the stage and temporarily queues them before loading them into your target table. Alternatively, you can use an existing external stage.

Note

* To configure secure access to the cloud storage location, see [Configuring Secure Access to Cloud Storage](#configuring-secure-access-to-cloud-storage) (in this topic).
* To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration object.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the path `files`. The stage references a storage integration named `my_storage_int`:

> ```
> USE SCHEMA snowpipe_db.public;
>
> CREATE STAGE mystage
>   URL = 's3://mybucket/load/files'
>   STORAGE_INTEGRATION = my_storage_int;
> ```
>
> Copy

### Step 2: Create a pipe with auto-ingest enabled[¶](#step-2-create-a-pipe-with-auto-ingest-enabled "Link to this heading")

Create a pipe using the [CREATE PIPE](../sql-reference/sql/create-pipe) command. The pipe defines the [COPY INTO <table>](../sql-reference/sql/copy-into-table) statement used by Snowpipe to load data from the ingestion queue into the target table.

The following example creates a pipe named `mypipe` in the active schema for the user session. The pipe loads the data from files staged in the `mystage` stage into the `mytable` table:

> ```
> CREATE PIPE snowpipe_db.public.mypipe
>   AUTO_INGEST = TRUE
>   AS
>     COPY INTO snowpipe_db.public.mytable
>       FROM @snowpipe_db.public.mystage
>       FILE_FORMAT = (type = 'JSON');
> ```
>
> Copy

The `AUTO_INGEST = TRUE` parameter specifies to read event notifications sent from an S3 bucket to an SQS queue when new data is ready to load.

Important

Compare the stage reference in the pipe definition with existing pipes. Verify that the directory paths for the same S3 bucket do not overlap; otherwise, multiple pipes could load the same set of data files multiple times, into one or more target tables. This can happen, for example, when multiple stages reference the same S3 bucket with different levels of granularity, such as `s3://mybucket/path1` and `s3://mybucket/path1/path2`. In this use case, if files are staged in `s3://mybucket/path1/path2`, the pipes for both stages would load a copy of the files.

This is different from the manual Snowpipe setup (with auto-ingest *disabled*), which requires users to submit a named set of files to a REST API to queue the files for loading. With auto-ingest enabled, each pipe receives a generated file list from the S3 event notifications. Additional care is required to avoid data duplication.

### Step 3: Configure security[¶](#step-3-configure-security "Link to this heading")

For each user who will execute continuous data loads using Snowpipe, grant sufficient access control privileges on the objects for the data load (i.e. the target database, schema, and table; the stage object, and the pipe).

Note

To follow the general principle of “least privilege”, we recommend creating a separate user and role to use for ingesting files using a pipe. The user should be created with this role as its default role.

Using Snowpipe requires a role with the following privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Named pipe | OWNERSHIP |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created in [Step 1: Create a Stage (If Needed)](#step-1-create-a-stage-if-needed) references a named file format. |
| Target database | USAGE |  |
| Target schema | USAGE |  |
| Target table | INSERT , SELECT |  |

Use the [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege) command to grant privileges to the role.

Note

Only security administrators (i.e. users with the SECURITYADMIN role) or higher, or another role with both the CREATE ROLE privilege on the account and the global MANAGE GRANTS privilege, can create roles and grant privileges.

For example, create a role named `snowpipe_role` that can access a set of `snowpipe_db.public` database objects as well as a pipe named `mypipe`; then, grant the role to a user:

> ```
> -- Create a role to contain the Snowpipe privileges
> USE ROLE SECURITYADMIN;
>
> CREATE OR REPLACE ROLE snowpipe_role;
>
> -- Grant the required privileges on the database objects
> GRANT USAGE ON DATABASE snowpipe_db TO ROLE snowpipe_role;
>
> GRANT USAGE ON SCHEMA snowpipe_db.public TO ROLE snowpipe_role;
>
> GRANT INSERT, SELECT ON snowpipe_db.public.mytable TO ROLE snowpipe_role;
>
> GRANT USAGE ON STAGE snowpipe_db.public.mystage TO ROLE snowpipe_role;
>
> -- Pause the pipe for OWNERSHIP transfer
> ALTER PIPE mypipe SET PIPE_EXECUTION_PAUSED = TRUE;
>
> -- Grant the OWNERSHIP privilege on the pipe object
> GRANT OWNERSHIP ON PIPE snowpipe_db.public.mypipe TO ROLE snowpipe_role;
>
> -- Grant the role to a user
> GRANT ROLE snowpipe_role TO USER jsmith;
>
> -- Set the role as the default role for the user
> ALTER USER jsmith SET DEFAULT_ROLE = snowpipe_role;
>
> -- Resume the pipe
> ALTER PIPE mypipe SET PIPE_EXECUTION_PAUSED = FALSE;
> ```
>
> Copy

### Step 4: Configure event notifications[¶](#step-4-configure-event-notifications "Link to this heading")

Configure event notifications for your S3 bucket to notify Snowpipe when new data is available to load. The auto-ingest feature relies on SQS queues to deliver event notifications from S3 to Snowpipe.

For ease of use, Snowpipe SQS queues are created and managed by Snowflake. The SHOW PIPES command output displays the Amazon Resource Name (ARN) of your SQS queue.

1. Execute the SHOW PIPES command:

   > ```
   > SHOW PIPES;
   > ```
   >
   > Copy

   Note the ARN of the SQS queue for the stage in the `notification_channel` column. Copy the ARN to a convenient location.

   Note

   Following AWS guidelines, Snowflake designates no more than one SQS queue per AWS S3 region. An SQS queue can be shared among multiple buckets in the same region from the same AWS account. The SQS queue coordinates notifications for all pipes connecting the external stages for the S3 buckets to the target tables. When a data file is uploaded into the bucket, all pipes that match the stage directory path perform a one-time load of the file into their corresponding target tables.
2. Log into the Amazon S3 console.
3. Configure an event notification for your S3 bucket using the instructions provided in the [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-event-notifications.html). Complete the fields as follows:

   > * Name: Name of the event notification (e.g. `Auto-ingest Snowflake`).
   > * Events: Select the ObjectCreate (All) option.
   > * Send to: Select SQS Queue from the dropdown list.
   > * SQS: Select Add SQS queue ARN from the dropdown list.
   > * SQS queue ARN: Paste the SQS queue name from the SHOW PIPES output.

Note

These instructions create a single event notification that monitors activity for the entire S3 bucket. This is the simplest approach. This notification handles all pipes configured at a more granular level in the S3 bucket directory. Snowpipe only loads data files as specified in pipe definitions. Note, however, that a high volume of notifications for activity outside a pipe definition could negatively impact the rate at which Snowpipe filters notifications and takes action.

Alternatively, in the above steps, configure one or more paths and/or file extensions (or *prefixes* and *suffixes*, in AWS terminology) to filter event activity. For instructions, see the object key name filtering information in the relevant [AWS documentation topic](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html). Repeat these steps for each additional path or file extension you want the notification to monitor.

Note that AWS limits the number of these notification *queue configurations* to a maximum of 100 per S3 bucket.

Also note that AWS does not allow overlapping queue configurations (across event notifications) for the same S3 bucket. For example, if an existing notification is configured for `s3://mybucket/load/path1`, then you cannot create another notification at a higher level, such as `s3://mybucket/load`, or vice-versa.

Snowpipe with auto-ingest is now configured!

When new data files are added to the S3 bucket, the event notification informs Snowpipe to load them into the target table defined in the pipe.

### Step 5: Load historical files[¶](#step-5-load-historical-files "Link to this heading")

To load any backlog of data files that existed in the external stage before SQS notifications were configured, see [Loading historic data](data-load-snowpipe-manage.html#label-snowpipe-load-historic-data).

### Step 6: Delete staged files[¶](#step-6-delete-staged-files "Link to this heading")

Delete the staged files after you successfully load the data and no longer require the files. For instructions, see
[Deleting staged files after Snowpipe loads the data](data-load-snowpipe-manage.html#label-snowpipe-delete-data-files).

## Option 2: Configuring Amazon SNS to automate Snowpipe using SQS notifications[¶](#option-2-configuring-amazon-sns-to-automate-snowpipe-using-sqs-notifications "Link to this heading")

This section describes how to trigger Snowpipe data loads automatically using [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/) notifications for an S3 bucket. The steps explain how to configure [Amazon Simple Notification Service (SNS)](https://aws.amazon.com/sns/) as a broadcaster to publish event notifications for your S3 bucket to multiple subscribers (e.g. SQS queues or AWS Lambda workloads), including the Snowflake SQS queue for Snowpipe automation.

> Note
>
> These instructions assume an event notification exists for the target path in your S3 bucket where your data files are located. If no event notification exists, either:
>
> * Follow [Option 1: Creating a New S3 Event Notification to Automate Snowpipe](#option-1-creating-a-new-s3-event-notification-to-automate-snowpipe) (in this topic) instead.
> * Create an event notification for your S3 bucket, then proceed with the instructions in this topic. For information, see the [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-event-notifications.html).

The following diagram shows the process flow for Snowpipe auto-ingest with Amazon SNS:

[![Snowpipe Auto-ingest Process Flow with Amazon SNS](../_images/data-load-snowpipe-s3-sns.png)](../_images/data-load-snowpipe-s3-sns.png)

1. Data files are loaded in a stage.
2. An S3 event notification published by SNS informs Snowpipe via an SQS queue that files are ready to load. Snowpipe copies the files into a queue.
3. A Snowflake-provided virtual warehouse loads data from the queued files into the target table based on parameters defined in the specified pipe.

Note

The instructions assume a target table already exists in the Snowflake database where your data will be loaded.

Snowpipe auto ingest supports AWS KMS-encrypted SNS topics. For more information, refer to [Encryption at rest](https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html).

### Prerequisite: Create an Amazon SNS Topic and Subscription[¶](#prerequisite-create-an-amazon-sns-topic-and-subscription "Link to this heading")

1. Create an SNS topic in your AWS account to handle all messages for the Snowflake stage location on your S3 bucket.
2. Subscribe your target destinations for the S3 event notifications (for example, other SQS queues or AWS Lambda workloads) to this topic. SNS publishes event notifications for your bucket to all subscribers to the topic.

For instructions, see the [SNS documentation](https://aws.amazon.com/documentation/sns/).

### Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic[¶](#step-1-subscribe-the-snowflake-sqs-queue-to-the-sns-topic "Link to this heading")

1. Sign in to the AWS Management Console.
2. From the home dashboard, choose Simple Notification Service (SNS).
3. Choose Topics from the left-hand navigation pane.
4. Locate the topic for your S3 bucket. Note the topic ARN.
5. Using a Snowflake client, query the [SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY](../sql-reference/functions/system_get_aws_sns_iam_policy) system function with your SNS topic ARN:

   > ```
   > select system$get_aws_sns_iam_policy('<sns_topic_arn>');
   > ```
   >
   > Copy

   The function returns an IAM policy that grants a Snowflake SQS queue permission to subscribe to the SNS topic.

   For example:

   > ```
   > select system$get_aws_sns_iam_policy('arn:aws:sns:us-west-2:001234567890:s3_mybucket');
   >
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > | SYSTEM$GET_AWS_SNS_IAM_POLICY('ARN:AWS:SNS:US-WEST-2:001234567890:S3_MYBUCKET')                                                                                                                                                                   |
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > | {"Version":"2012-10-17","Statement":[{"Sid":"1","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"},"Action":["sns:Subscribe"],"Resource":["arn:aws:sns:us-west-2:001234567890:s3_mybucket"]}]}                 |
   > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   > ```
   >
   > Copy
6. Return to the AWS Management Console. Choose Topics from the left-hand navigation pane.
7. Select the topic for your S3 bucket, and click the Edit button. The Edit page opens.
8. Click Access policy - Optional to expand this area of the page.
9. Merge the IAM policy addition from the SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY function results into the JSON document.

   For example:

   **Original IAM policy (abbreviated):**

   > ```
   > {
   >   "Version":"2008-10-17",
   >   "Id":"__default_policy_ID",
   >   "Statement":[
   >      {
   >         "Sid":"__default_statement_ID",
   >         "Effect":"Allow",
   >         "Principal":{
   >            "AWS":"*"
   >         }
   >         ..
   >      }
   >    ]
   >  }
   > ```
   >
   > Copy

   **Merged IAM policy:**

   > ```
   > {
   >   "Version":"2008-10-17",
   >   "Id":"__default_policy_ID",
   >   "Statement":[
   >      {
   >         "Sid":"__default_statement_ID",
   >         "Effect":"Allow",
   >         "Principal":{
   >            "AWS":"*"
   >         }
   >         ..
   >      },
   >      {
   >         "Sid":"1",
   >         "Effect":"Allow",
   >         "Principal":{
   >           "AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
   >          },
   >          "Action":[
   >            "sns:Subscribe"
   >          ],
   >          "Resource":[
   >            "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
   >          ]
   >      }
   >    ]
   >  }
   > ```
   >
   > Copy
10. Add an additional policy grant to allow S3 to publish event notifications for the bucket to the SNS topic.

    For example (using the SNS topic ARN and S3 bucket used throughout these instructions):

    > ```
    > {
    >     "Sid":"s3-event-notifier",
    >     "Effect":"Allow",
    >     "Principal":{
    >        "Service":"s3.amazonaws.com"
    >     },
    >     "Action":"SNS:Publish",
    >     "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
    >     "Condition":{
    >        "ArnLike":{
    >           "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
    >        }
    >     }
    >  }
    > ```
    >
    > Copy

    **Merged IAM policy:**

    > ```
    > {
    >   "Version":"2008-10-17",
    >   "Id":"__default_policy_ID",
    >   "Statement":[
    >      {
    >         "Sid":"__default_statement_ID",
    >         "Effect":"Allow",
    >         "Principal":{
    >            "AWS":"*"
    >         }
    >         ..
    >      },
    >      {
    >         "Sid":"1",
    >         "Effect":"Allow",
    >         "Principal":{
    >           "AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"
    >          },
    >          "Action":[
    >            "sns:Subscribe"
    >          ],
    >          "Resource":[
    >            "arn:aws:sns:us-west-2:001234567890:s3_mybucket"
    >          ]
    >      },
    >      {
    >         "Sid":"s3-event-notifier",
    >         "Effect":"Allow",
    >         "Principal":{
    >            "Service":"s3.amazonaws.com"
    >         },
    >         "Action":"SNS:Publish",
    >         "Resource":"arn:aws:sns:us-west-2:001234567890:s3_mybucket",
    >         "Condition":{
    >            "ArnLike":{
    >               "aws:SourceArn":"arn:aws:s3:*:*:s3_mybucket"
    >            }
    >         }
    >       }
    >    ]
    >  }
    > ```
    >
    > Copy
11. Click Save changes.

### Step 2: Create a stage (if needed)[¶](#step-2-create-a-stage-if-needed "Link to this heading")

Create an external stage that references your S3 bucket using the [CREATE STAGE](../sql-reference/sql/create-stage) command. Snowpipe fetches your data files from the stage and temporarily queues them before loading them into your target table.

Alternatively, you can use an existing external stage.

Note

To configure secure access to the cloud storage location, see [Configuring Secure Access to Cloud Storage](#configuring-secure-access-to-cloud-storage) (in this topic).

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the path `files`. The stage references a storage integration named `my_storage_int`:

> ```
> CREATE STAGE mystage
>   URL = 's3://mybucket/load/files'
>   STORAGE_INTEGRATION = my_storage_int;
> ```
>
> Copy

### Step 3: Create a pipe with auto-ingest enabled[¶](#step-3-create-a-pipe-with-auto-ingest-enabled "Link to this heading")

Create a pipe using the [CREATE PIPE](../sql-reference/sql/create-pipe) command. The pipe defines the [COPY INTO <table>](../sql-reference/sql/copy-into-table) statement used by Snowpipe to load data from the ingestion queue into the target table. In the COPY statement, identify the SNS topic ARN from [Prerequisite: Create an Amazon SNS Topic and Subscription](#prerequisite-create-an-amazon-sns-topic-and-subscription).

The following example creates a pipe named `mypipe` in the active schema for the user session. The pipe loads the data from files staged in the `mystage` stage into the `mytable` table:

> ```
> CREATE PIPE snowpipe_db.public.mypipe
>   AUTO_INGEST = TRUE
>   AWS_SNS_TOPIC='<sns_topic_arn>'
>   AS
>     COPY INTO snowpipe_db.public.mytable
>       FROM @snowpipe_db.public.mystage
>       FILE_FORMAT = (type = 'JSON');
> ```
>
> Copy

Where:

`AUTO_INGEST = TRUE`
:   Specifies to read event notifications sent from an S3 bucket to an SQS queue when new data is ready to load.

`AWS_SNS_TOPIC = '<sns_topic_arn>'`
:   Specifies the ARN for the SNS topic for your S3 bucket, e.g. `arn:aws:sns:us-west-2:001234567890:s3_mybucket` in the current example. The CREATE PIPE statement subscribes the Snowflake SQS queue to the specified SNS topic. Note that the pipe will only copy files to the ingest queue triggered by event notifications via the SNS topic.

To remove either parameter from a pipe, it is currently necessary to recreate the pipe using the CREATE OR REPLACE PIPE syntax.

Important

Verify that the storage location reference in the COPY INTO *<table>* statement does not overlap with the reference in existing pipes
in the account. Otherwise, multiple pipes could load the same set of data files into the target tables. For example, this situation can
occur when multiple pipe definitions reference the same storage location with different levels of granularity, such as
`<storage_location>/path1/` and `<storage_location>/path1/path2/`. In this example, if files are staged in
`<storage_location>/path1/path2/`, both pipes would load a copy of the files.

View the COPY INTO *<table>* statements in the definitions of all pipes in the account by executing [SHOW PIPES](../sql-reference/sql/show-pipes)
or by querying either the [PIPES](../sql-reference/account-usage/pipes) view in Account Usage or the
[PIPES](../sql-reference/info-schema/pipes) view in the Information Schema.

### Step 4: Configure security[¶](#step-4-configure-security "Link to this heading")

For each user who will execute continuous data loads using Snowpipe, grant sufficient access control privileges on the objects for the data load (i.e. the target database, schema, and table; the stage object, and the pipe).

Note

To follow the general principle of “least privilege”, we recommend creating a separate user and role to use for ingesting files using a pipe. The user should be created with this role as its default role.

Using Snowpipe requires a role with the following privileges:

| Object | Privilege | Notes |
| --- | --- | --- |
| Named pipe | OWNERSHIP |  |
| Named storage integration | USAGE | Needed if the stage you created in [Step 2: Create a Stage (If Needed)](#step-2-create-a-stage-if-needed) references a storage integration. |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created in [Step 2: Create a Stage (If Needed)](#step-2-create-a-stage-if-needed) references a named file format. |
| Target database | USAGE |  |
| Target schema | USAGE |  |
| Target table | INSERT , SELECT |  |

Use the [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege) command to grant privileges to the role.

Note

Only security administrators (i.e. users with the SECURITYADMIN role) or higher can create roles.

For example, create a role named `snowpipe_role` that can access a set of `snowpipe_db.public` database objects as well as a pipe named `mypipe`; then, grant the role to a user:

> ```
> -- Create a role to contain the Snowpipe privileges
> USE ROLE SECURITYADMIN;
>
> CREATE OR REPLACE ROLE snowpipe_role;
>
> -- Grant the required privileges on the database objects
> GRANT USAGE ON DATABASE snowpipe_db TO ROLE snowpipe_role;
>
> GRANT USAGE ON SCHEMA snowpipe_db.public TO ROLE snowpipe_role;
>
> GRANT INSERT, SELECT ON snowpipe_db.public.mytable TO ROLE snowpipe_role;
>
> GRANT USAGE, READ ON STAGE snowpipe_db.public.mystage TO ROLE snowpipe_role;
>
> -- Pause the pipe for OWNERSHIP transfer
> ALTER PIPE mypipe SET PIPE_EXECUTION_PAUSED = TRUE;
>
> -- Grant the OWNERSHIP privilege on the pipe object
> GRANT OWNERSHIP ON PIPE snowpipe_db.public.mypipe TO ROLE snowpipe_role;
>
> -- Grant the role to a user
> GRANT ROLE snowpipe_role TO USER jsmith;
>
> -- Set the role as the default role for the user
> ALTER USER jsmith SET DEFAULT_ROLE = snowpipe_role;
>
> -- Resume the pipe
> ALTER PIPE mypipe SET PIPE_EXECUTION_PAUSED = FALSE;
> ```
>
> Copy

Snowpipe with auto-ingest is now configured!

When new data files are added to the S3 bucket, the event notification informs Snowpipe to load them into the target table defined in the pipe.

### Step 5: Load historical files[¶](#id5 "Link to this heading")

To load any backlog of data files that existed in the external stage before SQS notifications were configured, see [Loading historic data](data-load-snowpipe-manage.html#label-snowpipe-load-historic-data).

### Step 6: Delete staged files[¶](#id6 "Link to this heading")

Delete the staged files after you successfully load the data and no longer require the files. For instructions, see
[Deleting staged files after Snowpipe loads the data](data-load-snowpipe-manage.html#label-snowpipe-delete-data-files).

## Option 3: Setting up Amazon EventBridge to automate Snowpipe[¶](#option-3-setting-up-amazon-eventbridge-to-automate-snowpipe "Link to this heading")

Similar to Option 2, you can also set up Amazon EventBridge to automate Snowpipe.

### Step 1: Create an Amazon SNS topic[¶](#step-1-create-an-amazon-sns-topic "Link to this heading")

Follow [Prerequisite: Create an Amazon SNS Topic and Subscription](#prerequisite-create-an-amazon-sns-topic-and-subscription) (in this topic).

### Step 2: Create an EventBridge rule to subscribe S3 buckets and send notifications to SNS topic[¶](#step-2-create-an-eventbridge-rule-to-subscribe-s3-buckets-and-send-notifications-to-sns-topic "Link to this heading")

* [Enable Amazon EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications-eventbridge.html) for S3 buckets.
* Create EventBridge rules to [send notifications](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-s3-object-created-tutorial.html) to the SNS topic created in step 1.

### Step 3: Configuring Amazon SNS to automate Snowpipe using SQS notifications[¶](#step-3-configuring-amazon-sns-to-automate-snowpipe-using-sqs-notifications "Link to this heading")

Follow [Option 2: Configuring Amazon SNS to automate Snowpipe using SQS notifications](#label-configuring-amazon-sns-for-snowpipe) (in this topic).

## SYSTEM$PIPE\_STATUS output[¶](#system-pipe-status-output "Link to this heading")

The [SYSTEM$PIPE\_STATUS](../sql-reference/functions/system_pipe_status) function retrieves a JSON representation of the current status of a pipe.

For pipes with AUTO\_INGEST set to TRUE, the function returns a JSON object containing the following name/value pairs (if applicable to the current pipe status):

> {“executionState”:”<value>”,”oldestFileTimestamp”:<value>,”pendingFileCount”:<value>,”notificationChannelName”:”<value>”,”numOutstandingMessagesOnChannel”:<value>,”lastReceivedMessageTimestamp”:”<value>”,”lastForwardedMessageTimestamp”:”<value>”,”error”:<value>,”fault”:<value>}

For descriptions of the output values, see the reference topic for the SQL function.

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

1. [Cloud platform support](#cloud-platform-support)
2. [Network traffic](#network-traffic)
3. [Configuring secure access to Cloud Storage](#configuring-secure-access-to-cloud-storage)
4. [Determining the correct option](#determining-the-correct-option)
5. [Option 1: Creating a new S3 event notification to automate Snowpipe](#option-1-creating-a-new-s3-event-notification-to-automate-snowpipe)
6. [Option 2: Configuring Amazon SNS to automate Snowpipe using SQS notifications](#option-2-configuring-amazon-sns-to-automate-snowpipe-using-sqs-notifications)
7. [Option 3: Setting up Amazon EventBridge to automate Snowpipe](#option-3-setting-up-amazon-eventbridge-to-automate-snowpipe)
8. [SYSTEM$PIPE\_STATUS output](#system-pipe-status-output)

Related content

1. [CREATE STORAGE INTEGRATION](/user-guide/../sql-reference/sql/create-storage-integration)
2. [DESCRIBE INTEGRATION](/user-guide/../sql-reference/sql/desc-integration)
3. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/user-guide/../sql-reference/functions/system_validate_storage_integration)
4. [CREATE PIPE](/user-guide/../sql-reference/sql/create-pipe)
5. [SYSTEM$PIPE\_STATUS](/user-guide/../sql-reference/functions/system_pipe_status)
6. [AWS S3 Access Logs Ingestion (Snowflake Quickstart)](https://quickstarts.snowflake.com/guide/s3_access_log_ingestion/)