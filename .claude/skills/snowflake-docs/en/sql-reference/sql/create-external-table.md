---
auto_generated: true
description: Creates a new external table in the current or specified schema or replaces
  an existing external table. When queried, an external table reads data from a set
  of one or more files in a specified extern
last_scraped: '2026-01-14T16:56:04.777599+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-external-table
title: CREATE EXTERNAL TABLE | Snowflake Documentation
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

     + [SHOW OBJECTS](show-objects.md)
     + Table
     + [CREATE TABLE](create-table.md)
     + [ALTER TABLE](alter-table.md)
     + [DROP TABLE](drop-table.md)
     + [UNDROP TABLE](undrop-table.md)
     + [SHOW TABLES](show-tables.md)
     + [SHOW COLUMNS](show-columns.md)
     + [SHOW PRIMARY KEYS](show-primary-keys.md)
     + [DESCRIBE TABLE](desc-table.md)
     + [DESCRIBE SEARCH OPTIMIZATION](desc-search-optimization.md)
     + [TRUNCATE TABLE](truncate-table.md)
     + Dynamic table
     + [CREATE DYNAMIC TABLE](create-dynamic-table.md)
     + [ALTER DYNAMIC TABLE](alter-dynamic-table.md)
     + [DESCRIBE DYNAMIC TABLE](desc-dynamic-table.md)
     + [DROP DYNAMIC TABLE](drop-dynamic-table.md)
     + [UNDROP DYNAMIC TABLE](undrop-dynamic-table.md)
     + [SHOW DYNAMIC TABLES](show-dynamic-tables.md)
     + Event table
     + [CREATE EVENT TABLE](create-event-table.md)
     + [ALTER TABLE (Event Table)](alter-table-event-table.md)")
     + [SHOW EVENT TABLES](show-event-tables.md)
     + [DESCRIBE EVENT TABLE](desc-event-table.md)
     + External table
     + [CREATE EXTERNAL TABLE](create-external-table.md)
     + [ALTER EXTERNAL TABLE](alter-external-table.md)
     + [DROP EXTERNAL TABLE](drop-external-table.md)
     + [SHOW EXTERNAL TABLES](show-external-tables.md)
     + [DESCRIBE EXTERNAL TABLE](desc-external-table.md)
     + Hybrid table
     + [CREATE HYBRID TABLE](create-hybrid-table.md)
     + [CREATE INDEX](create-index.md)
     + [DROP INDEX](drop-index.md)
     + [SHOW HYBRID TABLES](show-hybrid-tables.md)
     + [SHOW INDEXES](show-indexes.md)
     + Apache Iceberg™ table
     + [CREATE ICEBERG TABLE](create-iceberg-table.md)
     + [ALTER ICEBERG TABLE](alter-iceberg-table.md)
     + [DROP ICEBERG TABLE](drop-iceberg-table.md)
     + [UNDROP ICEBERG TABLE](undrop-iceberg-table.md)
     + [SHOW ICEBERG TABLES](show-iceberg-tables.md)
     + [DESCRIBE ICEBERG TABLE](desc-iceberg-table.md)
     + Interactive tables and warehouses
     + [CREATE INTERACTIVE TABLE](create-interactive-table.md)
     + [CREATE INTERACTIVE WAREHOUSE](create-interactive-warehouse.md)
     + View
     + [CREATE VIEW](create-view.md)
     + [ALTER VIEW](alter-view.md)
     + [DROP VIEW](drop-view.md)
     + [SHOW VIEWS](show-views.md)
     + [DESCRIBE VIEW](desc-view.md)
     + Materialized view
     + [CREATE MATERIALIZED VIEW](create-materialized-view.md)
     + [ALTER MATERIALIZED VIEW](alter-materialized-view.md)
     + [DROP MATERIALIZED VIEW](drop-materialized-view.md)
     + [SHOW MATERIALIZED VIEWS](show-materialized-views.md)
     + [DESCRIBE MATERIALIZED VIEW](desc-materialized-view.md)
     + [TRUNCATE MATERIALIZED VIEW](truncate-materialized-view.md)
     + Semantic view
     + [CREATE SEMANTIC VIEW](create-semantic-view.md)
     + [ALTER SEMANTIC VIEW](alter-semantic-view.md)
     + [DROP SEMANTIC VIEW](drop-semantic-view.md)
     + [SHOW SEMANTIC VIEWS](show-semantic-views.md)
     + [SHOW SEMANTIC DIMENSIONS](show-semantic-dimensions.md)
     + [SHOW SEMANTIC DIMENSIONS FOR METRIC](show-semantic-dimensions-for-metric.md)
     + [SHOW SEMANTIC FACTS](show-semantic-facts.md)
     + [SHOW SEMANTIC METRICS](show-semantic-metrics.md)
     + [DESCRIBE SEMANTIC VIEW](desc-semantic-view.md)
     + Sequence
     + [CREATE SEQUENCE](create-sequence.md)
     + [ALTER SEQUENCE](alter-sequence.md)
     + [DROP SEQUENCE](drop-sequence.md)
     + [SHOW SEQUENCES](show-sequences.md)
     + [DESCRIBE SEQUENCE](desc-sequence.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)CREATE EXTERNAL TABLE

# CREATE EXTERNAL TABLE[¶](#create-external-table "Link to this heading")

Creates a new [external table](../../user-guide/tables-external-intro) in the current or specified schema
or replaces an existing external table. When queried, an external table reads
data from a set of one or more files in a specified external stage, and then outputs the data in a single VARIANT column.

Additional columns can be defined, with each column definition consisting of a name, data type, and optionally whether the column requires
a value (NOT NULL) or has any referential integrity constraints (such as primary key, foreign key). For more information, see the usage notes.

See also:
:   [ALTER EXTERNAL TABLE](alter-external-table) , [DROP EXTERNAL TABLE](drop-external-table) , [SHOW EXTERNAL TABLES](show-external-tables) , [DESCRIBE EXTERNAL TABLE](desc-external-table)

## Syntax[¶](#syntax "Link to this heading")

