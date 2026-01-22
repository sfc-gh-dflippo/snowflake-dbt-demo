---
auto_generated: true
description: Enterprise Edition Feature
last_scraped: '2026-01-14T16:57:14.606868+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-masking-policy.html
title: CREATE MASKING POLICY | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
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

     + Column-level Security
     + [CREATE MASKING POLICY](create-masking-policy.md)
     + [ALTER MASKING POLICY](alter-masking-policy.md)
     + [DROP MASKING POLICY](drop-masking-policy.md)
     + [SHOW MASKING POLICIES](show-masking-policies.md)
     + [DESCRIBE MASKING POLICY](desc-masking-policy.md)
     + Row access policy
     + [CREATE ROW ACCESS POLICY](create-row-access-policy.md)
     + [ALTER ROW ACCESS POLICY](alter-row-access-policy.md)
     + [DROP ROW ACCESS POLICY](drop-row-access-policy.md)
     + [SHOW ROW ACCESS POLICIES](show-row-access-policies.md)
     + [DESCRIBE ROW ACCESS POLICY](desc-row-access-policy.md)
     + Tag
     + [CREATE TAG](create-tag.md)
     + [ALTER TAG](alter-tag.md)
     + [SHOW TAGS](show-tags.md)
     + [DROP TAG](drop-tag.md)
     + [UNDROP TAG](undrop-tag.md)
     + Contact
     + [CREATE CONTACT](create-contact.md)
     + [ALTER CONTACT](alter-contact.md)
     + [SHOW CONTACTS](show-contacts.md)
     + [DROP CONTACT](drop-contact.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Data Governance](../commands-data-governance.md)CREATE MASKING POLICY

# CREATE MASKING POLICY[¶](#create-masking-policy "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Enterprise Edition Feature](../../user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new masking policy in the current/specified schema or replaces an existing masking policy.

After creating a masking policy, apply the masking policy to a column in a table using an [ALTER TABLE … ALTER COLUMN](alter-table-column) command or a view using
an [ALTER VIEW](alter-view) command.

