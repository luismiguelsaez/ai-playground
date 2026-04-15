# Environment
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=0,1
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export SAFETENSORS_FAST_GPU=1
export NCCL_P2P_DISABLE=1 # No NVLink — SHM is faster than P2P PCIe
export NCCL_IB_DISABLE=1  # No InfiniBand
export NCCL_SHM_DISABLE=0
export NCCL_NVLS_ENABLE=0
export OMP_NUM_THREADS=8
export VLLM_USE_V1=1
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

python -m vllm.entrypoints.openai.api_server \
  --model lukealonso/MiniMax-M2.7-NVFP4 \
  --trust-remote-code \
  --tensor-parallel-size 2 \
  --attention-backend FLASH_ATTN \
  --gpu-memory-utilization 0.92 \
  --max-model-len 65536 \
  --max-num-seqs 64 \
  --max-num-batched-tokens 16384 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser minimax_m2 \
  --reasoning-parser minimax_m2_append_think \
  --host 0.0.0.0 \
  --port 8000
