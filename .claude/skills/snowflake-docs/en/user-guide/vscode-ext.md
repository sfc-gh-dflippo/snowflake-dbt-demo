---
auto_generated: true
description: The Snowflake Visual Studio Code (VS Code) extension enables you to write
  and execute Snowflake SQL statements directly in VS Code. The extension also integrates
  with Snowpark Python to provide debugg
last_scraped: '2026-01-14T16:56:02.170407+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/vscode-ext
title: Snowflake Extension for Visual Studio Code | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)

   * User interface
   * [Snowsight](ui-snowsight.md)
   * Command-line clients
   * [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
   * [SnowSQL](snowsql.md)
   * Extensions for code editors
   * [Visual Studio Code SQL extension](vscode-ext.md)
   * Infrastructure as code
   * [Snowflake Terraform provider](terraform.md)
   * Drivers and libraries
   * [API reference](../api-reference.md)
   * Downloads and configuration
   * [Download clients, drivers, and libraries](snowflake-client-repository.md)
   * [Configure clients, drivers, libraries, and applications to connect to Snowflake](gen-conn-config.md)
   * [Troubleshoot Snowflake client connectivity](client-connectivity-troubleshooting/overview.md)
   * Additional information about clients

     * [View the client version used in a query](snowflake-client-version-check.md)
     * [Limits on query text size](query-size-limits.md)
     * [SQL statements supported for preparation](sql-prepare.md)
   * Third-party software
   * [Ecosystem](ecosystem.md)
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
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)Visual Studio Code SQL extension

# Snowflake Extension for Visual Studio Code[¶](#sf-vscext "Link to this heading")

