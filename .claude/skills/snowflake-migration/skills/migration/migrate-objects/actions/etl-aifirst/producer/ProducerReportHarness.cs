// The non-Moq harness for the three producer-drivable reports.
//
// WHY HAND-WRITTEN AND NOT MOQ. `poc/spikes/slice-reports-registry/Program.cs` proved these writers are
// drivable, but it did so with four Moq mocks. This project's callable entry point deliberately excludes
// Moq from its reference set (CallableMigrator.csproj `_ExcludeDlls`) because the whole question SPIKE 1
// answered was whether the chain runs without the test host. Re-admitting Moq to get reports would
// un-answer it. Every mock in that spike was a no-setup loose mock or a two-property stub, so the
// faithful replacement is a plain class.
//
// THE MEMBER LISTS ARE THE COMPILER'S. Three separate times in this project a single-line signature grep
// has undercounted an interface (see NoOpServices.cs, NoOpSqlValueMigrator.cs). Every `NotSupportedException`
// below is a member the report path is BELIEVED not to touch; if it does, the driver fails loudly at the
// exact member rather than writing a report built on a silent default.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using System.Linq;
using Artinsoft.Common.AST;
using Artinsoft.Common.Tools.Composition;
using Mobilize.AnsiSql.AST;
using Mobilize.Assessment.AssessmentMode.Interfaces;
using Mobilize.Assessment.AssessmentMode.Model;
using Mobilize.Snow.Assessment;
using Mobilize.Snow.Assessment.Interfaces;
using Mobilize.Snow.Configuration;
using Mobilize.Snow.Constants;
using Mobilize.Sql.Lineage;

/// <summary>
/// Satisfies the ONE seam every <c>SnowCustomReportWriter&lt;T&gt;</c> actually reads:
/// <c>TryEnumerateInventory&lt;T&gt;</c>. The writer calls it, and on <c>false</c> writes a one-line
/// PLACEHOLDER file and still returns <c>true</c> — which is why the driver reads the bytes back
/// instead of trusting the return value.
/// </summary>
internal sealed class CalculatorBackedWriterModel(IAssessmentDynamicCalculator calculator)
  : IAssessmentWriterModel
{
  public bool TryEnumerateInventory<T>(ReportKind reportKind, IAssessmentModeModel model, out IEnumerable<T> fields)
    where T : class, IReportField
  {
    fields = calculator.EnumerateRows(model).OfType<T>().ToList();
    return fields.Any();
  }

  public bool TryGetCalculator<T>(out T? calculator2)
    where T : class, IAssessmentCalculator
  {
    calculator2 = calculator as T;
    return calculator2 is not null;
  }

  public IEnumerable<AssessmentReportItem> EnumerateInventory(
    IAssessmentSummary summary, IEnumerable<IAssessmentKey> keys)
    => throw new NotSupportedException(nameof(this.EnumerateInventory));

  public void EnumerateInventory<T>(
    IAssessmentSummary summary, IEnumerable<T> keys, Action<T, string> predicate)
    where T : IAssessmentKey
    => throw new NotSupportedException(nameof(this.EnumerateInventory));

  public string Get(IAssessmentKey key, IAssessmentSummary summary)
    => throw new NotSupportedException(nameof(this.Get));

  public string? Get(string key, IAssessmentSummary summary)
    => throw new NotSupportedException(nameof(this.Get));

  // From IAssessmentComponent, and a member the FOURTH signature-grep undercount in this project would
  // have missed: the compiler named it. Left as a no-op rather than a throw because the report writers
  // are entitled to reset a model they own, and throwing would turn a legitimate reset into a crash.
  public void Clear()
  {
  }
}

/// <summary>
/// <c>SnowReportWriter</c>'s constructor does exactly one thing with this:
/// <c>if (configurationProvider?.Configuration is null) throw new ArgumentNullException(...)</c>.
/// So a non-null configuration is the entire contract for the three CSV writers driven here.
/// </summary>
internal sealed class ProducerAssessmentConfigurationProvider : IAssessmentConfigurationProvider
{
  public IAssessmentConfiguration Configuration { get; } = new ProducerAssessmentConfiguration();

  public IAssessmentConfiguration GetConfigurationForDialect(string dialect) => this.Configuration;
}

/// <summary>
/// Every member throws. The producer has no AST, no top-level object taxonomy and no code-unit
/// validator, so a benign default here would be a claim about source code nothing read.
/// </summary>
internal sealed class ProducerAssessmentConfiguration : IAssessmentConfiguration
{
  public string LanguageSlug => throw new NotSupportedException(nameof(this.LanguageSlug));

  public string SourceLanguage => throw new NotSupportedException(nameof(this.SourceLanguage));

  public bool ShouldCountComments => throw new NotSupportedException(nameof(this.ShouldCountComments));

  public IObjectDefinition ObjectDefinition => throw new NotSupportedException(nameof(this.ObjectDefinition));

  public ISqlCodeUnitValidator CodeUnitValidator => throw new NotSupportedException(nameof(this.CodeUnitValidator));

  public IFileDefinition FileDefinition => throw new NotSupportedException(nameof(this.FileDefinition));

