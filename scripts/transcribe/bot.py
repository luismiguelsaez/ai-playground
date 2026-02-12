#!/usr/bin/env python3
"""
Telegram Bot for handling voice recordings.

This bot:
- Accepts a /start command to initiate conversation
- Waits for audio voice recordings from users
- Saves recorded audio to a configured folder with timestamp as filename
"""

from utils import convert_ogg_to_wav, read_wav_from_bytes
from models import load_asr_model, Chat

import logging
from datetime import datetime
from pathlib import Path
from typing import Final

from telegram import Update, Voice
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import dotenv_values

env = dotenv_values(dotenv_path=".env")

# Configuration
TOKEN: Final = env.get("TELEGRAM_TOKEN")
DEFAULT_DOWNLOAD_FOLDER: Final = env.get("DOWNLOAD_FOLDER")

# Enable logging first before any other logging calls
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load models
asr_model = load_asr_model()
chat = Chat(quantization=True, device="cuda:0")
chat.load_model()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I'm your voice recording bot.\n\n"
        "Please send me a voice recording, and I'll save it to disk."
    )


async def handle_voice_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle incoming voice messages and save them to disk."""
    voice: Voice = update.message.voice

    # Get the file
    file = await voice.get_file()

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = voice.file_unique_id  # Use unique ID as part of filename
    filename = f"{timestamp}_{file_extension}.ogg"

    # Determine download directory
    download_folder = Path(
        context.bot_data.get("download_folder", DEFAULT_DOWNLOAD_FOLDER)
    )

    # Create directory if it doesn't exist
    download_folder.mkdir(parents=True, exist_ok=True)

    # Construct full path
    file_path = download_folder / filename

    # Download the file
    await file.download_to_drive(file_path)

    logger.info(f"Voice message saved to: {file_path}")

    # Convert ogg to wav
    try:
        wav_path = convert_ogg_to_wav(file_path, download_folder)
        logger.info(f"Converted to WAV: {wav_path}")

        # Get the ASR model (loaded at startup)
        model = asr_model

        # Send the converted wav file
        # await update.message.reply_document(wav_path)

        if model:
            try:
                # Read the wav file and transcribe
                wav_bytes = wav_path.read_bytes()
                audio_data, sample_rate = read_wav_from_bytes(wav_bytes)

                # Transcribe the audio
                results = model.transcribe(
                    audio=(audio_data, sample_rate),
                    language=None,
                )

                # Send the transcribed text
                transcribed_text = results[0].text
                transcribed_lang = results[0].language
                await update.message.reply_text(
                    f"📝 Transcribed text ({transcribed_lang}):\n{transcribed_text}"
                )
                model_msg = chat.generate(transcribed_text)
                await update.message.reply_markdown(
                    text=model_msg,
                )
            finally:
                # Clean up audio files after processing (whether successful or failed)
                try:
                    file_path.unlink()  # Delete .ogg file
                    logger.info(f"Cleaned up .ogg file: {file_path}")
                except FileNotFoundError:
                    logger.warning(
                        f"Could not clean up .ogg file: {file_path} - not found"
                    )

                try:
                    wav_path.unlink()  # Delete .wav file
                    logger.info(f"Cleaned up .wav file: {wav_path}")
                except FileNotFoundError:
                    logger.warning(
                        f"Could not clean up .wav file: {wav_path} - not found"
                    )
        else:
            logger.warning("ASR model not loaded")
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        await update.message.reply_text(f"⚠️ An error occurred: {str(e)}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Add handler for voice messages
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, handle_voice_message)
    )

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
