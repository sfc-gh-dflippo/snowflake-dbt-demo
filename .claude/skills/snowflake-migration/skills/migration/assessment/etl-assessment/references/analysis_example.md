# AI Analysis Example Template

This document provides a reference example of a well-structured `ai_analysis` for SSIS package assessments. Use this as a template when writing analysis.

---

## Required Structure

Every analysis **MUST** contain these four sections, each as a separate paragraph:

1. **Classification:** - Category + evidence-based reasoning
2. **Sources & Destinations:** - Connection analysis (INTERNAL vs EXTERNAL)
3. **Purpose:** - What the package does and why
4. **Conversion:** - SnowConvert suitability assessment

**Critical:** Sections must be separated by blank lines (paragraph breaks).

---

## Quick Reference Template

Copy and fill in:

```
Classification: [Category]. [2-3 sentences explaining WHY this classification applies. Focus on reasoning: What is the primary purpose of the package? What does the SQL/Script logic reveal about its function? How do the connection configurations support this classification? Explain the evidence that led to this conclusion, not just a list of components.]

Sources & Destinations: [List all sources and destinations. Explicitly mark each as INTERNAL or EXTERNAL. Include database names, table names, and connection details. Identify source types for external connections (Cloud Service, API, File, External Database).]

Purpose: [Describe the business purpose and value of the package - why does it exist? What business need does it serve? What downstream processes or users depend on it? Avoid technical pipeline descriptions (the DAG shows that). Focus on business context, data consumers, and the functional outcome.]

Conversion: [Assess conversion path. State if Excellent/Good/Partial/Requires Connector Solution. Explain what converts (Control Flow → Tasks, Data Flow → dbt). For ingestion, identify source type and recommend connector solution (Snowpark Python, Fivetran, Snowpipe, Openflow). Include estimated effort hours with brief justification.]
```

---

## Good Example: Data Transformation Package

```
Classification: Data Transformation. The package is classified as Data Transformation because its primary purpose is to apply business logic to data that already exists within the data warehouse. The SQL logic reveals SCD Type 2 dimensional loading patterns - comparing incoming records against existing dimension data, tracking history with effective dates, and applying business rules for change detection. All connection managers point to internal databases within the same data warehouse environment, confirming no external data extraction is involved. The transformation focus is evident from the MERGE operations and derived column calculations that enrich the data rather than simply moving it.

Sources & Destinations: All connections are INTERNAL to the data warehouse environment. Sources include ODS.dbo.Customer staging table and DDS.dbo.DimCustomer for existing record lookup. Destinations are DDS.dbo.DimCustomer (INSERT for new records, UPDATE for existing via OLE DB Command) and control framework tables (ctlfw.ProcLog, ctlfw.PackageRestartPoint) for execution tracking.

Purpose: Maintains the CustomerDimension as the single source of truth for customer master data in the data warehouse. The package ensures that any changes to customer attributes in the operational system are captured with full history tracking, enabling analysts to query customer state at any point in time. This supports regulatory compliance requirements and historical trend analysis. The SCD Type 2 implementation preserves previous values when attributes change, which is critical for accurate revenue attribution in historical reports.

Conversion: Excellent conversion candidate. The Data Flow logic maps directly to a dbt incremental model using merge strategy - the change detection pattern becomes a JOIN with CASE expressions. Execute SQL Tasks convert to Snowflake Tasks or can be incorporated into dbt models. No external dependencies or Script Tasks requiring manual intervention.
```

---

## Good Example: Ingestion Package

```
Classification: Ingestion. The package is classified as Ingestion because its primary purpose is to bring data INTO the data warehouse from an external operational system. The connection manager configuration reveals an external server (navision-prod.corp.example.com) that exists outside the data warehouse environment. The SQL and Data Flow logic shows simple SELECT statements with basic column mapping rather than complex business transformations, confirming the focus is on data extraction rather than enrichment. The watermark-based incremental pattern is a common ingestion technique for capturing changed records from source systems.

Sources & Destinations: Source is EXTERNAL - Navision ERP database (navision-prod.corp.example.com) via OLE DB connection. This is a production transactional system outside the data warehouse. Destination is INTERNAL - ODS.dbo.SalesTransaction staging table on DWHPRODLSTN. The package also writes to control framework tables (ctlfw.ProcLog) for execution logging.

Purpose: Captures sales transaction data from the Navision ERP system to make it available for downstream analytics and reporting. This package runs as part of the nightly batch to ensure the data warehouse reflects the latest transactional activity. The incremental extraction approach minimizes load on the source ERP system while ensuring no transactions are missed. This data feeds into revenue reporting, sales performance dashboards, and financial reconciliation processes.

Conversion: Package logic converts but requires external connector solution. Source type: External SQL Server database. Since this is pure ingestion with minimal transformation, recommend Fivetran SQL Server connector or Snowflake Openflow to replicate SalesTransaction data directly to Snowflake staging. The watermark pattern and incremental logic can be handled by the connector's CDC capabilities. Estimated effort: 6 hours for connector setup + 2 hours for validation.
```

