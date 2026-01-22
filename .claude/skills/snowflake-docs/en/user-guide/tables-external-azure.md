---
auto_generated: true
description: 'You can create external tables and refresh the external table metadata
  automatically by using Microsoft Azure Event Grid notifications for an Azure container.
  This operation synchronizes the metadata '
last_scraped: '2026-01-14T16:55:20.149362+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/tables-external-azure
title: Refresh external tables automatically for Azure Blob Storage | Snowflake Documentation
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

[Guides](../guides/README.md)[Databases, Tables, & Views](../guides/overview-db.md)[External Tables](tables-external-intro.md)[Automatic Refreshing](tables-external-auto.md)Azure Blob Storage

# Refresh external tables automatically for Azure Blob Storage[¶](#refresh-external-tables-automatically-for-azure-blob-storage "Link to this heading")

You can create external tables and refresh the external table metadata automatically by using [Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) notifications for an Azure container. This operation synchronizes the metadata with the latest set of associated files in the external stage and path.

The following list shows how the state of files in the path affects the table metadata:

> * New files in the path are added to the table metadata.
> * Changes to files in the path are updated in the table metadata.
> * Files no longer in the path are removed from the table metadata.

## Supported accounts, APIs, and schemas[¶](#supported-accounts-apis-and-schemas "Link to this heading")

Snowflake supports the following types of blob storage accounts:

* Blob storage
* Data Lake Storage Gen2
* General-purpose v2

Note

Only `Microsoft.Storage.BlobCreated` and `Microsoft.Storage.BlobDeleted` events trigger the refreshing of external table metadata. Adding new objects to blob storage triggers these events. Renaming a directory or object doesn’t trigger these events. Snowflake recommends that you only send supported events for external tables to reduce costs, event noise, and latency.

For cloud platform support, triggering automated external metadata refreshes using Azure Event Grid messages is supported by Snowflake accounts
hosted on Microsoft Azure (Azure).

Snowflake supports the following `Microsoft.Storage.BlobCreated` APIs:

* `CopyBlob`
* `PutBlob`
* `PutBlockList`
* `FlushWithClose`
* `SftpCommit`

Snowflake supports the following `Microsoft.Storage.BlobDeleted` APIs:

* `DeleteBlob`
* `DeleteFile`
* `SftpRemove`

For Data Lake Storage Gen2 storage accounts, `Microsoft.Storage.BlobCreated` events are triggered when clients use the `CreateFile`
and `FlushWithClose` operations. If the SSH File Transfer Protocol (SFTP) is used, `Microsoft.Storage.BlobCreated` events are triggered with `SftpCreate` and `SftpCommit` operations. The `CreateFile` or `SftpCreate` API alone does not indicate a commit of a file in the storage account. If the
`FlushWithClose` or `SftpCommit` message is not sent, Snowflake does not refresh the external table metadata.

