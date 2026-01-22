---
auto_generated: true
description: Uploads one or more data files from a local file system onto an internal
  stage.
last_scraped: '2026-01-14T16:56:25.288705+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/put.html
title: PUT | Snowflake Documentation
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
   * [File staging](../commands-file.md)

     + [PUT](put.md)
     + [COPY FILES](copy-files.md)
     + [GET](get.md)
     + [LIST](list.md)
     + [REMOVE](remove.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[File staging](../commands-file.md)PUT

# PUT[¶](#put "Link to this heading")

Uploads one or more data files from a local file system onto an [internal stage](../../user-guide/data-load-local-file-system-create-stage).

After you upload files onto an internal stage, you can load data from the files into a table using the [COPY INTO <table>](copy-into-table) command.

Note

* PUT does not support uploading files onto an external stage. To upload files to an external stage, use the utilities provided
  by your cloud service.
* [snowflake.snowpark.FileOperation.put](/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.FileOperation.put) from Snowpark stored procedures does support external stages and bills at normal data transfer rates.
* The [ODBC driver](../../developer-guide/odbc/odbc) supports PUT with Snowflake accounts hosted on the following platforms:

  + Amazon Web Services
  + Google Cloud
  + Microsoft Azure

See also:
:   [GET](get) , [LIST](list) , [REMOVE](remove) , [COPY FILES](copy-files) , [CREATE STAGE](create-stage) , [Overview of data loading](../../user-guide/data-load-overview)

## Syntax[¶](#syntax "Link to this heading")

```
PUT file://<absolute_path_to_file>/<filename> internalStage
    [ PARALLEL = <integer> ]
    [ AUTO_COMPRESS = TRUE | FALSE ]
    [ SOURCE_COMPRESSION = AUTO_DETECT | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE ]
    [ OVERWRITE = TRUE | FALSE ]
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

## Required parameters[¶](#required-parameters "Link to this heading")

`file://absolute_path_to_file/filename`
:   Specifies the URI for the data files on the client machine, where:

    * `absolute_path_to_file` is the local directory path to the files to upload.
    * `filename` is the name of the file to upload. You can use wildcard characters (`*`, `?`) to upload multiple files. If the
      directory path or filename includes special characters or spaces, enclose the entire file URI in single quotes.

      Attention

      Be careful when selecting multiple files using a PUT query. PUT queries that match a large number of files can have significant cost and performance consequences.

    The URI formatting differs depending on your client operating system.

    > Linux/macOS:
    > :   Specify the absolute path to the file from the root directory (`/`).
    >     For example, for a file named `my-data.csv` use `file:///my/file/path/my-data.csv`.
    >
    > Windows:
    > :   Specify the absolute path from the root of the drive where the file or files are located.
    >     For example, for a file named `my-data.csv` use `file://C:temp\my-data.csv`.
    >
    >     If the file path includes special characters, you must enclose the entire path in single quotes and change
    >     the drive and path separator from a backward slash to a forward slash (`/`).
    >     For example, for a file named `my$data.csv`, use: `'file://C:/temp/my$data.csv'`.

    Note

    Snowflake doesn’t support tar (tape archive) files.

`internalStage`
:   Specifies the internal stage location to upload the files onto:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]int_stage_name[/path]` | Files are uploaded onto the specified named internal stage. |
    > | `@[namespace.]%table_name[/path]` | Files are uploaded onto the stage for the specified table. |
    > | `@~[/path]` | Files are uploaded onto the stage for the current user. |

    Where:

    * `namespace` is the database or schema that contains the named internal stage or table. It is optional if a
      database and schema are in use within the session.
    * `path` is an optional case-sensitive path for files in the cloud storage location that limits access to a set of files. Paths
      are alternatively called *prefixes* or *folders* by different cloud storage services.

    Note

    If the stage name or path includes spaces or special characters, enclose it in single quotes. For example, use `'@"my stage"'`
    for a stage named `"my stage"`.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`PARALLEL = integer`
:   Specifies the number of threads to use for uploading files. Snowflake uploads separate batches of data files by size:

    * Files that are smaller than 64 MB (compressed or uncompressed) are staged in parallel as individual files.
    * Larger files are automatically split into chunks, staged concurrently, and reassembled in the target stage. A single thread can
      upload multiple chunks.

    Increasing the number of threads can improve performance when uploading large files.

    Supported values: Any integer value from `1` (no parallelism) to `99` (use 99 threads for uploading files).

    Default: `4`

    Note

    A 16 MB limit applies to older versions of Snowflake drivers, including:

    * JDBC Driver versions prior to 3.12.1.
    * ODBC Driver versions prior to 2.20.5.
    * Python Connector versions prior to 2.2.0.

`AUTO_COMPRESS = TRUE | FALSE`
:   Specifies whether Snowflake uses gzip to compress files during upload:

    * `TRUE`: Snowflake compresses the files (if they are not already compressed).
    * `FALSE`: Snowflake doesn’t compress the files.

    This option does not support other compression types. To use a different compression type, compress the file separately before
    executing the PUT command. Then, identify the compression type using the `SOURCE_COMPRESSION` option.

    Ensure your local folder has sufficient space for Snowflake to compress the data files before staging them. If necessary, set the
    `TEMP`, `TMPDIR` or `TMP` environment variable in your operating system to point to a local folder that contains additional
    free space.

    Default: `TRUE`

`SOURCE_COMPRESSION = AUTO_DETECT | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Specifies the method of compression used on already-compressed files that are being staged:

    > | Supported Values | Notes |
    > | --- | --- |
    > | `AUTO_DETECT` | Compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. If you’re uploading Brotli-compressed files, explicitly use `BROTLI` instead of `AUTO_DETECT`. |
    > | `GZIP` | Doesn’t support the `*.tar.gz` file format. |
    > | `BZ2` | Doesn’t support the `*.tar.bz2` file format. |
    > | `BROTLI` | Must be used if uploading Brotli-compressed files. |
    > | `ZSTD` | Zstandard v0.8 (and higher) supported. |
    > | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
    > | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
    > | `NONE` | Data files have not been compressed. |

    Default: `AUTO_DETECT`

    Note

    Snowflake uses this option to detect how the data files were compressed so that they can be uncompressed and the data extracted
    for uploading; it does not use this option to compress the files.

    Loading files that were compressed with other utilities is not currently supported.

