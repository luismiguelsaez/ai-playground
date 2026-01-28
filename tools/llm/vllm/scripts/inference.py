from vllm import LLM, SamplingParams
from os import environ

environ["CUDA_VISIBLE_DEVICES"] = "2"
environ["VLLM_TARGET_DEVICE"] = "cuda:1"

sampling_params = SamplingParams(temperature=0.1, top_p=0.1)
llm = LLM(
    model="LiquidAI/LFM2.5-1.2B-Instruct",
    kv_cache_dtype="fp8",
    calculate_kv_scales=True,
    gpu_memory_utilization=0.25,
)
prompt = "London is the capital of"
out = llm.generate(prompt, sampling_params)[0].outputs[0].text
print(out)