Snowflake only supports the [Azure Event Grid event schema](https://learn.microsoft.com/en-us/azure/event-grid/event-schema); it doesn’t support the [CloudEvents schema with Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/cloud-event-schema).

External tables don’t support storage versioning (S3 versioning, Object Versioning in Google Cloud Storage, or versioning for Azure Storage).

## Prerequisites[¶](#prerequisites "Link to this heading")

Before you proceed, ensure you meet the following prerequisites:

> * A role that has the CREATE STAGE and CREATE EXTERNAL TABLE privileges on a schema.
> * Administrative access to Microsoft Azure. If you aren’t an Azure administrator, ask your Azure administrator to complete the steps in [Step 1: Configuring the Event Grid Subscription](#step-1-configuring-the-event-grid-subscription).
> * A notification integration so that you can refresh external tables automatically for Azure Blob Storage.

## Configure secure access to Cloud Storage[¶](#configure-secure-access-to-cloud-storage "Link to this heading")

Important

If you already configured secure access to the Azure blob storage container that stores your data files, you can skip this section, and proceed to [Step 1: Configuring the Event Grid Subscription](#step-1-configuring-the-event-grid-subscription).

You must configure a Snowflake storage integration object to delegate authentication responsibility for cloud storage to a Snowflake identity and access management (IAM) entity.

Note

Snowflake strongly recommends that you configure secure access so that you don’t need to supply IAM credentials when you access cloud storage. For information about additional storage access options, see [Configuring an Azure container for loading data](data-load-azure-config).

This section describes how to use storage integrations to allow Snowflake to read data from and write data to an Azure container referenced in an external (Azure) stage. Integrations are named, first-class Snowflake objects that avoid the need for passing explicit cloud provider credentials such as secret keys or access tokens. Integration objects store an Azure identity and access management (IAM) user ID called the *app registration*. An administrator in your organization grants this app the necessary permissions in the Azure account.

An integration must also specify containers (and optional paths) that limit the locations users can specify when creating external stages that use the integration.

Note

Completing the instructions in this section requires permissions in Azure to manage storage accounts. If you are not an Azure administrator, ask your Azure administrator to perform these tasks.

**In this Section:**

* [Step 1: Create a cloud storage integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake)
* [Step 2: Grant Snowflake Access to the Storage Locations](#step-2-grant-snowflake-access-to-the-storage-locations)

### Step 1: Create a cloud storage integration in Snowflake[¶](#step-1-create-a-cloud-storage-integration-in-snowflake "Link to this heading")

Create a storage integration using the [CREATE STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration) command. A storage integration is a Snowflake object that stores a generated service principal for your Azure cloud storage, along with an optional set of allowed or blocked storage locations (that is, containers). Cloud provider administrators in your organization grant permissions on the storage locations to the generated service principal. This option allows users to avoid supplying credentials when creating stages or loading data.

A single storage integration can support multiple external (that is, Azure) stages. The URL in the stage definition must align with the Azure containers (and optional paths) specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

```
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'AZURE'
  ENABLED = TRUE
  AZURE_TENANT_ID = '<tenant_id>'
  STORAGE_ALLOWED_LOCATIONS = ('azure://<account>.blob.core.windows.net/<container>/<path>/', 'azure://<account>.blob.core.windows.net/<container>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('azure://<account>.blob.core.windows.net/<container>/<path>/', 'azure://<account>.blob.core.windows.net/<container>/<path>/') ]
```

Copy

Where:

* `integration_name` is the name of the new integration.
* `tenant_id` is the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to. A storage integration can authenticate to only one tenant, so the allowed and blocked storage locations must refer to storage accounts that all belong this tenant.

  To find your tenant ID, sign in to the Azure portal and click Azure Active Directory » Properties. The tenant ID is displayed in the Tenant ID field.
* `container` is the name of an Azure container that stores your data files (for example, `mycontainer`). The STORAGE\_ALLOWED\_LOCATIONS and STORAGE\_BLOCKED\_LOCATIONS parameters allow or block access to these containers, respectively, when stages that reference this integration are created or modified.
* `path` is an optional path that can be used to provide granular control over logical directories in the container.

The following example creates an integration that explicitly limits external stages that use the integration to reference either of two containers and paths. In a later step, we will create an external stage that references one of these containers and paths. Multiple external stages that use this integration can reference the allowed containers and paths:

> ```
> CREATE STORAGE INTEGRATION azure_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'AZURE'
>   ENABLED = TRUE
>   AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
>   STORAGE_ALLOWED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer1/mypath1/', 'azure://myaccount.blob.core.windows.net/mycontainer2/mypath2/')
>   STORAGE_BLOCKED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer1/mypath1/sensitivedata/', 'azure://myaccount.blob.core.windows.net/mycontainer2/mypath2/sensitivedata/');
> ```
>
> Copy

### Step 2: Grant Snowflake Access to the Storage Locations[¶](#step-2-grant-snowflake-access-to-the-storage-locations "Link to this heading")

1. Execute the [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) command to retrieve the consent URL:

   ```
   DESC STORAGE INTEGRATION <integration_name>;
   ```

   Copy

   Where:

   * `integration_name` is the name of the integration you created in [Step 1: Create a Cloud Storage Integration in Snowflake](#step-1-create-a-cloud-storage-integration-in-snowflake).

   Note the values in the following columns:

   AZURE\_CONSENT\_URL:
   :   URL to the Microsoft permissions request page.

   AZURE\_MULTI\_TENANT\_APP\_NAME:
   :   Name of the Snowflake client application created for your account. In a later step in this section, you will need to grant this
       application the permissions necessary to obtain an access token on your allowed storage locations.
2. In a web browser, navigate to the URL in the AZURE\_CONSENT\_URL column. The page displays a Microsoft permissions request page.
3. Click the Accept button. This action allows the Azure service principal created for your Snowflake account to be granted an access token on specified resources inside your tenant. Obtaining an access token succeeds only if you grant the service principal the appropriate permissions on the container (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
4. Sign in to the Microsoft Azure portal.
5. Navigate to Azure Services » Storage Accounts. Click the name of the storage account you are granting the Snowflake service principal access to.
6. Click Access Control (IAM) » Add role assignment.
7. Select the desired role to grant to the Snowflake service principal:

   * `Storage Blob Data Reader` grants read access only. This allows loading data from files staged in the storage account.
   * `Storage Blob Data Contributor` grants read and write access. This allows loading data from or unloading data to files staged in
     the storage account. The role also allows executing the [REMOVE](../sql-reference/sql/remove) command to remove files staged in the
     storage account.
8. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the DESC STORAGE INTEGRATION output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   * It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft request page in this section. If the service principal is not available immediately, we recommend waiting an hour or two and then searching again.
   * If you delete the service principal, the storage integration stops working.

   [![Add role assignment in Azure Storage Console](../_images/azure-storage-add-role-assignment.png)](../_images/azure-storage-add-role-assignment.png)
9. Click the Review + assign button.

   Note

   * According to the Microsoft Azure documentation, role assignments may take up to five minutes to propagate.
   * Snowflake caches the temporary credentials for a period that cannot exceed the 60 minute expiration time. If you revoke access from Snowflake, users might be able to list files and load data from the cloud storage location until the cache expires.

Note

You can use the [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](../sql-reference/functions/system_validate_storage_integration)
function to validate the configuration for your storage integration.

## Configuring Automation With Azure Event Grid[¶](#configuring-automation-with-azure-event-grid "Link to this heading")

### Step 1: Configuring the Event Grid Subscription[¶](#step-1-configuring-the-event-grid-subscription "Link to this heading")

This section describes how to set up an Event Grid subscription for Azure Storage events using the Azure CLI. For more information about the steps described in this section, see the following articles in the Azure documentation:

* <https://docs.microsoft.com/en-us/azure/event-grid/custom-event-to-queue-storage>
* <https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-quickstart>

#### Create a resource group[¶](#create-a-resource-group "Link to this heading")

An Event Grid *topic* provides an endpoint where the source (that is, Azure Storage) sends events. A topic is used for a collection of related events. Event Grid topics are Azure resources, and must be placed in an Azure resource group.

Execute the following command to create a resource group:

```
az group create --name <resource_group_name> --location <location>
```

Copy

Where:

* `resource_group_name` is the name of the new resource group.
* `location` is the location, or *region* in Snowflake terminology, of your Azure Storage account.

#### Enable the Event Grid resource provider[¶](#enable-the-event-grid-resource-provider "Link to this heading")

Execute the following command to register the Event Grid resource provider. Note that this step is only required if you have not previously used Event Grid with your Azure account:

```
az provider register --namespace Microsoft.EventGrid
az provider show --namespace Microsoft.EventGrid --query "registrationState"
```

Copy

#### Create a storage account for data files[¶](#create-a-storage-account-for-data-files "Link to this heading")

Execute the following command to create a storage account to store your data files. This account must be either a Blob storage (that is, a `BlobStorage` kind) or GPv2 (that is, a `StorageV2` kind) account, because only these two account types support event messages.

Note

If you already have a Blob storage or GPv2 account, you can use that account instead.

For example, create a Blob storage account:

```
az storage account create --resource-group <resource_group_name> --name <storage_account_name> --sku Standard_LRS --location <location> --kind BlobStorage --access-tier Hot
```

Copy

Where:

* `resource_group_name` is the name of the resource group you created in [Create a Resource Group](#create-a-resource-group).
* `storage_account_name` is the name of the new storage account.
* `location` is the location of your Azure Storage account.

#### Create a storage account for the storage queue[¶](#create-a-storage-account-for-the-storage-queue "Link to this heading")

Execute the following command to create a storage account to host your storage queue. This account must be a GPv2 account, because only this kind of account supports event messages to a storage queue.

Note

If you already have a GPv2 account, you can use that account to host both your data files and your storage queue.

For example, create a GPv2 account:

```
az storage account create --resource-group <resource_group_name> --name <storage_account_name> --sku Standard_LRS --location <location> --kind StorageV2
```

Copy

Where:

* `resource_group_name` is the name of the resource group you created in [Create a resource group](#create-a-resource-group).
* `storage_account_name` is the name of the new storage account.
* `location` is the location of your Azure Storage account.

#### Create a storage queue[¶](#create-a-storage-queue "Link to this heading")

A single Azure Queue Storage queue can collect the event messages for many Event Grid subscriptions. For best performance, Snowflake recommends creating a single storage queue to accommodate all of your subscriptions related to Snowflake.

Execute the following command to create a storage queue. A storage queue stores a set of messages, in this case event messages from Event Grid:

```
az storage queue create --name <storage_queue_name> --account-name <storage_account_name>
```

Copy

Where:

* `storage_queue_name` is the name of the new storage queue.
* `storage_account_name` is the name of the storage account you created in [Create a storage account for the storage queue](#create-a-storage-account-for-the-storage-queue).

#### Export the storage account and queue IDs for Reference[¶](#export-the-storage-account-and-queue-ids-for-reference "Link to this heading")

Execute the following commands to set environment variables for the storage account and queue IDs that will be requested later in these instructions:

* Linux or macOS:

  ```
  export storageid=$(az storage account show --name <data_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  export queuestorageid=$(az storage account show --name <queue_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  export queueid="$queuestorageid/queueservices/default/queues/<storage_queue_name>"
  ```

  Copy
* Windows:

  ```
  set storageid=$(az storage account show --name <data_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  set queuestorageid=$(az storage account show --name <queue_storage_account_name> --resource-group <resource_group_name> --query id --output tsv)
  set queueid="%queuestorageid%/queueservices/default/queues/<storage_queue_name>"
  ```

  Copy

Where:

* `data_storage_account_name` is the name of the storage account you created in [Create a storage account for data files](#create-a-storage-account-for-data-files).
* `queue_storage_account_name` is the name of the storage account you created in [Create a storage account for the storage queue](#create-a-storage-account-for-the-storage-queue).
* `resource_group_name` is the name of the resource group you created in [Create a resource group](#create-a-resource-group).
* `storage_queue_name` is the name of the storage queue you created in [Create a storage queue](#create-a-storage-queue).

#### Install the Event Grid extension[¶](#install-the-event-grid-extension "Link to this heading")

Execute the following command to install the Event Grid extension for Azure CLI:

```
az extension add --name eventgrid
```

Copy

#### Create the Event Grid subscription[¶](#create-the-event-grid-subscription "Link to this heading")

Execute the following command to create the Event Grid subscription. Subscribing to a topic informs Event Grid which events to track:

* Linux or macOS:

  ```
  az eventgrid event-subscription create \
  --source-resource-id $storageid \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint $queueid \
  --advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
  ```

  Copy
* Windows:

  ```
  az eventgrid event-subscription create \
  --source-resource-id %storageid% \
  --name <subscription_name> --endpoint-type storagequeue \
  --endpoint %queueid% \
  -advanced-filter data.api stringin CopyBlob PutBlob PutBlockList FlushWithClose SftpCommit DeleteBlob DeleteFile SftpRemove
  ```

  Copy

Where:

* `storageid` and `queueid` are the storage account and queue ID environment variables you set in [Export the storage account and queue IDs for reference](#export-the-storage-account-and-queue-ids-for-reference).
* `subscription_name` is the name of the new Event Grid subscription.

### Step 2: Creating the notification integration[¶](#step-2-creating-the-notification-integration "Link to this heading")

A *notification integration* is a Snowflake object that provides an interface between Snowflake and a third-party cloud message queuing service such as Azure Event Grid.

Note

A single notification integration supports a single Azure Storage queue. Referencing the same storage queue in multiple notification integrations can result in missing data in target tables because event notifications are split between notification integrations.

#### Retrieve the storage queue URL and tenant ID[¶](#retrieve-the-storage-queue-url-and-tenant-id "Link to this heading")

1. Sign in to the Microsoft Azure portal.
2. Navigate to Storage account » Queue service » Queues. Record the URL for the queue you created in [Create a storage queue](#create-a-storage-queue) for reference later. The URL has the following format:

   ```
   https://<storage_account_name>.queue.core.windows.net/<storage_queue_name>
   ```

   Copy
3. Navigate to Azure Active Directory » Properties. Record the Tenant ID value for reference later. The directory ID, or *tenant ID*, is needed to generate the consent URL that grants Snowflake access to the Event Grid subscription.

#### Create the notification integration[¶](#create-the-notification-integration "Link to this heading")

Create a notification integration using the
[CREATE NOTIFICATION INTEGRATION](../sql-reference/sql/create-notification-integration-queue-inbound-azure) command.

Note

* Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.
* The Azure service principal for notification integrations is different from the service principal created for storage integrations.

```
CREATE NOTIFICATION INTEGRATION <integration_name>
  ENABLED = true
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = '<queue_URL>'
  AZURE_TENANT_ID = '<directory_ID>';
```

Copy

Where:

* `integration_name` is the name of the new integration.
* `queue_URL` and `directory_ID` are the queue URL and tenant ID you recorded in [Retrieve the storage queue URL and tenant ID](#retrieve-the-storage-queue-url-and-tenant-id).

For example:

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  ENABLED = true
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myqueue.queue.core.windows.net/mystoragequeue'
  AZURE_TENANT_ID = 'a123bcde-1234-5678-abc1-9abc12345678';
```

Copy

#### Grant Snowflake access to the storage queue[¶](#grant-snowflake-access-to-the-storage-queue "Link to this heading")

Note that specific steps in this section require a local installation of the Azure CLI.

1. Execute the [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) command to retrieve the consent URL:

   ```
   DESC NOTIFICATION INTEGRATION <integration_name>;
   ```

   Copy

   Where:

   * `integration_name` is the name of the integration you created in [Create the notification integration](#create-the-notification-integration).

   Note the values in the following columns:

   AZURE\_CONSENT\_URL:
   :   URL to the Microsoft permissions request page.

   AZURE\_MULTI\_TENANT\_APP\_NAME:
   :   Name of the Snowflake client application created for your account. In a later step in this section, you will need to grant this
       application the permissions necessary to obtain an access token on your allowed topic.
2. In a web browser, navigate to the URL in the AZURE\_CONSENT\_URL column. The page displays a Microsoft permissions request page.
3. Click the Accept button. This action allows the Azure service principal created for your Snowflake account to obtain an access
   token on any resource inside your tenant. Obtaining an access token succeeds only if you grant the service principal the appropriate
   permissions on the container (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
4. Sign in to the Microsoft Azure portal.
5. Navigate to Azure Active Directory » Enterprise applications. Verify that the Snowflake application identifier you
   recorded in Step 2 in this section is listed.

   Important

   If you delete the Snowflake application in Azure Active Directory at a later time, the notification integration stops working.
6. Navigate to Queues » `storage_queue_name`, where `storage_queue_name` is the name of the storage queue you created in [Create a storage queue](#create-a-storage-queue).
7. Click Access Control (IAM) » Add role assignment.
8. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property in the DESC NOTIFICATION
   INTEGRATION output (in Step 1). Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   * It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft request page in
     this section. If the service principal is not available immediately, we recommend waiting an hour or two and then searching again.
   * If you delete the service principal, the notification integration stops working.
9. Grant the Snowflake app the following permissions:

   * Role: Storage Queue Data Message Processor (the minimum required role), or Storage Queue Data Contributor.
   * Assign access to: Azure AD user, group, or service principal.
   * Select: The `appDisplayName` value.

   The Snowflake application identifier should now be listed under Storage Queue Data Message Processor or Storage Queue Data Contributor (on the same dialog).

### (Optional) Step 3: Creating a stage[¶](#optional-step-3-creating-a-stage "Link to this heading")

Create an external stage that references your Azure container by using the [CREATE STAGE](../sql-reference/sql/create-stage) command. Snowflake reads your staged data files into the external table metadata. Alternatively, you can use an existing external stage.

Note

* To configure secure access to the cloud storage location, see [Configure Secure Access to Cloud Storage](#configure-secure-access-to-cloud-storage) earlier in this topic.
* To reference a storage integration in the CREATE STAGE statement, the role must have the USAGE privilege on the storage integration object.

The following example creates a stage named `mystage` in the active schema for the user session. The cloud storage URL includes the path `files`. The stage references a storage integration named `my_storage_int`:

> ```
> USE SCHEMA mydb.public;
>
> CREATE STAGE mystage
>   URL='azure://myaccount.blob.core.windows.net/mycontainer/files/'
>   STORAGE_INTEGRATION = my_storage_int;
> ```
>
> Copy

Note

Use the `blob.core.windows.net` endpoint for all supported types of Azure blob storage accounts, including Data Lake Storage Gen2.

### Step 4: Create an external table[¶](#step-4-create-an-external-table "Link to this heading")

Create an external table by using the [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table) command.

For example, create an external table in the `mydb.public` schema that reads JSON data from files staged in the `mystage` stage with the `path1/` path:

```
CREATE OR REPLACE EXTERNAL TABLE ext_table
 INTEGRATION = 'MY_NOTIFICATION_INT'
 WITH LOCATION = @mystage/path1/
 FILE_FORMAT = (TYPE = JSON);
```

Copy

The INTEGRATION parameter references the `my_notification_int` notification integration you created in [Step 2: Creating the Notification Integration](#step-2-creating-the-notification-integration). You must enter the integration name in all uppercase letters.

When a notification integration is provided, the `AUTO_REFRESH` parameter is `TRUE` by default. If there is no notification integration, AUTO\_REFRESH is always `FALSE`.

After you complete this step, the external stage with auto-refresh is configured.

When new or updated data files are added to the Azure container, the event notification informs Snowflake to scan them into the external table metadata.

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

This step synchronizes the metadata with the list of files in the stage and path in the external table definition. Also, this step ensures that the external table can read the data files in the specified stage and path, and that no files were missed in the external table definition.

If the list of files in the `file` column doesn’t match your expectations, verify the paths in the external table definition and external stage definition. Any path in the external table definition is appended to any path specified in the stage definition. For more information, see [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table).

Important

If this step is not completed successfully at least once after the external table is created, querying the external table returns no results until an Event Grid notification refreshes the external table metadata automatically for the first time.

This step ensures that the metadata is synchronized with any changes to the file list that occurred after Step 4. Thereafter, Event Grid notifications trigger the metadata refresh automatically.

### Step 6: Configure security[¶](#step-6-configure-security "Link to this heading")

For each additional role that you will use to query the external table, grant sufficient access control privileges on the various objects (that is, the databases, schemas, stage, and table) by using [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege):

| Object | Privilege | Notes |
| --- | --- | --- |
| Database | USAGE |  |
| Schema | USAGE |  |
| Named stage | USAGE , READ |  |
| Named file format | USAGE | Optional; only needed if the stage you created in [(Optional) Step 3: Creating a stage](#optional-step-3-creating-a-stage) references a named file format. |
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

1. [Supported accounts, APIs, and schemas](#supported-accounts-apis-and-schemas)
2. [Prerequisites](#prerequisites)
3. [Configure secure access to Cloud Storage](#configure-secure-access-to-cloud-storage)
4. [Configuring Automation With Azure Event Grid](#configuring-automation-with-azure-event-grid)

Related content

1. [CREATE STORAGE INTEGRATION](/user-guide/../sql-reference/sql/create-storage-integration)
2. [DESCRIBE INTEGRATION](/user-guide/../sql-reference/sql/desc-integration)
3. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/user-guide/../sql-reference/functions/system_validate_storage_integration)
4. [CREATE STAGE](/user-guide/../sql-reference/sql/create-stage)
5. [CREATE EXTERNAL TABLE](/user-guide/../sql-reference/sql/create-external-table)