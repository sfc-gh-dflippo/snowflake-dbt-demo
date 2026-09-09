// <copyright file="AiFirstProducerDataFlowContext.cs" company="Snowflake Inc">
//        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
// </copyright>

namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Linq;
using Artinsoft.Common.AST;
using Microsoft.Extensions.Logging;
using Mobilize.AnsiSql.AST;
using Mobilize.AnsiSql.Parser;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.DbtGeneration;
using Snowflake.SnowConvert.EtlToDbt.DbtGeneration.Translations;
using Snowflake.SnowConvert.EtlToDbt.Models;
using Snowflake.SnowConvert.EtlToDbt.Models.Columns;
using Snowflake.SnowConvert.EtlToDbt.Services.Interfaces;
using Snowflake.SnowConvert.EtlToDbt.Variables;

/// <summary>
/// The AI-first producer's own <see cref="IEtlIrToDbtContext"/>. Implements the interface directly
/// rather than reusing <c>InformaticaSpecificDbtGenerationContext</c> or
/// <c>SsisSpecificDbtGenerationContext</c>: both of those route
/// <see cref="IEtlIrToDbtContext.TranslateExpression"/> into a platform-specific expression parser,
/// which would silently reinterpret the producer's Snowflake SQL text (invariant 7).
///
/// <para>
/// Every member the producer believes is unnecessary throws <see cref="NotSupportedException"/>, so
/// a hidden dependency on parsed-source state surfaces as a loud failure instead of a benign default
/// that lets a test pass while generating garbage. The counters
/// (<see cref="TranslateExpressionCalls"/>, <see cref="NonConvertedExpressions"/>) exist for the
/// anti-vacuous-pass assertions: the emission path swallows expression-translation exceptions and
/// substitutes an EWI placeholder, so a test must prove that did not happen.
/// </para>
/// </summary>
internal sealed class AiFirstProducerDataFlowContext : IEtlIrToDbtContext
{
  /// <summary>Node <c>Type</c> value the producer uses to mark a staging source.</summary>
  internal const string SourceNodeType = "source";

  private readonly Dictionary<string, string> modelNamesByNodeId;
  private readonly Dictionary<string, string> sourceRelationsByNodeId;
  private readonly string? platformId;

  /// <summary>
  /// One synthesized <see cref="Source"/> per SourceQualifier that declared a relation. Cached, and
  /// the caching is load-bearing rather than an optimisation: <c>HasConnectionCollision</c> and
  /// <c>ResolveDbtSourceGroup</c> compare entities by <c>ReferenceEquals</c>, and the translator calls
  /// <c>GetIncomingEntities</c> more than once per model, so handing out a fresh instance each time
  /// would make a source collide with itself.
  /// </summary>
  private readonly Dictionary<string, Source> synthesizedSources = new(StringComparer.Ordinal);

  internal AiFirstProducerDataFlowContext(
    DagPipeline<Transformation> pipeline,
    IReadOnlyDictionary<string, string> modelNamesByNodeId,
    DbtProjectGenerationContext projectGenerationContext,
    IEtlAssessmentBuilderForPipelineContainer assessmentBuilder,
    ILogger logger,
    string currentItemName,
    string currentFileName,
    IReadOnlyDictionary<string, string>? sourceRelationsByNodeId = null,
    string? platformId = null)
  {
    this.DagPipeline = pipeline;
    this.modelNamesByNodeId = new Dictionary<string, string>(modelNamesByNodeId, StringComparer.Ordinal);
    this.sourceRelationsByNodeId = sourceRelationsByNodeId is null
      ? new Dictionary<string, string>(StringComparer.Ordinal)
      : new Dictionary<string, string>(sourceRelationsByNodeId, StringComparer.Ordinal);
    this.ProjectGenerationContext = projectGenerationContext;
    this.AssessmentReportsServiceForContainer = assessmentBuilder;
    this.Logger = logger;
    this.CurrentContextName = currentItemName;
    this.CurrentFileName = currentFileName;
    this.platformId = platformId;
  }

