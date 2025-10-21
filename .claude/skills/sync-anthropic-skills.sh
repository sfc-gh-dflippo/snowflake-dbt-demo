#!/bin/bash
# Script to sync Anthropic's official skills repository

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/anthropic-reference"
ZIP_URL="https://github.com/anthropics/skills/archive/refs/heads/main.zip"
TEMP_DIR=$(mktemp -d)

echo "Syncing Anthropic reference skills..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Download and extract the zip file
echo "Downloading latest skills from main branch..."
if command -v curl &> /dev/null; then
    curl -L "$ZIP_URL" -o "$TEMP_DIR/skills.zip"
elif command -v wget &> /dev/null; then
    wget "$ZIP_URL" -O "$TEMP_DIR/skills.zip"
else
    echo "Error: curl or wget is required to download the skills"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Extracting skills..."
unzip -q "$TEMP_DIR/skills.zip" -d "$TEMP_DIR"

# Remove existing skills and copy new ones
echo "Updating skills directory..."
rm -rf "$SKILLS_DIR"
mv "$TEMP_DIR/skills-main" "$SKILLS_DIR"

# Clean up
rm -rf "$TEMP_DIR"

echo "✓ Anthropic skills synced successfully to: $SKILLS_DIR"
echo ""
echo "Available skills:"
echo "  - Creative & Design: algorithmic-art, canvas-design, slack-gif-creator"
echo "  - Development: artifacts-builder, mcp-builder, webapp-testing"
echo "  - Enterprise: brand-guidelines, internal-comms, theme-factory"
echo "  - Document Skills: docx, pdf, pptx, xlsx"
echo "  - Meta: skill-creator, template-skill"

