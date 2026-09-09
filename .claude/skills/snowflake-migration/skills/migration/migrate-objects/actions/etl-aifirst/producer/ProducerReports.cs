// ETL LINEAGE AND REPORTS FOR THE CALLABLE DRIVER.
//
// WHAT WAS MISSING AND WHY NOBODY NOTICED. Measured on `poc/blind-run/runS`: 186 files per platform tree,
// four trees, and ZERO lineage rows plus ZERO report/assessment artifacts. The capability was never
// broken — it was never carried across. The vertical-slice path produced 18 of 18 DataStage lineage rows,
// but it did so in TWO processes: an MSTest fixture wrote `producer-handoff.json`, and
// `poc/spikes/slice-reports-registry/Program.cs` read that file and drove the real writers. The callable
// driver is neither of those programs, so it inherited neither half. This file collapses both into the
// one process that actually ships.
//
// THE DOOR IS `IObjectReferenceCalculator.AddDirect`, whose own doc comment names this exact case:
// "bypassing the AST-based tracker/visitor machinery. Used by components that construct lineage entries
// from non-AST sources". A producer has no AST, so this is the supported route and not a workaround.
// The engine takes it itself for Informatica in
// `Assemblies/EtlToDbt/InfPowerCenter/InfPcNonAstLineageEmissionTask.cs`.
//
// THE DEDUP TRAP, PAID FOR ONCE ALREADY. `AddDirect` -> `AddReferenceIfNotExists` keys on
// `(caller_code_unit_full_name, referenced_element_full_name, relation_type)` and NOTHING ELSE — not the
// line, not the element id. When DataStage model names collided, 18 edges became 6 rows with no error and
// no log, at the same time as `DbtModelsWriter` silently overwrote 20 of 29 models (ENG-015). So this
// file ASSERTS the names it is about to use are distinct per node and reports the arithmetic
// (`edges N -> rows M`), because "some rows appeared" is exactly the reading that hid the first loss.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Logging;
using Mobilize.Assessment.AssessmentMode;
using Mobilize.Snow.Assessment;
using Mobilize.Snow.Assessment.AssessmentMode.Calculators;
using Mobilize.Snow.Assessment.AssessmentMode.ETLAndReporting;
using Mobilize.Snow.Assessment.AssessmentMode.ETLReplatform;
using Mobilize.Snow.Assessment.AssessmentMode.Writers;
using Mobilize.Snow.Assessment.Db;
using Mobilize.Snow.Common;
using Mobilize.Snow.Common.Dbt;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.Models;

/// <summary>
/// Drives the three producer-drivable ETL reports — <c>ObjectReferences</c>, <c>ETL.Elements</c> and
/// <c>ETL.Issues</c> — from the run that just happened, using the engine's own calculators and writers.
/// </summary>
internal static class ProducerReports
{
  private const string PartitionKey = "Development Session";
  private const string SessionTimestamp = "NA";
  private const string CallerCodeUnit = "ETL PROCESS";
  private const string NotApplicable = "N/A";

  /// <summary>Relation type for a model-to-model edge, matching the vertical slice's rows.</summary>
  private const string DbtRefRelation = "DBT REF";

  /// <summary>Relation type for a source stage reading a physical relation. Matches the engine's own
  /// SSIS/Informatica ObjectReferences rows, which say <c>OPEN ROWSET</c> / <c>SELECT - FROM</c>.</summary>
  private const string ReadRelation = "SELECT - FROM";

  /// <summary>Relation type for a target stage writing a physical relation.</summary>
  private const string WriteRelation = "INSERT";

  /// <summary>
  /// Relation types for an edge stated by a MODEL-AUTHORED (tier-3) model file rather than by the IR.
  /// </summary>
  /// <remarks>
  /// <para>
  /// SEPARATE RELATION TYPES, AND NOT A COSMETIC CHOICE. <c>AddDirect</c> -> <c>AddReferenceIfNotExists</c>
  /// keys on <c>(caller_code_unit_full_name, referenced_element_full_name, relation_type)</c>. If a
  /// tier-3 row reused <c>DBT REF</c> it would collide with the IR row for the same edge and be dropped
  /// SILENTLY -- the same dedup trap that turned 18 DataStage edges into 6 rows. With its own relation
  /// type the row survives, and the column states its provenance, so a consumer can tell "the producer
  /// identified this edge" from "the SQL that actually shipped contains this ref()".
  /// </para>
  /// <para>
  /// Those two are not the same claim and this project has a measured case where they disagree in each
  /// direction -- see the OVER-STATEMENT and UNDER-STATEMENT notes on <see cref="BuildLineageRows"/>.
  /// Folding them into one relation type would delete the only evidence of the difference.
  /// </para>
  /// </remarks>
  private const string ModelAuthoredRefRelation = "DBT REF (MODEL-AUTHORED)";

  /// <summary>Relation type for a physical read stated by a model-authored model file.</summary>
  private const string ModelAuthoredReadRelation = "SELECT - FROM (MODEL-AUTHORED)";

  /// <summary>
  /// The caller-code-unit label for a model-authored row, so provenance is legible in the row itself
  /// and not only in the relation type.
  /// </summary>
  private const string ModelAuthoredCallerCodeUnit = "ETL PROCESS (MODEL-AUTHORED)";

  /// <summary>The tier-3 stamp <c>ai_fill.py</c> writes into every model it authors.</summary>
  private const string ModelAuthoredMarker = "SSC-AI-AUTHORED";

  private static readonly System.Text.RegularExpressions.Regex RefCall =
    new(@"\{\{\s*ref\(\s*'([^']+)'\s*\)\s*\}\}", System.Text.RegularExpressions.RegexOptions.Compiled);

  private static readonly System.Text.RegularExpressions.Regex SourceCall =
    new(@"\{\{\s*source\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)\s*\}\}",
      System.Text.RegularExpressions.RegexOptions.Compiled);

  /// <summary>
  /// Captures every engine issue code rendered into model SQL, including blocking
  /// <c>!!!RESOLVE EWI!!!</c> comments and non-blocking <c>--** SSC-FDM-...</c> comments. Limiting
  /// reconciliation to the first shape let foreign-dialect FDMs bypass the gate entirely.
  /// </summary>
  private static readonly System.Text.RegularExpressions.Regex EngineIssueMarker =
    new(@"(?:!!!RESOLVE EWI!!! /\*\*\*|--\*\*)\s*(SSC-(?:EWI|FDM|PRF)-[A-Za-z0-9-]+)\b",
      System.Text.RegularExpressions.RegexOptions.Compiled);

