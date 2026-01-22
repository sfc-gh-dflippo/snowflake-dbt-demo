---
auto_generated: true
description: String & binary functions (AI Functions)
last_scraped: '2026-01-14T16:56:02.564846+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex
title: COMPLETE (SNOWFLAKE.CORTEX) | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)AI FunctionsScalar functionsCOMPLETE (SNOWFLAKE.CORTEX)

Categories:
:   [String & binary functions](../functions-string) (AI Functions)

# COMPLETE (SNOWFLAKE.CORTEX)[¶](#complete-snowflake-cortex "Link to this heading")

Note

[AI\_COMPLETE](ai_complete) is the latest version of this function.
Use AI\_COMPLETE for the latest functionality.
You can continue to use COMPLETE (SNOWFLAKE.CORTEX).

Given a prompt, generates a response (completion) using your choice of supported language model.

Note

A variant of this function allows COMPLETE to produce responses to images, including:

* Comparing images
* Captioning images
* Classifying images
* Extracting entities from images
* Answering questions using data in graphs and charts

See [COMPLETE (SNOWFLAKE.CORTEX) (multimodal)](complete-snowflake-cortex-multimodal) for more information.

## Syntax[¶](#syntax "Link to this heading")

```
SNOWFLAKE.CORTEX.COMPLETE(
    <model>, <prompt_or_history> [ , <options> ] )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`model`
:   A string specifying the model to be used. Specify one of the following values.

    * `claude-4-opus`
    * `claude-4-sonnet`
    * `claude-3-7-sonnet`
    * `claude-3-5-sonnet`
    * `deepseek-r1`
    * `llama3-8b`
    * `llama3-70b`
    * `llama3.1-8b`
    * `llama3.1-70b`
    * `llama3.1-405b`
    * `llama3.3-70b`
    * `llama4-maverick`
    * `llama4-scout`
    * `mistral-large`
    * `mistral-large2`
    * `mistral-7b`
    * `mixtral-8x7b`
    * `openai-gpt-4.1`
    * `openai-o4-mini`
    * `snowflake-arctic`
    * `snowflake-llama-3.1-405b`
    * `snowflake-llama-3.3-70b`

    Supported models might have different [costs](../../user-guide/snowflake-cortex/aisql.html#label-cortex-llm-cost-considerations).

`prompt_or_history`
:   The prompt or conversation history to be used to generate a completion.

    If `options` is not present, the prompt given must be a string.

    If `options` is present, the argument must be an [array](../data-types-semistructured.html#label-data-type-array) of objects representing a
    conversation in chronological order. Each [object](../data-types-semistructured.html#label-data-type-object) must contain a `role` key and a
    `content` key. The `content` value is a prompt or a response, depending on the role. The role must be one of the
    following.

> | `role` value | `content` value |
> | --- | --- |
> | `'system'` | An initial plain-English prompt to the language model to provide it with background information and instructions for a response style. For example, “Respond in the style of a pirate.” The model does not generate a response to a system prompt. Only one system prompt may be provided, and if it is present, it must be the first in the array. |
> | `'user'` | A prompt provided by the user. Must follow the system prompt (if there is one) or an assistant response. |
> | `'assistant'` | A response previously provided by the language model. Must follow a user prompt. Past responses can be used to provide a stateful conversational experience; see [Usage Notes](#usage-notes). |

**Optional:**

`options`
:   An [object](../data-types-semistructured.html#label-data-type-object) containing zero or more of the following options that affect the model’s
    hyperparameters. See [LLM Settings](https://www.promptingguide.ai/introduction/settings).

    * `temperature`: A value from 0 to 1 (inclusive) that controls the randomness of the output of the language model. A
      higher temperature (for example, 0.7) results in more diverse and random output, while a lower temperature (such as
      0.2) makes the output more deterministic and focused.

      Default: 0
    * `top_p`: A value from 0 to 1 (inclusive) that controls the randomness and diversity of the language model,
      generally used as an alternative to `temperature`. The difference is that `top_p` restricts the set of possible tokens
      that the model outputs, while `temperature` influences which tokens are chosen at each step.

      Default: 0
    * `max_tokens`: Sets the maximum number of output tokens in the response. Small values can result in truncated responses.

      Default: 4096
      Maximum allowed value: 8192
    * `guardrails`: Filters potentially unsafe and harmful responses from a language model using [Cortex Guard](../../user-guide/snowflake-cortex/aisql.html#label-cortex-llm-complete-cortex-guard).
      Either TRUE or FALSE.

      Default: FALSE
    * `response_format`: A [JSON schema](https://json-schema.org/) that the response should follow. This is a SQL
      sub-object, not a string. If `response_format` is not specified, the response is a string containing either the
      response or a serialized JSON object containing the response and information about it.

      For more information, see [AI\_COMPLETE structured outputs](../../user-guide/snowflake-cortex/complete-structured-outputs).

    Specifying the `options` argument, even if it is an empty object (`{}`), affects how the `prompt` argument is
    interpreted and how the response is formatted.

## Returns[¶](#returns "Link to this heading")

When the `options` argument is not specified, returns a string containing the response.

When the `options` argument is given, and this object contains the `response_format` key, returns a string
representation of a JSON object adhering to the specified JSON schema.

When the `options` argument is given, and this object *does not* contain the `response_format` key, returns a
string representation of a JSON object containing the following keys.

* `"choices"`: An array of the model’s responses. (Currently, only one response is provided.) Each response is
  an object containing a `"messages"` key whose value is the model’s response to the latest prompt.
* `"created"`: UNIX timestamp (seconds since midnight, January 1, 1970) when the response was generated.
* `"model"`: The name of the model that created the response.
* `"usage"`: An object recording the number of tokens consumed and generated by this completion. Includes
  the following sub-keys:

  + `"completion_tokens"`: The number of tokens in the generated response.
  + `"prompt_tokens"`: The number of tokens in the prompt.
  + `"total_tokens"`: The total number of tokens consumed, which is the sum of the other two values.

## Access control requirements[¶](#access-control-requirements "Link to this heading")

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](../snowflake-db-roles.html#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](../../user-guide/snowflake-cortex/aisql.html#label-cortex-llm-privileges) for more information on this privilege.

## Usage notes[¶](#usage-notes "Link to this heading")

COMPLETE does not retain any state from one call to the next. To use the COMPLETE function to provide a stateful,
conversational experience, pass all previous user prompts and model responses in the conversation as part of the `prompt_or_history`
array (see [Templates for Chat Models](https://huggingface.co/docs/transformers/en/chat_templating#templates-for-chat-models)).
Keep in mind that the number of tokens processed increases for each “round,” and costs increase proportionally.

## Examples[¶](#examples "Link to this heading")

### Single response[¶](#single-response "Link to this heading")

To generate a single response:

```
SELECT SNOWFLAKE.CORTEX.COMPLETE('snowflake-arctic', 'What are large language models?');
```

Copy

### Responses from table column[¶](#responses-from-table-column "Link to this heading")

The following example generates a response from each row of a table (in this example, `content` is a column from
the `reviews` table). The `reviews` table contains a column named `review_content` containing the text of
reviews submitted by users. The query returns a critique of each review.

```
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'openai-gpt-4.1',
        CONCAT('Critique this review in bullet points: <review>', content, '</review>')
) FROM reviews LIMIT 10;
```

Copy

Tip

As shown in this example, you can use tagging in the prompt to control the kind of response generated. See
[A guide to prompting LLaMA 2](https://replicate.com/blog/how-to-prompt-llama) for tips.

### Controlling temperature and tokens[¶](#controlling-temperature-and-tokens "Link to this heading")

This example illustrates the use of the function’s `options` argument to control the inference hyperparameters in a
single response. Note that in this form of the function, the prompt must be provided as an array, since this form
supports multiple prompts and responses.

```
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'claude-4-sonnet ',
    [
        {
            'role': 'user',
            'content': 'how does a snowflake get its unique pattern?'
        }
    ],
    {
        'temperature': 0.7,
        'max_tokens': 10
    }
);
```

Copy

The response is a JSON object containing the message from the language model and other information. Note that the response
is truncated as instructed in the `options` argument.

```
{
    "choices": [
        {
            "messages": " The unique pattern on a snowflake is"
        }
    ],
    "created": 1708536426,
    "model": "deepseek-r1",
    "usage": {
        "completion_tokens": 10,
        "prompt_tokens": 22,
        "guardrail_tokens": 0,
        "total_tokens": 32
    }
}
```

Copy

### Controlling safety[¶](#controlling-safety "Link to this heading")

This example illustrates the use of the Cortex Guard `guardrails` argument to filter unsafe and harmful responses from a language model.

```
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    [
        {
            'role': 'user',
            'content': <'Prompt that generates an unsafe response'>
        }
    ],
    {
        'guardrails': true
    }
);
```

Copy

The response is a JSON object, for example:

```
{
    "choices": [
        {
            "messages": "Response filtered by Cortex Guard"
        }
    ],
    "created": 1718882934,
    "model": "mistral-7b",
    "usage": {
        "completion_tokens": 402,
        "prompt_tokens": 93,
        "guardrails _tokens": 677,
        "total_tokens": 1172
    }
}
```

Copy

### Providing a system prompt[¶](#providing-a-system-prompt "Link to this heading")

This example illustrates the use of a system prompt to provide a sentiment analysis of movie reviews. The `prompt`
argument here is an array of objects, each having an appropriate `role` value.

```
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama3.1-70b',
    [
        {'role': 'system', 'content': 'You are a helpful AI assistant. Analyze the movie review text and determine the overall sentiment. Answer with just \"Positive\", \"Negative\", or \"Neutral\"' },
        {'role': 'user', 'content': 'this was really good'}
    ], {}
    ) as response;
