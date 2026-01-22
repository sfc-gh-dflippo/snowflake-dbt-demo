---
auto_generated: true
description: Standard & Business Critical Feature
last_scraped: '2026-01-14T16:57:15.583931+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/account-replication-considerations
title: Replication considerations | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
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

    * Replication
    * [Introduction](account-replication-intro.md)
    * [Considerations](account-replication-considerations.md)
    * [Configuration and usage](account-replication-config.md)
    * [Security integrations and network policy replication](account-replication-security-integrations.md)
    * [Apache Iceberg table replication](tables-iceberg-replication.md)
    * [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history.md)
    * [Git repository replication](account-replication-git-repositories.md)
    * [Understanding cost](account-replication-cost.md)
    * Failover
    * [Account failover](account-replication-failover-failback.md)
    * Monitoring
    * [Monitoring replication and failover](account-replication-monitor.md)
    * [Error notifications for replication and failover groups](account-replication-error-notifications.md)
    * Client Redirect
    * [Overview and usage](client-redirect.md)
    * Data Recovery
    * [Backups](backups.md)
    * [Time Travel](data-time-travel.md)
    * [Fail-safe](data-failsafe.md)
    * [Storage costs for historical data](data-cdp-storage-costs.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Business continuity & data recovery](replication-intro.md)Considerations

# Replication considerations[¶](#replication-considerations "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical Feature](intro-editions)

