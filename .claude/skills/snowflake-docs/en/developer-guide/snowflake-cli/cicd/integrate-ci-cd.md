---
auto_generated: true
description: Snowflake CLI integrates popular CI/CD (continuous integration and continuous
  delivery) systems and frameworks, such as GitHub Actions, to efficiently automate
  your Snowflake workflows for SQL, Snowpa
last_scraped: '2026-01-14T16:57:48.456508+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowflake-cli/cicd/integrate-ci-cd
title: Integrating CI/CD with Snowflake CLI | Snowflake Documentation
---

1. [Overview](../../../developer.md)
2. Builders
3. [Snowflake DevOps](../../builders/devops.md)
4. [Observability](../../builders/observability.md)
5. Snowpark Library
6. [Snowpark API](../../snowpark/index.md)
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
29. [Snowflake CLI](../index.md)

    * [Introduction](../introduction/introduction.md)
    * [Installing Snowflake CLI](../installation/installation.md)
    * [Configuring Snowflake CLI and connecting to Snowflake](../connecting/connect.md)
    * [Bootstrapping a project from a template](../bootstrap-project/bootstrap.md)
    * [Project definition files](../project-definitions/about.md)
    * [Managing Snowflake objects](../objects/manage-objects.md)
    * [Managing Snowflake stages](../stages/manage-stages.md)
    * [Managing Container Services](../services/overview.md)
    * [Using Snowpark APIs](../snowpark/overview.md)
    * [Working with notebooks](../notebooks/use-notebooks.md)
    * [Working with Streamlit in Snowflake](../streamlit-apps/overview.md)
    * [Using Snowflake Native Apps](../native-apps/overview.md)
    * [Executing SQL](../sql/execute-sql.md)
    * [Managing Snowflake Git repositories](../git/overview.md)
    * [Managing data pipelines](../data-pipelines/data-pipelines.md)
    * [Integrating CI/CD with Snowflake CLI](integrate-ci-cd.md)
    * [Migrating from SnowSQL](../../../user-guide/snowsql-migrate.md)
    * [Command reference](../command-reference/overview.md)
30. [Git](../../git/git-overview.md)
31. Drivers
32. [Overview](../../drivers.md)
33. [Considerations when drivers reuse sessions](../../driver-connections.md)
34. [Scala versions](../../scala-version-differences.md)
35. Reference
36. [API Reference](../../../api-reference.md)

[Developer](../../../developer.md)[Snowflake CLI](../index.md)Integrating CI/CD with Snowflake CLI

# Integrating CI/CD with Snowflake CLI[¶](#integrating-ci-cd-with-sf-cli "Link to this heading")

