#!/bin/bash
# name: Check Environment Prerequisites
# description: Verify the dbt Fusion engine (dbt 2.0) is installed and on PATH before dbt setup

set -e

echo "=== Environment Check ==="
echo ""

# Check for dbt on PATH
if command -v dbt &> /dev/null; then
    echo "✓ dbt: INSTALLED"
    DBT_INSTALLED="true"

    # Show detailed dbt version info
    echo ""
    echo "→ dbt version details:"
    DBT_VERSION_OUTPUT=$(dbt --version 2>&1)
    echo "$DBT_VERSION_OUTPUT" | sed 's/^/  /'

    # Confirm this is the Fusion engine (dbt 2.0.x)
    if echo "$DBT_VERSION_OUTPUT" | grep -Eiq "fusion|2\.0\."; then
        echo ""
        echo "✓ dbt Fusion engine (2.0.x) detected"
        DBT_FUSION="true"
    else
        echo ""
        echo "⚠ dbt is installed but does not appear to be the Fusion engine (2.0.x)"
        echo "  Install/update with: ./install-dbt.sh   (or: dbt system update)"
        DBT_FUSION="false"
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
    DBT_FUSION="false"
fi

echo ""

# Check for snowflake-cli (separate tool, optional but recommended)
if command -v snow &> /dev/null; then
    SNOW_VERSION=$(snow --version 2>&1 | head -n1)
    echo "✓ snowflake-cli: INSTALLED ($SNOW_VERSION)"
    SNOW_INSTALLED="true"
else
    echo "✗ snowflake-cli: NOT INSTALLED (optional: UV_SYSTEM_CERTS=true uv tool install snowflake-cli)"
    SNOW_INSTALLED="false"
fi

echo ""

# Check for curl (needed for the Fusion installer)
if command -v curl &> /dev/null; then
    echo "✓ curl: INSTALLED"
    CURL_INSTALLED="true"
else
    echo "✗ curl: NOT INSTALLED (required for the Fusion installer)"
    CURL_INSTALLED="false"
fi

echo ""
echo "=== Recommendations ==="
echo ""

if [ "$DBT_INSTALLED" = "true" ] && [ "$DBT_FUSION" = "true" ]; then
    echo "✓ dbt Fusion is installed. Verify with: dbt --version"
    echo "  To update later, run: dbt system update"
elif [ "$DBT_INSTALLED" = "true" ]; then
    echo "→ dbt is installed but not the Fusion engine (2.0.x)."
    echo "  Run './install-dbt.sh' to install Fusion, or 'dbt system update' to update."
else
    echo "→ RECOMMENDED: Run './install-dbt.sh' to install the dbt Fusion engine (2.0.x)"
    echo "  (installs to \$HOME/.local/bin, no sudo required)"
fi

echo ""
echo "=== Summary ==="
echo "dbt_installed=$DBT_INSTALLED"
echo "dbt_fusion=$DBT_FUSION"
echo "snowflake_cli_installed=$SNOW_INSTALLED"
echo "curl_installed=$CURL_INSTALLED"
