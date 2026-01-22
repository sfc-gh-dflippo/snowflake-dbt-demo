---
auto_generated: true
description: The Snowpark Migration Accelerator (SMA) not only generates a comprehensive
  assessment of your code but can also convert specific elements from your source
  code into compatible formats for your target
last_scraped: '2026-01-14T16:52:01.468113+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/user-guide/conversion/how-the-conversion-works
title: 'Snowpark Migration Accelerator:  How the Conversion Works | Snowflake Documentation'
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../README.md)

        + General

          + [Introduction](../../general/introduction.md)
          + [Getting started](../../general/getting-started/README.md)
          + [Conversion software terms of use](../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../general/release-notes/README.md)
          + [Roadmap](../../general/roadmap.md)
        + User guide

          + [Overview](../overview.md)
          + [Before using the SMA](../before-using-the-sma/README.md)
          + [Project overview](../project-overview/README.md)
          + [Technical discovery](../project-overview/optional-technical-discovery.md)
          + [AI assistant](../chatbot.md)
          + [Assessment](../assessment/README.md)
          + [Conversion](README.md)

            - [How the conversion works](how-the-conversion-works.md)
            - [Conversion quick start](conversion-quick-start.md)
            - [Conversion setup](conversion-setup.md)
            - [Understanding the conversion assessment and reporting](understanding-the-conversion-assessment-and-reporting.md)
            - [Output code](output-code.md)
          + [Using the SMA CLI](../using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../use-cases/migration-lab/README.md)
          + [Sample project](../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../issue-analysis/approach.md)
          + [Issue code categorization](../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../translation-reference/translation-reference-overview.md)
          + [SIT tagging](../../translation-reference/sit-tagging/README.md)
          + [SQL embedded code](../../translation-reference/sql-embedded-code.md)
          + [HiveSQL](../../translation-reference/hivesql/README.md)
          + [Spark SQL](../../translation-reference/spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../workspace-estimator/overview.md)
          + [Getting started](../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../interactive-assessment-application/overview.md)
          + [Installation guide](../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../support/glossary.md)
          + [Contact us](../../support/contact-us.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)User guide[Conversion](README.md)How the conversion works

# Snowpark Migration Accelerator: How the Conversion Works[¶](#snowpark-migration-accelerator-how-the-conversion-works "Link to this heading")

The Snowpark Migration Accelerator (SMA) not only generates a comprehensive assessment of your code but can also convert specific elements from your source code into compatible formats for your target codebase. This conversion process follows the same steps as the initial assessment, with just one additional step.

## Conversion in the SMA[¶](#conversion-in-the-sma "Link to this heading")

In both assessment and conversion modes, the Snowpark Migration Accelerator (SMA):

* Searches through all files within a specified directory
* Detects which files contain code
* Analyzes the code files according to their programming language
* Creates a structured representation of the code (Abstract Syntax Tree or AST)
* Creates and fills a Symbol Table with program information
* Identifies and classifies any errors found
* Creates detailed reports of the results

All of these processes are repeated when you run SMA in conversion mode, even if you previously ran it in assessment mode. However, conversion mode includes one additional final step.

* Format the generated code from the Abstract Syntax Tree (AST) to improve readability

The Abstract Syntax Tree (AST) is a model that represents how your source code works. When the same functionality exists in both the source and target languages, SMA can generate equivalent code in the target language. This code generation only happens during the actual conversion process.

## Types of Conversion in the SMA[¶](#types-of-conversion-in-the-sma "Link to this heading")

The Snowpark Migration Accelerator (SMA) currently supports the following code conversions:

* Converts Python or Scala code from Spark API calls to equivalent Snowpark API calls

Note

The SMA does not perform any SQL conversion. For SQL files or SQL-only assessments, the tool provides assessment only, without any automated conversion.

Let’s examine an example written in both Scala and Python programming languages.

## Examples of Conversion of References to the Spark API to the Snowpark API[¶](#examples-of-conversion-of-references-to-the-spark-api-to-the-snowpark-api "Link to this heading")

### Example of Spark Scala to Snowpark[¶](#example-of-spark-scala-to-snowpark "Link to this heading")

When using Scala as your source language, the Snowpark Migration Accelerator (SMA) automatically converts Spark API references in your Scala code to their equivalent Snowpark API references. Below is an example that demonstrates how a basic Spark application is converted. The example application performs several common data operations:

