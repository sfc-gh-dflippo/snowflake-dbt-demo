---
auto_generated: true
description: A typical Amazon Redshift-to-Snowflake migration can be broken down into
  nine key phases. This guide provides a comprehensive framework to navigate the technical
  and strategic challenges involved, ens
last_scraped: '2026-01-14T16:51:12.340272+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/guides/redshift
title: Amazon Redshift to Snowflake Migration Guide | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../README.md)

    * Tools

      * [SnowConvert AI](../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../sma-docs/README.md)
    * Guides

      * [Teradata](teradata.md)
      * [Databricks](databricks.md)
      * [SQL Server](sqlserver.md)
      * [Amazon Redshift](redshift.md)
      * [Oracle](oracle.md)
      * [Azure Synapse](azuresynapse.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../user-guide/replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Migrations](../README.md)GuidesAmazon Redshift

# **Amazon Redshift to Snowflake Migration Guide**[¶](#amazon-redshift-to-snowflake-migration-guide "Link to this heading")

## **Snowflake Migration Framework**[¶](#snowflake-migration-framework "Link to this heading")

A typical Amazon Redshift-to-Snowflake migration can be broken down into nine key phases. This guide provides a comprehensive framework to navigate the technical and strategic challenges involved, ensuring a smooth transition to Snowflake’s cloud data platform.

## **Migration Phases**[¶](#migration-phases "Link to this heading")

### **Phase 1: Planning and Design**[¶](#phase-1-planning-and-design "Link to this heading")

This initial phase is critical for establishing the foundation of a successful migration. Rushing this step often leads to scope creep, budget overruns, and missed deadlines. A thorough plan ensures all stakeholders are aligned and the project’s goals are clearly defined.

**Your Actionable Steps:**

* **Conduct a Thorough Assessment of Your Redshift Environment:**

  + **Inventory & Analyze:** Catalog all databases, schemas, tables, views, stored procedures, and user-defined functions (UDFs) in your Redshift cluster. Use Redshift system tables (SVV\_TABLE\_INFO, PG\_PROC, etc.) to gather metadata.
  + **Analyze Workloads:** Use Redshift’s STL\_QUERY and SVL\_QUERY\_SUMMARY views to identify query patterns, user concurrency, and performance bottlenecks. This data is crucial for designing your Snowflake virtual warehouse strategy.
  + **Identify Dependencies:** Map all upstream data sources (ETL/ELT jobs) and downstream consumers (BI tools, applications, data science notebooks).
* **Define the Migration Scope and Strategy:**

  + **Prioritize Workloads:** Classify workloads by business impact and technical complexity. Start with a high-impact, low-complexity workload for a quick win and to build momentum.
  + **Choose a Migration Approach:** Decide between a “lift and shift” approach for a faster migration or a re-architecture approach to modernize and optimize data models and pipelines.
* **Develop the Project Plan:**

  + **Establish a Team:** Create a migration team with clear roles and responsibilities (e.g., Project Manager, Data Engineer, DBA, Security Admin, Business Analyst).
  + **Create a Timeline:** Define realistic timelines and milestones for each of the nine phases.
  + **Define Success Metrics:** Establish clear KPIs to measure the success of the migration, such as cost reduction, query performance improvement, and user satisfaction.

### **Phase 2: Environment and Security**[¶](#phase-2-environment-and-security "Link to this heading")

With a solid plan in place, the next step is to prepare the Snowflake environment and replicate your security posture. A key advantage of migrating from Redshift is that both platforms typically run on the same cloud provider (AWS), which simplifies data transfer.

**Your Actionable Steps:**

* **Set Up Your Snowflake Account:**

  + **Choose Edition and Cloud Provider:** Select the Snowflake edition (e.g., Standard, Enterprise, Business Critical) that meets your needs. Choose AWS as the cloud provider and select the same region as your current S3 buckets to minimize data transfer costs and latency.
  + **Design a Warehouse Strategy:** Based on the workload analysis from Phase 1, create an initial set of virtual warehouses. Isolate different workloads (e.g., WH\_LOADING, WH\_TRANSFORM, WH\_BI\_ANALYTICS) to prevent resource contention. Start with T-shirt sizes (e.g., X-Small, Small) and plan to resize them based on performance testing.
