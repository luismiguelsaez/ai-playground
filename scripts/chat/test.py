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

print(f"{Fore.GREEN}Input IDs:\n{Fore.RED}{inputs['input_ids']}{Fore.RESET}")
print(
    f"{Fore.GREEN}Input IDs shape:\n{Fore.RED}{inputs['input_ids'].shape}{Fore.RESET}"
)

outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)

print(f"{Fore.GREEN}Outputs:\n{Fore.RED}{outputs}{Fore.RESET}")
print(
    f"{Fore.GREEN}Outputs decoded:\n{Fore.RED}{tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1] :])}{Fore.RESET}"
)