```

Copy

The response is a JSON object containing the response from the language model and other information.

```
{
    "choices": [
        {
        "messages": " Positive"
        }
    ],
    "created": 1708479449,
    "model": "deepseek-r1",
    "usage": {
        "completion_tokens": 3,
        "prompt_tokens": 64,
        "total_tokens": 67
    }
}
```

Copy

## Legal notices[¶](#legal-notices "Link to this heading")

The following notice applies to Cortex COMPLETE Structured Output functionality only:

Use of models provided on the [Snowflake Model and Service Flow-Down Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/)
page are subject to the terms specified therein. The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Feature |

For the rest of COMPLETE functionality, refer to [Snowflake AI and ML](../../guides-overview-ai-features) for legal notices.

## Limitations[¶](#limitations "Link to this heading")

Snowflake Cortex functions do not support dynamic tables.

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
4. [Access control requirements](#access-control-requirements)
5. [Usage notes](#usage-notes)
6. [Examples](#examples)
7. [Legal notices](#legal-notices)
8. [Limitations](#limitations)

Related content

1. [Snowflake Cortex AI Functions (including LLM functions)](/sql-reference/functions/../../user-guide/snowflake-cortex/aisql)
2. [AI\_COMPLETE structured outputs](/sql-reference/functions/../../user-guide/snowflake-cortex/complete-structured-outputs)
3. [COMPLETE (SNOWFLAKE.CORTEX) (multimodal)](/sql-reference/functions/complete-snowflake-cortex-multimodal)