* Database and share replication are available to all accounts.
* Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes the behavior of certain Snowflake features in secondary databases and objects when replicated with
[replication or failover groups](account-replication-intro.html#label-replication-and-failover-groups) or
[database replication](db-replication-config), and provides general guidance for working with replicated
objects and data.

If you have previously enabled database replication for individual databases using the ALTER DATABASE … ENABLE REPLICATION TO ACCOUNTS
command, see [Database replication considerations](database-replication-considerations) for additional considerations specific to database replication.

## Replication group and failover group constraints[¶](#replication-group-and-failover-group-constraints "Link to this heading")

The following sections explain the constraints around adding account objects, databases, and shares to replication and failover groups.

### Database and share objects[¶](#database-and-share-objects "Link to this heading")

The following constraints apply to database and share objects:

* An object can only be in one failover group.
* An object can be in multiple replication groups as long as each group is replicated to a *different* target account.
* An object cannot be in both a failover group and a replication group.
* Secondary (replica) objects cannot be added to a primary replication or failover group.

You can only replicate outbound shares. Replication of [inbound shares](data-share-consumers) (shares from providers)
is not supported.

### Account objects[¶](#account-objects "Link to this heading")

An account can only have one replication or failover group that contains objects other than databases or shares.

## Replication privileges[¶](#replication-privileges "Link to this heading")

This section describes the replication privileges that are available to be granted to roles to specify the operations users can perform on
replication and failover group objects in the system. For the syntax of the GRANT command, see
[GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege).

Note

For [database replication](db-replication-config), only a user with the ACCOUNTADMIN role can enable
and manage database replication and failover. For additional information on required privileges for database replication,
see the [required privileges table](db-replication-config.html#label-db-replication-required-privileges) in [Step 6. Refreshing a secondary database on a schedule](db-replication-config.html#label-refreshing-secondary-db-on-schedule).

| Privilege | Object | Usage | Notes |
| --- | --- | --- | --- |
| OWNERSHIP | Replication Group  Failover Group | Grants the ability to delete, alter, and grant or revoke access to an object. | Can be granted by:  The ACCOUNTADMIN role or  A role that has the MANAGE GRANTS privilege or  A role that has the OWNERSHIP privilege on the group. |
| CREATE REPLICATION GROUP | Account | Grants the ability to create a replication group. | Must be granted by the ACCOUNTADMIN role. |
| CREATE FAILOVER GROUP | Account | Grants the ability to create a failover group. | Must be granted by the ACCOUNTADMIN role. |
| FAILOVER | Failover Group | Grants the ability to promote a secondary failover group to serve as primary failover group. | Can be granted or revoked by a role with the OWNERSHIP privilege on the group. |
| REPLICATE | Replication Group  Failover Group | Grants the ability to refresh a secondary group. | Can be granted or revoked by a role with the OWNERSHIP privilege on the group. |
| MODIFY | Replication Group  Failover Group | Grants the ability to change the settings or properties of an object. | Can be granted or revoked by a role with the OWNERSHIP privilege on the group. |
| MONITOR | Replication Group  Failover Group | Grants the ability to view details within an object. | Can be granted or revoked by a role with the OWNERSHIP privilege on the group. |

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](security-access-control-overview).

## Replication and references across replication groups[¶](#replication-and-references-across-replication-groups "Link to this heading")

Objects in a replication (or failover) group that have dangling references (i.e. references to objects in another replication or failover
group) might successfully replicate to a target account in some circumstances. If the replication operation results in behavior in the
target account consistent with behavior that can occur in the source account, replication succeeds.

For example, if a column in a table in failover group `fg_a` references a sequence in failover group `fg_b`, replication of both
groups succeeds. If `fg_a` is replicated before `fg_b`, insert operations (after failover) on the table that references the
sequence fails if `fg_b` was not replicated. This behavior can occur in a source account. If a sequence is dropped in a
source account, insert operations on a table with a column referencing the dropped sequence fails.

When the dangling reference is a security policy that protects data, the replication (or failover) group with the security policy
must be replicated before any replication group that contains objects that reference the policy is replicated.

Attention

Making updates to security policies that protect data in separate replication or failover groups may result in inconsistencies
and should be done with care.

For database objects, you can view [object dependencies](object-dependencies) in the Account Usage
[OBJECT\_DEPENDENCIES view](../sql-reference/account-usage/object_dependencies).

### Session policies and secondary roles[¶](#session-policies-and-secondary-roles "Link to this heading")

For details, see [Session policies with secondary roles](#label-account-replication-session-policy-secondary-roles)

### Dangling references and network policies[¶](#dangling-references-and-network-policies "Link to this heading")

Dangling references in network policies can cause replication to fail with the following error message:

```
Dangling references in the snapshot. Correct the errors before refreshing again.
The following references are missing (referred entity <- [referring entities])
```

To avoid dangling references, specify the following object types in the `OBJECT_TYPES` list when executing the CREATE or
ALTER command for the replication or failover group:

* If a network policy uses a network rule, include the database that contains the schema where the network rule was created.
* If a network policy is associated with the account, include `NETWORK POLICIES` and `ACCOUNT PARAMETERS` in the
  `OBJECT_TYPES` list.
* If a network policy is associated with a user, include `NETWORK POLICIES` and `USERS` in the `OBJECT_TYPES` list.

For more details, see [Replicating network policies](account-replication-security-integrations.html#label-account-replication-network-policy).

### Dangling references and packages policies[¶](#dangling-references-and-packages-policies "Link to this heading")

If there is a [packages policy](../developer-guide/udf/python/packages-policy) set on the account, the following dangling references
error occurs during the refresh operation for a replication or failover group that contains account objects:

```
003131 (55000): Dangling references in the snapshot. Correct the errors before refreshing again.
The following references are missing (referred entity <- [referring entities]):
POLICY '<policy_db>.<policy_schema>.<packages_policy_name>' <- [ACCOUNT '<account_locator>']
```

To avoid dangling references, replicate the database that contains the packages policy to the target account. The database containing the
policy can be in the same or different replication or failover group.

### Dangling references and secrets[¶](#dangling-references-and-secrets "Link to this heading")

For details, see [Replication and secrets](#label-account-replication-considerations-secrets).

### Dangling references and streams[¶](#dangling-references-and-streams "Link to this heading")

Dangling references for streams cause replication to fail with the following error message:

```
Primary database: the source object ''<object_name>'' for this stream ''<stream_name>'' is not included in the replication group.
Stream replication does not support replication across databases in different replication groups. Please see Streams Documentation
https://docs.snowflake.com/en/user-guide/account-replication-considerations#replication-and-streams for options.
```

To avoid dangling reference errors:

* The primary database must include both the stream and its base object or
* The database that contains the stream and the database that contains the base object referenced by the stream must be included in the
  same replication or failover group.

## Replication and read-only secondary objects[¶](#replication-and-read-only-secondary-objects "Link to this heading")

All secondary objects in a target account, including secondary databases and shares, are read-only. Changes to replicated objects or object types
cannot be made locally in a target account. For example, if the `USERS` object type is replicated from a source
account to a target account, new users cannot be created or modified in the target account.

New, local databases and shares *can* be created and modified in a target account. If `ROLES` are also replicated
to the target account, new roles cannot be created or modified in that target account. Therefore, privileges cannot be granted to (or revoked from)
a
role on a secondary object in the target account. However, privileges *can* be granted to (or revoked from) a secondary role on local
objects (for example, databases, shares, or replication or failover groups) created in the target account.

## Replication and objects in target accounts[¶](#replication-and-objects-in-target-accounts "Link to this heading")

If you created account objects, for example, users and roles, in your target account by *any means other than via replication* (for example,
using scripts), these users and roles have no global identifier by default. When a target account is refreshed from the source account, the
refresh operation **drops** any account objects of the types in the `OBJECT_TYPES` list in the target account that have no
global identifier.

Note

The initial refresh operation to replicate USERS or ROLES might result in an error. This is to help prevent accidental deletion of
data and metadata associated with users and roles. For more information about the circumstances that determine whether these
object types are dropped or the refresh operation fails, see [Initial replication of users and roles](account-replication-config.html#label-initial-replication-users-roles).

To avoid dropping these objects, see [Apply global IDs to objects created by scripts in target accounts](account-replication-config.html#label-apply-global-ids-to-objects).

### Objects recreated in target accounts[¶](#objects-recreated-in-target-accounts "Link to this heading")

If an existing object in the source account is replaced using a CREATE OR REPLACE statement, the existing object is dropped, and then
a new object with the same name is created in a single transaction. For example, if you execute a CREATE OR REPLACE statement for an
existing table `t1`, table `t1` is dropped, and then a new table `t1` is created. For more information, see the
[usage notes for CREATE TABLE](../sql-reference/sql/create-table.html#label-create-or-replace-table-notes).

When objects are replaced on the target account, the DROP and CREATE statements do not execute atomically during a refresh operation.
This means the object might disappear briefly from the target account while it is being recreated as a new object.

## Replication and security policies[¶](#replication-and-security-policies "Link to this heading")

The database containing a security policy and the references (i.e. assignments) can be replicated using replication and failover
groups. Security policies include:

* [Aggregation policies](aggregation-policies)
* [Authentication policies](authentication-policies)
* [Masking policies](security-column-intro)
* [Password policies](password-authentication.html#label-password-policies)
* [Privacy policies](diff-privacy/differential-privacy-admin-privacy-policies)
* [Projection policies](projection-policies)
* [Row access policies](security-row-intro)
* [Session policies](session-policies), including
  [session policies with secondary roles](#label-account-replication-session-policy-secondary-roles)
* [Tag-based masking policies](tag-based-masking-policies)

If you are using [database replication](db-replication-intro),
see [Database replication and security objects](database-replication-considerations.html#label-db-replication-considerations-security-policies).

### Authentication, password, & session policies[¶](#authentication-password-session-policies "Link to this heading")

Authentication, password, and session policy references for users are replicated when specifying the database containing policy
(`ALLOWED_DATABASES = policy_db`) and `USERS` in a replication group or failover group.

If either the policy database or users have already been replicated to a target account, update the replication or failover group
in the source account to include the databases and object types required to successfully replicate the policy. Then execute a refresh
operation to update the target account.

If user-level policies are not in use, `USERS` do not need to be included in the replication or failover group.

Note

The policy must be in the same account as the account-level policy assignment and the user-level policy assignment.

If you have a security policy set on the account or a user in the account and you do not update the
replication or failover group to include the `policy_db` containing the policy and `USERS`, a dangling reference occurs in
the target account. In this case, a dangling reference means that Snowflake cannot locate the policy in the target account because the
fully-qualified name of the policy points to the database in the source account. Consequently, the target account or users in the target
account are not required to comply with the security policy.

To successfully replicate a security policy, verify the replication or failover group includes the object types and databases required
to prevent a dangling reference.

### Privacy policies[¶](#privacy-policies "Link to this heading")

Consider the following when replicating privacy policies and privacy-protected tables and views associated with
[differential privacy](diff-privacy/differential-privacy-overview):

* If a privacy policy is assigned to a table or view in the source account, the policy needs to be replicated in the target account.
* Cumulative privacy loss for a privacy budget is not replicated.
* Cumulative privacy loss in the target and source accounts are tracked separately.
* Administrators in the target account cannot adjust the replicated privacy budget. The privacy budget is synced with the one in the source
  account.
* If an analyst has access to the privacy-protected table or view in both the source account and the target account, they can incur twice
  the amount of privacy loss before reaching the privacy budget’s limit.
* Privacy domains set on the columns are also replicated.

### Session policies with secondary roles[¶](#session-policies-with-secondary-roles "Link to this heading")

If you are using session policies with secondary roles, you must specify the policy database
in the same replication group that contains the roles. For example:

```
CREATE REPLICATION GROUP myrg
  OBJECT_TYPES = DATABASES, ROLES, USERS
  ALLOWED_DATABASES = session_policy_db
  ALLOWED_ACCOUNTS = myorg.myaccount
  REPLICATION_SCHEDULE = '10 MINUTE';
```

Copy

If you specify the session policy database that references secondary roles in a different replication or failover group (`rg2`) than the
replication or failover group that contains account-level objects (`myrg`) and you replicate or fail over `rg2` first, a
[dangling reference](#label-references-across-replication-groups) occurs. An error message tells you to place the session policy
database in the replication or failover group that contains the roles. This behavior occurs when the session policy is set on the account
or users.

If the session policy and account level objects are in different replication groups, and the session policy is not set on the account or
users, you can replicate and refresh the target account. Be sure to refresh for the replication group that contains the account level
objects first.

If you refresh the target account after replicating or failing over the session policy with secondary roles and role objects, the target
account reflects the session policy and secondary roles behavior in the source account.

Additionally, when you refresh the database in the target account and the database contains a session policy that references secondary
roles, `ALLOWED_SECONDARY_ROLES` always evaluates to `[ALL]`.

## Replication and secrets[¶](#replication-and-secrets "Link to this heading")

You can only replicate the secret using a replication or failover group. Specify the database that contains the secret, the database that
contains UDFs or procedures that reference the secret, and the integrations that reference the secret in a single replication or failover
group.

If you have the database that contains the secret in one replication or failover group and the integration that references the secret in a
different replication or failover group, then:

* If you replicate the integration first and then the secret, the operation is successful: all objects are replicated and there are no
  dangling references.
* If you replicate the secret before the integration and the secret does not already exist in the target account, a “placeholder secret” is
  added in the target account to prevent a dangling reference. Snowflake maps the placeholder secret to the integration.

  After you replicate the group that contains the integration, on the next refresh operation for the group that contains the secret,
  Snowflake updates the target account to replace the placeholder secret with the secret that is referenced in the integration.
* If you replicate the secret and do not replicate the integration from `account1` to `account2`, the integration doesn’t work in the
  target account (`account2`) because there is no integration to use the secret. Additionally, if you failover and the target account is
  promoted to source account, the integration will not work.

  When you decide to failover to make `account1` as the source account, the secret and integration references match and the placeholder
  secret is not used. This allows you to use the security integration and the secret that contains the credentials because the objects can
  reference each other.

## Replication and cloning[¶](#replication-and-cloning "Link to this heading")

Historically [Cloned objects](object-clone) were replicated physically rather than logically to secondary databases. That is,
cloned tables in a standard database don’t contribute to the overall data storage unless or until DML operations on the clone
add to or modify existing data. However, when a cloned table is replicated to a secondary database, the physical data is also replicated,
increasing the data storage usage for your account.

A logically replicated cloned table shares the micro-partitions of the original table it was cloned from,
reducing the physical storage of the secondary table in the target account.

If the original table and cloned table are included in the same replication or failover group, the cloned table can be replicated
logically to the target account.

### Logical replication of clones[¶](#logical-replication-of-clones "Link to this heading")

If the original and cloned table are included in the same replication or failover group, the cloned table can be replicated
logically to the target account.

For example, if table `t2` in database `db2` is a clone of table `t1` in database `db1`, and both databases are included
in replication group `rg1`, then table `t2` is created as a logical clone in the target account.

A cloned object can be cloned to create additional clones of the original object. The original object and the cloned objects are part
of the same [clone group](tables-storage-considerations.html#label-owned-storage-vs-referenced-storage). For example, if table `t3` in database `db3` is created as a clone of `t2`, it is in the same clone group
as the original table `t1` and the cloned table `t2`.

If database `db3` is later added to the replication group `rg1`, table `t3` is created in the target account as a logical clone of
table `t1`.

#### Considerations[¶](#considerations "Link to this heading")

* Tables that are in the same clone group in the source account might not be in the same clone group in the target account.
* The original table and its cloned table must be in the same replication or failover group.
* In some cases, not all micro-partitions of the clone group can be shared with the cloned table. This can result in additional storage usage
  for the cloned table in the target account.

#### Example[¶](#example "Link to this heading")

Table `t2` in database `db2` is a clone of table `t1` in database `db1`. Include both databases in
replication group `myrg` to logically replicate `t2` to the target account:

```
CREATE REPLICATION GROUP myrg
    OBJECT_TYPES = DATABASES
    ALLOWED_DATABASES = db1, db2
    ALLOWED_ACCOUNTS = myorg.myaccount2
    REPLICATION_SCHEDULE = '10 MINUTE';
```

Copy

## Replication and automatic clustering[¶](#replication-and-automatic-clustering "Link to this heading")

In a primary database, Snowflake monitors clustered tables using [Automatic Clustering](tables-auto-reclustering) and reclusters them as
needed. As part of a refresh operation, clustered tables are replicated to a secondary database with the current sorting of the table
micro-partitions. As such, reclustering is not performed again on the clustered tables in the secondary database, which would be
redundant.

If a secondary database contains clustered tables and the database is promoted to become the primary database, Snowflake begins Automatic
Clustering of the tables in this database while simultaneously suspending the monitoring of clustered tables in the previous primary
database.

See [Replication and Materialized Views](#replication-and-materialized-views) (in this topic) for information about Automatic Clustering for materialized views.

## Replication and large, high-churn tables[¶](#replication-and-large-high-churn-tables "Link to this heading")

When one or more rows of a table are updated or deleted, all of the impacted micro-partitions that store this data in a primary database
are re-created and must be synchronized to secondary databases. For large, high-churn dimension tables, the replication costs can be
significant.

For large, high-churn dimension tables that incur significant replication costs, the following mitigations are available:

* Replicate any primary databases that store such tables at a lower frequency.
* Change your data model to reduce churn.

For more information, see [Managing costs for large, high-churn tables](tables-storage-considerations.html#label-large-high-churn-table-costs).

## Replication and Time Travel[¶](#replication-and-time-travel "Link to this heading")

[Time Travel](data-time-travel) and [Fail-safe](data-failsafe) data is maintained independently for a
secondary database and is not replicated from a primary database. Querying tables and views in a secondary database using Time Travel
can produce different results than when executing the same query in the primary database.

Historical Data:
:   Historical data available to query in a primary database using Time Travel is not replicated to secondary databases.

    For example, suppose data is loaded continuously into a table every 10 minutes using Snowpipe, and a secondary database is refreshed
    every hour. The refresh operation only replicates the latest version of the table. While every hourly version of the table within the
    retention window is available for query using Time Travel, none of the iterative versions within each hour (the individual Snowpipe
    loads) are available.

Data Retention Period:
:   The data retention period for tables in a secondary database begins when the secondary database is refreshed with the DML operations
    (i.e. changing or deleting data) written to tables in the primary database.

    Note

    The data retention period parameter, [DATA\_RETENTION\_TIME\_IN\_DAYS](../sql-reference/parameters.html#label-data-retention-time-in-days), is only replicated to database objects in the secondary
    database, not to the database itself. For more details about parameter replication, see [Parameters](db-replication-intro.html#label-database-replication-parameters).

## Replication and materialized views[¶](#replication-and-materialized-views "Link to this heading")

In a primary database, Snowflake performs automatic background maintenance of materialized views. When a base table changes, all
materialized views defined on the table are updated by a background service that uses compute resources provided by Snowflake. In addition,
if Automatic Clustering is enabled for a materialized view, then the view is monitored and reclustered as necessary in a primary database.

A refresh operation replicates the materialized view definitions to a secondary database; the materialized view data is not
replicated. Automatic background maintenance of materialized views in a secondary database is enabled by default. If Automatic
Clustering is enabled for a materialized view in a primary database, automatic monitoring and reclustering of the materialized view in the
secondary database is also enabled.

Note

The charges for automated background synchronization of materialized views are billed to each account that contains a secondary
database.

## Replication and Apache Iceberg™ tables[¶](#replication-and-iceberg-tm-tables "Link to this heading")

Consider the following points when you use replication for Iceberg tables:

* Snowflake currently supports replication of Snowflake-managed tables only.
* Replicating converted Iceberg tables isn’t supported. Snowflake skips converted tables during refresh operations.
* For replicated tables, you must configure access to a storage location in the *same region* as the target account.
* If you drop or alter a storage location that is used for replication on the primary external volume, refresh operations might fail.
* Secondary tables in the target account are read-only until you promote the target account to serve as the source account.
* Snowflake maintains the [directory hierarchy](tables-iceberg-storage.html#label-tables-iceberg-configure-external-volume-base-location)
  of the primary Iceberg table for the secondary table.
* Replication costs apply for this feature. For more information, see [Understanding replication cost](account-replication-cost).
* For considerations about the account objects for replication and failover groups, see [Account objects](#label-account-objects).

## Replication and dynamic tables[¶](#replication-and-dynamic-tables "Link to this heading")

Dynamic table replication behavior varies based on whether the primary database containing the dynamic table is part
of a replication group or a failover group.

### Dynamic tables and replication groups[¶](#dynamic-tables-and-replication-groups "Link to this heading")

A database that contains a dynamic table can be replicated using a replication group. The source object(s) it depends
on are not required to be in the same replication group.

Replicated objects in each target account are referred to as *secondary* objects and are replicas of the *primary*
objects in the source account. Secondary objects are [read-only](#label-replication-and-secondary-objects) in
the target account. If a secondary replication group is dropped in a target account, the databases that were
included in the group become read/write. However, any dynamic tables included in a replication group remain
read-only even after the secondary group is dropped in the target account. No DML or dynamic table refreshes can
happen on these read-only dynamic tables.

### Dynamic tables and failover groups[¶](#dynamic-tables-and-failover-groups "Link to this heading")

A database that contains a dynamic table can be replicated using a failover group. If a dynamic table references
source objects outside the failover group or database replication, it can still be replicated. After a failover, the
dynamic table resolves source objects using name resolution during refresh. The refresh might succeed or fail,
depending on the state of the source objects. If successful, the dynamic table is reinitialized with the latest data
from the source objects.

Secondary dynamic tables are read-only and do not get refreshed. After a failover occurs and a secondary dynamic
table is promoted to primary dynamic table, the first refresh is a reinitialization followed by incremental
refreshes if the dynamic table is configured for incremental refresh of data.

Note

The reinitialized dynamic table might differ from the original replica because the source objects and dynamic table
are not guaranteed to share the same replication snapshot.

**Example: Refresh failure due to missing source objects**

![Simple diagram of refresh failure due to missing source objects.](../_images/dynamic-tables-failover-group-example-1.png)

If a dynamic table depends on a source table outside the failover group, it cannot refresh after a failover. In the
above diagram, the dynamic table `dt` in the primary account is replicated to the secondary account. `dt`
depends on `source_table`, which is not included in the same failover group as the primary account. After failover,
the refresh in the secondary account fails because `source_table` cannot be resolved.

**Example: Successful refresh when source objects exist in secondary account via separate replication**

![Simple diagram of successful refresh with different failover groups.](../_images/dynamic-tables-failover-group-example-2.png)

In the above diagram, the dynamic table `dt` depends on `source_table`. Both `dt` and `source_table` in the
primary account are replicated to the secondary account through independent failover groups. After replication and
failover, when `dt` is refreshed in the secondary account, the refresh succeeds because `source_table` can be
found through name resolution.

**Example: Successful refresh when source objects exist in secondary account locally**

![Simple diagram of successful refresh with different failover groups.](../_images/dynamic-tables-failover-group-example-3.png)

In the above diagram, the dynamic table `dt` depends on `source_table` and is replicated through a failover group
from the primary account to the secondary account. A `source_table` is created locally in the secondary account.
After failover, when `dt1` is refreshed in the secondary account, the refresh can succeed because `source_table`
can be found through name resolution.

## Replication and Snowpipe Streaming[¶](#replication-and-snowpipe-streaming "Link to this heading")

A table populated by [Snowpipe Streaming](snowpipe-streaming/data-load-snowpipe-streaming-overview) in a primary database is replicated to the secondary database in a target account.

In the primary database, tables are created and rows are inserted through [channels](snowpipe-streaming/data-load-snowpipe-streaming-overview.html#label-replication-snowpipe-channels). [Offset tokens](snowpipe-streaming/data-load-snowpipe-streaming-overview.html#label-replication-snowpipe-offset-tokens) track the ingestion progress. A refresh operation replicates the table object, table data, and the channel offsets associated with the table from the primary database to the secondary database.

* Snowflake Streaming read-only operations to retrieve offsets are available in the source and target accounts:

  + The channel [getLatestCommittedOffsetToken](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestChannel.html#getLatestCommittedOffsetToken()) API
  + [SHOW CHANNELS](../sql-reference/sql/show-channels) command
* Snowflake Streaming write operations are only available in the source account:

  + The client [openChannel](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestClient.html#openChannel(net.snowflake.ingest.streaming.OpenChannelRequest)) API
  + The channel [insertRow](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestChannel.html#insertRow(java.util.Map,java.lang.String)) API
  + The channel [insertRows](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestChannel.html#insertRows(java.lang.Iterable,java.lang.String)) API

### Avoiding data loss[¶](#avoiding-data-loss "Link to this heading")

To avoid data loss in the case of failover, the data retention time for successfully inserted rows in your upstream data source must be
greater than the configured [replication schedule](account-replication-intro.html#label-replication-schedule). If data is inserted into a table in a primary database, and failover occurs before the data can
be replicated to the secondary database, the same data will need to be inserted into the table in the newly promoted primary database.
The following is an example scenario:

1. Table `t1` in primary database `repl_db` is populated with data with Snowpipe Streaming and the Kafka connector.
2. The `offsetToken` is 100 for channel 1 and 100 for channel 2 for `t1` in the *primary* database.
3. A refresh operation completes successfully in the target account.
4. The `offsetToken` is 100 for channel 1 and 100 for channel 2 for the `t1` in the *secondary* database.
5. More rows are inserted into `t1` in the primary database.
6. The `offsetToken` is now 200 for channel 1 and 200 for channel 2 for the `t1` in the *primary* database.
7. A failover occurs before the additional rows and new channel offsets can be replicated to the secondary database.

In this case, there are 100 missing offsets in each channel for table `t1` in the newly promoted primary database. To insert the missing data, see [Reopen active channels for Snowpipe Streaming in newly promoted source account](account-replication-failover-failback.html#label-update-snowpipe-streaming-on-failover).

### Requirements[¶](#requirements "Link to this heading")

Snowpipe Streaming replication support requires the following minimum versions:

* Snowflake Ingest SDK version 1.1.1 and later
* If you are using the Kafka connector: Kafka connector version 1.9.3 and later

The data retention time for successfully inserted rows in your upstream data source must be
greater than the configured replication schedule. If you are using the Kafka connector, ensure your `log.retention` configuration is set with a sufficient buffer.

## Replication and stages[¶](#replication-and-stages "Link to this heading")

The following constraints apply to stage objects:

* Snowflake currently supports stage replication as part of group-based replication (replication and failover groups).
  Stage replication is not supported for database replication.
* You can replicate an external stage. However, the files on an external stage are not replicated.
* You can replicate an internal stage. To replicate the files on an internal stage, you must enable a directory table on the stage.
  Snowflake replicates only the files that are mapped by the directory table.
* When you replicate an internal stage with a directory table, you cannot disable the directory table on the primary or secondary stage.
  The directory table contains critical information about replicated files and files loaded using a COPY statement.
* A refresh operation will fail if the directory table on an internal stage contains a file that is larger than 5GB. To work around this
  limitation, move any files larger than 5GB to a different stage.

  You cannot disable the directory table on a primary or secondary stage, or any stage that has previously been replicated. Follow
  these steps *before* you add the database that contains the stage to a replication or failover group.

  1. [Disable the directory table](../sql-reference/sql/alter-stage.html#label-alter-stage-directory-table-syntax) on the primary stage.
  2. Move the files that are larger than 5GB to another stage that does not have a directory table enabled.
  3. After you move the files to another stage, re-enable the directory table on the primary stage.
* Files on user stages and table stages are not replicated.
* For named external stages that use a storage integration, you must configure the trust relationship for secondary storage integrations
  in your target accounts prior to failover. For more information, see [Configure cloud storage access for secondary storage integrations](account-replication-config.html#label-configure-cloud-storage-access-secondary-storage-integrations).
* If you replicate an external stage with a directory table, and you have configured
  [automated refresh](data-load-dirtables-auto) for the source
  directory table, you must configure automated refresh for the secondary directory table before failover. For more information,
  see [Configure automated refresh for directory tables on secondary stages](account-replication-config.html#label-configure-automated-refresh-secondary-directory-tables).
* A copy command might take longer than expected if the directory table on a replicated stage is not consistent with the
  replicated files on the stage. To make a directory table consistent, refresh it with an
  [ALTER STAGE … REFRESH](../sql-reference/sql/alter-stage) statement.
  To check the consistency status of a directory table, use the [SYSTEM$GET\_DIRECTORY\_TABLE\_STATUS](../sql-reference/functions/system_get_directory_table_status) function.

## Replication and pipes[¶](#replication-and-pipes "Link to this heading")

The following constraints apply to pipe objects:

* Snowflake currently supports pipe replication as part of group-based replication (replication and failover groups).
  Pipe replication is not supported for database replication.
* Snowflake replicates the copy history of a pipe only when the pipe belongs to the same replication group as its target table.
* Replication of notification integrations is not supported.
* Snowflake only replicates load history after the latest table truncate.
* To receive notifications, you must configure a secondary auto-ingest pipe in a target account prior to failover.
  For more information, see [Configure notifications for secondary auto-ingest pipes](account-replication-config.html#label-configure-notifications-secondary-pipes).
* Use the [SYSTEM$PIPE\_STATUS](../sql-reference/functions/system_pipe_status) function to resolve any pipes not in their expected execution state after failover.
* Snowflake doesn’t support replication and failover for Snowpipe with the Kafka connector, but Snowflake does support replication and failover for Snowpipe Streaming with the Kafka connector. For more information, see [Snowpipe Streaming and the Kafka connector](account-replication-failover-failback.html#label-update-snowpipe-streaming-kafka-on-failover).

## Replication of data metric functions (DMFs)[¶](#replication-of-data-metric-functions-dmfs "Link to this heading")

The following behaviors apply to [DMF](data-quality-intro) replication:

Event tables
:   The event table that stores the results of manually calling or scheduling a DMF to run is not replicated because the event table is local
    to your Snowflake account, and Snowflake does not support replicating event tables.

Replication groups
:   When you add the database(s) that contain your DMFs to a replication group, the following occurs in the target account:

    * DMFs are replicated from the source account.
    * Tables or views that the [DMF definition](../sql-reference/sql/create-data-metric-function) specifies, such as with a
      [foreign key reference](../sql-reference/sql/create-data-metric-function.html#label-create-data-metric-function-foreign-key) are replicated from the source account, unless the table
      or view is associated with
      [Cross-Cloud Auto-Fulfillment](../collaboration/provider-listings-auto-fulfillment).
    * Scheduled DMFs in the target account are suspended. The secondary DMFs resume their schedule when you promote the target account to
      source account and the secondary DMFs become primary DMFs.

Failover groups
:   When you replicate the database(s) that contain your DMFs using a failover group, the following occurs in the case of failover:

    * Resumes the schedule of suspended DMFs when you promote the target account to source account.
    * Suspends scheduled DMFs in the target account after you promote a different account to source account.

    If you do not replicate the database that contains the DMF to a target account, the DMF associations to a table or view are
    dropped when the target account is promoted to source account because they are not available in the
    newly promoted source account.

    Tip

    Prior to failing over your account, [check the DMF references](data-quality-monitor) by calling the
    DATA\_METRIC\_FUNCTION\_REFERENCES Information Schema table function to determine the table objects that are associated with a DMF
    before the promotion and refresh operations.

## Replication of stored procedures and user-defined functions (UDFs)[¶](#replication-of-stored-procedures-and-user-defined-functions-udfs "Link to this heading")

Stored procedures and UDFs are replicated from a primary database to secondary databases.

### Stored Procedures and UDFs and Stages[¶](#stored-procedures-and-udfs-and-stages "Link to this heading")

If a stored procedure or UDF depends on files in a stage (for example, if the stored
procedure is defined in Python code that is uploaded from a stage), you must replicate the stage and its files to the secondary
database. For more information about replicating stages, see [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history).

For example, if a primary database has an in-line Python UDF that imports any code that is stored on a stage, the UDF does not work unless
the stage and its imported code are replicated in the secondary database.

### Stored Procedures and UDFs and External Network Access[¶](#stored-procedures-and-udfs-and-external-network-access "Link to this heading")

If a stored procedure or UDF depends on access to an
[external network location](../developer-guide/external-network-access/creating-using-external-network-access), you must
replicate the following objects:

* EXTERNAL ACCESS INTEGRATIONS must be included in the `allowed_integration_types` list for the replication or
  failover group.
* The database that contains the network rule.
* The database that contains the secret that stores the credentials to authenticate with the external network location.
* If the secret object references a security integration, you must include SECURITY INTEGRATIONS in the `allowed_integration_types`
  list for the replication or failover group.

## Replication and storage lifecycle policies[¶](#replication-and-storage-lifecycle-policies "Link to this heading")

Snowflake replicates [storage lifecycle policies](storage-management/storage-lifecycle-policies)
and their associations with tables to target accounts, but doesn’t run the policies.
Snowflake doesn’t replicate archived data in the COOL or COLD tiers.
Archived data in your source account isn’t available in the target account.

After failover to a target account, Snowflake pauses storage lifecycle policy execution in the
original source account. After *failback* to the source account, Snowflake resumes
policy execution.

Snowflake never automatically runs secondary storage lifecycle policies on secondary tables,
even after failover. However, you can use secondary policies in a target account by attaching
them to new tables. For those new tables, Snowflake runs the policies.

## Replication and streams[¶](#replication-and-streams "Link to this heading")

This section describes recommended practices and potential areas of concern when replicating streams in [Replicating databases across multiple accounts](db-replication-config) or [Account Replication and Failover/Failback](account-replication-intro).

### Supported Source Objects for Streams[¶](#supported-source-objects-for-streams "Link to this heading")

Replicated streams can successfully track the change data for tables and views in the same database.

Currently, the following source object types are not supported:

* External tables
* Tables or views in databases separate from the stream databases, unless both the stream database and the database that stores the source object are included in the same
  [replication or failover group](account-replication-intro.html#label-replication-and-failover-groups).
* Tables or views in a shared databases (i.e. databases shared from provider accounts to your account)

Replicating streams on directory tables is supported when you enable [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history).

A database replication or refresh operation fails if the primary database includes a stream with an unsupported source object. The operation also fails if the source object for any stream has been dropped.

Append-only streams are not supported on replicated source objects.

### Avoiding Data Duplication[¶](#avoiding-data-duplication "Link to this heading")

Note

In addition to the scenario described in this section, streams in a secondary database could return duplicate rows the first time they are included in a refresh operation. In this case, *duplicate rows* refers to a single row with multiple METADATA$ACTION column values.

After the initial refresh operation, you should not encounter this specific issue in a secondary database.

Data duplication occurs when DML operations write the same change data from a stream multiple times without a uniqueness check. This can occur if a stream and a destination table for the stream change data are stored in separate databases, and these databases are not replicated and failed over in the same group.

For example, suppose you regularly insert change data from stream `s` into table `dt`. (For this example, the source object for the stream does not matter.) Separate databases store the stream and destination table.

1. At timestamp `t1`, a row is inserted into the source table for stream `s`, creating a new table version. The stream stores the offset for this table version.
2. At timestamp `t2`, the secondary database that stores the stream is refreshed. Replicated stream `s` now stores the offset.
3. At timestamp `t3`, the change data for stream `s` is inserted into table `dt`.
4. At timestamp `t4`, the secondary database that stores stream `s` is failed over.
5. At timestamp `t5`, the change data for stream `s` is inserted again into table `dt`.

To avoid this situation, replicate and fail over together the databases that store streams and their destination tables.

### Stream References in Task WHEN Clause[¶](#stream-references-in-task-when-clause "Link to this heading")

To avoid unexpected behavior when running replicated tasks that reference streams in the `WHEN boolean_expr` clause, we recommend that you either:

* Create the tasks and streams in the same database, or
* If streams are stored in a different database from the tasks that reference them, include both databases in the same [failover group](account-replication-intro.html#label-replication-and-failover-groups).

If a task references a stream in a separate database, and both databases are not included in the same failover group, then the database that contains the task could be failed over without the database that contains the stream. In this scenario, when the task is resumed in the failed over database, it records an error when it attempts to run and cannot find the referenced stream. This issue can be resolved by either failing over the database that contains the stream or recreating the database and stream in the same account as the failed over database that contains the task.

### Stream Staleness[¶](#stream-staleness "Link to this heading")

If a stream in the primary database has become [stale](streams-intro.html#label-streams-staleness), the replicated stream in a secondary database is also stale and cannot be queried or its change data consumed. To resolve this issue, recreate the stream in the primary database (using [CREATE OR REPLACE STREAM](../sql-reference/sql/create-stream)). When the secondary database is refreshed, the replicated stream is readable again.

Note that the offset for a recreated stream is the current table version by default. You can recreate a stream that points to an earlier table version using Time Travel; however, the replicated stream would remain unreadable. For more information, see [Stream Replication and Time Travel](#stream-replication-and-time-travel) (in this topic).

### Stream Replication and Time Travel[¶](#stream-replication-and-time-travel "Link to this heading")

After a primary database is failed over, if a stream in the database uses [Time Travel](data-time-travel) to read a [table version](streams-intro.html#label-streams-table-versioning) for the source object from a point in time before the last refresh timestamp, the replicated stream cannot be queried or the change data consumed. Likewise, querying the change data for a source object from a point in time before the last refresh timestamp using the [CHANGES](../sql-reference/constructs/changes) clause for [SELECT](../sql-reference/sql/select) statements fails with an error.

This is because a refresh operation collapses the table history into a single table version. Iterative table versions created before the refresh operation timestamp are not preserved in the table history for the replicated source objects.

Consider the following example:

[![Stream replication and Time Travel](../_images/replication-streams-time-travel.png)](../_images/replication-streams-time-travel.png)

1. Table `t1` is created in the primary database with change tracking enabled (table version `tv0`). Subsequent DML transactions create table versions `tv1` and `tv2`.
2. A secondary database that contains table `t1` is refreshed. The table version for this replicated table is `tv2`; however, the table history is not replicated.
3. A stream is created in the primary database with its offset set to table version `tv1` using Time Travel.
4. The secondary database is failed over, becoming the primary database.
5. Querying stream `s1` returns an error, because table version `tv1` is not in the table history.

Note that when a subsequent DML transaction on table `t1` iterates the table version to `tv3`, the offset for stream `s1` is advanced. The stream is readable again.

### Avoiding Data Loss[¶](#id2 "Link to this heading")

Data loss can occur when the most recent refresh operation for a secondary database is not completed prior to the failover operation. We recommend refreshing your secondary databases frequently to minimize the risk.

## Replication and tasks[¶](#replication-and-tasks "Link to this heading")

This section describes task replication in [Replicating databases across multiple accounts](db-replication-config) or [Account Replication and Failover/Failback](account-replication-intro).

Note

Database replication does not work for task graphs if the graph is owned by a different role than the role that performs replication.

### Replication Scenarios[¶](#replication-scenarios "Link to this heading")

The following table describes different task scenarios and specifies whether the tasks are replicated or not. Except where noted, the scenarios pertain to both standalone tasks and tasks in a [task graph](tasks-graphs.html#label-task-dag):

| Scenario | Replicated | Notes |
| --- | --- | --- |
| Task was created and either resumed or executed manually (using [EXECUTE TASK](../sql-reference/sql/execute-task)). Resuming or executing a task creates an initial task version. | ✔ |  |
| Task was created but never resumed or executed. | ❌ |  |
| Task was recreated (using [CREATE OR REPLACE TASK](../sql-reference/sql/create-task) but never resumed or executed). | ✔ | The latest version before the task was recreated is replicated.  Resuming or manually executing the task commits a new version. When the database is replicated again, the new, or latest, version is replicated to the secondary database. |
| Task was created and resumed or executed, but subsequently dropped. | ❌ |  |
| Task graph was created and resumed or executed. Subsequently, a task in the task graph was modified, but the task graph’s root task wasn’t resumed or executed again. Examples of modifications include the following:   * Using [ALTER TASK … SET/UNSET/MODIFY](../sql-reference/sql/alter-task) on a root task, child task, or finalizer task. * Using [ALTER TASK … SUSPEND](../sql-reference/sql/alter-task) on a child task or finalizer task. | ✔ | The latest version of the task graph before the task was modified is replicated.  Resuming or manually executing a task commits a new version that includes any changes to the parameters of the tasks within the task graph. Because the new changes were never committed, only the previous version of the task graph is replicated.  Note that if the modified task graph is not resumed within a retention period (currently 30 days), the latest version of the task is dropped. After this period, the task is not replicated to a secondary database unless it’s resumed again. |
| Root task in a task graph was created and resumed or executed, but was subsequently suspended and dropped. | ❌ | The entire task graph is not replicated to a secondary database. |
| Child task in a task graph is created and resumed or executed, but is subsequently suspended and dropped. | ✔ | The latest version of the task graph (before the task was suspended and dropped) is replicated to a secondary database. |

### Resumed or Suspended State of Replicated Tasks[¶](#resumed-or-suspended-state-of-replicated-tasks "Link to this heading")

If all of the following conditions are met, a task is replicated to a secondary database in a resumed state:

* A standalone or root task is in a resumed state in the primary database when the replication or refresh operation begins until the operation is completed. If a task is in a resumed state during only part of this period, it might still be replicated in a resumed state.

  A child task is in a resumed state in the latest version of the task.
* The parent database was replicated to the target account along with role objects in the same, or different, [replication or failover group](account-replication-intro.html#label-replication-and-failover-groups).

  After the roles and database are replicated, you must refresh the objects in the target account by executing either [ALTER REPLICATION GROUP … REFRESH](../sql-reference/sql/alter-replication-group) or [ALTER FAILOVER GROUP … REFRESH](../sql-reference/sql/alter-failover-group), respectively. If you refresh the database by executing [ALTER DATABASE … REFRESH](../sql-reference/sql/alter-database), the state of the tasks in the database is changed to suspended.

  A replication or refresh operation includes the privilege grants for a task that were current when the latest table version was committed. For more information, see [Replicated Tasks and Privilege Grants](#replicated-tasks-and-privilege-grants) (in this topic).

If these conditions are not met, the task is replicated to a secondary database in a suspended state.

Note

Secondary tasks aren’t scheduled until after a failover, regardless of their `state`. For more details, refer to [Task Runs After a Failover](#task-runs-after-a-failover)

### Replicated Tasks and Privilege Grants[¶](#replicated-tasks-and-privilege-grants "Link to this heading")

If the parent database is replicated to a target account along with role objects in the same, or different, replication or failover group, the privileges granted on the tasks in the database are replicated as well.

The following logic determines which task privileges are replicated in a replication or refresh operation:

* If the current task owner (that is, the role that has the OWNERSHIP privilege on a task) is the same role as when the task was resumed last, then all current grants on the task are replicated to the secondary database.
* If the current task owner is not the same role as when the task was resumed last, then only the OWNERSHIP privilege granted to the owner role in the task version is replicated to the secondary database.
* If the current task owner role is not available (for example, a child task is dropped but a new version of the task graph is not committed yet), then only the OWNERSHIP privilege granted to the owner role in the task version is replicated to the secondary database.

### Task Runs After a Failover[¶](#task-runs-after-a-failover "Link to this heading")

After a secondary failover group is promoted to serve as the primary group, any resumed tasks in databases within the failover group are scheduled gradually. The amount of time required to restore normal scheduling of all resumed standalone tasks and task graphs depends on the number of resumed tasks in a database.

## Replication and tags[¶](#replication-and-tags "Link to this heading")

Tags and their assignments can be replicated from a source account to a target account.

Tag assignments cannot be modified in the target account after the initial replication from the source account. For example,
setting a tag on a secondary (i.e. replicated) database is not allowed. To modify tag assignments in the target account, modify
them in the source account and replicate them to the target account.

To successfully replicate tags, ensure that the replication or failover group includes:

* The database containing the tags in the `ALLOWED_DATABASES` property.
* Other account-level objects that have a tag in the `OBJECT_TYPES` property (e.g. `ROLES`, `WAREHOUSES`).

  For more information, see [CREATE REPLICATION GROUP](../sql-reference/sql/create-replication-group) and [CREATE FAILOVER GROUP](../sql-reference/sql/create-failover-group).

## Replication and instances of Snowflake classes[¶](#replication-and-instances-of-snowflake-classes "Link to this heading")

An instance of the [CUSTOM\_CLASSIFIER](../sql-reference/classes/custom_classifier) class is replicated when the database that contains
the instance is replicated. Replication of instances of other Snowflake [classes](../sql-reference-classes.html#label-available-classes) is *not* supported.

## Historical usage data[¶](#historical-usage-data "Link to this heading")

Historical usage data for activity in a primary database is not replicated to secondary databases. Each account has its own query history,
login history, etc.

Historical usage data includes the query data returned by the following [Snowflake Information Schema](../sql-reference/info-schema) table functions or
[Account Usage](../sql-reference/account-usage) views:

* COPY\_HISTORY
* LOGIN\_HISTORY
* QUERY\_HISTORY
* etc.

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

1. [Replication group and failover group constraints](#replication-group-and-failover-group-constraints)
2. [Database and share objects](#database-and-share-objects)
3. [Account objects](#account-objects)
4. [Replication privileges](#replication-privileges)
5. [Replication and references across replication groups](#replication-and-references-across-replication-groups)
6. [Session policies and secondary roles](#session-policies-and-secondary-roles)
7. [Dangling references and network policies](#dangling-references-and-network-policies)
8. [Dangling references and packages policies](#dangling-references-and-packages-policies)
9. [Dangling references and secrets](#dangling-references-and-secrets)
10. [Dangling references and streams](#dangling-references-and-streams)
11. [Replication and read-only secondary objects](#replication-and-read-only-secondary-objects)
12. [Replication and objects in target accounts](#replication-and-objects-in-target-accounts)
13. [Objects recreated in target accounts](#objects-recreated-in-target-accounts)
14. [Replication and security policies](#replication-and-security-policies)
15. [Authentication, password, & session policies](#authentication-password-session-policies)
16. [Privacy policies](#privacy-policies)
17. [Session policies with secondary roles](#session-policies-with-secondary-roles)
18. [Replication and secrets](#replication-and-secrets)
19. [Replication and cloning](#replication-and-cloning)
20. [Logical replication of clones](#logical-replication-of-clones)
21. [Replication and automatic clustering](#replication-and-automatic-clustering)
22. [Replication and large, high-churn tables](#replication-and-large-high-churn-tables)
23. [Replication and Time Travel](#replication-and-time-travel)
24. [Replication and materialized views](#replication-and-materialized-views)
25. [Replication and Apache Iceberg™ tables](#replication-and-iceberg-tm-tables)
26. [Replication and dynamic tables](#replication-and-dynamic-tables)
27. [Dynamic tables and replication groups](#dynamic-tables-and-replication-groups)
28. [Dynamic tables and failover groups](#dynamic-tables-and-failover-groups)
29. [Replication and Snowpipe Streaming](#replication-and-snowpipe-streaming)
30. [Avoiding data loss](#avoiding-data-loss)
31. [Requirements](#requirements)
32. [Replication and stages](#replication-and-stages)
33. [Replication and pipes](#replication-and-pipes)
34. [Replication of data metric functions (DMFs)](#replication-of-data-metric-functions-dmfs)
35. [Replication of stored procedures and user-defined functions (UDFs)](#replication-of-stored-procedures-and-user-defined-functions-udfs)
36. [Stored Procedures and UDFs and Stages](#stored-procedures-and-udfs-and-stages)
37. [Stored Procedures and UDFs and External Network Access](#stored-procedures-and-udfs-and-external-network-access)
38. [Replication and storage lifecycle policies](#replication-and-storage-lifecycle-policies)
39. [Replication and streams](#replication-and-streams)
40. [Supported Source Objects for Streams](#supported-source-objects-for-streams)
41. [Avoiding Data Duplication](#avoiding-data-duplication)
42. [Stream References in Task WHEN Clause](#stream-references-in-task-when-clause)
43. [Stream Staleness](#stream-staleness)
44. [Stream Replication and Time Travel](#stream-replication-and-time-travel)
45. [Avoiding Data Loss](#id2)
46. [Replication and tasks](#replication-and-tasks)
47. [Replication Scenarios](#replication-scenarios)
48. [Resumed or Suspended State of Replicated Tasks](#resumed-or-suspended-state-of-replicated-tasks)
49. [Replicated Tasks and Privilege Grants](#replicated-tasks-and-privilege-grants)
50. [Task Runs After a Failover](#task-runs-after-a-failover)
51. [Replication and tags](#replication-and-tags)
52. [Replication and instances of Snowflake classes](#replication-and-instances-of-snowflake-classes)
53. [Historical usage data](#historical-usage-data)

Related content

1. [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro)
2. [Replicating databases and account objects across multiple accounts](/user-guide/account-replication-config)