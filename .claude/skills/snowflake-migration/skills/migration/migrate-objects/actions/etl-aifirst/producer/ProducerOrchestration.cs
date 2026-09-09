// SPIKE 4 — can a producer declare orchestration for a platform the engine does not know?
//
// THE QUESTION behind it: scan_unit.py reports `Elements: 0` on the DataStage tree and `Elements: 1`
// on SSIS. Element discovery reads only the unit-level orchestration SQL and its
// `---- Start block` / `---- End block` markers, so a tree with no orchestration SQL scores zero
// however good its dbt models are.
//
// WHAT THIS FILE ESTABLISHES, measured rather than argued:
//   1. `OrchestratorTaskTranslatorRegistry` is `public abstract` with only TWO abstract members, so a
//      producer can subclass it from OUTSIDE the engine assembly. No engine change is needed to
//      introduce a new platform's orchestration.
//   2. An UNREGISTERED TaskType does not vanish. The dispatch at
//      OrchestratorTaskTranslatorRegistry.cs:87 falls through to GetTranslatedUnsupportedTask, which
//      "Always wrap[s] in CREATE TASK". Whether that carries the boundary markers is what the run
//      measures.
//   3. `NotSupportedIssueName` is abstract and must come from the closed 888-member IssueName enum,
//      which has no platform-neutral member. That is ENG-017, and it bites here too: the only two
//      orchestration registries in the engine hard-code SSISControlFlowElementNotConverted and
//      InformaticaPcWorkflowElementNotConverted respectively.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Linq;
using Artinsoft.Common.AST;
using Mobilize.AnsiSql.AST;
using Mobilize.Snow.Assessment.AssessmentMode.ETLAndReporting;
using Mobilize.Snow.Issues;
using Snowflake.Etl.AST;
using Snowflake.SnowConvert.EtlToDbt;
using Snowflake.SnowConvert.EtlToDbt.Context;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration;
using Snowflake.SnowConvert.EtlToDbt.EtlOrchestration.OrchestratorTaskTranslators;
using Snowflake.SnowConvert.EtlToDbt.FileSystem;
using Snowflake.SnowConvert.EtlToDbt.Services.Interfaces;
using Snowflake.SnowConvert.EtlToDbt.Utils;
using Snowflake.SnowConvert.EtlToDbt.Variables;

/// <summary>
/// One orchestrator task for a platform the engine has never heard of. All five interface members are
/// plain strings the producer supplies, so nothing here is derived from a parser.
/// </summary>
/// <param name="TaskType">
/// The dispatch key (`OrchestratorTaskTranslatorRegistry.cs:87`, OrdinalIgnoreCase). Deliberately a
/// value NO registered translator claims, so the unsupported path is what gets exercised.
/// </param>
/// <param name="PlatformTaskType">The source platform's own name for the element, e.g. a DataStage `DSJOB`.</param>
internal sealed record ProducerOrchestratorTask(
  string TaskType,
  string Name,
  string PlatformTaskType,
  string FullName,
  string DdlIdentifierName) : IOrchestratorTask;

