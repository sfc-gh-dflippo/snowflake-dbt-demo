@echo off
REM Install Miniconda non-interactively
REM For AI agent execution

setlocal enabledelayedexpansion

echo === Installing Miniconda ===
echo.
echo Miniconda provides minimal conda with the defaults channel.
echo Source: https://docs.anaconda.com/miniconda/
echo.

set INSTALLER_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

echo -^> Downloading Miniconda installer...
curl -L -o Miniconda3-Windows-x86_64.exe %INSTALLER_URL%

echo -^> Running installer...
start /wait "" Miniconda3-Windows-x86_64.exe /InstallationType=JustMe /AddToPath=1 /RegisterPython=0 /S /D=%USERPROFILE%\miniconda3

echo -^> Initializing conda for all shells...
call %USERPROFILE%\miniconda3\Scripts\conda.exe init --all

REM Clean up
del Miniconda3-Windows-x86_64.exe

echo.
echo + Miniconda installed successfully!
echo.
echo Installation directory: %USERPROFILE%\miniconda3
echo Conda has been initialized for all shells ^(PowerShell, cmd, bash, etc.^)
echo.
echo IMPORTANT: Restart your terminal ^(or start a new terminal session^)
echo to activate conda, then run 'check-environment.bat' to verify.
