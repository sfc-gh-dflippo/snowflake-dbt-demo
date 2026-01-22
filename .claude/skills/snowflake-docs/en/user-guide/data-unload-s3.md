---
auto_generated: true
description: If you already have a Amazon Web Services (AWS) account and use S3 buckets
  for storing and managing your data files, you can make use of your existing buckets
  and folder paths when unloading data from
last_scraped: '2026-01-14T16:57:47.353227+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-unload-s3
title: Unloading into Amazon S3 | Snowflake Documentation
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

      * [Overview](data-unload-overview.md)
      * [Features](intro-summary-unloading.md)
      * [Considerations](data-unload-considerations.md)
      * [Preparing to Unload Data](data-unload-prepare.md)
      * [Unloading into a Snowflake Stage](data-unload-snowflake.md)
      * [Unloading into Amazon S3](data-unload-s3.md)
      * [Unloading into Google Cloud Storage](data-unload-gcs.md)
      * [Unloading into Microsoft Azure](data-unload-azure.md)
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

[Guides](../guides/README.md)Data engineering[Data Unloading](../guides/overview-unloading-data.md)Unloading into Amazon S3

# Unloading into Amazon S3[¶](#unloading-into-amazon-s3 "Link to this heading")

If you already have a Amazon Web Services (AWS) account and use S3 buckets for storing and managing your data files, you can make use of your existing buckets and folder paths when unloading data from
Snowflake tables. This topic describes how to use the COPY command to unload data from a table into an Amazon S3 bucket. You can then download the unloaded data files to your local file system.

As illustrated in the diagram below, unloading data to an S3 bucket is performed in two steps:

Step 1:
:   Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to copy the data from the Snowflake database table into one or more files in an S3 bucket. In the command, you specify a named
    external stage object that references the S3 bucket (recommended) or you can choose to unload directly to the bucket by specifying the URI and either the storage integration or the security credentials (if required) for the bucket.

    Regardless of the method you use, this step requires a running, current virtual warehouse for the session if you execute the command
    manually or within a script. The warehouse provides the compute resources to write rows from the table.

Step 2:
:   Use the interfaces/tools provided by Amazon to download the files from the S3 bucket.

![Unloading data to S3](../_images/data-unload-s3.png)

Tip

The instructions in this set of topics assume you have read [Preparing to unload data](data-unload-prepare) and have created a named file format, if desired.

Before you begin, you may also want to read [Data unloading considerations](data-unload-considerations) for best practices, tips, and other guidance.

## Allowing the Amazon Virtual Private Cloud IDs[¶](#allowing-the-amazon-virtual-private-cloud-ids "Link to this heading")

If an AWS administrator in your organization has not explicitly granted Snowflake access to your AWS S3 storage account, you can do so now.
Follow the steps in [Allowing the Virtual Private Cloud IDs](data-load-s3-allow) in the data loading configuration instructions.

## Configuring an S3 bucket for unloading data[¶](#configuring-an-s3-bucket-for-unloading-data "Link to this heading")

Snowflake requires the following permissions on an S3 bucket and folder to create new files in the folder (and any sub-folders):

* `s3:DeleteObject`
* `s3:PutObject`

As a best practice, Snowflake recommends configuring a storage integration object to delegate authentication responsibility for external cloud storage to a Snowflake identity and access management (IAM) entity.

For configuration instructions, see [Configuring secure access to Amazon S3](data-load-s3-config).

## Configuring support for Amazon S3 access control lists — *Optional*[¶](#configuring-support-for-amazon-s3-access-control-lists-optional "Link to this heading")

Snowflake storage integrations support AWS access control lists (ACLs) to grant the bucket owner full control. Files created in Amazon S3 buckets from unloaded table data are owned by an AWS Identity and Access Management (IAM) role. ACLs support the use case where IAM roles in one AWS account are configured to access S3 buckets in one or more other AWS accounts. Without ACL support, users in the bucket-owner accounts could not access the data files unloaded to an external (S3) stage using a storage integration. When users unload Snowflake table data to data files in an external (S3) stage using [COPY INTO <location>](../sql-reference/sql/copy-into-location), the unload operation applies an ACL to the unloaded data files. The data files apply the `"s3:x-amz-acl":"bucket-owner-full-control"` privilege to the files, granting the S3 bucket owner full control over them.

