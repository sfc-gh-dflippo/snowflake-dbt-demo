## AI Summary Guide (SSIS to Snowflake Assessment)

Use this guide to **draft** an AI summary that gives a high-level, decision-ready overview of the SSIS workload before readers dive into individual packages. The audience is data engineers and solution architects preparing a migration to Snowflake.

### Summary Command (single source of truth)
Use this command to extract all signals in one place. It returns a well‑formatted text summary with:
1) AI analysis text per package
2) Classification counts
3) Top‑level summary (packages, connection managers, control flow components, data flow components, not supported elements)
4) Connection managers (name + creationName)

```bash
scai assessment etl summary
```

### Step: Draft AI Summary (HTML)
Add this step after generating `etl_assessment_analysis.json`:

1. Review the output signals (classifications, complexity, scripts, connection managers).
2. Write a medium AI summary in HTML using the template below.
3. Save it as `ai_ssis_summary.html` so it can be embedded into the SSIS report later.
4. Update the assessment JSON to point to the summary HTML:
```bash
scai assessment etl ai-summary <HTML_PATH>
```

### What to Look For
Focus on the most impactful signals from the summary command output:

**1) Workload Overview**
- Total package count, component count, estimated effort hours
- Business domains covered (e.g., finance, customer, operations, marketing)
- Major purposes (e.g., "supports a background check platform covering BI fact loading, MongoDB ingestion, partner integrations")

**2) Package Classification Breakdown**
- Distribution by classification: Ingestion / Data Transformation / Mixed / Configuration & Control
- Calculate percentages for each classification
- Identify the dominant pattern (e.g., "50% are Data Transformation packages")

**3) Sources and Destinations**
- **Sources:** Top source systems (SQL Server, Oracle, MySQL, MongoDB, APIs, files, SFTP, SharePoint, cloud storage)
- **Destinations:** Target systems (warehouse layers, reporting, operational, outbound feeds, files)
- **Classify as Internal vs External:** Internal = databases within the platform (SQL Server DBs); External = files, APIs, FTP, cloud storage, external databases
- Note data movement patterns (batch loads, incremental, CDC, staging to core, tiered destinations)

**4) Connection Manager Types**
- Identify all connection manager types from the summary output (OLEDB, FLATFILE, EXCEL, ADO.NET, ODBC, FTP, HTTP, custom/3rd-party)
- Highlight dominant types and notable external integrations (ZappySys, Attunity, custom connectors)
- Note any existing Snowflake connections (indicates partial migration)

**5) Complexity Drivers**
- **Unsupported Elements:** Count and list component types affected
- **3rd-Party Components:** ZappySys, Attunity, custom connectors (impact: High/Medium)
- **Script Tasks:** Count packages with C#/.NET scripts; note common use cases (Excel resolution, error handling, validation)
- **Tiered Destination Patterns:** Note batching strategies (e.g., 100K/25K/10K row batches)
- **ForEach Loops + DML:** Packages with iterative row-by-row operations
- **Most Complex Package:** Name, component count, key complexity factors (lookups, nested event handlers, etc.)

**6) Recommended Migration Approach**
- **Data Transformation packages:** Map to dbt models + Snowflake MERGE
- **Mixed packages:** Decompose into Snowpipe/Tasks (ingestion) + dbt (transformation) layers
- **Ingestion packages:** Replace with External stages, COPY INTO, Snowpipe
- **Configuration & Control:** Re-architect using Snowflake Tasks, stored procedures, notification integrations

**7) Key Risks and Dependencies**
- Pick the top 4 risks based on impact (2 high-severity red, 2 medium-severity amber)
- Common risks: ZappySys/3rd-party dependencies, script task prevalence, network share dependencies, stored procedure ecosystems, missing documentation, external APIs
- For each risk: provide a title and a short description of the impact and mitigation approach

### Connection Managers Overview (all packages)
The summary output already includes connection managers (name + creationName).
Use it to:
- Identify dominant connection types (OLEDB, FLATFILE, FTP/SFTP, HTTP/API, etc.).
- Highlight external systems and file-based integrations.
- Summarize common source/destination patterns for the AI summary.

