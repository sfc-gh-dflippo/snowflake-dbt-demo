@echo off
REM Install Miniforge (conda-forge) non-interactively
REM For AI agent execution

setlocal enabledelayedexpansion

echo === Installing Miniforge ===
echo.
echo Miniforge provides conda with conda-forge as the default channel.
echo Source: https://github.com/conda-forge/miniforge
echo.

set INSTALLER_URL=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe

echo -^> Downloading Miniforge installer...
curl -L -o Miniforge3-Windows-x86_64.exe %INSTALLER_URL%

echo -^> Running installer...
start /wait "" Miniforge3-Windows-x86_64.exe /InstallationType=JustMe /AddToPath=1 /RegisterPython=0 /S /D=%USERPROFILE%\miniforge3

echo -^> Initializing conda for all shells...
call %USERPROFILE%\miniforge3\Scripts\conda.exe init --all

REM Clean up
del Miniforge3-Windows-x86_64.exe

echo.
echo + Miniforge installed successfully!
echo.
echo Installation directory: %USERPROFILE%\miniforge3
echo Conda has been initialized for all shells ^(PowerShell, cmd, bash, etc.^)
echo.
echo IMPORTANT: Restart your terminal ^(or start a new terminal session^)
echo to activate conda, then run 'check-environment.bat' to verify.

