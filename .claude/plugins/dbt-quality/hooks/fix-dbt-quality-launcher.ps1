# SessionStart step. Windows only; it does nothing elsewhere.
# MCP clients start bin/dbt-quality with cross-spawn and shell:false.
# On Windows, cross-spawn first accepts only a file with a PATHEXT extension, so it runs bin/dbt-quality.cmd.
# If no .cmd exists, it falls back to the extensionless bin/dbt-quality, reads its "#!/bin/sh" line,
# and runs sh. That fails with ENOENT, or with "unsupported platform" under Git Bash.
# Remove the sh launcher when bin/dbt-quality.cmd exists next to it.
# This keeps any client that tries the exact path first from picking the sh launcher.
# This step is idempotent, prints nothing to stdout, and always exits 0.
param([string]$PluginRoot = (Split-Path -Parent $PSScriptRoot))

if ($env:OS -ne 'Windows_NT') { exit 0 }
$launcher = Join-Path $PluginRoot 'bin/dbt-quality'
try {
    if ((Test-Path -LiteralPath "$launcher.cmd" -PathType Leaf) -and (Test-Path -LiteralPath $launcher -PathType Leaf)) {
        Remove-Item -LiteralPath $launcher -Force -ErrorAction Stop
    }
} catch {
    [Console]::Error.WriteLine("dbt-quality: cannot remove $launcher : $($_.Exception.Message)")
}
exit 0
