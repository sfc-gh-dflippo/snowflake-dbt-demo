:; exit 0
@echo off
@powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix-dbt-quality-launcher.ps1" 1>&2
@exit /b 0
