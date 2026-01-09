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
        "--output-audio", type=str, required=True, help="Output audio file path"
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

    wav = model.generate(
        text,
        language_id=language_id,
        audio_prompt_path=INPUT_AUDIO_PROMPT,
        exaggeration=2.0,
        cfg_weight=0.5,
    )

    ta.save(args.output_audio, wav, model.sr)


if __name__ == "__main__":
    main()
