// <copyright file="AiFirstProducerIrHydrator.cs" company="Snowflake Inc">
//        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
// </copyright>

namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Text.Json;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.Models;
using Snowflake.SnowConvert.EtlToDbt.Models.Columns;

/// <summary>
/// Deterministic JSON → engine-IR hydrator for the AI-first producer. This is the piece that makes
/// the producer DATA-driven: an agent emits the JSON, this class turns it into the exact same
/// <see cref="DagPipeline{T}"/> of <see cref="Transformation"/> objects a hand-written test body
/// would build, and the production dbt emitter renders it. No parser, no source file.
/// </summary>
/// <remarks>
/// <para>
/// The schema deliberately does NOT expose <c>ColumnExpression.IsLocal</c>, <c>IsLagged</c>,
/// <c>SetVariableKind</c> or <c>Transformation.IsReusable</c>. Those are the Informatica-specific
/// fields invariants 5 and 6 forbid a producer from setting, and the cheapest way to enforce a
/// "must not set" rule is a schema that cannot express it. <c>TableColumnReference</c> is withheld
/// for the same reason: setting it injects aliases into the <c>source_data</c> CTE.
/// </para>
/// <para>
/// Every lookup is strict. A missing required property, an unknown <c>$kind</c>, a duplicate node id
/// or an edge naming a node that is not in <c>nodes</c> all throw. A producer schema that silently
/// tolerates a typo would push the failure into the generated SQL, where it looks like a conversion
/// bug rather than a malformed input.
/// </para>
/// <para>
/// <c>"$kind": null</c> is the one thing that is NOT a typo, and it is handled separately. The
/// identification framework emits a node with an explicit null <c>$kind</c> plus
/// <c>_unsupported: "&lt;native kind&gt;"</c> for an element it identified but could not map to a
/// data-flow element — on SSIS that is the Data Flow Task CONTAINER, which in the engine becomes a
/// DIRECTORY plus a row in the orchestration SQL, never a dbt model. That is a faithful report, not a
/// malformed input, so it hydrates into <see cref="HydratedIr.UnsupportedNodes"/> instead of throwing.
/// A <c>$kind</c> that is a STRING the dispatch does not know still throws: an unrecognised name is a
/// producer mistake, whereas an explicit null is a producer statement.
/// </para>
/// <para>
/// A null <c>$kind</c> keeps the node out of the graph and therefore drops every edge touching it,
/// which on the DataStage export cost 19 of 19 edges. So a producer that identified a genuine
/// DATA-FLOW element it cannot translate must not use null — it says
/// <c>"$kind": "UnsupportedTransformation"</c> instead, keeping <c>_unsupported</c> alongside. The
/// node stays in the graph with its edges, the engine's own
/// <see cref="UnsupportedTransformation"/> translator emits a NULL-projecting placeholder with a
/// NOT-SUPPORTED EWI, and the framework's census still reports <c>NotSupported</c> because its
/// <c>element.$kind</c> obligation is still unmet. Null is now reserved for what it always meant
/// structurally: a container or an orchestration element that no data-flow class describes.
/// </para>
/// </remarks>
internal static class AiFirstProducerIrHydrator
{
  /// <summary>
  /// The hydrated graph plus the per-node dbt model names. The model name is carried per node rather
  /// than derived, because the seam supplies no platform-neutral naming policy — see
  /// <c>findings/12-dataflow-producer.md</c>.
  /// </summary>
  /// <param name="Pipeline">The data-flow graph, containing only nodes a translator handles.</param>
  /// <param name="ModelNamesByNodeId">dbt model name per data-flow node id.</param>
  /// <param name="UnsupportedNodes">
  /// Nodes the producer declared with <c>"$kind": null</c>. Surfaced rather than dropped: on SSIS this
  /// is exactly the control-flow container the ORCHESTRATION half of the producer has to emit a task
  /// for, so discarding it would throw away the one fact the other half needs.
  /// </param>
  /// <param name="EdgesDroppedForUnsupportedNodes">
  /// Edges removed because an endpoint was unsupported, as <c>"from -&gt; to"</c>. Recorded rather than
  /// skipped silently, because a lost edge changes which model a downstream <c>ref()</c> points at.
  /// </param>
  /// <param name="SourceRelationsByNodeId">
  /// The physical relation a <c>SourceQualifier</c> node reads, per node id, when the producer stated
  /// one as <c>element.TableName</c>. Carried OUT-OF-BAND rather than set on the hydrated element,
  /// because <see cref="SourceQualifier"/> has no <c>TableName</c> property: the engine takes the
  /// relation from the <see cref="Source"/> entities <c>ctx.GetIncomingEntities</c> returns, which is
  /// a CONTEXT question and is answered in
  /// <see cref="AiFirstProducerDataFlowContext.GetIncomingEntities"/>. See there for why this is not
  /// an extra graph node.
  /// </param>
  internal sealed record HydratedIr(
    DagPipeline<Transformation> Pipeline,
    IReadOnlyDictionary<string, string> ModelNamesByNodeId,
    IReadOnlyList<UnsupportedIrNode> UnsupportedNodes,
    IReadOnlyList<string> EdgesDroppedForUnsupportedNodes,
    IReadOnlyDictionary<string, string> SourceRelationsByNodeId,
    IReadOnlyDictionary<string, IReadOnlyList<ModelAuthoredFact>> ModelAuthoredByNodeId);

