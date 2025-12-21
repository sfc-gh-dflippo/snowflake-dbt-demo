@echo off
REM Check environment for dbt setup prerequisites
REM Outputs structured information for AI agent decision-making

setlocal enabledelayedexpansion

echo === Environment Check ===
echo.

REM Check for conda first
where conda >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('conda --version 2^>^&1') do set CONDA_VERSION=%%v
    echo + conda: INSTALLED ^(!CONDA_VERSION!^)
    set CONDA_INSTALLED=true

    echo.
    echo -^> Checking conda environments for dbt...

    REM List all conda environments and check each for dbt
    set DBT_SF_ENV_FOUND=
    set FIRST_DBT_SF_ENV=
    set DBT_ENV_FOUND=
    set FIRST_DBT_ENV=

    for /f "skip=2 tokens=1" %%e in ('conda env list 2^>nul') do (
        if not "%%e"=="base" (
            REM Check if this environment has dbt-core
            conda list -n %%e 2^>nul | findstr /b "dbt-core" >nul 2>nul
            if !errorlevel! equ 0 (
                for /f "tokens=2" %%v in ('conda list -n %%e 2^>nul ^| findstr /b "dbt-core"') do (
                    set DBT_CORE_VER=%%v

                    REM Check for dbt-snowflake adapter
                    conda list -n %%e 2^>nul | findstr /b "dbt-snowflake" >nul 2>nul
                    if !errorlevel! equ 0 (
                        for /f "tokens=2" %%s in ('conda list -n %%e 2^>nul ^| findstr /b "dbt-snowflake"') do (
                            echo   + '%%e' has dbt-core !DBT_CORE_VER! + dbt-snowflake %%s
                            if "%%e"=="dbt" (
                                set DBT_SF_ENV_FOUND=dbt
                            ) else if not defined FIRST_DBT_SF_ENV (
                                set FIRST_DBT_SF_ENV=%%e
                            )
                        )
                    ) else (
                        echo   o '%%e' has dbt-core !DBT_CORE_VER! ^(no dbt-snowflake^)
                        if "%%e"=="dbt" (
                            set DBT_ENV_FOUND=dbt
                        ) else if not defined FIRST_DBT_ENV (
                            set FIRST_DBT_ENV=%%e
                        )
                    )
                )
            )
        )
    )

    REM Try to activate an environment with dbt (prefer ones with snowflake adapter)
    if defined DBT_SF_ENV_FOUND (
        echo.
        echo -^> Activating conda 'dbt' environment...
        call conda activate dbt >nul 2>nul
    ) else if defined FIRST_DBT_SF_ENV (
        echo.
        echo -^> Activating conda '!FIRST_DBT_SF_ENV!' environment...
        call conda activate !FIRST_DBT_SF_ENV! >nul 2>nul
    ) else if defined DBT_ENV_FOUND (
        echo.
        echo -^> Activating conda 'dbt' environment...
        call conda activate dbt >nul 2>nul
    ) else if defined FIRST_DBT_ENV (
        echo.
        echo -^> Activating conda '!FIRST_DBT_ENV!' environment...
        call conda activate !FIRST_DBT_ENV! >nul 2>nul
    ) else (
        REM Check if dbt environment exists (but no dbt installed yet)
        conda env list | findstr /b "dbt " >nul 2>nul
        if !errorlevel! equ 0 (
            echo   + 'dbt' environment exists ^(but dbt not detected yet^)
            echo.
            echo -^> Activating conda 'dbt' environment...
            call conda activate dbt >nul 2>nul
        )
    )
) else (
    echo - conda: NOT INSTALLED
    set CONDA_INSTALLED=false

    REM Try .venv as fallback
    if exist ".venv" (
        echo.
        echo -^> Activating .venv environment...
        call .venv\Scripts\activate.bat >nul 2>nul
    )
)

echo.

REM Check for Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v

    REM Extract major and minor version
    for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
        set MAJOR=%%a
        set MINOR=%%b
    )

    REM Check if version is 3.9-3.12
    if !MAJOR! equ 3 (
        if !MINOR! geq 9 (
            if !MINOR! leq 12 (
                echo + Python: INSTALLED ^(!PYTHON_VERSION! - compatible with dbt Core 1.9.4^)
                set PYTHON_COMPATIBLE=true
                goto python_compat_done
            )
        )
    )

    echo ! Python: INSTALLED ^(!PYTHON_VERSION! - NOT compatible, need 3.9-3.12^)
    set PYTHON_COMPATIBLE=false
    :python_compat_done
    set PYTHON_INSTALLED=true
) else (
    echo - Python: NOT INSTALLED
    set PYTHON_INSTALLED=false
    set PYTHON_COMPATIBLE=false
)

REM Check for dbt
where dbt >nul 2>nul
if %errorlevel% equ 0 (
    echo + dbt: INSTALLED
    set DBT_INSTALLED=true

    REM Show detailed dbt version info
    echo.
    echo -^> dbt version details:
    dbt --version 2^>^&1

    REM Check specifically for dbt-snowflake
    dbt --version 2^>^&1 | findstr "snowflake:" >nul 2>nul
    if !errorlevel! equ 0 (
        echo.
        echo + dbt-snowflake adapter is installed
    ) else (
        echo.
        echo - dbt-snowflake adapter not found in active environment
        echo   Install with: pip install dbt-snowflake
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
)

echo.

REM Check for curl
where curl >nul 2>nul
if %errorlevel% equ 0 (
    echo + curl: INSTALLED
    set CURL_INSTALLED=true
) else (
    echo - curl: NOT INSTALLED ^(required for automated installations^)
    set CURL_INSTALLED=false
)

echo.
echo === Recommendations ===
echo.

if "%DBT_INSTALLED%"=="true" (
    echo + dbt is already installed. You can verify with: dbt --version
    echo.
    echo To update dbt, use:
    if "%CONDA_INSTALLED%"=="true" (
        echo   conda activate dbt ^&^& conda update dbt-core dbt-snowflake
    ) else (
        echo   pip install -U dbt-core dbt-snowflake
    )
) else if "%CONDA_INSTALLED%"=="true" (
    echo -^> RECOMMENDED: Use 'setup-conda-env.bat' to create dbt environment
    echo   ^(conda is already installed^)
) else if "%PYTHON_COMPATIBLE%"=="true" (
    echo -^> RECOMMENDED: Use 'setup-venv-env.bat' to create dbt environment with venv
    echo   ^(Python !MINOR! is compatible^)
) else (
    echo -^> STEP 1: Install conda first
    echo   - Run 'install-miniforge.bat' ^(recommended, free^)
    echo   - OR run 'install-miniconda.bat'
    echo.
    echo -^> STEP 2: Then run 'setup-conda-env.bat' to create dbt environment
)

echo.
echo === Summary ===
echo conda_installed=%CONDA_INSTALLED%
echo python_installed=%PYTHON_INSTALLED%
echo python_compatible=%PYTHON_COMPATIBLE%
echo dbt_installed=%DBT_INSTALLED%
echo curl_installed=%CURL_INSTALLED%