  /// <summary>What one report attempt produced. Read from DISK, never from the writer's return value.</summary>
  internal sealed record ReportOutcome(string Name, bool Written, int DataRows, bool IsPlaceholder, string? Error);

  /// <summary>Everything the driver needs to print and everything stage 4 needs to gate on.</summary>
  internal sealed record ReportsResult(
    IReadOnlyList<ReportOutcome> Reports,
    int LineageRowsOffered,
    int LineageRowsStored,
    IReadOnlyDictionary<string, int> LineageRowsByRelation,
    int EwiRowsOffered,
    int FdmRowsOffered,
    int ElementRowsOffered,
    IReadOnlyList<string> Warnings,
    int ReconciliationMarkersChecked,
    IReadOnlyList<string> ReconciliationFailures)
  {
    internal int PopulatedReports => this.Reports.Count(r => r.Written && !r.IsPlaceholder);

    internal int PlaceholderReports => this.Reports.Count(r => r.Written && r.IsPlaceholder);

    internal int MissingReports => this.Reports.Count(r => !r.Written);
  }

  /// <summary>
  /// Builds and writes the reports into <c>&lt;outRoot&gt;/Reports</c>, mirroring where a real
  /// SnowConvert run puts them (measured against <c>poc/blind-run/runA/*/out/Reports</c>).
  /// </summary>
  /// <param name="outRoot">The migration output root.</param>
  /// <param name="pipeline">The hydrated data-flow graph.</param>
  /// <param name="modelNamesByNodeId">dbt model name per node id.</param>
  /// <param name="sourceRelationsByNodeId">Physical relation read per source node id.</param>
  /// <param name="modelFileStems">
  /// The stems of the model files actually on disk. Used to resolve each producer model name to the
  /// name a <c>ref()</c> in the tree will use.
  /// </param>
  /// <param name="modelSqlByFileStem">
  /// The TEXT of every model file actually on disk, keyed by the same stem as <paramref
  /// name="modelFileStems"/>. Read once by the caller (Program.cs, right after
  /// <c>DbtModelsWriter.WriteModels</c>) rather than re-read here, for the same reason
  /// <paramref name="modelFileStems"/> is passed in rather than re-derived: one read of the shipped
  /// tree, not two that can drift. Used ONLY by the reconciliation gate below, to find every
  /// engine EWI/FDM/PRF marker actually shipped and check it against what this method is about to
  /// write into ETL.Elements/ETL.Issues.
  /// </param>
  /// <param name="unsupportedNodes">Nodes the producer declared unmappable, as (id, name, nativeKind).</param>
  /// <param name="assessment">The recording assessment builder the translators wrote to.</param>
  /// <param name="ewiInformation">The engine's EWI metadata service, for code/severity/description.</param>
  /// <param name="sourceDocumentName">The source document file name, for the FileName column.</param>
  /// <param name="platformId">The producer's own platform id, recorded in Additional Info.</param>
  /// <param name="logger">A CAPTURING logger: the writers swallow every exception into a LogError.</param>
  /// <returns>The measured outcome.</returns>
  internal static ReportsResult Emit(
    string outRoot,
    DagPipeline<Transformation> pipeline,
    IReadOnlyDictionary<string, string> modelNamesByNodeId,
    IReadOnlyDictionary<string, string> sourceRelationsByNodeId,
    IReadOnlyList<string> modelFileStems,
    IReadOnlyDictionary<string, string> modelSqlByFileStem,
    IReadOnlyList<(string Id, string Name, string NativeKind)> unsupportedNodes,
    RecordingEtlAssessmentBuilder assessment,
    IEwiInformationService ewiInformation,
    string sourceDocumentName,
    string platformId,
    ILogger logger)
  {
    var reportsDir = Path.Combine(outRoot, "Reports");
    Directory.CreateDirectory(reportsDir);

    var warnings = new List<string>();
    var setup = new AssessmentSetup { SessionTimestamp = SessionTimestamp };
    var migrationData = new ProducerMigrationDataService(
      etlInputPath: sourceDocumentName,
      partitionKey: PartitionKey,
      migrationId: "AIFIRST-" + platformId.ToUpperInvariant(),
      sessionTimestamp: SessionTimestamp);
    var configProvider = new ProducerAssessmentConfigurationProvider();
    var telemetry = new RecordingSnowTelemetry();

    // ---- lineage ---------------------------------------------------------------------------------
    var rows = BuildLineageRows(
      pipeline, modelNamesByNodeId, sourceRelationsByNodeId, modelFileStems, sourceDocumentName, warnings);

    // TIER-3 MODELS WERE INVISIBLE HERE, and the cause was ORDERING, not resolution.
    //
    // MEASURED: the Pentaho tree contains `stg_raw__read_customer` with a live
    // `source('raw','CUSTOMER')` call and there was NO row for it, because that model was authored by
    // `ai_fill.py` at stage 3b -- AFTER this emitter ran. Lineage was built from the IR, and tier-3 SQL
    // is not in the IR, so every tier-3 model was absent from the graph it belongs to.
    //
    // The owner decision that makes this a defect rather than a known limitation is recorded in
    // CONFIDENCE.yml as `an-out-of-engine-flow-is-required-the-IR-happy-path-is-not-enough`: if the
    // out-of-engine flow is first-class, a model-authored artifact has to be as fully represented as an
    // engine-authored one.
    //
    // SCRAPED FROM THE SHIPPED SQL, not from the sidecar. The sidecar states what a model OFFERED;
    // `ai_fill` writes it only over a model that was already degraded, so the sidecar is not evidence
    // that the SQL shipped. The file on disk is.
    //
    // On the stage-3 call this finds NOTHING, because ai_fill has not run yet -- so the two callers
    // share one lineage implementation rather than having a second one for the re-emit.
    rows.AddRange(ScrapeModelAuthoredRows(outRoot, sourceDocumentName));

    var byRelation = rows
      .GroupBy(r => r.RelationType, StringComparer.Ordinal)
      .ToDictionary(g => g.Key, g => g.Count(), StringComparer.Ordinal);

    var (lineageReport, stored) = WriteLineage(
      reportsDir, rows, migrationData, configProvider, setup, warnings, logger);

    // ---- ETL.Issues: the EWIs the engine's own translators raised ---------------------------------
    // Not invented here. Every row comes from RecordingEtlAssessmentBuilder, which received exactly
    // what NoOpEtlAssessmentBuilder used to discard.
    //
    // ONE DEGRADATION REGISTERS TWICE, WITH TWO DIFFERENT KEYS, and the first version of this report
    // emitted both as component rows. READ:
    //   * `TransformationUnitTranslator.GenerateUnsupportedElementConversion` calls
    //     `RegisterEwi(transformation.Id, ...)`  -> keyed by the ELEMENT.
    //   * `UnsupportedTransformationTranslator` then calls `ctx.AddIssueToElement(...)`, which routes
    //     to `SqlUtils.AddIssueToElement(..., elementName: ctx.CurrentContextName, ...)`
    //     -> keyed by the CONTAINER, i.e. the dbt project name.
    // So SSIS produced two rows for one swallowed component, the second naming a DIRECTORY where a
    // component belongs. MEASURED against the engine's own runA output for the same document: FOUR
    // rows, all keyed by component, none by container.
    //
    // The engine's row rule is in `EtlAssessmentBuilderForPipelineContainer.RegisterPendingEntries`,
    // which iterates `namesToCheck` — a set populated by RegisterSubtype / RegisterStatus /
    // RegisterDeclarationName and NOT by RegisterEwi. A container-keyed EWI therefore never becomes a
    // row there either. This reproduces that rule from the same data: a registration is a component
    // row when its key is an element the producer declared; otherwise it is counted and named as
    // container-scoped, never silently dropped.
    var knownElementIds = new HashSet<string>(
      pipeline.Nodes.Select(n => n.Id).Concat(unsupportedNodes.Select(u => u.Id)),
      StringComparer.Ordinal);

    // COMPUTED ONCE, READ BY BOTH THE ETL.ISSUES LOOP BELOW (INDIRECTLY, VIA assessment.Issues) AND
    // ETL.ELEMENTS' CodesFor, AND BY THE RECONCILIATION GATE AT THE END. Hoisted above both instead of
    // being computed a second time inside the Elements try-block, so a mid-run divergence between "what
    // Elements saw" and "what the gate checked" cannot be a computation-order artifact.
    var issuesByComponent = assessment.GetCollectedIssuesByComponent();

    var ewiRows = 0;
    var fdmRows = 0;
    var containerScoped = 0;
    // (FullName, Code) pairs that actually became a row in ETL.Issues -- i.e. survived BOTH the
    // knownElementIds check and IsForeignDialectBleed. The reconciliation gate needs this exact set,
    // not a re-derivation of the filters, because a re-derivation that drifts from the real filter
    // would let the gate pass on a report it never actually inspected.
    var issuesReportedInEtlIssues = new HashSet<(string FullName, string Code)>();
    var issuesReport = new ReportOutcome("ETL.Issues." + SessionTimestamp + ".csv", false, 0, false, null);
    try
    {
      var calculator = new EtlReplatformIssuesCalculator();
      IEtlReplatformIssueCalculator issueSink = calculator;
      var foreignBleedSkipped = 0;
      foreach (var (fullName, issueName, args) in assessment.Issues)
      {
        var code = SafeCode(ewiInformation, issueName);
        if (!knownElementIds.Contains(fullName))
        {
          containerScoped++;
          continue;
        }

        if (IsForeignDialectBleed(code, platformId))
        {
          foreignBleedSkipped++;
          continue;
        }

        if (IsFdmCode(code))
        {
          fdmRows++;
        }
        else
        {
          ewiRows++;
        }

        issueSink.Add(new EtlReplatformIssuesReportItem
        {
          SessionID = PartitionKey,
          Severity = Safe(() => ewiInformation.GetSeverity(issueName), "Unknown"),
          Code = code,
          Name = Safe(() => ewiInformation.GetFriendlyName(issueName, args), issueName.ToString()),
          Description = Safe(() => ewiInformation.GetDescription(issueName, args), string.Empty),
          ParentFileName = sourceDocumentName,
          ComponentFullName = fullName,
          MigrationID = migrationData.MigrationId,
        });
        issuesReportedInEtlIssues.Add((fullName, code));
      }

      if (containerScoped > 0)
      {
        warnings.Add(
          $"{containerScoped} issue registration(s) were keyed by the CONTAINER context "
          + "(SqlUtils.AddIssueToElement passes ctx.CurrentContextName), not by an element. Counted "
          + "here, not emitted as component rows -- the engine's own builder does not emit them either.");
      }

      if (foreignBleedSkipped > 0)
      {
        warnings.Add(
          $"{foreignBleedSkipped} issue registration(s) skipped as foreign-dialect bleed on platform "
          + $"'{platformId}' (owner 2026-08-13). AIM coexistence fills ETL.Issues later.");
      }

      var writer = new EtlReplatformIssuesReportWriter(
        configProvider,
        setup,
        new CalculatorBackedWriterModel(calculator),
        new EtlIssuesReportItemConverter(),
        migrationData,
        logger,
        telemetry);
      issuesReport = Inspect(reportsDir, writer.FormattedReportName, writer.GenerateReport(null!, null!, logger, reportsDir));
    }
    catch (Exception ex)
    {
      issuesReport = issuesReport with { Error = $"{ex.GetType().Name}: {ex.Message}" };
      warnings.Add($"ETL.Issues threw: {ex.GetType().Name}: {ex.Message}");
    }

    // ---- ETL.Elements: the element census ---------------------------------------------------------
    var elementRows = 0;
    var elementsReport = new ReportOutcome("ETL.Elements." + SessionTimestamp + ".csv", false, 0, false, null);
    try
    {
      var calculator = new EtlReplatformCalculator();
      IEtlReplatformCalculator elementSink = calculator;

      foreach (var node in pipeline.Nodes)
      {
        var codes = CodesFor(issuesByComponent, node.Id, ewiInformation);
        elementSink.Add(ElementRow(
          node.Id,
          node.Element.GetType().Name,
          node.Type,
          sourceDocumentName,
          StatusFor(assessment, node.Id, node.Element, codes.Count > 0),
          codes,
          platformId,
          inGraph: true,
          columns: node.Element.OutputColumns.Count,
          migrationData.MigrationId));
        elementRows++;
      }

      // The nodes the producer deliberately kept OUT of the graph are still elements it identified.
      // Omitting them would make the census agree with the model count by construction, which is the
      // one thing a census must not do.
      foreach (var (id, name, nativeKind) in unsupportedNodes)
      {
        elementSink.Add(ElementRow(
          id,
          string.IsNullOrEmpty(nativeKind) ? name : nativeKind,
          "not-in-graph",
          sourceDocumentName,
          EtlReplatformStatus.NotSupported,
          [],
          platformId,
          inGraph: false,
          columns: 0,
          migrationData.MigrationId));
        elementRows++;
      }

      var writer = new EtlReplatformReportWriter(
        configProvider,
        setup,
        new CalculatorBackedWriterModel(calculator),
        new EtlReplatformReportItemConverter(),
        migrationData,
        logger,
        telemetry);
      elementsReport = Inspect(reportsDir, writer.FormattedReportName, writer.GenerateReport(null!, null!, logger, reportsDir));
    }
    catch (Exception ex)
    {
      elementsReport = elementsReport with { Error = $"{ex.GetType().Name}: {ex.Message}" };
      warnings.Add($"ETL.Elements threw: {ex.GetType().Name}: {ex.Message}");
    }

    // ---- RECONCILIATION GATE: does every SQL marker have a report row that agrees with it? ---------
    // THE CLASS THIS FILE CLOSES, not just the SSC-EWI-INF0087 instance that surfaced it. Every prior
    // section above builds ETL.Elements/ETL.Issues from `assessment` and `issuesByComponent`; this
    // section is the only place that also reads the SQL ACTUALLY SHIPPED and checks the two against
    // each other. A marker with no matching report row, or a report row naming a code illegal for this
    // platform, is a HARD FAILURE recorded in `ReconciliationFailures` -- never fixed by deleting the
    // marker, downgrading a status, or filtering the code out of a report. The marker is truth; the
    // report has to catch up, or this method has to say, loudly, that it did not.
    var (reconciliationChecked, reconciliationFailures) = ReconcileMarkersAndReports(
      pipeline, modelNamesByNodeId, modelFileStems, modelSqlByFileStem, issuesByComponent,
      issuesReportedInEtlIssues, ewiInformation, platformId);

    return new ReportsResult(
      [lineageReport, elementsReport, issuesReport],
      rows.Count,
      stored,
      byRelation,
      ewiRows,
      fdmRows,
      elementRows,
      warnings,
      reconciliationChecked,
      reconciliationFailures);
  }

