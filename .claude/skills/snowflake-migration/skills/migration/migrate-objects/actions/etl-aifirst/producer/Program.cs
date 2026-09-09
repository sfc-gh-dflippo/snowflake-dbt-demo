// SPIKE 1 — the callable entry point.
//
// THE QUESTION: does the AI-first producer chain run outside the xUnit/MSTest host?
//
// Static analysis said the three producer files reference no test framework at all, and that
// the fixture's only test dependency was Moq — four bare `new Mock<X>().Object` stubs with no
// `.Setup(...)` anywhere. But "no test-framework using directives" is not "runs outside the
// test host": that is the adjacent-verification trap this project has hit repeatedly. Only a
// compiled, executed console app answers it. This is that app.
//
// Usage: aifirst-migrate <producer-ir.json> <output-root>
//
// It does what AiFirstVerticalSliceFixture does, minus Moq and minus the test framework:
//   IR JSON -> hydrate -> production translator -> DbtModelFactory -> production writers -> disk
// plus the orchestration SQL, because scan_unit.py counts elements only from <unit>.sql.
namespace AiFirst;

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using AiFirst.Producer;
using Artinsoft.Common.AST;
using Artinsoft.Common.Tools.PrettyPrinter;
using Microsoft.Extensions.Logging.Abstractions;
using Mobilize.AnsiSql.Tools.PrettyPrinter;
using Mobilize.Snow.Common;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt;
using Snowflake.SnowConvert.EtlToDbt.Context;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.Dbt;
using Snowflake.SnowConvert.EtlToDbt.DbtGeneration;
using Snowflake.SnowConvert.EtlToDbt.DbtGeneration.Translations;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration.OrchestratorMappers;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration.OrchestratorTaskTranslators.SSIS;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration.OrchestratorVariableWrappers;
using Snowflake.SnowConvert.EtlToDbt.FileSystem;
using Snowflake.SnowConvert.EtlToDbt.Models;
using Snowflake.SnowConvert.EtlToDbt.Models.Columns;
using Snowflake.SnowConvert.EtlToDbt.Serialization;
using Snowflake.SnowConvert.EtlToDbt.Services;
using Snowflake.SnowConvert.EtlToDbt.Utils;
using Snowflake.SnowConvert.EtlToDbt.Variables;

internal static class Program
{
  // THESE WERE CONSTANTS, AND THAT WAS THE WORST SSIS BIAS IN THE PROJECT.
  //
  // MEASURED on poc/blind-run/runS: all four platforms emitted a BYTE-IDENTICAL orchestration file
  // (md5 eb7f92d6f569a48a1d15008ef5781521) at Output/ETL/DerivedColumn/DerivedColumn.sql, whose body
  // says `---- Start block 'Package\Data Flow Task'` and
  // `EXECUTE DBT PROJECT public.Data_Flow_Task`. `Package\Data Flow Task` is an SSIS control-flow
  // path and `DerivedColumn` is an SSIS component name, so a DataStage DSJOB called
  // `CustomerSummaryDerive` and a Pentaho transformation called
  // `customer_summary_fullname_birthyear` both shipped a task graph that named neither.
  //
  // It survived every gate: stage 4 counted EWIs, sentinels, column-less models, model-authored
  // models and dbt compile status; Gate A counted DATA-FLOW element coverage. Nothing asked whether
  // the orchestration SQL bore any relation to the input document — a feature with no gate, which is
  // this project's own recurring finding, in our harness rather than the engine's.
  //
  // They are now DERIVED. See ResolveOrchestrationIdentity: the identity comes from the container
  // node the producer already put in the IR (`$kind: null` + `_unsupported: <native container kind>`),
  // which HydratedIr.UnsupportedNodes exists to surface. Where the IR states no container, NOTHING is
  // emitted and the driver says so, because an absent task graph is an honest degradation and a
  // mislabelled one is a wrong answer that looks right.
  //
  // The two constants below survive ONLY for --target-probe and --novel-orchestration, which
  // synthesise their own elements and have no producer IR to derive an identity from.
  private const string ProbeOrchestratorName = "DerivedColumn";
  private const string ProbeDataFlowDirectoryName = "Data_Flow_Task";

  /// <summary>
  /// The names the orchestration half writes, all taken from the producer's IR or the input document.
  /// </summary>
  /// <param name="UnitName">
  /// The unit of work: the <c>Output/ETL/&lt;unit&gt;</c> directory and the <c>&lt;unit&gt;.sql</c>
  /// filename, and the parent Snowflake task name.
  /// </param>
  /// <param name="DataFlowFullName">
  /// The container's platform-native full path, used verbatim as the emitted block label. This is the
  /// string that used to read <c>Package\Data Flow Task</c> on every platform.
  /// </param>
  /// <param name="DataFlowName">The container's display name.</param>
  /// <param name="DataFlowDirectoryName">The dbt project directory, from the container's own modelName.</param>
  /// <param name="NativeKind">The platform's own name for the container kind, for the driver's log.</param>
  /// <param name="Source">How the identity was resolved, printed so it is never guessed at.</param>
  private sealed record OrchestrationIdentity(
    string UnitName,
    string DataFlowFullName,
    string DataFlowName,
    string DataFlowDirectoryName,
    string NativeKind,
    string Source);

  internal static int Main(string[] args)
  {
    // A real exit code, unlike Assemblies/CmdRunner/Program.cs:34 which is `void Main` and
    // therefore exits 0 after a crash (ENG-009). A callable migrator has to be able to fail.
    var noShim = Array.IndexOf(args, "--no-shim") >= 0;
    var novelOrchestration = Array.IndexOf(args, "--novel-orchestration") >= 0;
    var relineage = Array.IndexOf(args, "--relineage") >= 0;
    var targetProbe = Array.IndexOf(args, "--target-probe") >= 0;
    if (targetProbe)
    {
      try
      {
        return RunTargetProbe();
      }
      catch (Exception ex)
      {
        Console.Error.WriteLine($"FAILED: {ex.GetType().Name}: {ex.Message}");
        Console.Error.WriteLine(ex.StackTrace);
        return 1;
      }
    }

    var positional = args.Where(a => !a.StartsWith("--", StringComparison.Ordinal)).ToArray();

    // SPIKE 4 takes an output root only — it synthesises its own tasks, no IR needed.
    if (novelOrchestration)
    {
      if (positional.Length != 1)
      {
        Console.Error.WriteLine("usage: aifirst-migrate --novel-orchestration <output-root>");
        return 2;
      }

      try
      {
        return RunNovelOrchestration(positional[0]);
      }
      catch (Exception ex)
      {
        Console.Error.WriteLine($"FAILED: {ex.GetType().Name}: {ex.Message}");
        Console.Error.WriteLine(ex.StackTrace);
        return 1;
      }
    }

    if (positional.Length is < 2 or > 3)
    {
      Console.Error.WriteLine(
        "usage: aifirst-migrate [--no-shim] <producer-ir.json> <output-root> [source-document]");
      return 2;
    }

    var irPath = positional[0];
    var outRoot = positional[1];

    // ---- RE-EMIT LINEAGE OVER AN ALREADY-FILLED TREE -------------------------------------------
    // Tier-3 models were invisible to lineage because ai_fill writes them at stage 3b, AFTER this
    // program computed the graph. This mode runs after the fill and states the shipped tree's edges.
    // See ProducerReports.EmitLineageOnly for why it re-emits lineage ONLY.
    if (relineage)
    {
      try
      {
        return RunRelineage(irPath, outRoot, positional.Length == 3 ? positional[2] : null);
      }
      catch (Exception ex)
      {
        Console.Error.WriteLine($"FAILED: {ex.GetType().Name}: {ex.Message}");
        return 1;
      }
    }

    // The source document name, for the FileName column of every report row. Optional so the two
    // committed spike invocations keep working; when absent the reports say so rather than inventing
    // a name, because a report row naming the wrong file is worse than one naming an obvious
    // placeholder.
    var sourceDocument = positional.Length == 3 ? positional[2] : null;

    try
    {
      var files = Run(irPath, outRoot, noShim, sourceDocument);
      Console.WriteLine($"OK: {files.Count} file(s) written under {outRoot}");
      return 0;
    }
    catch (Exception ex)
    {
      Console.Error.WriteLine($"FAILED: {ex.GetType().Name}: {ex.Message}");
      return 1;
    }
  }

