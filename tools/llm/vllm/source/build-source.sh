#!/usr/bin/env bash

MAKEFLAGS="-j$(nproc)" uv pip install -e vllm --torch-backend=auto --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
uv pip install transformers -U

MAKEFLAGS="-j$(nproc)" uv pip install git+https://github.com/vllm-project/vllm@v0.19.2rc0 --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
uv pip install git+https://github.com/huggingface/transformers@v5.5.4