```
-- Partitions computed from expressions
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  [ REFRESH_ON_CREATE =  { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ PATTERN = '<regex_pattern>' ]
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ AWS_SNS_TOPIC = '<string>' ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]

-- Partitions added and removed manually
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  PARTITION_TYPE = USER_SPECIFIED
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]

-- Delta Lake
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  PARTITION_TYPE = USER_SPECIFIED
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ TABLE_FORMAT = DELTA ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

Copy

Where:

> ```
> inlineConstraint ::=
>   [ NOT NULL ]
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE | PRIMARY KEY | [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> ] ) ] }
>   [ <constraint_properties> ]
> ```
>
> Copy
>
> For additional inline constraint details, see [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint).
>
> ```
> cloudProviderParams (for Google Cloud Storage) ::=
>   [ INTEGRATION = '<integration_name>' ]
>
> cloudProviderParams (for Microsoft Azure) ::=
>   [ INTEGRATION = '<integration_name>' ]
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
> formatTypeOptions ::=
> -- If FILE_FORMAT = ( TYPE = CSV ... )
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      RECORD_DELIMITER = '<string>' | NONE
>      FIELD_DELIMITER = '<string>' | NONE
>      MULTI_LINE = TRUE | FALSE
>      SKIP_HEADER = <integer>
>      SKIP_BLANK_LINES = TRUE | FALSE
>      ESCAPE_UNENCLOSED_FIELD = '<character>' | NONE
>      TRIM_SPACE = TRUE | FALSE
>      FIELD_OPTIONALLY_ENCLOSED_BY = '<character>' | NONE
>      NULL_IF = ( '<string1>' [ , '<string2>' , ... ] )
>      EMPTY_FIELD_AS_NULL = TRUE | FALSE
>      ENCODING = '<string>'
> -- If FILE_FORMAT = ( TYPE = JSON ... )
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      MULTI_LINE = TRUE | FALSE
>      ALLOW_DUPLICATE = TRUE | FALSE
>      STRIP_OUTER_ARRAY = TRUE | FALSE
>      STRIP_NULL_VALUES = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
> -- If FILE_FORMAT = ( TYPE = AVRO ... )
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
> -- If FILE_FORMAT = ( TYPE = ORC ... )
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ]
> -- If FILE_FORMAT = ( TYPE = PARQUET ... )
>      COMPRESSION = AUTO | SNAPPY | NONE
>      BINARY_AS_TEXT = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
> ```
>
> Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

### CREATE EXTERNAL TABLE … USING TEMPLATE[¶](#create-external-table-using-template "Link to this heading")

Creates a new external table with the column definitions derived from a set of staged files that contain semi-structured data. This feature supports Apache Parquet, Apache Avro, ORC, JSON, and CSV files. The support for CSV and JSON files is currently in preview.

> ```
> CREATE [ OR REPLACE ] EXTERNAL TABLE <table_name>
>   USING TEMPLATE <query>
>   [ ... ]
>   [ COPY GRANTS ]
> ```
>
> Copy

Note

If the statement is replacing an existing table of the same name, then the grants are copied from the table
being replaced. If there is no existing table of that name, then the grants are copied from the source table
being cloned.

For more information about COPY GRANTS, see [COPY GRANTS](create-table.html#label-create-table-copy-grants) in this document.

## Required parameters[¶](#required-parameters "Link to this heading")

`table_name`
:   String that specifies the identifier (that is, name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and can’t contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case sensitive.

    For more information, see [Identifier requirements](../identifiers-syntax).

`[ WITH ] LOCATION =`
:   Specifies the external stage and optional path where the files containing data to be read are staged:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]ext_stage_name[/path]` | Files are in the specified named external stage. |

    Neither string literals nor SQL variables are supported.

    Where:

    > * `namespace` is the database or schema in which the external stage resides, in the form of `database_name.schema_name`
    >   or `schema_name`. It is optional if a database and schema are currently in use within the user session; otherwise, it
    >   is required.
    > * `path` is an optional case-sensitive directory path for files in the cloud storage location that limits the set of files to load.
    >   Paths are alternatively called *prefixes* or *folders* by different cloud storage services.
    >
    >   The external table appends this directory path to any path specified in the stage definition. To view the stage definition,
    >   run `DESC STAGE stage_name` and check the `url` property value. For example, if the stage URL includes
    >   path `a` and the external table location includes path `b`, then the external table reads files staged in
    >   `stage/a/b`.
    >
    >   Note
    >
    >   + Specify a full *directory* path, and not a partial path (shared prefix) for files in your storage location (for example, use a path like `@my_ext_stage/2025/`
    >     instead of `@my_ext_stage/2025-*`). To filter for files that share a common prefix, use partition columns instead.
    >   + The `[ WITH ] LOCATION` value cannot reference specific file names. To point an external table to individual
    >     staged files, use the `PATTERN` parameter.

