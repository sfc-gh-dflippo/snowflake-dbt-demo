---
auto_generated: true
description: This guide documents the compatibility between the Snowpark Connect for
  Spark implementation of the Spark DataFrame APIs and native Apache Spark. It is
  intended to help users understand the key differ
last_scraped: '2026-01-14T16:54:58.641895+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-compatibility
title: Snowpark Connect for Spark compatibility guide | Snowflake Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](snowpark-connect-overview.md)

   * [Development clients](snowpark-connect-clients.md)
   * [Cloud service data access](snowpark-connect-file-data.md)
   * [Snowflake SQL execution](snowpark-connect-snowflake-sql.md)
   * [Batch workloads with Snowpark Submit](snowpark-submit.md)
   * [Compatibility](snowpark-connect-compatibility.md)
8. Machine Learning
9. [Snowflake ML](../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../snowpark-container-services/overview.md)
12. [Functions and procedures](../extensibility.md)
13. [Logging, Tracing, and Metrics](../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../streamlit/object-management/billing.md)
      - [Security considerations](../streamlit/object-management/security.md)
      - [Privilege requirements](../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../streamlit/app-development/dependency-management.md)
      - [File organization](../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../streamlit/features/git-integration.md)
      - [External access](../streamlit/features/external-access.md)
      - [Row access policies](../streamlit/features/row-access.md)
      - [Sleep timer](../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../streamlit/troubleshooting.md)
    - [Release notes](../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../snowflake-cli/index.md)
30. [Git](../git/git-overview.md)
31. Drivers
32. [Overview](../drivers.md)
33. [Considerations when drivers reuse sessions](../driver-connections.md)
34. [Scala versions](../scala-version-differences.md)
35. Reference
36. [API Reference](../../api-reference.md)

[Developer](../../developer.md)[Spark workloads on Snowflake](snowpark-connect-overview.md)Compatibility

# Snowpark Connect for Spark compatibility guide[¶](#spconnect-compatibility-guide "Link to this heading")

This guide documents the compatibility between the Snowpark Connect for Spark implementation of the Spark DataFrame APIs and native
Apache Spark. It is intended to help users understand the key differences, unsupported features, and migration considerations when moving
Spark workloads to Snowpark Connect for Spark.

Snowpark Connect for Spark aims to provide a familiar Spark DataFrame API experience on top of the Snowflake execution engine.
However, there are the compatibility gaps described in this topic. This guide highlights those differences to help you plan and adapt
your migration. These might be addressed in a future release.

## DataTypes[¶](#datatypes "Link to this heading")

### Unsupported data types[¶](#unsupported-data-types "Link to this heading")

* [DayTimeIntervalType](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/types/DayTimeIntervalType.html)
* [YearMonthIntervalType](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/types/YearMonthIntervalType.html)
* [UserDefinedTypes](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/types/UserDefinedType.html)

### Implicit data type conversion[¶](#implicit-data-type-conversion "Link to this heading")

When using Snowpark Connect for Spark, keep in mind how data types are handled. Snowpark Connect for Spark implicitly represents `ByteType`,
`ShortType`, and `IntegerType` as `LongType`. This means that while you might define columns or data with
`ByteType`, `ShortType`, or `IntegerType`, the data will be represented and returned by Snowpark Connect for Spark as
`LongType`. Similarly, implicit conversion might also occur for `FloatType` and
`DoubleType` depending on the specific operations and context. The Snowflake execution engine will internally handle data
type compression and may in fact store the data as `Byte` or `Short`, but these are considered implementation details and not exposed to the
end user.

Semantically, this representation will not impact the correctness of your Spark queries.

| Data type from native PySpark | Data type from Snowpark Connect for Spark |
| --- | --- |
| `ByteType` | `LongType` |
| `ShortType` | `LongType` |
| `IntegerType` | `LongType` |
| `LongType` | `LongType` |

The following example shows a difference in how Spark and Snowpark Connect for Spark handle data types in query results.

#### Query[¶](#query "Link to this heading")

```
query = """
    SELECT * FROM VALUES
    (float(1.0), double(1.0), 1.0, "1", true, :code:`NULL`),
    (float(2.0), double(2.0), 2.0, "2", false, :code:`NULL`),
    (float(3.0), double(3.0), :code:`NULL`, "3", false, :code:`NULL`)
    AS tab(a, b, c, d, e, f)
    """
```

