---
auto_generated: true
description: SnowConvert AI Helpers is a set of classes with functions designed to
  facilitate the conversion of Teradata script files to Python files that Snowflake
  can interpret.
last_scraped: '2026-01-14T16:53:46.865818+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/snowconvert-script-helpers
title: SnowConvert AI - Teradata - SnowConvert AI Scripts Helpers | Snowflake Documentation
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

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](../sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](README.md)

              * [BTEQ](bteq-translation.md)
              * [FLOAD](fastload-translation.md)
              * [MLOAD](multiload-translation.md)
              * [TPT](tpt-translation.md)
              * [Script helpers](snowconvert-script-helpers.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts To Python](README.md)Script helpers

# SnowConvert AI - Teradata - SnowConvert AI Scripts Helpers[¶](#snowconvert-ai-teradata-snowconvert-ai-scripts-helpers "Link to this heading")

SnowConvert AI Helpers is a set of classes with functions designed to facilitate the conversion of Teradata script files to Python files that Snowflake can interpret.

SnowConvert AI for Teradata can take in any Teradata SQL or scripts (BTEQ, FastLoad, MultiLoad, and TPump) and convert them to functionally equivalent Snowflake SQL, JavaScript embedded in Snowflake SQL, and Python. Any output Python code from SnowConvert AI will call functions from these helper classes to complete the conversion and create a functionally equivalent output in Snowflake.

The [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) will also be called in order to connect to your Snowflake account and run the output Python code created by SnowConvert.

