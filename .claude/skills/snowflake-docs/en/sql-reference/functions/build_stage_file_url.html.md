---
auto_generated: true
description: File functions
last_scraped: '2026-01-14T16:55:30.021520+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/build_stage_file_url.html
title: BUILD_STAGE_FILE_URL | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](ai_classify.md)
       * [AI\_COMPLETE](ai_complete.md)
       * [AI\_COUNT\_TOKENS](ai_count_tokens.md)
       * [AI\_EMBED](ai_embed.md)
       * [AI\_EXTRACT](ai_extract.md)
       * [AI\_FILTER](ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](ai_parse_document.md)
       * [AI\_REDACT](ai_redact.md)
       * [AI\_SENTIMENT](ai_sentiment.md)
       * [AI\_SIMILARITY](ai_similarity.md)
       * [AI\_TRANSCRIBE](ai_transcribe.md)
       * [AI\_TRANSLATE](ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](try_complete-snowflake-cortex.md)")
   * [Bitwise expression](../expressions-byte-bit.md)
   * [Conditional expression](../expressions-conditional.md)
   * [Context](../functions-context.md)
   * [Conversion](../functions-conversion.md)
   * [Data generation](../functions-data-generation.md)
   * [Data metric](../functions-data-metric.md)
   * [Date & time](../functions-date-time.md)
   * [Differential privacy](../functions-differential-privacy.md)
   * [Encryption](../functions-encryption.md)
   * [File](../functions-file.md)

     + Files on stages
     + [GET\_STAGE\_LOCATION](get_stage_location.md)
     + [GET\_RELATIVE\_PATH](get_relative_path.md)
     + [GET\_ABSOLUTE\_PATH](get_absolute_path.md)
     + [GET\_PRESIGNED\_URL](get_presigned_url.md)
     + [BUILD\_SCOPED\_FILE\_URL](build_scoped_file_url.md)
     + [BUILD\_STAGE\_FILE\_URL](build_stage_file_url.md)
     + AI Functions
     + [AI\_COMPLETE](ai_complete.md)
     + [AI\_PARSE\_DOCUMENT](ai_parse_document.md)
     + [AI\_TRANSCRIBE](ai_transcribe.md)
     + FILE objects
     + [FL\_GET\_CONTENT\_TYPE](fl_get_content_type.md)
     + [FL\_GET\_ETAG](fl_get_etag.md)
     + [FL\_GET\_FILE\_TYPE](fl_get_file_type.md)
     + [FL\_GET\_LAST\_MODIFIED](fl_get_last_modified.md)
     + [FL\_GET\_RELATIVE\_PATH](fl_get_relative_path.md)
     + [FL\_GET\_SCOPED\_FILE\_URL](fl_get_scoped_file_url.md)
     + [FL\_GET\_SIZE](fl_get_size.md)
     + [FL\_GET\_STAGE](fl_get_stage.md)
     + [FL\_GET\_STAGE\_FILE\_URL](fl_get_stage_file_url.md)
     + [FL\_IS\_AUDIO](fl_is_audio.md)
     + [FL\_IS\_COMPRESSED](fl_is_compressed.md)
     + [FL\_IS\_DOCUMENT](fl_is_document.md)
     + [FL\_IS\_IMAGE](fl_is_image.md)
     + [FL\_IS\_VIDEO](fl_is_video.md)
     + [TO\_FILE](to_file.md)
     + [TRY\_TO\_FILE](try_to_file.md)
   * [Geospatial](../functions-geospatial.md)
   * [Hash](../functions-hash-scalar.md)
   * [Metadata](../functions-metadata.md)
   * [ML Model Monitors](../functions-model-monitors.md)
   * [Notification](../functions-notification.md)
   * [Numeric](../functions-numeric.md)
   * [Organization users and organization user groups](../functions-organization-users.md)
   * [Regular expressions](../functions-regexp.md)
   * [Semi-structured and structured data](../functions-semistructured.md)
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[File](../functions-file.md)BUILD\_STAGE\_FILE\_URL

Categories:
:   [File functions](../functions-file)

# BUILD\_STAGE\_FILE\_URL[¶](#build-stage-file-url "Link to this heading")

Generates a Snowflake *file URL* to a staged file using the stage name and relative file path as inputs. A file URL permits
prolonged access to a specified file. That is, the file URL does not expire.

Call this SQL function in a query, user-defined function (UDF), or stored procedure.

Access files in a stage by sending the file URL in a request to the REST API for file support. When users send a file URL to the REST API
to access files, Snowflake performs the following actions:

1. Authenticate the user.
2. Verify that the role has sufficient privileges on the stage that contains the file.
3. Redirect the user to the staged file in the cloud storage service.

## Syntax[¶](#syntax "Link to this heading")

```
BUILD_STAGE_FILE_URL( @<stage_name> , '<relative_file_path>' )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

`relative_file_path`
:   Path and filename of the file relative to its location in the stage.

## Returns[¶](#returns "Link to this heading")

The function returns a file URL in the following format:

```
https://<account_identifier>/api/files/<db_name>/<schema_name>/<stage_name>/<relative_path>
```

Copy

Where:

`account_identifier`
:   Hostname of the Snowflake account for your stage. The hostname starts with an account locator (provided by Snowflake) and ends with the
    Snowflake domain (`snowflakecomputing.com`):

    `account_locator.snowflakecomputing.com`

    For more details, see [Account identifiers](../../user-guide/admin-account-identifier).

    Note

    For [Business Critical](../../user-guide/intro-editions) accounts, a `privatelink` segment is prepended to the URL just before
    `snowflakecomputing.com` (`privatelink.snowflakecomputing.com`), even if private connectivity to the Snowflake service is not
    enabled for your account.

    Important

    Currently, the function returns the account identifier in the form `organization_name-account_name`. When a file URL is used
    as input to a GET request, the API endpoint returns an error.

    To resolve the error, you must manually convert the account identifier to the applicable form for your account:

    `account_locator.region_id` or

    `account_locator.region_id.cloud`

    For more information about these forms, see [Format 2: Account locator in a region](../../user-guide/admin-account-identifier.html#label-account-locator).

    In an upcoming release, the function will return file URLs in the correct form.

`db_name`
:   Name of the database that contains the stage where your files are located.

`schema_name`
:   Name of the schema that contains the stage where your files are located.

`stage_name`
:   Name of the stage where your files are located.

`relative_path`
:   Path to the files to access using the file URL.

## Usage notes[¶](#usage-notes "Link to this heading")

* The permissions required to call this SQL function differ depending on how it is called:

  | SQL Operation | Permissions Required |
  | --- | --- |
  | Query | USAGE (external stage) or READ (internal stage) |
  | Stored procedure | The stored procedure owner (i.e. role that has the OWNERSHIP privilege on the stored procedure) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the stored procedure only requires the USAGE privilege on the stored procedure. |
  | UDF | The UDF owner (i.e. role that has the OWNERSHIP privilege on the UDF) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the UDF only requires the USAGE privilege on the UDF. |
* An HTTP client that sends a file URL to the REST API must be configured to allow redirects.
* When a file URL is accessed, the query history shows that the internal GET\_STAGE\_FILE function was called.

* If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples[¶](#examples "Link to this heading")

Retrieve a file URL for a bitmap format image file in an external stage:

```
SELECT BUILD_STAGE_FILE_URL(@images_stage,'/us/yosemite/half_dome.jpg');
```

Copy

```
https://my_account.snowflakecomputing.com/api/files/MY_DB/PUBLIC/IMAGES_STAGE/us/yosemite/half_dome.jpg
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
2. [Arguments](#arguments)
3. [Returns](#returns)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)