Copy

#### Spark[¶](#spark "Link to this heading")

```
spark.sql(query).printSchema()
```

Copy

```
root
 |-- a: float (nullable = false)
 |-- b: double (nullable = false)
 |-- c: decimal(2,1) (nullable = true)
 |-- d: string (nullable = false)
 |-- e: boolean (nullable = false)
 |-- f: void (nullable = true)
```

#### Snowpark Connect for Spark[¶](#spconnect "Link to this heading")

```
snowpark_connect_spark.sql(query).printSchema()
```

Copy

```
root
 |-- a: double (nullable = false)
 |-- b: double (nullable = false)
 |-- c: decimal (nullable = true)
 |-- d: string (nullable = false)
 |-- e: boolean (nullable = true)
 |-- f: string (nullable = true)
```

### `NullType` nuance[¶](#nulltype-nuance "Link to this heading")

Snowpark Connect for Spark doesn’t support the [NullType](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.types.NullType.html)
datatype, which is a supported data type in Spark. This causes behavior changes when using `Null` or `None` in dataframes.

In Spark, a literal `NULL` (for example, with `lit(None)`) is automatically inferred as a `NullType`. In Snowpark Connect for Spark, it is inferred as a
`StringType` during schema inference.

```
df = self.spark.range(1).select(lit(None).alias("null_col"))
field = df.schema["null_col"]

# Spark: StructField('null_col', :code:`NullType`(), True)
# Snowpark Connect for Spark: StructField('null_col', :code:`StringType`(), True)
```

Copy

### Structured data types in `ArrayType`, `MapType`, and `ObjectType`[¶](#structured-data-types-in-arraytype-maptype-and-objecttype "Link to this heading")

While structured type support is not available by default in Snowpark Connect for Spark, `ARRAY`, `MAP` and `Object` datatypes are
treated as generic, untyped collections. This means there is no enforcement of element types, field names, schema, or nullability, unlike
what would be provided by structured type support.

If you have a dependency on this support, please work with your account team to enable this feature for your account.

## Unsupported Spark APIs[¶](#unsupported-spark-apis "Link to this heading")

The following are the APIs supported by classic Spark and Spark Connect but not supported in Snowpark Connect for Spark.

* [Dataframe.hint](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.hint.html):
  Snowpark Connect for Spark ignores any hint that is set on a dataframe. The Snowflake query optimizer automatically determines the
  most efficient execution strategy.
* [DataFrame.repartition](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.repartition.html):
  This is a no-op in Snowpark Connect for Spark. Snowflake automatically manages data distribution and partitioning across its distributed
  computing infrastructure.
* [pyspark.RDD](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html): RDD APIs are not supported in
  Spark Connect (including Snowpark Connect for Spark).
