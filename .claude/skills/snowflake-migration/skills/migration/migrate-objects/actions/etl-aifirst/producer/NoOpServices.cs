// SPIKE 1 — the four Moq stand-ins, plus the two helpers the fixture defined privately.
//
// The fixture used `new Mock<X>().Object` for four interfaces and NEVER called `.Setup(...)`
// on any of them. That matters for fidelity: a bare loose Moq returns `default` for every
// member — null for reference types, zero/false for value types — and records nothing. So the
// faithful replacement is a no-op returning `default`, NOT a hand-tuned fake that behaves
// "sensibly". Behaving sensibly would change what the chain sees and make this spike prove
// something other than what the test proved.
//
// Where a member returns a non-nullable reference type, `null!` is used deliberately. That is
// exactly what Moq handed the production code, so if the production code dereferences it, it
// dereferenced a null under the test too and the test was passing for a reason nobody checked.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using Artinsoft.Common.AST;
using Mobilize.AnsiSql.AST;
using Mobilize.Snow.Assessment.AssessmentMode.ETLAndReporting;
using Mobilize.Snow.Common;
using Mobilize.Snow.Issues;
using Mobilize.SnowFlake.Sql.Ast;
using Snowflake.SnowConvert.EtlToDbt;
using Snowflake.SnowConvert.EtlToDbt.Context;
using Snowflake.SnowConvert.EtlToDbt.DbtGeneration;
using Snowflake.SnowConvert.EtlToDbt.Services.Interfaces;
using Snowflake.SnowConvert.EtlToDbt.Variables;

/// <summary>Replaces <c>new Mock&lt;IEtlAssessmentBuilderForPipelineContainer&gt;().Object</c>.</summary>
internal sealed class NoOpEtlAssessmentBuilder : IEtlAssessmentBuilderForPipelineContainer
{
  public void RegisterEwi(string fullName, IssueName issueName, params object[] args)
  {
  }

  public void RegisterSubtype(string fullName, string subtype)
  {
  }

  public void RegisterStatus(string fullName, EtlReplatformStatus status)
  {
  }

  public void RegisterDeclarationName(string fullName, string declarationName)
  {
  }

  public void RegisterPendingEntries()
  {
  }

  public void RegisterAdditionalInfo(string fullName, string propertyName, object value)
  {
  }

  public IReadOnlyList<(IssueName IssueName, object[] Args)> GetCollectedIssuesWithArgs()
    => Array.Empty<(IssueName, object[])>();

  public IReadOnlyDictionary<string, IReadOnlyList<(IssueName IssueName, object[] Args)>>
    GetCollectedIssuesByComponent()
    => new Dictionary<string, IReadOnlyList<(IssueName, object[])>>();

  // Nothing was registered, so nothing was assessed. The interface documents an empty set as the
  // answer for that case, which is also the only honest one for a builder that keeps nothing.
  public IReadOnlySet<string> GetAssessedComponents()
    => new HashSet<string>(StringComparer.Ordinal);
}

/// <summary>Replaces <c>new Mock&lt;IObjectTaggingProvider&gt;().Object</c>.</summary>
internal sealed class NoOpObjectTaggingProvider : IObjectTaggingProvider
{
  public SfCommentClause? GetObjectTagComment(IObjectTaggingContext context) => null;

  // Non-nullable in the interface, but loose Moq returned null here. Preserved rather than
  // "fixed", so the chain sees what it saw under the test.
  public SfCommentClause GetObjectTagComment(
    IReadOnlyDictionary<string, IList<string>> additionalComments) => null!;

  public string GetObjectUdfTagComment() => null!;

  // A fourth member my first pass MISSED. The grep that enumerated this interface used a
  // single-line signature pattern, and this declaration wraps its generic constraint onto a
  // second line, so it was invisible to the check that claimed to have listed every member.
  // The compiler caught it. Recording it because it is the same shape as the rest of this
  // project: a check that ran cleanly and answered a slightly narrower question than asked.
  public void AddObjectTagCommentAsDdlOption<TDdlOption>(
    IList<TDdlOption> ddlOptions, IObjectTaggingContext context)
    where TDdlOption : ISqlDdlOption
  {
  }
}

/// <summary>Replaces <c>new Mock&lt;ITaskConfigJsonGenerator&gt;().Object</c>.</summary>
internal sealed class NoOpTaskConfigJsonGenerator : ITaskConfigJsonGenerator
{
  public string? BuildConfigJson(IOrchestrationConversionContext context) => null;
}

