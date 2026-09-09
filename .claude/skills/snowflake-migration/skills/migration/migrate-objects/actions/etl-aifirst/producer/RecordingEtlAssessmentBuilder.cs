// The assessment builder that WAS a no-op, and the measurement that made replacing it necessary.
//
// WHAT WAS MEASURED. `TransformationUnitTranslator.GenerateUnsupportedElementConversion` calls
//   ctx.AssessmentReportsServiceForContainer.RegisterEwi(transformation.Id, ctx.IssueForExceptionOnPipelineElement, ewiArgs);
//   ctx.AssessmentReportsServiceForContainer.RegisterStatus(transformation.Id, EtlReplatformStatus.NotSupported);
// and `SqlUtils.AddIssueToElement` — the one routine every `ctx.AddIssueToElement` call goes through —
// calls `assessmentBuilder.RegisterEwi(elementName, issueName, args)` for EVERY issue it attaches.
// `NoOpEtlAssessmentBuilder` implements all of them as `{ }`.
//
// So the EWIs were never suppressed and never absent: they were RAISED, rendered into the .sql as an
// inline `!!!RESOLVE EWI!!!` comment, and then DROPPED on the reporting side. Four blind trees carried
// two inline EWIs between them and zero issue rows, and the two facts had the same single cause.
// Recording them is the whole difference between "the artifact says so" and "the report says so".
//
// It records rather than throws (unlike ThrowingEwiService, whose loudness is right for the EWI
// FORMATTER): a builder that throws on RegisterEwi turns the engine's honest-degradation path into a
// crash, which would destroy the very information this class exists to collect.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Linq;
using Mobilize.Snow.Assessment.AssessmentMode.ETLAndReporting;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Services.Interfaces;

/// <summary>
/// An <see cref="IEtlAssessmentBuilderForPipelineContainer"/> that KEEPS what it is told, so the
/// producer's ETL.Issues and ETL.Elements reports are built from what the engine's own translators
/// actually raised rather than from anything this driver decided.
/// </summary>
internal sealed class RecordingEtlAssessmentBuilder : IEtlAssessmentBuilderForPipelineContainer
{
  private readonly List<(string FullName, IssueName IssueName, object[] Args)> issues = [];
  private readonly Dictionary<string, EtlReplatformStatus> statuses = new(StringComparer.Ordinal);
  private readonly Dictionary<string, string> subtypes = new(StringComparer.Ordinal);
  private readonly Dictionary<string, string> declarationNames = new(StringComparer.Ordinal);
  private readonly List<(string FullName, string Property, object Value)> additionalInfo = [];

  /// <summary>Every issue registration, in registration order, with the component it was attached to.</summary>
  internal IReadOnlyList<(string FullName, IssueName IssueName, object[] Args)> Issues => this.issues;

  /// <summary>Statuses the engine assigned per component full name.</summary>
  internal IReadOnlyDictionary<string, EtlReplatformStatus> Statuses => this.statuses;

  internal IReadOnlyDictionary<string, string> Subtypes => this.subtypes;

  internal IReadOnlyDictionary<string, string> DeclarationNames => this.declarationNames;

  internal IReadOnlyList<(string FullName, string Property, object Value)> AdditionalInfo => this.additionalInfo;

  /// <summary>
  /// Times <see cref="RegisterPendingEntries"/> was called. Recorded rather than acted on: the real
  /// builder flushes deferred rows here, and a producer that never sees the call would be quietly
  /// missing them.
  /// </summary>
  internal int PendingEntryFlushes { get; private set; }

  public void RegisterEwi(string fullName, IssueName issueName, params object[] args)
    => this.issues.Add((fullName ?? string.Empty, issueName, args ?? []));

  public void RegisterSubtype(string fullName, string subtype)
    => this.subtypes[fullName ?? string.Empty] = subtype;

  public void RegisterStatus(string fullName, EtlReplatformStatus status)
    => this.statuses[fullName ?? string.Empty] = status;

  public void RegisterDeclarationName(string fullName, string declarationName)
    => this.declarationNames[fullName ?? string.Empty] = declarationName;

  public void RegisterPendingEntries() => this.PendingEntryFlushes++;

  public void RegisterAdditionalInfo(string fullName, string propertyName, object value)
    => this.additionalInfo.Add((fullName ?? string.Empty, propertyName, value));

  public IReadOnlyList<(IssueName IssueName, object[] Args)> GetCollectedIssuesWithArgs()
    => this.issues.Select(i => (i.IssueName, i.Args)).ToList();

  public IReadOnlyDictionary<string, IReadOnlyList<(IssueName IssueName, object[] Args)>>
    GetCollectedIssuesByComponent()
    => this.issues
      .GroupBy(i => i.FullName, StringComparer.Ordinal)
      .ToDictionary(
        g => g.Key,
        g => (IReadOnlyList<(IssueName, object[])>)g.Select(i => (i.IssueName, i.Args)).ToList(),
        StringComparer.Ordinal);

  /// <summary>
  /// Every component this builder was told anything about, by any registration route. The engine's
  /// own builder answers the names it was asked to check unioned with the ones carrying issues; a
  /// builder that keeps what it is told has no separate "asked to check" set, so the union of all
  /// registration surfaces is the same fact. Ordinal for the reason the engine states: these keys
  /// are source-derived ids, case-sensitive by spec, matched by name elsewhere.
  /// </summary>
  public IReadOnlySet<string> GetAssessedComponents()
  {
    var assessed = new HashSet<string>(StringComparer.Ordinal);
    assessed.UnionWith(this.statuses.Keys);
    assessed.UnionWith(this.subtypes.Keys);
    assessed.UnionWith(this.declarationNames.Keys);
    assessed.UnionWith(this.additionalInfo.Select(a => a.FullName));
    assessed.UnionWith(this.issues.Select(i => i.FullName));
    return assessed;
  }
}