  /// <summary>
  /// One fact a MODEL authored rather than the document stating it — TIER 2 of the fallback ladder.
  /// </summary>
  /// <remarks>
  /// <para>
  /// WHY THIS CROSSES THE BOUNDARY AT ALL. Tier 2 is engine-rendered output built from a
  /// model-supplied payload: the producer's IR carries the payload as ordinary values, so by the time
  /// the engine's translators see them they are indistinguishable from values a rule read out of the
  /// document. MEASURED consequence on <c>poc/blind-run/runU/pentaho</c>:
  /// <c>int_derive_fullname_and_birthyear.sql</c> shipped
  /// <c>FirstName || ' ' || MiddleName || ' ' || LastName AS FullName</c> and
  /// <c>YEAR(BirthDate) AS BirthYear</c> with NO marker of any kind, while the .ktr states both as
  /// Java. Tier 3 has always been stamped <c>SSC-AI-AUTHORED</c>; tier 2 was invisible, so stage 4's
  /// MODEL-AUTHORED count read 2 on a tree where 3 of 4 models hold model-authored content.
  /// </para>
  /// <para>
  /// The producer already draws this line: <c>MODEL</c> is its own provenance class in the slot
  /// ledger, for exactly this reason. It was kept there and dropped from the artifact, which is the
  /// only thing a reviewer reads.
  /// </para>
  /// </remarks>
  /// <param name="Path">The IR field the model supplied, e.g. <c>element.OutputColumns[0]</c>.</param>
  /// <param name="Sidecar">The sidecar key it came from, e.g. <c>sidecar:OutputColumns</c>.</param>
  /// <param name="Detail">The producer's own account of what was supplied and why.</param>
  internal sealed record ModelAuthoredFact(string Path, string Sidecar, string Detail);

  /// <summary>
  /// A node the producer identified and explicitly declared unmappable to a data-flow element.
  /// </summary>
  /// <param name="Id">The node id, which on SSIS is the element's refId and therefore its FullName.</param>
  /// <param name="Name">The element's display name.</param>
  /// <param name="NativeKind">The source platform's own type name, from <c>_unsupported</c>.</param>
  /// <param name="ModelName">
  /// The sanitized identifier the producer computed for this node, when it stated one. Null when it
  /// did not. Used by the ORCHESTRATION half for the dbt project directory and the Snowflake task
  /// name — never as a model name, because this node produces no model.
  /// </param>
  internal sealed record UnsupportedIrNode(string Id, string Name, string NativeKind, string? ModelName = null);