---

## Good Example: Configuration & Control Package

```
Classification: Configuration & Control. The package is classified as Configuration & Control because its primary purpose is orchestration and coordination rather than data movement. The DAG structure reveals a parent package that calls multiple child packages in a specific execution order - it acts as a conductor directing when other packages run. The SQL logic operates exclusively on metadata and control framework tables (BatchLog, PackageRestartPoint, ProcLog) rather than business data tables. The absence of Data Flows and the presence of Execute Package Tasks, Event Handlers, and Send Mail Tasks confirms this is about managing the ETL process itself, not transforming or moving business data.

Sources & Destinations: All control flow connections are INTERNAL to DWHPRODLSTN (JQETL, JGDDS databases). Execute Package Tasks reference child packages on the ETL server. Metadata tables accessed include ctlfw.BatchLog, ctlfw.PackageTasks, ctlfw.PackageRestartPoint, and dbo.ETLConfig. One Send Mail Task connects to SMTP server for failure notifications - this is an external dependency for alerting only, not data movement.

Purpose: Serves as the master controller for the nightly ETL batch, ensuring all data warehouse tables are refreshed in the correct order before business users begin their day. The package guarantees data consistency by enforcing dependencies - dimensions must complete before facts, facts before aggregates. The restart/recovery capability ensures that a failure at 3am doesn't require a full re-run; operations can resume from the last checkpoint, meeting the 6am SLA for data availability. Email notifications keep the support team informed of batch status.

Conversion: Good conversion candidate with moderate complexity. Execute Package Tasks convert to Snowflake Task DAG dependencies. Execute SQL Tasks operating on metadata tables convert to Snowflake stored procedures or inline SQL. Event Handlers require redesign - Snowflake Tasks lack OnPostExecute/OnError events; recommend Snowflake Alert + Notification Integration for failure alerting. SMTP integration needs external function or separate notification service. Estimated effort: 40 hours due to orchestration complexity and notification redesign.
```

---

## Good Example: Mixed Package

```
Classification: Mixed: Ingestion + Transformation. The package is classified as Mixed because it performs two distinct functions that require different handling. The first portion extracts data from an external cloud service (SharePoint) - this is ingestion that requires a connector solution. However, the package doesn't stop at extraction; subsequent Data Flows apply significant business logic including JOINs with dimension tables, calculated fields for revenue projections, and MERGE operations for incremental loading. This combination of external source extraction AND meaningful business transformation within the same package is the defining characteristic of a Mixed classification. Neither pure Ingestion nor pure Data Transformation accurately describes the full scope.

Sources & Destinations: Mixed EXTERNAL and INTERNAL sources. Primary source is EXTERNAL - SharePoint Online via OData connection (sharepoint.corp.example.com/sites/Sales/Lists/Opportunities). Source type: Cloud Service (SharePoint). Secondary sources are INTERNAL - DDS.dbo.DimCustomer and DDS.dbo.DimProduct for enrichment lookups. Destination is INTERNAL - DDS.dbo.FactSalesOpportunity via MERGE upsert pattern.

Purpose: Integrates sales pipeline data from SharePoint CRM into the enterprise data warehouse, enabling unified reporting across CRM and transactional systems. The package enriches raw opportunity records with customer segmentation and product categorization from master data dimensions, then applies business rules for revenue forecasting and probability scoring. This powers the executive sales pipeline dashboard and feeds into quarterly revenue projections used by finance for planning.

Conversion: Package converts with connector solution needed for SharePoint source. Recommend Fivetran SharePoint connector or Snowpark Python with Microsoft Graph API to land opportunity data in Snowflake staging. The transformation logic (Data Flows 2-3) converts directly to dbt models with JOIN and calculation logic. Recommend architectural separation: connector for ingestion, dbt for transformation. Estimated effort: 8 hours connector setup + 16 hours dbt model development = 24 hours total.
```

---

## Anti-Patterns to Avoid

### Bad: Missing Section Headers

```
This package loads customer data. It reads from the ODS database and writes to the DDS database. The transformations include derived columns and lookups. It's a good candidate for SnowConvert and should take about 10 hours.
```

**Problem:** No clear section headers. Missing Classification, Sources & Destinations, Purpose, Conversion labels.

---

### Bad: No Paragraph Separation

```
Classification: Data Transformation. This package loads dimension data. Sources & Destinations: All internal connections to DWHPRODLSTN. Purpose: Loads DimCustomer incrementally. Conversion: Good candidate for SnowConvert.
```

**Problem:** All sections on one line. Must have paragraph breaks between sections.

---

### Bad: Wrong Section Labels

```
Classification Reasoning: This is a transformation package because it moves data between internal tables.

Sources: ODS.dbo.Customer table
Destinations: DDS.dbo.DimCustomer table

Conversion Assessment: The package converts well to Snowflake.
```

**Problem:** Uses "Classification Reasoning:" instead of "Classification:", "Sources:" instead of "Sources & Destinations:", "Conversion Assessment:" instead of "Conversion:".