* [pyspark.ml](https://spark.apache.org/docs/latest/api/python/reference/pyspark.ml.html)
* [pyspark streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)

## UDF differences[¶](#udf-differences "Link to this heading")

### `StructType` differences[¶](#structtype-differences "Link to this heading")

When Spark converts a `StructType` to be used in a user-defined function (UDF), it converts it to a `tuple` type in Python. Snowpark Connect for Spark will convert a
`StructType` into a `dict` type in Python. This has fundamental differences in element access and output.

* Spark will access indexes with 0, 1, 2, 3, and so on.
* Snowpark Connect for Spark will access indexes using ‘\_1’, ‘\_2’, and so on.

```
def f(e):
    return e[0]

    df = self.spark.createDataFrame([((1.0, 1.0), (1, 1))], ["c1", "c2"])
    result = df.select("*", udf(f, DoubleType())("c1"))

# This results in an index access issue. Workaround is to use _1, _2 as indicies.
# Workaround:

def f(e):
    return e['_1']

row = (
    self.spark.range(1)
    .selectExpr("struct(1, 2) as struct")
    .select(
        udf(lambda x: x, "struct<col1:int,col2:int>")("struct"),
    )
    .first()
)

self.assertEquals(row[0], Row(col1=1, col2=2))

# Spark: Row(col1=1, col2=2)

# Snowpark Connect for Spark: {'col1': 1, 'col2': 2}
```

Copy

### Iterator Type in UDFs[¶](#iterator-type-in-udfs "Link to this heading")

Iterator isn’t supported as a return type or as an input type.

```
# This will not work
def func(iterator):
  for _ in iterator:
              ...

df = self.spark.range(10)
actual = df.repartition(1).mapInArrow(func, "a long").collect()
```

Copy

### Importing files to a Python UDF[¶](#importing-files-to-a-python-udf "Link to this heading")

With Snowpark Connect for Spark, you can specify external libraries and files in Python UDFs. Snowflake includes Python files and archives in your code’s
execution context. You can import functions from these included files in a UDF without additional steps. This dependency-handling behavior
works as described in [Creating a Python UDF with code uploaded from a stage](../udf/python/udf-python-creating.html#label-udf-python-stage).

To include external libraries and files, you provide stage paths to the files as the value of the configuration setting
`snowpark.connect.udf.imports`. The configuration value should be an array of stage paths to the files, where the paths are
separated by commas.

Code in the following example includes two files in the UDF’s execution context. The UDF imports functions from these files and uses them
in its logic.

```
# Files need to be previously staged
spark.conf.set("snowpark.connect.udf.imports", "[@stage/library.py, @other_lib.zip]")

@udf(returnType = StringType())
def import_example(input: str) -> str:
  from library import first_function
  from other_lib.custom import second_function

  return first_function(input) + second_function(input)

spark.range(1).select(import_read_example("example_string")).show()
```

Copy

You can use the `snowpark.connect.udf.imports` setting to include other kinds of files as well, such as those with data your code
needs to read. Note that when you do this, your code should only read from the included files; any writes to such files will be lost after
the function’s execution ends.

```
# Files need to be previously staged
spark.conf.set("snowpark.connect.udf.imports", "[@stage/data.csv]")

@udf(returnType = StringType())
def import_read_example(file_name: str) -> str:
  with open(file_name) as f:
    return f.read()

spark.range(1).select(import_read_example("data.csv")).show()
```

Copy

## Lambda function limitations[¶](#lambda-function-limitations "Link to this heading")

User-defined functions (UDFs) are not supported within lambda expressions. This includes both custom UDFs and
certain built-in functions whose underlying implementation relies on Snowflake UDFs. Attempting to use a UDF inside a lambda expression
will result in an error.

```
df = spark.createDataFrame([({"a": 123},)], ("data",))
df.select(map_filter("data", lambda _, v: bit_count(v) > 3)).show() # does not work, since `bit_count` is implemented with UDF
```

Copy

## Temporary views[¶](#temporary-views "Link to this heading")

By default, Snowpark Connect for Spark does not create a temporary view in Snowflake. You can specify that Snowpark Connect for Spark creates a temporary view by
setting the configuration parameter `snowpark.connect.temporary.views.create_in_snowflake` to `true`.

If the parameter is set to `false`, Snowpark Connect for Spark stores views as DataFrames without creating a Snowflake view. This helps to prevent
the issue that can occur when the view definition SQL created from Spark Connect request exceeds Snowflake view size limit (95KB).

Temporary views are normally visible when using Spark Connect Catalog API. However, they are not accessible when called from SQL statements
with configuration `snowpark.connect.sql.passthrough` set to `true`. To create Snowflake temporary views, set configuration
`snowpark.connect.temporary.views.create_in_snowflake` to `true`.

## Data sources[¶](#data-sources "Link to this heading")

| Data source | Compatibility issues compared with PySpark |
| --- | --- |
| Avro | File type is not supported. |
| CSV | Save mode is not supported for the following: `Append`, `Ignore`.  The following options are not supported: `encoding`, `quote`, `quoteAll`, `escape`, `escapeQuotes`, `comment`, `preferDate`, `enforceSchema`, `ignoreLeadingWhiteSpace`, `ignoreTrailingWhiteSpace`, `nanValue`, `positiveInf`, `negativeInf`, `timestampNTZFormat`, `enableDateTimeParsingFallback`, `maxColumns`, `maxCharsPerColumn`, `mode`, `columnNameOfCorruptRecord`, `charToEscapeQuoteEscaping`, `samplingRatio`, `emptyValue`, `locale`, `lineSep`, `unescapedQuoteHandling`, `compression`. |
| JSON | Save mode not supported for the following: `Append`, `Ignore`.  The following options not supported: `timeZone`, `primitivesAsString`, `prefersDecimal`, `allowComments`, `allowUnquotedFieldNames`, `allowSingleQuotes`, `allowNumericLeadingZeros`, `allowBackslashEscapingAnyCharacter`, `mode`, `columnNameOfCorruptRecord`, `timestampNTZFormat`, `enableDateTimeParsingFallback`, `allowUnquotedControlChars`, `encoding`, `lineSep`, `samplingRatio`, `dropFieldIfAllNull`, `locale`, `allowNonNumericNumbers`, `compression`, `ignoreNullFields`.  Difference in `Show`: If the value of field is string, it would be quoted. An extra “n” character would be shown in result. |
| Orc | File type is not supported. |
| Parquet | Save mode is not supported for the following: `Append`, `Ignore`.  The following options are not supported: `datetimeRebaseMode`, `int96RebaseMode`, `mergeSchema`, `compression`.  Configuration not supported: (ALL) |
| Text | Write mode not supported for the following: `Append`, `Ignore`.  The following options are not supported: `compression`.  The `lineSep` parameter not supported in write. |
| XML | File type is not supported. |
| Snowflake table | Write to table doesn’t need a provider format.  Bucketing and partitioning are not supported.  Storage format and versioning are not supported. |

## Catalog[¶](#catalog "Link to this heading")

### Snowflake Horizon Catalog provider support[¶](#snowflake-horizon-catalog-provider-support "Link to this heading")

* Only Snowflake is supported as a catalog provider.

### Unsupported catalog APIs[¶](#unsupported-catalog-apis "Link to this heading")

* `registerFunction`
* `listFunctions`
* `getFunction`
* `functionExists`
* `createExternalTable`

### Partially supported catalog APIs[¶](#partially-supported-catalog-apis "Link to this heading")

* `createTable` (no external table support)

## Iceberg[¶](#iceberg "Link to this heading")

### Snowflake managed iceberg table[¶](#snowflake-managed-iceberg-table "Link to this heading")

Snowpark Connect for Spark works with Apache Iceberg™ tables, including externally managed Iceberg tables and catalog-linked databases.

#### Read[¶](#read "Link to this heading")

Time travel is not supported, including historical snapshot, branch, and incremental read.

#### Write[¶](#write "Link to this heading")

* Using Spark SQL to create tables is not supported.
* Schema merge is not supported.
* To create the table, you must:

  + Create an external volume.
  + Link the external volume needs to the table creation in either of the following ways:

    - Set the EXTERNAL\_VOLUME to the database.
    - Set `snowpark.connect.iceberg.external_volume` to Spark configuration.

### External managed Iceberg table[¶](#external-managed-iceberg-table "Link to this heading")

#### Read[¶](#id1 "Link to this heading")

* You must create a Snowflake unmanaged table entity.
* Time travel is not supported, including historical snapshot, branch, and incremental read.

#### Write[¶](#id2 "Link to this heading")

* Table creation is not supported.
* Writing to the existing Iceberg table is supported.

## Duplication column names[¶](#duplication-column-names "Link to this heading")

Snowflake does not support duplicate column names.

The following code fails at the view creation step with the following SQL compilation error: `duplicate column name 'foo'`.

```
df = spark.createDataFrame([
(1, 1),
(2, 2)
], ["foo", "foo"])

df.show() # works

df.createTempView("df_view") # Fails with SQL compilation error: duplicate column name 'foo'
```

Copy

To work around this, set the `snowpark.connect.views.duplicate_column_names_handling_mode` configuration option to one the following
values:

* `rename`: A suffix such as `_dedup_1`, `_dedup_2`, and so on will be appended to all of the duplicate column names
  after the first one.
* `drop`: All of the duplicate columns except one will be dropped. This might lead to incorrect results if the columns have
  different values.

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

1. [DataTypes](#datatypes)
2. [Unsupported Spark APIs](#unsupported-spark-apis)
3. [UDF differences](#udf-differences)
4. [Lambda function limitations](#lambda-function-limitations)
5. [Temporary views](#temporary-views)
6. [Data sources](#data-sources)
7. [Catalog](#catalog)
8. [Iceberg](#iceberg)
9. [Duplication column names](#duplication-column-names)