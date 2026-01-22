---
auto_generated: true
description: 'Downloads data files from one of the following internal stage types
  to a local directory or folder on a client machine:'
last_scraped: '2026-01-14T16:56:27.736938+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/get.html
title: GET | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[File staging](../commands-file.md)GET

# GET[¶](#get "Link to this heading")

Downloads data files from one of the following [internal stage](../../user-guide/data-load-overview.html#label-data-load-overview-internal-stages)
types to a local directory or folder on a client machine:

* Named internal stage.
* Internal stage for a specified table.
* Internal stage for the current user.

You can use this command to download data files after unloading data from a table onto a
Snowflake stage using the [COPY INTO <location>](copy-into-location) command.

For more information about using the GET command, see [Unloading into a Snowflake stage](../../user-guide/data-unload-snowflake).

See also:
:   [LIST](list) , [PUT](put) , [REMOVE](remove) , [COPY FILES](copy-files)

## Syntax[¶](#syntax "Link to this heading")

```
GET internalStage file://<local_directory_path>
    [ PARALLEL = <integer> ]
    [ PATTERN = '<regex_pattern>'' ]
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

`internalStage`
:   Specifies the location in Snowflake from which to download the files:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]int_stage_name[/path]` | Files are downloaded from the specified named internal stage. |
    > | `@[namespace.]%table_name[/path]` | Files are downloaded from the stage for the specified table. |
    > | `@~[/path]` | Files are downloaded from the stage for the current user. |

    Where:

    * `namespace` is the database and/or schema in which the named internal stage or table resides. It is optional if a
      database and schema are currently in use within the session; otherwise, it is required.
    * `path` is an optional case-sensitive path for files in the cloud storage location (that is, files have names that begin with a
      common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud
      storage services. If `path` is specified, but no file is explicitly named in the path, all data files in the path are
      downloaded.

    Note

    If the stage name or path includes spaces or special characters, it must be enclosed in single quotes (example: `'@"my stage"'`
    for a stage named `"my stage"`).

`file://local_directory_path`
:   Specifies the local directory path on the client machine where the files are downloaded:

    Linux/macOS:
    :   You must include the initial forward slash in the path (example: `file:///tmp/load`).

        If the directory path includes special characters, the entire file URI must be enclosed in single quotes.

    Windows:
    :   You must include the drive and backslash in the path (example: `file://C:tempload`).

        If the directory path includes special characters, the entire file URI must be enclosed in single quotes. Note that
        the drive and path separator is a forward slash (`/`) in enclosed URIs (example: `'file://C:/Users/%Username%/Data 2025-01'`).

    Note

    The GET command returns an error if you specify a filename as part of the path, except if you use the
    [JDBC driver](../../developer-guide/jdbc/jdbc) or [ODBC driver](../../developer-guide/odbc/odbc). If you specify a filename when
    using either driver, the driver treats the filename as part of the directory path and creates a subdirectory with the specified
    filename.

    For example, if you specify `file:///tmp/load/file.csv`, the JDBC or ODBC driver creates a subdirectory named `file.csv/`
    under the path `/tmp/load/`. The GET command then downloads the staged files into this new subdirectory.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`PARALLEL = integer`
:   Specifies the number of threads to use for downloading the files. The granularity unit for downloading is one file.

    Increasing the number of threads can improve performance when downloading large files.

    Supported values: Any integer value from `1` (no parallelism) to `99` (use 99 threads for downloading files).

    Default: `10`

`PATTERN = 'regex_pattern'`
:   Specifies a regular expression pattern for filtering files to download. The command lists all files in the specified `path`
    and applies the regular expression pattern on each of the files found.

    Default: No value (all files in the specified stage are downloaded)

## Usage notes[¶](#usage-notes "Link to this heading")

* GET does not support the following actions:

  + Downloading files from external stages. To download files from external stages, use the utilities
    provided by your cloud service.
  + Downloading multiple files with divergent directory paths. The command
    *does not* preserve stage directory structure when transferring files to your client machine.

    For example, the following GET statement returns an error since you can’t download multiple files named `tmp.parquet` that are in
    different subdirectories on the stage.

    ```
    GET @my_int_stage my_target_path PATTERN = "tmp.parquet";
    ```

    Copy
* The [ODBC driver](../../developer-guide/odbc/odbc) supports GET with Snowflake accounts hosted on the following platforms:

> * Amazon Web Services (using ODBC Driver Version 2.17.5 and higher).
> * Google Cloud (using ODBC Driver Version 2.21.5 and higher).
> * Microsoft Azure (using ODBC Driver Version 2.20.2 and higher).

* The command cannot be executed from the Worksheets [![Worksheet tab](../../_images/ui-navigation-worksheet-icon.svg)](../../_images/ui-navigation-worksheet-icon.svg) page in either Snowflake web interface; instead, use the
  SnowSQL client to download data files, or check the documentation for the specific Snowflake client to verify support for this command.
* The command does not rename files.
* Downloaded files are automatically decrypted using the same key that was used to encrypt the file when it was either uploaded
  (using [PUT](put)) or unloaded from a table (using [COPY INTO <location>](copy-into-location)).
* For the [PUT](put) and [GET](#) commands,
  an EXECUTION\_STATUS of `success` in the [QUERY\_HISTORY](../account-usage/query_history)
  does *not* mean that data files were successfully uploaded or downloaded.
  Instead, the status indicates that Snowflake received authorization to proceed with the file transfer.

## Examples[¶](#examples "Link to this heading")

Download all files in the stage for the `mytable` table to the `/tmp/data` local directory (in a Linux or macOS environment):

> ```
> GET @%mytable file:///tmp/data/;
> ```
>
> Copy

Download files from the `myfiles` path in the stage for the current user to the `/tmp/data` local directory (in a Linux or
macOS environment):

> ```
> GET @~/myfiles file:///tmp/data/;
> ```
>
> Copy

For additional examples, see [Unloading into a Snowflake stage](../../user-guide/data-unload-snowflake).

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

Related content

1. [CREATE STAGE](/sql-reference/sql/create-stage)
2. [Staging files using Snowsight](/sql-reference/sql/../../user-guide/data-load-local-file-system-stage-ui)