#!/bin/bash

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

./llama.cpp/build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8002 \
  --hf-repo unsloth/Nemotron-3-Nano-30B-A3B-GGUF \
  --hf-file Nemotron-3-Nano-30B-A3B-Q4_K_M.gguf \
  --alias nvidia-nemotron-3-nano-30b \
  --gpu-layers -1 \
  --tensor-split 1,1 \
  --split-mode layer \
  --ctx-size 32684 \
  --temp 0.8 \
  --top-k 40 \
  --top-p 0.9