  internal static HydratedIr Hydrate(string json, string? platformId = null)
  {
    using var document = JsonDocument.Parse(json);
    var root = document.RootElement;

    var nodes = new List<DagNode<Transformation>>();
    var nodesById = new Dictionary<string, DagNode<Transformation>>(StringComparer.Ordinal);
    var modelNames = new Dictionary<string, string>(StringComparer.Ordinal);
    var sourceRelations = new Dictionary<string, string>(StringComparer.Ordinal);
    var unsupported = new List<UnsupportedIrNode>();
    var modelAuthored =
      new Dictionary<string, IReadOnlyList<ModelAuthoredFact>>(StringComparer.Ordinal);
    var unsupportedIds = new HashSet<string>(StringComparer.Ordinal);

    foreach (var nodeJson in Required(root, "nodes").EnumerateArray())
    {
      var id = RequiredString(nodeJson, "id");
      var elementJson = Required(nodeJson, "element");

      // An explicit null $kind is the producer saying "I identified this element and it has no
      // data-flow mapping". Take it at its word: record it and keep it out of the graph, because a
      // container is not a model.
      //
      // `modelName` IS read here now, and the comment that used to say it "is meaningless for
      // something that never becomes a model" was the reason a wrong task graph shipped. The
      // container's modelName is the only sanitized, injectivity-checked identifier the producer
      // computes for it, and the ORCHESTRATION half needs exactly that: a directory name and a
      // Snowflake task name for the unit of work. It stays OPTIONAL, because a producer is not
      // obliged to name something it declared unmappable.
      if (Required(elementJson, "$kind").ValueKind == JsonValueKind.Null)
      {
        unsupported.Add(new UnsupportedIrNode(
          id,
          RequiredString(elementJson, "Name"),
          elementJson.TryGetProperty("_unsupported", out var nativeKind)
            ? nativeKind.GetString() ?? string.Empty
            : string.Empty,
          nodeJson.TryGetProperty("modelName", out var containerModelName)
            ? containerModelName.GetString()
            : null));

        if (!unsupportedIds.Add(id))
        {
          throw new InvalidOperationException($"Duplicate node id in producer IR: '{id}'.");
        }

        continue;
      }

      // "type" selects Staging vs Intermediate, i.e. whether the downstream ref() is prefixed
      // stg_raw__ or int_. Load-bearing: a wrong value still renders, still parses, and points at a
      // model that does not exist.
      var type = RequiredString(nodeJson, "type");
      var modelName = RequiredString(nodeJson, "modelName");

      var node = new DagNode<Transformation>(id, type, HydrateElement(elementJson, id, platformId));
      nodes.Add(node);
      if (!nodesById.TryAdd(id, node) || unsupportedIds.Contains(id))
      {
        throw new InvalidOperationException($"Duplicate node id in producer IR: '{id}'.");
      }

      modelNames.Add(id, modelName);

      // TIER-2 PROVENANCE, read for the node it belongs to. OPTIONAL: a document that needed no
      // sidecar has none, and that is the normal case on the two platforms the engine supports.
      if (nodeJson.TryGetProperty("modelAuthored", out var authoredJson)
        && authoredJson.ValueKind == JsonValueKind.Array)
      {
        var facts = new List<ModelAuthoredFact>();
        foreach (var factJson in authoredJson.EnumerateArray())
        {
          facts.Add(new ModelAuthoredFact(
            RequiredString(factJson, "path"),
            RequiredString(factJson, "sidecar"),
            factJson.TryGetProperty("detail", out var d) ? d.GetString() ?? string.Empty : string.Empty));
        }

        if (facts.Count > 0)
        {
          modelAuthored.Add(id, facts);
        }
      }

      // THE SOURCE RELATION, read here and applied by the context. A producer that
      // identified the table a source reads says so as `element.TableName` on a
      // SourceQualifier node. SourceQualifier has no TableName property to hydrate into,
      // and inventing one would be an engine change; the engine asks for the relation a
      // different way -- `GetIncomingEntities(sq)` returning Source entities -- so the
      // value is kept beside the graph and answered there.
      if (node.Element is SourceQualifier
        && OptionalString(elementJson, "TableName") is { Length: > 0 } relation)
      {
        sourceRelations.Add(id, relation);
      }
    }

    var edges = new List<DagEdge<Transformation>>();
    var droppedEdges = new List<string>();
    foreach (var edgeJson in Required(root, "edges").EnumerateArray())
    {
      var fromId = RequiredString(edgeJson, "from");
      var toId = RequiredString(edgeJson, "to");
      if (unsupportedIds.Contains(fromId) || unsupportedIds.Contains(toId))
      {
        droppedEdges.Add($"{fromId} -> {toId}");
        continue;
      }

      var from = ResolveNode(nodesById, fromId);
      var to = ResolveNode(nodesById, toId);
      var label = edgeJson.TryGetProperty("label", out var labelJson) ? labelJson.GetString() : null;
      edges.Add(new DagEdge<Transformation>(from, to, label));
    }

    var pipeline = new DagPipeline<Transformation> { Nodes = nodes, Edges = edges };
    return new HydratedIr(
      pipeline, modelNames, unsupported, droppedEdges, sourceRelations, modelAuthored);
  }

