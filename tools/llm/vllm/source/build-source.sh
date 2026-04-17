#!/usr/bin/env bash

MAKEFLAGS="-j$(nproc)" uv pip install -e vllm --torch-backend=auto --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
uv pip install transformers -U
