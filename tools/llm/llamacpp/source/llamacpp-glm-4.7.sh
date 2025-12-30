#!/bin/bash

# Doc: https://unsloth.ai/docs/models/glm-4.7

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

CPU_OFFLOAD=".ffn_.*_exps.=CPU"                                                    # Offload all MoE layers
CPU_OFFLOAD="\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU" # Offload gate, up and down MoE layers from 6th layer onwards
CPU_OFFLOAD=-".ffn_(up)_exps.=CPU"                                                 # Offload only up projection layers
CPU_OFFLOAD=-".ffn_(up|down)_exps.=CPU"                                            # Offload projection layers

./llama.cpp/build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8002 \
  --hf-repo unsloth/GLM-4.7-GGUF:IQ4_XS \
  --alias glm4.7 \
  --threads 42 \
  --ctx-size 16384 \
  --flash-attn on \
  --temp 1.0 \
  --top-k 40 \
  --top-p 0.95 \
  --jinja \
  -ot "${CPU_OFFLOAD}" \
  --fit on \
  --cache-type-k q4_1 \
  --cache-type-v q4_1 \
  >/tmp/llamacpp.log 2>&1 &
