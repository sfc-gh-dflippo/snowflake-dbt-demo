// A logger that CAPTURES errors instead of discarding them.
//
// WHY THIS IS NOT NullLogger. TransformationUnitTranslator wraps each element's translation in a
// try/catch and, on failure, substitutes a NOT-SUPPORTED placeholder via
// GenerateUnsupportedElementConversion. The placeholder IS renderable — so a node can come back with a
// perfectly good-looking artifact and have actually failed. The only trace is an ILogger.LogError call.
//
// With NullLogger that trace is thrown away, and the emitter would report a substituted node as a
// success. That is the "reports success while accomplishing nothing" shape this project has found
// sixteen times; using NullLogger here would have been the seventeenth.
namespace AiFirst.Producer;

using System;
using System.Collections.Generic;
using Microsoft.Extensions.Logging;

internal sealed class CapturingLogger : ILogger
{
  internal List<string> Errors { get; } = [];

  public IDisposable BeginScope<TState>(TState state)
    where TState : notnull => NullScope.Instance;

  public bool IsEnabled(LogLevel logLevel) => true;

  public void Log<TState>(
    LogLevel logLevel,
    EventId eventId,
    TState state,
    Exception? exception,
    Func<TState, Exception?, string> formatter)
  {
    if (logLevel >= LogLevel.Error)
    {
      var text = formatter(state, exception);
      this.Errors.Add(exception is null ? text : $"{text} :: {exception.GetType().Name}: {exception.Message}");
    }
  }

  private sealed class NullScope : IDisposable
  {
    internal static readonly NullScope Instance = new();

    public void Dispose()
    {
    }
  }
}
