source .venv/bin/activate

vllm serve Lorbus/Qwen3.6-27B-int4-AutoRound --kv-cache-dtype fp8_e4m3 --max-model-len 30000 --max-num-seqs 1
