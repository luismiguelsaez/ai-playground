#!/bin/bash

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

./llama.cpp/build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8002 \
  --hf-repo unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF:Q4_K_M \
  --alias qwen3-next \
  --ctx-size 32768 \
  --n-predict 32768 \
  --no-context-shift \
  --flash-attn on \
  --temp 1.0 \
  --top-k 40 \
  --top-p 0.95 \
  --jinja \
  --tensor-split 1,1,1,1 \
  --gpu-layers 999 \
  >/tmp/llamacpp.log 2>&1 &
