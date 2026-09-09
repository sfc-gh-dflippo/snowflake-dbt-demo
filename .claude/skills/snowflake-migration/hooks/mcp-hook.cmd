:; exec sh "$(cd "$(dirname "$0")" && pwd)/mcp-hook.sh" "$@"
@echo off
@powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0mcp-hook.ps1" %*
