#!/usr/bin/env bash

set -a

. ../config/models/nvidia-nemotron-super-120b-nvfp4.env
vllm serve --config ../config/models/nvidia-nemotron-super-120b-nvfp4.yaml
