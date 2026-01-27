#!/usr/bin/env bash

CHECKPOINT="LiquidAI/LFM2.5-1.2B-Instruct"
CHECKPOINT="/home/luismi/github/ai-playground/tools/llm/vllm/scripts/LFM2.5-1.2B-Instruct-W4A16-G128"

vllm serve --calculate-kv-scales --kv-cache-dtype=fp8 --gpu-memory-utilization=0.75 $CHECKPOINT