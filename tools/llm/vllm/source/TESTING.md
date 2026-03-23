# Testing


## Nvidia Nemotron 3 Nano 30B NVFP4

```bash
#VLLM_FLASHINFER_MOE_BACKEND=throughput \
#VLLM_USE_FLASHINFER_MOE_FP4=1 \
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
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

## Nvidia Nemotron 3 Super 120B A12B NVFP4 ( [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/vllm_cookbook.ipynb) )

- VRAM: `88.051Gi`

```bash
# curl -sL https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4/resolve/main/super_v3_reasoning_parser.py -o config/plugins/reasoning/super_v3_reasoning_parser.py
VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 \
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
vllm serve nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4 \
  --port 8000 \
  --async-scheduling \
  --served-model-name model \
  --kv-cache-dtype fp8 \
  --tensor-parallel-size 1 \
  --swap-space 0 \
  --trust-remote-code \
  --attention-backend TRITON_ATTN \
  --gpu-memory-utilization 0.9 \
  --enable-chunked-prefill \
  --max-num-seqs 512 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --reasoning-parser-plugin config/plugins/reasoning/super_v3_reasoning_parser.py \
  --reasoning-parser super_v3
```

## Qwen 2.5 35B/122B AWQ/NVFP4 4bit ( [Recipe](https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3.5.html) )

- Models
  - `cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit` - OK
  - `Sehyo/Qwen3.5-122B-A10B-NVFP4`
  - `Sehyo/Qwen3.5-35B-A3B-NVFP4`

### 1 x RTX Pro 6000

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
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


### 2 x RTX 3090

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2,3 \
vllm serve cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit \
  --port 8000 \
  --served-model-name model \
  --tensor-parallel-size 1 \
  --enable-auto-tool-choice \
  --no-enforce-eager \
  --language-model-only \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --gpu-memory-utilization 0.80
```


## Qwen 3.5 27B NVFP4

- Models
  - `cyankiwi/Qwen3.5-27B-AWQ-4bit`

### 2 x RTX 3090

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2,3 \
vllm serve cyankiwi/Qwen3.5-27B-AWQ-4bit \
  --port 8000 \
  --served-model-name model \
  --tensor-parallel-size 2 \
  --enable-auto-tool-choice \
  --enable-prefix-caching \
  --language-model-only \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --gpu-memory-utilization 0.80
```


## Qwen 3.5 122B NVFP4

### 1 x RTX Pro 6000

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
vllm serve Sehyo/Qwen3.5-122B-A10B-NVFP4 \
  --port 8000 \
  --served-model-name model \
  --enable-auto-tool-choice \
  --enable-prefix-caching \
  --language-model-only \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3 \
  --kv-cache-dtype fp8 \
  --language-model-only \
  --gpu-memory-utilization 0.95
```

*Out of memory*

## Minimax M2.5 AWQ

### 1 x RTX Pro 6000

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1,2 \
HF_HOME=$HOME/.cache/huggingface \
HUGGINGFACE_HUB_CACHE=$HF_HOME/hub \
PYTORCH_ALLOC_CONF=expandable_segments:True,max_split_size_mb:512 \
VLLM_SLEEP_WHEN_IDLE=1 \
vllm serve mratsim/MiniMax-M2.5-FP8-INT4-AWQ \
  --served-model-name model \
  --quantization modelopt \
  --trust-remote-code \
  --tensor-parallel-size 2 \
  --enable-auto-tool-choice \
  --override-generation-config '{"temperature": 1, "top_p": 0.95, "top_k": 40, "repetition_penalty": 1.1, "frequency_penalty": 0.40}' \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2
```

