---
auto_generated: true
description: You can write the handler for a user-defined function (UDF) in JavaScript.
  Topics in this section describe how to design and write a JavaScript handler.
last_scraped: '2026-01-14T16:55:18.531945+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-introduction
title: Introduction to JavaScript UDFs | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../../snowpark/index.md)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)

    * [Function or procedure?](../../stored-procedures-vs-udfs.md)
    * [Guidelines](../../udf-stored-procedure-guidelines.md)
    * [Stored procedures](../../stored-procedure/stored-procedures-overview.md)
    * [User-defined functions](../udf-overview.md)

      + [Privileges](../udf-access-control.md)
      + [Creating](../udf-creating-sql.md)
      + [Executing](../udf-calling-sql.md)
      + [Viewing in Snowsight](../../../user-guide/ui-snowsight-data-databases-function.md)
      + Handler writing
      + [Java](../java/udf-java-introduction.md)
      + [Javascript](udf-javascript-introduction.md)

        - [Limitations](udf-javascript-limitations.md)
        - [Scalar functions](udf-javascript-scalar-functions.md)
        - [Table functions](udf-javascript-tabular-functions.md)
        - [Troubleshooting](udf-javascript-troubleshooting.md)
      + [Python](../python/udf-python-introduction.md)
      + [Scala](../scala/udf-scala-introduction.md)
      + [SQL](../sql/udf-sql-introduction.md)
    * [Packaging handler code](../../udf-stored-procedure-building.md)
    * [External network access](../../external-network-access/external-network-access-overview.md)
13. [Logging, Tracing, and Metrics](../../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../../streamlit/object-management/billing.md)
      - [Security considerations](../../streamlit/object-management/security.md)
      - [Privilege requirements](../../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../../streamlit/app-development/dependency-management.md)
      - [File organization](../../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../../streamlit/features/git-integration.md)
      - [External access](../../streamlit/features/external-access.md)
      - [Row access policies](../../streamlit/features/row-access.md)
      - [Sleep timer](../../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../../streamlit/troubleshooting.md)
    - [Release notes](../../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../../snowflake-cli/index.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Functions and procedures](../../extensibility.md)[User-defined functions](../udf-overview.md)Javascript

# Introduction to JavaScript UDFs[¶](#introduction-to-javascript-udfs "Link to this heading")

You can write the handler for a user-defined function (UDF) in JavaScript. Topics in this section describe how to design and write a
JavaScript handler.

For an introduction to UDFs, including a list of languages in which you can write a UDF handler, refer to [User-defined functions overview](../udf-overview).

Once you have a handler, you create the UDF with SQL. For information on using SQL to create or call a UDF, refer to
[Creating a user-defined function](../udf-creating-sql) or [Executing a UDF](../udf-calling-sql).

You can capture log and trace data as your handler code executes. For more information, refer to
[Logging, tracing, and metrics](../../logging-tracing/logging-tracing-overview).

Note

For limitations related to JavaScript UDF handlers, refer to [JavaScript UDF limitations](udf-javascript-limitations).

## How a JavaScript handler works[¶](#how-a-javascript-handler-works "Link to this heading")

When a user calls a UDF, the user passes UDF’s name and arguments to Snowflake. Snowflake calls the associated handler code
(with arguments, if any) to execute the UDF’s logic. The handler function then returns the output to Snowflake, which passes it back to the
client.

For each row passed to a UDF, the UDF returns either a scalar (i.e. single) value or, if defined as a table function, a set of rows.

### Example[¶](#example "Link to this heading")