* Reading data
* Filtering records
* Joining datasets
* Calculating averages
* Displaying results

Apache Spark Code Written in Scala

```
import org.apache.spark.sql._ 
import org.apache.spark.sql.functions._ 
import org.apache.spark.sql.SparkSession 

object SimpleApp {
  // This function calculates the average salary for jobs in a specific department
  def avgJobSalary(session: SparkSession, dept: String) {
    // Load employee data from CSV file
    val employees = session.read.csv("path/data/employees.csv")
    // Load job data from CSV file
    val jobs = session.read.csv("path/data/jobs.csv")

val jobsAvgSalary = employees
    .filter(column("Department") === dept)    // Filter employees by department
    .join(jobs)                              // Join with jobs table
    .groupBy("JobName")                      // Group results by job name
    .avg("Salary")                          // Calculate average salary for each job

// Calculate and display a list of all salaries in the department
jobsAvgSalary.select(collect_list("Salary")).show()

```scala
// Calculate and display the average salary
jobsAvgSalary.show()
}
```

Copy

The Code After Conversion to Snowflake:

```
import com.snowflake.snowpark._ 
import com.snowflake.snowpark.functions._ 
import com.snowflake.snowpark.Session 

object SimpleApp {
  // This function calculates the average salary for jobs in a specific department
  def avgJobSalary(session: Session, dept: String) {
    // Load employee data from CSV file
    val employees = session.read.csv("path/data/employees.csv")
    // Load job data from CSV file
    val jobs = session.read.csv("path/data/jobs.csv")

val jobsAvgSalary = employees
    .filter(column("Department") === dept)    // Filter employees by department
    .join(jobs)                              // Join with jobs table
    .groupBy("JobName")                      // Group results by job name
    .avg("Salary")                           // Calculate average salary per job

```scala
// Calculate and display all salaries in the department 
jobsAvgSalary.select(array_agg("Salary")).show()

// Display the average salary
jobsAvgSalary.show()
}
}
```

Copy

In this example, the code structure remains largely unchanged. However, the code has been updated to use Snowpark API references instead of Spark API references.

### Example of PySpark to Snowpark[¶](#example-of-pyspark-to-snowpark "Link to this heading")

When you choose Python as your source language, SMA automatically converts PySpark API calls in your Python code to their equivalent Snowpark API calls. Below is an example script that demonstrates various PySpark functions:

```
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Row

Create a Spark session by building and initializing a new SparkSession object, or retrieve an existing one if already available.

df = spark_session.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

# cube()
df.cube("name", df.age).count().orderBy("name", "age").show()

# take()
df_new1.take(2)

# describe()
df.describe(['age']).show()

# explain()
df.explain() 
df.explain("simple") # Physical plan
df.explain(True) 

# intersect()
df1 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3), ("c", 4)], ["C1", "C2"])
df2 = spark_session.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])

# where()
df_new1.where(F.col('Id2')>30).show()
```

Copy

The Code After Conversion to Snowflake:

```
from datetime import date, datetime
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
from snowflake.snowpark import Row

Create a Spark session using the Session builder:

spark_session = Session.builder.create()

df = spark_session.create_dataframe([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

# cube()
df.cube("name", df.age).count().sort("name", "age").show()

# take()
df_new1.take(2)

# describe()
df.describe(['age']).show()

# explain()
df.explain()
df.explain("simple") # Physical plan
df.explain(True)

# intersect()
df1 = spark_session.create_dataframe([("a", 1), ("a", 1), ("b", 3), ("c", 4)], ["C1", "C2"])
df2 = spark_session.create_dataframe([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])

# where()
df_new1.where(F.col('Id2')>30).show()
```

Copy

In this example, the code structure remains largely unchanged. However, the code has been updated to use Snowpark API calls instead of Spark API calls.

During the conversion process with the Snowpark Migration Accelerator (SMA), you can expect the following:

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

1. [Conversion in the SMA](#conversion-in-the-sma)
2. [Types of Conversion in the SMA](#types-of-conversion-in-the-sma)
3. [Examples of Conversion of References to the Spark API to the Snowpark API](#examples-of-conversion-of-references-to-the-spark-api-to-the-snowpark-api)