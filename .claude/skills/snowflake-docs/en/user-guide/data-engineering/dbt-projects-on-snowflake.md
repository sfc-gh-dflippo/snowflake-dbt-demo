---
auto_generated: true
description: dbt Core is an open-source data transformation tool and framework that
  you can use to define, test, and deploy SQL transformations.
last_scraped: '2026-01-14T16:54:19.594274+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake
title: dbt Projects on Snowflake | Snowflake Documentation
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

[Guides](../../guides/README.md)Data engineeringdbt Projects on Snowflake

# dbt Projects on Snowflake[¶](#dbt-projects-on-snowflake "Link to this heading")

[dbt Core](https://github.com/dbt-labs/dbt-core) is an open-source data transformation tool and framework that you can use to define, test, and deploy SQL transformations.

With dbt Projects on Snowflake, you can use familiar Snowflake features to create, edit, test, run, and manage your dbt Core projects, typically as follows:

1. **Start with a valid dbt project:** (With `dbt_project.yml`, `profile.yml`, `/models/...`.) This is stored either in a
   workspace in Snowsight or a Git repository that you’ve connected to Snowflake. Prepare a database, schema, and warehouse with a
   role that has the [necessary privileges](dbt-projects-on-snowflake-access-control).
2. **Install dependencies:** Execute the `dbt deps` command within a Snowflake workspace, local machine, or git orchestrator to
   populate the `dbt_packages` folder for your dbt Project.

   For more information, see [Understand dependencies for dbt Projects on Snowflake](dbt-projects-on-snowflake-dependencies).
3. **Deploy the DBT PROJECT object:** Create a schema-level DBT PROJECT object by copying your project files into a new version of that
   object. You can do this by using the CREATE OR REPLACE DBT PROJECT … FROM <source> command or the `snow dbt deploy` Snowflake CLI
   command.

   For more information, see [Deploy dbt project objects](dbt-projects-on-snowflake-deploy).
4. **Execute the dbt project in Snowflake:** Execute a dbt Core project within a dbt project object by using the EXECUTE DBT PROJECT command
   or the `snow dbt execute` Snowflake CLI command. Executing a dbt project involves invoking dbt Core commands to build or test models;
   this is what you schedule and orchestrate.

   For more information, see [EXECUTE DBT PROJECT](../../sql-reference/sql/execute-dbt-project).
5. **Schedule with Snowflake tasks:** Use Snowflake tasks to schedule and orchestrate dbt project runs.

   For more information, see [Scheduling runs of dbt Projects on Snowflake](dbt-projects-on-snowflake-schedule-project-execution).
6. **Set up CI/CD integrations:** Use Snowflake CLI commands to integrate deployment and execution into your CI/CD workflows.

   dbt project objects support Snowflake CLI commands that you can use to create and manage dbt projects from the command line. This is
   useful for integrating dbt projects into your data engineering workflows and CI/CD pipelines. For more information, see
   [Snowflake CLI](../../developer-guide/snowflake-cli/index), [Integrating CI/CD with Snowflake CLI](../../developer-guide/snowflake-cli/cicd/integrate-ci-cd), and
   [snow dbt commands](../../developer-guide/snowflake-cli/command-reference/dbt-commands/overview).
7. **Monitor the dbt project:** Use Snowflake monitoring features to inspect, manage, and tune dbt project execution whether you execute a
   dbt project object manually or use tasks to execute dbt project objects on a schedule.

   For more information, see [Monitor dbt Projects on Snowflake](dbt-projects-on-snowflake-monitoring-observability).

## Key concepts[¶](#key-concepts "Link to this heading")

* **dbt project objects:** A *dbt project* is a directory that contains a `dbt_project.yml` file and a set of files that define dbt
  assets, such as models and sources. A DBT PROJECT is a schema-level object that contains versioned source files for your dbt project in
  Snowflake. You can connect a dbt project object to a workspace, or you can create and manage the object independent of a workspace. You
  can CREATE, ALTER, and DROP dbt project objects like other schema-level objects in Snowflake.

  A dbt project object is typically based on a dbt project directory that contains a `dbt-project.yml` file. This is the pattern that
  Snowflake uses when you deploy (create) a dbt project object from within a workspace.

  For more information, see [Understanding dbt project objects](dbt-projects-on-snowflake-understanding-dbt-project-objects).
* **Schema customization:** dbt uses the default macro `generate_schema_name` to decide where a model is built. You can customize how
  dbt builds your models, seeds, snapshots, and test tables.

  For more information, see [Understanding schema generation and customization](dbt-projects-on-snowflake-schema-customization).
* **Workspaces:** Workspaces in the Snowflake web interface are a Git-connected web IDE where you can visualize, test, run, and scaffold one
  or many dbt projects, link them to a Snowflake dbt project object to create/update it, and edit other Snowflake code in one place.

  For more information, see [Using workspaces for dbt Projects on Snowflake](dbt-projects-on-snowflake-using-workspaces).
* **Versioning:** Every dbt project object is versioned; versions live under `snow://dbt/<db>.<schema>.<project>/versions/...`.

  For more information, see [Versioning for dbt project objects and files](dbt-projects-on-snowflake-understanding-dbt-project-objects.html#label-dbt-key-concepts-dbt-project-versioning).

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

1. [Key concepts](#key-concepts)

Related content

1. [Workspaces](/user-guide/data-engineering/../ui-snowsight/workspaces)
2. [CREATE DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/create-dbt-project)
3. [EXECUTE DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/execute-dbt-project)
4. [ALTER DBT PROJECT](/user-guide/data-engineering/../../sql-reference/sql/alter-dbt-project)
5. [Managing dbt Projects on Snowflake using Snowflake CLI](/user-guide/data-engineering/../../developer-guide/snowflake-cli/data-pipelines/dbt-projects)
6. [snow dbt commands](/user-guide/data-engineering/../../developer-guide/snowflake-cli/command-reference/dbt-commands/overview)
7. [Managing data pipelines in Snowflake CLI](/user-guide/data-engineering/../../developer-guide/snowflake-cli/data-pipelines/data-pipelines)