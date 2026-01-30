#!/usr/bin/env bash

# Documentation
# - Server arguments: https://docs.vllm.ai/en/latest/cli/serve/#arguments
#

CHECKPOINT="LiquidAI/LFM2.5-1.2B-Instruct"

vllm serve --config ./config.yaml
#  --model=$CHECKPOINT \
#  --kv-cache-dtype=fp8 \
#  --calculate-kv-scales \
#  --gpu-memory_utilization=0.25 \
#  --max-num_batched_tokens=8192 \
#  --max-num_seqs=256 \
#  --max-model_len=8192 \
#  --cpu-offload_gb=0 \
#  --tensor-parallel_size=1 \
#  --pipeline-parallel_size=1