Snowflake CLI integrates popular CI/CD (continuous integration and continuous delivery) systems and frameworks, such as [GitHub Actions](https://github.com/features/actions), to efficiently automate your Snowflake workflows for SQL, Snowpark, Native Apps, or Notebooks.

The following illustration shows a typical CI/CD workflow in Snowflake CLI.

![Snowflake CI/CD workflow](../../../_images/cli-cicd-devops-flow.png)

## CI/CD workflow steps[¶](#ci-cd-workflow-steps "Link to this heading")

1. **Store:** Configure a remote Git repository to manage your Snowflake files securely.
2. **Code:** Develop your Snowflake code using an IDE or Snowsight, tailored to your preferences.
3. **Install:** [Install](../installation/installation) Snowflake CLI, and provision your preferred CI/CD provider, such as GitHub Actions.
4. **Deploy:** Automate deployment by combining the Snowflake CLI with your selected CI/CD tool.
5. **Monitor:** Track code and workflow performance in Snowflake using [Snowflake Trail](https://www.snowflake.com/en/product/features/snowflake-trail/) for real-time insights.
6. **Iterate:** Apply small, frequent updates to your project for continuous improvement; smaller changes simplify management and rollback, if necessary.

## CI/CD with GitHub Actions[¶](#ci-cd-with-github-actions "Link to this heading")

A Snowflake CLI action is a GitHub action designed to integrate Snowflake CLI into CI/CD pipelines. You can use it to automate execution of Snowflake CLI commands within your GitHub workflows. For more information, see the [snowflake-cli-action](https://github.com/snowflakedb/snowflake-cli-action) repository.

## Using Snowflake CLI actions[¶](#using-sf-cli-actions "Link to this heading")

Github Actions streamlines the process of installing and using Snowflake CLI in your CI/CD workflows. The CLI is installed in an
isolated way, ensuring that it won’t conflict with the dependencies of your project. It automatically sets up
the input configuration file within the `~/.snowflake/` directory.

The action enables automation of your Snowflake CLI tasks, such as deploying Snowflake Native Apps or running Snowpark scripts within your Snowflake environment.

### Input parameters[¶](#input-parameters "Link to this heading")

A Snowflake CLI action uses the following inputs from your Github workflow YAML file, such as `<repo-name>/.github/workflows/my-workflow.yaml`:

* `cli-version`: The specified Snowflake CLI version, such as `3.11.0`. If not provided, the latest version of the Snowflake CLI is used.
* `custom-github-ref`: The branch, tag, or commit in the Github repository that you want to install Snowflake CLI directly from.

  Note

  You cannot use both `cli-version` and `custom-github-ref` together; specify only one of these parameters.
* `default-config-file-path`: Path to the configuration file (`config.toml`) in your repository. The path must be relative to the root of the repository. The configuration file is not required when a temporary connection (`-x` option) is used. For more information, see [Managing Snowflake connections](../connecting/configure-connections).
* `use-oidc`: Boolean flag to enable OIDC authentication. When set to `true`, the action configures the CLI to use GitHub’s OIDC token for authentication with Snowflake, eliminating the need for storing private keys as secrets. Default is `false`.

### Install Snowflake CLI from a GitHub branch or tag[¶](#install-sf-cli-from-a-github-branch-or-tag "Link to this heading")

* To install Snowflake CLI from a specific branch, tag, or commit in the GitHub repository (for example, to test unreleased features or a fork), use the following configuration:

```
- uses: snowflakedb/snowflake-cli-action@v2.0
  with:
    custom-github-ref: "feature/my-branch" # or a tag/commit hash
```

Copy

You can also include other [input parameters](#label-cli-cicd-inputs).

This feature is available in snowflake-cli-action version 1.6 or later.

### Safely configure the action in your CI/CD workflow[¶](#safely-configure-the-action-in-your-ci-cd-workflow "Link to this heading")

You can safely configure the action in your CI/CD workflow by using either of the following methods:

* [Use workload identity federation (WIF) OpenID Connect (OIDC) authentication](#label-cli-github-actions-oidc-auth)
* [Use private key authentication](#label-cli-github-actions-private-key-auth)

#### Use workload identity federation (WIF) OpenID Connect (OIDC) authentication[¶](#use-workload-identity-federation-wif-openid-connect-oidc-authentication "Link to this heading")

Note

WIF OIDC authentication requires Snowflake CLI version 3.11.0 or later.

WIF OIDC authentication provides a secure and modern way to authenticate with Snowflake without storing private keys as secrets. This approach uses GitHub’s OIDC (OpenID Connect) token to authenticate with Snowflake.

To set up WIF OIDC authentication, follow these steps:

1. Configure WIF OIDC by setting up a service user with the OIDC workload identity type:

   ```
   CREATE USER <username>
   TYPE = SERVICE
   WORKLOAD_IDENTITY = (
     TYPE = OIDC
     ISSUER = 'https://token.actions.githubusercontent.com'
     SUBJECT = '<your_subject>'
   )
   ```

   Copy

Note

> By default, your subject should look like `repo:<repository-owner/repository-name>:environment:<environment>`.

* To simplify generation of the subject, use `gh` command, where `<environment_name>` is the environment defined in your repository settings, as shown in the following example:

> ```
> gh repo view <repository-owner/repository-name> --json nameWithOwner | jq -r '"repo:\(.nameWithOwner):environment:<environment_name>"'
> ```
>
> Copy
>
> For more information about customizing your subject, see the [OpenID Connect](https://docs.github.com/en/actions/reference/security/oidc) reference on GitHub.

1. Store your Snowflake account identifier in GitHub secrets. For more information, see [GitHub Actions documentation](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository).
2. Configure the Snowflake CLI action in your GitHub workflow YAML file, as shown:

   ```
   name: Snowflake OIDC
   on: [push]

   permissions:
     id-token: write  # Required for OIDC token generation
     contents: read

   jobs:
     oidc-job:
       runs-on: ubuntu-latest
       environment: test-env # this should match the environment used in the subject
       steps:
         - uses: actions/checkout@v4
           with:
             persist-credentials: false
         - name: Set up Snowflake CLI
           uses: snowflakedb/snowflake-cli-action@v2.0
           with:
             use-oidc: true
             cli-version: "3.11"
         - name: test connection
           env:
             SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
           run: snow connection test -x
   ```

   Copy

   For more information about setting up WIF OIDC authentication for your Snowflake account and configuring the GitHub OIDC provider, see [Workload identity federation](../../../user-guide/workload-identity-federation).

#### Use private key authentication[¶](#use-private-key-authentication "Link to this heading")

To use private key authentication, you need to store your Snowflake private key in GitHub secrets and configure the Snowflake CLI action to use it.

1. Store your Snowflake private key in GitHub secrets.

For more information, see [GitHub Actions documentation](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository).

2. Configure the Snowflake CLI action in your GitHub workflow YAML file, as shown:

   ```
   name: Snowflake Private Key
   on: [push]

   jobs:
     private-key-job:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             persist-credentials: false
         - name: Set up Snowflake CLI
           uses: snowflakedb/snowflake-cli-action@v2.0
   ```

   Copy

## Defining connections[¶](#defining-connections "Link to this heading")

You can define a GitHub action to connect to Snowflake with a temporary connection or with a connection defined in your configuration file. For more information about managing connections, see [Managing Snowflake connections](../connecting/configure-connections).

### Use a temporary connection[¶](#use-a-temporary-connection "Link to this heading")

For more information about temporary connections, see [Use a temporary connection](../connecting/configure-connections.html#label-snowcli-temporary-connection).

To set up your Snowflake credentials for a temporary connection, follow these steps:

1. Map secrets to environment variables in your GitHub workflow, in the form `SNOWFLAKE_<key>=<value>`, as shown:

   ```
   env:
     SNOWFLAKE_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
     SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
   ```

   Copy
2. Configure the Snowflake CLI action.

   If you use the latest version of Snowflake CLI, you do not need to include the `cli-version` parameter. The following example instructs the action to use Snowflake CLI version 3.11.0 specifically:

   ```
   - uses: snowflakedb/snowflake-cli-action@v2.0
     with:
       cli-version: "3.11.0"
   ```

   Copy
3. Optional: If your private key is encrypted, to set up a passphrase, set the PRIVATE\_KEY\_PASSPHRASE environment variable to the private key passphrase. Snowflake uses this passphrase to decrypt the private key. For example:

   ```
   - name: Execute Snowflake CLI command
     env:
       PRIVATE_KEY_PASSPHRASE: ${{ secrets.PASSPHARSE }}
   ```

   Copy

   To use a password instead of a private key, unset the `SNOWFLAKE_AUTHENTICATOR` environment variable, and add the `SNOWFLAKE_PASSWORD` variable, as follows:

   ```
   - name: Execute Snowflake CLI command
     env:
       SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
       SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
       SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
   ```

   Copy

   Note

   To enhance your experience when using a password and MFA, Snowflake recommends that you [configure MFA caching](../connecting/configure-connections.html#label-snowcli-mfa-caching).

   For more information about setting Snowflake credentials in environment variables, see [Use environment variables for Snowflake credentials](../connecting/configure-connections.html#label-snowcli-environment-creds), and for information about defining environment variables within your GitHub CI/CD workflow, see [Defining environment variables for a single workflow](https://docs.github.com/en/actions/learn-github-actions/variables#defining-environment-variables-for-a-single-workflow).
4. Add the `snow` commands you want to execute with the temporary connection, as shown:

   ```
   run: |
     snow --version
     snow connection test --temporary-connection
   ```

   Copy

The following example shows a completed sample `<repo-name>/.github/workflows/my-workflow.yaml` file:

```
name: deploy
on: [push]

jobs:
  version:
    name: "Check Snowflake CLI version"
    runs-on: ubuntu-latest
    steps:
      # Snowflake CLI installation
      - uses: snowflakedb/snowflake-cli-action@v2.0

        # Use the CLI
      - name: Execute Snowflake CLI command
        env:
          SNOWFLAKE_AUTHENTICATOR: SNOWFLAKE_JWT
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
          PRIVATE_KEY_PASSPHRASE: ${{ secrets.PASSPHARSE }} # Passphrase is only necessary if private key is encrypted.
        run: |
          snow --help
          snow connection test -x
```

Copy

After verifying that your action can connect to Snowflake successfully, you can add more Snowflake CLI commands like `snow notebook create` or `snow git execute`. For information about supported commands, see [Snowflake CLI command reference](../command-reference/overview).

### Use a configuration file[¶](#use-a-configuration-file "Link to this heading")

For more information about defining connections, see [Define connections](../connecting/configure-connections.html#label-snowcli-define-connections).

To set up your Snowflake credentials for a specific connection, follow these steps:

1. Create a `config.toml` file at the root of your Git repository with an empty configuration connection, as shown:

   ```
   default_connection_name = "myconnection"

   [connections.myconnection]
   ```

   Copy

   This file serves as a template and should not contain actual credentials.
2. Map secrets to environment variables in your GitHub workflow, in the form `SNOWFLAKE_<key>=<value>`, as shown:

   ```
   env:
     SNOWFLAKE_CONNECTIONS_MYCONNECTION_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
     SNOWFLAKE_CONNECTIONS_MYCONNECTION_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
   ```

   Copy
3. Configure the Snowflake CLI action.

   If you use the latest version of Snowflake CLI, you do not need to include the `cli-version` parameter. The following example specifies a desired version and the name of your default configuration file:

   ```
   - uses: snowflakedb/snowflake-cli-action@v2.0
     with:
       cli-version: "3.11.0"
       default-config-file-path: "config.toml"
   ```

   Copy
4. Optional: If your private key is encrypted, to set up a passphrase, set the PRIVATE\_KEY\_PASSPHRASE environment variable to the private key passphrase. Snowflake uses this passphrase to decrypt the private key. For example:

   ```
   - name: Execute Snowflake CLI command
     env:
       PRIVATE_KEY_PASSPHRASE: ${{ secrets.PASSPHARSE }}
   ```

   Copy

   To use a password instead of a private key, unset the `SNOWFLAKE_AUTHENTICATOR` environment variable, and add the `SNOWFLAKE_PASSWORD` variable, as follows:

   ```
   - name: Execute Snowflake CLI command
     env:
       SNOWFLAKE_CONNECTIONS_MYCONNECTION_USER: ${{ secrets.SNOWFLAKE_USER }}
       SNOWFLAKE_CONNECTIONS_MYCONNECTION_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
       SNOWFLAKE_CONNECTIONS_MYCONNECTION_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
   ```

   Copy

   Note

   To enhance your experience when using a password and MFA, Snowflake recommends that you [configure MFA caching](../connecting/configure-connections.html#label-snowcli-mfa-caching).
5. Add the `snow` commands you want to execute with a named connection, as shown:

   ```
   run: |
     snow --version
     snow connection test
   ```

   Copy

The following example shows a sample `config.toml` file in your Git repository and a completed sample `<repo-name>/.github/workflows/my-workflow.yaml` file:

* Sample `config.toml` file:

  ```
  default_connection_name = "myconnection"

  [connections.myconnection]
  ```

  Copy
* Sample Git workflow file:

  ```
  name: deploy
  on: [push]
  jobs:
    version:
      name: "Check Snowflake CLI version"
      runs-on: ubuntu-latest
      steps:
        # Checkout step is necessary if you want to use a config file from your repo
        - name: Checkout repo
          uses: actions/checkout@v4
          with:
            persist-credentials: false

          # Snowflake CLI installation
        - uses: snowflakedb/snowflake-cli-action@v2.0
          with:
            default-config-file-path: "config.toml"

          # Use the CLI
        - name: Execute Snowflake CLI command
          env:
            SNOWFLAKE_CONNECTIONS_MYCONNECTION_AUTHENTICATOR: SNOWFLAKE_JWT
            SNOWFLAKE_CONNECTIONS_MYCONNECTION_USER: ${{ secrets.SNOWFLAKE_USER }}
            SNOWFLAKE_CONNECTIONS_MYCONNECTION_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
            SNOWFLAKE_CONNECTIONS_MYCONNECTION_PRIVATE_KEY_RAW: ${{ secrets.SNOWFLAKE_PRIVATE_KEY_RAW }}
            PRIVATE_KEY_PASSPHRASE: ${{ secrets.PASSPHARSE }} #Passphrase is only necessary if private key is encrypted.
          run: |
            snow --help
            snow connection test
  ```

  Copy

After verifying that your action can connect to Snowflake successfully, you can add more Snowflake CLI commands like `snow notebook create` or `snow git execute`. For information about supported commands, see [Snowflake CLI command reference](../command-reference/overview).

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

1. [CI/CD workflow steps](#ci-cd-workflow-steps)
2. [CI/CD with GitHub Actions](#ci-cd-with-github-actions)
3. [Using Snowflake CLI actions](#using-sf-cli-actions)
4. [Defining connections](#defining-connections)

Related content

1. [Snowflake CLI](/developer-guide/snowflake-cli/cicd/../index)