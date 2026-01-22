---
auto_generated: true
description: This topic describes how to use SnowSQL, including starting/stopping
  the client, using commands and variables within the client, and other general usage
  information.
last_scraped: '2026-01-14T16:55:56.931555+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowsql-use.html
title: Using SnowSQL | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)

   * User interface
   * [Snowsight](ui-snowsight.md)
   * Command-line clients
   * [Snowflake CLI](../developer-guide/snowflake-cli/index.md)
   * [SnowSQL](snowsql.md)

     + [Installing](snowsql-install-config.md)
     + [Configuring](snowsql-config.md)
     + [Connecting](snowsql-start.md)
     + [Using](snowsql-use.md)
     + [Migrating to Snowflake CLI](snowsql-migrate.md)
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

[Guides](../guides/README.md)[Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)[SnowSQL](snowsql.md)Using

# Using SnowSQL[¶](#using-snowsql "Link to this heading")

This topic describes how to use SnowSQL, including starting/stopping the client, using commands and variables within the client, and other general usage information.

## Executing commands[¶](#executing-commands "Link to this heading")

In a Snowflake session, you can issue commands to take specific actions. All commands in SnowSQL start with an exclamation point (`!`), followed by the command name.

For example:

> ```
> user#> !help
>
> +------------+-------------------------------------------+-------------+--------------------------------------------------------------------------------------------+
> | Command    | Use                                       | Aliases     | Description                                                                                |
> |------------+-------------------------------------------+-------------+--------------------------------------------------------------------------------------------|
> | !abort     | !abort <query id>                         |             | Abort a query                                                                              |
> | !connect   | !connect <connection_name>                |             | Create a new connection                                                                    |
> | !define    | !define <variable>=<value>                |             | Define a variable as the given value                                                       |
> | !edit      | !edit <query>                             |             | Opens up a text editor. Useful for writing longer queries. Defaults to last query          |
> | !exit      | !exit                                     | !disconnect | Drop the current connection                                                                |
> | !help      | !help                                     | !helps, !h  | Show the client help.                                                                      |
> | !options   | !options                                  | !opts       | Show all options and their values                                                          |
> | !pause     | !pause                                    |             | Pauses running queries.                                                                    |
> | !print     | !print <message>                          |             | Print given text                                                                           |
> | !queries   | !queries help, <filter>=<value>, <filter> |             | Lists queries matching the specified filters. Write <!queries> help for a list of filters. |
> | !quit      | !quit                                     | !q          | Drop all connections and quit SnowSQL                                                      |
> | !rehash    | !rehash                                   |             | Refresh autocompletion                                                                     |
> | !result    | !result <query id>                        |             | See the result of a query                                                                  |
> | !set       | !set <option>=<value>                     |             | Set an option to the given value                                                           |
> | !source    | !source <filename>, <url>                 | !load       | Execute given sql file                                                                     |
> | !spool     | !spool <filename>, off                    |             | Turn on or off writing results to file                                                     |
> | !system    | !system <system command>                  |             | Run a system command in the shell                                                          |
> | !variables | !variables                                | !vars       | Show all variables and their values                                                        |
> +------------+-------------------------------------------+-------------+--------------------------------------------------------------------------------------------+
> ```
>
> Copy

