@echo off
rem Launcher: runs dbt-quality on Windows. It follows the same steps as bin/dbt-quality:
rem %DBT_QUALITY_EXE%, then a local build in bin\<target>\, then a cached download in
rem %LOCALAPPDATA%\dbt-quality\<version>\<target>\, else download, check the SHA-256, and cache.
rem MCP clients reach this file through cross-spawn: it resolves bin/dbt-quality with PATHEXT
rem and runs .cmd files through cmd.exe. Keep VERSION equal to the Cargo version.
rem The integrity ceiling is described in bin/dbt-quality.
setlocal
set "VERSION=0.3.1-pr9958"
rem Detect ARM64 the same way as hooks\install-dependencies.ps1. An x64 process on ARM64 Windows
rem reports AMD64 in PROCESSOR_ARCHITECTURE, so PROCESSOR_IDENTIFIER is checked too.
set "TARGET=x86_64-pc-windows-msvc"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "TARGET=aarch64-pc-windows-msvc"
if /i "%PROCESSOR_ARCHITEW6432%"=="ARM64" set "TARGET=aarch64-pc-windows-msvc"
echo %PROCESSOR_IDENTIFIER% | findstr /i "ARM AArch64" >nul && set "TARGET=aarch64-pc-windows-msvc"
set "HERE=%~dp0"
set "DBT_QUALITY_BIN=%HERE%dbt-quality.cmd"
set "WORK="
if defined DBT_QUALITY_EXE (
  set "EXE=%DBT_QUALITY_EXE%"
  goto run
)
if exist "%HERE%%TARGET%\dbt-quality.exe" (
  set "EXE=%HERE%%TARGET%\dbt-quality.exe"
  goto run
)
set "CACHE=%LOCALAPPDATA%\dbt-quality\%VERSION%\%TARGET%"
set "EXE=%CACHE%\dbt-quality.exe"
if exist "%EXE%" goto run

if not defined DBT_QUALITY_DOWNLOAD_BASE set "DBT_QUALITY_DOWNLOAD_BASE=https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/releases/download"
set "ARCHIVE=dbt-quality-%TARGET%.zip"
set "URL=%DBT_QUALITY_DOWNLOAD_BASE%/dbt-quality-v%VERSION%/%ARCHIVE%"
if not exist "%CACHE%" mkdir "%CACHE%" || goto fail
rem The work directory is in the cache directory, so the final move is a rename.
set "WORK=%CACHE%\.download-%RANDOM%%RANDOM%"
mkdir "%WORK%" || goto fail
rem MCP clients wait about 30 s for a server to start. Both downloads together stay under that.
curl.exe -fsSL --max-time 5 -o "%WORK%\%ARCHIVE%.sha256" "%URL%.sha256" || goto fail
curl.exe -fsSL --max-time 20 -o "%WORK%\%ARCHIVE%" "%URL%" || goto fail
set "EXPECTED="
for /f "usebackq tokens=1" %%h in ("%WORK%\%ARCHIVE%.sha256") do if not defined EXPECTED set "EXPECTED=%%h"
set "ACTUAL="
for /f "skip=1 delims=" %%h in ('certutil -hashfile "%WORK%\%ARCHIVE%" SHA256') do if not defined ACTUAL set "ACTUAL=%%h"
if not defined EXPECTED goto fail
if not defined ACTUAL goto fail
rem Older certutil versions print the hash with spaces between bytes.
set "ACTUAL=%ACTUAL: =%"
if /i not "%ACTUAL%"=="%EXPECTED%" goto fail
tar.exe -xf "%WORK%\%ARCHIVE%" -C "%WORK%" || goto fail
move /y "%WORK%\dbt-quality-%TARGET%\bin\dbt-quality.exe" "%EXE%" >nul || goto fail
rmdir /s /q "%WORK%"

:run
"%EXE%" %*
exit /b %errorlevel%

:fail
echo dbt-quality: cannot download and verify %URL% 1>&2
echo dbt-quality: download it and its .sha256 file, or build with scripts\build-plugin.ps1 1>&2
if defined WORK if exist "%WORK%" rmdir /s /q "%WORK%"
exit /b 1