`FILE_FORMAT = ( FORMAT_NAME = 'file_format_name' )` or . `FILE_FORMAT = ( TYPE = CSV | JSON | AVRO | ORC | PARQUET [ ... ] )`
:   String (constant) that specifies the file format:

    > `FORMAT_NAME = file_format_name`
    > :   Specifies an existing named file format that describes the staged data files to scan. The named file format determines the format
    >     type (such as, CSV, JSON), and any other format options, for data files.
    >
    > `TYPE = CSV | JSON | AVRO | ORC | PARQUET [ ... ]`
    > :   Specifies the format type of the staged data files to scan when querying the external table.
    >
    >     If a file format type is specified, additional format-specific options can be specified. For more information, see
    >     [Format Type Options](#label-create-ext-table-formattypeoptions) in this topic.

    Default: `TYPE = CSV`.

    Important

    An external table doesn’t inherit FILE\_FORMAT options specified in a stage definition when that stage is used for loading data into the table. To specify FILE\_FORMAT options, you must explicitly do so in the external table definition. Snowflake uses defaults for any FILE\_FORMAT parameters omitted from the external table definition.

    Note

    `FORMAT_NAME` and `TYPE` are mutually exclusive; to avoid unintended behavior, only specify one or the other
    when you create an external table.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`col_name`
:   String that specifies the column identifier (that is, name). All the requirements for table identifiers also apply to column identifiers.

    For more information, see [Identifier requirements](../identifiers-syntax).

`col_type`
:   String (constant) that specifies the data type for the column. The data type must match the result of `expr` for the column.

    For information about the data types that can be specified for table columns, see [SQL data types reference](../../sql-reference-data-types).

`expr`
:   String that specifies the expression for the column. When queried, the column returns results derived from this expression.

    External table columns are virtual columns, which are defined by using an explicit expression. Add virtual columns as expressions by using the
    VALUE column or the METADATA$FILENAME pseudocolumn:

    VALUE:
    :   A VARIANT type column that represents a single row in the external file.

        CSV:
        :   The VALUE column structures each row as an object with elements identified by column position (that is,
            `{c1: <column_1_value>, c2: <column_2_value>, c3: <column_1_value> ...}`).

            For example, add a VARCHAR column named `mycol` that references the first column in the staged CSV files:

            ```
            mycol varchar as (value:c1::varchar)
            ```

            Copy

        Semi-structured data:
        :   Enclose element names and values in double-quotes. Traverse the path in the VALUE column by using dot notation.

            Suppose the following example represents a single row of semi-structured data in a staged file:

            ```
            { "a":"1", "b": { "c":"2", "d":"3" } }
            ```

            Copy

            Add a VARCHAR column named `mycol` that references the nested repeating `c` element in the staged file:

            ```
            mycol varchar as (value:"b"."c"::varchar)
            ```

            Copy

    METADATA$FILENAME:
    :   A pseudocolumn that identifies the name of each staged data file that is included in the external table, including its path in the stage. For
        an example, see [Partitions Added Automatically From Partition Column Expressions](#partitions-added-automatically-from-partition-column-expressions) in this topic.

`CONSTRAINT ...`
:   String that defines an inline or out-of-line constraint for the specified columns in the table.

    For syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](create-table-constraint). For more information about constraints, see
    [Constraints](../constraints).

`REFRESH_ON_CREATE = TRUE | FALSE`
:   Specifies whether to automatically refresh the external table metadata one time, immediately after the external table is created. Refreshing
    the external table metadata synchronizes the metadata with the current list of data files in the specified stage path. This action is
    required for the metadata to register any existing data files in the named external stage specified in the
    `[ WITH ] LOCATION =` setting.

    `TRUE`
    :   Snowflake automatically refreshes the external table metadata one time after creation.

        Note

        If the specified location contains close to 1 million files or more, we recommend that you
        set `REFRESH_ON_CREATE = FALSE`. After you create the external table, refresh the metadata
        incrementally by running ALTER EXTERNAL TABLE … REFRESH statements that specify subpaths in
        the location (that is, subsets of files to include in the refresh) until the metadata includes
        all of the files in the location.

    `FALSE`
    :   Snowflake doesn’t automatically refresh the external table metadata. To register any existing data files in the stage, you must
        manually refresh the external table metadata one time by using [ALTER EXTERNAL TABLE](alter-external-table) … REFRESH.

    Default: `TRUE`

`AUTO_REFRESH = TRUE | FALSE`
:   Specifies whether Snowflake should enable triggering automatic refreshes of the external table metadata when new or updated data
    files are available in the named external stage specified in the `[ WITH ] LOCATION =` setting.

    Note

    * Setting this parameter to TRUE isn’t supported by partitioned external tables when partitions are added manually by the
      object owner (that is, when `PARTITION_TYPE = USER_SPECIFIED`).
    * Setting this parameter to TRUE isn’t supported for external tables that reference data files
      in S3-compatible storage (a storage application or device
      that provides an API compliant with the S3 REST API). For more information, see [Working with Amazon S3-compatible storage](../../user-guide/data-load-s3-compatible-storage).

      You must manually refresh the metadata by running an [ALTER EXTERNAL TABLE … REFRESH](alter-external-table) command.
    * You must configure an event notification for your storage location to notify Snowflake when new or updated data is available
      to read into the external table metadata. For more information, see the instructions for your cloud storage service:

      + Amazon S3:
        :   [Refresh external tables automatically for Amazon S3](../../user-guide/tables-external-s3)
      + Google Cloud Storage:
        :   [Refresh external tables automatically for Google Cloud Storage](../../user-guide/tables-external-gcs)
      + Microsoft Azure:
        :   [Refresh external tables automatically for Azure Blob Storage](../../user-guide/tables-external-azure)
    * When an external table is created, its metadata is refreshed automatically one time unless `REFRESH_ON_CREATE = FALSE`.

    `TRUE`
    :   Snowflake enables triggering automatic refreshes of the external table metadata.

    `FALSE`
    :   Snowflake doesn’t enable triggering automatic refreshes of the external table metadata. You must manually refresh the external table
        metadata periodically by using [ALTER EXTERNAL TABLE](alter-external-table) … REFRESH to synchronize the metadata with the current list of files in the
        stage path.

    Default: `TRUE`

`PATTERN = 'regex_pattern'`
:   A regular expression pattern string, enclosed in single quotes, specifying the filenames and paths on the external stage to match.

    Tip

    For the best performance, don’t apply patterns that filter on a large number of files.

`AWS_SNS_TOPIC = 'string'`
:   Required only when configuring AUTO\_REFRESH for Amazon S3 stages using Amazon Simple Notification Service (SNS). Specifies the
    Amazon Resource Name (ARN) for the SNS topic for your S3 bucket. The CREATE EXTERNAL TABLE statement subscribes the Amazon Simple Queue
    Service (SQS) queue to the specified SNS topic. Event notifications through the SNS topic trigger metadata refreshes. For more information,
    see [Refresh external tables automatically for Amazon S3](../../user-guide/tables-external-s3).

`TABLE_FORMAT = DELTA`
:   Note

    This feature is still supported but will be deprecated in a future release.

    Consider using an [Apache Iceberg™ table](../../user-guide/tables-iceberg) instead. Iceberg tables
    use an [external volume](../../user-guide/tables-iceberg.html#label-tables-iceberg-external-volume-def)
    to connect to Delta table files in your cloud storage.

    For more information, see [Iceberg tables](../../user-guide/tables-iceberg) and [CREATE ICEBERG TABLE (Delta files in object storage)](create-iceberg-table-delta).
    You can also [Migrate a Delta external table to Apache Iceberg™](../../user-guide/tables-external-intro.html#label-tables-external-intro-migrate-to-iceberg).

    Identifies the external table as referencing a Delta Lake on the cloud storage location. A Delta Lake on Amazon S3, Google Cloud Storage,
    or Microsoft Azure cloud storage is supported.

    Note

    This [preview feature](../../release-notes/preview-features) is available to all accounts.

    When this parameter is set, the external table scans for Delta Lake transaction log files in the `[ WITH ] LOCATION` location.
    Delta log files have names like `_delta_log/00000000000000000000.json` and
    `_delta_log/00000000000000000010.checkpoint.parquet`.

    When the metadata for an external table is refreshed, Snowflake parses the Delta Lake transaction logs and determines which Parquet
    files are current. In the background, the refresh performs add and remove file operations to keep the external table metadata in sync.

    Note

    * The external stage and optional path specified in `[ WITH ] LOCATION =` must contain the data files and metadata for a
      single Delta Lake table only. That is, the specified storage location can only contain one `__delta_log`
      directory.
    * The ordering of event notifications triggered by DDL operations in cloud storage isn’t guaranteed. Therefore, the ability to
      automatically refresh isn’t available for external tables that reference Delta Lake files. Both `REFRESH_ON_CREATE` and
      `AUTO_REFRESH` must be set to FALSE.

      Periodically run an [ALTER EXTERNAL TABLE … REFRESH](alter-external-table) statement to register any
      added or removed files.
    * The `FILE_FORMAT` value must specify Parquet as the file type.
    * For optimal performance, we recommend defining partition columns for the external table.
    * The following parameters aren’t supported when referencing a Delta Lake:

      + `AWS_SNS_TOPIC = 'string'`
      + `PATTERN = 'regex_pattern'`

`COPY GRANTS`
:   Specifies retaining the access permissions from the original table when an external table is recreated using the CREATE OR REPLACE TABLE
    variant. The parameter copies all permissions, except OWNERSHIP, from the existing table to the new table. By default, the role
    that runs the CREATE EXTERNAL TABLE command owns the new external table.

    Note

    The operation to copy grants occurs atomically in the CREATE EXTERNAL TABLE command (that is, within the same transaction).

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the external table.

    Default: No value

`ROW ACCESS POLICY <policy_name> ON (VALUE)`
:   Specifies the [row access policy](../../user-guide/security-row-intro) to set on the table.

    Specify the VALUE column when applying a row access policy to an external table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](../../user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](../../user-guide/object-tagging/introduction.html#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](../../user-guide/contacts-using).

### Partitioning parameters[¶](#partitioning-parameters "Link to this heading")

Use these parameters to partition your external table.

`part_col_name col_type AS part_expr`
:   Defines one or more partition columns in the external table.

    The format of a partition column definition differs depending on whether partitions are computed and added automatically from an
    expression in each partition column or the partitions are added manually.

    Added from an expression:
    :   A partition column must evaluate as an expression that parses the path or filename information in the METADATA$FILENAME
        pseudocolumn. Partition columns optimize query performance by pruning out the data files that don’t need to be scanned (that is,
        partitioning the external table). A partition consists of all data files that match the path or filename in the expression for
        the partition column.

        |  |  |
        | --- | --- |
        | `part_col_name` | String that specifies the partition column identifier (that is, name). All the requirements for table identifiers also apply to column identifiers. |
        | `col_type` | String (constant) that specifies the data type for the column. The data type must match the result of `part_expr` for the column. |
        | `part_expr` | String that specifies the expression for the column. The expression must include the METADATA$FILENAME pseudocolumn. |

        External tables currently support the following subset of functions in partition expressions:

        * `=`, `<>`, `>`, `>=`, `<`, `<=`
        * `||`
        * `+`, `-`
        * `-` (negate)
        * `*`
        * `AND`, `OR`
        * [ARRAY\_CONSTRUCT](../functions/array_construct)
        * [CASE](../functions/case)
        * [CAST , ::](../functions/cast)
        * [CONCAT , ||](../functions/concat)
        * [ENDSWITH](../functions/endswith)
        * [IS [ NOT ] NULL](../functions/is-null)
        * [IFF](../functions/iff)
        * [IFNULL](../functions/ifnull)
        * [[ NOT ] IN](../functions/in)
        * [LOWER](../functions/lower)
        * `NOT`
        * [NULLIF](../functions/nullif)
        * [NVL2](../functions/nvl2)
        * [SPLIT\_PART](../functions/split_part)
        * [STARTSWITH](../functions/startswith)
        * [SUBSTR , SUBSTRING](../functions/substr)
        * [UPPER](../functions/upper)
        * [ZEROIFNULL](../functions/zeroifnull)

    Added manually:
    :   Required: Also set the `PARTITION_TYPE` parameter value to `USER_SPECIFIED`.

        A partition column definition is an expression that parses the column metadata in the internal (hidden)
        METADATA$EXTERNAL\_TABLE\_PARTITION column. Essentially, the definition only defines the data type for the column. The following example shows the format of the
        partition column definition:

        `part_col_name col_type AS ( PARSE_JSON (METADATA$EXTERNALTABLE_PARTITION):part_col_name::data_type )`

        For example, suppose columns `col1`, `col2`, and `col3` contain varchar, number, and timestamp (time zone) data, respectively:

        ```
        col1 varchar as (parse_json(metadata$external_table_partition):col1::varchar),
        col2 number as (parse_json(metadata$external_table_partition):col2::number),
        col3 timestamp_tz as (parse_json(metadata$external_table_partition):col3::timestamp_tz)
        ```

        Copy

    After defining any partition columns for the table, identify these columns by using the PARTITION BY clause.

    Note

    The maximum length of user-specified partition column names is 32 characters.

`PARTITION_TYPE = USER_SPECIFIED`
:   Defines the partition type for the external table as *user-defined*. The owner of the external table (that is, the role that has the
    OWNERSHIP privilege on the external table) must add partitions to the external metadata manually by running ALTER EXTERNAL
    TABLE … ADD PARTITION statements.

    Don’t set this parameter if partitions are added to the external table metadata automatically upon evaluation of expressions
    in the partition columns.

`[ PARTITION BY ( part_col_name [, part_col_name ... ] ) ]`
:   Specifies any partition columns to evaluate for the external table.

    Usage:
    :   When you query an external table, include one or more partition columns in a WHERE clause; for example:

        `... WHERE part_col_name = 'filter_value'`

        Snowflake filters on the partition columns to restrict the set of data files to scan. All rows in these files are scanned.
        If a WHERE clause includes non-partition columns, those filters are evaluated after the data files are filtered.

        A common practice is to partition the data files based on increments of time; or, if the data files are staged from multiple sources,
        to partition by a data source identifier and date or timestamp.

## Cloud provider parameters (`cloudProviderParams`)[¶](#cloud-provider-parameters-cloudproviderparams "Link to this heading")

> **Google Cloud Storage**
>
> > `INTEGRATION = integration_name`
> > :   Specifies the name of the notification integration used to automatically refresh the external table metadata using Google Pub/Sub
> >     event notifications. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party
> >     cloud message queuing services.
> >
> >     This parameter is required to enable auto-refresh operations for the external table. For instructions about how to configure the
> >     auto-refresh capability, see [Refresh external tables automatically for Google Cloud Storage](../../user-guide/tables-external-gcs).
>
> **Microsoft Azure**
>
> > `INTEGRATION = integration_name`
> > :   Specifies the name of the notification integration used to automatically refresh the external table metadata using Azure Event Grid
> >     notifications. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party cloud
> >     message queuing services.
> >
> >     This parameter is required to enable auto-refresh operations for the external table. For instructions about how to configure the auto-refresh
> >     capability, see [Refresh external tables automatically for Azure Blob Storage](../../user-guide/tables-external-azure).

## Format type options (`formatTypeOptions`)[¶](#format-type-options-formattypeoptions "Link to this heading")

Format type options are used for [loading data into](../../guides-overview-loading-data) and [unloading data out of](../../user-guide/data-unload-overview)
tables.

Depending on the file format type specified (`FILE_FORMAT = ( TYPE = ... )`), you can include one or more of the following
format-specific options (separated by blank spaces, commas, or new lines):

### TYPE = CSV[¶](#type-csv "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   String (constant) that specifies the current compression algorithm for the data files to be queried. Snowflake uses this option to detect
    how already-compressed data files were compressed so that the compressed data in the files can be extracted for querying.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. If querying Brotli-compressed files, explicitly use `BROTLI` instead of `AUTO`. |
    | `GZIP` |  |
    | `BZ2` |  |
    | `BROTLI` | Must be specified when querying Brotli-compressed files. |
    | `ZSTD` | Zstandard v0.8 (and higher) supported. |
    | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
    | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
    | `NONE` | Data files have not been compressed. |

`RECORD_DELIMITER = 'string' | NONE`
:   One or more characters that separate records in an input file. Accepts common escape sequences or the following singlebyte or multibyte characters:

    Singlebyte characters:
    :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

    Multibyte characters:
    :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

        The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (e.g. `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

    The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

    Also accepts a value of `NONE`.

    Default: New line character. Note that “new line” is logical such that `\r\n` is understood as a new line for files on a Windows platform.

`FIELD_DELIMITER = 'string' | NONE`
:   One or more singlebyte or multibyte characters that separate fields in an input file. Accepts common escape sequences or the following singlebyte or multibyte characters:

    Singlebyte characters:
    :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

    Multibyte characters:
    :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

        The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (e.g. `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

        > Note
        >
        > For non-ASCII characters, you must use the hex byte sequence value to get a deterministic behavior.

    The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

    Also accepts a value of `NONE`.

    Default: comma (`,`)

`MULTI_LINE = TRUE | FALSE`
:   Boolean that specifies whether multiple lines are allowed.

    If MULTI\_LINE is set to `FALSE` and the specified record delimiter is present within a CSV field, the record containing the field will be interpreted as an error.

    Default: `TRUE`

`SKIP_HEADER = integer`
:   Number of lines at the start of the file to skip.

    Note that SKIP\_HEADER does not use the RECORD\_DELIMITER or FIELD\_DELIMITER values to determine what a header line is; rather, it simply skips the specified number of CRLF (Carriage Return, Line Feed)-delimited lines in the file. RECORD\_DELIMITER and FIELD\_DELIMITER are then used to determine the rows of data to query.

    Default: `0`

`SKIP_BLANK_LINES = TRUE | FALSE`
:   Use:
    :   Data querying only

    Definition:
    :   Boolean that specifies to skip any blank lines encountered in the data files; otherwise, blank lines produce an end-of-record error (default behavior).

    Default: `FALSE`

`ESCAPE_UNENCLOSED_FIELD = 'character' | NONE`
:   A singlebyte character string used as the escape character for unenclosed field values only. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_DELIMITER` or `RECORD_DELIMITER` characters in the data as literals. The escape character can also be used to escape instances of itself in the data.

    Accepts common escape sequences, octal values, or hex values.

    Specifies the escape character for unenclosed fields only.

    Note

    * The default value is `\\`. If a row in a data file ends in the backslash (`\`) character, this character escapes the newline or
      carriage return character specified for the `RECORD_DELIMITER` file format option. As a result, this row and the next row are
      handled as a single row of data. To avoid this issue, set the value to `NONE`.
    * This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
      as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
      the option value.

      In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
      option as the character encoding for your data files to ensure the character is interpreted correctly.

    Default: backslash (`\\`)

`TRIM_SPACE = TRUE | FALSE`
:   Boolean that specifies whether to remove white space from fields.

    For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
    field (that is, the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces when querying data.

    As another example, if leading or trailing spaces surround quotes that enclose strings, you can remove the surrounding spaces using this option and the quote character using the
    `FIELD_OPTIONALLY_ENCLOSED_BY` option. Note that any spaces within the quotes are preserved. For example, assuming `FIELD_DELIMITER = '|'` and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`:

    ```
    |"Hello world"|    /* returned as */  >Hello world<
    |" Hello world "|  /* returned as */  > Hello world <
    | "Hello world" |  /* returned as */  >Hello world<
    ```

    Copy

    Note that the brackets in this example are not returned; they are used to demarcate the beginning and end of the returned strings.

    Default: `FALSE`

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Character used to enclose strings. Value can be `NONE`, single quote character (`'`), or double quote character (`"`). To use the single quote character, use the octal or hex representation (`0x27`) or the double single-quoted escape (`''`).

    Default: `NONE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   String used to convert to and from SQL NULL:

    When querying data, Snowflake replaces these values in the returned data with SQL NULL. To specify more than one string, enclose
    the list of strings in parentheses and use commas to separate each value.

    Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as
    a value, all instances of `2` as either a string or number are converted.

    For example:

    `NULL_IF = ('\N', 'NULL', 'NUL', '')`

    Note that this option can include empty strings.

    Default: `\N` (that is, NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\\`)

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   Specifies whether to return SQL NULL for empty fields in an input file, which are represented by two successive delimiters (e.g. `,,`).

    If set to `FALSE`, Snowflake attempts to cast an empty field to the corresponding column type. An empty string is returned for columns of type STRING. For other column types, the query returns an error.

    Default: `TRUE`

`ENCODING = 'string'`
:   String (constant) that specifies the character set of the source data when querying data.

    > | Character Set | `ENCODING` Value | Supported Languages | Notes |
    > | --- | --- | --- | --- |
    > | Big5 | `BIG5` | Traditional Chinese |  |
    > | EUC-JP | `EUCJP` | Japanese |  |
    > | EUC-KR | `EUCKR` | Korean |  |
    > | GB18030 | `GB18030` | Chinese |  |
    > | IBM420 | `IBM420` | Arabic |  |
    > | IBM424 | `IBM424` | Hebrew |  |
    > | IBM949 | `IBM949` | Korean |  |
    > | ISO-2022-CN | `ISO2022CN` | Simplified Chinese |  |
    > | ISO-2022-JP | `ISO2022JP` | Japanese |  |
    > | ISO-2022-KR | `ISO2022KR` | Korean |  |
    > | ISO-8859-1 | `ISO88591` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
    > | ISO-8859-2 | `ISO88592` | Czech, Hungarian, Polish, Romanian |  |
    > | ISO-8859-5 | `ISO88595` | Russian |  |
    > | ISO-8859-6 | `ISO88596` | Arabic |  |
    > | ISO-8859-7 | `ISO88597` | Greek |  |
    > | ISO-8859-8 | `ISO88598` | Hebrew |  |
    > | ISO-8859-9 | `ISO88599` | Turkish |  |
    > | ISO-8859-15 | `ISO885915` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish | Identical to ISO-8859-1 except for 8 characters, including the Euro currency symbol. |
    > | KOI8-R | `KOI8R` | Russian |  |
    > | Shift\_JIS | `SHIFTJIS` | Japanese |  |
    > | UTF-8 | `UTF8` | All languages | For loading data from delimited files (CSV, TSV, etc.), UTF-8 is the default. . . For loading data from all other supported file formats (JSON, Avro, etc.), as well as unloading data, UTF-8 is the only supported character set. |
    > | UTF-16 | `UTF16` | All languages |  |
    > | UTF-16BE | `UTF16BE` | All languages |  |
    > | UTF-16LE | `UTF16LE` | All languages |  |
    > | UTF-32 | `UTF32` | All languages |  |
    > | UTF-32BE | `UTF32BE` | All languages |  |
    > | UTF-32LE | `UTF32LE` | All languages |  |
    > | windows-874 | `WINDOWS874` | Thai |  |
    > | windows-949 | `WINDOWS949` | Korean |  |
    > | windows-1250 | `WINDOWS1250` | Czech, Hungarian, Polish, Romanian |  |
    > | windows-1251 | `WINDOWS1251` | Russian |  |
    > | windows-1252 | `WINDOWS1252` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
    > | windows-1253 | `WINDOWS1253` | Greek |  |
    > | windows-1254 | `WINDOWS1254` | Turkish |  |
    > | windows-1255 | `WINDOWS1255` | Hebrew |  |
    > | windows-1256 | `WINDOWS1256` | Arabic |  |

    Default: `UTF8`

    Note

    Snowflake stores all data internally in the UTF-8 character set. The data is converted into UTF-8.

### TYPE = JSON[¶](#type-json "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   String (constant) that specifies the current compression algorithm for the data files to be returned. Snowflake uses this option to
    detect how already-compressed data files were compressed so that the compressed data in the files can be extracted for querying.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. If querying Brotli-compressed files, explicitly use `BROTLI` instead of `AUTO`. |
    | `GZIP` |  |
    | `BZ2` |  |
    | `BROTLI` |  |
    | `ZSTD` |  |
    | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
    | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
    | `NONE` | Indicates the files have not been compressed. |

    Default: `AUTO`

`MULTI_LINE = TRUE | FALSE`
:   Boolean that specifies whether multiple lines are allowed.

    If MULTI\_LINE is set to `FALSE` and a new line is present within a JSON record, the record containing the new line will be interpreted as an error.

    Default: `TRUE`

`ALLOW_DUPLICATE = TRUE | FALSE`
:   Boolean that specifies to allow duplicate object field names (only the last one will be preserved).

    Default: `FALSE`

`STRIP_OUTER_ARRAY = TRUE | FALSE`
:   Boolean that instructs the JSON parser to remove outer brackets (that is, `[ ]`).

    Default: `FALSE`

`STRIP_NULL_VALUES = TRUE | FALSE`
:   Boolean that instructs the JSON parser to remove object fields or array elements containing `null` values. For example, when set to `TRUE`:

    > | Before | After |
    > | --- | --- |
    > | `[null]` | `[]` |
    > | `[null,null,3]` | `[,,3]` |
    > | `{"a":null,"b":null,"c":123}` | `{"c":123}` |
    > | `{"a":[1,null,2],"b":{"x":null,"y":88}}` | `{"a":[1,,2],"b":{"y":88}}` |

    Default: `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
    option performs a one-to-one character replacement.

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default: `FALSE`

### TYPE = AVRO[¶](#type-avro "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   String (constant) that specifies the current compression algorithm for the data files to be queried. Snowflake uses this option to
    detect how already-compressed data files were compressed so that the compressed data in the files can be extracted for querying.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. If querying Brotli-compressed files, explicitly use `BROTLI` instead of `AUTO`. |
    | `GZIP` |  |
    | `BZ2` |  |
    | `BROTLI` |  |
    | `ZSTD` |  |
    | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
    | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
    | `NONE` | Data files to query have not been compressed. |

    Default: `AUTO`.

Note

We recommend that you use the default `AUTO` option because it will determine both the file and codec compression. Specifying a compression option refers to the compression of files, not the compression of blocks (codecs).

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
    option performs a one-to-one character replacement.

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default: `FALSE`

### TYPE = ORC[¶](#type-orc "Link to this heading")

`TRIM_SPACE = TRUE | FALSE`
:   Boolean that specifies whether to remove leading and trailing white space from strings.

    For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the field (that is, the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces.

    This file format option is applied to the following actions only:

    * Querying object values in staged ORC data files.
    * Querying ORC data in separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
    * Querying ORC data in separate columns by specifying a query in the COPY statement (that is, COPY transformation).

    Default: `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
    option performs a one-to-one character replacement.

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default: `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data source with SQL NULL. To specify more than
    one string, enclose the list of strings in parentheses and use commas to separate each value.

    Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
    value, all instances of `2` as either a string or number are converted.

    For example:

    `NULL_IF = ('\N', 'NULL', 'NUL', '')`

    Note that this option can include empty strings.

    This file format option is applied when querying object values in staged ORC data files.

    Default: `\N` (that is, NULL)

### TYPE = PARQUET[¶](#type-parquet "Link to this heading")

`COMPRESSION = AUTO | SNAPPY | NONE`
:   String (constant) that specifies the current compression algorithm for columns in the Parquet files.

    | Supported Values | Notes |
    | --- | --- |
    | `AUTO` | Compression algorithm detected automatically. Supports the following compression algorithms: Brotli, gzip, Lempel-Ziv-Oberhumer (LZO), LZ4, Snappy, or Zstandard v0.8 (and higher). |
    | `SNAPPY` |  |
    | `NONE` | Data files have not been compressed. |

    Default: `AUTO`

`BINARY_AS_TEXT = TRUE | FALSE`
:   Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. When set to `FALSE`, Snowflake interprets these columns as binary data.

    Default: `TRUE`

    Note

    Snowflake recommends that you set BINARY\_AS\_TEXT to FALSE to avoid any potential conversion issues.

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
    option performs a one-to-one character replacement.

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default: `FALSE`

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE EXTERNAL TABLE | Schema |  |
| CREATE STAGE | Schema | Required if creating a new stage. |
| USAGE | Stage | Required if referencing an existing stage. |
| USAGE | File format |  |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## Usage notes[¶](#usage-notes "Link to this heading")

* External tables support external (S3, Azure, or GCS) stages only; internal (Snowflake) stages aren’t supported.

  External tables don’t support storage versioning (S3 versioning, Object Versioning in Google Cloud Storage, or versioning for Azure Storage).

  You cannot access data held in archival cloud storage classes that requires restoration before it can be retrieved. These archival storage classes include, for example, the Amazon S3 Glacier Flexible Retrieval or Glacier Deep Archive storage class, or Microsoft Azure Archive Storage.
* Snowflake doesn’t enforce integrity constraints on external tables. In particular, unlike normal tables, Snowflake doesn’t enforce
  NOT NULL constraints.
* External tables include the following metadata column:

  + METADATA$FILENAME: Name of each staged data file that is included in the external table. Includes the path to the data file in the stage.
  + METADATA$FILE\_ROW\_NUMBER: Row number for each record in the staged data file.

* The following items aren’t supported for external tables:

  + Clustering keys
  + Cloning
  + Data in XML format
  + Time Travel
* For information about using an external table with a policy, see the following topics:

  + [Masking policies and external tables](../../user-guide/security-column-intro.html#label-security-column-intro-ext-table).
  + [Row access policies and external tables](../../user-guide/security-row-intro.html#label-security-row-intro-ext-table).
* Using `OR REPLACE` is the equivalent of using [DROP EXTERNAL TABLE](drop-external-table) on the existing external table, and then creating a new
  external table with the same name.

  CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

  This means that any queries concurrent with the CREATE OR REPLACE EXTERNAL TABLE operation use either the old or new external table version.
* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).
* When you create an external table with a row access policy added to the external table, use the
  [POLICY\_CONTEXT](../functions/policy_context) function to simulate a query on the external table that is protected by a row access policy.
* [SELECT](select) `*` always returns the VALUE column, in which all regular or semi-structured data is cast to variant rows.
* The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.

## Examples[¶](#examples "Link to this heading")

### Partitions added automatically from partition column expressions[¶](#partitions-added-automatically-from-partition-column-expressions "Link to this heading")

Create an external table with partitions computed from expressions in the partition column definitions.

In step 2 of the following example, the data files are organized in cloud storage with the following structure: `logs/YYYY/MM/DD/HH24`.
For example:

* `logs/2018/08/05/0524/`
* `logs/2018/08/27/1408/`

1. Create an external stage named `s1` for the storage location where the data files are stored. For more information, see
   [CREATE STAGE](create-stage).

   The stage definition includes the path `/files/logs/`:

   **Amazon S3**

   > ```
   > CREATE STAGE s1
   >   URL='s3://mybucket/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy

   **Google Cloud Storage**

   > ```
   > CREATE STAGE s1
   >   URL='gcs://mybucket/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy

   **Microsoft Azure**

   > ```
   > CREATE STAGE s1
   >   URL='azure://mycontainer/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy
2. Query the METADATA$FILENAME pseudocolumn in the staged data, and then use the results to develop your partition columns:

   ```
   SELECT metadata$filename FROM @s1/;

   +----------------------------------------+
   | METADATA$FILENAME                      |
   |----------------------------------------|
   | files/logs/2018/08/05/0524/log.parquet |
   | files/logs/2018/08/27/1408/log.parquet |
   +----------------------------------------+
   ```

   Copy
3. Create the partitioned external table.

   The partition column `date_part` casts `YYYY/MM/DD` in the METADATA$FILENAME pseudocolumn as a date by using
   [TO\_DATE , DATE](../functions/to_date). The SQL command also specifies Parquet as the file format type.

   The external tables for Amazon S3 and Microsoft Azure cloud storage include the parameter that is required to refresh the metadata
   automatically when triggered by event notifications from the respective cloud messaging service:

   **Amazon S3**

   > ```
   > CREATE EXTERNAL TABLE et1(
   >  date_part date AS TO_DATE(SPLIT_PART(metadata$filename, '/', 3)
   >    || '/' || SPLIT_PART(metadata$filename, '/', 4)
   >    || '/' || SPLIT_PART(metadata$filename, '/', 5), 'YYYY/MM/DD'),
   >  timestamp bigint AS (value:timestamp::bigint),
   >  col2 varchar AS (value:col2::varchar))
   >  PARTITION BY (date_part)
   >  LOCATION=@s1/logs/
   >  AUTO_REFRESH = true
   >  FILE_FORMAT = (TYPE = PARQUET)
   >  AWS_SNS_TOPIC = 'arn:aws:sns:us-west-2:001234567890:s3_mybucket';
   > ```
   >
   > Copy

   **Google Cloud Storage**

   > ```
   > CREATE EXTERNAL TABLE et1(
   >   date_part date AS TO_DATE(SPLIT_PART(metadata$filename, '/', 3)
   >     || '/' || SPLIT_PART(metadata$filename, '/', 4)
   >     || '/' || SPLIT_PART(metadata$filename, '/', 5), 'YYYY/MM/DD'),
   >   timestamp bigint AS (value:timestamp::bigint),
   >   col2 varchar AS (value:col2::varchar))
   >   PARTITION BY (date_part)
   >   LOCATION=@s1/logs/
   >   AUTO_REFRESH = true
   >   FILE_FORMAT = (TYPE = PARQUET);
   > ```
   >
   > Copy

   **Microsoft Azure**

   > ```
   > CREATE EXTERNAL TABLE et1(
   >   date_part date AS TO_DATE(SPLIT_PART(metadata$filename, '/', 3)
   >     || '/' || SPLIT_PART(metadata$filename, '/', 4)
   >     || '/' || SPLIT_PART(metadata$filename, '/', 5), 'YYYY/MM/DD'),
   >   timestamp bigint AS (value:timestamp::bigint),
   >   col2 varchar AS (value:col2::varchar))
   >   PARTITION BY (date_part)
   >   INTEGRATION = 'MY_INT'
   >   LOCATION=@s1/logs/
   >   AUTO_REFRESH = true
   >   FILE_FORMAT = (TYPE = PARQUET);
   > ```
   >
   > Copy
4. Refresh the external table metadata:

   ```
   ALTER EXTERNAL TABLE et1 REFRESH;
   ```

   Copy

When you query the external table, filter the data by the partition column by using a WHERE clause. Snowflake only scans the files in the
specified partitions that match the filter conditions:

```
SELECT timestamp, col2 FROM et1 WHERE date_part = to_date('08/05/2018');
```

Copy

### Partitions added manually[¶](#partitions-added-manually "Link to this heading")

Create an external table with user-defined partitions (that is, the partitions are added manually by the external table owner).

1. Create an external stage named `s2` for the storage location where the data files are stored:

   The stage definition includes the path `/files/logs/`:

   **Amazon S3**

   > ```
   > CREATE STAGE s2
   >   URL='s3://mybucket/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy

   **Google Cloud Storage**

   > ```
   > CREATE STAGE s2
   >   URL='gcs://mybucket/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy

   **Microsoft Azure**

   > ```
   > CREATE STAGE s2
   >   URL='azure://mycontainer/files/logs/'
   >   ...
   >   ;
   > ```
   >
   > Copy
2. Create the partitioned external table. The external table includes three partition columns with different data types.

   The following rules apply:

   * The column names in the partition expressions are case-sensitive.
   * A partition column name must be in uppercase, unless the column name is enclosed in double quotes. Alternatively,
     use [GET\_IGNORE\_CASE](../functions/get_ignore_case) instead of the case-sensitive `:` character in the SQL
     expression.
   * If a column name is enclosed in double quotes (for example, “Column1”), the partition column name must also be enclosed in
     double quotes and match the column name exactly.

   The syntax for each of the three cloud storage services (Amazon S3, Google Cloud Storage, and Microsoft Azure) is identical
   because the external table metadata isn’t refreshed:

   ```
   create external table et2(
     col1 date as (parse_json(metadata$external_table_partition):COL1::date),
     col2 varchar as (parse_json(metadata$external_table_partition):COL2::varchar),
     col3 number as (parse_json(metadata$external_table_partition):COL3::number))
     partition by (col1,col2,col3)
     location=@s2/logs/
     partition_type = user_specified
     file_format = (type = parquet);
   ```

   Copy
3. Add partitions for the partition columns:

   ```
   ALTER EXTERNAL TABLE et2 ADD PARTITION(col1='2022-01-24', col2='a', col3='12') LOCATION '2022/01';
   ```

   Copy

   Snowflake adds the partitions to the metadata for the external table. The operation also adds any new data files in the specified
   location to the metadata:

   ```
   +---------------------------------------+----------------+-------------------------------+
   |                       file            |     status     |          description          |
   +---------------------------------------+----------------+-------------------------------+
   | mycontainer/files/logs/2022/01/24.csv | REGISTERED_NEW | File registered successfully. |
   | mycontainer/files/logs/2022/01/25.csv | REGISTERED_NEW | File registered successfully. |
   +---------------------------------------+----------------+-------------------------------+
   ```

   Copy

When you query the external table, filter the data by the partition columns by using a WHERE clause. This example returns the records in the
order in which they are stored in the staged data files:

```
SELECT col1, col2, col3 FROM et1 WHERE col1 = TO_DATE('2022-01-24') AND col2 = 'a' ORDER BY METADATA$FILE_ROW_NUMBER;
```

Copy

### Materialized view on an external table[¶](#materialized-view-on-an-external-table "Link to this heading")

Create a materialized view that is based on a subquery of the columns in the external table created in the
[Partitions Added Automatically From Partition Column Expressions](#partitions-added-automatically-from-partition-column-expressions) example:

```
CREATE MATERIALIZED VIEW et1_mv
  AS
  SELECT col2 FROM et1;
```

Copy

For general syntax, usage notes, and further examples for this SQL command, see [CREATE MATERIALIZED VIEW](create-materialized-view).

### External table created with detected column definitions[¶](#external-table-created-with-detected-column-definitions "Link to this heading")

Create an external table where the column definitions are derived from a set of staged files that contain Avro, Parquet, or ORC data.

Note

The `mystage` stage and `my_parquet_format` file format referenced in the statement must already exist. A set of files must
already be staged in the cloud storage location referenced in the stage definition.

The following example builds on an example in the [INFER\_SCHEMA](../functions/infer_schema) topic:

> ```
> CREATE EXTERNAL TABLE mytable
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
>     FROM TABLE(
>       INFER_SCHEMA(
>         LOCATION=>'@mystage',
>         FILE_FORMAT=>'my_parquet_format'
>       )
>     )
>   )
>   LOCATION=@mystage
>   FILE_FORMAT=my_parquet_format
>   AUTO_REFRESH=false;
> ```
>
> Copy

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 16 MB. Avoid using `*` for larger result sets, and only use the required columns, `COLUMN NAME`, `TYPE`, and `NULLABLE`, for the query, as the following example demonstrates. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`:

> ```
> CREATE EXTERNAL TABLE mytable
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME',COLUMN_NAME, 'TYPE',TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION',EXPRESSION))
>     FROM TABLE(
>       INFER_SCHEMA(
>         LOCATION=>'@mystage',
>         FILE_FORMAT=>'my_parquet_format'
>       )
>     )
>   )
>   LOCATION=@mystage
>   FILE_FORMAT=my_parquet_format
>   AUTO_REFRESH=false;
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
2. [Variant syntax](#variant-syntax)
3. [Required parameters](#required-parameters)
4. [Optional parameters](#optional-parameters)
5. [Cloud provider parameters (cloudProviderParams)](#cloud-provider-parameters-cloudproviderparams)
6. [Format type options (formatTypeOptions)](#format-type-options-formattypeoptions)
7. [Access control requirements](#access-control-requirements)
8. [Usage notes](#usage-notes)
9. [Examples](#examples)

Related content

1. [Introduction to external tables](/sql-reference/sql/../../user-guide/tables-external-intro)
2. [SYSTEM$VALIDATE\_STORAGE\_INTEGRATION](/sql-reference/sql/../functions/system_validate_storage_integration)