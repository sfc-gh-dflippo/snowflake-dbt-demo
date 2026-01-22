---
auto_generated: true
description: 'Unloads data from a table (or query) into one or more files in one of
  the following locations:'
last_scraped: '2026-01-14T16:57:41.547375+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
title: COPY INTO <location> | Snowflake Documentation
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

     + Stage
     + [CREATE STAGE](create-stage.md)
     + [ALTER STAGE](alter-stage.md)
     + [DROP STAGE](drop-stage.md)
     + [DESCRIBE STAGE](desc-stage.md)
     + [SHOW STAGES](show-stages.md)
     + File format
     + [ALTER FILE FORMAT](alter-file-format.md)
     + [CREATE FILE FORMAT](create-file-format.md)
     + [DESCRIBE FILE FORMAT](desc-file-format.md)
     + [SHOW FILE FORMATS](show-file-formats.md)
     + [DROP FILE FORMAT](drop-file-format.md)
     + External volume
     + [CREATE EXTERNAL VOLUME](create-external-volume.md)
     + [ALTER EXTERNAL VOLUME](alter-external-volume.md)
     + [DROP EXTERNAL VOLUME](drop-external-volume.md)
     + [UNDROP EXTERNAL VOLUME](undrop-external-volume.md)
     + [SHOW EXTERNAL VOLUMES](show-external-volumes.md)
     + [DESCRIBE EXTERNAL VOLUME](desc-external-volume.md)
     + Pipe
     + [ALTER PIPE](alter-pipe.md)
     + [CREATE PIPE](create-pipe.md)
     + [DESCRIBE PIPE](desc-pipe.md)
     + [SHOW PIPE](show-pipes.md)
     + [DROP PIPE](drop-pipe.md)
     + Snowpipe Streaming
     + [SHOW CHANNELS](show-channels.md)
     + Loading and unloading
     + [COPY INTO <table>](copy-into-table.md)
     + [COPY INTO <location>](copy-into-location.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Data loading & unloading](../commands-data-loading.md)COPY INTO <location>

# COPY INTO *<location>*[¶](#copy-into-location "Link to this heading")

Unloads data from a table (or query) into one or more files in one of the following locations:

* Named internal stage (or table/user stage). The files can then be downloaded from the stage/location using the [GET](get) command.
* Named external stage that references an external location (Amazon S3, Google Cloud Storage, or Microsoft Azure).
* External location (Amazon S3, Google Cloud Storage, or Microsoft Azure).

See also:
:   [COPY INTO <table>](copy-into-table)

## Syntax[¶](#syntax "Link to this heading")

```
COPY INTO { internalStage | externalStage | externalLocation }
     FROM { [<namespace>.]<table_name> | ( <query> ) }
[ PARTITION BY <expr> ]
[ FILE_FORMAT = ( { FORMAT_NAME = '[<namespace>.]<file_format_name>' |
                    TYPE = { CSV | JSON | PARQUET } [ formatTypeOptions ] } ) ]
[ copyOptions ]
[ VALIDATION_MODE = RETURN_ROWS ]
[ HEADER ]
```

Copy

Where:

