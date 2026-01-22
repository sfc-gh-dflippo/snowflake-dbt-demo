---
auto_generated: true
description: You can use the Snowflake Cortex REST API to invoke inference with the
  LLM of your choice. You can make requests using any programming language that can
  make HTTP POST requests. This functionality all
last_scraped: '2026-01-14T16:55:59.660209+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api
title: Cortex REST API | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)

    * [Cross-region inference](cross-region-inference.md)
    * [Opt out of AI features](opting-out.md)
    * [Snowflake Intelligence](snowflake-intelligence.md)
    * [Cortex AI Functions](aisql.md)
    * [Cortex Agents](cortex-agents.md)
    * [Snowflake-managed MCP server](cortex-agents-mcp.md)
    * [Cortex Analyst](cortex-analyst.md)
    * [Cortex Search](cortex-search/cortex-search-overview.md)
    * [Cortex Knowledge Extensions](cortex-knowledge-extensions/cke-overview.md)
    * [Cortex REST API](cortex-rest-api.md)

      + [OpenAI SDK Compatibility](open_ai_sdk.md)
    * [AI Observability](ai-observability.md)
    * [ML Functions](../../guides/overview-ml-functions.md)
    * [Document AI](document-ai/overview.md)
    * [Provisioned Throughput](provisioned-throughput.md)
    * [ML Development and ML Ops](../../developer-guide/snowpark-ml/overview.md)
21. [Snowflake Postgres](../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Snowflake AI & ML](../../guides/overview-ai-features.md)Cortex REST API

# Cortex REST API[¶](#cortex-rest-api "Link to this heading")

You can use the Snowflake Cortex REST API to invoke inference with the LLM of your choice.
You can make requests using any programming language that can make HTTP POST requests.
This functionality allows you to bring state-of-the-art AI functionality to your applications.
Using this API doesn’t require a warehouse.

Note

The `_snowflake` Python API module is unsupported for production use with Cortex REST APIs. It can be modified or deprecated without notice.

The Cortex REST API streams generated tokens back to you as
[server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events).

## Setting up authentication[¶](#setting-up-authentication "Link to this heading")

To authenticate to the Cortex REST API, you can use the methods described in
[Authenticating Snowflake REST APIs with Snowflake](../../developer-guide/snowflake-rest-api/authentication).

Tip

Consider creating a dedicated user for Cortex REST API requests.

## Setting up authorization[¶](#setting-up-authorization "Link to this heading")

To send a REST API request, your default role must be granted the SNOWFLAKE.CORTEX\_USER database role, which has been
granted the privileges to use the LLM functions. In most cases, users already have this privilege, because the
SNOWFLAKE.CORTEX\_USER role is granted to the PUBLIC role automatically, and all roles inherit PUBLIC.

If your Snowflake administrator prefers to opt in individual users, he or she might have revoked SNOWFLAKE.CORTEX\_USER from
PUBLIC, and must grant this role to the users who should be able to use the Cortex REST API as follows.

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE my_role;
GRANT ROLE my_role TO USER my_user;
```

Copy

Important

REST API requests use the user’s default role, so that role must have the necessary privileges. You can change
a user’s default role with [ALTER USER … SET DEFAULT\_ROLE](../../sql-reference/sql/alter-user).

```
ALTER USER my_user SET DEFAULT_ROLE=my_role
```

Copy

## Submitting requests[¶](#submitting-requests "Link to this heading")

You make a request to the Cortex REST API by sending an HTTP POST request to the API’s REST endpoint. In the request, you
must set `Authorization` header to include the token for authentication (for example, a JSON web token (JWT), OAuth token, or
[programmatic access token](../programmatic-access-tokens)). For details, see
[Authenticating Snowflake REST APIs with Snowflake](../../developer-guide/snowflake-rest-api/authentication).

The body of the request is a JSON object that specifies the model, the prompt or conversation history, and options. For
information, see the API reference sections in this topic.

You can make REST requests using the Python API. To install the Python API, use the following command:

```
pip install snowflake-ml-python
```

Copy

The Python API is included in the `snowflake-ml-python` package starting with version 1.6.1.

## Prompt caching[¶](#prompt-caching "Link to this heading")

Prompt caching allows you to reuse previously processed context (such as large documents, system instructions, or
conversation history) across multiple requests, reducing cost and latency for applications that repeatedly use the same context.
Cortex REST supports prompt caching for all OpenAI models and Anthropic models from claude-3-7-sonnet onwards.

OpenAI Prompt Caching
:   * Prompt caching is implicit for OpenAI models; you don’t need to modify your requests to opt-in.
    * Prompts with 1024 tokens or more will utilize caching, with cache hits occurring in 128-token increments.
    * Messages, images, tool use and structured outputs can be cached.
    * Cache writes: no cost.
    * Cache reads: charged at 0.25x or 0.50x the price of the original input pricing.

Anthropic Prompt Caching
:   * You can enable prompt caching for Anthropic models by providing cache points in the request.
    * Prompts with 1024 tokens or more can utilize caching.
    * A maximum of 4 cache points can be provided per request.
    * User messages, system messages, tools and images can be cached.
    * Only cache control type ephemeral is supported.
    * Cache writes: charged at 1.25x the price of the original input pricing.
    * Cache reads: charged at 0.1x the price of the original input pricing.

## Cost considerations[¶](#cost-considerations "Link to this heading")

Snowflake Cortex REST API requests incur compute costs based on the number of tokens processed. Refer to the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for each function’s cost
in dollars per million tokens. A token is the smallest unit of text processed by Snowflake Cortex LLM functions,
approximately equal to four characters of text. The equivalence of raw input or output text to tokens can vary by model.

The COMPLETE function generates new text given an input prompt. Both input and output tokens incur compute cost. If
you use COMPLETE to provide a conversational or chat user experience, all previous prompts and responses are processed
to generate each new response, with corresponding costs.

## COMPLETE function[¶](#complete-function "Link to this heading")

You can use the REST API to prompt the [AI\_COMPLETE](../../sql-reference/functions/ai_complete) function.

You call the COMPLETE function from the `/api/v2/cortex/inference:complete` endpoint. It takes the form:

```
POST https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete
```

where `account_identifier` is the [account identifier](../admin-account-identifier) you use to access Snowsight.

### Model availability[¶](#model-availability "Link to this heading")

The following tables show the different functions that are available in the Cortex LLM REST API for each region:

Cross-region and Cross-cloudNorth AmericaEuropeAsia-Pacific

| Model | Cross Cloud  (Any Region) | AWS US  (Cross-Region) | AWS EU  (Cross-Region) | AWS APJ  (Cross-Region) | Azure US  (Cross-Region) | Azure EU  (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- |
| `claude-sonnet-4-5` | ✔ | ✔ | ✔ |  |  |  |
| `claude-opus-4-5` | \* |  |  |  |  |  |
| `claude-haiku-4-5` | \* | \* |  |  |  |  |
| `claude-4-sonnet` | ✔ | ✔ | ✔ | ✔ |  |  |
| `claude-4-opus` | ✔ | ✔ |  |  |  |  |
| `claude-3-7-sonnet` | ✔ | ✔ |  |  |  |  |
| `claude-3-5-sonnet` | ✔ | ✔ |  |  |  |  |
| `openai-gpt-4.1` | ✔ |  |  |  | ✔ |  |
| `openai-gpt-5` | \* |  |  |  | \* | \* |
| `openai-gpt-5-mini` | \* |  |  |  | \* |  |
| `openai-gpt-5-nano` | \* |  |  |  | \* |  |
| `openai-gpt-5-chat` | ✔ |  |  |  |  |  |
| `openai-gpt-oss-120b` | \* |  |  |  |  |  |
| `llama4-maverick` | ✔ | ✔ |  |  |  |  |
| `llama3.1-8b` | ✔ | ✔ |  |  |  |  |
| `llama3.1-70b` | ✔ | ✔ |  |  |  |  |
| `llama3.1-405b` | ✔ | ✔ |  |  |  |  |
| `deepseek-r1` | ✔ | ✔ |  |  |  |  |
| `mistral-7b` | ✔ | ✔ |  |  |  |  |
| `mistral-large` | ✔ | ✔ |  |  |  |  |
| `mistral-large2` | ✔ | ✔ |  |  |  |  |
| `snowflake-llama-3.3-70b` | ✔ | ✔ |  |  |  |  |

| Model | AWS US West 2  (Oregon) | AWS US East 1  (N. Virginia) | Azure East US 2  (Virginia) |
| --- | --- | --- | --- |
| `claude-3-5-sonnet` | ✔ | ✔ |  |
| `llama4-maverick` | ✔ |  |  |
| `llama3.1-8b` | ✔ | ✔ | ✔ |
| `llama3.1-70b` | ✔ | ✔ | ✔ |
| `llama3.1-405b` | ✔ | ✔ | ✔ |
| `deepseek-r1` | ✔ |  |  |
| `mistral-7b` | ✔ | ✔ | ✔ |
| `mistral-large` | ✔ | ✔ | ✔ |
| `mistral-large2` | ✔ | ✔ | ✔ |
| `snowflake-llama-3.3-70b` | ✔ |  |  |

| Model | AWS Europe Central 1  (Frankfurt) | AWS Europe West 1  (Ireland) | Azure West Europe  (Netherlands) |
| --- | --- | --- | --- |
| `llama3.1-8b` | ✔ |  | ✔ |
| `llama3.1-70b` | ✔ | ✔ | ✔ |
| `mistral-7b` | ✔ |  | ✔ |
| `mistral-large` | ✔ |  | ✔ |
| `mistral-large2` | ✔ | ✔ | ✔ |

| Model | AWS AP Southeast 2  (Sydney) | AWS AP Northeast 1  (Tokyo) |
| --- | --- | --- |
| `llama3.1-8b` | ✔ | ✔ |
| `llama3.1-70b` | ✔ | ✔ |
| `mistral-7b` |  | ✔ |
| `mistral-large` |  | ✔ |
| `mistral-large2` | ✔ | ✔ |

**\*** Indicates a preview function or model. Preview features are not suitable for production workloads.

You can also use any [fine-tuned](cortex-finetuning) model in any supported region.

### API Reference[¶](#api-reference "Link to this heading")

#### POST /api/v2/cortex/inference:complete[¶](#post-api-v2-cortex-inference-complete "Link to this heading")

Completes a prompt or conversation using the specified large language model. The body of the request is a JSON object
containing the arguments.

This endpoint corresponds to the [COMPLETE](../../sql-reference/functions/complete-snowflake-cortex) SQL function.

Required headers

`Authorization: Bearer token`
:   Authorization for the request. `token` is a JSON web token (JWT), OAuth token, or
    [programmatic access token](../programmatic-access-tokens)). For details, see
    [Authenticating Snowflake REST APIs with Snowflake](../../developer-guide/snowflake-rest-api/authentication).

`Content-Type: application/json`
:   Specifies that the body of the request is in JSON format.

`Accept: application/json, text/event-stream`
:   Specifies that the response will either contain JSON (error case) or server-sent events.

##### Optional headers[¶](#optional-headers "Link to this heading")

`X-Snowflake-Authorization-Token-Type: type`
:   Defines the type of authorization token.

    If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

    Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

    * `KEYPAIR_JWT` (for key-pair authentication)
    * `OAUTH` (for OAuth)
    * `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](../programmatic-access-tokens))

##### Required JSON arguments[¶](#required-json-arguments "Link to this heading")

