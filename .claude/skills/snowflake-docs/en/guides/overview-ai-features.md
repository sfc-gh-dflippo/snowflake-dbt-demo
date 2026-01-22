---
auto_generated: true
description: Snowflake offers two broad categories of powerful, intelligent features
  based on Artificial Intelligence (AI) and Machine Learning (ML). These features
  can help you do more with your data in less time
last_scraped: '2026-01-14T16:54:24.150947+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-ai-features
title: Snowflake AI and ML | Snowflake Documentation
---

1. [Overview](README.md)
2. [Snowflake Horizon Catalog](../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](overview-connecting.md)
6. [Virtual warehouses](../user-guide/warehouses.md)
7. [Databases, Tables, & Views](overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](overview-loading-data.md)
    - [Dynamic Tables](../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](overview-unloading-data.md)
12. [Storage Lifecycle Policies](../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](overview-sharing.md)
19. [Snowflake AI & ML](overview-ai-features.md)

    * [Cross-region inference](../user-guide/snowflake-cortex/cross-region-inference.md)
    * [Opt out of AI features](../user-guide/snowflake-cortex/opting-out.md)
    * [Snowflake Intelligence](../user-guide/snowflake-cortex/snowflake-intelligence.md)
    * [Cortex AI Functions](../user-guide/snowflake-cortex/aisql.md)
    * [Cortex Agents](../user-guide/snowflake-cortex/cortex-agents.md)
    * [Snowflake-managed MCP server](../user-guide/snowflake-cortex/cortex-agents-mcp.md)
    * [Cortex Analyst](../user-guide/snowflake-cortex/cortex-analyst.md)
    * [Cortex Search](../user-guide/snowflake-cortex/cortex-search/cortex-search-overview.md)
    * [Cortex Knowledge Extensions](../user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview.md)
    * [Cortex REST API](../user-guide/snowflake-cortex/cortex-rest-api.md)
    * [AI Observability](../user-guide/snowflake-cortex/ai-observability.md)
    * [ML Functions](overview-ml-functions.md)
    * [Document AI](../user-guide/snowflake-cortex/document-ai/overview.md)
    * [Provisioned Throughput](../user-guide/snowflake-cortex/provisioned-throughput.md)
    * [ML Development and ML Ops](../developer-guide/snowpark-ml/overview.md)
