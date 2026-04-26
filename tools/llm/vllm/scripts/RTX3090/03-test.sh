source .venv/bin/activate

# 20.380Gi on startup
vllm serve Lorbus/Qwen3.6-27B-int4-AutoRound --kv-cache-dtype fp8_e4m3 --max-model-len 30000 --max-num-seqs 1

# Patches applied ( https://github.com/Sandermage/genesis-vllm-patches )
vllm serve Lorbus/Qwen3.6-27B-int4-AutoRound \
  --host 0.0.0.0 --port 8000 \
  --dtype float16 \
  --tensor-parallel-size 1 \
  --trust-remote-code \
  --kv-cache-dtype turboquant_3bit_nc \
  --max-num-seqs 1 \
  --max-num-batched-tokens 4128 \
  --max-model-len 125000 \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --enable-prefix-caching \
  --enable-chunked-prefill \
  --no-scheduler-reserve-full-isl \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
