// <copyright file="AiFirstSsisSemanticsShim.cs" company="Snowflake Inc">
//        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
// </copyright>

namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;

/// <summary>
/// The SSIS semantics the Python identification framework does not model, applied to producer IR
/// before it reaches <see cref="AiFirstProducerIrHydrator"/>.
/// </summary>
/// <remarks>
/// <para>
/// <b>This was called <c>AiFirstProducerIrAdapter</c> and it was named wrong.</b> The vertical slice
/// needed three transforms to get the framework's IR into the hydrator and described all three as
/// schema adaptation. Only ONE of them was: the framework emitted the Data Flow Task container as a
/// node with <c>"$kind": null</c> and the hydrator threw on it. That was a genuine schema
/// disagreement and it has been <b>converged</b> — the hydrator now accepts such a node and reports it
/// on <c>HydratedIr.UnsupportedNodes</c>, so no transform is required and the container is available
/// to the orchestration half instead of being discarded.
/// </para>
/// <para>
/// <b><c>SynthesizePassThrough</c> IS GONE, AND IT WAS A NEUTRALITY DEFECT, NOT A CLEANUP.</b> The step
/// materialised SSIS implicit pass-through: for every element, it copied each <c>InputColumns</c> entry
/// that was not already in <c>OutputColumns</c> into <c>OutputColumns</c>. That is a per-component SSIS
/// buffer rule, and it was applied to <b>every platform</b>, because this shim never sees which platform
/// produced the IR.
/// </para>
/// <para>
/// The producer now models buffer semantics per platform — <c>column_propagation.mode</c> in each
/// <c>platform_*.json</c> — which superseded the step where it was right and left it firing only where
/// it was wrong. MEASURED, per platform, immediately before deletion:
/// </para>
/// <list type="bullet">
/// <item><description>SSIS <c>DerivedColumn.dtsx</c>: 0 firings. <c>CustomerSummary_DerivedColumn_ConditionalSplit.dtsx</c>: 0 firings. Correctly superseded by <c>mode=ACCUMULATE</c>.</description></item>
/// <item><description>DataStage, Pentaho, ADF: 0 firings.</description></item>
/// <item><description>Informatica <c>m_CUSTOMER_SUMMARY_fullname_birthyear.xml</c>: <b>4 firings</b> — FirstName, MiddleName, LastName, BirthDate onto <c>EXP_DERIVE_CUSTOMER</c>.</description></item>
/// </list>
/// <para>
/// Those four are FABRICATED COLUMNS and the document says so outright. The Expression transformation
/// declares those ports <c>PORTTYPE="INPUT"</c> (xml:35-38) — input-only — and <c>FullName</c> /
/// <c>BirthYear</c> as <c>PORTTYPE="OUTPUT"</c> (xml:39-40); the only CONNECTORs leaving the instance
/// carry FullName and BirthYear (xml:64-65). Informatica's table states the same rule in the other
/// direction: <c>column_propagation.mode=FILL_WHEN_UNDECLARED</c>, because a PowerCenter
/// transformation declares EVERY port it has and an absent port is genuinely absent. So the step
/// contradicted that table's own declaration, and its ONLY remaining effect anywhere was to put four
/// columns into a model that the source explicitly does not emit.
/// </para>
/// <para>
/// MEASURED EFFECT ON THE ARTIFACT — <c>models/intermediate/int_exp_derive_customer.sql</c>:
/// </para>
/// <code>
/// before                                        after
/// ------                                        -----
/// SELECT                                        SELECT
///    FirstName || ' ' || ... AS FullName,          FirstName || ' ' || ... AS FullName,
///    GET_DATE_PART(BirthDate,'YYYY') AS BirthYear, GET_DATE_PART(BirthDate,'YYYY') AS BirthYear
///    FirstName  AS FirstName,                   FROM
///    MiddleName AS MiddleName,                     source_data
///    LastName   AS LastName,
///    BirthDate  AS BirthDate
/// FROM
///    source_data
/// </code>
/// <para>
/// Nothing downstream loses anything: <c>int_fil_birthyear_1990</c> and the mart select FullName and
/// BirthYear only.
/// </para>
/// <para>
/// What is left is not schema adaptation either, and it is not incidental.
/// <see cref="ShimSteps.TranslateExpressions"/> — the framework reports expression text in the SOURCE
/// dialect because that is what the document states. Translating SSIS to Snowflake needs an expression
/// translator, which exists nowhere in the chain. This is a MISSING COMPONENT, not a mismatched field:
/// the two sides agree the field is a string and disagree about the language it is written in, and no
/// schema can settle that.
/// </para>
/// <para>
/// RESIDUAL NEUTRALITY RISK — NOW CLOSED, AND THE FIX WAS AN IR-SCHEMA CHANGE.
/// <c>TranslateExpressions</c> was an SSIS-specific semantic applied to every platform, unguarded for
/// one structural reason: this component was never told which platform produced the IR. It was
/// harmless only because its three textual rules key off constructs the other four platforms'
/// FIXTURES do not use — MEASURED <c>rewrittenExpressions=0</c> on Informatica, DataStage, Pentaho and
/// ADF, and 2 and 1 on the two SSIS fixtures. That is a property of those fixtures, not a guarantee:
/// an Informatica expression containing a double-quoted literal (legal, and meaning a STRING in
/// PowerCenter's expression language) would be rewritten by a rule written for another language.
/// </para>
/// <para>
/// A previous pass declined to fix it because "gating it needs the platform identity to cross the
/// process boundary, which is an IR-schema change and is reported as its own item rather than smuggled
/// in here". We own the IR schema. <c>emit.py</c> now emits a root <c>platform</c> key copied verbatim
/// from the platform table's own <c>platform</c> declaration, and <see cref="Apply"/> gates the step on
/// it. NEGATIVE-TESTED rather than assumed: with a double-quoted literal planted into the Informatica
/// IR's <c>Expression</c>, the gate reports <c>0 rewritten</c> of <c>1 inspected</c>; with the SAME IR's
/// <c>platform</c> value changed to <c>SqlServerIntegrationServices</c> and nothing else touched, the
/// same run rewrites it. So the gate is load-bearing and not a no-op that reads like one.
/// </para>
/// <para>
/// AN IR THAT STATES NO PLATFORM GETS NO PLATFORM-SPECIFIC SEMANTICS, and that direction is deliberate.
/// The two hand-authored spike fixtures predate this key; defaulting an absent platform to SSIS would
/// have preserved their behaviour and reinstated the defect for every future producer that forgets the
/// field. Neither fixture needs the step — both carry already-translated Snowflake, as their own doc
/// comments say — so failing neutral costs nothing here and cannot fabricate anything later. The
/// absence is REPORTED, not silently equated with "not SSIS".
/// </para>
/// <para>
/// WHY GATED RATHER THAN DELETED, argued from the measurement. <c>SynthesizePassThrough</c> was deleted
/// because the producer had SUPERSEDED it: <c>column_propagation.mode</c> in each platform table states
/// the same rule per platform, so the step's only remaining effect anywhere was wrong. Nothing
/// supersedes this one. It is still the ONLY thing in the chain that turns SSIS
/// <c>[YEAR](x)</c>, <c>"lit"</c> and <c>+</c> into Snowflake, and with it off the two SSIS fixtures
/// emit expression text that <c>SqlParser.ParseExpr</c> rejects — a real, currently-load-bearing 2 and
/// 1 rewrites. Deleting a step that is right where it fires and gating it where it does not are
/// different actions, and only the second is available here.
/// </para>
/// <para>
/// Nothing here is production quality; <see cref="RewriteExpression"/> in particular is a stub standing
/// in for a real SSIS expression translator. It reports every rewrite it performs so a test can assert
/// on the list instead of trusting it.
/// </para>
/// </remarks>
internal static class AiFirstSsisSemanticsShim
{
  /// <summary>
  /// The <c>platform</c> value <c>platform_ssis.json</c> declares. The ONLY platform whose expression
  /// dialect <see cref="RewriteExpression"/> implements rules for.
  /// </summary>
  internal const string SsisPlatform = "SqlServerIntegrationServices";

