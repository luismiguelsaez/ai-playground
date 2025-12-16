
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

DEVICE = "cuda"

model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)

AUDIO_PROMPT_PATH = "/input/hola-paquito.opus"

text = "Hola Paquito. Que sepas que te deseo una feliz navidad y próspero año nuevo"
wav = model.generate(text, language_id="es", audio_prompt_path=AUDIO_PROMPT_PATH)
ta.save("/output/diana-navidad.wav", wav, model.sr)