* **Implement the Security Model:**

  + **Map Redshift Users/Groups to Snowflake Roles:** Translate Redshift’s user and group permissions into Snowflake’s Role-Based Access Control (RBAC) model. Create a hierarchy of functional roles (e.g., SYSADMIN, SECURITYADMIN) and access roles (e.g., BI\_READ\_ONLY, ETL\_READ\_WRITE).
  + **Configure Network Policies and Authentication:** Set up network policies to restrict access to trusted IP addresses. Configure authentication methods, such as federated authentication (SSO) using an identity provider like Okta or Azure AD.

### **Phase 3: Database Code Conversion**[¶](#phase-3-database-code-conversion "Link to this heading")

This phase involves converting Redshift’s DDL, DML, and procedural code to be compatible with Snowflake. Automation tools can accelerate this process, but manual review and adjustment are essential due to differences in SQL dialects and platform architecture.

**Your Actionable Steps:**

* **Convert DDL (Data Definition Language):**

  + **Tables and Views:** Extract CREATE TABLE and CREATE VIEW statements from Redshift. Convert Redshift-specific data types to their Snowflake equivalents (see Appendix 2).
  + **Remove Redshift-Specific Clauses:** Eliminate Redshift-specific physical design clauses like DISTSTYLE, DISTKEY, and SORTKEY. Snowflake’s architecture handles data distribution and clustering automatically or through logical clustering keys on very large tables.
* **Convert DML (Data Manipulation Language) and Procedural Code:**

  + **Rewrite Stored Procedures:** Redshift uses PL/pgSQL for stored procedures. These must be manually rewritten into a language supported by Snowflake, such as Snowflake Scripting (SQL), JavaScript, Python, or Java. This is often the most time-consuming part of the code conversion process.
  + **Translate SQL Functions:** Map Redshift-specific functions to their Snowflake counterparts. For example, Redshift’s GETDATE() becomes Snowflake’s CURRENT\_TIMESTAMP(). See Appendix 3 for common function mappings.
  + **Replace Maintenance Commands:** Scripts containing Redshift-specific commands like VACUUM, ANALYZE, and REINDEX should be removed, as Snowflake handles these maintenance tasks automatically.

### **Phase 4: Data Migration**[¶](#phase-4-data-migration "Link to this heading")

This phase focuses on the physical movement of historical data from your Redshift cluster to Snowflake tables. The most efficient method leverages Amazon S3 as an intermediate staging area.

**Your Actionable Steps:**

* **Unload Data from Redshift to S3:**

  + Use the Redshift UNLOAD command to export data from tables into a designated S3 bucket. This is highly parallelized and significantly faster than a SELECT query via a client tool.
  + Format data as Parquet or compressed CSV for optimal loading performance into Snowflake. Use the PARALLEL ON option to write multiple files.
* **Load Data from S3 into Snowflake:**

  + **Create External Stages:** In Snowflake, create an external stage object that points to the S3 bucket containing your unloaded data.
  + **Use the COPY INTO Command:** Use Snowflake’s COPY INTO <table> command to load the data from the S3 stage into the target Snowflake tables. This command is highly performant and scalable.
  + **Leverage a Sized-Up Warehouse:** Use a dedicated, larger virtual warehouse for the initial data load to accelerate the process, and then scale it down or suspend it afterward to manage costs.

### **Phase 5: Data Ingestion**[¶](#phase-5-data-ingestion "Link to this heading")

Once the historical data is migrated, you must re-engineer your ongoing data ingestion pipelines to feed data directly into Snowflake instead of Redshift.

**Your Actionable Steps:**

* **Migrate Batch ETL/ELT Jobs:**

  + Update existing ETL jobs (in tools like AWS Glue, Talend, or Informatica) to target Snowflake as the destination. This typically involves changing the connection details and updating any SQL overrides to use Snowflake’s dialect.
* **Implement Continuous Ingestion with Snowpipe:**

  + For continuous data streams (e.g., from Kinesis or application logs landing in S3), configure Snowpipe. Snowpipe automatically and efficiently loads new data files from S3 into Snowflake tables as they arrive, providing a near-real-time ingestion solution.
