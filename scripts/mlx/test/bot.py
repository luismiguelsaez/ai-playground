from colorama import Fore
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

model, tokenizer = load("LiquidAI/LFM2.5-1.2B-Instruct")
modelv, tokenizerv = load("Qwen/Qwen3-0.6B")

sampler = make_sampler(
    top_p=0.1,
    top_k=50,
    min_p=0.01,
    temp=0.1,
)

messages = []

while True:
    user_input = input(f"{Fore.BLUE}User: ")

    messages.append({"role": "user", "content": user_input})
    prompt = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
    )

    system = ""
    print(f"{Fore.RED}System: ", end="")
    for response in stream_generate(
        model, tokenizer, prompt, sampler=sampler, max_tokens=2048
    ):
        print(f"{Fore.RED}{response.text}", end="", flush=True)
        system += response.text
    print()

    messages.append({"role": "assistant", "content": system})
