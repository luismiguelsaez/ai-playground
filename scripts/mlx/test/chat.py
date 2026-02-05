from threading import Thread
from time import perf_counter
from typing import AnyStr

from colorama import Fore, Style
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextIteratorStreamer,
)


class Chat:
    def __init__(
        self,
        checkpoint: str,
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

    def read_file(file_path: str) -> [str]:
        """
        Read file contents from the file system

        Args:
            file_path: The location of the file in the local file system
        """
        return "Example file contents"

    def _load_model(self):
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

    def start(self):
        self._load_model()
        while True:
            user_msg = input(f"{Fore.RED}> User: ")
            print(Fore.RESET, end="")

            if user_msg == "quit":
                break
            if user_msg == "reset":
                self.messages = []
                continue

            self.messages.append({"role": "user", "content": user_msg})

            print(f"{Style.DIM}Generating inputs ...{Style.RESET_ALL}")
            inputs_t_start = perf_counter()
            inputs = self.tokenizer.apply_chat_template(
                self.messages,
                return_dict=True,
                tokenize=True,
                return_tensors="pt",
                add_generation_prompt=True,
                tools=[self.read_file],
            ).to(self.model.device)
            inputs_t_end = perf_counter()
            inputs_t_elapsed = inputs_t_end - inputs_t_start
            inputs_len = inputs["input_ids"].shape[-1]
            print(
                f"{Style.DIM}Generated inputs[{inputs_len}][{inputs_t_elapsed:.5f}]: {inputs['input_ids'].tolist()}{Style.RESET_ALL}"
            )

            print(f"{Style.DIM}Generating outputs ...{Style.RESET_ALL}")
            outputs_t_start = perf_counter()

            if self.stream:
                streamer = TextIteratorStreamer(
                    tokenizer=self.tokenizer, skip_prompt=True, skip_special_tokens=True
                )
                generation_config = inputs
                generation_config["streamer"] = streamer
                generation_config["max_new_tokens"] = self.max_new_tokens
                tread = Thread(target=self.model.generate, kwargs=generation_config)
                tread.start()

                system_msg = ""
                print(f"{Fore.BLUE}> System: ", end="")
                for t in streamer:
                    print(t, end="", flush=True)
                    system_msg += t
                print()

                outputs_t_end = perf_counter()
                outputs_t_elapsed = outputs_t_end - outputs_t_start
                outputs_len = len(system_msg)
                print(
                    f"{Style.DIM}Generated outputs[{outputs_len}][{outputs_t_elapsed:.5f}]{Style.RESET_ALL}"
                )
                self.messages.append({"role": "system", "content": system_msg})
            else:
                generation_config = inputs
                generation_config["streamer"] = None
                generation_config["max_new_tokens"] = self.max_new_tokens
                outputs = self.model.generate(**generation_config)
                outputs_t_end = perf_counter()
                outputs_t_elapsed = outputs_t_end - outputs_t_start
                outputs_len = len(outputs[0])
                print(
                    f"{Style.DIM}Generated outputs[{outputs_len}][{outputs_t_elapsed:.5f}]: {outputs[0][inputs_len:].tolist()}{Style.RESET_ALL}"
                )
                decoded_outputs = self.tokenizer.decode(
                    outputs[0][inputs_len:], skip_special_tokens=True
                )
                print(f"{Fore.BLUE}> System: {decoded_outputs}")
                self.messages.append({"role": "system", "content": decoded_outputs})


def main():
    chat = Chat(
        checkpoint="LiquidAI/LFM2.5-1.2B-Instruct",
        stream=True,
        max_new_tokens=2048,
        quantization=True,
        device="mps",
    )
    chat.start()


if __name__ == "__main__":
    main()


def main():
    chat = Chat(
        checkpoint="LiquidAI/LFM2.5-1.2B-Instruct", stream=True, max_new_tokens=2048
    )
    chat.start()


if __name__ == "__main__":
    main()
