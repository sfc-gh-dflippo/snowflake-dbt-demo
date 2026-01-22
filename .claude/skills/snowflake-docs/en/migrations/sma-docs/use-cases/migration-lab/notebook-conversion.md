---
auto_generated: true
description: 'Let’s step over to the Reporting Notebook in our codebase: Basic Reporting
  Notebook - SqlServer Spark.ipynb. We’re going to walk through a similar set of steps
  as we did with the pipeline script.'
last_scraped: '2026-01-14T16:52:05.208146+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/migration-lab/notebook-conversion
title: 'Snowpark Migration Accelerator: Notebook Conversion | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Migration lab](README.md)Notebook conversion

# Snowpark Migration Accelerator: Notebook Conversion[¶](#snowpark-migration-accelerator-notebook-conversion "Link to this heading")

Let’s step over to the Reporting Notebook in our codebase: **Basic Reporting Notebook - SqlServer Spark.ipynb**. We’re going to walk through a similar set of steps as we did with the pipeline script.

* **Resolve All Issues**: “Issues” here means the issues generated by the SMA. Take a look at the output code. Resolve parsing errors and conversion errors, and investigate warnings.
* **Resolve the session calls**: How the session call is written in the output code depends on where we are going to run the file. We will resolve this for running the code file(s) in the same location as they were originally going to be run, and then for running them in Snowflake.
* **Resolve the Input/Outputs**: Connections to different sources cannot be resolved entirely by the SMA. There are differences in the platforms, and the SMA will usually disregard this. This also is affected by where the file is going to be run.
* **Clean up and Test**! Let’s run the code. See if it works. We will be smoke testing in this lab, but there are tools to do more extensive testing and data validation including Snowpark Python Checkpoints.

Let’s get started.

## Resolve All Issues[¶](#resolve-all-issues "Link to this heading")

Let’s go ahead and look at the issues present in the notebook.

(Note that you can open the notebook in VS Code, but to view it appropriately, you may want to install the Jupyter extension for VS Code. Alternatively, you could open this in Jupyter, but Snowflake still recommends VS Code with the Snowflake extension installed).

You can use the compare feature to view both of these side by side as we did with the pipeline file, though it will look more like a json if you do so:

![Converted code comparison](../../../../_images/converted-code-comparison.png)

Not that there are only two unique EWI’s in this notebook. You can return to the search bar to find them, but since this is so short, you could also just… scroll down. These are the unique issues:

* **SPRKPY1002** => *pyspark.sql.readwriter.DataFrameReader.jdbc is not supported*. This is a similar issue to the one we saw in the pipeline file, but that was a write call. This is a read call to the SQL Server database. We will resolve this in a bit.
* **SPRKPY1068** => *“pyspark.sql.dataframe.DataFrame.toPandas is not supported if there are columns of type ArrayType, but it has a workaround. See documentation for more info.* This is another warning. If we pass an array to this function in Snowpark, it may not work. Let’s keep an eye on this when we test it.

And that’s it for the notebook… and our issues. We resolved a parsing error, recognized that we will have to fix the input/outputs, and there’s a couple of potential functional differences we should keep an eye on. Let’s move on to the next step: resolving any session calls.

## Resolve the Session Calls[¶](#resolve-the-session-calls "Link to this heading")

To update the session calls in the reporting notebook, we need to locate the cell with the session call in it. That looks like this:

![Cell with session call](../../../../_images/cell-with-session-call.png)

Now let’s do what we already did for our pipeline file:

* Change all references to the “spark” session variable to “session” (note that this is throughout the notebook)
* Remove the config function with the spark driver.

The before and after on this will look like this:

```
# Old Session
spark = Session.builder.config('spark.driver.extraClassPath', driver_path).app_name("AdventureWorksSummary", True).getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":7,"minor":4,"patch":10},"attributes":{"language":"Python"}})

# New Session
# Session
session = Session.builder.app_name("AdventureWorksSummary", True).getOrCreate()
session.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":7,"minor":4,"patch":10},"attributes":{"language":"Python"}})
```

Copy

Note that there is other code in this cell. This code:

```
url = sql_server_url
properties = {'user' : sql_server_user, 'password' : sql_server_password}
# Spark dataframe.
#EWI: SPRKPY1002 => pyspark.sql.readwriter.DataFrameReader.jdbc is not supported
df = session.read.jdbc(url = url, table = 'dbo.DimCustomer', properties = properties)
print('Session successfully setup.')
```

Copy

We’re almost ready to take on the read statement, but we’re not there yet. Let’s just move all of this to another cell. Create a new cell below this one, and move this code to that cell. It will look like this:

