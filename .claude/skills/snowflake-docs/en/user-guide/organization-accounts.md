---
auto_generated: true
description: Enterprise Edition Feature
last_scraped: '2026-01-14T16:57:50.199548+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/organization-accounts
title: Organization accounts | Snowflake Documentation
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

    * Organizations
    * [Introduction](organizations.md)
    * [Organization administrators](organization-administrators.md)
    * [Organization account](organization-accounts.md)

      + [Premium views](organization-accounts-premium-views.md)
    * [Organization users](organization-users.md)
    * [Managing accounts](organizations-manage-accounts.md)
    * Accounts
    * [Connecting to your accounts](organizations-connect.md)
    * [Account identifiers](admin-account-identifier.md)
    * [Trial accounts](admin-trial-account.md)
    * [Parameter management](admin-account-management.md)
    * [User management](admin-user-management.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Organizations & Accounts](../guides/overview-manage.md)Organization account

# Organization accounts[¶](#organization-accounts "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The *organization account* is a special type of account that organization administrators use to perform tasks that affect the entire
organization. For example, administrators use the organization account to do the following:

* View organization-level data collected from all accounts in the organization, including the query history from each account.
* Manage organization-level objects — for example, organization users — for all accounts, or a subset of accounts, in an organization.
* Enable Snowflake Marketplace terms for the entire organization.
* Manage the lifecycle of accounts in an organization, including creating and deleting accounts.
* Enable replication for an account.

There is only one organization account for an organization.

## Features available in the organization account[¶](#features-available-in-the-organization-account "Link to this heading")

This section describes features that are available from the organization account.

See the following sections for more information about each feature:

