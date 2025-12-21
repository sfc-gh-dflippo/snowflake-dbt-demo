# dbt Setup Guide

## 📚 Documentation Navigation

| Document                                           | Description                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------ |
| **[README.md](README.md)**                         | Project overview, architecture, and feature matrix                 |
| **[DBT_SETUP_GUIDE.md](DBT_SETUP_GUIDE.md)**       | 👈 **You are here** - Complete installation and setup instructions |
| **[DBT_BEST_PRACTICES.md](DBT_BEST_PRACTICES.md)** | Implementation guide for dbt modeling best practices               |

---

This guide walks you through setting up dbt for Snowflake development on various platforms.

## 🏔️ dbt Projects on Snowflake (Recommended)

**New in 2025**: Snowflake now offers native support for dbt projects directly within the Snowflake
platform. This is our **recommended approach** for most teams, but we do have instructions below for
local installs.

### What is dbt Projects on Snowflake?

[dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)
is a native integration that allows you to create, edit, test, run, and manage dbt Core projects
directly within Snowflake using:

- **Snowsight Workspaces**: Web-based IDE for dbt development
- **DBT PROJECT Objects**: Schema-level objects that contain versioned dbt projects
- **Native Execution**: Run dbt commands using Snowflake warehouses
- **Git Integration**: Connect workspaces to Git repositories for version control
- **Task Scheduling**: Use Snowflake tasks to orchestrate dbt runs

### Key Benefits

✅ **No Local Setup Required**: Develop dbt projects entirely in the browser ✅ **Negligible Cost**:
Leverages an existing virtual warehouse that can also execute the queries ✅ **Integrated
Monitoring**: Built-in observability and logging ✅ **Version Control**: Automatic versioning of dbt
project objects ✅ **Team Collaboration**: Share workspaces and manage access with RBAC ✅ **CI/CD
Ready**: Integrate with Snowflake CLI for automated deployments ✅ **Package Management**: Access
dbt Hub packages with proper external access configuration

### Getting Started with dbt Projects on Snowflake

1. **Enable Personal Database** (requires ACCOUNTADMIN, enabled by default):

   ```sql
   -- Enable personal databases for your account
   ALTER ACCOUNT SET ENABLE_PERSONAL_DATABASE = TRUE;
   ```

2. **Set Up External Access Integration for `dbt deps`** (requires ACCOUNTADMIN):

   ```sql
   -- Create NETWORK RULE for external access integration
   CREATE OR REPLACE NETWORK RULE dbt_network_rule
     MODE = EGRESS
     TYPE = HOST_PORT
     -- Minimal URL allowlist that is required for dbt deps
     VALUE_LIST = (
       'hub.getdbt.com',
       'codeload.github.com'
       );

   -- Create EXTERNAL ACCESS INTEGRATION for dbt access to external dbt package locations
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
     ALLOWED_NETWORK_RULES = (dbt_network_rule)
     ENABLED = TRUE;
   ```

3. **Create Git API Integration** (requires ACCOUNTADMIN):

   Choose one of the following authentication methods based on your security requirements.

   **Option A - Personal Access Token Authentication or No Authentication**: PAT is required for
   private repositories

   ```sql
   -- GitHub
   CREATE OR REPLACE API INTEGRATION git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = (
      -- Examples for all repositories on a service
       'https://github.com/',
       'https://gitlab.com/',
       'https://dev.azure.com/',
       -- Examples for specific orgs on a service:
       'https://github.com/organization/',
       'https://gitlab.com/organization/',
       'https://dev.azure.com/organization/'
     );
   ```

   **Option B - OAuth Authentication** (GitHub only):

   ```sql
   -- GitHub OAuth (supports OAuth, PAT, or no auth)
   CREATE OR REPLACE API INTEGRATION github_oauth_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://github.com/')
     API_USER_AUTHENTICATION = ( TYPE = snowflake_github_app );
   ```

4. **Gather Your Git Repository Information**:

   **GitHub**:

   - Repository URL: `https://github.com/username/repository-name.git`
   - Username: Your GitHub username
   - PAT: Settings → Developer settings → Personal access tokens → Generate new token (classic)
     - Required scopes: `repo` (full control of private repositories)
   - _Note: You can skip PAT if using OAuth in step 5_

   **GitLab**:

   - Repository URL: `https://gitlab.com/username/repository-name.git`
   - Username: Your GitLab username
   - PAT: User Settings → Access Tokens → Add new token
     - Required scopes: `read_repository`, `write_repository`

   **Azure DevOps**:

   - Repository URL: `https://dev.azure.com/organization/project/_git/repository-name`
   - Username: Your Azure DevOps username
   - PAT: User settings → Personal access tokens → New Token
     - Required scopes: `Code (read & write)`

