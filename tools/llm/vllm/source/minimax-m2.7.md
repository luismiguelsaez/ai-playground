# Minimax M2.7 on 2 x RTX 6000 Pro

## docs

- [Engine arguments](https://docs.vllm.ai/en/v0.4.1/models/engine_args.html)


## Hardware and architecture

- Topology

```bash
~ nvidia-smi topo -m

        GPU0    GPU1    CPU Affinity    NUMA Affinity   GPU NUMA ID
GPU0     X      NODE    0-47    0               N/A
GPU1    NODE     X      0-47    0               N/A

Legend:

  X    = Self
  SYS  = Connection traversing PCIe as well as the SMP interconnect between NUMA nodes (e.g., QPI/UPI)
  NODE = Connection traversing PCIe as well as the interconnect between PCIe Host Bridges within a NUMA node
  PHB  = Connection traversing PCIe as well as a PCIe Host Bridge (typically the CPU)
  PXB  = Connection traversing multiple PCIe bridges (without traversing the PCIe Host Bridge)
  PIX  = Connection traversing at most a single PCIe bridge
  NV#  = Connection traversing a bonded set of # NVLinks
```

- GPUs

```bash
~ nvidia-smi

Tue Apr 14 16:30:23 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 590.48.01              Driver Version: 590.48.01      CUDA Version: 13.1     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA RTX PRO 6000 Blac...    Off |   00000000:01:00.0 Off |                  Off |
| 30%   30C    P8             12W /  600W |       2MiB /  97887MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA RTX PRO 6000 Blac...    Off |   00000000:21:00.0 Off |                  Off |
| 30%   29C    P8             13W /  600W |       2MiB /  97887MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```


## First attempt

- Command

```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0,1
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export SAFETENSORS_FAST_GPU=1
export NCCL_P2P_DISABLE=1 # No NVLink — SHM is faster than P2P PCIe
export NCCL_IB_DISABLE=1  # No InfiniBand
export NCCL_SHM_DISABLE=0
export NCCL_NVLS_ENABLE=0
export OMP_NUM_THREADS=8
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

python -m vllm.entrypoints.openai.api_server \
  --model lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --tensor-parallel-size 2 \
  --attention-backend FLASH_ATTN \
  --gpu-memory-utilization 0.92 \
  --max-model-len 65536 \
  --max-num-seqs 64 \
  --max-num-batched-tokens 16384 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --host 0.0.0.0 \
  --port 8000
```

- Failure

```
(Worker_TP1 pid=4122) ERROR 04-14 16:37:13 [multiproc_executor.py:949] torch.AcceleratorError: CUDA error: the provided PTX was compiled with an unsupported toolchain.
(Worker_TP1 pid=4122) ERROR 04-14 16:37:13 [multiproc_executor.py:949] Search for `cudaErrorUnsupportedPtxVersion' in https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html for more information.
(Worker_TP1 pid=4122) ERROR 04-14 16:37:13 [multiproc_executor.py:949] CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
(Worker_TP1 pid=4122) ERROR 04-14 16:37:13 [multiproc_executor.py:949] For debugging consider passing CUDA_LAUNCH_BLOCKING=1
(Worker_TP1 pid=4122) ERROR 04-14 16:37:13 [multiproc_executor.py:949] Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

- Verify versions

```bash
$ python -c "import torch; print(torch.version.cuda)"
12.8

$ python -c "import vllm; print(vllm.__version__)"
0.19.0

$ pip show vllm | grep -E "Version|Location"
Version: 0.19.0+cu132
Location: /home/luismi/github/ai-playground/tools/llm/vllm/source/.venv/lib/python3.12/site-packages

$ nvidia-smi | grep "CUDA Version"
| NVIDIA-SMI 590.48.01              Driver Version: 590.48.01      CUDA Version: 13.1     |
```


## Second attempt

Use `--enforce-eager` to verify that the model loads. This will work but lose ~20-30% throughput vs CUDA graphs.

- Command

```bash
SAFETENSORS_FAST_GPU=1 \
NCCL_P2P_DISABLE=1 \
NCCL_IB_DISABLE=1 \
NCCL_NVLS_ENABLE=0 \
OMP_NUM_THREADS=8 \
python -m vllm.entrypoints.openai.api_server \
  --model lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 32768 \
  --max-num-seqs 32 \
  --enforce-eager \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think
```

*Still crashing on first request even though it loads*


## Third attempt

Disable flash attention

```bash
SAFETENSORS_FAST_GPU=1 \
NCCL_P2P_DISABLE=1 \
NCCL_IB_DISABLE=1 \
NCCL_NVLS_ENABLE=0 \
VLLM_ATTENTION_BACKEND=FLASHINFER \
VLLM_USE_FLASHINFER_MOE_FP4=0 \
VLLM_NVFP4_GEMM_BACKEND=cutlass \
OMP_NUM_THREADS=8 \
python -m vllm.entrypoints.openai.api_server \
  --model lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --quantization modelopt_fp4 \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 32768 \
  --max-num-seqs 32 \
  --enforce-eager \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --host 0.0.0.0 \
  --port 8000
```

*Crashes on first request as before*


## Fourth attempt ( Docker )

```bash
docker run --gpus all \
  --ipc=host --shm-size=32g \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e SAFETENSORS_FAST_GPU=1 \
  -e NCCL_P2P_DISABLE=1 \
  -e NCCL_IB_DISABLE=1 \
  -e NCCL_NVLS_ENABLE=0 \
  -e VLLM_USE_FLASHINFER_MOE_FP4=0 \
  -e VLLM_NVFP4_GEMM_BACKEND=cutlass \
  -e OMP_NUM_THREADS=8 \
  vllm/vllm-openai:latest \
  lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --quantization modelopt_fp4 \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 65536 \
  --max-num-seqs 64 \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think
```

*Works, but throughput isn't good. Likely due to CUDA graphs not being used*

```
(APIServer pid=1) INFO 04-14 15:27:05 [loggers.py:259] Engine 000: Avg prompt throughput: 884.6 tokens/s, Avg generation throughput: 36.4 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 6.7%, Prefix cache hit rate: 53.9%
```


## Fifth attempt ( Docker )

Try to use CUDA graphs by adding

```bash
# Add to model args:
--compilation-config '{"cudagraph_mode":"PIECEWISE"}' \
```

```bash
docker run --gpus all \
  --ipc=host --shm-size=32g \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e SAFETENSORS_FAST_GPU=1 \
  -e NCCL_P2P_DISABLE=1 \
  -e NCCL_IB_DISABLE=1 \
  -e NCCL_NVLS_ENABLE=0 \
  -e VLLM_USE_FLASHINFER_MOE_FP4=0 \
  -e VLLM_NVFP4_GEMM_BACKEND=cutlass \
  -e OMP_NUM_THREADS=8 \
  -e VLLM_USE_V1=1 \
  vllm/vllm-openai:latest \
  lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --quantization modelopt_fp4 \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 65536 \
  --max-num-seqs 64 \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --compilation-config '{"cudagraph_mode":"PIECEWISE"}'
```

*Works faster, but stalls at first request*

```
shm_broadcast.py: No available shared memory broadcast block found in 60 seconds
```


## Sixth attempg ( Docker )

Try to fix the initial 60 seconds stall

```bash
# Add to docker run args:
--max-num-seqs 256 \
--compilation-config '{"cudagraph_mode":"PIECEWISE","cudagraph_num_of_warmups":1,"pass_config":{"fuse_minimax_qk_norm":true}}' \
```

```bash
docker run --gpus all \
  --ipc=host --shm-size=32g \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e SAFETENSORS_FAST_GPU=1 \
  -e NCCL_P2P_DISABLE=1 \
  -e NCCL_IB_DISABLE=1 \
  -e NCCL_NVLS_ENABLE=0 \
  -e VLLM_USE_FLASHINFER_MOE_FP4=0 \
  -e VLLM_NVFP4_GEMM_BACKEND=cutlass \
  -e OMP_NUM_THREADS=8 \
  -e VLLM_USE_V1=1 \
  vllm/vllm-openai:latest \
  lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --quantization modelopt_fp4 \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 65536 \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --max-num-seqs 256 \
  --compilation-config '{"cudagraph_mode":"PIECEWISE","cudagraph_num_of_warmups":1}'
```


# Improvements

- Increase performance

```bash
--shm-size=64g \   # up from typical 32g

# NCCL tuning for PCIe Ring topology  
-e NCCL_ALGO=Ring \
-e NCCL_PROTO=Simple \
-e NCCL_MIN_NCHANNELS=8 \

# Allow larger batches
--max-num-batched-tokens 65536 \
--max-num-seqs 256 \
--gpu-memory-utilization 0.95 \
```

- Longer context

```bash
--max-model-len 524288 \   # 512K, safe starting point
--max-num-seqs 4 \          # fewer concurrent reqs to fit long contexts
--gpu-memory-utilization 0.95 \
--kv-cache-dtype fp8 \      # essential — halves KV cache memory vs bf16
--enable-chunked-prefill \  # required for long inputs
--max-num-batched-tokens 131072 \
```


# Testing

```bash
# Fire multiple requests simultaneously to test
for i in {1..8}; do
  curl -s http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"MiniMax-M2.7-NVFP4","messages":[{"role":"user","content":"Write a long essay about AI"}],"max_tokens":500}' &
done
wait

# Simple warmup script to run after container starts
until curl -sf http://localhost:8000/v1/models > /dev/null; do sleep 2; done
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"lukealonso/MiniMax-M2.7-NVFP4","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
  > /dev/null
echo "Model warmed up"
```


## Measure performance

- Using `nvidia-smi`

```
nvidia-smi dmon -s pucvmt -d 2
```

*Keep it running during inference and analyze output afterwards to see whether the GPUs where busy or not*

- From vLLM logs

```
vllm-minimax-m2.7-1  | (APIServer pid=1) INFO 04-14 17:17:00 [loggers.py:259] Engine 000: Avg prompt throughput: 1241.3 tokens/s, Avg generation throughput: 64.5 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 3.1%, Prefix cache hit rate: 1.8%
vllm-minimax-m2.7-1  | (APIServer pid=1) INFO 04-14 17:13:20 [loggers.py:259] Engine 000: Avg prompt throughput: 6.0 tokens/s, Avg generation throughput: 294.4 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.7%, Prefix cache hit rate: 63.6%
vllm-minimax-m2.7-1  | (APIServer pid=1) INFO 04-14 17:13:40 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 63.6%
```

*Check `generation throughput` ,`prompt throughput` and KV cache usage metrics*


## Verify versions match

- vLLM version

```bash
python -c "import vllm; print(vllm.__version__)"
```

- torch CUDA version

```bash
python -c "import torch; print(torch.version.cuda)"
```

- CUDA compiler version

```bash
nvcc --version
```
