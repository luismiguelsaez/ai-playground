#!/usr/bin/env bash

# 2026-01-21 - Fix for GLM4.7-Flash - vllm/vllm/transformers_utils/model_arch_config_convertor.py - +glm4_moe_lite ( line 192 )

python3 -m venv .venv
source .venv/bin/activate

cd vllm
export MAKEFLAGS="-j$(nproc)"
VLLM_USE_PRECOMPILED=0 \
  TORCH_CUDA_ARCH_LIST="12.0" \
  MAX_JOBS="$(nproc)" \
  uv pip install --editable --no-build-isolation .

python3 -m pip install -U flash-linear-attention
