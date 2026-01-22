---
auto_generated: true
description: 'Lists the existing objects for the specified object type. The output
  includes metadata for the objects, including:'
last_scraped: '2026-01-14T16:55:27.482153+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/show.html
title: SHOW <objects> | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)

     + [ALTER](alter.md)
     + [COMMENT](comment.md)
     + [CREATE](create.md)
     + [CREATE OR ALTER](create-or-alter.md)
     + [DESCRIBE](desc.md)
     + [DROP](drop.md)
     + [UNDROP](undrop.md)
     + [SHOW](show.md)
     + [USE](use.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[General DDL](../sql-ddl-summary.md)SHOW

# SHOW *<objects>*[¶](#show-objects "Link to this heading")

Lists the existing objects for the specified object type. The output includes metadata for the objects, including:

* Common properties (name, creation timestamp, owning role, comment, etc.)
* Object-specific properties

See also:
:   [CREATE <object>](create) , [DESCRIBE <object>](desc)

## SHOW commands[¶](#show-commands "Link to this heading")

For specific syntax, usage notes, and examples, see:

**Account Operations**

> * [SHOW ACCOUNTS](show-accounts)
> * [SHOW CONNECTIONS](show-connections)
> * [SHOW GLOBAL ACCOUNTS](show-global-accounts)
> * [SHOW ORGANIZATION ACCOUNTS](show-organization-accounts)
> * [SHOW PARAMETERS](show-parameters)
> * [SHOW REGIONS](show-regions)
> * [SHOW RELEASE DIRECTIVES](show-release-directives)
> * [SHOW REPLICATION ACCOUNTS](show-replication-accounts)
> * [SHOW VERSIONS IN APPLICATION PACKAGE](show-versions)

**Session / User Operations:**

> * [SHOW LOCKS](show-locks)
> * [SHOW PARAMETERS](show-parameters)
> * [SHOW TRANSACTIONS](show-transactions)
> * [SHOW VARIABLES](show-variables)

**Account Objects:**

> * [SHOW APPLICATIONS](show-applications)
> * [SHOW APPLICATION PACKAGES](show-application-packages)
> * [SHOW CATALOG INTEGRATIONS](show-catalog-integrations)
> * [SHOW COMPUTE POOLS](show-compute-pools)
> * [SHOW COMPUTE POOL INSTANCE FAMILIES](show-compute-pool-instance-families)
> * [SHOW DATABASE ROLES](show-database-roles)
> * [SHOW DATABASES](show-databases)
> * [SHOW EXTERNAL VOLUMES](show-external-volumes)
> * [SHOW FAILOVER GROUPS](show-failover-groups)
> * [SHOW INTEGRATIONS](show-integrations)
> * [SHOW FEATURE POLICIES](show-feature-policies)
> * [SHOW FUNCTIONS](show-functions)
> * [SHOW GRANTS](show-grants)
> * [SHOW NETWORK POLICIES](show-network-policies)
> * [SHOW NOTIFICATION INTEGRATIONS](show-notification-integrations)
> * [SHOW OPENFLOW DATA PLANE INTEGRATIONS](show-oflow-data-plane-integration)
> * [SHOW ORGANIZATION PROFILES](show-organization-profiles)
> * [SHOW PARAMETERS](show-parameters)
> * [SHOW REPLICATION DATABASES](show-replication-databases)
> * [SHOW REPLICATION GROUPS](show-replication-groups)
> * [SHOW RESOURCE MONITORS](show-resource-monitors)
> * [SHOW ROLES](show-roles)
> * [SHOW SHARES](show-shares)
> * [SHOW USER PROGRAMMATIC ACCESS TOKENS](show-user-programmatic-access-tokens)
> * [SHOW USERS](show-users)
> * [SHOW WAREHOUSES](show-warehouses)

**Database Objects:**

> * [SHOW AGENTS](show-agents)
> * [SHOW AGGREGATION POLICIES](show-aggregation-policies)
> * [SHOW ALERTS](show-alerts)
> * [SHOW AUTHENTICATION POLICIES](show-authentication-policies)
> * [SHOW BACKUP POLICIES](show-backup-policies)
> * [SHOW BACKUP SETS](show-backup-sets)
> * [SHOW CHANNELS](show-channels)
> * [SHOW CLASSES](show-classes)
> * [SHOW COLUMNS](show-columns)
> * [SHOW CONTACTS](show-contacts)
> * [SHOW CORTEX SEARCH SERVICES](show-cortex-search)
> * [SHOW DATA METRIC FUNCTIONS](show-data-metric-functions)
> * [SHOW DATASETS](show-datasets)
> * [SHOW DBT PROJECTS](show-dbt-projects)
> * [SHOW DYNAMIC TABLES](show-dynamic-tables)
> * [SHOW EVENT TABLES](show-event-tables)
> * [SHOW EXPERIMENTS](show-experiments)
> * [SHOW EXTERNAL FUNCTIONS](show-external-functions)
> * [SHOW EXTERNAL TABLES](show-external-tables)
> * [SHOW FILE FORMATS](show-file-formats)
> * [SHOW FUNCTIONS](show-functions)
> * [SHOW GIT BRANCHES](show-git-branches)
> * [SHOW GIT REPOSITORIES](show-git-repositories)
> * [SHOW GIT TAGS](show-git-tags)
> * [SHOW HYBRID TABLES](show-hybrid-tables)
> * [SHOW ICEBERG TABLES](show-iceberg-tables)
> * [SHOW INDEXES](show-indexes)
> * [SHOW IMAGE REPOSITORIES](show-image-repositories)
> * [SHOW JOIN POLICIES](show-join-policies)
> * [SHOW LISTINGS](show-listings)
> * [SHOW MASKING POLICIES](show-masking-policies)
> * [SHOW MATERIALIZED VIEWS](show-materialized-views)
> * [SHOW MCP SERVERS](show-mcp-servers)
> * [SHOW MODEL MONITORS](show-model-monitors)
> * [SHOW MODELS](show-models)
> * [SHOW NETWORK RULES](show-network-rules)
> * [SHOW NOTEBOOKS](show-notebooks)
> * [SHOW NOTEBOOK PROJECTS](show-notebook-projects)
> * [SHOW OBJECTS](show-objects)
> * [SHOW OBJECTS OWNED BY APPLICATION](show-objects-owned-by-application)
> * [SHOW ONLINE FEATURE TABLES](show-online-feature-tables)
> * [SHOW PACKAGES POLICIES](show-packages-policies)
> * [SHOW PASSWORD POLICIES](show-password-policies)
> * [SHOW PIPES](show-pipes)
> * [SHOW PRIVACY POLICIES](show-privacy-policies)
> * [SHOW PROCEDURES](show-procedures)
> * [SHOW PROJECTION POLICIES](show-projection-policies)
> * [SHOW ROW ACCESS POLICIES](show-row-access-policies)
> * [SHOW SCHEMAS](show-schemas)
> * [SHOW SECRETS](show-secrets)
> * [SHOW SEMANTIC DIMENSIONS](show-semantic-dimensions)
> * [SHOW SEMANTIC DIMENSIONS FOR METRIC](show-semantic-dimensions-for-metric)
> * [SHOW SEMANTIC FACTS](show-semantic-facts)
> * [SHOW SEMANTIC METRICS](show-semantic-metrics)
> * [SHOW SEMANTIC VIEWS](show-semantic-views)
> * [SHOW SEQUENCES](show-sequences)
> * [SHOW SERVICES](show-services)
> * [SHOW SESSION POLICIES](show-session-policies)
> * [SHOW SNAPSHOT POLICIES — Deprecated](show-snapshot-policies) (deprecated; prefer [SHOW BACKUP POLICIES](show-backup-policies))
> * [SHOW SNAPSHOT SETS — Deprecated](show-snapshot-sets) (deprecated; prefer [SHOW BACKUP SETS](show-backup-sets))
> * [SHOW SNAPSHOTS](show-snapshots)
> * [SHOW SPECIFICATIONS](show-specifications)
> * [SHOW STAGES](show-stages)
> * [SHOW STORAGE LIFECYCLE POLICIES](show-storage-lifecycle-policies)
> * [SHOW STREAMLITS](show-streamlits)
> * [SHOW STREAMS](show-streams)
> * [SHOW TABLES](show-tables)
> * [SHOW TAGS](show-tags)
> * [SHOW TASKS](show-tasks)
> * [SHOW USER FUNCTIONS](show-user-functions)
> * [SHOW USER PROCEDURES](show-user-procedures)
> * [SHOW VERSIONS IN DATASET](show-versions-in-dataset)
> * [SHOW VERSIONS IN DBT PROJECT](show-versions-in-dbt-project)
> * [SHOW VERSIONS IN LISTING](show-versions-in-listing)
> * [SHOW VERSIONS IN MODEL](show-versions-in-model)
> * [SHOW VIEWS](show-views)

**Classes:**

> * [SHOW SNOWFLAKE.ML.ANOMALY\_DETECTION](../classes/anomaly-detection/commands/show-anomaly-detection.html#label-class-anomaly-detection-show)
> * [SHOW BUDGET](../classes/budget/commands/show-budget)
> * [SHOW SNOWFLAKE.ML.CLASSIFICATION](../classes/classification/commands/show-classification)
> * [SHOW CLASSIFICATION\_PROFILE](../classes/classification_profile/commands/show-classification-profile)
> * [SHOW CUSTOM\_CLASSIFIER](../classes/custom_classifier/commands/show-custom-classifiers)
> * [SHOW SNOWFLAKE.ML.FORECAST](../classes/forecast/commands/show-forecast.html#label-class-forecast-show)

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

1. [SHOW commands](#show-commands)