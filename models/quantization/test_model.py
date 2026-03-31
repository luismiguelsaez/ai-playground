"""Test GPTQ quantized model with longer, complex prompts."""

import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

q_dir = "LFM2.5-1.2B-Instruct-GPTQ4bit"

print("Loading GPTQ quantized model...")
model = AutoModelForCausalLM.from_pretrained(q_dir, device_map="cuda:0")
tokenizer = AutoTokenizer.from_pretrained(q_dir)
device = "cuda:0"

print("Model loaded!\n")

# Complex test prompts
test_prompts = [
    {
        "role": "user",
        "content": "Explain the concept of recursion in computer science, including its advantages, disadvantages, and practical applications. Provide code examples if possible."
    },
    {
        "role": "user",
        "content": "Write a detailed technical explanation of how transformers work in large language models, including attention mechanisms, positional encoding, and the difference between encoder and decoder architectures."
    },
    {
        "role": "user",
        "content": "Compare and contrast Kubernetes and Docker. When should you use one over the other? Include use cases and practical examples."
    },
]

NUM_RUNS = 3
MAX_NEW_TOKENS = 150

def test_generation(prompt_dict):
    """Test generation for a single prompt."""
    prompt = tokenizer.apply_chat_template([prompt_dict], tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Warmup
    _ = model.generate(**inputs, max_new_tokens=20, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    torch.cuda.synchronize()

    # Benchmark runs
    times = []
    for run in range(NUM_RUNS):
        torch.cuda.synchronize()
        start = time.perf_counter()

        output = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    num_tokens = output[0].shape[0] - inputs.input_ids.shape[1]
    tps = num_tokens / avg_time

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    assistant_part = response.split("assistant")[-1].strip()

    return assistant_part, num_tokens, avg_time, tps


print("="*70)
print("EVALUATION")
print("="*70)

total_tokens = 0
total_time = 0

for i, prompt_dict in enumerate(test_prompts):
    print(f"\n{'='*70}")
    print(f"PROMPT {i+1}: {prompt_dict['content'][:80]}...")
    print(f"{'='*70}")

    response, num_tokens, avg_time, tps = test_generation(prompt_dict)

    total_tokens += num_tokens
    total_time += avg_time

    print(f"\n[Response - {num_tokens} tokens, {avg_time:.2f}s, {tps:.1f} tok/s]")
    print(f"{'-'*50}")
    print(response[:1000] + "..." if len(response) > 1000 else response)

# Summary
avg_tps = total_tokens / total_time if total_time > 0 else 0
print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(f"Total tokens generated: {total_tokens}")
print(f"Total time: {total_time:.2f}s")
print(f"Average TPS: {avg_tps:.1f} tokens/sec")