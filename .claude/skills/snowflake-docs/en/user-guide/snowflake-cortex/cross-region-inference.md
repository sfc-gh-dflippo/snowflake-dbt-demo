---
auto_generated: true
description: Inference is the process of using a machine learning model to get an
  output based on a user input. For example, when you call the SNOWFLAKE.CORTEX.COMPLETE
  function, you are requesting an inference fr
last_scraped: '2026-01-14T16:55:58.994503+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference
title: Cross-region inference | Snowflake Documentation
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

[Guides](../../guides/README.md)[Snowflake AI & ML](../../guides/overview-ai-features.md)Cross-region inference

# Cross-region inference[¶](#cross-region-inference "Link to this heading")

Inference is the process of using a machine learning model to get an output based on a user input. For example, when you call the
SNOWFLAKE.CORTEX.COMPLETE function, you are requesting an inference from the LLM with your prompt as the input. In Snowflake, you can
configure your account to allow cross-region inference processing with the [CORTEX\_ENABLED\_CROSS\_REGION](../../sql-reference/parameters.html#label-cortex-enable-cross-region)
parameter. This parameter enables inference requests to be processed in a different region from the default region.
The cross-region inference parameter is used to determine the inference behavior for any Snowflake feature supported by
cross-region inference, including Cortex LLM Functions.

When enabled, cross-region inference occurs if the LLM or feature is not supported in your default region.

By default, the parameter is set to DISABLED. This allows requests to be processed only in the default region.
You can specify the regions you want to allow cross-region inference to using the [ALTER ACCOUNT](../../sql-reference/sql/alter-account) command.

For details on this parameter, see [CORTEX\_ENABLED\_CROSS\_REGION](../../sql-reference/parameters.html#label-cortex-enable-cross-region).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

This parameter can only be set at the account level, not at the user or session levels. Only the ACCOUNTADMIN role can set the parameter
using the [ALTER ACCOUNT](../../sql-reference/sql/alter-account) command:

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';
```

Copy

This parameter cannot be set by the ORGADMIN role.

## How to use the cross-region inference parameter[¶](#how-to-use-the-cross-region-inference-parameter "Link to this heading")

By default, this parameter is set to `DISABLED`, which means the inference requests are only processed in the default region. The
following examples show how to set the cross-region parameter for various use cases.

### Any region[¶](#any-region "Link to this heading")

To allow any of the Snowflake regions that support cross-region inference requests to process your requests, set the parameter to
`'ANY_REGION'`.

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

Copy

### Default region only[¶](#default-region-only "Link to this heading")

To process inference requests only in the default region, set this parameter to `'DISABLED'`.

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'DISABLED';
```

Copy

### Specify regions[¶](#specify-regions "Link to this heading")

To allow only specified regions to process your requests, set this parameter to the regions separated by commas. For a full list of
regions, see [CORTEX\_ENABLED\_CROSS\_REGION](../../sql-reference/parameters.html#label-cortex-enable-cross-region).

The following example specifies `AWS_US` and `AWS_EU` regions to process your inference requests:

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US,AWS_EU';
```

Copy

### US Commercial Gov regions[¶](#us-commercial-gov-regions "Link to this heading")

Cross-region inference for Snowflake’s government-authorized, FIPS-compliant commercial environments is designed to maintain data-handling boundaries while providing access to supported AI models. When enabled, inference requests remain within the same cloud and compliance boundary, and processing occurs on FIPS-validated infrastructure such as AWS Bedrock FIPS endpoints. This approach allows customers in select U.S. government-authorized regions to use Snowflake AI capabilities securely and without exceptions to compliance policies.

To enable this feature, set the CORTEX\_ENABLED\_CROSS\_REGION parameter to `AWS_US` for workloads in a supported government-authorized region:

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';
```

Copy

Cross-region inference is available for US Commercial Gov in these regions:

* US East (Commercial Gov - N. Virginia)
* US West (Commercial Gov - Oregon)

## Cost considerations[¶](#cost-considerations "Link to this heading")

* You are charged credits for the use of LLM as listed in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
  Credits are considered consumed in the requesting region. For example, if you call an LLM Function from the `us-east-2` region and
  the request is processed in the `us-west-2` region, the credits are considered consumed in the `us-east-2` region.
* You do not incur data egress charges for using cross-region inference.

## Considerations[¶](#considerations "Link to this heading")

* Latency between regions depends on the cloud provider infrastructure and network status. Snowflake recommends that you test your specific
  use-case with cross-region inference enabled.
* Cross-region inference is not supported in [U.S. SnowGov regions](../intro-regions.html#label-us-gov-regions). This means you cannot make cross-region
  inference requests into or out of the SnowGov regions.
* You can use this setting from GCP or Azure regions to make inference requests for features that are not supported in those regions.
* User inputs, service generated prompts, and outputs are not stored or cached during cross-region inference.
* The data required for the inference request traverses between regions as follows:

  + If both the source and destination regions are in AWS, the data stays within the [AWS global network](https://aws.amazon.com/about-aws/global-infrastructure/).
    All data flowing across the AWS global network that interconnects the data centers and regions is automatically
    encrypted at the physical layer.
  + If both the source and destination regions are in Azure, the traffic stays entirely within the Azure global network. It never enters the public internet.
  + If the regions are on different cloud providers, then the data traverses the public internet using Mutual Transport Layer Security (mTLS).
* Cross-region inference for [Cortex Search](cortex-search/cortex-search-overview) is not supported in [all regions](cortex-search/cortex-search-overview.html#label-cortex-search-overview-regional-availability).

## Next steps[¶](#next-steps "Link to this heading")

* For details on the cross-region inference parameter, see [CORTEX\_ENABLED\_CROSS\_REGION](../../sql-reference/parameters.html#label-cortex-enable-cross-region) section of the SQL parameter reference.

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

1. [Access control requirements](#access-control-requirements)
2. [How to use the cross-region inference parameter](#how-to-use-the-cross-region-inference-parameter)
3. [Cost considerations](#cost-considerations)
4. [Considerations](#considerations)
5. [Next steps](#next-steps)