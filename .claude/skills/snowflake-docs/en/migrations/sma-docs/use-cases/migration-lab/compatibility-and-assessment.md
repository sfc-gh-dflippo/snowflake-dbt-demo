---
auto_generated: true
description: As with SnowConvert, we will run code through the SMA, evaluate the result,
  resolve any issues, and run it on the new platform. However, unlike SnowConvert,
  the SMA does NOT connect to any source plat
last_scraped: '2026-01-14T16:52:04.340240+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/use-cases/migration-lab/compatibility-and-assessment
title: 'Snowpark Migration Accelerator: Pipeline Lab - Assessment | Snowflake Documentation'
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Use cases[Migration lab](README.md)Compatibility and assessment

# Snowpark Migration Accelerator: Pipeline Lab - Assessment[¶](#snowpark-migration-accelerator-pipeline-lab-assessment "Link to this heading")

As with SnowConvert, we will run code through the SMA, evaluate the result, resolve any issues, and run it on the new platform. However, unlike SnowConvert, the SMA does NOT connect to any source platform, nor does it connect to Snowflake. It is a local application that can be run completely offline. But its power is in its assessment. Most of the heavy lifting on conversion has been done by building compatibility between the Spark API and the Snowpark API.

## Extraction / Code Availability[¶](#extraction-code-availability "Link to this heading")

The files we will use for the AdventureWorks Lab are here:

[end\_to\_end\_lab\_source\_code.zip](../../../../_downloads/62b8c258bb35353bbc7914de3d0095d2/end_to_end_lab_source_code.zip)

For the purpose of this lab, we will assume that the notebook and script file that we are converting are already accessible as files. In general, the SMA takes in files as an input and does not connect to any source platform. If the files are being orchestrated by a specific tool, you may need to export them. If you are using notebooks as part of databricks or EMR, you can export those as .ipynb files just as the jupyter notebook we are going to run through the SMA today.

This lab only has a few files, but it’s common in a large migration to have hundreds or thousands of files. Extract what you can and run those files through the SMA. The good thing about using a tool like this is that it can tell you what you might be missing.

Note that there is also a data file as well: ‘customer\_update.csv’. This is a sample of the file being generated locally by the Point of Sale (POS) system that Adventure Works is currently using. While that system is also being updated, this Proof of Concept (POC) is focused on making the existing pipeline work with Snowpark instead of Spark.

Let’s take each of these files, and drop them into a single directory on our local machine:

![Source files](../../../../_images/source-files.png)

It would be recommended to create a project directory. This can be called whatever you like, but as a suggestion for this lab, let’s go with **spark\_adw\_lab**. This means we would create a folder with the name spark\_adw\_lab, then create another folder in that directory called source\_files (the path being something like **/your/accessible/directory/spark\_adw\_lab/source\_files**). This isn’t required, but will help keep things organized. The SMA will scan any set of subdirectories as well, so you could add specific pipelines in a folder and notebooks in another.

## Access [¶](#access "Link to this heading")

Now that we have our source files in an accessible directory, it is time to run the SMA.

