import torchaudio as ta
import torch
from chatterbox.tts_turbo import ChatterboxTurboTTS

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# Generate with Paralinguistic Tags
text = "Hola Paquito. Que sepas que te deseo una feliz navidad y prospero año nuevo."

# Generate audio (requires a reference clip for voice cloning)
wav = model.generate(text, audio_prompt_path="/input/hola-paquito.opus")

ta.save("/output/diana-navidad.wav", wav, model.sr)