5. **Create a Workspace**:

   With your API integration and repository information ready, create a dbt workspace in Snowsight:

   - Navigate to **Projects** → **Worksheets** in Snowsight. By default you will be in "My
     Workspace".
   - To use a Git Repository
     - Click **My Workspace** → **Create Workspace** → **From Git repository** and enter:
       - Repository URL: URL from step 4
       - Workspace name: custom name
       - API integration: GIT API Integration from Step 3
       - Choose OAuth, PAT, or Public repository
       - For a PAT, chose where to store the Snowflake Secret containing the Username and PAT
   - To create a dbt project in My Workspace
     - Click **+ Add new** → select **dbt Project**
   - If connecting to Git, you'll use the API integration created in step 3

6. **Configure Your Project**:

   - Each workspace requires a `profiles.yml` file specifying target warehouse, database, schema,
     and role
   - The project will run under your current Snowflake account and user context
   - Example `profiles.yml`:
     ```yaml
     my_dbt_project:
       target: dev
       outputs:
         dev:
           type: snowflake
           account: "" # Leave empty - uses current account context
           user: "" # Leave empty - uses current user context
           warehouse: MY_WAREHOUSE
           database: MY_DATABASE
           schema: MY_SCHEMA
           role: MY_ROLE
     ```

7. **Deploy as DBT PROJECT Object**:
   - Deploy your workspace as a schema-level DBT PROJECT object
   - This enables version control, scheduling, and production execution
   - Use the **Deploy** button in your workspace or SQL commands

### Supported dbt Commands

| Command    | Workspaces          | EXECUTE DBT PROJECT | snow dbt execute |
| ---------- | ------------------- | ------------------- | ---------------- |
| `build`    | ✅                  | ✅                  | ✅               |
| `compile`  | ✅                  | ✅                  | ✅               |
| `run`      | ✅                  | ✅                  | ✅               |
| `test`     | ✅                  | ✅                  | ✅               |
| `seed`     | ✅                  | ✅                  | ✅               |
| `snapshot` | ✅                  | ✅                  | ✅               |
| `deps`     | ✅ (workspace only) | ❌                  | ❌               |

### Scheduling and Automation

You can
[schedule dbt project execution](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution)
using Snowflake tasks:

```sql
-- Create a task to run your dbt project daily
CREATE TASK my_dbt_daily_task
  WAREHOUSE = 'MY_WAREHOUSE'
  SCHEDULE = 'USING CRON 0 6 * * * UTC'  -- Daily at 6 AM UTC
AS
  EXECUTE DBT PROJECT my_dbt_project_object COMMAND 'build';

-- Start the task
ALTER TASK my_dbt_daily_task RESUME;
```

#### Accessing dbt Artifacts and Logs Programmatically

