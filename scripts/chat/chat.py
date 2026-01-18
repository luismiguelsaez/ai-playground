from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
from termcolor import colored

class Chat():
    def __init__(self, checkpoint: str, device: str = "auto", max_new_tokens: int = 1024, quantize: bool = False):
        self.checkpoint = checkpoint
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.quantize = quantize

        if not self.quantize:
            quantization_config = None
        else:
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(load_in_4bit=True)
            
        self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint, device_map=self.device, quantization_config=quantization_config)
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)

    def start(self):
        streamer = TextIteratorStreamer(tokenizer=self.tokenizer, skip_prompt=True, skip_special_tokens=False)

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
                do_sample = True,
                max_new_tokens = self.max_new_tokens,
                temperature = 0.6,
                top_p = 0.95,
                top_k = 20,
                min_p = 0,
            )

            thread = Thread(target=self.model.generate, kwargs=generation_config)
            thread.start()

            assistant_msg = ""
            print(colored("Assistant: ", "blue"), end="")
            for token in streamer:
                print(token, end="", flush=True)
                assistant_msg += token
            
            messages.append({
                "role": "assistant",
                "content": assistant_msg   
            })     
            

def main():
    chat = Chat(checkpoint="Qwen/Qwen3-8B", device="cuda:0", quantize=True, max_new_tokens=32000)
    chat.start()

if __name__ == "__main__":
    main()
