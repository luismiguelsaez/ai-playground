#!/usr/bin/env bash

export CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3

.venv/bin/vllm serve --config ../config/models/qwen3-thinking.yaml
