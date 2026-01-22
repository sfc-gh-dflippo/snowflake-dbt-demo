---
auto_generated: true
description: Enterprise Edition Feature
last_scraped: '2026-01-14T16:57:35.090197+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/security-column-ddm-use
title: Using Dynamic Data Masking | Snowflake Documentation
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

    * Data quality monitoring

      * [Data profile](data-quality-profile.md)
      * [Introduction to DMFs](data-quality-intro.md)
      * [Tutorial: Getting started with DMFs](tutorials/data-quality-tutorial-start.md)
      * [System DMFs](data-quality-system-dmfs.md)
      * [Custom DMFs](data-quality-custom-dmfs.md)
      * [Use DMFs for quality checks](data-quality-working.md)
      * [Monitor quality checks in Snowsight](data-quality-ui-monitor.md)
      * [Notifications for failed quality checks](data-quality-notifications.md)
      * [View DMF results using SQL](data-quality-results.md)
      * [Remediate data quality issues](data-quality-fixing.md)
      * [Track use of DMFs](data-quality-monitor.md)
      * [Access control](data-quality-access-control.md)
    * Object tagging

      * [Introduction](object-tagging/introduction.md)
      * [Tag inheritance](object-tagging/inheritance.md)
      * [Automatic propagation](object-tagging/propagation.md)
      * [Work with object tags](object-tagging/work.md)
      * [Monitor object tags](object-tagging/monitor.md)
      * [Interaction with other features](object-tagging/interaction.md)
    * Sensitive data classification

      * [Introduction](classify-intro.md)
      * [Tutorial: Automatically classify and tag sensitive data](tutorials/sensitive-data-auto-classification.md)
      * [Custom classification](classify-custom.md)
      * [Automatic classification](classify-auto.md)
      * [Manual classification](classify-using.md)
      * [Legacy APIs](classify-classic.md)
    * Data access policies

      * Aggregation Policies

        * [Introduction](aggregation-policies.md)
        * [Entity-Level Privacy](aggregation-policies-entity-privacy.md)
      * Masking Policies

        * [Introduction](security-column-intro.md)
        * [Dynamic Data Masking](security-column-ddm-intro.md)

          + [Using Dynamic Data Masking](security-column-ddm-use.md)
        * [External Tokenization](security-column-ext-token-intro.md)
        * [Tag-based Masking](tag-based-masking-policies.md)
        * [Advanced](security-column-advanced.md)
      * [Join Policies](join-policies.md)
      * [Projection Policies](projection-policies.md)
      * Row Access Policies

        * [Introduction](security-row-intro.md)
        * [Using Row Access Policies](security-row-using.md)
    * [Data lineage](ui-snowsight-lineage.md)
    * [Access history](access-history.md)
    * [Object dependencies](object-dependencies.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Data Governance](../guides/overview-govern.md)Data access policiesMasking Policies[Dynamic Data Masking](security-column-ddm-intro.md)Using Dynamic Data Masking

# Using Dynamic Data Masking[¶](#using-dynamic-data-masking "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides instructions on how to configure and use Dynamic Data Masking in Snowflake.

To learn more about using a masking policy with a tag, see [Tag-based masking policies](tag-based-masking-policies).

## Using Dynamic Data Masking[¶](#id1 "Link to this heading")

The following lists the high-level steps to configure and use Dynamic Data Masking in Snowflake:

1. Grant masking policy management privileges to a custom role for a security or privacy officer.
2. Grant the custom role to the appropriate users.
3. The security or privacy officer creates and defines masking policies and applies them to columns with sensitive data.
4. Execute queries in Snowflake. Note the following:

   * Snowflake dynamically rewrites the query applying the masking policy SQL expression to the column.
   * The column rewrite occurs at every place where the column specified in the masking policy appears in the query (e.g. projections, join predicate, where clause predicate, order by, and group by).
   * Users see masked data based on the execution context conditions defined in the masking policies. For more information on the execution context in Dynamic Data Masking policies, see [Advanced Column-level Security topics](security-column-advanced).

### Step 1: Grant masking policy privileges to custom role[¶](#step-1-grant-masking-policy-privileges-to-custom-role "Link to this heading")

