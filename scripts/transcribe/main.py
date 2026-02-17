#!/usr/bin/env python3
"""
Telegram Bot for handling voice recordings.

This bot:
- Accepts a /start command to initiate conversation
- Waits for audio voice recordings from users
- Saves recorded audio to a configured folder with timestamp as filename
"""

from models import Chat, Transcriber, Diffuser

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
chat = Chat(
    quantization=True,
    device="cuda:0",
    max_new_tokens=1024,
    system_msg="You are an assistant that provide concise responses to fit a mobile phone chat, usually using markdown to enrich the text",
)
chat.load_model()

transcriber = Transcriber(device="cuda:0")
transcriber.load_model()

diffuser = Diffuser(device="cuda:0")
diffuser.load_model()


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
        wav_path = transcriber._convert_ogg_to_wav(
            ogg_path=file_path, output_dir=download_folder
        )
        logger.info(f"Converted to WAV: {wav_path}")

        # Send the converted wav file
        # await update.message.reply_document(wav_path)

        if transcriber.model:
            try:
                # Read the wav file and transcribe
                wav_bytes = wav_path.read_bytes()
                transcribed_lang, transcribed_text = transcriber.transcribe(wav_bytes)

                # Send the transcribed text
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


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat.clear()


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate an image from the user's prompt and send it back to the chat."""
    try:
        # Load diffuser model if not already loaded
        if not diffuser._model_loaded:
            await update.message.reply_text(
                "📨 Loading diffusion model... (this may take a moment)"
            )
            diffuser.load_model()

        # Get the text prompt from user
        prompt = update.message.text.strip()

        # Remove the /image command from the prompt if present
        if prompt.lower().startswith("/image"):
            prompt = prompt[6:].strip()  # Remove "/image" and any leading space

        if not prompt:
            await update.message.reply_text(
                "Please provide a text prompt after /image, e.g:\n"
                "/image A cat holding a sign that says hello world"
            )
            return

        await update.message.reply_text(
            "🪩 Generating image... (this may take a moment)"
        )

        # Generate filename with timestamp in /tmp folder
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/{timestamp}.png"

        # Generate the image using diffuser
        diffuser.generate(
            prompt=prompt,
            image_path=output_path,
            height=1024,
            width=1024,
        )

        await update.message.reply_document(document=output_path)
        logger.info(f"Image generated and sent to user: {output_path}")

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        await update.message.reply_text(f"⚻️ Image generation failed: {str(e)}")


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
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("image", generate_image))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