  private static IReadOnlyList<string> Run(
    string irPath, string outRoot, bool noShim, string? sourceDocument)
  {
    if (!File.Exists(irPath))
    {
      throw new FileNotFoundException($"producer IR not found: {irPath}", irPath);
    }

    var json = File.ReadAllText(irPath);
    if (json.Length == 0)
    {
      throw new InvalidOperationException($"producer IR is empty: {irPath}");
    }

    // The platform id, derived ONCE here and reused at every call site that needs to tell a native
    // SSIS/Informatica document apart from everything else (the hydrator's
    // UnsupportedTransformation issue code and the context's IssueForExceptionOnPipelineElement both
    // need this to stop writing Informatica/SSIS-coded EWIs into non-native platforms' .sql, same as
    // ProducerReports.Emit already does for the CSV sink below).
    var platformId = sourceDocument is null ? "unstated" : Path.GetExtension(sourceDocument).TrimStart('.');

    // ---- the SSIS semantics shim, then hydrate ------------------------------------------------
    // SPIKE 2: `--no-shim` runs ShimSteps.None, which hydrates the framework IR VERBATIM. That is
    // the decisive test for whether the Python->C# handoff is a schema problem or a semantics
    // problem.
    //
    // Note Describe(), not ToString(). ShimReport declares its lists `internal`, and a C# record's
    // generated ToString() includes only PUBLIC members — so printing the record yields
    // "ShimReport { }" whether or not any transform fired. The first run of this app printed
    // exactly that and it meant nothing at all.
    var steps = noShim ? AiFirstSsisSemanticsShim.ShimSteps.None
                       : AiFirstSsisSemanticsShim.ShimSteps.All;
    var (shimmed, shimReport) = AiFirstSsisSemanticsShim.Apply(json, steps);
    Console.WriteLine($"shim steps  : {steps}");
    Console.WriteLine($"shim        : {shimReport.Describe()}");
    foreach (var r in shimReport.RewrittenExpressions)
    {
      Console.WriteLine($"  rewrite   : {r}");
    }

    var ir = AiFirstProducerIrHydrator.Hydrate(shimmed, platformId);
    Console.WriteLine(
      $"hydrated    : {ir.Pipeline.Nodes.Count} node(s), {ir.Pipeline.Edges.Count} edge(s)");

    // ---- the orchestration identity, DERIVED, before anything is written -----------------------
    var identity = ResolveOrchestrationIdentity(ir, sourceDocument);
    if (identity is null)
    {
      Console.WriteLine(
        "orchestration: NO IDENTITY -- the IR states no container node ($kind null with "
        + "_unsupported), and no source document was supplied to fall back on. NO ORCHESTRATION SQL "
        + "WILL BE WRITTEN. This is deliberate: the constant that used to be emitted here named an "
        + "SSIS package path on every platform.");
    }
    else
    {
      Console.WriteLine($"orchestration: unit '{identity.UnitName}'  ({identity.Source})");
      Console.WriteLine($"  container : '{identity.DataFlowFullName}'  name='{identity.DataFlowName}'  nativeKind='{identity.NativeKind}'");
      Console.WriteLine($"  dbt dir   : {identity.DataFlowDirectoryName}");
    }

    var unitName = identity?.UnitName
      ?? (sourceDocument is null
        ? Path.GetFileNameWithoutExtension(irPath)
        : Path.GetFileNameWithoutExtension(sourceDocument));

    // WITHOUT A CONTAINER THERE IS NO NAME FOR THE DATA-FLOW DIRECTORY, and this placeholder says so
    // in the path itself rather than borrowing a plausible-looking one. The models still have to land
    // somewhere — withholding them would throw away real work — but the directory must not imply an
    // orchestration container the IR never stated. `EXECUTE DBT PROJECT` would reference this name,
    // and no statement referencing it is emitted.
    var dataFlowDirectoryName = identity?.DataFlowDirectoryName ?? "data_flow_UNNAMED_BY_IR";

    // ---- the producer's context, Moq replaced by the no-ops --------------------------------
    // A CAPTURING logger, not NullLogger: TransformationUnitTranslator swallows an element-level
    // exception and substitutes a renderable NOT-SUPPORTED placeholder, and the only trace is a
    // LogError. NullLogger would let a substituted node be reported as a success.
    var logger = new CapturingLogger();

    // A RECORDING assessment builder, not the no-op.
    //
    // MEASURED CAUSE OF ZERO REPORT ROWS. Every `ctx.AddIssueToElement` call routes through
    // `SqlUtils.AddIssueToElement`, which calls `assessmentBuilder.RegisterEwi(...)`; and
    // `TransformationUnitTranslator.GenerateUnsupportedElementConversion` calls both `RegisterEwi` and
    // `RegisterStatus`. `NoOpEtlAssessmentBuilder` implements all of them as `{ }`. So the EWIs the
    // engine raised were rendered into the .sql AND discarded on the reporting side, from one cause.
    // Keeping them is what makes ETL.Issues and ETL.Elements possible at all.
    var assessment = new RecordingEtlAssessmentBuilder();
    var ewiInformation = new EwiInformationService(new EwiModelReader(logger));
    var ctx = new AiFirstProducerDataFlowContext(
      ir.Pipeline,
      ir.ModelNamesByNodeId,
      new DbtProjectGenerationContext(new RecordingEwiService(), logger),
      assessment,
      logger,
      currentItemName: dataFlowDirectoryName,
      currentFileName: sourceDocument is null
        ? "producer://" + unitName
        : Path.GetFileName(sourceDocument),
      sourceRelationsByNodeId: ir.SourceRelationsByNodeId,
      platformId: platformId);

    // ---- production translators: the whole registered set, not one -------------------------
    // This is the change that makes the entry point PLATFORM-GENERAL. It previously did
    //     .OfType<ExpressionTransformation>().Single()
    // which is an SSIS DerivedColumn assumption: a DataStage graph has 43 nodes and NO expression
    // element, so `Single()` threw "Sequence contains no elements" and the whole run failed at
    // stage 3 while the equivalent xUnit fixture emitted 29 models. One line, and it was the entire
    // difference between "SSIS only" and "any platform with a table".
    var unit = new TransformationUnitTranslator(
      [
        new ExpressionTransformationTranslator(),
        new SourceQualifierTranslator(
          new NoOpMultiDialectEtlSqlProcessor(), new NoOpInfPcSqlValueMigrator(), SourceLanguage.Ansi),
        new TargetTranslator(new NoOpInfPcSqlValueMigrator(), new NoOpEtlSqlProcessor(), logger),
        // Added with the hydrator widening. Despite deriving from InfPcFilterTranslatorBase, this
        // translator is behaviourally NEUTRAL -- its own source comment says the plan (passthrough
        // projection + raw condition) is "computed once in the shared base" -- and it takes nothing
        // platform-specific, only ILogger. The InfPc name is where the code LIVES, not what it means.
        new FilterTranslator(logger),
        new UnsupportedTransformationTranslator(),
      ],
      reusableTransformationTracker: null);

    var models = new List<IDbtModel>();

    // THE EXACT FILE TIER-2 STAMPING MAY TOUCH, KEYED BY THE NODE THAT PRODUCED IT -- never a
    // name lookup. Populated only for a node whose outcome is "ok" (not SUBST/EMPTY/THREW) AND
    // whose element is not an UnsupportedTransformation (a placeholder the producer declared
    // rather than a translation, and therefore an unresolved node despite raising no exception).
    // Both exclusions matter: a suffix/name match on modelName alone previously let one node's
    // "summary" collide with another's "int_customer_summary" and stamped the wrong file.
    var modelFileRelativePathByNodeId = new Dictionary<string, string>(StringComparer.Ordinal);
    int ok = 0, substituted = 0, empty = 0, threw = 0;
    foreach (var node in ir.Pipeline.Nodes)
    {
      var errorsBefore = logger.Errors.Count;
      // SET/CLEAR AROUND THE CALL, NOT LEFT STANDING. AddIssueToElement keys every registration this
      // translator makes on whichever element is "current" -- clearing in the finally means a
      // translator running OUTSIDE this loop (there is none today, but SPIKE 3's RunTargetProbe calls
      // TargetTranslator directly with no loop at all) cannot inherit whichever node happened to
      // translate last.
      ctx.SetCurrentElement(node.Id);
      try
      {
        var results = unit.Translate(node.Element, ctx);

        // ISqlQueryForDbt, NOT IIntermediateQueryForDbt. A source stage yields an
        // IStagingQueryForDbt and a target yields a MartQueryForDbt; narrowing to the intermediate
        // interface would silently record every source and every target as producing nothing.
        var query = results.OfType<ISqlQueryForDbt>().FirstOrDefault();
        if (query is null)
        {
          empty++;
          Console.WriteLine($"  EMPTY  {node.Id,-30} {node.Element.GetType().Name}");
          continue;
        }

        var model = DbtModelFactory.CreateModel(query, ctx);
        models.Add(model);

        // "Renderable" is not "translated". A swallowed exception yields a placeholder that looks
        // fine, so the logger is what distinguishes them.
        if (logger.Errors.Count > errorsBefore)
        {
          substituted++;
          Console.WriteLine($"  SUBST  {node.Id,-30} {node.Element.GetType().Name}");
          foreach (var e in logger.Errors.Skip(errorsBefore))
          {
            Console.WriteLine($"           swallowed: {e}");
          }
        }
        else
        {
          ok++;
          if (node.Element is not UnsupportedTransformation)
          {
            modelFileRelativePathByNodeId[node.Id] =
              Path.Combine(model.GetModelPathParts().Append(model.Name + ".sql").ToArray());
          }
        }
      }
      catch (Exception ex)
      {
        threw++;
        Console.WriteLine($"  THREW  {node.Id,-30} {ex.GetType().Name}: {ex.Message}");
      }
      finally
      {
        ctx.SetCurrentElement(null);
      }
    }

    Console.WriteLine(
      $"translated  : {models.Count} renderable of {ir.Pipeline.Nodes.Count} node(s) "
      + $"(ok {ok}, substituted {substituted}, empty {empty}, threw {threw})");

    // PRINTED UNCONDITIONALLY, including the zero. "The producer supplied no source relation" and
    // "the source relation reached the FROM clause" are opposite facts and a silent line renders
    // them identically -- which is exactly how a staging model ending on a bare `FROM` survived
    // four blind runs and read as a clean stage-3 emit.
    Console.WriteLine(
      $"source rels : {ctx.SuppliedSourceRelations.Count} relation(s) answered from "
      + "element.TableName rather than from the graph"
      + (ctx.SuppliedSourceRelations.Count == 0
        ? " -- every SourceQualifier's FROM will be EMPTY"
        : string.Empty));
    foreach (var r in ctx.SuppliedSourceRelations)
    {
      Console.WriteLine($"  source    : {r}");
    }
    if (models.Count == 0)
    {
      throw new InvalidOperationException(
        $"no node produced a renderable artifact: {empty} empty, {threw} threw");
    }

    // ---- production writers onto disk -----------------------------------------------------
    var fileSystem = new FileSystemService();
    var yaml = new YamlSerializer();

    var etlRoot = Path.Combine(outRoot, "Output", "ETL");
    var unitDir = Path.Combine(etlRoot, unitName);
    var dbtProjectDir = Path.Combine(unitDir, dataFlowDirectoryName);
    Directory.CreateDirectory(dbtProjectDir);

    new DbtProjectStructureWriter(fileSystem, yaml, new DbtPackageTracker(), logger)
      .InitializeProjectStructure(dbtProjectDir);

    new DbtModelsWriter(fileSystem, logger).WriteModels(models, dbtProjectDir);

    // ---- TIER-2 PROVENANCE INTO THE ARTIFACT ------------------------------------------------
    // Ordered immediately after the writer, because it amends files the writer just produced and
    // nothing between here and the reports reads them.
    var stamped = StampModelAuthored(dbtProjectDir, modelFileRelativePathByNodeId, ir);
    Console.WriteLine(
      $"tier2 marks : {stamped.Count} model file(s) stamped SSC-AI-ASSISTED of "
      + $"{ir.ModelAuthoredByNodeId.Count} node(s) carrying model-authored facts"
      + (ir.ModelAuthoredByNodeId.Count == 0 ? " -- no sidecar contributed to this document" : string.Empty));
    foreach (var s in stamped)
    {
      Console.WriteLine($"  tier2     : {s}");
    }

    new DefaultConfigurationFilesWriterService(fileSystem).GenerateConfigurationFiles(etlRoot);

    // THE ENGINE'S ONLY INSTRUMENTATION WRITER IS SSIS-SPECIFIC, AND THIS USED TO RUN ON EVERY
    // PLATFORM. It emits ssis_read_control_flow_config_from_stage.sql, ssis_read_baseline_data.sql,
    // ssis_baseline_metrics_log_table.sql and ssis_task_table_usage.sql -- SSIS control-flow config
    // and SSIS baseline metrics. MEASURED (runs/m1-ready-2026-08-19): all four shipped inside an
    // ALTERYX migration's output, and no gate caught it because gate_b.py excluded the whole
    // directory as "framework scaffolding". An absent instrumentation tree is a gap; an SSIS-shaped
    // one under a non-SSIS document is a false statement about the source, so absence wins.
    if (DialectPlatform.IsSsisNative(platformId))
    {
      new SsisSpecificConfigurationFilesWriterService(fileSystem)
        .GenerateConfigurationFiles(Path.Combine(etlRoot, "etl_instrumentation"));
    }
    else
    {
      Console.WriteLine(
        "instrument  : NOT WRITTEN -- the engine's only instrumentation writer is SSIS-specific "
        + $"and this document is '{platformId}'. The tree is ABSENT, not platform-neutral.");
    }

    // ---- the two dbt macros ---------------------------------------------------------------
    // The engine's own copies live in a PRIVATE STATIC method,
    // Assemblies/EtlToDbt/DtsxSsis/DataFlowStrategy/DbtDataFlowStrategy.cs GetDefaultArtifacts(),
    // whose content is entirely static. A producer cannot call it, so the text is duplicated —
    // two of the must-create files are unreachable purely because of an access modifier.
    // Writing them through the production DbtMacroWriter proves the writer itself is reusable.
    new DbtMacroWriter(fileSystem, logger).WriteMacros(DefaultMacros(), dbtProjectDir);

    // ---- orchestration SQL -----------------------------------------------------------------
    // WRITTEN ONLY WHEN THE IR NAMED A CONTAINER. Emitting nothing is the deliberate alternative to
    // emitting the old constant: `scan_unit.py` counts elements from <unit>.sql, so an absent file
    // scores zero elements and stage 4 reports it — whereas the constant scored a full house while
    // naming an SSIS package path on a DataStage job.
    //
    // TWO STATEMENTS NOW, NOT ONE. The file holds the unit's ROOT task and then the container's task.
    // See EmitOrchestrationSql: the child's `AFTER` was always right and the root it named was never
    // emitted, which is a task graph that cannot be resumed rather than one that names the wrong thing.
    if (identity is not null)
    {
      var orchestrationSql = EmitOrchestrationSql(
        identity,
        sourceDocument ?? ("producer://" + unitName),
        outRoot);
      File.WriteAllText(Path.Combine(unitDir, unitName + ".sql"), orchestrationSql);
      var rootTasks = CountOf(orchestrationSql, "CREATE OR REPLACE TASK");
      var afterClauses = CountOf(orchestrationSql, "AFTER ");
      Console.WriteLine(
        $"orch sql    : {unitName}.sql written, {orchestrationSql.Length} byte(s), "
        + $"{rootTasks} CREATE TASK ({afterClauses} with AFTER, so {rootTasks - afterClauses} root)");
    }
    else
    {
      Console.WriteLine(
        "orch sql    : NOT WRITTEN -- no orchestration container in the IR. The task graph is "
        + "ABSENT, not wrong.");
    }

    // ---- REGISTER THE PLACEHOLDER'S OWN EWI (finding 66) -----------------------------------
    // UnsupportedTransformationTranslator only calls ctx.AddIssueToElement, which
    // SqlUtils.AddIssueToElement keys by ctx.CurrentContextName -- the CONTAINER, not the element
    // (see StatusFor's remarks below). ProducerReports.CodesFor looks issues up by node.Id, so a
    // node the producer already declared UnsupportedTransformation never contributes a code there,
    // even though its shipped SQL carries a "!!!RESOLVE EWI!!!" comment. Re-registering under the
    // element id is additive, not a substitute for that container-keyed entry: IsForeignDialectBleed
    // and the container-scoped warning below both still see it. The `Any` guard skips a node whose
    // translator instead THREW and was swallowed into GenerateUnsupportedElementConversion, which
    // already registered an element-keyed issue of its own -- reusing IssueCodeForNotConverted for a
    // node like that would state a second, invented failure alongside the real one.
    foreach (var node in ir.Pipeline.Nodes)
    {
      if (node.Element is UnsupportedTransformation unsupported
        && !assessment.Issues.Any(i => i.FullName == node.Id))
      {
        assessment.RegisterEwi(node.Id, unsupported.IssueCodeForNotConverted, unsupported.IssueArgs.ToArray());
      }
    }

    // ---- ETL LINEAGE AND THE THREE DRIVABLE REPORTS ----------------------------------------
    // These are the artifacts four blind runs produced ZERO of while nothing noticed. Everything
    // printed below is read back off disk; the writers swallow exceptions into a LogError and return
    // false, and on an empty inventory they write a one-line placeholder and return TRUE.
    //
    // MODEL FILES READ ONCE, HERE, AND HANDED TO BOTH CALLERS BELOW. The stems drive lineage
    // resolution exactly as before; the TEXT is new (SNOW-3979042 Phase 1c) and exists so the
    // reconciliation gate inside ProducerReports.Emit can find every !!!RESOLVE EWI!!! marker actually
    // shipped, rather than trusting that a report built from the same registrations agrees with itself.
    var modelSqlFiles = Directory.Exists(Path.Combine(dbtProjectDir, "models"))
      ? Directory.GetFiles(Path.Combine(dbtProjectDir, "models"), "*.sql", SearchOption.AllDirectories)
      : [];
    var modelSqlByFileStem = modelSqlFiles
      .Select(f => (Stem: Path.GetFileNameWithoutExtension(f), Text: File.ReadAllText(f)))
      .Where(t => t.Stem is not null)
      .ToDictionary(t => t.Stem!, t => t.Text, StringComparer.Ordinal);
    var modelFileStems = modelSqlByFileStem.Keys.ToList();

    var reports = ProducerReports.Emit(
      outRoot,
      ir.Pipeline,
      ir.ModelNamesByNodeId,
      ir.SourceRelationsByNodeId,
      modelFileStems,
      modelSqlByFileStem,
      ir.UnsupportedNodes.Select(n => (n.Id, n.Name, n.NativeKind)).ToList(),
      assessment,
      ewiInformation,
      sourceDocumentName: sourceDocument is null
        ? "producer://" + unitName
        : Path.GetFileName(sourceDocument),
      platformId: platformId,
      logger);

    // PRINTED UNCONDITIONALLY, INCLUDING THE ZEROS, for the reason the source-relation line gives:
    // a silent line makes "no lineage was produced" and "lineage was produced" look identical, and
    // that is precisely how zero-of-186 survived four platforms.
    Console.WriteLine(
      $"lineage rows: {reports.LineageRowsStored} stored of {reports.LineageRowsOffered} offered"
      + (reports.LineageRowsOffered == 0 ? " -- NO LINEAGE AT ALL" : string.Empty));
    foreach (var (relation, count) in reports.LineageRowsByRelation.OrderBy(kv => kv.Key, StringComparer.Ordinal))
    {
      Console.WriteLine($"  lineage   : {count,3}  {relation}");
    }

    Console.WriteLine(
      $"issue rows  : {reports.EwiRowsOffered} EWI + {reports.FdmRowsOffered} FDM registered by the "
      + "engine's own translators"
      + (reports.EwiRowsOffered + reports.FdmRowsOffered == 0 ? " -- NONE RAISED" : string.Empty));
    Console.WriteLine($"element rows: {reports.ElementRowsOffered}");
    foreach (var report in reports.Reports)
    {
      var state = !report.Written ? "ABSENT"
        : report.IsPlaceholder ? "PLACEHOLDER (no rows)"
        : $"{report.DataRows} data row(s)";
      Console.WriteLine($"  report    : {report.Name,-34} {state}{(report.Error is null ? string.Empty : "  " + report.Error)}");
    }

    foreach (var warning in reports.Warnings)
    {
      Console.WriteLine($"  WARN      : {warning}");
    }

    // ---- SNOW-3979042 PHASE 1c: MARKER/REPORT RECONCILIATION -------------------------------
    // PRINTED UNCONDITIONALLY, including the zero-failure case, for the same reason every other count
    // in this method is: "the gate ran and found nothing" and "the gate did not run" must not look
    // identical. `aifirst-migrate.sh` stage 4 greps this exact prefix ("RECONCILE FAIL") out of the
    // captured emitter log and turns a non-zero count into `degraded=1` -- see that script's stage 4
    // for the wiring. A failure here is NEVER a reason to remove the marker, downgrade a status, or
    // filter a code out of a report; it is a reason to fix the report, or to say plainly that the
    // underlying question (should this platform's document reach this translator at all) is open.
    Console.WriteLine(
      $"reconcile   : {reports.ReconciliationMarkersChecked} SQL marker(s) checked against "
      + $"ETL.Elements/ETL.Issues, {reports.ReconciliationFailures.Count} failure(s)");
    foreach (var failure in reports.ReconciliationFailures)
    {
      Console.WriteLine($"  RECONCILE FAIL : {failure}");
    }

    return Directory
      .GetFiles(outRoot, "*", SearchOption.AllDirectories)
      .Select(f => Path.GetRelativePath(outRoot, f).Replace('\\', '/'))
      .OrderBy(f => f, StringComparer.Ordinal)
      .ToList();
  }

