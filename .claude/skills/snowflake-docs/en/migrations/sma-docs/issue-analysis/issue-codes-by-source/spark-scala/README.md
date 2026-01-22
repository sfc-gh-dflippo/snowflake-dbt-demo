---
auto_generated: true
description: 'Message: org.apache.spark.sql.functions.covar_pop has a workaround,
  see documentation for more info'
last_scraped: '2026-01-14T16:51:26.720932+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/issue-analysis/issue-codes-by-source/spark-scala/README
title: 'Snowpark Migration Accelerator: Issue Codes for Spark - Scala | Snowflake
  Documentation'
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../README.md)

        + General

          + [Introduction](../../../general/introduction.md)
          + [Getting started](../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../general/release-notes/README.md)
          + [Roadmap](../../../general/roadmap.md)
        + User guide

          + [Overview](../../../user-guide/overview.md)
          + [Before using the SMA](../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../user-guide/chatbot.md)
          + [Assessment](../../../user-guide/assessment/README.md)
          + [Conversion](../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../approach.md)
          + [Issue code categorization](../../issue-code-categorization.md)
          + [Issue codes by source](../README.md)

            - [General](../general.md)
            - [Python](../python/README.md)
            - [Spark Scala](README.md)
            - [SQL](../sql/README.md)
            - [Pandas](../pandas/README.md)
            - [Snowpark Connect Python](../python/snowpark-connect-codes-python.md)
            - [Snowpark Connect Scala](snowpark-connect-codes-scala.md)
          + [Troubleshooting the output code](../../troubleshooting-the-output-code/README.md)
          + [Workarounds](../../workarounds.md)
          + [Deploying the output code](../../deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../../workspace-estimator/overview.md)
          + [Getting started](../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../support/glossary.md)
          + [Contact us](../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Issue analysis[Issue codes by source](../README.md)Spark Scala

# Snowpark Migration Accelerator: Issue Codes for Spark - Scala[¶](#snowpark-migration-accelerator-issue-codes-for-spark-scala "Link to this heading")

## SPRKSCL1126[¶](#sprkscl1126 "Link to this heading")

Message: org.apache.spark.sql.functions.covar\_pop has a workaround, see documentation for more info

Category: Warning

### Description[¶](#description "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.covar\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#covar_pop(columnName1:String,columnName2:String):org.apache.spark.sql.Column) function, which has a workaround.

**Input**

Below is an example of the `org.apache.spark.sql.functions.covar_pop` function, first used with column names as the arguments and then with column objects.

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

val result1 = df.select(covar_pop("column1", "column2").as("covariance_pop"))
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1126` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

/*EWI: SPRKSCL1126 => org.apache.spark.sql.functions.covar_pop has a workaround, see documentation for more info*/
val result1 = df.select(covar_pop("column1", "column2").as("covariance_pop"))
/*EWI: SPRKSCL1126 => org.apache.spark.sql.functions.covar_pop has a workaround, see documentation for more info*/
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [covar\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#covar_pop(column1:com.snowflake.snowpark.Column,column2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

val result1 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

Copy

#### Additional recommendations[¶](#additional-recommendations "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1112[¶](#sprkscl1112 "Link to this heading")

Message: ***spark element*** is not supported

Category: Conversion error

### Description[¶](#id1 "Link to this heading")

This issue appears when the SMA detects the use of a Spark element that is not supported by Snowpark, and it does not have its own error code associated with it. This is a generic error code used by the SMA for any unsupported Spark element.

#### Scenario[¶](#scenario "Link to this heading")

**Input**

Below is an example of a Spark element that is not supported by Snowpark, and therefore it generates this EWI.

```
val df = session.range(10)
val result = df.isLocal
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1112` to the output code to let you know that this element is not supported by Snowpark.

```
val df = session.range(10)
/*EWI: SPRKSCL1112 => org.apache.spark.sql.Dataset.isLocal is not supported*/
val result = df.isLocal
```

Copy

**Recommended fix**

Since this is a generic error code that applies to a range of unsupported functions, there is not a single and specific fix. The appropriate action will depend on the particular element in use.

Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It only means that the SMA itself cannot find the solution.

#### Additional recommendations[¶](#id2 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1143[¶](#sprkscl1143 "Link to this heading")

Message: An error occurred when loading the symbol table

Category: Conversion error

### Description[¶](#id3 "Link to this heading")

This issue appears when there is an error loading the symbols of the SMA symbol table. The symbol table is part of the underlying architecture of the SMA allowing for more complex conversions.

#### Additional recommendations[¶](#id4 "Link to this heading")

* This is unlikely to be an error in the source code itself, but rather is an error in how the SMA processes the source code. The best resolution would be to post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1153[¶](#sprkscl1153 "Link to this heading")

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.3.2](../../../general/release-notes/README.html#spark-conversion-core-version-4-3-2)

Message: org.apache.spark.sql.functions.max has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id5 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.max](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#max(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id6 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.max` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
val result1 = df.select(max("value"))
val result2 = df.select(max(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1153` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
/*EWI: SPRKSCL1153 => org.apache.spark.sql.functions.max has a workaround, see documentation for more info*/
val result1 = df.select(max("value"))
/*EWI: SPRKSCL1153 => org.apache.spark.sql.functions.max has a workaround, see documentation for more info*/
val result2 = df.select(max(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [max](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#max(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
val result1 = df.select(max(col("value")))
val result2 = df.select(max(col("value")))
```

Copy

#### Additional recommendations[¶](#id7 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1102[¶](#sprkscl1102 "Link to this heading")

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](../../../general/release-notes/README)

Message:Explode is not supported

Category: Warning

### Description[¶](#id8 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.explode](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#explode(e:org.apache.spark.sql.Column):org.apache.spark.sql.Column) function, which is not supported by Snowpark.

#### Scenario[¶](#id9 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.explode` function used to get the consolidated information of the array fields of the dataset.

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

    dfExplode.select(explode(dfExplode("Translation").alias("exploded")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1102` to the output code to let you know that this function is not supported by Snowpark.

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

    /*EWI: SPRKSCL1102 => Explode is not supported */
    dfExplode.select(explode(dfExplode("Translation").alias("exploded")))
```

Copy

**Recommended Fix**

Since explode is not supported by Snowpark, the function [flatten](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/DataFrame.html#flatten(input:com.snowflake.snowpark.Column):com.snowflake.snowpark.DataFrame) could be used as a substitute.

The following fix creates flatten of the dfExplode dataframe, then makes the query to replicate the result in Spark.

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

     var dfFlatten = dfExplode.flatten(col("Translation")).alias("exploded")
                              .select(col("exploded.value").alias("Translation"))
```

Copy

#### Additional recommendations[¶](#id10 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1136[¶](#sprkscl1136 "Link to this heading")

Warning

This issue code is **deprecated** since [Spark Conversion Core 4.3.2](../../../general/release-notes/README.html#spark-conversion-core-version-4-3-2)

Message: org.apache.spark.sql.functions.min has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id11 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.min](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#min(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id12 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.min` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(min("value"))
val result2 = df.select(min(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1136` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
/*EWI: SPRKSCL1136 => org.apache.spark.sql.functions.min has a workaround, see documentation for more info*/
val result1 = df.select(min("value"))
/*EWI: SPRKSCL1136 => org.apache.spark.sql.functions.min has a workaround, see documentation for more info*/
val result2 = df.select(min(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [min](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#min(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that takes a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(min(col("value")))
val result2 = df.select(min(col("value")))
```

Copy

#### Additional recommendations[¶](#id13 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1167[¶](#sprkscl1167 "Link to this heading")

Message: Project file not found on input folder

Category: Warning

### Description[¶](#id14 "Link to this heading")

This issue appears when the SMA detects that input folder do not have any project configuration file. The project configuration files supported by the SMA are:

* build.sbt
* build.gradle
* pom.xml

#### Additional recommendations[¶](#id15 "Link to this heading")

* Include a configuration project file on input folder.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1147[¶](#sprkscl1147 "Link to this heading")

Message: org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id16 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.tanh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#tanh(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id17 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.tanh` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
val result1 = df.withColumn("tanh_value", tanh("value"))
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1147` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
/*EWI: SPRKSCL1147 => org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info*/
val result1 = df.withColumn("tanh_value", tanh("value"))
/*EWI: SPRKSCL1147 => org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info*/
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [tanh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#tanh(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
val result1 = df.withColumn("tanh_value", tanh(col("value")))
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

Copy

#### Additional recommendations[¶](#id18 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1116[¶](#sprkscl1116 "Link to this heading")

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.40.1](../../../general/release-notes/README)

Message: org.apache.spark.sql.functions.split has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id19 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.split](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#split(str:org.apache.spark.sql.Column,pattern:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id20 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI.

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
val result1 = df.withColumn("split_values", split(col("values"), ","))
val result2 = df.withColumn("split_values", split(col("values"), ",", 0))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1116` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
/*EWI: SPRKSCL1116 => org.apache.spark.sql.functions.split has a workaround, see documentation for more info*/
val result1 = df.withColumn("split_values", split(col("values"), ","))
/*EWI: SPRKSCL1116 => org.apache.spark.sql.functions.split has a workaround, see documentation for more info*/
val result2 = df.withColumn("split_values", split(col("values"), ",", 0))
```

Copy

**Recommended fix**

For the Spark overload that receives two arguments, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function as a workaround.

The overload that receives three arguments is not yet supported by Snowpark and there is no workaround.

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
val result1 = df.withColumn("split_values", split(col("values"), lit(",")))
val result2 = df.withColumn("split_values", split(col("values"), ",", 0)) // This overload is not supported yet
```

Copy

#### Additional recommendations[¶](#id21 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1122[¶](#sprkscl1122 "Link to this heading")

Message: org.apache.spark.sql.functions.corr has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id22 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.corr](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#corr(columnName1:String,columnName2:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id23 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.corr` function, first used with column names as the arguments and then with column objects.

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

val result1 = df.select(corr("col1", "col2"))
val result2 = df.select(corr(col("col1"), col("col2")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1122` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

/*EWI: SPRKSCL1122 => org.apache.spark.sql.functions.corr has a workaround, see documentation for more info*/
val result1 = df.select(corr("col1", "col2"))
/*EWI: SPRKSCL1122 => org.apache.spark.sql.functions.corr has a workaround, see documentation for more info*/
val result2 = df.select(corr(col("col1"), col("col2")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [corr](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#corr(column1:com.snowflake.snowpark.Column,column2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives two column objects as arguments. For that reason, the Spark overload that receives column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

val result1 = df.select(corr(col("col1"), col("col2")))
val result2 = df.select(corr(col("col1"), col("col2")))
```

Copy

#### Additional recommendations[¶](#id24 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1173[¶](#sprkscl1173 "Link to this heading")

Message: SQL embedded code cannot be processed.

Category: Warning.

### Description[¶](#id25 "Link to this heading")

This issue appears when the SMA detects a SQL-embedded code that can not be processed. Then, the SQL-embedded code can not be converted to Snowflake.

#### Scenario[¶](#id26 "Link to this heading")

**Input**

Below is an example of a SQL-embedded code that can not be processed.

```
spark.sql("CREATE VIEW IF EXISTS My View" + "AS Select * From my Table WHERE date < current_date()")
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1173` to the output code to let you know that the SQL-embedded code can not be processed.

```
/*EWI: SPRKSCL1173 => SQL embedded code cannot be processed.*/
spark.sql("CREATE VIEW IF EXISTS My View" + "AS Select * From my Table WHERE date < current_date()")
```

Copy

**Recommended fix**

Make sure that the SQL-embedded code is a string without interpolations, variables or string concatenations.

#### Additional recommendations[¶](#id27 "Link to this heading")

* You can find more information about SQL-embedded [here](../../../translation-reference/sql-embedded-code).
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1163[¶](#sprkscl1163 "Link to this heading")

Message: The element is not a literal and can’t be evaluated.

Category: Conversion error.

### Description[¶](#id28 "Link to this heading")

This issue occurs when the current processing element is not a literal, then it can not be evaluated by SMA.

#### Scenario[¶](#id29 "Link to this heading")

**Input**

Below is an example when element to process is not a literal and it can not be evaluated by SMA.

```
val format_type = "csv"
spark.read.format(format_type).load(path)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1163` to the output code to let you know that `format_type` parameter is not a literal and it can not be evaluated by the SMA.

```
/*EWI: SPRKSCL1163 => format_type is not a literal and can't be evaluated*/
val format_type = "csv"
spark.read.format(format_type).load(path)
```

Copy

**Recommended fix**

* Make sure that a value of the variable is a valid one in order to avoid unexpected behaviors.

#### Additional recommendations[¶](#id30 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1132[¶](#sprkscl1132 "Link to this heading")

Message: org.apache.spark.sql.functions.grouping\_id has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id31 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.grouping\_id](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#grouping_id(colName:String,colNames:String*):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id32 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.grouping_id` function, first used with multiple column name as arguments and then with column objects.

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id("store", "product"))
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1132` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

/*EWI: SPRKSCL1132 => org.apache.spark.sql.functions.grouping_id has a workaround, see documentation for more info*/
val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id("store", "product"))
/*EWI: SPRKSCL1132 => org.apache.spark.sql.functions.grouping_id has a workaround, see documentation for more info*/
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [grouping\_id](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#grouping_id(cols:com.snowflake.snowpark.Column*):com.snowflake.snowpark.Column) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives multiple column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

Copy

#### Additional recommendations[¶](#id33 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1106[¶](#sprkscl1106 "Link to this heading")

Warning

This issue code has been **deprecated**

Message: Writer option is not supported.

Category: Conversion error.

### Description[¶](#id34 "Link to this heading")

This issue appears when the tool detects, in writer statement, the usage of an option not supported by Snowpark.

#### Scenario[¶](#id35 "Link to this heading")

**Input**

Below is an example of the [org.apache.spark.sql.DataFrameWriter.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html) used to add options to a writer statement.

```
df.write.format("net.snowflake.spark.snowflake").option("dbtable", tablename)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1106` to the output code to let you know that the option method is not supported by Snowpark.

```
df.write.saveAsTable(tablename)
/*EWI: SPRKSCL1106 => Writer option is not supported .option("dbtable", tablename)*/
```

Copy

**Recommended fix**

There is no recommended fix for this scenario

#### Additional recommendations[¶](#id36 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1157[¶](#sprkscl1157 "Link to this heading")

Message: org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id37 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.kurtosis](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#kurtosis(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id38 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.kurtosis` function that generates this EWI. In this example, the `kurtosis` function is used to calculate the kurtosis of selected column.

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = kurtosis(col("elements"))
val result2 = kurtosis("elements")
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1157` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("1", "2", "3").toDF("elements")
/*EWI: SPRKSCL1157 => org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info*/
val result1 = kurtosis(col("elements"))
/*EWI: SPRKSCL1157 => org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info*/
val result2 = kurtosis("elements")
```

Copy

**Recommended fix**

Snowpark has an equivalent [kurtosis](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#kurtosis(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = kurtosis(col("elements"))
val result2 = kurtosis(col("elements"))
```

Copy

#### Additional recommendations[¶](#id39 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1146[¶](#sprkscl1146 "Link to this heading")

Message: org.apache.spark.sql.functions.tan has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id40 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.tan](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#tan(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id41 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.tan` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
val result1 = df.withColumn("tan_value", tan("angle"))
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1146` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
/*EWI: SPRKSCL1146 => org.apache.spark.sql.functions.tan has a workaround, see documentation for more info*/
val result1 = df.withColumn("tan_value", tan("angle"))
/*EWI: SPRKSCL1146 => org.apache.spark.sql.functions.tan has a workaround, see documentation for more info*/
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [tan](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#tan(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
val result1 = df.withColumn("tan_value", tan(col("angle")))
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

Copy

#### Additional recommendations[¶](#id42 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1117[¶](#sprkscl1117 "Link to this heading")

Warning

This issue code is **deprecated** since [Spark Conversion Core 2.40.1](../../../general/release-notes/README)

Message: org.apache.spark.sql.functions.translate has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id43 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.translate](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#translate(src:org.apache.spark.sql.Column,matchingString:String,replaceString:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id44 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.translate` function that generates this EWI. In this example, the `translate` function is used to replace the characters **‘a’**, **‘e’** and **‘o’** in each word with **‘1’**, **‘2’** and **‘3’**, respectively.

```
val df = Seq("hello", "world", "scala").toDF("word")
val result = df.withColumn("translated_word", translate(col("word"), "aeo", "123"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1117` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("hello", "world", "scala").toDF("word")
/*EWI: SPRKSCL1117 => org.apache.spark.sql.functions.translate has a workaround, see documentation for more info*/
val result = df.withColumn("translated_word", translate(col("word"), "aeo", "123"))
```

Copy

**Recommended fix**

As a workaround, you can convert the second and third argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function.

```
val df = Seq("hello", "world", "scala").toDF("word")
val result = df.withColumn("translated_word", translate(col("word"), lit("aeo"), lit("123")))
```

Copy

#### Additional recommendations[¶](#id45 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1123[¶](#sprkscl1123 "Link to this heading")

Message: org.apache.spark.sql.functions.cos has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id46 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.cos](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#cos(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id47 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.cos` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
val result1 = df.withColumn("cosine_value", cos("angle_radians"))
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1123` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
/*EWI: SPRKSCL1123 => org.apache.spark.sql.functions.cos has a workaround, see documentation for more info*/
val result1 = df.withColumn("cosine_value", cos("angle_radians"))
/*EWI: SPRKSCL1123 => org.apache.spark.sql.functions.cos has a workaround, see documentation for more info*/
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [cos](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#cos(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
val result1 = df.withColumn("cosine_value", cos(col("angle_radians")))
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

Copy

#### Additional recommendations[¶](#id48 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1172[¶](#sprkscl1172 "Link to this heading")

Message: Snowpark does not support StructFiled with metadata parameter.

Category: Warning

### Description[¶](#id49 "Link to this heading")

This issue appears when the SMA detects that [org.apache.spark.sql.types.StructField.apply](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/StructField.html) with [org.apache.spark.sql.types.Metadata](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/Metadata.html) as parameter. This is because Snowpark does not supported the metadata parameter.

#### Scenario[¶](#id50 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.types.StructField.apply` function that generates this EWI. In this example, the `apply` function is used to generate and instance of StructField.

```
val result = StructField("f1", StringType(), True, metadata)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1172` to the output code to let you know that metadata parameter is not supported by Snowflake.

```
/*EWI: SPRKSCL1172 => Snowpark does not support StructFiled with metadata parameter.*/
val result = StructField("f1", StringType(), True, metadata)
```

Copy

**Recommended fix**

Snowpark has an equivalent [com.snowflake.snowpark.types.StructField.apply](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/types/StructField$.html#apply(name:String,dataType:com.snowflake.snowpark.types.DataType):com.snowflake.snowpark.types.StructField) function that receives three parameters. Then, as workaround, you can try to remove the metadata argument.

```
val result = StructField("f1", StringType(), True, metadata)
```

Copy

#### Additional recommendations[¶](#id51 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1162[¶](#sprkscl1162 "Link to this heading")

Note

This issue code has been **deprecated**

Message: An error occurred when extracting the dbc files.

Category: Warning.

### Description[¶](#id52 "Link to this heading")

This issue appears when a dbc file cannot be extracted. This warning could be caused by one or more of the following reasons: Too heavy, inaccessible, read-only, etc.

#### Additional recommendations[¶](#id53 "Link to this heading")

* As a workaround, you can check the size of the file if it is too heavy to be processed. Also, analyze whether the tool can access it to avoid any access issues.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1133[¶](#sprkscl1133 "Link to this heading")

Message: org.apache.spark.sql.functions.least has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id54 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.least](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#least(columnName:String,columnNames:String*):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id55 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.least` function, first used with multiple column name as arguments and then with column objects.

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
val result1 = df.withColumn("least", least("value1", "value2", "value3"))
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1133` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
/*EWI: SPRKSCL1133 => org.apache.spark.sql.functions.least has a workaround, see documentation for more info*/
val result1 = df.withColumn("least", least("value1", "value2", "value3"))
/*EWI: SPRKSCL1133 => org.apache.spark.sql.functions.least has a workaround, see documentation for more info*/
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [least](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#least(exprs:com.snowflake.snowpark.Column*):com.snowflake.snowpark.Column) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives multiple column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
val result1 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

Copy

#### Additional recommendations[¶](#id56 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1107[¶](#sprkscl1107 "Link to this heading")

Warning

This issue code has been **deprecated**

Message: Writer save is not supported.

Category: Conversion error.

### Description[¶](#id57 "Link to this heading")

This issue appears when the tool detects, in writer statement, the usage of a writer save method that is not supported by Snowpark.

#### Scenario[¶](#id58 "Link to this heading")

**Input**

Below is an example of the [org.apache.spark.sql.DataFrameWriter.save](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html) used to save the DataFrame content.

```
df.write.format("net.snowflake.spark.snowflake").save()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1107` to the output code to let you know that the save method is not supported by Snowpark.

```
df.write.saveAsTable(tablename)
/*EWI: SPRKSCL1107 => Writer method is not supported .save()*/
```

Copy

**Recommended fix**

There is no recommended fix for this scenario

#### Additional recommendations[¶](#id59 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1156[¶](#sprkscl1156 "Link to this heading")

Message: org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id60 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.degrees](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#degrees(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id61 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.degrees` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
val result1 = df.withColumn("degrees", degrees("radians"))
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1156` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
/*EWI: SPRKSCL1156 => org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info*/
val result1 = df.withColumn("degrees", degrees("radians"))
/*EWI: SPRKSCL1156 => org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info*/
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [degrees](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#degrees(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
val result1 = df.withColumn("degrees", degrees(col("radians")))
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

Copy

#### Additional recommendations[¶](#id62 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1127[¶](#sprkscl1127 "Link to this heading")

Message: org.apache.spark.sql.functions.covar\_samp has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id63 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.covar\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#covar_samp(columnName1:String,columnName2:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id64 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.covar_samp` function, first used with column names as the arguments and then with column objects.

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

val result1 = df.select(covar_samp("value1", "value2").as("sample_covariance"))
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1127` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

/*EWI: SPRKSCL1127 => org.apache.spark.sql.functions.covar_samp has a workaround, see documentation for more info*/
val result1 = df.select(covar_samp("value1", "value2").as("sample_covariance"))
/*EWI: SPRKSCL1127 => org.apache.spark.sql.functions.covar_samp has a workaround, see documentation for more info*/
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [covar\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#covar_samp(column1:com.snowflake.snowpark.Column,column2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

val result1 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

Copy

#### Additional recommendations[¶](#id65 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1113[¶](#sprkscl1113 "Link to this heading")

Message: org.apache.spark.sql.functions.next\_day has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id66 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.next\_day](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#next_day(date:org.apache.spark.sql.Column,dayOfWeek:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id67 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.next_day` function, first used with a string as the second argument and then with a column object.

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
val result1 = df.withColumn("next_monday", next_day(col("date"), "Mon"))
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1113` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
/*EWI: SPRKSCL1113 => org.apache.spark.sql.functions.next_day has a workaround, see documentation for more info*/
val result1 = df.withColumn("next_monday", next_day(col("date"), "Mon"))
/*EWI: SPRKSCL1113 => org.apache.spark.sql.functions.next_day has a workaround, see documentation for more info*/
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [next\_day](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#next_day(date:com.snowflake.snowpark.Column,dayOfWeek:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives a column object and a string, you can convert the string into a column object using the [com.snowflake.snowpark.functions.lit](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#lit(literal:Any):org.apache.spark.sql.Column) function as a workaround.

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
val result1 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

Copy

#### Additional recommendations[¶](#id68 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1002[¶](#sprkscl1002 "Link to this heading")

Message: This code section has recovery from parsing errors ***statement***

Category: Parsing error.

### Description[¶](#id69 "Link to this heading")

This issue appears when the SMA detects some statement that cannot correctly read or understand in the code of a file, it is called as **parsing error**, however the SMA can recovery from that parsing error and continue analyzing the code of the file. In this case, the SMA is able to process the code of the file without errors.

#### Scenario[¶](#id70 "Link to this heading")

**Input**

Below is an example of invalid Scala code where the SMA can recovery.

```
Class myClass {

    def function1() & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1002` to the output code to let you know that the code of the file has parsing errors, however the SMA can recovery from that error and continue analyzing the code of the file.

```
class myClass {

    def function1();//EWI: SPRKSCL1002 => Unexpected end of declaration. Failed token: '&' @(3,21).
    & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

Copy

**Recommended fix**

Since the message pinpoint the error in the statement you can try to identify the invalid syntax and remove it or comment out that statement to avoid the parsing error.

```
Class myClass {

    def function1() = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

Copy

```
Class myClass {

    // def function1() & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

Copy

#### Additional recommendations[¶](#id71 "Link to this heading")

* Check that the code of the file is a valid Scala code.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1142[¶](#sprkscl1142 "Link to this heading")

Message: ***spark element*** is not defined

Category: Conversion error

### Description[¶](#id72 "Link to this heading")

This issue appears when the SMA could not determine an appropriate mapping status for the given element. This means, the SMA doesn’t know yet if this element is supported or not by Snowpark. Please note, this is a generic error code used by the SMA for any not defined element.

#### Scenario[¶](#id73 "Link to this heading")

**Input**

Below is an example of a function for which the SMA could not determine an appropriate mapping status, and therefore it generated this EWI. In this case, you should assume that `notDefinedFunction()` is a valid Spark function and the code runs.

```
val df = session.range(10)
val result = df.notDefinedFunction()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1142` to the output code to let you know that this element is not defined.

```
val df = session.range(10)
/*EWI: SPRKSCL1142 => org.apache.spark.sql.DataFrame.notDefinedFunction is not defined*/
val result = df.notDefinedFunction()
```

Copy

**Recommended fix**

To try to identify the problem, you can perform the following validations:

* Check if it is a valid Spark element.
* Check if the element has the correct syntax and it is spelled correctly.
* Check if you are using a Spark version supported by the SMA.

If this is a valid Spark element, please report that you encountered a conversion error on that particular element using the [Report an Issue](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue) option of the SMA and include any additional information that you think may be helpful.

Please note that if an element is not defined by the SMA, it does not mean necessarily that it is not supported by Snowpark. You should check the [Snowpark Documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/index.html) to verify if an equivalent element exist.

#### Additional recommendations[¶](#id74 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1152[¶](#sprkscl1152 "Link to this heading")

Message: org.apache.spark.sql.functions.variance has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id75 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.variance](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#variance(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id76 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.variance` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
val result1 = df.select(variance("value"))
val result2 = df.select(variance(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1152` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
/*EWI: SPRKSCL1152 => org.apache.spark.sql.functions.variance has a workaround, see documentation for more info*/
val result1 = df.select(variance("value"))
/*EWI: SPRKSCL1152 => org.apache.spark.sql.functions.variance has a workaround, see documentation for more info*/
val result2 = df.select(variance(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [variance](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#variance(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
val result1 = df.select(variance(col("value")))
val result2 = df.select(variance(col("value")))
```

Copy

#### Additional recommendations[¶](#id77 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1103[¶](#sprkscl1103 "Link to this heading")

This issue code has been **deprecated**

Message: SparkBuilder method is not supported ***method name***

Category: Conversion Error

### Description[¶](#id78 "Link to this heading")

This issue appears when the SMA detects a method that is not supported by Snowflake in the SparkBuilder method chaining. Therefore, it might affects the migration of the reader statement.

The following are the not supported SparkBuilder methods:

* master
* appName
* enableHiveSupport
* withExtensions

#### Scenario[¶](#id79 "Link to this heading")

**Input**

Below is an example of a SparkBuilder method chaining with many methods are not supported by Snowflake.

```
val spark = SparkSession.builder()
           .master("local")
           .appName("testApp")
           .config("spark.sql.broadcastTimeout", "3600")
           .enableHiveSupport()
           .getOrCreate()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1103` to the output code to let you know that master, appName and enableHiveSupport methods are not supported by Snowpark. Then, it might affects the migration of the Spark Session statement.

```
val spark = Session.builder.configFile("connection.properties")
/*EWI: SPRKSCL1103 => SparkBuilder Method is not supported .master("local")*/
/*EWI: SPRKSCL1103 => SparkBuilder Method is not supported .appName("testApp")*/
/*EWI: SPRKSCL1103 => SparkBuilder method is not supported .enableHiveSupport()*/
.create
```

Copy

**Recommended fix**

To create the session is required to add the proper Snowflake Snowpark configuration.

In this example a configs variable is used.

```
    val configs = Map (
      "URL" -> "https://<myAccount>.snowflakecomputing.com:<port>",
      "USER" -> <myUserName>,
      "PASSWORD" -> <myPassword>,
      "ROLE" -> <myRole>,
      "WAREHOUSE" -> <myWarehouse>,
      "DB" -> <myDatabase>,
      "SCHEMA" -> <mySchema>
    )
    val session = Session.builder.configs(configs).create
```

Copy

Also is recommended the use of a configFile (profile.properties) with the connection information:

```
## profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

Copy

And with the `Session.builder.configFile` the session can be created:

```
val session = Session.builder.configFile("/path/to/properties/file").create
```

Copy

### Additional recommendations[¶](#id80 "Link to this heading")

* [Developer guide for create a session.](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-session)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1137[¶](#sprkscl1137 "Link to this heading")

Message: org.apache.spark.sql.functions.sin has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id81 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sin](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#sin(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id82 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.sin` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
val result1 = df.withColumn("sin_value", sin("angle"))
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1137` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
/*EWI: SPRKSCL1137 => org.apache.spark.sql.functions.sin has a workaround, see documentation for more info*/
val result1 = df.withColumn("sin_value", sin("angle"))
/*EWI: SPRKSCL1137 => org.apache.spark.sql.functions.sin has a workaround, see documentation for more info*/
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [sin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#sin(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
val result1 = df.withColumn("sin_value", sin(col("angle")))
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

Copy

#### Additional recommendations[¶](#id83 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1166[¶](#sprkscl1166 "Link to this heading")

Note

This issue code has been **deprecated**

Message: org.apache.spark.sql.DataFrameReader.format is not supported.

Category: Warning.

### Description[¶](#id84 "Link to this heading")

This issue appears when the [org.apache.spark.sql.DataFrameReader.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html#format(source:String):org.apache.spark.sql.DataFrameReader) has an argument that is not supported by Snowpark.

#### Scenarios[¶](#scenarios "Link to this heading")

There are some scenarios depending on the type of format you are trying to load. It can be a `supported`, or `non-supported` format.

##### Scenario 1[¶](#scenario-1 "Link to this heading")

**Input**

The tool analyzes the type of format that is trying to load, the supported formats are:

* `csv`
* `json`
* `orc`
* `parquet`
* `text`

The below example shows how the tool transforms the `format` method when passing a `csv` value.

```
spark.read.format("csv").load(path)
```

Copy

**Output**

The tool transforms the `format` method into a `csv` method call when load function has one parameter.

```
spark.read.csv(path)
```

Copy

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2[¶](#scenario-2 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

```
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

Copy

**Output**

The tool shows the EWI `SPRKSCL1166` indicating that the value `net.snowflake.spark.snowflake` is not supported.

```
/*EWI: SPRKSCL1166 => The parameter net.snowflake.spark.snowflake is not supported for org.apache.spark.sql.DataFrameReader.format
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

Copy

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3[¶](#scenario-3 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

```
val myFormat = "csv"
spark.read.format(myFormat).load(path)
```

Copy

**Output**

Since the tool can not determine the value of the variable in runtime, shows the EWI `SPRKSCL1163` indicating that the value is not supported.

```
/*EWI: SPRKSCL1163 => myFormat is not a literal and can't be evaluated
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format(myFormat).load(path)
```

Copy

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations[¶](#id85 "Link to this heading")

* The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
* The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/DataFrameReader.html)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1118[¶](#sprkscl1118 "Link to this heading")

Message: org.apache.spark.sql.functions.trunc has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id86 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.trunc](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#trunc(date:org.apache.spark.sql.Column,format:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id87 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.trunc` function that generates this EWI.

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

val result = df.withColumn("truncated", trunc(col("date"), "month"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1118` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

/*EWI: SPRKSCL1118 => org.apache.spark.sql.functions.trunc has a workaround, see documentation for more info*/
val result = df.withColumn("truncated", trunc(col("date"), "month"))
```

Copy

**Recommended fix**

As a workaround, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function.

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

val result = df.withColumn("truncated", trunc(col("date"), lit("month")))
```

Copy

#### Additional recommendations[¶](#id88 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1149[¶](#sprkscl1149 "Link to this heading")

Message: org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id89 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.toRadians](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#toRadians(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id90 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.toRadians` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
val result1 = df.withColumn("radians", toRadians("degrees"))
val result2 = df.withColumn("radians", toRadians(col("degrees")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1149` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
/*EWI: SPRKSCL1149 => org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info*/
val result1 = df.withColumn("radians", toRadians("degrees"))
/*EWI: SPRKSCL1149 => org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info*/
val result2 = df.withColumn("radians", toRadians(col("degrees")))
```

Copy

**Recommended fix**

As a workaround, you can use the [radians](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#radians(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function.

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
val result1 = df.withColumn("radians", radians(col("degrees")))
val result2 = df.withColumn("radians", radians(col("degrees")))
```

Copy

#### Additional recommendations[¶](#id91 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1159[¶](#sprkscl1159 "Link to this heading")

Message: org.apache.spark.sql.functions.stddev\_samp has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id92 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#stddev_samp(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id93 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.stddev_samp` function that generates this EWI. In this example, the `stddev_samp` function is used to calculate the sample standard deviation of selected column.

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
val result1 = stddev_samp(col("elements"))
val result2 = stddev_samp("elements")
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1159` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
/*EWI: SPRKSCL1159 => org.apache.spark.sql.functions.stddev_samp has a workaround, see documentation for more info*/
val result1 = stddev_samp(col("elements"))
/*EWI: SPRKSCL1159 => org.apache.spark.sql.functions.stddev_samp has a workaround, see documentation for more info*/
val result2 = stddev_samp("elements")
```

Copy

**Recommended fix**

Snowpark has an equivalent [stddev\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#stddev_samp(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
val result1 = stddev_samp(col("elements"))
val result2 = stddev_samp(col("elements"))
```

Copy

#### Additional recommendations[¶](#id94 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1108[¶](#sprkscl1108 "Link to this heading")

Note

This issue code has been **deprecated.**

Message: org.apache.spark.sql.DataFrameReader.format is not supported.

Category: Warning.

### Description[¶](#id95 "Link to this heading")

This issue appears when the [org.apache.spark.sql.DataFrameReader.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html#format(source:String):org.apache.spark.sql.DataFrameReader) has an argument that is not supported by Snowpark.

#### Scenarios[¶](#id96 "Link to this heading")

There are some scenarios depending on the type of format you are trying to load. It can be a `supported`, or `non-supported` format.

##### Scenario 1[¶](#id97 "Link to this heading")

**Input**

The tool analyzes the type of format that is trying to load, the supported formats are:

* `csv`
* `json`
* `orc`
* `parquet`
* `text`

The below example shows how the tool transforms the `format` method when passing a `csv` value.

```
spark.read.format("csv").load(path)
```

Copy

**Output**

The tool transforms the `format` method into a `csv` method call when load function has one parameter.

```
spark.read.csv(path)
```

Copy

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2[¶](#id98 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

```
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

Copy

**Output**

The tool shows the EWI `SPRKSCL1108` indicating that the value `net.snowflake.spark.snowflake` is not supported.

```
/*EWI: SPRKSCL1108 => The parameter net.snowflake.spark.snowflake is not supported for org.apache.spark.sql.DataFrameReader.format
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

Copy

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3[¶](#id99 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

```
val myFormat = "csv"
spark.read.format(myFormat).load(path)
```

Copy

**Output**

Since the tool can not determine the value of the variable in runtime, shows the EWI `SPRKSCL1163` indicating that the value is not supported.

```
/*EWI: SPRKSCL1108 => myFormat is not a literal and can't be evaluated
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format(myFormat).load(path)
```

Copy

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations[¶](#id100 "Link to this heading")

* The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
* The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/DataFrameReader.html)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1128[¶](#sprkscl1128 "Link to this heading")

Message: org.apache.spark.sql.functions.exp has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id101 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.exp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#exp(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id102 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.exp` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("exp_value", exp("value"))
val result2 = df.withColumn("exp_value", exp(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1128` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
/*EWI: SPRKSCL1128 => org.apache.spark.sql.functions.exp has a workaround, see documentation for more info*/
val result1 = df.withColumn("exp_value", exp("value"))
/*EWI: SPRKSCL1128 => org.apache.spark.sql.functions.exp has a workaround, see documentation for more info*/
val result2 = df.withColumn("exp_value", exp(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [exp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#exp(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("exp_value", exp(col("value")))
val result2 = df.withColumn("exp_value", exp(col("value")))
```

Copy

#### Additional recommendations[¶](#id103 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1169[¶](#sprkscl1169 "Link to this heading")

Message: ***Spark element*** is missing on the method chaining.

Category: Warning.

### Description[¶](#id104 "Link to this heading")

This issue appears when the SMA detects that a Spark element call is missing on the method chaining. SMA needs to know that Spark element to analyze the statement.

#### Scenario[¶](#id105 "Link to this heading")

**Input**

Below is an example where load function call is missing on the method chaining.

```
val reader = spark.read.format("json")
val df = reader.load(path)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1169` to the output code to let you know that load function call is missing on the method chaining and SMA can not analyze the statement.

```
/*EWI: SPRKSCL1169 => Function 'org.apache.spark.sql.DataFrameReader.load' is missing on the method chaining*/
val reader = spark.read.format("json")
val df = reader.load(path)
```

Copy

**Recommended fix**

Make sure that all function calls of the method chaining are in the same statement.

```
val reader = spark.read.format("json").load(path)
```

Copy

#### Additional recommendations[¶](#id106 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1138[¶](#sprkscl1138 "Link to this heading")

Message: org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id107 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sinh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#sinh(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id108 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.sinh` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("sinh_value", sinh("value"))
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1138` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
/*EWI: SPRKSCL1138 => org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info*/
val result1 = df.withColumn("sinh_value", sinh("value"))
/*EWI: SPRKSCL1138 => org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info*/
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [sinh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#sinh(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("sinh_value", sinh(col("value")))
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

Copy

#### Additional recommendations[¶](#id109 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1129[¶](#sprkscl1129 "Link to this heading")

Message: org.apache.spark.sql.functions.floor has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id110 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.floor](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#floor(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id111 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.floor` function, first used with a column name as an argument, then with a column object and finally with two column objects.

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
val result1 = df.withColumn("floor_value", floor("value"))
val result2 = df.withColumn("floor_value", floor(col("value")))
val result3 = df.withColumn("floor_value", floor(col("value"), lit(1)))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1129` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result1 = df.withColumn("floor_value", floor("value"))
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result2 = df.withColumn("floor_value", floor(col("value")))
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result3 = df.withColumn("floor_value", floor(col("value"), lit(1)))
```

Copy

**Recommended fix**

Snowpark has an equivalent [floor](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#floor(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

For the overload that receives a column object and a scale, you can use the [callBuiltin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#callBuiltin(functionName:String,args:Any*):com.snowflake.snowpark.Column) function to invoke the Snowflake builtin [FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor) function. To use it, you should pass the string **“floor”** as the first argument, the column as the second argument and the scale as the third argument.

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
val result1 = df.withColumn("floor_value", floor(col("value")))
val result2 = df.withColumn("floor_value", floor(col("value")))
val result3 = df.withColumn("floor_value", callBuiltin("floor", col("value"), lit(1)))
```

Copy

#### Additional recommendations[¶](#id112 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1168[¶](#sprkscl1168 "Link to this heading")

Message: ***Spark element*** with argument(s) value(s) ***given arguments*** is not supported.

Category: Warning.

### Description[¶](#id113 "Link to this heading")

This issue appears when the SMA detects that Spark element with the given parameters is not supported.

#### Scenario[¶](#id114 "Link to this heading")

**Input**

Below is an example of Spark element which parameter is not supported.

```
spark.read.format("text").load(path)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1168` to the output code to let you know that Spark element with the given parameter is not supported.

```
/*EWI: SPRKSCL1168 => org.apache.spark.sql.DataFrameReader.format(scala.String) with argument(s) value(s) (spark.format) is not supported*/
spark.read.format("text").load(path)
```

Copy

**Recommended fix**

For this scenario there is no specific fix.

#### Additional recommendations[¶](#id115 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1139[¶](#sprkscl1139 "Link to this heading")

Message: org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id116 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sqrt](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#sqrt(colName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id117 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.sqrt` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
val result1 = df.withColumn("sqrt_value", sqrt("value"))
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1139` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
/*EWI: SPRKSCL1139 => org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info*/
val result1 = df.withColumn("sqrt_value", sqrt("value"))
/*EWI: SPRKSCL1139 => org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info*/
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [sqrt](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#sqrt(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
val result1 = df.withColumn("sqrt_value", sqrt(col("value")))
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

Copy

#### Additional recommendations[¶](#id118 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1119[¶](#sprkscl1119 "Link to this heading")

Message: org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id119 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.Column.endsWith](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Column.html#endsWith(literal:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id120 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.Column.endsWith` function, first used with a literal string argument and then with a column object argument.

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
val result1 = df1.filter(col("email").endsWith(".com"))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
val result2 = df2.filter(col("email").endsWith(col("suffix")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1119` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
/*EWI: SPRKSCL1119 => org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info*/
val result1 = df1.filter(col("email").endsWith(".com"))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
/*EWI: SPRKSCL1119 => org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info*/
val result2 = df2.filter(col("email").endsWith(col("suffix")))
```

Copy

**Recommended fix**

As a workaround, you can use the [com.snowflake.snowpark.functions.endswith](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#endswith(expr:com.snowflake.snowpark.Column,str:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function, where the first argument would be the column whose values will be checked and the second argument the suffix to check against the column values. Please note that if the argument of the Spark’s `endswith` function is a literal string, you should convert it into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function.

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
val result1 = df1.filter(endswith(col("email"), lit(".com")))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
val result2 = df2.filter(endswith(col("email"), col("suffix")))
```

Copy

#### Additional recommendations[¶](#id121 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1148[¶](#sprkscl1148 "Link to this heading")

Message: org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id122 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.toDegrees](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#toDegrees(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id123 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.toDegrees` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
val result1 = df.withColumn("angle_in_degrees", toDegrees("angle_in_radians"))
val result2 = df.withColumn("angle_in_degrees", toDegrees(col("angle_in_radians")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1148` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
/*EWI: SPRKSCL1148 => org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info*/
val result1 = df.withColumn("angle_in_degrees", toDegrees("angle_in_radians"))
/*EWI: SPRKSCL1148 => org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info*/
val result2 = df.withColumn("angle_in_degrees", toDegrees(col("angle_in_radians")))
```

Copy

**Recommended fix**

As a workaround, you can use the [degrees](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#degrees(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function.

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
val result1 = df.withColumn("angle_in_degrees", degrees(col("angle_in_radians")))
val result2 = df.withColumn("angle_in_degrees", degrees(col("angle_in_radians")))
```

Copy

#### Additional recommendations[¶](#id124 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1158[¶](#sprkscl1158 "Link to this heading")

Message: org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id125 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.skewness](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#skewness(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id126 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.skewness` function that generates this EWI. In this example, the `skewness` function is used to calculate the skewness of selected column.

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = skewness(col("elements"))
val result2 = skewness("elements")
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1158` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("1", "2", "3").toDF("elements")
/*EWI: SPRKSCL1158 => org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info*/
val result1 = skewness(col("elements"))
/*EWI: SPRKSCL1158 => org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info*/
val result2 = skewness("elements")
```

Copy

**Recommended fix**

Snowpark has an equivalent [skew](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#skew(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = skew(col("elements"))
val result2 = skew(col("elements"))
```

Copy

#### Additional recommendations[¶](#id127 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1109[¶](#sprkscl1109 "Link to this heading")

Note

This issue code has been **deprecated**

Message: The parameter is not defined for org.apache.spark.sql.DataFrameReader.option

Category: Warning

### Description[¶](#id128 "Link to this heading")

This issue appears when the SMA detects that giving parameter of [org.apache.spark.sql.DataFrameReader.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html#option(key:String,value:Double):org.apache.spark.sql.DataFrameReader) is not defined.

#### Scenario[¶](#id129 "Link to this heading")

**Input**

Below is an example of undefined parameter for `org.apache.spark.sql.DataFrameReader.option` function.

```
spark.read.option("header", True).json(path)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1109` to the output code to let you know that giving parameter to the org.apache.spark.sql.DataFrameReader.option function is not defined.

```
/*EWI: SPRKSCL1109 => The parameter header=True is not supported for org.apache.spark.sql.DataFrameReader.option*/
spark.read.option("header", True).json(path)
```

Copy

**Recommended fix**

Check the Snowpark documentation for reader format option [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions), in order to identify the defined options.

#### Additional recommendations[¶](#id130 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1114[¶](#sprkscl1114 "Link to this heading")

Message: org.apache.spark.sql.functions.repeat has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id131 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.repeat](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#repeat(str:org.apache.spark.sql.Column,n:Int):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id132 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.repeat` function that generates this EWI.

```
val df = Seq("Hello", "World").toDF("word")
val result = df.withColumn("repeated_word", repeat(col("word"), 3))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1114` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("Hello", "World").toDF("word")
/*EWI: SPRKSCL1114 => org.apache.spark.sql.functions.repeat has a workaround, see documentation for more info*/
val result = df.withColumn("repeated_word", repeat(col("word"), 3))
```

Copy

**Recommended fix**

As a workaround, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function.

```
val df = Seq("Hello", "World").toDF("word")
val result = df.withColumn("repeated_word", repeat(col("word"), lit(3)))
```

Copy

#### Additional recommendations[¶](#id133 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1145[¶](#sprkscl1145 "Link to this heading")

Message: org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id134 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sumDistinct](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#sumDistinct(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id135 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.sumDistinct` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

val result1 = df.groupBy("name").agg(sumDistinct("value"))
val result2 = df.groupBy("name").agg(sumDistinct(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1145` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

/*EWI: SPRKSCL1145 => org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info*/
val result1 = df.groupBy("name").agg(sumDistinct("value"))
/*EWI: SPRKSCL1145 => org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info*/
val result2 = df.groupBy("name").agg(sumDistinct(col("value")))
```

Copy

**Recommended fix**

As a workaround, you can use the [sum\_distinct](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#sum_distinct(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

val result1 = df.groupBy("name").agg(sum_distinct(col("value")))
val result2 = df.groupBy("name").agg(sum_distinct(col("value")))
```

Copy

#### Additional recommendations[¶](#id136 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1171[¶](#sprkscl1171 "Link to this heading")

Message: Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info.

Category: Warning.

### Description[¶](#id137 "Link to this heading")

This issue appears when the SMA detects that [org.apache.spark.sql.functions.split](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#split(str:org.apache.spark.sql.Column,pattern:String,limit:Int):org.apache.spark.sql.Column) has more than two parameters or containing regex pattern.

#### Scenarios[¶](#id138 "Link to this heading")

The `split` function is used to separate the given column around matches of the given pattern. This Spark function has three overloads.

##### Scenario 1[¶](#id139 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has two parameters and the second argument is a string, not a regex pattern.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), "Snow"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result = df.select(split(col("words"), "Snow"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [split](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#split(str:com.snowflake.snowpark.Column,pattern:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as a second argument. For that reason, the Spark overload that receives a string argument in the second argument, but it is not a regex pattern, can convert the string into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), lit("Snow")))
```

Copy

##### Scenario 2[¶](#id140 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has two parameters and the second argument is a regex pattern.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), "^([\\d]+-[\\d]+-[\\d])"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark because regex patterns are not supported by Snowflake.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result = df.select(split(col("words"), "^([\\d]+-[\\d]+-[\\d])"))
```

Copy

**Recommended fix**

Since Snowflake does not supported regex patterns, try to replace the pattern by a not regex pattern string.

##### Scenario 3[¶](#id141 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has more than two parameters.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(df("words"), "Snow", 3))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark, because Snowflake does not have a split function with more than two parameters.

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result3 = df.select(split(df("words"), "Snow", 3))
```

Copy

**Recommended fix**

Since Snowflake does not supported split function with more than two parameters, try to use the split function supported by Snowflake.

#### Additional recommendations[¶](#id142 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1120[¶](#sprkscl1120 "Link to this heading")

Message: org.apache.spark.sql.functions.asin has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id143 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.asin](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#asin(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id144 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.asin` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
val result1 = df.select(col("value"), asin("value").as("asin_value"))
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1120` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
/*EWI: SPRKSCL1120 => org.apache.spark.sql.functions.asin has a workaround, see documentation for more info*/
val result1 = df.select(col("value"), asin("value").as("asin_value"))
/*EWI: SPRKSCL1120 => org.apache.spark.sql.functions.asin has a workaround, see documentation for more info*/
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [asin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#asin(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
val result1 = df.select(col("value"), asin(col("value")).as("asin_value"))
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

Copy

#### Additional recommendations[¶](#id145 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1130[¶](#sprkscl1130 "Link to this heading")

Message: org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id146 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.greatest](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#greatest(columnName:String,columnNames:String*):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id147 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.greatest` function, first used with multiple column names as arguments and then with multiple column objects.

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

val result1 = df.withColumn("greatest", greatest("value1", "value2", "value3"))
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1130` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

/*EWI: SPRKSCL1130 => org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info*/
val result1 = df.withColumn("greatest", greatest("value1", "value2", "value3"))
/*EWI: SPRKSCL1130 => org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info*/
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [greatest](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#greatest(exprs:com.snowflake.snowpark.Column*):com.snowflake.snowpark.Column) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

val result1 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

Copy

#### Additional recommendations[¶](#id148 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

---

description: >-
Snowpark and Snowpark Extensions were not added to the project configuration
file.

---

## SPRKSCL1161[¶](#sprkscl1161 "Link to this heading")

Message: Failed to add dependencies.

Category: Conversion error.

### Description[¶](#id149 "Link to this heading")

This issue occurs when the SMA detects a Spark version in the project configuration file that is not supported by the SMA, therefore SMA could not add the Snowpark and Snowpark Extensions dependencies to the corresponding project configuration file. If Snowpark dependencies are not added, the migrated code will not compile.

#### Scenarios[¶](#id150 "Link to this heading")

There are three possible scenarios: sbt, gradle and pom.xml. The SMA tries to process the project configuration file by removing Spark dependencies and adding Snowpark and Snowpark Extensions dependencies.

##### Scenario 1[¶](#id151 "Link to this heading")

**Input**

Below is an example of the `dependencies` section of a `sbt` project configuration file.

```
...
libraryDependencies += "org.apache.spark" % "spark-core_2.13" % "3.5.3"
libraryDependencies += "org.apache.spark" % "spark-sql_2.13" % "3.5.3"
...
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

```
...
libraryDependencies += "org.apache.spark" % "spark-core_2.13" % "3.5.3"
libraryDependencies += "org.apache.spark" % "spark-sql_2.13" % "3.5.3"
...
```

Copy

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `sbt` project configuration file.

```
...
libraryDependencies += "com.snowflake" % "snowpark" % "1.14.0"
libraryDependencies += "net.mobilize.snowpark-extensions" % "snowparkextensions" % "0.0.18"
...
```

Copy

Make sure to use the Snowpark version that best meets your project’s requirements.

##### Scenario 2[¶](#id152 "Link to this heading")

**Input**

Below is an example of the `dependencies` section of a `gradle` project configuration file.

```
dependencies {
    implementation group: 'org.apache.spark', name: 'spark-core_2.13', version: '3.5.3'
    implementation group: 'org.apache.spark', name: 'spark-sql_2.13', version: '3.5.3'
    ...
}
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

```
dependencies {
    implementation group: 'org.apache.spark', name: 'spark-core_2.13', version: '3.5.3'
    implementation group: 'org.apache.spark', name: 'spark-sql_2.13', version: '3.5.3'
    ...
}
```

Copy

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `gradle` project configuration file.

```
dependencies {
    implementation 'com.snowflake:snowpark:1.14.2'
    implementation 'net.mobilize.snowpark-extensions:snowparkextensions:0.0.18'
    ...
}
```

Copy

Make sure that dependencies version are according to your project needs.

##### Scenario 3[¶](#id153 "Link to this heading")

**Input**

Below is an example of the `dependencies` section of a `pom.xml` project configuration file.

```
<dependencies>
  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.13</artifactId>
    <version>3.5.3</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-sql_2.13</artifactId>
    <version>3.5.3</version>
    <scope>compile</scope>
  </dependency>
  ...
</dependencies>
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

```
<dependencies>
  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.13</artifactId>
    <version>3.5.3</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-sql_2.13</artifactId>
    <version>3.5.3</version>
    <scope>compile</scope>
  </dependency>
  ...
</dependencies>
```

Copy

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `gradle` project configuration file.

```
<dependencies>
  <dependency>
    <groupId>com.snowflake</groupId>
    <artifactId>snowpark</artifactId>
    <version>1.14.2</version>
  </dependency>

  <dependency>
    <groupId>net.mobilize.snowpark-extensions</groupId>
    <artifactId>snowparkextensions</artifactId>
    <version>0.0.18</version>
  </dependency>
  ...
</dependencies>
```

Copy

Make sure that dependencies version are according to your project needs.

#### Additional recommendations[¶](#id154 "Link to this heading")

* Make sure that input has a project configuration file:

  + build.sbt
  + build.gradle
  + pom.xml
* Spark version supported by the SMA is 2.12:3.1.2
* You can check the latest Snowpark version [here](https://github.com/snowflakedb/snowpark-java-scala/releases/latest).
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1155[¶](#sprkscl1155 "Link to this heading")

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.3.2](../../../general/release-notes/README.html#spark-conversion-core-version-4-3-2)

Message: org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id155 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.countDistinct](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#countDistinct(columnName:String,columnNames:String*):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id156 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.countDistinct` function, first used with column names as arguments and then with column objects.

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

val result1 = df.select(countDistinct("name", "value"))
val result2 = df.select(countDistinct(col("name"), col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1155` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

/*EWI: SPRKSCL1155 => org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info*/
val result1 = df.select(countDistinct("name", "value"))
/*EWI: SPRKSCL1155 => org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info*/
val result2 = df.select(countDistinct(col("name"), col("value")))
```

Copy

**Recommended fix**

As a workaround, you can use the [count\_distinct](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#count_distinct(expr:com.snowflake.snowpark.Column,exprs:com.snowflake.snowpark.Column*):com.snowflake.snowpark.Column) function. For the Spark overload that receives string arguments, you additionally have to convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function.

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

val result1 = df.select(count_distinct(col("name"), col("value")))
val result2 = df.select(count_distinct(col("name"), col("value")))
```

Copy

#### Additional recommendations[¶](#id157 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1104[¶](#sprkscl1104 "Link to this heading")

This issue code has been **deprecated**

Message: Spark Session builder option is not supported.

Category: Conversion Error.

### Description[¶](#id158 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.SparkSession.Builder.config](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/SparkSession$$Builder.html#config(conf:org.apache.spark.SparkConf):org.apache.spark.sql.SparkSession.Builder) function, which is setting an option of the Spark Session and it is not supported by Snowpark.

#### Scenario[¶](#id159 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.SparkSession.Builder.config` function used to set an option in the Spark Session.

```
val spark = SparkSession.builder()
           .master("local")
           .appName("testApp")
           .config("spark.sql.broadcastTimeout", "3600")
           .getOrCreate()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1104` to the output code to let you know config method is not supported by Snowpark. Then, it is not possible to set options in the Spark Session via config function and it might affects the migration of the Spark Session statement.

```
val spark = Session.builder.configFile("connection.properties")
/*EWI: SPRKSCL1104 => SparkBuilder Option is not supported .config("spark.sql.broadcastTimeout", "3600")*/
.create()
```

Copy

**Recommended fix**

To create the session is require to add the proper Snowflake Snowpark configuration.

In this example a configs variable is used.

```
    val configs = Map (
      "URL" -> "https://<myAccount>.snowflakecomputing.com:<port>",
      "USER" -> <myUserName>,
      "PASSWORD" -> <myPassword>,
      "ROLE" -> <myRole>,
      "WAREHOUSE" -> <myWarehouse>,
      "DB" -> <myDatabase>,
      "SCHEMA" -> <mySchema>
    )
    val session = Session.builder.configs(configs).create
```

Copy

Also is recommended the use of a configFile (profile.properties) with the connection information:

```
## profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

Copy

And with the `Session.builder.configFile` the session can be created:

```
val session = Session.builder.configFile("/path/to/properties/file").create
```

Copy

### Additional recommendations[¶](#id160 "Link to this heading")

* [Developer guide for create a session.](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-session)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1124[¶](#sprkscl1124 "Link to this heading")

Message: org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id161 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.cosh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#cosh(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id162 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.cosh` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
val result1 = df.withColumn("cosh_value", cosh("value"))
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1124` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
/*EWI: SPRKSCL1124 => org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info*/
val result1 = df.withColumn("cosh_value", cosh("value"))
/*EWI: SPRKSCL1124 => org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info*/
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [cosh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#cosh(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
val result1 = df.withColumn("cosh_value", cosh(col("value")))
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

Copy

#### Additional recommendations[¶](#id163 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1175[¶](#sprkscl1175 "Link to this heading")

Message: The two-parameter`udf`function is not supported in Snowpark. It should be converted into a single-parameter`udf`function. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.

Category: Conversion error.

### Description[¶](#id164 "Link to this heading")

This issue appears when the SMA detects an use of the two-parameter [org.apache.spark.sql.functions.udf](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#udf(f:org.apache.spark.sql.api.java.UDF0%5B_%5D,returnType:org.apache.spark.sql.types.DataType):org.apache.spark.sql.expressions.UserDefinedFunction) function in the source code, because Snowpark does not have an equivalent two-parameter `udf` function, then the output code might not compile.

#### Scenario[¶](#id165 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.udf` function that generates this EWI. In this example, the `udf` function has two parameters.

```
val myFuncUdf = udf(new UDF1[String, Integer] {
  override def call(s: String): Integer = s.length()
}, IntegerType)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1175` to the output code to let you know that the `udf` function is not supported, because it has two parameters.

```
/*EWI: SPRKSCL1175 => The two-parameter udf function is not supported in Snowpark. It should be converted into a single-parameter udf function. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
val myFuncUdf = udf(new UDF1[String, Integer] {
  override def call(s: String): Integer = s.length()
}, IntegerType)
```

Copy

**Recommended fix**

Snowpark only supports the single-parameter `udf` function (without the return type parameter), so you should convert your two-parameter `udf` function into a single-parameter `udf` function in order to make it work in Snowpark.

For example, for the sample code mentioned above, you would have to manually convert it into this:

```
val myFuncUdf = udf((s: String) => s.length())
```

Copy

Please note that there are some caveats about creating `udf` in Snowpark that might require you to make some additional manual changes to your code. Please check this other recommendations [here](#additional-recommendations) related with creating single-parameter `udf` functions in Snowpark for more details.

#### Additional recommendations[¶](#id166 "Link to this heading")

* To learn more about how to create user-defined functions in Snowpark, please refer to the following documentation: [Creating User-Defined Functions (UDFs) for DataFrames in Scala](../../../../../developer-guide/snowpark/scala/creating-udfs.html#label-snowpark-udf-data-types)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1001[¶](#sprkscl1001 "Link to this heading")

Message: This code section has parsing errors. The parsing error was found at: line ***line number***, column ***column number***. When trying to parse ***statement***. This file was not converted, so it is expected to still have references to the Spark API.

Category: Parsing error.

### Description[¶](#id167 "Link to this heading")

This issue appears when the SMA detects some statement that cannot correctly read or understand in the code of a file, it is called as **parsing error**. Besides, this issue appears when a file has one or more parsing error(s).

#### Scenario[¶](#id168 "Link to this heading")

**Input**

Below is an example of invalid Scala code.

```
/#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1001` to the output code to let you know that the code of the file has parsing errors. Therefore, SMA is not able to process a file with this error.

```
// **********************************************************************************************************************
// EWI: SPRKSCL1001 => This code section has parsing errors
// The parsing error was found at: line 0, column 0. When trying to parse ''.
// This file was not converted, so it is expected to still have references to the Spark API
// **********************************************************************************************************************
/#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

Copy

**Recommended fix**

Since the message pinpoint the error statement you can try to identify the invalid syntax and remove it or comment out that statement to avoid the parsing error.

```
Class myClass {

    def function1() = { 1 }

}
```

Copy

```
// /#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

Copy

#### Additional recommendations[¶](#id169 "Link to this heading")

* Check that the code of the file is a valid Scala code.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1141[¶](#sprkscl1141 "Link to this heading")

Message: org.apache.spark.sql.functions.stddev\_pop has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id170 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#stddev_pop(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id171 "Link to this heading")

Below is an example of the `org.apache.spark.sql.functions.stddev_pop` function, first used with a column name as an argument and then with a column object.

**Input**

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

val result1 = df.select(stddev_pop("age"))
val result2 = df.select(stddev_pop(col("age")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1141` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

/*EWI: SPRKSCL1141 => org.apache.spark.sql.functions.stddev_pop has a workaround, see documentation for more info*/
val result1 = df.select(stddev_pop("age"))
/*EWI: SPRKSCL1141 => org.apache.spark.sql.functions.stddev_pop has a workaround, see documentation for more info*/
val result2 = df.select(stddev_pop(col("age")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [stddev\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#stddev_pop(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

val result1 = df.select(stddev_pop(col("age")))
val result2 = df.select(stddev_pop(col("age")))
```

Copy

#### Additional recommendations[¶](#id172 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1110[¶](#sprkscl1110 "Link to this heading")

Note

This issue code has been **deprecated**

Message: Reader method not supported ***method name***.

Category: Warning

### Description[¶](#id173 "Link to this heading")

This issue appears when the SMA detects a method that is not supported by Snowflake in the DataFrameReader method chaining. Then, it might affects the migration of the reader statement.

#### Scenario[¶](#id174 "Link to this heading")

**Input**

Below is an example of a DataFrameReader method chaining where load method is not supported by Snowflake.

```
spark.read.
    format("net.snowflake.spark.snowflake").
    option("query", s"select * from $tablename")
    load()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1110` to the output code to let you know that load method is not supported by Snowpark. Then, it might affects the migration of the reader statement.

```
session.sql(s"select * from $tablename")
/*EWI: SPRKSCL1110 => Reader method not supported .load()*/
```

Copy

**Recommended fix**

Check the Snowpark documentation for reader [here](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/DataFrameReader.html), in order to know the supported methods by Snowflake.

#### Additional recommendations[¶](#id175 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1100[¶](#sprkscl1100 "Link to this heading")

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](../../../general/release-notes/README)

Message: Repartition is not supported.

Category: Parsing error.

### Description[¶](#id176 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.DataFrame.repartition](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Dataset.html#repartition(partitionExprs:org.apache.spark.sql.Column*):org.apache.spark.sql.Dataset%5BT%5D) function, which is not supported by Snowpark. Snowflake manages the storage and the workload on the clusters making repartition operation inapplicable.

#### Scenario[¶](#id177 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.DataFrame.repartition` function used to return a new `DataFrame` partitioned by the given partitioning expressions.

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    val dfRepartitionByExpresion = dfName.repartition($"name")

    val dfRepartitionByNumber = dfJob.repartition(3)

    val dfRepartitionByBoth = dfAge.repartition(3, $"age")

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1100` to the output code to let you know that this function is not supported by Snowpark.

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByExpresion = dfName.repartition($"name")

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByNumber = dfJob.repartition(3)

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByBoth = dfAge.repartition(3, $"age")

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

Copy

**Recommended Fix**

Since Snowflake manages the storage and the workload on the clusters making repartition operation inapplicable. This means that the use of repartition before the join is not required at all.

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    val dfRepartitionByExpresion = dfName

    val dfRepartitionByNumber = dfJob

    val dfRepartitionByBoth = dfAge

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

Copy

#### Additional recommendations[¶](#id178 "Link to this heading")

* The [Snowflake’s architecture guide](https://docs.snowflake.com/en/user-guide/intro-key-concepts) provides insight about Snowflake storage management.
* Snowpark [Dataframe reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/dataframe) could be useful in how to adapt a particular scenario without the need of repartition.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1151[¶](#sprkscl1151 "Link to this heading")

Message: org.apache.spark.sql.functions.var\_samp has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id179 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.var\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#var_samp(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id180 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.var_samp` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

val result1 = df.groupBy("category").agg(var_samp("value"))
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1151` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

/*EWI: SPRKSCL1151 => org.apache.spark.sql.functions.var_samp has a workaround, see documentation for more info*/
val result1 = df.groupBy("category").agg(var_samp("value"))
/*EWI: SPRKSCL1151 => org.apache.spark.sql.functions.var_samp has a workaround, see documentation for more info*/
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [var\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#var_samp(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

val result1 = df.groupBy("category").agg(var_samp(col("value")))
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

Copy

#### Additional recommendations[¶](#id181 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

---

description: >-
The format of the reader on DataFrameReader method chaining is not one of the
defined by Snowpark.

---

## SPRKSCL1165[¶](#sprkscl1165 "Link to this heading")

Message: Reader format on DataFrameReader method chaining can’t be defined

Category: Warning

### Description[¶](#id182 "Link to this heading")

This issue appears when the SMA detects that `format` of the reader in DataFrameReader method chaining is not one of the following supported for Snowpark: `avro`, `csv`, `json`, `orc`, `parquet` and `xml`. Therefore, the SMA can not determine if setting options are defined or not.

#### Scenario[¶](#id183 "Link to this heading")

**Input**

Below is an example of DataFrameReader method chaining where SMA can determine the format of reader.

```
spark.read.format("net.snowflake.spark.snowflake")
                 .option("query", s"select * from $tableName")
                 .load()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1165` to the output code to let you know that `format` of the reader can not be determine in the giving DataFrameReader method chaining.

```
/*EWI: SPRKSCL1165 => Reader format on DataFrameReader method chaining can't be defined*/
spark.read.option("query", s"select * from $tableName")
                 .load()
```

Copy

**Recommended fix**

Check the Snowpark documentation [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to get more information about format of the reader.

#### Additional recommendations[¶](#id184 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1134[¶](#sprkscl1134 "Link to this heading")

Message: org.apache.spark.sql.functions.log has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id185 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.log](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#log(base:Double,columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id186 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.log` function that generates this EWI.

```
val df = Seq(10.0, 20.0, 30.0, 40.0).toDF("value")
val result1 = df.withColumn("log_value", log(10, "value"))
val result2 = df.withColumn("log_value", log(10, col("value")))
val result3 = df.withColumn("log_value", log("value"))
val result4 = df.withColumn("log_value", log(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1134` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(10.0, 20.0, 30.0, 40.0).toDF("value")
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result1 = df.withColumn("log_value", log(10, "value"))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result2 = df.withColumn("log_value", log(10, col("value")))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result3 = df.withColumn("log_value", log("value"))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result4 = df.withColumn("log_value", log(col("value")))
```

Copy

**Recommended fix**

Below are the different workarounds for all the overloads of the `log` function.

**1. def log(base: Double, columnName: String): Column**

You can convert the base into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function and convert the column name into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function.

```
val result1 = df.withColumn("log_value", log(lit(10), col("value")))
```

Copy

**2. def log(base: Double, a: Column): Column**

You can convert the base into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function.

```
val result2 = df.withColumn("log_value", log(lit(10), col("value")))
```

Copy

**3.def log(columnName: String): Column**

You can pass `lit(Math.E)` as the first argument and convert the column name into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function and pass it as the second argument.

```
val result3 = df.withColumn("log_value", log(lit(Math.E), col("value")))
```

Copy

**4. def log(e: Column): Column**

You can pass `lit(Math.E)` as the first argument and the column object as the second argument.

```
val result4 = df.withColumn("log_value", log(lit(Math.E), col("value")))
```

Copy

#### Additional recommendations[¶](#id187 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1125[¶](#sprkscl1125 "Link to this heading")

Warning

This issue code is **deprecated** since [Spark Conversion Core 2.9.0](../../../general/release-notes/old-version-release-notes/sc-spark-scala-release-notes/README.html#id5)

Message: org.apache.spark.sql.functions.count has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id188 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.count](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#count(columnName:String):org.apache.spark.sql.TypedColumn%5BAny,Long%5D) function, which has a workaround.

#### Scenario[¶](#id189 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.count` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

val result1 = df.groupBy("name").agg(count("subject").as("subject_count"))
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1125` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

/*EWI: SPRKSCL1125 => org.apache.spark.sql.functions.count has a workaround, see documentation for more info*/
val result1 = df.groupBy("name").agg(count("subject").as("subject_count"))
/*EWI: SPRKSCL1125 => org.apache.spark.sql.functions.count has a workaround, see documentation for more info*/
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [count](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#count(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

val result1 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

Copy

#### Additional recommendations[¶](#id190 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1174[¶](#sprkscl1174 "Link to this heading")

Message: The single-parameter `udf` function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.

Category: Warning.

### Description[¶](#id191 "Link to this heading")

This issue appears when the SMA detects an use of the single-parameter [org.apache.spark.sql.functions.udf](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#udf(f:org.apache.spark.sql.api.java.UDF10%5B_,_,_,_,_,_,_,_,_,_,_%5D,returnType:org.apache.spark.sql.types.DataType):org.apache.spark.sql.expressions.UserDefinedFunction) function in the code. Then, it might require a manual intervention.

The Snowpark API provides an equivalent [com.snowflake.snowpark.functions.udf](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html) function that allows you to create a user-defined function from a lambda or function in Scala, however, there are some caveats about creating `udf` in Snowpark that might require you to make some manual changes to your code in order to make it work properly.

#### Scenarios[¶](#id192 "Link to this heading")

The Snowpark `udf` function should work as intended for a wide range of cases without requiring manual intervention. However, there are some scenarios that would requiere you to manually modify your code in order to get it work in Snowpark. Some of those scenarios are listed below:

##### Scenario 1[¶](#id193 "Link to this heading")

**Input**

Below is an example of creating UDFs in an object with the App Trait.

The Scala’s `App` trait simplifies creating executable programs by providing a `main` method that automatically runs the code within the object definition. Extending `App` delays the initialization of the fields until the `main` method is executed, which can affect the UDFs definitions if they rely on initialized fields. This means that if an object extends `App` and the `udf` references an object field, the `udf` definition uploaded to Snowflake will not include the initialized value of the field. This can result in `null` values being returned by the `udf`.

For example, in the following code the variable myValue will resolve to `null` in the `udf` definition:

```
object Main extends App {
  ...
  val myValue = 10
  val myUdf = udf((x: Int) => x + myValue) // myValue in the `udf` definition will resolve to null
  ...
}
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1174` to the output code to let you know that the single-parameter `udf` function is supported in Snowpark but it requires manual intervention.

```
object Main extends App {
  ...
  val myValue = 10
  /*EWI: SPRKSCL1174 => The single-parameter udf function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
  val myUdf = udf((x: Int) => x + myValue) // myValue in the `udf` definition will resolve to null
  ...
}
```

Copy

**Recommended fix**

To avoid this issue, it is recommended to not extend `App` and implement a separate `main` method for your code. This ensure that object fields are initialized before `udf` definitions are created and uploaded to Snowflake.

```
object Main {
  ...
  def main(args: Array[String]): Unit = {
    val myValue = 10
    val myUdf = udf((x: Int) => x + myValue)
  }
  ...
}
```

Copy

For more details about this topic, see [Caveat About Creating UDFs in an Object With the App Trait](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs#caveat-about-creating-udfs-in-an-object-with-the-app-trait).

##### Scenario 2[¶](#id194 "Link to this heading")

**Input**

Below is an example of creating UDFs in Jupyter Notebooks.

```
def myFunc(s: String): String = {
  ...
}

val myFuncUdf = udf((x: String) => myFunc(x))
df1.select(myFuncUdf(col("name"))).show()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1174` to the output code to let you know that the single-parameter `udf` function is supported in Snowpark but it requires manual intervention.

```
def myFunc(s: String): String = {
  ...
}

/*EWI: SPRKSCL1174 => The single-parameter udf function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
val myFuncUdf = udf((x: String) => myFunc(x))
df1.select(myFuncUdf(col("name"))).show()
```

Copy

**Recommended fix**

To create a `udf` in a Jupyter Notebook, you should define the implementation of your function in a class that extends `Serializable`. For example, you should manually convert it into this:

```
object ConvertedUdfFuncs extends Serializable {
  def myFunc(s: String): String = {
    ...
  }

  val myFuncAsLambda = ((x: String) => ConvertedUdfFuncs.myFunc(x))
}

val myFuncUdf = udf(ConvertedUdfFuncs.myFuncAsLambda)
df1.select(myFuncUdf(col("name"))).show()
```

Copy

For more details about how to create UDFs in Jupyter Notebooks, see [Creating UDFs in Jupyter Notebooks](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs#creating-udfs-in-jupyter-notebooks).

#### Additional recommendations[¶](#id195 "Link to this heading")

* To learn more about how to create user-defined functions in Snowpark, please refer to the following documentation: [Creating User-Defined Functions (UDFs) for DataFrames in Scala](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1000[¶](#sprkscl1000 "Link to this heading")

Message: Source project spark-core version is ***version number***, the spark-core version supported by snowpark is 2.12:3.1.2 so there may be functional differences between the existing mappings

Category: Warning

### Description[¶](#id196 "Link to this heading")

This issue appears when the SMA detects a version of the `spark-core` that is not supported by SMA. Therefore, there may be functional differences between the existing mappings and the output might have unexpected behaviors.

#### Additional recommendations[¶](#id197 "Link to this heading")

* The spark-core version supported by SMA is 2.12:3.1.2. Consider changing the version of your source code.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1140[¶](#sprkscl1140 "Link to this heading")

Message: org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id198 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#stddev(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id199 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.stddev` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

val result1 = df.select(stddev("score"))
val result2 = df.select(stddev(col("score")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1140` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

/*EWI: SPRKSCL1140 => org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info*/
val result1 = df.select(stddev("score"))
/*EWI: SPRKSCL1140 => org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info*/
val result2 = df.select(stddev(col("score")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [stddev](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#stddev(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

val result1 = df.select(stddev(col("score")))
val result2 = df.select(stddev(col("score")))
```

Copy

#### Additional recommendations[¶](#id200 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1111[¶](#sprkscl1111 "Link to this heading")

Note

This issue code has been **deprecated**

Message: CreateDecimalType is not supported.

Category: Conversion error.

### Description[¶](#id201 "Link to this heading")

This issue appears when the SMA detects a usage [org.apache.spark.sql.types.DataTypes.CreateDecimalType](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/DecimalType.html) function.

#### Scenario[¶](#id202 "Link to this heading")

**Input**

Below is an example of usage of org.apache.spark.sql.types.DataTypes.CreateDecimalType function.

```
var result = DataTypes.createDecimalType(18, 8)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1111` to the output code to let you know that CreateDecimalType function is not supported by Snowpark.

```
/*EWI: SPRKSCL1111 => CreateDecimalType is not supported*/
var result = createDecimalType(18, 8)
```

Copy

**Recommended fix**

There is not a recommended fix yet.

Message: Spark Session builder option is not supported.

Category: Conversion Error.

#### Description[¶](#id203 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.SparkSession.Builder.config](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/SparkSession$$Builder.html#config(conf:org.apache.spark.SparkConf):org.apache.spark.sql.SparkSession.Builder) function, which is setting an option of the Spark Session and it is not supported by Snowpark.

#### Scenario[¶](#id204 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.SparkSession.Builder.config` function used to set an option in the Spark Session.

```
val spark = SparkSession.builder()
           .master("local")
           .appName("testApp")
           .config("spark.sql.broadcastTimeout", "3600")
           .getOrCreate()
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1104` to the output code to let you know config method is not supported by Snowpark. Then, it is not possible to set options in the Spark Session via config function and it might affects the migration of the Spark Session statement.

```
val spark = Session.builder.configFile("connection.properties")
/*EWI: SPRKSCL1104 => SparkBuilder Option is not supported .config("spark.sql.broadcastTimeout", "3600")*/
.create()
```

Copy

**Recommended fix**

To create the session is require to add the proper Snowflake Snowpark configuration.

In this example a configs variable is used.

```
    val configs = Map (
      "URL" -> "https://<myAccount>.snowflakecomputing.com:<port>",
      "USER" -> <myUserName>,
      "PASSWORD" -> <myPassword>,
      "ROLE" -> <myRole>,
      "WAREHOUSE" -> <myWarehouse>,
      "DB" -> <myDatabase>,
      "SCHEMA" -> <mySchema>
    )
    val session = Session.builder.configs(configs).create
```

Copy

Also is recommended the use of a configFile (profile.properties) with the connection information:

```
## profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

Copy

And with the `Session.builder.configFile` the session can be created:

```
val session = Session.builder.configFile("/path/to/properties/file").create
```

Copy

### Additional recommendations[¶](#id205 "Link to this heading")

* [Developer guide for create a session.](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-session)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1101[¶](#sprkscl1101 "Link to this heading")

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](../../../general/release-notes/README)

Message: Broadcast is not supported

Category: Warning

### Description[¶](#id206 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.broadcast](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#broadcast%5BT%5D(df:org.apache.spark.sql.Dataset%5BT%5D):org.apache.spark.sql.Dataset%5BT%5D) function, which is not supported by Snowpark. This function is not supported because Snowflake does not support [broadcast variables](https://spark.apache.org/docs/latest/api/java/org/apache/spark/broadcast/Broadcast.html).

#### Scenario[¶](#id207 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.broadcast` function used to create a broadcast object to use on each Spark cluster:

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      broadcast(dfCollege),
      Seq("CollegeName")
    )
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1101` to the output code to let you know that this function is not supported by Snowpark.

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      /*EWI: SPRKSCL1101 => Broadcast is not supported*/
      broadcast(dfCollege),
      Seq("CollegeName")
    )
```

Copy

**Recommended fix**

Since Snowflake manages the storage and the workload on the clusters making broadcast objects inapplicable. This means that the use of broadcast could not be required at all, but each case should require further analysis.

The recommended approach is replace a Spark dataframe broadcast by a Snowpark regular dataframe or by using a dataframe method as [Join](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrame.join).

For the proposed input the fix is to adapt the join to use directly the dataframe `collegeDF` without the use of broadcast for the dataframe.

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      dfCollege,
      Seq("CollegeName")
    ).show()
```

Copy

#### Additional recommendations[¶](#id208 "Link to this heading")

* The [Snowflake’s architecture guide](https://docs.snowflake.com/en/user-guide/intro-key-concepts) provides insight about Snowflake storage management.
* Snowpark [Dataframe reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/dataframe) could be useful in how to adapt a particular broadcast scenario.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1150[¶](#sprkscl1150 "Link to this heading")

Message: org.apache.spark.sql.functions.var\_pop has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id209 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.var\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#var_pop(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id210 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.var_pop` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

val result1 = df.groupBy("group").agg(var_pop("value"))
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1150` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

/*EWI: SPRKSCL1150 => org.apache.spark.sql.functions.var_pop has a workaround, see documentation for more info*/
val result1 = df.groupBy("group").agg(var_pop("value"))
/*EWI: SPRKSCL1150 => org.apache.spark.sql.functions.var_pop has a workaround, see documentation for more info*/
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [var\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#var_pop(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

val result1 = df.groupBy("group").agg(var_pop(col("value")))
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

Copy

#### Additional recommendations[¶](#id211 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

---

description: >-
The parameter of org.apache.spark.sql.DataFrameReader.option function is not
defined.

---

## SPRKSCL1164[¶](#sprkscl1164 "Link to this heading")

Note

This issue code has been **deprecated**

Message: The parameter is not defined for org.apache.spark.sql.DataFrameReader.option

Category: Warning

### Description[¶](#id212 "Link to this heading")

This issue appears when the SMA detects that giving parameter of [org.apache.spark.sql.DataFrameReader.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html#option(key:String,value:Double):org.apache.spark.sql.DataFrameReader) is not defined.

#### Scenario[¶](#id213 "Link to this heading")

**Input**

Below is an example of undefined parameter for `org.apache.spark.sql.DataFrameReader.option` function.

```
spark.read.option("header", True).json(path)
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1164` to the output code to let you know that giving parameter to the org.apache.spark.sql.DataFrameReader.option function is not defined.

```
/*EWI: SPRKSCL1164 => The parameter header=True is not supported for org.apache.spark.sql.DataFrameReader.option*/
spark.read.option("header", True).json(path)
```

Copy

**Recommended fix**

Check the Snowpark documentation for reader format option [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions), in order to identify the defined options.

#### Additional recommendations[¶](#id214 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1135[¶](#sprkscl1135 "Link to this heading")

Warning

This issue code is **deprecated** since [Spark Conversion Core 4.3.2](../../../general/release-notes/README.html#spark-conversion-core-version-4-3-2)

Message: org.apache.spark.sql.functions.mean has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id215 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.mean](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#mean(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id216 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.mean` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(mean("value"))
val result2 = df.select(mean(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1135` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
/*EWI: SPRKSCL1135 => org.apache.spark.sql.functions.mean has a workaround, see documentation for more info*/
val result1 = df.select(mean("value"))
/*EWI: SPRKSCL1135 => org.apache.spark.sql.functions.mean has a workaround, see documentation for more info*/
val result2 = df.select(mean(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [mean](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#mean(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(mean(col("value")))
val result2 = df.select(mean(col("value")))
```

Copy

#### Additional recommendations[¶](#id217 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1115[¶](#sprkscl1115 "Link to this heading")

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.6.0](../../../general/release-notes/README.html#snowpark-conversion-core-version-4-6-0)

Message: org.apache.spark.sql.functions.round has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id218 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.round](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#round(e:org.apache.spark.sql.Column,scale:Int):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id219 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.round` function that generates this EWI.

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
val result1 = df.withColumn("rounded_value", round(col("value")))
val result2 = df.withColumn("rounded_value", round(col("value"), 2))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1115` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
/*EWI: SPRKSCL1115 => org.apache.spark.sql.functions.round has a workaround, see documentation for more info*/
val result1 = df.withColumn("rounded_value", round(col("value")))
/*EWI: SPRKSCL1115 => org.apache.spark.sql.functions.round has a workaround, see documentation for more info*/
val result2 = df.withColumn("rounded_value", round(col("value"), 2))
```

Copy

**Recommended fix**

Snowpark has an equivalent [round](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#round(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a column object and a scale, you can convert the scale into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#lit(literal:Any):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
val result1 = df.withColumn("rounded_value", round(col("value")))
val result2 = df.withColumn("rounded_value", round(col("value"), lit(2)))
```

Copy

#### Additional recommendations[¶](#id220 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1144[¶](#sprkscl1144 "Link to this heading")

Message: The symbol table could not be loaded

Category: Parsing error

### Description[¶](#id221 "Link to this heading")

This issue appears when there is a critical error in the SMA execution process. Since the symbol table cannot be loaded, the SMA cannot start the assessment or conversion process.

#### Additional recommendations[¶](#id222 "Link to this heading")

* This is unlikely to be an error in the source code itself, but rather is an error in how the SMA processes the source code. The best resolution would be to post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1170[¶](#sprkscl1170 "Link to this heading")

Note

This issue code has been **deprecated**

Message: sparkConfig member key is not supported with platform specific key.

Category: Conversion error

### Description[¶](#id223 "Link to this heading")

If you are using an older version, please upgrade to the latest.

#### Additional recommendations[¶](#id224 "Link to this heading")

* Upgrade your application to the latest version.
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1121[¶](#sprkscl1121 "Link to this heading")

Message: org.apache.spark.sql.functions.atan has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id225 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.atan](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#atan(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id226 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.atan` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
val result1 = df.withColumn("atan_value", atan("value"))
val result2 = df.withColumn("atan_value", atan(col("value")))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1121` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
/*EWI: SPRKSCL1121 => org.apache.spark.sql.functions.atan has a workaround, see documentation for more info*/
val result1 = df.withColumn("atan_value", atan("value"))
/*EWI: SPRKSCL1121 => org.apache.spark.sql.functions.atan has a workaround, see documentation for more info*/
val result2 = df.withColumn("atan_value", atan(col("value")))
```

Copy

**Recommended fix**

Snowpark has an equivalent [atan](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#atan(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
val result1 = df.withColumn("atan_value", atan(col("value")))
val result2 = df.withColumn("atan_value", atan(col("value")))
```

Copy

#### Additional recommendations[¶](#id227 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1131[¶](#sprkscl1131 "Link to this heading")

Message: org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id228 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.grouping](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#grouping(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id229 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.grouping` function, first used with a column name as an argument and then with a column object.

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
val result1 = df.cube("name").agg(grouping("name"), sum("age"))
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1131` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
/*EWI: SPRKSCL1131 => org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info*/
val result1 = df.cube("name").agg(grouping("name"), sum("age"))
/*EWI: SPRKSCL1131 => org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info*/
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

Copy

**Recommended fix**

Snowpark has an equivalent [grouping](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#grouping(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
val result1 = df.cube("name").agg(grouping(col("name")), sum("age"))
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

Copy

#### Additional recommendations[¶](#id230 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1160[¶](#sprkscl1160 "Link to this heading")

Note

This issue code has been **deprecated** since [Spark Conversion Core 4.1.0](../../../general/release-notes/README.html#spark-conversion-core-version-4-1-0)

Message: org.apache.spark.sql.functions.sum has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id231 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sum](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#sum(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id232 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.sum` function that generates this EWI. In this example, the `sum` function is used to calculate the sum of selected column.

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
val result1 = sum(col("elements"))
val result2 = sum("elements")
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1160` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
/*EWI: SPRKSCL1160 => org.apache.spark.sql.functions.sum has a workaround, see documentation for more info*/
val result1 = sum(col("elements"))
/*EWI: SPRKSCL1160 => org.apache.spark.sql.functions.sum has a workaround, see documentation for more info*/
val result2 = sum("elements")
```

Copy

**Recommended fix**

Snowpark has an equivalent [sum](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#sum(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
val result1 = sum(col("elements"))
val result2 = sum(col("elements"))
```

Copy

#### Additional recommendations[¶](#id233 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1154[¶](#sprkscl1154 "Link to this heading")

Message: org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info

Category: Warning

### Description[¶](#id234 "Link to this heading")

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.ceil](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html#ceil(columnName:String):org.apache.spark.sql.Column) function, which has a workaround.

#### Scenario[¶](#id235 "Link to this heading")

**Input**

Below is an example of the `org.apache.spark.sql.functions.ceil` function, first used with a column name as an argument, then with a column object and finally with a column object and a scale.

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
val result1 = df.withColumn("ceil", ceil("value"))
val result2 = df.withColumn("ceil", ceil(col("value")))
val result3 = df.withColumn("ceil", ceil(col("value"), lit(1)))
```

Copy

**Output**

The SMA adds the EWI `SPRKSCL1154` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result1 = df.withColumn("ceil", ceil("value"))
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result2 = df.withColumn("ceil", ceil(col("value")))
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result3 = df.withColumn("ceil", ceil(col("value"), lit(1)))
```

Copy

**Recommended fix**

Snowpark has an equivalent [ceil](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#ceil(e:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

For the overload that receives a column object and a scale, you can use the [callBuiltin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/functions$.html#callBuiltin(functionName:String,args:Any*):com.snowflake.snowpark.Column) function to invoke the Snowflake builtin [CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil) function. To use it, you should pass the string **“ceil”** as the first argument, the column as the second argument and the scale as the third argument.

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
val result1 = df.withColumn("ceil", ceil(col("value")))
val result2 = df.withColumn("ceil", ceil(col("value")))
val result3 = df.withColumn("ceil", callBuiltin("ceil", col("value"), lit(1)))
```

Copy

#### Additional recommendations[¶](#id236 "Link to this heading")

* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

## SPRKSCL1105[¶](#sprkscl1105 "Link to this heading")

This issue code has been **deprecated**

Message: Writer format value is not supported.

Category: Conversion Error

### Description[¶](#id237 "Link to this heading")

This issue appears when the [org.apache.spark.sql.DataFrameWriter.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html#format(source:String):org.apache.spark.sql.DataFrameWriter%5BT%5D) has an argument that is not supported by Snowpark.

#### Scenarios[¶](#id238 "Link to this heading")

There are some scenarios depending on the type of format you are trying to save. It can be a `supported`, or `non-supported` format.

##### Scenario 1[¶](#id239 "Link to this heading")

**Input**

The tool analyzes the type of format that is trying to save, the supported formats are:

* `csv`
* `json`
* `orc`
* `parquet`
* `text`

```
    dfWrite.write.format("csv").save(path)
```

Copy

**Output**

The tool transforms the `format` method into a `csv` method call when save function has one parameter.

```
    dfWrite.write.csv(path)
```

Copy

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2[¶](#id240 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

```
dfWrite.write.format("net.snowflake.spark.snowflake").save(path)
```

Copy

**Output**

The tool shows the EWI `SPRKSCL1105` indicating that the value `net.snowflake.spark.snowflake` is not supported.

```
/*EWI: SPRKSCL1105 => Writer format value is not supported .format("net.snowflake.spark.snowflake")*/
dfWrite.write.format("net.snowflake.spark.snowflake").save(path)
```

Copy

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3[¶](#id241 "Link to this heading")

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

```
val myFormat = "csv"
dfWrite.write.format(myFormat).save(path)
```

Copy

**Output**

Since the tool can not determine the value of the variable in runtime, shows the EWI `SPRKSCL1163` indicating that the value is not supported.

```
val myFormat = "csv"
/*EWI: SPRKSCL1163 => format_type is not a literal and can't be evaluated*/
dfWrite.write.format(myFormat).load(path)
```

Copy

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations[¶](#id242 "Link to this heading")

* The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
* The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/com/snowflake/snowpark/DataFrameWriter.html)
* For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) or post an issue [in the SMA](../../../user-guide/project-overview/configuration-and-settings.html#report-an-issue).

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The Snowpark Migration Accelerator tool (SMA) is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [SPRKSCL1126](#sprkscl1126)
2. [SPRKSCL1112](#sprkscl1112)
3. [SPRKSCL1143](#sprkscl1143)
4. [SPRKSCL1153](#sprkscl1153)
5. [SPRKSCL1102](#sprkscl1102)
6. [SPRKSCL1136](#sprkscl1136)
7. [SPRKSCL1167](#sprkscl1167)
8. [SPRKSCL1147](#sprkscl1147)
9. [SPRKSCL1116](#sprkscl1116)
10. [SPRKSCL1122](#sprkscl1122)
11. [SPRKSCL1173](#sprkscl1173)
12. [SPRKSCL1163](#sprkscl1163)
13. [SPRKSCL1132](#sprkscl1132)
14. [SPRKSCL1106](#sprkscl1106)
15. [SPRKSCL1157](#sprkscl1157)
16. [SPRKSCL1146](#sprkscl1146)
17. [SPRKSCL1117](#sprkscl1117)
18. [SPRKSCL1123](#sprkscl1123)
19. [SPRKSCL1172](#sprkscl1172)
20. [SPRKSCL1162](#sprkscl1162)
21. [SPRKSCL1133](#sprkscl1133)
22. [SPRKSCL1107](#sprkscl1107)
23. [SPRKSCL1156](#sprkscl1156)
24. [SPRKSCL1127](#sprkscl1127)
25. [SPRKSCL1113](#sprkscl1113)
26. [SPRKSCL1002](#sprkscl1002)
27. [SPRKSCL1142](#sprkscl1142)
28. [SPRKSCL1152](#sprkscl1152)
29. [SPRKSCL1103](#sprkscl1103)
30. [SPRKSCL1137](#sprkscl1137)
31. [SPRKSCL1166](#sprkscl1166)
32. [SPRKSCL1118](#sprkscl1118)
33. [SPRKSCL1149](#sprkscl1149)
34. [SPRKSCL1159](#sprkscl1159)
35. [SPRKSCL1108](#sprkscl1108)
36. [SPRKSCL1128](#sprkscl1128)
37. [SPRKSCL1169](#sprkscl1169)
38. [SPRKSCL1138](#sprkscl1138)
39. [SPRKSCL1129](#sprkscl1129)
40. [SPRKSCL1168](#sprkscl1168)
41. [SPRKSCL1139](#sprkscl1139)
42. [SPRKSCL1119](#sprkscl1119)
43. [SPRKSCL1148](#sprkscl1148)
44. [SPRKSCL1158](#sprkscl1158)
45. [SPRKSCL1109](#sprkscl1109)
46. [SPRKSCL1114](#sprkscl1114)
47. [SPRKSCL1145](#sprkscl1145)
48. [SPRKSCL1171](#sprkscl1171)
49. [SPRKSCL1120](#sprkscl1120)
50. [SPRKSCL1130](#sprkscl1130)
51. [SPRKSCL1161](#sprkscl1161)
52. [SPRKSCL1155](#sprkscl1155)
53. [SPRKSCL1104](#sprkscl1104)
54. [SPRKSCL1124](#sprkscl1124)
55. [SPRKSCL1175](#sprkscl1175)
56. [SPRKSCL1001](#sprkscl1001)
57. [SPRKSCL1141](#sprkscl1141)
58. [SPRKSCL1110](#sprkscl1110)
59. [SPRKSCL1100](#sprkscl1100)
60. [SPRKSCL1151](#sprkscl1151)
61. [SPRKSCL1165](#sprkscl1165)
62. [SPRKSCL1134](#sprkscl1134)
63. [SPRKSCL1125](#sprkscl1125)
64. [SPRKSCL1174](#sprkscl1174)
65. [SPRKSCL1000](#sprkscl1000)
66. [SPRKSCL1140](#sprkscl1140)
67. [SPRKSCL1111](#sprkscl1111)
68. [SPRKSCL1101](#sprkscl1101)
69. [SPRKSCL1150](#sprkscl1150)
70. [SPRKSCL1164](#sprkscl1164)
71. [SPRKSCL1135](#sprkscl1135)
72. [SPRKSCL1115](#sprkscl1115)
73. [SPRKSCL1144](#sprkscl1144)
74. [SPRKSCL1170](#sprkscl1170)
75. [SPRKSCL1121](#sprkscl1121)
76. [SPRKSCL1131](#sprkscl1131)
77. [SPRKSCL1160](#sprkscl1160)
78. [SPRKSCL1154](#sprkscl1154)
79. [SPRKSCL1105](#sprkscl1105)