* **Utilize the Snowflake Ecosystem:**

  + Explore Snowflake’s native connectors for platforms like Kafka and Spark to simplify direct data streaming.

### **Phase 6: Reporting and Analytics**[¶](#phase-6-reporting-and-analytics "Link to this heading")

This phase involves redirecting all downstream applications, particularly BI and reporting tools, to query data from Snowflake.

**Your Actionable Steps:**

* **Update Connection Drivers:** Install and configure Snowflake’s ODBC/JDBC drivers on servers hosting your BI tools (e.g., Tableau Server, Power BI Gateway).
* **Redirect Reports and Dashboards:**

  + In your BI tools, change the data source connection from Redshift to Snowflake.
  + Test all critical reports and dashboards to ensure they function correctly.
* **Review and Optimize Queries:**

  + Some dashboards may contain custom SQL or database-specific functions. Review and refactor these queries to use Snowflake’s SQL dialect and take advantage of its performance features. Use the Query Profile tool in Snowflake to analyze and optimize slow-running reports.

### **Phase 7: Data Validation and Testing**[¶](#phase-7-data-validation-and-testing "Link to this heading")

Rigorous testing is essential to build business confidence in the new platform and ensure data integrity and performance meet expectations.

**Your Actionable Steps:**

* **Perform Data Validation:**

  + **Row Counts:** Compare row counts between source tables in Redshift and target tables in Snowflake.
  + **Cell-Level Validation:** For critical tables, perform a deeper validation by comparing aggregated values (e.g., SUM(), AVG(), MIN(), MAX()) or using checksums on key columns.
* **Conduct Query and Performance Testing:**

  + **Benchmark Queries:** Execute a representative set of queries against both Redshift and Snowflake and compare results and performance.
  + **BI Tool Performance:** Test the load times and interactivity of key dashboards connected to Snowflake.
* **User Acceptance Testing (UAT):**

  + Involve business users to validate their reports and perform their daily tasks using the new Snowflake environment. Gather feedback and address any issues.

### **Phase 8: Deployment**[¶](#phase-8-deployment "Link to this heading")

Deployment is the final cutover from Redshift to Snowflake. This process should be carefully managed to minimize disruption to business operations.

**Your Actionable Steps:**

* **Develop a Cutover Plan:**

  + Define the sequence of events for the cutover weekend or evening. This includes stopping ETL jobs pointing to Redshift, performing a final data sync, redirecting all connections, and validating system health.
* **Execute the Final Data Sync:**

  + Perform one last incremental data load to capture any data changes that occurred during the testing phase.
* **Go Live:**

  + Switch all production data pipelines and user connections from Redshift to Snowflake.
  + Keep the Redshift environment in a read-only state for a short period as a fallback before decommissioning it.
* **Decommission Redshift:**

  + Once the Snowflake environment is stable and validated in production, you can decommission your Redshift cluster to stop incurring costs.

### **Phase 9: Optimize and Run**[¶](#phase-9-optimize-and-run "Link to this heading")

This final phase is an ongoing process of managing performance, cost, and governance in your new Snowflake environment. The goal is to continuously refine your setup to maximize value.

**Your Actionable Steps:**

* **Implement Performance and Cost Optimization:**

  + **Right-Size Warehouses:** Continuously monitor workload performance and adjust virtual warehouse sizes up or down to meet SLAs at the lowest possible cost.
  + **Set Aggressive Auto-Suspend Policies:** Set the auto-suspend timeout for all warehouses to 60 seconds to avoid paying for idle compute time.
  + **Use Clustering Keys:** For very large tables (multi-terabyte), analyze query patterns and define clustering keys to improve the performance of highly filtered queries.
* **Establish Long-Term FinOps and Governance:**

  + **Monitor Costs:** Use Snowflake’s ACCOUNT\_USAGE schema and resource monitors to track credit consumption and prevent budget overruns.
  + **Refine Security:** Regularly audit roles and permissions to ensure the principle of least privilege is maintained. Implement advanced security features like Dynamic Data Masking and Row-Access Policies for sensitive data.

