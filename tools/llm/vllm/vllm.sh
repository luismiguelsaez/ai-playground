#!/bin/bash

export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=1
export NCCL_P2P_LEVEL=NVL
export NCCL_SOCKET_IFNAME=lo
export NCCL_TIMEOUT=1800
export RAY_DEDUP_LOGS=0
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export CUDA_VISIBLE_DEVICES=0,1

source .venv/bin/activate

python3 -m vllm.entrypoints.openai.api_server --model=Qwen/Qwen2.5-Coder-32B-Instruct \
  --host=0.0.0.0 \
  --port=8000 \
  --tensor-parallel-size=2 \
  --gpu-memory-utilization=0.90 \
  --max-model-len=16384 \
  --disable-log-requests \
  --served-model-name=qwen-coder-32b \
  --trust-remote-code
