---
auto_generated: true
description: You can trigger external table metadata refreshes by using Google Cloud
  Pub/Sub messages for Google Cloud Storage (GCS) events.
last_scraped: '2026-01-14T16:55:19.340407+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/tables-external-gcs
title: Refresh external tables automatically for Google Cloud Storage | Snowflake
  Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)

   * [Table Structures](tables-micro-partitions.md)
   * [Temporary And Transient Tables](tables-temp-transient.md)
   * [External Tables](tables-external-intro.md)

     + [Automatic Refreshing](tables-external-auto.md)

       - [Amazon S3](tables-external-s3.md)
       - [Google Cloud Storage](tables-external-gcs.md)
       - [Azure Blob Storage](tables-external-azure.md)
     + [Troubleshooting](tables-external-ts.md)
     + [Integrating Apache Hive Metastores](tables-external-hive.md)
   * [Hybrid Tables](tables-hybrid.md)
   * [Interactive tables](interactive.md)
   * [Working with tables in Snowsight](ui-snowsight-data-databases-table.md)
   * [Search optimization service](search-optimization-service.md)
   * Views
   * [Views](views-introduction.md)
   * [Secure Views](views-secure.md)
   * [Materialized Views](views-materialized.md)
   * [Semantic Views](views-semantic/overview.md)
   * [Working with Views in Snowsight](ui-snowsight-data-databases-view.md)
   * Considerations
   * [Views, Materialized Views, and Dynamic Tables](overview-view-mview-dts.md)
   * [Table Design](table-considerations.md)
   * [Cloning](object-clone.md)
   * [Data Storage](tables-storage-considerations.md)
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

[Guides](../guides/README.md)[Databases, Tables, & Views](../guides/overview-db.md)[External Tables](tables-external-intro.md)[Automatic Refreshing](tables-external-auto.md)Google Cloud Storage

# Refresh external tables automatically for Google Cloud Storage[¶](#refresh-external-tables-automatically-for-google-cloud-storage "Link to this heading")