  /// <summary>
  /// Relations answered from the producer's <c>element.TableName</c> rather than from the graph, as
  /// "nodeId => relation", in first-ask order. Exists so the driver can PRINT what it supplied: a
  /// silently-empty list is exactly how the dangling FROM survived four blind runs.
  /// </summary>
  internal List<string> SuppliedSourceRelations { get; } = [];

  /// <summary>Expression strings the producer's Snowflake parser accepted, in call order.</summary>
  internal List<string> TranslateExpressionCalls { get; } = [];

  /// <summary>
  /// Expressions that fell through to the non-converted placeholder. MUST stay empty: a non-empty
  /// list means the generated SQL contains an EWI placeholder instead of real translated SQL.
  /// </summary>
  internal List<string> NonConvertedExpressions { get; } = [];

  /// <summary>Issues attached to emitted AST nodes, in attach order.</summary>
  internal List<IssueName> AttachedIssues { get; } = [];

  /// <summary>
  /// The node id of the element the per-element translation loop is currently translating, or
  /// <c>null</c> when no element is in scope. Set by <see cref="SetCurrentElement"/> around each
  /// <c>TransformationUnitTranslator.Translate</c> call.
  /// </summary>
  /// <remarks>
  /// THE BUG THIS CLOSES. <see cref="AddIssueToElement{T}"/> used to key every registration on
  /// <see cref="CurrentContextName"/> unconditionally -- the CONTAINER (dbt project name), never the
  /// element -- because that was the only identity the context had. <c>ProducerReports.CodesFor</c>
  /// looks issues up by node id, so a container-keyed registration never becomes a component row: it
  /// is silently counted as "keyed by the CONTAINER context" and dropped from <c>ETL.Elements</c>.
  /// This measurably happened on TWO independent paths that share nothing but the call:
  /// <c>UnsupportedTransformationTranslator</c> (fixed narrowly for its own placeholder in
  /// SNOW-3979042/bfbdabadfa, by re-registering after the fact) and the engine's own
  /// <c>TargetTranslator</c> raising <c>InformaticaPcTargetFieldsMissing</c> (SSC-EWI-INF0087) on a
  /// mart's target element -- measured on the 2026-08-27 Alteryx run, where three
  /// <c>TargetTransformation</c> nodes carried a live <c>!!!RESOLVE EWI!!!</c> in their SQL and
  /// <c>EWI Count 0</c> in the report. Rather than special-case a third translator, this closes the
  /// class at the one place every <c>ctx.AddIssueToElement</c> call funnels through: the element the
  /// per-node loop is currently translating IS the right key, unconditionally, for every translator
  /// that calls it from inside that loop.
  /// </remarks>
  internal string? CurrentElementId { get; private set; }

  /// <summary>
  /// Sets or clears the element currently in scope. The per-element translation loop in
  /// <c>Program.cs</c> calls this with the node id immediately before
  /// <c>TransformationUnitTranslator.Translate(node.Element, ctx)</c> and clears it (passing
  /// <c>null</c>) in a <c>finally</c>, so an issue raised by a translator running OUTSIDE that loop
  /// (a spike, or a future caller with no element in scope) falls back to the container -- the
  /// pre-existing, still-correct behaviour for a genuinely container-level registration -- instead of
  /// silently inheriting whichever node happened to translate last.
  /// </summary>
  internal void SetCurrentElement(string? nodeId) => this.CurrentElementId = nodeId;

  // ---- IEtlIrContext ------------------------------------------------------------------------

  public DagPipeline<Transformation> DagPipeline { get; }

  public ILogger Logger { get; }

  public DagNode<Transformation>? GetIncomingEntity(Transformation transformation)
    => this.DagPipeline.Edges.FirstOrDefault(e => ReferenceEquals(e.To.Element, transformation))?.From;

  // The producer states connectivity explicitly through the column lists it emits: every declared
  // input port is wired. An IR that needs unconnected ports would carry a per-port flag.
  public bool IsInputColumnConnected(Transformation transformation, Column inputColumn) => true;