![Code in new cell](../../../../_images/code-in-new-cell.png)

Is this all we need for the session call? No. Recall (and possibly review) the previous page under [**Notes on Session Calls**](pipeline-conversion.html#notes-on-the-session-calls). You will either need to make sure that your connection.toml file has your connection information or you will need to explicitly specify the connection parameters you intend to use in the session.

## Resolving the Inputs/Outputs[¶](#resolving-the-inputs-outputs "Link to this heading")

So let’s resolve our inputs and outputs now. Note that this is going to diverge based on whether you’re running the files locally or Snowflake, but for the notebook, everything can be run locally or in Snowflake. The code will be a bit simpler as we won’t even need to call a session. We’ll just… get the active session. As with the pipeline file, we’ll do this in two parts: to be run/orchestrated locally, and to be run in Snowflake.

Working through the inputs and outputs in the reporting notebook will be considerably simpler than it was for the pipeline. There is no reading from a local file or moving data between files. There is simply a read from a table in SQL Server that is now a read from a table in Snowflake. Since we will not be accessing SQL Server, we can ditch any reference to the SQL Server properties. And the read statement can be replaced by a table statement in Snowflake. The before and after for this cell should look like this:

```
# Before
url = sql_server_url
properties = {'user' : sql_server_user, 'password' : sql_server_password}
# Spark dataframe.
#EWI: SPRKPY1002 => pyspark.sql.readwriter.DataFrameReader.jdbc is not supported
df = session.read.jdbc(url = url, table = 'dbo.DimCustomer', properties = properties)
print('Session successfully setup.')
```

Copy

```
# After
# New table call
# Snowpark Dataframe table.
df = session.table('ADVENTUREWORKS.DBO.DIMCUSTOMER')
print('Table loaded successfully.')
df.show()
```

Copy

![Before and after for cell](../../../../_images/before-and-after-for-cell.png)

That’s actually… it. Let’s move on to the Clean up and test part of the notebook file.

## Clean Up and Test[¶](#clean-up-and-test "Link to this heading")

Let’s do some clean up (like we did previously for the pipeline file). We never looked at our import calls and we have config files that are not necessary at all. Let’s start by removing the references to the config files. This will be each of the cells between the import statements and the session call.

![Config file references removed](../../../../_images/config-file-references-removed.png)

Now let’s look at our imports. The reference to the os can be deleted. (Seems like that wasn’t used in the original file either…) There is a pandas reference. There does not appear to be any usages of pandas in this notebook anymore now that the config files are referenced. There is a toPandas reference as part of the Snowpark dataframe API in the reporting section, but that’s not part of the pandas library.

You can optionally replace all of the import calls to pandas with the modin pandas library. This library will optimize pandas dataframes to take advantage of Snowflake’s powerhouse computing. This change would look like this:

```
# Old
import pandas as pd

# New
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
```

Copy

Having said that, we can delete that one as well. Note that the SMA has replaced any spark specific import statements with those related to Snowpark. The final import cell would look like this:

![Imports edited](../../../../_images/imports-edited.png)

And that’s it for our cleanup. We still have a couple of EWIs in the reporting and visualization cells, but it looks like we should make it. Let’s run this one and see if we get an output.

![Successful run with output](../../../../_images/successful-run-with-output.png)

And we did. The reports seem to match what was output by the Spark Notebook. Even though the reporting cells seemed complex, Snowpark is able to work with them. The SMA let us know there could be an issue, but there doesn’t appear to be any problems. More testing would help, but our first round of smoke testing has passed.

Now let’s look at this notebook in Snowsight. Unlike the pipeline file, we can do this entirely in Snowsight.

## Running the Notebook in Snowsight[¶](#running-the-notebook-in-snowsight "Link to this heading")

Let’s take the version of the notebook that we have right now (having worked through the issues, the session calls, and the inputs and outputs) and load it into Snowflake. To do this, go to the notebooks section in SnowSight:

![Snowsight Notebooks section](../../../../_images/snowsight-notebooks-section.png)

And select down arrow next to the +Notebook button in the top right, and select “Import .ipynb file” (shown above).

Once this has been imported, choose the notebook file that we have been working with in the output directory created by the SMA in your project folder.

There will be a create notebook dialog window that opens. For this upload, we will choose the following options:

* Notebook location:

  + Database: **ADVENTUREWORKS**
  + Schema: **DBO**
* Python environment: **Run on warehouse**

  + This is not a large notebook with a bunch of ml. This is a basic reporting notebook. We can run this on a warehouse.
* Query warehouse: **DEFAULT\_WH**
* Notebook warehouse: **DEFAULT\_WH** (you can leave it as the system chosen warehouse (will be a streamlit warehouse)… for this notebook, it will not matter)

You can see these selections below:

![Create notebook page](../../../../_images/create-notebook-page.png)

This should load your notebook into Snowflake and it will look something like this:

![Notebook loaded in Snowflake](../../../../_images/notebook-loaded-in-snowflake.png)

There are a couple of quick checks/changes we need to make from the version we just tested locally in order to ensure that the notebook runs in Snowsight:

* Change the session calls to retrieve the active session
* Ensure any dependent libraries we need to install are available

Let’s start with the first one. It may seem odd to alter the session call again after we spent so much time on it in the first place, but we’re running inside of Snowflake now. You can remove anything associated with reading the session call and replacing it with the “get\_active\_session” call that is standard at the top of most Snowflake notebooks:

```
//# Old for Jupyter
session = Session.builder.app_name("AdventureWorksSummary", True).getOrCreate()

# New for Snowsight
from snowflake.snowpark.context import get_active_session
session = get_active_session()
```

Copy

We don’t need to specify connection parameters or update a .toml file because we are already connected. we are in Snowflake.

Let’s replace the old code in the cell with the new code. That will look something like this:

![New code in cell](../../../../_images/new-code-in-cell.png)

Now let’s address the available packages for this run, but instead of us figuring out what we need to add. Let’s let Snowflake. One of the better parts of using a notebook is that we can run individual cells and see what the results are. Let’s run our import library cell.

If you haven’t already, go ahead and start the session by clicking in the top right corner of the screen where it says “Start”:

![Start button](../../../../_images/start-button.png)

If you run the topmost cell in the notebook, and you will likely discover that matplotlib is not loaded into the session:

![ModuleNotFoundError message](../../../../_images/modulenotfounderror-message.png)

This is a pretty important one for this notebook. You can add that library to your notebook/session by using the “Packages” option in the top right of the notebook:

![Search in Packages dialog box](../../../../_images/search-in-packages-dialog-box.png)

Search for **matplotlib**, and select it. This will make this package available in the session.

![matplotlib selected for installation](../../../../_images/matplotlib-selected-for-installation.png)

Once you load this library, you will have to restart the session. Once you have restarted the session, run that first cell again. You will likely be told that it was a success this time.

![Libraries imported](../../../../_images/libraries-imported.png)

With the packages loaded, the session fixed, and the rest of the issues in the code already resolved, what can we do to check the rest of the notebook? Run it! You can run all the cells in the notebook by selecting “Run all” in the top right corner of the screen, and see if we get any errors.

It looks like there was a successful run:

![Successful run of first cell](../../../../_images/successful-run-of-first-cell.png)

If you compare the two notebooks execution, it looks like the only difference is that the Snowflake version put all of the output datasets first followed by the images, whereas they are intermixed in the Spark Jupyter Notebook:

![Datasets intermixed](../../../../_images/datasets-intermixed.png)

Note that this difference is not an API difference, but rather a difference in how notebooks in Snowflake orchestrate this. This is likely a difference AdventureWorks is willing to accept!

## Conclusions[¶](#conclusions "Link to this heading")

By utilizing the SMA, we were able to accelerate the migration of both a data pipeline and a reporting notebook. The more of each that you have, the more value a tool like the SMA can provide.

And let’s go back to the assessment -> conversion -> validation flow that we have consistently come back to. In this migration, we:

* Setup out project in the SMA
* Ran SMA’s assessment and conversion engine on the code files
* Reviewed the output reporting from the SMA to better understand what we have
* Review what could not be converted by the SMA in VS Code
* Resolve issues and errors
* Resolve session references
* Resolve input/output references
* Run the code locally
* And run the code in Snowflake
* Ran the newly migrated scripts and validated their success

Snowflake has spent a great deal of time improving its ingestion and data engineering capabilities, just as it has spent time improving migration tools like SnowConvert, the SnowConvert Migration Assistant, and the Snowpark Migration Accelerator. Each of these will continue to improve. Please feel free to reach out if you have any suggestions for migration tooling. These teams are always looking for additional feedback to improve the tools.

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

1. [Resolve All Issues](#resolve-all-issues)
2. [Resolve the Session Calls](#resolve-the-session-calls)
3. [Resolving the Inputs/Outputs](#resolving-the-inputs-outputs)
4. [Clean Up and Test](#clean-up-and-test)
5. [Running the Notebook in Snowsight](#running-the-notebook-in-snowsight)
6. [Conclusions](#conclusions)