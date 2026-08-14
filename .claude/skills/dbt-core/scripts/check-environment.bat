@echo off
REM Check environment for dbt Fusion (dbt 2.0) prerequisites
REM Outputs structured information for AI agent decision-making

setlocal enabledelayedexpansion

echo === Environment Check ===
echo.

REM Check for dbt on PATH
where dbt >nul 2>nul
if %errorlevel% equ 0 (
    echo + dbt: INSTALLED
    set DBT_INSTALLED=true

    REM Show detailed dbt version info
    echo.
    echo -^> dbt version details:
    dbt --version 2^>^&1

    REM Confirm this is the Fusion engine (dbt 2.0.x)
    dbt --version 2^>^&1 | findstr /i "fusion 2.0." >nul 2>nul
    if !errorlevel! equ 0 (
        echo.
        echo + dbt Fusion engine ^(2.0.x^) detected
        set DBT_FUSION=true
    ) else (
        echo.
        echo ! dbt is installed but does not appear to be the Fusion engine ^(2.0.x^)
        echo   Install/update with: install-dbt.ps1   ^(or: dbt system update^)
        set DBT_FUSION=false
    )

    REM Test basic dbt command
    echo.
    echo -^> Testing dbt command...
    dbt --help >nul 2^>^&1
    if !errorlevel! equ 0 (
        echo + dbt command works correctly
    ) else (
        echo - dbt command failed
    )
) else (
    echo - dbt: NOT INSTALLED
    set DBT_INSTALLED=false
    set DBT_FUSION=false
)

echo.

REM Check for snowflake-cli (separate tool, optional but recommended)
where snow >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('snow --version 2^>^&1') do set SNOW_VERSION=%%v
    echo + snowflake-cli: INSTALLED ^(!SNOW_VERSION!^)
    set SNOW_INSTALLED=true
) else (
    echo - snowflake-cli: NOT INSTALLED ^(optional: set UV_SYSTEM_CERTS=true ^&^& uv tool install snowflake-cli^)
    set SNOW_INSTALLED=false
)

echo.

REM Check for curl (needed for the Fusion installer)
where curl >nul 2>nul
if %errorlevel% equ 0 (
    echo + curl: INSTALLED
    set CURL_INSTALLED=true
) else (
    echo - curl: NOT INSTALLED ^(required for the Fusion installer^)
    set CURL_INSTALLED=false
)

echo.
echo === Recommendations ===
echo.

if "%DBT_INSTALLED%"=="true" (
    if "%DBT_FUSION%"=="true" (
        echo + dbt Fusion is installed. Verify with: dbt --version
        echo   To update later, run: dbt system update
    ) else (
        echo -^> dbt is installed but not the Fusion engine ^(2.0.x^).
        echo   Run 'install-dbt.ps1' to install Fusion, or 'dbt system update' to update.
    )
) else (
    echo -^> RECOMMENDED: Run 'install-dbt.ps1' to install the dbt Fusion engine ^(2.0.x^)
    echo   ^(installs to %%USERPROFILE%%\.local\bin, no admin required^)
)

echo.
echo === Summary ===
echo dbt_installed=%DBT_INSTALLED%
echo dbt_fusion=%DBT_FUSION%
echo snowflake_cli_installed=%SNOW_INSTALLED%
echo curl_installed=%CURL_INSTALLED%
