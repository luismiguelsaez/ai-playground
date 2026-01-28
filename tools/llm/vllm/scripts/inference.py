from vllm import LLM, SamplingParams
from vllm.entrypoints.openai import api_server
from os import environ

# environ["CUDA_VISIBLE_DEVICES"] = "4"
# environ["VLLM_TARGET_DEVICE"] = "cuda:1"
environ["DYN_KVBM_CPU_CACHE_GB"] = "0"

model = "kaitchup/LFM2.5-1.2B-Thinking-AWQ-W4A16-ASYM"

sampling_params = SamplingParams(temperature=0.1, top_p=0.1)
llm = LLM(
    model=model,
    kv_cache_dtype="fp8",
    calculate_kv_scales=True,
    gpu_memory_utilization=0.25,
    max_num_batched_tokens=8192,
    max_num_seqs=256,
    max_model_len=8192,
    cpu_offload_gb=0,
    tensor_parallel_size=1,
    pipeline_parallel_size=1,
    disable_log_stats=False,
)

prompt = "London is the capital of"
out = llm.generate(prompt, sampling_params)[0].outputs[0].text
print(out)