When dbt projects execute, logs and artifacts are saved in a `dbt_results.zip` file. You can
[access these programmatically](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#access-dbt-artifacts-and-logs-programmatically)
using the following approach:

**Stored procedure for automated execution with tasks:**

```sql
-- Create a named internal stage
CREATE OR REPLACE STAGE my_dbt_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Create a stored procedure that executes dbt and copies results
CREATE OR REPLACE PROCEDURE my_db.public.run_dbt_and_copy_results_file()
RETURNS varchar
LANGUAGE SQL
COMMENT = 'Execute dbt and copy the files in the same sproc call.'
EXECUTE AS CALLER
AS
DECLARE
    output_archive_url varchar;
BEGIN
    EXECUTE DBT PROJECT my_db.my_schema.my_dbt_project args='build';
    output_archive_url := (SELECT output_archive_url FROM TABLE(RESULT_SCAN(last_query_id())));
    COPY FILES INTO @my_dbt_stage/results/
      FROM (SELECT :output_archive_url,
            (to_char(current_timestamp(), 'YYYYMMDD_HH24_MI') || '.zip'));
    RETURN 'dbt execution and log copy completed successfully';
END;

-- Create a task that runs the stored procedure every 6 hours
CREATE OR REPLACE TASK my_db.my_schema.run_my_dbt_project
  WAREHOUSE = my_dbt_warehouse
  SCHEDULE = '6 hours'
AS
  CALL my_db.public.run_dbt_and_copy_results_file();

-- Start the task
ALTER TASK my_db.my_schema.run_my_dbt_project RESUME;
```

#### Enabling Enhanced Monitoring

To enable detailed monitoring features for your dbt project, configure logging levels on the
database and schema:

```sql
-- Enable comprehensive logging and monitoring
ALTER SCHEMA my_db.my_dbt_project_schema SET LOG_LEVEL = 'INFO';
ALTER SCHEMA my_db.my_dbt_project_schema SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA my_db.my_dbt_project_schema SET METRIC_LEVEL = 'ALL';
```

After enabling these settings, you can monitor dbt project executions in Snowsight under
**Monitoring** → **dbt Projects**.

### Team Collaboration Flexibility

**Important**: Teams can use different development approaches simultaneously:

- **Developer A**: Uses dbt Projects on Snowflake workspaces
- **Developer B**: Uses dbt Cloud for development
- **Developer C**: Uses VS Code with local dbt installation
- **All developers**: Check code into the same Git repository

This flexibility allows teams to adopt dbt Projects on Snowflake gradually while maintaining
existing workflows.

### When to Use dbt Projects on Snowflake

**✅ Recommended for:**

- Teams already heavily invested in Snowflake
- Organizations wanting to minimize local development setup
- Projects requiring tight integration with Snowflake features
- Teams needing centralized dbt execution and monitoring

**🤔 Consider alternatives if:**

- You need dbt Cloud's advanced features (IDE, semantic layer, etc.)
- Your team prefers local development environments
- You're using multiple data warehouses beyond Snowflake

### Snowflake CLI dbt Commands

The
[Snowflake CLI provides native dbt commands](https://docs.snowflake.com/en/developer-guide/snowflake-cli/data-pipelines/dbt-projects)
for managing dbt Projects on Snowflake from the command line or CI/CD pipelines.

#### Install Snowflake CLI (version 3.9.0 or later):

```bash
pip install snowflake-cli
```

#### Core Commands

| Command            | Description                                             | Example                                 |
| ------------------ | ------------------------------------------------------- | --------------------------------------- |
| `snow dbt deploy`  | Deploy dbt project to Snowflake as a DBT PROJECT object | `snow dbt deploy my_project --source .` |
| `snow dbt execute` | Execute dbt commands on deployed project                | `snow dbt execute my_project run`       |
| `snow dbt list`    | List all dbt projects in current connection             | `snow dbt list`                         |

**Deploy a dbt project:**

```bash
# Deploy from current directory
snow dbt deploy jaffle_shop --source .

# Deploy with specific connection and database
snow dbt deploy jaffle_shop --source . --connection my_conn --database MY_DB
```

**Execute dbt commands:**

```bash
# Run all models
snow dbt execute jaffle_shop run

# Run specific models with selection
snow dbt execute jaffle_shop run --select @source:snowplow,tag:nightly

# Run tests
snow dbt execute jaffle_shop test

# Build everything (run + test)
snow dbt execute jaffle_shop build

# Execute asynchronously
snow dbt execute --run-async jaffle_shop run
```

**List deployed projects:**

```bash
# List all dbt projects
snow dbt list

# List with specific connection
snow dbt list --connection my_connection
```

#### CI/CD Integration

The CLI commands are ideal for building CI/CD pipelines. You can trigger deployment to a dbt project
when a branch changes. This also allows you to use git repositories in your dependencies by running
dbt deps in the pipeline. Here's a typical workflow:

```yaml
# GitHub Actions example
- name: Parse and deploy dbt project
  run: |
    dbt clean
    dbt deps
    dbt parse
    snow dbt deploy product_pipeline --source .
```

**Key advantages for CI/CD:**

- No Git repository object in Snowflake required - just your CI/CD pipeline with dbt and Snowflake
  CLI
- Direct integration with existing CI/CD tools

#### Requirements for CLI Usage

Your dbt project must include:

- `dbt_project.yml` in the main project directory
- `profiles.yml` with connection details
- Profile name in `dbt_project.yml` must match profile defined in `profiles.yml`
- **Important**: Remove any passwords from `profiles.yml` - Snowflake's dbt projects don't need them

### Learn More

- [📖 dbt Projects on Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)
- [🚀 Getting Started Tutorial](https://docs.snowflake.com/en/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial) -
  Includes detailed Git setup and external access configuration
- [📊 Monitoring & Observability](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability)
- [⏰ Scheduling Project Execution](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution)

---

## 💻 Traditional dbt Setup (Alternative Approaches)

If you prefer traditional dbt development or need features not yet available in dbt Projects on
Snowflake, the following sections cover local installation options.

## Prerequisites

This project depends on the following two data sets:

- **SNOWFLAKE_SAMPLE_DATA** that is available by default in all new Snowflake accounts
- **[Snowflake Finance & Economics](https://app.snowflake.com/marketplace/data-products/search?search=Finance%20%26%20Economics)**,
  formerly known as the Cybersyn Financial Economic Essentials.
  - It is available for free in the Snowflake Data Marketplace
  - If named other than "CYBERSYN_FINANCIAL_ECONOMIC_ESSENTIALS", update the database name in
    sources.yml

## Installing dbt using Miniforge (Recommended)

If you can install your own software, I generally recommend using
[Miniforge](https://conda-forge.org/download/) to create an isolated Python environment just for
dbt. Miniforge is completely open source, does not require a license like Anaconda or Miniconda, and
uses the free Conda-Forge repository for packages. A dbt-conda-env.yml file has been provided so you
can set up this environment and switch to it with the following commands. This is much simpler than
some other flavors of Python.

```shell
conda env create -f dbt-conda-env.yml
conda activate dbt
```

If you have SSL errors, you may need to install pip_system_certs into your base environment first.
The dbt-conda-env.yml file already includes this for your child environment. The `--trusted-host`
parameters below will allow you to bypass firewall issues.

```shell
conda activate base
python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

## Installing dbt using any other flavor of Python - Windows

### Setting up Python and verifying which python you are now using:

- Install Python using your company's Self Service portal or install the
  [open source version of Python.org](https://www.python.org/downloads/)
- First you will want to see if you have the correct version of Python in your path using a Windows
  Command Prompt:
  ```shell
  where python
  python --version
  ```
- It should return a path like `C:\Program Files\Python311`. You can use Python 3.9 and higher. If
  you can't run `python --version` it is likely that you do not have the right version of python in
  your PATH.

### How to change your PATH

If this is not the correct version of Python or the wrong location, you can update your PATH on
Windows 10 & 11 using the following:

1. Open Start Search, type "env", and select "Edit the system environment variables".
2. Click the "Environment Variables…" button.
3. In the "User Variables" section, locate "Path", and click edit.
4. In the "Edit environment variable" UI, click "New" to add the new path to your preferred version
   of Python.
5. Use the "Move Up" button to make your new path the first entry
6. Close and reopen any command prompts or VS Code to use the new PATH
7. Use the `where python` and `python --version` commands again to verify that you are now using the
   correct version.

### Update pip and install dbt

- Next make sure pip is up to date and that pip_system_certs is also installed. The `--trusted-host`
  parameters below will help you avoid firewall issues.
  ```shell
  python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  ```
- Next install virtualenv and create a new virtual environment called `dbt`
  ```shell
  python -m pip install --user virtualenv
  python -m venv dbt
  ```
- Now you can activate your virtual environment, verify that the location of python has changed, and
  install dbt
  ```shell
  .\dbt\Scripts\activate
  where python
  python -m pip install -U dbt-core dbt-snowflake
  dbt --version
  ```

## Installing dbt using any other flavor of Python - Unix/macOS

- Install Python using your company's Self Service portal or install the
  [open source version of Python.org](https://www.python.org/downloads/)
- First you will want to see if you have the correct version of Python in your path using a shell:
  ```shell
  which python
  python --version
  ```
- You can use Python 3.8 and higher. If you can't run `python --version` it is likely that you do
  not have the right version of python in your PATH.

### How to change your PATH

This command can be used to append your folder before the existing PATH. You may need to add this to
your .bash_profile or other shell configuration file to make the change permanent.

```shell
export PATH=/my/path/to/python/:$PATH
```

### Update pip and install dbt

- Next make sure pip is up to date and that pip_system_certs is also installed. The `--trusted-host`
  parameters below will help you avoid firewall issues.
  ```shell
  python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  ```
- Next install virtualenv and create a new virtual environment called `dbt`
  ```shell
  python -m pip install --user virtualenv
  python -m venv dbt
  ```
- Now you can activate your virtual environment, verify that the location of python has changed, and
  install dbt. We install/update pip and pip_system_certs this time in the virtual env.
  ```shell
  source dbt/bin/activate
  which python
  python -m pip install pip -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  python -m pip install pip_system_certs -U --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
  python -m pip install -U dbt-core dbt-snowflake
  dbt --version
  ```

## Creating a simple dbt sample project to test your connection to Snowflake

The dbt init command can step you through creating a `~/.dbt/profiles.yml` file and starter project
structure.

⚠️ **Important Notes:**

- Running this project will create a table and a view in the schema you specify.
- The sample project is designed to have a test fail when you first run `dbt build`. If you open the
  first model under /models/ you will see that it has a where clause you can uncomment to make the
  test pass.

```shell
dbt init
dbt compile
dbt build
```

## Setting Up Your Editor

Most dbt users edit their dbt scripts with Microsoft's free editor, VSCode:

### VSCode Setup

- [Download VSCode](https://code.visualstudio.com/Download)
- From the Extensions screen (icon looks like Tetris) you should install two extensions:
  - **python**
  - **["Snowflake"](https://docs.snowflake.com/en/user-guide/vscode-ext)**
- In the Explorer, right click in the background and "Add folder to workspace" to add where your dbt
  project will be located.
- On Windows, you will want to change the default terminal to "Command Prompt". Under _File_ ->
  _Preferences_ -> _Settings_, search for "windows terminal" and scroll down to where it says the
  default is "null" and change that to "Command Prompt".
- You will want to set the default interpreter to your new "dbt" environment using
  [these instructions from Microsoft](https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter).

## Setting Up Your Snowflake Account for this sample project

- Create a target schema in Snowflake that you want to deploy your dbt demo into
- Add the Knoema Economy Data Atlas and Snowflake Sample Data to your account if necessary

## Update Configuration For Your Account and Test Execution

- Update your `~/.dbt/profiles.yml` file with your credentials and target DB/schema. There is a
  sample profiles.yml file you can copy to your ~/.dbt/ folder and update if you don't already have
  one.
- From the root folder, run `dbt deps` to download modules from the dbt hub
- Run `dbt build --full-refresh` and troubleshoot any errors such as missing objects or permission
  issues

## Cheatsheet of most common dbt commands

### Essential Commands

- `dbt deps` - download 3rd party packages (necessary for this project before build)
- `dbt build` - both compile and then run all models & associated tests
- `dbt build --full-refresh` - have incremental models run as a full reload

### Selection Commands

- `dbt build --select modelname` - will only compile/run modelname
- `dbt build --select +modelname` - will compile/run modelname and all parents
- `dbt build --select modelname+` - will compile/run modelname and all children
- `dbt build --select +modelname+` - will compile/run modelname, and all parents and children
- `dbt build --select @modelname` - will compile/run modelname, all parents, all children, AND all
  parents of all children
- `dbt build --exclude modelname` - will compile/run all models except modelname

### Other Useful Commands

- `dbt compile` - compile all models but do not execute them
- `dbt run` - run all models & tests
- `dbt seed` - create or refresh small tables from .csv seed files
- `dbt clean` - clear your logs and compiled scripts (can fix issues)
- `dbt docs generate` - refresh the documentation for your project
- `dbt docs generate --static` - Generate as a single static_index.html file that you can host on a
  server or open in your browser
- `dbt docs serve` - open this documentation in your browser

Additional commands and details are available in
[dbt's documentation](https://docs.getdbt.com/reference/dbt-commands)

## Troubleshooting

### Common Issues

- **SSL/Firewall Issues**: Use the `--trusted-host` parameters shown in the installation commands
- **Python Path Issues**: Verify you're using the correct Python version with `which python` or
  `where python`
- **Virtual Environment Issues**: Make sure you've activated your virtual environment before
  installing dbt
- **Connection Issues**: Verify your `profiles.yml` file has the correct Snowflake credentials

### Getting Help

- [dbt Documentation](https://docs.getdbt.com/)
- [Snowflake dbt Documentation](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)