/// <summary>
/// THE ORCHESTRATION UNIT ITSELF — the thing whose ROOT TASK was missing.
/// </summary>
/// <remarks>
/// <para>
/// WHAT WAS WRONG, MEASURED. Our SSIS orchestration file held ONE statement:
/// <c>CREATE OR REPLACE TASK public.customersummary_derivedcolumn_conditionalsplit_dft_load_customer_summary
/// ... AFTER public.customersummary_derivedcolumn_conditionalsplit</c>. The engine's own output for the
/// same document (<c>poc/blind-run/runA</c>) holds TWO, and the first is the one that clause names.
/// So the <c>AFTER</c> was CORRECT and the target did not exist: a Snowflake task graph whose only task
/// can never be resumed, because <c>ALTER TASK ... RESUME</c> on a child requires its predecessor.
/// The defect was NOT a dangling reference to be rewritten — it was a MISSING ROOT.
/// </para>
/// <para>
/// This is the producer's <see cref="IEtlOrchestrator"/>: the unit of work whose DAG the child tasks
/// hang off. It exists so the engine's OWN root emitter
/// (<c>SfCreateTaskEmitter.EmitRootCreateTaskStatement</c>, reached through
/// <c>EtlOrchestratorToTaskGraphMapper.GetSnowflakeSqlOrchestrator</c>) can be called instead of
/// hand-writing <c>CREATE TASK ... AS SELECT 1</c> here. Everything about the emitted root — its
/// schema, its name formatting, its dummy body, its option order — is then the engine's rule and not
/// a copy of it.
/// </para>
/// <para>
/// ONE ORCHESTRATION UNIT PER PLATFORM, and the mapping is stated rather than assumed:
/// SSIS Control Flow (the package), Informatica Workflow, DataStage Job, Pentaho Transformation.
/// The producer names the unit; this record carries no platform vocabulary at all.
/// </para>
/// <para>
/// <c>GetInnerTasks</c> and <c>GetLinks</c> return EMPTY, and that is not a stub. The root emitter
/// reads neither: it takes only the orchestrator's NAME (via
/// <c>GetRootTaskOrchestratorName</c>) and its DESCRIPTION (via <c>GetCommentClause</c>). The child
/// task graph reaches the mapper as already-translated <c>ISqlStatement</c>s, on the same path the
/// engine's own converter uses. Returning a second, differently-shaped copy of the graph here would
/// be two sources of truth for one fact.
/// </para>
/// </remarks>
/// <param name="Name">The unit's name. Becomes the root task's DDL identifier after the emitter formats it.</param>
/// <param name="Description">
/// The unit's description, verbatim from the source document or empty. Reaches the root task's
/// <c>COMMENT</c> clause only when a tagging provider is supplied — see
/// <c>Program.EmitOrchestrationSql</c> for why ours is not.
/// </param>
internal sealed record ProducerEtlOrchestrator(string Name, string Description) : IEtlOrchestrator
{
  public string GetName() => this.Name;

  public string GetDescription() => this.Description;

  public IEnumerable<IEtlOrchestratorTaskLink> GetLinks() => Array.Empty<IEtlOrchestratorTaskLink>();

  public IEnumerable<IEtlOrchestratorTask> GetInnerTasks() => Array.Empty<IEtlOrchestratorTask>();
}

/// <summary>
/// The <see cref="IOrchestrationConversionContext"/> a producer never had.
/// </summary>
/// <remarks>
/// <para>
/// <c>ProducerTaskTranslatorRegistry</c>'s own doc comment records the constraint this removes:
/// "a producer has no orchestration-conversion context to hand it — the same constraint DESIGN.md
/// 2.6.3 records". That was true of the CONCRETE contexts (both are platform-named and both are built
/// by a platform converter), and false of the ABSTRACT one:
/// <c>OrchestrationConversionContext</c> is <c>public abstract</c> with a <c>protected</c> constructor
/// and every member already implemented, so a producer outside the engine assembly can subclass it.
/// Nothing in the engine changed to make this work.
/// </para>
/// <para>
/// WHAT THE ROOT EMITTER ACTUALLY READS FROM IT, checked against
/// <c>SfCreateTaskEmitter.EmitRootCreateTaskStatement</c> line by line, so that none of the values
/// below is a guess dressed as a default:
/// <c>AllDefinitions</c> (empty -> no <c>CONFIG</c> clause, matching the engine's own output for a
/// document declaring no variables), <c>VariableStatements</c> (null -> the body is the emitter's
/// <c>SELECT 1</c>), and — on the SSIS subclass only, and only when the orchestrator is a
/// <c>DtsxExecutable</c>, which a producer's never is — the context is passed to
/// <c>GetMainExecutableName</c>. Everything else on the interface
/// (<c>DecoratedSource</c>, <c>GetRelativeOutputFileName</c>, <c>SnowflakeScriptsByDataFlow</c>) is
/// untouched on this path.
/// </para>
/// <para>
/// <c>decoratedSource</c> is therefore passed <c>null!</c>, deliberately and for the reason
/// <c>NoOpServices</c> states about Moq: if a code path we take dereferences it, we want the
/// <c>NullReferenceException</c> rather than a plausible-looking stand-in that hides which paths were
/// exercised.
/// </para>
/// </remarks>
internal sealed class ProducerOrchestrationConversionContext : OrchestrationConversionContext
{
  internal ProducerOrchestrationConversionContext(
    string inputFilePath,
    string outputPath,
    string fileName,
    string orchestratorName)
    : base(
      inputFilePath: inputFilePath,
      paths: new MigrationPathInfo(
        EtlInputPath: System.IO.Path.GetDirectoryName(inputFilePath) ?? ".",
        OutputPath: outputPath,
        CurrentFileName: fileName),
      assessmentBuilder: new NoOpEtlAssessmentBuilderForFile(),
      fileName: fileName,
      fileSystemService: new FileSystemService(),
      decoratedSource: null!)
  {
    this.OrchestratorName = orchestratorName;
  }
}

