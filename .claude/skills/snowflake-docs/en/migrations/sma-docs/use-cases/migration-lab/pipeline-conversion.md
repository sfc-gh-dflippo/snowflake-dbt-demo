---
auto_generated: true
description: The SMA has “converted” our scripts, but has it really? What it has actually
  done is converted all references from the Spark API to the Snowpark API, but what
  it has not done is to replace the connect
last_scraped: '2026-01-14T16:52:05.775144+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/migration-lab/pipeline-conversion
title: 'Snowpark Migration Accelerator: Pipeline Conversion | Snowflake Documentation'
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

          + [Overview](../../user-guide/overview.md)
          + [Before using the SMA](../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../user-guide/project-overview/README.md)
          + [Technical discovery](../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../user-guide/chatbot.md)
          + [Assessment](../../user-guide/assessment/README.md)
          + [Conversion](../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../assessment-walkthrough/README.md)
          + [Conversion walkthrough](../conversion-walkthrough.md)
          + [Migration lab](README.md)

            - [Compatibility and assessment](compatibility-and-assessment.md)
            - [Pipeline conversion](pipeline-conversion.md)
            - [Notebook conversion](notebook-conversion.md)
            - [Conclusions](conclusions.md)
          + [Sample project](../sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../sma-cli-walkthrough.md)
          + [Snowpark Connect](../snowpark-connect/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Migration lab](README.md)Pipeline conversion

# Snowpark Migration Accelerator: Pipeline Conversion[¶](#snowpark-migration-accelerator-pipeline-conversion "Link to this heading")

The SMA has “converted” our scripts, but has it really? What it has actually done is converted all references from the Spark API to the Snowpark API, but what it has not done is to replace the connections that may exist in your pipelines.

The SMA’s power is in the assessment reporting that it does as the conversion is tied to converting references from the Spark API to the Snowpark API. Note that the conversion of these references will not be enough to run any data pipeline. You will have to ensure that the pipeline’s connections are resolved manually. The SMA cannot assume to know connection parameters or other elements that are likely not available to be run through it.

As with any conversion, dealing with the converted code can be done in a variety of ways. The following steps are how we would **recommend** that you approach the output of the conversion tool. Like SnowConvert, the SMA requires attention to be paid to the output. No conversion will ever be 100% automated. This is particularly true for the SMA. Since the SMA is converting references from the Spark API to the Snowpark API, you will always need to check how those references are being run. It does not attempt to orchestrate the successful execution of any script or notebook run through it.

So we’ll follow these steps to work through the output of the SMA that will be slightly different than SnowConvert:

* **Resolve All Issues**: “Issues” here means the issues generated by the SMA. Take a look at the output code. Resolve parsing errors and conversion errors, and investigate warnings.
* **Resolve the session calls**: How the session call is written in the output code depends on where we are going to run the file. We will resolve this for running the code file(s) in the same location as they were originally going to be run, and then for running them in Snowflake.
* **Resolve the Input/Outputs**: Connections to different sources cannot be resolved entirely by the SMA. There are differences in the platforms, and the SMA will usually disregard this. This also is affected by where the file is going to be run.
* **Clean up and Test**! Let’s run the code. See if it works. We will be smoke testing in this lab, but there are tools to do more extensive testing and data validation including Snowpark Python Checkpoints.

So let’s take a look at what this looks like. We’re going to do this with two approaches: the first approach is to run this in Python on the local machine (as the source script is running). The second would be to do everything in Snowflake… in Snowsight, but for a data pipeline reading from a local source, this will not be 100% possible in Snowsight. That’s ok though. We are not converting the orchestration of this script in this POC.

Let’s start with the pipeline script file, and get to the notebook in the next section.

## Resolve Issues[¶](#resolve-issues "Link to this heading")

Let’s open our source and our output code in a code editor. You can use any code editor of your choice, but as has been mentioned multiple times, Snowflake would recommend using **VS Code with the Snowflake Extension**. Not only does the Snowflake Extension help navigate through the issues from SnowConvert, but can also run **Snowpark Checkpoints** for Python, which would help with testing and root cause analysis (though just barely out of scope for this lab).

