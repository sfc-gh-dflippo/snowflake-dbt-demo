# dbt for Snowflake Demonstration Project

## How to get started

This project depends on the following two data sets

- SNOWFLAKE_SAMPLE_DATA that is available by default in all new Snowflake accounts
- [Cybersyn Financial & Economic Essentials](https://app.snowflake.com/marketplace/data-products/search?search=Cybersyn%20Financial%20%26%20Economic%20Essentials)
  - It is available for free in the Snowflake Data Markeplace
  - If named other than "CYBERSYN_FINANCIAL_ECONOMIC_ESSENTIALS", update the database name in sources.yml


## Installing dbt using Miniforge

- If you can install your own software, I generally recommend using [Miniforge](https://conda-forge.org/download/) to create an isolated Python environment just for dbt. Miniforge is completely open source, does not require a license like Anaconda or Miniconda, and uses the free Conda-Forge repository for packages. A dbt-conda-env.yml file has been provided so you can set up this environment and switch to it with the following commands. This is much simpler than some other flavors of Python.
    ```shell
    conda env create -f dbt-conda-env.yml
    conda activate dbt
    ```
- If you have SSL errors, you may need to install pip_system_certs into your base environment first. The dbt-conda-env.yml file already includes this for your child environment. The `--trusted-host` parameters below will allow you to bypass firewall issues.
    ```shell
    conda activate base
    python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    ```

## Installing dbt using any other flavor of Python - Windows

### Setting up Python and verifying which python you are now using:

- Install Python using your company's Self Service portal or install the [open source version of Python.org](https://www.python.org/downloads/)
- First you will want to see if you have the correct version of Python in your path using a Windows Command Prompt:
    ```shell
    where python
    python --version
    ```
- It should return a path like `C:\Program Files\Python311`. You can use Python 3.8 and higher. If you can't run `python --version` it is likely that you do not have the right version of python in your PATH.

### How to change your PATH

- If this is not the correct version of Python or the wrong location, you can update your PATH on Windows 10 & 11 using the following:
    1) Open Start Search, type “env”, and select “Edit the system environment variables”.
    2) Click the “Environment Variables…” button.
    3) In the “User Variables” section, locate “Path”, and click edit.
    4) In the “Edit environment variable” UI, click “New” to add the new path to your preferred version of Python.
    5) Use the "Move Up" button to make your new path the first entry
    6) Close and reopen any command prompts or VS Code to use the new PATH
    7) Use the `where python` and `python --version` commands again to verify that you are now using the correct version.

### Update pip and install dbt

- Next make sure pip is up to date and that pip_system_certs is also installed. The `--trusted-host` parameters below will help you avoid firewall issues.
    ```shell
    python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    ```
- Next install virtualenv and create a new virtual environment called `dbt`
    ```shell
    python -m pip install --user virtualenv
    python -m venv dbt
    ```
- Now you can activate your virtual environment, verify that the location of python has changed, and install dbt
    ```shell
    .\dbt\Scripts\activate
    where python
    python -m pip install -U dbt-core dbt-snowflake
    dbt --version
    ```

## Installing dbt using any other flavor of Python - Unix/macOS
- Install Python using your company's Self Service portal or install the [open source version of Python.org](https://www.python.org/downloads/)
- First you will want to see if you have the correct version of Python in your path using a shell:
    ```shell
    which python
    python --version
    ```
- You can use Python 3.8 and higher. If you can't run `python --version` it is likely that you do not have the right version of python in your PATH.
### How to change your PATH
- This command can be used to append your folder before the existing PATH. You may need to add this to your .bash_profile or other shell configuration file to make the change permanant.
    ```shell
    export PATH=/my/path/to/python/:$PATH
    ```
### Update pip and install dbt
- Next make sure pip is up to date and that pip_system_certs is also installed. The `--trusted-host` parameters below will help you avoid firewall issues.
    ```shell
    python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    ```
- Next install virtualenv and create a new virtual environment called `dbt`
    ```shell
    python -m pip install --user virtualenv
    python -m venv dbt
    ```
- Now you can activate your virtual environment, verify that the location of python has changed, and install dbt. We install/update pip and pip_system_certs this time in the virtual env.
    ```shell
    source dbt/bin/activate
    which python
    python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
    python -m pip install -U dbt-core dbt-snowflake
    dbt --version
    ```

## Creating a simple dbt sample project to test your connection to Snowflake
- The dbt init command can step you through creating a `~/.dbt/profiles.yml` file and starter project structure.
- Be aware that running this project will create a table and a view in the schema you specify.
- Also be aware that the sample project is designed to have a test fail when you first run `dbt build`. If you open the first model under /models/ you will see that it has a where clause you can uncomment to make the test pass.
    ```shell
    dbt init
    dbt compile
    dbt build
    ```

