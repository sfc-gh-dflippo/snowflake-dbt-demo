---
auto_generated: true
description: Stages can be used to import third-party packages. You can also specify
  Anaconda packages to install when you create Python UDFs.
last_scraped: '2026-01-14T16:54:58.203648+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html
title: Using third-party packages | Snowflake Documentation
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

    * [Function or procedure?](../../stored-procedures-vs-udfs.md)
    * [Guidelines](../../udf-stored-procedure-guidelines.md)
    * [Stored procedures](../../stored-procedure/stored-procedures-overview.md)
    * [User-defined functions](../udf-overview.md)

      + [Privileges](../udf-access-control.md)
      + [Creating](../udf-creating-sql.md)
      + [Executing](../udf-calling-sql.md)
      + [Viewing in Snowsight](../../../user-guide/ui-snowsight-data-databases-function.md)
      + Handler writing
      + [Java](../java/udf-java-introduction.md)
      + [Javascript](../javascript/udf-javascript-introduction.md)
      + [Python](udf-python-introduction.md)

        - [Limitations](udf-python-limitations.md)
        - [Designing](udf-python-designing.md)
        - [Creating](udf-python-creating.md)
        - [Table functions](udf-python-tabular-functions.md)
        - [Vectorized UDFs](udf-python-batch.md)
        - [Vectorized UDTFs](udf-python-tabular-vectorized.md)
        - [Aggregate functions](udf-python-aggregate-functions.md)
        - [Using third-party packages](udf-python-packages.md)
        - [Packages policies](packages-policy.md)
        - [Examples](udf-python-examples.md)
        - [Troubleshooting](udf-python-troubleshooting.md)
      + [Scala](../scala/udf-scala-introduction.md)
      + [SQL](../sql/udf-sql-introduction.md)
    * [Packaging handler code](../../udf-stored-procedure-building.md)
    * [External network access](../../external-network-access/external-network-access-overview.md)
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

[Developer](../../../developer.md)[Functions and procedures](../../extensibility.md)[User-defined functions](../udf-overview.md)[Python](udf-python-introduction.md)Using third-party packages

# Using third-party packages[¶](#using-third-party-packages "Link to this heading")

Stages can be used to import third-party packages. You can also specify Anaconda packages to install when you create Python UDFs.

## Artifact Repository overview[¶](#artifact-repository-overview "Link to this heading")

