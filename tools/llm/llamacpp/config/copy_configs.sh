#!/bin/bash

# Script to copy configs to home folders

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure source directories exist
if [[ ! -d "$SCRIPT_DIR/pi" ]]; then
    echo "Error: pi directory not found at $SCRIPT_DIR/pi"
    exit 1
fi

if [[ ! -d "$SCRIPT_DIR/opencode" ]]; then
    echo "Error: opencode directory not found at $SCRIPT_DIR/opencode"
    exit 1
fi

# Create destination directories
mkdir -p "$HOME/.pi"
mkdir -p "$HOME/.config/opencode"

echo "Copying pi config..."
cp -r "$SCRIPT_DIR/pi/." "$HOME/.pi/"
echo "Done: pi -> ~/.pi"

# Check if pi coding agent is already installed
if command -v pi &> /dev/null && pi --version &> /dev/null; then
    echo "pi coding agent is already installed, skipping..."
else
    echo "Installing pi coding agent..."
    npm install -g @mariozechner/pi-coding-agent
    echo "Done: pi coding agent installed"
fi

echo "Copying opencode config..."
cp -r "$SCRIPT_DIR/opencode/." "$HOME/.config/opencode/"
echo "Done: opencode -> ~/.config/opencode"

# Install opencode based on platform
UNAME=$(uname -s)

if command -v opencode &> /dev/null && opencode --version &> /dev/null; then
    echo "opencode is already installed, skipping..."
else
    echo "Installing opencode..."
    if [[ "$UNAME" == "Darwin" ]]; then
        # MacOS
        if command -v brew &> /dev/null; then
            brew install anomalyco/tap/opencode
            echo "Done: opencode installed via Homebrew"
        else
            echo "Error: Homebrew not found. Please install Homebrew first."
            exit 1
        fi
    else
        # Linux
        if command -v npm &> /dev/null; then
            npm i -g opencode-ai
            echo "Done: opencode installed via npm"
        else
            curl -fsSL https://opencode.ai/install | bash
            echo "Done: opencode installed via cURL"
        fi
    fi
fi

echo "All configs copied successfully!"