/// <summary>
/// Copied verbatim from the fixture. Every member throws, so the translator's
/// swallow-and-substitute path cannot complete quietly — the mutation guard that stops this
/// spike from passing while generating error text.
/// </summary>
internal sealed class ThrowingEwiService : IEtlEwiService
{
  public IEwiFormatter EwiFormatter => throw new NotSupportedException(nameof(this.EwiFormatter));

  public void RegisterPipelineContainerNotConverted(
    string elementName, string parentName, string currentFileName)
    => throw new NotSupportedException(nameof(this.RegisterPipelineContainerNotConverted));

  public void RegisterPipelinePreProcessError(
    string elementName, string parentName, string currentFileName, IssueName issueName)
    => throw new NotSupportedException(nameof(this.RegisterPipelinePreProcessError));

  public void RegisterConversionLevelIssue(IssueName issueName, string contextName, params object[] args)
    => throw new NotSupportedException(nameof(this.RegisterConversionLevelIssue));

  public bool IsFdm(IssueName issueName) => throw new NotSupportedException(nameof(this.IsFdm));
}

/// <summary>Copied verbatim from the fixture.</summary>
internal sealed class PassThroughIssueCommentGenerator : IIssueCommentGenerator
{
  public TNode AddIssueCommentToSqlNode<TNode>(
    TNode node,
    (IssueName issue, object[] issueArguments) issueDetails)
    where TNode : class, ICompound
    => node;
}

/// <summary>
/// SPIKE 3b — a RECORDING EWI service, used only by the target probe.
/// <para>
/// <see cref="ThrowingEwiService"/> is the right default: it makes the translator's
/// swallow-and-substitute path impossible to complete quietly. But when that path IS taken, the throw
/// masks the ORIGINAL exception that caused the degradation. This variant records instead of throwing so
/// the underlying cause can be read, and it prints every registration so nothing is swallowed silently.
/// </para>
/// </summary>
internal sealed class RecordingEwiService : IEtlEwiService
{
  private readonly EwiInformationService ewiInformation =
    new(new EwiModelReader(null));

  public IEwiFormatter EwiFormatter { get; } =
    new EwiFormatter(new EwiInformationService(new EwiModelReader(null)));

  public void RegisterPipelineContainerNotConverted(
    string elementName, string parentName, string currentFileName)
    => System.Console.WriteLine($"  [ewi] container-not-converted: {elementName}");

  public void RegisterPipelinePreProcessError(
    string elementName, string parentName, string currentFileName, IssueName issueName)
    => System.Console.WriteLine($"  [ewi] pre-process-error: {elementName} {issueName}");

  public void RegisterConversionLevelIssue(IssueName issueName, string contextName, params object[] args)
    => System.Console.WriteLine($"  [ewi] conversion-level: {issueName} ctx={contextName}");

  /// <summary>
  /// ANSWERED FROM THE ISSUE'S OWN CODE, not hardcoded.
  /// </summary>
  /// <remarks>
  /// <para>
  /// This member used to be <c>=> false</c>, and that is not a harmless stub.
  /// <c>SqlUtils.AddIssueToElement</c> does <c>bool isBreaking = !ewiService.IsFdm(issueName)</c> and
  /// passes it to <c>AddCommentForEwiText</c>, so a hardcoded <c>false</c> renders EVERY issue as a
  /// BLOCKING <c>!!!RESOLVE EWI!!!</c> marker — including an FDM, which by definition is a functional
  /// difference to review rather than something that stops the model from running.
  /// </para>
  /// <para>
  /// No current artifact changes: measured across all four blind trees, zero FDMs are raised, so the
  /// old value was accidentally correct on every input tested. It was still a claim about issues
  /// nothing had classified, and the first FDM would have shipped mislabelled and inflated the
  /// blocking-EWI count. The engine's own rule is one line
  /// (<c>EtlEwiService.IsFdm</c>: the code's prefix equals <c>IssueTypePrefix.FdmIssuePrefix</c>) and
  /// is reproduced here rather than approximated, with the same prefix constant.
  /// </para>
  /// </remarks>
  /// <param name="issueName">The issue.</param>
  /// <returns>True when the issue's code is an FDM.</returns>
  public bool IsFdm(IssueName issueName)
  {
    try
    {
      return this.ewiInformation.GetCode(issueName)
        .StartsWith(IssueTypePrefix.FdmIssuePrefix, StringComparison.OrdinalIgnoreCase);
    }
    catch (Exception)
    {
      // An unclassifiable issue is treated as BREAKING, which is the safe direction: it over-reports
      // severity rather than quietly downgrading something to a non-blocking comment.
      return false;
    }
  }
}