  /// <summary>
  /// Re-emits ETL lineage over a tree that stages 3b/3c have already amended.
  /// </summary>
  /// <remarks>
  /// The IR is re-hydrated rather than carried across a process boundary: hydration is deterministic
  /// and cheap, and the alternative is a second serialised copy of the graph that can drift from the
  /// one the models were built from. The MODEL FILE STEMS are read off disk exactly as the first pass
  /// reads them, so a lineage row still names what a <c>ref()</c> names.
  /// </remarks>
  private static int RunRelineage(string irPath, string outRoot, string? sourceDocument)
  {
    if (!File.Exists(irPath))
    {
      throw new FileNotFoundException($"producer IR not found: {irPath}", irPath);
    }

    var logger = new CapturingLogger();
    var platformId = sourceDocument is null ? "unstated" : Path.GetExtension(sourceDocument).TrimStart('.');
    var ir = AiFirstProducerIrHydrator.Hydrate(File.ReadAllText(irPath), platformId);
    var modelsRoots = Directory.Exists(Path.Combine(outRoot, "Output", "ETL"))
      ? Directory.GetDirectories(Path.Combine(outRoot, "Output", "ETL"), "models", SearchOption.AllDirectories)
      : [];
    var stems = modelsRoots
      .Where(d => !d.Contains(Path.DirectorySeparatorChar + "target" + Path.DirectorySeparatorChar, StringComparison.Ordinal)
               && !d.Contains("dbt_internal_packages", StringComparison.Ordinal))
      .SelectMany(d => Directory.GetFiles(d, "*.sql", SearchOption.AllDirectories))
      .Select(Path.GetFileNameWithoutExtension)
      .Where(x => x is not null)
      .Select(x => x!)
      .Distinct(StringComparer.Ordinal)
      .ToList();

    var result = ProducerReports.EmitLineageOnly(
      outRoot,
      ir.Pipeline,
      ir.ModelNamesByNodeId,
      ir.SourceRelationsByNodeId,
      stems,
      sourceDocument is null ? "producer://" + Path.GetFileNameWithoutExtension(irPath) : Path.GetFileName(sourceDocument),
      platformId,
      logger);

    Console.WriteLine(
      $"lineage rows: {result.Stored} stored of {result.Offered} offered (re-emitted over the shipped tree)");
    foreach (var (relation, count) in result.ByRelation.OrderBy(kv => kv.Key, StringComparer.Ordinal))
    {
      Console.WriteLine($"  lineage   : {count,3}  {relation}");
    }

    var state = !result.Report.Written ? "ABSENT"
      : result.Report.IsPlaceholder ? "PLACEHOLDER (no rows)"
      : $"{result.Report.DataRows} data row(s)";
    Console.WriteLine($"  report    : {result.Report.Name,-34} {state}");
    foreach (var warning in result.Warnings)
    {
      Console.WriteLine($"  WARN      : {warning}");
    }

    return 0;
  }