  private static Transformation HydrateElement(JsonElement elementJson, string nodeId, string? platformId)
  {
    // Never null here: Hydrate routes an explicit null $kind to UnsupportedNodes before this point.
    var kind = RequiredString(elementJson, "$kind");
    Transformation element = kind switch
    {
      "SourceQualifier" => new SourceQualifier(),
      "ExpressionTransformation" => new ExpressionTransformation(),

      // WIDENING (blind run follow-up). The vocabulary above was TWO element kinds, which is why
      // DataStage and Pentaho emitted zero models: every real pipeline has a target and most have a
      // filter, and neither had a door. Both classes below are platform-NEUTRAL and both already have
      // registered translators, so this is a switch arm, not new translation logic.
      //
      // PAYLOAD IS REQUIRED, NOT OPTIONAL, and that is a safety rule rather than strictness.
      // FilterTranslator's shared base falls back to `WHERE TRUE` when FilterConditions is empty and
      // records it only as a LOG WARNING. A filter that silently becomes TRUE does not fail, it
      // returns every row -- an unfiltered dataset that looks like a successful migration. That is
      // strictly worse than not representing the filter at all, because the honest alternative
      // (UnsupportedTransformation) carries a blocking EWI into the artifact where a reviewer sees it.
      //
      // So a producer that cannot extract the predicate must NOT claim FilterTransformation. Throwing
      // here would be wrong too -- it would lose the whole document over one element -- so the
      // PRODUCER decides: emit.py only assigns these kinds when the required payload resolved, and
      // otherwise falls through to degrade_to. This throw exists to catch a producer that ignores
      // that contract, which is a bug in the producer exactly as an unknown $kind string is.
      "FilterTransformation" => new FilterTransformation
      {
        FilterConditions = RequiredString(elementJson, "FilterConditions"),
      },

      // TableName is likewise required: TargetTranslator uses it to name the relation being written,
      // AND (TargetHelper.GetAliasForTargetModelName -> DbtModel.Alias) interpolates it verbatim into
      // `config(alias='...')` -- an unquoted-context string, same defect shape as the Source-side
      // UNC-path-as-identifier problem, so it gets the same sanitization here.
      // Schema and Database are genuinely optional -- plenty of source documents state neither, and
      // absent is a truthful answer for them, unlike an absent filter predicate.
      "TargetTransformation" => new TargetTransformation
      {
        TableName = AiFirstProducerDataFlowContext.SanitizeRelationIdentifier(RequiredString(elementJson, "TableName")),
        SchemaName = OptionalString(elementJson, "SchemaName"),
        Database = OptionalString(elementJson, "Database"),
      },

      // NOT WIDENED, and it is worth recording why rather than leaving it looking like an oversight.
      // RouterTransformation is `public abstract` and its only concrete subclasses are
      // SsisRouterTransformation and InfPcRouterTransformation; RouterTranslator<T> is abstract too.
      // So there is no neutral router to instantiate -- a producer would have to pick a platform's
      // subclass and thereby assert that platform. That is the same defect shape as ENG-017/ENG-018
      // (a closed vocabulary forcing a producer to name a platform it is not), one level up: not a
      // wrong issue NAME but a wrong element CLASS. Filed rather than worked around.
      //
      // Consequence, stated plainly: a multi-output router (SSIS Conditional Split with two live
      // branches, an Informatica Router) still cannot be represented. Our blind scenario uses a
      // single-branch filter, so it is reachable via FilterTransformation -- but that is a property
      // of the scenario, not a general capability.

      // The HONEST-DEGRADATION door. A producer that identified an element and has no honest
      // data-flow class for it has two ways to say so, and they are NOT the same statement:
      //
      //   "$kind": null                       -> "this is not a data-flow element at all"
      //   "$kind": "UnsupportedTransformation" -> "this IS a data-flow element and I cannot
      //                                            translate it"
      //
      // The second one has to stay IN the graph, because dropping it drops every edge touching
      // it — measured at 19 of 19 edges on the DataStage export, i.e. 43 nodes and no lineage
      // whatsoever. UnsupportedTransformation is the engine's own class for this case: its
      // translator projects `null AS <col>` per output column and attaches a NOT-SUPPORTED EWI,
      // so downstream refs still resolve and the output says plainly that it is a placeholder.
      //
      // OriginalTransformationText is filled from `_unsupported`, the producer's own name for the
      // native element type, so the emitted comment names WHAT could not be translated rather
      // than only that something could not be — plus `_unsupported_body`, the element's own
      // SOURCE FRAGMENT, when the producer supplied one. See UnsupportedSourceText.
      // IssueCodeForNotConverted defaults (per UnsupportedTransformation's own declaration) to
      // IssueName.InformaticaPcTransformationNotSupported -- SSC-EWI-INF0001, unconditionally, on
      // every platform, because the engine has exactly one native caller of this class and it is
      // Informatica. On the three platforms that reach this producer without an
      // Informatica-native document (Alteryx/Pentaho/DataStage), that Informatica-coded EWI was
      // getting written straight into the placeholder's blocking comment. Native only when the
      // document genuinely is Informatica; every other platform gets the same General-dialect
      // fallback IssueForExceptionOnPipelineElement uses (see AiFirstProducerDataFlowContext).
      "UnsupportedTransformation" => new UnsupportedTransformation
      {
        OriginalTransformationText = UnsupportedSourceText(elementJson),
        IssueCodeForNotConverted = DialectPlatform.IsInformaticaNative(platformId)
          ? IssueName.InformaticaPcTransformationNotSupported
          : IssueName.ExceptionThrownWhileConverting,
      },

      _ => throw new NotSupportedException(
        $"Producer IR node '{nodeId}' declares element $kind '{kind}', which no registered translator handles. "
        + "An unmatched type falls through TransformationUnitTranslator's dispatch and produces NOTHING."),
    };

    element.Name = RequiredString(elementJson, "Name");
    element.Id = nodeId;
    element.InputColumns = HydrateColumns(elementJson, "InputColumns");
    element.OutputColumns = HydrateColumns(elementJson, "OutputColumns");

    // INVARIANT 3 RESOLVED BY MEASUREMENT. The rule was to leave `Columns` empty "until a spike
    // proves otherwise", and leaving it empty WAS that spike. It has now produced its result, so the
    // clause is discharged rather than still open.
    //
    // What proved it: with TargetTransformation newly reachable, every mart model on all four blind
    // platforms emitted a column-less outer projection --
    //
    //     WITH source_data AS (SELECT FullName, BirthYear FROM ...)
    //     SELECT              <-- nothing here
    //     FROM source_data AS sd
    //
    // -- while the CTE above it was correct. TargetTranslatorBase iterates `target.Columns` for the
    // outer projection (not OutputColumns, which feeds the CTE), so an empty Columns yields valid-
    // looking SQL that selects nothing. Unrunnable, and NOT flagged by the artifact inspector, whose
    // column test reads between SELECT and FROM on the FIRST such pair it finds -- the CTE's.
    //
    // Populated from OutputColumns rather than InputColumns because Columns is the element's own
    // projection, which is what it emits, and for a target OutputColumns is itself derived from the
    // inbound columns by the producer. Same list, so no new claim is introduced here: this line
    // changes which engine property can SEE the columns, not what the columns are.
    element.Columns = element.OutputColumns;

    return element;
  }

