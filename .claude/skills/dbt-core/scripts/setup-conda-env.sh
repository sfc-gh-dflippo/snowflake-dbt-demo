#!/bin/bash
# name: Setup dbt with Conda
# description: Create or update a conda environment for dbt with all required dependencies

set -e

echo "=== Setting up dbt with conda ==="
echo ""

# Check if dbt-conda-env.yml exists
if [ ! -f "dbt-conda-env.yml" ]; then
    echo "✗ Error: dbt-conda-env.yml not found in current directory"
    echo "  Please navigate to the .claude/skills/dbt-core/ directory"
    exit 1
fi

# Check if environment already exists
if conda env list | grep -q "^dbt "; then
    echo "→ conda environment 'dbt' already exists, updating..."
    conda env update -f dbt-conda-env.yml
    echo "✓ Environment updated"
else
    echo "→ Creating conda environment from dbt-conda-env.yml..."
    conda env create -f dbt-conda-env.yml
    echo "✓ Environment created"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the environment:"
echo "  conda activate dbt"
echo ""
echo "To verify installation:"
echo "  dbt --version"
echo ""
echo "To deactivate when done:"
echo "  conda deactivate"

