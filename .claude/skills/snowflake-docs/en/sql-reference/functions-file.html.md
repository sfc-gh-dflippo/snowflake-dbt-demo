---
auto_generated: true
description: File functions enable you to access files staged in cloud storage.
last_scraped: '2026-01-14T16:55:28.411317+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions-file.html
title: File functions | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)

   * [Summary of functions](intro-summary-operators-functions.md)
   * [All functions (alphabetical)](functions-all.md)")
   * [Aggregate](functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](functions/ai_classify.md)
       * [AI\_COMPLETE](functions/ai_complete.md)
       * [AI\_COUNT\_TOKENS](functions/ai_count_tokens.md)
       * [AI\_EMBED](functions/ai_embed.md)
       * [AI\_EXTRACT](functions/ai_extract.md)
       * [AI\_FILTER](functions/ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](functions/ai_parse_document.md)
       * [AI\_REDACT](functions/ai_redact.md)
       * [AI\_SENTIMENT](functions/ai_sentiment.md)
       * [AI\_SIMILARITY](functions/ai_similarity.md)
       * [AI\_TRANSCRIBE](functions/ai_transcribe.md)
       * [AI\_TRANSLATE](functions/ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](functions/classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](functions/complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](functions/embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](functions/embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](functions/entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](functions/extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](functions/finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](functions/parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](functions/sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](functions/summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](functions/translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](functions/ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](functions/ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](functions/count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](functions/search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](functions/split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](functions/split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](functions/try_complete-snowflake-cortex.md)")
   * [Bitwise expression](expressions-byte-bit.md)
   * [Conditional expression](expressions-conditional.md)
   * [Context](functions-context.md)
   * [Conversion](functions-conversion.md)
   * [Data generation](functions-data-generation.md)
   * [Data metric](functions-data-metric.md)
   * [Date & time](functions-date-time.md)
   * [Differential privacy](functions-differential-privacy.md)
   * [Encryption](functions-encryption.md)
   * [File](functions-file.md)

     + Files on stages
     + [GET\_STAGE\_LOCATION](functions/get_stage_location.md)
     + [GET\_RELATIVE\_PATH](functions/get_relative_path.md)
     + [GET\_ABSOLUTE\_PATH](functions/get_absolute_path.md)
     + [GET\_PRESIGNED\_URL](functions/get_presigned_url.md)
     + [BUILD\_SCOPED\_FILE\_URL](functions/build_scoped_file_url.md)
     + [BUILD\_STAGE\_FILE\_URL](functions/build_stage_file_url.md)
     + AI Functions
     + [AI\_COMPLETE](functions/ai_complete.md)
     + [AI\_PARSE\_DOCUMENT](functions/ai_parse_document.md)
     + [AI\_TRANSCRIBE](functions/ai_transcribe.md)
     + FILE objects
     + [FL\_GET\_CONTENT\_TYPE](functions/fl_get_content_type.md)
     + [FL\_GET\_ETAG](functions/fl_get_etag.md)
     + [FL\_GET\_FILE\_TYPE](functions/fl_get_file_type.md)
     + [FL\_GET\_LAST\_MODIFIED](functions/fl_get_last_modified.md)
     + [FL\_GET\_RELATIVE\_PATH](functions/fl_get_relative_path.md)
     + [FL\_GET\_SCOPED\_FILE\_URL](functions/fl_get_scoped_file_url.md)
     + [FL\_GET\_SIZE](functions/fl_get_size.md)
     + [FL\_GET\_STAGE](functions/fl_get_stage.md)
     + [FL\_GET\_STAGE\_FILE\_URL](functions/fl_get_stage_file_url.md)
     + [FL\_IS\_AUDIO](functions/fl_is_audio.md)
     + [FL\_IS\_COMPRESSED](functions/fl_is_compressed.md)
     + [FL\_IS\_DOCUMENT](functions/fl_is_document.md)
     + [FL\_IS\_IMAGE](functions/fl_is_image.md)
     + [FL\_IS\_VIDEO](functions/fl_is_video.md)
     + [TO\_FILE](functions/to_file.md)
     + [TRY\_TO\_FILE](functions/try_to_file.md)
   * [Geospatial](functions-geospatial.md)
   * [Hash](functions-hash-scalar.md)
   * [Metadata](functions-metadata.md)
   * [ML Model Monitors](functions-model-monitors.md)
   * [Notification](functions-notification.md)
   * [Numeric](functions-numeric.md)
   * [Organization users and organization user groups](functions-organization-users.md)
   * [Regular expressions](functions-regexp.md)
   * [Semi-structured and structured data](functions-semistructured.md)
   * [Snowpark Container Services](functions-spcs.md)
   * [String & binary](functions-string.md)
   * [System](functions-system.md)
   * [Table](functions-table.md)
   * [Vector](functions-vector.md)
   * [Window](functions-window.md)
   * [Stored procedures](../sql-reference-stored-procedures.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[Function and stored procedure reference](../sql-reference-functions.md)File

# File functions[¶](#file-functions "Link to this heading")

File functions enable you to access files staged in cloud storage.

## List of functions[¶](#list-of-functions "Link to this heading")

| Function Name | Notes |
| --- | --- |
| **Stages** |  |
| [GET\_STAGE\_LOCATION](functions/get_stage_location) | Returns the URL for an external or internal named stage using the stage name as the input. |
| [GET\_RELATIVE\_PATH](functions/get_relative_path) | Extracts the path of a staged file relative to its location in the stage using the stage name and absolute file path in cloud storage as inputs. |
| [GET\_ABSOLUTE\_PATH](functions/get_absolute_path) | Returns the absolute path of a staged file using the stage name and path of the file relative to its location in the stage as inputs. |
| [GET\_PRESIGNED\_URL](functions/get_presigned_url) | Generates the pre-signed URL to a staged file using the stage name and relative file path as inputs. Access files in an external stage using the function. |
| [BUILD\_SCOPED\_FILE\_URL](functions/build_scoped_file_url) | Generates a scoped Snowflake file URL to a staged file using the stage name and relative file path as inputs. |
| [BUILD\_STAGE\_FILE\_URL](functions/build_stage_file_url) | Generates a Snowflake file URL to a staged file using the stage name and relative file path as inputs. |
| **AI Functions** |  |
| [AI\_COMPLETE](functions/ai_complete) | Generates a response (completion) from text or an image using a supported language model. |
| [AI\_PARSE\_DOCUMENT](functions/ai_parse_document) | Returns the extracted content from a document on a Snowflake stage as a JSON-formatted string. |
| [AI\_TRANSCRIBE](functions/ai_transcribe) | Transcribes text from an audio file with optional timestamps and speaker labels. |

The following functions are for use with the FILE data type. For more information, see [Unstructured data types](data-types-unstructured).

| Sub-category | Function |
| --- | --- |
| Constructor | [TO\_FILE](functions/to_file) |
|  | [TRY\_TO\_FILE](functions/try_to_file) |
| Accessors | [FL\_GET\_CONTENT\_TYPE](functions/fl_get_content_type) |
|  | [FL\_GET\_ETAG](functions/fl_get_etag) |
|  | [FL\_GET\_FILE\_TYPE](functions/fl_get_file_type) |
|  | [FL\_GET\_LAST\_MODIFIED](functions/fl_get_last_modified) |
|  | [FL\_GET\_RELATIVE\_PATH](functions/fl_get_relative_path) |
|  | [FL\_GET\_SCOPED\_FILE\_URL](functions/fl_get_scoped_file_url) |
|  | [FL\_GET\_SIZE](functions/fl_get_size) |
|  | [FL\_GET\_STAGE](functions/fl_get_stage) |
|  | [FL\_GET\_STAGE\_FILE\_URL](functions/fl_get_stage_file_url) |
| Utility Functions | [FL\_IS\_AUDIO](functions/fl_is_audio) |
|  | [FL\_IS\_COMPRESSED](functions/fl_is_compressed) |
|  | [FL\_IS\_DOCUMENT](functions/fl_is_document) |
|  | [FL\_IS\_IMAGE](functions/fl_is_image) |
|  | [FL\_IS\_VIDEO](functions/fl_is_video) |

## Usage notes[¶](#usage-notes "Link to this heading")

* GET\_PRESIGNED\_URL and BUILD\_SCOPED\_FILE\_URL are non-deterministic functions; the others are deterministic.

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

1. [List of functions](#list-of-functions)
2. [Usage notes](#usage-notes)