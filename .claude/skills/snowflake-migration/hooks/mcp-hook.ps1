# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Windows locator for migration-mcp-server (sibling of scai.exe). See mcp-hook.sh.
# Caches the resolved path at <cwd>/.scai/tmp/mcp-server-bin.

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name
)

# First session (and any host without scai on PATH): do not fail the Cortex hook.
function Skip { exit 0 }

$Cache = Join-Path (Get-Location) ".scai/tmp/mcp-server-bin"

function ReadCache {
    if (-not (Test-Path -LiteralPath $Cache)) { return $null }
    $path = (Get-Content -LiteralPath $Cache -TotalCount 1 -ErrorAction SilentlyContinue)
    if (-not $path) { return $null }
    $path = $path.Trim()
    if ($path -and (Test-Path -LiteralPath $path)) { return $path }
    return $null
}

function WriteCache([string]$Bin) {
    $dir = Split-Path -Parent $Cache
    New-Item -ItemType Directory -Path $dir -Force -ErrorAction SilentlyContinue | Out-Null
    Set-Content -LiteralPath $Cache -Value $Bin -ErrorAction SilentlyContinue
}

function SiblingOf([string]$Exe) {
    $dir = Split-Path -Parent $Exe
    foreach ($name in @("migration-mcp-server.exe", "migration-mcp-server")) {
        $candidate = Join-Path $dir $name
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    return $null
}

function BinFromShim([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $text = Get-Content -LiteralPath $Path -Raw -ErrorAction SilentlyContinue
    if (-not $text) { return $null }
    if ($text -match 'export MIGRATION_MCP_SERVER_BIN="([^"]+)"') {
        if (Test-Path -LiteralPath $Matches[1]) { return $Matches[1] }
    }
    if ($text -match 'exec "([^"]+)"') {
        return SiblingOf $Matches[1]
    }
    # install.ps1 shim:  "C:\...\orchestrator\scai.exe" %*
    if ($text -match '"([^"]*scai\.exe)"') {
        return SiblingOf $Matches[1]
    }
    return $null
}

$bin = $null
if ($env:MIGRATION_MCP_SERVER_BIN -and (Test-Path -LiteralPath $env:MIGRATION_MCP_SERVER_BIN)) {
    $bin = $env:MIGRATION_MCP_SERVER_BIN
} else {
    $bin = ReadCache
    if (-not $bin) {
        $scai = $env:SCAI_CLI
        if (-not $scai) {
            $cmd = Get-Command scai -ErrorAction SilentlyContinue
            if (-not $cmd) { Skip }
            $scai = $cmd.Source
        }
        if (-not $scai -or -not (Test-Path -LiteralPath $scai)) { Skip }
        $bin = BinFromShim $scai
        if (-not $bin) {
            $target = $scai
            $item = Get-Item -LiteralPath $scai -ErrorAction SilentlyContinue
            if ($item -and $item.LinkType) {
                $target = $item.Target
                if ($target -and -not [System.IO.Path]::IsPathRooted($target)) {
                    $target = Join-Path (Split-Path -Parent $scai) $target
                }
            }
            $bin = SiblingOf $target
        }
        if (-not $bin) { Skip }
    }
}

WriteCache $bin
& $bin hook $Name
exit $LASTEXITCODE
