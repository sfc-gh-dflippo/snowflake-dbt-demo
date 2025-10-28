#!/bin/bash
# Check environment for dbt setup prerequisites
# Outputs structured information for AI agent decision-making

set -e

echo "=== Environment Check ==="
echo ""

# Check for conda first
if command -v conda &> /dev/null; then
    CONDA_VERSION=$(conda --version 2>&1 | head -n1)
    echo "✓ conda: INSTALLED ($CONDA_VERSION)"
    CONDA_INSTALLED="true"
    
    # List all conda environments and check each for dbt
    echo ""
    echo "→ Checking conda environments for dbt..."
    DBT_ENVS=()
    DBT_SNOWFLAKE_ENVS=()
    
    while IFS= read -r env_line; do
        # Parse environment name (first column, skip comments and headers)
        env_name=$(echo "$env_line" | awk '{print $1}')
        if [[ ! "$env_name" =~ ^#.* ]] && [[ -n "$env_name" ]] && [[ "$env_name" != "base" ]]; then
            # Check if this environment has dbt-core
            if conda list -n "$env_name" 2>/dev/null | grep -q "^dbt-core"; then
                DBT_CORE_VERSION=$(conda list -n "$env_name" 2>/dev/null | grep "^dbt-core" | awk '{print $2}')
                
                # Check for dbt-snowflake adapter
                if conda list -n "$env_name" 2>/dev/null | grep -q "^dbt-snowflake"; then
                    DBT_SF_VERSION=$(conda list -n "$env_name" 2>/dev/null | grep "^dbt-snowflake" | awk '{print $2}')
                    echo "  ✓ '$env_name' has dbt-core $DBT_CORE_VERSION + dbt-snowflake $DBT_SF_VERSION"
                    DBT_ENVS+=("$env_name")
                    DBT_SNOWFLAKE_ENVS+=("$env_name")
                else
                    echo "  ○ '$env_name' has dbt-core $DBT_CORE_VERSION (no dbt-snowflake)"
                    DBT_ENVS+=("$env_name")
                fi
            fi
        fi
    done < <(conda env list | tail -n +3)
    
    # Try to activate an environment with dbt
    if [ ${#DBT_SNOWFLAKE_ENVS[@]} -gt 0 ]; then
        # Prefer 'dbt' environment if it has snowflake adapter, otherwise use first found with snowflake
        if [[ " ${DBT_SNOWFLAKE_ENVS[@]} " =~ " dbt " ]]; then
            ACTIVATE_ENV="dbt"
        else
            ACTIVATE_ENV="${DBT_SNOWFLAKE_ENVS[0]}"
        fi
    elif [ ${#DBT_ENVS[@]} -gt 0 ]; then
        # Fallback to any dbt environment even without snowflake adapter
        if [[ " ${DBT_ENVS[@]} " =~ " dbt " ]]; then
            ACTIVATE_ENV="dbt"
        else
            ACTIVATE_ENV="${DBT_ENVS[0]}"
        fi
        
        echo ""
        echo "→ Activating conda '$ACTIVATE_ENV' environment..."
        eval "$(conda shell.bash hook)"
        conda activate "$ACTIVATE_ENV" 2>/dev/null || true
    elif conda env list | grep -q "^dbt "; then
        echo "  ✓ 'dbt' environment exists (but dbt not detected yet)"
        echo ""
        echo "→ Activating conda 'dbt' environment..."
        eval "$(conda shell.bash hook)"
        conda activate dbt 2>/dev/null || true
    fi
else
    echo "✗ conda: NOT INSTALLED"
    CONDA_INSTALLED="false"
    
    # Try .venv as fallback
    if [ -d ".venv" ]; then
        echo ""
        echo "→ Activating .venv environment..."
        source .venv/bin/activate 2>/dev/null || true
    fi
fi

echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 9 ] && [ "$MINOR" -le 12 ]; then
        echo "✓ Python: INSTALLED ($PYTHON_VERSION - compatible with dbt Core 1.9.4)"
        PYTHON_COMPATIBLE="true"
    else
        echo "⚠ Python: INSTALLED ($PYTHON_VERSION - NOT compatible, need 3.9-3.12)"
        PYTHON_COMPATIBLE="false"
    fi
    PYTHON_INSTALLED="true"
else
    echo "✗ Python: NOT INSTALLED"
    PYTHON_INSTALLED="false"
    PYTHON_COMPATIBLE="false"
fi

# Check for dbt
if command -v dbt &> /dev/null; then
    echo "✓ dbt: INSTALLED"
    DBT_INSTALLED="true"
    
    # Show detailed dbt version info
    echo ""
    echo "→ dbt version details:"
    DBT_VERSION_OUTPUT=$(dbt --version 2>&1)
    echo "$DBT_VERSION_OUTPUT" | sed 's/^/  /'
    
    # Check specifically for dbt-snowflake in the output
    if echo "$DBT_VERSION_OUTPUT" | grep -q "snowflake:"; then
        echo ""
        echo "✓ dbt-snowflake adapter is installed"
    else
        echo ""
        echo "✗ dbt-snowflake adapter not found in active environment"
        echo "  Install with: pip install dbt-snowflake"
    fi
    
    # Test basic dbt command
    echo ""
    echo "→ Testing dbt command..."
    if dbt --help > /dev/null 2>&1; then
        echo "✓ dbt command works correctly"
    else
        echo "✗ dbt command failed"
    fi
else
    echo "✗ dbt: NOT INSTALLED"
    DBT_INSTALLED="false"
fi

echo ""

# Check for curl (needed for installations)
if command -v curl &> /dev/null; then
    echo "✓ curl: INSTALLED"
    CURL_INSTALLED="true"
else
    echo "✗ curl: NOT INSTALLED (required for automated installations)"
    CURL_INSTALLED="false"
fi

echo ""
echo "=== Recommendations ==="
echo ""

if [ "$DBT_INSTALLED" = "true" ]; then
    echo "✓ dbt is already installed. You can verify with: dbt --version"
    echo ""
    echo "To update dbt, use:"
    if [ "$CONDA_INSTALLED" = "true" ]; then
        echo "  conda activate dbt && conda update dbt-core dbt-snowflake"
    else
        echo "  pip install -U dbt-core dbt-snowflake"
    fi
elif [ "$CONDA_INSTALLED" = "true" ]; then
    echo "→ RECOMMENDED: Use 'setup-conda-env.sh' to create dbt environment"
    echo "  (conda is already installed)"
elif [ "$PYTHON_COMPATIBLE" = "true" ]; then
    echo "→ RECOMMENDED: Use 'setup-venv-env.sh' to create dbt environment with venv"
    echo "  (Python 3.$MINOR is compatible)"
else
    echo "→ STEP 1: Install conda first"
    echo "  - Run 'install-miniforge.sh' (recommended, free)"
    echo "  - OR run 'install-miniconda.sh'"
    echo ""
    echo "→ STEP 2: Then run 'setup-conda-env.sh' to create dbt environment"
fi

echo ""
echo "=== Summary ==="
echo "conda_installed=$CONDA_INSTALLED"
echo "python_installed=$PYTHON_INSTALLED"
echo "python_compatible=$PYTHON_COMPATIBLE"
echo "dbt_installed=$DBT_INSTALLED"
echo "curl_installed=$CURL_INSTALLED"

