"""
Utility functions for the Telegram bot application.
"""

from pathlib import Path
import soundfile as sf
import numpy as np
import io
from pydub import AudioSegment


def read_wav_from_bytes(audio_bytes: bytes) -> tuple[np.ndarray, int]:
    """Read WAV audio data from bytes."""
    with io.BytesIO(audio_bytes) as f:
        wav, sr = sf.read(f, dtype="float32", always_2d=False)
    return np.asarray(wav, dtype=np.float32), int(sr)


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
