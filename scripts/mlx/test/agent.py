from colorama import Fore, Style
from transformers import AutoModelForCausalLM, AutoTokenizer
from time import perf_counter


checkpoint = "LiquidAI/LFM2.5-1.2B-Instruct"

print(f"Loading model [{checkpoint}] ...")
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="mps")
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
print("Model loaded")

messages = []

while True:
    user_msg = input(f"{Fore.RED}> User: ")
    print(Fore.RESET, end="")
    messages.append({"role": "user", "content": user_msg})

    print(f"{Style.DIM}Generating inputs ...{Style.RESET_ALL}")
    inputs_t_start = perf_counter()
    inputs = tokenizer.apply_chat_template(
        messages,
        return_dict=True,
        tokenize=True,
        return_tensors="pt",
        add_generation_prompt=True,
    ).to(model.device)
    inputs_t_end = perf_counter()
    inputs_t_elapsed = inputs_t_end - inputs_t_start
    inputs_len = inputs["input_ids"].shape[-1]
    print(
        f"{Style.DIM}Generated inputs[{inputs_len}][{inputs_t_elapsed:.5f}]: {inputs['input_ids'].tolist()}{Style.RESET_ALL}"
    )

    print(f"{Style.DIM}Generating outputs ...{Style.DIM}")
    outputs_t_start = perf_counter()
    outputs = model.generate(**inputs, max_new_tokens=512)
    outputs_t_end = perf_counter()
    outputs_t_elapsed = outputs_t_end - outputs_t_start
    outputs_len = len(outputs[0])
    print(
        f"{Style.DIM}Generated outputs[{outputs_len}][{outputs_t_elapsed:.5f}]: {outputs[0][inputs_len:].tolist()}{Style.RESET_ALL}"
    )
    decoded_outputs = tokenizer.decode(
        outputs[0][inputs_len:], skip_special_tokens=True
    )
    print(f"{Fore.BLUE}> System: {decoded_outputs}")
    messages.append({"role": "system", "content": decoded_outputs})