  /// <summary>
  /// THE GATE ITSELF. Walks every model file actually on disk (<paramref name="modelSqlByFileStem"/>),
  /// finds every engine EWI/FDM/PRF marker the translators left in the shipped SQL, and checks each
  /// one against what this method's caller is about to write into ETL.Elements and
  /// ETL.Issues.
  /// </summary>
  /// <remarks>
  /// <para>
  /// WHY A SEPARATE PASS OVER THE SQL, RATHER THAN TRUSTING <paramref name="issuesByComponent"/> ALONE.
  /// <paramref name="issuesByComponent"/> is built from the SAME registrations ETL.Elements reads, so a
  /// bug in registration (Fact 1 of SNOW-3979042: a registration keyed by the CONTAINER instead of the
  /// element) is invisible to a check that only re-reads that structure -- it would agree with itself
  /// perfectly while both are wrong. The SQL on disk is the one artifact upstream of every registration
  /// bug there is: the engine's translator wrote the marker whether or not <c>ctx.AddIssueToElement</c>
  /// filed it under the right name afterward. Checking the marker against the report is therefore a
  /// check the report cannot pass by being self-consistent.
  /// </para>
  /// <para>
  /// THREE FAILURE SHAPES, each stated with file and element rather than folded into one count:
  /// (1) a marker with no ETL.Elements row carrying its code for that element; (2) a marker whose code
  /// IS in ETL.Elements but has no row in ETL.Issues for the same element -- possible, and EXPECTED to
  /// fire, when the code is foreign-dialect-bled off ETL.Issues by <see cref="IsForeignDialectBleed"/>
  /// (owner 2026-08-13): that policy says the code should not be an ETL.Issues row on this platform, and
  /// this gate says a marker naming that code should not be silently unaccounted for either. Both are
  /// true at once, and reporting them together is the point -- it is the visible seam Fact 3 names,
  /// not a bug in this gate. (3) any marker code carrying a dialect prefix illegal for this platform,
  /// found directly in the SQL regardless of whether it made either report.
  /// </para>
  /// </remarks>
  internal static (int Checked, List<string> Failures) ReconcileMarkersAndReports(
    DagPipeline<Transformation> pipeline,
    IReadOnlyDictionary<string, string> modelNamesByNodeId,
    IReadOnlyList<string> modelFileStems,
    IReadOnlyDictionary<string, string> modelSqlByFileStem,
    IReadOnlyDictionary<string, IReadOnlyList<(IssueName IssueName, object[] Args)>> issuesByComponent,
    HashSet<(string FullName, string Code)> issuesReportedInEtlIssues,
    IEwiInformationService ewiInformation,
    string platformId)
  {
    var failures = new List<string>();
    var checkedCount = 0;

    // The reverse of the map ETL.Elements' own row-per-node loop walks forward: which node does this
    // FILE ON DISK belong to. Same match rule as BuildLineageRows' Resolve, so a file this gate cannot
    // attribute to an element is exactly the set BuildLineageRows already warns about, not a second,
    // divergent notion of "unmatched".
    var nodeIdByStem = new Dictionary<string, string>(StringComparer.Ordinal);
    foreach (var node in pipeline.Nodes)
    {
      if (!modelNamesByNodeId.TryGetValue(node.Id, out var modelName))
      {
        continue;
      }

      var stem = ResolveStem(modelName, modelFileStems);
      if (stem is not null)
      {
        nodeIdByStem[stem] = node.Id;
      }
    }

    foreach (var (stem, sql) in modelSqlByFileStem)
    {
      var markerCodes = EngineIssueMarker.Matches(sql)
        .Select(m => m.Groups[1].Value)
        .Distinct(StringComparer.Ordinal)
        .ToList();
      if (markerCodes.Count == 0)
      {
        continue;
      }

      checkedCount += markerCodes.Count;

      if (!nodeIdByStem.TryGetValue(stem, out var nodeId))
      {
        failures.Add(
          $"'{stem}.sql' carries {markerCodes.Count} engine issue marker(s) "
          + $"({string.Join(", ", markerCodes)}) but could not be matched to a unique element -- "
          + "cannot reconcile against ETL.Elements/ETL.Issues.");
        continue;
      }

      var elementCodes = issuesByComponent.TryGetValue(nodeId, out var raw)
        ? raw.Select(i => SafeCode(ewiInformation, i.IssueName)).ToHashSet(StringComparer.Ordinal)
        : new HashSet<string>(StringComparer.Ordinal);

      foreach (var code in markerCodes)
      {
        if (!elementCodes.Contains(code))
        {
          failures.Add(
            $"marker {code} shipped in '{stem}.sql' (element '{nodeId}') has NO matching row in "
            + "ETL.Elements.NA.csv -- the SQL raised an EWI/FDM the report does not carry for this "
            + "element. Fix the registration or the report; do not remove the marker.");
        }
        else if (!issuesReportedInEtlIssues.Contains((nodeId, code)))
        {
          failures.Add(
            $"marker {code} shipped in '{stem}.sql' (element '{nodeId}') is counted in "
            + "ETL.Elements.NA.csv but has NO row in ETL.Issues.NA.csv for this element. Do not "
            + "satisfy this by downgrading the element's status or filtering the code out of "
            + "ETL.Issues -- if the reason is IsForeignDialectBleed, say so, do not hide it.");
        }

        if (IsForeignDialectBleed(code, platformId))
        {
          failures.Add(
            $"marker {code} shipped in '{stem}.sql' (element '{nodeId}') carries a dialect prefix "
            + $"illegal on platform '{DialectPlatform.DisplayName(platformId)}' -- an engine-catalogue "
            + "code from a foreign dialect's own translator shipped into this platform's SQL. Not "
            + "stripped: reported here per policy, and this is the loud failure the gate exists to "
            + "produce rather than a defect in the gate.");
        }
      }
    }

    return (checkedCount, failures);
  }

