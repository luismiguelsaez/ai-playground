from sys import argv

from colorama import Fore
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

MAX_NEW_TOKENS = 10000

checkpoints = ["LiquidAI/LFM2-2.6B-Exp", "Qwen/Qwen3-0.6B"]

tokenizer = AutoTokenizer.from_pretrained(checkpoints[0])
model = AutoModelForCausalLM.from_pretrained(checkpoints[0], device_map="cuda:3")

streamer = TextIteratorStreamer(tokenizer=tokenizer, skip_prompt=True)

messages = [
    {
        "role": "user",
        "content": argv[1],
    },
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=False,
    return_dict=False,
)

tokens = tokenizer.tokenize(inputs)
print(f"{Fore.GREEN}Tokens:{Fore.RESET}\n{Fore.BLUE}{tokens}{Fore.RESET}")

print(f"{Fore.GREEN}Inputs:{Fore.RESET}\n{Fore.BLUE}{inputs}{Fore.RESET}")
input_ids = tokenizer.encode(inputs, return_tensors="pt").to(model.device)

print(f"{Fore.GREEN}Input IDs: {Fore.RESET}", end="")
for t in input_ids[0].tolist():
    print(f"{Fore.BLUE}{t}{Fore.RESET}", end=" ")
print()

outputs = model.generate(
    input_ids,
    max_new_tokens=MAX_NEW_TOKENS,
    repetition_penalty=1.05,
)

print(f"{Fore.GREEN}Output IDs: {Fore.RESET}", end="")
inputs_len = len(input_ids[0])
c = 0
for t in outputs[0].tolist():
    if c < inputs_len:
        print(f"{Fore.BLUE}{t}{Fore.RESET}", end=" ")
        c += 1
    else:
        print(f"{Fore.RED}{t}{Fore.RESET}", end=" ")
print()

decoded_outputs = tokenizer.decode(outputs[0][inputs_len:], skip_special_tokens=True)
print(f"{Fore.GREEN}Outputs decoded:\n{Fore.RED}{decoded_outputs}{Fore.RESET}")
