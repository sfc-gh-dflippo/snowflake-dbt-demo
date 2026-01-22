---
auto_generated: true
description: All warehouse tasks can be performed from the Snowflake web interface
  or using the DDL commands for warehouses.
last_scraped: '2026-01-14T16:57:40.173469+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/warehouses-tasks
title: Working with warehouses | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)

   * [Overview](warehouses-overview.md)
   * [Multi-cluster](warehouses-multicluster.md)
   * [Considerations](warehouses-considerations.md)
   * [Working with warehouses](warehouses-tasks.md)
   * [Next-generation standard warehouses](warehouses-gen2.md)
   * [Query Acceleration Service](query-acceleration-service.md)
   * [Monitoring load](warehouses-load-monitoring.md)
   * [Snowpark-optimized warehouses](warehouses-snowpark-optimized.md)
   * [Interactive tables and warehouses](interactive.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Virtual warehouses](warehouses.md)Working with warehouses

# Working with warehouses[¶](#working-with-warehouses "Link to this heading")

All warehouse tasks can be performed from the Snowflake web interface or using the DDL commands for warehouses.

## Creating a warehouse[¶](#creating-a-warehouse "Link to this heading")

You can create a warehouse using the Snowsight or SQL:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses » Warehouse
>
> SQL:
> :   Execute a [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command.
>
> Python:
> :   Use the [WarehouseCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseCollection#snowflake.core.warehouse.WarehouseCollection.create)
>     API ([Creating a warehouse](../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses.html#label-snowflake-python-create-wh)).

When you create a warehouse, you can specify whether the warehouse is created initially in the “Started” (i.e. running) or “Suspended”
state. If you choose “Started”, the warehouse starts consuming credits once all the compute resources are provisioned for the warehouse.

Note

If you choose to create a warehouse in the “Started” state, the warehouse may take some time to become fully available as Snowflake
provisions all the compute resources for the warehouse.

## Starting or resuming a warehouse[¶](#starting-or-resuming-a-warehouse "Link to this heading")

A warehouse can be started at any time, including on initial creation. Once a warehouse is created, resuming a warehouse is the same as
starting a warehouse.

You can resume a suspended (that is, inactive) warehouse by using the following interfaces:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses » *<suspended\_warehouse\_name>* » [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Resume
>
> SQL:
> :   Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command with the `RESUME` keyword.
>
> Python:
> :   Use the [WarehouseResource.resume](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseResource#snowflake.core.warehouse.WarehouseResource.resume)
>     API ([Performing warehouse operations](../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses.html#label-snowflake-python-perform-wh-operations)).

Starting a warehouse typically takes only a few seconds; however, in some rare instances, it can take longer as Snowflake provisions the
compute resources for the warehouse.

Warehouses consume credits while running:

* A warehouse begins to consume credits once all the compute resources are provisioned for the warehouse.

  + In a rare instance when some of the compute resources fail to provision, the warehouse only consumes credits for the provisioned
    compute resources.
  + Once the remaining compute resources are successfully provisioned, the warehouse starts consuming credits for all requested compute
    resources.
* While starting or resuming a warehouse often takes only a few seconds, in some instances, it can take longer as Snowflake provisions the
  compute resources for the warehouse.
* Snowflake does not begin executing SQL statements submitted to a warehouse until all of the compute resources for the warehouse are
  successfully provisioned, unless any of the resources fail to provision:

  + If any of the compute resources for the warehouse fail to provision during start-up, Snowflake attempts to repair the failed resources.
  + During the repair process, the warehouse starts processing SQL statements once 50% or more of the requested compute resources are
    successfully provisioned.

Credits are billed on a per-second basis while the warehouse is running, with a 1-minute minimum each time the warehouse is resumed; however,
credit consumption is reported in 60-minute (i.e. hourly) increments.

Note

A warehouse must be running and the current warehouse for the session (i.e. [in use](../sql-reference/sql/use-warehouse)) to
process SQL statements submitted in the session. For more information, refer to [Using a Warehouse](#using-a-warehouse) in this topic.

## Suspending a warehouse[¶](#suspending-a-warehouse "Link to this heading")

A running warehouse can be suspended at any time, even while executing SQL statements. Suspending a warehouse stops the
warehouse from consuming credits once all the compute resources shut down.

You can suspend a warehouse by using the following interfaces:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses » *<started\_warehouse\_name>* » [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Suspend
>
> SQL:
> :   Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command with the `SUSPEND` keyword.
>
> Python:
> :   Use the [WarehouseResource.suspend](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseResource#snowflake.core.warehouse.WarehouseResource.suspend)
>     API ([Performing warehouse operations](../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses.html#label-snowflake-python-perform-wh-operations)).

When you suspend a warehouse, Snowflake immediately shuts down all idle compute resources for the warehouse, but allows any compute
resources that are executing statements to continue until the statements complete, at which time the resources are shut down and the status
of the warehouse changes to “Suspended”. Compute resources waiting to shut down are considered to be in “quiesce” mode.

## Resizing a warehouse[¶](#resizing-a-warehouse "Link to this heading")

A warehouse can be resized up or down at any time, including while it is running and processing statements.

You can resize a warehouse by using the following interfaces:

> Snowsight:
> :   In the navigation menu, select Compute » Warehouses » *<warehouse\_name>* » [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit
>
> SQL:
> :   Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command with `SET WAREHOUSE_SIZE = ...`.
>
> Python:
> :   Use the [WarehouseResource.create\_or\_alter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseResource#snowflake.core.warehouse.WarehouseResource.create_or_alter)
>     API ([Creating or altering a warehouse](../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses.html#label-snowflake-python-alter-wh)).

Resizing a warehouse to a larger size is useful when the operations being performed by the warehouse will benefit from more compute resources,
including:

* Improving the performance of large, complex queries against large data sets.
* Improving performance while loading and unloading significant amounts of data.

### Effects of resizing a running warehouse[¶](#effects-of-resizing-a-running-warehouse "Link to this heading")

Resizing a running warehouse adds or removes compute resources in each cluster in the warehouse. All the usage and credit
rules associated with starting or suspending a warehouse apply to resizing a started warehouse, such as:

* Compute resources added to a warehouse start using credits when they are provisioned; however, the additional compute resources don’t
  start executing statements until they are all provisioned, unless some of the resources fail to provision.
* Compute resources are removed from a warehouse only when they are no longer being used to execute any current statements.

Resizing a warehouse doesn’t have any impact on statements that are currently being executed by the warehouse. When resizing to a larger
size, the new compute resources, once fully provisioned, are used only to execute statements that are already in the warehouse queue, as
well as all future statements submitted to the warehouse.

Tip

To verify the additional compute resources for your warehouse have been fully provisioned, add the `WAIT_FOR_COMPLETION` parameter
to the [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command. You can also use [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses) to check its
`state`.

### Effects of resizing a suspended warehouse[¶](#effects-of-resizing-a-suspended-warehouse "Link to this heading")

Resizing a suspended warehouse does not provision any new compute resources for the warehouse. It simply instructs Snowflake to provision
the additional compute resources when the warehouse is next resumed, at which time all the usage and credit rules associated with starting a
warehouse apply.

## Using a warehouse[¶](#using-a-warehouse "Link to this heading")

To execute a query or DML statement in Snowflake, a warehouse must be running and it must be specified as the current warehouse for the
session in which the query/statement is submitted.

A Snowflake session can only have one current warehouse at a time. The current warehouse for the session can be specified or changed at any
time through the [USE WAREHOUSE](../sql-reference/sql/use-warehouse) SQL command or the [WarehouseResource.use\_warehouse](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseResource#snowflake.core.warehouse.WarehouseResource.use_warehouse) Python API.

Once a running warehouse has been set as the current warehouse for the session, queries and DML statements submitted within the session are
processed by the warehouse. In the Query History and Workspaces pages in Snowsight, you can view the warehouse used to
process each query/statement.

Note

Some Snowsight features require a warehouse to run SQL queries for retrieving data, such as Task Run History or
Data Preview for a table. An X-Small warehouse is recommended and generally sufficient for most of these queries. For information,
see [Warehouse considerations](warehouses-considerations).

## Delegating warehouse management[¶](#delegating-warehouse-management "Link to this heading")

By default, the ACCOUNTADMIN role is granted the ability to alter, suspend, describe, and perform other operations on all
warehouses in the account.

If you need to delegate these abilities to a custom role in your account, you can grant the MANAGE WAREHOUSES privilege to that role.
Granting the MANAGE WAREHOUSES privilege is equivalent to granting the
MODIFY, MONITOR, and OPERATE privileges on all warehouses in the account.

The following examples demonstrate how you can delegate the ability to manage warehouses to a custom role named
`manage_wh_role`. The example uses the `manage_wh_role` to make changes to the warehouse `test_wh`, which is owned by a
different role (`create_wh_role`).

Create a new role that will create and own a new warehouse, and grant the CREATE WAREHOUSE privilege to that role:

SQLPython

Using the [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege) command:

```
CREATE ROLE create_wh_role;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE create_wh_role;
GRANT ROLE create_wh_role TO ROLE SYSADMIN;
```

Copy

Using the [RoleResource.grant\_privileges](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.role.RoleResource#snowflake.core.role.RoleResource) API:

```
from snowflake.core.role import Role, Securable

my_role = Role(name="create_wh_role")
my_role_res = root.roles.create(my_role)

my_role_res.grant_privileges(
  privileges=["CREATE WAREHOUSE"], securable_type="ACCOUNT"
)

root.roles['SYSADMIN'].grant_role(role_type="ROLE", role=Securable(name='create_wh_role'))
```

Copy

Create a second role that will manage all warehouses in the account, and grant the MANAGE WAREHOUSES privilege to that role:

SQLPython

```
CREATE ROLE manage_wh_role;
GRANT MANAGE WAREHOUSES ON ACCOUNT TO ROLE manage_wh_role;
GRANT ROLE manage_wh_role TO ROLE SYSADMIN;
```

Copy

```
from snowflake.core.role import Role, Securable

my_role = Role(name="manage_wh_role")
my_role_res = root.roles.create(my_role)

my_role_res.grant_privileges(
  privileges=["MANAGE WAREHOUSES"], securable_type="ACCOUNT"
)

root.roles['SYSADMIN'].grant_role(role_type="ROLE", role=Securable(name='manage_wh_role'))
```

Copy

Using the `create_wh_role` role, create a new warehouse:

SQLPython

```
USE ROLE create_wh_role;
CREATE OR REPLACE WAREHOUSE test_wh
    WITH WAREHOUSE_SIZE= XSMALL;
```

Copy

```
from snowflake.core import CreateMode
from snowflake.core.warehouse import Warehouse

root.session.use_role("create_wh_role")

my_wh = Warehouse(
  name="test_wh",
  warehouse_size="XSMALL"
)
root.warehouses.create(my_wh, mode=CreateMode.or_replace)
```

Copy

Change the current role to `manage_wh_role`:

SQLPython

```
USE ROLE manage_wh_role;
```

Copy

```
root.session.use_role("manage_wh_role")
```

Copy

Although the `manage_wh_role` does not own the `test_wh`, that role does have the MANAGE WAREHOUSES privilege, which means
that you can:

* Suspend and resume the warehouse:

  SQLPython

  ```
  ALTER WAREHOUSE test_wh SUSPEND;
  ALTER WAREHOUSE test_wh RESUME;
  ```

  Copy

  ```
  my_wh_res = root.warehouses["test_wh"]
  my_wh_res.suspend()
  my_wh_res.resume()
  ```

  Copy
* Change the size of the warehouse:

  SQLPython

  ```
  ALTER WAREHOUSE test_wh SET WAREHOUSE_SIZE = SMALL;
  ```

  Copy

  ```
  my_wh = root.warehouses["test_wh"].fetch()
  my_wh.warehouse_size = "SMALL"
  root.warehouses["test_wh"].create_or_alter(my_wh)
  ```

  Copy
* Describe the warehouse:

  SQLPython

  ```
  DESC WAREHOUSE test_wh;
  ```

  Copy

  ```
  my_wh = root.warehouses["test_wh"].fetch()
  print(my_wh.to_dict())
  ```

  Copy

## Review Warehouse Details in Snowsight[¶](#review-warehouse-details-in-sf-web-interface "Link to this heading")

You must use the ACCOUNTADMIN role, or a role granted the relevant [warehouse privileges](security-access-control-privileges.html#label-warehouse-privileges).

To review warehouses and manage warehouse details in Snowsight, complete the following steps:

1. Sign in to [Snowsight](ui-snowsight-gs.html#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select Compute » Warehouses.

You can then review the table of warehouses, search for warehouses, or filter the list of warehouses by status or size.

By default, you can see the following information about each warehouse:

* Name
* Status, such as Started, Resuming, or Suspended.
* Size
* Clusters, indicated by a bar in the column. You can hover over the value to see how many clusters are active.
* Running, for details on how many SQL statements are being executed by the warehouse.
* Queued, for details on how many SQL statements are queued for the warehouse.
* Owner, or the owning role for the warehouse.
* Resumed, to see how long ago the warehouse was resumed. Hover over the value to see the exact date and timestamp in your local time zone.

You can also add columns to see additional details for each warehouse in the table:

* QAS (Scale Factor), to see the scale factor of the warehouse used by Query Acceleration Service (QAS).
  See [Using the Query Acceleration Service (QAS)](query-acceleration-service).
* Scaling Policy, to see the scaling policy defined for the warehouse. See [Setting the scaling policy for a multi-cluster warehouse](warehouses-multicluster.html#label-mcw-scaling-policies).
* Auto Resume, to see whether auto-resume is set up for the warehouse.
* Auto Suspend, to see the time period before auto-suspend occurs for the warehouse.
* Created, to see when the warehouse was created. Hover over the value to see the exact date and timestamp in your local time zone.

When you select a warehouse in the Warehouses table, you can see more details:

* The Warehouse Activity section provides a graph of warehouse load over a period of time, which can help you understand why a
  query might be running slowly. See [Monitoring warehouse load](warehouses-load-monitoring) for more details.
* The Details section provides additional information about your warehouse, including:

  + The status of the warehouse.
  + The size of the warehouse.
  + Maximum and minimum number of clusters the warehouse can use.
  + The scaling policy.
  + The number of tasks that are running and queued.
  + The period of no activity before the warehouse is automatically suspended.
  + If the warehouse is suspended, whether to automatically resume the warehouse when needed.
  + The last time the warehouse resumed operation.
* You can use the Privileges section to view, grant, and revoke privileges on the warehouse.

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

1. [Creating a warehouse](#creating-a-warehouse)
2. [Starting or resuming a warehouse](#starting-or-resuming-a-warehouse)
3. [Suspending a warehouse](#suspending-a-warehouse)
4. [Resizing a warehouse](#resizing-a-warehouse)
5. [Using a warehouse](#using-a-warehouse)
6. [Delegating warehouse management](#delegating-warehouse-management)
7. [Review Warehouse Details in Snowsight](#review-warehouse-details-in-sf-web-interface)

Related content

1. [Understanding compute cost](/user-guide/cost-understanding-compute)
2. [Working with resource monitors](/user-guide/resource-monitors)
3. [Managing Snowflake virtual warehouses with Python](/user-guide/../developer-guide/snowflake-python-api/snowflake-python-managing-warehouses)