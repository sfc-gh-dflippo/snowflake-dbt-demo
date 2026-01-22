---
auto_generated: true
description: To use Snowpark in your application, you need to create a session. For
  convenience in writing code, you can also import the names of packages and objects.
last_scraped: '2026-01-14T16:55:06.034368+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session
title: Creating a Session for Snowpark Python | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../index.md)

   * [Java](../java/index.md)
   * [Python](index.md)

     + [Setting Up a Development Environment](setup.md)
     + [Creating a Session](creating-session.md)
     + [Snowpark DataFrames](working-with-dataframes.md)
     + [pandas on Snowflake](pandas-on-snowflake.md)
     + [Python API Reference](../reference/python/latest/index.md)
   * [Scala](../scala/index.md)
7. [Spark workloads on Snowflake](../../snowpark-connect/snowpark-connect-overview.md)
8. Machine Learning
9. [Snowflake ML](../../snowflake-ml/overview.md)
10. Snowpark Code Execution Environments
11. [Snowpark Container Services](../../snowpark-container-services/overview.md)
12. [Functions and procedures](../../extensibility.md)
13. [Logging, Tracing, and Metrics](../../logging-tracing/logging-tracing-overview.md)
14. Snowflake APIs
15. [Snowflake Python APIs](../../snowflake-python-api/snowflake-python-overview.md)
16. [Snowflake REST APIs](../../snowflake-rest-api/snowflake-rest-api.md)
17. [SQL API](../../sql-api/index.md)
18. Apps
19. Streamlit in Snowflake

    - [About Streamlit in Snowflake](../../streamlit/about-streamlit.md)
    - Getting started

      - [Deploy a sample app](../../streamlit/getting-started/overview.md)
      - [Create and deploy Streamlit apps using Snowsight](../../streamlit/getting-started/create-streamlit-ui.md)
      - [Create and deploy Streamlit apps using SQL](../../streamlit/getting-started/create-streamlit-sql.md)
      - [Create and deploy Streamlit apps using Snowflake CLI](../../streamlit/getting-started/create-streamlit-snowflake-cli.md)
    - Streamlit object management

      - [Billing considerations](../../streamlit/object-management/billing.md)
      - [Security considerations](../../streamlit/object-management/security.md)
      - [Privilege requirements](../../streamlit/object-management/privileges.md)
      - [Understanding owner's rights](../../streamlit/object-management/owners-rights.md)
      - [PrivateLink](../../streamlit/object-management/privatelink.md)
      - [Logging and tracing](../../streamlit/object-management/logging-tracing.md)
    - App development

      - [Runtime environments](../../streamlit/app-development/runtime-environments.md)
      - [Dependency management](../../streamlit/app-development/dependency-management.md)
      - [File organization](../../streamlit/app-development/file-organization.md)
      - [Secrets and configuration](../../streamlit/app-development/secrets-and-configuration.md)
      - [Editing your app](../../streamlit/app-development/editing-your-app.md)
    - Migrations and upgrades

      - [Identify your app type](../../streamlit/migrations-and-upgrades/overview.md)
      - [Migrate to a container runtime](../../streamlit/migrations-and-upgrades/runtime-migration.md)
      - [Migrate from ROOT\_LOCATION](../../streamlit/migrations-and-upgrades/root-location.md)
    - Features

      - [Git integration](../../streamlit/features/git-integration.md)
      - [External access](../../streamlit/features/external-access.md)
      - [Row access policies](../../streamlit/features/row-access.md)
      - [Sleep timer](../../streamlit/features/sleep-timer.md)
    - [Limitations and library changes](../../streamlit/limitations.md)
    - [Troubleshooting Streamlit in Snowflake](../../streamlit/troubleshooting.md)
    - [Release notes](../../../release-notes/streamlit-in-snowflake.md)
    - [Streamlit open-source library documentation](https://docs.streamlit.io/)
20. [Snowflake Native App Framework](../../native-apps/native-apps-about.md)
21. [Snowflake Declarative Sharing](../../declarative-sharing/about.md)
22. [Snowflake Native SDK for Connectors](../../native-apps/connector-sdk/about-connector-sdk.md)
23. External Integration
24. [External Functions](../../../sql-reference/external-functions.md)
25. [Kafka and Spark Connectors](../../../user-guide/connectors.md)
26. Snowflake Scripting
27. [Snowflake Scripting Developer Guide](../../snowflake-scripting/index.md)
28. Tools
29. [Snowflake CLI](../../snowflake-cli/index.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Snowpark API](../index.md)[Python](index.md)Creating a Session

# Creating a Session for Snowpark Python[¶](#creating-a-session-for-snowpark-python "Link to this heading")

To use Snowpark in your application, you need to create a session. For convenience in writing code, you can also import the names
of packages and objects.

## Creating a Session[¶](#creating-a-session "Link to this heading")

The first step in using the library is establishing a session with the Snowflake database.

Import the Session class.

```
from snowflake.snowpark import Session
```

Copy

To authenticate, you use the same mechanisms that the [Snowflake Connector for Python](../../python-connector/python-connector-example) supports.

Establish a session with a Snowflake database using the same parameters (for example, the account name, user name, etc.) that you use in the `connect` function in the Snowflake
Connector for Python. For more information, see the [parameters for the connect function](../../python-connector/python-connector-api.html#label-snowflake-connector-methods) in the Python Connector API documentation.

## Connect by using the `connections.toml` file[¶](#connect-by-using-the-connections-toml-file "Link to this heading")

To add credentials in a connections configuration file:

1. In a text editor, open the `connections.toml` file for editing. For example, to open the file in the Linux **vi** editor:

   ```
   vi connections.toml
   ```

   Copy
2. Add a new Snowflake connection definition.

   You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
   [Configuring a client, driver, library, or third-party application to connect to Snowflake](../../../user-guide/gen-conn-config).

   For example, to add a Snowflake connection called `myconnection` with the account `myaccount`,
   user `johndoe`, and password credentials, as well as database information,
   add the following lines to the configuration file:

   ```
   [myconnection]
   account = "myaccount"
   user = "jdoe"
   password = "******"
   warehouse = "my-wh"
   database = "my_db"
   schema = "my_schema"
   ```

   Copy

   Connection definitions support the same configuration options available in the
   [snowflake.connector.connect](../../python-connector/python-connector-api.html#label-snowflake-connector-methods-connect) method.
3. Optional: Add more connections, as shown:

   ```
   [myconnection_test]
   account = "myaccount"
   user = "jdoe-test"
   password = "******"
   warehouse = "my-test_wh"
   database = "my_test_db"
   schema = "my_schema"
   ```

   Copy
4. Save changes to the file.
5. In your Python code, supply connection name to `snowflake.connector.connect` and then add it to `session`, similar to the following:

   ```
   session = Session.builder.config("connection_name", "myconnection").create()
   ```

   Copy

For more information, see [configuration file](../../python-connector/python-connector-connect.html#label-python-connection-toml).

## Connect by specifying connection parameters[¶](#connect-by-specifying-connection-parameters "Link to this heading")

Construct a dictionary (`dict`) containing the names and values of these parameters
(e.g. `account`, `user`, `role`, `warehouse`, `database`, `schema`, etc.).

To create the session:

1. Create a Python dictionary (`dict`) containing the names and values of the parameters for connecting to Snowflake.
2. Pass this dictionary to the `Session.builder.configs` method to return a builder object that has these connection parameters.
3. Call the `create` method of the `builder` to establish the session.

The following example uses a `dict` containing connection parameters to create a new session:

```
connection_parameters = {
  "account": "<your snowflake account>",
  "user": "<your snowflake user>",
  "password": "<your snowflake password>",
  "role": "<your snowflake role>",  # optional
  "warehouse": "<your snowflake warehouse>",  # optional
  "database": "<your snowflake database>",  # optional
  "schema": "<your snowflake schema>",  # optional
}

new_session = Session.builder.configs(connection_parameters).create()
```

Copy

For the `account` parameter, use your [account identifier](../../../user-guide/admin-account-identifier).
Note that the account identifier does not include the snowflakecomputing.com suffix.

Note

This example shows you one way to create a session but there are several other ways that you can connect, including:
the default authenticator, single sign-on (SSO), multi-factor authentication (MFA), key pair authentication,
using a proxy server, and OAuth. For more information, see [Connecting to Snowflake with the Python Connector](../../python-connector/python-connector-connect).

## Using single sign-on (SSO) through a web browser[¶](#using-single-sign-on-sso-through-a-web-browser "Link to this heading")

If you have [configured Snowflake to use single sign-on (SSO)](../../../user-guide/admin-security-fed-auth-overview), you can configure
your client application to use browser-based SSO for authentication.

Construct a dictionary (`dict`) containing the names and values of these parameters
(e.g. `account`, `user`, `role`, `warehouse`, `database`, `authenticator`, etc.).

To create the session:

1. Create a Python dictionary (`dict`) containing the names and values of the parameters for connecting to Snowflake.
2. Pass this dictionary to the `Session.builder.configs` method to return a builder object that has these connection parameters.
3. Call the `create` method of the `builder` to establish the session.

The following example uses a `dict` containing connection parameters to create a new session. Set the `authenticator` option to `externalbrowser`.

```
from snowflake.snowpark import Session
connection_parameters = {
  "account": "<your snowflake account>",
  "user": "<your snowflake user>",
  "role":"<your snowflake role>",
  "database":"<your snowflake database>",
  "schema":"<your snowflake schema",
  "warehouse":"<your snowflake warehouse>",
  "authenticator":"externalbrowser"
}
session = Session.builder.configs(connection_parameters).create()
```

Copy

## Closing a Session[¶](#closing-a-session "Link to this heading")

If you no longer need to use a session for executing queries and you want to
cancel any queries that are currently running, call the close method of the Session object.
For example:

```
new_session.close()
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

1. [Creating a Session](#creating-a-session)
2. [Connect by using the connections.toml file](#connect-by-using-the-connections-toml-file)
3. [Connect by specifying connection parameters](#connect-by-specifying-connection-parameters)
4. [Using single sign-on (SSO) through a web browser](#using-single-sign-on-sso-through-a-web-browser)
5. [Closing a Session](#closing-a-session)