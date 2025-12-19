from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
from colorama import Fore
import torch
import time

checkpoint = "Qwen/Qwen3-0.6B"

load_start_time = time.perf_counter()
print(f"\n{Fore.RED}Loading model{Fore.RESET}")

model = AutoModelForCausalLM.from_pretrained(
    checkpoint, device_map="cuda:0", dtype=torch.bfloat16
)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

load_end_time = time.perf_counter()
print(
    f"{Fore.RED}Model loading time: {load_end_time - load_start_time:.6f} seconds{Fore.RESET}"
)

messages = []

while True:
    user_message = input(f"\n{Fore.RED}- User: {Fore.RESET}")

    if user_message == "quit":
        break

    messages.append({"role": "user", "content": user_message})

    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False, return_attention_mask=True
    )

    input_ids = tokenizer.encode(inputs, return_tensors="pt").to(model.device)

    streamer = TextIteratorStreamer(
        tokenizer=tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    generation_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        max_new_tokens=2048,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )

    start_time = time.perf_counter()

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    print(f"{Fore.GREEN}System: {Fore.RESET}", end="")
    for new_token in streamer:
        print(f"{Fore.MAGENTA}{new_token}{Fore.RESET}", end="", flush=True)

    end_time = time.perf_counter()

    thread.join()
