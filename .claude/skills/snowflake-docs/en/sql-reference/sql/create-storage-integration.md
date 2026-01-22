---
auto_generated: true
description: Creates a new storage integration in the account or replaces an existing
  integration.
last_scraped: '2026-01-14T16:56:03.667366+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration
title: CREATE STORAGE INTEGRATION | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Integrations](../commands-integration.md)CREATE STORAGE INTEGRATION

# CREATE STORAGE INTEGRATION[¶](#create-storage-integration "Link to this heading")

Creates a new storage integration in the account or replaces an existing integration.

A storage integration is a Snowflake object that stores a generated identity and access management (IAM) entity for your external
cloud storage, along with an optional set of allowed or blocked storage locations (Amazon S3, Google Cloud Storage, or Microsoft Azure).
Cloud provider administrators in your organization grant permissions on the storage locations to the generated entity. This option
allows users to avoid supplying credentials when creating stages or when loading or unloading data.

A single storage integration can support multiple external stages. The URL in the stage definition must align with the storage location
specified for the STORAGE\_ALLOWED\_LOCATIONS parameter.

Note

* If your cloud storage is located on a different cloud platform from your Snowflake
  account, the storage location must be in the public cloud and not a virtual private environment.

  Snowflake charges a per-byte fee when you unload data from Snowflake into an external stage in a different
  [region](../../user-guide/intro-regions) or different cloud provider. For details, see the
  [pricing page](https://www.snowflake.com/pricing/).
* Accessing cloud storage in a [government region](../../user-guide/intro-regions.html#label-us-gov-regions) using a storage integration is limited to Snowflake
  accounts hosted in the same government region.

  Similarly, if you need to access cloud storage in a region in China, you can use a storage integration only from a Snowflake
  account hosted in the same region in China.

  In these cases, use the CREDENTIALS parameter in the [CREATE STAGE](create-stage) command (rather than using a storage
  integration) to provide the credentials for authentication.

See also:
:   [ALTER STORAGE INTEGRATION](alter-storage-integration) , [DROP INTEGRATION](drop-integration) , [SHOW INTEGRATIONS](show-integrations)

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] STORAGE INTEGRATION [IF NOT EXISTS]
  <name>
  TYPE = EXTERNAL_STAGE
  cloudProviderParams
  ENABLED = { TRUE | FALSE }
  STORAGE_ALLOWED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] )
  [ STORAGE_BLOCKED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

Copy

Where:

> ```
> cloudProviderParams (for Amazon S3) ::=
>   STORAGE_PROVIDER = 'S3'
>   STORAGE_AWS_ROLE_ARN = '<iam_role>'
>   [ STORAGE_AWS_EXTERNAL_ID = '<external_id>' ]
>   [ STORAGE_AWS_OBJECT_ACL = 'bucket-owner-full-control' ]
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```
>
> Copy
>
> ```
> cloudProviderParams (for Google Cloud Storage) ::=
>   STORAGE_PROVIDER = 'GCS'
> ```
>
> Copy
>
> ```
> cloudProviderParams (for Microsoft Azure) ::=
>   STORAGE_PROVIDER = 'AZURE'
>   AZURE_TENANT_ID = '<tenant_id>'
>   [ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
> ```
>
> Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   String that specifies the identifier (i.e. name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

`TYPE = EXTERNAL_STAGE`
:   Specify the type of integration:

    * `EXTERNAL_STAGE`: Creates an interface between Snowflake and an external cloud storage location.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this storage integration is available for usage in stages.

    > * `TRUE` allows users to create new stages that reference this integration. Existing stages that reference this integration
    >   function normally.
    > * `FALSE` prevents users from creating new stages that reference this integration. Existing stages that reference this integration
    >   cannot access the storage location in the stage definition.

`STORAGE_ALLOWED_LOCATIONS = ( 'cloud_specific_url' )`
:   Explicitly limits external stages that use the integration to reference one or more storage locations (i.e. S3 bucket, GCS bucket, or
    Azure container). Supports a comma-separated list of URLs for existing buckets and, optionally, paths used to store data files for
    loading/unloading. Alternatively supports the `*` wildcard, meaning “allow access to all buckets and/or paths”.

    **Amazon S3**

    > `STORAGE_ALLOWED_LOCATIONS = ( 'protocol://bucket/path/' [ , 'protocol://bucket/path/' ... ]  )`
    >
    > > * `protocol` is one of the following:
    > >
    > >   + `s3` refers to S3 storage in public AWS regions outside of China.
    > >   + `s3china` refers to S3 storage in public AWS regions in China.
    > >   + `s3gov` refers to S3 storage in [government regions](../../user-guide/intro-regions.html#label-us-gov-regions).
    > > * `bucket` is the name of an S3 bucket that stores your data files (e.g. `mybucket`).
    > > * `path` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with
    > >   a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud
    > >   storage services.

    **Google Cloud Storage**

    > `STORAGE_ALLOWED_LOCATIONS = ( 'gcs://bucket/path/' [ , 'gcs://bucket/path/' ... ] )`
    >
    > > * `bucket` is the name of a GCS bucket that stores your data files (e.g. `mybucket`).
    > > * `path` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with
    > >   a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud
    > >   storage services.

    **Microsoft Azure**

    > `STORAGE_ALLOWED_LOCATIONS = ( 'azure://account.blob.core.windows.net/container/path/' [ , 'azure://account.blob.core.windows.net/container/path/' ... ] )`
    >
    > > * `account` is the name of the Azure storage account (e.g. `myaccount`). Use the `blob.core.windows.net` endpoint
    > >   for all supported types of Azure blob storage accounts, including Data Lake Storage Gen2.
    > > * `container` is the name of a Azure blob storage container that stores your data files (e.g. `mycontainer`).
    > > * `path` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with
    > >   a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud
    > >   storage services.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`STORAGE_BLOCKED_LOCATIONS = ( 'cloud_specific_url' )`
:   Explicitly prohibits external stages that use the integration from referencing one or more storage locations (i.e. S3 buckets or
    GCS buckets). Supports a comma-separated list of URLs for existing storage locations and, optionally, paths used to store data files
    for loading/unloading. Commonly used when STORAGE\_ALLOWED\_LOCATIONS is set to the `*` wildcard, allowing access to all buckets
    in your account except for blocked storage locations and, optionally, paths.

    Note

    Make sure to enclose only individual cloud storage location URLs in quotes. If you enclose the entire
    `STORAGE_BLOCKED_LOCATIONS` value in quotes, the value is invalid. As a result, the `STORAGE_BLOCKED_LOCATIONS`
    parameter setting is ignored when users create stages that reference the storage integration.

    **Amazon S3**

    > `STORAGE_BLOCKED_LOCATIONS = ( 'protocol://bucket/path/' [ , 'protocol://bucket/path/' ... ]  )`
    >
    > > * `protocol` is one of the following:
    > >
    > >   + `s3` refers to S3 storage in public AWS regions outside of China.
    > >   + `s3china` refers to S3 storage in public AWS regions in China.
    > >   + `s3gov` refers to S3 storage in [government regions](../../user-guide/intro-regions.html#label-us-gov-regions).
    > > * `bucket` is the name of an S3 bucket that stores your data files (e.g. `mybucket`).
    > > * `path` is an optional path (or *directory*) in the bucket that further limits access to the data files.

    **Google Cloud Storage**

    > `STORAGE_BLOCKED_LOCATIONS = ( 'gcs://bucket/path/' [ , 'gcs://bucket/path/' ... ] )`
    >
    > > * `bucket` is the name of a GCS bucket that stores your data files (e.g. `mybucket`).
    > > * `path` is an optional path (or *directory*) in the bucket that further limits access to the data files.

    **Microsoft Azure**

    > `STORAGE_BLOCKED_LOCATIONS = ( 'azure://account.blob.core.windows.net/container/path/' [ , 'azure://account.blob.core.windows.net/container/path/' ... ] )`
    >
    > > * `account` is the name of the Azure storage account (e.g. `myaccount`).
    > > * `container` is the name of a Azure blob storage container that stores your data files (e.g. `mycontainer`).
    > > * `path` is an optional path (or *directory*) in the bucket that further limits access to the data files.

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Cloud provider parameters (`cloudProviderParams`)[¶](#cloud-provider-parameters-cloudproviderparams "Link to this heading")

**Amazon S3**

> `STORAGE_PROVIDER = '{ S3 | S3CHINA | S3GOV }'`
> :   Specifies the cloud storage provider that stores your data files:
>
>     * `'S3'`: S3 storage in public AWS regions outside of China.
>     * `'S3CHINA'`: S3 storage in public AWS regions in China.
>     * `'S3GOV'`: S3 storage in AWS government regions.
>
> `STORAGE_AWS_ROLE_ARN = 'iam_role'`
> :   Specifies the Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges on the S3 bucket
>     containing your data files. For more information, see [Configuring secure access to Amazon S3](../../user-guide/data-load-s3-config).

> `STORAGE_AWS_EXTERNAL_ID = 'external_id'`
> :   Optionally specifies an external ID that Snowflake uses to establish a trust relationship with AWS.
>     You must specify the same external ID in the trust policy of the IAM role
>     that you configured for this storage integration. For more information,
>     see [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).
>
>     If you don’t specify a value for this parameter,
>     Snowflake automatically generates an external ID when you create the storage integration.
>
> `STORAGE_AWS_OBJECT_ACL = 'bucket-owner-full-control'`
> :   Enables support for AWS access control lists (ACLs) to grant the bucket owner full control. Files created in Amazon S3 buckets from
>     unloaded table data are owned by an AWS Identity and Access Management (IAM) role. ACLs support the use case where IAM roles in one
>     AWS account are configured to access S3 buckets in one or more other AWS accounts. Without ACL support, users in the bucket-owner
>     accounts could not access the data files unloaded to an external (S3) stage using a storage integration.
>
>     When users unload Snowflake table data to data files in an S3 stage using [COPY INTO <location>](copy-into-location), the unload
>     operation applies an ACL to the unloaded data files. The data files apply the `"s3:x-amz-acl":"bucket-owner-full-control"`
>     privilege to the files, granting the S3 bucket owner full control over them.
>
> `USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
> :   Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter, see
>     [Private connectivity to external stages for Amazon Web Services](../../user-guide/data-load-aws-private).

**Google Cloud Storage**

> `STORAGE_PROVIDER = 'GCS'`
> :   Specifies the cloud storage provider that stores your data files.

**Microsoft Azure**

> `STORAGE_PROVIDER = 'AZURE'`
> :   Specifies the cloud storage provider that stores your data files.
>
> `AZURE_TENANT_ID = 'tenant_id'`
> :   Specifies the ID for your Office 365 tenant that the allowed and blocked storage accounts belong to. A storage integration can
>     authenticate to only one tenant, and so the allowed and blocked storage locations must refer to storage accounts that all belong
>     this tenant.
>
>     To find your tenant ID, log into the Azure portal and click Azure Active Directory » Properties. The tenant ID
>     is displayed in the Tenant ID field.
>
> `USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
> :   Specifies whether to use outbound private connectivity to harden your security posture. For information about using this parameter,
>     see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](../../user-guide/data-load-azure-private).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## Usage notes[¶](#usage-notes "Link to this heading")

Caution

Recreating a storage integration (using CREATE OR REPLACE STORAGE INTEGRATION) breaks the association between the storage integration
and any stage that references it. This is because a stage links to a storage integration using a hidden ID rather than the name of the
storage integration. Behind the scenes, the CREATE OR REPLACE syntax drops the object and recreates it with a different hidden ID.

If you must recreate a storage integration after it has been linked to one or more stages, you must reestablish the association between
each stage and the storage integration by executing [ALTER STAGE](alter-stage) `stage_name` SET STORAGE\_INTEGRATION =
`storage_integration_name`, where:

* `stage_name` is the name of the stage.
* `storage_integration_name` is the name of the storage integration.

* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).

* The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
* CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples[¶](#examples "Link to this heading")

The following example creates an integration that explicitly limits external stages that use the integration to reference either of
two buckets and paths:

**Amazon S3**

> ```
> CREATE STORAGE INTEGRATION s3_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'S3'
>   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('s3://mybucket1/path1/', 's3://mybucket2/path2/');
> ```
>
> Copy
>
> If the S3 storage is in a public AWS region in China, use `'S3CHINA'` for the STORAGE\_PROVIDER parameter and
> `s3china://` protocol in STORAGE\_ALLOWED\_LOCATIONS.

**Google Cloud Storage**

> ```
> CREATE STORAGE INTEGRATION gcs_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'GCS'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('gcs://mybucket1/path1/', 'gcs://mybucket2/path2/');
> ```
>
> Copy

**Microsoft Azure**

> ```
> CREATE STORAGE INTEGRATION azure_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'AZURE'
>   ENABLED = TRUE
>   AZURE_TENANT_ID = '<tenant_id>'
>   STORAGE_ALLOWED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer/path1/', 'azure://myaccount.blob.core.windows.net/mycontainer/path2/');
> ```
>
> Copy

The following example creates an integration that allows external stages that use the integration to reference any bucket and
path in your account except for those that are explicitly blocked:

**Amazon S3**

> ```
> CREATE STORAGE INTEGRATION s3_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'S3'
>   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('*')
>   STORAGE_BLOCKED_LOCATIONS = ('s3://mybucket3/path3/', 's3://mybucket4/path4/');
> ```
>
> Copy
>
> If the S3 storage is in a public AWS region in China, use `'S3CHINA'` for the STORAGE\_PROVIDER parameter and
> `s3china://` protocol in STORAGE\_BLOCKED\_LOCATIONS.

**Google Cloud Storage**

> ```
> CREATE STORAGE INTEGRATION gcs_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'GCS'
>   ENABLED = TRUE
>   STORAGE_ALLOWED_LOCATIONS = ('*')
>   STORAGE_BLOCKED_LOCATIONS = ('gcs://mybucket3/path3/', 'gcs://mybucket4/path4/');
> ```
>
> Copy

**Microsoft Azure**

> ```
> CREATE STORAGE INTEGRATION azure_int
>   TYPE = EXTERNAL_STAGE
>   STORAGE_PROVIDER = 'AZURE'
>   ENABLED = TRUE
>   AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
>   STORAGE_ALLOWED_LOCATIONS = ('*')
>   STORAGE_BLOCKED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer/path3/', 'azure://myaccount.blob.core.windows.net/mycontainer/path4/');
> ```
>
> Copy

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

On this page

1. [Syntax](#syntax)
2. [Required parameters](#required-parameters)
3. [Optional parameters](#optional-parameters)
4. [Cloud provider parameters (cloudProviderParams)](#cloud-provider-parameters-cloudproviderparams)
5. [Access control requirements](#access-control-requirements)
6. [Usage notes](#usage-notes)
7. [Examples](#examples)

Related content

1. [Snowflake storage integration for AWS](/sql-reference/sql/../../user-guide/data-load-s3-config-storage-integration)
2. [Snowflake storage integration for Google Cloud Storage](/sql-reference/sql/../../user-guide/data-load-gcs-config)
3. [Snowflake storage integration for Microsoft Azure](/sql-reference/sql/../../user-guide/data-load-azure-config)
4. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/sql/../functions/system_validate_storage_integration)
5. [External stages](/sql-reference/sql/../../user-guide/data-load-overview#label-data-load-overview-external-stages)
6. [Load data into Snowflake](/sql-reference/sql/../../guides-overview-loading-data)