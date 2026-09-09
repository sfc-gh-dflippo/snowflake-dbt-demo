namespace AiFirst.Producer.Tests;

using System;
using System.Collections.Generic;
using System.Linq;
using AiFirst.Producer;
using Microsoft.Extensions.Logging.Abstractions;
using Mobilize.Snow.Issues;
using Snowflake.SnowConvert.EtlToDbt.Dag;
using Snowflake.SnowConvert.EtlToDbt.Models;

internal static class ReconciliationTests
{
  private const string NodeId = "probe";
  private const string Stem = "probe";

  public static int Main()
  {
    try
    {
      MissingEwiRegistrationFailsAccounting();
      ForeignFdmFailsReportAndDialectChecks();
      NativeFdmWithMatchingReportsPasses();
      ForeignDialectBleedClassification();
      Console.WriteLine("ReconciliationTests: 4 passed");
      return 0;
    }
    catch (Exception ex)
    {
      Console.Error.WriteLine(ex.Message);
      return 1;
    }
  }

  private static void MissingEwiRegistrationFailsAccounting()
  {
    var result = Reconcile(
      "!!!RESOLVE EWI!!! /*** SSC-EWI-0013 - SYNTHETIC ACCOUNTING MISMATCH ***/!!!",
      new Dictionary<string, IReadOnlyList<(IssueName, object[])>>(),
      new HashSet<(string, string)>(),
      "yxmd");

    Assert(result.Checked == 1, "EWI mismatch: expected one marker");
    Assert(result.Failures.Count == 1, "EWI mismatch: expected exactly one accounting failure");
    Assert(result.Failures.Single().Contains("NO matching row in ETL.Elements.NA.csv", StringComparison.Ordinal),
      "EWI mismatch: wrong failure reason");
    Assert(!result.Failures.Single().Contains("illegal on platform", StringComparison.Ordinal),
      "EWI mismatch: generic code must not be classified as dialect bleed");
  }

  private static void ForeignFdmFailsReportAndDialectChecks()
  {
    var issues = IssuesFor(IssueName.InformaticaPcDuplicateTargetsUnionAll);
    var result = Reconcile(
      "--** SSC-FDM-INF0029 - SYNTHETIC FOREIGN FDM **",
      issues,
      new HashSet<(string, string)>(),
      "yxmd");

    Assert(result.Checked == 1, "foreign FDM: expected one marker");
    Assert(result.Failures.Count == 2, "foreign FDM: expected report-row and dialect failures");
    Assert(result.Failures.Any(f => f.Contains("NO row in ETL.Issues.NA.csv", StringComparison.Ordinal)),
      "foreign FDM: missing ETL.Issues failure");
    Assert(result.Failures.Any(f => f.Contains("illegal on platform 'Alteryx'", StringComparison.Ordinal)),
      "foreign FDM: missing illegal-dialect failure");
    Assert(result.Failures.All(f => !f.Contains("NO matching row in ETL.Elements.NA.csv", StringComparison.Ordinal)),
      "foreign FDM: element registration should be present");
  }

  private static void NativeFdmWithMatchingReportsPasses()
  {
    var issues = IssuesFor(IssueName.InformaticaPcDuplicateTargetsUnionAll);
    var result = Reconcile(
      "--** SSC-FDM-INF0029 - SYNTHETIC NATIVE FDM **",
      issues,
      new HashSet<(string, string)> { (NodeId, "SSC-FDM-INF0029") },
      "xml");

    Assert(result.Checked == 1, "native FDM: expected one marker");
    Assert(result.Failures.Count == 0, "native FDM: matching SQL and reports must reconcile");
  }


  private static void ForeignDialectBleedClassification()
  {
    // Defense-in-depth matrix previously driven through the product --check-bleed CLI.
    // Call the production classifier directly; do not reintroduce a product test hook.
    (string Code, string PlatformId, bool ExpectBleed)[] cases =
    [
      ("SSC-EWI-INF0001", "yxmd", true),
      ("SSC-EWI-SSIS0007", "yxmd", true),
      ("SSC-EWI-0013", "yxmd", false),
      ("SSC-EWI-INF0001", "xml", false),
      ("SSC-EWI-SSIS0007", "dtsx", false),
      ("SSC-EWI-INF0001", "dtsx", true),
      ("SSC-EWI-SSIS0007", "xml", true),
    ];

    foreach (var (code, platformId, expectBleed) in cases)
    {
      var actual = ProducerReports.IsForeignDialectBleed(code, platformId);
      Assert(actual == expectBleed,
        $"IsForeignDialectBleed({code}, {platformId}) expected {expectBleed}, got {actual}");
    }
  }

  private static (int Checked, List<string> Failures) Reconcile(
    string sql,
    IReadOnlyDictionary<string, IReadOnlyList<(IssueName IssueName, object[] Args)>> issues,
    HashSet<(string FullName, string Code)> reported,
    string platformId)
  {
    var element = new UnsupportedTransformation { Id = NodeId, Name = "Probe" };
    var pipeline = new DagPipeline<Transformation>
    {
      Nodes = [new DagNode<Transformation>(NodeId, "Intermediate", element)],
      Edges = [],
    };

    return ProducerReports.ReconcileMarkersAndReports(
      pipeline,
      new Dictionary<string, string>(StringComparer.Ordinal) { [NodeId] = Stem },
      [Stem],
      new Dictionary<string, string>(StringComparer.Ordinal) { [Stem] = sql },
      issues,
      reported,
      new EwiInformationService(new EwiModelReader(NullLogger.Instance)),
      platformId);
  }

  private static IReadOnlyDictionary<string, IReadOnlyList<(IssueName, object[])>> IssuesFor(IssueName issue)
    => new Dictionary<string, IReadOnlyList<(IssueName, object[])>>(StringComparer.Ordinal)
    {
      [NodeId] = new List<(IssueName, object[])> { (issue, Array.Empty<object>()) },
    };

  private static void Assert(bool condition, string message)
  {
    if (!condition)
    {
      throw new InvalidOperationException(message);
    }
  }
}
