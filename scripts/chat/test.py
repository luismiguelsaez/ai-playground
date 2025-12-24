from sys import argv

from colorama import Fore
from transformers import AutoModelForCausalLM, AutoTokenizer

MAX_NEW_TOKENS = 10000

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B", device_map="cuda:0")
messages = [
    {
        "role": "user",
        "content": argv[1],
    },
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

print(f"{Fore.GREEN}Input IDs: {Fore.RESET}", end="")
for t in inputs["input_ids"][0].tolist():
    print(f"{Fore.BLUE}{t}{Fore.RESET}", end=" ")
print()

outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)

print(f"{Fore.GREEN}Output IDs: {Fore.RESET}", end="")
inputs_shape = inputs["input_ids"].shape[-1]
c = 0
for t in outputs[0].tolist():
    if c < inputs_shape:
        print(f"{Fore.BLUE}{t}{Fore.RESET}", end=" ")
        c += 1
    else:
        print(f"{Fore.RED}{t}{Fore.RESET}", end=" ")
print()

decoded_outputs = tokenizer.decode(outputs[0][inputs_shape:], skip_special_tokens=True)
print(f"{Fore.GREEN}Outputs decoded:\n{Fore.RED}{decoded_outputs}{Fore.RESET}")