  // ==========================================================================================
  // SPIKE 4 — orchestration for a platform the engine has never heard of.
  // Emits <unit>.sql for a DataStage-shaped unit: 3 jobs, each an orchestrator task whose TaskType
  // NO registered translator claims. Then scan_unit.py is run against the result to see whether the
  // unsupported path still produces scannable elements.
  // ==========================================================================================
  private static int RunNovelOrchestration(string outRoot)
  {
    const string UnitName = "MaskDemoNovel";

    // Three DataStage jobs. Names and platform type are producer-supplied strings; nothing here comes
    // from a parser, which is the whole point.
    var jobs = new[] { "DictSubst", "LocalOra", "PushDb2" };
    var tasks = jobs
      .Select(j => new ProducerOrchestratorTask(
        // A TaskType no registered translator claims — the unsupported path is what we are measuring.
        TaskType: "DataStageJob",
        Name: j,
        PlatformTaskType: "DSJOB",
        FullName: $@"{UnitName}\{j}",
        DdlIdentifierName: $"{UnitName.ToLowerInvariant()}_{j.ToLowerInvariant()}"))
      .ToList();

    var pipeline = new DagPipeline<IOrchestratorTask>();
    foreach (var t in tasks)
    {
      pipeline.Nodes.Add(new DagNode<IOrchestratorTask>(t.FullName, "Task", t));
    }

    var logger = NullLogger.Instance;
    var registry = new ProducerTaskTranslatorRegistry(
      translators: Array.Empty<IOrchestratorTaskTranslator>(),   // deliberately NONE registered
      logger: logger,
      ewiFormatter: new EwiFormatter(new EwiInformationService(new EwiModelReader(logger))),
      createTaskEmitter: new SsisSfCreateTaskEmitter(
        new NoOpObjectTaggingProvider(), new NoOpTaskConfigJsonGenerator()),
      createProcedureEmitter: new SfCreateProcedureEmitter(new NoOpObjectTaggingProvider()),
      assessmentBuilder: new NoOpEtlAssessmentBuilder(),
      pipeline: pipeline,
      orchestratorName: UnitName,
      topLevelTaskNames: tasks.Select(t => t.FullName).ToHashSet(StringComparer.Ordinal));

    var sql = new StringBuilder();
    foreach (var t in tasks)
    {
      var stmt = registry.EmitUnsupportedTask(t);

      // Markers are applied INSIDE ProducerTaskTranslatorRegistry.GetTranslatedUnsupportedTask,
      // wrapping the task's INNER statement. Marking the CREATE TASK from out here is what produced
      // Elements: 2 of 3 with both attributed to the wrong task — see that override's remarks.
      var w = new StringWriter();
      SqlPrettyPrinter.Instance.Print(
        stmt, w, PrettyPrinterOptions.Spaced(3, 3, maxLineLength: 1000));
      sql.AppendLine(w.ToString());
      sql.AppendLine();
    }

    var unitDir = Path.Combine(outRoot, "Output", "ETL", UnitName);
    Directory.CreateDirectory(unitDir);
    var sqlPath = Path.Combine(unitDir, UnitName + ".sql");
    File.WriteAllText(sqlPath, sql.ToString());

    var text = sql.ToString();
    Console.WriteLine($"tasks emitted     : {tasks.Count} (TaskType 'DataStageJob', 0 translators registered)");
    Console.WriteLine($"CREATE TASK count : {CountOf(text, "CREATE OR REPLACE TASK")}");
    Console.WriteLine($"Start block count : {CountOf(text, "---- Start block")}");
    Console.WriteLine($"End block count   : {CountOf(text, "---- End block")}");
    Console.WriteLine($"EWI count         : {CountOf(text, "SSC-EWI")}");
    Console.WriteLine($"written           : {sqlPath}");
    return 0;
  }

