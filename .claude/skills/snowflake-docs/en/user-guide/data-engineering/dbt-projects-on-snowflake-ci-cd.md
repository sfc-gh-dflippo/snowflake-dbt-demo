---
auto_generated: true
description: dbt project objects support using Snowflake CLI commands to integrate
  deployment and execution into your CI/CD workflows.
last_scraped: '2026-01-14T16:57:47.664402+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-ci-cd
title: CI/CD integrations on dbt Projects on Snowflake | Snowflake Documentation
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
    - [dbt Projects on Snowflake](dbt-projects-on-snowflake.md)

      * Tutorials

        * [Tutorial: Getting started with dbt Projects](../tutorials/dbt-projects-on-snowflake-getting-started-tutorial.md)
        * [Tutorial: Set up CI/CD integrations on dbt Projects](../tutorials/dbt-projects-on-snowflake-ci-cd-tutorial.md)
      * Key concepts

        * [Understanding dbt dependencies](dbt-projects-on-snowflake-dependencies.md)
        * [Understanding schema generation and customization](dbt-projects-on-snowflake-schema-customization.md)
        * [Using workspaces for dbt Projects on Snowflake](dbt-projects-on-snowflake-using-workspaces.md)
        * [Understanding dbt project objects](dbt-projects-on-snowflake-understanding-dbt-project-objects.md)
      * [Access control](dbt-projects-on-snowflake-access-control.md)
      * dbt Project operations

        * [Deploying dbt projects](dbt-projects-on-snowflake-deploy.md)
        * [Scheduling project runs](dbt-projects-on-snowflake-schedule-project-execution.md)
      * [CI/CD integrations on dbt Projects](dbt-projects-on-snowflake-ci-cd.md)
      * [Managing dbt Projects](dbt-projects-on-snowflake-manage.md)
      * [Monitoring & observability](dbt-projects-on-snowflake-monitoring-observability.md)
      * Supported commands and limitations

        * [Supported dbt commands and flags](dbt-projects-on-snowflake-supported-commands.md)
        * [Supported source file locations](dbt-projects-on-snowflake-sources.md)
        * [Limitations](dbt-projects-on-snowflake-limitations.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)Data engineering[dbt Projects on Snowflake](dbt-projects-on-snowflake.md)CI/CD integrations on dbt Projects

# CI/CD integrations on dbt Projects on Snowflake[¶](#ci-cd-integrations-on-sf-dbt "Link to this heading")

dbt project objects support using Snowflake CLI commands to integrate deployment and execution into your CI/CD workflows.

This topic explains how to use GitHub Actions to automatically test and deploy your dbt Projects on Snowflake whenever you open a pull request or merge to
main.

Continuous Integration (CI) runs your dbt project against a dev schema on each pull request. In other words, whenever someone opens or
updates a pull request in your code repository, you automatically run tests and builds on the new code. This helps catch problems early
before merging.

Continuous Deployment (CD) keeps a dbt project object in Snowflake up to date after your commits are merged. In other words, whenever code
gets merged into a branch, you automatically deploy the updated code to production. This ensures that your production environment stays
up-to-date, reliably and reproducibly.

CI/CD helps avoid manual, error-prone deployments, ensures changes are validated before being merged, and enables consistent, repeatable
deployments and versioning.

## Why use CI/CD for a dbt Project[¶](#why-use-ci-cd-for-a-dbt-project "Link to this heading")

dbt projects define all your data transformations in code, so frequent updates can easily introduce errors. CI catches these issues early by
testing every change in a separate dev environment before merging.

After changes are merged, CD automatically updates the official dbt project object in your Snowflake production environment. This removes
manual steps, reduces risk, keeps everything version-controlled, and supports a reliable, collaborative workflow.

## High-level prerequisites for using CI/CD on dbt Projects[¶](#high-level-prerequisites-for-using-ci-cd-on-dbt-projects "Link to this heading")

* A dbt project stored in a Git repository (for example, GitHub).
* A Snowflake account and user with privileges as described in [Access control for dbt projects on Snowflake](dbt-projects-on-snowflake-access-control).
* Privileges to create and edit the following objects or access to an administrator who can create each of them on your behalf:

  + GitHub repository environment variables and secrets to hold Snowflake account, database and schema values, and workflow files (for example,
    `.github/workflows/…`) that define CI and CD jobs.
  + Snowflake service account to communicate with GitHub
* A separation between dev environment (for CI) and prod environment (for CD) in Snowflake (for example, separate databases or schemas for each
  environment).
* A way to permit your CI/CD runner (for example, GitHub Actions) to connect to Snowflake, such as OIDC or PAT. For more information, see
  [Safely configure the action in your CI/CD workflow](../../developer-guide/snowflake-cli/cicd/integrate-ci-cd.html#label-integrate-ci-cd-safely-configure).
* In your code repository, a `profiles.yml` file configured to point to dev and prod targets (for example, databases/schemas, warehouse).
* A network policy that allows inbound access from your Git provider into Snowflake.

## CI/CD workflow overview[¶](#ci-cd-workflow-overview "Link to this heading")

The following steps outline the typical workflow with CI/CD. For a detailed tutorial, see [Tutorial: Setting up CI/CD integrations on dbt Projects on Snowflake](../tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

1. Developer writes or modifies dbt code (models, tests, etc.) in a branch.
2. Developer opens a pull request.
3. CI kicks in: a tester instance of the dbt project object is deployed to the Snowflake dev environment, which runs the `dbt run`
   and `dbt test` commands.

   * If an operation fails, the pull request fails. The developer must fix and update, then rerun.
   * If all operations pass, the pull request is eligible for merge.
4. Pull request is merged to main.
5. CD kicks in: the production dbt project object in Snowflake is updated to reflect the latest code.
6. Optionally, automated scheduling (for example, via Snowflake tasks) can be deployed, so data pipelines run on a schedule without manual
   intervention.

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

1. [Why use CI/CD for a dbt Project](#why-use-ci-cd-for-a-dbt-project)
2. [High-level prerequisites for using CI/CD on dbt Projects](#high-level-prerequisites-for-using-ci-cd-on-dbt-projects)
3. [CI/CD workflow overview](#ci-cd-workflow-overview)

Related content

1. [Workspaces](/user-guide/data-engineering/../ui-snowsight/workspaces)
2. [CREATE DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/create-dbt-project)
3. [EXECUTE DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/execute-dbt-project)
4. [snow dbt commands](/user-guide/data-engineering/../../developer-guide/snowflake-cli/command-reference/dbt-commands/overview)
5. [Integrating CI/CD with Snowflake CLI](/user-guide/data-engineering/../../developer-guide/snowflake-cli/cicd/integrate-ci-cd)
6. [Snowflake CLI](/user-guide/data-engineering/../../developer-guide/snowflake-cli/index)