/// <summary>
/// A file-level assessment builder that records nothing, for the same reason
/// <see cref="NoOpEtlAssessmentBuilder"/> exists: the root-task path never calls it, and a recording
/// implementation here would put rows in the reports that no translator raised.
/// </summary>
internal sealed class NoOpEtlAssessmentBuilderForFile : IEtlAssessmentBuilderForFile
{
  public IEtlAssessmentBuilderForPipelineContainer CreateBuilderForPipelineElement(
    string categoryName, string containerName) => new NoOpEtlAssessmentBuilder();

  public void RegisterReplatformEntry(
    string categoryName,
    string name,
    string subType,
    EtlReplatformStatus status,
    IssueName[] issues,
    string kind = "N/A",
    string additionalInfo = "",
    string? declarationName = null,
    string? displayName = null)
  {
  }

  public void RegisterEwiEntry(string componentName, IssueName ewi, params object[] args)
  {
  }
}

/// <summary>
/// A producer-owned orchestration registry for a novel platform, subclassing the engine's public
/// abstract base from outside the engine assembly.
/// </summary>
internal sealed class ProducerTaskTranslatorRegistry : OrchestratorTaskTranslatorRegistry
{
  private readonly IEtlAssessmentBuilderForPipelineContainer assessmentBuilder;
  private readonly DagPipeline<IOrchestratorTask> pipeline;
  private readonly string orchestratorName;
  private readonly HashSet<string> topLevelTaskNames;
  private readonly string? platformId;

  internal ProducerTaskTranslatorRegistry(
    IEnumerable<IOrchestratorTaskTranslator> translators,
    Microsoft.Extensions.Logging.ILogger logger,
    IEwiFormatter ewiFormatter,
    ISfCreateTaskEmitter createTaskEmitter,
    ISfCreateProcedureEmitter createProcedureEmitter,
    IEtlAssessmentBuilderForPipelineContainer assessmentBuilder,
    DagPipeline<IOrchestratorTask> pipeline,
    string orchestratorName,
    HashSet<string> topLevelTaskNames,
    string? platformId = null)
    : base(translators, logger, ewiFormatter, createTaskEmitter, createProcedureEmitter)
  {
    this.assessmentBuilder = assessmentBuilder;
    this.pipeline = pipeline;
    this.orchestratorName = orchestratorName;
    this.topLevelTaskNames = topLevelTaskNames;
    this.platformId = platformId;
  }

  /// <summary>
  /// DIALECT-GUARDED (SNOW-3979042 Phase 1b). Still forced onto SOME dialect's code by ENG-017 -- there
  /// is no platform-neutral "element not converted" member in the 888-member IssueName enum -- but no
  /// longer forced onto Informatica's UNCONDITIONALLY. A DataStage/Alteryx/Pentaho/etc. registry now
  /// falls back to the dialect-neutral engine code, matching the pattern the other two guarded
  /// hand-off sites already use (AiFirstProducerIrHydrator.cs, AiFirstProducerDataFlowContext.cs:144).
  /// <see cref="platformId"/> is nullable and defaults to null (no native dialect) rather than being
  /// required, because the two existing call sites of this constructor (RunNovelOrchestration's spike)
  /// never had a platform id to pass -- see that method for why fixing this does not change the real
  /// driver's EmitOrchestrationSql path, which never constructs this registry at all.
  /// </summary>
  protected override IssueName NotSupportedIssueName
    => DialectPlatform.IsInformaticaNative(this.platformId)
      ? IssueName.InformaticaPcWorkflowElementNotConverted
      : IssueName.ExceptionThrownWhileConverting;

