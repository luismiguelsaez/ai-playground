from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
from termcolor import colored
import logging
from torch import bfloat16
from torch.cuda import is_available


class Chat:
    def __init__(
        self,
        checkpoint: str,
        device: str = "auto",
        max_new_tokens: int = 1024,
        quantize: bool = False,
    ):
        self.checkpoint = checkpoint
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.quantize = quantize

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self._load_model()

    def _load_model(self):
        if not self.quantize:
            logging.debug("Quantization disabled, not setting quantization config")
            quantization_config = None
        else:
            logging.debug("Quantization enabled, setting quantization config")
            from transformers import BitsAndBytesConfig

            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="fp4",
                bnb_4bit_compute_dtype=bfloat16,
            )

        logging.info(f"Loading model: {self.checkpoint}")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.checkpoint,
            device_map=self.device,
            quantization_config=quantization_config,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)

    def start(self):
        streamer = TextIteratorStreamer(
            tokenizer=self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        messages = []

        while True:
            print()
            user_msg = input(colored("User: ", "red"))

            messages.append({"role": "user", "content": user_msg})

            if user_msg == "quit":
                print(colored("\nBye!", "green"))
                break

            if user_msg == "clear":
                messages.clear()
                print(colored("\nHistory cleared.", "yellow"))
                continue

            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt",
                tokenize=True,
                enable_thinking=True,
            ).to(self.model.device)

            generation_config = dict(
                inputs=inputs,
                streamer=streamer,
                do_sample=True,  # Whether or not to use sampling ; use greedy decoding otherwise.
                max_new_tokens=self.max_new_tokens,  # The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
                use_cache=True,
                # temperature = 0.6,                    # The value used to module the next token probabilities. This value is set in a model's generation_config.json file. If it isn't set, the default value is 1.0
                # top_p = 0.95,                         # If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation. This value is set in a model's generation_config.json file. If it isn't set, the default value is 1.0
                # use_cache = True,
                # top_k = 20,                           # The number of highest probability vocabulary tokens to keep for top-k-filtering. This value is set in a model's generation_config.json file. If it isn't set, the default value is 50.
                # min_p = 0,                            # Minimum token probability, which will be scaled by the probability of the most likely token. It must be a value between 0 and 1. Typical values are in the 0.01-0.2 range, comparably selective as setting top_p in the 0.99-0.8 range (use the opposite of normal top_p values).
            )

            thread = Thread(target=self.model.generate, kwargs=generation_config)
            thread.start()

            assistant_msg = ""
            assistant_thinking = False
            token_count = 0

            print(colored("Assistant: ", "blue"), end="")
            for token in streamer:
                token_count += 1

                if token == "\n\n":
                    assistant_thinking = True
                if token == "\n\n\n\n":
                    assistant_thinking = False

                if not assistant_thinking and token != "\n\n\n\n":
                    assistant_msg += token
                    print(colored(token, "light_blue"), end="", flush=True)
                else:
                    print(colored(token, "light_grey"), end="", flush=True)

            print()

            logging.debug(colored(f"Tokens: {token_count}", "green"))

            messages.append({"role": "assistant", "content": assistant_msg})


def main():
    checkpoint = "LiquidAI/LFM2.5-1.2B-Instruct"
    checkpoint = "Qwen/Qwen3-4B-Instruct-2507"
    checkpoint = "Nanbeige/Nanbeige4.1-3B"
    device = "cuda:0" if is_available() else "cpu"
    chat = Chat(
        checkpoint=checkpoint, device=device, quantize=True, max_new_tokens=32000
    )
    chat.start()


if __name__ == "__main__":
    main()
