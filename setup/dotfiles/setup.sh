#!/bin/bash

# Dotfiles Setup Script
# This script copies dotfiles from the current directory to the home directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="$HOME"

echo "=== Dotfiles Setup Script ==="
echo "Source directory: $SCRIPT_DIR"
echo "Target directory: $HOME_DIR"
echo ""

# Function to copy a file or directory
copy_to_home() {
    local source="$1"
    local target="$HOME_DIR/$2"
    local relative_path="$2"
    
    # Create target directory if it doesn't exist
    mkdir -p "$(dirname "$target")"
    
    # Check if target already exists
    if [ -e "$target" ]; then
        echo "⚠️  $relative_path already exists"
        read -p "Replace it? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping $relative_path"
            return 0
        fi
    fi
    
    # Copy the file/directory
    cp -r "$source" "$target"
    echo "✅ Copied $relative_path"
}

# Copy dotfiles from current directory
echo "Copying dotfiles..."

# Copy .zshrc
if [ -f "$SCRIPT_DIR/.zshrc" ]; then
    copy_to_home "$SCRIPT_DIR/.zshrc" ".zshrc"
fi

# Copy .config directory
if [ -d "$SCRIPT_DIR/.config" ]; then
    for item in "$SCRIPT_DIR/.config"/*; do
        if [ -d "$item" ]; then
            item_name=$(basename "$item")
            copy_to_home "$item" ".config/$item_name"
        fi
    done
fi

# Copy .pi directory
if [ -d "$SCRIPT_DIR/.pi" ]; then
    copy_to_home "$SCRIPT_DIR/.pi" ".pi"
fi

echo ""
echo "=== Setup Complete ==="
echo "Your dotfiles have been copied to $HOME_DIR"