## AI Summary Guide (Informatica PowerCenter to Snowflake Assessment)

Use this guide to **draft** an AI summary that gives a high-level, decision-ready overview of the Informatica PowerCenter workload before readers dive into individual workflows. The audience is data engineers and solution architects preparing a migration to Snowflake.

### Conversion Mode Awareness

The assessment output JSON includes `metadata.conversion_mode` ("dbt" or "scripting"). **You MUST adapt all target references based on this mode:**

- **dbt mode:** Use "dbt models", "dbt project", "ref()", "Snowflake Tasks calling dbt"
- **scripting mode:** Use "stored procedures", "CALL statements", "Snowflake Scripting", "Snowflake Tasks with inline SQL". **Zero dbt references allowed.**

When filling the HTML template below, choose the appropriate target terminology for the active mode. Do NOT include both — pick one based on `conversion_mode`.

### Summary Command (single source of truth)
Use this command to extract all signals in one place. It returns a well‑formatted text summary with:
1) AI analysis text per workflow
2) Classification counts
3) Top‑level summary (workflows, mappings, components, EWIs, FDMs)

```bash
uv run python -m informatica_assessment_analyzer informatica <JSON_PATH> summary
```

### Step: Draft AI Summary (HTML)
Add this step after completing workflow analysis:

1. Review the output signals (classifications, complexity, custom transforms, sources/targets).
2. Write a medium AI summary in HTML using the template below.
3. Save it as `ai_informatica_summary.html` so it can be embedded into the Informatica report later.
4. Update the assessment JSON to point to the summary HTML:
```bash
uv run python -m informatica_assessment_analyzer informatica <JSON_PATH> ai-summary ai_informatica_summary.html
```

### What to Look For
Focus on the most impactful signals from the summary command output:

**1) Workload Overview**
- Total workflow count, mapping count, total components, estimated effort hours
- Business domains covered (e.g., finance, sales, operations, product)
- Major purposes (e.g., "ETL platform covering AR processing, GL aggregations, party management")

**2) Workflow Classification Breakdown**
- Distribution by classification: Data Transformation / Ingestion / Mixed: Ingestion + Transformation / Configuration & Control
- Calculate percentages for each classification
- Identify the dominant pattern (e.g., "65% are Data Transformation workflows")

**3) Sources and Destinations**
- **Sources:** Top source systems (Oracle, DB2, Teradata, Flat File, ODBC, Sybase, Informix)
- **Destinations:** Target systems (data warehouse layers, staging, reporting, operational)
- **Classify as Internal vs External:** Internal = databases within the data platform; External = flat files, FTP, APIs, external databases not being migrated
- Note data movement patterns (batch loads, incremental, staging to core)

**4) Connector & Session Types**
- Identify database connection types from SOURCE/TARGET DATABASETYPE attributes
- Highlight dominant connection types and notable external integrations
- Note any file-based sources (flat files, XML) requiring alternative ingestion solutions

**5) Complexity Drivers**
- **Not Supported Elements:** Count and list component types affected
- **Custom Transformations:** Java Transformation, Custom Transformation (impact: High — requires manual rewrite)
- **SQL Overrides:** Source Qualifier or Lookup with custom SQL (impact: Medium — needs manual review)
- **Complex Orchestration:** Workflows with decisions, timers, conditional routing
- **Most Complex Workflow:** Name, mapping count, key complexity factors

**6) Recommended Migration Approach**

Adapt recommendations based on `informatica_target`:

**dbt mode:**
- **Data Transformation workflows:** Mappings → dbt models, Workflow → Snowflake Tasks
- **Mixed workflows:** Decompose into ingestion (Snowpipe/Fivetran) + transformation (dbt) layers
- **Ingestion workflows:** Replace with External stages, COPY INTO, Snowpipe, or Fivetran connectors
- **Configuration & Control:** Re-architect using Snowflake Tasks, stored procedures, notification integrations

**scripting mode:**
- **Data Transformation workflows:** Mappings → Snowflake stored procedures, Workflow → Snowflake Tasks with CALL statements
- **Mixed workflows:** Decompose into ingestion (Snowpipe/Fivetran) + transformation (stored procedures) layers
- **Ingestion workflows:** Replace with External stages, COPY INTO, Snowpipe, or Fivetran connectors
- **Configuration & Control:** Re-architect using Snowflake Tasks with inline SQL, stored procedures, notification integrations