  // SPIKE 3b — drive the REAL TargetTranslator with a no-op Informatica migrator.
  private static int RunTargetProbe()
  {
    var target = new TargetTransformation
    {
      Name = "MaskedCustomer",
      TableName = "MASKED_CUSTOMER",
      SchemaName = "PUBLIC",
      // No PreSql/PostSql/UpdateOverride/SqlQuery: a producer for a novel platform has no
      // Informatica session hooks, so the no-op migrator is the TRUTHFUL answer, not a shortcut.
    };
    target.Columns.Add(new Column { Name = "FirstName", DataType = "string" });
    target.Columns.Add(new Column { Name = "BirthDateYear", DataType = "integer" });

    // A target with NO incoming entity is a malformed graph, not a platform-coupling failure. The
    // first version of this probe omitted the upstream node and BaseEtlElementTranslator threw
    // "Transformation has no incoming entity" — which the registry then degraded honestly, masking
    // the cause behind SSC-EWI-SSIS0009. Give the target a real upstream so the probe tests what it
    // claims to test.
    var upstream = new ExpressionTransformation { Name = "Src" };
    upstream.OutputColumns.Add(new Column { Name = "FirstName", DataType = "string" });
    upstream.OutputColumns.Add(new Column { Name = "BirthDateYear", DataType = "integer" });

    var upstreamNode = new DagNode<Transformation>(upstream.Name, "Expression", upstream);
    var targetNode = new DagNode<Transformation>(target.Name, "Target", target);
    var pipeline = new DagPipeline<Transformation>
    {
      Nodes = [upstreamNode, targetNode],
      Edges = [new DagEdge<Transformation>(upstreamNode, targetNode, null)],
    };

    var logger = NullLogger.Instance;
    var ctx = new AiFirstProducerDataFlowContext(
      pipeline,
      new Dictionary<string, string>(StringComparer.Ordinal)
      {
        [target.Name] = "masked_customer",
        [upstream.Name] = "src",
      },
      new DbtProjectGenerationContext(new RecordingEwiService(), logger),
      new NoOpEtlAssessmentBuilder(),
      logger,
      currentItemName: ProbeDataFlowDirectoryName,
      currentFileName: "producer://TargetProbe");

    // sqlProcessor is passed NULL deliberately: if a target with no SQL hooks never touches it, that is
    // itself part of the answer. A NullReferenceException here would say the processor is mandatory too.
    var translator = new TargetTranslator(new NoOpInfPcSqlValueMigrator(), new NoOpEtlSqlProcessor(), logger);

    // Call the translator DIRECTLY first. TransformationUnitTranslator wraps Translate in a
    // try/catch that routes to GenerateUnsupportedElementConversion, which is correct behaviour but
    // discards the exception into an EWI string — so the registry hides exactly the cause this probe
    // is trying to read.
    try
    {
      var direct = translator.Translate((Transformation)target, ctx);
      Console.WriteLine($"DIRECT CALL SUCCEEDED: {direct.Length} result(s)");
    }
    catch (Exception ex)
    {
      Console.WriteLine($"DIRECT CALL THREW: {ex.GetType().Name}");
      Console.WriteLine($"  message: {ex.Message}");
      Console.WriteLine($"  at     : {ex.StackTrace?.Split('\n')[0].Trim()}");
      if (ex.InnerException is not null)
      {
        Console.WriteLine($"  inner  : {ex.InnerException.GetType().Name}: {ex.InnerException.Message}");
      }
    }

    Console.WriteLine();
    var results = new TransformationUnitTranslator([translator], reusableTransformationTracker: null)
      .Translate(target, ctx);

    Console.WriteLine($"results        : {results.Length}");
    for (var i = 0; i < results.Length; i++)
    {
      Console.WriteLine($"  [{i}] {results[i].GetType().Name}");
      if (results[i] is ISqlQueryForDbt q)
      {
        var model = DbtModelFactory.CreateModel(q, ctx);
        Console.WriteLine($"      model name : {model.Name}");
        Console.WriteLine($"      path       : {string.Join("/", model.GetModelPathParts())}");
        Console.WriteLine("      ---- SQL ----");
        Console.WriteLine(model.GetModelContent());
      }
    }

    return 0;
  }

