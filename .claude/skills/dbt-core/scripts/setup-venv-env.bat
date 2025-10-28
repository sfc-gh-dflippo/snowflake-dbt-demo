@echo off
REM Create Python venv environment with dbt non-interactively
REM For AI agent execution

setlocal enabledelayedexpansion

echo === Setting up dbt with Python venv ===
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo - Error: requirements.txt not found in current directory
    echo   Please navigate to the .claude\skills\dbt-core\ directory
    exit /b 1
)

REM Check if venv module is available
python -m venv --help >nul 2>nul
if %errorlevel% neq 0 (
    echo -^> venv module not found, installing virtualenv...
    pip install virtualenv
)

REM Create virtual environment
if exist ".venv" (
    echo -^> Virtual environment .venv already exists, recreating...
    rmdir /s /q .venv
)

echo -^> Creating virtual environment...
python -m venv .venv

REM Activate and install dependencies
echo -^> Installing dependencies from requirements.txt...
call .venv\Scripts\activate.bat
python -m pip install -U pip
pip install -U -r requirements.txt

echo.
echo === Setup Complete ===
echo.
echo To activate the environment:
echo   .venv\Scripts\activate
echo.
echo To verify installation:
echo   dbt --version
echo.
echo To deactivate when done:
echo   deactivate

