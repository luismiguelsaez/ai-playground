
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

