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
# print_info: n_layer               = 62

./llama.cpp/build/bin/llama-server \
  -v \
  --host 0.0.0.0 \
  --port 8002 \
  --model ~/.cache/huggingface/hub/Ex0bit_MiniMax-M2.1-PRISM_MiniMax-M2.1-PRISM-IQ4_NL.gguf \
  --alias coding-agent \
  --threads 42 \
  --ctx-size 120000 \
  --n-predict 120000 \
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
  --gpu-layers 99 \
  --split-mode layer \
  -ot "blk.(1|2|3|4|5|6|7|8|9|10).ffn_.*_exps.weight=CPU","blk.(17|18|19|20|21|22|23|24|25).ffn_.*_exps.weight=CPU","blk.(33|34|35|36|37|38|39|40|41).ffn_.*_exps.weight=CPU","blk.(49|50|51|52|53|54|55|56|57).ffn_.*_exps.weight=CPU"

# Memory distribution with abobe configuration
#
# llama_memory_breakdown_print: | memory breakdown [MiB] | total    free     self   model   context   compute       unaccounted |
# llama_memory_breakdown_print: |   - CUDA0 (RTX 3090)   | 24117 = 23773 + (20903 = 12096 +    7504 +    1302) + 17592186023856 |
# llama_memory_breakdown_print: |   - CUDA1 (RTX 3090)   | 24124 = 23845 + (21747 = 14040 +    7504 +     202) + 17592186022947 |
# llama_memory_breakdown_print: |   - CUDA2 (RTX 3090)   | 24124 = 23845 + (21747 = 14040 +    7504 +     202) + 17592186022947 |
# llama_memory_breakdown_print: |   - CUDA3 (RTX 3090)   | 24124 = 23845 + (17542 = 10579 +    6566 +     396) + 17592186027152 |
# llama_memory_breakdown_print: |   - Host               |                  72498 = 72257 +       0 +     240                   |
# llama_params_fit_impl: projected memory use with initial parameters [MiB]:
# llama_params_fit_impl:   - CUDA0 (NVIDIA GeForce RTX 3090):  24117 total,  20903 used,   2870 free vs. target of   1024
# llama_params_fit_impl:   - CUDA1 (NVIDIA GeForce RTX 3090):  24124 total,  21747 used,   2097 free vs. target of   1024
# llama_params_fit_impl:   - CUDA2 (NVIDIA GeForce RTX 3090):  24124 total,  21747 used,   2097 free vs. target of   1024
# llama_params_fit_impl:   - CUDA3 (NVIDIA GeForce RTX 3090):  24124 total,  17542 used,   6303 free vs. target of   1024
# llama_params_fit_impl: projected to use 81940 MiB of device memory vs. 95309 MiB of free device memory
