#!/bin/bash
# Install Miniconda non-interactively
# For AI agent execution

set -e

echo "=== Installing Miniconda ==="
echo ""
echo "Miniconda provides minimal conda with the defaults channel."
echo "Source: https://docs.anaconda.com/miniconda/"
echo ""

# Detect OS and architecture
if [[ "$OSTYPE" == "darwin"* ]]; then
    ARCH=$(uname -m)
    if [[ "$ARCH" == "arm64" ]]; then
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    else
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    fi
else
    # Linux
    ARCH=$(uname -m)
    if [[ "$ARCH" == "aarch64" ]]; then
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
    elif [[ "$ARCH" == "ppc64le" ]]; then
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-ppc64le.sh"
    elif [[ "$ARCH" == "s390x" ]]; then
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-s390x.sh"
    else
        INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    fi
fi

echo "→ Downloading Miniconda installer..."
curl -L -O "$INSTALLER_URL"
INSTALLER_NAME=$(basename "$INSTALLER_URL")

echo "→ Running installer..."
bash "$INSTALLER_NAME" -b -p "$HOME/miniconda3"

echo "→ Initializing conda for all shells..."
"$HOME/miniconda3/bin/conda" init --all

# Clean up
rm "$INSTALLER_NAME"

echo ""
echo "✓ Miniconda installed successfully!"
echo ""
echo "Installation directory: $HOME/miniconda3"
echo "Conda has been initialized for all shells (bash, zsh, fish, etc.)"
echo ""
echo "IMPORTANT: Restart your terminal (or start a new terminal session)"
echo "to activate conda, then run 'check-environment.sh' to verify."