See also:
:   [Choosing a centralized, hybrid, or decentralized approach](../../user-guide/security-column-intro.html#label-security-column-mgmt-approach), [Advanced Column-level Security topics](../../user-guide/security-column-advanced)

    [Masking policy DDL](../../user-guide/security-column-intro.html#label-security-column-intro-ddl)

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] MASKING POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
RETURNS <arg_type_to_mask> -> <body>
[ COMMENT = '<string_literal>' ]
[ EXEMPT_OTHER_POLICIES = { TRUE | FALSE } ]
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   Identifier for the masking policy; must be unique for your schema.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

`AS ( arg_name_to_mask arg_type_to_mask [ , arg_1 arg_type_1 ... ] )`
:   The signature for the masking policy; specifies the input columns and data types to evaluate at query runtime.

    For more details, see [SQL data types reference](../../sql-reference-data-types).

    `arg_name_to_mask arg_type_to_mask`
    :   The first column and its data type always indicate the column data type values to mask or tokenize in the subsequent
        policy conditions.

        Note that you can not specify a virtual column as the first column argument in a conditional masking policy.

    `[ , arg_1 arg_type_1 ... ]`
    :   Specifies the conditional columns and their data types to evaluate to determine whether the policy conditions should mask or tokenize
        the data in the first column in each row of the query result.

        If these additional columns and data types are not specified, Snowflake evaluates the policy as a normal masking policy.

`RETURNS arg_type_to_mask`
:   The return data type must match the input data type of the first column that is specified as an input column.

`body`
:   SQL expression that transforms the data in the column designated by `arg_name_to_mask`.

    The expression can include [Conditional expression functions](../expressions-conditional) to represent conditional logic, built-in functions, or UDFs to
    transform the data.

    If a UDF or external function is used inside the masking policy body, the policy owner must have USAGE on the UDF or external function.
    The USAGE privilege on the UDF or external function is not required for the role used to query a column that has a masking policy applied
    to it.

    If a UDF or external function is used inside the conditional masking policy body, the policy owner must have OWNERSHIP on the UDF or
    external function. Users querying a column that has a conditional masking policy applied to it do not need to have USAGE on the UDF or
    external function.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the masking policy.

`EXEMPT_OTHER_POLICIES = TRUE | FALSE`
:   One of the following depending on the usage:

    * Specifies whether a row access policy or conditional masking policy can reference a column that is already protected by this masking
      policy.
    * Specifies whether a masking policy assigned to a virtual column overrides the masking policy that the virtual column inherits from the
      VALUE column. When working with external tables, specify this property in the masking policy that protects the VALUE column.

    `TRUE`
    :   Allows a different policy to reference the masked column or allows the masking policy set on a virtual column to override the masking
        policy the virtual column inherits from the VALUE column in an external table.

    `FALSE`
    :   Does not allow a different policy to reference the masked column or allow the masking policy and does not allow the masking policy the virtual column inherits from the VALUE column in an external table.

    Note the following:

    * The value of this property in the masking policy cannot change after setting the masking policy on a table or view. To update
      the value of this property setting, execute a CREATE OR REPLACE MASKING POLICY statement on the masking policy.
    * When the property is set to true it is included in the output of calling the [GET\_DDL](../functions/get_ddl) function on the
      policy.

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE MASKING POLICY | Schema |  |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

When specifying the `EXEMPT_OTHER_POLICIES` property in a masking policy, the role that owns the masking policy
(i.e. the role with OWNERSHIP privilege on the policy) must be in the role hierarchy of the role that owns the row access
policy or the conditional masking policy.

For example, the policy administrator custom roles can form a [role hierarchy](../../user-guide/security-access-control-overview.html#label-role-hierarchy-and-privilege-inheritance) as
follows:

> `masking_admin` » `rap_admin` » SYSADMIN
>
> `masking_admin` » `cond_masking_admin` » SYSADMIN

Where:

`masking_admin`
:   Specifies the custom role that owns the masking policy that is set on the column that will be specified in the signature of a row access
    policy or a conditional masking policy.

`rap_admin`
:   Specifies the custom role that owns the row access policy.

`cond_masking_admin`
:   Specifies the custom role that owns the conditional masking policy.

For additional details on masking policy DDL and privileges, see [Managing Column-level Security](../../user-guide/security-column-intro.html#label-security-column-manage).

## Usage notes[¶](#usage-notes "Link to this heading")

* If you want to replace an existing masking policy and need to see the current definition of the policy, call the
  [GET\_DDL](../functions/get_ddl) function or run the [DESCRIBE MASKING POLICY](desc-masking-policy) command.
* For masking policies that include a subquery in the masking policy body, use [EXISTS](../operators-subquery) in the
  WHEN branch of the CASE function. For a representative example, refer to the custom entitlement table example in the
  [Normal Masking Policy](#label-create-masking-policy-normal) section (in this topic).
* If the policy `body` contains a mapping table lookup, create a centralized mapping table and store the mapping table
  in the same database as the protected table. This is particularly important if the `body` calls the
  [IS\_DATABASE\_ROLE\_IN\_SESSION](../functions/is_database_role_in_session) function. For details, see the function usage notes.
* A given table or view column can be specified in either a masking policy signature or a row access policy signature. In other words, the
  same column cannot be specified in both a masking policy signature and a row access policy signature at the same time.

  For more information, see [CREATE ROW ACCESS POLICY](create-row-access-policy).
* A data sharing provider cannot create a masking policy in a [reader account](../../user-guide/data-sharing-reader-create).
* If using a [UDF](../../developer-guide/udf/udf-overview) in a masking policy, ensure the data type of the column, UDF, and masking
  policy match. For more information, see [User-defined functions in a masking policy](../../user-guide/security-column-intro.html#label-security-column-intro-udf-policy).
* If you specify the [CURRENT\_DATABASE](../functions/current_database) or [CURRENT\_SCHEMA](../functions/current_schema) function in the
  body of a masking or row access policy, the function returns the database or schema that contains the protected table, not the database or
  schema in use for the session.
* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).

* The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
* CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Example: Normal masking policy[¶](#example-normal-masking-policy "Link to this heading")

You can use [Conditional expression functions](../expressions-conditional), [Context functions](../functions-context), and UDFs to write the SQL expression.

The following are representative examples of the policy body to show how to create masking policy conditions using different SQL
expressions, functions, and data types.

These examples mostly use the [CURRENT\_ROLE](../functions/current_role) context function. If role activation and role hierarchy is
necessary in the policy conditions, use [IS\_ROLE\_IN\_SESSION](../functions/is_role_in_session).

Full mask:

> The `analyst` custom role can see the plain-text value. Users without the `analyst` custom role see a full mask.
>
> ```
> CREATE OR REPLACE MASKING POLICY email_mask AS (val string) returns string ->
>   CASE
>     WHEN current_role() IN ('ANALYST') THEN VAL
>     ELSE '*********'
>   END;
> ```
>
> Copy

Allow a production [account](../../user-guide/admin-account-identifier) to see unmasked values and all other accounts
(e.g. development, test) to see masked values.

> ```
> case
>   when current_account() in ('<prod_account_identifier>') then val
>   else '*********'
> end;
> ```
>
> Copy

Return NULL for unauthorized users:

> ```
> case
>   when current_role() IN ('ANALYST') then val
>   else NULL
> end;
> ```
>
> Copy

Return a static masked value for unauthorized users:

> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE '********'
> END;
> ```
>
> Copy

Return a hash value using [SHA2 , SHA2\_HEX](../functions/sha2) for unauthorized users. Using a hashing function in a masking policy may result in collisions; therefore, exercise caution with this approach. For more information, see [Advanced Column-level Security topics](../../user-guide/security-column-advanced).

> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE sha2(val) -- return hash of the column value
> END;
> ```
>
> Copy

Apply a partial mask or full mask:

> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   WHEN current_role() IN ('SUPPORT') THEN regexp_replace(val,'.+\@','*****@') -- leave email domain unmasked
>   ELSE '********'
> END;
> ```
>
> Copy

Using timestamps.

> ```
> case
>   WHEN current_role() in ('SUPPORT') THEN val
>   else date_from_parts(0001, 01, 01)::timestamp_ntz -- returns 0001-01-01 00:00:00.000
> end;
> ```
>
> Copy
>
> Important
>
> Currently, Snowflake does not support different input and output data types in a masking policy, such as defining the masking policy to target a timestamp and return a string (e.g. `***MASKED***`); the input and output data types must match.
>
> A workaround is to cast the actual timestamp value with a fabricated timestamp value. For more information, see [DATE\_FROM\_PARTS](../functions/date_from_parts) and [CAST , ::](../functions/cast).

Using a UDF:

> ```
> CASE
>   WHEN current_role() IN ('ANALYST') THEN val
>   ELSE mask_udf(val) -- custom masking function
> END;
> ```
>
> Copy

On variant data:

> ```
> CASE
>    WHEN current_role() IN ('ANALYST') THEN val
>    ELSE OBJECT_INSERT(val, 'USER_IPADDRESS', '****', true)
> END;
> ```
>
> Copy

Using a custom entitlement table. Note the use of [EXISTS](../operators-subquery) in the WHEN clause. Always use EXISTS when including a subquery in the masking policy body. For more information on subqueries that Snowflake supports, see [Working with Subqueries](../../user-guide/querying-subqueries).

> ```
> CASE
>   WHEN EXISTS
>     (SELECT role FROM <db>.<schema>.entitlement WHERE mask_method='unmask' AND role = current_role()) THEN val
>   ELSE '********'
> END;
> ```
>
> Copy

Using [DECRYPT](../functions/decrypt) on previously encrypted data with either [ENCRYPT](../functions/encrypt) or [ENCRYPT\_RAW](../functions/encrypt_raw), with a passphrase on the encrypted data:

> ```
> case
>   when current_role() in ('ANALYST') then DECRYPT(val, $passphrase)
>   else val -- shows encrypted value
> end;
> ```
>
> Copy

Using a [<JavaScript UDF](../../developer-guide/udf/javascript/udf-javascript-introduction) on JSON (VARIANT):

> In this example, a JavaScript UDF masks location data in a JSON string. It is important to set the data type as VARIANT in the UDF and
> the masking policy. If the data type in the table column, UDF, and masking policy signature do not match, Snowflake returns an error
> message because it cannot resolve the SQL.
>
> ```
> -- Flatten the JSON data
>
> create or replace table <table_name> (v variant) as
> select value::variant
> from @<table_name>,
>   table(flatten(input => parse_json($1):stationLocation));
>
> -- JavaScript UDF to mask latitude, longitude, and location data
>
> CREATE OR REPLACE FUNCTION full_location_masking(v variant)
>   RETURNS variant
>   LANGUAGE JAVASCRIPT
>   AS
>   $$
>     if ("latitude" in V) {
>       V["latitude"] = "**latitudeMask**";
>     }
>     if ("longitude" in V) {
>       V["longitude"] = "**longitudeMask**";
>     }
>     if ("location" in V) {
>       V["location"] = "**locationMask**";
>     }
>
>     return V;
>   $$;
>
>   -- Grant UDF usage to ACCOUNTADMIN
>
>   grant ownership on function FULL_LOCATION_MASKING(variant) to role accountadmin;
>
>   -- Create a masking policy using JavaScript UDF
>
>   create or replace masking policy json_location_mask as (val variant) returns variant ->
>     CASE
>       WHEN current_role() IN ('ANALYST') THEN val
>       else full_location_masking(val)
>       -- else object_insert(val, 'latitude', '**locationMask**', true) -- limited to one value at a time
>     END;
> ```
>
> Copy

Using the [GEOGRAPHY](../data-types-geospatial) data type:

> In this example, a masking policy uses the [TO\_GEOGRAPHY](../functions/to_geography) function to convert all GEOGRAPHY data in a
> column to a fixed point, the longitude and latitude for Snowflake in San Mateo, California, for users whose CURRENT\_ROLE is not
> `ANALYST`.
>
> > ```
> > create masking policy mask_geo_point as (val geography) returns geography ->
> >   case
> >     when current_role() IN ('ANALYST') then val
> >     else to_geography('POINT(-122.35 37.55)')
> >   end;
> > ```
> >
> > Copy
>
> Set the masking policy on a column with the GEOGRAPHY data type and set the [GEOGRAPHY\_OUTPUT\_FORMAT](../parameters.html#label-geography-output-format) value for the session to
> `GeoJSON`:
>
> > ```
> > alter table mydb.myschema.geography modify column b set masking policy mask_geo_point;
> > alter session set geography_output_format = 'GeoJSON';
> > use role public;
> > select * from mydb.myschema.geography;
> > ```
> >
> > Copy
>
> Snowflake returns the following:
>
> > ```
> > ---+--------------------+
> >  A |         B          |
> > ---+--------------------+
> >  1 | {                  |
> >    |   "coordinates": [ |
> >    |     -122.35,       |
> >    |     37.55          |
> >    |   ],               |
> >    |   "type": "Point"  |
> >    | }                  |
> >  2 | {                  |
> >    |   "coordinates": [ |
> >    |     -122.35,       |
> >    |     37.55          |
> >    |   ],               |
> >    |   "type": "Point"  |
> >    | }                  |
> > ---+--------------------+
> > ```
> >
> > Copy
>
> The query result values in column B depend on the GEOGRAPHY\_OUTPUT\_FORMAT parameter value for the session. For example, if the parameter
> value is set to `WKT`, Snowflake returns the following:
>
> > ```
> > alter session set geography_output_format = 'WKT';
> > select * from mydb.myschema.geography;
> >
> > ---+----------------------+
> >  A |         B            |
> > ---+----------------------+
> >  1 | POINT(-122.35 37.55) |
> >  2 | POINT(-122.35 37.55) |
> > ---+----------------------+
> > ```
> >
> > Copy

For examples using other context functions and role hierarchy, see [Advanced Column-level Security topics](../../user-guide/security-column-advanced).

## Example: Conditional masking policy[¶](#example-conditional-masking-policy "Link to this heading")

The following example returns unmasked data for users whose [CURRENT\_ROLE](../functions/current_role) is the `admin` custom role, or
whose value in the visibility column is `Public`. All other conditions result in a fixed masked value.

> ```
> -- Conditional Masking
>
> create masking policy email_visibility as
> (email varchar, visibility string) returns varchar ->
>   case
>     when current_role() = 'ADMIN' then email
>     when visibility = 'Public' then email
>     else '***MASKED***'
>   end;
> ```
>
> Copy

The following example returns detokenized data for users whose [CURRENT\_ROLE](../functions/current_role) is the `admin` custom role,
and whose value in a different column is `Public`. All other conditions result in a tokenized value.

> ```
> -- Conditional Tokenization
>
> create masking policy de_email_visibility as
>  (email varchar, visibility string) returns varchar ->
>    case
>      when current_role() = 'ADMIN' and visibility = 'Public' then de_email(email)
>      else email -- sees tokenized data
>    end;
> ```
>
> Copy

## Example: Allow a masked column in a row access policy or conditional masking policy[¶](#example-allow-a-masked-column-in-a-row-access-policy-or-conditional-masking-policy "Link to this heading")

Replace a masking policy that either allows viewing the email address, viewing only the email address domain, or a viewing fixed masked
value:

> ```
> create or replace masking policy governance.policies.email_mask
> as (val string) returns string ->
> case
>   when current_role() in ('ANALYST') then val
>   when current_role() in ('SUPPORT') then regexp_replace(val,'.+\@','*****@')
>   else '********'
> end
> comment = 'specify in row access policy'
> exempt_other_policies = true
> ;
> ```
>
> Copy

This policy can now be set on a column and a row access policy or a conditional masking policy can reference the column protected by this
masking policy as needed.

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

1. [Syntax](#syntax)
2. [Required parameters](#required-parameters)
3. [Optional parameters](#optional-parameters)
4. [Access control requirements](#access-control-requirements)
5. [Usage notes](#usage-notes)
6. [Example: Normal masking policy](#example-normal-masking-policy)
7. [Example: Conditional masking policy](#example-conditional-masking-policy)
8. [Example: Allow a masked column in a row access policy or conditional masking policy](#example-allow-a-masked-column-in-a-row-access-policy-or-conditional-masking-policy)

Related content

1. [masking policy](/sql-reference/sql/../../user-guide/security-column-intro)