---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:57:50.598417+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/organization-users
title: Organization users | Snowflake Documentation
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

[Guides](../guides/README.md)[Organizations & Accounts](../guides/overview-manage.md)Organization users

# Organization users[¶](#organization-users "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

Available to the organization account, which requires Enterprise Edition or higher.

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Organizations with multiple accounts often need to have the same person be a user in more than one of those accounts. To avoid the
repetition of creating a user object for the person in each account separately, the organization administrator can create an
*organization user* in the [organization account](organization-accounts). Each organization user acts as a global user
entity that can be imported into regular accounts by account administrators, simplifying the process of having the same person have a
user object in multiple accounts.

Account administrators don’t add organization users directly to their regular account. Rather, they add *organization user groups*, which
are logical groupings of organization users. When the account administrator imports the organization user group, its organization users are
added to the account.

Note

If you want to create organization users for people who already have a user object in one or more regular accounts, you’ll need to link
the organization user with the existing user object after importing the organization user group. For more information, see
[Resolve conflicts after importing users](#label-org-users-conflicts).

## Get started[¶](#get-started "Link to this heading")

The basic workflow of getting organization users into one or more accounts is as follows:

1. As a global organization administrator in the organization account:

   1. [Create an organization user](#label-org-users) for each person that
      you want to be a user in multiple regular accounts.
   2. [Create an organization user group](#label-org-users-groups-create) that is a logical grouping of the users.
   3. [Add the organization users to the organization user group](#label-org-users-groups-add).
   4. [Make the organization user group available](#label-org-users-groups-visibility) to the account administrators in regular accounts.
2. As an administrator in a regular account:

   1. [Import the organization user group](#label-org-users-add) into the account.
   2. [Check for and resolve any conflicts](#label-org-users-conflicts).

For an end-to-end example of this workflow, see [Extended example](#label-org-users-example).

## Create an organization user[¶](#create-an-organization-user "Link to this heading")

The organization administrator creates an organization user with the basic properties of a user object such as the login name and email.
Only an email is required, but these basic properties can’t be set in a regular account after the user is imported. For a list of these
basic properties, see [CREATE ORGANIZATION USER](../sql-reference/sql/create-organization-user).

As an example, the following command creates an organization user:

```
USE ROLE GLOBALORGADMIN;

CREATE ORGANIZATION USER asmith
   EMAIL = 'asmith@example.com'
   LOGIN_NAME = 'asmith@example.com';
```

Copy

## Organization user groups[¶](#organization-user-groups "Link to this heading")

*Organization user groups* are logical groupings of organization users. The organization administrator creates these organization
user groups, then adds the organization users that should belong in each group. When the account administrator imports an organization user
group into an account, all the organization users in the group become user objects in the regular account. An organization user can be a
member of multiple organization user groups.

When the account administrator imports an organization user group into a regular account, Snowflake creates an access control
[role](security-access-control-overview.html#label-access-control-overview-roles) of the same name. For example, if the organization user group is named `data_stewards`,
then importing the group to the regular account creates a role named `data_stewards`. Each user imported from the organization user group is
granted this role.

Administrators in the regular account can fine-tune access control by granting and revoking privileges to the role that has
been granted to each of the users that were imported from the organization user group. You can also grant account-specific roles to the new
role or grant the new role to account-specific roles.

You can import the same organization user group into multiple regular accounts to implement consistent roles across the organization. Each
regular account can assign account-specific privileges to the role, but the naming will be consistent. Alternatively, you could create a
separate organization user group for each account, then add the organization users that are needed in a particular account to the
appropriate organization user group.

If the administrator imports multiple organization user groups that contain the same organization user, only one local user is created, and
this user is granted the roles from all of the organization user groups.

The organization administrator task of preparing an organization user group for the account administrator of regular accounts is a
three-step process:

1. [Create the organization user group](#label-org-users-groups-create).
2. [Add organization users to the group](#label-org-users-groups-add).
3. [Set the visibility of the group](#label-org-users-groups-visibility) to specify which regular accounts can access it.

### Create an organization user group[¶](#create-an-organization-user-group "Link to this heading")

The organization administrator executes the [CREATE ORGANIZATION USER GROUP](../sql-reference/sql/create-organization-user-group) command to create a new organization
user group in the organization account.

As an example, the following command creates an organization user group that represents a logical grouping of data engineers.

```
CREATE ORGANIZATION USER GROUP data_engineers_group
 IS_GRANTABLE = TRUE;
```

Copy

Because the administrator set `IS_GRANTABLE=TRUE`, the account administrator will be able to grant the role created from the
organization user group to a local, account-specific role. Without that parameter, the account administrator can’t grant the role imported
from the organization user group to another role in the regular account.

### Add organization users to an organization user group[¶](#add-organization-users-to-an-organization-user-group "Link to this heading")

After the organization administrator creates an organization user group, they can execute the
[ALTER ORGANIZATION USER GROUP](../sql-reference/sql/alter-organization-user-group) command to add organization users to the group as a comma-delimited list. For
example, to add two existing organization users to the organization user group `data_engineers_group`, execute:

```
ALTER ORGANIZATION USER GROUP data_engineers_group
   ADD ORGANIZATION USERS asmith, sjohnson;
```

Copy

### Make organization user groups available to regular accounts[¶](#make-organization-user-groups-available-to-regular-accounts "Link to this heading")

After you have created an organization group, you need to specify which regular accounts can view and import the group. Account administrators
cannot use the organization user group to import users until you use the [ALTER ORGANIZATION USER GROUP](../sql-reference/sql/alter-organization-user-group) command
to set the visibility of the group. You can specify that all regular accounts can import the organization user group or you can restrict access
to specific accounts.

Important

Executing the ALTER ORGANIZATION USER GROUP command to set the visibility overwrites previous visibility settings. For example, if the
visibility was set to `ALL`, and then the ALTER command was executed to set visibility to `account_a`, the users and roles created
from the organization user group will be removed from all accounts except for `account_a`.

The following command only allows the account `qa_env` to add the organization user group:

```
ALTER ORGANIZATION USER GROUP data_engineers_group
   SET VISIBILITY = ACCOUNTS qa_env;
```

Copy

## Import users in a regular account[¶](#import-users-in-a-regular-account "Link to this heading")

After the organization administrator has created an organization user group, administrators in regular accounts can
import the organization users by executing the ALTER ACCOUNT command to add the organization user group. These administrators can
only import an organization user group if the organization administrator has
[set the visibility of the group](#label-org-users-groups-visibility) so the regular account can access it.

By default, only users with the ACCOUNTADMIN role can import organization user groups into the regular account. To allow other users to import an
organization group, grant them the IMPORT ORGANIZATION USER GROUPS privilege.

The syntax to import an organization user group to a regular account is as follows:

```
ALTER ACCOUNT ADD ORGANIZATION USER GROUP <group_name>
```

Copy

For an example of importing an organization user group to add users, see [Extended example](#label-org-users-example).

## Resolve conflicts after importing users[¶](#resolve-conflicts-after-importing-users "Link to this heading")

The account administrator who imports organization users in their regular account must manually check for conflicts. These conflicts can
arise between the properties of users or the name of the organization user group.

### Conflict between organization user group and existing role[¶](#conflict-between-organization-user-group-and-existing-role "Link to this heading")

A conflict occurs when the name of the organization user group matches the name of an existing
[role](security-access-control-overview.html#label-access-control-overview-roles) in the regular account. The users in the group are not imported until you resolve the
conflict.

To check whether there is a conflict after importing an organization user group, do the following:

1. Execute the [SHOW ORGANIZATION USER GROUPS](../sql-reference/sql/show-organization-user-groups) command.
2. In the `is_imported` column, check if the value is TRUE. If the value is FALSE, the organization user group was not successfully
   imported, which might indicate that there is a conflict.

You can resolve the conflict between a role and an organization user group by linking the role with the group. Linking a role allows it to
be managed as an organization user group going forward. After you link the conflicting role, the organization user group is added to the
account without further action. Call the [SYSTEM$LINK\_ORGANIZATION\_USER\_GROUP](../sql-reference/functions/system_link_organization_user_group) function to link a role with
an organization user group.

For example, suppose the role `marketing_team` existed in your account before importing the organization user group `marketing_team` to the
account. To link the role to the organization user group and complete the process of importing the group, execute the following:

```
SELECT SYSTEM$LINK_ORGANIZATION_USER_GROUP('marketing_team');
```

Copy

### Conflict between organization user and existing user[¶](#conflict-between-organization-user-and-existing-user "Link to this heading")

A conflict occurs when any of the following is true:

* The `name` property of an organization user matches the `name` of an existing user in the regular account.
* The `login_name` property of an organization user matches the `login_name` of an existing user in the regular account.

To check whether there is a user conflict after importing an organization user group, do the following:

1. Execute the [SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP](../sql-reference/sql/show-organization-users) command.
2. In the `is_imported` column, find rows where the value is FALSE. At least one property of the user in that row conflicts with the
   properties of an existing user.

Tip

You can use the [pipe operator](../sql-reference/operators-flow) (`->>`) to post-process the output of SHOW ORGANIZATION USERS and filter on
the `is_imported` column. For example, to search for organization users that were not successfully imported from the
`marketing_team` organization user group, run the following query:

```
SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP marketing_team
  ->> SELECT * FROM $1 WHERE "is_imported" = 'false';
```

Copy

Use one of the following strategies to resolve a conflict between an organization user and an existing user:

* **Link the existing user**: If an existing user object corresponds to the same person as an organization user, and you want to manage the
  user as an organization user going forward, you can link the existing user with the organization user to resolve the conflict. Call the
  [SYSTEM$LINK\_ORGANIZATION\_USER](../sql-reference/functions/system_link_organization_user) function to link an existing user with an organization user. For example, to
  link the existing user `jloeb` with the organization user `jloebsmith`, call the function as follows:

  ```
  SELECT SYSTEM$LINK_ORGANIZATION_USER('jloeb', 'jloebsmith');
  ```

  Copy
* **Drop the existing user**: If you want the organization user to completely replace the local user, run a
  [DROP USER](../sql-reference/sql/drop-user) command to delete the local user. After the local object is dropped, Snowflake automatically adds the
  new user object that corresponds to the organization user.
* **Rename the existing user or its properties**: If you don’t want to link the existing local user with an organization user, but you
  want to preserve the existing user instead of dropping it, you can rename the user object or its properties in the
  regular account to resolve the conflict. After the local object is renamed, Snowflake automatically adds the new user object that
  corresponds to the organization user. For example, if the pre-existing user and the organization user both have the login name
  `JOE_LOGIN`, you could execute the following in the regular account to avoid the conflict:

  ```
  USE ROLE ACCOUNTADMIN;
  ALTER USER joe SET LOGIN_NAME = joe_login_renamed;
  ```

  Copy

## Modifying imported users[¶](#modifying-imported-users "Link to this heading")

Administrators in a regular account can use the [ALTER USER](../sql-reference/sql/alter-user) command to modify a subset of the properties of a user
object after it has been imported. The administrator can modify all properties *except* the properties that can be set on the
organization user in the organization account. For a list of the properties that can only be set in the organization account, see
[CREATE ORGANIZATION USER](../sql-reference/sql/create-organization-user).

## Removing organization users and groups[¶](#removing-organization-users-and-groups "Link to this heading")

Organization users and organization user groups can be [removed from a single account](#label-org-users-remove-account) or removed from
all accounts by [dropping them in the organization account](#label-org-users-remove-org).

### Removing users from a single regular account[¶](#removing-users-from-a-single-regular-account "Link to this heading")

An account administrator can execute an ALTER ACCOUNT command to remove an organization user group from the account. Removing the
organization user group drops all of the users that were imported and removes the role that was created when the organization user group
was imported. This command does not affect the organization users and organization user groups in other regular accounts, nor in the
organization account.

Note

An organization user can be a member of multiple organization user groups. If a user was imported from more than one organization
group, removing one of the groups from the regular account does not remove the user. The user isn’t removed until all of the organization
user groups are removed.

For example, the following command drops all of the users imported from the `data_stewards` group and deletes the `data_stewards`
role:

```
ALTER ACCOUNT REMOVE ORGANIZATION USER GROUP data_stewards;
```

Copy

### Removing users from all regular accounts[¶](#removing-users-from-all-regular-accounts "Link to this heading")

When an organization user is dropped in the organization account, the corresponding user object is dropped from every regular account that
imported the user. To drop an organization user, execute the [DROP ORGANIZATION USER](../sql-reference/sql/drop-organization-user) command in the organization
account.

When an organization user group is dropped in the organization account, the effect on organization users depends on whether the users in the
regular account belong to other organization user groups that were also imported into the account. If an organization user belongs to a different
organization user group that was imported, the user is not removed from the account. Otherwise, dropping the organization user group removes
all of the users imported from the group.

Dropping an organization user group also removes the role that was created when the group was imported.

To drop an organization user group, execute the [DROP ORGANIZATION USER GROUP](../sql-reference/sql/drop-organization-user-group) command in the organization account.

## Unlinking organization users and organization user groups[¶](#unlinking-organization-users-and-organization-user-groups "Link to this heading")

When organization users are successfully imported into a regular account, the local user object is linked to the organization user. If you
decide you want to keep the user object in an account, but no longer want it associated with the organization user, you can use the
[SYSTEM$UNLINK\_ORGANIZATION\_USER](../sql-reference/functions/system_unlink_organization_user) function to unlink the local user from the organization user. All of the
properties of the user are preserved and it can be managed as a local user going forward.

Similarly, you can use the [SYSTEM$UNLINK\_ORGANIZATION\_USER\_GROUP](../sql-reference/functions/system_unlink_organization_user_group) function to unlink a role that was created
by adding an organization user group. This keeps everything about the role the same, but unlinks it from the organization user group. Local
user objects that were added when the organization user group was imported are also unlinked, and are managed as local users going forward.

## Extended example[¶](#extended-example "Link to this heading")

Organization administrator workflow
:   1. As the organization administrator, sign in to the organization account.
    2. Create organization users for two people who are data stewards:

       ```
       USE ROLE GLOBALORGADMIN;

       CREATE ORGANIZATION USER joe_kelley
       EMAIL = 'jkelley@example.com'
       LOGIN_NAME = 'jkelley@example.com';

       CREATE ORGANIZATION USER grace_vivian
       EMAIL = 'gvivian@example.com'
       LOGIN_NAME = 'gvivian@example.com';
       ```

       Copy
    3. Create an organization user group that represents a logical grouping of data stewards.

       ```
       CREATE ORGANIZATION USER GROUP data_stewards_group;
       ```

       Copy
    4. Add the organization users to the new organization user group.

       ```
       ALTER ORGANIZATION USER GROUP data_stewards_group
          ADD ORGANIZATION USERS joe_kelley, grace_vivian;
       ```

       Copy
    5. Allow all regular accounts to import the organization user group.

       ```
       ALTER ORGANIZATION USER GROUP data_stewards_group
          SET VISIBILITY = ALL;
       ```

       Copy

Account administrator workflow
:   1. As the account administrator, sign in to the regular account where you want to import the organization users.
    2. List the organization user groups that can be imported into the account.

       ```
       USE ROLE ACCOUNTADMIN;

       SHOW ORGANIZATION USER GROUPS;
       ```

       Copy
    3. Import the organization user group into the account.

       ```
       ALTER ACCOUNT
         ADD ORGANIZATION USER GROUP data_stewards_group;
       ```

       Copy
    4. Check for conflicts between the organization user group and an existing role:

       ```
       SHOW ORGANIZATION USER GROUPS;
       ```

       Copy

       Make sure the value of the `is_imported` column is TRUE, which indicates there was no conflict.
    5. List the users that have been added to the account and check for conflicts:

       ```
       SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP data_stewards_group;
       ```

       Copy

       Make sure the value of the `is_imported` column is TRUE for all of the organization users, which indicates there were no
       conflicts.

## Related functions[¶](#related-functions "Link to this heading")

For a list of functions that help you work with organization users and organization user groups, see
[Organization user and organization user group functions](../sql-reference/functions-organization-users).

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

1. [Get started](#get-started)
2. [Create an organization user](#create-an-organization-user)
3. [Organization user groups](#organization-user-groups)
4. [Import users in a regular account](#import-users-in-a-regular-account)
5. [Resolve conflicts after importing users](#resolve-conflicts-after-importing-users)
6. [Modifying imported users](#modifying-imported-users)
7. [Removing organization users and groups](#removing-organization-users-and-groups)
8. [Unlinking organization users and organization user groups](#unlinking-organization-users-and-organization-user-groups)
9. [Extended example](#extended-example)
10. [Related functions](#related-functions)

Related content

1. [Organization accounts](/user-guide/organization-accounts)