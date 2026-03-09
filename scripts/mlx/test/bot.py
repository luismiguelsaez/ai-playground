from colorama import Fore
from mlx_vlm import load, stream_generate
from mlx_vlm.utils import load_config
from mlx_vlm.prompt_utils import apply_chat_template

model, processor = load("mlx-community/Qwen3.5-0.8B-MLX-8bit")
config = load_config("mlx-community/Qwen3.5-0.8B-MLX-8bit")

messages = []

while True:
    user_input = input(f"{Fore.BLUE}User: ")

    prompt = apply_chat_template(
        processor=processor,
        prompt="What is a virus?",
        num_images=0,
        config=config,
    )

    system = ""
    print(f"{Fore.RED}System: ", end="")
    for response in stream_generate(
        model=model,
        processor=processor,
        prompt=prompt,
    ):
        print(f"{Fore.RED}{response.text}", end="", flush=True)
        system += response.text
    print()