param(
    [Parameter(Mandatory = $true)][string]$PackageDirectory,
    [Parameter(Mandatory = $true)][string]$ScratchDirectory
)
$ErrorActionPreference = 'Stop'
$Package = (Resolve-Path $PackageDirectory).Path
$Scratch = [System.IO.Path]::GetFullPath($ScratchDirectory)
$Suffix = if ($IsWindows) { '.exe' } else { '' }
$Cli = Join-Path $Package "bin/dbt-quality$Suffix"
foreach ($Directory in @('.cortex-plugin', '.claude-plugin')) {
    $Manifest = Get-Content "$Package/$Directory/plugin.json" -Raw | ConvertFrom-Json
    $Command = $Manifest.mcpServers.'dbt-quality'.command.Replace('${CLAUDE_PLUGIN_ROOT}', $Package)
    if (-not (Test-Path $Command -PathType Leaf)) { throw "Packaged MCP command missing: $Command" }
    if ((@($Manifest.mcpServers.'dbt-quality'.args) -join ' ') -ne 'mcp') { throw "Packaged MCP args are not 'mcp' in $Directory" }
}
$Readme = [System.IO.File]::ReadAllText("$Package/README.md")
foreach ($Document in @('skills/dbt-audit/SKILL.md', 'skills/dbt-audit/references/rule-catalog.md', 'DBT_PIN.md')) {
    if (-not (Test-Path "$Package/$Document" -PathType Leaf)) { throw "Packaged documentation missing: $Document" }
    if (-not $Readme.Contains("]($Document)")) { throw "Packaged README link missing: $Document" }
}
New-Item -ItemType Directory -Force "$Scratch/project/models" | Out-Null
$Project = Join-Path $Scratch 'project'
'name: smoke_project', "version: '1.0'", 'profile: smoke_project' | Set-Content "$Project/dbt_project.yml" -Encoding utf8NoBOM
"select a.x from a, b where a.id = b.id`r`n" | Set-Content "$Project/models/a.sql" -Encoding utf8NoBOM -NoNewline
$Original = [System.IO.File]::ReadAllBytes("$Project/models/a.sql")
foreach ($Line in Get-Content "$Package/SHA256SUMS") {
    $Expected, $Relative = $Line -split '  ', 2
    $Actual = (Get-FileHash (Join-Path $Package $Relative) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Actual -ne $Expected) { throw "Checksum mismatch: $Relative" }
}
& $Cli --version
if ($LASTEXITCODE -ne 0) { throw 'CLI version failed' }
$Report = & $Cli audit $Project --stdout --quiet
if ($LASTEXITCODE -ne 0) { throw 'CLI audit failed' }
if (-not (($Report | ConvertFrom-Json).suggestions.rule_id -contains 'SSC-EWI-DBTSQL0007')) { throw 'Expected comma-join finding missing' }
$Lint = & $Cli lint $Project --format json
if ($LASTEXITCODE -ne 0) { throw 'CLI lint failed' }
if (-not ($Lint | ConvertFrom-Json)) { throw 'Empty lint output' }
& $Cli setup-tasks $Project
if ($LASTEXITCODE -ne 0) { throw 'Editor task generation failed' }
& git -C $Project init -q
if ($LASTEXITCODE -ne 0) { throw 'Git init failed' }
& git -C $Project add .
if ($LASTEXITCODE -ne 0) { throw 'Git add failed' }
& git -C $Project -c user.name=smoke -c user.email=smoke@example.invalid -c commit.gpgsign=false commit -q -m fixture
if ($LASTEXITCODE -ne 0) { throw 'Fixture commit failed' }
$Start = [System.Diagnostics.ProcessStartInfo]::new($Cli)
$Start.ArgumentList.Add('mcp')
$Start.UseShellExecute = $false
$Start.RedirectStandardInput = $true
$Start.RedirectStandardOutput = $true
$Process = [System.Diagnostics.Process]::Start($Start)
$Requests = @(
    @{jsonrpc='2.0'; id=1; method='initialize'; params=@{protocolVersion='2025-06-18'; capabilities=@{}; clientInfo=@{name='artifact-smoke'; version='1'}}},
    @{jsonrpc='2.0'; method='notifications/initialized'},
    @{jsonrpc='2.0'; id=2; method='tools/list'},
    @{jsonrpc='2.0'; id=3; method='tools/call'; params=@{name='version'; arguments=@{}}},
    @{jsonrpc='2.0'; id=4; method='tools/call'; params=@{name='report'; arguments=@{path=$Project; out_dir="$Scratch/reports"; html=$false}}},
    @{jsonrpc='2.0'; id=5; method='tools/call'; params=@{name='annotate'; arguments=@{path=$Project; dry_run=$true; rule_ids=@('SSC-EWI-DBTSQL0007')}}},
    @{jsonrpc='2.0'; id=6; method='tools/call'; params=@{name='annotate'; arguments=@{path=$Project; dry_run=$false; rule_ids=@('SSC-EWI-DBTSQL0007')}}}
)
$OutputTask = $Process.StandardOutput.ReadToEndAsync()
foreach ($Request in $Requests) { $Process.StandardInput.WriteLine(($Request | ConvertTo-Json -Compress -Depth 10)) }
$Process.StandardInput.Close()
if (-not $Process.WaitForExit(60000)) { $Process.Kill(); throw 'MCP smoke timed out' }
if ($Process.ExitCode -ne 0) { throw 'MCP process failed' }
$Replies = @{}
foreach ($Line in $OutputTask.GetAwaiter().GetResult() -split "`n") {
    if ($Line.Trim()) { $Reply = $Line | ConvertFrom-Json; $Replies[[int]$Reply.id] = $Reply }
}
if ($Replies.Count -ne 6) { throw 'Unexpected MCP reply count' }
if ($Replies[2].result.tools.Count -ne 6) { throw 'Unexpected MCP tool count' }
foreach ($Id in 3..6) { if ($Replies[$Id].error -or $Replies[$Id].result.isError) { throw "MCP tool $Id failed" } }
if ($Replies[3].result.structuredContent.rules -ne 124) { throw 'Unexpected rule count' }
if ($Replies[5].result.structuredContent.written -or -not $Replies[6].result.structuredContent.written) { throw 'Annotation dry-run/write contract failed' }
if (-not ([System.IO.File]::ReadAllText("$Project/models/a.sql").Contains('SSC-EWI-DBTSQL0007'))) { throw 'Annotation did not write marker' }
& $Cli annotate $Project --remove --write --allow-dirty
if ($LASTEXITCODE -ne 0) { throw 'Marker removal failed' }
if ([Convert]::ToBase64String([System.IO.File]::ReadAllBytes("$Project/models/a.sql")) -ne [Convert]::ToBase64String($Original)) { throw 'Annotation round-trip changed input bytes' }
Write-Output 'Packaged CLI, editor tasks, MCP, and annotation round-trip passed.'