Let’s open the directory that we originally created in the project creation screen (Spark ADW Lab) in VS Code:

![lab directory](../../../../_images/lab-directory.png)

Note that the **Output** directory structure will be the same as the input directory. Even the data file will be copied over despite no conversion taking place. There will also be a couple of **checkpoints.json** files that will be created by the SMA. These are json files that contain instructions for the Snowpark Checkpoints extension. The Snowflake extension can load checkpoints into both the source and output code based on the data in those files. We will ignore them for now.

Finally, let’s compare the input python script with the converted one in the output script.

![Script comparison](../../../../_images/script-comparison.png)

This is a very basic side-by-side comparison with the original Spark code on the left and the output Snowpark compatible code on the right. Looks like some imports were converted as well as the session call(s). We can see an EWI at the bottom of the image above, but let’s not start there. We need to find the parsing error before we do anything else.

We can search the document for the error code for that parsing error that was shown in both the UI and the issues.csv: **SPRKPY1101**.

![Error code](../../../../_images/error-code.png)

Since I have not filtered the results, the listing of this error code in the **issues.csv** also comes up in the search and the **AssessmentReport.json** that is used to build the **AssessmentReport.docx** summary assessment report. This is the main report that users will navigate through to understand a large workload, but we did not look at it in this lab. ([More info on the this report can be found in the SMA documentation](https://docs.snowconvert.com/sma/user-guide/assessment/output-reports/curated-reports).) Let’s choose where this EWI shows up in the **pipeline\_dimcustomer.py** file as shown above.

You can see that this line of code was present at the bottom of the source code.

```
# Conversion Input.
some rogue code that doesn't make any sense!

# Conversion Output.
some
# EWI: SPRKPY1101 => Unrecognized or invalid CODE STATEMENT @(131, 6). Last valid token was 'some' @(131, 1), failed token 'rogue' @(131, 6)
#     rogue code that doesn't make any sense!
```

Copy

Looks like this parsing error was because of… “some rogue code that doesn’t make any sense!”. This line of code is at the bottom of the pipeline file. This is not unusual to have extra characters or other elements in a code file as part of an extraction from a source. Note have the SMA detected that this was not valid Python code, and it generated the parsing error.

You can also see how the SMA inserts both the error code and the description into the output code as a comment where the error occurred. This is how all error messages will appear in the output.

Since this is not valid code, it is at the end of the file, and there is nothing else that was removed as a result of this error, the original code and the comment can safely be removed from the output code file.

And now we’ve resolved our first and most serious issue. Get excited.

Let’s work through the rest of our EWIs in this file. We can search for “EWI” because we now know that text will appear in the comment every time there is an error code. (Alternatively, we could sort the issues.csv file and order the issues by severity… but that’s not really necessary here.)

The next one is actually just a warning, not an error. It’s telling us that there was a function used that isn’t always equivalent in Spark and Snowpark:

```
#EWI: SPRKPY1067 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info.
split_col = split(df_uppercase['NAME'], '.first:')
```

Copy

The description here though gives away that we probably don’t have to worry about this. There are only two parameters being passed. Let’s leave this EWI as a comment in the file, so we know to check for it when we are running the file later.

The last one for this file is a conversion error saying that something is not supported:

![Not supported error](../../../../_images/not-supported-error.png)

This is the write call to the spark jdbc driver to write the output dataframe into SQL Server. Since this is part of the “resolve all inputs/outputs” step that we are going to deal with after we address our issues, we’ll leave this for later. Note, however, that this error must be resolved. The previous one was just a warning and may still work with no change being made.

## Resolving the Session Calls[¶](#resolving-the-session-calls "Link to this heading")

The session calls are converted by the SMA, but you should pay special attention to them to make sure they are functional. In our pipeline script, this is the before and after code:

![Script before and after](../../../../_images/script-before-and-after.png)

The SparkSession reference was changed to Session. You can see that reference change near the top of this file in the import statement as well:

![Reference change](../../../../_images/reference-change.png)

Note in the image above, the variable assignment of the session call to “spark” is not changed. This is because this is a variable assignment. It is not necessary to change this, but if you’d like to change the “spark” decorator to “session”, that would be more in line with what Snowpark recommends. (Note that the VS Code Extension “SMA Assistant” will suggest these changes as well.)

This is a simple exercise, but it’s worth doing. You can do a find and replace using VS Code’s own search ability to find the references to “spark” in this file and replace them with session. You can see the result of this in the image below. The references to the “spark” variable in the converted code have been replaced with “session”:

![Spark variables converted to session](../../../../_images/spark-variables-converted-to-session.png)

We also can remove something else from this session call. Since we are not going to be running “spark” anymore, we do not need to specify the driver path for the spark driver. So we can remove the config function entirely from the session call like this:

```
# Old Converted output.
# Spark Session
session = Session.builder.config('spark.driver.extraClassPath', driver_path) \
                    .app_name('SparkSQLServerExample', True) \
                    .getOrCreate()

# New Converted Output
# Snowpark Session
session = Session.builder.app_name('SparkSQLServerExample', True).getOrCreate()
```

Copy

Might as well convert it to a single line. The SMA couldn’t be sure we didn’t need that driver (although that seems logical), so it did not remove it. But now that we have our session call is complete.

(Note that the SMA also adds a “query tag” to the session. This is to help troubleshoot issues with this session or query later on, but this is completely optional to leave or remove.)

### Notes on the Session Calls[¶](#notes-on-the-session-calls "Link to this heading")

Believe it or not that is all that we need to change in the code for the session call, but that’s not all we need to do to create the session. This refers back to the original question that a lot of this depends on where you want to run these files. These original spark session calls used a configuration that was setup elsewhere. If you look at the original Spark session call it’s looking for a config file that is being read into a pandas dataframe location at the start of this script file (this is actually true for our notebook file as well).

![Config file reference](../../../../_images/config-file-reference.png)

Snowpark can function the same way, and this conversion assumes that is how this user will run this code. However, for the existing session call to work, the user would have to load all of the information for their Snowflake account into the local (or at least accessible) connections.toml file on this machine, and that the account they are attempting to connect to is set as the default. [You can learn more about updating the connections.toml file in the Snowflake/Snowpark documentation](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session#connect-by-using-the-connections-toml-file), but the idea behind it is that there is an accessible location that has the credentials. When a snowpark session is created, it is going to check this… unless the connection parameters are explicitly passed to the session call.

The standard way to do this is to input the connection parameters directly as strings and call them with the session:

```
# Parameters in a dictionary.
connection_parameters = {
  "account": "<your snowflake account>",
  "user": "<your snowflake user>",
  "password": "<your snowflake password>",
  "role": "<your snowflake role>",  # optional
  "warehouse": "<your snowflake warehouse>",  # optional
  "database": "<your snowflake database>",  # optional
  "schema": "<your snowflake schema>",  # optional
}

# The session call
session = Session.builder.configs(connection_parameters).app_name("AdventureWorksSummary", True).getOrCreate()
```

Copy

AdventureWorks appears to have referenced a file with these credentials and called it. Assuming there is a similar file called ‘snowflake\_credentials.txt’ that is accessible, then the syntax that would match that could look something like:

```
# Load into a dataframe.
snow_creds = pd.read_csv('snowflake_credentials.txt', index_col=None, header=0)

# Build the parameters.
connection_parameters = {
  "account": snow_creds.loc[snow_creds['Specific_Element'] == 'Account', 'Value'].item(),
  "user": snow_creds.loc[snow_creds['Specific_Element'] == 'Username', 'Value'].item(),
  "password": snow_creds.loc[snow_creds['Specific_Element'] == 'Password', 'Value'].item(),
  "role": "<your snowflake role>",  # optional
  "warehouse": snow_creds.loc[snow_creds['Specific_Element'] == 'Warehouse', 'Value'].item(),  # optional
  "database": snow_creds.loc[snow_creds['Specific_Element'] == 'Database', 'Value'].item(),  # optional
  "schema": snow_creds.loc[snow_creds['Specific_Element'] == 'Schema', 'Value'].item(),  # optional
}

# Then pass the parameters to the configs function of the session builder.
session = Session.builder.configs(connection_parameters).app_name("AdventureWorksSummary", True).getOrCreate()
```

Copy

For the purpose of the time limit on this lab, the first option may make more sense. [There’s more on this in the Snowpark documentation](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session#connect-by-specifying-connection-parameters).

Note that for our notebook file to run inside of Snowflake using Snowsight, you wouldn’t need to do any of this. You would just call the active session and run it.

Now it’s time for the most critical component of this migration, resolving any input/output references.

## Resolving the Inputs and Outputs[¶](#resolving-the-inputs-and-outputs "Link to this heading")

So let’s resolve our inputs and outputs now. Note that this is going to diverge based on whether you’re running the files locally or Snowflake. for the python script, Let’s make sure what we gain/lose by running directly inside of Snowsight: **you cannot run the whole operation in Snowsight** (at least not currently). The local csv file is not accessible from Snowsight. You will have to load the .csv file into a stage manually. This will likely not be an ideal solution, but we can test the conversion by doing this.

So we’ll first prep this file to be run/orchestrated locally, and then to be run in Snowflake.

To get the pipeline script’s inputs and output resolved, we need to first identify them. They are pretty simple. This script seems to:

* access a local file
* load the result into SQL Server (but now Snowflake)
* moves the file to make way for the next one

Simple enough. So we need to replace each component of the code that does those things. Let’s start with accessing the local file.

As was mentioned at the start of this, it would be strongly suggested to rearchitect the Point of Sale System and the orchestration tools used to run this python script, to put the output file into a cloud storage location. Then you could turn that location into an External Table, and voila… you are in Snowflake. However, the current architecture says that this file is not in a cloud storage location and will stay where it is, so we need to create a way for Snowflake to access this file preserving the existing logic.

We have options to do this, but we will create an internal stage and move the file into the stage with the script. We would then need to move the file in the local file system, and also move it in the stage. This can all be done with Snowpark. Let’s break it down:

* accessing a local file: Create an internal stage (it one doesn’t exist already) -> Load the file into the stage -> Read the file into a dataframe
* loading the result into SQL Server: Load the transformed data into a table in Snowflake
* moves the file to make way for the next one: Move the local file -> Move the file in the stage.

Let’s look at code that can do each of these things.

### Access a Locally Accessible File[¶](#access-a-locally-accessible-file "Link to this heading")

This source code in Spark looks like this:

```
# Spark read from a local csv file.
df = spark.read.csv('customer_update.csv', header=True, inferSchema=True)
```

Copy

And the transformed snowpark code (by the SMA) looks like this:

```
# Snowpark read from a local csv file.
df = session.read.option("PARSE_HEADER", True).option("INFER_SCHEMA", True).csv('customer_update.csv')
```

Copy

We can replace that with this with code that does the steps above:

1. Create an internal stage (if one does not exist already). We will create a stage called ‘LOCAL\_LOAD\_STAGE’ and go through a few steps to make sure that the stage is r

```
# Create a stage if one does not already exist.
# name the stage we're going to use.
target_stage_name = "LOCAL_LOAD_STAGE"

# Check to see if this stage already exists.
stages = session.sql("SHOW STAGES").collect()
target_stages = [stage for stage in stages if stage['name'] == target_stage_name]

# Create the stage if it does not already exist.
if(len(target_stages) < 1):
    from snowflake.core import Root
    from snowflake.core.stage import Stage, StageEncryption, StageResource
    root = Root(session)
    my_stage = Stage(name="LOCAL_LOAD_STAGE",encryption=StageEncryption(type="SNOWFLAKE_SSE"))
    root.databases["ADVENTUREWORKS"].schemas["DBO"].stages.create(my_stage)
    print('%s created.'%(target_stage_name))
else:
    print('%s already exists.'%(target_stage_name))
```

Copy

2. Load the file into the stage.

```
# Move the file.
put_results = session.file.put(local_file_name="customer_update.csv",
                    stage_location="ADVENTUREWORKS.DBO.LOCAL_LOAD_STAGE",
                    overwrite=False,
                    auto_compress=False)

# Read the results.
for r in put_results:
    str_output = ("File {src}: {stat}").format(src=r.source,stat=r.status)
    print(str_output)
```

Copy

3. Read the file into a dataframe. This is the part that the SMA actually converted. We need to specify that the location of the file is now the internal stage.

```
# Location of the file in the stage.
csv_file_path = "@LOCAL_LOAD_STAGE/customer_update.csv"

# Spark read from a local csv file.
df = session.read.option("PARSE_HEADER", True).option("INFER_SCHEMA", True).csv(csv_file_path)
```

Copy

The result of that would look like this:

![Rewritten code](../../../../_images/rewritten-code.png)

Let’s move on to the next step.

### Load the result into Snowflake[¶](#load-the-result-into-snowflake "Link to this heading")

The original script wrote the dataframe into SQL Server. Now we are going to load into Snowflake. This is a much simpler conversion. The dataframe is already a Snowpark dataframe. This is one of the advantages of Snowflake. Now that the data is accessible to Snowflake, everything happens inside Snowflake.

```
# Original output from the conversion tool.
# Write the DataFrame to SQL Server.
#EWI: SPRKPY1002 => pyspark.sql.readwriter.DataFrameWriter.jdbc is not supported
df_transformed.write.jdbc(url=sql_server_url,
              table='dbo.DimCustomer',
              mode="append",
              properties={
                  "user": sql_server_user,
                  "password": sql_server_password,
                  "driver": driver_path
              })

# Corrected Snowflake/Snowpark code.
df_transformed.write.save_as_table("ADVENTUREWORKS.DBO.DIMCUSTOMER", mode="append")
```

Copy

Note that we may want to write to a temp table to do some testing/validation, but this is the behavior in the original script.

### Move the file to make way for the next one[¶](#move-the-file-to-make-way-for-the-next-one "Link to this heading")

This is the behavior in the orginal script. We don’t really need to make this happen in Snowflake, but we can to showcase the exact same functionality in the stage. This is done with an os command in the original file system. That does not depend on Spark and will remain the same. But to emulate this behavior in snowpark, we would need to move this file in the stage to a new directory.

This can be done simply enough with the following python code:

```
# New filename.
original_filepath = '@LOCAL_LOAD_STAGE/customer_update.csv'
new_filepath = '@LOCAL_LOAD_STAGE/old_versions/customer_update_%s.csv'%(today_time)

copy_sql = f"COPY FILES INTO {new_filepath} FROM {original_filepath}"
session.sql(copy_sql).collect()
print(f"File copied from {original_filepath} to {new_filepath}")

remove_sql = f"REMOVE {original_filepath}"
session.sql(remove_sql).collect()
print(f"Original file {original_filepath} removed.")
```

Copy

Note that this would not replace any of the existing code. Since we already want to keep the existing motion of moving the spark code to snowpark, we will leave the os reference. The final version will look like this:

![Final code](../../../../_images/final-code.png)

Now we have the same motion completely done. Now let’s do our final cleanup, and test this script out.

## Clean up and Test[¶](#clean-up-and-test "Link to this heading")

We never looked at our import calls and we have config files that are not necessary at all. We could leave the references to the config files and run the script. In fact, assuming those config files are still accessible, then the code will still run. But if we’re taking a close look at our import statements, we might as well remove them. These files are represented by all of the code between the import statements and the session call:

![Removed statements](../../../../_images/removed-statements.png)

There’s a few other things we should do:

* Check that all of our imports are still necessary. We can leave them for now. If there is an erorr, we can address it.
* We also have one EWI that we left in there as a warning to check. So we want to make sure we inspect that output.
* We need to make sure that our file system behavior mirrors that of the expected file system for the POS system. To do this, we should move the customer\_update.csv file into the root folder you chose when first launching VS Code.
* Create a directory called “old\_versions” in that same directory. This should allow the os operations to run.

Finally, if you are not comfortable running the code directly into the production table, you can create a copy of that table for this test, and point the load to that copy. Replace the load statement with the one below. Since this is a lab, feel free to write to the “production” table:

```
# In case we want to test.
create_sql = """
                CREATE OR REPLACE TABLE ADVENTUREWORKS.DBO.DIMCUSTOMER_1
                AS select * from ADVENTUREWORKS.DBO.DIMCUSTOMER;
                """
session.sql(create_sql).collect()

# Write the DataFrame to SQL Server.
df_transformed.write.save_as_table("ADVENTUREWORKS.DBO.DIMCUSTOMER_1", mode="append")
```

Copy

Now we’re finally ready to test this out. We can run this script in Python to a testing table and see if it will fail. So run it!

Tragic! The script failed with the following error:

![Script fail error](../../../../_images/script-fail-error.png)

It looks like the way we are referencing an identifier is not the way that Snowpark wanted it. The code that failed is in the exact spot where the remaining EWI is:

![Code line responsible for error](../../../../_images/code-line-responsible-for-error.png)

You could reference the documentation on the link provided by the error, but in the interest of time, Snowpark needs this variable to expressly be a literal. We need to make the following replacement:

```
# Old
split_col = split(df_uppercase['NAME'], '.first:')

# New
split_col = split(df_uppercase['NAME'], lit('.first:'))
```

Copy

This should take care of this error. Note that there are always going to be some functional differences between source and a target platforms. Conversion tools like the SMA like to make these differences as obvious as possible. But note that no conversion is 100% automated.

Let’s run it again. This time… success!

![Success message](../../../../_images/success-message.png)

We can write some queries in python to validate this, but why don’t we just go into Snowflake (because that’s what we’re about to do anyways).

Navigate to your snowflake account that you have been using to run these scripts. This should be the same one you used to load the database from SQL Server (and if you haven’t done that, the above scripts won’t work anyways beecause the data has not yet been migrated).

You can quickly check this by seeing if the stage was created with the file:

![Created stage located](../../../../_images/created-stage-located.png)

Enable the directory table view to see if the old\_versions folder is in there:

![Enable Directory Table button](../../../../_images/enable-directory-table-button.png)

And it is:

![old_versions folder located](../../../../_images/old_versions-folder-located.png)

Since that was the last element of our script, it looks like we’re good!

We can also simply validate that the data was loaded by simply querying the table for the data we uploaded. You can open a new worksheet and simply write this query:

```
select * from ADVENTUREWORKS.DBO.DIMCUSTOMER
where FIRSTNAME like '%Brandon%'
AND LASTNAME like '%Carver%'
```

Copy

This is one of the names that was just loaded. And it looks like our pipeline has worked:

![Successful query](../../../../_images/successful-query.png)

## Running the Pipeline Script in Snowsight[¶](#running-the-pipeline-script-in-snowsight "Link to this heading")

Let’s take a quick look back at the flow we are attempting to convert was doing in Spark:

* accessing a local file
* loading the result into SQL Server
* moving the file to make way for the next one

This flow is not possible to run entirely from within Snowsight. Snowsight does not have access to a local file system. The recommendation here would be to move the export from the POS to a data lake… or any number of other options that would be accessible via Snowsight.

We can, however, take a closer look at how Snowpark handles the transformation logic by running the Python script in Snowflake. If you have already made the changes recommended above, you can run the body of the script in a Python Worksheet in Snowflake.

To do this, first login to your Snowflake account and navigate to the worksheets section. In this worksheet, create a new Python worksheet:

![Worksheets menu items](../../../../_images/worksheets-menu-items.png)

Specify the database, schema, role, and warehouse you’d like to use:

![Menu for database and schema](../../../../_images/menu-for-database-and-schema.png)

Now we do not have to deal with our session call. You will see a template generated in the worksheet window:

![Generated Python template](../../../../_images/generated-python-template.png)

Let’s start by bringing over our import calls. After making the previous script ready to use, we should have the following set of imports:

```
# General Imports
import pandas as pd
import os
import shutil
import datetime

# Snowpark Imports
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import upper
from snowflake.snowpark.functions import lower
from snowflake.snowpark.functions import split
from snowflake.snowpark.functions import trim
from snowflake.snowpark.functions import when
from snowflake.snowpark.functions import lit
from snowflake.snowpark.functions import expr
from snowflake.snowpark.functions import regexp_replace
```

Copy

We only need the snowpark imports. We will not be moving files around a file system. We could keep the datetime reference if we want to move the file in the stage. (Let’s do it.)

Paste the Snowpark imports (plus datetime) in the python worksheet below the other imports that are already present. Note that ‘col’ is already imported, so you can remove one of those:

![New code with pasted imports](../../../../_images/new-code-with-pasted-imports.png)

Under the “def main” call, let’s paste in all of our transformation code. This will include everything from the assignment of the csv location to the writing of the dataframe to a table.

From here:

![Copied code](../../../../_images/copied-code.png)

To here:

![Pasted code](../../../../_images/pasted-code.png)

We can also add back in the code that moves the files around in the stage. This part:

![Added code](../../../../_images/added-code.png)

Before you can run the code though, you will have to manually create the stage and move the file into the stage. We can add the create stage statement into the script, but we would still need to manually load the file into the stage.

So if you open another worksheet (this time… a sql worksheet), you can run a basic SQL statement that will create the stage:

```
CREATE STAGE my_int_stage
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

Copy

Make sure to select the correct database, schema, role, and warehouse:

![Database and schema selected](../../../../_images/database-and-schema-selected.png)

You can also [create an internal stage directly in the Snowsight UI](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage#create-a-named-stage-using-snowsight). Now that the stage exists, we can manually load the file of interest into the stage. Navigate to the Databases section of the Snowsight UI, and find the stage we just created in the appropriate database.schema:

![Stage located in schema](../../../../_images/stage-located-in-schema.png)

Let’s add our csv file by selecting the +Files option in the top right corner of the window. This will launch the Upload Your Files menu:

![Upload Your Files menu](../../../../_images/upload-your-files-menu.png)

Drag and drop or browse to our project directory and load the customer\_update.csv file into the stage:

![customer_update file uploaded](../../../../_images/customer_update-file-uploaded.png)

Select Upload in the bottom right corner of the screen. You will be taken back to the stage screen. To view the files, you will need to select Enable Directory Table:

![Enable Directory Table button](../../../../_images/enable-directory-table-button-for-stage.png)

And now… our file appears in the stage:

![Uploaded file in stage](../../../../_images/uploaded-file-in-stage.png)

This is not really a pipeline anymore, of course. But at least we can run the login in Snowflake. Run the rest of the code that you moved into the worksheet. This user had success the first time, but that’s no guarantee of success the second time:

![Results of query execution](../../../../_images/results-of-query-execution.png)

Note that once you’ve defined this function in Snowflake, you can call it in other ways. If AdventureWorks is 100% replacing their POS, then it may make sense to have the transformation logic in Snowflake, especially if orchestration and file movement will be handled somewhere else entirely. This allows Snowpark to focus on where it excels with the transformation logic.

## Conclusion[¶](#conclusion "Link to this heading")

And that’s it for the script file. It’s not the best example of a pipeline, but it does hit hard on how to deal with the output from the SMA:

* Resolve All Issues
* Resolve the session calls
* Resolve the Input/Outputs
* Clean up and Test!

Let’s move on to the reporting notebook.

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

1. [Resolve Issues](#resolve-issues)
2. [Resolving the Session Calls](#resolving-the-session-calls)
3. [Resolving the Inputs and Outputs](#resolving-the-inputs-and-outputs)
4. [Clean up and Test](#clean-up-and-test)
5. [Running the Pipeline Script in Snowsight](#running-the-pipeline-script-in-snowsight)
6. [Conclusion](#conclusion)