  public IReportFieldDefinition ReportFieldDefinition
    => throw new NotSupportedException(nameof(this.ReportFieldDefinition));

  public IEnumerable<Lazy<IExtensibleAstDelegate>> TranslationRules
    => throw new NotSupportedException(nameof(this.TranslationRules));

  public ILanguageAssessmentSetup AssessmentSetup => throw new NotSupportedException(nameof(this.AssessmentSetup));

  public IDocxTemplateInformation TemplateInformation
    => throw new NotSupportedException(nameof(this.TemplateInformation));

  public bool IsScriptingEnabled => throw new NotSupportedException(nameof(this.IsScriptingEnabled));

  public HashSet<string> ExcludedIssueCategories
    => throw new NotSupportedException(nameof(this.ExcludedIssueCategories));

  public int MaxNamesNumber => throw new NotSupportedException(nameof(this.MaxNamesNumber));

  public IReadmeTemplateInformation ReadmeTemplateInformation
    => throw new NotSupportedException(nameof(this.ReadmeTemplateInformation));

  public bool EnclosedQualifiedNamesAllowed
    => throw new NotSupportedException(nameof(this.EnclosedQualifiedNamesAllowed));

  public char QuotedIdentifiersCharacter
    => throw new NotSupportedException(nameof(this.QuotedIdentifiersCharacter));

  public bool IsNodeSupported(Compound node, TargetLanguages target = 0)
    => throw new NotSupportedException(nameof(this.IsNodeSupported));
}

