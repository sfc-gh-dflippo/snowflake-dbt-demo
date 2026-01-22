---
auto_generated: true
description: Creates a named file format that describes a set of staged data to access
  or load into Snowflake tables.
last_scraped: '2026-01-14T16:55:38.290292+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html
title: CREATE FILE FORMAT | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Data loading & unloading](../commands-data-loading.md)CREATE FILE FORMAT

# CREATE FILE FORMAT[¶](#create-file-format "Link to this heading")

Creates a named file format that describes a set of staged data to access or load into Snowflake tables.

This command supports the following variants:

* [CREATE OR ALTER FILE FORMAT](#label-create-or-alter-file-format-syntax): Creates a named file format if it doesn’t exist or alters an existing file format.

See also:
:   [ALTER FILE FORMAT](alter-file-format) , [DROP FILE FORMAT](drop-file-format) , [SHOW FILE FORMATS](show-file-formats) , [DESCRIBE FILE FORMAT](desc-file-format)

    [COPY INTO <location>](copy-into-location) , [COPY INTO <table>](copy-into-table) , [CREATE OR ALTER <object>](create-or-alter)

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY | VOLATILE } ] FILE FORMAT [ IF NOT EXISTS ] <name>
  [ TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM} [ formatTypeOptions ] ]
  [ COMMENT = '<string_literal>' ]