Enable ACL support in the storage integration for an S3 stage via the optional `STORAGE_AWS_OBJECT_ACL = 'bucket-owner-full-control'` parameter. A storage integration is a Snowflake object that stores a generated identity and access management (IAM) user for your S3 cloud storage, along with an optional set of allowed or blocked storage locations (i.e. S3 buckets). An AWS administrator in your organization adds the generated IAM user to the role to grant Snowflake permissions to access specified S3 buckets. This feature allows users to avoid supplying credentials when creating stages or loading data. An administrator can set the `STORAGE_AWS_OBJECT_ACL` parameter when creating a storage integration (using [CREATE STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration)) or later (using [ALTER STORAGE INTEGRATION](../sql-reference/sql/alter-storage-integration)).

## Unloading data into an external stage[¶](#unloading-data-into-an-external-stage "Link to this heading")

External stages are named database objects that provide the greatest degree of flexibility for data unloading. Because they are database objects, privileges for named stages can be granted to any role.

You can create an external named stage using either Snowsight or SQL:

> Snowsight:
> :   In the navigation menu, select Catalog » Database Explorer » *<db\_name>* » Stages » Create
>
> SQL:
> :   [CREATE STAGE](../sql-reference/sql/create-stage)

### Creating a named stage[¶](#creating-a-named-stage "Link to this heading")

Snowflake uses multipart uploads when uploading to Amazon S3 and Google Cloud Storage.
This process might leave incomplete uploads in the storage location for your external stage.

To prevent incomplete uploads from accumulating, we recommend that you set a lifecycle rule.
For instructions, see the [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
or [Google Cloud Storage](https://cloud.google.com/storage/docs/lifecycle#abort-mpu) documentation.

The following example creates an external stage named `my_ext_unload_stage` using an S3 bucket named `unload` with a
folder path named `files`. The stage accesses the S3 bucket using an existing storage integration named `s3_int`.

The stage references a named file format object called `my_csv_unload_format`. For instructions, see [Preparing to unload data](data-unload-prepare).

```
CREATE OR REPLACE STAGE my_ext_unload_stage URL='s3://unload/files/'
  STORAGE_INTEGRATION = s3_int
  FILE_FORMAT = my_csv_unload_format;
```

Copy

### Unloading data to the named stage[¶](#unloading-data-to-the-named-stage "Link to this heading")

1. Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to unload data from a table into an S3 bucket using the external stage.

   The following example uses the `my_ext_unload_stage` stage to unload all the rows in the `mytable` table into one or more files into the S3 bucket. A `d1` filename prefix is applied
   to the files:

   ```
   COPY INTO @my_ext_unload_stage/d1 from mytable;
   ```

   Copy
2. Use the S3 console (or equivalent client application) to retrieve the objects (i.e. files generated by the command) from the bucket.

## Unloading data directly into an S3 bucket[¶](#unloading-data-directly-into-an-s3-bucket "Link to this heading")

1. Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to unload data from a table directly into a specified S3 bucket. This option works well for ad hoc unloading, when you aren’t planning regular data unloading with the same table and bucket parameters.

   You must specify the URI for the S3 bucket and the storage integration or credentials for accessing the bucket in the COPY command.

   The following example unloads all the rows in the `mytable` table into one or more files with the folder path prefix `unload/` in the `mybucket` S3 bucket:

   ```
   COPY INTO 's3://mybucket/unload/'
     FROM mytable
     STORAGE_INTEGRATION = s3_int;
   ```

   Copy

   Note

   In this example, the referenced S3 bucket is accessed using a referenced storage integration named `s3_int`.
2. Use the S3 console (or equivalent client application) to retrieve the objects (i.e. files generated by the command) from the bucket.

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

1. [Allowing the Amazon Virtual Private Cloud IDs](#allowing-the-amazon-virtual-private-cloud-ids)
2. [Configuring an S3 bucket for unloading data](#configuring-an-s3-bucket-for-unloading-data)
3. [Configuring support for Amazon S3 access control lists — Optional](#configuring-support-for-amazon-s3-access-control-lists-optional)
4. [Unloading data into an external stage](#unloading-data-into-an-external-stage)
5. [Unloading data directly into an S3 bucket](#unloading-data-directly-into-an-s3-bucket)

Related content

1. [Bulk loading from Amazon S3](/user-guide/data-load-s3)
2. [Unloading into a Snowflake stage](/user-guide/data-unload-snowflake)
3. [Unloading into Microsoft Azure](/user-guide/data-unload-azure)