/// <summary>
/// The producer's own migration metadata.
/// </summary>
/// <remarks>
/// <para>
/// <c>EtlInputPath</c> is NOT cosmetic: <c>EtlReplatformIssuesReportWriter</c>'s constructor sets
/// <c>shouldGenerateReport = !string.IsNullOrEmpty(migrationDataService.EtlInputPath)</c>, and
/// <c>ShouldBeGenerated</c> gates <c>GenerateReport</c> into returning false with NO file and NO error.
/// Leave it empty and ETL.Issues is silently absent — which is indistinguishable from "there were no
/// issues" unless something counts the files, which is what stage 4 now does.
/// </para>
/// <para>
/// Everything the report path does not read throws, for the reason
/// <see cref="ProducerAssessmentConfiguration"/> gives.
/// </para>
/// </remarks>
internal sealed class ProducerMigrationDataService(
  string etlInputPath,
  string partitionKey,
  string migrationId,
  string sessionTimestamp) : IMigrationDataService
{
  public string? EtlInputPath => etlInputPath;

  public string PartitionKey => partitionKey;

  public string MigrationId => migrationId;

  public string SessionTimestamp => sessionTimestamp;

  // Read by ObjectReferenceCalculator.Add(ICompound, ILineageContext) -- the AST route, which a producer
  // never takes. Answered rather than thrown only because the ctor stores it eagerly.
  public string InputPath => etlInputPath;

  public string SourceLanguage => "Ansi";

  public bool ParseAndAssess => false;

  public bool ReSync => false;

  public bool MidwayReSync => false;

  public bool MidwayMapping => false;

  public string? MidwayMappingFilePath => null;

  public bool MidwayWorkflow => false;

  public bool OverwriteWorkingDirectory => false;

  public EngineWorkFlow EngineWorkFlow => throw new NotSupportedException(nameof(this.EngineWorkFlow));

  public string? ProjectPath => null;

  public string? ArtifactsPath => null;

  public string? WorkingDirectory => null;

  public string? EtlTargetBasePath => null;

  public string AppVersion => "aifirst-producer-0.0.1";

  public string SnowflakeAccountIdentifier => throw new NotSupportedException(nameof(this.SnowflakeAccountIdentifier));

  public string SnowflakeUser => throw new NotSupportedException(nameof(this.SnowflakeUser));

  public string AppType => throw new NotSupportedException(nameof(this.AppType));

  public string ProductName => throw new NotSupportedException(nameof(this.ProductName));

  public string LicenseData => throw new NotSupportedException(nameof(this.LicenseData));

  public bool SnowScript => false;

  public string ConversionCore => throw new NotSupportedException(nameof(this.ConversionCore));

  public string WorkloadName => throw new NotSupportedException(nameof(this.WorkloadName));

  public string CreateSession => throw new NotSupportedException(nameof(this.CreateSession));

  public string SystemRam => throw new NotSupportedException(nameof(this.SystemRam));

  public string SystemCpu => throw new NotSupportedException(nameof(this.SystemCpu));

  public string RunAsAdmin => throw new NotSupportedException(nameof(this.RunAsAdmin));

  public bool Preprocessed => false;

  public string WarehouseName => throw new NotSupportedException(nameof(this.WarehouseName));

  public string TargetLagValue => throw new NotSupportedException(nameof(this.TargetLagValue));

  public string ProjectName => throw new NotSupportedException(nameof(this.ProjectName));

  public string OutputPath => throw new NotSupportedException(nameof(this.OutputPath));

  public bool TransformExternalTablesToRegular => false;

  public bool AddPartitionedColumnsToTableDefinition => false;

  public bool EnableDynamicSqlAnalysis => false;

  public SfTableType TargetTableType => throw new NotSupportedException(nameof(this.TargetTableType));

  // The six members below arrived on IMigrationDataService with the engine's bindable-database and
  // Power BI multi-db work, AFTER this producer was last built (the hand-copied POC bin predates them).
  // The producer takes none of those routes, so all six answer rather than throw: a thrown member here
  // would fail composition on a path the report run does walk.
  public bool GenerateSnowflakeBindableFormat => false;

  public bool GenerateSourceBindableFormat => false;

  public string? SourceBindablePath => null;

  // NOT the directory the producer's own reports land in. ProducerReports computes
  // `<outRoot>/Reports` and hands it to the writer directly, and the engine's report writers take
  // MigrationVariableKey.ReportsPath through MEF composition, not this property. The only interface
  // consumer is BindableDatabaseYamlWriter, unreachable while both bindable flags above are false.
  public string? ReportsPath => null;

  public string? DatabaseBindingsPath => null;

  public bool PbiMultiDb => false;

  public bool DisableUseDatabaseGeneration => false;

  // The eight members below arrived on IMigrationDataService with the engine's Hybrid Table work,
  // after this producer was last built. Standard is the engine's own default and the only
  // equivalence-preserving mode: no source table is converted to a Hybrid Table. A producer for a
  // novel platform states no opinion on target table type, so the selection sets are empty and the
  // two generation toggles are off, which is what an unset migration answers.
  public HybridTableConversionMode HybridTableConversionMode => HybridTableConversionMode.Standard;

  public IReadOnlySet<string> HybridTables => new HashSet<string>(StringComparer.Ordinal);

  public IReadOnlySet<string> HybridIncludePatterns => new HashSet<string>(StringComparer.Ordinal);

  public IReadOnlySet<string> HybridExcludePatterns => new HashSet<string>(StringComparer.Ordinal);

  // The factory is documented to never fail to construct; with no symbol-table provider it answers
  // the default SQL comparer, which is what the selection sets above would be compared with had any
  // of them been non-empty.
  public IdentifierNameComparer HybridTableNameComparer
    => IdentifierNameComparerFactory.Create(this.SourceLanguage, null);

  public IReadOnlySet<string> HybridSourceCommentPatterns
    => new HashSet<string>(StringComparer.Ordinal);

  public bool EnableHybridSecondaryIndexes => false;

  public bool EnableHybridInlineProcedures => false;

  public HashSet<string>? WhereFilteredPaths => null;

  public string? SourceId => null;

  public string? ResyncChangesPath => null;

  public bool DisableRegistry => true;

  public bool UseIntervalDatatype => false;

  public bool UsePeriodDatatype => false;

  public TargetLanguages ProcedureTargetLanguage
    => throw new NotSupportedException(nameof(this.ProcedureTargetLanguage));

  public string CustomSchema => throw new NotSupportedException(nameof(this.CustomSchema));

  public string CustomDatabase => throw new NotSupportedException(nameof(this.CustomDatabase));

  public bool UseExistingNameQualification => false;

  public bool CommentIfMissingDependencies => false;

  public bool AvoidStringTokenizationComparisons => false;

  public bool SerializeTransformedCode => false;

  public string? ProjectContextPath => null;

  public string ConversionRateMode => throw new NotSupportedException(nameof(this.ConversionRateMode));

  public bool DisableEwisGeneration => false;

  public bool SplitPeriodDatatype => false;

  public bool DisableTopologicalLevelReorder => false;

  public SupportedEncodings Encoding => throw new NotSupportedException(nameof(this.Encoding));

  public bool InformaticaToSnowflakeScripting => false;

  public bool RenamingEnabled => false;

  public bool EnableAiTransformation => false;

  public string? AiCustomSkillsPath => null;

  public bool OutputAiSkills => false;
}

/// <summary>
/// Records the reports the writers announce, so the driver can print what the engine THINKS it wrote
/// next to what is actually on disk. The two disagreeing is the placeholder case.
/// </summary>
internal sealed class RecordingSnowTelemetry : ISnowTelemetry
{
  internal List<(ReportKind Kind, string Name)> Reports { get; } = [];

  public void AddReport(ReportKind kind, string reportName) => this.Reports.Add((kind, reportName));

  public void SendInformation(IAssessmentModeModel model, IAssessmentSummary summary)
    => throw new NotSupportedException(nameof(this.SendInformation));
}

/// <summary>
/// Only consulted on <c>ObjectReferenceCalculator.Add(ICompound, ILineageContext)</c> — the AST route.
/// The producer uses <c>AddDirect</c>, which reads nothing from it, so a throw here proves that claim
/// rather than assuming it.
/// </summary>
internal sealed class UnusedLineageInputPathCalculator : Mobilize.Snow.Common.ILineageInputPathCalculator
{
  public string GetInputPath(ILineageContext ctx, CallerElement caller)
    => throw new NotSupportedException(
      "GetInputPath was called, so the producer reached the AST lineage route after all.");
}