  /// <summary>
  /// The SAME model-name-to-file-stem match rule <see cref="BuildLineageRows"/> uses, extracted so the
  /// reconciliation gate uses IT rather than a second copy that can drift from it. See BuildLineageRows'
  /// <c>Resolve</c> local function for the measured reason this match rule exists at all (a lineage row
  /// naming the producer's name rather than the file on disk resolves to nothing a <c>ref()</c> uses).
  /// </summary>
  private static string? ResolveStem(string modelName, IReadOnlyList<string> modelFileStems)
  {
    var matches = modelFileStems
      .Where(s => string.Equals(s, modelName, StringComparison.OrdinalIgnoreCase)
               || s.EndsWith("_" + modelName, StringComparison.OrdinalIgnoreCase))
      .ToList();
    return matches.Count switch
    {
      1 => matches[0],
      0 => null,
      _ => matches.OrderBy(s => s.Length).First(),
    };
  }

  /// <summary>
  /// The producer's lineage, in three kinds, all from facts the producer already stated.
  /// </summary>
  /// <remarks>
  /// <para>
  /// DIRECTION. <c>caller = edge.To</c>, <c>referenced = edge.From</c>: the DOWNSTREAM model is the
  /// caller, because it is the one whose SQL contains the <c>ref()</c>. This matches the vertical
  /// slice's rows and the engine's own convention (a target's row names the target as caller and the
  /// table it writes as referenced). Inverting it renders the whole graph backwards with no error.
  /// </para>
  /// <para>
  /// The physical read/write rows are what make the count comparable to the engine's own: measured on
  /// <c>runA</c>, SnowConvert's ObjectReferences for the same SSIS document holds exactly two rows, one
  /// <c>OPEN ROWSET</c> read of <c>[dbo].[CUSTOMER]</c> and one of <c>[dbo].[CUSTOMER_SUMMARY]</c>.
  /// Emitting only model-to-model edges would produce a bigger number that answered a different
  /// question, so both kinds are emitted and counted SEPARATELY.
  /// </para>
  /// <para>
  /// TWO MEASURED DIVERGENCES FROM THE EMITTED SQL, both reported rather than smoothed over, because
  /// each says something the other artifacts do not.
  /// </para>
  /// <para>
  /// OVER-STATEMENT, SSIS. The rows carry
  /// <c>int_cspl_filter_birthyear &lt;- int_der_add_fullname_birthyear</c>, and that model contains NO
  /// <c>ref()</c>: its translator threw, so the placeholder projects nulls with no FROM at all. The
  /// row describes the edge the PRODUCER IDENTIFIED; the model is the degraded thing. Rewriting
  /// lineage to mirror degraded SQL would delete the evidence that an edge was lost, so it is left
  /// as-is — but a consumer joining these rows to dbt's own manifest will find one edge dbt does not
  /// have, and that is a real difference, not a rounding error.
  /// </para>
  /// <para>
  /// UNDER-STATEMENT, PENTAHO. The tree contains <c>stg_raw__read_customer</c> with a live
  /// <c>source('raw','CUSTOMER')</c> call and there is NO <c>SELECT - FROM</c> row for it, because
  /// that model was AUTHORED BY <c>ai_fill</c> at stage 3b — after this emitter ran. Lineage is built
  /// from the IR, and tier-3 SQL is not in the IR, so every tier-3 model is invisible here. That is an
  /// ordering consequence of the ladder, not a defect in the resolution above.
  /// </para>
  /// </remarks>
  private static List<Reference> BuildLineageRows(
    DagPipeline<Transformation> pipeline,
    IReadOnlyDictionary<string, string> modelNamesByNodeId,
    IReadOnlyDictionary<string, string> sourceRelationsByNodeId,
    IReadOnlyList<string> modelFileStems,
    string sourceDocumentName,
    List<string> warnings)
  {
    // INJECTIVITY FIRST. The calculator's dedup is silent, so a collision detected here is the only
    // place it can be reported as a cause rather than observed later as a smaller number.
    var collisions = modelNamesByNodeId
      .GroupBy(kv => kv.Value, StringComparer.OrdinalIgnoreCase)
      .Where(g => g.Count() > 1)
      .ToList();
    foreach (var collision in collisions)
    {
      warnings.Add(
        $"model name '{collision.Key}' is shared by {collision.Count()} node(s) "
        + $"({string.Join(", ", collision.Select(kv => kv.Key))}) -- lineage rows WILL be deduplicated away");
    }

    // RESOLVE EACH PRODUCER MODEL NAME TO THE NAME A ref() WILL ACTUALLY USE.
    //
    // MEASURED: the first version of these rows named `customersummaryderive__odbc_customer`, while the
    // file on disk is `stg_raw__customersummaryderive__odbc_customer.sql` and the downstream model says
    // `ref('stg_raw__customersummaryderive__odbc_customer')`. Every row was internally consistent and
    // NONE of them joined to the dbt graph they claimed to describe -- the whole point of the feature.
    // The prefixes come from `DbtModelNameFormatter` inside the writer, so they are READ BACK OFF DISK
    // rather than re-derived here: duplicating the formatter's rule is how the two drift apart.
    //
    // The match rule is the one `coverage_gate.py` already uses and prints: the file stem is the
    // model name, optionally behind a `<prefix>_` the emitter added. Ambiguity is reported, not
    // resolved by picking one.
    string Resolve(string modelName)
    {
      var stem = ResolveStem(modelName, modelFileStems);
      if (stem is not null)
      {
        var matchCount = modelFileStems.Count(s =>
          string.Equals(s, modelName, StringComparison.OrdinalIgnoreCase)
          || s.EndsWith("_" + modelName, StringComparison.OrdinalIgnoreCase));
        if (matchCount > 1)
        {
          warnings.Add(
            $"model name '{modelName}' matched {matchCount} files; the shortest ('{stem}') is used "
            + "and the ambiguity is stated rather than hidden");
        }

        return stem;
      }

      warnings.Add(
        $"model name '{modelName}' matched NO file on disk; its lineage row names the producer's "
        + "name, which no ref() in this tree uses");
      return modelName;
    }

    var rows = new List<Reference>();

    foreach (var edge in pipeline.Edges)
    {
      if (!modelNamesByNodeId.TryGetValue(edge.To.Id, out var caller)
        || !modelNamesByNodeId.TryGetValue(edge.From.Id, out var referenced))
      {
        warnings.Add($"edge {edge.From.Id} -> {edge.To.Id} has no model name on one end; no lineage row");
        continue;
      }

      rows.Add(Row(sourceDocumentName, Resolve(caller), "DBT MODEL", Resolve(referenced), DbtRefRelation));
    }

    foreach (var (nodeId, relation) in sourceRelationsByNodeId.OrderBy(kv => kv.Key, StringComparer.Ordinal))
    {
      if (!modelNamesByNodeId.TryGetValue(nodeId, out var caller))
      {
        continue;
      }

      // "MISSING" is the engine's own vocabulary for a referenced object outside the migration scope,
      // and it is what runA's rows carry for exactly these tables. Claiming "TABLE" would assert the
      // relation was found somewhere, which nothing checked.
      rows.Add(Row(sourceDocumentName, Resolve(caller), "MISSING", relation, ReadRelation));
    }

    foreach (var node in pipeline.Nodes)
    {
      if (node.Element is not TargetTransformation target || string.IsNullOrWhiteSpace(target.TableName))
      {
        continue;
      }

      if (!modelNamesByNodeId.TryGetValue(node.Id, out var caller))
      {
        continue;
      }

      var full = string.Join(
        ".",
        new[] { target.Database, target.SchemaName, target.TableName }
          .Where(p => !string.IsNullOrWhiteSpace(p)));
      rows.Add(Row(sourceDocumentName, Resolve(caller), "MISSING", full, WriteRelation));
    }

    return rows;
  }