  /// <summary>
  /// Stamps every model file whose node carries TIER-2, model-authored facts.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE DEFECT, MEASURED. <c>poc/blind-run/runU/pentaho/.../int_derive_fullname_and_birthyear.sql</c>
  /// shipped <c>FirstName || ' ' || MiddleName || ' ' || LastName AS FullName</c> and
  /// <c>YEAR(BirthDate) AS BirthYear</c> with no marker of any kind. Both expressions were authored by
  /// a MODEL: the .ktr states them in Java (<c>FirstName + " " + MiddleName + " " + LastName</c> and
  /// <c>BirthDate.getYear() + 1900</c>) and no engine translator lowers Java. The file was
  /// indistinguishable from an expression read from the document and lowered by a translator. Tier 3
  /// is stamped <c>SSC-AI-AUTHORED</c>; tier 2 was invisible, so stage 4's MODEL-AUTHORED count read 2
  /// on a Pentaho tree in which 3 of 4 models hold model-authored content.
  /// </para>
  /// <para>
  /// A DIFFERENT MARKER, DELIBERATELY, AND NOT A WEAKER ONE. <c>SSC-AI-ASSISTED</c> is not
  /// <c>SSC-AI-AUTHORED</c> because the two are different fidelity positions and collapsing them
  /// would lose information a reviewer needs. Tier 2: the ENGINE's translators rendered this model,
  /// from a payload a model supplied -- the SQL around the payload has been through
  /// <c>ExpressionTransformationTranslator</c>, <c>DbtModelFactory</c> and the production writers.
  /// Tier 3: a model wrote the whole file and no engine component ever saw it. Tier 2 is the stronger
  /// position, and the marker says which one this is rather than flattening both to "AI wrote it".
  /// </para>
  /// <para>
  /// THE WORDING FOLLOWS <c>ai_fill.py</c>'s DISCIPLINE, and that discipline was paid for: its stamp
  /// used to assert "RUNNABLE, NOT VERIFIED" and RUNNABLE was measured false. So this states
  /// PROVENANCE (which fields a model authored, and from which sidecar key) and the ABSENCE of
  /// verification, and claims nothing whatsoever about whether the SQL is right. It says so
  /// explicitly, because a marker on correct SQL that reads as an accusation is its own false report.
  /// </para>
  /// <para>
  /// A TIER-3 FILL LATER OVERWRITES THIS FILE AND THAT IS CORRECT. <c>ai_fill.py</c> runs at stage 3b
  /// and replaces a model that carries a blocking EWI or projects no columns, writing its own
  /// <c>SSC-AI-AUTHORED</c> header. Once the body is gone the tier-2 marker no longer describes the
  /// file, so it must not survive. MEASURED on Pentaho: <c>Filter BirthYear</c> is tier 2 for its
  /// predicate and then tier 3 because <c>FilterTranslator</c> threw (ENG-020), and its file ends up
  /// correctly stamped tier 3 alone.
  /// </para>
  /// </remarks>
  /// <param name="dbtProjectDir">The dbt project the models were written into.</param>
  /// <param name="modelFileRelativePathByNodeId">
  /// The exact file (relative to <paramref name="dbtProjectDir"/>'s <c>models/</c>) the translate loop
  /// wrote FOR THAT NODE, present only when the node's outcome was ok -- not SUBST, not EMPTY, not
  /// THREW -- and the node is not an <c>UnsupportedTransformation</c> placeholder. Threaded from the
  /// translate loop rather than re-derived by name: a modelName match (exact-or-suffix) let one node's
  /// "summary" collide with another's "int_customer_summary" and stamp the wrong file.
  /// </param>
  /// <param name="ir">The hydrated IR, carrying the producer's MODEL-provenance facts per node.</param>
  /// <returns>The file names stamped, for the driver's log.</returns>
  private static IReadOnlyList<string> StampModelAuthored(
    string dbtProjectDir,
    IReadOnlyDictionary<string, string> modelFileRelativePathByNodeId,
    AiFirstProducerIrHydrator.HydratedIr ir)
  {
    var stamped = new List<string>();
    var modelsDir = Path.Combine(dbtProjectDir, "models");
    if (ir.ModelAuthoredByNodeId.Count == 0 || !Directory.Exists(modelsDir))
    {
      return stamped;
    }

    foreach (var pair in ir.ModelAuthoredByNodeId.OrderBy(kv => kv.Key, StringComparer.Ordinal))
    {
      var nodeId = pair.Key;
      var facts = pair.Value;

      // Absence means the node's outcome was not "ok" (SUBST/EMPTY/THREW) or it is an unresolved
      // UnsupportedTransformation placeholder -- neither carries the tier-2 content the sidecar
      // described, so it must not be stamped.
      if (!modelFileRelativePathByNodeId.TryGetValue(nodeId, out var relativePath))
      {
        continue;
      }

      var file = Path.Combine(modelsDir, relativePath);
      if (!File.Exists(file))
      {
        continue;
      }

      var body = File.ReadAllText(file);
      if (body.Contains("SSC-AI-ASSISTED", StringComparison.Ordinal))
      {
        continue;
      }

      var header = new StringBuilder();
      header.AppendLine(
        "-- SSC-AI-ASSISTED: part of this model's content was authored by a MODEL and was NOT read");
      header.AppendLine("--                  from the source document by a deterministic rule.");
      header.AppendLine($"-- Source element : {nodeId}");
      header.AppendLine(
        "-- Tier           : 2 -- SnowConvert's own translators rendered this model. A model supplied");
      header.AppendLine(
        "--                  the payload listed below because the source dialect has no engine");
      header.AppendLine("--                  translator.");
      header.AppendLine("-- Model-authored :");
      foreach (var fact in facts)
      {
        header.AppendLine($"--   {fact.Path}  <- {fact.Sidecar}");
        if (!string.IsNullOrWhiteSpace(fact.Detail))
        {
          header.AppendLine($"--     {fact.Detail}");
        }
      }

      header.AppendLine(
        "-- Verification   : NONE. These values were not read from the document, were not checked by");
      header.AppendLine(
        "--                  an engine expression translator, and were not compared against source");
      header.AppendLine("--                  behaviour by this stage. Review before use.");
      // THE TIER-3 MARKER IS NOT SPELLED OUT IN THIS TEXT, AND THAT IS A CAUGHT DEFECT.
      // The first version of this header ended "...a STRONGER position than tier 3
      // (SSC-AI-AUTHORED), where...". Two things then broke, both measured on the Pentaho
      // tree in the first run after this stamp existed:
      //   * stage 4's `grep -rl "SSC-AI-AUTHORED"` matched the tier-2 file, so
      //     MODEL-AUTHORED read 3 where 2 models were tier-3 filled -- a marker that
      //     miscounted the very thing it was added to count;
      //   * worse, `ai_fill.py` skips any file already containing that marker, so
      //     `int_filter_birthyear` -- tier 2 for its predicate and tier 3 because
      //     FilterTranslator threw -- STOPPED BEING FILLED. Adding provenance silently
      //     removed a migration.
      // A marker string inside prose is still a marker string. The comparison is made in
      // words instead.
      header.AppendLine(
        "-- NOT a claim    : nothing here says the SQL is wrong. Tier 2 is engine-rendered from a");
      header.AppendLine(
        "--                  model-supplied payload, which is a STRONGER position than tier 3,");
      header.AppendLine(
        "--                  where a model wrote the whole model body and no engine component");
      header.AppendLine("--                  saw it.");
      File.WriteAllText(file, header.ToString() + body);
      stamped.Add(Path.GetFileName(file));
    }

    return stamped;
  }