If you have not already downloaded it, the SMA is accessible from [the Snowflake website](https://www.snowflake.com/en/migrate-to-the-cloud/migration-accelerator/). It is also accessible from the Migrations page in SnowSight in your Snowflake account:

![Access SMA](../../../../_images/access-sma.png)

Once you download the tool, install it! There is more information on [installing the SMA](https://docs.snowconvert.com/sma/general/getting-started/installation) in the SMA documentation.

## Using the Snowpark Migration Accelerator[¶](#using-the-snowpark-migration-accelerator "Link to this heading")

Once you have installed the tool, open it! When you launch the SMA, it will look very similar to its partner tool, SnowConvert. Both of these tools are built on a similar concept where you input code files into the tool and it runs. As a reminder, we have seen that SnowConvert can take the DDL and data directly from the source and input it directly into Snowflake. The SMA does not do this. It only takes in code files as a source and outputs those files to something that is compatible with Snowflake. This is primarily because the tool does not know how a user will orchestrate their spark code, but also to make it more secure to use.

Once you have launched the tool, It will ask you if you would like to create a new project or open an already existing one:

![New project](../../../../_images/new-project.png)

This will take you to the project creation screen:

![Project creation](../../../../_images/project-creation.png)

On this screen, you will enter the relevant details for your project. Note that all fields are required. For this project, you could enter something similar to:

* Project Name: **Spark ADW Lab**
* Input Folder Path: **/your/accessible/directory/spark\_adw\_lab/source\_files**
* Output Folder Path (the SMA will auto generate a directory for the output, but you can modify this): **/your/accessible/directory/spark\_adw\_lab/source\_files\_output**
* Email Address: **your.name@your\_domain.com**
* Customer’s Company: **Your Organization**

A couple of notes about this project creation screen:

* The email and company fields are to help you track projects that may be ongoing. For example, at any large SI, there may be multiple email addresses and multiple organizations on behalf of whom a single user may run the SMA. This information is stored in the project file created by the SMA.
* There is a hidden field for SQL. Note that the SMA can scan/analyze SQL, but it does not convert any SQL.It also can only identify SQL in the following circumstances:

  + SQL that is in .sql files
  + SQL that is in SQL cells in a Jupyter Notebook
  + SQL that is passed as a single string to a spark.sql statement.
* While this SQL capability can be helpful to determine where there is incompatible SQL with Snowflake, it is not the primary use for the SMA. More support for Spark SQL and HiveQL are coming soon.

Once you’ve entered all of your project information, for this HoL, we are going to **skip** the assessment phase. (What… aren’t we building an assessment?) If you do not want to convert any code, running an assessment can be helpful as it will allow you to get the full set of reports generated by the SMA. You can then navigate through those or share them with others in your organization while not creating extra copies of the converted code. However, all of these same assessment reports are also generated during a conversion. So we will skip assessment mode for now and go to conversion.

Select “SAVE & SKIP ASSESSMENT” in the bottom right corner of the application.

![Skip assessment](../../../../_images/skip-assessment.png)

Note that what you are “saving” is a local project file. All of the information that you entered on the project creation screen will be saved to this local text file with the extension ‘.snowma’ in the directory you just specified above.

![Save local project file](../../../../_images/save-local-project-file.png)

This will take you to the conversion screen. On this screen you will again see the input and output directory fields, but those will have already been populated by what you have entered in the project creation page. The only new field here will be to enter an access code. Access codes are freely available, but they do expire. So even if you have already requested an access code to use the Snowpark Migration Accelerator (SMA), you may need to request one again. (And while the mechanism for generating these access codes is similar to SnowConvert, the access codes for SnowConvert will not work with the SMA. You will have to request and use a different one.)

You can request an access code by selecting “Inquire about an access code” out to the side of the “Enter access code…” field:

![Inquire about access code](../../../../_images/inquire-about-access-code.png)

When you select this, a pop up menu will appear asking you who you are so an access code can be generated:

![Identity pop up](../../../../_images/identity-pop-up.png)

Fill out all of the fields shown above, and ensure that you enter a valid email address. In the project creation screen earlier, you entered an email address to associate with the project you were creating. However, nothing was actually sent to that email. That was only to track your project locally. This form will trigger an access code to be sent to the email you enter.

Once you submit the form, you should receive an email with an access code shortly. The email will come from [sma-notifications@snowflakel.com](mailto:sma-notifications%40snowflakel.com), and it will look something like this:

![Access code email](../../../../_images/access-code-email.png)

In the image above, where it says **<your access code here>,** you should see a series of numbers, letters, and dashes. Copy that string, and paste it in the access code field for the SMA:

![Paste access code](../../../../_images/paste-access-code.png)

When you paste the value into the box, the SMA will validate the access code. A successful validation will show the access code details below the access code dialog box:

![Validate access code](../../../../_images/validate-access-code.png)

To validate the access code, the SMA will call out to the Snowflake licensing API. If you are not connected to the internet, the tool will not be able to validate the access code and you will get an error message. If you need to run the tool in a completely offline environment, please reach out to [sma-support@snowflake.com](mailto:sma-support%40snowflake.com) for help validating an access code.

Now that the access code has been validated, you can take a look at the conversion settings:

![View conversion settings](../../../../_images/view-conversion-settings.png)

There is one setting that will simplify the output of this hands on lab, which would be to disable the attempted conversion of pandas dataframes to the Snowpark API:

![Simplify output](../../../../_images/simplify-output.png)

This one setting is currently being updated, so there will be a lot of additional warnings added if this option is not deselected. Most of the pandas dataframe can be used as part of the modin implementation of pandas, so a simple import call change should suffice for now. Look for an issue on this issue by the end of June 2025. You can look at the other settings, but we will leave them as is. It’s important to note that there is a testing library that the output code is compatible with called Snowpark Checkpoints. There are settings related to this, but we will not alter them in this lab.

Select “CLOSE” to save and close your settings.

![Close conversion settings](../../../../_images/close-conversion-settings.png)

The “START CONVERSION” option will be available in the bottom right corner of the application. Let’s start the conversion by selecting this option.

The next screen will show the progress of the conversion:

![Conversion progress](../../../../_images/conversion-progress.png)

Like SnowConvert, the SMA is building a semantic model of the entire codebase in the input directory. It is building relationships between code elements, sql objects, and other referenced artifacts, and creating the closest output it can to a functional equivalent for Snowflake. This primarily means converting references from the Spark API to the Snowpark API. The SMA’s engineering team is a part of the Snowpark engineering team, so most transformations that take place have been built into the Snowpark API, so the changes may seem minor. But the wealth of assessment information that is generated by the SMA allows a migration project to really get moving forward. An in-depth look at all of the generated assessment information will have to take place elsewhere because the SMA has likely finished this conversion in the time it took to read this paragraph.

When the SMA has finished, the “VIEW RESULTS” option will be available in the bottom right corner:

![View results](../../../../_images/view-results.png)

The results page will show the… results.

![Conversion results page](../../../../_images/conversion-results-page.png)

The results page has some “Readiness Scores” that are very simplified metrics on how “ready” this codebase is for Snowflake. We will review the results next, but note that running the Snowpark Migration Accelerator is the easy part. Note that this is just an “accelerator”. It is not a silver bullet or a hands-off automation tool. Pipelines that connect to one data source and output to another are not fully migrated by this tool will always need more attention than a straight SQL-to-SQL migration of DDL as is done by SnowConvert. But Snowflake is continuously working towards making this as simple as possible.

## Interpreting the Output[¶](#interpreting-the-output "Link to this heading")

The SMA, even more so than SnowConvert, generates a large amount of assessment information. It can be difficult to parse through the results. There are many different directions you could go depending on what you want to achieve.

Note that this is an extremely simple scenario, so some of the steps we are going to take will look like overkill. (I mean, do we really need to analyze the dependencies present in this project when there are only two files and we could just… look?) The goal is to still walk through what we normally recommend even in this small POC. But let’s be clear… that the scope is clear, and there are only two files. We just need both of them to work as they do in the source.

### **Readiness Scores**[¶](#readiness-scores "Link to this heading")

With that in mind, let’s take a look at the first part of the output that you will see in the application: the readiness scores. There will be multiple readiness scores and you can expand on each one of them to better understand what is captured by that readiness score.

![View readiness scores](../../../../_images/view-readiness-scores.png)

Each readiness score is a very basic calculation of the count of functions or elements in an API that are supported in Snowpark/Snowflake divided by the count of all functions or elements related to that API for this execution. The calculation showing you how the score is calculated is shown when you expand the window. You can also learn more about how to interpret the readiness scores by selecting “How to read through the scores” near the top left corner of this window.

This execution has a Spark API Readiness Score of 97.92%. (Please note that yours may be different! These tools are updated on a biweekly basis and there may be a change as compatibility between the two platforms is ever evolving.) This means that 97.92% of the references to the Spark API that the tool identified are supported in Snowflake. “Supported” in this case means that there could be a similar function that already exists or that the SMA has created a functionally equivalent output. The higher this score is, the more likely this code can quickly run in Snowflake.

(Note that this 97.92% of references are either supported directly by the Snowpark API or they are converted by the SMA. Most of them are likely supported directly, but you can find out exactly what was converted and what was passed through by reviewing the **SparkUsageInventory.csv** report in the output Reports folder generated by the SMA. We will not walk through that in this lab as we will see what is NOT supported in the **issues.csv** file, but you can use this information for reference.)

There are other readiness scores and you may see more than what is shown in the lab as the readiness scores do change over time. This lab won’t walk through each of them, but note that a low score will always be worth investigating.

### **Code Analyzed**[¶](#code-analyzed "Link to this heading")

Just below each of the readiness scores, will be a small indicator that lets you know if there was any code that could not be processed:

![Code that could not be processed](../../../../_images/code-that-could-not-be-processed.png)

This number represents the **percentage of files** that were fully parsed. If this number is less than 100%, then there is some code that the SMA could not parse or process. This is the first place you should start looking to resolve problems. If it’s less than 100%, you should see where the parsing errors occurred by looking at the issue summary. This is the first place you should look when working through the SMA’s output because it’s the only one where it might make sense to run the tool again if a large amount of code was not able to be scanned.

In this case, we only have **50%** of our workload successfully parsed. Tragic. Now, this might seem like something we should panic about, but let’s not be too quick to judge. We only have 2 files, and we don’t yet know how many parsing errors we have.

Regardless of the result of this number, the last place we will visit on this page is the Issue Summary. Scroll down in the application until you see this summary:

![Issues summary](../../../../_images/issues-summary.png)

### **Issue Summary**[¶](#issue-summary "Link to this heading")

Issues are one of the key elements of both SnowConvert and the SMA. Each tool is attempting to create a functional equivalent output based on the input that it receives, but no conversion is 100% automated. These tools know this, and mark everything that cannot be converted or even might need extra attention with an issue. These issues are summarized in a spreadsheet, but are also written as comments directly into the output code.

The issue summary in the UI highlights issues that were found in this execution of the tool. These issues are often referred to with the acronym EWI (error, warning, and issue). Similar, but not identical to SnowConvert, the SMA generates three types of issues:

* **Parsing Error** - This type of issue is considered critical and will need you deal with it immediately. Because of the way the SMA works, having code that does not parse, could mean missing information in the reports and missing conversion piece as well.
* **Conversion Error** - This is something the SMA recognizes (or at least thinks that it recognizes), but it cannot convert for one reason or another. These errors usually have very specific issue codes and should be dealt with next.
* **Warning** - These error codes identify code that the SMA did convert or is something that has an equivalent in Snowpark/Snowflake, but there may be issues when you do testing. There may not be 100% functional equivalence.

There is more [information on issue types on the SMA documentation page](../../issue-analysis/issue-code-categorization), but the issue summary for our execution is shown here:

![Highlighted issue codes](../../../../_images/highlighted-issue-codes.png)

In this summary, you can find the code, count, level, and description for the unique issues present. Even if there are a lot of issues present, the fewer unique issues there are, the more likely they can be dealt with programmatically. For more information on each unique issue code, you can click the code in the UI. This will take you to the SMA documentation page for that specific issue.

Looks like we have some conversion errors, warnings, and 1 parsing error. This means there was 1 thing the tool could not read. (Note that if you get a lot of error codes that start with PND, then you may not have deselected that option in the conversion settings. Now worries, if you see those, you can ignore them.)

Regardless of how many issues you have, it is always recommended to explore the detailed issues file if you’re ready to start migrating. This is a csv file that is stored locally on the machine where you ran the SMA. You can find this file by selecting the “VIEW REPORTS” option in the bottom right of the SMA:

![Select view reports](../../../../_images/select-view-reports.png)

This will take you to the local directory that has all of the reports… and as of this writing, there are a lot of reports generated by the SMA:

![Generated reports list](../../../../_images/generated-reports-list.png)

Each of these reports has some valuable information in it depending on how you are using the SMA. For now, we will only look at the issues.csv file, but note there is more information on EVERY report and inventory generated by the SMA [in the SMA documentation](../../user-guide/assessment/output-reports/README).

When you open the issues file, it will look something like this:

![Issues file contents](../../../../_images/issues-file-contents.png)

Note the schema of this report. It tells you the issue code, a description of the issue, the type of issue (category), the file each issue is in, the line number of the file each issue is in, and provides a link to the documentation page for that specific issue. All of this is helpful information when navigating through the issues.

You can pivot this by file to see what type of issue you have by file:

![Issues by type](../../../../_images/issues-by-type.png)

Looks like we only have a few issues, and our parsing error is in the pipeline python script. That’s where we want to start.

Normally, we would take a look at one other report in our Reports directory, the **ArtifactDependencyInventory.csv** file. But this is such a small execution, let’s take a look at what’s actually in these output files now, and see if we can’t get it to run in (or with) Snowflake.

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

1. [Extraction / Code Availability](#extraction-code-availability)
2. [Access](#access)
3. [Using the Snowpark Migration Accelerator](#using-the-snowpark-migration-accelerator)
4. [Interpreting the Output](#interpreting-the-output)