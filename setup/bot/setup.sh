#!/bin/bash
# Telegram Bot Setup Script
# This script installs and enables the Telegram bot systemd service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOT_DIR="/opt/telegram-bot"
CONFIG_DIR="/root/.config/telegram-bot"
SERVICE_NAME="telegram-bot"
SERVICE_FILE="${SERVICE_NAME}.service"

echo "Telegram Bot Setup Script"
echo "========================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ] && [ "$(whoami)" != "root" ]; then
    echo "Please run this script as root or with sudo"
    exit 1
fi

# Check if bot user exists, create if not
echo "[0/6] Checking for bot user..."
if ! id "bot" &>/dev/null; then
    echo "[0/6] Creating bot user..."
    useradd --system --no-create-home --shell /usr/sbin/nologin bot
else
    echo "[0/6] Bot user already exists"
fi

# Create bot directory
echo "[1/6] Creating bot directory..."
mkdir -p "$BOT_DIR"

# Create virtualenv
echo "[1.5/6] Creating virtualenv..."
python3 -m venv "$BOT_DIR/venv"

# Install required packages
echo "[1.6/6] Installing required packages..."
"$BOT_DIR/venv/bin/pip" install --upgrade pip
"$BOT_DIR/venv/bin/pip" install python-telegram-bot

# Copy the bot script
echo "[2/6] Copying bot script..."
cp "$SCRIPT_DIR/telegram_bot.py" "$BOT_DIR/"
chmod +x "$BOT_DIR/telegram_bot.py"

# Create config directory
echo "[2.5/6] Creating config directory..."
mkdir -p "$CONFIG_DIR"

# Create the systemd service file
echo "[3/6] Creating systemd service file..."
cat > "/etc/systemd/system/$SERVICE_FILE" << EOF
[Unit]
Description=Telegram Bot - System Status Reporter
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=$BOT_DIR
ExecStart=$BOT_DIR/venv/bin/python $BOT_DIR/telegram_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=XDG_CONFIG_HOME=/home/bot/.config

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
echo "[4/6] Reloading systemd daemon..."
systemctl daemon-reload

# Enable the service
echo "[5/6] Enabling the service..."
systemctl enable "$SERVICE_NAME"

# Create config directory with proper ownership
echo "[6/6] Setting up config directory..."
mkdir -p "$CONFIG_DIR"
chown -R bot:bot "$CONFIG_DIR"

echo ""
echo "Setup complete!"
echo ""
echo "The Telegram bot has been installed and will start automatically on boot."
echo "Service name: $SERVICE_NAME"
echo "Running as user: bot (nologin system user)"
echo ""
echo "To manually start the bot: systemctl start $SERVICE_NAME"
echo "To check status: systemctl status $SERVICE_NAME"
echo "To view logs: journalctl -u $SERVICE_NAME -f"
echo ""
echo "IMPORTANT: After first boot, send /start to @esp_lmsm_bot to add your chat ID"