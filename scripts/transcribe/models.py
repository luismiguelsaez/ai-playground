from qwen_asr import Qwen3ASRModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from diffusers import Flux2KleinPipeline
import torch

from pathlib import Path
import soundfile as sf
import numpy as np
import io
from pydub import AudioSegment
from typing import AnyStr, Tuple


class Diffuser:
    def __init__(
        self,
        checkpoint: str = "black-forest-labs/FLUX.2-klein-4B",
        device: str = "auto",
    ):
        self.checkpoint = checkpoint
        self.device = device
        self.dtype = torch.bfloat16
        self._model_loaded = False

    def load_model(self):
        self.pipe = Flux2KleinPipeline.from_pretrained(
            self.checkpoint, torch_dtype=self.dtype
        )
        self._model_loaded = True

    def generate(
        self, prompt: str, image_path: str, height: int = 1024, width: int = 1024
    ):
        self.pipe.enable_model_cpu_offload()
        self.image = self.pipe(
            prompt,
            height=height,
            width=width,
            guidance_scale=4.0,
            num_inference_steps=4,
            generator=torch.Generator(device=self.device).manual_seed(0),
        ).images[0]
        self.image.save(image_path)


class Transcriber:
    def __init__(
        self,
        checkpoint: str = "Qwen/Qwen3-ASR-1.7B",
        device: str = "auto",
    ):
        self.checkpoint = checkpoint
        self.device = device

    def _read_wav_from_bytes(self, audio_bytes: bytes) -> tuple[np.ndarray, int]:
        """Read WAV audio data from bytes."""
        with io.BytesIO(audio_bytes) as f:
            wav, sr = sf.read(f, dtype="float32", always_2d=False)
        return np.asarray(wav, dtype=np.float32), int(sr)

    def _convert_ogg_to_wav(self, ogg_path: Path, output_dir: Path) -> Path:
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

    def load_model(self):
        self.model = Qwen3ASRModel.from_pretrained(
            "Qwen/Qwen3-ASR-1.7B",
            dtype=torch.bfloat16,
            device_map="cuda:0",
            attn_implementation="flash_attention_2",
            max_inference_batch_size=32,
            max_new_tokens=256,
        )

    def transcribe(self, data: bytes) -> Tuple[AnyStr, AnyStr]:
        results = self.model.transcribe(
            audio=self._read_wav_from_bytes(data),
            language=None,
        )

        transcribed_lang = results[0].language
        transcribed_text = results[0].text

        return transcribed_lang, transcribed_text


class Chat:
    def __init__(
        self,
        checkpoint: str = "LiquidAI/LFM2.5-1.2B-Instruct",
        stream: bool = True,
        max_new_tokens: int = 512,
        quantization: bool = False,
        device: str = "auto",
        system_msg: str = "You are a chat bot that responds using markdown syntax",
    ):
        self.checkpoint = checkpoint
        self.stream = stream
        self.max_new_tokens = max_new_tokens
        self.quantization = quantization
        self.device = device
        self.system_msg = system_msg
        self.messages = [{"role": "system", "content": self.system_msg}]

    def load_model(self):
        if self.quantization and self.device != "mps":
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        else:
            quantization_config = None
        self.model = AutoModelForCausalLM.from_pretrained(
            self.checkpoint,
            device_map=self.device,
            quantization_config=quantization_config,
            trust_remote_code=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.checkpoint, skip_special_tokens=True
        )

    def clear(self):
        self.messages = [{"role": "system", "content": self.system_msg}]

    def generate(self, message: str):
        user_msg = message

        self.messages.append({"role": "user", "content": user_msg})

        inputs = self.tokenizer.apply_chat_template(
            self.messages,
            return_dict=True,
            tokenize=True,
            return_tensors="pt",
            add_generation_prompt=True,
        ).to(self.model.device)

        inputs_len = inputs["input_ids"].shape[-1]

        generation_config = inputs
        generation_config["max_new_tokens"] = self.max_new_tokens
        generation_config["use_cache"] = True

        outputs = self.model.generate(**generation_config)
        decoded_outputs = self.tokenizer.decode(
            outputs[0][inputs_len:], skip_special_tokens=True
        )
        self.messages.append({"role": "system", "content": decoded_outputs})

        return decoded_outputs
