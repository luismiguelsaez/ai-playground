#!/usr/bin/env bash

# Documentation
# - Server arguments: https://docs.vllm.ai/en/latest/cli/serve/#arguments
#

CONFIG_DIR=../config/models/
CONFIG_FILE=${1:-lfm.yaml}

VLLM_LOG_FILE=/tmp/vllm_serve.log
OPENWEBUI_LOG_FILE=/tmp/openwebui.log

vllm serve --config ${CONFIG_DIR}${CONFIG_FILE} 2>&1 >${VLLM_LOG_FILE} &

OPENAI_API_BASE_URL=http://localhost:8000/v1 open-webui serve --host 0.0.0.0 --port 8888 2>&1 >${OPENWEBUI_LOG_FILE} &
