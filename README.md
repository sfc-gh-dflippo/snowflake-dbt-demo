# dbt for Snowflake Demonstration Project

## 📚 Documentation Navigation

| Document                                           | Description                                                              |
| -------------------------------------------------- | ------------------------------------------------------------------------ |
| **[README.md](README.md)**                         | 👈 **You are here** - Project overview, architecture, and feature matrix |
| **[DBT_SETUP_GUIDE.md](DBT_SETUP_GUIDE.md)**       | Complete installation and setup instructions for all platforms           |
| **[DBT_BEST_PRACTICES.md](DBT_BEST_PRACTICES.md)** | Implementation guide for dbt modeling best practices                     |

---

## 🚀 Quick Start

**New to dbt?** Check out our comprehensive **[dbt Setup Guide](DBT_SETUP_GUIDE.md)** for detailed installation instructions across all platforms.

**Ready to explore?** This project demonstrates dbt best practices integrated with medallion architecture for comprehensive training.

### Prerequisites

- SNOWFLAKE_SAMPLE_DATA (available by default in all Snowflake accounts)
- [Snowflake Finance & Economics](https://app.snowflake.com/marketplace/data-products/search?search=Finance%20%26%20Economics) (free in Snowflake Data Marketplace)

### Quick Setup

```bash
# Install dependencies
dbt deps

# Build the project
dbt build --full-refresh
```

For detailed setup instructions, see **[DBT_SETUP_GUIDE.md](DBT_SETUP_GUIDE.md)**.

### 📋 Quick Command Reference

```bash
# Essential commands
dbt deps                       # Install packages
dbt build                      # Run all models and tests
dbt build --full-refresh       # Full reload of incremental models

# Selection commands
dbt build --select modelname   # Run specific model
dbt build --select +modelname  # Run model and parents
dbt build --select modelname+  # Run model and children

# Documentation
dbt docs generate              # Generate documentation
dbt docs serve                 # Serve documentation locally
```

See **[DBT_SETUP_GUIDE.md](DBT_SETUP_GUIDE.md)** for complete command reference and troubleshooting.

## 🔍 Quick Feature Finder

Looking for a specific dbt feature? Jump directly to examples:

**🏗️ Materializations:** [Ephemeral](#materializations) • [Incremental](#materializations) • [Dynamic Tables](#materializations) • [Python Models](#materializations)
**🧪 Testing:** [dbt_constraints](#-testing-framework) • [Generic Tests](#-testing-framework) • [Singular Tests](#-testing-framework) • [Contracts](#-testing-framework)
**📊 Advanced:** [Snapshots](#-advanced-dbt-features) • [Exposures](#-advanced-dbt-features) • [Seeds](#-advanced-dbt-features) • [Analyses](#-advanced-dbt-features)
**🔧 Jinja:** [Advanced Templating](#-jinja--macros) • [Custom Macros](#-jinja--macros) • [Variables](#-jinja--macros) • [Loops](#-jinja--macros)
**⚙️ Snowflake:** [Streams](#snowflake-specific-features) • [Sequences](#snowflake-specific-features) • [Secure Views](#snowflake-specific-features) • [Warehouses](#snowflake-specific-features)
**📈 Business:** [Executive Dashboards](#-business-intelligence-integration) • [Customer Analytics](#-business-intelligence-integration) • [TPC-H Benchmarks](#-business-intelligence-integration)

---

## Project Architecture

This project demonstrates **dbt Best Practices integrated with Medallion Architecture** for comprehensive training:

### 🏆 Integrated Architecture: Best Practices + Medallion

- **Bronze Layer** (`models/bronze/`) - **Staging models** + raw data patterns
- **Silver Layer** (`models/silver/`) - **Intermediate models** + transformation examples
- **Gold Layer** (`models/gold/`) - **Marts models** + advanced analytics

### 📚 Complexity-Based Learning Path

Each layer contains three complexity levels with integrated best practices:

#### 🥉 **Bronze Layer: Staging + Raw Patterns**

- **Crawl** (`bronze/crawl/`) - Simple staging models with basic column renaming
  - `stg_tpc_h__nations`, `stg_tpc_h__regions`, `stg_tpc_h__customers`, `stg_tpc_h__orders`
- **Walk** (`bronze/walk/`) - Complex staging with composite keys and external sources
  - `stg_tpc_h__lineitem`, `stg_economic_essentials__fx_rates`, `stg_customers_with_tests`
- **Run** (`bronze/run/`) - Advanced staging with streams and incremental loading
  - `customer_cdc_stream`, `stg_orders_incremental`

#### 🥈 **Silver Layer: Intermediate + Transformations**

- **Crawl** (`silver/crawl/`) - Simple data cleaning and standardization
  - `clean_nations`
- **Walk** (`silver/walk/`) - Business logic and aggregations
  - `int_customers__with_orders`, `customer_segments`, `lookup_exchange_rates`
- **Run** (`silver/run/`) - Complex transformations with advanced features
  - `int_fx_rates__daily`, `order_facts_dynamic`, `customer_clustering`, `async_bulk_operations`

#### 🥇 **Gold Layer: Marts + Analytics**

- **Crawl** (`gold/crawl/`) - Simple aggregated views and summaries
  - `dim_current_year_orders`, `dim_current_year_open_orders`, `nation_summary`
- **Walk** (`gold/walk/`) - Complete business dimensions and analytics
  - `dim_customers`, `dim_orders`, `customer_insights`, `dim_calendar_day`, `dim_customer_changes`
- **Run** (`gold/run/`) - High-performance fact tables and advanced analytics
  - `fct_order_lines`, `executive_dashboard`, `fact_order_line_full_reload`, `fact_order_line_pivot`

#### 🔧 **Other Layer: Utility + Reference Models**

- **Utility Models** (`other/`) - System monitoring and reference implementations
  - `dbt_query_history`, `dynamic_warehouse_assignment`
- **Benchmarks** (`other/tpc_h_benchmarks/`) - Industry-standard performance queries
  - `Q1_FACT_PRICING_SUMMARY_REPORT_QUERY`, `Q2_MINIMUM_COST_SUPPLIER_QUERY`, `Q3_SHIPPING_PRIORITY_QUERY`, `Q4_ORDER_PRIORITY_CHECKING_QUERY`

### 🎯 Best Practices Demonstrated

#### ✅ **Integrated Best Practices by Layer**

**🥉 Bronze (Staging) Best Practices:**

- **One-to-one source relationships**: Each source has exactly one staging model
- **Standardized naming**: `stg_{source_name}__{table_name}` convention
- **View materialization**: All staging models as views for optimal performance
- **Feature organization**: `basic_staging/` (crawl) vs `complex_staging/` (walk)
- **Complexity assessment**: Most staging is crawl-level (basic column renaming)
- **Comprehensive testing**: Primary keys, foreign keys, data quality checks

**🥈 Silver (Intermediate) Best Practices:**

- **Business logic isolation**: Complex transformations separated from staging
- **Feature organization**: `business_logic/` vs `advanced_transformations/`
- **Ephemeral materialization**: For reusable components (`business_logic/`)
- **Table materialization**: For complex logic that needs persistence (`advanced_transformations/`)
- **No direct source references**: Only references staging models

**🥇 Gold (Marts) Best Practices:**

- **Business-ready data**: Final data products for consumption
- **Feature organization**: `dimensions/` vs `facts/` by data modeling pattern
- **Proper dependencies**: References staging, intermediate, and other marts only
- **Clear naming**: `dim_` for dimensions, `fct_` for facts
- **Incremental materialization**: Large fact tables for scalability
- **Comprehensive business testing**: Relationship validation, business rule checks

**Key Rules Implemented:**

- ✅ **No Direct Joins to Source**: All models reference staging layer, not sources directly
- ✅ **Proper Staging Layer**: One-to-one relationship between sources and staging models
- ✅ **No Source Fanout**: Each source referenced by exactly one staging model
- ✅ **Proper Model Dependencies**: Clear lineage from staging → intermediate → marts
- ✅ **Standardized Naming**: Consistent `stg_`, `int_`, `dim_`, `fct_` prefixes
- ✅ **No Hard-coded References**: All references use `ref()` and `source()` functions

## 🎯 Comprehensive dbt-core Features Demonstrated

### **🏗️ Materializations** {#materializations}

| Feature                      | Model                         | Location                                                                                                       | Layer     | Description                                          |
| ---------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------- |
| **Ephemeral (Staging)**      | `stg_tpc_h__customers`        | [`bronze/crawl/`](models/bronze/crawl/stg_tpc_h__customers.sql)                                                | 🥉 Bronze | One-to-one source relationship, CTE compilation      |
| **Ephemeral (Staging)**      | `stg_tpc_h__lineitem`         | [`bronze/walk/`](models/bronze/walk/stg_tpc_h__lineitem.sql)                                                   | 🥉 Bronze | Complex staging with composite keys                  |
| **Ephemeral (Intermediate)** | `int_customers__with_orders`  | [`silver/walk/`](models/silver/walk/int_customers__with_orders.sql)                                            | 🥈 Silver | Reusable business logic, aggregations                |
| **Table (Intermediate)**     | `int_fx_rates__daily`         | [`silver/run/`](models/silver/run/int_fx_rates__daily.sql)                                                     | 🥈 Silver | Complex transformations with window functions        |
| **Table (Dimensions)**       | `dim_customers`               | [`gold/walk/`](models/gold/walk/dim_customers.sql)                                                             | 🥇 Gold   | Business-ready customer dimension                    |
| **Table (Dimensions)**       | `dim_orders`                  | [`gold/walk/`](models/gold/walk/dim_orders.sql)                                                                | 🥇 Gold   | Business-ready orders dimension                      |
| **Incremental (Facts)**      | `fct_order_lines`             | [`gold/run/`](models/gold/run/fct_order_lines.sql)                                                             | 🥇 Gold   | High-performance fact table with incremental loading |
| **Incremental (Advanced)**   | `stg_orders_incremental`      | [`bronze/run/`](models/bronze/run/stg_orders_incremental.sql)                                                  | 🥉 Bronze | Advanced incremental with complex Jinja logic        |
| **Incremental (Macros)**     | `dim_customers_macro_example` | [`gold/run/incremental_with_macros/`](models/gold/run/incremental_with_macros/dim_customers_macro_example.sql) | 🥇 Gold   | SCD Type 2 with custom macros                        |
| **Dynamic Table**            | `order_facts_dynamic`         | [`silver/run/`](models/silver/run/order_facts_dynamic.sql)                                                     | 🥈 Silver | Real-time analytics with dynamic tables              |
| **Python Model (ML)**        | `customer_clustering`         | [`silver/run/`](models/silver/run/customer_clustering.py)                                                      | 🥈 Silver | Machine learning with scikit-learn                   |
| **Python Model (Async)**     | `async_bulk_operations`       | [`silver/run/`](models/silver/run/async_bulk_operations.py)                                                    | 🥈 Silver | Parallel processing and bulk operations              |
| **View (Legacy)**            | `dim_calendar_day`            | [`gold/walk/`](models/gold/walk/dim_calendar_day.sql)                                                          | 🥇 Gold   | Calendar dimension with ghost keys                   |

### **🧪 Testing Framework**

| Feature                  | Model/Location                       | Complexity                                                                 | Description                                          |
| ------------------------ | ------------------------------------ | -------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------- |
| **dbt_constraints (PK)** | All dimension models                 | All                                                                        | Primary key constraints with database enforcement    |
| **dbt_constraints (FK)** | All fact models                      | All                                                                        | Foreign key relationships with referential integrity |
| **dbt_constraints (UK)** | Various models                       | All                                                                        | Unique key constraints for business rules            |
| **Generic Tests**        | `test_positive_values`               | [`tests/generic/`](tests/generic/test_positive_values.sql)                 | Walk                                                 | Custom reusable test for positive values  |
| **Singular Tests**       | `test_customer_balance_distribution` | [`tests/singular/`](tests/singular/test_customer_balance_distribution.sql) | Run                                                  | Specific business rule validation         |
| **Advanced Testing**     | `fct_order_lines`                    | [`gold/_models.yml`](models/gold/_models.yml)                              | Run                                                  | Complex test combinations and expressions |
| **Contract Enforcement** | `order_facts_dynamic`                | [`silver/_models.yml`](models/silver/_models.yml)                          | Run                                                  | Column contracts and data types           |
| **dbt_utils Tests**      | Various models                       | All                                                                        | Unique combinations, accepted values, ranges         |

### **📊 Advanced dbt Features**

| Feature                    | Model/Location                   | Complexity                                                                              | Description |
| -------------------------- | -------------------------------- | --------------------------------------------------------------------------------------- | ----------- | -------------------------------------------- |
| **Snapshots (SCD Type 2)** | `DIM_CUSTOMERS_SCD`              | [`snapshots/30_presentation/`](snapshots/30_presentation/DIM_CUSTOMERS_SCD.sql)         | Run         | Historical data tracking with check strategy |
| **Snapshots (Streams)**    | `DIM_CUSTOMERS_FROM_STREAM`      | [`snapshots/30_presentation/`](snapshots/30_presentation/DIM_CUSTOMERS_FROM_STREAM.sql) | Run         | Change data capture with Snowflake streams   |
| **Exposures**              | `executive_dashboard_exposure`   | [`exposures/`](exposures/executive_dashboard_exposure.yml)                              | Walk        | BI tool integration and lineage              |
| **Analyses**               | `customer_cohort_analysis`       | [`analyses/`](analyses/customer_cohort_analysis.sql)                                    | Run         | Exploratory data analysis                    |
| **Seeds**                  | `dynamic_warehouses`             | [`seeds/`](seeds/dynamic_warehouses.csv)                                                | Walk        | Reference data management                    |
| **Operations**             | `medallion_architecture_helpers` | [`macros/`](macros/medallion_architecture_helpers.sql)                                  | Run         | Custom dbt operations                        |

### **🔧 Jinja & Macros**

| Feature             | Model/Location              | Complexity                                                    | Description |
| ------------------- | --------------------------- | ------------------------------------------------------------- | ----------- | ------------------------------------------ |
| **Advanced Jinja**  | `order_facts_dynamic`       | [`silver/run/`](models/silver/run/order_facts_dynamic.sql)    | Run         | Complex loops, conditionals, and variables |
| **Custom Macros**   | `snowflake_integration_key` | [`macros/`](macros/snowflake_integration_key.sql)             | Run         | Surrogate key generation                   |
| **Custom Macros**   | `insert_ghost_key`          | [`macros/`](macros/insert_ghost_key.sql)                      | Run         | Ghost key insertion for dimensions         |
| **Custom Macros**   | `get_scd_sql`               | [`macros/`](macros/get_scd_sql.sql)                           | Run         | SCD Type 2 SQL generation                  |
| **Jinja Variables** | `raw_orders_incremental`    | [`bronze/run/`](models/bronze/run/raw_orders_incremental.sql) | Run         | Dynamic SQL with environment variables     |
| **Jinja Loops**     | `fact_order_line_pivot`     | [`gold/run/`](models/gold/run/fact_order_line_pivot.sql)      | Run         | Dynamic column generation                  |

### **⚙️ Snowflake-Specific Features** {#snowflake-specific-features}

| Feature              | Model/Location           | Complexity                                                                             | Description                          |
| -------------------- | ------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------- |
| **Dynamic Tables**   | `order_facts_dynamic`    | [`silver/run/`](models/silver/run/order_facts_dynamic.sql)                             | Run                                  | Real-time materialized views with lag |
| **Streams**          | `customer_cdc_stream`    | [`bronze/run/`](models/bronze/run/customer_cdc_stream.sql)                             | Run                                  | Change data capture streams           |
| **Sequences**        | Various dimension models | Run                                                                                    | Auto-incrementing surrogate keys     |
| **Secure Views**     | `DIM_CUSTOMERS_SHARE`    | [`gold/walk/sensitive_data/`](models/gold/walk/sensitive_data/DIM_CUSTOMERS_SHARE.sql) | Walk                                 | Data sharing with row-level security  |
| **Transient Tables** | Various models           | All                                                                                    | Optimized storage for temporary data |
| **Query Tags**       | All models               | All                                                                                    | Query identification and monitoring  |
| **Warehouses**       | Various models           | All                                                                                    | Dynamic warehouse assignment         |

### **🔄 Development Workflow**

| Feature               | Location                | Complexity | Description                                                             |
| --------------------- | ----------------------- | ---------- | ----------------------------------------------------------------------- |
| **Project Structure** | `dbt_project.yml`       | All        | Medallion architecture configuration                                    |
| **Variables**         | `dbt_project.yml`       | Walk       | Global configuration management                                         |
| **Environments**      | `profiles.yml.sample`   | Walk       | Multi-environment setup                                                 |
| **Packages**          | `packages.yml`          | All        | External package management (dbt_constraints, dbt_utils, dbt_artifacts) |
| **Documentation**     | `DBT_SETUP_GUIDE.md`    | All        | Complete installation and configuration guide                           |
| **Best Practices**    | `DBT_BEST_PRACTICES.md` | All        | Implementation guide for dbt modeling standards                         |
| **Hooks (Pre/Post)**  | Various models          | Run        | Custom SQL execution before/after model runs                            |
| **Grants**            | `dbt_project.yml`       | All        | Automated permission management                                         |

### **📈 Business Intelligence Integration**

| Feature                    | Model/Location            | Complexity                                                                                          | Description |
| -------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------- |
| **Executive Dashboard**    | `executive_dashboard`     | [`gold/run/`](models/gold/run/executive_dashboard.sql)                                              | Run         | KPI aggregations for leadership reporting |
| **Customer Insights**      | `customer_insights`       | [`gold/walk/`](models/gold/walk/customer_insights.sql)                                              | Walk        | Customer analytics and segmentation       |
| **TPC-H Performance**      | `Q1_FACT_PRICING_SUMMARY` | [`other/tpc_h_benchmarks/`](models/other/tpc_h_benchmarks/Q1_FACT_PRICING_SUMMARY_REPORT_QUERY.sql) | Run         | Industry-standard performance benchmarks  |
| **Query History Analysis** | `dbt_query_history`       | [`other/`](models/other/dbt_query_history.sql)                                                      | Run         | dbt execution monitoring and optimization |

### **🎓 Training & Learning Path**

| Complexity                 | Focus                                       | Example Models                                | Key Concepts                                       |
| -------------------------- | ------------------------------------------- | --------------------------------------------- | -------------------------------------------------- |
| **🥉 Crawl (Beginner)**    | Basic staging, simple transformations       | `stg_tpc_h__customers`, `raw_nations`         | Source relationships, basic SQL, ephemeral models  |
| **🥈 Walk (Intermediate)** | Business logic, intermediate models         | `int_customers__with_orders`, `dim_customers` | Aggregations, joins, business rules, testing       |
| **🥇 Run (Advanced)**      | Complex analytics, performance optimization | `fct_order_lines`, `customer_clustering`      | Incremental loading, Python models, advanced Jinja |

## Resources

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Free [on-demand training](https://courses.getdbt.com/)
- [Additional Packages](https://hub.getdbt.com/)
- Create PK, UK, and FK in Snowflake using [dbt Constraints](https://github.com/Snowflake-Labs/dbt_constraints)
- Snowflake Guide - [Accelerating Data Teams with dbt Core & Snowflake](https://quickstarts.snowflake.com/guide/data_teams_with_dbt_core/index.html)
- Snowflake Guide - [Accelerating Data Teams with dbt Cloud & Snowflake](https://quickstarts.snowflake.com/guide/data_teams_with_dbt_cloud/index.html)
- Snowflake Guide - [Data Engineering with Apache Airflow, Snowflake & dbt](https://quickstarts.snowflake.com/guide/data_engineering_with_apache_airflow/index.html)