## Setting Up Your Editor

- Most dbt users edit their dbt scripts with Microsoft's free editor, VSCode
  - [Download VSCode](https://code.visualstudio.com/Download)
  - From the Extensions screen (icon looks like Tetris) you should install two extensions
    - ["Snowflake"](https://docs.snowflake.com/en/user-guide/vscode-ext)
    - ["dbt Power User"](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user) (which will also add "vscode-dbt")
  - In the Explorer, right click in the background and "Add folder to workspace" to add where your dbt project will be located.
  - On Windows, you will want to change the default terminal to "Command Prompt". Under *File* -> *Preferences* -> *Settings*, search for "windows terminal" and scroll down to where it says the default is "null" and change that to "Command Prompt".
  - You will want to set the default intepreter to your new "dbt" environment using [these instructions from Microsoft](https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter).

### Setting Up Your Snowflake Account for this sample project

- Create a target schema in Snowflake that you want to deploy your dbt demo into
- Add the Knoema Economy Data Atlas and Snowflake Sample Data to your account if necessary

### Update Configuration For Your Account and Test Execution

- Update your ~/.dbt/profiles.yml file with your credentials and target DB/schema. There is a sample profiles.yml file you can copy to your ~/.dbt/ folder and update if you don't already have one.
- From the root folder, run `dbt deps` to download modules from the dbt hub
- Run `dbt build --full-refresh` and troubleshoot any errors such as missing objects or permission issues

## Cheatsheet of most common dbt commands

- `dbt deps` - download 3rd party packages (necessary for this project before build)
- `dbt build` - both compile and then run all models & associated tests
- `dbt build --full-refresh` - have incremental models run as a full reload
- `dbt build --select modelname` - will only compile/run modelname
- `dbt build --select +modelname` - will compile/run modelname and all parents
- `dbt build --select modelname+` - will compile/run modelname and all children
- `dbt build --select +modelname+` - will compile/run modelname, and all parents and children
- `dbt build --select @modelname` - will compile/run modelname, all parents, all children, AND all parents of all children
- `dbt build --exclude modelname` - will compile/run all models except modelname
- `dbt compile` - compile all models but do not execute them
- `dbt run` - run all models & tests
- `dbt seed` - create or refresh small tables from .csv seed files
- `dbt clean` - clear your logs and compiled scripts (can fix issues)
- `dbt docs generate` - refresh the documentation for your project
- `dbt docs serve` - open this documentation in your browser

Additional commands and details are available in [dbt's documentation](https://docs.getdbt.com/reference/dbt-commands)

## Project features

- How to nest models:
  - DIM_ORDERS
  - DIM_CURRENT_YEAR_ORDERS
  - DIM_CURRENT_YEAR_OPEN_ORDERS
- Snowflake commands in a pre-hook:
  - DIM_CALENDAR_DAY
- Materializations:
  - LKP_EXCHANGE_RATES (table)
  - LKP_CUSTOMERS_WITH_ORDERS (ephemeral)
  - DIM_CUSTOMERS_SHARE (secure view)
  - FACT_ORDER_LINE (incremental fact)
  - DIM_CUSTOMERS, DIM__CUSTOMERS (incremental dim)
  - DIM_CUSTOMERS_TYPE2 (snapshot)
- Source data quality tests:
  - sources.yml
- Model data quality tests:
  - schema.yml
- Features available in dbt_project.yml
  - run-start/run-end hooks
  - logging before and after modules
  - default materializations by folder path
  - Snowflake features - copy_grants, secure views, warehouse
  - schemas for models
- Macro examples:
  - snowflake_surrogate_key
  - copy_log_to_snowflake
  - create_masking_policies
- Jinja expressions:
  - Q1_FACT_PRICING_SUMMARY_REPORT_QUERY
  - Q2_MINIMUM_COST_SUPPLIER_QUERY
  - Q3_SHIPPING_PRIORITY_QUERY
  - Q4_ORDER_PRIORITY_CHECKING_QUERY

## Resources

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Free [on-demand training](https://courses.getdbt.com/)
- [Additional Packages](https://hub.getdbt.com/)
- Create PK, UK, and FK in Snowflake using [dbt Constraints](https://github.com/Snowflake-Labs/dbt_constraints)
- Snowflake Guide - [Accelerating Data Teams with dbt Core & Snowflake](https://quickstarts.snowflake.com/guide/data_teams_with_dbt_core/index.html)
- Snowflake Guide - [Accelerating Data Teams with dbt Cloud & Snowflake](https://quickstarts.snowflake.com/guide/data_teams_with_dbt_cloud/index.html)
- Snowflake Guide - [Data Engineering with Apache Airflow, Snowflake & dbt](https://quickstarts.snowflake.com/guide/data_engineering_with_apache_airflow/index.html)