  public bool IsOutputColumnConnected(Transformation transformation, Column outputColumn) => true;

  /// <summary>
  /// Name-based port matching: an output/input port is fed by the upstream port of the same name.
  /// Returning null for a name the upstream does not project is load-bearing — it is what makes the
  /// two computed columns classify as Expression rather than passthrough.
  /// </summary>
  public string? GetOriginColumnName(Transformation fromEntity, Transformation toEntity, string toColumnName)
    => fromEntity.OutputColumns.Any(c => string.Equals(c.Name, toColumnName, StringComparison.OrdinalIgnoreCase))
      ? toColumnName
      : null;

  // ---- IEtlIrToDbtContext: project/file metadata --------------------------------------------

  public string CurrentContextName { get; }

  public IEtlAssessmentBuilderForPipelineContainer AssessmentReportsServiceForContainer { get; }

  public string CurrentFileName { get; }

  /// <summary>
  /// SQL-artifact dialect bleed: <c>TransformationUnitTranslator.GenerateUnsupportedElementConversion</c>
  /// uses this value UNCONDITIONALLY, on whatever node threw, on whatever platform this context is
  /// processing -- it is not an SSIS-only path. Hardcoding <c>SSISExceptionConvertingComponent</c> put
  /// <c>SSC-EWI-SSIS0009</c> inline in every non-SSIS platform's .sql (measured on the Pentaho blind
  /// run's <c>Filter BirthYear</c>, see NOTES-assessment.md). Native only when the document genuinely
  /// is SSIS; every other platform gets the General-dialect <c>ExceptionThrownWhileConverting</c>
  /// (SSC-EWI-0013), which is <see cref="IsForeignDialectBleed"/>'s own definition of "not foreign" for
  /// EVERY platform, applied here instead of only at the CSV sink.
  /// </summary>
  public IssueName IssueForExceptionOnPipelineElement => DialectPlatform.IsSsisNative(this.platformId)
    ? IssueName.SSISExceptionConvertingComponent
    : IssueName.ExceptionThrownWhileConverting;

  /// <summary>
  /// The shared target translator combines repeated writers with UNION ALL. Informatica retains
  /// its native diagnostic; every other producer platform uses the engine's General-dialect FDM.
  /// </summary>
  public IssueName IssueNameForDuplicateTargetsUnionAll =>
    DialectPlatform.IsInformaticaNative(this.platformId)
      ? IssueName.InformaticaPcDuplicateTargetsUnionAll
      : IssueName.MultipleTargetWritersCombinedWithUnionAll;

  // EXPLICIT RESIDUAL: the shared translator's deferred duplicate-target branch asks the context for
  // this value. The engine registry has SSIS- and DataStage-specific entries but no semantically honest
  // General entry; mapping it to "exception thrown" would misdescribe a model-collision decision. This
  // producer cannot currently reach that deferred branch: it hydrates no UpdateStrategyTransformation,
  // while two ordinary TargetTransformation nodes take the separate UNION ALL branch. Keep the exact
  // engine contract here. If future IR widening makes it reachable on a foreign platform, reconciliation
  // now scans every SSC-EWI/FDM/PRF marker and fails loudly instead of filtering or hiding the code.
  public IssueName IssueNameForMultipleTargetForModel => IssueName.SSISTableModelAlreadyDefined;

  public DbtProjectGenerationContext ProjectGenerationContext { get; }

  public bool IsGeneratingMacro => false;

  public string RelativeOutputPathForDbtProject => this.CurrentContextName;

  // ---- IEtlIrToDbtContext: graph/model-name resolution --------------------------------------

  public string? GetIncomingDbtModelName(Transformation transformation)
  {
    var from = this.GetIncomingEntity(transformation);
    return from is null ? null : this.ModelNameForNode(from);
  }

