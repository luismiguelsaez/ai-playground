#!/bin/bash

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

./llama.cpp/build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8002 \
  --hf-repo unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF:Q4_K_M \
  --alias qwen3-next \
  -t 24 \
  --n-cpu-moe 38 \
  --ctx-size 32684 \
  --temp 0.8 \
  --top-k 40 \
  --top-p 0.9 \
  >/tmp/llamacpp.log 2>&1 &
