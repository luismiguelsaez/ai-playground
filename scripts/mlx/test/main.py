from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

model, tokenizer = load("LiquidAI/LFM2.5-1.2B-Instruct")
modelv, tokenizerv = load("Qwen/Qwen3-0.6B")

sampler = make_sampler(
    top_p=0.1,
    top_k=50,
    temp=0.1,
)

samplerv = make_sampler(
    top_p=0.95,
    top_k=20,
    temp=0.6,
)

messages = []
messagesv = [
    {
        "role": "system",
        "content": """
            You are in charge of verifying answers to questions.
            The user will ask you to verify the answer in this format: Verify this answer to the question 'question': 'answer'.
            Your response has to tell the user whether the answer was correct and incorrect, providing the correct answer.
        """,
    }
]

while True:
    user_input = input("User: ")

    messages.append({"role": "user", "content": user_input})
    prompt = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
    )

    system = ""
    for response in stream_generate(
        model, tokenizer, prompt, sampler=sampler, max_tokens=512
    ):
        print(response.text, end="", flush=True)
        system += response.text
    print()

    messages.append({"role": "assistant", "content": system})

    # Verify response
    print()
    print("Verify response: ")
    messagesv.append(
        {
            "role": "user",
            "content": f"Verify this answer to the question '{user_input}': '{system}'",
        }
    )
    promptv = tokenizerv.apply_chat_template(
        messagesv,
        add_generation_prompt=True,
    )

    for r in stream_generate(
        modelv, tokenizerv, promptv, sampler=samplerv, max_tokens=2048
    ):
        print(r.text, end="", flush=True)
    print()

    messages = []