  /// <summary>
  /// The entities feeding a transformation. For everything except a SourceQualifier that is exactly
  /// the graph's predecessors.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE DANGLING <c>FROM</c>, AND WHY IT IS ANSWERED HERE. Every staging model on all four blind
  /// platforms ended on a bare <c>FROM</c> with no relation — the sole <c>dbt0101</c> on SSIS and
  /// Informatica. The cause is NOT the stubbed <see cref="NoOpMultiDialectEtlSqlProcessor"/>, which was
  /// the standing hypothesis: <c>SourceQualifierTranslator.BuildStandardSelectQuery</c> builds its FROM
  /// from <c>ctx.GetIncomingEntities(sourceQualifier)</c>, takes
  /// <c>source.TableName ?? source.Name</c> off each incoming <see cref="Source"/>, and hands the list
  /// to <c>CreateFromClause</c> — no SQL processor is on that path at all. A SourceQualifier has no
  /// predecessor in our graph, so the list was EMPTY and <c>CreateFromClause</c> built a FROM with zero
  /// table factors, which prints as <c>FROM</c> and stops. Wiring the real processor would not have
  /// touched it.
  /// </para>
  /// <para>
  /// AND WHY NOT AN EXTRA GRAPH NODE. Adding a <c>Source</c> node upstream of each SourceQualifier
  /// would answer the same question, and it would change the IR's node count on every platform — which
  /// four committed <c>AiFirstProducerIrSchemaConvergenceTests</c> DataRows assert by exact number, and
  /// which the spike's own regression control forbids. The relation is not a node in the producer's
  /// graph; it is a PROPERTY of the read. So it travels as one (<c>element.TableName</c>) and is
  /// materialised into the shape the engine asks for at the moment it asks.
  /// </para>
  /// <para>
  /// The synthesized entity is deliberately minimal: <c>Name</c> and <c>TableName</c> only.
  /// <c>Database</c> and <c>Schema</c> stay null, so <c>ResolveSourceGroupOrigin</c> keeps the default
  /// <c>raw</c> group and the model emits <c>{{ source('raw', '&lt;table&gt;') }}</c> — the same shape
  /// real SnowConvert emits. Asserting a database or schema would state a destination the producer's
  /// table deliberately does not (see the SSIS destination's note on dropping <c>dbo</c>).
  /// </para>
  /// </remarks>
  /// <param name="transformation">The element whose feeding entities are wanted.</param>
  /// <returns>The graph predecessors, or the synthesized source relation for a SourceQualifier.</returns>
  public Transformation[] GetIncomingEntities(Transformation transformation)
  {
    var fromGraph = this.DagPipeline.Edges
      .Where(e => ReferenceEquals(e.To.Element, transformation))
      .Select(e => e.From.Element)
      .ToArray();

    // Graph predecessors win. A SourceQualifier with a real upstream node is reading a model, not a
    // relation, and overriding that with a source() call would silently reroute the read.
    if (fromGraph.Length > 0 || transformation is not SourceQualifier)
    {
      return fromGraph;
    }

    var id = transformation.Id;
    if (id is null || !this.sourceRelationsByNodeId.TryGetValue(id, out var relation))
    {
      return fromGraph;
    }

    if (!this.synthesizedSources.TryGetValue(id, out var source))
    {
      // `relation` is whatever the source platform's own file-path
      // syntax states (a Windows UNC share, on Alteryx's DbFileInput) — not a SQL
      // identifier. SourceQualifierTranslator.BuildStandardSelectQuery (engine, not ours)
      // takes `source.TableName ?? source.Name` and uses that ONE string as BOTH the
      // dbt source() literal AND the unquoted correlation alias, so whatever we hand it
      // here must already be a legal bare identifier — sanitizing only one of the two
      // properties would not help, since the engine never looks at the other. Sanitizing
      // here rather than at emission keeps every downstream consumer of this Source (the
      // SQL, and any sources.yml the engine writes from the same object) in agreement.
      var sanitizedRelation = SanitizeRelationIdentifier(relation);
      source = new Source { Name = sanitizedRelation, TableName = sanitizedRelation };
      this.synthesizedSources.Add(id, source);
      this.SuppliedSourceRelations.Add($"{id} => {relation}");
    }

    return [source];
  }