With Artifact Repository, you can directly use Python packages from the Python Package Index ([PyPI](https://pypi.org/)) within Snowpark Python user-defined functions (UDFs) and stored procedures so that building and scaling Python-powered applications in Snowflake is easier.

### Get started[¶](#get-started "Link to this heading")

Use Snowflake’s default Artifact Repository (`snowflake.snowpark.pypi_shared_repository`) to connect and install PyPI packages within Snowpark UDFs and procedures.

Before you use this repository, the account administrator (a user who has been granted the ACCOUNTADMIN role) must grant the SNOWFLAKE.PYPI\_REPOSITORY\_USER database role to your role:

```
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE some_user_role;
```

Copy

The account administrator may also grant this database role to all users in the account:

```
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE PUBLIC;
```

Copy

With this role, you can install the package from the repository. When you create the UDF, you set the `ARTIFACT_REPOSITORY` parameter to the artifact repository name.
You also set the `PACKAGES` parameter to the list of the names of the packages that will come from artifact repository. In the following example, because the artifact repository is configured with PyPI, the package `scikit-learn` is sourced from PyPI:

```
CREATE OR REPLACE FUNCTION sklearn_udf()
  RETURNS FLOAT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
  PACKAGES = ('scikit-learn')
  HANDLER = 'udf'
  AS
$$
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def udf():
  X, y = load_iris(return_X_y=True)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

  model = RandomForestClassifier()
  model.fit(X_train, y_train)
  return model.score(X_test, y_test)
$$;

SELECT sklearn_udf();
```

Copy

Note

To specify a package version, add it as shown:

```
PACKAGES = ('scikit-learn==1.5')
```

Copy

### Packages built only for x86[¶](#packages-built-only-for-x86 "Link to this heading")

If a package is built only for x86, choose one of the warehouses that uses x86 CPU architecture — `MEMORY_1X_x86` or `MEMORY_16X_x86` — and then specify `RESOURCE_CONSTRAINT=(architecture='x86')`, as in the following example:

```
CREATE OR REPLACE FUNCTION pymeos_example()
RETURNS STRING
LANGUAGE PYTHON
HANDLER='main'
RUNTIME_VERSION='3.11'
ARTIFACT_REPOSITORY=snowflake.snowpark.pypi_shared_repository
PACKAGES=('pymeos') -- dependency pymeos-cffi is x86 only
RESOURCE_CONSTRAINT=(architecture='x86')
AS $$
def main() -> str:
   from pymeos import pymeos_initialize, pymeos_finalize, TGeogPointInst, TGeogPointSeq

   # Always initialize MEOS library
   pymeos_initialize()

   sequence_from_string = TGeogPointSeq(
      string='[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

   sequence_from_points = TGeogPointSeq(instant_list=[TGeogPointInst(string='Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst(string='Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst(string='Point(10.0 10.0)@2019-09-03 00:00:00+01')],
          lower_inc=True, upper_inc=True)
   speed = sequence_from_points.speed()

   # Call finish at the end of your code
   pymeos_finalize()

   return speed
$$;

SELECT pymeos_example();
```

Copy

For more information, see [Snowpark-optimized warehouses](../../../user-guide/warehouses-snowpark-optimized).

You can use Artifact Repository with UDF and Stored Procedure client APIs such as the following:

* [snowflake.snowpark.udf.UDFRegistration](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.udf.UDFRegistration)
* [snowflake.snowpark.functions.sproc](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.sproc)

When using them, specify the following parameters:

> * `ARTIFACT_REPOSITORY`
> * `PACKAGES`

and provide the package name in the `PACKAGES` field.

See the following example:

> ```
> ...
> ARTIFACT_REPOSITORY="snowflake.snowpark.pypi_shared_repository",
> PACKAGES=["urllib3", "requests"],
> ...
> ```
>
> Copy

### Troubleshooting[¶](#troubleshooting "Link to this heading")

If the package install fails for the function or procedure creation part, run the following pip command locally to see whether the package specification is valid:

```
pip install <package name> --only-binary=:all: --python-version 3.12 –platform <platform_tag>
```

Copy

### Limitations[¶](#limitations "Link to this heading")

* Access to private repositories is not supported.
* You cannot use this feature directly in Notebooks. However, you can use a UDF or stored procedure that uses PyPI packages within a notebook.
* You cannot use Artifact Repository within anonymous stored procedures.

Note

* Snowflake does not check or curate the security of Python packages from external sources. You are responsible for evaluating these packages and ensuring that they are safe and reliable.
* Snowflake reserves the right to block or remove any package that may be harmful or risky, without prior notice. This is to protect the platform’s integrity.

## Importing packages through a Snowflake stage[¶](#importing-packages-through-a-snowflake-stage "Link to this heading")

Snowflake stages can be used to import packages. You can bring in any Python code that follows guidelines defined in [General limitations](udf-python-limitations.html#label-limitations-on-python-udfs).
For more information, see [Creating a Python UDF with code uploaded from a stage](udf-python-creating.html#label-udf-python-stage).

You can only upload pure Python packages or packages with native code through a Snowflake stage.

As an example, you can use the following SQL, which creates a warehouse named `so_warehouse` that has x86 CPU architecture:

```
CREATE WAREHOUSE so_warehouse WITH
   WAREHOUSE_SIZE = 'LARGE'
   WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
   RESOURCE_CONSTRAINT = 'MEMORY_16X_X86';
```

Copy

To install a package with native code via importing from Stage, use the following example:

```
CREATE or REPLACE function native_module_test_zip()
  RETURNS string
  LANGUAGE python
  RUNTIME_VERSION=3.12
  RESOURCE_CONSTRAINT=(architecture='x86')
  IMPORTS=('@mystage/mycustompackage.zip')
  HANDLER='compute'
  as
  $$
  def compute():
      import mycustompackage
      return mycustompackage.mycustompackage()
  $$;
```

Copy

## Using third-party packages from Anaconda[¶](#using-third-party-packages-from-anaconda "Link to this heading")

Snowflake provides access to a curated set of Python packages built by Anaconda. These packages integrate directly into Snowflake’s Python features at no extra cost.

### Licensing terms[¶](#licensing-terms "Link to this heading")

* **In Snowflake:** Governed by your existing Snowflake customer agreement, including the Anaconda usage restrictions described in this documentation. No separate Anaconda terms apply for in-Snowflake use.
* **Local development:** From Snowflake’s [dedicated Anaconda repository](https://repo.anaconda.com/pkgs/snowflake/) : Subject to Anaconda’s Embedded End Customer Terms and Anaconda’s Terms of Service posted on the repository. Local use is limited to developing/testing workloads intended for deployment in Snowflake.

### User guidelines[¶](#user-guidelines "Link to this heading")

#### Permitted uses[¶](#permitted-uses "Link to this heading")

* **Within Snowflake:** Use packages freely across all supported Python features.

  > Note
  >
  > You cannot call a UDF within the DEFAULT clause of a CREATE TABLE statement, with the exception of packages that remain freely available in Snowflake Notebooks on Snowpark Container Services.
* **Local development:** Use packages from Snowflake’s dedicated Anaconda repository to develop or test workloads intended for Snowflake.

#### Prohibited uses[¶](#prohibited-uses "Link to this heading")

The following uses of packages are prohibited:

* Using packages for projects not related to Snowflake.
* Hosting or mirroring package content externally.
* Removing or modifying copyright or license notices.

### Finding and managing packages[¶](#finding-and-managing-packages "Link to this heading")

Can’t find a package you need?

* Submit requests via the [Snowflake Ideas forum](https://community.snowflake.com/s/ideas).
* Pure Python packages (without compiled extensions) can be [uploaded directly to a Snowflake stage](../../snowflake-cli/snowpark/upload).

### Support and security[¶](#support-and-security "Link to this heading")

#### Support coverage[¶](#support-coverage "Link to this heading")

Snowflake provides standard package support, including:

* Installation guidance
* Environment troubleshooting
* Integration assistance

#### Warranty and SLA[¶](#warranty-and-sla "Link to this heading")

Anaconda packages are third-party software provided *as-is* and are not covered by Snowflake’s warranty or SLA (Service-level agreement).

#### Security practices[¶](#security-practices "Link to this heading")

Anaconda packages provided by Snowflake are built on trusted infrastructure and digitally signed.

For more details, see [Anaconda’s Security Practices](https://www.anaconda.com/docs/reference/policies-practices/security) .

#### Compliance and licensing[¶](#compliance-and-licensing "Link to this heading")

Each package includes its own open-source license. Customers must comply with individual package license terms in addition to the usage guidelines outlined in this documentation.

#### Frequently asked questions[¶](#frequently-asked-questions "Link to this heading")

* **Can I use packages from other Anaconda channels (e.g., conda-forge or Anaconda Defaults)?** No. Other channels are separate offerings and may require a commercial license from Anaconda.
* **Can I use these packages locally for projects unrelated to Snowflake?** No. Local usage is strictly limited to developing or testing workloads intended for Snowflake deployment. Other uses require a separate Anaconda license.
* **Why does Snowpark Container Services require separate licensing?** Using packages in custom Docker images extends beyond Snowflake’s integrated environment, necessitating separate Anaconda licensing.

### Displaying and using packages[¶](#displaying-and-using-packages "Link to this heading")

#### Displaying available packages[¶](#displaying-available-packages "Link to this heading")

You can display all packages available and their version information by querying the PACKAGES view in the Information Schema.

```
select * from information_schema.packages where language = 'python';
```

Copy

To display version information about a specific package, for example `numpy`, use this command:

```
select * from information_schema.packages where (package_name = 'numpy' and language = 'python');
```

Copy

Note

Some packages in the Anaconda Snowflake channel are not intended for use inside Snowflake UDFs because UDFs are executed within a restricted engine.
For more information, see [Following good security practices](udf-python-designing.html#label-udf-python-security).

When queries that call Python UDFs are executed inside a Snowflake warehouse, Anaconda packages are installed seamlessly and cached on the virtual warehouse on your behalf.

#### Displaying imported packages[¶](#displaying-imported-packages "Link to this heading")

You can display a list of the packages and modules a UDF or UDTF is using by executing the [DESCRIBE FUNCTION](../../../sql-reference/sql/desc-function) command.
Executing the DESCRIBE FUNCTION command for a UDF whose handler is implemented in Python returns the values of several properties, including a list of imported modules and packages,
as well as installed packages, the function signature, and its return type.

When specifying the identifier for the UDF, be sure to include function parameter types, if any.

```
desc function stock_sale_average(varchar, number, number);
```

Copy

#### Using Anaconda packages[¶](#using-anaconda-packages "Link to this heading")

For an example of how to use an imported Anaconda package in a Python UDF,
refer to [Importing a package in an in-line handler](udf-python-examples.html#label-udf-python-in-line-examples).

#### Setting packages policies[¶](#setting-packages-policies "Link to this heading")

You can use a packages policy to set allowlists and blocklists for third-party Python packages from Anaconda at the account level.
This lets you meet stricter auditing and security requirements and gives you more fine-grained control over which packages are available or blocked in your environment.
For more information, see [Packages policies](packages-policy).

### Performance on cold warehouses[¶](#performance-on-cold-warehouses "Link to this heading")

For more efficient resource management, newly provisioned virtual warehouses do not preinstall Anaconda packages.
Instead, Anaconda packages are installed on-demand the first time a UDF is used.
The packages are cached for future UDF execution on the same warehouse. The cache is dropped when the warehouse is suspended.
This may result in slower performance the first time a UDF is used or after the warehouse is resumed.
The additional latency could be approximately 30 seconds.

## Local development and testing[¶](#local-development-and-testing "Link to this heading")

To help you create a conda environment on your local machine for development and testing, Anaconda has
created a Snowflake channel which mirrors a subset of the packages and versions that are supported in
the Snowflake Python UDF environment.
You may use the Snowflake conda channel for local testing and development at no cost under the Supplemental Embedded Software
Terms to Anaconda’s Terms of Service.

For example, to create a new conda environment locally using the Snowflake channel, type something like
this on the command line:

```
conda create --name py312_env -c https://repo.anaconda.com/pkgs/snowflake python=3.12 numpy pandas
```

Copy

Note that because of platform differences, your local conda environment may not be exactly the same as
the server environment.

## Best practices[¶](#best-practices "Link to this heading")

Within the `create function` statement, the package specification (for example, `packages = ('numpy','pandas')`) should
only specify the top-level packages that the UDF is using directly.
Anaconda performs dependency management of packages and will install the required dependencies automatically. Because of this,
you should not specify dependency packages.

Anaconda will install the most up-to-date version of the package and its dependencies if you don’t specify a package version.
Generally, it isn’t necessary to specify a particular package version.
Note that version resolution is performed once, when the UDF is created using the `create function` command.
After that, the resulting version resolution is frozen and the same set of packages will be used when this particular UDF executes.

For an example of how to use the package specification within the `create function` statement, see [Importing a package in an in-line handler](udf-python-examples.html#label-udf-python-in-line-examples).

## Known issues with third-party packages[¶](#known-issues-with-third-party-packages "Link to this heading")

### Performance with single row prediction[¶](#performance-with-single-row-prediction "Link to this heading")

Some data science frameworks, such as Scikit-learn and TensorFlow, might be slow when doing single-row ML prediction.
To improve performance, do batch prediction instead of single-row prediction.
To do this, you can use vectorized Python UDFs, with which you can define Python functions that receive input rows in batches, on which machine
learning or data science libraries are optimized to operate. For more information, see [Vectorized Python UDFs](udf-python-batch).

### Downloading data on demand from data science libraries[¶](#downloading-data-on-demand-from-data-science-libraries "Link to this heading")

Some data science libraries, such as [NLTK](https://www.nltk.org/data.html), [Keras](https://www.tensorflow.org/api_docs/python/tf/keras/datasets),
and [spaCy](https://spacy.io) provide functionality to download additional corpora, data, or models on demand.

However, on-demand downloading does not work with Python UDFs due to Snowflake security constraints, which disable some
capabilities, such as network access and writing to files.

To work around this issue, download the data to your local environment and then provide it
to the UDF via a Snowflake stage.

### XGBoost[¶](#xgboost "Link to this heading")

When using XGBoost in UDF or UDTF for parallel prediction or training, the concurrency for each XGBoost instance should
be set to 1. This ensures that XGBoost is configured for optimal performance when executing in
the Snowflake environment.

Examples:

```
import xgboost as xgb
model = xgb.Booster()
model.set_param('nthread', 1)
model.load_model(...)
```

Copy

```
import xgboost as xgb
model = xgb.XGBRegressor(n_jobs=1)
```

Copy

### TensorFlow/Keras[¶](#tensorflow-keras "Link to this heading")

When using Tensorflow/Keras for prediction, use Model.predict\_on\_batch and
not Model.predict.

Example:

```
import keras
model = keras.models.load_model(...)
model.predict_on_batch(np.array([input]))
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

1. [Artifact Repository overview](#artifact-repository-overview)
2. [Importing packages through a Snowflake stage](#importing-packages-through-a-snowflake-stage)
3. [Using third-party packages from Anaconda](#using-third-party-packages-from-anaconda)
4. [Local development and testing](#local-development-and-testing)
5. [Best practices](#best-practices)
6. [Known issues with third-party packages](#known-issues-with-third-party-packages)