## **Appendix**[¶](#appendix "Link to this heading")

### **Appendix 1: Snowflake vs. Redshift Architecture**[¶](#appendix-1-snowflake-vs-redshift-architecture "Link to this heading")

| Feature | Amazon Redshift | Snowflake |
| --- | --- | --- |
| **Architecture** | Tightly coupled compute and storage (MPP) | Decoupled compute, storage, and cloud services (Multi-cluster, Shared Data) |
| **Storage** | Managed columnar storage on local SSDs attached to nodes | Centralized object storage (e.g., S3) with automatic micro-partitioning |
| **Compute** | Fixed-size cluster of nodes (Leader + Compute Nodes) | Elastic, on-demand virtual warehouses (compute clusters) |
| **Concurrency** | Limited by cluster size; queries can queue | High concurrency via multi-cluster warehouses that spin up automatically |
| **Scaling** | Scale by adding nodes (takes minutes to hours, involves data redistribution) | Instantly scale compute up/down/out (seconds); storage scales automatically |
| **Maintenance** | Requires manual VACUUM and ANALYZE commands | Fully managed; maintenance tasks are automated and run in the background |

### **Appendix 2: Data Type Mappings**[¶](#appendix-2-data-type-mappings "Link to this heading")

| Amazon Redshift | Snowflake | Notes |
| --- | --- | --- |
| SMALLINT | SMALLINT / NUMBER(5,0) |  |
| INTEGER | INTEGER / NUMBER(10,0) |  |
| BIGINT | BIGINT / NUMBER(19,0) |  |
| DECIMAL(p,s) / NUMERIC(p,s) | NUMBER(p,s) |  |
| REAL / FLOAT4 | FLOAT |  |
| DOUBLE PRECISION / FLOAT8 | FLOAT |  |
| BOOLEAN | BOOLEAN |  |
| CHAR(n) | CHAR(n) / VARCHAR(n) | Snowflake pads CHAR with spaces; VARCHAR is often preferred. |
| VARCHAR(n) | VARCHAR(n) | Max length in Snowflake is 16MB. |
| DATE | DATE |  |
| TIMESTAMP | TIMESTAMP\_NTZ | Snowflake separates timestamps with and without time zones. |
| TIMESTAMPTZ | TIMESTAMP\_TZ |  |
| GEOMETRY | GEOGRAPHY / GEOMETRY | Snowflake has native support for geospatial data. |
| SUPER | VARIANT | For semi-structured data (JSON). |

### **Appendix 3: SQL & Function Differences**[¶](#appendix-3-sql-function-differences "Link to this heading")

| Amazon Redshift | Snowflake | Notes |
| --- | --- | --- |
| GETDATE() | CURRENT\_TIMESTAMP() | Snowflake has several functions for current date/time. |
| SYSDATE | CURRENT\_TIMESTAMP() | SYSDATE is an alias for GETDATE in Redshift. |
| LISTAGG(expr, delim) | LISTAGG(expr, delim) | Syntax is similar but ordering behavior can differ. |
| NVL(expr1, expr2) | NVL(expr1, expr2) / IFNULL(expr1, expr2) | Functionality is identical. |
| DECODE(expr, search, result…) | DECODE(expr, search, result…) | Supported in both. CASE statements are more standard. |
| DATEDIFF(part, start, end) | DATEDIFF(part, start, end) | Supported, but date/time parts may have different names (e.g., yr vs year). |
| DATEADD(part, num, date) | DATEADD(part, num, date) | Supported, but date/time parts may have different names. |
| **Stored Procedures** | PL/pgSQL | Snowflake Scripting (SQL), JavaScript, Python, Java |
| **DDL Clauses** | DISTKEY, SORTKEY, ENCODE | None. Replaced by automatic micro-partitioning and optional Clustering Keys. |
| **Maintenance** | VACUUM, ANALYZE | None. Automated background services handle maintenance. |
| **Data Loading** | UNLOAD, COPY | COPY INTO, Snowpipe |

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

1. [Snowflake Migration Framework](#snowflake-migration-framework)
2. [Migration Phases](#migration-phases)
3. [Appendix](#appendix)