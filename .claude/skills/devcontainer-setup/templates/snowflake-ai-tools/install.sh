#!/bin/bash
set -e

echo "Installing Snowflake & AI Development Tools..."

# Options from devcontainer-feature.json
INSTALL_SNOWFLAKE_CLI="${INSTALLSNOWFLAKECLI:-true}"
INSTALL_SCHEMACHANGE="${INSTALLSCHEMACHANGE:-true}"
INSTALL_CLAUDE_CODE="${INSTALLCLAUDECODE:-true}"
INSTALL_CORTEX_CODE="${INSTALLCORTEXCODE:-true}"
INSTALL_RIPGREP="${INSTALLRIPGREP:-true}"

# Detect target user and set HOME so all tools install to user's ~/.local/bin
USERNAME="${_REMOTE_USER:-${SUDO_USER:-vscode}}"
export HOME=$(getent passwd "$USERNAME" | cut -d: -f6 || echo "/home/$USERNAME")
export UV_TOOL_BIN_DIR="$HOME/.local/bin"
echo "[INFO] Installing for user: $USERNAME (home: $HOME)"

# --- UPGRADE SYSTEM PACKAGES AND INSTALL RIPGREP ---
echo "[INFO] Upgrading system packages..."
if command -v apt-get &> /dev/null; then
    rm -f /etc/apt/sources.list.d/yarn.list 2>/dev/null || true  # Remove expired yarn repo
    apt-get update
    apt-get upgrade -y
    [ "$INSTALL_RIPGREP" = "true" ] && apt-get install -y --no-install-recommends ripgrep
    apt-get clean && rm -rf /var/lib/apt/lists/*
elif command -v apk &> /dev/null; then
    [ "$INSTALL_RIPGREP" = "true" ] && apk add --no-cache ripgrep
elif command -v dnf &> /dev/null; then
    [ "$INSTALL_RIPGREP" = "true" ] && dnf install -y ripgrep && dnf clean all
elif command -v yum &> /dev/null; then
    [ "$INSTALL_RIPGREP" = "true" ] && yum install -y ripgrep && yum clean all
fi

# --- CREATE MOUNT POINT DIRECTORIES ---
echo "[INFO] Creating mount point directories..."
mkdir -p "$HOME"/.{local/bin,cache/pip,cache/uv,snowflake,claude,cursor}

# --- INSTALL TOOLS ---
echo "[INFO] Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

[ "$INSTALL_SNOWFLAKE_CLI" = "true" ] && uv tool install snowflake-cli
[ "$INSTALL_SCHEMACHANGE" = "true" ] && uv tool install schemachange
[ "$INSTALL_CLAUDE_CODE" = "true" ] && curl -fsSL https://claude.ai/install.sh | bash
[ "$INSTALL_CORTEX_CODE" = "true" ] && (NON_INTERACTIVE=1 bash -c "$(curl -fsSL https://ai.snowflake.com/static/cc-scripts/install.sh)" || true)

# Fix ownership for non-root user
[ "$USERNAME" != "root" ] && chown -R "${USERNAME}:${USERNAME}" "$HOME" 2>/dev/null || true

# --- INSTALL POST-CREATE SCRIPT ---
echo "[INFO] Installing post-create setup script..."

cat > /usr/local/bin/snowflake-ai-tools-setup << 'POSTCREATE'
#!/bin/bash
set -e

echo "=========================================="
echo "Starting Agentic Environment Setup..."
echo "=========================================="

# --- DETECT ENVIRONMENT ---
ARCH=$(uname -m)
echo "[INFO] Architecture: $ARCH"
echo "[INFO] User: $(whoami)"
echo "[INFO] Home: $HOME"

# --- CONFIGURE SHELL ---
for RCFILE in ~/.bashrc ~/.zshrc; do
    if [ -f "$RCFILE" ]; then
        # Add ~/.local/bin to PATH for user-installed tools (uv, pip)
        if ! grep -q 'HOME/.local/bin' "$RCFILE" 2>/dev/null; then
            echo "" >> "$RCFILE"
            echo "# Add user local bin to PATH" >> "$RCFILE"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RCFILE"
        fi
    fi
done

# --- UPDATE AI TOOLS ---
echo ""
echo "[INFO] Updating AI tools..."
command -v claude &> /dev/null && claude update 2>/dev/null || true
command -v cortex &> /dev/null && cortex update 2>/dev/null || true
echo "[OK] AI tools update complete"

# --- VERIFY INSTALLATION ---
echo ""
echo "[INFO] Verifying tools..."
command -v cortex &> /dev/null && echo "[OK] Cortex Code: $(which cortex)" || echo "[--] Cortex Code: not installed"
command -v claude &> /dev/null && echo "[OK] Claude Code: $(which claude)" || echo "[--] Claude Code: not installed"
command -v snow &> /dev/null && echo "[OK] Snowflake CLI: $(which snow)" || echo "[--] Snowflake CLI: not installed"
command -v uv &> /dev/null && echo "[OK] uv: $(which uv)" || echo "[--] uv: not installed"
command -v rg &> /dev/null && echo "[OK] ripgrep: $(which rg)" || echo "[--] ripgrep: not installed"

# --- CHECK SNOWFLAKE CONFIG ---
echo ""
if [ -f "$HOME/.snowflake/connections.toml" ]; then
    echo "[OK] Snowflake config: ~/.snowflake/connections.toml"
else
    echo "[--] Snowflake config: not found (create ~/.snowflake/connections.toml)"
fi

# --- FIX PERMISSIONS ---
for DIR in ~/.claude ~/.cursor ~/.cache ~/.snowflake; do
    [ -d "$DIR" ] && sudo chown -R $(whoami) "$DIR" 2>/dev/null || true
done

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
POSTCREATE

chmod +x /usr/local/bin/snowflake-ai-tools-setup

echo ""
echo "[OK] Snowflake & AI Development Tools installation complete!"
