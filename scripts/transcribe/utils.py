"""
Utility functions for the Telegram bot application.
"""

from pathlib import Path

from pydub import AudioSegment


def convert_ogg_to_wav(ogg_path: Path, output_dir: Path) -> Path:
    """
    Convert an .ogg file to .wav format.

    Args:
        ogg_path: Path to the source .ogg file
        output_dir: Directory where the .wav file will be saved

    Returns:
        Path to the converted .wav file
    """
    # Load the ogg file
    audio = AudioSegment.from_ogg(ogg_path)

    # Generate output filename with .wav extension
    wav_filename = ogg_path.stem + ".wav"
    wav_path = output_dir / wav_filename

    # Export as wav
    audio.export(wav_path, format="wav")

    return wav_path