  /// <summary>
  /// The text a degraded node carries into its placeholder model as line comments: the native kind
  /// name, then the element's own source fragment when the producer supplied one.
  /// </summary>
  /// <remarks>
  /// <para>
  /// WHAT CHANGED AND WHAT DELIBERATELY DID NOT. This used to be <c>_unsupported</c> alone — the
  /// native kind NAME — so every degraded element in every platform rendered as a single line,
  /// <c>--CTransformerStage</c>. That names what failed and says nothing about what was lost.
  /// Vanilla SnowConvert's own not-supported path emits the original element commented out
  /// (<c>UnsupportedTransformationConfigurator.GetCommentText</c> serialises the transformation plus
  /// its connectors), and a placeholder that quotes the source is useful to both readers of the
  /// file: a human recovering the logic by hand, and a tier-3 model asked to replace the very model
  /// it is reading.
  /// </para>
  /// <para>
  /// <c>_unsupported</c> KEEPS ITS MEANING. The kind name is emitted FIRST and unchanged, so the
  /// existing marker line is byte-identical and the <c>$kind: null</c> path — which reads the same
  /// property for <see cref="UnsupportedIrNode.NativeKind"/> — is untouched. The body is an addition
  /// beside it, never a redefinition of it: losing the kind name would break the one thing the old
  /// placeholder got right.
  /// </para>
  /// <para>
  /// NO ESCAPING HAPPENS HERE. The producer emits a body that is already safe for a SQL comment —
  /// newlines normalised (the engine's
  /// <c>UnsupportedTransformationComments.WithSourceText</c> splits on them and emits one line
  /// comment each), Jinja delimiters spaced apart because dbt renders templates before any SQL
  /// parser sees the file, and the length capped by the platform table with the cut announced
  /// inside the body. Duplicating that here would put the same policy in two places and let them
  /// disagree.
  /// </para>
  /// </remarks>
  private static string UnsupportedSourceText(JsonElement elementJson)
  {
    var kind = OptionalString(elementJson, "_unsupported") ?? string.Empty;
    var body = OptionalString(elementJson, "_unsupported_body");
    return string.IsNullOrEmpty(body) ? kind : kind + "\n" + body;
  }