`OVERWRITE = TRUE | FALSE`
:   Specifies whether Snowflake overwrites an existing file with the same name during upload:

    * `TRUE`: An existing file with the same name is overwritten.
    * `FALSE`: An existing file with the same name is not overwritten.

      Snowflake performs a LIST operation on the stage in the background, which can affect the performance of the PUT operation.

      If attempts to PUT a file fail because a file with the same name exists in the target stage, you can take the following actions:

      + Load the data from the existing file into one or more tables, and remove the file from the stage. Then PUT a file with new or
        updated data onto the stage.
      + Rename the local file, and then attempt the PUT operation again.
      + Set `OVERWRITE = TRUE` in the PUT statement. Do this only if it’s safe to overwrite the existing (staged) file with the same name.

    If your Snowflake account is hosted on Google Cloud, PUT statements don’t recognize when the OVERWRITE parameter is
    set to TRUE. A PUT operation always overwrites any existing files in the target stage with the local files you’re uploading.

    The following clients support the OVERWRITE option for Snowflake accounts hosted on Amazon Web Services or Microsoft Azure:

    > * SnowSQL
    > * Snowflake ODBC Driver
    > * Snowflake JDBC Driver
    > * Snowflake Connector for Python

    Supported values: TRUE, FALSE.

    Default: `FALSE`.

## Usage notes[¶](#usage-notes "Link to this heading")