**7) Key Risks and Dependencies**
- Pick the top 4 risks based on impact (2 high-severity red, 2 medium-severity amber)
- Common risks: Custom/Java Transformation dependencies, SQL override complexity, external database connections, file-based ingestion patterns, complex orchestration logic
- For each risk: provide a title and a short description of the impact and mitigation approach

### Writing Guidance
- **Use data from the summary command output** to populate tables with real counts and percentages
- **Keep narrative text minimal** - let structured tables and layouts carry the information
- **Use inline styles** (not CSS classes) since this is an embedded HTML snippet
- **Pick the top 4 risks** based on not-supported element counts, custom transform prevalence, and external dependencies
- **Classify sources/destinations as Internal vs External** based on DATABASETYPE analysis
- **Use specific numbers** - don't say "many workflows", say "8 workflows"
- **Match donut chart colors** in the classification table:
  - Data Transformation: `#F59E0B` (orange)
  - Mixed: Ingestion + Transformation: `#8B5CF6` (purple)
  - Ingestion: `#29B5E8` (blue)
  - Configuration & Control: `#22C55E` (green)
  - Unclassified: `#9CA3AF` (gray)

### HTML Template (structured layout)
Use this structure with visual sections so it can be embedded into the HTML report:

```html
<section id="ai-summary" class="section">
  <h2 style="font-size: 1.5rem; font-weight: 700; color: #11567F; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid #29B5E8;">AI Summary</h2>
  <p style="color: #64748b; font-size: 0.875rem; margin-bottom: 1.5rem;">High-level, decision-ready overview of the Informatica PowerCenter workload for data engineers and solution architects preparing a migration to Snowflake.</p>

  <!-- 1. Workload Overview -->
  <div style="background: #f0f9ff; border-left: 4px solid #29B5E8; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
    <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Workload Overview</h3>
    <p style="font-size: 0.9rem; color: #334155; line-height: 1.7; margin: 0;">
      [Short narrative paragraph with <strong>bold key numbers</strong>: workflow count, total mappings, total components, estimated effort hours, and 1-2 sentences about what business domains/processes this workload covers.]
    </p>
  </div>

  <!-- 2. Workflow Classification Breakdown -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Workflow Classification Breakdown</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Classification</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Workflows</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">% of Total</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Snowflake Target</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #F59E0B; border-radius: 3px; margin-right: 8px;"></span>Data Transformation</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">dbt models + Snowflake Tasks (dbt) / Stored procedures + Tasks (scripting)</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #8B5CF6; border-radius: 3px; margin-right: 8px;"></span>Mixed: Ingestion + Transformation</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">Snowpipe/Fivetran + dbt layers (dbt) / Snowpipe/Fivetran + stored procs (scripting)</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #29B5E8; border-radius: 3px; margin-right: 8px;"></span>Ingestion</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">External stages, COPY INTO, Snowpipe</td>
        </tr>
        <tr>
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #22C55E; border-radius: 3px; margin-right: 8px;"></span>Configuration &amp; Control</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">Snowflake Tasks, stored procedures</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 3. Sources & Destinations -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Sources &amp; Destinations</h3>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
    <!-- Sources -->
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem;">
      <h4 style="font-size: 0.85rem; font-weight: 600; color: #11567F; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.03em;">Sources</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8125rem;">
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">[Database Type (Internal/External)]</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">[Details/Schema names]</td>
        </tr>
        <!-- Add more rows as needed -->
      </table>
    </div>
    <!-- Destinations -->
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem;">
      <h4 style="font-size: 0.85rem; font-weight: 600; color: #11567F; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.03em;">Destinations</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8125rem;">
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">[Database Type]</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">[Details]</td>
        </tr>
        <!-- Add more rows as needed -->
      </table>
    </div>
  </div>

  <!-- 4. Connector & Session Types -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Connector Types</h3>
  <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
    <!-- Add badges for each database type found. Use distinct colors. Examples: -->
    <span style="display: inline-block; background: #11567F; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">Oracle</span>
    <span style="display: inline-block; background: #29B5E8; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">Teradata</span>
    <span style="display: inline-block; background: #22C55E; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">Flat File</span>
    <!-- Add more as needed with different colors: #F59E0B, #7D44CF, #D45B90, #ef4444, #8A999E, #71D3DC, #94a3b8 -->
  </div>
  <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 1.5rem; line-height: 1.6;">
    [Short paragraph noting dominant database types and any notable external integrations. E.g., "Teradata dominates as the primary source/target. Notable external patterns include flat file ingestion from FTP and ODBC connections to operational Oracle databases."]
  </p>

  <!-- 5. Complexity Drivers -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Complexity Drivers</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Complexity Factor</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Impact</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #FF9F36;">Details</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">Not Supported Elements</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fef2f2; color: #dc2626; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">[COUNT]</span></td>
          <td style="padding: 10px 14px; color: #475569;">[Component types and systems affected]</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">[Factor name]</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: [#fef2f2 for high / #fff7ed for medium]; color: [#dc2626 for high / #c2410c for medium]; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">[High/Medium/COUNT]</span></td>
          <td style="padding: 10px 14px; color: #475569;">[Details]</td>
        </tr>
        <!-- Add rows for: Custom Transformations, SQL Overrides, Complex Orchestration, Most Complex Workflow -->
      </tbody>
    </table>
  </div>

  <!-- 6. Recommended Migration Approach -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Recommended Migration Approach</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Classification</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Count</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Migration Strategy</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #22C55E;">Key Considerations</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">Data Transformation</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="padding: 10px 14px; color: #475569;"><strong>dbt models + Snowflake Tasks</strong> (dbt) / <strong>Stored procedures + Tasks with CALL</strong> (scripting)</td>
          <td style="padding: 10px 14px; color: #475569;">[Key considerations for this classification]</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">Mixed: Ingestion + Transform</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="padding: 10px 14px; color: #475569;"><strong>Snowpipe/Fivetran + dbt</strong> (dbt) / <strong>Snowpipe/Fivetran + stored procs</strong> (scripting)</td>
          <td style="padding: 10px 14px; color: #475569;">[Key considerations]</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px; font-weight: 500;">Ingestion</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="padding: 10px 14px; color: #475569;"><strong>External stages + COPY INTO</strong></td>
          <td style="padding: 10px 14px; color: #475569;">[Key considerations]</td>
        </tr>
        <tr>
          <td style="padding: 10px 14px; font-weight: 500;">Configuration &amp; Control</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="padding: 10px 14px; color: #475569;"><strong>Re-architect</strong></td>
          <td style="padding: 10px 14px; color: #475569;">[Key considerations]</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 7. Key Risks -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Key Risks</h3>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.5rem;">
    <!-- High severity risks (red) -->
    <div style="background: #fef2f2; border-left: 4px solid #ef4444; border-radius: 8px; padding: 1rem 1.25rem;">
      <div style="font-weight: 600; color: #991b1b; font-size: 0.9rem; margin-bottom: 0.4rem;">[Risk Title]</div>
      <div style="font-size: 0.825rem; color: #7f1d1d; line-height: 1.6;">[Short description of the risk and its impact]</div>
    </div>
    <div style="background: #fef2f2; border-left: 4px solid #ef4444; border-radius: 8px; padding: 1rem 1.25rem;">
      <div style="font-weight: 600; color: #991b1b; font-size: 0.9rem; margin-bottom: 0.4rem;">[Risk Title]</div>
      <div style="font-size: 0.825rem; color: #7f1d1d; line-height: 1.6;">[Short description]</div>
    </div>
    <!-- Medium severity risks (amber) -->
    <div style="background: #fff7ed; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1rem 1.25rem;">
      <div style="font-weight: 600; color: #92400e; font-size: 0.9rem; margin-bottom: 0.4rem;">[Risk Title]</div>
      <div style="font-size: 0.825rem; color: #78350f; line-height: 1.6;">[Short description]</div>
    </div>
    <div style="background: #fff7ed; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1rem 1.25rem;">
      <div style="font-weight: 600; color: #92400e; font-size: 0.9rem; margin-bottom: 0.4rem;">[Risk Title]</div>
      <div style="font-size: 0.825rem; color: #78350f; line-height: 1.6;">[Short description]</div>
    </div>
  </div>
</section>
```

### Output File
Write the summary as an HTML snippet file (not a full HTML page) so it can be embedded into the Informatica report:

- `ai_informatica_summary.html`