  public string? GetSourceModelName(Transformation transformation, string? columnName)
  {
    var from = this.GetIncomingEntity(transformation);
    return from is null ? null : this.ModelNameForNode(from);
  }

  public string GetSourceModelNameForRelation(Transformation from, Transformation to, Column? targetColumn = null)
    => this.ModelNameForElement(from);

  public ReferencedModelKind GetIncomingModelKind(Transformation toTransformation)
  {
    var from = this.GetIncomingEntity(toTransformation);
    return from is null ? ReferencedModelKind.Unknown : KindForNode(from);
  }

  public ReferencedModelKind GetReferencedModelKind(Transformation? incoming)
  {
    if (incoming is null)
    {
      return ReferencedModelKind.Unknown;
    }

    var node = this.NodeForElement(incoming);
    return node is null ? ReferencedModelKind.Unknown : KindForNode(node);
  }

  public string GetModelName(Transformation transformation) => this.ModelNameForElement(transformation);

  public DagNode<Transformation>? GetNodeByName(string nodeName)
    => this.DagPipeline.Nodes.FirstOrDefault(n => n.Id == nodeName);

  public string GetMaterialization(Transformation transformation) => "view";

  public string GetLineageIdForTransformation(Transformation transformation)
    => $"{this.CurrentFileName}.{transformation.Id}";

  // ---- IEtlIrToDbtContext: expression translation (invariant 7) -----------------------------

  /// <summary>
  /// Parses the producer-supplied expression text with the SNOWFLAKE/ANSI grammar
  /// (<see cref="SqlParser.ParseExpr"/>), the same way
  /// <c>Assemblies/EtlToDbt/InfPowerCenter/Translations/InfPcSourceQualifierTranslatorBase.cs</c>
  /// parses a SQL override. No Informatica or SSIS expression parser is involved. A parse failure
  /// throws rather than falling back to a raw-text literal, so a malformed expression cannot reach
  /// the output disguised as SQL.
  /// </summary>
  public SqlExpr TranslateExpression(
    string expression,
    IEnumerable<Column>? currentColumns = null,
    Dictionary<string, string>? idsToQualify = null,
    IEnumerable<EtlVariableReference>? variableReferences = null,
    Dictionary<string, string>? idResolutions = null)
  {
    this.TranslateExpressionCalls.Add(expression);
    var parsed = new SqlParser().ParseExpr(expression, default)
      ?? throw new InvalidOperationException(
        $"The Snowflake expression parser returned null for producer expression: {expression}");
    return parsed;
  }

  public SqlExpr GetDefaultExpressionForNonConvertedExpression(string expression, SqlExpr? defaultExpr = null)
  {
    this.NonConvertedExpressions.Add(expression);
    return defaultExpr ?? SqlEmit.Instance.SingleNameExpr("__PRODUCER_EXPRESSION_NOT_CONVERTED__");
  }

  // ---- IEtlIrToDbtContext: issue reporting -------------------------------------------------

  public string CreateEwiCommentString(IssueName issueName, bool breaking = false, object[] args = null!)
    => this.ProjectGenerationContext.EwiService.EwiFormatter.CreateEwiComment(issueName, args ?? []);