* [Premium views](#label-organization-accounts-premium-views)
* [Organization users and user groups](#label-organization-users-and-user-groups)

### Premium views[¶](#premium-views "Link to this heading")

The ORGANIZATION\_USAGE schema in the organization account contains views that are not available in the ORGANIZATION\_USAGE schema of a
regular account. These additional views are called *premium views*, which are available by default when you create the organization account.
These premium views provide organization-level data that isn’t otherwise available in a single view. For example, you can query the
TAG\_REFERENCES premium view to learn how tags are used throughout the organization, not just in a specific account.

For more information, including costs associated with premium views, see [Premium views in the organization account](organization-accounts-premium-views).

### Organization users and user groups[¶](#organization-users-and-user-groups "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Organizations with more than one account sometimes need someone to manage a user or role in multiple accounts. If you don’t want to create
a separate user or role in each account, then you can create an organization user and organization user group in the organization account.

For more information, see [Organization users](organization-users).

## Compliance considerations for hybrid organizations[¶](#compliance-considerations-for-hybrid-organizations "Link to this heading")

An organization can have accounts in both regulated regions and non-regulated regions. For example, an organization can have one account in
a [U.S. SnowGov Region](intro-regions.html#label-intro-regions-snowgov-regions) and another in a [commercial region](intro-regions.html#label-na-general-regions).
These organizations are called *hybrid organizations*.

Features associated with an organization account might result in [metadata](../sql-reference/metadata) moving from one region to another.
For example, [premium views](organization-accounts-premium-views) might move associated metadata from a regular account’s
region to the region of the organization account. Metadata associated with an organization-level object — for example, an
[organization user](organization-users) — might move from the region of the organization account to the region of an
account that imports the object. For hybrid organizations, this means that metadata might move between a regulated region and a non-regulated
region.

If you have a hybrid organization, Snowflake recommends the following actions:

* Create your organization account in the regulated region.
* Don’t define an organization-level object with sensitive or regulated data.

Compliance standards, such as [FedRAMP](cert-fedramp), and support for different regulated workloads, such as
[ITAR](cert-itar), might be different or unavailable outside of your U.S. SnowGov Region. Consider your compliance
requirements before choosing to move or share data between Snowflake regions.

## About administrator roles and assignable privileges[¶](#about-administrator-roles-and-assignable-privileges "Link to this heading")

Organization administrators use the GLOBALORGADMIN role in the organization account to perform all organization-level tasks, including
administration of the organization account itself.

Note

Before the introduction of the organization account, organization administrators used the ORGADMIN role in an ORGADMIN-enabled account to
perform organization-level tasks. Using the ORGADMIN role in an ORGADMIN-enabled account is being phased out. Use the GLOBALORGADMIN role
in the organization account to perform organization-level tasks.

Snowflake will send a notification email to customers at least three months prior to phasing out the ORGADMIN role.

The GLOBALORGADMIN role can assign privileges to other roles to let other users perform organization-level tasks. In the organization
account, the GLOBALORGADMIN role can assign the following privileges:

* APPLY TAG
* MANAGE ACCOUNTS
* MANAGE LISTING AUTO FULFILLMENT
* MANAGE ORGANIZATION CONTACTS
* MANAGE ORGANIZATION TERMS
* PURCHASE DATA EXCHANGE LISTING

These privileges are set on the account level. For example, to assign the MANAGE ACCOUNTS privilege to the role `custom_role`, execute the
following:

```
USE ROLE GLOBALORGADMIN;

GRANT MANAGE ACCOUNTS ON ACCOUNT TO ROLE custom_role;
```

Copy

For more information about these privileges, see [Access control privileges](security-access-control-privileges).

## Create the organization account[¶](#create-the-organization-account "Link to this heading")

Before create the organization account, consider the following details:

* If your organization includes an account in a [U.S. SnowGov Region](intro-regions.html#label-intro-regions-snowgov-regions), Snowflake recommends
  creating the organization account in this regulated region. For more information about the implication of having an organization with
  both regulated and non-regulated accounts, see [Compliance considerations for hybrid organizations](#label-orgs-hybrid-considerations).
* Creating the organization account results in the ORGANIZATION\_USAGE schema being populated with data, which
  [incurs additional costs](organization-accounts-premium-views.html#label-org-account-views-cost) for your organization.
* You can’t convert an existing ORGADMIN enabled account to be the organization account.

To create the organization account:

1. Choose an existing account from which you will create the organization account. This existing account must have the
   [ORGADMIN role enabled](organization-administrators.html#label-enabling-orgadmin-role-for-account).
2. Sign in to the account you are using to create the organization account.
3. Switch to the ORGADMIN role. For example:

   ```
   USE ROLE ORGADMIN;
   ```

   Copy
4. Execute the [CREATE ORGANIZATION ACCOUNT](../sql-reference/sql/create-organization-account) command. For example:

   ```
   CREATE ORGANIZATION ACCOUNT myorgaccount
       ADMIN_NAME = admin
       ADMIN_PASSWORD = 'TestPassword1'
       EMAIL = 'myemail@myorg.org'
       MUST_CHANGE_PASSWORD = true
       EDITION = enterprise;
   ```

   Copy

Note

Snowflake does not support custom account locators for organization accounts. For alternatives, contact your Snowflake representative.

## Delete the organization account[¶](#delete-the-organization-account "Link to this heading")

If you want to drop the organization account in your multi-account organization, then contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Note

New functionality in Snowflake that includes organization-level administrative tasks will require an organization account. If you are
concerned about the costs associated with [premium views](organization-accounts-premium-views), contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request that they be disabled instead of deleting the account.

## Move the organization account to a different region[¶](#move-the-organization-account-to-a-different-region "Link to this heading")

You can move an organization account between regions as long as those regions are in either the PUBLIC region group or a VPS region group.

Snowflake uses replication groups to move objects from the organization account in the source region to the organization account in the new
region. As a result, only objects that can be replicated are moved with the organization account and there are replication costs associated
with the move. For a list of objects that can be moved with the organization account, see [Replicated objects](account-replication-intro.html#label-replicated-objects).

Note

[Organization profiles](collaboration/organization-profiles/org-profiles-create-manage) move with the organization
account to the new region.

Moving the organization account to a different region is a two-step process:

1. Call the [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](../sql-reference/functions/system_initiate_move_organization_account) function from the organization account to start
   the process of moving it. Snowflake begins replicating objects to the new region.

   The function accepts a temporary account name, the new region, and a list of objects to move as its arguments. For example:

   ```
   CALL SYSTEM$INITIATE_MOVE_ORGANIZATION_ACCOUNT(
     'MY_TEMP_NAME',
     'aws_us_west_2',
     'ALL');
   ```

   Copy
2. When you have verified that the data in the organization account has been successfully replicated in the new region, call the
   [SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT](../sql-reference/functions/system_commit_move_organization_account) function to finalize the move, specifying a grace period
   after which the original organization account is deleted.

   For example, the following call finalizes the move, and specifies that the original organization account in the source region will
   be deleted after 14 days.

   ```
   CALL SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT(14);
   ```

   Copy

At any point, you can view the status of an attempt to move an organization account by calling the
[SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS](../sql-reference/functions/system_show_move_organization_account_status) function.

Note

When an organization account is moved, the views in the ORGANIZATION\_USAGE schema must be repopulated with data, a process that can take up
to one week.

## Limitations[¶](#limitations "Link to this heading")

Replication isn’t fully supported for the organization account; some objects can’t be replicated to or from the organization account.

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

1. [Features available in the organization account](#features-available-in-the-organization-account)
2. [Compliance considerations for hybrid organizations](#compliance-considerations-for-hybrid-organizations)
3. [About administrator roles and assignable privileges](#about-administrator-roles-and-assignable-privileges)
4. [Create the organization account](#create-the-organization-account)
5. [Delete the organization account](#delete-the-organization-account)
6. [Move the organization account to a different region](#move-the-organization-account-to-a-different-region)
7. [Limitations](#limitations)