Code in the following example creates a UDF called `my_array_reverse` with a handler code that accepts an input ARRAY and
returns an ARRAY containing the elements in reverse order. The JavaScript argument and return types are converted to and from SQL
by Snowflake, according to mappings described in [SQL-JavaScript Data Type Mappings](../../udf-stored-procedure-data-type-mapping.html#label-javascript-supported-snowpark-types).

Note that the JavaScript code must refer to the input parameter names as all uppercase, even if the names are not uppercase in the
SQL code.

```
-- Create the UDF.
CREATE OR REPLACE FUNCTION my_array_reverse(a ARRAY)
  RETURNS ARRAY
  LANGUAGE JAVASCRIPT
AS
$$
  return A.reverse();
$$
;
```

Copy

## JavaScript data types[¶](#javascript-data-types "Link to this heading")

SQL and JavaScript UDFs provide similar, but different, data types, based on their native data type support. Objects within Snowflake
and JavaScript are transferred using the following mappings.

### Integers and doubles[¶](#integers-and-doubles "Link to this heading")

JavaScript has no integer type; all numbers are represented as doubles. JavaScript UDFs do not accept or return integer values except
through type conversion (i.e. you can pass an integer to a JavaScript UDF that accepts a double).

Both Snowflake SQL and JavaScript support double values. These values are transferred as-is.

### Strings[¶](#strings "Link to this heading")

Both Snowflake SQL and JavaScript support string values. These values are transferred as-is.

### Binary values[¶](#binary-values "Link to this heading")

All binary values are converted into JavaScript `Uint8Array` objects. These typed arrays can be accessed in the same way as
regular JavaScript arrays, but they are more efficient and support additional methods.

If a JavaScript UDF returns a `Uint8Array` object, it is converted into a Snowflake SQL binary value.

### Dates[¶](#dates "Link to this heading")

All timestamp and date types are converted into JavaScript `Date()` objects. The JavaScript date type is equivalent to
TIMESTAMP\_LTZ(3) in Snowflake SQL.

Consider the following notes for JavaScript UDFs that accept a date or time:

* All precision beyond milliseconds is lost.
* A JavaScript `Date` generated from SQL TIMESTAMP\_NTZ no longer acts as “wallclock” time; it is influenced by daylight saving time.
  This is similar to behavior when converting TIMESTAMP\_NTZ to TIMESTAMP\_LTZ.
* A JavaScript `Date` generated from SQL TIMESTAMP\_TZ loses time zone information, but represents the same moment in time as the
  input (similar to when converting TIMESTAMP\_TZ to TIMESTAMP\_LTZ).
* SQL DATE is converted to JavaScript `Date` representing midnight of the current day in the local time zone.

Additionally, consider the following notes for JavaScript UDFs that return DATE and TIMESTAMP types:

* JavaScript `Date` objects are converted to the UDF’s result data type, adhering to the same conversion semantics as casts from
  TIMESTAMP\_LTZ(3) to the return data type.
* JavaScript `Date` objects nested inside VARIANT objects are always of type TIMESTAMP\_LTZ(3).

### Variant, objects, and arrays[¶](#variant-objects-and-arrays "Link to this heading")

JavaScript UDFs allow easy, intuitive manipulation of variant and JSON data. Variant objects passed to a UDF are transformed to native
JavaScript types and values. Any of the previously-listed values are translated into their corresponding JavaScript types. Variant objects
and arrays are converted to JavaScript objects and arrays. Similarly, all values returned by the UDF are transformed into the appropriate
variant values. Note that objects and arrays returned by the UDF are subject to size and depth limitations.

```
-- flatten all arrays and values of objects into a single array
-- order of objects may be lost
CREATE OR REPLACE FUNCTION flatten_complete(v variant)
  RETURNS variant
  LANGUAGE JAVASCRIPT
  AS '
  // Define a function flatten(), which always returns an array.
  function flatten(input) {
    var returnArray = [];
    if (Array.isArray(input)) {
      var arrayLength = input.length;
      for (var i = 0; i < arrayLength; i++) {
        returnArray.push.apply(returnArray, flatten(input[i]));
      }
    } else if (typeof input === "object") {
      for (var key in input) {
        if (input.hasOwnProperty(key)) {
          returnArray.push.apply(returnArray, flatten(input[key]));
        }
      }
    } else {
      returnArray.push(input);
    }
    return returnArray;
  }

  // Now call the function flatten() that we defined earlier.
  return flatten(V);
  ';

select value from table(flatten(flatten_complete(parse_json(
'[
  {"key1" : [1, 2], "key2" : ["string1", "string2"]},
  {"key3" : [{"inner key 1" : 10, "inner key 2" : 11}, 12]}
  ]'))));

-----------+
   VALUE   |
-----------+
 1         |
 2         |
 "string1" |
 "string2" |
 10        |
 11        |
 12        |
-----------+
```

Copy

## JavaScript arguments and returned values[¶](#javascript-arguments-and-returned-values "Link to this heading")

Arguments may be referenced directly by name within JavaScript. Note that an unquoted identifier must be referenced with the
capitalized variable name. As arguments and the UDF are referenced from within JavaScript, they must be legal JavaScript identifiers.
Specifically, UDF and argument names must begin with a letter or `$`, while subsequent characters can be alphanumeric, `$`,
or `_`. Additionally, names can not be JavaScript-reserved words.

The following three examples illustrate UDFs that use arguments referenced by name:

```
-- Valid UDF.  'N' must be capitalized.
CREATE OR REPLACE FUNCTION add5(n double)
  RETURNS double
  LANGUAGE JAVASCRIPT
  AS 'return N + 5;';

select add5(0.0);

-- Valid UDF. Lowercase argument is double-quoted.
CREATE OR REPLACE FUNCTION add5_quoted("n" double)
  RETURNS double
  LANGUAGE JAVASCRIPT
  AS 'return n + 5;';

select add5_quoted(0.0);

-- Invalid UDF. Error returned at runtime because JavaScript identifier 'n' cannot be resolved.
CREATE OR REPLACE FUNCTION add5_lowercase(n double)
  RETURNS double
  LANGUAGE JAVASCRIPT
  AS 'return n + 5;';

select add5_lowercase(0.0);
```

Copy

### NULL and undefined values[¶](#null-and-undefined-values "Link to this heading")

When using JavaScript UDFs, pay close attention to rows and variables that might contain NULL values. Specifically, Snowflake
contains two distinct NULL values (SQL `NULL` and variant’s JSON `null`), while JavaScript contains the `undefined`
value in addition to `null`.

SQL `NULL` arguments to a JavaScript UDF will translate to the JavaScript `undefined` value. Likewise, returned
JavaScript `undefined` values translate back to SQL `NULL`. This is true for all data types, including variant.
For non-variant types, a returned JavaScript `null` will also result in a SQL `NULL` value.

Arguments and returned values of the variant type distinguish between JavaScript’s `undefined` and `null` values.
SQL `NULL` continues to translate to JavaScript `undefined` (and JavaScript `undefined` back to SQL `NULL`);
variant JSON `null` translates to JavaScript `null` (and JavaScript `null` back to variant JSON `null`).
An `undefined` value embedded in a JavaScript object (as the value) or array will cause the element to be omitted.

> Create a table with one string and one `NULL` value:
>
> ```
> create or replace table strings (s string);
> insert into strings values (null), ('non-null string');
> ```
>
> Copy
>
> Create a function that converts a string to a `NULL` and a `NULL` to a string:
>
> ```
> CREATE OR REPLACE FUNCTION string_reverse_nulls(s string)
>     RETURNS string
>     LANGUAGE JAVASCRIPT
>     AS '
>     if (S === undefined) {
>         return "string was null";
>     } else
>     {
>         return undefined;
>     }
>     ';
> ```
>
> Copy
>
> Call the function:
>
> ```
> select string_reverse_nulls(s) 
>     from strings
>     order by 1;
> +-------------------------+
> | STRING_REVERSE_NULLS(S) |
> |-------------------------|
> | string was null         |
> | NULL                    |
> +-------------------------+
> ```
>
> Copy
>
> Create a function that shows the difference between passing a SQL `NULL` and passing a variant JSON `null`:
>
> ```
> CREATE OR REPLACE FUNCTION variant_nulls(V VARIANT)
>       RETURNS VARCHAR
>       LANGUAGE JAVASCRIPT
>       AS '
>       if (V === undefined) {
>         return "input was SQL null";
>       } else if (V === null) {
>         return "input was variant null";
>       } else {
>         return V;
>       }
>       ';
> ```
>
> Copy
>
> ```
> select null, 
>        variant_nulls(cast(null as variant)),
>        variant_nulls(PARSE_JSON('null'))
>        ;
> +------+--------------------------------------+-----------------------------------+
> | NULL | VARIANT_NULLS(CAST(NULL AS VARIANT)) | VARIANT_NULLS(PARSE_JSON('NULL')) |
> |------+--------------------------------------+-----------------------------------|
> | NULL | input was SQL null                   | input was variant null            |
> +------+--------------------------------------+-----------------------------------+
> ```
>
> Copy
>
> Create a function that shows the difference between returning `undefined`, `null`, and a variant that contains
> `undefined` and `null` (note that the `undefined` value is removed from the returned variant):
>
> ```
> CREATE OR REPLACE FUNCTION variant_nulls(V VARIANT)
>       RETURNS variant
>       LANGUAGE JAVASCRIPT
>       AS $$
>       if (V == 'return undefined') {
>         return undefined;
>       } else if (V == 'return null') {
>         return null;
>       } else if (V == 3) {
>         return {
>             key1 : undefined,
>             key2 : null
>             };
>       } else {
>         return V;
>       }
>       $$;
> ```
>
> Copy
>
> ```
> select variant_nulls('return undefined'::VARIANT) AS "RETURNED UNDEFINED",
>        variant_nulls('return null'::VARIANT) AS "RETURNED NULL",
>        variant_nulls(3) AS "RETURNED VARIANT WITH UNDEFINED AND NULL; NOTE THAT UNDEFINED WAS REMOVED";
> +--------------------+---------------+---------------------------------------------------------------------------+
> | RETURNED UNDEFINED | RETURNED NULL | RETURNED VARIANT WITH UNDEFINED AND NULL; NOTE THAT UNDEFINED WAS REMOVED |
> |--------------------+---------------+---------------------------------------------------------------------------|
> | NULL               | null          | {                                                                         |
> |                    |               |   "key2": null                                                            |
> |                    |               | }                                                                         |
> +--------------------+---------------+---------------------------------------------------------------------------+
> ```
>
> Copy

### Type conversion within JavaScript[¶](#type-conversion-within-javascript "Link to this heading")

JavaScript will implicitly convert values between many different types. When any value is returned, the value is first converted to
the requested return type before being translated to a SQL value. For example, if a number is returned, but the UDF is declared as
returning a string, this number will converted to a string within JavaScript. Keep in mind that JavaScript programming errors, such as
returning the wrong type, may be hidden by this behavior. In addition, if an error is thrown while converting the value’s type, an
error will result.

### JavaScript Number Range[¶](#javascript-number-range "Link to this heading")

The range for numbers with precision intact is from

> -(2^53 -1)

to

> (2^53 -1)

The range of valid values in Snowflake NUMBER(p, s) and DOUBLE data types is larger. Retrieving a value from Snowflake
and storing it in a JavaScript numeric variable can result in loss of precision. For example:

> ```
> CREATE OR REPLACE FUNCTION num_test(a double)
>   RETURNS string
>   LANGUAGE JAVASCRIPT
> AS
> $$
>   return A;
> $$
> ;
> ```
>
> Copy
>
> ```
> select hash(1) AS a, 
>        num_test(hash(1)) AS b, 
>        a - b;
> +----------------------+----------------------+------------+
> |                    A | B                    |      A - B |
> |----------------------+----------------------+------------|
> | -4730168494964875235 | -4730168494964875000 | -235.00000 |
> +----------------------+----------------------+------------+
> ```
>
> Copy

The first two columns should match, and the third should contain 0.0.

The problem applies to JavaScript user-defined functions (UDFs) and stored procedures.

If you experience the problem in stored procedures when using `getColumnValue()`, you might be able to avoid the
problem by retrieving a value as a string, e.g. with:

```
getColumnValueAsString()
```

Copy

You can then return the string from the stored procedure, and cast the string to a numeric data type in SQL.

## JavaScript errors[¶](#javascript-errors "Link to this heading")

Any errors encountered while executing JavaScript appear to the user as SQL errors. This includes parsing errors, runtime errors,
and uncaught error thrown within the UDF. If the error contains a stacktrace, it will be printed along with the error message. It is
acceptable to throw an error without catching it in order to end the query and produce a SQL error.

When debugging, you may find it useful to print argument values along with the error message so that they appear in the SQL error
message text. For deterministic UDFs, this provides the necessary data to reproduce errors in a local JavaScript engine. One common
pattern is to place an entire JavaScript UDF body in a try-catch block, append argument values to the caught error’s message, and
throw an error with the extended message. You should consider removing such mechanisms prior to deploying UDFs to a production
environment; recording values in error messages may unintentionally reveal sensitive data.

The function can throw and catch pre-defined exceptions or custom exceptions. A simple example of throwing a
custom exception is [here](udf-javascript-scalar-functions.html#label-javascript-udf-throw-custom-exception).

See also [Troubleshooting JavaScript UDFs](udf-javascript-troubleshooting).

## JavaScript UDF security[¶](#javascript-udf-security "Link to this heading")

JavaScript UDFs are designed to be safe and secure by providing several layers of query and data isolation:

* Compute resources within the virtual warehouse that executes a JavaScript UDF are accessible only from within your account
  (i.e. warehouses do not share resources with other Snowflake accounts).
* Table data is encrypted within the virtual warehouse to prevent unauthorized access.
* JavaScript code is executed within a restricted engine, preventing system calls from the JavaScript context (e.g. no network and
  disk access) and constraining the system resources available to the engine, specifically memory.

As a result, JavaScript UDFs can access only the data needed to perform the defined function and can not affect the state of the
underlying system, other than consuming a reasonable amount of memory and processor time.

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

1. [How a JavaScript handler works](#how-a-javascript-handler-works)
2. [JavaScript data types](#javascript-data-types)
3. [JavaScript arguments and returned values](#javascript-arguments-and-returned-values)
4. [JavaScript errors](#javascript-errors)
5. [JavaScript UDF security](#javascript-udf-security)