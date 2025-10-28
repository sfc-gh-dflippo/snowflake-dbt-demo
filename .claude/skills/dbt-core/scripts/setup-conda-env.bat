@echo off
REM Create conda environment with dbt non-interactively
REM For AI agent execution

setlocal enabledelayedexpansion

echo === Setting up dbt with conda ===
echo.

REM Check if dbt-conda-env.yml exists
if not exist "dbt-conda-env.yml" (
    echo - Error: dbt-conda-env.yml not found in current directory
    echo   Please navigate to the .claude\skills\dbt-core\ directory
    exit /b 1
)

REM Check if environment already exists
conda env list | findstr /b "dbt " >nul
if %errorlevel% equ 0 (
    echo -^> conda environment 'dbt' already exists, updating...
    conda env update -f dbt-conda-env.yml
    echo + Environment updated
) else (
    echo -^> Creating conda environment from dbt-conda-env.yml...
    conda env create -f dbt-conda-env.yml
    echo + Environment created
)

echo.
echo === Setup Complete ===
echo.
echo To activate the environment:
echo   conda activate dbt
echo.
echo To verify installation:
echo   dbt --version
echo.
echo To deactivate when done:
echo   conda deactivate