  /// <summary>
  /// What the shim had to supply. Each list is evidence for one missing component.
  /// </summary>
  internal sealed record ShimReport
  {
    /// <summary>Gets expressions rewritten from SSIS dialect to Snowflake dialect, as "before => after".</summary>
    internal List<string> RewrittenExpressions { get; } = [];

    /// <summary>Gets the platform the IR declared, or null when it declared none.</summary>
    internal string? Platform { get; init; }

    /// <summary>
    /// Gets or sets how many <c>Expression</c> values the IR carries.
    /// </summary>
    /// <remarks>
    /// COUNTED WHETHER OR NOT THE STEP RAN, and that is the point. "0 rewritten" over 0 expressions
    /// and "0 rewritten" over 12 are opposite facts, and before the platform gate existed the single
    /// number could not distinguish "this platform needs no rewriting" from "nothing was inspected".
    /// The same reason stage 4 of the driver prints <c>models the SQL gate read</c> beside its verdict.
    /// </remarks>
    internal int ExpressionsInspected { get; set; }

    /// <summary>Gets or sets a value indicating whether the SSIS expression step was applied.</summary>
    internal bool TranslateExpressionsApplied { get; set; }

    /// <summary>Gets or sets a value indicating whether the caller selected the step at all.</summary>
    internal bool TranslateExpressionsSelected { get; set; }