For a detailed description of each command, see [Commands reference](#label-snowsql-commands) (in this topic).

## Using variables[¶](#using-variables "Link to this heading")

You can use variables to store and reuse values in a Snowflake session. Variables enable you to use user-defined and database values in queries.

The next sections explain how to define and use variables:

* [Defining variables](#label-snowsql-defining-variables)
* [Enabling variable substitution](#label-snowsql-enabling-variable-substitution)
* [Substituting variables in a session](#variable-substitution)
* [Listing variables](#label-snowsql-listing-variables)
* [Using the built-in variables](#label-snowsql-builtin-variables)

### Defining variables[¶](#defining-variables "Link to this heading")

You can define variables for SnowSQL in several ways:

* [Defining variables before connecting (configuration file)](#label-snowsql-defining-variables-config)
* [Defining variables while connecting (-D or --variable command-line flag)](#label-snowsql-defining-variables-connect)
* [Defining variables within a session (!define command)](#label-snowsql-defining-variables-session)

#### Defining variables before connecting (configuration file)[¶](#defining-variables-before-connecting-configuration-file "Link to this heading")

To define variables before connecting to Snowflake, add the variables in the `config` configuration file:

1. Open the [SnowSQL configuration file](snowsql-config) (named `config`) in a text editor. The default
   location of the file is:

   Linux/macOS:
   :   `~/.snowsql/`

   Windows:
   :   `%USERPROFILE%\.snowsql\`

   Note

   You can change the default location by specifying the `--config path` command-line flag when starting SnowSQL.

1. In the `[variables]` section, define any variables that you plan to use:

   > ```
   > [variables]
   > <variable_name>=<variable_value>
   > ```
   >
   > Copy
   >
   > Where:
   >
   > * `variable_name` is a string of alphanumeric characters (case-insensitive) representing the name of the variable.
   > * `variable_value` is a string representing the value for the variable. If needed, the string can be enclosed by
   >   single or double quotes.

   For example:

   > ```
   > [variables]
   > tablename=CENUSTRACKONE
   > ```
   >
   > Copy

#### Defining variables while connecting (`-D` or `--variable` command-line flag)[¶](#defining-variables-while-connecting-d-or-variable-command-line-flag "Link to this heading")

To define variables while connecting to Snowflake, on the terminal command line, specify the `-D` or `--variable`
command-line flag. For the argument to this flag, specify the variable name and value in the form of
`variable_name=variable_value`.

For example:

Linux/macOS:
:   ```
    $ snowsql ... -D tablename=CENUSTRACKONE --variable db_key=$DB_KEY
    ```

    Copy

Windows:
:   ```
    $ snowsql ... -D tablename=CENUSTRACKONE --variable db_key=%DB_KEY%
    ```

    Copy

In the above example:

* `-D` sets a variable named `tablename` to `CENUSTRACKONE`.
* `--variable` assigns a Snowflake variable named `db_key` to the `DB_KEY` environment variable.

#### Defining variables within a session (`!define` command)[¶](#defining-variables-within-a-session-define-command "Link to this heading")

To define a variable after connecting to Snowflake, execute the `!define` command in the session.

For example:

> ```
> user#> !define tablename=CENUSTRACKONE
> ```
>
> Copy

### Enabling variable substitution[¶](#enabling-variable-substitution "Link to this heading")

To enable SnowSQL to substitute values for the variables, you must set the `variable_substitution` configuration option to
`true` in one of the following ways:

* To set this option before you start SnowSQL, open the [SnowSQL configuration file](snowsql-config) in a text
  editor, and set this option in the `[options]` section:

  ```
  [options]
  variable_substitution = True
  ```

  Copy
* To set this option when you start SnowSQL, specify the `-o` command-line flag:

  ```
  $ snowsql ... -o variable_substitution=true
  ```

  Copy
* To set this option when in a SnowSQL session, execute the `!set` command in the session:

  ```
  user#> !set variable_substitution=true
  ```

  Copy

  Note

  There is currently no option to unset an option value, such as the `variable_substitution` option. If you need
  to disable variable substitution, execute the command `!set variable_substitution=false`.

### Substituting variables in a session[¶](#substituting-variables-in-a-session "Link to this heading")

After you [enable variable substitution](#label-snowsql-enabling-variable-substitution), you can use variables in SQL
statements.

To use a variable in a statement, use the `&variable_name` syntax. Note that variable names are case-insensitive. For
example:

> ```
> user#> !define snowshell=bash
>
> user#> !set variable_substitution=true
>
> user#> select '&snowshell';
>
> +--------+
> | 'BASH' |
> |--------|
> | bash   |
> +--------+
> ```
>
> Copy

If the `variable_substitution` option is not enabled, no variable substitution occurs. For example:

> ```
> user#> !define snowshell=bash
>
> user#> !set variable_substitution=false
>
> user#> select '&snowshell';
>
> +--------------+
> | '&SNOWSHELL' |
> |--------------|
> | &snowshell   |
> +--------------+
> ```
>
> Copy

If you refer to a variable that has not been defined, SnowSQL displays an error. For example:

> ```
> select '&z';
>
> Variable z is not defined
> ```
>
> Copy

To combine a variable with text, enclose the variable reference in curly braces. For example:

> ```
> user#> !define snowshell=bash
>
> user#> !set variable_substitution=true
>
> select '&{snowshell}_shell';
>
> +--------------+
> | 'BASH_SHELL' |
> |--------------|
> | bash_shell   |
> +--------------+
> ```
>
> Copy

To use an ampersand sign without using substitution, escape the ampersand sign with a second ampersand sign:

> `&&variable`

For example:

> ```
> user#> !set variable_substitution=true
>
> user#> select '&notsubstitution';
>
> Variable notsubstitution is not defined
>
> user#> select '&&notsubstitution';
>
> +--------------------+
> | '&NOTSUBSTITUTION' |
> |--------------------|
> | &notsubstitution   |
> +--------------------+
> ```
>
> Copy

### Listing variables[¶](#listing-variables "Link to this heading")

To list variables, execute the `!variables` or `!vars` command in the session:

> ```
> user#> !variables
>
> +-----------+-------+
> | Name      | Value |
> |-----------+-------|
> | snowshell | bash  |
> +-----------+-------+
> ```
>
> Copy

### Using the built-in variables[¶](#using-the-built-in-variables "Link to this heading")

SnowSQL includes a set of built-in variables that return metadata about statements executed in the current user session.

Each of these variable names begins with two underscore characters (“\_\_”).

`__rowcount`
:   Returns the number of rows affected by the most recent DML statement executed by the user.

    > ```
    > user#> insert into a values(1),(2),(3);
    >
    > +-------------------------+
    > | number of rows inserted |
    > |-------------------------|
    > |                       3 |
    > +-------------------------+
    > 3 Row(s) produced. Time Elapsed: 0.950s
    >
    > user#> !set variable_substitution=true
    >
    > user#> select &__rowcount;
    >
    > +---+
    > | 3 |
    > |---|
    > | 3 |
    > +---+
    > ```
    >
    > Copy

`__sfqid`
:   Returns the query ID for the most recent query executed by the user.

    > ```
    > user#> !set variable_substitution=true
    >
    > user#> select * from a;
    >
    > user#> select '&__sfqid';
    >
    > +----------------------------------------+
    > | 'A5F35B56-49A2-4437-BA0E-998496CE793E' |
    > |----------------------------------------|
    > | a5f35b56-49a2-4437-ba0e-998496ce793e   |
    > +----------------------------------------+
    > ```
    >
    > Copy

## Using auto-complete[¶](#using-auto-complete "Link to this heading")

Various SQL functions, table names, and variables are stored in SnowSQL and are auto-completed in interactive mode. To select an auto-complete suggestion, press the `Tab` key. To choose a different
suggestion, use the `↑` and `↓` keys to highlight the desired option, and then press `Tab`.

To disable auto-complete interactively, set the `auto_completion` configuration option to `False` in the [configuration file](snowsql-config.html#label-configuring-snowsql).

## Viewing your command-line history[¶](#viewing-your-command-line-history "Link to this heading")

Your recent command-line history can be recalled by using the `↑` key. Press the key repeatedly to scroll through the buffer.

### History file[¶](#history-file "Link to this heading")

The interactive command-line history file is named `history` and is located in `~/.snowsql/history`.

## Running batch scripts[¶](#running-batch-scripts "Link to this heading")

You can run batch scripts in two ways:

* Using connection parameters (while connecting to Snowflake)
* Executing commands (on the command line in the Snowflake session)

### Running while connecting (`-f` connection parameter)[¶](#running-while-connecting-f-connection-parameter "Link to this heading")

To execute a SQL script while connecting to Snowflake, use the `-f <input_filename>` connection parameter.

An output file for the script can be specified using `-o output_file=<output_filename>`. In addition, you can use `-o quiet=true` to turn off the standard output and
`-o friendly=false` to turn off the startup and exit messages.

For example:

> ```
> snowsql -a myorganization-myaccount -u jsmith -f /tmp/input_script.sql -o output_file=/tmp/output.csv -o quiet=true -o friendly=false -o header=false -o output_format=csv
> ```
>
> Copy

For more information about all connection parameters, see [Connection parameters reference](snowsql-start.html#label-snowsql-connection-parameters).

### Running in a session (`!source` or `!load` command)[¶](#running-in-a-session-source-or-load-command "Link to this heading")

To run a SQL script after connecting to Snowflake, execute the `!source` (or `!load`) command in the session.

For example:

> ```
> user#> !source example.sql
> ```
>
> Copy

## Exporting data[¶](#exporting-data "Link to this heading")

Output query results to a file in a defined format using the following [configuration options](snowsql-config.html#label-snowsql-options):

* `output_format=output_format`
* `output_file=output_filename`

To remove the splash text, header text, timing, and goodbye message from the output, also set the following options:

* `friendly=false`
* `header=false`
* `timing=false`

As with all configuration options, you can set them using any of the following methods:

* In the configuration file (before connecting to Snowflake).
* Using the `-o` or `--options` connection parameter (while connecting to Snowflake).
* Executing the `!set` command (on the command line in the Snowflake session).

Note that consecutive queries are appended to the output file. Alternatively, to redirect query output to a file and overwrite the file with each new statement, use the greater-than sign (`>`) in a
script.

In the following example, SnowSQL connects to an account using a named connection and queries a table. The output is written to a CSV file named `output_file.csv` in the current local directory:

Linux/macOS:

```
snowsql -c my_example_connection -d sales_db -s public -q 'select * from mytable limit 10' -o output_format=csv -o header=false -o timing=false -o friendly=false  > output_file.csv
```

Copy

Windows:

```
snowsql -c my_example_connection -d sales_db -s public -q "select * from mytable limit 10" -o output_format=csv -o header=false -o timing=false -o friendly=false  > output_file.csv
```

Copy

## Changing the SnowSQL prompt format[¶](#changing-the-snowsql-prompt-format "Link to this heading")

The SnowSQL prompt dynamically displays context information about the current session:

* When you log into Snowflake, the prompt displays your user name, as well as the default warehouse, database, and schema (if defaults have been set).
* If you use a USE command in the session to set or change the warehouse, database, or schema, the prompt changes to reflect the context.

You can control the appearance and structure of the prompt using the `prompt_format` configuration option and a Pygments token in brackets for each object type, in the form of `[token]`
(e.g. `[user]` or `[warehouse]`).

The token affects the prompt going forward. You can change the order and color for each token, as well as the delimiters between tokens.

As with all configuration options, you can set the prompt using any of the following methods:

* In the configuration file (before connecting to Snowflake).
* Using the `-o` or `--options` connection parameter (while connecting to Snowflake).
* Executing the `!set` command (on the command line in the Snowflake session).

Note

If you change the prompt using the connection parameter or directly on the command line, the change applies to the current session only. To persist the change in future sessions, set the option in
the configuration file.

### Supported tokens[¶](#supported-tokens "Link to this heading")

SnowSQL supports the following object types as tokens:

* `user`
* `account`
* `role`
* `database`
* `schema`
* `warehouse`

### Default prompt[¶](#default-prompt "Link to this heading")

The SnowSQL default prompt uses the following tokens and structure:

> ```
> [user]#[warehouse]@[database].[schema]>
> ```
>
> Copy

For example:

> ```
> jdoe#DATALOAD@BOOKS_DB.PUBLIC>
> ```
>
> Copy

### Prompt example[¶](#prompt-example "Link to this heading")

Continuing the example above, the following `!set` command executed in the command line adds the role token and changes the token order
to `user` and `role`, `database` and `schema`, then `warehouse`. It
also changes the delimiter for each token to a period (`.`) and sets the tokens to use different colors:

> ```
> jdoe#DATALOAD@BOOKS_DB.PUBLIC> !set prompt_format=[#FF0000][user].[role].[#00FF00][database].[schema].[#0000FF][warehouse]>
> ```
>
> Copy

This example results in the following prompt for the session:

> [![SnowSQL prompt format](../_images/snowsql-prompt-format.png)](../_images/snowsql-prompt-format.png)

## Disconnecting from Snowflake and stopping SnowSQL[¶](#disconnecting-from-snowflake-and-stopping-snowsql "Link to this heading")

SnowSQL provides separate commands for:

* Exiting individual connections (i.e. sessions) without stopping SnowSQL.
* Quitting SnowSQL, which also automatically terminates all connections.

To exit a connection/session, use the `!exit` command (or its alias, `!disconnect`). You can then connect again using `!connect <connection_name>` if you can defined multiple
connections in the SnowSQL `config` file. Note that, if you only have one connection open, the `!exit` command also quits/stops SnowSQL.

To exit all connections and then quit/stop SnowSQL, use the `!quit` command (or its alias, `!q`). You can also type
`CTRL` + `d` on your keyboard.

### Exit codes[¶](#exit-codes "Link to this heading")

There are several possible exit codes that are returned when SnowSQL quits/exits:

`0`:
:   Everything ran smoothly.

`1`:
:   Something went wrong with the client.

`2`:
:   Something went wrong with the command-line arguments.

`3`:
:   SnowSQL could not contact the server.

`4`:
:   SnowSQL could not communicate properly with the server.

`5`:
:   The `exit_on_error` configuration option was set and SnowSQL exited because of an error.

## Default key bindings[¶](#default-key-bindings "Link to this heading")

`Tab`
:   Accept the current auto-complete suggestion.

`CTRL` + `d`
:   Quit/stop SnowSQL.

## Commands reference[¶](#commands-reference "Link to this heading")

### `!abort`[¶](#abort "Link to this heading")

Aborts a query (specified by query ID). The query ID can be obtained from the History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page in the web interface.

For example:

> ```
> user#> !abort 77589bd1-bcbf-4ec8-9ebc-6c949b00614d;
> ```
>
> Copy

### `!connect`[¶](#connect "Link to this heading")

SnowSQL supports multiple sessions (i.e. connections) with `!connect <connection_name>`:

* The connection parameters/options associated with `connection_name` are stored in the corresponding `[connections.<connection_name>]` section in the SnowSQL configuration file.
* If a parameter/option is not specified in the `[connections.<connection_name>]` section, the unspecified parameter will default to the parameters under `[connections]`.

When connecting, the connection is added to your connection stack, and exiting will return you to your previous connection. Quitting will exit all of your connections and quit, no matter how many connections you have.

For example:

Configuration file:

> ```
> [connections.my_example_connection]
> ...
> ```
>
> Copy

Command line:

> ```
> user#> !connect my_example_connection
> ```
>
> Copy

### `!define`[¶](#define "Link to this heading")

Sets a variable to a specified value, using the following format:

> `!define <variable_name>=<variable_value>`

The name and value must be separated by a single `=` with no spaces. Valid characters that can be used in the variable are:

> `0-9a-zA-Z_`

For more information on defining and using variables, see [Using variables](#label-snowsql-variables).

### `!edit`[¶](#edit "Link to this heading")

Opens up the editor that was set using the `editor` connection parameter (if no editor was set, the default is `vim`). The command accepts a query as an argument. If no argument is passed,
it opens up the last query that was run.

Note

You must save before or while exiting the editor, or else any text that was entered/modified in the editor will not be saved.

### `!exit` , `!disconnect`[¶](#exit-disconnect "Link to this heading")

Drops the current connection and quits SnowSQL if it is the last connection.

### `!help` , `!helps` , `!h`[¶](#help-helps-h "Link to this heading")

Displays the help for SnowSQL commands.

### `!options` , `!opts`[¶](#options-opts "Link to this heading")

Returns a list of all the SnowSQL [configuration options](snowsql-config.html#label-snowsql-options) and their currently-set values. These options can be set using the `!set` command in the current SnowSQL
session.

Note

These options can also be set in the [configuration file](snowsql-config.html#label-configuring-snowsql) for SnowSQL or as [connector parameters](snowsql-start.html#label-connection-syntax) in the command line when
invoking SnowSQL.

### `!pause`[¶](#pause "Link to this heading")

Pause running queries. Press the return key to continue.

### `!print`[¶](#print "Link to this heading")

Prints the specified text to the screen and any files you are currently spooling to.

For example:

> ```
> user#> !print Include This Text
> ```
>
> Copy

### `!queries`[¶](#queries "Link to this heading")

Lists all queries that match the specified filters. The default filters are `session` and `amount=25`, which return the 25 most recent queries in the current session.

For example:

* Return the 25 most recent queries that ran in this current session:

  ```
  !queries session
  ```

  Copy
* Return the 20 most recent queries run in the account:

  ```
  !queries amount=20
  ```

  Copy
* Return the 20 most recent queries run in the account that took more than 200 milliseconds to run:

  ```
  !queries amount=20 duration=200
  ```

  Copy
* Return the 25 most recent queries that ran in the specified warehouse:

  ```
  !queries warehouse=mywh
  ```

  Copy

This command creates a variable for each query ID returned. Note that variable substitution must be enabled for you to use these variables. For example:

> ```
> user#> !queries session
>
> +-----+--------------------------------------+----------+-----------+----------+
> | VAR | QUERY ID                             | SQL TEXT | STATUS    | DURATION |
> |-----+--------------------------------------+----------+-----------+----------|
> | &0  | acbd6778-c68c-4e79-a977-510b2d8c08f1 | select 1 | SUCCEEDED |       19 |
> +-----+--------------------------------------+----------+-----------+----------+
>
> user#> !result &0
>
> +---+
> | 1 |
> |---|
> | 1 |
> +---+
>
> user#> !result acbd6778-c68c-4e79-a977-510b2d8c08f1
>
> +---+
> | 1 |
> |---|
> | 1 |
> +---+
> ```
>
> Copy

### `!quit` , `!q` (also `CTRL` + `d`)[¶](#quit-q-also-ctrl-d "Link to this heading")

Drops all connections and exits SnowSQL.

### `!rehash`[¶](#rehash "Link to this heading")

Re-syncs the auto-complete tokens.

Normal use does not require re-syncing the auto-complete tokens. However, forcing an update to the server-side tokens could be useful in certain scenarios (e.g. if a new user-defined function is
created in a different session).

### `!result`[¶](#result "Link to this heading")

Returns the result of a completed query (specified by query ID). Query IDs can be obtained from the History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page in the web interface or using the `!queries` command.

If the query is still running, the command waits until the query completes.

For example:

> ```
> user#> !result 77589bd1-bcbf-4ec8-9ebc-6c949b00614d;
> ```
>
> Copy

### `!set`[¶](#set "Link to this heading")

Sets the specified SnowSQL [configuration option](snowsql-config.html#label-snowsql-options) to a given value using the form `<option>=<value>`.

Note that there is no option currently to unset an option value. To change the value for an option, run the `!set` command again with the desired value.

For example:

> ```
> user#> !options
>
> +-----------------------+-------------------+
> | Name                  | Value             |
> |-----------------------+-------------------|
>  ...
> | rowset_size           | 1000              |
>  ...
> +-----------------------+-------------------+
>
> user#> !set rowset_size=500
>
> user#> !options
>
> +-----------------------+-------------------+
> | Name                  | Value             |
> |-----------------------+-------------------|
>  ...
> | rowset_size           | 500               |
>  ...
> +-----------------------+-------------------+
>
> user#> !set rowset_size=1000
>
> user#> !options
>
> +-----------------------+-------------------+
> | Name                  | Value             |
> |-----------------------+-------------------|
>  ...
> | rowset_size           | 1000              |
>  ...
> +-----------------------+-------------------+
> ```
>
> Copy

Important

Spaces are not allowed between an option and its value. Some options support a defined set of values; SnowSQL returns an error if the provided value is unsupported. You cannot create new options.

For a list of all the configuration options you can set, use the `!options` command.

### `!source` , `!load`[¶](#source-load "Link to this heading")

Executes SQL from a file. You can SQL from local files or a URL.

For example:

> ```
> user#> !source example.sql
>
> user#> !load /tmp/scripts/example.sql
>
> user#> !load http://www.example.com/sql_text.sql
> ```
>
> Copy

### `!spool`[¶](#spool "Link to this heading")

This command can be executed in two ways:

* Enable spooling and write the results of all subsequent statements/queries to the specified file:

  > `!spool <file_name>`
* Turn off results spooling (if it is enabled):

  > `!spool off`

For example:

> ```
> user#> select 1 num;
>
> +-----+
> | NUM |
> |-----|
> |   1 |
> +-----+
>
> user#> !spool /tmp/spool_example
>
> user#> select 2 num;
>
> +---+
> | 2 |
> |---|
> | 2 |
> +---+
>
> user#> !spool off
>
> user#> select 3 num;
>
> +---+
> | 3 |
> |---|
> | 3 |
> +---+
>
> user#> !exit
>
> Goodbye!
>
> $ cat /tmp/spool_example
>
> +---+
> | 2 |
> |---|
> | 2 |
> +---+
> ```
>
> Copy

You can change the output format by first running the `!set output_format=<format>` command. The option supports the following values:

* `expanded`
* `fancy_grid`
* `grid`
* `html`
* `latex`
* `latex_booktabs`
* `mediawiki`
* `orgtbl`
* `pipe`
* `plain`
* `psql`
* `rst`
* `simple`
* `tsv`

Recommended value: `psql`, `fancy_grid`, or `grid`

For example, to output in CSV format:

> ```
> user#> !set output_format=csv
>
> user#> !spool /tmp/spool_example
> ```
>
> Copy

### `!system`[¶](#system "Link to this heading")

Executes a shell command.

> `!system <command>`

The following example runs the `ls` command in the user’s home directory:

> ```
> user#> !system ls ~
> ```
>
> Copy

### `!variables` , `!vars`[¶](#variables-vars "Link to this heading")

Lists all current variables. Returns each `<variable_name>=<variable_value>` pair currently defined.

Once a variable is assigned, it cannot be deleted, but its value can be removed by specifying the variable name with no value. For example:

> ```
> user#> !set variable_substitution=true
>
> user#> !define SnowAlpha=_ALPHA_
>
> user#> !variables
>
> +------------------+---------+
> | Name             | Value   |
> |------------------+---------|
> | snowalpha        | _ALPHA_ |
> +------------------+---------+
>
> user#> !define SnowAlpha
>
> user#> !variables
>
> +------------------+-------+
> | Name             | Value |
> |------------------+-------|
> | snowalpha        |       |
> +------------------+-------+
>
> user#> !define snowalpha=456
>
> user#> select &snowalpha;
>
> +-----+
> | 456 |
> |-----|
> | 456 |
> +-----+
> ```
>
> Copy

For more information about setting variables, see [Using variables](#label-snowsql-variables) (in this topic).

## Troubleshooting[¶](#troubleshooting "Link to this heading")

### Error Message: `Variable is not defined`[¶](#error-message-variable-is-not-defined "Link to this heading")

Cause:
:   If you see this error message when running commands in SnowSQL, the cause might be an ampersand (`&`) inside a
    [CREATE FUNCTION](../sql-reference/sql/create-function) command. (The ampersand is the SnowSQL variable substitution character.) For
    example, executing the following in SnowSQL causes this error:

    ```
    create function mask_bits(...)
        ...
        as
        $$
        var masked = (x & y);
        ...
        $$;
    ```

    Copy

    The error occurs when the function is created, not when the function is called.

Solution:
:   If you do not intend to use variable substitution in SnowSQL, you can explicitly disable variable substitution by executing the
    following command:

    ```
    !set variable_substitution=false;
    ```

    Copy

    For more information about variable substitution, see [Using variables](#label-snowsql-variables).

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

1. [Executing commands](#executing-commands)
2. [Using variables](#using-variables)
3. [Using auto-complete](#using-auto-complete)
4. [Viewing your command-line history](#viewing-your-command-line-history)
5. [Running batch scripts](#running-batch-scripts)
6. [Exporting data](#exporting-data)
7. [Changing the SnowSQL prompt format](#changing-the-snowsql-prompt-format)
8. [Disconnecting from Snowflake and stopping SnowSQL](#disconnecting-from-snowflake-and-stopping-snowsql)
9. [Default key bindings](#default-key-bindings)
10. [Commands reference](#commands-reference)
11. [Troubleshooting](#troubleshooting)

Related content

1. [Query Data in Snowflake](/user-guide/../guides-overview-queries)
2. [Load data into Snowflake](/user-guide/../guides-overview-loading-data)
3. [Overview of data unloading](/user-guide/data-unload-overview)