param(
    [ValidateSet('x86_64-pc-windows-msvc')]
    [string]$Target = 'x86_64-pc-windows-msvc'
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path $PSScriptRoot -Parent
$Plugin = if ($env:DBT_QUALITY_PLUGIN_DIR) { $env:DBT_QUALITY_PLUGIN_DIR } else { Join-Path $Root 'plugin' }
$Toolchain = if ($env:RUSTUP_TOOLCHAIN) { $env:RUSTUP_TOOLCHAIN } else { '1.96' }
& cargo "+$Toolchain" build --locked --release --manifest-path "$Root/rust/Cargo.toml" --target $Target -p dbt-quality-cli
if ($LASTEXITCODE -ne 0) { throw 'Cargo build failed' }
$Destination = Join-Path $Plugin "bin/$Target"
New-Item -ItemType Directory -Force $Destination | Out-Null
Copy-Item "$Root/rust/target/$Target/release/dbt-quality.exe" "$Destination/dbt-quality.exe"
Write-Output "Built $Target in $Destination"