21. [Snowflake Postgres](../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](overview-alerts.md)
25. [Security](overview-secure.md)
26. [Data Governance](overview-govern.md)
27. [Privacy](overview-privacy.md)
29. [Organizations & Accounts](overview-manage.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Snowflake AI & ML

# Snowflake AI and ML[¶](#snowflake-ai-and-ml "Link to this heading")

Snowflake offers two broad categories of powerful, intelligent features based on Artificial Intelligence (AI) and
Machine Learning (ML). These features can help you do more with your data in less time than ever before.

* **Snowflake Cortex** is a suite of AI features that use large language models (LLMs) to understand unstructured data,
  answer freeform questions, and provide intelligent assistance. This suite of Snowflake AI Features comprises:

  + [Cortex Agents](user-guide/snowflake-cortex/cortex-agents)
  + [Snowflake Cortex AI Functions (including LLM functions)](user-guide/snowflake-cortex/aisql)
  + [Cortex Analyst](user-guide/snowflake-cortex/cortex-analyst)
  + [Cortex Fine-tuning](user-guide/snowflake-cortex/cortex-finetuning)
  + [Cortex Search](user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
  + [Snowflake Copilot](user-guide/snowflake-copilot)
  + [Snowflake Intelligence](user-guide/snowflake-cortex/snowflake-intelligence)
* **Snowflake ML** provides functionality for you to build your own models.

  + [ML Functions](guides-overview-ml-functions) simplify the process of creating and using traditional machine
    learning models to detect patterns in your structured data. These powerful out-of-the-box analysis tools help
    time-strapped analysts, data engineers, and data scientists understand, predict, and classify data, without any
    programming.
  + For data scientists and developers, [Snowflake ML](developer-guide/snowflake-ml/overview) lets you develop
    and operationalize custom models to solve your unique data challenges, while keeping your data inside Snowflake.
    Snowflake ML incorporates model development classes based on popular ML frameworks, along with ML Ops capabilities
    such as a feature store, a model registry, framework connectors, and immutable data snapshots.

## Use of Snowflake AI Features[¶](#use-of-snowflake-ai-features "Link to this heading")

Snowflake AI Features and their underlying models are designed with the following principles in mind:

* **Full security.** Except as you elect, all AI models run inside of Snowflake’s security and governance perimeter. Your data is not
  available to other customers or model developers.
* **Data privacy.** Snowflake never uses your Customer Data to train models made available to our customer base.
* **Control.** You have control over your team’s use of Snowflake AI Features through familiar
  [role-based access control](user-guide/security-access-control-overview).

## AI/ML model update process[¶](#ai-ml-model-update-process "Link to this heading")

Snowflake is continually working to improve the quality of its offerings, including the models powering the Snowflake AI Features.
This section describes how updates to those models fit into [Snowflake’s Behavior Change](release-notes/intro-bcr-releases) process.

### Behavior change process for models[¶](#behavior-change-process-for-models "Link to this heading")

At Snowflake, feature updates are announced and deployed in the following 3 types of releases:

* [Bundled Behavior Changes](release-notes/intro-bcr-releases) - Once a month release that introduces behavior changes.
* [Unbundled Behavior Changes](release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes) - Unbundled releases are not
  associated with a bundled or standard weekly release.
* [What’s new](release-notes/new-features) - Newly released features or important updates to existing features.

Model updates follow a similar pattern of announcements. For model updates, the following would constitute a **behavior change**:

* Required syntax changes (e.g. specifying a new model or model version in the function parameter).
* Required prompts or input updates to get similar results.
* Significant changes in structure of the model output.
* Deprecation of a model.

**Bundled behavior changes** would include most anticipated behavior changes, including:

* Model deprecation in the ordinary course, such as planned deprecation by the model provider or Snowflake (including those on which
  fine-tuning is permitted).
* Model updates, e.g. new versions or new models, that may result in changes to syntax, prompts, or output structure.

**Unbundled behavior** changes would typically be reserved for the following:

* Model deprecation for emergency reasons, e.g. concerns about the quality of a model or its outputs.

Lastly, **What’s new** denotes general improvements that would likely not constitute a behavior change and therefore would be
automatically included. This would typically be the following:

* Model updates or new versions (whether provided by a third party or Snowflake) that improve results but have no anticipated material
  effect on how you interact with the model.

The following table shows some examples of model updates and how they would be announced:

| Type of update | Unbundled behavior change | Bundled behavior change | What’s new |
| --- | --- | --- | --- |
| A new version of the Jamba model is released but has no anticipated material effect on how you interact with the model. |  |  | ✔ |
| A new Llama model is made available through Snowflake. |  |  | ✔ |
| One of the Mistral models is deprecated. |  | ✔ |  |
| An update to the TRANSLATE model results in a change in the output structure. |  | ✔ |  |
| A model is deprecated due to safety concerns regarding the model output. | ✔ |  |  |

## Legal Notices[¶](#legal-notices "Link to this heading")

* If you choose to use any of the Snowflake AI Features, your use is subject to our
  [Acceptable Use Policy](https://www.snowflake.com/legal/acceptable-use-policy/).
* The outputs of Snowflake AI Features may be inaccurate, inappropriate, inefficient, or biased. Decisions based on such
  outputs, including those built into automatic pipelines, should have human oversight and review processes to ensure they are
  safe, accurate, and suitable for your intended use.
* Your use of any Snowflake AI Feature that is identified as being powered by a third-party, open-source model is subject to any
  applicable license agreement and/or acceptable use policy set forth under the Offering-Specific Terms page available at
  <https://www.snowflake.com/legal/>.
* For further information, see the [Snowflake AI Trust and Safety FAQ](https://www.snowflake.com/en/legal/snowflake-ai-trust-and-safety/).

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

1. [Use of Snowflake AI Features](#use-of-snowflake-ai-features)
2. [AI/ML model update process](#ai-ml-model-update-process)
3. [Legal Notices](#legal-notices)