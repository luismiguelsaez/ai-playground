#!/bin/bash

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

./llama.cpp/build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8002 \
  --model "/home/luismi/.cache/huggingface/hub/unsloth_GLM-4.5-Air-GGUF_Q5_K_S_GLM-4.5-Air-Q5_K_S-00001-of-00002.gguf" \
  --alias glm4.5-air \
  -t 32 \
  --n-cpu-moe 4 \
  --ctx-size 32684 \
  --temp 0.8 \
  --top-k 40 \
  --top-p 0.9 \
  >/tmp/llamacpp.log 2>&1 &