You can trigger external table metadata refreshes by using
[Google Cloud Pub/Sub](https://cloud.google.com/storage/docs/reporting-changes) messages for Google Cloud Storage (GCS) events.

## Prerequisites[¶](#prerequisites "Link to this heading")

Before you proceed, ensure you meet the following prerequisites:

> * A role that has the CREATE STAGE and CREATE EXTERNAL TABLE privileges on a schema.
> * Administrative access to Google Cloud (GC). If you aren’t a GC administrator, ask your GC
>   administrator to complete the prerequisite steps.
> * Only `OBJECT_DELETE` and `OBJECT_FINALIZE` events trigger refreshes for external table metadata.
>   To reduce costs, event noise, and latency, send only supported events for external tables.
> * External tables don’t support storage versioning (S3 versioning, Object Versioning in Google Cloud Storage, or versioning for Azure Storage).

## Cloud platform support[¶](#cloud-platform-support "Link to this heading")

Triggering automated external metadata refreshes by using GCS Pub/Sub event messages is supported by Snowflake accounts
hosted on Google Cloud (GC).

## Configure secure access to Cloud Storage[¶](#configure-secure-access-to-cloud-storage "Link to this heading")

Important

If you have already configured secure access to the GCS bucket that stores your data files, you can skip this section and proceed to [Configuring Automation Using GCS Pub/Sub](#configuring-automation-using-gcs-pub-sub).

You must configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage
to a Snowflake identity and access management (IAM) entity.

This section describes how to use storage integrations to allow Snowflake to read data from and write to a Google Cloud Storage bucket referenced in an external
(that is, Cloud Storage) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as
secret keys or access tokens; instead, integration objects reference a Cloud Storage service account. An administrator in your organization grants the service
account permissions in the Cloud Storage account.

Administrators can also restrict users to a specific set of Cloud Storage buckets (and optional paths) accessed by external stages that use the integration.

Note

* Completing the instructions in this section requires access to your Cloud Storage project as a project editor. If you are not a project
  editor, ask your Cloud Storage administrator to perform these tasks.
* Confirm that Snowflake supports the Google Cloud Storage region that your storage is hosted in. For more information, see
  [Supported cloud regions](intro-regions).

The following diagram shows the integration flow for a Cloud Storage stage:

[![Google Cloud Storage Stage Integration Flow](../_images/storage-integration-gcs.png)](../_images/storage-integration-gcs.png)

1. An external (that is, Cloud Storage) stage references a storage integration object in its definition.
2. Snowflake automatically associates the storage integration with a Cloud Storage service account created for your account. Snowflake creates a single service account that is referenced by all GCS storage integrations in your Snowflake account.
3. A project editor for your Cloud Storage project grants permissions to the service account to access the bucket referenced in the stage definition. Note that many external stage objects can reference different buckets and paths and use the same integration for authentication.

When a user loads or unloads data from or to a stage, Snowflake verifies the permissions granted to the service account on the bucket before allowing or denying access.

**In this Section:**

* [Step 1: Create a Cloud Storage integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake)
* [Step 2: Retrieve the Cloud Storage service account for your Snowflake account](#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account)
* [Step 3: Grant the service account permissions to access bucket objects](#step-3-grant-the-service-account-permissions-to-access-bucket-objects)

  + [Creating a custom IAM role](#creating-a-custom-iam-role)
  + [Assigning the Custom Role to the Cloud Storage Service Account](#assigning-the-custom-role-to-the-cloud-storage-service-account)
  + [Granting the Cloud Storage service account permissions on the Cloud Key Management Service cryptographic keys](#granting-the-cloud-storage-service-account-permissions-on-the-cloud-key-management-service-cryptographic-keys)

### Step 1: Create a Cloud Storage integration in Snowflake[¶](#step-1-create-a-cloud-storage-integration-in-snowflake "Link to this heading")

Create an integration using the [CREATE STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration) command. An integration is a Snowflake object that delegates authentication responsibility for external cloud storage to a Snowflake-generated entity (that is, a Cloud Storage service account). For accessing Cloud Storage buckets, Snowflake creates a service account that can be granted permissions to access the bucket(s) that store your data files.

A single storage integration can support multiple external (that is, GCS) stages. The URL in the stage definition must align with the GCS buckets (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'GCS'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('gcs://<bucket>/<path>/', 'gcs://<bucket>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('gcs://<bucket>/<path>/', 'gcs://<bucket>/<path>/') ]
```

Copy

Where:

* `integration_name` is the name of the new integration.
* `bucket` is the name of a Cloud Storage bucket that stores your data files (for example, `mybucket`). The required STORAGE\_ALLOWED\_LOCATIONS parameter and optional STORAGE\_BLOCKED\_LOCATIONS parameter restrict or block access to these buckets, respectively, when stages that reference this integration are created or modified.
* `path` is an optional path that can be used to provide granular control over objects in the bucket.

The following example creates an integration that explicitly limits external stages that use the integration to reference either of two buckets and paths. In a later step, we will create an external stage that references one of these buckets and paths.

Additional external stages that also use this integration can reference the allowed buckets and paths:

> ```
> CREATE STORAGE INTEGRATION gcs_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'GCS'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('gcs://mybucket1/path1/', 'gcs://mybucket2/path2/')
>   STORAGE_BLOCKED_LOCATIONS = ('gcs://mybucket1/path1/sensitivedata/', 'gcs://mybucket2/path2/sensitivedata/');
> ```
>
> Copy

### Step 2: Retrieve the Cloud Storage service account for your Snowflake account[¶](#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account "Link to this heading")

Execute the [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) command to retrieve the ID for the Cloud Storage service account that was created automatically for your Snowflake account:

```
DESC STORAGE INTEGRATION <integration_name>;
```

Copy

Where:

> * `integration_name` is the name of the integration you created in [Step 1: Create a Cloud Storage integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake) (in this topic).

For example:

> ```
> DESC STORAGE INTEGRATION gcs_int;
>
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
> | property                    | property_type | property_value                                                              | property_default |
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------|
> | ENABLED                     | Boolean       | true                                                                        | false            |
> | STORAGE_ALLOWED_LOCATIONS   | List          | gcs://mybucket1/path1/,gcs://mybucket2/path2/                               | []               |
> | STORAGE_BLOCKED_LOCATIONS   | List          | gcs://mybucket1/path1/sensitivedata/,gcs://mybucket2/path2/sensitivedata/   | []               |
> | STORAGE_GCP_SERVICE_ACCOUNT | String        | service-account-id@project1-123456.iam.gserviceaccount.com                  |                  |
> +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
> ```
>
> Copy

The STORAGE\_GCP\_SERVICE\_ACCOUNT property in the output shows the Cloud Storage service account created for your Snowflake account (that is, `service-account-id@project1-123456.iam.gserviceaccount.com`). We provision a single Cloud Storage service account for your entire Snowflake account. All Cloud Storage integrations use that service account.

### Step 3: Grant the service account permissions to access bucket objects[¶](#step-3-grant-the-service-account-permissions-to-access-bucket-objects "Link to this heading")

The following step-by-step instructions describe how to configure IAM access permissions for Snowflake in your Google Cloud console so that you can use a Cloud Storage bucket to load and unload data:

#### Creating a custom IAM role[¶](#creating-a-custom-iam-role "Link to this heading")

Create a custom role that has the permissions required to access the bucket and get objects.

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, select IAM & Admin » Roles.
3. Select Create Role.
4. Enter a Title and optional Description for the custom role.
5. Select Add Permissions.
6. Filter the list of permissions, and add the following from the list:

   > | Action(s) | Required permissions |
   > | --- | --- |
   > | Data loading only | * `storage.buckets.get` * `storage.objects.get` * `storage.objects.list` |
   > | Data loading with purge option, executing the REMOVE command on the stage | * `storage.buckets.get` * `storage.objects.delete` * `storage.objects.get` * `storage.objects.list` |
   > | Data loading and unloading | * `storage.buckets.get` (for calculating data transfer costs) * `storage.objects.create` * `storage.objects.delete` * `storage.objects.get` * `storage.objects.list` |
   > | Data unloading only | * `storage.buckets.get` * `storage.objects.create` * `storage.objects.delete` * `storage.objects.list` |
   > | Using [COPY FILES](../sql-reference/sql/copy-files) to copy files to an external stage | You must have the following additional permissions:  * `storage.multipartUploads.abort` * `storage.multipartUploads.create` * `storage.multipartUploads.list` * `storage.multipartUploads.listParts` |
7. Select Add.
8. Select Create.

#### Assigning the Custom Role to the Cloud Storage Service Account[¶](#assigning-the-custom-role-to-the-cloud-storage-service-account "Link to this heading")

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, select Cloud Storage » Buckets.
3. Filter the list of buckets, and select the bucket that you specified when you created your storage integration.
4. Select Permissions » View by principals, then select Grant access.
5. Under Add principals, paste the name of the service account name that you retrieved from the DESC STORAGE INTEGRATION command output.
6. Under Assign roles, select the custom IAM role that you created previously, then select Save.

Important

If your Google Cloud organization was created on or after May 3, 2024, Google Cloud enforces a
[domain restriction constraint](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains)
in project organization policies. The default constraint lists your domain as the only allowed value.

To allow the Snowflake service account access to your storage, you must
[update the domain restriction](data-load-gcs-allow).

#### Granting the Cloud Storage service account permissions on the Cloud Key Management Service cryptographic keys[¶](#granting-the-cloud-storage-service-account-permissions-on-the-cloud-key-management-service-cryptographic-keys "Link to this heading")

Note

This step is required only if your GCS bucket is encrypted using a key stored in the Google Cloud Key Management Service (Cloud KMS).

1. Sign in to the Google Cloud console as a project editor.
2. From the home dashboard, search for and select Security » Key Management.
3. Select the key ring that is assigned to your GCS bucket.
4. Click SHOW INFO PANEL in the upper-right corner. The information panel for the key ring slides out.
5. Click the ADD PRINCIPAL button.
6. In the New principals field, search for the service account name from the DESCRIBE INTEGRATION output in [Step 2: Retrieve the Cloud Storage service account for your Snowflake account](#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account) (in this topic).
7. From the Select a role dropdown, select the `Cloud KMS CrytoKey Encryptor/Decryptor` role.
8. Click the Save button. The service account name is added to the Cloud KMS CrytoKey Encryptor/Decryptor role dropdown in the information panel.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](../sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

## Configuring Automation Using GCS Pub/Sub[¶](#configuring-automation-using-gcs-pub-sub "Link to this heading")

### Prerequisites[¶](#id1 "Link to this heading")

The instructions in this topic assume the following items have been created and configured:

GCP account:
:   * Pub/Sub topic that receives event messages from the GCS bucket. For more information, see [Creating the Pub/Sub Topic](#creating-the-pub-sub-topic) (in this topic).
    * Subscription that receives event messages from the Pub/Sub topic. For more information, see [Creating the Pub/Sub Subscription](#creating-the-pub-sub-subscription) (in this topic).

    For instructions, see the [Pub/Sub documentation](https://cloud.google.com/pubsub/docs).

Snowflake:
:   * Target table in the Snowflake database where your data will be loaded.

#### Creating the Pub/Sub Topic[¶](#creating-the-pub-sub-topic "Link to this heading")

Create a Pub/Sub topic using [Cloud Shell](https://cloud.google.com/shell) or [Cloud SDK](https://cloud.google.com/sdk).

Execute the following command to create the topic and enable it to listen for activity in the specified GCS bucket:

```
$ gsutil notification create -t <topic> -f json -e OBJECT_FINALIZE -e OBJECT_DELETE gs://<bucket-name>
```

Copy

Where:

* `<topic>` is the name for the topic.
* `<bucket-name>` is the name of your GCS bucket.

If the topic already exists, the command uses it; otherwise, a new topic is created.

For more information, see [Using Pub/Sub notifications for Cloud Storage](https://cloud.google.com/storage/docs/reporting-changes) in the Pub/Sub documentation.

#### Creating the Pub/Sub Subscription[¶](#creating-the-pub-sub-subscription "Link to this heading")

Create a subscription with pull delivery to the Pub/Sub topic using the Cloud Console, `gcloud` command-line tool, or the Cloud Pub/Sub API. For instructions, see [Managing topics and subscriptions](https://cloud.google.com/pubsub/docs/admin) in the Pub/Sub documentation.

Note

* Only Pub/Sub subscriptions that use the default pull delivery are supported with Snowflake. Push delivery is not supported.

#### Retrieving the Pub/Sub Subscription ID[¶](#retrieving-the-pub-sub-subscription-id "Link to this heading")

The Pub/Sub topic subscription ID is used in these instructions to allow Snowflake access to event messages.

1. Log into the Google Cloud Platform Console as a project editor.
2. From the home dashboard, choose Big Data » Pub/Sub » Subscriptions.
3. Copy the ID in the Subscription ID column for the topic subscription

### Step 1: Create a Notification Integration in Snowflake[¶](#step-1-create-a-notification-integration-in-snowflake "Link to this heading")

Create a notification integration using the
[CREATE NOTIFICATION INTEGRATION](../sql-reference/sql/create-notification-integration-queue-inbound-gcp) command.

The notification integration references your Pub/Sub subscription. Snowflake associates the notification integration with a GCS
service account created for your account. Snowflake creates a single service account that is referenced by all GCS notification
integrations in your Snowflake account.

Note

* Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.
* The GCS service account for notification integrations is different from the service account created for storage integrations.
* A single notification integration supports a single Google Cloud Pub/Sub subscription. Referencing the same Pub/Sub subscription in multiple notification integrations can result in missing data in target tables because event notifications are split between notification integrations.

```
CREATE NOTIFICATION INTEGRATION <integration_name>
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  ENABLED = true
  GCP_PUBSUB_SUBSCRIPTION_NAME = '<subscription_id>';
```

Copy

Where:

* `integration_name` is the name of the new integration.
* `subscription_id` is the subscription name you recorded in [Retrieving the Pub/Sub Subscription ID](#retrieving-the-pub-sub-subscription-id).

For example:

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  ENABLED = true
  GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/project-1234/subscriptions/sub2';
```

Copy

### Step 2: Grant Snowflake Access to the Pub/Sub Subscription[¶](#step-2-grant-snowflake-access-to-the-pub-sub-subscription "Link to this heading")

1. Execute the [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) command to retrieve the Snowflake service account ID:

   ```
   DESC NOTIFICATION INTEGRATION <integration_name>;
   ```

   Copy

   Where:

   * `integration_name` is the name of the integration you created in [Step 1: Create a Notification Integration in Snowflake](#step-1-create-a-notification-integration-in-snowflake).

   For example:

   > ```
   > DESC NOTIFICATION INTEGRATION my_notification_int;
   > ```
   >
   > Copy
2. Record the service account name in the GCP\_PUBSUB\_SERVICE\_ACCOUNT column, which has the following format:

   ```
   <service_account>@<project_id>.iam.gserviceaccount.com
   ```

   Copy
3. Log into the Google Cloud Platform Console as a project editor.
4. From the home dashboard, choose Big Data » Pub/Sub » Subscriptions.
5. Select the subscription to configure for access.
6. Click SHOW INFO PANEL in the upper-right corner. The information panel for the subscription slides out.
7. Click the ADD PRINCIPAL button.
8. In the New principals field, search for the service account name you recorded.
9. From the Select a role dropdown, select Pub/Sub Subscriber.
10. Click the Save button. The service account name is added to the Pub/Sub Subscriber role dropdown in the information panel.
11. Navigate to the Dashboard page in the Cloud Console, and select your project from the dropdown list.
12. Click the ADD PEOPLE TO THIS PROJECT button.
13. Add the service account name you recorded.
14. From the Select a role dropdown, select Monitoring Viewer.
15. Click the Save button. The service account name is added to the Monitoring Viewer role.

### (Optional) Step 3: Create a stage[¶](#optional-step-3-create-a-stage "Link to this heading")

Create an external stage that references your GCS bucket by using the [CREATE STAGE](../sql-reference/sql/create-stage) command. Snowflake reads your
staged data files into the external table metadata. Alternatively, you can use an existing external stage.

Note

* To configure secure access to the cloud storage location, see [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage) earlier in this topic.
* To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration
  object.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the
path `files`. The stage references a storage integration named `my_storage_int`:

> ```
> USE SCHEMA mydb.public;
>
> CREATE STAGE mystage
>   URL='gcs://load/files/'
>   STORAGE_INTEGRATION = my_storage_int;
> ```
>
> Copy

### Step 4: Create an external table[¶](#step-4-create-an-external-table "Link to this heading")

Create an external table by using the [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table) command.

For example, create an external table in the `mydb.public` schema that reads JSON data from files staged in the `mystage` stage with
the `path1/` path.

The INTEGRATION parameter references the `my_notification_int` notification integration you created in
[Step 1: Create a notification integration in Snowflake](#step-1-create-a-notification-integration-in-snowflake). You must enter the integration name in all uppercase letters.

The `AUTO_REFRESH` parameter is `TRUE` by default:

```
CREATE OR REPLACE EXTERNAL TABLE ext_table
 INTEGRATION = 'MY_NOTIFICATION_INT'
 WITH LOCATION = @mystage/path1/
 FILE_FORMAT = (TYPE = JSON);
```

Copy

After you complete this step, the external stage with auto-refresh is configured.

When new or updated data files are added to the GCS bucket, the event notification informs Snowflake to scan them into the external
table metadata.

### Step 5: Manually refresh the external table metadata[¶](#step-5-manually-refresh-the-external-table-metadata "Link to this heading")

Manually refresh the external table metadata once by using [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-external-table) with the REFRESH parameter; for example:

> ```
> ALTER EXTERNAL TABLE ext_table REFRESH;
>
> +---------------------------------------------+----------------+-------------------------------+
> | file                                        | status         | description                   |
> |---------------------------------------------+----------------+-------------------------------|
> | files/path1/file1.json                      | REGISTERED_NEW | File registered successfully. |
> | files/path1/file2.json                      | REGISTERED_NEW | File registered successfully. |
> | files/path1/file3.json                      | REGISTERED_NEW | File registered successfully. |
> +---------------------------------------------+----------------+-------------------------------+
> ```
>
> Copy

This step synchronizes the metadata with the list of files in the stage and path in the external table definition. Also, this step ensures
that the external table can read the data files in the specified stage and path, and that no files were missed in the external table definition.

If the list of files in the `file` column doesn’t match your expectations, verify the paths in the external table definition and
external stage definition. Any path in the external table definition is appended to any path specified in the stage definition. For more
information, see [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table).

Important

If this step is not completed successfully at least once after the external table is created, querying the external table returns no
results until a Pub/Sub notification refreshes the external table metadata automatically for the first time.

This step ensures that the metadata is synchronized with any changes to the file list that occurred after Step 4. Thereafter, Pub/Sub
notifications trigger the metadata refresh automatically.

### Step 6: Configure security[¶](#step-6-configure-security "Link to this heading")

For each additional role that you will use to query the external table, grant sufficient access control privileges on the various
objects (that is, the databases, schemas, stage, and table) by using [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created in [(Optional) Step 3: Create a stage](#optional-step-3-create-a-stage) references a named file format. |
| External table | SELECT |  |

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
2. [Cloud platform support](#cloud-platform-support)
3. [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage)
4. [Configuring Automation Using GCS Pub/Sub](#configuring-automation-using-gcs-pub-sub)

Related content

1. [CREATE STORAGE INTEGRATION](/user-guide/../sql-reference/sql/create-storage-integration)
2. [DESCRIBE INTEGRATION](/user-guide/../sql-reference/sql/desc-integration)
3. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/user-guide/../sql-reference/functions/system_validate_storage_integration)
4. [CREATE STAGE](/user-guide/../sql-reference/sql/create-stage)
5. [CREATE EXTERNAL TABLE](/user-guide/../sql-reference/sql/create-external-table)