  private static Reference Row(
    string fileName,
    string caller,
    string referencedType,
    string referenced,
    string relationType,
    string callerCodeUnit = CallerCodeUnit,
    string line = "-1")
    => new(
      partitionKey: PartitionKey,
      fileName: fileName,
      callerCodeUnit: callerCodeUnit,
      callerCodeUnitDatabase: NotApplicable,
      callerCodeUnitSchema: NotApplicable,
      callerCodeUnitName: caller,
      callerCodeUnitFullName: caller,
      referencedElementType: referencedType,
      referencedElementDatabase: NotApplicable,
      referencedElementSchema: NotApplicable,
      referencedElementName: referenced,
      referencedElementFullName: referenced,
      line: line,
      relationType: relationType);

  private static EtlReplatformReportItem ElementRow(
    string fullName,
    string subtype,
    string category,
    string fileName,
    EtlReplatformStatus status,
    IReadOnlyList<string> codes,
    string platformId,
    bool inGraph,
    int columns,
    string migrationId)
  {
    var ewis = codes.Where(c => !IsFdmCode(c)).ToList();
    var fdms = codes.Where(IsFdmCode).ToList();
    return new EtlReplatformReportItem
    {
      SessionID = PartitionKey,

      Technology = DialectPlatform.DisplayName(platformId),
      Category = category,
      Subtype = subtype,
      FullName = fullName,
      FileName = fileName,
      Status = status,
      EwiCount = ewis.Count.ToString(),
      Ewis = string.Join(",", ewis),
      FdmCount = fdms.Count.ToString(),
      Fdms = string.Join(",", fdms),
      PrfCount = "0",
      Prfs = string.Empty,
      EntryKind = NotApplicable,
      AdditionalInfo =
        $"{{\"sourceDocumentExtension\":\"{platformId}\","
        + $"\"inGraph\":{(inGraph ? "true" : "false")},\"columns\":{columns}}}",
      MigrationID = migrationId,
    };
  }