  private static List<Column> HydrateColumns(JsonElement ownerJson, string propertyName)
  {
    var columns = new List<Column>();
    if (!ownerJson.TryGetProperty(propertyName, out var arrayJson))
    {
      return columns;
    }

    foreach (var columnJson in arrayJson.EnumerateArray())
    {
      var kind = columnJson.TryGetProperty("$kind", out var kindJson) ? kindJson.GetString() : null;
      Column column = kind switch
      {
        null or "Column" => new Column(),
        "ColumnExpression" => new ColumnExpression { Expression = RequiredString(columnJson, "Expression") },
        _ => throw new NotSupportedException($"Producer IR declares column $kind '{kind}', which is not supported."),
      };

      column.Name = RequiredString(columnJson, "Name");
      if (columnJson.TryGetProperty("DataType", out var dataType))
      {
        column.DataType = dataType.GetString() ?? string.Empty;
      }

      if (columnJson.TryGetProperty("Precision", out var precision))
      {
        column.Precision = precision.GetInt32();
      }

      if (columnJson.TryGetProperty("Scale", out var scale))
      {
        column.Scale = scale.GetInt32();
      }

      columns.Add(column);
    }

    return columns;
  }

  private static DagNode<Transformation> ResolveNode(
    IReadOnlyDictionary<string, DagNode<Transformation>> nodesById, string id)
    => nodesById.TryGetValue(id, out var node)
      ? node
      : throw new InvalidOperationException(
        $"Producer IR edge references node '{id}', which is not declared in 'nodes'. Invariant 4 requires "
        + "edges to reference nodes that are also in the graph.");

  private static JsonElement Required(JsonElement owner, string propertyName)
    => owner.TryGetProperty(propertyName, out var value)
      ? value
      : throw new InvalidOperationException($"Producer IR is missing required property '{propertyName}'.");

  private static string RequiredString(JsonElement owner, string propertyName)
    => Required(owner, propertyName).GetString()
      ?? throw new InvalidOperationException($"Producer IR property '{propertyName}' must be a string.");

  /// <summary>
  /// Reads an optional string property, returning <c>null</c> when it is absent OR explicitly null.
  /// </summary>
  /// <remarks>
  /// Absent and JSON-null are deliberately collapsed here, which is the opposite of the rule that
  /// governs <c>$kind</c>. For <c>$kind</c> the distinction is load-bearing — absent means "no door
  /// onto this element", explicit null means "not a data-flow element at all" — so collapsing them
  /// there would erase a real statement. For a target's schema or database it is not: both spellings
  /// mean the source document does not say, and inventing a difference between them would invent a
  /// distinction the producer never drew.
  /// </remarks>
  private static string? OptionalString(JsonElement owner, string propertyName)
    => owner.TryGetProperty(propertyName, out var value) && value.ValueKind != JsonValueKind.Null
      ? value.GetString()
      : null;
}
