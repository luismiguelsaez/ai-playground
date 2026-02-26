# Testing


## Nvidia Nemotron 3 Nano 30B NVFP4

```bash
#VLLM_FLASHINFER_MOE_BACKEND=throughput \
#VLLM_USE_FLASHINFER_MOE_FP4=1 \
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
vllm serve nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 \
  --port 8000 \
  --served-model-name model \
  --max-num-seqs 8 \
  --tensor-parallel-size 1 \
  --max-model-len 262144 \
  --trust-remote-code \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --reasoning-parser-plugin config/plugins/reasoning/nano_v3_reasoning_parser.py \
  --reasoning-parser nano_v3 \
  --kv-cache-dtype fp8
```


## Qwen 2.5 35B/122B AWQ/NVFP4 4bit ( [Recipe](https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3.5.html) )

- Models
  - `cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit` - OK
  - `Sehyo/Qwen3.5-122B-A10B-NVFP4`
  - `Sehyo/Qwen3.5-35B-A3B-NVFP4`

### 1 x RTX Pro 6000

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
vllm serve Sehyo/Qwen3.5-35B-A3B-NVFP4 \
  --port 8000 \
  --served-model-name model \
  --tensor-parallel-size 1 \
  --max-model-len 262144 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --enable-prefix-caching \
  --gpu-memory-utilization 0.5
```


### 4 x RTX 3090 

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0,1 \
vllm serve cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit \
  --port 8000 \
  --served-model-name model \
  --tensor-parallel-size 2 \
  --max-model-len 20000 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --gpu-memory-utilization 0.9
```