  /// <summary>
  /// The element's status, from what the engine did rather than from what it registered.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE REGISTERED STATUS IS OFTEN ABSENT, AND THE REASON IS AN ENGINE LIMITATION WORTH NAMING.
  /// <c>RegisterStatus</c> is called only by
  /// <c>TransformationUnitTranslator.GenerateUnsupportedElementConversion</c>, i.e. only when a
  /// translator THREW and was swallowed. A node the producer already declared
  /// <c>UnsupportedTransformation</c> takes the placeholder path WITHOUT throwing, so nothing
  /// registers a status for it — the engine's own <c>SqlUtils.AddIssueToElement</c> keys the EWI on
  /// <c>ctx.CurrentContextName</c>, the CONTAINER, never the element. (The caller now closes the EWI
  /// half of that gap itself, re-registering under the element id right before <see cref="Emit"/>;
  /// this special case remains because nothing does the same for status.)
  /// </para>
  /// <para>
  /// MEASURED: the DataStage <c>CTransformerStage</c> node <c>CustomerSummaryDerive/V0S2</c> emitted a
  /// model whose first line is <c>!!!RESOLVE EWI!!! SSC-EWI-INF0001</c> and was reported
  /// <c>Success</c> with <c>EWI Count 0</c>, before that caller-side re-registration existed. The
  /// element type is the fact the STATUS row can still be built from: an
  /// <see cref="UnsupportedTransformation"/> is NotSupported by definition, whatever was registered.
  /// </para>
  /// </remarks>
  private static EtlReplatformStatus StatusFor(
    RecordingEtlAssessmentBuilder assessment, string nodeId, Transformation element, bool hasIssues)
  {
    if (assessment.Statuses.TryGetValue(nodeId, out var status))
    {
      return status;
    }

    if (element is UnsupportedTransformation)
    {
      return EtlReplatformStatus.NotSupported;
    }

    return hasIssues ? EtlReplatformStatus.Partial : EtlReplatformStatus.Success;
  }

