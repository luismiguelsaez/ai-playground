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
  --alias coding-agent \
  --threads 40 \
  --ctx-size 27000 \
  --n-predict 27000 \
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
  --override-tensor "blk\.(1|2|3|4|5|6|7|8|9)\.ffn_.*_exps\.weight=CPU","blk\.(24|25|26|27|28|29|30|31|32)\.ffn_.*_exps\.weight=CPU","blk\.(47|48|49|50|51|52|53|54|55)\.ffn_.*_exps\.weight=CPU","blk\.(70|71|72|73|74|75|76|77|78)\.ffn_.*_exps\.weight=CPU"
