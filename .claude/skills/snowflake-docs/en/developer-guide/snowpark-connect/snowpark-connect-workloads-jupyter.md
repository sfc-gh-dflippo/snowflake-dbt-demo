---
auto_generated: true
description: You can run Spark workloads interactively from Jupyter Notebooks, VS
  Code, or any Python-based interface without needing to manage a Spark cluster. The
  workloads run on the Snowflake infrastructure.
last_scraped: '2026-01-14T16:54:55.354879+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-workloads-jupyter
title: Run Spark workloads from VS Code, Jupyter Notebooks, or a terminal | Snowflake
  Documentation
---

1. [Overview](../../developer.md)
2. Builders
3. [Snowflake DevOps](../builders/devops.md)
4. [Observability](../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../snowpark/index.md)
7. [Spark workloads on Snowflake](snowpark-connect-overview.md)

   * [Development clients](snowpark-connect-clients.md)

     + [Snowflake Notebook](snowpark-connect-workloads-snowflake-notebook.md)
     + [VS Code, Jupyter, or a terminal](snowpark-connect-workloads-jupyter.md)
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

[Developer](../../developer.md)[Spark workloads on Snowflake](snowpark-connect-overview.md)[Development clients](snowpark-connect-clients.md)VS Code, Jupyter, or a terminal

# Run Spark workloads from VS Code, Jupyter Notebooks, or a terminal[¶](#run-spark-workloads-from-vs-code-jupyter-notebooks-or-a-terminal "Link to this heading")

You can run Spark workloads interactively from Jupyter Notebooks, VS Code, or any Python-based interface without needing to manage a
Spark cluster. The workloads run on the Snowflake infrastructure.

For example, you can do the following tasks:

1. Confirm that you have prerequisites.
2. Set up your environment to connect with Snowpark Connect for Spark on Snowflake.
3. Install Snowpark Connect for Spark.
4. Run PySpark code from your client to run on Snowflake.

## Prerequisites[¶](#prerequisites "Link to this heading")

Confirm that your Python and Java installations are based on the same computer architecture. For example, if Python is based is arm64, Java
must also be arm64 (not x86\_64, for example).

## Set up your environment[¶](#set-up-your-environment "Link to this heading")

You can set up your development environment by ensuring the your code can connect to Snowpark Connect for Spark on Snowflake. To connect to Snowflake
client code will use a `.toml` file containing connection details.

If you have Snowflake CLI installed, you can use it to define a connection. Otherwise, you can manually write connection parameters in a
`config.toml` file.

### Add a connection by using Snowflake CLI[¶](#add-a-connection-by-using-sf-cli "Link to this heading")

You can use Snowflake CLI to add connection properties that Snowpark Connect for Spark can use to connect to Snowflake. Your changes are saved to a
`config.toml` file.

1. Run the following command to add a connection using the snow connection **add** command.

   ```
   snow connection add
   ```

   Copy
2. Follow the prompts to define a connection.

   Be sure to specify `spark-connect` as the connection name.

   This command adds a connection to your `config.toml` file, as in the following example:

   ```
   [connections.spark-connect]
   host = "example.snowflakecomputing.com"
   port = 443
   account = "example"
   user = "test_example"
   password = "password"
   protocol = "https"
   warehouse = "example_wh"
   database = "example_db"
   schema = "public"
   ```

   Copy
3. Run the following command to confirm that the connection works.

   You can test the connection in this way when you’ve added it by using Snowflake CLI.

   ```
   snow connection list
   snow connection test --connection spark-connect
   ```

   Copy

### Add a connection by manually writing a connection file[¶](#add-a-connection-by-manually-writing-a-connection-file "Link to this heading")

You can manually write or update a `connections.toml` file so that your code can connect to Snowpark Connect for Spark on Snowflake.

1. Run the following command to ensure that your `connections.toml` file allows only the owner (user) to have read and write access.

   ```
   chmod 0600 "~/.snowflake/connections.toml"
   ```

   Copy
2. Edit the `connections.toml` file so that it contains a `[spark-connect]` connection with the connection properties in the
   following example.

   Be sure to replace values with your own connection specifics.

   ```
   [spark-connect]
   host="my_snowflake_account.snowflakecomputing.com"
   account="my_snowflake_account"
   user="my_user"
   password="&&&&&&&&"
   warehouse="my_wh"
   database="my_db"
   schema="public"
   ```

   Copy

### Install Snowpark Connect for Spark[¶](#install-spconnect "Link to this heading")

You can install Snowpark Connect for Spark as a Python package.