A [security or privacy officer](security-column-intro.html#label-security-column-mgmt-approach) should serve as the masking policy administrator (i.e. custom role: `MASKING_ADMIN`) and have the privileges to define, manage, and apply masking policies to columns.

Snowflake provides the following privileges to grant to a security or privacy officer for Column-level Security masking policies:

| Privilege | Description |
| --- | --- |
| CREATE MASKING POLICY | This schema-level privilege controls who can create masking policies. |
| APPLY MASKING POLICY | This account-level privilege controls who can [un]set masking policies on columns and is granted to the ACCOUNTADMIN role by default. . This privilege only allows applying a masking policy to a column and does not provide any additional table privileges described in [Access control privileges](security-access-control-privileges). |
| APPLY ON MASKING POLICY | Optional. This policy-level privilege can be used by a policy owner to decentralize the [un]set operations of a given masking policy on columns to the object owners (i.e. the role that has the OWNERSHIP privilege on the object). . Snowflake supports [discretionary access control](security-access-control-overview) where object owners are also considered data stewards. . If the policy administrator trusts the object owners to be data stewards for protected columns, then the policy administrator can use this privilege to decentralize applying the policy [un]set operations. |

The following example creates the `MASKING_ADMIN` role and grants masking policy privileges to that role.

Create a masking policy administrator custom role:

> ```
> use role useradmin;
> CREATE ROLE masking_admin;
> ```
>
> Copy

Grant privileges to `masking_admin` role:

> ```
> use role securityadmin;
> GRANT CREATE MASKING POLICY on SCHEMA <db_name.schema_name> to ROLE masking_admin;
> GRANT APPLY MASKING POLICY on ACCOUNT to ROLE masking_admin;
> ```
>
> Copy

Allow `table_owner` role to set or unset the `ssn_mask` masking policy (optional):

> ```
> GRANT APPLY ON MASKING POLICY ssn_mask to ROLE table_owner;
> ```
>
> Copy

Where:

* `db_name.schema_name`
  :   Specifies the identifier for the schema for which the privilege should be granted.

For more information, see:

* [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege)
* [Configuring access control](security-access-control-configure)
* [Access control privileges](security-access-control-privileges)

### Step 2: Grant the custom role to a user[¶](#step-2-grant-the-custom-role-to-a-user "Link to this heading")

Grant the `MASKING_ADMIN` custom role to a user serving as the security or privacy officer.

```
GRANT ROLE masking_admin TO USER jsmith;
```

Copy

### Step 3: Create a masking policy[¶](#step-3-create-a-masking-policy "Link to this heading")

Using the MASKING\_ADMIN role, create a masking policy and apply it to a column.

In this representative example, users with the ANALYST role see the unmasked value. Users without the ANALYST role see a full mask.

```
CREATE OR REPLACE MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE
    WHEN CURRENT_ROLE() IN ('ANALYST') THEN val
    ELSE '*********'
  END;
```

Copy

Tip

If you want to update an existing masking policy and need to see the current definition of the policy, call the [GET\_DDL](../sql-reference/functions/get_ddl) function or run the [DESCRIBE MASKING POLICY](../sql-reference/sql/desc-masking-policy) command.

### Step 4: Apply the masking policy to a table or view column[¶](#step-4-apply-the-masking-policy-to-a-table-or-view-column "Link to this heading")

These examples assume that a masking policy is not applied to the table column when the table is created and the view column when the view
is created. You can optionally apply a masking policy to a table column when you create the table with a
[CREATE TABLE](../sql-reference/sql/create-table) statement or a view column with a [CREATE VIEW](../sql-reference/sql/create-view) statement.

Execute the following statements to apply the policy to a table column or a view column.

```
-- apply masking policy to a table column

ALTER TABLE IF EXISTS user_info MODIFY COLUMN email SET MASKING POLICY email_mask;

-- apply the masking policy to a view column

ALTER VIEW user_info_v MODIFY COLUMN email SET MASKING POLICY email_mask;
```

Copy

### Step 5: Query data in Snowflake[¶](#step-5-query-data-in-snowflake "Link to this heading")

Execute two different queries in Snowflake, one query with the ANALYST role and another query with a different role, to verify that users without the ANALYST role see a full mask.

```
-- using the ANALYST role

USE ROLE analyst;
SELECT email FROM user_info; -- should see plain text value

-- using the PUBLIC role

USE ROLE PUBLIC;
SELECT email FROM user_info; -- should see full data mask
```

Copy

## Masking policy with a memoizable function[¶](#masking-policy-with-a-memoizable-function "Link to this heading")

This example uses a [memoizable function](../developer-guide/udf/sql/udf-sql-scalar-functions.html#label-udf-sql-scalar-memoizable) to cache the result of a query on the mapping table that
determines whether a role is authorized to view PII data. A data engineer uses a masking policy to protect the columns in the table.

The following procedure references these objects:

* A table that contains PII data, `employee_data`:

  ```
  +----------+-------------+---------------+
  | USERNAME |     ID      | PHONE_NUMBER  |
  +----------+-------------+---------------+
  | JSMITH   | 12-3456-89  | 1555-523-8790 |
  | AJONES   | 12-0124-32  | 1555-125-1548 |
  +----------+-------------+---------------+
  ```
* A mapping table that determines whether a particular role is authorized to view data, `auth_role_t`:

  ```
  +---------------+---------------+
  | ROLE          | IS_AUTHORIZED |
  +---------------+---------------+
  | DATA_ENGINEER | TRUE          |
  | DATA_STEWARD  | TRUE          |
  | IT_ADMIN      | TRUE          |
  | PUBLIC        | FALSE         |
  +---------------+---------------+
  ```

Complete these steps to create a masking policy that calls a memoizable function with arguments:

1. Create a memoizable function that queries the mapping table. The function returns an array of roles based on the value of the
   `is_authorized` column:

   ```
   CREATE FUNCTION is_role_authorized(arg1 VARCHAR)
   RETURNS BOOLEAN
   MEMOIZABLE
   AS
   $$
     SELECT ARRAY_CONTAINS(
       arg1::VARIANT,
       (SELECT ARRAY_AGG(role) FROM auth_role WHERE is_authorized = TRUE)
     )
   $$;
   ```

   Copy
2. Call the memoizable function to cache the query results. In this example, pass the value `TRUE` as the argument value because the
   resultant array serves as the source of allowed roles to access the data protected by the masking policy:

   ```
   SELECT is_role_authorized(IT_ADMIN);
   ```

   Copy

   ```
   +---------------------------------------------+
   |         is_role_authorized(IT_ADMIN)        |
   +---------------------------------------------+
   |                    TRUE                     |
   +---------------------------------------------+
   ```
3. Create a masking policy to protect the `id` column. The policy calls the memoizable function to determine whether the
   role used to query the table is authorized to see the data in the protected column:

   ```
   CREATE OR REPLACE MASKING POLICY empl_id_mem_mask
   AS (val VARCHAR) RETURNS VARCHAR ->
   CASE
     WHEN is_role_authorized(CURRENT_ROLE()) THEN val
     ELSE NULL
   END;
   ```

   Copy
4. Set the masking policy on the table with an [ALTER TABLE … ALTER COLUMN](../sql-reference/sql/alter-table-column) command:

   ```
   ALTER TABLE employee_data MODIFY COLUMN id
     SET MASKING POLICY empl_id_mem_mask;
   ```

   Copy
5. Query the table to test the policy:

   ```
   USE ROLE data_engineer;
   SELECT * FROM employee_data;
   ```

   Copy

   This query returns unmasked data.

   However, if you switch roles to the PUBLIC role and repeat the query in this step, the values in the `id` are replaced
   with `NULL`.

## Additional masking policy examples[¶](#additional-masking-policy-examples "Link to this heading")

The following are additional, representative examples that can be used in the body of the Dynamic Data Masking policy.

Allow a production [account](admin-account-identifier) to see unmasked values and all other accounts
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

Return a hash value using [SHA2 , SHA2\_HEX](../sql-reference/functions/sha2) for unauthorized users. Using a hashing function in a masking policy may result in collisions; therefore, exercise caution with this approach. For more information, see [Advanced Column-level Security topics](security-column-advanced).

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
> A workaround is to cast the actual timestamp value with a fabricated timestamp value. For more information, see [DATE\_FROM\_PARTS](../sql-reference/functions/date_from_parts) and [CAST , ::](../sql-reference/functions/cast).

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

Using a custom entitlement table. Note the use of [EXISTS](../sql-reference/operators-subquery) in the WHEN clause. Always use EXISTS when including a subquery in the masking policy body. For more information on subqueries that Snowflake supports, see [Working with Subqueries](querying-subqueries).

> ```
> CASE
>   WHEN EXISTS
>     (SELECT role FROM <db>.<schema>.entitlement WHERE mask_method='unmask' AND role = current_role()) THEN val
>   ELSE '********'
> END;
> ```
>
> Copy

Using [DECRYPT](../sql-reference/functions/decrypt) on previously encrypted data with either [ENCRYPT](../sql-reference/functions/encrypt) or [ENCRYPT\_RAW](../sql-reference/functions/encrypt_raw), with a passphrase on the encrypted data:

> ```
> case
>   when current_role() in ('ANALYST') then DECRYPT(val, $passphrase)
>   else val -- shows encrypted value
> end;
> ```
>
> Copy

Using a [<JavaScript UDF](../developer-guide/udf/javascript/udf-javascript-introduction) on JSON (VARIANT):

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

Using the [GEOGRAPHY](../sql-reference/data-types-geospatial) data type:

> In this example, a masking policy uses the [TO\_GEOGRAPHY](../sql-reference/functions/to_geography) function to convert all GEOGRAPHY data in a
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
> Set the masking policy on a column with the GEOGRAPHY data type and set the [GEOGRAPHY\_OUTPUT\_FORMAT](../sql-reference/parameters.html#label-geography-output-format) value for the session to
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

For examples using other context functions and role hierarchy, see [Advanced Column-level Security topics](security-column-advanced).

**Next Topics:**

* [Advanced Column-level Security topics](security-column-advanced)

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

1. [Using Dynamic Data Masking](#id1)
2. [Masking policy with a memoizable function](#masking-policy-with-a-memoizable-function)
3. [Additional masking policy examples](#additional-masking-policy-examples)

Related content

1. [Understanding Column-level Security](/user-guide/security-column-intro)
2. [Tag-based masking policies](/user-guide/tag-based-masking-policies)