  private static int CountOf(string haystack, string needle)
  {
    var n = 0;
    var i = haystack.IndexOf(needle, StringComparison.Ordinal);
    while (i >= 0)
    {
      n++;
      i = haystack.IndexOf(needle, i + needle.Length, StringComparison.Ordinal);
    }

    return n;
  }

  // Copied from the fixture, which duplicated it from the engine's private static
  // GetDefaultArtifacts(). The duplication IS the finding — see the call site.
  private static DbtMacro[] DefaultMacros() =>
  [
    new DbtMacro(
      "m_update_row_count_variable",
      new[] { "variable_name", "target_relation", "variable_scope" },
      @"  {# Step 1: Construct the specific SQL string for counting rows. #}
  {% set count_sql = ""SELECT COUNT(*) FROM "" ~ target_relation %}
  {{ log(""m_update_row_count_variable started. Received value: "" ~ count_sql, info=True) }}

  {# Step 2: Call m_update_control_variable with the COUNT query. #}
  {{ m_update_control_variable(variable_name, count_sql, variable_scope) }}"),
    new DbtMacro(
      "m_update_control_variable",
      new[] { "variable_name", "new_value_sql", "variable_scope" },
      @"  UPDATE public.control_variables
  SET
    variable_value = ({{new_value_sql}}),
    last_updated_at = CURRENT_TIMESTAMP()
  WHERE
    variable_name = '{{ variable_name }}'
    AND variable_scope = '{{ variable_scope }}';"),
  ];

  /// <summary>
  /// Resolves the orchestration identity from the producer's IR, or returns null when the IR states
  /// no container and there is nothing honest to name the unit after.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE CONTAINER IS ALREADY IN THE IR, and <c>HydratedIr.UnsupportedNodes</c>'s own doc comment says
  /// why it is surfaced: "on SSIS this is exactly the control-flow container the ORCHESTRATION half of
  /// the producer has to emit a task for, so discarding it would throw away the one fact the other
  /// half needs." That fact was surfaced and then not used — the orchestration half read three
  /// constants instead.
  /// </para>
  /// <para>
  /// MEASURED, one container node per document on three of four blind platforms:
  /// SSIS <c>Package\DFT Load Customer Summary</c> (<c>Microsoft.Pipeline</c>, modelName
  /// <c>dft_load_customer_summary</c>); DataStage <c>CustomerSummaryDerive</c> (<c>DSJOB</c>);
  /// Pentaho <c>customer_summary_fullname_birthyear</c> (<c>transformation</c>). INFORMATICA HAS NONE:
  /// its IR is four data-flow nodes and no container, because the real Informatica orchestration unit
  /// is the workflow/session and the producer's document is a single mapping. So Informatica gets no
  /// task graph, stated as absent — the alternative would be a task named after a mapping, asserting
  /// an orchestration container Informatica does not have at that level.
  /// </para>
  /// <para>
  /// UNIT NAME. Taken from the source DOCUMENT stem, not from the container: the container is the
  /// data-flow unit (an SSIS Data Flow Task sits INSIDE a package), so using it for both would name
  /// the parent task after the child. The document stem is the closest thing to the enclosing unit
  /// that the producer states, and it is at least a name that appears in the input. Where the two
  /// genuinely coincide — DataStage, where the DSJOB is both — the emitted names repeat, which is a
  /// true property of that platform rather than a defect here.
  /// </para>
  /// </remarks>
  private static OrchestrationIdentity? ResolveOrchestrationIdentity(
    AiFirstProducerIrHydrator.HydratedIr ir, string? sourceDocument)
  {
    // First container the producer declared. More than one means a multi-unit document, which this
    // driver does not yet emit for; it is reported rather than silently collapsed onto the first.
    var containers = ir.UnsupportedNodes;
    if (containers.Count == 0)
    {
      return null;
    }

    if (containers.Count > 1)
    {
      Console.WriteLine(
        $"orchestration: {containers.Count} container nodes declared "
        + $"({string.Join(", ", containers.Select(c => c.Id))}). This driver emits ONE unit, so only "
        + "the first is used and the rest have NO task graph. Not a silent collapse: counted here.");
    }

    var container = containers[0];

    // The dbt project directory, computed by THE SAME ROUTINE THE ENGINE USES TO NAME THE PROJECT IN
    // THE SQL. `SsisDataPipelineTaskTranslator:54` does
    // `projectName = SsisNameUtilities.GetComponentNameWithoutPackage(task.FullName)` and hands that
    // to `EXECUTE DBT PROJECT public.<projectName>`. Calling it here rather than guessing makes the
    // directory on disk and the name in the generated SQL agree BY CONSTRUCTION.
    //
    // MEASURED WHY THIS MATTERS: with the container's own sanitized `modelName` used instead, SSIS
    // emitted `EXECUTE DBT PROJECT public.DFT_Load_Customer_Summary` while the models sat in
    // `dft_load_customer_summary/`. Same string on a case-insensitive macOS filesystem, two different
    // directories on Linux — a defect that cannot be reproduced on the machine that shipped it.
    //
    // The routine is SSIS-NAMED and platform-NEUTRAL in behaviour: split the refId on '\', sanitize
    // each segment, join with '_'. On a container id with no separator (DataStage `CustomerSummaryDerive`,
    // Pentaho `customer_summary_fullname_birthyear`) it returns the sanitized id unchanged.
    var directory = SsisNameUtilities.GetComponentNameWithoutPackage(container.Id);
    if (string.IsNullOrWhiteSpace(directory) || directory == "unknown")
    {
      directory = !string.IsNullOrWhiteSpace(container.ModelName)
        ? container.ModelName!
        : SanitizeIdentifier(container.Name);
    }

    // The unit name is the document stem VERBATIM, not lowercased. GROUND TRUTH, measured against
    // `poc/blind-run/runA/ssis/out/Output/ETL`: real SnowConvert writes
    // `CustomerSummary_DerivedColumn_ConditionalSplit/CustomerSummary_DerivedColumn_ConditionalSplit.sql`
    // for this exact document, and the task-name lowercasing happens INSIDE the emitter, not in the
    // path. Lowercasing here produced a directory the engine would not have written.
    var unitFromDocument = sourceDocument is null
      ? null
      : Path.GetFileNameWithoutExtension(sourceDocument);

    return new OrchestrationIdentity(
      UnitName: string.IsNullOrWhiteSpace(unitFromDocument) ? directory : unitFromDocument!,
      DataFlowFullName: container.Id,
      DataFlowName: container.Name,
      DataFlowDirectoryName: directory,
      NativeKind: string.IsNullOrWhiteSpace(container.NativeKind) ? "(unstated)" : container.NativeKind,
      Source: unitFromDocument is null
        ? $"unit from container name; container from IR node '{container.Id}'"
        : $"unit from document stem; container from IR node '{container.Id}'");
  }

  /// <summary>
  /// One replacement character per illegal character, never a collapsed run — the same deliberately
  /// injective rule finding 31 settled on, because collapsing runs is how two distinct source names
  /// become one identifier and one of the two artifacts is silently overwritten.
  /// </summary>
  private static string SanitizeIdentifier(string name)
  {
    var chars = name.Select(c => char.IsLetterOrDigit(c) ? char.ToLowerInvariant(c) : '_').ToArray();
    var result = new string(chars).Trim('_');
    return result.Length == 0 || char.IsDigit(result[0]) ? "u_" + result : result;
  }

  /// <summary>
  /// Emits the unit's orchestration SQL: the ROOT task for the orchestration unit, then one child task
  /// for the container the IR named.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE DEFECT THIS CLOSED, AND MY FIRST DIAGNOSIS OF IT WAS WRONG. This method used to return the
  /// CHILD task alone, whose <c>AFTER public.customersummary_derivedcolumn_conditionalsplit</c> named
  /// nothing in the file. Recorded first as "a dangling AFTER" — i.e. as a reference to be rewritten.
  /// It is the opposite: the <c>AFTER</c> is CORRECT and names the task that ought to exist. What was
  /// missing is the ROOT TASK of the orchestration unit. MEASURED, the engine's own output for the same
  /// document (<c>poc/blind-run/runA/ssis/out/Output/ETL/CustomerSummary_DerivedColumn_ConditionalSplit/</c>)
  /// is TWO statements, and the first is a no-op <c>AS SELECT 1</c> task carrying provenance metadata —
  /// the Snowflake task-graph idiom, where the root has no predecessor and every child carries
  /// <c>AFTER</c>. Rewriting the <c>AFTER</c> to point at something that existed would have destroyed a
  /// correct DAG to satisfy a gate.
  /// </para>
  /// <para>
  /// THE ROOT IS NOT HAND-WRITTEN HERE. It comes from
  /// <c>SfCreateTaskEmitter.EmitRootCreateTaskStatement</c>, reached through the engine's own task-graph
  /// mapper <c>SsisControlFlowMapper</c> (<c>: EtlOrchestratorToTaskGraphMapper</c>), which is also what
  /// assembles the file: root, then each child statement, with the engine's own separators. So the
  /// dummy <c>SELECT 1</c> body, the <c>public</c> schema, the name formatting and the statement order
  /// are the engine's rules rather than a second copy of them. The mapper needed two things a producer
  /// was previously said not to have — an <c>IEtlOrchestrator</c> and an
  /// <c>IOrchestrationConversionContext</c> — and both are producer-supplied now; see
  /// <see cref="ProducerEtlOrchestrator"/> and <see cref="ProducerOrchestrationConversionContext"/>.
  /// </para>
  /// <para>
  /// WHY THE ROOT AND THE CHILD'S <c>AFTER</c> AGREE BY CONSTRUCTION, not by coincidence. The child's
  /// predecessor list is empty, so <c>SfCreateTaskEmitter.GetPredecessorNames</c> falls back to
  /// <c>public.GetFormattedSsisIdentifier(translationContext.OrchestratorName)</c>; the root's name is
  /// <c>public.FormatRootTaskName(orchestrator.GetName())</c>, and the SSIS emitter's
  /// <c>FormatRootTaskName</c> IS <c>GetFormattedSsisIdentifier</c>. Both sides are handed
  /// <c>identity.UnitName</c>, so the same function is applied to the same string twice.
  /// </para>
  /// <para>
  /// NOT BYTE-IDENTICAL TO RUN A, AND IT CANNOT BE — stated here because a previous pass claimed byte
  /// identity without running a diff and the claim was false. The remaining difference is exactly one
  /// line: Run A's root task carries a <c>COMMENT</c> holding
  /// <c>"convertedOn": "08/02/2026"</c> and <c>"migrationid": "x8SfAVd0IHyEUn94kjbxCg=="</c>. That
  /// comment is produced by <c>ObjectTaggingProvider</c> from <c>IMigrationDataService.MigrationId</c>,
  /// which <c>ContainerConfigurationBuilder.cs:105</c> mints as
  /// <c>Convert.ToBase64String(Guid.CreateVersion7().ToByteArray())</c> — FRESH PER RUN. So no run
  /// reproduces Run A's root task byte-for-byte, including a second engine run on the same document on
  /// the same day. Our tagging provider is the no-op (it returns <c>null</c>, so the clause is omitted),
  /// which is why the line is absent rather than present-and-different.
  /// </para>
  /// <para>
  /// AND WIRING THE REAL PROVIDER WAS REJECTED ON EVIDENCE, not skipped. <c>ObjectTaggingProvider</c>
  /// takes a <c>SourceLanguage</c> and writes it into the tag as <c>"component"</c>. Run A says
  /// <c>"component": "transact"</c>, so matching it means hardcoding <c>SourceLanguage.Transact</c> —
  /// a member of a closed 21-value enum with no DataStage, Pentaho or ADF member (ENG-017's shape).
  /// That is precisely the SSIS-named constant on every platform that the header of this file records
  /// as the project's worst neutrality defect, and closing a one-line cosmetic diff is not worth
  /// reintroducing it.
  /// </para>
  /// <para>
  /// THE CLASSES ARE STILL SSIS-NAMED AND THAT IS ENG-018, NOT A CHOICE HERE.
  /// <c>SsisExecutableToSfTaskTranslator</c> gates whether a <c>CREATE TASK</c> is emitted at all on
  /// <c>context is SsisControlFlowTaskTranslationContext { IsReusablePackage: false }</c>, and
  /// <c>SsisDataPipelineTaskTranslator</c> derives from it. Only two concrete translation contexts
  /// exist and both are platform-named, so a producer either passes the SSIS one or gets no task. The
  /// same is true one level up: the only two task-graph mappers are SSIS's and Informatica's.
  /// </para>
  /// <para>
  /// What HAS changed is that every STRING is now the producer's. The arguments below — the task's
  /// display name, its refId, the package name and the unit name — are the container's own name, the
  /// container's own platform-native path, and the unit name, so the emitted block label, the root task
  /// name and the child task name all come from the input document. The type names never reached the
  /// output (finding 35 measured exactly one leak, the issue name); the strings did, on every line.
  /// </para>
  /// </remarks>
  /// <param name="identity">The derived identity.</param>
  /// <param name="sourceDocumentPath">
  /// The input document path, for the conversion context. Not read on the root-task path; the context's
  /// constructor rejects a blank one, so it is passed rather than defaulted.
  /// </param>
  /// <param name="outRoot">The migration output root, same argument.</param>
  /// <returns>The pretty-printed orchestration SQL: root task first, then the container's task.</returns>
  private static string EmitOrchestrationSql(
    OrchestrationIdentity identity, string sourceDocumentPath, string outRoot)
  {
    var createTaskEmitter = new SsisSfCreateTaskEmitter(
      new NoOpObjectTaggingProvider(), new NoOpTaskConfigJsonGenerator());

    var task = new SsisDataPipelineTask(
      name: identity.DataFlowName,
      refId: identity.DataFlowFullName,
      packageName: identity.UnitName);

    var pipeline = new DagPipeline<IOrchestratorTask>();
    pipeline.Nodes.Add(new DagNode<IOrchestratorTask>(task.FullName, "Task", task));

    var context = new SsisControlFlowTaskTranslationContext(
      fileName: identity.UnitName,
      orchestratorAssessmentBuilder: new NoOpEtlAssessmentBuilder(),
      additionalProcedures: new List<ICompound>(),
      orchestratorPipeline: pipeline,
      orchestratorName: identity.UnitName,
      allDefinitions: new List<EtlVariableDefinition>(),
      topLevelTaskNames: [task.FullName],
      orchestrationContext: null!,
      isReusablePackage: false);

    var translator = new SsisDataPipelineTaskTranslator(
      new PassThroughIssueCommentGenerator(),
      createTaskEmitter,
      new ExecuteDbtProjectStatementGenerator(),
      new TaskVariableWrapperService(
        Array.Empty<IOrchestratorTaskVariableWrapper>(), NullLogger.Instance));

    var childTask = translator.Translate(task, context)
      ?? throw new InvalidOperationException("the translator returned no statement at all");

    // ---- the root task, from the engine's own task-graph mapper --------------------------------
    // The description is EMPTY and that is what the producer states: `HydratedIr.UnsupportedNodes`
    // carries (id, name, nativeKind, modelName) and no description, so there is nothing to pass.
    // Run A's tag reads `"description": ""` for this same document, so nothing is lost by it either.
    var orchestrator = new ProducerEtlOrchestrator(identity.UnitName, string.Empty);
    var conversionContext = new ProducerOrchestrationConversionContext(
      inputFilePath: sourceDocumentPath,
      outputPath: outRoot,
      fileName: identity.UnitName,
      orchestratorName: identity.UnitName);

    var mapper = new SsisControlFlowMapper(
      new PrettyPrinterService(), createTaskEmitter, new PassThroughIssueCommentGenerator());

    return mapper.GetSnowflakeSqlOrchestrator(
      orchestrator,
      [childTask],
      conversionContext,
      new OrchestrationConversionDetails(new NoOpEtlAssessmentBuilder()));
  }
}