  public T AddIssueToElement<T>(T compound, IssueName issueName, params object[] args)
    where T : class, ICompound
  {
    // TargetTranslator is shared, but its missing-projection diagnostic describes an Informatica
    // TARGETFIELD export. A foreign producer can hit the same fallback (SELECT *) without being an
    // Informatica document. Normalize at this single emission seam so the attached SQL marker and
    // the assessment registration cannot disagree. Informatica keeps its precise native issue;
    // other platforms use the registry's established General-dialect conversion-failure fallback.
    //
    // The other hardcoded TargetTranslator diagnostics are deliberately not rewritten here. This
    // producer does not hydrate IsSelfReferencingTarget, UnconnectedColumns, or TableNamePrefix, so
    // those branches are unreachable. Duplicate-target issue selection now belongs to the engine's
    // IssueNameForDuplicateTargetsUnionAll context seam; this method only preserves the separate
    // element-identity requirement for the already-rendered model.
    if (issueName == IssueName.InformaticaPcTargetFieldsMissing
      && !DialectPlatform.IsInformaticaNative(this.platformId))
    {
      var targetName = args.Length > 0 ? args[0] : this.CurrentElementId ?? this.CurrentContextName;
      issueName = IssueName.ExceptionThrownWhileConverting;
      args = [$"Target projection for '{targetName}'", 0, this.CurrentFileName];
    }

    var issueElementId = this.CurrentElementId ?? this.CurrentContextName;
    if (issueName == this.IssueNameForDuplicateTargetsUnionAll)
    {
      issueElementId = this.GetExistingDuplicateTargetId() ?? issueElementId;
    }

    this.AttachedIssues.Add(issueName);
    return SqlUtils.AddIssueToElement(
      compound,
      issueName,
      this.ProjectGenerationContext.EwiService,
      this.AssessmentReportsServiceForContainer,
      issueElementId,
      args);
  }

  public void RegisterConversionLevelIssue(IssueName issueName, string componentFullName, params object[] args)
    => this.AttachedIssues.Add(issueName);

  // ---- IEtlIrToDbtContext: column projection ------------------------------------------------

  /// <summary>
  /// Projects the producer's columns as SELECT-list expressions. Implemented because the DataStage
  /// slice measured that it HAS to be: <c>SourceQualifierTranslator</c> calls it for every source
  /// stage, and with this member throwing, all 11 DataStage source stages went through the engine's
  /// swallow-and-substitute path and came out as NOT-SUPPORTED placeholders.
  /// </summary>
  /// <remarks>
  /// <para>
  /// Worth recording that the SHIPPED SSIS context does not implement this either —
  /// <c>Assemblies/EtlToDbt/DtsxSsis/SsisSpecificDbtGenerationContext.cs</c> throws
  /// <c>NotImplementedException</c> — so <c>SourceQualifier</c> is in practice an Informatica-only
  /// element. Any producer that maps a source to <c>SourceQualifier</c> because it is "the IR's only
  /// source-shaped door" inherits that.
  /// </para>
  /// <para>
  /// Deliberately NOT reusing <c>InformaticaPowerCenterTranslatorHelper.TranslateColumns</c>: with a
  /// null <c>sourceEntity</c> — which is the producer's case, since the IR has no separate
  /// <c>Source</c> node — it routes to the batch path and calls
  /// <c>GetColumnNameMappingsForTransformation</c>, which is Informatica port-mapping state a producer
  /// does not have. So this emits UNQUALIFIED names, which is correct for a staging model selecting
  /// from a single <c>source()</c> or <c>ref()</c>, and nothing else is invented: a plain column
  /// contributes its own name, and a <see cref="ColumnExpression"/> contributes its expression parsed
  /// by the same Snowflake grammar <see cref="TranslateExpression"/> uses, aliased to the column name.
  /// </para>
  /// </remarks>
  public IEnumerable<SqlExpr> TranslateColumns(
    IEnumerable<Column> columns, Transformation transformation, Transformation? sourceEntity = null)
  {
    foreach (var column in columns)
    {
      var name = SqlEmit.Instance.SingleNameExpr(column.Name);
      yield return column is ColumnExpression { Expression.Length: > 0 } computed
        ? SqlEmit.Instance.ExprAlias(
            this.TranslateExpression(computed.Expression),
            SqlEmit.Instance.AsClause(SqlEmit.Instance.SimpleName(column.Name), aas: true))
        : name;
    }
  }

  // ---- Deliberately unimplemented: proves the per-translator surface is small ---------------

  public Dictionary<string, (string SourceFieldKey, string TableName)> GetColumnNameMappingsForTransformation(
    Transformation transformation)
    => throw new NotSupportedException(nameof(this.GetColumnNameMappingsForTransformation));