  private static List<string> CodesFor(
    IReadOnlyDictionary<string, IReadOnlyList<(IssueName IssueName, object[] Args)>> byComponent,
    string nodeId,
    IEwiInformationService ewiInformation)
    => byComponent.TryGetValue(nodeId, out var issues)
      ? issues.Select(i => SafeCode(ewiInformation, i.IssueName)).ToList()
      : [];

  private static bool IsFdmCode(string code)
    => code.StartsWith("SSC-FDM", StringComparison.OrdinalIgnoreCase);

  /// <summary>
  /// Owner 2026-08-13: foreign dialect bleed into ETL.Issues is forbidden. This producer is the
  /// AI-First path for unsupported platforms; SSIS/INF-named codes on a non-SSIS/non-Inf document
  /// must not become assessment rows (AIM coexistence fills the honest channel later in Python).
  /// </summary>
  internal static bool IsForeignDialectBleed(string code, string platformId)
  {
    if (string.IsNullOrEmpty(code) || code.StartsWith("AIM-", StringComparison.OrdinalIgnoreCase))
    {
      return false;
    }

    var upper = code.ToUpperInvariant();
    var isSsisCode = upper.Contains("-SSIS");
    var isInfCode = upper.Contains("-INF");
    if (DialectPlatform.IsSsisNative(platformId))
    {
      return isInfCode;
    }

    if (DialectPlatform.IsInformaticaNative(platformId))
    {
      return isSsisCode;
    }

    // Unsupported proving platforms (yxmd/ktr/dsx/adf/...): both SSIS and INF are bleed.
    return isSsisCode || isInfCode;
  }

  private static string SafeCode(IEwiInformationService ewiInformation, IssueName issueName)
    => Safe(() => ewiInformation.GetCode(issueName), issueName.ToString());

  private static string Safe(Func<string> get, string fallback)
  {
    try
    {
      var value = get();
      return string.IsNullOrEmpty(value) ? fallback : value;
    }
    catch (Exception)
    {
      return fallback;
    }
  }

  /// <summary>
  /// Writes ObjectReferences from an already-built row list. ONE lineage implementation, shared by the
  /// stage-3 emit and the post-fill re-emit.
  /// </summary>
  private static (ReportOutcome Report, int Stored) WriteLineage(
    string reportsDir,
    List<Reference> rows,
    ProducerMigrationDataService migrationData,
    ProducerAssessmentConfigurationProvider configProvider,
    AssessmentSetup setup,
    List<string> warnings,
    ILogger logger)
  {
    var stored = 0;
    var report = new ReportOutcome("ObjectReferences." + SessionTimestamp + ".csv", false, 0, false, null);
    try
    {
      // `using`: IAssessmentDb is IDisposable and owns the SQLite write connection. In-memory mode
      // (inputFileCount 0 < DiskThresholdFileCount 10_000) means nothing lands on disk.
      using var db = new SqliteAssessmentDb();
      // The registry is read on one line of the calculator, inside Add(ICompound, ILineageContext) --
      // the AST route, which this producer never takes because every row arrives through AddDirect.
      // An empty registry is therefore the inert answer, for the same reason the input-path
      // calculator above is the unused one.
      var calculator = new ObjectReferenceCalculator(
        migrationData, db, new UnusedLineageInputPathCalculator(), new DbtModelRegistry());
      IObjectReferenceCalculator sink = calculator;
      foreach (var row in rows)
      {
        sink.AddDirect(row);
      }

      // MEASURED, NOT ASSUMED. The calculator dedups on (caller, referenced, relationType) and drops
      // silently. Counting what came back out is the only way to see that happen.
      stored = calculator.GetAllReferences().Count();
      if (stored != rows.Count)
      {
        warnings.Add(
          $"lineage dedup: offered {rows.Count} row(s), the calculator stored {stored}. "
          + "Model names are colliding on (caller, referenced, relation) -- see ENG-015.");
      }

      var writer = new ObjectReferencesReportWriter(
        configProvider,
        setup,
        new CalculatorBackedWriterModel(calculator),
        new ObjectReferenceReportItemConverter(isLightWeightVersion: false),
        logger);
      report = Inspect(reportsDir, writer.FormattedReportName, writer.GenerateReport(null!, null!, logger, reportsDir));
    }
    catch (Exception ex)
    {
      report = report with { Error = $"{ex.GetType().Name}: {ex.Message}" };
      warnings.Add($"ObjectReferences threw: {ex.GetType().Name}: {ex.Message}");
    }

    return (report, stored);
  }