```

Copy

Where:

> ```
> formatTypeOptions ::=
> -- If TYPE = CSV
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      RECORD_DELIMITER = '<string>' | NONE
>      FIELD_DELIMITER = '<string>' | NONE
>      MULTI_LINE = TRUE | FALSE
>      FILE_EXTENSION = '<string>'
>      PARSE_HEADER = TRUE | FALSE
>      SKIP_HEADER = <integer>
>      SKIP_BLANK_LINES = TRUE | FALSE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      ESCAPE = '<character>' | NONE
>      ESCAPE_UNENCLOSED_FIELD = '<character>' | NONE
>      TRIM_SPACE = TRUE | FALSE
>      FIELD_OPTIONALLY_ENCLOSED_BY = '<character>' | NONE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      EMPTY_FIELD_AS_NULL = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
>      ENCODING = '<string>' | UTF8
> -- If TYPE = JSON
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      TRIM_SPACE = TRUE | FALSE
>      MULTI_LINE = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      FILE_EXTENSION = '<string>'
>      ENABLE_OCTAL = TRUE | FALSE
>      ALLOW_DUPLICATE = TRUE | FALSE
>      STRIP_OUTER_ARRAY = TRUE | FALSE
>      STRIP_NULL_VALUES = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> -- If TYPE = AVRO
>      COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = ORC
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = PARQUET
>      COMPRESSION = AUTO | LZO | SNAPPY | NONE
>      SNAPPY_COMPRESSION = TRUE | FALSE
>      BINARY_AS_TEXT = TRUE | FALSE
>      USE_LOGICAL_TYPE = TRUE | FALSE
>      TRIM_SPACE = TRUE | FALSE
>      USE_VECTORIZED_SCANNER = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = XML
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      PRESERVE_SPACE = TRUE | FALSE
>      STRIP_OUTER_ELEMENT = TRUE | FALSE
>      DISABLE_AUTO_CONVERT = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> ```
>
> Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

### CREATE OR ALTER FILE FORMAT[¶](#create-or-alter-file-format "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Creates a new named file format if it doesn’t already exist, or transforms an existing file format into the one defined in the statement.
A CREATE OR ALTER FILE FORMAT statement follows the syntax rules of a CREATE FILE FORMAT statement and has the same limitations as an
[ALTER FILE FORMAT](alter-file-format) statement.

Supported alterations include changes to the [formatTypeOptions](#label-create-file-format-formattypeoptions) and COMMENT properties.
You can’t alter the TYPE property.

For more information, see [CREATE OR ALTER FILE FORMAT usage notes](#label-create-or-alter-file-format-usage-notes).

```
CREATE OR ALTER [ { TEMP | TEMPORARY | VOLATILE } ] FILE FORMAT <name>
  [ TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM } [ formatTypeOptions ] ]
  [ COMMENT = '<string_literal>' ]
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   Specifies the identifier for the file format; must be unique for the schema in which the file format is created.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`), Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

## Optional parameters[¶](#optional-parameters "Link to this heading")

`{ TEMP | TEMPORARY | VOLATILE }`
:   Specifies that the file format persists only for the duration of the [session](../../user-guide/session-policies) that you created it in.
    A temporary file format is dropped at the end of the session.

    Default: No value. If a file format is not declared as `TEMPORARY`, the file format is permanent.

    If you want to avoid unexpected conflicts, avoid naming temporary file formats after file formats that already exist in the schema.

    If you created a temporary file format with the same name as another file format in the schema, all queries and operations used on the
    file format only affect the temporary file format in the session, until you drop the temporary file format. If you drop the file format
    using a DROP FILE FORMAT command, you drop the temporary file format, and not the file format that already exists in the schema.

`TYPE = CSV | JSON | AVRO | ORC | PARQUET | XML [ ... ]`
:   Specifies the format of the input files (for data loading) or output files (for data unloading). Depending on the format type, you can
    specify additional format-specific options. For more information, see [Format Type Options](#label-create-file-format-formattypeoptions)
    (in this topic).

    Valid values depend on whether the file format is for loading or unloading data:

    > `CSV` (for loading or unloading)
    > :   Any flat, delimited plain text file that uses specific characters such as the following:
    >
    >     * Separators for fields within records (for example, commas).
    >     * Separators for records (for example, new line characters).
    >
    >     Although the name (CSV) suggests comma-separated values, you can use any valid character as a field separator.
    >
    > `JSON` (for loading or unloading)
    > :   Any plain text file containing one or more JSON documents (such as objects or arrays). JSON is a semi-structured file format. The
    >     documents can be comma-separated and optionally enclosed in a big array. A single JSON document can span multiple lines.
    >
    >     Note
    >
    >     * When you load data from files into tables, Snowflake supports either [NDJSON](https://github.com/ndjson/ndjson-spec) (newline delimited JSON)
    >       standard format or comma-separated JSON format.
    >     * When you unload table data to files, Snowflake outputs *only* to NDJSON format.
    >
    > `AVRO` (for loading only; you can’t unload data to AVRO format)
    > :   Binary file in AVRO format.
    >
    > `ORC` (for loading only; you can’t unload data to ORC format)
    > :   Binary file in ORC format.
    >
    > `PARQUET` (for loading or unloading)
    > :   Binary file in PARQUET format.
    >
    > `XML` (for loading only; you can’t unload data to XML format)
    > :   Plain text file containing XML elements.
    >
    > `CUSTOM` (for loading unstructured data only)
    > :   [![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open
    >
    >     Available to all accounts.
    >
    >     This format type specifies that the underlying stage holds unstructured data and can only be used with the `FILE_PROCESSOR` copy option.

    For more information about CSV, see [Usage Notes](#usage-notes) in this topic. For more information about JSON and the other semi-structured file formats,
    see [Introduction to Loading Semi-structured Data](../../user-guide/semistructured-intro). For more information about `CUSTOM` type, see [Loading unstructured data with Document AI](../../user-guide/data-load-unstructured-data).

    Default: `CSV`

`COMMENT = 'string_literal'`
:   Specifies a comment for the file format.

    Default: No value

## Format type options (`formatTypeOptions`)[¶](#format-type-options-formattypeoptions "Link to this heading")

Depending on the file format type specified (`TYPE = ...`), you can include one or more of the following format-specific options
(separated by blank spaces, commas, or new lines):

### TYPE = CSV[¶](#type-csv "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   * When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        * When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified when loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Default:
    :   `AUTO`

`RECORD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   Data loading:
        :   New line character. Note that “new line” is logical such that `\r\n` will be understood as a new line for files on a Windows platform.

        Data unloading:
        :   New line character (`\n`).