The latest version information of the package can be found [here](https://pypi.org/project/snowconvert-helpers/).

Note

The Python package`snowconvert-helpers` supports Python versions 3.6, 3.7, 3.8, and 3.9.

## Script Migration[¶](#script-migration "Link to this heading")

### Source[¶](#source "Link to this heading")

Suppose you have the following BTEQ code to be migrated.

```
 insert into table1 values(1, 2);
insert into table1 values(3, 4);
insert into table1 values(5, 6);
```

Copy

### Output[¶](#output "Link to this heading")

You should get an output like the one below.

Note

The `log_on`function parameters (‘user’, ‘password’, ‘account’, ‘database’, ‘warehouse’, ‘role’, ‘token’) should be defined by the user.

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    INSERT INTO table1
    VALUES (1, 2)
    """)
  exec("""
    INSERT INTO table1
    VALUES (3, 4)
    """)
  exec("""
    INSERT INTO table1
    VALUES (5, 6)
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

## Getting Started[¶](#getting-started "Link to this heading")

To install the package, you should run the following command in your python environment. If you’re not familiar with installing packages in Python, visit the following page on python packages (<https://packaging.python.org/tutorials/installing-packages/>).

```
 pip install snowconvert-helpers
```

Copy

Once your package is installed, you will be able to run the script migrated code in Python.

## Run the code[¶](#run-the-code "Link to this heading")

To run the migrated code, you just have to open the `Command Prompt` or the `Terminal` and execute the following command.

```
 python sample_BTEQ.py
```

Copy

If the script has no errors, you will get in your console an output like the one below.

```
 Executing: INSERT INTO PUBLIC.table1 VALUES (1, 2).
Printing Result Set:
number of rows inserted
1

Executing: INSERT INTO PUBLIC.table1 VALUES (3, 4).
Printing Result Set:
number of rows inserted
1

Executing: INSERT INTO PUBLIC.table1 VALUES (5, 6).
Printing Result Set:
number of rows inserted
1

Error Code 0
Script done >>>>>>>>>>>>>>>>>>>>
Error Code 0
```

Copy

### Passing connection parameters[¶](#passing-connection-parameters "Link to this heading")

There are several ways to pass the connection parameters to the connection of the database:

* As parameters in the function call snowconvert.helpers.log\_on inside the python file.
* As positional parameters with the specific order of user, password, account, database, warehouse, and role when the python is being executed from the command line.
* As named parameters with no order restriction of SNOW\_USER, SNOW\_PASSWORD, SNOW\_ACCOUNT, SNOW\_DATABASE, SNOW\_WAREHOUSE, SNOW\_ROLE, SNOW\_QUERYTAG, SNOWAUTHENTICATOR and SNOWTOKEN when the python is being executed from the command line and any of them are passed like –param-VARNAME=VALUE.
* As environment variables named SNOW\_USER, SNOW\_PASSWORD, SNOW\_ACCOUNT, SNOW\_DATABASE, SNOW\_WAREHOUSE, SNOW\_ROLE, SNOW\_QUERYTAG, SNOWAUTHENTICATOR and SNOWTOKEN before python execution.

The previous order specified is the way to determine the precedence.

#### Parameters in the function call[¶](#parameters-in-the-function-call "Link to this heading")

They can be set as positional parameters in the function call as follows.

```
    .....
   con = snowconvert.helpers.log_on(
     'myuser',
     'mypassword',
     'myaccount',
     'mydatabase',
     'mywarehouse',
     'myrole',
     5,
     'myauthenticator',
     'mytoken')
   .....
```

Copy

Or they can be set any of the named parameters in any order in the function call as follows.

```
    .....
   con = snowconvert.helpers.log_on(
     account:'myaccount',
     password:'mypassword',
     user:'myuser',     
     warehouse:'mywarehouse',
     login_timeout:5,
     authenticator:'myauthenticator',
     toke:'mytoken')
   .....
```

Copy

#### Positional parameters[¶](#positional-parameters "Link to this heading")

They need to be set in the specific order in the command line as follows.

```
 python sample_BTEQ.py myuser mypassword myaccount mydatabase mywarehouse myrole myauthenticator mytokenr
```

Copy

Or they can be set only some of the parameters but always starting with the user parameter as follows.

```
 python sample_BTEQ.py myuser mypassword myaccount
```

Copy

#### Named parameters[¶](#named-parameters "Link to this heading")

They can be set any of the named parameters in any order in the command line as follows (use a single line, multiline shown for readability reasons).

```
python sample_BTEQ.py --param-SNOW_WAREHOUSE=mywarehouse 
  --param-SNOW_ROLE=myrole 
  --param-SNOW_PASSWORD=mypassword 
  --param-SNOW_USER=myuser 
  --param-SNOW_QUERYTAG=mytag 
  --param-SNOW_ACCOUNT=myaccount
  --param-SNOW_DATABASE=mydatabase 
  --param-SNOW_AUTHENTICATOR=myauthenticator
  --param-SNOW_TOKEN=mytoken
  --param-PRIVATE_KEY_PATH=myprivatekey
  --param-PRIVATE_KEY_PASSWORD=myprivatekeypassword
```

Copy

#### Environment variables[¶](#environment-variables "Link to this heading")

Before calling the python script, any of the following environment variables can be set:

* SNOW\_USER
* SNOW\_PASSWORD
* SNOW\_ACCOUNT
* SNOW\_DATABASE
* SNOW\_WAREHOUSE
* SNOW\_ROLE
* SNOW\_QUERYTAG
* SNOW\_AUTHENTICATOR
* SNOW\_TOKEN
* PRIVATE\_KEY\_PATH
* PRIVATE\_KEY\_PASSWORD

#### Key Pair Authentication[¶](#key-pair-authentication "Link to this heading")

The `log_on` function can also support the key pair authetication process. Review the following [Snowflake documentation](https://docs.snowflake.com/en/user-guide/key-pair-auth) for more information about the key creation . Please notice the required parameters:

`log_on(`

`user='YOUR_USER',`

`account='YOUR_ACCOUNT',`

`role = 'YOUR_ROLE',`

`warehouse = 'YOUR_WAREHOUSE',`

`database = 'YOUR_DATABASE',`

`private_key_path='/YOUR_PATH/rsa_key.p8',`

`private_key_password='YOUR_PASSWORD')`

### Example of passing environment variables[¶](#example-of-passing-environment-variables "Link to this heading")

Here is an example of using SNOW\_AUTHENTICATOR, SNOW\_USER and SNOW\_PASSWORD. They must be defined before running the output python file and then run the python generated file.

#### Windows[¶](#windows "Link to this heading")

```
 SET SNOW_AUTHENTICATOR=VALUE
SET SNOW_USER=myuser
SET SNOW_PASSWORD=mypassword
python sample_BTEQ.py
```

Copy

##### Linux/Mac[¶](#linux-mac "Link to this heading")

```
 export SNOW_AUTHENTICATOR=VALUE
export SNOW_USER=myuser
export SNOW_PASSWORD=mypassword
python3 sample_BTEQ.py
```

Copy

### Enabling Logging[¶](#enabling-logging "Link to this heading")

To enable logging, you should enable an environment variable called SNOW\_LOGGING set as true.

Then, if you want to customize the logging configuration you can pass a parameter to the `snowconvert.helpers.configure_log()` method like this:

```
 snowconvert.helpers.configure_log("SOMEPATH.conf")
```

Copy

The configuration file should contain the next structure. For more information about python logging, [click here](https://docs.python.org/es/3/library/logging.config.html)

```
 [loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('python2.log', 'w')

[formatter_simpleFormatter]
format=%(asctime)s -%(levelname)s - %(message)s
```

Copy

## Snowflake[¶](#snowflake "Link to this heading")

Once any migrated code you have been executed, you can go to Snowflake and check your changes or deployments.

```
 select * from PUBLIC.table1;
```

Copy

You will be able to see the rows you have inserted in the example above.

![Query result](../../../../../_images/result.png)

## Local Helpers Documentation[¶](#local-helpers-documentation "Link to this heading")

First of all, it is required to install the python package named pydoc (Available since version 2.0.2 of snowconvert-helpers).

```
 pip install pydoc
```

Copy

Then in order to display the python documentation of the package snowconvert-helpers, you should go to a folder where you have the converted output code and you have a python output.

```
D:\bteq\Output>dir

 Volume in drive D is Storage
 Volume Serial Number is 203C-168C

 Directory of D:\bteq\Output

05/25/2021  03:55 PM    <DIR>          .
05/25/2021  03:55 PM    <DIR>          ..
05/25/2021  03:55 PM               630 input_BTEQ.py
               1 File(s)            630 bytes
               2 Dir(s)  1,510,686,502,912 bytes free
```

Copy

Located in this directory you need to run:

```
 python -m pydoc -b
```

Copy

The console will open your preferred browser with the HTML help of the documentation for all the installed packages.

```
D:\bteq\Output>python -m pydoc -b
Server ready at http://localhost:61355/
Server commands: [b]rowser, [q]uit
server>
```

Copy

This will open the browser with the documentation of your code like:

![Home page for the generated local documentation](../../../../../_images/builtin.png)

Scroll thru the end of the page to see the installed packages. And you will see something similar to:

![Local installed packages documentation index](../../../../../_images/scroll.png)

Clicking in the SnowConvert AI(package) you will see something like:

![Home page for the snowconvert-helpers documentation](../../../../../_images/other.png)

Clicking in the module helpers will display a screen similar to:

![Home page for helpers module](../../../../../_images/module.png)

Then you can scroll thru the functions and classes of the module.

![Functions documentation](../../../../../_images/final.png)

## Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

## Related EWIs [¶](#related-ewis "Link to this heading")

No related EWIs.

## Technical Documentation[¶](#technical-documentation "Link to this heading")

### Functions[¶](#functions "Link to this heading")

All the functions defined in the project.

#### access[¶](#access "Link to this heading")

Note

**`access`**`(path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True)`

##### **Description:**[¶](#description "Link to this heading")

*Use the real uid/gid to test for access to a path.*

*dir\_fd, effective\_ids, and follow\_symlinks may not be implemented on your platform. If they are unavailable, using them will raise a NotImplementedError.*

*Note that most operations will use the effective uid/gid, therefore this routine can be used in a suid/sgid environment to test if the invoking user has the specified access to the path.*

##### **Parameters:**[¶](#parameters "Link to this heading")

* **`path,`** Path to be tested; can be string, bytes, or a path-like [object](http://localhost:65458/builtins.html#object)
* **`mode,`** Operating-system mode bitfield. Can be F\_OK to test existence, or the inclusive-OR of R\_OK, W\_OK, and X\_OK
* **`dir_fd,`** If not None, it should be a file descriptor open to a directory, and path should be relative; path will then be relative to that directory
* **`effective_ids,`** If True, access will use the effective uid/gid instead of the real uid/gid
* **`follow_symlinks,`** If False, and the last element of the path is a symbolic link, access will examine the symbolic link itself instead of the file the link points to

#### at\_exit\_helpers[¶](#at-exit-helpers "Link to this heading")

Note

**`at_exit_helpers`**`()`

##### **Description:**[¶](#id1 "Link to this heading")

*Executes at the exit of the execution of the script.*

#### colored[¶](#colored "Link to this heading")

Note

**`colored`**`(text, color='blue')`

##### **Description:**[¶](#id2 "Link to this heading")

*Prints colored text from the specified color.*

##### **Parameters:**[¶](#id3 "Link to this heading")

* `text`**`,`** The text to be printed
* `color="blue"`**`,`** The color to print

#### configure\_log[¶](#configure-log "Link to this heading")

Note

**`configure_log`**`(configuration_path)`

##### **Description:**[¶](#id4 "Link to this heading")

*Configures the logging that will be performed for any data-related execution on the snowflake connection. The log file is named ‘snowflake\_python\_connector.log’ by default.*

**Parameters:**

* `configuration_path`**`,`** The configuration path of the file that contains all the settings desired for the logging

#### drop\_transient\_table[¶](#drop-transient-table "Link to this heading")

Note

**`drop_transient_table`**`(tempTableName, con=None)`

##### **Description:**[¶](#id5 "Link to this heading")

*Drops the transient table with the specified name.*

**Parameters:**

* `tempTableName`**`,`** The name of the temporary table
* `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exception\_hook[¶](#exception-hook "Link to this heading")

Note

**`exception_hook`**`(exctype, value, tback)`

##### **Description:**[¶](#id6 "Link to this heading")

**Parameters:**

* `exctype`
* `value`
* `tback`

#### exec[¶](#exec "Link to this heading")

Note

**`exec`**`(sql_string, using=None, con=None)`

##### **Description:**[¶](#id7 "Link to this heading")

*Executes a sql string using the last connection, optionally it uses arguments or an specific connection. Examples:*

* *`exec("SELECT * FROM USER")`*
* *`exec("SELECT * FROM USER", con)`*
* *`exec("SELECT * FROM CUSTOMER WHERE CUSTOMERID= %S", customer)`*

**Parameters:**

* `sql_string`**`,`** The definition of the sql
* `using=None`**`,`** The optional parameter that can be used in the sql passed
* `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exec\_file[¶](#exec-file "Link to this heading")

Note

**`exec_file`**`(filename, con=None)`

##### **Description:**[¶](#id8 "Link to this heading")

*Reads the content of a file and executes the sql statements contained with the specified connection.*

**Parameters:**

* `filename`**`,`** The filename to be read and executed
* `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### exec\_os[¶](#exec-os "Link to this heading")

Note

**`exec_os`**`(command)`

##### **Description:**[¶](#id9 "Link to this heading")

*Executes a command in the operative system.*

#### exec\_sql\_statement[¶](#exec-sql-statement "Link to this heading")

Note

**`exec_sql_statement`**`(sql_string, con, using=None)`

##### **Description:**[¶](#id10 "Link to this heading")

*Executes a sql statement in the connection passed, with the optional arguments.*

**Parameters:**

* `sql_string`**`,`** The sql containing the string to be executed
* `con`**`,`** The connection to be used
* `using`**`,`** The optional parameters to be used in the sql execution

#### **expands\_using\_params**[¶](#expands-using-params "Link to this heading")

Note

**`expands_using_params`**`(statement, params)`

##### **Description:**[¶](#id11 "Link to this heading")

*Expands the statement passed with the parameters.*

**Parameters:**

* `statement`**`,`** The sql containing the string to be executed
* `params`**`,`** The parameters of the sql statement

#### **expandvar**[¶](#expandvar "Link to this heading")

Note

**`expandvar`**`(str)`

##### **Description:**[¶](#id12 "Link to this heading")

*Expands the variable from the string passed.*

**Parameters:**

* `str`**`,`** The string to be expanded with the variables

#### **expandvars**[¶](#expandvars "Link to this heading")

Note

**`expandvars`**`(path, params, skip_escaped=False)`

##### **Description:**[¶](#id13 "Link to this heading")

*Expand environment variables of form $var and ${var}. If parameter ‘skip\_escaped’ is True, all escaped variable references (i.e. preceded by backslashes) are skipped. Unknown variables are set to ‘default’. If ‘default’ is None, they are left unchanged.*

**Parameters:**

* `path`**`,`**
* `params`**`,`**
* `skip_escaped=False`**`,`**

#### **fast\_load**[¶](#fast-load "Link to this heading")

Note

**`fast_load`**`(target_schema, filepath, stagename, target_table_name, con=None)`

##### **Description:**[¶](#id14 "Link to this heading")

*Executes the fast load with the passed parameters target\_schema, filepath, stagename and target\_table\_name.*

**Parameters:**

* `target_schema`**`,`** The name of the schema to be used in the fast load
* `filepath`**`,`** The filename path to be loaded in the table
* `target_table_name`**`,`** The name of the table that will have the data loaded
* `con=None`**`,`** The connection to be used, if None is passed it will use the last connection performed

#### **file\_exists\_and\_readable**[¶](#file-exists-and-readable "Link to this heading")

Note

**`file_exists_and_readable`**`(filename)`

##### **Description:**[¶](#id15 "Link to this heading")

**Parameters:**

* `filename`**`,`**

#### **get\_argkey**[¶](#get-argkey "Link to this heading")

Note

**`get_argkey`**`(astr)`

##### **Description:**[¶](#id16 "Link to this heading")

*Gets the argument key value from the passed string. It must start with the string ‘–param-’*

**Parameters:**

* `astr`**`,`** The argument string to be used. The string should have a value similar to –param-column=32 and the returned string will be ‘32

#### **get\_error\_position**[¶](#get-error-position "Link to this heading")

Note

**`get_error_position`**`()`

##### **Description:**[¶](#id17 "Link to this heading")

*Gets the error position from the file using the information of the stack of the produced error.*

#### **get\_from\_vars\_or\_args\_or\_environment**[¶](#get-from-vars-or-args-or-environment "Link to this heading")

Note

**`get_from_vars_or_args_or_environment`**`(arg_pos, variable_name, vars, args)`

##### **Description:**[¶](#id18 "Link to this heading")

*Gets the argument from the position specified or gets the value from the table vars or gets the environment variable name passed.*

**Parameters:**

* `arg_pos`**`,`** The argument position to be used from the arguments parameter
* `variable_name`**`,`** The name of the variable to be obtained
* `vars`**`,`** The hash with the variables names and values
* `args`**`,`** The arguments array parameter

#### **import\_data\_to\_temptable**[¶](#import-data-to-temptable "Link to this heading")

Note

**`import_data_to_temptable`**`(tempTableName, inputDataPlaceholder, con)`

##### **Description:**[¶](#id19 "Link to this heading")

*Imports data to a temporary table using an input data place holder.*

**Parameters:**

* `tempTableName,` The temporary table name.
* `inputDataPlaceholder,` The input place holder used that is a stage in the snowflake database
* `con,` The connection to be used

#### **import\_file**[¶](#import-file "Link to this heading")

Note

**`import_file`**`(filename, separator=' ')`

##### **Description:**[¶](#id20 "Link to this heading")

*Imports the passed filename with the optional separator.*

**Parameters:**

* `filename,` The filename path to be imported
* `separator=' ',` The optional separator

#### **import\_file\_to\_temptable**[¶](#import-file-to-temptable "Link to this heading")

Note

**`import_file_to_temptable`**`(filename, tempTableName, columnDefinition)`

##### **Description:**[¶](#id21 "Link to this heading")

*Imports the file passed to a temporary table. It will use a public stage named as the temporary table with the prefix Stage\_. At the end of the loading to the temporary table, it will delete the stage that was used in the process.*

**Parameters:**

* `filename,` The name of the file to be read
* `tempTableName,` The name of the temporary table
* `columnDefinition,` The definition of all the fields that will have the temporary table

#### **import\_reset**[¶](#import-reset "Link to this heading")

Note

**`import_reset`**`()`

##### **Description:**[¶](#id22 "Link to this heading")

#### **log**[¶](#log "Link to this heading")

Note

**`log`**`(*msg, level=20, writter=None)`

##### **Description:**[¶](#id23 "Link to this heading")

*Prints a message to the console (standard output) or to the log file, depending on if logging is enabled*

**Parameters:**

* `*msg,` The message to print or log
* `level=20,`
* `writter=None,`

#### **log\_on**[¶](#log-on "Link to this heading")

Note

**`log_on`**`(user=None, password=None, account=None, database=None, warehouse=None, role=None, login_timeout=10, authenticator=None)`

##### **Description:**[¶](#id24 "Link to this heading")

*Logs on the snowflake database with the credentials, database, warehouse, role, login\_timeout and authenticator passed parameters.*

**Parameters:**

* `user,` The user of the database
* `password` The password of the user of the database
* `database,` The database to be connected
* `warehouse,` The warehouse of the database to be connected
* `role,` The role to be connected
* `login_timeout,` The maximum timeout before giving error if the connection is taking too long to connect
* `authenticator,` The authenticator supported value to use like SNOWFLAKE, EXTERNALBROWSER, SNOWFLAKE\_JWT or OAUTH
* `token,` The OAUTH or JWT token

#### **os**[¶](#os "Link to this heading")

Note

**`os`**`(args)`

##### **Description:**[¶](#id25 "Link to this heading")

**Parameters:**

* `args,`

#### **print\_table**[¶](#print-table "Link to this heading")

Note

**`print_table`**`(dictionary)`

##### **Description:**[¶](#id26 "Link to this heading")

*Prints the dictionary without exposing user and password values.*

**Parameters:**

* `dictionary,`

#### **quit\_application**[¶](#quit-application "Link to this heading")

Note

**`quit_application`**`(code=None)`

##### **Description:**[¶](#id27 "Link to this heading")

*Quits the application and optionally returns the passed code.*

**Parameters:**

* `code=None,` The code to be returned after it quits

#### **read\_params\_args**[¶](#read-params-args "Link to this heading")

Note

**`read_param_args`**`(args)`

##### **Description:**[¶](#id28 "Link to this heading")

*Reads the parameter arguments from the passed array.*

**Parameters:**

* `args,` The arguments to be used

#### **readrun**[¶](#readrun "Link to this heading")

Note

**readrun**(line, skip=0)

##### **Description:**[¶](#id29 "Link to this heading")

*Reads the given filename lines and optionally skips some lines at the beginning of the file.*

**Parameters:**

* `line,` The filename to be read
* `skip=0,` The lines to be skipped

#### **remark**[¶](#remark "Link to this heading")

Note

**remark**(arg)

##### **Description:**[¶](#id30 "Link to this heading")

*Prints the argument.*

**Parameters:**

* `arg,` The argument to be printed

#### **repeat\_previous\_sql\_statement**[¶](#repeat-previous-sql-statement "Link to this heading")

Note

**`repeat_previous_sql_statement`**`(con=None, n=1)`

##### **Description:**[¶](#id31 "Link to this heading")

*Repeats the previous executed sql statement(s).*

**Parameters:**

* `con=None,` Connection if specified. If it is not passed it will use the last connection performed
* `n=1,` The number of previous statements to be executed again

#### **set\_default\_error\_level**[¶](#set-default-error-level "Link to this heading")

Note

**`set_default_error_level`**`(severity_value)`

##### **Description:**[¶](#id32 "Link to this heading")

**Parameters:**

* `severity_value,`

#### **set\_error\_level**[¶](#set-error-level "Link to this heading")

Note

**`set_error_level`**`(arg, severity_value)`

##### **Description:**[¶](#id33 "Link to this heading")

**Parameters:**

* `arg,`
* `severity_value,`

#### **simple\_fast\_load**[¶](#simple-fast-load "Link to this heading")

Note

**`simple_fast_load`**`(con, target_schema, filepath, stagename, target_table_name)`

##### **Description:**[¶](#id34 "Link to this heading")

Executes a simple fast load in the connection and the passed parameter target\_schema, filepath, stagename and target table name.

**Parameters:**

* `arg,` The connection to be used
* `target_schema,` The name of the schema to be used in the fast load
* `filepath,` The filename path to be loaded in the table
* `target_table_name,` The name of the table that will have the data loaded

#### **stat**[¶](#stat "Link to this heading")

Note

**`stat`**`(path, *, dir_fd=None, follow_symlinks=True)`

##### **Description:**[¶](#id35 "Link to this heading")

*Perform a stat system call on the given path.* dir\_fd and follow\_symlinks may not be implemented on your platform. If they are unavailable, using them will raise a NotImplementedError. It’s an error to use dir\_fd or follow\_symlinks when specifying path as an open file descriptor

**Parameters:**

* `path,` Path to be examined; can be string, bytes, a path-like [object](http://localhost:55262/builtins.html#object) or  
  open-file-descriptor int
* `dir_fd,` If not None, it should be a file descriptor open to a directory, and path should be a relative string; path will then be relative to that directory
* `follow_symlinks,` If False, and the last element of the path is a symbolic link, stat will examine the symbolic link itself instead of the file the link points to

#### **system**[¶](#system "Link to this heading")

Note

**`system`**`(command)`

##### **Description:**[¶](#id36 "Link to this heading")

*Execute the command in a subshell.*

**Parameters:**

* *`command`*`,`

#### **using**[¶](#using "Link to this heading")

Note

**`using`**`(*argv)`

##### **Description:**[¶](#id37 "Link to this heading")

**Parameters:**

* *`*argv`*`,`

### Classes[¶](#classes "Link to this heading")

All the classes defined in the project

#### BeginLoading Class[¶](#beginloading-class "Link to this heading")

This class contains the `import_file_to_tab` static function which provides support for the BEGIN LOADING and associated commands in FastLoad.

##### `import_file_to_tab()`[¶](#import-file-to-tab "Link to this heading")

Parameters:

1. `target_schema_table`

   * the target schema (optional) and table name
2. `define_file`

   * The name of the file to be read
3. `define_columns`

   * The definition of all the columns for the temporary table
4. `begin_loading_columns`

   * The column names to insert. Dictates the order in which values are inserted
5. `begin_loading_values`

   * The list of raw insert values to convert
6. `field_delimiter`

   * The field delimiter
7. *(optional)* `skip_header`

   * The number of rows to skip
8. *(optional)* `input_data_place_holder`

   * The location of the file in a supported cloud provider. Set parameter when the file is not stored locally
9. *(optional)* `con`

   * The connection to be used

#### Export Class[¶](#export-class "Link to this heading")

Static methods in the class

* `defaults()`
* `null(value=None)`
* `record_mode(value=None)`
* `report(file, separator=' ')`
* `reset()`
* `separator_string(value=None)`
* `separator_width(value=None)`
* `side_titles(value=None)`
* `title_dashes(value=None, withValue=None)`
* `title_dashes_with(value=None)`
* `width(value=None)`

Data and other attributes defined here

* `expandedfilename = None`
* `separator = ''` \

#### Import Class[¶](#import-class "Link to this heading")

Methods in the class

* `reset()`

Static methods in the class

* `file(file, separator=' ')`
* `using(globals, *argv)`

Data and other attributes defined in the class

* `expandedfilename = None`
* `no_more_rows = False`
* `read_obj = None`
* `reader = None`
* `separator = ' '`

#### `Parameters` Class[¶](#parameters-class "Link to this heading")

Data and other attributes defined in the class

* `passed_variables = {}`

##### [¶](#id38 "Link to this heading")

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

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Script Migration](#script-migration)
2. [Getting Started](#getting-started)
3. [Run the code](#run-the-code)
4. [Snowflake](#snowflake)
5. [Local Helpers Documentation](#local-helpers-documentation)
6. [Known Issues](#known-issues)
7. [Related EWIs](#related-ewis)
8. [Technical Documentation](#technical-documentation)