// <copyright file="DialectPlatform.cs" company="Snowflake Inc">
//        Copyright (c) 2019-2026 Snowflake Inc. All rights reserved.
// </copyright>

namespace AiFirst.Producer;

using System;

/// <summary>
/// One place that knows which <c>platformId</c> strings mean "this document is genuinely SSIS" or
/// "genuinely Informatica". <see cref="ProducerReports.IsForeignDialectBleed"/> used to be the only
/// caller of this classification; SQL-artifact dialect bleed needs the SAME classification at
/// EMISSION time (<see cref="AiFirstProducerDataFlowContext"/>, <see cref="AiFirstProducerIrHydrator"/>),
/// before there is a code string to test. Two independent copies of "ssis is dtsx-or-ssis" is how they
/// drift; this is the one definition both the report filter and the emitters read.
/// </summary>
internal static class DialectPlatform
{
  internal static bool IsSsisNative(string? platformId) => Normalize(platformId) is "ssis" or "dtsx";

  internal static bool IsInformaticaNative(string? platformId) => Normalize(platformId) is "informatica" or "infpc" or "xml";

  internal static string Normalize(string? platformId) => (platformId ?? string.Empty).Trim().TrimStart('.').ToLowerInvariant();

  /// <summary>
  /// The name this document's platform goes under in the assessment report's <c>Technology</c> column.
  /// </summary>
  /// <remarks>
  /// <para>
  /// THE COLUMN WAS NEVER CLOSED. <c>EtlReplatformReportItem.Technology</c> is a free
  /// <see cref="string"/> defaulting to <c>N/A</c>, and the engine's own writers put unconstrained
  /// names in it (<c>Power BI</c>, <c>dbt</c>, Tableau's). The value this method used to return --
  /// a hardcoded <c>Ssis</c> on every platform -- was justified by a closed-vocabulary premise that
  /// does not hold for this column. It confused the column with the <c>EtlTechnology</c> ENUM, which
  /// is closed, and which only the engine's own <c>EtlAssessmentBuilderForFile</c> converts.
  /// </para>
  /// <para>
  /// ONE ENGINE CONSUMER READS THE VALUE, THOUGH NOT ON THIS PATH.
  /// <c>EtlTransformationTask.GenerateSsisInstrumentationConfigIfRequired</c> compares the column
  /// case-insensitively against <c>EtlTechnologies.SSIS</c> and generates SSIS baseline
  /// instrumentation when a row matches. The producer does not run that task, so no measured run was
  /// affected by it -- do NOT cite it as a consequence of the old value. It is stated here for the
  /// opposite reason: it is why a genuinely SSIS document must keep reading <c>Ssis</c> if these rows
  /// ever reach that task.
  /// </para>
  /// <para>
  /// The values below track <c>EtlTechnology</c>'s member names
  /// where that enum has a member, so a producer-written row reads the same as an engine-written one
  /// (<c>EtlAssessmentBuilderForFile</c> writes <c>technologyId.ToString()</c>). The platform tables'
  /// own <c>platform</c> keys are deliberately NOT used: they say
  /// <c>SqlServerIntegrationServices</c>, which would stop matching the gate above and would silently
  /// disable instrumentation for real SSIS.
  /// </para>
  /// <para>
  /// An id this does not recognize returns the column's own default rather than borrowing some other
  /// platform's name. <c>json</c> is unmapped for that reason: both the ADF and the SSIS table claim it.
  /// </para>
  /// </remarks>
  internal static string DisplayName(string? platformId)
  {
    if (IsSsisNative(platformId))
    {
      return "Ssis";
    }

    if (IsInformaticaNative(platformId))
    {
      return "InformaticaPowerCenter";
    }

    return Normalize(platformId) switch
    {
      "alteryx" or "yxmd" or "yxmc" => "Alteryx",
      "datastage" or "dsx" => "DataStage",
      "pentaho" or "ktr" or "kjb" => "Pentaho",
      "adf" => "AzureDataFactory",
      _ => "N/A",
    };
  }
}