### Writing Guidance
- **Use data from the summary command output** to populate tables with real counts and percentages
- **Keep narrative text minimal** - let structured tables and layouts carry the information
- **Use inline styles** (not CSS classes) since this is an embedded HTML snippet
- **Pick the top 4 risks** based on unsupported element counts, script prevalence, and external dependencies
- **Classify sources/destinations as Internal vs External** based on connection analysis (Internal: SQL Server, databases within the platform; External: files, APIs, FTP, cloud storage, external databases)
- **Use specific numbers** - don't say "many packages", say "43 packages"
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
  <p style="color: #64748b; font-size: 0.875rem; margin-bottom: 1.5rem;">High-level, decision-ready overview of the SSIS workload for data engineers and solution architects preparing a migration to Snowflake.</p>

  <!-- 1. Workload Overview -->
  <div style="background: #f0f9ff; border-left: 4px solid #29B5E8; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
    <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Workload Overview</h3>
    <p style="font-size: 0.9rem; color: #334155; line-height: 1.7; margin: 0;">
      [Short narrative paragraph with <strong>bold key numbers</strong>: package count, total components, estimated effort hours, and 1-2 sentences about what business domains/processes this workload covers.]
    </p>
  </div>

  <!-- 2. Package Classification Breakdown -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Package Classification Breakdown</h3>
  <div style="overflow-x: auto; margin-bottom: 1.5rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
      <thead>
        <tr style="background: #f1f5f9;">
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Classification</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Packages</th>
          <th style="text-align: center; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">% of Total</th>
          <th style="text-align: left; padding: 10px 14px; font-weight: 600; color: #334155; border-bottom: 2px solid #29B5E8;">Snowflake Target</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #F59E0B; border-radius: 3px; margin-right: 8px;"></span>Data Transformation</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">dbt models + Snowflake MERGE</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px;"><span style="display: inline-block; width: 10px; height: 10px; background: #8B5CF6; border-radius: 3px; margin-right: 8px;"></span>Mixed: Ingestion + Transformation</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="text-align: center; padding: 10px 14px;">[%]</td>
          <td style="padding: 10px 14px; color: #475569;">Snowpipe/Tasks + dbt layers</td>
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
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">[System Type (Internal/External)]</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">[Details/Database names]</td>
        </tr>
        <!-- Add more rows as needed -->
      </table>
    </div>
    <!-- Destinations -->
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem;">
      <h4 style="font-size: 0.85rem; font-weight: 600; color: #11567F; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.03em;">Destinations</h4>
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8125rem;">
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 6px 0; color: #334155; font-weight: 500;">[System Type]</td>
          <td style="padding: 6px 0; text-align: right; color: #64748b;">[Details]</td>
        </tr>
        <!-- Add more rows as needed -->
      </table>
    </div>
  </div>

  <!-- 4. Connection Manager Types -->
  <h3 style="font-size: 1rem; font-weight: 600; color: #11567F; margin-bottom: 0.75rem;">Connection Manager Types</h3>
  <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem;">
    <!-- Add badges for each connection type found. Use distinct colors. Examples: -->
    <span style="display: inline-block; background: #11567F; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">OLEDB</span>
    <span style="display: inline-block; background: #29B5E8; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">FLATFILE</span>
    <span style="display: inline-block; background: #22C55E; color: white; padding: 0.3rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">EXCEL</span>
    <!-- Add more as needed with different colors: #F59E0B, #7D44CF, #D45B90, #ef4444, #8A999E, #71D3DC, #94a3b8 -->
  </div>
  <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 1.5rem; line-height: 1.6;">
    [Short paragraph noting dominant patterns and any notable external integrations. E.g., "OLEDB dominates across source/destination/logging connections. Notable external integrations include ZappySys connectors for MongoDB, S3, and SMTP."]
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
          <td style="padding: 10px 14px; font-weight: 500;">Unsupported Elements</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: #fef2f2; color: #dc2626; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">[COUNT]</span></td>
          <td style="padding: 10px 14px; color: #475569;">[Component types and systems affected]</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">[Factor name]</td>
          <td style="text-align: center; padding: 10px 14px;"><span style="background: [#fef2f2 for high / #fff7ed for medium]; color: [#dc2626 for high / #c2410c for medium]; padding: 2px 10px; border-radius: 10px; font-weight: 600; font-size: 0.8rem;">[High/Medium/COUNT]</span></td>
          <td style="padding: 10px 14px; color: #475569;">[Details]</td>
        </tr>
        <!-- Add rows for: Script Tasks, Tiered Destination Patterns, ForEach Loops, Most Complex Package -->
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
          <td style="padding: 10px 14px; color: #475569;"><strong>dbt models</strong></td>
          <td style="padding: 10px 14px; color: #475569;">[Key considerations for this classification]</td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background: #fafafa;">
          <td style="padding: 10px 14px; font-weight: 500;">Mixed: Ingestion + Transform</td>
          <td style="text-align: center; padding: 10px 14px; font-weight: 600;">[COUNT]</td>
          <td style="padding: 10px 14px; color: #475569;"><strong>Snowpipe/Tasks + dbt</strong></td>
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
Write the summary as an HTML snippet file (not a full HTML page) so it can be embedded into the SSIS report:

- `ai_ssis_summary.html`