> ```
> internalStage ::=
>     @[<namespace>.]<int_stage_name>[/<path>]
>   | @[<namespace>.]%<table_name>[/<path>]
>   | @~[/<path>]
> ```
>
> Copy
>
> ```
> externalStage ::=
>   @[<namespace>.]<ext_stage_name>[/<path>]
> ```
>
> Copy
>
> ```
> externalLocation (for Amazon S3) ::=
>   '<protocol>://<bucket>[/<path>]'
>   [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( {  { AWS_KEY_ID = '<string>' AWS_SECRET_KEY = '<string>' [ AWS_TOKEN = '<string>' ] } } ) } ]
>   [ ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] [ MASTER_KEY = '<string>' ] |
>                    [ TYPE = 'AWS_SSE_S3' ] |
>                    [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ] ] |
>                    [ TYPE = 'NONE' ] ) ]
> ```
>
> Copy
>
> ```
> externalLocation (for Google Cloud Storage) ::=
>   'gcs://<bucket>[/<path>]'
>   [ STORAGE_INTEGRATION = <integration_name> ]
>   [ ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = '<string>' ] | [ TYPE = 'NONE' ] ) ]
> ```
>
> Copy
>
> ```
> externalLocation (for Microsoft Azure) ::=
>   'azure://<account>.blob.core.windows.net/<container>[/<path>]'
>   [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( [ AZURE_SAS_TOKEN = '<string>' ] ) } ]
>   [ ENCRYPTION = ( [ TYPE = { 'AZURE_CSE' | 'NONE' } ] [ MASTER_KEY = '<string>' ] ) ]
> ```
>
> Copy
>
> ```
> formatTypeOptions ::=
> -- If FILE_FORMAT = ( TYPE = CSV ... )
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      RECORD_DELIMITER = '<string>' | NONE
>      FIELD_DELIMITER = '<string>' | NONE
>      FILE_EXTENSION = '<string>'
>      ESCAPE = '<character>' | NONE
>      ESCAPE_UNENCLOSED_FIELD = '<character>' | NONE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      FIELD_OPTIONALLY_ENCLOSED_BY = '<character>' | NONE
>      NULL_IF = ( '<string1>' [ , '<string2>' , ... ] )
>      EMPTY_FIELD_AS_NULL = TRUE | FALSE
> -- If FILE_FORMAT = ( TYPE = JSON ... )
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      FILE_EXTENSION = '<string>'
> -- If FILE_FORMAT = ( TYPE = PARQUET ... )
>      COMPRESSION = AUTO | LZO | SNAPPY | NONE
>      SNAPPY_COMPRESSION = TRUE | FALSE
> ```
>
> Copy
>
> ```
> copyOptions ::=
>      OVERWRITE = TRUE | FALSE
>      SINGLE = TRUE | FALSE
>      MAX_FILE_SIZE = <num>
>      INCLUDE_QUERY_ID = TRUE | FALSE
>      DETAILED_OUTPUT = TRUE | FALSE
> ```
>
> Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`INTO ...`
:   Specifies the internal or external location where the data files are unloaded:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]int_stage_name[/path]` | Files are unloaded to the specified named internal stage. |
    > | `@[namespace.]ext_stage_name[/path]` | Files are unloaded to the specified named external stage. |
    > | `@[namespace.]%table_name[/path]` | Files are unloaded to the stage for the specified table. |
    > | `@~[/path]` | Files are unloaded to the stage for the current user. |
    > | `'protocol://bucket[/path]'` | Files are unloaded to the specified external location (S3 bucket). Additional parameters could be required. For details, see [Additional Cloud Provider Parameters](#additional-cloud-provider-parameters) (in this topic). |
    > | `'gcs://bucket[/path]'` | Files are unloaded to the specified external location (Google Cloud Storage bucket). Additional parameters could be required. For details, see [Additional Cloud Provider Parameters](#additional-cloud-provider-parameters) (in this topic). |
    > | `'azure://account.blob.core.windows.net/container[/path]'` | Files are unloaded to the specified external location (Azure container). Additional parameters could be required. For details, see [Additional Cloud Provider Parameters](#additional-cloud-provider-parameters) (in this topic). |

    Where:

    > * `namespace` is the database and/or schema in which the internal or external stage resides, in the form of
    >   `database_name.schema_name` or `schema_name`. It is optional if a database and schema are currently in use within
    >   the user session; otherwise, it is required.
    > * `protocol` is one of the following:
    >
    >   + `s3` refers to S3 storage in public AWS regions outside of China.
    >   + `s3china` refers to S3 storage in public AWS regions in China.
    >   + `s3gov` refers to S3 storage in [government regions](../../user-guide/intro-regions.html#label-us-gov-regions).
    >
    >   Accessing cloud storage in a [government region](../../user-guide/intro-regions.html#label-us-gov-regions) using a storage integration is limited to Snowflake
    >   accounts hosted in the same government region.
    >
    >   Similarly, if you need to access cloud storage in a region in China, you can use a storage integration only from a Snowflake
    >   account hosted in the same region in China.
    >
    >   In these cases, use the CREDENTIALS parameter in the [CREATE STAGE](create-stage) command (rather than using a storage
    >   integration) to provide the credentials for authentication.
    > * `bucket` is the name of the bucket.
    >
    > * `account` is the name of the Azure account (e.g. `myaccount`). Use the `blob.core.windows.net` endpoint for all
    >   supported types of Azure blob storage accounts, including Data Lake Storage Gen2.
    >
    >   Note that currently, accessing Azure blob storage in [government regions](../../user-guide/intro-regions.html#label-us-gov-regions) using a storage
    >   integration is limited to Snowflake accounts hosted on Azure in the same government region. Accessing your blob storage from an
    >   account hosted outside of the government region using direct credentials is supported.
    > * `container` is the name of the Azure container (e.g. `mycontainer`).
    >
    > * The optional `path` parameter specifies a folder and filename prefix for the file(s) containing unloaded data. If a filename
    >   prefix is not included in `path` or if the `PARTITION BY` parameter is specified, the filenames for
    >   the generated data files are prefixed with `data_`.
    >
    >   Relative path modifiers such as `/./` and `/../` are interpreted literally, because “paths” are literal prefixes for a name.
    >   For example:
    >
    >   > ```
    >   > -- S3 bucket
    >   > COPY INTO 's3://mybucket/./../a.csv' FROM mytable;
    >   >
    >   > -- Google Cloud Storage bucket
    >   > COPY INTO 'gcs://mybucket/./../a.csv' FROM mytable;
    >   >
    >   > -- Azure container
    >   > COPY INTO 'azure://myaccount.blob.core.windows.net/mycontainer/./../a.csv' FROM mytable;
    >   > ```
    >   >
    >   > Copy
    >
    >   In these COPY statements, Snowflake creates a file that is literally named `./../a.csv` in the storage location.

    Note

    * If the internal or external stage or path name includes special characters, including spaces, enclose the `INTO ...` string in
      single quotes.
    * The `INTO ...` value must be a literal constant. The value cannot be a [SQL variable](../session-variables).
    * When writing to an external stage within the Snowflake Native App Framework, you must use `STAGE_URL` to specify a URL instead of the external stage name and path.

`FROM ...`
:   Specifies the source of the data to be unloaded, which can either be a table or a query:

    > `[namespace.]table_name`
    > :   Specifies the name of the table from which data is unloaded.
    >
    >     Namespace optionally specifies the database and/or schema in which the table resides, in the form of `database_name.schema_name`
    >     or `schema_name`. It is optional if a database and schema are currently in use within the user session; otherwise, it is
    >     required.
    >
    > `( query )`
    > :   [SELECT](select) statement that returns data to be unloaded into files. You can limit the number of rows returned by specifying a
    >     [LIMIT / FETCH](../constructs/limit) clause in the query.
    >
    >     Note
    >
    >     When casting column values to a data type using the [CAST , ::](../functions/cast) function, verify the data type supports
    >     all of the column values. Values too long for the specified data type could be truncated.

### Additional cloud provider parameters[¶](#additional-cloud-provider-parameters "Link to this heading")

`STORAGE_INTEGRATION = integration_name` or . `CREDENTIALS = ( cloud_specific_credentials )`
:   Supported when the COPY statement specifies an external storage URI rather than an external stage name for the target cloud storage location. Specifies the security credentials for connecting to the cloud provider and accessing the private storage container where the unloaded files are staged.

    Required only for unloading into an external private cloud storage location; not required for public buckets/containers

    **Amazon S3**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](create-storage-integration).
    >
    >     Note
    >
    >     Snowflake recommends the use of storage integrations. This option avoids the need to supply cloud storage credentials using the CREDENTIALS
    >     parameter when creating stages or loading data.
    >
    > `CREDENTIALS = ( AWS_KEY_ID = 'string' AWS_SECRET_KEY = 'string' [ AWS_TOKEN = 'string' ] )` or . `CREDENTIALS = ( AWS_ROLE = 'string' )`
    > :   Specifies the security credentials for connecting to AWS and accessing the private S3 bucket where the unloaded files are staged. For more
    >     information, see [Configuring secure access to Amazon S3](../../user-guide/data-load-s3-config).
    >
    >     The credentials you specify depend on whether you associated the Snowflake access permissions for the bucket with an AWS IAM (Identity &
    >     Access Management) user or role:
    >
    >     * **IAM user:** Temporary IAM credentials are required. Temporary (aka “scoped”) credentials are generated by AWS Security Token Service
    >       (STS) and consist of three components:
    >
    >       > + `AWS_KEY_ID`
    >       > + `AWS_SECRET_KEY`
    >       > + `AWS_TOKEN`
    >
    >       All three are required to access a private bucket. After a designated period of time, temporary credentials expire and can no
    >       longer be used. You must then generate a new set of valid temporary credentials.
    >
    >       Important
    >
    >       COPY commands contain complex syntax and sensitive information, such as credentials. In addition, they are executed frequently and are
    >       often stored in scripts or worksheets, which could lead to sensitive information being inadvertently exposed. The COPY command allows
    >       permanent (aka “long-term”) credentials to be used; however, for security reasons, do not use permanent credentials in COPY
    >       commands. Instead, use temporary credentials.
    >
    >       If you must use permanent credentials, use [external stages](create-stage), for which credentials are entered
    >       once and securely stored, minimizing the potential for exposure.
    >     * **IAM role:** Omit the security credentials and access keys and, instead, identify the role using `AWS_ROLE` and specify the AWS
    >       role ARN (Amazon Resource Name).
    >
    >       Important
    >
    >       The ability to use an AWS IAM role to access a private S3 bucket to load or unload data is now deprecated (i.e. support will be removed
    >       in a future release, TBD). Snowflake recommends modifying any existing S3 stages that use this feature to instead reference storage
    >       integration objects. For instructions, see [Option 1: Configuring a Snowflake storage integration to access Amazon S3](../../user-guide/data-load-s3-config-storage-integration).

    **Google Cloud Storage**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](create-storage-integration).

    **Microsoft Azure**

    > `STORAGE_INTEGRATION = integration_name`
    > :   Specifies the name of the storage integration used to delegate authentication responsibility for external cloud storage to a Snowflake
    >     identity and access management (IAM) entity. For more details, see [CREATE STORAGE INTEGRATION](create-storage-integration).
    >
    >     Note
    >
    >     Snowflake recommends the use of storage integrations. This option avoids the need to supply cloud storage credentials using the
    >     CREDENTIALS parameter when creating stages or loading data.
    >
    > `CREDENTIALS = ( AZURE_SAS_TOKEN = 'string' )`
    > :   Specifies the SAS (shared access signature) token for connecting to Azure and accessing the private container where the files containing
    >     data are staged. Credentials are generated by Azure.

`ENCRYPTION = ( cloud_specific_encryption )`
:   For use in ad hoc COPY statements (statements that do not reference a named external stage). Required only for unloading data to files in encrypted storage locations

    **Amazon S3**

    > `ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] [ MASTER_KEY = '<string>' ] | [ TYPE = 'AWS_SSE_S3' ] | [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ] ] | [ TYPE = 'NONE' ] )`
    >
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     * `AWS_CSE`: Client-side encryption (requires a `MASTER_KEY` value). Currently, the client-side
    > >       [master key](https://csrc.nist.gov/glossary/term/master_key) you provide can only be a symmetric key. Note that, when a
    > >       `MASTER_KEY` value is provided, Snowflake assumes `TYPE = AWS_CSE` (i.e. when a `MASTER_KEY` value is
    > >       provided, `TYPE` is not required).
    > >     * `AWS_SSE_S3`: Server-side encryption that requires no additional encryption settings.
    > >     * `AWS_SSE_KMS`: Server-side encryption that accepts an optional `KMS_KEY_ID` value.
    > >
    > >     For more information about the encryption types, see the AWS documentation for
    > >     [client-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html)
    > >     or [server-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html).
    > >
    > >     * `NONE`: No encryption.
    > >
    > > `MASTER_KEY = 'string'` (applies to `AWS_CSE` encryption only)
    > > :   Specifies the client-side master key used to encrypt the files in the bucket. The master key must be a 128-bit or 256-bit key in
    > >     Base64-encoded form.
    > >
    > > `KMS_KEY_ID = 'string'` (applies to `AWS_SSE_KMS` encryption only)
    > > :   Optionally specifies the ID for the AWS KMS-managed key used to encrypt files unloaded into the bucket. If no value is
    > >     provided, your default KMS key ID is used to encrypt files on unload.
    > >
    > >     Note that this value is ignored for data loading.

    **Google Cloud Storage**

    > `ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' | 'NONE' ] [ KMS_KEY_ID = 'string' ] )`
    >
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     * `GCS_SSE_KMS`: Server-side encryption that accepts an optional `KMS_KEY_ID` value.
    > >
    > >       For more information, see the Google Cloud documentation:
    > >
    > >       + <https://cloud.google.com/storage/docs/encryption/customer-managed-keys>
    > >       + <https://cloud.google.com/storage/docs/encryption/using-customer-managed-keys>
    > >     * `NONE`: No encryption.
    > >
    > > `KMS_KEY_ID = 'string'` (applies to `GCS_SSE_KMS` encryption only)
    > > :   Optionally specifies the ID for the Cloud KMS-managed key that is used to encrypt files unloaded into the bucket. If no value
    > >     is provided, your default KMS key ID set on the bucket is used to encrypt files on unload.
    > >
    > >     This value is ignored for data loading. The load operation should succeed if the service account has sufficient permissions
    > >     to decrypt data in the bucket.

    **Microsoft Azure**

    > `ENCRYPTION = ( [ TYPE = 'AZURE_CSE' | 'NONE' ] [ MASTER_KEY = 'string' ] )`
    >
    > > `TYPE = ...`
    > > :   Specifies the encryption type used. Possible values are:
    > >
    > >     * `AZURE_CSE`: Client-side encryption (requires a MASTER\_KEY value). For information, see the
    > >       [Client-side encryption information](https://docs.microsoft.com/en-us/azure/storage/common/storage-client-side-encryption) in
    > >       the Microsoft Azure documentation.
    > >     * `NONE`: No encryption.
    > >
    > > `MASTER_KEY = 'string'` (applies to AZURE\_CSE encryption only)
    > > :   Specifies the client-side master key used to encrypt files. The master key must be a 128-bit or 256-bit key in Base64-encoded form.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`PARTITION BY expr`
:   Specifies an expression used to partition the unloaded table rows into separate files. Supports any SQL expression that evaluates to a
    string.

    The unload operation splits the table rows based on the partition expression and determines the number of files to create based on the
    amount of data and number of parallel operations, distributed among the compute resources in the warehouse.

    Filenames are prefixed with `data_` and include the partition column values. Individual filenames in each partition are identified
    with a universally unique identifier (UUID). The UUID is the query ID of the COPY statement used to unload the data files.

    Caution

    COPY INTO *<location>* statements write partition column values to the unloaded file names. Snowflake recommends partitioning your
    data on common data types such as dates or timestamps rather than potentially sensitive string or integer values.

    Note that file URLs are included in the internal logs that Snowflake maintains to aid in debugging issues when customers create Support
    cases. As a result, data in columns referenced in a PARTITION BY expression is also indirectly stored in internal logs. These logs
    might be processed outside of your deployment region. Hence, as a best practice, only include dates, timestamps, and Boolean data types
    in PARTITION BY expressions.

    If you prefer to disable the PARTITION BY parameter in COPY INTO *<location>* statements for your account, please contact
    [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    Note that Snowflake provides a set of parameters to further restrict data unloading operations:

    * [PREVENT\_UNLOAD\_TO\_INLINE\_URL](../parameters.html#label-prevent-unload-to-inline-url) prevents ad hoc data unload operations to external cloud storage locations (i.e. COPY INTO
      *<location>* statements that specify the cloud storage URL and access settings directly in the statement).
    * [PREVENT\_UNLOAD\_TO\_INTERNAL\_STAGES](../parameters.html#label-prevent-unload-to-internal-stages) prevents data unload operations to any internal stage, including user stages,
      table stages, or named internal stages.

    For an example, see [Partitioning Unloaded Rows to Parquet Files](#partitioning-unloaded-rows-to-parquet-files) (in this topic).

    Note

    * The following copy option values are not supported in combination with PARTITION BY:

      + `OVERWRITE = TRUE`
      + `SINGLE = TRUE`
      + `INCLUDE_QUERY_ID = FALSE`
    * Including the ORDER BY clause in the SQL statement in combination with PARTITION BY does not guarantee that the specified order is
      preserved in the unloaded files.
    * If the PARTITION BY expression evaluates to NULL, the partition path in the output filename is `_NULL_`
      (e.g. `mystage/_NULL_/data_01234567-0123-1234-0000-000000001234_01_0_0.snappy.parquet`).
    * When unloading to files of type `PARQUET`:

      + Small data files unloaded by parallel execution threads are merged automatically into a single file that matches the MAX\_FILE\_SIZE
        copy option value as closely as possible.
      + All row groups are 128 MB in size. A row group is a logical horizontal partitioning of the data into rows. There is no physical
        structure that is guaranteed for a row group. A row group consists of a column chunk for each column in the dataset.
      + The unload operation attempts to produce files as close in size to the `MAX_FILE_SIZE` copy option setting as possible. The
        default value for this copy option is 16 MB. Note that this behavior applies only when unloading data to Parquet files.
      + VARIANT columns are converted into simple JSON strings. Casting the values to an array (using the
        [TO\_ARRAY](../functions/to_array) function) results in an array of JSON strings.
    * There is no option to omit the columns in the partition expression from the unloaded data files.

`FILE_FORMAT = ( FORMAT_NAME = 'file_format_name' )` or . `FILE_FORMAT = ( TYPE = CSV | JSON | PARQUET [ ... ] )`
:   Specifies the format of the data files containing unloaded data:

    `FORMAT_NAME = 'file_format_name'`
    :   Specifies an existing named file format to use for unloading data from the table. The named file format determines the format type
        (CSV, JSON, PARQUET), as well as any other format options, for the data files. For more information, see [CREATE FILE FORMAT](create-file-format).

    `TYPE = CSV | JSON | PARQUET`
    :   Specifies the type of files unloaded from the table.

        If a format type is specified, you can specify additional format-specific options. For information, see
        [Format Type Options](#label-copy-into-location-formattypeoptions) (in this topic).

    Note

    * JSON can only be used to unload data from columns of type VARIANT (i.e. columns containing JSON data).
    * Currently, nested data in VARIANT columns cannot be unloaded successfully in Parquet format.

`copyOptions`
:   Specifies one or more copy options for the unloaded data. For more details, see [Copy Options](#label-copy-into-location-copyoptions)
    (in this topic).

`VALIDATION_MODE = RETURN_ROWS`
:   String (constant) that instructs the COPY command to return the results of the query in the SQL statement instead of unloading
    the results to the specified cloud storage location. The only supported validation option is `RETURN_ROWS`. This option returns
    all rows produced by the query.

    When you have validated the query, you can remove the `VALIDATION_MODE` to perform the unload operation.

`HEADER = TRUE | FALSE`
:   Specifies whether to include the table column headings in the output files.

    * Set this option to `TRUE` to include the table column headings to the output files.

      Note that if the COPY operation unloads the data to multiple files, the column headings are included in every file.

      When unloading data in Parquet format, the table column names are retained in the output files.
    * Set this option to `FALSE` to specify the following behavior:

      CSV:
      :   Do not include table column headings in the output files.

      Parquet:
      :   Include generic column headings (e.g. `col1`, `col2`, etc.) in the output files.

    Default: `FALSE`

## Format type options (`formatTypeOptions`)[¶](#format-type-options-formattypeoptions "Link to this heading")

Depending on the file format type specified (`FILE_FORMAT = ( TYPE = ... )`), you can include one or more of the following
format-specific options (separated by blank spaces, commas, or new lines):

### TYPE = CSV[¶](#type-csv "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   String (constant) that specifies to compresses the unloaded data files using the specified compression algorithm.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Unloaded files are automatically compressed using the default, which is gzip. |
    | `GZIP` |  |
    | `BZ2` |  |
    | `BROTLI` | Must be specified when loading Brotli-compressed files. |
    | `ZSTD` | Zstandard v0.8 (and higher) supported. |
    | `DEFLATE` | Unloaded files are compressed using Deflate (with zlib header, RFC1950). |
    | `RAW_DEFLATE` | Unloaded files are compressed using Raw Deflate (without header, RFC1951). |
    | `NONE` | Unloaded files are not compressed. |

    Default: `AUTO`

`RECORD_DELIMITER = 'string' | NONE`
:   One or more singlebyte or multibyte characters that separate records in an unloaded file. Accepts common escape sequences or the following singlebyte or multibyte characters:

    Singlebyte characters:
    :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

    Multibyte characters:
    :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

        The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (e.g. `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

    The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

    Also accepts a value of `NONE`.

    Default: New line character. Note that “new line” is logical such that `\r\n` is understood as a new line for files on a Windows platform.

`FIELD_DELIMITER = 'string' | NONE`
:   One or more singlebyte or multibyte characters that separate fields in an unloaded file. Accepts common escape sequences or the following singlebyte or multibyte characters:

    Singlebyte characters:
    :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

    Multibyte characters:
    :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

        The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (e.g. `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

        > Note
        >
        > For non-ASCII characters, you must use the hex byte sequence value to get a deterministic behavior.

The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

> Also accepts a value of `NONE`.
>
> Default: comma (`,`)

`FILE_EXTENSION = 'string'`
:   String that specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a valid file extension that can be read by the desired software or
    service.

    Note

    If the `SINGLE` copy option is `TRUE`, then the COPY command unloads a file without a file extension by default. To specify a file extension, provide a file name and extension in the
    `internal_location` or `external_location` path. For example:

    > `copy into @stage/data.csv ...`

    Default: null, meaning the file extension is determined by the format type, e.g. `.csv[compression]`, where `compression` is the extension added by the compression method, if
    `COMPRESSION` is set.

`DATE_FORMAT = 'string' | AUTO`
:   String that defines the format of date values in the unloaded data files. If a value is not specified or is set to `AUTO`, the value for the [DATE\_OUTPUT\_FORMAT](../parameters.html#label-date-output-format) parameter is used.

    Default: `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   String that defines the format of time values in the unloaded data files. If a value is not specified or is set to `AUTO`, the value for the [TIME\_OUTPUT\_FORMAT](../parameters.html#label-time-output-format) parameter is used.

    Default: `AUTO`

`TIMESTAMP_FORMAT = 'string' | AUTO`
:   String that defines the format of timestamp values in the unloaded data files. If a value is not specified or is set to `AUTO`, the value for the [TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format) parameter is used.

    Default: `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   String (constant) that defines the encoding format for binary output. The option can be used when unloading data from binary columns in a table.

    Default: `HEX`

`ESCAPE = 'character' | NONE`
:   Use:
    :   Data loading and unloading

    Definition:
    :   A singlebyte character string used as the escape character for enclosed or unenclosed field values. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_OPTIONALLY_ENCLOSED_BY` character in the data as literals. The escape character can also be used to escape instances of itself in the data.

    Accepts common escape sequences, octal values, or hex values.

    Specify the character used to enclose fields by setting `FIELD_OPTIONALLY_ENCLOSED_BY`.

    If this option is set, it overrides the escape character set for `ESCAPE_UNENCLOSED_FIELD`.

    Default:
    :   `NONE`

`ESCAPE_UNENCLOSED_FIELD = 'character' | NONE`
:   Use:
    :   Data loading and unloading

    Definition:
    :   A singlebyte character string used as the escape character for unenclosed field values only. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_DELIMITER` or `RECORD_DELIMITER` characters in the data as literals. The escape character can also be used to escape instances of itself in the data.

    Accepts common escape sequences, octal values, or hex values.

    If `ESCAPE` is set, the escape character set for that file format option overrides this option.

    Default:
    :   backslash (`\\`)

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Character used to enclose strings. Value can be `NONE`, single quote character (`'`), or double quote character (`"`). To use the single quote character, use the octal or hex
    representation (`0x27`) or the double single-quoted escape (`''`).

    When a field in the source table contains this character, Snowflake escapes it using the same character for unloading. For example, if the value is the double quote character and a field contains the string `A "B" C`, Snowflake escapes the double quotes for unloading as follows:

    `A ""B"" C`

    Default: `NONE`

`NULL_IF = ( 'string1' [ , 'string2' ... ] )`
:   String used to convert from SQL NULL. Snowflake converts SQL NULL values to the first value in the list.

    Default: `\N` (that is, NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\` (default))

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   Used in combination with `FIELD_OPTIONALLY_ENCLOSED_BY`. When `FIELD_OPTIONALLY_ENCLOSED_BY = NONE`, setting `EMPTY_FIELD_AS_NULL = FALSE` specifies to unload empty strings in tables to empty string values without quotes enclosing the field values.

    If set to `TRUE`, `FIELD_OPTIONALLY_ENCLOSED_BY` must specify a character to enclose strings.

    Default: `TRUE`

### TYPE = JSON[¶](#type-json "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   String (constant). Compresses the data file using the specified compression algorithm.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Unloaded files are automatically compressed using the default, which is gzip. |
    | `GZIP` |  |
    | `BZ2` |  |
    | `BROTLI` |  |
    | `ZSTD` |  |
    | `DEFLATE` | Unloaded files are compressed using Deflate (with zlib header, RFC1950). |
    | `RAW_DEFLATE` | Unloaded files are compressed using Raw Deflate (without header, RFC1951). |
    | `NONE` | Unloaded files are not compressed. |

    Default: `AUTO`

`FILE_EXTENSION = 'string' | NONE`
:   String that specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a valid file extension that can be read by the desired software or
    service.

    Default: null, meaning the file extension is determined by the format type (e.g. `.csv[compression]`), where `compression` is the extension added by the compression method, if
    `COMPRESSION` is set.

### TYPE = PARQUET[¶](#type-parquet "Link to this heading")

`COMPRESSION = AUTO | LZO | SNAPPY | NONE`
:   String (constant). Compresses the data file using the specified compression algorithm.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Files are compressed using Snappy, the default compression algorithm. |
    | `LZO` | Files are compressed using the Snappy algorithm by default. If applying Lempel-Ziv-Oberhumer (LZO) compression instead, specify this value. |
    | `SNAPPY` | Files are compressed using the Snappy algorithm by default. You can optionally specify this value. |
    | `NONE` | Specifies that the unloaded files are not compressed. |

    Default: `AUTO`

`SNAPPY_COMPRESSION = TRUE | FALSE`
:   Boolean that specifies whether the unloaded file(s) are compressed using the SNAPPY algorithm.

    Note

    Deprecated. Use `COMPRESSION = SNAPPY` instead.

    Default: `TRUE`

## Copy options (`copyOptions`)[¶](#copy-options-copyoptions "Link to this heading")

You can specify one or more of the following copy options (separated by blank spaces, commas, or new lines):

`OVERWRITE = TRUE | FALSE`
:   Definition:
    :   Boolean that specifies whether the COPY command overwrites existing files with matching names, if any, in the location where files are stored. The option does not remove any existing files that do not match the names of the files that the COPY command unloads.

        In many cases, enabling this option helps prevent data duplication in the target stage when the same COPY INTO *<location>* statement is executed multiple times. However, when an unload operation writes multiple files to a stage, Snowflake appends a suffix that ensures each file name is unique across parallel execution threads (e.g. `data_0_1_0`). The number of parallel execution threads can vary between unload operations. If the files written by an unload operation do not have the same filenames as files written by a previous operation, SQL statements that include this copy option cannot replace the existing files, resulting in duplicate files.

        In addition, in the rare event of a machine or network failure, the unload job is retried. In that scenario, the unload operation writes additional files to the stage without first removing any files that were previously written by the first attempt.

        To avoid data duplication in the target stage, we recommend setting the `INCLUDE_QUERY_ID = TRUE` copy option instead of `OVERWRITE = TRUE` and removing all data files in the target stage and path (or using a different path for each unload operation) between each unload job.

    Default:
    :   `FALSE`

`SINGLE = TRUE | FALSE`
:   Definition:
    :   Boolean that specifies whether to generate a single file or multiple files. If `FALSE`, a filename prefix must be included in `path`.

    Important

    If `SINGLE = TRUE`, then COPY ignores the `FILE_EXTENSION` file format option and outputs a file simply named **data**. To specify a file extension, provide a filename and extension in the internal or external location `path`. For example:

    > ```
    > COPY INTO @mystage/data.csv ...
    > ```
    >
    > Copy

    In addition, if the `COMPRESSION` file format option is also explicitly set to one of the supported compression algorithms (e.g. `GZIP`), then the specified internal or external location `path` must end in a filename with the corresponding file extension (e.g. `gz`) so that the file can be uncompressed using the appropriate tool. For example:

    > ```
    > COPY INTO @mystage/data.gz ...
    >
    > COPY INTO @mystage/data.csv.gz ...
    > ```
    >
    > Copy

    Default:
    :   `FALSE`

`MAX_FILE_SIZE = num`
:   Definition:
    :   Specifies the maximum size (in bytes) of each file to be generated in parallel per thread.
        Snowflake utilizes parallel execution to optimize performance. The number of threads can’t be modified.

        Note

        The actual unloaded file size and number of files unloaded depends on the total amount of data and number of nodes available for parallel processing. The unloaded file size depends on the available memory in the warehouse worker, which varies based on:

        * The warehouse size and available resources.
        * The number of concurrent queries running on the warehouse.

        MAX\_FILE\_SIZE sets an upper limit but does not guarantee that files reach this size. Files might be smaller than
        the specified MAX\_FILE\_SIZE when memory constraints require earlier file completion.

        The COPY command unloads one set of table rows at a time. If you set a very small `MAX_FILE_SIZE` value (for example, less than 1 MB), the amount of data in a set of rows could exceed the specified size.

    Default:
    :   16777216 (16 MB)

    Maximum:
    :   5368709120 (5 GB)

`INCLUDE_QUERY_ID = TRUE | FALSE`
:   Definition:
    :   Boolean that specifies whether to uniquely identify unloaded files by including a universally unique identifier (UUID) in the filenames of unloaded data files. This option helps ensure that concurrent COPY statements do not overwrite unloaded files accidentally.

    Values:
    :   If `TRUE`, a UUID is added to the names of unloaded files. The UUID is the query ID of the COPY statement used to unload the data files. The UUID is a segment of the filename: `<path>/data_<uuid>_<name>.<extension>`. This option also prevents unloading duplicate data if an internal retry occurs. When an internal retry occurs, Snowflake deletes the partial set of unloaded files (identified by UUID), then restarts the copy operation.

        If `FALSE`, then a UUID is not added to the unloaded data files.

        Note

        * `INCLUDE_QUERY_ID = TRUE` is the default copy option value when you partition the unloaded table rows into separate files (by setting `PARTITION BY expr` in the COPY INTO *<location>* statement). This value cannot be changed to FALSE.
        * `INCLUDE_QUERY_ID = TRUE` is not supported when either of the following copy options is set:

          + `SINGLE = TRUE`
          + `OVERWRITE = TRUE`
        * In the rare event of a machine or network failure, the unload job is retried. In that scenario, the unload operation removes any files that were written to the stage with the UUID of the current query ID and then attempts to unload the data again. Any new files written to the stage have the retried query ID as the UUID.

    Default:
    :   `FALSE`

`DETAILED_OUTPUT = TRUE | FALSE`
:   Definition:
    :   Boolean that specifies whether the command output should describe the unload operation or the individual files unloaded as a result of the operation.

    Values:
    :   * If `TRUE`, the command output includes a row for each file unloaded to the specified stage. Columns show the path and name for each file, its size, and the number of rows that were unloaded to the file.
        * If `FALSE`, the command output consists of a single row that describes the entire unload operation. Columns show the total amount of data unloaded from tables, before and after compression (if applicable), and the total number of rows that were unloaded.

    Default:
    :   `FALSE`

## Usage notes[¶](#usage-notes "Link to this heading")

* `STORAGE_INTEGRATION` or `CREDENTIALS` only applies if you are unloading directly into a private storage location (Amazon S3,
  Google Cloud Storage, or Microsoft Azure). If you are unloading into a public bucket, secure access is not required, and if you are
  unloading into a named external stage, the stage provides all the credential information required for accessing the bucket.
* If referencing a file format in the current namespace, you can omit the single quotes around the format identifier.
* `JSON` can be specified for `TYPE` only when unloading data from VARIANT columns in tables.
* When unloading to files of type `CSV`, `JSON`, or `PARQUET`:

  By default, VARIANT columns are converted into simple JSON strings in the output file.

  + To unload the data as Parquet LIST values, explicitly cast the column values to arrays
    (using the [TO\_ARRAY](../functions/to_array) function).
  + If a VARIANT column contains XML, Snowflake recommends explicitly casting the column values to
    XML in a `FROM ...` query. Casting the values using the
    [TO\_XML](../functions/to_xml) function unloads XML-formatted strings
    instead of JSON strings.
* When unloading to files of type `PARQUET`:

  Unloading TIMESTAMP\_TZ or TIMESTAMP\_LTZ data produces an error.
* If the source table contains 0 rows, then the COPY operation does not unload a data file.
* This SQL command does not return a warning when unloading into a non-empty storage location. To avoid unexpected behaviors when files in
  a storage location are consumed by data pipelines, Snowflake recommends only writing to empty storage locations.
* Failed unload operations:

  + A failed unload operation can still result in unloaded data files (for example, if the statement is canceled or exceeds its timeout limit).
    For [Partitioned data unloading](../../user-guide/data-unload-overview.html#label-data-unload-overview-partitioned) or if `INCLUDE_QUERY_ID = TRUE`,
    Snowflake attempts to clean up unloaded files and might retry the failed unload operation.
    If the cleanup operation times out and returns an error message, you can use the failed query ID to find and manually
    remove the files from your storage location. Alternatively, you can identify files to remove by the
    [file naming pattern](../../user-guide/data-unload-overview.html#label-data-unload-overview-file-names).

    To facilitate cleanup and avoid timeout, Snowflake recommends that you only unload into empty storage locations.
  + A failed unload operation to cloud storage in a different region results in data transfer costs.
* If a [masking policy](../../user-guide/security-column-intro) is set on a column, the masking policy is applied to the data resulting in
  unauthorized users seeing masked data in the column.
* To view the status and history of this command’s executions, use [QUERY\_HISTORY view](../account-usage/query_history).
* For [outbound private connectivity](../../user-guide/private-connectivity-outbound), unloading directly to an external location (external
  storage URI) isn’t supported. Instead, use an external stage with a storage integration configured for outbound private connectivity.
  For more information, see the following topics:

  + [Private connectivity to external stages for Amazon Web Services](../../user-guide/data-load-aws-private)
  + [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](../../user-guide/data-load-azure-private)

To learn more, see [Explicitly converting numeric columns to Parquet data types](../../user-guide/data-unload-considerations.html#label-converting-numeric-columns-to-parquet-data-types).

## Examples[¶](#examples "Link to this heading")

### Unloading data from a table to files in a table stage[¶](#unloading-data-from-a-table-to-files-in-a-table-stage "Link to this heading")

Unload data from the `orderstiny` table into the table’s stage using a folder/filename prefix (`result/data_`), a named
file format (`myformat`), and gzip compression:

> ```
> COPY INTO @%orderstiny/result/data_
>   FROM orderstiny FILE_FORMAT = (FORMAT_NAME ='myformat' COMPRESSION='GZIP');
> ```
>
> Copy

### Unloading data from a query to files in a named internal stage[¶](#unloading-data-from-a-query-to-files-in-a-named-internal-stage "Link to this heading")

Unload the result of a query into a named internal stage (`my_stage`) using a folder/filename prefix (`result/data_`), a named
file format (`myformat`), and gzip compression:

> ```
> COPY INTO @my_stage/result/data_ FROM (SELECT * FROM orderstiny)
>    file_format=(format_name='myformat' compression='gzip');
> ```
>
> Copy
>
> Note that the above example is functionally equivalent to the first example, except the file containing the unloaded data is stored in
> the stage location for `my_stage` rather than the table location for `orderstiny`.

### Unloading data from a table directly to files in an external location[¶](#unloading-data-from-a-table-directly-to-files-in-an-external-location "Link to this heading")

Note

This option isn’t supported for [outbound private connectivity](../../user-guide/private-connectivity-outbound).
Instead, use an external stage.

Unload all data in a table into a storage location using a named `my_csv_format` file format:

**Amazon S3**

> Access the referenced S3 bucket using a referenced storage integration named `myint`:
>
> ```
> COPY INTO 's3://mybucket/unload/'
>   FROM mytable
>   STORAGE_INTEGRATION = myint
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```
>
> Copy
>
> Access the referenced S3 bucket using supplied credentials:
>
> ```
> COPY INTO 's3://mybucket/unload/'
>   FROM mytable
>   CREDENTIALS = (AWS_KEY_ID='xxxx' AWS_SECRET_KEY='xxxxx' AWS_TOKEN='xxxxxx')
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```
>
> Copy

**Google Cloud Storage**

> Access the referenced GCS bucket using a referenced storage integration named `myint`:
>
> ```
> COPY INTO 'gcs://mybucket/unload/'
>   FROM mytable
>   STORAGE_INTEGRATION = myint
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```
>
> Copy

**Microsoft Azure**

> Access the referenced container using a referenced storage integration named `myint`:
>
> ```
> COPY INTO 'azure://myaccount.blob.core.windows.net/unload/'
>   FROM mytable
>   STORAGE_INTEGRATION = myint
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```
>
> Copy
>
> Access the referenced container using supplied credentials:
>
> ```
> COPY INTO 'azure://myaccount.blob.core.windows.net/mycontainer/unload/'
>   FROM mytable
>   CREDENTIALS=(AZURE_SAS_TOKEN='xxxx')
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```
>
> Copy

### Partitioning unloaded rows to Parquet files[¶](#partitioning-unloaded-rows-to-parquet-files "Link to this heading")

The following example partitions unloaded rows into Parquet files by the values in two columns: a date column and a time column. The
example specifies a maximum size for each unloaded file:

```
CREATE or replace TABLE t1 (
  dt date,
  ts time
  )
AS
  SELECT TO_DATE($1)
        ,TO_TIME($2)
    FROM VALUES
           ('2020-01-28', '18:05')
          ,('2020-01-28', '22:57')
          ,('2020-01-28', NULL)
          ,('2020-01-29', '02:15')
;

SELECT * FROM t1;

+------------+----------+
| DT         | TS       |
|------------+----------|
| 2020-01-28 | 18:05:00 |
| 2020-01-28 | 22:57:00 |
| 2020-01-28 | 22:32:00 |
| 2020-01-29 | 02:15:00 |
+------------+----------+

-- Partition the unloaded data by date and hour. Set ``32000000`` (32 MB) as the upper size limit of each file to be generated in parallel per thread.
COPY INTO @%t1
  FROM t1
  PARTITION BY ('date=' || to_varchar(dt, 'YYYY-MM-DD') || '/hour=' || to_varchar(date_part(hour, ts))) -- Concatenate labels and column values to output meaningful filenames
  FILE_FORMAT = (TYPE=parquet)
  MAX_FILE_SIZE = 32000000
  HEADER=true;

LIST @%t1;

+------------------------------------------------------------------------------------------+------+----------------------------------+------------------------------+
| name                                                                                     | size | md5                              | last_modified                |
|------------------------------------------------------------------------------------------+------+----------------------------------+------------------------------|
| __NULL__/data_019c059d-0502-d90c-0000-438300ad6596_006_4_0.snappy.parquet                |  512 | 1c9cb460d59903005ee0758d42511669 | Wed, 5 Aug 2020 16:58:16 GMT |
| date=2020-01-28/hour=18/data_019c059d-0502-d90c-0000-438300ad6596_006_4_0.snappy.parquet |  592 | d3c6985ebb36df1f693b52c4a3241cc4 | Wed, 5 Aug 2020 16:58:16 GMT |
| date=2020-01-28/hour=22/data_019c059d-0502-d90c-0000-438300ad6596_006_6_0.snappy.parquet |  592 | a7ea4dc1a8d189aabf1768ed006f7fb4 | Wed, 5 Aug 2020 16:58:16 GMT |
| date=2020-01-29/hour=2/data_019c059d-0502-d90c-0000-438300ad6596_006_0_0.snappy.parquet  |  592 | 2d40ccbb0d8224991a16195e2e7e5a95 | Wed, 5 Aug 2020 16:58:16 GMT |
+------------------------------------------------------------------------------------------+------+----------------------------------+------------------------------+
```

Copy

### Retaining NULL/empty field data in unloaded files[¶](#retaining-null-empty-field-data-in-unloaded-files "Link to this heading")

Retain SQL NULL and empty fields in unloaded files:

> ```
> -- View the table column values
> SELECT * FROM HOME_SALES;
>
> +------------+-------+-------+-------------+--------+------------+
> | CITY       | STATE | ZIP   | TYPE        | PRICE  | SALE_DATE  |
> |------------+-------+-------+-------------+--------+------------|
> | Lexington  | MA    | 95815 | Residential | 268880 | 2017-03-28 |
> | Belmont    | MA    | 95815 | Residential |        | 2017-02-21 |
> | Winchester | MA    | NULL  | Residential |        | 2017-01-31 |
> +------------+-------+-------+-------------+--------+------------+
>
> -- Unload the table data into the current user's personal stage. The file format options retain both the NULL value and the empty values in the output file
> COPY INTO @~ FROM HOME_SALES
>   FILE_FORMAT = (TYPE = csv NULL_IF = ('NULL', 'null') EMPTY_FIELD_AS_NULL = false);
>
> -- Contents of the output file
> Lexington,MA,95815,Residential,268880,2017-03-28
> Belmont,MA,95815,Residential,,2017-02-21
> Winchester,MA,NULL,Residential,,2017-01-31
> ```
>
> Copy

### Unloading data to a single file[¶](#unloading-data-to-a-single-file "Link to this heading")

Unload all rows to a single data file using the SINGLE copy option:

> ```
> copy into @~ from HOME_SALES
> single = true;
> ```
>
> Copy

### Including the UUID in the unloaded filenames[¶](#including-the-uuid-in-the-unloaded-filenames "Link to this heading")

Include the UUID in the names of unloaded files by setting the INCLUDE\_QUERY\_ID copy option to TRUE:

```
-- Unload rows from the T1 table into the T1 table stage:
COPY INTO @%t1
  FROM t1
  FILE_FORMAT=(TYPE=parquet)
  INCLUDE_QUERY_ID=true;

-- Retrieve the query ID for the COPY INTO location statement.
-- This optional step enables you to see that the query ID for the COPY INTO location statement
-- is identical to the UUID in the unloaded files.
SELECT last_query_id();
+--------------------------------------+
| LAST_QUERY_ID()                      |
|--------------------------------------|
| 019260c2-00c0-f2f2-0000-4383001cf046 |
+--------------------------------------+

LS @%t1;
+----------------------------------------------------------------+------+----------------------------------+-------------------------------+
| name                                                           | size | md5                              | last_modified                 |
|----------------------------------------------------------------+------+----------------------------------+-------------------------------|
| data_019260c2-00c0-f2f2-0000-4383001cf046_0_0_0.snappy.parquet |  544 | eb2215ec3ccce61ffa3f5121918d602e | Thu, 20 Feb 2020 16:02:17 GMT |
+----------------------------------------------------------------+------+----------------------------------+-------------------------------+
```

Copy

### Validating data to be unloaded (from a query)[¶](#validating-data-to-be-unloaded-from-a-query "Link to this heading")

Execute COPY in validation mode to return the result of a query and view the data that will be unloaded from the `orderstiny` table if
COPY is executed in normal mode:

```
COPY INTO @my_stage
  FROM (SELECT * FROM orderstiny LIMIT 5)
  VALIDATION_MODE='RETURN_ROWS';
```

Copy

Output:

```
+-----+--------+----+-----------+------------+----------+-----------------+----+---------------------------------------------------------------------------+
|  C1 |   C2   | C3 |    C4     |     C5     |    C6    |       C7        | C8 |                                    C9                                     |
+-----+--------+----+-----------+------------+----------+-----------------+----+---------------------------------------------------------------------------+
|  1  | 36901  | O  | 173665.47 | 1996-01-02 | 5-LOW    | Clerk#000000951 | 0  | nstructions sleep furiously among                                         |
|  2  | 78002  | O  | 46929.18  | 1996-12-01 | 1-URGENT | Clerk#000000880 | 0  |  foxes. pending accounts at the pending\, silent asymptot                 |
|  3  | 123314 | F  | 193846.25 | 1993-10-14 | 5-LOW    | Clerk#000000955 | 0  | sly final accounts boost. carefully regular ideas cajole carefully. depos |
|  4  | 136777 | O  | 32151.78  | 1995-10-11 | 5-LOW    | Clerk#000000124 | 0  | sits. slyly regular warthogs cajole. regular\, regular theodolites acro   |
|  5  | 44485  | F  | 144659.20 | 1994-07-30 | 5-LOW    | Clerk#000000925 | 0  | quickly. bold deposits sleep slyly. packages use slyly                    |
+-----+--------+----+-----------+------------+----------+-----------------+----+---------------------------------------------------------------------------+
```

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
3. [Additional cloud provider parameters](#additional-cloud-provider-parameters)
4. [Optional parameters](#optional-parameters)
5. [Format type options (formatTypeOptions)](#format-type-options-formattypeoptions)
6. [TYPE = CSV](#type-csv)
7. [TYPE = JSON](#type-json)
8. [TYPE = PARQUET](#type-parquet)
9. [Copy options (copyOptions)](#copy-options-copyoptions)
10. [Usage notes](#usage-notes)
11. [Examples](#examples)
12. [Unloading data from a table to files in a table stage](#unloading-data-from-a-table-to-files-in-a-table-stage)
13. [Unloading data from a query to files in a named internal stage](#unloading-data-from-a-query-to-files-in-a-named-internal-stage)
14. [Unloading data from a table directly to files in an external location](#unloading-data-from-a-table-directly-to-files-in-an-external-location)
15. [Partitioning unloaded rows to Parquet files](#partitioning-unloaded-rows-to-parquet-files)
16. [Retaining NULL/empty field data in unloaded files](#retaining-null-empty-field-data-in-unloaded-files)
17. [Unloading data to a single file](#unloading-data-to-a-single-file)
18. [Including the UUID in the unloaded filenames](#including-the-uuid-in-the-unloaded-filenames)
19. [Validating data to be unloaded (from a query)](#validating-data-to-be-unloaded-from-a-query)

Related content

1. [Unload Data from Snowflake](/sql-reference/sql/../../guides-overview-unloading-data)
2. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/sql/../functions/system_validate_storage_integration)
3. [GET](/sql-reference/sql/get)