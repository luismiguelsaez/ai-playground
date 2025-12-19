#!/usr/bin/env python3

import argparse
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


def main():
    parser = argparse.ArgumentParser(
        description="Generate multilingual speech with custom inputs"
    )
    parser.add_argument(
        "--input-audio", type=str, required=True, help="Input audio prompt path"
    )
    parser.add_argument(
        "--text", type=str, required=True, help="Text for generated audio"
    )
    parser.add_argument(
        "--language-id", type=str, required=True, help="Language ID for generation"
    )

    args = parser.parse_args()

    # Store command line arguments in variables as requested
    INPUT_AUDIO_PROMPT = args.input_audio
    text = args.text
    language_id = args.language_id

    print(f"Input audio prompt: {INPUT_AUDIO_PROMPT}")
    print(f"Text for generated audio: {text}")
    print(f"Language ID: {language_id}")

    DEVICE = "cuda"

    model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)

    AUDIO_PROMPT_PATH = "/input/hola-paquito.opus"

    text = "Hola Paquito. Que sepas que te deseo una feliz navidad y próspero año nuevo"

    wav = model.generate(
        text,
        language_id=language_id,
        audio_prompt_path=AUDIO_PROMPT_PATH,
        exaggeration=0.7,
        cfg_weight=0.3
    )

    ta.save("/output/diana-navidad.wav", wav, model.sr)


if __name__ == "__main__":
    main()