* The command cannot be executed from the Worksheets [![Worksheet tab](../../_images/ui-navigation-worksheet-icon.svg)](../../_images/ui-navigation-worksheet-icon.svg) page in either Snowflake web interface; instead, use the
  [SnowSQL client](../../user-guide/snowsql) or [Drivers](../../developer-guide/drivers) to upload data files,
  or check the documentation for a specific Snowflake client to verify support for this command.

  Alternatively, you can [use the Snowsight UI to upload files onto a name internal stage](../../user-guide/data-load-local-file-system-stage-ui.html#label-snowsight-stage-upload-files-internal).
* File-globbing patterns, like wildcards, are supported unless the files that match the pattern have divergent directory paths.
  The command *does not* support uploading multiple files with divergent directory paths, because Snowflake
  doesn’t preserve file system directory structure when uploading files onto your stage.

  For example, the following PUT statement returns an error since you
  can’t specify multiple files in nested subdirectories.

  ```
  PUT file:///tmp/data/** @my_int_stage AUTO_COMPRESS=FALSE;
  ```

  Copy
* The command does not create or rename files.
* All files stored on internal stages for data loading and unloading operations are automatically encrypted using AES-256 strong encryption
  on the server side. By default, Snowflake provides additional client-side encryption with a 128-bit key
  (with the option to configure a 256-bit key). For more information, see [encryption types for internal stages](create-stage.html#label-create-stage-internalstageparams).
* The command ignores any duplicate files you attempt to upload to the same stage. A duplicate file is an unmodified file with the same
  name as an already-staged file.

  To overwrite an already-staged file, you must modify the file you are uploading so that its contents are different from the staged file,
  which results in a new checksum for the newly-staged file.
* For the [PUT](#) and [GET](get) commands,
  an EXECUTION\_STATUS of `success` in the [QUERY\_HISTORY](../account-usage/query_history)
  does *not* mean that data files were successfully uploaded or downloaded.
  Instead, the status indicates that Snowflake received authorization to proceed with the file transfer.

Tip

For security reasons, the command times out after a set period of time. This can occur when uploading large, uncompressed data files. To
avoid timeout issues, we recommend compressing large data files using one of the supported compression types before uploading the files.
Then, specify the compression type for the files using the `SOURCE_COMPRESSION` option.

You can also consider increasing the value of the `PARALLEL` option, which can help with performance when uploading large data files.

Furthermore, to take advantage of parallel operations when loading data into tables (using the
[COPY INTO <table>](copy-into-table) command), we recommend using data files ranging in size from roughly 100 to 250 MB
compressed. If your data files are larger, consider using a third-party tool to split them into smaller files before compressing
and uploading them.

## Examples[¶](#examples "Link to this heading")

### Linux and macOS[¶](#linux-and-macos "Link to this heading")

**Load a file onto an internal stage**

Load a file named `mydata.csv` in the `/tmp/data` directory to an internal stage named
`my_int_stage`:

```
PUT file:///tmp/data/mydata.csv @my_int_stage;
```

Copy

**Load a file onto a table stage**

Load a file named `orders_001.csv` in the `/tmp/data` directory to the stage for the
`orderstiny_ext` table, with automatic data compression disabled:

```
PUT file:///tmp/data/orders_001.csv @%orderstiny_ext
  AUTO_COMPRESS = FALSE;
```

Copy

**Load multiple files onto an internal stage**

Use wildcard characters in the filename to upload multiple files:

```
PUT file:///tmp/data/orders_*01.csv @my_int_stage
  AUTO_COMPRESS = FALSE;
```

Copy

**Specify a file path with special characters**

Enclose a file path with special characters or spaces in single quotes:

```
PUT 'file:///tmp/data/orders 001.csv' @my_int_stage
  AUTO_COMPRESS = FALSE;
```

Copy

### Windows[¶](#windows "Link to this heading")

**Load a file onto the current user’s stage**

Load a file named `mydata.csv` in the `C:\temp\data` directory onto the stage for the current
user, with automatic data compression enabled:

```
PUT file://C:\temp\data\mydata.csv @~
  AUTO_COMPRESS = TRUE;
```

Copy

**Specify a file path with special characters**

To specify a Windows file path with special characters, you must
enclose the path in single quotes and change backslashes to forward slashes.

In this example, the file name contains a space (`my data.csv`):

```
PUT 'file://C:/temp/data/my data.csv' @my_int_stage
  AUTO_COMPRESS = TRUE;
```

Copy

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
4. [Usage notes](#usage-notes)
5. [Examples](#examples)
6. [Linux and macOS](#linux-and-macos)
7. [Windows](#windows)

Related content

1. [Choosing an internal stage for local files](/sql-reference/sql/../../user-guide/data-load-local-file-system-create-stage)
2. [CREATE STAGE](/sql-reference/sql/create-stage)
3. [Staging files using Snowsight](/sql-reference/sql/../../user-guide/data-load-local-file-system-stage-ui)
4. [Upload files onto a named internal stage](/sql-reference/sql/../../user-guide/data-load-local-file-system-stage-ui#label-snowsight-stage-upload-files-internal)