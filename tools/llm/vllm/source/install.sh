#!/usr/bin/env bash

# 2026-01-21 - Fix for GLM4.7-Flash - vllm/vllm/transformers_utils/model_arch_config_convertor.py - +glm4_moe_lite ( line 192 )

python3 -m venv .venv
source .venv/bin/activate

cd vllm
VLLM_USE_PRECOMPILED=1 uv pip install --editable .

python3 -m pip install -U flash-linear-attention