`FIELD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

            > Note
            >
            > For non-ASCII characters, you must use the hex byte sequence value to get a deterministic behavior.

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   comma (`,`)

`MULTI_LINE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and the specified record delimiter is present within a CSV field, the record containing the field will be interpreted as an error.

    Default:
    :   `TRUE`

    Note

    If you are loading large uncompressed CSV files (greater than 128MB) that follow the RFC4180 specification, Snowflake supports parallel scanning of these CSV files when MULTI\_LINE is set to `FALSE`, COMPRESSION is set to `NONE`, and ON\_ERROR is set to `ABORT_STATEMENT` or `CONTINUE`.

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.csv[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

    Note

    If the `SINGLE` copy option is `TRUE`, then the COPY command unloads a file without a file extension by default. To specify a file extension, provide a file name and extension in the
    `internal_location` or `external_location` path (For example, `copy into @stage/data.csv`).

`PARSE_HEADER = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to use the first row headers in the data files to determine column names.

    This file format option is applied to the following actions only:

    > * Automatically detecting column definitions by using the INFER\_SCHEMA function.
    > * Loading CSV data into separate columns by using the INFER\_SCHEMA function and MATCH\_BY\_COLUMN\_NAME copy option.

    If the option is set to TRUE, the first row headers will be used to determine column names. The default value FALSE will return column names as c\*, where \* is the position of the column.

    Note

    * This option isn’t supported for external tables.
    * The SKIP\_HEADER option isn’t supported if you set `PARSE_HEADER = TRUE`.

    Default:
    :   `FALSE`

`SKIP_HEADER = integer`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Number of lines at the start of the file to skip.

    Note that SKIP\_HEADER does not use the RECORD\_DELIMITER or FIELD\_DELIMITER values to determine what a header line is; rather, it simply skips the specified number of CRLF (Carriage Return, Line Feed)-delimited lines in the file. RECORD\_DELIMITER and FIELD\_DELIMITER are then used to determine the rows of data to load.

    Default:
    :   `0`

`SKIP_BLANK_LINES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to skip any blank lines encountered in the data files; otherwise, blank lines produce an end-of-record error (default behavior).

    Default:
    :   `FALSE`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of date values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](../parameters.html#label-date-input-format) (data loading) or [DATE\_OUTPUT\_FORMAT](../parameters.html#label-date-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of time values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](../parameters.html#label-time-input-format) (data loading) or [TIME\_OUTPUT\_FORMAT](../parameters.html#label-time-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of timestamp values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](../parameters.html#label-timestamp-input-format) (data loading) or [TIMESTAMP\_OUTPUT\_FORMAT](../parameters.html#label-timestamp-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the encoding format for binary input or output. The option can be used when loading data into or unloading data from binary columns in a table.

    Default:
    :   `HEX`

`ESCAPE = 'character' | NONE`
:   Use:
    :   Data loading and unloading

    Definition:
    :   A singlebyte character string used as the escape character for enclosed or unenclosed field values. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_OPTIONALLY_ENCLOSED_BY` character in the data as literals.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for enclosed fields only. Specify the character used to enclose fields by setting `FIELD_OPTIONALLY_ENCLOSED_BY`.

        Note

        This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
        as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
        the option value.

        In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
        option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If this option is set, it overrides the escape character set for `ESCAPE_UNENCLOSED_FIELD`.

    Default:
    :   `NONE`

`ESCAPE_UNENCLOSED_FIELD = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   A singlebyte character string used as the escape character for unenclosed field values only. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_DELIMITER` or `RECORD_DELIMITER` characters in the data as literals. The escape character can also be used to escape instances of itself in the data.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for unenclosed fields only.

        Note

        * The default value is `\\`. If a row in a data file ends in the backslash (`\`) character, this character escapes the newline or
          carriage return character specified for the `RECORD_DELIMITER` file format option. As a result, the load operation treats
          this row and the next row as a single row of data. To avoid this issue, set the value to `NONE`.
        * This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
          as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
          the option value.

          In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
          option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If `ESCAPE` is set, the escape character set for that file format option overrides this option.

    Default:
    :   backslash (`\\`)

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove white space from fields.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        As another example, if leading or trailing spaces surround quotes that enclose strings, you can remove the surrounding spaces using this option and the quote character using the
        `FIELD_OPTIONALLY_ENCLOSED_BY` option. Note that any spaces within the quotes are preserved. For example, assuming `FIELD_DELIMITER = '|'` and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`:

        ```
        |"Hello world"|    /* loads as */  >Hello world<
        |" Hello world "|  /* loads as */  > Hello world <
        | "Hello world" |  /* loads as */  >Hello world<
        ```

        Copy

        (the brackets in this example are not loaded; they are used to demarcate the beginning and end of the loaded strings)

    Default:
    :   `FALSE`

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   Character used to enclose strings. Value can be `NONE`, single quote character (`'`), or double quote character (`"`). To use the single quote character, use the octal or hex representation (`0x27`) or the double single-quoted escape (`''`).

        Data unloading only:
        :   When a field in the source table contains this character, Snowflake escapes it using the same character for unloading. For example, if the value is the double quote character and a field contains the string `A "B" C`, Snowflake escapes the double quotes for unloading as follows:

            `A ""B"" C`

    Default:
    :   `NONE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   String used to convert to and from SQL NULL:

        * When loading data, Snowflake replaces these values in the data load source with SQL NULL. To specify more than one string, enclose
          the list of strings in parentheses and use commas to separate each value.

          Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as
          a value, all instances of `2` as either a string or number are converted.

          For example:

          `NULL_IF = ('\N', 'NULL', 'NUL', '')`

          Note that this option can include empty strings.
        * When unloading data, Snowflake converts SQL NULL values to the first value in the list.

    Default:
    :   `\N` (that is, NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\\`)

`ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table.

        If set to `FALSE`, an error is not generated and the load continues. If the file is successfully loaded:

        * If the input file contains records with more fields than columns in the table, the matching fields are loaded in order of occurrence in the file and the remaining fields are not loaded.
        * If the input file contains records with fewer fields than columns in the table, the non-matching columns in the table are loaded with NULL values.

        This option assumes all the records within the input file are the same length (i.e. a file containing records of varying length return an error regardless of the value specified for this parameter).

    Default:
    :   `TRUE`

    Note

    When [transforming data during loading](../../user-guide/data-load-transform) (i.e. using a query as the source for the COPY command), this option is ignored. There is no requirement for your data files to have
    the same number and ordering of columns as your target table.

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`).

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   * When loading data, specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters (For example, `,,`).

          If set to `FALSE`, Snowflake attempts to cast an empty field to the corresponding column type. An empty string is inserted into columns of type STRING. For other column types, the COPY command produces an error.
        * When unloading data, this option is used in combination with `FIELD_OPTIONALLY_ENCLOSED_BY`. When `FIELD_OPTIONALLY_ENCLOSED_BY = NONE`, setting `EMPTY_FIELD_AS_NULL = FALSE` specifies to unload empty strings in tables to empty string values without quotes enclosing the field values.

          If set to `TRUE`, `FIELD_OPTIONALLY_ENCLOSED_BY` must specify a character to enclose strings.

    Default:
    :   `TRUE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

`ENCODING = 'string'`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String (constant) that specifies the character set of the source data when loading data into a table.

        | Character Set | `ENCODING` Value | Supported Languages | Notes |
        | --- | --- | --- | --- |
        | Big5 | `BIG5` | Traditional Chinese |  |
        | EUC-JP | `EUCJP` | Japanese |  |
        | EUC-KR | `EUCKR` | Korean |  |
        | GB18030 | `GB18030` | Chinese |  |
        | IBM420 | `IBM420` | Arabic |  |
        | IBM424 | `IBM424` | Hebrew |  |
        | IBM949 | `IBM949` | Korean |  |
        | ISO-2022-CN | `ISO2022CN` | Simplified Chinese |  |
        | ISO-2022-JP | `ISO2022JP` | Japanese |  |
        | ISO-2022-KR | `ISO2022KR` | Korean |  |
        | ISO-8859-1 | `ISO88591` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | ISO-8859-2 | `ISO88592` | Czech, Hungarian, Polish, Romanian |  |
        | ISO-8859-5 | `ISO88595` | Russian |  |
        | ISO-8859-6 | `ISO88596` | Arabic |  |
        | ISO-8859-7 | `ISO88597` | Greek |  |
        | ISO-8859-8 | `ISO88598` | Hebrew |  |
        | ISO-8859-9 | `ISO88599` | Turkish |  |
        | ISO-8859-15 | `ISO885915` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish | Identical to ISO-8859-1 except for 8 characters, including the Euro currency symbol. |
        | KOI8-R | `KOI8R` | Russian |  |
        | Shift\_JIS | `SHIFTJIS` | Japanese |  |
        | UTF-8 | `UTF8` | All languages | For loading data from delimited files (CSV, TSV, etc.), UTF-8 is the default. . . For loading data from all other supported file formats (JSON, Avro, etc.), as well as unloading data, UTF-8 is the only supported character set. |
        | UTF-16 | `UTF16` | All languages |  |
        | UTF-16BE | `UTF16BE` | All languages |  |
        | UTF-16LE | `UTF16LE` | All languages |  |
        | UTF-32 | `UTF32` | All languages |  |
        | UTF-32BE | `UTF32BE` | All languages |  |
        | UTF-32LE | `UTF32LE` | All languages |  |
        | windows-874 | `WINDOWS874` | Thai |  |
        | windows-949 | `WINDOWS949` | Korean |  |
        | windows-1250 | `WINDOWS1250` | Czech, Hungarian, Polish, Romanian |  |
        | windows-1251 | `WINDOWS1251` | Russian |  |
        | windows-1252 | `WINDOWS1252` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | windows-1253 | `WINDOWS1253` | Greek |  |
        | windows-1254 | `WINDOWS1254` | Turkish |  |
        | windows-1255 | `WINDOWS1255` | Hebrew |  |
        | windows-1256 | `WINDOWS1256` | Arabic |  |

    Default:
    :   `UTF8`

    Note

    Snowflake stores all data internally in the UTF-8 character set. The data is converted into UTF-8 before it is loaded into Snowflake.

### TYPE = JSON[¶](#type-json "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   * When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        * When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Default:
    :   `AUTO`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of date string values in the data files. If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](../parameters.html#label-date-input-format) parameter is used.

        This file format option is applied to the following actions only:

        * Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        * Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of time string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](../parameters.html#label-time-input-format) parameter is used.

        This file format option is applied to the following actions only:

        * Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        * Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of timestamp string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](../parameters.html#label-timestamp-input-format) parameter is used.

        This file format option is applied to the following actions only:

        * Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        * Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the encoding format for binary string values in the data files. The option can be used when loading data into binary columns in a table.

        This file format option is applied to the following actions only:

        * Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        * Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `HEX`

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`MULTI_LINE = TRUE | FALSE`
:   Use: Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and a new line is present within a JSON record, the record containing the new line will be interpreted as an error.

    Default:
    :   `TRUE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.json[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

`ENABLE_OCTAL = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that enables parsing of octal numbers.

    Default:
    :   `FALSE`

`ALLOW_DUPLICATE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to allow duplicate object field names (only the last one will be preserved).

    Default:
    :   `FALSE`

`STRIP_OUTER_ARRAY = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove outer brackets (i.e. `[ ]`).

    Default:
    :   `FALSE`

`STRIP_NULL_VALUES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove object fields or array elements containing `null` values. For example, when set to `TRUE`:

        | Before | After |
        | --- | --- |
        | `[null]` | `[]` |
        | `[null,null,3]` | `[,,3]` |
        | `{"a":null,"b":null,"c":123}` | `{"c":123}` |
        | `{"a":[1,null,2],"b":{"x":null,"y":88}}` | `{"a":[1,,2],"b":{"y":88}}` |

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

### TYPE = AVRO[¶](#type-avro "Link to this heading")

`COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   * When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        * When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Default:
    :   `AUTO`.

Note

We recommend that you use the default `AUTO` option because it will determine both the file and codec compression. Specifying a compression option refers to the compression of files, not the compression of blocks (codecs).

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

### TYPE = ORC[¶](#type-orc "Link to this heading")

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

### TYPE = PARQUET[¶](#type-parquet "Link to this heading")

`COMPRESSION = AUTO | LZO | SNAPPY | NONE`
:   Use:
    :   Data unloading and external tables

    Definition:

    * When unloading data, specifies the compression algorith for columns in the Parquet files.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically. Supports the following compression algorithms: Brotli, gzip, Lempel-Ziv-Oberhumer (LZO), LZ4, Snappy, or Zstandard v0.8 (and higher). . When unloading data, unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `LZO` | When unloading data, files are compressed using the Snappy algorithm by default. If unloading data to LZO-compressed files, specify this value. |
        | `SNAPPY` | When unloading data, files are compressed using the Snappy algorithm by default. You can optionally specify this value. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Default:
    :   `AUTO`

`SNAPPY_COMPRESSION = TRUE | FALSE`
:   Use:
    :   Data unloading only

        | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | Unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `SNAPPY` | May be specified if unloading Snappy-compressed files. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Definition:
    :   Boolean that specifies whether unloaded file(s) are compressed using the SNAPPY algorithm.

    Note

    Deprecated. Use `COMPRESSION = SNAPPY` instead.

    Limitations:
    :   Only supported for data unloading operations.

    Default:
    :   `TRUE`

`BINARY_AS_TEXT = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. When set to `FALSE`, Snowflake interprets these columns as binary data.

    Default:
    :   `TRUE`

    Note

    Snowflake recommends that you set BINARY\_AS\_TEXT to FALSE to avoid any potential conversion issues.

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`USE_LOGICAL_TYPE = TRUE | FALSE`
:   Use:
    :   Data loading, data querying in staged files, and schema detection.

    Definition:
    :   Boolean that specifies whether to use Parquet logical types. With this file format option, Snowflake can interpret Parquet logical types during data loading. For more information, see [Parquet Logical Type Definitions](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md). To enable Parquet logical types, set USE\_LOGICAL\_TYPE as TRUE when you create a new file format option.

    Limitations:
    :   Not supported for data unloading.

`USE_VECTORIZED_SCANNER = TRUE | FALSE`
:   Use:
    :   Data loading and data querying in staged files

    Definition:
    :   Boolean that specifies whether to use a vectorized scanner for loading Parquet files.

    Default:
    :   `FALSE`. In a future BCR, the default value will be `TRUE`.

    Using the vectorized scanner can significantly reduce the latency for loading Parquet files, because this scanner is well suited for the columnar format of a [Parquet](https://parquet.apache.org/docs/file-format/) file. The scanner only downloads relevant sections of the Parquet file into memory, such as the subset of selected columns.

    If `USE_VECTORIZED_SCANNER` is set to `TRUE`, the vectorized scanner has the following behaviors:

    > * The `BINARY_AS_TEXT` option is always treated as `FALSE` and the `USE_LOGICAL_TYPE` option is always treated as `TRUE`, no matter what the actual value is being set to.
    > * The vectorized scanner supports Parquet map types. The output of scanning a map type is as follows:
    >
    >   > ```
    >   > "my_map":
    >   >   {
    >   >    "k1": "v1",
    >   >    "k2": "v2"
    >   >   }
    >   > ```
    >   >
    >   > Copy
    > * The vectorized scanner shows `NULL` values in the output, as the following example demonstrates:
    >
    >   > ```
    >   > "person":
    >   >  {
    >   >   "name": "Adam",
    >   >   "nickname": null,
    >   >   "age": 34,
    >   >   "phone_numbers":
    >   >   [
    >   >     "1234567890",
    >   >     "0987654321",
    >   >     null,
    >   >     "6781234590"
    >   >   ]
    >   >   }
    >   > ```
    >   >
    >   > Copy
    > * The vectorized scanner handles Time and Timestamp as follows:
    >
    >   > | Parquet | Snowflake vectorized scanner |
    >   > | --- | --- |
    >   > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS/NANOS) | TIME |
    >   > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_LTZ |
    >   > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_NTZ |
    >   > | INT96 | TIMESTAMP\_LTZ |

    If `USE_VECTORIZED_SCANNER` is set to `FALSE`, the scanner has the following behaviors:

    > * This option does not support Parquet maps. The output of scanning a map type is as follows:
    >
    >   > ```
    >   > "my_map":
    >   >  {
    >   >   "key_value":
    >   >   [
    >   >    {
    >   >           "key": "k1",
    >   >           "value": "v1"
    >   >       },
    >   >       {
    >   >           "key": "k2",
    >   >           "value": "v2"
    >   >       }
    >   >     ]
    >   >   }
    >   > ```
    >   >
    >   > Copy
    > * This option does not explicitly show `NULL` values in the scan output, as the following example demonstrates:
    >
    >   > ```
    >   > "person":
    >   >  {
    >   >   "name": "Adam",
    >   >   "age": 34
    >   >   "phone_numbers":
    >   >   [
    >   >    "1234567890",
    >   >    "0987654321",
    >   >    "6781234590"
    >   >   ]
    >   >  }
    >   > ```
    >   >
    >   > Copy
    > * This option handles Time and Timestamp as follows:
    >
    >   > | Parquet | When USE\_LOGICAL\_TYPE = TRUE | When USE\_LOGICAL\_TYPE = FALSE |
    >   > | --- | --- | --- |
    >   > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS) | TIME | + TIME (If ConvertedType present) + INTEGER (If ConvertedType not present) |
    >   > | TimeType(isAdjustedToUtc=True/False, unit=NANOS) | TIME | INTEGER |
    >   > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS) | TIMESTAMP\_LTZ | TIMESTAMP\_NTZ |
    >   > | TimestampType(isAdjustedToUtc=True, unit=NANOS) | TIMESTAMP\_LTZ | INTEGER |
    >   > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS) | TIMESTAMP\_NTZ | + TIMESTAMP\_LTZ (If ConvertedType present) + INTEGER (If ConvertedType not present) |
    >   > | TimestampType(isAdjustedToUtc=False, unit=NANOS) | TIMESTAMP\_NTZ | INTEGER |
    >   > | INT96 | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ |

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

