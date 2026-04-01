export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0,1
export HF_HOME=$HOME/.cache/huggingface
export HUGGINGFACE_HUB_CACHE=$HF_HOME/hub
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export SAFETENSORS_FAST_GPU=1
export VLLM_NVFP4_GEMM_BACKEND=cutlass
export VLLM_USE_FLASHINFER_MOE_FP4=0
export NCCL_P2P_DISABLE=1
export NCCL_SHM_DISABLE=0
export NCCL_IB_DISABLE=1
export OMP_NUM_THREADS=8
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

vllm serve lukealonso/MiniMax-M2.5-NVFP4 \
  --download-dir $HUGGINGFACE_HUB_CACHE \
  --host 0.0.0.0 \
  --port 1235 \
  --served-model-name MiniMax-M2.5-NVFP4 \
  --trust-remote-code \
  --tensor-parallel-size 2 \
  --attention-backend FLASHINFER \
  --gpu-memory-utilization 0.95 \
  --max-model-len 190000 \
  --max-num-batched-tokens 16384 \
  --max-num-seqs 64 \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --compilation-config '{"cudagraph_mode": "PIECEWISE"}'
