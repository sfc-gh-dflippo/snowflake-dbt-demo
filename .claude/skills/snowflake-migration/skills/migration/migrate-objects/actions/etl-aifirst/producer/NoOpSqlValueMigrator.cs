// SPIKE 3b (continued) — is the target path's Informatica coupling NOMINAL or SEMANTIC?
//
// TargetTranslatorBase's constructor REQUIRES IInfPcSqlValueMigrator and enforces it:
//   this.sqlValueMigrator = sqlValueMigrator ?? throw new ArgumentNullException(...)
// so no target translator can be constructed without supplying an Informatica-named service.
//
// Three facts suggested the coupling might be nominal rather than semantic, and this file tests that
// rather than reasoning about it:
//   1. IInfPcSqlValueMigrator lives in Services.SqlProcessing — a NEUTRAL namespace, not an
//      Informatica one. Every member returns a nullable string or an empty-able record.
//   2. InfPcTranslationHelpers.BuildColumnProjection is neutral code — Sql.MemberAccessExpr /
//      Sql.SingleNameExpr plus an optional cast. Nothing Informatica-shaped.
//   3. BuildNullColumnProjection, by contrast, calls InfPcDataTypeMapping.BuildSizedSnowflakeType —
//      Informatica type mapping. So the coupling may be confined to NULL columns.
//
// If a no-op migrator yields correct target SQL, the requirement is a dependency-injection artefact and
// targets ARE reusable. If not, the target path is genuinely Informatica and every real migration is
// blocked on it, because data has to land somewhere.
//
// NOTE ON THE MEMBER LIST: extracting it by grep undercounted twice — first 6 of 11, because signatures
// wrap across lines, then again because MigrateWithIssues and MigrateWithSources are inherited from a
// base interface and are not in the file at all. The list below is the COMPILER's, which is the only
// authoritative one. Third time in this project that a single-line signature grep has undercounted an
// interface; the lesson is to let the compiler enumerate, not a regex.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using Artinsoft.Common.AST;
using Mobilize.Snow.Common;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Services.SqlProcessing;
using Snowflake.SnowConvert.EtlToDbt.Variables;

/// <summary>
/// A no-op <see cref="IInfPcSqlValueMigrator"/>. Every member returns the "nothing to migrate" answer,
/// which is the TRUTHFUL answer for a producer that supplies no SQL hooks, no variable tokens and no
/// session overrides — not a convenient shortcut. Raw SQL is returned unchanged rather than nulled, so
/// that if the translator does use it, the output shows the input rather than silently losing it.
/// </summary>
internal sealed class NoOpInfPcSqlValueMigrator : IInfPcSqlValueMigrator
{
  public string? Migrate(
    string? rawSql,
    string fileName,
    string? lineageComponentName = null,
    IReadOnlyList<EtlVariableDefinition>? variableDefinitions = null,
    string? currentScopeName = null) => rawSql;

  public string? Migrate(
    string? rawSql,
    string fileName,
    IReadOnlyList<string> fdmComments,
    string? lineageComponentName = null,
    IReadOnlyList<EtlVariableDefinition>? variableDefinitions = null,
    string? currentScopeName = null) => rawSql;

  public (string? sql, IReadOnlyList<(IssueName IssueName, object[] Args)> ewis) MigrateWithIssues(
    string? rawSql,
    string fileName,
    string? lineageComponentName = null,
    IReadOnlyList<EtlVariableDefinition>? variableDefinitions = null,
    string? currentScopeName = null)
    => (rawSql, Array.Empty<(IssueName, object[])>());

  public SourceIdentificationResult IdentifySources(
    string? rawSql,
    string fileName,
    Func<string, string> sourceNameSanitizer,
    IReadOnlyList<string>? fdmComments = null,
    string? lineageComponentName = null,
    Func<ICompound, ICompound>? astTransform = null,
    SourceLanguage? dialect = null)
    => new() { BodyWithVariablePlaceholders = rawSql };

  public (string? sql, IReadOnlySet<string> identifiedSources,
          IReadOnlyList<(IssueName IssueName, object[] Args)> ewis) MigrateWithSources(
    string? rawSql,
    string fileName,
    Func<string, string> sourceNameSanitizer,
    IReadOnlyList<string>? fdmComments = null,
    string? lineageComponentName = null,
    IReadOnlyList<EtlVariableDefinition>? variableDefinitions = null,
    string? currentScopeName = null,
    Func<ICompound, ICompound>? astTransform = null)
    => (rawSql, new HashSet<string>(), Array.Empty<(IssueName, object[])>());

  public SourceIdentificationResult IdentifyHookBody(
    string? rawSql,
    string fileName,
    string? lineageComponentName = null)
    => new() { BodyWithVariablePlaceholders = rawSql };

  public string? MigrateToJinjaBody(
    SourceIdentificationResult identification,
    IReadOnlyList<EtlVariableDefinition>? variableDefinitions = null,
    string? currentScopeName = null) => identification.BodyWithVariablePlaceholders;

  public string? MigrateToScriptingBody(SourceIdentificationResult identification)
    => identification.BodyWithVariablePlaceholders;
}