    /// <summary>Gets a flat summary for test output.</summary>
    /// <remarks>
    /// TWO REASONS TO SKIP, REPORTED SEPARATELY. `--no-shim` selects no steps and the platform gate
    /// closes on four of five platforms; a single "SKIPPED" would attribute a `--no-shim` run on an
    /// SSIS document to the platform gate, which is a false statement about which mechanism fired.
    /// `--no-shim` exists to demonstrate the degradation path, so misreporting its cause would
    /// misreport the demonstration.
    /// </remarks>
    internal string Describe()
      => $"platform={this.Platform ?? "UNSTATED"} "
        + $"translateExpressions={(this.TranslateExpressionsApplied ? "APPLIED"
            : !this.TranslateExpressionsSelected ? "SKIPPED (step not selected by the caller)"
            : "SKIPPED (platform is not " + SsisPlatform + ")")} "
        + $"expressionsInspected={this.ExpressionsInspected} "
        + $"rewrittenExpressions={this.RewrittenExpressions.Count}";
  }

  /// <summary>
  /// Which steps to apply. Individually selectable so a test can enable exactly one and show what the
  /// other unsupplied semantics do to the output — the difference between a gap that fails loudly and
  /// a gap that silently produces wrong SQL.
  /// </summary>
  [Flags]
  internal enum ShimSteps
  {
    /// <summary>Apply nothing; hydrate the framework IR verbatim. This now WORKS — see the remarks.</summary>
    None = 0,

    /// <summary>Rewrite SSIS-dialect expression text into Snowflake dialect.</summary>
    TranslateExpressions = 1,

    /// <summary>
    /// Everything still owned here. <c>SynthesizePassThrough</c> used to be the second flag; the value
    /// 2 is deliberately NOT reused, so an out-of-tree caller that still passes it selects nothing
    /// rather than silently selecting expression translation instead.
    /// </summary>
    All = TranslateExpressions,
  }

  /// <summary>
  /// Applies SSIS semantics to framework IR JSON, returning JSON of the SAME SHAPE.
  /// </summary>
  /// <remarks>
  /// Note what this does NOT do: add, remove or rename a single node, edge or property, and — since
  /// <c>SynthesizePassThrough</c> was deleted — it no longer adds an entry to any column array either.
  /// Every change is to a VALUE inside an <c>element</c>. That is the measurable sense in which the
  /// schemas now agree.
  /// </remarks>
  /// <param name="frameworkJson">The JSON emitted by the Python framework, verbatim.</param>
  /// <param name="steps">Which steps to apply.</param>
  /// <returns>The shimmed JSON and a report of every change made.</returns>
  internal static (string Json, ShimReport Report) Apply(
    string frameworkJson, ShimSteps steps = ShimSteps.All)
  {
    var root = JsonNode.Parse(frameworkJson)!.AsObject();

    // ---- WHICH PLATFORM PRODUCED THIS IR ------------------------------------------------------
    // Read from the IR, never inferred from the shape of the graph. A structural guess ("this looks
    // like SSIS because the container id contains a backslash") is the same class of mistake as the
    // hardcoded `Package\Data Flow Task` constant Program.cs's header records.
    var platform =
      root.TryGetPropertyValue("platform", out var platformNode) && platformNode is not null
        ? platformNode.GetValue<string>()
        : null;
    var isSsis = string.Equals(platform, SsisPlatform, StringComparison.Ordinal);

    var report = new ShimReport
    {
      Platform = platform,
      TranslateExpressionsSelected = steps.HasFlag(ShimSteps.TranslateExpressions),
      TranslateExpressionsApplied = steps.HasFlag(ShimSteps.TranslateExpressions) && isSsis,
    };

    foreach (var node in root["nodes"]!.AsArray())
    {
      var nodeObject = node!.AsObject();
      var element = nodeObject["element"]!.AsObject();

      // ---- SSIS expression dialect -------------------------------------------------------------
      // AiFirstProducerDataFlowContext.TranslateExpression parses with the ANSI/Snowflake grammar
      // (SqlParser.ParseExpr). SSIS `+` concatenation, `"` string literals and `[FUNC]` bracketed
      // function names are not Snowflake. The hand-authored IR that passes the M1/M2 spike tests
      // carries already-translated Snowflake and its own doc comment calls that "the producing
      // agent's job". Nothing in the chain does that job.
      //
      // GATED ON THE PLATFORM, not on the step flag alone. The expressions are still COUNTED when the
      // gate closes, so the report can distinguish "this platform has no expressions" from "this
      // platform has expressions and they were deliberately left in the source dialect".
      if (element.TryGetPropertyValue("OutputColumns", out var outputColumnsNode)
        && outputColumnsNode is JsonArray outputColumns)
      {
        foreach (var column in outputColumns)
        {
          var columnObject = column!.AsObject();
          if (!columnObject.TryGetPropertyValue("Expression", out var expressionNode) || expressionNode is null)
          {
            continue;
          }

          report.ExpressionsInspected++;
          if (!report.TranslateExpressionsApplied)
          {
            continue;
          }

          var before = expressionNode.GetValue<string>();
          var after = RewriteExpression(before);
          if (!string.Equals(before, after, StringComparison.Ordinal))
          {
            report.RewrittenExpressions.Add($"{before} => {after}");
            columnObject["Expression"] = after;
          }
        }
      }
    }

    return (root.ToJsonString(new System.Text.Json.JsonSerializerOptions { WriteIndented = true }), report);
  }

  /// <summary>
  /// Minimal SSIS-to-Snowflake expression rewrite. NOT a translator: three textual rules chosen to
  /// cover this one fixture, kept deliberately small so the test can show exactly how much is
  /// missing rather than hiding it behind something that looks general.
  /// </summary>
  /// <remarks>
  /// The `+` rule is the interesting one. Deciding whether SSIS `+` means numeric addition or string
  /// concatenation requires the operand TYPES. This stub infers "string" from the presence of a
  /// string literal in the expression, which is a heuristic that happens to be right here and is
  /// wrong in general — a real implementation needs the column type table the framework already has
  /// but does not consult for this purpose.
  /// </remarks>
  private static string RewriteExpression(string ssis)
  {
    // [YEAR](x) -> YEAR(x). SSIS brackets function names; in Snowflake brackets are not quoting.
    var rewritten = Regex.Replace(ssis, @"\[([A-Za-z_][A-Za-z0-9_]*)\]\s*\(", "$1(");

    // "literal" -> 'literal'. In Snowflake a double-quoted token is a quoted IDENTIFIER, so leaving
    // this alone yields SQL that parses and then fails at run time on an unknown column.
    var hadStringLiteral = Regex.IsMatch(rewritten, "\"[^\"]*\"");
    rewritten = Regex.Replace(rewritten, "\"([^\"]*)\"", "'$1'");

    // + -> || only when the expression contains a string literal (see remarks).
    if (hadStringLiteral)
    {
      rewritten = Regex.Replace(rewritten, @"\s*\+\s*", " || ");
    }

    return rewritten;
  }
}
