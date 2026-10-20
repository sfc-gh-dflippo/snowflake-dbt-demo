param(
    [Parameter(Mandatory = $true)][string]$ArchiveDirectory,
    [Parameter(Mandatory = $true)][string]$Target,
    [Parameter(Mandatory = $true)][string]$ScratchDirectory
)
# Tests the plugin launchers against a packaged archive served from a file:// URL.
# The launcher copies have no bin/<target>/ build, so they must download, check, and cache.
$ErrorActionPreference = 'Stop'
$Root = Split-Path $PSScriptRoot -Parent
$Plugin = if ($env:DBT_QUALITY_PLUGIN_DIR) { $env:DBT_QUALITY_PLUGIN_DIR } else { Join-Path $Root 'plugin' }
$Version = (Select-String -Path "$Root/rust/Cargo.toml" -Pattern '^version = "(.+)"' | Select-Object -First 1).Matches[0].Groups[1].Value
foreach ($Launcher in @('dbt-quality', 'dbt-quality.cmd')) {
    $Text = [System.IO.File]::ReadAllText("$Plugin/bin/$Launcher")
    if ($Text -notmatch "(?m)VERSION=$([regex]::Escape($Version))(`"|\r?$)") { throw "bin/$Launcher VERSION is not the Cargo version $Version" }
}

$Scratch = [System.IO.Path]::GetFullPath($ScratchDirectory)
if (Test-Path $Scratch) { Remove-Item -Recurse -Force $Scratch }
$Bin = (New-Item -ItemType Directory -Force "$Scratch/plugin with spaces/bin").FullName
Copy-Item "$Plugin/bin/dbt-quality", "$Plugin/bin/dbt-quality.cmd" $Bin
if (-not $IsWindows) {
    & chmod +x "$Bin/dbt-quality"
    if ($LASTEXITCODE -ne 0) { throw 'chmod failed' }
}
$Archive = if ($IsWindows) { "dbt-quality-$Target.zip" } else { "dbt-quality-$Target.tar.gz" }
$Download = Join-Path $Scratch 'dl'
function Publish-Release([string]$Checksum) {
    $Release = (New-Item -ItemType Directory -Force "$Download/dbt-quality-v$Version").FullName
    Copy-Item "$ArchiveDirectory/$Archive" $Release
    if ($Checksum) {
        [System.IO.File]::WriteAllText("$Release/$Archive.sha256", "$Checksum  $Archive`n")
    } else {
        Copy-Item "$ArchiveDirectory/$Archive.sha256" $Release
    }
}
$env:DBT_QUALITY_DOWNLOAD_BASE = [System.Uri]::new($Download, [System.UriKind]::Absolute).AbsoluteUri
$Cache = Join-Path $Scratch 'cache dir'
if ($IsWindows) { $env:LOCALAPPDATA = $Cache } else { $env:XDG_CACHE_HOME = $Cache }
$Cached = if ($IsWindows) { "$Cache/dbt-quality/$Version/$Target/dbt-quality.exe" } else { "$Cache/dbt-quality/$Version/$Target/dbt-quality" }
$Entry = if ($IsWindows) { "$Bin/dbt-quality.cmd" } else { "$Bin/dbt-quality" }
function Invoke-Launcher { $Output = & $Entry --version 2>&1; return @{ Code = $LASTEXITCODE; Text = ($Output -join "`n") } }

Publish-Release
$First = Invoke-Launcher
if ($First.Code -ne 0 -or $First.Text -notmatch "dbt-quality $([regex]::Escape($Version))") { throw "First run failed: $($First.Text)" }
if (-not (Test-Path $Cached -PathType Leaf)) { throw "Launcher did not cache $Cached" }

Remove-Item -Recurse -Force $Download
$Second = Invoke-Launcher
if ($Second.Code -ne 0) { throw "Cached run failed: $($Second.Text)" }

# MCP clients start the server with cross-spawn and the extensionless manifest path.
# On Windows, cross-spawn resolves bin/dbt-quality to bin/dbt-quality.cmd through PATHEXT.
$NodeModules = Join-Path $Scratch 'node'
& npm install --prefix $NodeModules --no-audit --no-fund --silent cross-spawn@7.0.6
if ($LASTEXITCODE -ne 0) { throw 'npm install cross-spawn failed' }
$Init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"launcher-smoke","version":"1"}}}'
$Script = 'const spawn = require(process.argv[1]); const r = spawn.sync(process.argv[2], ["mcp"], { input: process.argv[3] + "\n", encoding: "utf8", shell: false }); process.stdout.write(r.stdout || ""); process.stderr.write(String(r.error || r.stderr || "")); process.exit(r.status ?? 1);'
$Reply = & node -e $Script "$NodeModules/node_modules/cross-spawn" "$Bin/dbt-quality" $Init
if ($LASTEXITCODE -ne 0 -or -not ($Reply -match '"serverInfo"')) { throw "MCP through cross-spawn failed: $Reply" }

Remove-Item -Recurse -Force $Cache
Publish-Release -Checksum ('0' * 64)
$Bad = Invoke-Launcher
if ($Bad.Code -eq 0) { throw 'Launcher ran a binary whose checksum did not match' }
if (Test-Path $Cached) { throw 'Launcher cached a binary whose checksum did not match' }
Write-Output 'Launcher download, cache, cross-spawn MCP start, and checksum refusal passed.'
# The refusal check leaves a non-zero $LASTEXITCODE, which a pwsh CI step would report as failure.
exit 0