  /// <summary>
  /// Re-emits ObjectReferences ALONE over a tree that has already been filled, so that tier-3 models
  /// appear in lineage.
  /// </summary>
  /// <remarks>
  /// <para>
  /// WHY A SECOND PASS AND NOT A REORDERING. <c>ai_fill.py</c> can only decide what to fill by reading
  /// the emitted tree -- it replaces a model that carries a blocking EWI or projects no columns -- so
  /// it cannot run before emission, and lineage cannot describe the shipped tree until it has. The two
  /// orderings are mutually exclusive and the artifact is what has to be right.
  /// </para>
  /// <para>
  /// LINEAGE ONLY, DELIBERATELY. ETL.Issues and ETL.Elements are built from
  /// <c>RecordingEtlAssessmentBuilder</c>, i.e. from what the engine's translators registered DURING
  /// translation. Re-running them here, with no translation in this process, would overwrite two
  /// populated reports with placeholders -- turning a fix for one report into a regression in two.
  /// </para>
  /// </remarks>
  /// <param name="outRoot">The migration output root.</param>
  /// <param name="pipeline">The hydrated data-flow graph.</param>
  /// <param name="modelNamesByNodeId">dbt model name per node id.</param>
  /// <param name="sourceRelationsByNodeId">Physical relation read per source node id.</param>
  /// <param name="modelFileStems">The model file stems actually on disk.</param>
  /// <param name="sourceDocumentName">The source document file name.</param>
  /// <param name="platformId">The producer's own platform id, for the migration id.</param>
  /// <param name="logger">A capturing logger.</param>
  /// <returns>The rows offered, stored, their split by relation, the outcome and any warnings.</returns>
  internal static (int Offered, int Stored, IReadOnlyDictionary<string, int> ByRelation,
    ReportOutcome Report, IReadOnlyList<string> Warnings) EmitLineageOnly(
    string outRoot,
    DagPipeline<Transformation> pipeline,
    IReadOnlyDictionary<string, string> modelNamesByNodeId,
    IReadOnlyDictionary<string, string> sourceRelationsByNodeId,
    IReadOnlyList<string> modelFileStems,
    string sourceDocumentName,
    string platformId,
    ILogger logger)
  {
    var reportsDir = Path.Combine(outRoot, "Reports");
    Directory.CreateDirectory(reportsDir);
    var warnings = new List<string>();
    var rows = BuildLineageRows(
      pipeline, modelNamesByNodeId, sourceRelationsByNodeId, modelFileStems, sourceDocumentName, warnings);
    rows.AddRange(ScrapeModelAuthoredRows(outRoot, sourceDocumentName));
    var byRelation = rows
      .GroupBy(r => r.RelationType, StringComparer.Ordinal)
      .ToDictionary(g => g.Key, g => g.Count(), StringComparer.Ordinal);
    var (report, stored) = WriteLineage(
      reportsDir,
      rows,
      new ProducerMigrationDataService(
        etlInputPath: sourceDocumentName,
        partitionKey: PartitionKey,
        migrationId: "AIFIRST-" + platformId.ToUpperInvariant(),
        sessionTimestamp: SessionTimestamp),
      new ProducerAssessmentConfigurationProvider(),
      new AssessmentSetup { SessionTimestamp = SessionTimestamp },
      warnings,
      logger);
    return (rows.Count, stored, byRelation, report, warnings);
  }

  /// <summary>
  /// Lineage rows stated by MODEL-AUTHORED (tier-3) model files, read out of the shipped SQL.
  /// </summary>
  /// <remarks>
  /// <para>
  /// Only files carrying <see cref="ModelAuthoredMarker"/> are read. An engine-rendered model's edges
  /// are already in the IR, so scraping it too would emit a second row for every edge on every platform
  /// and answer a different question (see the relation-type remarks). A tier-2 model
  /// (<c>SSC-AI-ASSISTED</c>) is engine-rendered from a model-supplied payload, so its edges ARE in the
  /// IR and it is deliberately not scraped either.
  /// </para>
  /// <para>
  /// THE LINE NUMBER IS REAL. Every other row in this report carries <c>line: "-1"</c>, because a
  /// producer has no AST and no offsets. These rows have both: the <c>ref()</c> or <c>source()</c> call
  /// sits at a known line of a file on disk, so the row is locatable in a way the IR-derived rows are
  /// not. That is a difference worth carrying rather than flattening to -1 for uniformity.
  /// </para>
  /// </remarks>
  /// <param name="outRoot">The migration output root.</param>
  /// <param name="sourceDocumentName">The source document name, for the FileName column.</param>
  /// <returns>One row per ref()/source() call in every model-authored model file.</returns>
  private static List<Reference> ScrapeModelAuthoredRows(string outRoot, string sourceDocumentName)
  {
    var rows = new List<Reference>();
    var etlRoot = Path.Combine(outRoot, "Output", "ETL");
    if (!Directory.Exists(etlRoot))
    {
      return rows;
    }

    foreach (var file in Directory.GetFiles(etlRoot, "*.sql", SearchOption.AllDirectories))
    {
      // `target/` and `dbt_internal_packages/` hold dbt's own compiled copies of every model; reading
      // them would double every row. Same prune the driver's stage 4 applies, and for the same reason.
      var relative = Path.GetRelativePath(etlRoot, file).Replace('\\', '/');
      if (relative.Contains("/target/", StringComparison.Ordinal)
        || relative.Contains("/dbt_internal_packages/", StringComparison.Ordinal)
        || !relative.Contains("/models/", StringComparison.Ordinal))
      {
        continue;
      }

      var lines = File.ReadAllLines(file);
      if (!lines.Any(l => l.Contains(ModelAuthoredMarker, StringComparison.Ordinal)))
      {
        continue;
      }

      var caller = Path.GetFileNameWithoutExtension(file);
      for (var i = 0; i < lines.Length; i++)
      {
        foreach (System.Text.RegularExpressions.Match m in RefCall.Matches(lines[i]))
        {
          rows.Add(Row(
            sourceDocumentName, caller, "DBT MODEL", m.Groups[1].Value,
            ModelAuthoredRefRelation, ModelAuthoredCallerCodeUnit, (i + 1).ToString()));
        }

        foreach (System.Text.RegularExpressions.Match m in SourceCall.Matches(lines[i]))
        {
          // "MISSING" is the engine's own vocabulary for a referenced object outside the migration
          // scope, and it is what runA's rows carry for exactly these tables.
          rows.Add(Row(
            sourceDocumentName, caller, "MISSING",
            m.Groups[1].Value + "." + m.Groups[2].Value,
            ModelAuthoredReadRelation, ModelAuthoredCallerCodeUnit, (i + 1).ToString()));
        }
      }
    }

    return rows;
  }

  /// <summary>
  /// Reads the report back OFF DISK.
  /// </summary>
  /// <remarks>
  /// <c>SnowCustomReportWriter.GenerateReport</c> catches every exception, logs it and returns
  /// <c>false</c>; and on an empty inventory it writes a ONE-LINE placeholder and returns <c>true</c>.
  /// So neither the return value nor the file's existence is evidence that any row was written. The
  /// placeholder test is the slice spike's: a single line with no comma is prose, not CSV.
  /// </remarks>
  private static ReportOutcome Inspect(string reportsDir, string name, bool generated)
  {
    var path = Path.Combine(reportsDir, name);
    if (!File.Exists(path))
    {
      return new ReportOutcome(name, false, 0, false, generated ? "writer returned true but wrote no file" : null);
    }

    var lines = File.ReadAllText(path).Split('\n', StringSplitOptions.RemoveEmptyEntries);
    var isPlaceholder = lines.Length == 1 && !lines[0].Contains(',');
    return new ReportOutcome(name, true, isPlaceholder ? 0 : Math.Max(0, lines.Length - 1), isPlaceholder, null);
  }
}
