param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('x86_64-unknown-linux-musl', 'aarch64-unknown-linux-musl', 'x86_64-apple-darwin', 'aarch64-apple-darwin', 'x86_64-pc-windows-msvc')]
    [string]$Target,
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path $PSScriptRoot -Parent
$Plugin = if ($env:DBT_QUALITY_PLUGIN_DIR) { $env:DBT_QUALITY_PLUGIN_DIR } else { Join-Path $Root 'plugin' }
$WindowsTarget = $Target.EndsWith('-windows-msvc')
$Suffix = if ($WindowsTarget) { '.exe' } else { '' }
$Output = [System.IO.Path]::GetFullPath($OutputDirectory)
$Name = "dbt-quality-$Target"
$Package = Join-Path $Output $Name
if (Test-Path $Package) { throw "Package directory already exists: $Package" }
New-Item -ItemType Directory -Force "$Package/bin" | Out-Null
# README links point at plugin/ here and at ../dbt-quality/ in the snowflake-dbt-demo copy.
$Readme = [System.IO.File]::ReadAllText("$Root/README.md").Replace('](plugin/skills/', '](skills/').Replace('](../dbt-quality/skills/', '](skills/').Replace('](vendor/DBT_PIN.md)', '](DBT_PIN.md)')
[System.IO.File]::WriteAllText("$Package/README.md", $Readme)
Copy-Item "$Root/vendor/DBT_PIN.md" "$Package/DBT_PIN.md"
Copy-Item "$Plugin/skills" "$Package/skills" -Recurse
New-Item -ItemType Directory "$Package/licenses" | Out-Null
Copy-Item "$Root/vendor/dbt/LICENSE" "$Package/licenses/dbt-LICENSE"
Copy-Item "$Root/vendor/dbt/crates/dbt-jinja/LICENSE" "$Package/licenses/jinja-LICENSE"
foreach ($ManifestDirectory in @('.cortex-plugin', '.claude-plugin')) {
    New-Item -ItemType Directory "$Package/$ManifestDirectory" | Out-Null
    $Manifest = Get-Content "$Plugin/$ManifestDirectory/plugin.json" -Raw | ConvertFrom-Json
    $Manifest.mcpServers.'dbt-quality'.command = '${CLAUDE_PLUGIN_ROOT}/bin/dbt-quality' + $Suffix
    $Manifest | ConvertTo-Json -Depth 20 | Set-Content "$Package/$ManifestDirectory/plugin.json" -Encoding utf8NoBOM
}
Copy-Item "$Plugin/bin/$Target/dbt-quality$Suffix" "$Package/bin/dbt-quality$Suffix"
$Checksums = foreach ($File in Get-ChildItem "$Package/bin" -File | Sort-Object Name) {
    '{0}  bin/{1}' -f (Get-FileHash $File.FullName -Algorithm SHA256).Hash.ToLowerInvariant(), $File.Name
}
# Checksum files use LF on every platform, so `sha256sum -c` and `shasum -c` read them.
function Write-LfText([string]$Path, [string[]]$Lines) {
    [IO.File]::WriteAllText($Path, (($Lines -join "`n") + "`n"), [Text.UTF8Encoding]::new($false))
}
Write-LfText "$Package/SHA256SUMS" $Checksums
if ($WindowsTarget) {
    $Archive = "$Output/$Name.zip"
    Compress-Archive -Path $Package -DestinationPath $Archive
} else {
    & chmod +x "$Package/bin/dbt-quality"
    if ($LASTEXITCODE -ne 0) { throw 'Setting executable permissions failed' }
    $Archive = "$Output/$Name.tar.gz"
    & tar -czf $Archive -C $Output $Name
    if ($LASTEXITCODE -ne 0) { throw 'Creating archive failed' }
}
Write-LfText "$Archive.sha256" @('{0}  {1}' -f (Get-FileHash $Archive -Algorithm SHA256).Hash.ToLowerInvariant(), (Split-Path $Archive -Leaf))
Write-Output "Packaged $Archive"
