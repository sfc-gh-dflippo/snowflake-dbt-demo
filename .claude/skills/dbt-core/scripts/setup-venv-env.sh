#!/bin/bash
# name: Setup dbt with Python venv
# description: Create a Python virtual environment for dbt using venv

set -e

echo "=== Setting up dbt with Python venv ==="
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "✗ Error: requirements.txt not found in current directory"
    echo "  Please navigate to the .claude/skills/dbt-core/ directory"
    exit 1
fi

# Check if venv module is available
if ! python3 -m venv --help &> /dev/null; then
    echo "→ venv module not found, installing virtualenv..."
    pip3 install virtualenv
fi

# Create virtual environment
if [ -d ".venv" ]; then
    echo "→ Virtual environment .venv already exists, recreating..."
    rm -rf .venv
fi

echo "→ Creating virtual environment..."
python3 -m venv .venv

# Activate and install dependencies
echo "→ Installing dependencies from requirements.txt..."
source .venv/bin/activate
pip install -U pip
pip install -U -r requirements.txt

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To verify installation:"
echo "  dbt --version"
echo ""
echo "To deactivate when done:"
echo "  deactivate"

