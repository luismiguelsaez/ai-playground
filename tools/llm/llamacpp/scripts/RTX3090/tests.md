## Documents

- [llama-cpp TurboQuant](https://github.com/spiritbuun/buun-llama-cpp)


## Qwen3.5 27B

- Model: Ornstein 27B Q4_K_M
- Context: 262144
- VRAM usage: 19.68Gi
- KV quantization: K turbo3_tcq, V turbo2_tcq
- Command

```bash
 ~/github/ai-playground/tools/llm/llamacpp/source/buun-llama-cpp/build/bin/llama-cli -c 262144 -ctk turbo3_tcq -ctv turbo2_tcq -fa on --device CUDA0 -m /data/models/huggingface/hub/Ornstein-27B-Q4_K_M.gguf -n 8192
```

- Model: Ornstein 27B Q5_K_M
- Context: 262144
- VRAM usage: 23Gi
- KV quantization: K turbo3_tcq, V turbo2_tcq
- Command

```bash
 ~/github/ai-playground/tools/llm/llamacpp/source/buun-llama-cpp/build/bin/llama-cli -c 262144 -ctk turbo3_tcq -ctv turbo2_tcq -fa on --device CUDA0 -m /data/models/huggingface/hub/Ornstein-27B-Q5_K_M.gguf -n 8192
```

- Model: Carnice 27B Q4_K_M
- Context: 262144
- VRAM usage: 20.504Gi
- KV quantization: K turbo3_tcq, V turbo2_tcq
- Command

```bash
llama-server --host 0.0.0.0 --port 8000 -c 262144 -ctk turbo3_tcq -ctv turbo2_tcq -fa on -hfr kai-os/Carnice-27b-GGUF:Q4_K_M
```

- Model: Ornstein 31B Q4_K_M
- Context: 64000
- VRAM usage: 22Gi
- KV quantization: K turbo3_tcq, V turbo3_tcq
- Issues
  - `OOMKilled` at the OS level after a few requests
  - Test `--cache-ram 1024` to mitigate
- Command

```bash
llama-server --host 0.0.0.0 --port 8000 -c 131072 -ctk turbo3_tcq -ctv turbo3_tcq -fa on -hfr DJLougen/Ornstein-31B-it-GGUF:Q4_K_M --device CUDA0 --cache-ram 1024
```

## Qwen 3.6 35B A3B

- Model: Qwen3.5 35B A3B ( unstloth )
- Context: 262144
- VRAM usage: 20Gi
- KV quantization: K turbo3_tcq, V turbo2_tcq
- Command:

```bash
llama-server --host 0.0.0.0 --port 8000 -c 262144 -ctk turbo3_tcq -ctv turbo2_tcq -fa on -hfr unsloth/Qwen3.6-35B-A3B-GGUF:UD-IQ4_XS --device CUDA0
```

## Qwen 3.6 27B

- Model: Qwen3.6 27B ( unstloth )
- Context: 262144
- VRAM usage: 23.8Gi
- KV quantization: K turbo4, V turbo3_tcq
- Command:

```bash
llama-server --host 0.0.0.0 --port 8000 -c 262144 -ctk turbo4 -ctv turbo3_tcq --kv-unified -fa on -hfr unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL
```

```bash
build/bin/llama-server --host 0.0.0.0 --port 8002 -ngl 99 -ngld 99 -c 8192 -cd 4096 -fa on -ctk q8_0 -ctv q8_0 --draft-max 12 --draft-min 3 --draft-p-min 0.6 -hfr unsloth/Qwen3.6-27B-GGUF:Q4_K_M -md /data/models/huggingface/hub/Qwen3-1.7B-Q8_0.gguf --device CUDA0
```

