#!/bin/bash

export NVIDIA_VISIBLE_DEVICES=0
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

./ik_llama.cpp/build/bin/llama-server \
  --model ~/.cache/huggingface/hub/Sepolian_Huihui-Qwen3.5-27B-Claude-4.6-Opus-abliterated-Q4_K_M_Huihui-Qwen3.5-27B-Claude-4.6-Opus-abliterated-Q4_K_M.gguf \
  --alias coding-agent \
  --host 0.0.0.0 \
  --port 8000 \
  -ngl 99 \
  -c 262144 \
  -np 1 \
  --jinja \
  --cache-type-k q4_0 \
  --cache-type-v q4_0 \
  --flash-attn on \
  --temp 0.6 \
  --top-p 0.95 \
  --min-p 0.0 \
  --top-k 20 \
  --presence-penalty 0.0 \
  --repeat-penalty 1.0 \
  --chat-template-kwargs '{"enable_thinking": false}' \
  >/tmp/llamacpp.log 2>&1 &
