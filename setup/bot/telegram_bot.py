#!/usr/bin/env python3
"""
Telegram Bot - System Status Reporter
Sends a system resource report when the bot starts up.
"""

import asyncio
import configparser
import os
import re
import subprocess
import urllib.request
from telegram import Bot, Update
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configuration
TELEGRAM_TOKEN = "7411509635:AAEpYvGl3PF_W0mNrQicmy8SvCLahfImMLQ"
CONFIG_DIR = os.path.expanduser("~/.config/telegram-bot")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")


def get_public_ip():
    """Get the current public IP address."""
    try:
        services = [
            "https://api.ipify.org",
            "https://checkip.amazonaws.com",
            "https://ifconfig.me"
        ]
        for service in services:
            try:
                with urllib.request.urlopen(service, timeout=5) as response:
                    return response.read().decode("utf-8").strip()
            except Exception:
                continue
        return "Unknown"
    except Exception:
        return "Unknown"


def get_disk_usage():
    """Get disk usage information."""
    try:
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                return lines[1].split()[1:5]
        return "Unknown"
    except Exception:
        return "Unknown"


def get_connected_users():
    """Get number of connected users."""
    try:
        result = subprocess.run(
            ["who", "-q"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            match = re.search(r"users=(\d+)", output)
            if match:
                return match.group(1)
            users = [line.split()[0] for line in output.split("\n") if line]
            return str(len(set(users))) if users else "0"
        return "0"
    except Exception:
        return "0"


def get_system_info():
    """Get system information."""
    info = {}
    
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            info["uptime"] = f"{days}d {hours}h {minutes}m"
    except Exception:
        info["uptime"] = "Unknown"
    
    try:
        with open("/proc/meminfo", "r") as f:
            meminfo = f.read()
            total = re.search(r"MemTotal:\s+(\d+)\s+kB", meminfo)
            available = re.search(r"MemAvailable:\s+(\d+)\s+kB", meminfo)
            
            if total and available:
                total_kb = int(total.group(1))
                avail_kb = int(available.group(1))
                used_kb = total_kb - avail_kb
                used_percent = int((used_kb / total_kb) * 100) if total_kb > 0 else 0
                info["memory"] = f"{used_kb // 1024}MB / {total_kb // 1024}MB ({used_percent}%)"
            else:
                info["memory"] = "Unknown"
    except Exception:
        info["memory"] = "Unknown"
    
    return info


def load_config():
    """Load chat IDs from config file."""
    if not os.path.exists(CONFIG_FILE):
        return []
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if "chat_ids" in config and "ids" in config["chat_ids"]:
        ids_str = config["chat_ids"]["ids"]
        return [int(x.strip()) for x in ids_str.split(",") if x.strip()]
    
    return []


def save_chat_id(chat_id):
    """Save a chat ID to config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if "chat_ids" not in config:
        config["chat_ids"] = {}
    
    current_ids = load_config()
    if chat_id not in current_ids:
        current_ids.append(chat_id)
        config["chat_ids"]["ids"] = ",".join(str(x) for x in current_ids)
        
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        
        print(f"Saved chat ID: {chat_id}")


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - save sender's chat ID."""
    chat_id = update.message.chat_id
    user = update.message.from_user
    
    save_chat_id(chat_id)
    
    await update.message.reply_text(
        f"✅ Chat ID {chat_id} saved!\n\n"
        f"Your username: @{user.username if user.username else 'N/A'}\n"
        f"User ID: {user.id}\n\n"
        f"The bot will now send startup reports to this chat."
    )


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - send current system status."""
    chat_id = update.message.chat_id
    await send_status_message(chat_id)


async def send_status_message(chat_id):
    """Send a status message to a specific chat ID."""
    bot = Bot(token=TELEGRAM_TOKEN)
    
    public_ip = get_public_ip()
    disk_info = get_disk_usage()
    users = get_connected_users()
    sys_info = get_system_info()
    
    if isinstance(disk_info, list):
        disk_str = f"Total: {disk_info[0]}, Used: {disk_info[1]}, Available: {disk_info[2]}, Use: {disk_info[3]}"
    else:
        disk_str = disk_info
    
    message = f"""✅ Telegram Bot Status Report
━━━━━━━━━━━━━━━━━━━━
📊 System Resources:
━━━━━━━━━━━━━━━━━━━━
🌐 Public IP: {public_ip}
💾 Disk Usage: {disk_str}
👥 Connected Users: {users}
🧠 Memory: {sys_info['memory']}
⏱️ Uptime: {sys_info['uptime']}
━━━━━━━━━━━━━━━━━━━━
"""
    
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        return True
    except TelegramError as e:
        print(f"Failed to send status message to {chat_id}: {e}")
        return False


async def send_startup_messages():
    """Send startup message to all saved chat IDs."""
    bot = Bot(token=TELEGRAM_TOKEN)
    
    public_ip = get_public_ip()
    disk_info = get_disk_usage()
    users = get_connected_users()
    sys_info = get_system_info()
    
    if isinstance(disk_info, list):
        disk_str = f"Total: {disk_info[0]}, Used: {disk_info[1]}, Available: {disk_info[2]}, Use: {disk_info[3]}"
    else:
        disk_str = disk_info
    
    message = f"""✅ Telegram Bot Startup Report
━━━━━━━━━━━━━━━━━━━━
✅ Bot started successfully

📊 System Resources:
━━━━━━━━━━━━━━━━━━━━
🌐 Public IP: {public_ip}
💾 Disk Usage: {disk_str}
👥 Connected Users: {users}
🧠 Memory: {sys_info['memory']}
⏱️ Uptime: {sys_info['uptime']}
━━━━━━━━━━━━━━━━━━━━
"""
    
    chat_ids = load_config()
    
    if not chat_ids:
        print("No chat IDs configured. Run /start with the bot to add your chat ID.")
        print(f"Config file location: {CONFIG_FILE}")
        return False
    
    success_count = 0
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            print(f"Sent startup message to chat {chat_id}")
            success_count += 1
        except TelegramError as e:
            print(f"Failed to send to {chat_id}: {e}")
    
    return success_count > 0


def main():
    """Main entry point."""
    print("Telegram Bot starting...")
    
    # Load saved chat IDs and send startup messages
    chat_ids = load_config()
    
    if chat_ids:
        # Send startup messages before starting to poll
        asyncio.run(send_startup_messages())
    else:
        print(f"No chat IDs configured. First /start will add your ID.")
        print(f"Config file location: {CONFIG_FILE}")
    
    # Create application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("status", status_handler))
    
    # Start the bot
    print("Bot is running. Press Ctrl+C to stop.")
    print(f"Config file: {CONFIG_FILE}")
    print("Add me to a chat and send /start to receive startup reports.")
    
    application.run_polling()


if __name__ == "__main__":
    main()