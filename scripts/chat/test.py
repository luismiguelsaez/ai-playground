from transformers import AutoTokenizer, AutoModelForCausalLM
from colorama import Fore
from sys import argv

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
    print(f"{Fore.RED}{t}{Fore.RESET}", end=" ")
print()

outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)

print(f"{Fore.GREEN}Output IDs: {Fore.RESET}", end="")
for t in outputs[0].tolist():
    print(f"{Fore.RED}{t}{Fore.RESET}", end=" ")
print()

print(
    f"{Fore.GREEN}Outputs decoded:\n{Fore.RED}{tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1] :])}{Fore.RESET}"
)
