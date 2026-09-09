// SPIKE 3b (continued) — the SECOND mandatory dependency of the target path.
//
// TargetTranslatorBase requires IEtlSqlProcessor as well as IInfPcSqlValueMigrator, and enforces both
// with null checks. Unlike the migrator, this interface is NOT Informatica-named: it is a neutral SQL
// parsing/transforming service. A producer that supplies no embedded SQL has nothing for it to do, so
// "nothing parsed" is the truthful answer rather than a shortcut.
//
// Member list and return types taken from the COMPILER. A regex extraction over the interface file
// reported 2 of 4 members and got both return types wrong — the fourth undercount by signature-grep in
// this project. Non-nullable returns are satisfied with `null!`, the same fidelity choice made for the
// Moq replacements in NoOpServices.cs: if the translator dereferences it, it dereferenced null under
// the real service too and nobody noticed.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using Artinsoft.Common.AST;
using Mobilize.Snow.Common;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Services.SqlProcessing;

internal sealed class NoOpEtlSqlProcessor : IEtlSqlProcessor
{
  public string CurrentLanguageName => "producer";

  public AstSource ParseSqlQuery(string code, string currentFileName) => null!;

  public AstSource TransformSqlQueryForLineageOnly(
    string code,
    string currentFileName,
    string implicitLineageContext,
    string? implicitScope = null) => null!;

  public (AstSourceBuilder resultSource, IEnumerable<(IssueName IssueName, object[] Args)> ewis)
    TransformSqlQuery(
      string code,
      string currentFileName,
      string? implicitLineageContext = null,
      string? implicitScope = null,
      Dictionary<string, string>? replacements = null)
    => (null!, Array.Empty<(IssueName, object[])>());
}

/// <summary>
/// The multi-dialect variant <see cref="Snowflake.SnowConvert.EtlToDbt.DbtGeneration.Translations.SourceQualifierTranslator"/>
/// requires. A separate interface from <see cref="IEtlSqlProcessor"/>, not a subtype of it — so the
/// no-op above cannot be reused. Member list from the COMPILER, as before.
/// </summary>
internal sealed class NoOpMultiDialectEtlSqlProcessor : IMultiDialectEtlSqlProcessor
{
  public AstSource ParseSqlQuery(string code, string currentFileName, SourceLanguage dialect) => null!;

  public AstSource TransformSqlQueryForLineageOnly(
    string code,
    string currentFileName,
    SourceLanguage dialect,
    string implicitLineageContext,
    string? implicitScope = null) => null!;

  public (AstSourceBuilder resultSource, IEnumerable<(IssueName IssueName, object[] Args)> ewis)
    TransformSqlQuery(
      string code,
      string currentFileName,
      SourceLanguage dialect,
      string? implicitLineageContext = null,
      string? implicitScope = null,
      Dictionary<string, string>? replacements = null)
    => (null!, Array.Empty<(IssueName, object[])>());
}
