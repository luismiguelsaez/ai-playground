from vllm import LLM, SamplingParams

sampling_params = SamplingParams(temperature=0.1, top_p=0.1)
llm = LLM(
    model="LiquidAI/LFM2.5-1.2B-Instruct",
    kv_cache_dtype="fp8",
    calculate_kv_scales=True,
    gpu_memory_utilization=0.75,
)
prompt = "London is the capital of"
out = llm.generate(prompt, sampling_params)[0].outputs[0].text
print(out)