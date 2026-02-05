#!/bin/bash
# Telegram Bot Remote Installation Script
# Usage: ./install_on_remote.sh <username>@<host>
# Example: ./install_on_remote.sh user@192.168.1.100

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <username>@<host>"
    echo "Example: $0 user@192.168.1.100"
    exit 1
fi

TARGET="$1"

echo "Installing Telegram Bot on $TARGET..."
echo ""

# Create archive of the bot files
BOT_ARCHIVE="telegram-bot-setup.tar.gz"
cd "$SCRIPT_DIR"
tar -czf "$BOT_ARCHIVE" telegram_bot.py setup.sh

# Copy files to remote system
echo "Copying files to remote system..."
scp "$BOT_ARCHIVE" "$TARGET:/tmp/"
ssh "$TARGET" "mkdir -p /opt/telegram-bot && tar -xzf /tmp/$BOT_ARCHIVE -C /opt/telegram-bot"

# Execute setup on remote system
echo "Running setup on remote system..."
ssh "$TARGET" "cd /opt/telegram-bot && chmod +x setup.sh && sudo ./setup.sh"

# Cleanup
ssh "$TARGET" "rm /tmp/$BOT_ARCHIVE"

echo ""
echo "Installation complete!"
echo "The Telegram bot is now installed and enabled on $TARGET"