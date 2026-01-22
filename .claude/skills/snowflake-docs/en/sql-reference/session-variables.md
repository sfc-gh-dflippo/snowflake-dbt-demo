---
auto_generated: true
description: You can define and use SQL variables in sessions in Snowflake.
last_scraped: '2026-01-14T16:55:18.961133+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/session-variables
title: SQL variables | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)

   * [Parameters](parameters.md)
   * [References](references.md)
   * [Ternary logic](ternary-logic.md)
   * [Collation support](collation.md)
   * [SQL format models](sql-format-models.md)
   * [Object identifiers](identifiers.md)
   * [Constraints](constraints.md)
   * [SQL variables](session-variables.md)
   * [Bind variables](bind-variables.md)
   * [Transactions](transactions.md)
   * [Table literals](literals-table.md)
   * [SNOWFLAKE database](snowflake-db.md)
   * [Snowflake Information Schema](info-schema.md)
   * [Metadata fields](metadata.md)
   * [Conventions](conventions.md)
   * [Reserved keywords](reserved-keywords.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[General reference](../sql-reference.md)SQL variables

# SQL variables[¶](#sql-variables "Link to this heading")

You can define and use SQL variables in sessions in Snowflake.

## Overview[¶](#overview "Link to this heading")

Snowflake supports SQL variables declared by the user. They have many uses, such as storing application-specific environment settings.

### Variable identifiers[¶](#variable-identifiers "Link to this heading")

SQL variables are globally identified using case-insensitive names.

### Variable DDL[¶](#variable-ddl "Link to this heading")

Snowflake provides the following DDL commands for using SQL variables:

* [SET](sql/set)
* [UNSET](sql/unset)
* [SHOW VARIABLES](sql/show-variables)

## Initializing variables[¶](#initializing-variables "Link to this heading")

You can set variables by executing the SQL statement [SET](sql/set) or by setting the variables in the connection
string when you connect to Snowflake.

The size of string or binary variables is limited to 256 bytes.

### Using SQL to initialize variables in a session[¶](#using-sql-to-initialize-variables-in-a-session "Link to this heading")

Variables can be initialized in SQL using the [SET](sql/set) command. The data type of the variable is derived from the
data type of the result of the evaluated expression.

```
SET my_variable=10;
SET my_variable='example';
```

Copy

Multiple variables can be initialized in the same statement, thereby reducing the number of round-trip communications with the server.

```
SET (var1, var2, var3)=(10, 20, 30);
SET (var1, var2, var3)=(SELECT 10, 20, 30);
```

Copy

### Setting variables on connection[¶](#setting-variables-on-connection "Link to this heading")

In addition to using [SET](sql/set) to set variables within a session, you can pass variables as arguments in the connection
string used to initialize a session in Snowflake. This option is especially useful when using tools where the specification of the connection string
is the only customization possible.

For example, using the Snowflake JDBC driver, you can set additional connection properties that will be interpreted as parameters. Note that
the JDBC API requires SQL variables to be strings.

```
// Build connection properties
Properties properties = new Properties();

// Required connection properties
properties.put("user"    ,  "jsmith"      );
properties.put("password",  "mypassword");
properties.put("account" ,  "myaccount");

// Set some additional variables.
properties.put("$variable_1", "some example");
properties.put("$variable_2", "1"           );

// Create a new connection
String connectStr = "jdbc:snowflake://localhost:8080";

// Open a connection under the snowflake account and enable variable support
Connection con = DriverManager.getConnection(connectStr, properties);
```

Copy

## Using variables in SQL[¶](#using-variables-in-sql "Link to this heading")

Variables can be used in Snowflake anywhere a literal constant is allowed, except where noted in the documentation. To distinguish them
from bind values and column names, all variables must be prefixed with a `$` sign.

For example:

```
SET (min, max)=(40, 70);

SELECT $min;

SELECT AVG(salary) FROM emp WHERE age BETWEEN $min AND $max;
```

Copy

Note

Because the `$` sign is the prefix used to identify variables in SQL statements, it is treated as a special character when used
in identifiers. Identifiers (database names, table names, column names, etc.) cannot start with special characters unless the entire
name is enclosed in double quotes. For more information, see [Object identifiers](identifiers).

Variables can also contain identifier names, such as table names. To use a variable as an identifier, you must
wrap it inside `IDENTIFIER()`, e.g. `IDENTIFIER($my_variable)`. Some examples are below:

```
SET my_table_name='table1';
```

Copy

```
CREATE TABLE IDENTIFIER($my_table_name) (i INTEGER);
INSERT INTO IDENTIFIER($my_table_name) (i) VALUES (42);
```

Copy

```
SELECT * FROM IDENTIFIER($my_table_name);
```

Copy

```
+----+
|  I |
|----|
| 42 |
+----+
```

In the context of a FROM clause, you can wrap the variable name in `TABLE()`, as shown below:

```
SELECT * FROM TABLE($my_table_name);
```

Copy

```
+----+
|  I |
|----|
| 42 |
+----+
```

```
DROP TABLE IDENTIFIER($my_table_name);
```

Copy

For more information about `IDENTIFIER()`, see [Literals and variables as identifiers with IDENTIFIER() syntax](identifier-literal).

### Viewing variables for the session[¶](#viewing-variables-for-the-session "Link to this heading")

To see all the variables defined in the current session, use the [SHOW VARIABLES](sql/show-variables) command:

```
SET (min, max)=(40, 70);
```

Copy

```
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
```

```
SHOW VARIABLES;
```

Copy

```
+----------------+-------------------------------+-------------------------------+------+-------+-------+---------+
|     session_id | created_on                    | updated_on                    | name | value | type  | comment |
|----------------+-------------------------------+-------------------------------+------+-------+-------+---------|
| 10363773891062 | 2024-06-28 10:09:57.990 -0700 | 2024-06-28 10:09:58.032 -0700 | MAX  | 70    | fixed |         |
| 10363773891062 | 2024-06-28 10:09:57.990 -0700 | 2024-06-28 10:09:58.021 -0700 | MIN  | 40    | fixed |         |
+----------------+-------------------------------+-------------------------------+------+-------+-------+---------+
```

### Session variable functions[¶](#session-variable-functions "Link to this heading")

The following convenience functions are provided for manipulating session variables to support compatibility with other database systems
and to issue SQL through tools that do not support the `$` syntax for accessing variables. Note that all these functions accept and
return session variable values as strings:

> * SYS\_CONTEXT and SET\_SYS\_CONTEXT
> * SESSION\_CONTEXT and SET\_SESSION\_CONTEXT
> * [GETVARIABLE](functions/getvariable) and SETVARIABLE

Here are examples of using GETVARIABLE. First, define a variable using SET:

```
SET var_artist_name = 'Jackson Browne';
```

Copy

```
+----------------------------------+
| status                           |
+----------------------------------+
| Statement executed successfully. |
+----------------------------------+
```

Return the variable value:

```
SELECT GETVARIABLE('var_artist_name');
```

Copy

In this example, the output is NULL because Snowflake stores variables with all uppercase letters.

Update the casing:

```
SELECT GETVARIABLE('VAR_ARTIST_NAME');
```

Copy

```
+--------------------------------+
| GETVARIABLE('VAR_ARTIST_NAME') |
+--------------------------------+
| Jackson Browne                 |
+--------------------------------+
```

You can use the variable name in a WHERE clause, for example:

```
SELECT album_title
  FROM albums
  WHERE artist = $var_artist_name;
```

Copy

## Removing variables[¶](#removing-variables "Link to this heading")

SQL variables are private to a session. When a Snowflake session is closed, all variables created during the session are dropped. This
means that no one can access user-defined variables that have been set in another session, and when the session is closed, these variables
expire.

In addition, variables always can be explicitly destroyed using the [UNSET](sql/unset) command.

For example:

```
UNSET my_variable;
```

Copy

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

1. [Overview](#overview)
2. [Initializing variables](#initializing-variables)
3. [Using variables in SQL](#using-variables-in-sql)
4. [Removing variables](#removing-variables)

Related content

1. [Table literals](/sql-reference/literals-table)