### TYPE = XML[¶](#type-xml "Link to this heading")

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   * When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        * When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

    Default:
    :   `AUTO`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`PRESERVE_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content.

    Default:
    :   `FALSE`

`STRIP_OUTER_ELEMENT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents.

    Default:
    :   `FALSE`

`DISABLE_AUTO_CONVERT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip any BOM (byte order mark) present in an input file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FILE FORMAT | Schema |  |
| OWNERSHIP | File format | * A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object   that already exists in the schema. * Required to execute a [CREATE OR ALTER FILE FORMAT](#label-create-or-alter-file-format-syntax) statement for an *existing* file format.   Note that in a [managed access schema](../../user-guide/security-access-control-configure.html#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## CREATE OR ALTER FILE FORMAT usage notes[¶](#create-or-alter-file-format-usage-notes "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

* All limitations of the [ALTER FILE FORMAT](alter-file-format) command apply.
* You can’t turn a TEMP FILE FORMAT into a regular FILE FORMAT and vice versa.
* You can’t alter the TYPE property.

## Usage notes[¶](#usage-notes "Link to this heading")

Caution

Recreating a file format (using CREATE OR REPLACE FILE FORMAT) breaks the association between the file format and any external table that
references it. This is because an external table links to a file format using a hidden ID rather than the name of the file format.
Behind the scenes, the CREATE OR REPLACE syntax drops an object and recreates it with a different hidden ID.

If you must recreate a file format after it has been linked to one or more external tables, you must recreate each of the external tables
(using CREATE OR REPLACE EXTERNAL TABLE) to reestablish the association. Call the [GET\_DDL](../functions/get_ddl) function to
retrieve a DDL statement to recreate each of the external tables.

* Conflicting file format values in a SQL statement produce an error. A conflict occurs when the same option is specified multiple times
  with different values (e.g. `...TYPE = 'CSV' ... TYPE = 'JSON'...`).
* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).

* The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
* CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples[¶](#examples "Link to this heading")

Create a CSV file format named `my_csv_format` that uses all the default CSV format options:

```
CREATE OR REPLACE FILE FORMAT my_csv_format
  TYPE = CSV
  COMMENT = 'my_file_format';