1. Create a Python virtual environment.

   Confirm that your Python version is 3.10 or later and earlier than 3.13 by running `python3 --version`.

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Copy
2. Install the Snowpark Connect for Spark package.

   ```
   pip install --upgrade --force-reinstall 'snowpark-connect[jdk]'
   ```

   Copy
3. Add Python code to start a Snowpark Connect for Spark server and create a Snowpark Connect for Spark session.

   ```
   from snowflake import snowflake.snowpark_connect

   # Import snowpark_connect *before* importing pyspark libraries
   from pyspark.sql.types import Row

   spark = snowflake.snowpark_connect.server.init_spark_session()
   ```

   Copy

## Run Python code from your client[¶](#run-python-code-from-your-client "Link to this heading")

Once you have an authenticated connection in place, you can write code as you normally would.

You can run PySpark code that connects to Snowpark Connect for Spark by using the PySpark client library.

```
from pyspark.sql import Row

  df = spark.createDataFrame([
      Row(a=1, b=2.),
      Row(a=2, b=3.),
      Row(a=4, b=5.),])

  print(df.count())
```

Copy

## Run Scala code from your client[¶](#run-scala-code-from-your-client "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

You can run Scala applications that connect to Snowpark Connect for Spark by using the Spark Connect client library.

This guide walks you through setting up Snowpark Connect and connecting your Scala applications to the Snowpark Connect for Spark server.

### Step 1: Set up your Snowpark Connect for Spark environment[¶](#step-1-set-up-your-spconnect-environment "Link to this heading")

Set up your environment by using steps described in the following topics:

