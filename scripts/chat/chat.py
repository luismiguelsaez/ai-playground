from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
from termcolor import colored
import logging

class Chat():
    def __init__(self, checkpoint: str, device: str = "auto", max_new_tokens: int = 1024, quantize: bool = False):
        self.checkpoint = checkpoint
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.quantize = quantize

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        if not self.quantize:
            logging.debug("Quantization disabled, not setting quantization config")
            quantization_config = None
        else:
            logging.debug("Quantization enabled, setting quantization config")
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(load_in_4bit=True)
            
        logging.info(f"Loading model: {self.checkpoint}")
        self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint, device_map=self.device, quantization_config=quantization_config)
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)

    def start(self):
        streamer = TextIteratorStreamer(tokenizer=self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        messages = []

        while True:
            print()
            user_msg = input(colored("User: ", "red"))

            messages.append({
                "role": "user",
                "content": user_msg   
            })

            inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", tokenize=True, enable_thinking=True).to(self.model.device)

            generation_config = dict(
                inputs = inputs,
                streamer = streamer,
                do_sample = True,                     # Whether or not to use sampling ; use greedy decoding otherwise.
                max_new_tokens = self.max_new_tokens, # The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
                # temperature = 0.6,                    # The value used to module the next token probabilities. This value is set in a model’s generation_config.json file. If it isn’t set, the default value is 1.0
                # top_p = 0.95,                         # If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation. This value is set in a model’s generation_config.json file. If it isn’t set, the default value is 1.0
                # top_k = 20,                           # The number of highest probability vocabulary tokens to keep for top-k-filtering. This value is set in a model’s generation_config.json file. If it isn’t set, the default value is 50.
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

                if token == "<think>\n":
                    assistant_thinking = True
                if token == "</think>\n\n":
                    assistant_thinking = False

                if not assistant_thinking and token != "</think>\n\n":
                    assistant_msg += token
                    print(colored(token, "light_blue"), end="", flush=True)
                else:
                    print(colored(token, "light_grey"), end="", flush=True)

            print()

            logging.debug(colored(f"Tokens: {token_count}", "green"))

            messages.append({
                "role": "assistant",
                "content": assistant_msg   
            })
            

def main():
    chat = Chat(checkpoint="Qwen/Qwen3-0.6B", device="cuda:0", quantize=False, max_new_tokens=32000)
    chat.start()

if __name__ == "__main__":
    main()
