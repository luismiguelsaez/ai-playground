#!/usr/bin/env bash

vllm serve cyankiwi/GLM-4.7-Flash-AWQ-4bit \
  --served-model-name=coding-agent \
  --host=0.0.0.0 \
  --port=8002 \
  --speculative-config.method mtp \
  --speculative-config.num_speculative_tokens 1 \
  --tool-call-parser glm47 \
  --reasoning-parser glm45 \
  --enable-auto-tool-choice \
  --served-model-name glm-4.7-flash \
  --tensor-parallel-size 4 \
  --max-num-seqs 1 \
  --max-model-len 40000 \
  --gpu-memory-utilization 0.95
