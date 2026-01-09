#!/bin/bash

# Doc: https://unsloth.ai/docs/models/glm-4.7

export NVIDIA_VISIBLE_DEVICES=all
export NVIDIA_DRIVER_CAPABILITIES=compute,utility

CPU_OFFLOAD=".ffn_.*_exps.=CPU"                                                    # Offload all MoE layers
CPU_OFFLOAD=-".ffn_(up)_exps.=CPU"                                                 # Offload only up projection layers
CPU_OFFLOAD=-".ffn_(up|down)_exps.=CPU"                                            # Offload projection layers
CPU_OFFLOAD="\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU" # Offload gate, up and down MoE layers from 6th layer onwards
CPU_OFFLOAD="\.(3[0-9]|4[0-9]|5[0-9]|6[0-9])\.ffn_(gate|up|down)_exps.=CPU"        # Offload gate, up and down MoE layers from 6th layer onwards

# blk.51.ffn_up_exps.weight
# blk.51.ffn_down_exps.weight
# blk.51.ffn_gate_exps.weight
#
# tensor blk.39.ffn_gate_exps.weight (612 MiB iq4_xs) buffer type overridden to CUDA_Host

./llama.cpp/build/bin/llama-server \
  -v \
  --host 0.0.0.0 \
  --port 8002 \
  --model ~/.cache/huggingface/hub/Ex0bit_MiniMax-M2.1-PRISM_MiniMax-M2.1-PRISM-IQ4_NL.gguf \
  --alias coding-agent \
  --threads 40 \
  --ctx-size 196608 \
  --n-predict 196608 \
  --batch-size 512 \
  --no-context-shift \
  --flash-attn on \
  --repeat-penalty 1.05 \
  --temp 1.0 \
  --top-k 40 \
  --min-p 0.0 \
  --top-p 0.95 \
  --jinja \
  --fit on \
  --reasoning-format auto \
  --no-mmap \
  --tensor-split 1,1,1,1 \
  --gpu-layers 999 \
  --override-tensor "blk\.(1|2|3|4|5|6)\.ffn_.*_exps\.weight=CPU","blk\.(17|18|19|20|21|22)\.ffn_.*_exps\.weight=CPU","blk\.(33|34|35|36|37|38)\.ffn_.*_exps\.weight=CPU","blk\.(49|50|51|52|53|54)\.ffn_.*_exps\.weight=CPU" \
  >/tmp/llamacpp.log 2>&1 &