  protected override IOrchestratorTaskTranslationContext CreateContext(
    IOrchestrationConversionContext context,
    OrchestratorTraversalDetailsProvider orchestratorTraversalDetailsProvider)
    => this.BuildContext();

  /// <summary>
  /// THE PRODUCER RECIPE SPIKE 4 ESTABLISHES, and the reason it is an override rather than a helper
  /// call at the call site.
  /// <para>
  /// The base implementation emits `CREATE TASK` wrapping an EWI and never calls
  /// <see cref="TaskBoundaryCommentHelper"/> — that helper is invoked only from the SSIS and
  /// Informatica translators. So an unsupported task yields a valid CREATE TASK that `scan_unit.py`
  /// scores as **zero elements**, because element discovery reads `---- Start block` markers.
  /// </para>
  /// <para>
  /// AND THE MARKERS MUST GO INSIDE THE TASK BODY, wrapping the INNER statement — not around the
  /// `CREATE TASK`. Measured: marking the CREATE TASK gave 3 markers, 3 statements and
  /// <b>Elements: 2</b>, with both surviving elements attributed to the WRONG task, because the
  /// scanner treats an element as something nested within a statement and therefore binds each
  /// marker to the PRECEDING one. The engine's own SSIS output places them inside `BEGIN ... END`.
  /// This override reproduces that placement, and the same measurement then gives Elements: 3.
  /// </para>
  /// <para>
  /// No engine change is required for any of it: the base method is documented as overridable
  /// ("Can be overridden by derived classes to implement technology-specific logic"),
  /// <c>GetNotConvertedTaskStatement</c> and <c>GetUnsupportedCreateTask</c> are both
  /// <c>protected</c>, and <c>TaskBoundaryCommentHelper</c> is <c>public static</c>.
  /// </para>
  /// </summary>
  protected override ISqlStatement GetTranslatedUnsupportedTask(
    IOrchestratorTask orchestratorTask,
    IOrchestratorTaskTranslationContext translationContext)
  {
    var inner = this.GetNotConvertedTaskStatement(orchestratorTask, translationContext);
    var marked = TaskBoundaryCommentHelper.AddContainerBoundaryComments(
      [inner], orchestratorTask.FullName);
    return this.GetUnsupportedCreateTask(
      orchestratorTask, translationContext, marked.Single());
  }

  /// <summary>
  /// Exposes the protected unsupported-task path so the spike can drive it WITHOUT an
  /// <see cref="IOrchestrationConversionContext"/>. TranslateTasksToSnowflakeSql dereferences that
  /// parameter (`OrchestratorTaskTranslatorRegistry.cs:104`, AdditionalProcedures), and a producer has
  /// no orchestration-conversion context to hand it — the same constraint DESIGN.md 2.6.3 records.
  /// </summary>
  internal ISqlStatement EmitUnsupportedTask(IOrchestratorTask task)
    => this.GetTranslatedUnsupportedTask(task, this.BuildContext());

  private IOrchestratorTaskTranslationContext BuildContext()
    => new SsisControlFlowTaskTranslationContext(
      fileName: "producer://" + this.orchestratorName,
      orchestratorAssessmentBuilder: this.assessmentBuilder,
      additionalProcedures: new List<ICompound>(),
      orchestratorPipeline: this.pipeline,
      orchestratorName: this.orchestratorName,
      allDefinitions: new List<EtlVariableDefinition>(),
      topLevelTaskNames: this.topLevelTaskNames,
      orchestrationContext: null!,
      isReusablePackage: false);
}
