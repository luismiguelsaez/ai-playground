#!/usr/bin/env python3
"""
Telegram Bot for handling voice recordings.

This bot:
- Accepts a /start command to initiate conversation
- Waits for audio voice recordings from users
- Saves recorded audio to a configured folder with timestamp as filename
"""

from utils import convert_ogg_to_wav

import logging
from datetime import datetime
from pathlib import Path
from typing import Final
import io
import numpy as np
import soundfile as sf

import torch
from qwen_asr import Qwen3ASRModel

from telegram import Update, Voice
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Configuration
TOKEN: Final = "425033555:AAFYf2UU2b7PLJYwPS0q6-jpEkmpUeFPq3M"
DEFAULT_DOWNLOAD_FOLDER: Final = "/tmp"

# Import conversion utility


def _read_wav_from_bytes(audio_bytes: bytes) -> tuple[np.ndarray, int]:
    """Read WAV audio data from bytes."""
    with io.BytesIO(audio_bytes) as f:
        wav, sr = sf.read(f, dtype="float32", always_2d=False)
    return np.asarray(wav, dtype=np.float32), int(sr)


def load_asr_model() -> Qwen3ASRModel:
    """Load the Qwen3 ASR model."""
    logger.info("Loading Qwen3 ASR model...")
    model = Qwen3ASRModel.from_pretrained(
        "Qwen/Qwen3-ASR-1.7B",
        dtype=torch.bfloat16,
        device_map="cuda:0",
        attn_implementation="flash_attention_2",
        max_inference_batch_size=32,
        max_new_tokens=256,
    )
    logger.info("Qwen3 ASR model loaded successfully.")
    return model


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I'm your voice recording bot.\n\n"
        "Please send me a voice recording, and I'll save it to disk."
    )

    # Load the ASR model if not already loaded
    logger.info("Loading ASR model")
    if "asr_model" not in context.bot_data:
        context.bot_data["asr_model"] = load_asr_model()


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

        # Send confirmation that conversion is in progress
        await update.message.reply_text(
            f"✅ Voice recording saved successfully!\n"
            f"📁 Location: {file_path}\n\n"
            f"🔄 Converting to text..."
        )

        # Send the converted wav file
        await update.message.reply_document(wav_path)

        # Get the ASR model from context
        model = context.bot_data.get("asr_model")
        if model:
            # Read the wav file and transcribe
            wav_bytes = wav_path.read_bytes()
            audio_data, sample_rate = _read_wav_from_bytes(wav_bytes)

            # Transcribe the audio
            results = model.transcribe(
                audio=(audio_data, sample_rate),
                language=None,
            )

            # Send the transcribed text
            transcribed_text = results[0].text
            await update.message.reply_text(
                f"✅ Voice recording converted to WAV!\n"
                f"📝 Transcribed text:\n"
                f"{transcribed_text}"
            )
        else:
            await update.message.reply_text(
                f"✅ Voice recording converted to WAV!\n"
                f"📁 Location: {wav_path}\n\n"
                f"⚠️ ASR model not loaded yet."
            )
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