| Argument | Type | Description |
| --- | --- | --- |
| `model` | string | The identifier of the model to use (see [Choosing a model](aisql.html#label-cortex-llm-choosing)). For possible values, see [Model availability](#label-cortex-complete-llm-model-availability).  Alternatively, you may use the fully-qualified name of any [fine-tuned](cortex-finetuning) model in the format `database.schema.model`. |
| `messages` | array | The prompt or conversation history to be used to generate a completion. An array of objects representing a conversation in chronological order. Each object must contain either the `content` key or the `content_list` key. It may also contain a `role` key.   * `content`: A string containing a system message, a prompt from the user, or a previous response from the model. * `role`: A string indicating the role of the message, one of `'system'`, `'user'`, or `'assistant'`.   See [the COMPLETE roles table](../../sql-reference/functions/complete-snowflake-cortex.html#label-sql-functions-complete-cortex-role-content) for a more detailed description of these roles.  For prompts consisting of a single user message, `role` may be omitted; it is then assumed to be `user`. |

##### Optional JSON arguments[¶](#optional-json-arguments "Link to this heading")

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `guardrails` | object | `null` | An object that controls whether [Cortex Guard](aisql.html#label-cortex-llm-complete-cortex-guard) guardrails are used for the request. The object contains two fields:   * `enabled`: A boolean that controls whether guardrails are used for the request. If this field is not present or is not `true`, guardrails   are not used. * `response_when_unsafe`: A string that determines the response when the Cortex Guard model deems the response unsafe.   This string, not the actual completion, is returned in the output. Default: “Response filtered by Cortex Guard” |
| `max_tokens` | integer | 16384 | A value between 1 and 16,384 (inclusive) that controls the maximum number of tokens to output. Output is truncated after this number of tokens. |
| `top_p` | number | 1.0 | A value from 0 to 1 (inclusive) that controls the diversity of the language model by restricting the set of possible tokens that the model outputs. |
| `temperature` | number | 0.0 | A value from 0 to 1 (inclusive) that controls the randomness of the output of the language model by influencing which possible token is chosen at each step. |

##### Tools configuration[¶](#tools-configuration "Link to this heading")

The `tool_spec` field has an array of available tools. The following table shows the available fields:

Tool specifications[¶](#id9 "Link to this table")

| Field | Type | Description |
| --- | --- | --- |
| `tool_spec.type` | string | The type of tool. A combination of type and name is a unique identifier. |
| `tool_spec.name` | string | The name of the tool. A combination of type and name is a unique identifier. |
| `tool_spec.description` | string | A description of the tool being considered for tool use. |
| `tool_spec.input_schema` | object | The JSON schema for the tool input. |
| `tool_spec.input_schema.type` | string | The type of the input schema object. |
| `tool_spec.input_schema.properties` | object | The definitions for each input parameter. |
| `tool_spec.input_schema.required` | array | The list of required input parameters. |

The `tool_choice` field configures the tool selection behavior. It has the following fields:

Tool choice[¶](#id10 "Link to this table")

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | The manner in which the tools are selected.  Valid values:   * `"auto"`: The model decides whether or not to call the tools that you’ve provided. * `"required"`: Use one or more tools. * `"tool"`: Use the tools that you’ve specified. |
| `name` | array | The names of the tool being used. Only valid when `type` is `"tool"`. |

`tool_use` represents a model’s request to use a specific tool. It contains the tool identifier and input parameters for the execution.
It has the following fields:

Tool use[¶](#id11 "Link to this table")

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Identifies this as a tool use request. |
| `tool_use` | object | Container for tool use request details. |

Each object contains the following keys:

Tool use request keys[¶](#id12 "Link to this table")

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| `tool_use_id` | string | Unique identifier for this tool use request. | Yes |
| `name` | string | The name of the tool being used. | Yes |
| `input` | object | The name of the tool being used. | Yes |

##### Tool results[¶](#tool-results "Link to this heading")

Represents the results of a tool execution. Contains both the input parameters and output results from the tool execution.

Tool results[¶](#id13 "Link to this table")

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Identifies this as a tool result. |
| `tool_results` | string | Unique identifier for this tool use request. |

Each result can contain the following keys:

Tool results keys[¶](#id14 "Link to this table")

| Field | Type | Description | Required |
| --- | --- | --- | --- |
| `tool_use_id` | string | Unique identifier linking this result to its corresponding tool use request. | Yes |
| `name` | string | The name of the tool that was run. It must match the tool name from the `tools` array. | Yes |
| `content` | array | Array of content elements produced by the tool execution. | Yes |
| `id` | string | Optional identifier for the tool execution instance. | No |
| `status` | string | Status indicators for the tool execution. | No |
| `Results` | object | Additional result data in an arbitrary structure. `Additional properties` is set to `True`. | Yes |

##### Output[¶](#output "Link to this heading")

Tokens are sent as they are generated using server-sent events (SSEs). Each SSE event uses the `message` type
and contains a JSON object with the following structure.

| Key | Value type | Description |
| --- | --- | --- |
| `id` | string | Unique ID of the request, the same value for all events sent in response to the request. |
| `created` | number | UNIX timestamp (seconds since midnight, January 1, 1970) when the response was generated. |
| `model` | string | Identifier of the model used. |
| `choices` | array | The model’s responses. Each response is an object containing a `delta` key, whose value is an object, and whose `content` key contains the output generated by the model. If the response was blocked by Cortex Guard, the object contains a `finish_reason` key with a value of `"prohibited_content"`. Currently, this array always contains exactly one choice. |
| `'usage` | object | Token usage for this request, including:   * `prompt_tokens`: The number of tokens in the prompt. * `completion_tokens`: The number of tokens in the completion. * `guard_tokens`: The number of tokens consumed by Cortex Guard processing. This field is not present if guardrails are not enabled. * `total_tokens`: The total number of tokens in the prompt and completion. |

##### Status codes[¶](#status-codes "Link to this heading")

The Snowflake Cortex LLM REST API uses the following HTTP status codes to indicate successful completion or various error
conditions.

200 `OK`
:   Request completed successfully. The body of the response contains the output of the model.

400 `invalid options object`
:   The optional arguments have invalid values.

400 `unknown model model_name`
:   The specified model does not exist.

400 `schema validation failed`
:   Errors related to incorrect response schema structure. Correct the schema and try again.

400 `max tokens of count exceeded`
:   The request exceeded the maximum number of tokens supported by the model (see [Model restrictions](aisql.html#label-cortex-llm-model-restrictions)).

400 `all requests were throttled by remote service`
:   The request has been throttled due to a high level of usage. Try again later.

402 `budget exceeded`
:   The model consumption budget was exceeded.

403 `Not Authorized`
:   Account not enabled for REST API, or the default role for the calling user does not have the `snowflake.cortex_user` database role.

429 `too many requests`
:   The request was rejected because the usage quota has been exceeded. Please try your request later.

503 `inference timed out`
:   The request took too long.

### Basic example[¶](#basic-example "Link to this heading")

The following example uses `curl` to make a COMPLETE request. Replace `token`, `prompt`, and
`account_identifier` with the appropriate values in this command.

```
curl -X POST \
    -H "Authorization: Bearer <token>" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d '{
    "model": "mistral-large",
    "messages": [
        {
            "content": "<prompt>"
        }
    ],
    "top_p": 0,
    "temperature": 0
    }' \
https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete
```

Copy

#### Output[¶](#id1 "Link to this heading")

```
data: {
data:  "id": "65c5e2ac-529b-461e-8a8c-f80655e6bd3f",
data:  "created": 1723493954,
data:  "model": "mistral-7b",
data:  "choices": [
data:    {
data:      "delta": {
data:        "content": "Cor"
data:        }
data:      }
data:     ],
data:  "usage": {
data:    "prompt_tokens": 57,
data:    "completion_tokens": 1,
data:    "total_tokens": 58
data:  }
data: }

data: {
data:  "id": "65c5e2ac-529b-461e-8a8c-f80655e6bd3f",
data:  "created": 1723493954,
data:  "model": "mistral-7b",
data:  "choices": [
data:    {
data:      "delta": {
data:        "content": "tex"
data:        }
data:      }
data:     ],
data:  "usage": {
data:    "prompt_tokens": 57,
data:    "completion_tokens": 2,
data:    "total_tokens": 59
data:  }
data: }
```

### Tool calling with chain of thought example[¶](#tool-calling-with-chain-of-thought-example "Link to this heading")

The following example uses `curl` to make COMPLETE requests in a chain of thought process. In this case, the tool is used to get the weather information for San Francisco, CA.

#### Request[¶](#request "Link to this heading")

```
curl -X POST \
    -H "Authorization: Bearer <token>" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d '{
    "model": "claude-3-5-sonnet",
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like in San Francisco?"
      }
    ],
    "tools": [
      {
        "tool_spec": {
          "type": "generic",
          "name": "get_weather",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": [
              "location"
            ]
          }
        }
      }
    ],
    "max_tokens": 4096,
    "top_p": 1,
    "stream": true
    }' \
https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete
```

Copy

### Response[¶](#response "Link to this heading")

```
data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":"I","content_list":[{"text":"I","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":"'ll","content_list":[{"text":"'ll","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" help you","content_list":[{"text":" help you","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" check the","content_list":[{"text":" check the","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" weather in","content_list":[{"text":" weather in","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" San Francisco.","content_list":[{"text":" San Francisco.","type":"text"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content_list":[{"name":"get_weather","tool_use_id":"tooluse_Iwuh-FEeTC-Iefsxu2ueKQ"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content_list":[{"input":"{\"location\""}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content_list":[{"input":": \"San"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content_list":[{"input":" Francisco"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{"content_list":[{"input":", CA\"}"}]}}],"usage":{}}

data: {"id":"78fe5630-95b1-4960-ac2b-7eb85536b08e","model":"claude-3-5-sonnet","choices":[{"delta":{}}],"usage":{"prompt_tokens":390,"completion_tokens":53,"total_tokens":443}}
```

The user executes the `get_weather` tool on their end and provides the results to the model.

#### Follow-up Request[¶](#follow-up-request "Link to this heading")

```
curl -X POST \
    -H "Authorization: Bearer <token>" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d '{
    "model": "claude-3-5-sonnet",
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like in San Francisco?"
      },
      {
        "role": "assistant",
        "content": "I'll help you check the weather in San Francisco.",
        "content_list": [
          {
            "type": "tool_use",
            "tool_use": {
              "tool_use_id": "tooluse_Iwuh-FEeTC-Iefsxu2ueKQ",
              "name": "get_weather",
              "input": {
                "location": "San Francisco, CA"
              }
            }
          }
        ]
      },
      {
        "role": "user",
        "content_list": [
          {
            "type": "tool_results",
            "tool_results": {
              "tool_use_id": "tooluse_Iwuh-FEeTC-Iefsxu2ueKQ",
              "name": "get_weather",
              "content": [
                {
                  "type": "text",
                  "text": "\"temperature\": \"69 fahrenheit\""
                }
              ]
            }
          }
        ]
      }
    ],
    "tools": [
      {
        "tool_spec": {
          "type": "generic",
          "name": "get_weather",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": [
              "location"
            ]
          }
        }
      }
    ],
    "max_tokens": 4096,
    "top_p": 1,
    "stream": true
    }' \
https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete
```

Copy

#### Final Response[¶](#final-response "Link to this heading")

```
data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{"content":"\n\nBase","content_list":[{"type":"text","text":"\n\nBase"}]}}],"usage":{}}

data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{"content":"d on the weather data,","content_list":[{"type":"text","text":"d on the weather data,"}]}}],"usage":{}}

data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" it's currently 69 ","content_list":[{"type":"text","text":" it's currently 69 "}]}}],"usage":{}}

data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{"content":"degrees Fahrenheit in San Francisco,","content_list":[{"type":"text","text":"degrees Fahrenheit in San Francisco,"}]}}],"usage":{}}

data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{"content":" CA.","content_list":[{"type":"text","text":" CA."}]}}],"usage":{}}

data: {"id":"07ffa851-4c47-4cea-9b7e-017a4cddc21d","model":"claude-3-5-sonnet","choices":[{"delta":{}}],"usage":{"prompt_tokens":466,"completion_tokens":26,"total_tokens":492}}
```

### Structured output example[¶](#structured-output-example "Link to this heading")

This example demonstrates the use of `curl` to retrieve a structured response that adheres to a specified JSON schema.

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  --header 'Authorization: Bearer <token>' \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "model": "mistral-large2",
    "messages": [{ "content": "Please prepare me a data set consisting of 3 people and their ages" }],
    "max_tokens": 1000,
    "response_format": {
      "type": "json",
      "schema": {
        "type": "object",
        "properties": {
          "people": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "age": {
                  "type": "number"
                }
              },
              "required": ["name", "age"]
            }
          }
        },
        "required": ["people"]
      }
    }
  }'
```

Copy

### Image input example[¶](#image-input-example "Link to this heading")

Image inputs must be specified in the request as base64 encoded strings. A maximum of 5 images are supported per request. The request body must be less than 10MB.

Image inputs are supported for the following models:

* `claude-3-7-sonnet`
* `claude-4-sonnet`
* `openai-gpt-4.1`
* `openai-gpt-5`
* `openai-gpt-5-chat`
* `openai-gpt-5-mini`
* `openai-gpt-5-nano`

The following example uses `curl` to make a COMPLETE request with an image input.

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  --header 'Authorization: Bearer <token>' \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "model": "claude-4-sonnet",
    "messages": [
      {
        "role": "user",
        "content_list": [
          {
            "type": "image",
            "details": {
              "type": "base64",
              "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
              "content_type": "image/png"
            }
          },
          {
            "type": "image",
            "details": {
              "type": "base64",
              "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
              "content_type": "image/png"
            }
          },
          {
            "type": "text",
            "text": "What are these two images?"
          }
        ]
      }
    ]
  }'
```

Copy

### Prompt caching example[¶](#prompt-caching-example "Link to this heading")

This example uses curl to make a COMPLETE request for an Anthropic model with prompt caching enabled for user messages, system messages and tools.

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
  "model": "claude-4-sonnet",
  "messages": [
      {
          "role": "system",
          "content_list": [
              {
                  "type": "text",
                  "text": "<long system message>",
                  "cache_control": {
                      "type": "ephemeral"
                  }
              }
          ]
      },
      {
          "role": "user",
          "content_list": [
              {
                  "type": "text",
                  "text": "<large text input>",
                  "cache_control": {
                      "type": "ephemeral"
                  }
              }
          ]
      }
  ],
  "tools": [
      {
          "tool_spec": {
              "type": "generic",
              "name": "my_custom_tool",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "input_param": {
                          "type": "string",
                          "description": "<large tool spec>"
                      }
                  },
                  "required": [
                      "input_param"
                  ]
              }
          },
          "cache_control": {
              "type": "ephemeral"
          }
      }
  ],
  "max_tokens": 4096,
  "top_p": 1,
  "stream": true
}'
```

Copy

### Thinking and reasoning examples[¶](#thinking-and-reasoning-examples "Link to this heading")

Cortex REST supports reasoning for OpenAI reasoning models. Reasoning effort can be set to `minimal`, `low`,
`medium`, and `high`. Reasoning summaries are not supported for OpenAI models.

This example uses curl to make a COMPLETE request for an OpenAI model with reasoning effort set to low:

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
    "model": "openai-gpt-5",
    "messages": [
      {
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      }
    ],
    "openai": {
      "reasoning": {
        "effort": "low"
      }
    }
  }'
```

Copy

Similarly, Cortex REST supports thinking for Anthropic thinking models. This example uses curl to make a COMPLETE request for an Anthropic model with thinking budget tokens set to 4000:

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
    "model": "claude-haiku-4-5",
    "messages": [
      {
        "role": "user",
        "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      }
    ],
    "temperature": 1,
    "anthropic": {
      "thinking": {
        "budget_tokens": 4000
      }
    }
  }'
```

Copy

For Anthropic thinking models, Cortex REST returns a thinking block with summarized thinking and thinking signatures. These thinking blocks can be passed back in multi-turn conversations:

```
curl --location --request POST 'https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:complete' \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
    "model": "claude-haiku-4-5",
    "messages": [
      {
        "role": "user",
        "content": "Are there an infinite number of primes?"
      },
      {
        "content_list": [{"type": "anthropic", "anthropic": {"thinking": {"thinking": "<thinking>", "signature": "<signature>"}}}],
        "role": "assistant"
      },
      {
        "role": "user",
        "content": "Can you explain your reasoning more?"
      }
    ]
  }'
```

Copy

### Python API example request[¶](#python-api-example-request "Link to this heading")

You can use the Python API to make REST requests to the COMPLETE function. Before you get started with using the API, create a session.
For information about creating a session, see [Creating a Session for Snowpark Python](../../developer-guide/snowpark/python/creating-session).

The following Python API example prompts the `mistral-7b` model with a single message and prints the response.

```
from snowflake.snowpark import Session
from snowflake.cortex import Complete

session = Session.builder.configs(...).create()

stream = Complete(
  "mistral-7b",
  "What are unique features of the Snowflake SQL dialect?",
  session=session,
  stream=True)

for update in stream:
  print(update)
```

Copy

Note

The streaming mode of the Python API currently doesn’t work in stored procedures and in Snowsight.

### Rate Limits[¶](#rate-limits "Link to this heading")

To ensure high performance standards for all Snowflake customers, Snowflake
Cortex LLM REST API requests are subject to rate limits. Requests exceeding the
limits may receive an HTTP response code of 429. Snowflake may occasionally adjust these limits.

The default limits in the following tables are applied per account and are
applied independently for each model. Ensure your application handles the 429
response code gracefully by retrying the request with
[exponential backoff](https://platform.openai.com/docs/guides/rate-limits#retrying-with-exponential-backoff).

If you need to increase the limits,
contact Snowflake Support. Your inquiry helps us anticipate future demand
and adjust the infrastructure scale accordingly.

Cortex REST API rate limits[¶](#id15 "Link to this table")

| Model | Tokens Processed  per Minute (TPM) | Requests per  Minute (RPM) | Max output (tokens) |
| --- | --- | --- | --- |
| `claude-3-5-sonnet` | 300,000 | 300 | 16,384 |
| `claude-3-7-sonnet` | 300,000 | 300 | 16,384 |
| `claude-sonnet-4-5` | 600,000 | 600 | 16,384 |
| `claude-haiku-4-5` | 600,000 | 600 | 16,384 |
| `claude-4-sonnet` | 300,000 | 300 | 16,384 |
| `claude-4-opus` | 75,000 | 75 | 16,384 |
| `deepseek-r1` | 100,000 | 100 | 16,384 |
| `llama3.1-8b` | 400,000 | 400 | 16,384 |
| `llama3.1-70b` | 200,000 | 200 | 16,384 |
| `llama3.1-405b` | 100,000 | 100 | 16,384 |
| `mistral-7b` | 400,000 | 400 | 16,384 |
| `mistral-large2` | 200,000 | 200 | 16,384 |
| `openai-gpt-4.1` | 300,000 | 300 | 16,384 |
| `openai-gpt-5` | 300,000 | 300 | 16,384 |
| `openai-gpt-5-chat` | 300,000 | 300 | 16,384 |
| `openai-gpt-5-mini` | 1,000,000 | 1,00 | 16,384 |
| `openai-gpt-5-nano` | 5,000,000 | 5,000 | 16,384 |

#### Increase rate limits with cross-region inference[¶](#increase-rate-limits-with-cross-region-inference "Link to this heading")

If you set up [cross-region inference](cross-region-inference) in your Snowflake Account,
the rate limits for Cortex LLM REST API are higher for the following models:

Cortex REST API rate limits with cross-region inference[¶](#id16 "Link to this table")

| Model | Tokens Processed  per Minute (TPM) | Requests per  Minute (RPM) | Max output (tokens) |
| --- | --- | --- | --- |
| `claude-3-7-sonnet` | 600,000 | 600 | 16,384 |
| `claude-haiku-4-5` | 600,000 | 600 | 16,384 |
| `claude-sonnet-4-5` | 600,000 | 600 | 16,384 |
| `claude-4-sonnet` | 1,200,000 | 1,200 | 16,384 |
| `claude-4-opus` | 150,000 | 150 | 16,384 |
| `llama3.1-8b` | 800,000 | 400 | 16,384 |
| `llama3.1-70b` | 400,000 | 200 | 16,384 |
| `llama3.1-405b` | 200,000 | 100 | 16,384 |

#### Troubleshooting rate limit events[¶](#troubleshooting-rate-limit-events "Link to this heading")

Offending either the TPM or RPM limits will result in a 429 response code. If
your REST API usage is below the request per minute rate limit but still
received a 429 response code, double check the token usage rate.

Cortex REST API implements rate limits using the
[Sliding Window Counter](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/#sliding-windows-to-the-rescue)
pattern. The counters are stored in a highly-available Redis cluster only
accessible by Snowflake Cortex within Snowflake’s private network.

The sliding-window counter assumes that client traffic to the API in the previous time window is
uniformly distributed. When traffic is spiky, this assumption could overestimate the rate of
requests, but recovers quickly given the window is short. Please contact
Snowflake Support if you are subject to the overestimation and want to increase
the limits.

## EMBED function[¶](#embed-function "Link to this heading")

You can make requests to the `/api/v2/cortex/inference:embed` endpoint to create embeddings for your text. The request takes the following form:

```
POST https://<account_identifier>.snowflakecomputing.com/api/v2/cortex/inference:embed
```

where `account_identifier` is the [account identifier](../admin-account-identifier) you use to access Snowsight.

### Model availability[¶](#id2 "Link to this heading")

The following table shows the EMBED function models that you can prompt using the REST API.

EMBED function models[¶](#id17 "Link to this table")

| Model | AWS US West 2  (Oregon) | AWS US East 1  (N. Virginia) | AWS Europe Central 1  (Frankfurt) | AWS Europe West 1  (Ireland) | AWS AP Southeast 2  (Sydney) | AWS AP Northeast 1  (Tokyo) | Azure East US 2  (Virginia) | Azure West Europe  (Netherlands) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `snowflake-arctic-embed-m-v1.5` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-m` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `e5-base-v2` | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |
| `snowflake-arctic-embed-l-v2.0` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

The following table shows the number of dimensions that each model can return.

EMBED function models[¶](#id18 "Link to this table")

| Model | Number of  dimensions |
| --- | --- |
| `snowflake-arctic-embed-m-v1.5` | 768 |
| `snowflake-arctic-embed-m` | 768 |
| `e5-base-v2` | 768 |
| `snowflake-arctic-embed-l-v2.0` | 1024 |

### API Reference[¶](#id3 "Link to this heading")

#### POST /api/v2/cortex/inference:embed[¶](#post-api-v2-cortex-inference-embed "Link to this heading")

Creates an embedding for text that you specify.

Required headers

`Authorization: Bearer token`.
:   Authorization for the request. `token` is a JSON web token (JWT), OAuth token, or
    [programmatic access token](../programmatic-access-tokens)). For details, see
    [Authenticating Snowflake REST APIs with Snowflake](../../developer-guide/snowflake-rest-api/authentication).

`Content-Type: application/json`
:   Specifies that the body of the request is in JSON format.

`Accept: application/json`
:   Specifies that the response contains JSON.

##### Optional headers[¶](#id4 "Link to this heading")

`X-Snowflake-Authorization-Token-Type: type`
:   Defines the type of authorization token.

    If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

    Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

    * `KEYPAIR_JWT` (for key-pair authentication)
    * `OAUTH` (for OAuth)
    * `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](../programmatic-access-tokens))

##### Required JSON arguments[¶](#id5 "Link to this heading")

| Argument | Type | Description |
| --- | --- | --- |
| `text` | array | A list of text strings for which you’re generating embeddings. The list can contain up to 1280 strings, each of which can be up to 4096 characters long. |
| `model` | string | The model that you’re using to create the embeddings. |

##### Status codes[¶](#id6 "Link to this heading")

The Snowflake Cortex LLM REST API uses the following HTTP status codes to indicate successful completion or various error
conditions.

200 `OK`
:   Request completed successfully. The body of the response contains the output of the model.

400 `invalid options object`
:   The optional arguments have invalid values.

400 `unknown model model_name`
:   The specified model does not exist.

400 `schema validation failed`
:   Errors related to incorrect response schema structure. Correct the schema and try again.

400 `max tokens of count exceeded`
:   The request exceeded the maximum number of tokens supported by the model (see [Model restrictions](aisql.html#label-cortex-llm-model-restrictions)).

400 `all requests were throttled by remote service`
:   The request has been throttled due to a high level of usage. Try again later.

402 `budget exceeded`
:   The model consumption budget was exceeded.

403 `Not Authorized`
:   Account not enabled for REST API, or the default role for the calling user does not have the `snowflake.cortex_user` database role.

429 `too many requests`
:   The request was rejected because the usage quota has been exceeded. Please try your request later.

503 `embed timed out`
:   The request took too long.

### CURL request example[¶](#curl-request-example "Link to this heading")

The following example uses `curl` to make an EMBED request to the `e5-base-v2` model.
Replace `token` and `account_identifier` with the appropriate values in this command.

```
curl --location "<account_url>/api/v2/cortex/inference:embed" \
--header 'X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer <token>" \
--data '{
"text": ["foo", "bar"],
"model": "e5-base-v2"
}'
```

Copy

#### Output[¶](#id7 "Link to this heading")

The following is the output of the request:

```
{
  "object" : "list",
  "data" : [ {
    "object" : "embedding",
    "embedding" : [ [ -0.02102863, 0.0051381723, -0.0071509206, -0.032512695, 0.056507032, -0.0048937695, 0.04964661, 0.023239689, 0.012616035, 6.152943E-4, -0.02553793, 0.04697104, -0.07258329, 0.017351158, -0.039407425, 0.021243019, 0.035988644, -0.015490267, 0.05665567, -0.053865768, -0.04021352, -0.039481744, 0.008032414, -0.022284945, 0.014539813, 0.056415558, -0.009439873, 0.0452445, -0.070742406, -0.04087098, 0.018997658, 0.028213495, 0.030248754, -0.06257851, -0.078929186, 0.06901587, -0.01433257, -0.012313747, -0.0479315, -0.033473153, -0.0036935527, 0.00631302, 0.014592694, 0.009840421, -0.05247081, -0.025823781, -0.07126838, 0.062384125, -0.043775223, -0.06945036, -0.076539464, 0.050744276, 0.06811258, -0.010631514, -0.040602278, -9.8618606E-5, -0.023782805, -0.033667535, -0.0234455, -0.022579372, 0.024588903, 0.029179674, 0.034513652, -0.008181056, 0.014506939, 0.039761875, -0.015241577, 0.038847152, -0.03438216, -0.01464129, -0.03883572, 0.0032029606, -0.056404125, -0.04456989, -0.01811581, -0.03901295, 0.016362112, 0.060897704, 0.014445482, 0.045175895, 3.5731378E-4, -0.040259257, 0.0684899, 0.020189658, 0.018345919, -0.03804677, -0.0285508, 0.025762323, -0.03626306, 0.07249182, -0.018425958, -0.06349323, 0.018077219, 0.038018186, 0.062292654, -0.049417924, 0.024297336, -0.021676084, 0.024983378, 0.0071148323, -0.070502296, -0.04697104, -0.012957627, -0.005341126, -0.05370569, -0.022244927, 0.024060082, 0.042385988, -0.0156189, 0.033987686, -0.024211582, 0.008102447, 0.0043735206, 0.024837594, -0.03626878, 0.03845268, 0.030763287, -0.048011538, -0.01775921, 0.009250762, -0.0022539354, 0.062029675, 0.049315017, 0.08743611, 0.014078163, 0.019217765, -0.0033973393, 0.031495064, -0.039476026, -0.027496008, 0.041316908, 0.066477515, 0.023971466, -0.035908606, -0.022893809, -0.04403249, -0.03938455, -0.008456187, 0.006146154, 0.019652259, 0.0046407916, 0.007190225, 0.021315912, -0.021576036, 0.054014407, -0.03280998, -0.018031484, -0.030105831, -0.051750466, 0.007942371, 0.008939991, 0.033776157, 0.016630813, -0.026647031, -0.04227165, 0.0511216, 0.025389288, -0.00816319, -0.050767142, 0.008878533, 0.030734701, 0.03327878, 0.009108642, 0.0484689, -0.027779002, -0.04547318, 0.012650337, -0.011424036, -0.012454529, 0.043872416, -0.023902861, -0.06754088, 0.039395988, -0.009394137, -0.013557914, 0.054060146, 0.03977331, 0.01960938, 0.020804238, -0.016243484, -0.08142752, 0.05857659, 0.029253993, 0.030408831, -0.048834786, -0.042614672, 0.008380437, -0.033324514, 0.04100247, 0.01713391, -0.034262102, -0.062281217, 0.05965139, -0.044295475, 0.045255937, -0.03626306, 1.14161754E-4, 0.0087263165, 0.03139216, 0.05053846, 0.020355452, 0.01695954, 0.028790914, -0.07459568, -0.06803255, 0.0015907609, 0.041185413, -0.034239236, -0.0143690165, -0.0136236595, -0.01011341, -0.0054477844, 0.012941548, -0.037143484, 0.047319777, -0.044947214, 0.020506952, -0.039258778, -0.012000026, -0.021536015, 0.049909588, -0.0355713, -0.025071993, 0.041339774, 0.009808978, 0.045072988, 0.065974414, -0.02064702, 0.0044607054, -0.013032663, 1.0004786E-4, 0.04048222, -0.01808767, -0.027704682, -0.039378837, 0.037846677, -0.01080231, -0.00804099, 0.049658038, -0.04925785, -0.009008595, 0.03676616, -0.010243069, 0.043746643, -0.04403249, -0.033193022, 0.028302109, -0.035994362, -0.026950035, -0.03394195, -0.011519082, -0.028808065, 0.037440766, -0.019132009, 0.03737788, -0.045736164, 0.0033159165, 0.030523172, 0.074252665, 0.0112153655, 0.021767555, 0.02050052, 0.02876233, -0.052882437, 0.0010833754, -0.017059589, -0.021901906, -0.04230023, 0.061881028, 0.03359893, -0.002392573, 0.047531307, 0.015124377, 0.021558885, 0.04292339, -0.045421727, 0.038801417, -0.004391386, -0.019043395, -0.03198673, -0.009232273, 0.03895006, -0.06231552, -0.03994482, 0.027779002, -0.035965774, 0.0336218, -0.016790174, -0.024385951, -0.052013453, 0.006636746, 0.028728027, -0.07149705, -0.005236791, 0.02509629, -0.08283962, 0.024062939, 0.038264018, 0.0052610883, 0.019983845, -0.022567939, 0.036028665, 0.012551718, 0.039733294, 0.020849973, -0.06289866, -0.014504082, -0.014029568, -0.012900457, 0.046056315, -0.045210198, -0.029385487, 0.01857603, -0.015710996, 0.03486239, -0.03192384, -0.04491863, -0.026112491, -0.026069613, -0.03267277, -0.009650331, 0.01740261, 0.058107797, -0.015014325, 0.033264484, -0.007932008, -0.058942482, 0.016094483, -0.039453156, -0.049863853, -0.00993904, 0.0336904, 0.008465835, 0.054460336, -0.044101093, -0.011365437, -0.037966736, -0.04518733, -0.024280185, -0.012904745, 0.018640345, -0.011682732, 0.027887626, -0.0029442657, 0.06867285, -0.017228242, 0.009504546, -0.050618496, -0.012899027, -0.03216396, -0.028968142, 0.019423576, 0.011018128, -0.017585555, -0.02778472, -0.013630806, -0.007985963, 0.044478416, -0.01570537, -0.016562209, 0.04075092, -0.031900976, -0.014078163, -1.6436433E-4, 0.02021967, 0.018799707, -0.063424625, -0.024686094, 0.04659372, -0.055466533, -0.03190669, -0.021633206, -0.037772354, -0.019120127, -0.0011362578, -0.019701209, 0.03355891, 0.046868134, -0.03438216, -0.0099447565, -0.030340228, -0.13531044, -0.019526483, -0.012966203, -0.0062001087, 0.0069561847, 0.023239689, 0.025612252, 0.010147711, 0.002053125, 0.022387853, 0.04639362, 0.017559828, -0.017425478, -0.0066185235, -0.013880925, -0.04315207, -0.032404073, 0.05231074, -0.03317587, -0.012551718, 0.053808596, 0.05265376, 0.051396016, 0.02508057, -0.013882355, 0.018711807, -0.04357513, 0.07334937, -0.045518916, -0.016896654, -0.030197302, 0.073337935, -0.020974318, -0.032169674, 0.023462651, 0.07043369, -0.010009431, 0.0576047, -0.056061104, 0.031569388, -0.04271758, 0.023205386, -0.037778072, 0.006159375, 0.003181455, 0.008509785, 0.04234597, -0.040882416, 0.048520353, -0.053156856, -0.03995054, -0.0877677, 0.04227165, -0.012376278, -0.044489853, 0.00877777, -0.04128832, -0.027247319, -0.0066703334, 0.039230194, 0.034873825, 0.03382761, 0.044352643, -0.039698992, -0.03430784, -0.020772079, -0.065414146, 5.7384593E-4, 0.02876233, 0.0067003476, 0.04351796, 0.038366925, 0.03943029, -0.033650383, 0.037966736, -0.013735142, 0.05691866, 0.008862811, -0.037635144, 0.032421224, -0.013979544, -0.068787195, -0.018368786, -0.003927593, 0.009075055, -0.016353536, -0.029505543, 0.029848564, -0.035376925, -0.079306506, 0.0051510357, 0.013992407, 0.035622753, 0.006298013, 0.015807562, -0.033753287, 0.008042865, 0.0218333, -0.011912841, -0.055649478, 0.025718017, -0.02185617, -0.004469727, -0.02198766, -0.00784143, 0.034096308, 0.054448903, 0.0307004, -0.043952454, -0.017951444, 0.011615557, 0.054620415, -0.08550376, -0.050755706, -0.051350277, -0.03050602, 0.0114068845, 0.028590819, 0.008987871, 0.0056341235, 0.037475068, -0.030620363, -0.06979338, 0.007883101, 0.08535511, -0.023171084, 5.5740948E-5, -0.006744655, -0.005266805, -0.043815248, 0.015816137, -0.014817088, -0.042991996, 0.011708458, -0.05513495, -0.041299757, 0.027315922, -0.026052462, -0.04580477, -5.0309784E-4, 0.034336425, -0.027081525, -0.045021538, 0.047497004, 0.014702748, 0.07772861, -0.046182092, -0.014136762, -0.033930518, -0.00347309, -0.026355464, -0.00622655, 0.02927686, 0.0011187494, -0.018168692, 0.007931652, -0.0931417, 0.038972925, 0.030648947, 0.008319695, 0.060280263, 0.039481744, 0.033821892, -0.0066338875, 0.017376885, -0.040550824, 0.030917646, 0.047291193, 0.028756613, -0.038189698, -0.026195388, -0.016216328, 0.031740896, 0.0019152018, 0.008411166, -0.006047893, 0.0357714, -0.052184965, -0.014689884, -0.025695506, -0.02149028, 0.031763766, -0.028939558, -0.048228785, 0.013207746, -0.0398019, -0.009475961, -0.006676051, 0.021484561, -0.04663945, 0.020061024, 0.034530804, 0.071062565, -0.034010556, -0.02533283, 0.040785223, 0.03561132, 0.06579147, -0.05904539, 0.050698537, 0.049515113, 0.032724224, 0.026675617, -0.02870516, 0.0027112968, 0.044924345, -0.0581421, -0.039441727, 0.024989096, -0.0015623322, 0.029877149, 0.017241104, -0.051761903, 0.032735657, -4.761206E-4, -0.061755255, 0.01047787, -0.008168193, 0.022033395, 0.048960563, 0.0068146884, 0.023825683, 0.027441697, 0.02250791, 0.0694618, -0.049360756, 0.018354494, -0.028810926, 0.022639401, 0.04161991, -0.027533172, -0.03584, 0.015911898, -0.0063902, 0.0015421662, 0.0028013398, -0.0025083427, 0.017544108, -0.00964104, 0.042991996, 0.0678496, -0.039121572, -0.003293004, 0.054814793, -0.08136463, -0.011446547, 0.052779533, 0.030974817, -0.017465496, 0.0770197, 0.07642513, 0.020272555, -0.0023437997, -0.045541782, 0.036131572, -0.031752333, 0.04711968, 0.046730928, -0.011505503, 0.05251655, 0.01463843, -0.050721403, 0.017111043, 0.034107745, -0.0012934759, 0.0030232319, 0.030631796, 0.018627483, 0.08971148, 0.0218333, 0.013626519, 0.04323211, 0.010196507, 0.03526258, -0.014882834, 0.055500835, 0.03626306, 0.040905282, -0.012287307, 0.0082071405, -0.045850504, 0.023251122, -0.025523636, 0.014443338, 0.029116785, -0.013965787, 0.045844786, -0.049452227, -0.013456437, 0.05682718, 0.03505105, -0.004778, -0.025840933, 0.031880964, -0.051853374, 0.026344031, -6.017164E-4, 0.032189686, 0.039687555, -0.04258037, 0.047708537, -0.011151048, 0.034559388, 0.04538171, 0.015927618, -0.018894752, 0.055763815, -0.009576724, -0.04827452, 0.0014342575, -0.02035831, 0.018483127, -0.0011405456, 0.012522598, -0.0073949657, -0.037869543, -0.007829459, 0.020000996, 0.012756102, -0.013497885, -0.032758527, -0.0027970523, -0.016222045, 0.057993453, 0.006591903, 0.024383092, 0.033821892, 0.012242999, 0.02444598, 0.0030414548, 0.0018951923, 0.0031079152, 0.047862895, -0.07421836, 0.013179162, -0.052527986, 0.037355013, 0.03133213, -0.05690722, -0.067872465, 0.04806871, -0.04677666, -0.0230253, 0.008216788, 0.014526949, 0.033473153, -0.03350174, -0.031940993, -0.02492335, -0.023599861, 0.024911916, -0.022173464, 0.012191546, 0.03524543, 0.018300183, -0.047611345, 0.02682426, -0.037314992, 0.05846225, -0.022204908, 0.026318304, 0.0506528, -0.054883394, -0.013443573, 0.01051503, -0.014944291, -0.030025791, 0.024949076, 0.024880473, 0.022919536, 0.022096286, -0.003314264, -0.012304458, -0.05195628, -0.043163504, -0.06919882, 0.035371203, 0.052527986, -0.026944317, 0.035431232, 0.0025269228, 0.05272236, -0.005325762, -0.042363122, -0.0021331632, 0.010384968, 0.03630308 ] ],
    "index" : 0
  }, {
    "object" : "embedding",
    "embedding" : [ [ -0.03859099, -0.0025452692, 0.002827513, -0.023107057, 0.039019972, 5.159378E-4, 0.061831377, 0.03898519, -0.029060632, -0.022223009, -0.053750288, 0.043431528, -0.032805532, 0.023965022, -0.017704204, 0.011997003, 0.06898495, -0.021785328, 0.061373413, -0.06912407, -0.030892503, -0.030509897, 0.012025989, 0.016202766, 0.014523069, 0.023318652, -0.006604294, 0.02823745, -0.036880862, -0.03611565, 0.028460637, 0.028643245, 0.02898527, -0.04272429, -0.040660538, 0.030086711, -0.026191091, 0.012575259, -0.013680323, -0.01576219, -0.008541235, -0.021260696, 0.022008335, -0.003821708, -0.027663542, -0.03583449, -0.049043078, 0.02032737, -0.032077998, -0.0076017496, -0.041060533, 0.06408064, 0.04306052, -0.0013231777, -0.017536089, -0.029414253, -0.01623755, 7.7897916E-4, -0.008882537, -0.017736087, 0.026489638, 0.029350484, 0.04315907, -0.052324213, 0.031188153, 0.031260613, 0.008039789, 0.016778849, -0.013186849, 0.00850138, -0.013420633, -0.021936053, -0.043321386, -0.037240274, -0.007959356, -0.011695557, 0.018266518, 0.05426043, 0.02898527, -0.007870588, 0.005872416, -0.06765162, 0.011165126, 0.008720218, 0.02233605, -0.016701313, -0.03399592, -0.023336042, -0.044266306, 0.030689605, -0.03860838, -0.037344623, 0.034544647, 0.0287302, 0.041698214, -0.010895563, 0.0614024, -0.026791086, 0.04524601, 0.02768528, -0.054040138, -0.09088621, 1.3043372E-5, 0.023196913, -0.0216491, -0.027727311, 0.032509882, 0.024405599, -0.038202588, 0.017408554, -0.022408513, 0.022341846, -0.032341763, -0.0062035727, -0.04095039, 0.044011235, 0.048289463, -0.066109605, -0.026083846, -0.036417093, -0.006709909, 0.02206069, 0.027402675, 0.094144166, -0.007571315, 0.025495443, 0.0059477775, 0.030927286, -0.036080867, -0.020770846, 0.03634753, 0.027260648, 0.046666283, -0.014643359, 0.015353498, 0.014970892, -0.05443434, -0.012696274, -0.038857654, -0.014524519, -0.032654807, 0.003442001, 9.652095E-4, -0.0034563122, 0.025579503, -0.030290695, -0.005026691, -0.056857508, -0.024376612, -0.0010362234, 0.033646103, 0.06132124, 0.02885194, -0.01999114, -0.06839365, 0.03032439, 0.018050577, -0.0336519, -0.059222706, 0.0040927203, 0.0472228, 0.015218716, 0.014365191, 0.030280912, -0.0028231654, -0.018637529, 0.058353145, -0.020962149, 0.010339318, 0.076034166, -0.0139390165, -0.05917633, 0.022141848, -0.0033655523, -0.053286523, 0.049269162, 0.06115892, 0.0397446, -0.0021697287, -0.012431783, -0.08870652, 0.061819788, 0.02314184, 0.06744293, -0.041495316, -0.057182144, 0.06261978, -0.040509813, 0.024567915, 0.033280887, -0.01153179, -0.023972267, 0.018179562, -0.0034753338, 0.01546654, -0.025831673, -0.01932738, 0.02969541, 0.023617199, 0.019331727, -0.012065844, 0.02757079, 0.035448987, -0.04044025, -0.08306019, -0.005518796, 0.05088654, -0.041101113, -0.021089682, -0.015539004, -0.034370735, -0.027449053, 0.002491284, -0.05257928, 0.038289543, -0.022892568, 0.021760693, -0.04287501, 0.026283845, -0.013069458, 0.06844002, -0.029049039, -0.020631716, 0.026727319, -0.01527234, 0.038799684, 0.018989699, 0.0049050325, -0.005134741, -0.02601718, -0.0076673287, -0.0045050355, -0.01148007, -0.057866193, -0.052973483, 0.0210549, -0.0025536022, -0.025865007, 0.060382117, -0.0221404, -0.033425815, 0.02703746, -0.0149868345, 0.056057513, -0.026463551, -0.042590957, 0.042492405, -0.031338874, 0.010684695, -0.047825698, -0.0040680827, -0.029382369, 0.06259659, -0.050956108, 0.05108364, -0.037663464, 0.022369383, 0.07088638, 0.05288073, -0.008336164, 0.0109408535, 0.011480703, 0.053031452, -0.0383765, -0.022051994, -0.028486725, -0.027593978, -0.058086485, 0.036382314, 0.015199876, 0.005368797, 0.056718376, -0.009811333, 0.04100836, 0.03998808, -0.03548667, 0.041588064, 0.0067296554, -0.020220125, -0.026582392, -0.023315752, 0.02373604, -0.025530227, -0.030446127, 0.04246342, -0.035350434, 0.022324456, -0.020628817, -0.042967767, -0.058712564, -0.0029949031, 0.07806313, -0.024985302, -0.009120216, 0.023721546, -0.067454524, 0.011266574, 0.035350434, 0.014469448, 0.009962237, -0.02918817, 0.057889383, 0.041669227, 0.017017253, 0.02020853, -0.053118408, 0.0048550325, 0.011872185, -0.012254973, 0.026041092, -0.041906904, -0.04678223, 0.046376433, -0.039466344, -0.008434714, -0.0109317945, -0.05437637, -0.04884598, -0.031159166, -0.043008346, 0.013536846, 0.032677993, 0.061727032, -0.006807916, 0.012089757, -0.013465107, -0.02766934, 0.0055115493, -0.06427774, -0.065019764, -0.035234496, 0.04675904, -0.0059869075, 0.03499102, -0.03684608, -0.0098390505, -0.063593686, -0.015811466, -0.03543739, 0.004982568, 0.0049014096, 0.02172446, 0.035251886, -0.009378145, 0.04173879, -0.015215819, 0.033408422, -0.042903997, -0.00862493, 0.006968059, -0.007472403, 0.06191254, 0.022696918, -0.029228747, -0.028422957, -0.023040393, -0.008308628, 0.07406316, 0.027379489, -0.008115876, 0.019040424, -0.009273837, -0.0069673345, -0.011002809, 0.01806652, 0.020486789, -0.06972697, -0.021471564, 0.04533876, -0.022266487, -0.030283812, -0.028692521, -0.044075, -0.026515726, -0.029128022, -0.04504311, 0.030921487, 0.08469496, -0.032782342, 0.014194087, -0.03396494, -0.13650903, -0.012214213, 0.04805758, -0.032347564, -0.02746934, 0.023527345, 0.036214195, -0.0055876356, 0.013779597, -0.016514357, 0.03534464, 0.01294917, -0.02432444, -0.015641902, 0.02491284, -0.050051767, -0.02287083, 0.017144788, -0.0336519, -0.037460566, 0.03495044, 0.023257783, 0.08004572, -0.042851824, -0.051292334, 0.050434373, -0.032643214, 0.049344525, -0.08431236, -0.047083672, -0.04599383, 0.06449803, -0.015399874, -0.06425455, 0.019791143, 0.05728649, -0.021874098, 0.054561872, -0.035588115, 0.04233009, -0.04360544, 0.018565066, -0.04087503, 0.0026898333, -5.5760413E-4, 0.02457661, 0.03532145, -0.019567955, 0.0367997, -0.024602698, -0.04020837, -0.046573535, -0.016017986, 0.003593449, -0.054086514, 0.025596894, -0.02776789, 0.0042062155, -0.016185375, 0.04382573, 0.014463651, 0.027291082, 0.03497363, -0.0062620863, -0.027478037, -0.011715847, -0.032759152, 0.005775315, 7.014435E-4, -0.020028822, -0.003293089, 0.03933881, 0.0539242, -0.019943316, 0.053402465, -0.028764984, 0.06067197, -0.020599833, -0.03490986, 0.014773793, 0.0183013, -0.020828815, -0.053727098, 0.059976324, -1.688392E-4, -0.03583739, -0.014573794, -0.018708544, -0.053286523, -0.053101014, 0.024312844, -0.010033252, 0.008641234, -0.002898799, -0.013137574, -0.044243116, 0.061228488, -0.0069245812, -0.015627408, -0.05443434, 0.0077484874, -0.03904316, 0.014356405, -0.033373643, -0.04498514, 0.051048856, 0.022487497, 0.03756491, -0.058619812, -0.030730184, 0.045303978, 0.039918512, -0.04083445, -0.06504295, -0.04686339, -0.043141678, 0.016592618, 0.0048832935, -0.004784019, 0.026109932, 0.053205363, 0.002107229, -0.050318427, -0.015707843, 0.07165159, -0.018866513, 0.021356348, 0.010883245, 0.0028449043, -0.04928076, 0.016862182, -1.4420172E-4, -0.03745477, 0.06972697, -0.013194095, -0.04233009, 0.043477908, -0.0049738726, -0.062376305, 0.014419448, 0.034248997, -0.028266437, -0.023153435, 0.03197655, 0.048301052, 0.04439384, -0.02898527, 0.010327452, -0.012039938, -0.04720541, -0.02123461, -0.02084041, 0.05700823, 0.040741697, -0.040190976, 0.01771145, -0.077077635, 0.033524364, 0.026527321, -0.015602772, 0.034979425, 0.013237573, 0.022220109, -0.025722979, -0.010891216, -0.037779402, 0.0486083, 0.032834515, 0.02749253, -0.042422842, -0.04227212, -0.020172298, 0.020483892, 0.035020005, -0.012249175, -0.018825933, 0.010697014, -0.06284007, -0.014791184, -0.02623167, -0.043477908, 0.021579536, -0.028451942, -0.020930264, 0.043738775, -0.054144483, 0.012956416, 1.356873E-4, 0.03852722, -0.06169225, 0.0020688237, 0.0143165495, 0.0395533, -0.01948245, -0.023360679, 0.053286523, 0.038990986, 0.032243215, 0.0017579567, 0.03821418, 0.052811164, 0.05951256, 0.014761474, -0.008394134, -0.04570977, 0.050411183, -0.04535615, 0.013478151, 0.065645844, -0.02176504, 0.03219684, 0.044764854, -0.04004025, 0.055987947, 5.661186E-4, -0.0403417, 0.026411379, 0.026312828, 0.017658552, 0.033106975, 0.02964034, 0.015648967, 0.02072012, 0.04390689, 0.059912555, -0.038098242, 0.054364774, -0.057414025, 1.2608593E-4, 0.039582286, -0.014165102, -0.026573697, -0.0014348616, 0.012311494, -0.006537628, -0.012820186, 0.010105714, 0.0053970576, -0.05604592, 0.01999114, 0.04630687, -0.026991084, -0.022107065, 0.085657276, -0.062040072, -0.029628742, 0.046527155, 0.039825764, -0.0245998, 0.033246104, 0.0759646, 0.016838994, 0.032301188, -0.011652441, 0.023553431, 0.0022333153, 0.061796594, 0.049703944, 0.029820045, 0.047808304, 0.018956367, -0.06025458, 0.0025391097, 0.051918417, -0.025646167, 0.0145622, 0.021872284, 0.007741966, 0.059651688, -0.035182323, 0.0367997, 0.039541706, 0.03366929, 0.06706032, -0.015962189, 0.0242027, 0.04764599, 0.04159966, -0.020562151, -0.021808518, -0.025863556, 0.023112493, -0.0050463355, -2.4492553E-4, 0.06832408, -0.069054514, 0.038011286, -0.035750434, 0.0045985132, 0.05482854, 0.043385155, -0.059373427, -0.053448837, 0.032167852, -0.04661411, -0.004763729, 0.0086589875, -0.022428801, 0.011929749, -0.033895377, 0.025895441, 0.0035796808, 0.028991068, 0.05118799, -0.003233307, 0.018024852, 0.053541593, 0.052219864, -0.025014289, -0.029611353, -0.030991051, -0.0037087786, -0.02127229, 0.0513677, -0.0010724551, -0.037866358, -0.013722714, -0.031808436, 0.006594874, 0.0064303824, -0.010605711, -0.025965005, -0.03821418, 0.01824188, 0.013044821, 0.030330187, 0.023999805, -0.010734695, 0.032359157, -0.04652136, -0.048277866, 0.02615341, 0.053402465, -0.0649386, 0.005019524, -0.042225745, 0.054306805, 0.025060665, -0.066782065, -0.09074709, 0.043796744, -0.017163629, -0.010674007, 0.017776666, 0.034324355, 0.06856756, -0.023283869, -0.027999772, -0.018759267, -0.0061187907, 0.02621428, -0.04045764, 0.030486709, 0.009367315, -0.019452015, -0.0253853, 0.010181077, -0.0024782408, 0.013219367, -0.029773671, 0.03768665, 0.0539242, -0.01145353, -0.040811263, 0.085657276, -0.019811433, -0.033280887, 0.0067633507, 0.045785137, 0.04927496, 0.034306966, -0.009710065, 0.001575893, -0.04988945, -0.022904161, -0.048915546, 0.010472379, 0.07029508, -0.050747413, -0.005718794, 0.0033557697, 0.07256752, 0.0028471234, -0.050306838, -0.015710741, 0.010923099, -0.006999943 ] ],
    "index" : 1
  } ],
  "model" : "e5-base-v2",
  "usage" : {
    "total_tokens" : 6
  }
}
```

Each embedding has an index that corresponds to the text string in a list in the request. The index is 0-based, so the first text string in the list has an index of 0, the second text string has an index of 1, and so on.

In the preceding example, “foo” corresponds to the 0 index and “bar” corresponds to the 1 index. The embedding for “foo” is the first element in the list of embeddings, and the embedding for “bar” is the second element in the list of embeddings.

### Python request example[¶](#python-request-example "Link to this heading")

The following example uses the Python API to make an EMBED request to the `e5-base-v2` model.
Replace `token` and `account_identifier` with the appropriate values in this command.

```
from snowflake.core import Root
from snowflake.snowpark.context import get_active_session

def embed_service():
    # Initialize Snowflake session and root
    session = get_active_session()
    root = Root(session)

    # Send embed_request request and process response
    response = root.cortex_embed_service.embed("e5-base-v2", ['foo', 'bar'])
    print(response)

if __name__ == "__main__":
    embed_service()
```

Copy

#### Output[¶](#id8 "Link to this heading")

The following is the output of the request:

```
{
  "object" : "list",
  "data" : [ {
    "object" : "embedding",
    "embedding" : [ [ -0.02102863, 0.0051381723, -0.0071509206, -0.032512695, 0.056507032, -0.0048937695, 0.04964661, 0.023239689, 0.012616035, 6.152943E-4, -0.02553793, 0.04697104, -0.07258329, 0.017351158, -0.039407425, 0.021243019, 0.035988644, -0.015490267, 0.05665567, -0.053865768, -0.04021352, -0.039481744, 0.008032414, -0.022284945, 0.014539813, 0.056415558, -0.009439873, 0.0452445, -0.070742406, -0.04087098, 0.018997658, 0.028213495, 0.030248754, -0.06257851, -0.078929186, 0.06901587, -0.01433257, -0.012313747, -0.0479315, -0.033473153, -0.0036935527, 0.00631302, 0.014592694, 0.009840421, -0.05247081, -0.025823781, -0.07126838, 0.062384125, -0.043775223, -0.06945036, -0.076539464, 0.050744276, 0.06811258, -0.010631514, -0.040602278, -9.8618606E-5, -0.023782805, -0.033667535, -0.0234455, -0.022579372, 0.024588903, 0.029179674, 0.034513652, -0.008181056, 0.014506939, 0.039761875, -0.015241577, 0.038847152, -0.03438216, -0.01464129, -0.03883572, 0.0032029606, -0.056404125, -0.04456989, -0.01811581, -0.03901295, 0.016362112, 0.060897704, 0.014445482, 0.045175895, 3.5731378E-4, -0.040259257, 0.0684899, 0.020189658, 0.018345919, -0.03804677, -0.0285508, 0.025762323, -0.03626306, 0.07249182, -0.018425958, -0.06349323, 0.018077219, 0.038018186, 0.062292654, -0.049417924, 0.024297336, -0.021676084, 0.024983378, 0.0071148323, -0.070502296, -0.04697104, -0.012957627, -0.005341126, -0.05370569, -0.022244927, 0.024060082, 0.042385988, -0.0156189, 0.033987686, -0.024211582, 0.008102447, 0.0043735206, 0.024837594, -0.03626878, 0.03845268, 0.030763287, -0.048011538, -0.01775921, 0.009250762, -0.0022539354, 0.062029675, 0.049315017, 0.08743611, 0.014078163, 0.019217765, -0.0033973393, 0.031495064, -0.039476026, -0.027496008, 0.041316908, 0.066477515, 0.023971466, -0.035908606, -0.022893809, -0.04403249, -0.03938455, -0.008456187, 0.006146154, 0.019652259, 0.0046407916, 0.007190225, 0.021315912, -0.021576036, 0.054014407, -0.03280998, -0.018031484, -0.030105831, -0.051750466, 0.007942371, 0.008939991, 0.033776157, 0.016630813, -0.026647031, -0.04227165, 0.0511216, 0.025389288, -0.00816319, -0.050767142, 0.008878533, 0.030734701, 0.03327878, 0.009108642, 0.0484689, -0.027779002, -0.04547318, 0.012650337, -0.011424036, -0.012454529, 0.043872416, -0.023902861, -0.06754088, 0.039395988, -0.009394137, -0.013557914, 0.054060146, 0.03977331, 0.01960938, 0.020804238, -0.016243484, -0.08142752, 0.05857659, 0.029253993, 0.030408831, -0.048834786, -0.042614672, 0.008380437, -0.033324514, 0.04100247, 0.01713391, -0.034262102, -0.062281217, 0.05965139, -0.044295475, 0.045255937, -0.03626306, 1.14161754E-4, 0.0087263165, 0.03139216, 0.05053846, 0.020355452, 0.01695954, 0.028790914, -0.07459568, -0.06803255, 0.0015907609, 0.041185413, -0.034239236, -0.0143690165, -0.0136236595, -0.01011341, -0.0054477844, 0.012941548, -0.037143484, 0.047319777, -0.044947214, 0.020506952, -0.039258778, -0.012000026, -0.021536015, 0.049909588, -0.0355713, -0.025071993, 0.041339774, 0.009808978, 0.045072988, 0.065974414, -0.02064702, 0.0044607054, -0.013032663, 1.0004786E-4, 0.04048222, -0.01808767, -0.027704682, -0.039378837, 0.037846677, -0.01080231, -0.00804099, 0.049658038, -0.04925785, -0.009008595, 0.03676616, -0.010243069, 0.043746643, -0.04403249, -0.033193022, 0.028302109, -0.035994362, -0.026950035, -0.03394195, -0.011519082, -0.028808065, 0.037440766, -0.019132009, 0.03737788, -0.045736164, 0.0033159165, 0.030523172, 0.074252665, 0.0112153655, 0.021767555, 0.02050052, 0.02876233, -0.052882437, 0.0010833754, -0.017059589, -0.021901906, -0.04230023, 0.061881028, 0.03359893, -0.002392573, 0.047531307, 0.015124377, 0.021558885, 0.04292339, -0.045421727, 0.038801417, -0.004391386, -0.019043395, -0.03198673, -0.009232273, 0.03895006, -0.06231552, -0.03994482, 0.027779002, -0.035965774, 0.0336218, -0.016790174, -0.024385951, -0.052013453, 0.006636746, 0.028728027, -0.07149705, -0.005236791, 0.02509629, -0.08283962, 0.024062939, 0.038264018, 0.0052610883, 0.019983845, -0.022567939, 0.036028665, 0.012551718, 0.039733294, 0.020849973, -0.06289866, -0.014504082, -0.014029568, -0.012900457, 0.046056315, -0.045210198, -0.029385487, 0.01857603, -0.015710996, 0.03486239, -0.03192384, -0.04491863, -0.026112491, -0.026069613, -0.03267277, -0.009650331, 0.01740261, 0.058107797, -0.015014325, 0.033264484, -0.007932008, -0.058942482, 0.016094483, -0.039453156, -0.049863853, -0.00993904, 0.0336904, 0.008465835, 0.054460336, -0.044101093, -0.011365437, -0.037966736, -0.04518733, -0.024280185, -0.012904745, 0.018640345, -0.011682732, 0.027887626, -0.0029442657, 0.06867285, -0.017228242, 0.009504546, -0.050618496, -0.012899027, -0.03216396, -0.028968142, 0.019423576, 0.011018128, -0.017585555, -0.02778472, -0.013630806, -0.007985963, 0.044478416, -0.01570537, -0.016562209, 0.04075092, -0.031900976, -0.014078163, -1.6436433E-4, 0.02021967, 0.018799707, -0.063424625, -0.024686094, 0.04659372, -0.055466533, -0.03190669, -0.021633206, -0.037772354, -0.019120127, -0.0011362578, -0.019701209, 0.03355891, 0.046868134, -0.03438216, -0.0099447565, -0.030340228, -0.13531044, -0.019526483, -0.012966203, -0.0062001087, 0.0069561847, 0.023239689, 0.025612252, 0.010147711, 0.002053125, 0.022387853, 0.04639362, 0.017559828, -0.017425478, -0.0066185235, -0.013880925, -0.04315207, -0.032404073, 0.05231074, -0.03317587, -0.012551718, 0.053808596, 0.05265376, 0.051396016, 0.02508057, -0.013882355, 0.018711807, -0.04357513, 0.07334937, -0.045518916, -0.016896654, -0.030197302, 0.073337935, -0.020974318, -0.032169674, 0.023462651, 0.07043369, -0.010009431, 0.0576047, -0.056061104, 0.031569388, -0.04271758, 0.023205386, -0.037778072, 0.006159375, 0.003181455, 0.008509785, 0.04234597, -0.040882416, 0.048520353, -0.053156856, -0.03995054, -0.0877677, 0.04227165, -0.012376278, -0.044489853, 0.00877777, -0.04128832, -0.027247319, -0.0066703334, 0.039230194, 0.034873825, 0.03382761, 0.044352643, -0.039698992, -0.03430784, -0.020772079, -0.065414146, 5.7384593E-4, 0.02876233, 0.0067003476, 0.04351796, 0.038366925, 0.03943029, -0.033650383, 0.037966736, -0.013735142, 0.05691866, 0.008862811, -0.037635144, 0.032421224, -0.013979544, -0.068787195, -0.018368786, -0.003927593, 0.009075055, -0.016353536, -0.029505543, 0.029848564, -0.035376925, -0.079306506, 0.0051510357, 0.013992407, 0.035622753, 0.006298013, 0.015807562, -0.033753287, 0.008042865, 0.0218333, -0.011912841, -0.055649478, 0.025718017, -0.02185617, -0.004469727, -0.02198766, -0.00784143, 0.034096308, 0.054448903, 0.0307004, -0.043952454, -0.017951444, 0.011615557, 0.054620415, -0.08550376, -0.050755706, -0.051350277, -0.03050602, 0.0114068845, 0.028590819, 0.008987871, 0.0056341235, 0.037475068, -0.030620363, -0.06979338, 0.007883101, 0.08535511, -0.023171084, 5.5740948E-5, -0.006744655, -0.005266805, -0.043815248, 0.015816137, -0.014817088, -0.042991996, 0.011708458, -0.05513495, -0.041299757, 0.027315922, -0.026052462, -0.04580477, -5.0309784E-4, 0.034336425, -0.027081525, -0.045021538, 0.047497004, 0.014702748, 0.07772861, -0.046182092, -0.014136762, -0.033930518, -0.00347309, -0.026355464, -0.00622655, 0.02927686, 0.0011187494, -0.018168692, 0.007931652, -0.0931417, 0.038972925, 0.030648947, 0.008319695, 0.060280263, 0.039481744, 0.033821892, -0.0066338875, 0.017376885, -0.040550824, 0.030917646, 0.047291193, 0.028756613, -0.038189698, -0.026195388, -0.016216328, 0.031740896, 0.0019152018, 0.008411166, -0.006047893, 0.0357714, -0.052184965, -0.014689884, -0.025695506, -0.02149028, 0.031763766, -0.028939558, -0.048228785, 0.013207746, -0.0398019, -0.009475961, -0.006676051, 0.021484561, -0.04663945, 0.020061024, 0.034530804, 0.071062565, -0.034010556, -0.02533283, 0.040785223, 0.03561132, 0.06579147, -0.05904539, 0.050698537, 0.049515113, 0.032724224, 0.026675617, -0.02870516, 0.0027112968, 0.044924345, -0.0581421, -0.039441727, 0.024989096, -0.0015623322, 0.029877149, 0.017241104, -0.051761903, 0.032735657, -4.761206E-4, -0.061755255, 0.01047787, -0.008168193, 0.022033395, 0.048960563, 0.0068146884, 0.023825683, 0.027441697, 0.02250791, 0.0694618, -0.049360756, 0.018354494, -0.028810926, 0.022639401, 0.04161991, -0.027533172, -0.03584, 0.015911898, -0.0063902, 0.0015421662, 0.0028013398, -0.0025083427, 0.017544108, -0.00964104, 0.042991996, 0.0678496, -0.039121572, -0.003293004, 0.054814793, -0.08136463, -0.011446547, 0.052779533, 0.030974817, -0.017465496, 0.0770197, 0.07642513, 0.020272555, -0.0023437997, -0.045541782, 0.036131572, -0.031752333, 0.04711968, 0.046730928, -0.011505503, 0.05251655, 0.01463843, -0.050721403, 0.017111043, 0.034107745, -0.0012934759, 0.0030232319, 0.030631796, 0.018627483, 0.08971148, 0.0218333, 0.013626519, 0.04323211, 0.010196507, 0.03526258, -0.014882834, 0.055500835, 0.03626306, 0.040905282, -0.012287307, 0.0082071405, -0.045850504, 0.023251122, -0.025523636, 0.014443338, 0.029116785, -0.013965787, 0.045844786, -0.049452227, -0.013456437, 0.05682718, 0.03505105, -0.004778, -0.025840933, 0.031880964, -0.051853374, 0.026344031, -6.017164E-4, 0.032189686, 0.039687555, -0.04258037, 0.047708537, -0.011151048, 0.034559388, 0.04538171, 0.015927618, -0.018894752, 0.055763815, -0.009576724, -0.04827452, 0.0014342575, -0.02035831, 0.018483127, -0.0011405456, 0.012522598, -0.0073949657, -0.037869543, -0.007829459, 0.020000996, 0.012756102, -0.013497885, -0.032758527, -0.0027970523, -0.016222045, 0.057993453, 0.006591903, 0.024383092, 0.033821892, 0.012242999, 0.02444598, 0.0030414548, 0.0018951923, 0.0031079152, 0.047862895, -0.07421836, 0.013179162, -0.052527986, 0.037355013, 0.03133213, -0.05690722, -0.067872465, 0.04806871, -0.04677666, -0.0230253, 0.008216788, 0.014526949, 0.033473153, -0.03350174, -0.031940993, -0.02492335, -0.023599861, 0.024911916, -0.022173464, 0.012191546, 0.03524543, 0.018300183, -0.047611345, 0.02682426, -0.037314992, 0.05846225, -0.022204908, 0.026318304, 0.0506528, -0.054883394, -0.013443573, 0.01051503, -0.014944291, -0.030025791, 0.024949076, 0.024880473, 0.022919536, 0.022096286, -0.003314264, -0.012304458, -0.05195628, -0.043163504, -0.06919882, 0.035371203, 0.052527986, -0.026944317, 0.035431232, 0.0025269228, 0.05272236, -0.005325762, -0.042363122, -0.0021331632, 0.010384968, 0.03630308 ] ],
    "index" : 0
  }, {
    "object" : "embedding",
    "embedding" : [ [ -0.03859099, -0.0025452692, 0.002827513, -0.023107057, 0.039019972, 5.159378E-4, 0.061831377, 0.03898519, -0.029060632, -0.022223009, -0.053750288, 0.043431528, -0.032805532, 0.023965022, -0.017704204, 0.011997003, 0.06898495, -0.021785328, 0.061373413, -0.06912407, -0.030892503, -0.030509897, 0.012025989, 0.016202766, 0.014523069, 0.023318652, -0.006604294, 0.02823745, -0.036880862, -0.03611565, 0.028460637, 0.028643245, 0.02898527, -0.04272429, -0.040660538, 0.030086711, -0.026191091, 0.012575259, -0.013680323, -0.01576219, -0.008541235, -0.021260696, 0.022008335, -0.003821708, -0.027663542, -0.03583449, -0.049043078, 0.02032737, -0.032077998, -0.0076017496, -0.041060533, 0.06408064, 0.04306052, -0.0013231777, -0.017536089, -0.029414253, -0.01623755, 7.7897916E-4, -0.008882537, -0.017736087, 0.026489638, 0.029350484, 0.04315907, -0.052324213, 0.031188153, 0.031260613, 0.008039789, 0.016778849, -0.013186849, 0.00850138, -0.013420633, -0.021936053, -0.043321386, -0.037240274, -0.007959356, -0.011695557, 0.018266518, 0.05426043, 0.02898527, -0.007870588, 0.005872416, -0.06765162, 0.011165126, 0.008720218, 0.02233605, -0.016701313, -0.03399592, -0.023336042, -0.044266306, 0.030689605, -0.03860838, -0.037344623, 0.034544647, 0.0287302, 0.041698214, -0.010895563, 0.0614024, -0.026791086, 0.04524601, 0.02768528, -0.054040138, -0.09088621, 1.3043372E-5, 0.023196913, -0.0216491, -0.027727311, 0.032509882, 0.024405599, -0.038202588, 0.017408554, -0.022408513, 0.022341846, -0.032341763, -0.0062035727, -0.04095039, 0.044011235, 0.048289463, -0.066109605, -0.026083846, -0.036417093, -0.006709909, 0.02206069, 0.027402675, 0.094144166, -0.007571315, 0.025495443, 0.0059477775, 0.030927286, -0.036080867, -0.020770846, 0.03634753, 0.027260648, 0.046666283, -0.014643359, 0.015353498, 0.014970892, -0.05443434, -0.012696274, -0.038857654, -0.014524519, -0.032654807, 0.003442001, 9.652095E-4, -0.0034563122, 0.025579503, -0.030290695, -0.005026691, -0.056857508, -0.024376612, -0.0010362234, 0.033646103, 0.06132124, 0.02885194, -0.01999114, -0.06839365, 0.03032439, 0.018050577, -0.0336519, -0.059222706, 0.0040927203, 0.0472228, 0.015218716, 0.014365191, 0.030280912, -0.0028231654, -0.018637529, 0.058353145, -0.020962149, 0.010339318, 0.076034166, -0.0139390165, -0.05917633, 0.022141848, -0.0033655523, -0.053286523, 0.049269162, 0.06115892, 0.0397446, -0.0021697287, -0.012431783, -0.08870652, 0.061819788, 0.02314184, 0.06744293, -0.041495316, -0.057182144, 0.06261978, -0.040509813, 0.024567915, 0.033280887, -0.01153179, -0.023972267, 0.018179562, -0.0034753338, 0.01546654, -0.025831673, -0.01932738, 0.02969541, 0.023617199, 0.019331727, -0.012065844, 0.02757079, 0.035448987, -0.04044025, -0.08306019, -0.005518796, 0.05088654, -0.041101113, -0.021089682, -0.015539004, -0.034370735, -0.027449053, 0.002491284, -0.05257928, 0.038289543, -0.022892568, 0.021760693, -0.04287501, 0.026283845, -0.013069458, 0.06844002, -0.029049039, -0.020631716, 0.026727319, -0.01527234, 0.038799684, 0.018989699, 0.0049050325, -0.005134741, -0.02601718, -0.0076673287, -0.0045050355, -0.01148007, -0.057866193, -0.052973483, 0.0210549, -0.0025536022, -0.025865007, 0.060382117, -0.0221404, -0.033425815, 0.02703746, -0.0149868345, 0.056057513, -0.026463551, -0.042590957, 0.042492405, -0.031338874, 0.010684695, -0.047825698, -0.0040680827, -0.029382369, 0.06259659, -0.050956108, 0.05108364, -0.037663464, 0.022369383, 0.07088638, 0.05288073, -0.008336164, 0.0109408535, 0.011480703, 0.053031452, -0.0383765, -0.022051994, -0.028486725, -0.027593978, -0.058086485, 0.036382314, 0.015199876, 0.005368797, 0.056718376, -0.009811333, 0.04100836, 0.03998808, -0.03548667, 0.041588064, 0.0067296554, -0.020220125, -0.026582392, -0.023315752, 0.02373604, -0.025530227, -0.030446127, 0.04246342, -0.035350434, 0.022324456, -0.020628817, -0.042967767, -0.058712564, -0.0029949031, 0.07806313, -0.024985302, -0.009120216, 0.023721546, -0.067454524, 0.011266574, 0.035350434, 0.014469448, 0.009962237, -0.02918817, 0.057889383, 0.041669227, 0.017017253, 0.02020853, -0.053118408, 0.0048550325, 0.011872185, -0.012254973, 0.026041092, -0.041906904, -0.04678223, 0.046376433, -0.039466344, -0.008434714, -0.0109317945, -0.05437637, -0.04884598, -0.031159166, -0.043008346, 0.013536846, 0.032677993, 0.061727032, -0.006807916, 0.012089757, -0.013465107, -0.02766934, 0.0055115493, -0.06427774, -0.065019764, -0.035234496, 0.04675904, -0.0059869075, 0.03499102, -0.03684608, -0.0098390505, -0.063593686, -0.015811466, -0.03543739, 0.004982568, 0.0049014096, 0.02172446, 0.035251886, -0.009378145, 0.04173879, -0.015215819, 0.033408422, -0.042903997, -0.00862493, 0.006968059, -0.007472403, 0.06191254, 0.022696918, -0.029228747, -0.028422957, -0.023040393, -0.008308628, 0.07406316, 0.027379489, -0.008115876, 0.019040424, -0.009273837, -0.0069673345, -0.011002809, 0.01806652, 0.020486789, -0.06972697, -0.021471564, 0.04533876, -0.022266487, -0.030283812, -0.028692521, -0.044075, -0.026515726, -0.029128022, -0.04504311, 0.030921487, 0.08469496, -0.032782342, 0.014194087, -0.03396494, -0.13650903, -0.012214213, 0.04805758, -0.032347564, -0.02746934, 0.023527345, 0.036214195, -0.0055876356, 0.013779597, -0.016514357, 0.03534464, 0.01294917, -0.02432444, -0.015641902, 0.02491284, -0.050051767, -0.02287083, 0.017144788, -0.0336519, -0.037460566, 0.03495044, 0.023257783, 0.08004572, -0.042851824, -0.051292334, 0.050434373, -0.032643214, 0.049344525, -0.08431236, -0.047083672, -0.04599383, 0.06449803, -0.015399874, -0.06425455, 0.019791143, 0.05728649, -0.021874098, 0.054561872, -0.035588115, 0.04233009, -0.04360544, 0.018565066, -0.04087503, 0.0026898333, -5.5760413E-4, 0.02457661, 0.03532145, -0.019567955, 0.0367997, -0.024602698, -0.04020837, -0.046573535, -0.016017986, 0.003593449, -0.054086514, 0.025596894, -0.02776789, 0.0042062155, -0.016185375, 0.04382573, 0.014463651, 0.027291082, 0.03497363, -0.0062620863, -0.027478037, -0.011715847, -0.032759152, 0.005775315, 7.014435E-4, -0.020028822, -0.003293089, 0.03933881, 0.0539242, -0.019943316, 0.053402465, -0.028764984, 0.06067197, -0.020599833, -0.03490986, 0.014773793, 0.0183013, -0.020828815, -0.053727098, 0.059976324, -1.688392E-4, -0.03583739, -0.014573794, -0.018708544, -0.053286523, -0.053101014, 0.024312844, -0.010033252, 0.008641234, -0.002898799, -0.013137574, -0.044243116, 0.061228488, -0.0069245812, -0.015627408, -0.05443434, 0.0077484874, -0.03904316, 0.014356405, -0.033373643, -0.04498514, 0.051048856, 0.022487497, 0.03756491, -0.058619812, -0.030730184, 0.045303978, 0.039918512, -0.04083445, -0.06504295, -0.04686339, -0.043141678, 0.016592618, 0.0048832935, -0.004784019, 0.026109932, 0.053205363, 0.002107229, -0.050318427, -0.015707843, 0.07165159, -0.018866513, 0.021356348, 0.010883245, 0.0028449043, -0.04928076, 0.016862182, -1.4420172E-4, -0.03745477, 0.06972697, -0.013194095, -0.04233009, 0.043477908, -0.0049738726, -0.062376305, 0.014419448, 0.034248997, -0.028266437, -0.023153435, 0.03197655, 0.048301052, 0.04439384, -0.02898527, 0.010327452, -0.012039938, -0.04720541, -0.02123461, -0.02084041, 0.05700823, 0.040741697, -0.040190976, 0.01771145, -0.077077635, 0.033524364, 0.026527321, -0.015602772, 0.034979425, 0.013237573, 0.022220109, -0.025722979, -0.010891216, -0.037779402, 0.0486083, 0.032834515, 0.02749253, -0.042422842, -0.04227212, -0.020172298, 0.020483892, 0.035020005, -0.012249175, -0.018825933, 0.010697014, -0.06284007, -0.014791184, -0.02623167, -0.043477908, 0.021579536, -0.028451942, -0.020930264, 0.043738775, -0.054144483, 0.012956416, 1.356873E-4, 0.03852722, -0.06169225, 0.0020688237, 0.0143165495, 0.0395533, -0.01948245, -0.023360679, 0.053286523, 0.038990986, 0.032243215, 0.0017579567, 0.03821418, 0.052811164, 0.05951256, 0.014761474, -0.008394134, -0.04570977, 0.050411183, -0.04535615, 0.013478151, 0.065645844, -0.02176504, 0.03219684, 0.044764854, -0.04004025, 0.055987947, 5.661186E-4, -0.0403417, 0.026411379, 0.026312828, 0.017658552, 0.033106975, 0.02964034, 0.015648967, 0.02072012, 0.04390689, 0.059912555, -0.038098242, 0.054364774, -0.057414025, 1.2608593E-4, 0.039582286, -0.014165102, -0.026573697, -0.0014348616, 0.012311494, -0.006537628, -0.012820186, 0.010105714, 0.0053970576, -0.05604592, 0.01999114, 0.04630687, -0.026991084, -0.022107065, 0.085657276, -0.062040072, -0.029628742, 0.046527155, 0.039825764, -0.0245998, 0.033246104, 0.0759646, 0.016838994, 0.032301188, -0.011652441, 0.023553431, 0.0022333153, 0.061796594, 0.049703944, 0.029820045, 0.047808304, 0.018956367, -0.06025458, 0.0025391097, 0.051918417, -0.025646167, 0.0145622, 0.021872284, 0.007741966, 0.059651688, -0.035182323, 0.0367997, 0.039541706, 0.03366929, 0.06706032, -0.015962189, 0.0242027, 0.04764599, 0.04159966, -0.020562151, -0.021808518, -0.025863556, 0.023112493, -0.0050463355, -2.4492553E-4, 0.06832408, -0.069054514, 0.038011286, -0.035750434, 0.0045985132, 0.05482854, 0.043385155, -0.059373427, -0.053448837, 0.032167852, -0.04661411, -0.004763729, 0.0086589875, -0.022428801, 0.011929749, -0.033895377, 0.025895441, 0.0035796808, 0.028991068, 0.05118799, -0.003233307, 0.018024852, 0.053541593, 0.052219864, -0.025014289, -0.029611353, -0.030991051, -0.0037087786, -0.02127229, 0.0513677, -0.0010724551, -0.037866358, -0.013722714, -0.031808436, 0.006594874, 0.0064303824, -0.010605711, -0.025965005, -0.03821418, 0.01824188, 0.013044821, 0.030330187, 0.023999805, -0.010734695, 0.032359157, -0.04652136, -0.048277866, 0.02615341, 0.053402465, -0.0649386, 0.005019524, -0.042225745, 0.054306805, 0.025060665, -0.066782065, -0.09074709, 0.043796744, -0.017163629, -0.010674007, 0.017776666, 0.034324355, 0.06856756, -0.023283869, -0.027999772, -0.018759267, -0.0061187907, 0.02621428, -0.04045764, 0.030486709, 0.009367315, -0.019452015, -0.0253853, 0.010181077, -0.0024782408, 0.013219367, -0.029773671, 0.03768665, 0.0539242, -0.01145353, -0.040811263, 0.085657276, -0.019811433, -0.033280887, 0.0067633507, 0.045785137, 0.04927496, 0.034306966, -0.009710065, 0.001575893, -0.04988945, -0.022904161, -0.048915546, 0.010472379, 0.07029508, -0.050747413, -0.005718794, 0.0033557697, 0.07256752, 0.0028471234, -0.050306838, -0.015710741, 0.010923099, -0.006999943 ] ],
    "index" : 1
  } ],
  "model" : "e5-base-v2",
  "usage" : {
    "total_tokens" : 6
  }
}
```

Each embedding has an index that corresponds to the text string in a list in the request. The index is 0-based, so the first text string in the list has an index of 0, the second text string has an index of 1, and so on.

In the preceding example, “foo” corresponds to the 0 index and “bar” corresponds to the 1 index. The embedding for “foo” is the first element in the list of embeddings, and the embedding for “bar” is the second element in the list of embeddings.

### Usage quotas[¶](#usage-quotas "Link to this heading")

The following table shows the usage quotas for the EMBED function.

EMBED function quotas[¶](#id19 "Link to this table")

| Model | Tokens Processed  per Minute (TPM) | Requests per  Minute (RPM) | Max output (tokens) |
| --- | --- | --- | --- |
| `snowflake-arctic-embed-m-v1.5` | 400,000 | 200 | 4,096 |
| `snowflake-arctic-embed-m` | 400,000 | 200 | 4,096 |
| `e5-base-v2` | 400,000 | 200 | 4,096 |
| `nv-embed-qa-4` | 400,000 | 200 | 4,096 |
| `multilingual-e5-large` | 400,000 | 200 | 4,096 |
| `voyage-multilingual-2` | 400,000 | 200 | 4,096 |

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

1. [Setting up authentication](#setting-up-authentication)
2. [Setting up authorization](#setting-up-authorization)
3. [Submitting requests](#submitting-requests)
4. [Prompt caching](#prompt-caching)
5. [Cost considerations](#cost-considerations)
6. [COMPLETE function](#complete-function)
7. [Model availability](#model-availability)
8. [API Reference](#api-reference)
9. [Basic example](#basic-example)
10. [Tool calling with chain of thought example](#tool-calling-with-chain-of-thought-example)
11. [Response](#response)
12. [Structured output example](#structured-output-example)
13. [Image input example](#image-input-example)
14. [Prompt caching example](#prompt-caching-example)
15. [Thinking and reasoning examples](#thinking-and-reasoning-examples)
16. [Python API example request](#python-api-example-request)
17. [Rate Limits](#rate-limits)
18. [EMBED function](#embed-function)
19. [Model availability](#id2)
20. [API Reference](#id3)
21. [CURL request example](#curl-request-example)
22. [Python request example](#python-request-example)
23. [Usage quotas](#usage-quotas)