```

Copy

Alter `my_csv_format` so that it defines the following rules for data files and unsets the comment:

* Fields are delimited using the pipe character (`|`).
* Files include a single header line that will be skipped.
* The strings `NULL` and `null` will be replaced with NULL values.
* Empty strings will be interpreted as NULL values.
* Files will be compressed/decompressed using GZIP compression.

```
CREATE OR ALTER FILE FORMAT my_csv_format
  TYPE = CSV
  FIELD_DELIMITER = '|'
  SKIP_HEADER = 1
  NULL_IF = ('NULL', 'null')
  EMPTY_FIELD_AS_NULL = true
  COMPRESSION = gzip;
```

Copy

Create a JSON file format named `my_json_format` that uses all the default JSON format options:

```
CREATE OR REPLACE FILE FORMAT my_json_format
  TYPE = JSON;
```

Copy

Create a PARQUET file format named `my_parquet_format` that uses PARQUET logical types, instead of physical types or the legacy converted types.

```
CREATE OR REPLACE FILE FORMAT my_parquet_format
  TYPE = PARQUET
  USE_VECTORIZED_SCANNER = TRUE
  USE_LOGICAL_TYPE = TRUE;
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
2. [Variant syntax](#variant-syntax)
3. [Required parameters](#required-parameters)
4. [Optional parameters](#optional-parameters)
5. [Format type options (formatTypeOptions)](#format-type-options-formattypeoptions)
6. [Access control requirements](#access-control-requirements)
7. [CREATE OR ALTER FILE FORMAT usage notes](#create-or-alter-file-format-usage-notes)
8. [Usage notes](#usage-notes)
9. [Examples](#examples)