import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import your existing LLM functionality
from main import messages, get_response

# Get the Telegram token from environment variable
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable not set")

# Global variable to store conversation history for each user
user_conversations = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    logger.info(f"Received /start command from user {update.effective_user.id}")
    await update.message.reply_text(
        "Hello! I am your LLM assistant. Send me a message and I will respond!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    logger.info(f"Received /help command from user {update.effective_user.id}")
    await update.message.reply_text(
        "Send me a message and I will respond using the LLM. Type /start to restart or /clear to reset conversation."
    )


async def clear_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear the conversation history for the user."""
    user_id = update.effective_user.id
    logger.info(f"Clearing conversation for user {user_id}")
    if user_id in user_conversations:
        del user_conversations[user_id]
    await update.message.reply_text(
        "Conversation cleared! I've forgotten our previous conversation."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and respond using the LLM."""
    user_id = update.effective_user.id
    user_input = update.message.text

    logger.debug(f"Received message from user {user_id}: {user_input}")

    # Initialize user conversation if not exists
    if user_id not in user_conversations:
        user_conversations[user_id] = messages.copy()

    # Get response from LLM
    logger.info(f"Generating LLM response for user {user_id}")
    response = get_response(user_input, user_conversations[user_id])

    # Send response back to user
    logger.debug(f"Sending response to user {user_id}")
    await update.message.reply_text(response)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_conversation))

    # Register message handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