1. [Create a Python virtual environment and install Snowpark Connect](#label-snowpark-connect-client-env-setup).
2. [Set up a connection](#label-snowpark-connect-jupyter-install-spconnect).

### Step 2: Create a Snowpark Connect for Spark server script and launch the server[¶](#step-2-create-a-spconnect-server-script-and-launch-the-server "Link to this heading")

1. Create a Python script to launch the Snowpark Connect for Spark server.

   ```
   # launch-snowpark-connect.py

   from snowflake import snowpark_connect

   def main():
       snowpark_connect.start_session(is_daemon=False, remote_url="sc://localhost:15002")
       print("SAS started on port 15002")

   if __name__ == "__main__":
       main()
   ```

   Copy
2. Launch the Snowpark Connect for Spark server.

   ```
   # Make sure you're in the correct Python environment
   pyenv activate your-snowpark-connect-env

   # Run the server script
   python launch-snowpark-connect.py
   ```

   Copy

### Step 3: Set up your Scala application[¶](#step-3-set-up-your-scala-application "Link to this heading")

1. Add the Spark Connect client dependency to your build.sbt file.

   ```
   libraryDependencies += "org.apache.spark" %% "spark-connect-client-jvm" % "3.5.3"

   // Add JVM options for Java 9+ module system compatibility
   javaOptions ++= Seq(
     "--add-opens=java.base/java.nio=ALL-UNNAMED"
   )
   ```

   Copy
2. Execute Scala code to connect to the Snowpark Connect for Spark server.

   ```
   import org.apache.spark.sql.SparkSession
   import org.apache.spark.sql.connect.client.REPLClassDirMonitor

   object SnowparkConnectExample {
     def main(args: Array[String]): Unit = {
       // Create Spark session with Snowpark Connect
       val spark = SparkSession.builder().remote("sc://localhost:15002").getOrCreate()

       // Register ClassFinder for UDF support (if needed)
       // val classFinder = new REPLClassDirMonitor("target/scala-2.12/classes")
       // spark.registerClassFinder(classFinder)

       try {
         // Simple DataFrame operations
         import spark.implicits._

         val data = Seq(
           (1, "Alice", 25),
           (2, "Bob", 30),
           (3, "Charlie", 35)
         )

         val df = spark.createDataFrame(data).toDF("id", "name", "age")

         println("Original DataFrame:")
         df.show()

         println("Filtered DataFrame (age > 28):")
         df.filter($"age" > 28).show()

         println("Aggregated result:")
         df.groupBy().avg("age").show()

       } finally {
         spark.stop()
       }
     }
   }
   ```

   Copy
3. Compile and run your application.

   ```
   # Compile your Scala application
   sbt compile

   # Run the application
   sbt "runMain SnowparkConnectExample"
   ```

   Copy

### Scala UDF support on Snowpark Connect for Spark[¶](#scala-udf-support-on-spconnect "Link to this heading")

When using user-defined functions or custom code, do one of the following:

* Register a class finder to monitor and upload class files.

  ```
  import org.apache.spark.sql.connect.client.REPLClassDirMonitor

  val classFinder = new REPLClassDirMonitor("/absolute/path/to/target/scala-2.12/classes")
  spark.registerClassFinder(classFinder)
  ```

  Copy
* Upload JAR dependencies if needed.

  ```
  spark.addArtifact("/absolute/path/to/dependency.jar")
  ```

  Copy

### Troubleshoot Snowpark Connect for Spark installation[¶](#troubleshoot-spconnect-installation "Link to this heading")

With the following list of checks, you can troubleshoot Snowpark Connect for Spark installation and use.

* Ensure that Java and Python are [based on the same architecture](#label-snowpark-connect-jupyter-prereq).
* Use the most recent Snowpark Connect for Spark package file, as described in [Install Snowpark Connect for Spark](#label-snowpark-connect-jupyter-install-spconnect).
* Confirm that the **python** command with PySpark code is working correctly for local execution—that is, without Snowflake connectivity.

  For example, execute a command such as the following:

  ```
  python your_pyspark_file.py
  ```

  Copy

## Open source clients[¶](#open-source-clients "Link to this heading")

You can use standard, off-the-shelf open source software (OSS) Spark client packages—such as PySpark and Spark clients for Java or
Scala—from your preferred local environments, including Jupyter Notebooks and VS Code. In this way, you can avoid installing packages
specific to Snowflake.

You might find this useful if you want to write Spark code locally and have the code use Snowflake compute resources and enterprise governance.
In this scenario, you perform authentication and authorization through programmatic access tokens (PATs).

The following sections cover installation, configuration, and authentication. You’ll also find a simple PySpark example to validate your
connection.

### Step 1: Install Required Packages[¶](#step-1-install-required-packages "Link to this heading")

* Install `pyspark`. You don’t need to install any Snowflake packages.

  ```
  pip install "pyspark[connect]>=3.5.0,<4"
  ```

  Copy

### Step 2: Setup and Authentication[¶](#step-2-setup-and-authentication "Link to this heading")

1. Generate a programmatic access token (PAT).

   For more information, see the following topics:

   * [Using programmatic access tokens for authentication](../../user-guide/programmatic-access-tokens)
   * [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](../../sql-reference/sql/alter-user-add-programmatic-access-token)

   The following example adds a PAT named `TEST_PAT` for the user `sysadmin` and sets the expiration to 30 days.

   ```
   ALTER USER add PAT TEST_PAT ROLE_RESTRICTION = sysadmin DAYS_TO_EXPIRY = 30;
   ```

   Copy
2. Find your Snowflake Spark Connect host URL.

   Run the following SQL in Snowflake to find the hostname for your account:

   ```
   SELECT t.VALUE:type::VARCHAR as type,
          t.VALUE:host::VARCHAR as host,
          t.VALUE:port as port
     FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST()))) AS t where type = 'SNOWPARK_CONNECT';
   ```

   Copy

### Step 3: Connect to Spark Connect server[¶](#step-3-connect-to-spark-connect-server "Link to this heading")

* To connect to the Spark Connect server, use code such as the following:

  ```
  from pyspark.sql import SparkSession
  import urllib.parse

  # Replace with your actual PAT.
  pat = urllib.parse.quote("<pat>", safe="")

  # Replace with your Snowpark Connect host from the above SQL query.
  snowpark_connect_host = ""

  # Define database/schema/warehouse for executing your Spark session in Snowflake (recommended); otherwise, it will be resolved from your default_namespace and default_warehouse

  db_name = urllib.parse.quote("TESTDB", safe="")
  schema_name = urllib.parse.quote("TESTSCHEMA", safe="")
  warehouse_name = urllib.parse.quote("TESTWH", safe="")

  spark = SparkSession.builder.remote(f"sc://{snowpark_connect_host}/;token={pat};token_type=PAT;database={db_name};schema={schema_name};warehouse={warehouse_name}").getOrCreate()

  # Spark session is ready to use. You can write regular Spark DataFrame code, as in the following example:

  from pyspark.sql import Row

  df = spark.createDataFrame([
      Row(a=1, b=2.),
      Row(a=2, b=3.),
      Row(a=4, b=5.),])
  print(df.count())
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

On this page

1. [Prerequisites](#prerequisites)
2. [Set up your environment](#set-up-your-environment)
3. [Run Python code from your client](#run-python-code-from-your-client)
4. [Run Scala code from your client](#run-scala-code-from-your-client)
5. [Open source clients](#open-source-clients)

Related content

1. [Snowpark Connect for Spark compatibility guide](/developer-guide/snowpark-connect/snowpark-connect-compatibility)