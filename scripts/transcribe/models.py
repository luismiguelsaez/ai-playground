from qwen_asr import Qwen3ASRModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch


def load_asr_model() -> Qwen3ASRModel:
    model = Qwen3ASRModel.from_pretrained(
        "Qwen/Qwen3-ASR-1.7B",
        dtype=torch.bfloat16,
        device_map="cuda:0",
        attn_implementation="flash_attention_2",
        max_inference_batch_size=32,
        max_new_tokens=256,
    )
    return model


class Chat:
    def __init__(
        self,
        checkpoint: str = "LiquidAI/LFM2.5-1.2B-Instruct",
        stream: bool = True,
        max_new_tokens: int = 512,
        quantization: bool = False,
        device: str = "auto",
    ):
        self.checkpoint = checkpoint
        self.stream = stream
        self.max_new_tokens = max_new_tokens
        self.quantization = quantization
        self.device = device
        self.messages = []

    def load_model(self):
        if self.quantization and self.device != "mps":
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        else:
            quantization_config = None
        self.model = AutoModelForCausalLM.from_pretrained(
            self.checkpoint,
            device_map=self.device,
            quantization_config=quantization_config,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.checkpoint, skip_special_tokens=True
        )

    def clear(self):
        self.messages = []

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

        outputs = self.model.generate(**generation_config)
        decoded_outputs = self.tokenizer.decode(
            outputs[0][inputs_len:], skip_special_tokens=True
        )
        self.messages.append({"role": "system", "content": decoded_outputs})

        return decoded_outputs