  // ---- helpers ------------------------------------------------------------------------------

  /// <summary>
  /// The duplicate-target UNION ALL marker is attached to the already-written model, not the target
  /// currently being translated. Attribute its report row to that earlier model's node so SQL and
  /// reports retain the same element identity.
  /// </summary>
  private string? GetExistingDuplicateTargetId()
  {
    if (this.CurrentElementId is null)
    {
      return null;
    }

    var currentIndex = this.DagPipeline.Nodes.FindIndex(n => n.Id == this.CurrentElementId);
    if (currentIndex < 0 || this.DagPipeline.Nodes[currentIndex].Element is not TargetTransformation current)
    {
      return null;
    }

    return this.DagPipeline.Nodes
      .Take(currentIndex)
      .LastOrDefault(n => n.Element is TargetTransformation prior
        && string.Equals(prior.TableName, current.TableName, StringComparison.OrdinalIgnoreCase))
      ?.Id;
  }

  private static ReferencedModelKind KindForNode(DagNode<Transformation> node)
    => node.Type == SourceNodeType ? ReferencedModelKind.Staging : ReferencedModelKind.Intermediate;

  /// <summary>
  /// Resolves the DAG node for an element, by reference first and then by <see cref="Transformation.Id"/>.
  /// </summary>
  /// <remarks>
  /// The Id fallback is required, not a convenience. When a per-element translator throws,
  /// <c>TransformationUnitTranslator</c> swallows it and substitutes a BRAND NEW
  /// <see cref="UnsupportedTransformation"/> carrying the same Name and Id
  /// (<c>Assemblies/EtlToDbt/DbtGeneration/TransformationUnitTranslator.cs</c>,
  /// <c>GenerateUnsupportedElementConversion</c>). Reference-only lookup then rejects that substitute
  /// and throws a SECOND exception out of the context — which masks the first one entirely. That is
  /// exactly what happened on the DataStage slice: 11 nodes reported
  /// "Element 'Input' is not a node in the producer DAG" when the real failure was upstream in the
  /// element translator. Id is the right key anyway: the producer IR keys model names by node id and
  /// the hydrator sets <c>element.Id = nodeId</c>.
  /// </remarks>
  private DagNode<Transformation>? NodeForElement(Transformation element)
    => this.DagPipeline.Nodes.FirstOrDefault(n => ReferenceEquals(n.Element, element))
      ?? this.DagPipeline.Nodes.FirstOrDefault(n => string.Equals(n.Id, element.Id, StringComparison.Ordinal));

  private string ModelNameForNode(DagNode<Transformation> node)
    => this.modelNamesByNodeId.TryGetValue(node.Id, out var name)
      ? name
      : throw new NotSupportedException(
        $"The producer IR did not declare a dbt model name for node '{node.Id}'.");

  private string ModelNameForElement(Transformation element)
  {
    var node = this.NodeForElement(element)
      ?? throw new NotSupportedException($"Element '{element.Name}' is not a node in the producer DAG.");
    return this.ModelNameForNode(node);
  }

  /// <summary>
  /// One replacement character per illegal character, never a collapsed run — the same injective
  /// rule <c>Program.SanitizeIdentifier</c> uses for orchestration directory names, kept as a
  /// separate copy here because this type has no reference back to <c>Program</c>. Internal (not
  /// private) so <c>AiFirstProducerIrHydrator</c> can apply the same rule to
  /// <c>TargetTransformation.TableName</c> -- both are the SAME "raw platform path used as a bare SQL
  /// identifier" defect, just on the Source side vs. the Target/mart side.
  /// </summary>
  internal static string SanitizeRelationIdentifier(string relation)
  {
    var chars = relation.Select(c => char.IsLetterOrDigit(c) ? char.ToLowerInvariant(c) : '_').ToArray();
    var result = new string(chars).Trim('_');
    return result.Length == 0 || char.IsDigit(result[0]) ? "u_" + result : result;
  }
}
