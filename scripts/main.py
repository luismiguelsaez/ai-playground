from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, BitsAndBytesConfig
from colorama import Fore, Style
from threading import Thread
from time import sleep

model_name = "Qwen/Qwen3-0.6B"
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype="auto",
    device_map="auto",
)

messages = []

while True:
    msg = str(input(f"{Fore.RED}\n\nUser: {Fore.RESET}"))

    exit(0) if msg == "quit" else None

    messages.append({"role": "user", "content": msg})

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )

    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generation_args = {
        "max_new_tokens": 32768,
        "streamer": streamer,
        **model_inputs,
    }

    thread = Thread(
        target=model.generate,
        kwargs=generation_args,
    )
    thread.start()

    resp = ""
    for text_token in streamer:
        sleep(0.01)
        print(
            f"{Fore.LIGHTGREEN_EX}{Style.DIM}{text_token}{Style.RESET_ALL}{Fore.RESET}",
            end="",
        )
        resp += text_token

    messages.append({"role": "assistant", "content": resp})