The Snowflake [Visual Studio Code](https://code.visualstudio.com/) (VS Code) extension enables you to write and execute Snowflake SQL statements directly in VS Code. The extension also integrates with [Snowpark Python](../developer-guide/snowpark/python/index) to provide debugging, syntax highlighting, and autocomplete features for SQL in Python code.

You can either install the VS Code extension from the Visual Studio marketplace or download and install the `.vsix` file.

## Install the VS Code extension from Visual Studio Marketplace[¶](#install-the-vs-code-extension-from-visual-studio-marketplace "Link to this heading")

1. In VS Code, select Code > Settings > Extensions.
2. In the Search Extensions in Marketplace field, enter **Snowflake**, and then select the **Snowflake** extension.

   To confirm you’ve selected the correct extension, look for the Snowflake badge as shown in the following image:

   [![The Snowflake certification location. Snowflake certification is a check mark within a blue circle.](../_images/vsc-snowflake-certified.png)](../_images/vsc-snowflake-certified.png)
3. Select Install.

## Install the VS Code extension from a .vsix file[¶](#install-the-vs-code-extension-from-a-vsix-file "Link to this heading")

1. Download the extension:

   * Go to <https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc>.
   * Select the Version History tab.
   * Select Download for the VS Code extension version you want to install. Note where the file is downloaded.
2. In VS Code, select Code > Settings > Extensions.
3. Select More (…) > Install from VSIX.
4. Browse to the location of the `snowflake-x.y.z.vsix` file on your computer, select the file, and then select Install.

   After the installation completes, the Snowflake Extension for Visual Studio Code appears in the INSTALLED section of the Extensions menu in VS Code.

## Sign in to Snowflake with the VS Code extension[¶](#sign-in-to-snowflake-with-the-vs-code-extension "Link to this heading")

Before you can execute SQL statements, use Snowpark Python, or use Snowflake Native App Framework features, you must sign in to a Snowflake account.

Methods for signing in to Snowflake with the VS Code extension:

* Use your Snowflake account identifier, username, and password.
* Use federated authentication such as Security Assertion Markup Language (SAML) or Single sign-on (SSO).
* Use key-pair authentication.
* Use OAuth authentication in your `connections.toml` configuration file. See [Edit the Snowflake connections.toml file](#label-edit-toml).

The first time you use the VS Code extension to sign in to Snowflake, you need to enter either the account identifier for your Snowflake account or the URL that you use to connect to Snowflake. To determine your account identifier, see [Account identifiers](admin-account-identifier).

1. Select the Snowflake icon in the VS Code Activity Bar.
2. In the Account Identifier/URL field, enter the account identifier for your Snowflake account or the URL that you use to connect to Snowflake, and then select Continue.

   The Account Identifier/URL field isn’t available if you’ve previously provided your Snowflake account credentials.
3. Select one of the following options in the Auth Method list:

   * Select Single sign-on to use your SSO credentials to sign in to Snowflake.
   * Select Username/password to use your Snowflake username and password to sign in to Snowflake.
   * Select Key Pair to use your Snowflake username and password to sign in to Snowflake. For more information about key-pair authentication, see [Key-pair authentication and key-pair rotation](key-pair-auth).
4. Enter your credentials and then select Sign in.

   When you select SSO, a separate authentication page opens after you enter your username and select Sign in with single sign-on. Enter your SSO credentials and then return to VS Code to complete the Snowflake sign in.

   After you successfully sign in, the sidebar displays your account information, your default role, the OBJECT EXPLORER with a **Databases** list, and your QUERY HISTORY.

## Edit the Snowflake `connections.toml` file[¶](#edit-the-snowflake-connections-toml-file "Link to this heading")

You can add and modify connection definitions in the Snowflake `connections.toml` configuration file. A connection definition is a collection of connection-related parameters.

To connect to Snowflake with a TOML file, see [Connecting using the connections.toml file](../developer-guide/python-connector/python-connector-connect.html#label-python-connection-toml). To learn more about managing connections with a TOML file, see [Managing Snowflake connections](../developer-guide/snowflake-cli/connecting/configure-connections).

1. In VS Code, open the Snowflake VS Code extension and sign in to Snowflake.
2. In the ACCOUNT pane, select Snowflake:Edit Connections File .

   [![The Snowflake:Edit Connections File location.](../_images/vsc-edit-connections-file.png)](../_images/vsc-edit-connections-file.png)
3. Edit the TOML file.
4. Select Save, and then close the TOML file.

## The VS Code extension interface[¶](#the-vs-code-extension-interface "Link to this heading")

[![An overview of the Snowflake VS Code extension showing its main areas: the sidebar pane, the SQL pane, and the query results pane.](../_images/vsc-interface-03.png)](../_images/vsc-interface-03.png)

The following table provides descriptions of the VS Code extension interface functional areas.

| Item | Description |
| --- | --- |
| 1 | The sidebar pane contains the *Account*, *Native App*, *Object Explorer*, and *Query History* panes. Use this pane to specify account details, examine database objects, and examine query results. |
| 2 | Use the Snowflake Native App pane to create and manage a Snowflake Native App. |
| 3 | The Query History pane shows recent queries. |
| 4 | The current session information, including the current role, database, schema, and active warehouse. |
| 5 | Snowflake SQL pane. Displays Snowflake SQL files. |
| 6 | The Query Results pane shows query results. Select a query to display its execution result. |

## Use the VS Code extension with SnowSQL configuration files[¶](#use-the-vs-code-extension-with-snowsql-configuration-files "Link to this heading")

The Snowflake Extension for Visual Studio Code can use [Snow SQL configuration files](snowsql-config.html#label-configuring-snowsql)
for loading connection configurations.

Note

Only connection configuration values are used. Other SnowSQL configuration values are ignored.

1. In the VS Code search field, enter `>user settings` and then select Preferences: Open User Settings.
2. On the User tab, expand Extensions.
3. Scroll down and select Snowflake.
4. In the right pane, scroll down to Snowsql Config Path.
5. Enter a path to a valid SnowSQL configuration file.

   All connections defined in the configuration display in the **Account** pane.

## Work with SQL files[¶](#work-with-sql-files "Link to this heading")

You can use the Snowflake Extension for Visual Studio Code to create and load SQL files.
SQL files are text files that contain one or more SQL statements.

### Open or create SQL files[¶](#open-or-create-sql-files "Link to this heading")

1. In VS Code, select File > Open, browse to the location of a SQL file, and then open it.

   To create a new SQL file, select File > New File and
   create a file of type Snowflake SQL File.
2. Add one or more Snowflake SQL statements to the file.
3. Optional. Select Snowflake: Execute All Statements ([![Execute all statements button](../_images/vsc-execute-all.png)](../_images/vsc-execute-all.png)) to execute a command.

### Execute commands or queries[¶](#execute-commands-or-queries "Link to this heading")

Important

To display Snowflake query results, the VS Code extension automatically runs `DESC RESULT '<query_id>'` in the background after every query. This process makes `LAST_QUERY_ID()` inaccurate. For more information about the DESCRIBE RESULT command and its parameters, see [DESCRIBE RESULT](../sql-reference/sql/desc-result).

In VS Code, select one of the following options:

* To execute all SQL statements in a file, select Snowflake: Execute All Statements ([![Execute all statements button](../_images/vsc-execute-all.png)](../_images/vsc-execute-all.png)).
* To execute a specific command, place your cursor on the statement you want to run and then select Execute.
* To execute multiple commands, select the statements you want to run and then select Execute. The commands execute in order from top to bottom.

To use keyboard shortcuts to execute statements, select the SQL statements you want to run, press [![Apple OSX Command key.](../_images/osx-command-key.png)](../_images/osx-command-key.png) + [enter] on a Mac keyboard, or [![Generic control key.](../_images/control-key.png)](../_images/control-key.png) + [enter] on a Windows keyboard.

Executed SQL statement results display in the SNOWFLAKE pane.

To cancel in-progress queries, select a query in QUERY HISTORY list and select Cancel query ([![Cancel query button](../_images/vsc-cancel-query.png)](../_images/vsc-cancel-query.png)).

### View query history[¶](#view-query-history "Link to this heading")

1. In VS Code, expand Query History.
2. Select a statement.
3. Review the results in the SNOWFLAKE pane.
4. Optional. Select one of the following:

   * Select Snowflake: Copy to Clipboard ([![Copy query text to clipboard button](../_images/vsc-query-history-copy.png)](../_images/vsc-query-history-copy.png)) to copy the query text to the clipboard.
   * Select Snowflake: Remove Query ([![Delete query button](../_images/vsc-query-history-delete.png)](../_images/vsc-query-history-delete.png)) to delete a query.

### Work with query results[¶](#work-with-query-results "Link to this heading")

You can sort, reorder, hide, freeze, or save query results to disk.

1. In QUERY HISTORY, select a query.
2. In the SNOWFLAKE pane, choose a column.
3. Select the expander arrow (↓) and then one of: Sort Ascending, Sort Descending,
   Hide column “column name”, or Freeze columns up to “column name”.

   If a column was previously hidden, choose any other column and select Unhide N columns.
4. Optional. Select one of the following:

   * Select Cloud ([![Download results button](../_images/vsc-download.png)](../_images/vsc-download.png)) to save the results as a compressed gzip file.
   * Select Save ([![Save results button](../_images/vsc-save.png)](../_images/vsc-save.png)) to save the results as a comma-separated (CSV) file.

## Work with Snowpark Python code[¶](#work-with-snowpark-python-code "Link to this heading")

You can use the Snowflake Extension for Visual Studio Code to create, load, and execute SQL files.

### Debug Snowpark Python functions[¶](#debug-snowpark-python-functions "Link to this heading")

1. Write a Snowflake stored procedure in a Python function where the first parameter is a Snowpark `Session` object.
2. An inline Snowflake: Debug option appears above the function name. Choose this option to run the stored procedure in
   the function, using your current active session through the extension. You can also set debug breakpoints.

### Detect SQL statements automatically[¶](#detect-sql-statements-automatically "Link to this heading")

To set up automatic SQL syntax highlighting, enable the [extension setting](#label-vscode-ext-settings-preview)
Auto Detect Sql in Python. The extension automatically detects SQL statements by looking for a SQL keyword in all capital letters as
the first word in a Python string, as shown in the following image.

![A code snippet of a Snowflake SQL statement in a Python string showing automatic SQL syntax highlighting.](../_images/vsc-snowpark-syntax-highlight-autodetect.png)

### Denote SQL statements manually[¶](#denote-sql-statements-manually "Link to this heading")

1. Optional. Disable the [extension setting](#label-vscode-ext-settings-preview) Auto Detect Sql in Python.
2. Use comments to denote the start and end of a SQL statement. You can use any combination of the following markers:

   * Start markers: `-–startsql`, `-–beginsql`, `-–start-sql`, `-–begin-sql`
   * End markers: `–-endsql`, `–-end-sql`

   The following image shows how the `--begin-sql` and `--end-sql` markers manually denote a SQL statement.

![A code snippet of a Snowflake SQL statement in a Python string using comments to manually enable SQL syntax highlighting.](../_images/vsc-snowpark-syntax-highlight-manual.png)

### Use SQL autocomplete in Python strings[¶](#use-sql-autocomplete-in-python-strings "Link to this heading")

1. In a Python file, create a Python string while connected to an active Snowflake session with the VS Code extension.
2. Write a SQL statement. The autocomplete suggestions appear.

   For example, when you start writing a statement such as `SELECT * FROM db1.public`, the extension automatically suggests table names.

   Similarly, when you start filling out columns inside a SELECT statement that references a table, the extension automatically suggests column
   names, as shown in the following image.

![A code snippet of a Snowflake SQL statement in a Python string showing autocomplete suggestions for column names.](../_images/vsc-snowpark-autocomplete.png)

### Jinja template syntax highlighting[¶](#jinja-template-syntax-highlighting "Link to this heading")

By default, the VS Code extension adds basic syntax highlighting and bracket autocomplete for writing
[Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/) in Snowflake SQL, as shown in the following image.

![A code snippet of a Snowflake SQL statement with a Jinja template showing syntax highlighting and bracket autocomplete.](../_images/vsc-snowpark-syntax-highlight-jinja.png)

## Work with the Snowflake Native App Framework[¶](#work-with-the-naf "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

Available to all accounts. To use the Snowpark Python features of the VS Code extension, you must enable the extension setting
Enable Public Preview Features. For more information, see [VS Code extension preview settings](#label-vscode-ext-settings-preview).

You can use the VS Code extension to create and manage a Snowflake Native App. For more information about the Snowflake Native App Framework, see [About the Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about).

Note

To make sure you have the latest VS Code extension Snowflake Native App functionality, Snowflake recommends upgrading to the most recent version of the Snowflake CLI. See [Installing Snowflake CLI](../developer-guide/snowflake-cli/installation/installation).

Snowflake CLI versions 2.2.X and 3.X.X are supported.

### View the VS Code extension Snowflake Native App command palette[¶](#view-the-vs-code-extension-native-app-command-palette "Link to this heading")

The VS Code extension Snowflake Native App command palette provides access to the following Snowflake Native App commands:

* Create Native App
* Deploy a Native App
* Focus on a Native App View
* Open a Native App
* Run (deploy and re-install) a Native App
* Teardown a Native App

To access these commands, type `>Snowflake Native` in the search field at the top of the VS Code window.

### Create a Snowflake Native App[¶](#create-a-native-app "Link to this heading")

1. In VS Code, open the Snowflake VS Code extension and sign in to Snowflake.
2. Expand the NATIVE APP pane and then select Create new from template.
3. Select one of the following:

   * Enter the folder name where you want to create the Snowflake Native App and then press Enter.
   * Press Enter to accept the default directory as the location for the Snowflake Native App.
4. Select one of the following:

   * Enter the URL for the GitHub repository where your Snowflake Native App templates are stored, and then select Enter.
   * Enter the path to a local templates folder.
   * To accept the default GitHub Snowflake Native App template repository URL, select Enter.
5. Select one of the following templates:

   * Select basic to create a Snowflake Native App with minimal code examples and guidance.
   * Select streamlit-python to create a Snowflake Native App with Python extension code and Streamlit code examples.
   * Select streamlit-java to create a Snowflake Native App with Java extension code and Streamlit code examples.
   * Select spcs-basic to create a Snowflake Native App with SPCS extension code and Streamlit code examples.

### Deploy and open a Snowflake Native App[¶](#deploy-and-open-a-native-app "Link to this heading")

When you use the Run (deploy and re-install) or Deploy options, the application selected in the NATIVE APP pane is used. When multiple Snowflake Native App applications are available, a prompt appears, and you can select which `snowflake.yml` file to use for the deployment.

After you deploy your Snowflake Native App, you can open it in Snowflake to manage access, view, add, and validate app packages, view logs and events, and modify privileges.

1. Select one of the following:

   * In the VS Code extension NATIVE APP pane, select Run (deploy and re-install). This is the recommended option when you have made significant changes and an application object is required.
   * In the VS Code extension NATIVE APP pane, select Deploy. This is the recommended option when you are deploying application packages and stage files and an application object is not required.
2. Optional. Select the OUTPUT tab in the query results pane to view deployment progress.
3. In the NATIVE APP pane, select Open.

### View Snowflake Native App application object status[¶](#view-native-app-application-object-status "Link to this heading")

Note

Snowflake Native App application object status is not available in Snowflake CLI version 3.0.0.

* In the VS Code extension NATIVE APP pane, expand your application.

  A blue font and a blue circle indicate that the application object has not been installed or deployed.

### View the Snowflake Environment Variables Manager[¶](#view-the-snowflake-environment-variables-manager "Link to this heading")

Use the Snowflake Environment Variables Manager to create and manage environment variables in environment variable profiles. You can use an environment variable profile to customize object behavior in Snowflake Native App project definition files. For example, you can create environment variable profiles that change object behavior in development, stage, and production environments. For more information about environment variables and Snowflake connections, see [Project definition files](../developer-guide/snowflake-cli/native-apps/project-definitions).

Use one of the following methods to view the Snowflake Environment Variables Manager:

* In the VS Code extension NATIVE APP pane, select Environment Variables.
* In the command palette, select `Open Environment Variables Manager`.

### Add an environment variable to an environment variable profile[¶](#add-an-environment-variable-to-an-environment-variable-profile "Link to this heading")

An environment variable profile stores environment variables.

1. In the VS Code extension NATIVE APP pane, select Environment Variables.
2. In the Selected Profile list, select a profile.
3. In the Environment Variable column, enter an environment variable.
4. In the Value column, enter a value for the environment variable.
5. Optional: To add additional environment variables to the environment variable profile, repeat steps 3 and 4.
6. Optional: To add additional rows to the environment variable profile, select + (Add Row).

### Add an environment variable profile[¶](#add-an-environment-variable-profile "Link to this heading")

An environment variable profile stores environment variables. To customize object behavior in Snowflake Native App project definition files, create a new profile.

1. In the VS Code extension NATIVE APP pane, select Environment Variables.
2. Select Add Profile.
3. Enter a name for the profile, and then press Enter.

### Add a row to an environment variable profile[¶](#add-a-row-to-an-environment-variable-profile "Link to this heading")

> To add an environment variable, add a row to the environment variable profile.

1. In the VS Code extension NATIVE APP pane, select Environment Variables.
2. Select a profile in the Selected Profile list.
3. Select + (Add Row).

### Rename an environment variable profile[¶](#rename-an-environment-variable-profile "Link to this heading")

1. In the VS Code extension NATIVE APP pane, select Environment Variables.
2. Select a profile in the Selected Profile list.
3. Select Rename Profile.
4. Enter a name for the profile, and then press Enter.

### Delete an environment variable profile[¶](#delete-an-environment-variable-profile "Link to this heading")

1. In the VS Code extension NATIVE APP pane, select Environment Variables.
2. Select a profile in the Selected Profile list.
3. Select Delete Profile.

### Enable Snowflake Native App debug mode[¶](#enable-native-app-debug-mode "Link to this heading")

Use debug mode to view application objects that are not visible to consumers, such as shared content objects or objects not granted to a specific database role. For more information about debug mode and turning it on programmatically, see [About debug mode](../developer-guide/native-apps/installing-testing-application.html#label-native-apps-testing-debug-mode).

* In the VS Code extension NATIVE APP pane, select App Debug Mode: OFF.

### Drop Snowflake Native App packages and application objects[¶](#drop-native-app-packages-and-application-objects "Link to this heading")

Use the Teardown option to drop the application object and package defined in the resolved project definition.

* In the VS Code extension NATIVE APP pane, select Teardown. A confirmation message appears when teardown is complete.

## Change session context[¶](#change-session-context "Link to this heading")

You can use the Account section of the Side Bar pane to select roles, databases, schemas, and warehouses.
Use the associated dropdown to select each as appropriate.

Use the account drop down to sign in to, or switch between different accounts.

> [![Sign in to, or switch between accounts.](../_images/vsc-account-02.png)](../_images/vsc-account-02.png)

## Navigate with the Object Explorer[¶](#navigate-with-the-object-explorer "Link to this heading")

Use the OBJECT EXPLORER section of the Side Bar pane to examine and display characteristics of database objects.

1. Sign in to an account.
2. Expand OBJECT EXPLORER.
3. Expand the databases list.
4. Expand a database.
5. Expand a schema.
6. Navigate to a child component.
7. Select any element to view its characteristics in the SNOWFLAKE Query Results pane.
8. Optional. Select one of the following:

   * Select Open data preview ([![View object details button](../_images/vsc-view-object-details.png)](../_images/vsc-view-object-details.png)) to display a preview of up to 100 rows of content associated with a table, view, materialized view, or similar object.
   * Select Show SQL ([![View object DDL button](../_images/vsc-view-object-ddl.png)](../_images/vsc-view-object-ddl.png)) to display the SQL code associated with the object.

## Manage stage content[¶](#manage-stage-content "Link to this heading")

The Snowflake Extension for Visual Studio Code supports managing stage content directly in the Object Explorer.

### List all the files in a stage[¶](#list-all-the-files-in-a-stage "Link to this heading")

1. In the VS Code OBJECT EXPLORER, navigate to a stage.
2. Expand the stage to see all staged files.

### Upload files from the local file system to a stage[¶](#upload-files-from-the-local-file-system-to-a-stage "Link to this heading")

The Snowflake Extension for Visual Studio Code only supports uploads for internal stages, all other operations work for both internal and external stages.

1. In the VS Code OBJECT EXPLORER, navigate to a stage and select Upload ([![Upload file button](../_images/vsc-upload.png)](../_images/vsc-upload.png)).
2. Enter optional parameters for the upload operation. See [PUT](../sql-reference/sql/put) for a list of optional parameters.
3. Navigate to the folder containing upload files, and then select and upload one or more files.

### Download files from a stage to a local file system[¶](#download-files-from-a-stage-to-a-local-file-system "Link to this heading")

1. In the VS Code OBJECT EXPLORER, navigate to a stage.
2. Select Download ([![Download results button](../_images/vsc-download.png)](../_images/vsc-download.png)) to download all files, or expand the stage.
3. Select and download a file.
4. Select a directory to complete the download.

### Remove files from a stage[¶](#remove-files-from-a-stage "Link to this heading")

See also [REMOVE](../sql-reference/sql/remove).

1. In the VS Code OBJECT EXPLORER, navigate to a stage.
2. Select a file.
3. Select Remove ([![Remove button](../_images/vsc-trash.png)](../_images/vsc-trash.png)).

## VS Code extension settings[¶](#vs-code-extension-settings "Link to this heading")

The following table lists the Snowflake Extension for Visual Studio Code settings.

| Setting | Description | Default |
| --- | --- | --- |
| Autocomplete Object Details | Show details of a Snowflake object after you select its autocomplete entry | Disabled |
| Autocomplete Variant Keys | Show OBJECT/VARIANT key autocomplete suggestions | Disabled |
| Connections Config File | Specifies the location of the `config.toml` file | Unset |
| Enable Frequency Based Completion | Enable frequency-based auto-completion suggestions | Enabled |
| Enable Native App Panel | Enable the Snowflake Native App pane | Disabled |
| Export CSV > Delimiter | Specifies delimiter for columns | Comma |
| Export CSV > Header | Enable inclusion of header row in exported CSV file | Enabled |
| Export CSV > Include Empty Rows | Enable inclusion of empty rows in exported CSV file | Exclude |
| Export CSV > Quotes | Enable double quotes around all values in exported CSV file | Enabled |
| Highlight Query | Enable background highlight on the current SQL statement | Enabled |
| Native App: Activate Snowflake CLI Debugging | Enable debugging mode for Snowflake CLI operations (Snowflake Native App) | Disabled |
| Object Explorer: Search | Enable search in object explorer | Enabled |
| Query History: Item Limit | Specifies the maximum number of queries shown in history. Showing more queries might affect performance. | 1000 |
| Set Client Session Keep Alive | Specifies whether to keep the session active indefinitely when the connection is active, regardless of activity. If this is not enabled, you must sign in again after four hours of inactivity. | Enabled |
| Set HTTP Agent Keep Alive | Enable Node.js driver socket reuse for requests | Enabled |
| Show Execute Above Statement | Enable a selectable execute action above each statement | Enabled |
| Skip Native App Support Message | Hides the support message when a Snowflake Native App project is detected | Disabled |
| Skip YAML Support Message | Hides the YAML extension recommendation message | Disabled |
| Snowsql Config Path | If set, connection configuration will be loaded from this file | Unset |
| Syntax Highlighting: Auto Detect SQL In Python | Enable SQL statement syntax highlighting in Python strings | Enabled |

### VS Code extension preview settings[¶](#vs-code-extension-preview-settings "Link to this heading")

[![Snowflake logo in black (no text)](../_images/logo-snowflake-black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-notes/preview-features) — Open

Available to all accounts.

The following table lists the VS Code extension preview settings.

| Setting | Description | Default |
| --- | --- | --- |
| Enable Public Preview Features | Enable public preview features for the extension | Disabled |

### Change VS Code extension settings[¶](#change-vs-code-extension-settings "Link to this heading")

1. Select one of the following:

   * On Windows/Linux select File > Preferences > Settings.
   * On macOS select Code > Settings > Settings.
2. In the Search settings field, enter *Snowflake*.
3. Select the User or Workspace tabs to view or modify user specific or workspace specific settings.
4. Close the Settings tab.

## Show the VS Code extension changelog[¶](#show-the-vs-code-extension-changelog "Link to this heading")

1. Press `CMD+Shift+P` (Mac), or `CTRL+Shift+P` (Windows).
2. Enter the following command:

   ```
   Show Change Log
   ```

   Copy

## Uninstall the VS Code extension[¶](#uninstall-the-vs-code-extension "Link to this heading")

1. Select Code > Settings > Extensions
2. Select the extension.
3. Right-click and select Disable or Uninstall.

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

1. [Install the VS Code extension from Visual Studio Marketplace](#install-the-vs-code-extension-from-visual-studio-marketplace)
2. [Install the VS Code extension from a .vsix file](#install-the-vs-code-extension-from-a-vsix-file)
3. [Sign in to Snowflake with the VS Code extension](#sign-in-to-snowflake-with-the-vs-code-extension)
4. [Edit the Snowflake connections.toml file](#edit-the-snowflake-connections-toml-file)
5. [The VS Code extension interface](#the-vs-code-extension-interface)
6. [Use the VS Code extension with SnowSQL configuration files](#use-the-vs-code-extension-with-snowsql-configuration-files)
7. [Work with SQL files](#work-with-sql-files)
8. [Work with Snowpark Python code](#work-with-snowpark-python-code)
9. [Work with the Snowflake Native App Framework](#work-with-the-naf)
10. [Change session context](#change-session-context)
11. [Navigate with the Object Explorer](#navigate-with-the-object-explorer)
12. [Manage stage content](#manage-stage-content)
13. [VS Code extension settings](#vs-code-extension-settings)
14. [Show the VS Code extension changelog](#show-the-vs-code-extension-changelog)
15. [Uninstall the VS Code extension](#uninstall-the-vs-code-extension)

Related content

1. [SQL command reference](/user-guide/../sql-reference-commands)