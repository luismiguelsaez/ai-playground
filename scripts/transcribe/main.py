import torch
from qwen_asr import Qwen3ASRModel
import numpy as np
import soundfile as sf
import io
from typing import Tuple
from pathlib import Path


def _read_wav_from_bytes(audio_bytes: bytes) -> Tuple[np.ndarray, int]:
    with io.BytesIO(audio_bytes) as f:
        wav, sr = sf.read(f, dtype="float32", always_2d=False)
    return np.asarray(wav, dtype=np.float32), int(sr)


with open("samples/harvard.wav", "rb") as f:
    data = f.read()
# data = Path("samples/harvard.wav").read_bytes()


model = Qwen3ASRModel.from_pretrained(
    "Qwen/Qwen3-ASR-1.7B",
    dtype=torch.bfloat16,
    device_map="cuda:0",
    attn_implementation="flash_attention_2",
    max_inference_batch_size=32,  # Batch size limit for inference. -1 means unlimited. Smaller values can help avoid OOM.
    max_new_tokens=256,  # Maximum number of tokens to generate. Set a larger value for long audio input.
)

results = model.transcribe(
    # audio="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav",
    audio=_read_wav_from_bytes(data),
    language=None,
)

print(f"Transcribed audio in {results[0].language}")
print(results[0].text)
