#!/bin/bash

export CUDA_VISIBLE_DEVICES=0,1

#-hf unsloth/gemma-4-31B-it-GGUF:IQ4_XS
#-hf unsloth/gemma-4-31B-it-GGUF:UD-Q6_K_XL \
#--model /home/luismi/.cache/huggingface/hub/gemma-4-31B-it-IQ4_XS.gguf \

./llama.cpp/build/bin/llama-server \
  --model /home/luismi/.cache/huggingface/hub/gemma-4-31B-it-UD-Q6_K_XL.gguf \
  --alias coding-agent \
  --host 0.0.0.0 \
  --port 8002 \
  -ngl 999 \
  -c 256000 \
  --jinja \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  --flash-attn on \
  --fit on \
  --reasoning off
