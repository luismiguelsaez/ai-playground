# Llama.cpp compiled from source testing


## TurboQuant

### Harmonic Hermes 9B ( [GGUF](https://huggingface.co/DJLougen/Harmonic-Hermes-9B-GGUF) )

- TurboQuant enabled ( 9.22Gi )

```bash
./buun-llama-cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/Harmonic-Hermes-9B-Q5_K_M.gguf -c 262144 -ctk turbo3_tcq -ctv turbo3_tcq
```

- TurboQuant disabled ( 9.91Gi )

```bash
./llama.cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/Harmonic-Hermes-9B-Q5_K_M.gguf -c 262144 -ctk q4_0 -ctv q4_0 
```

### Gemma 4 26B ( [GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/blob/main/gemma-4-26B-A4B-it-UD-Q5_K_XL.gguf) )

- TurboQuant enabled ( 23.73Gi )

```bash
./buun-llama-cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/gemma-4-26B-A4B-it-UD-Q5_K_XL.gguf -c 262144 -ctk turbo3_tcq -ctv turbo3_tcq
```

### Qwen3.6 35B A3B

- TurboQuant enabled ( 19.121Gi )

```bash
llama-server --host 0.0.0.0 --port 8000 -c 131072 -ctk turbo3_tcq -ctv turbo2_tcq -fa on -hfr unsloth/Qwen3.6-35B-A3B-GGUF:UD-IQ4_XS --device CUDA0
```


## Big models

### GLM-4.7 REAP ( [GGUF](https://huggingface.co/unsloth/GLM-4.7-REAP-218B-A32B-GGUF) )

- TurboQuant disabled ( 74Gi + 74Gi )


```bash
./llama.cpp/build/bin/llama-cli -m /data/models/huggingface/hub/GLM-4.7-REAP-218B-A32B-UD-Q4_K_XL-00001-of-00003.gguf -c 262144 -ctk q4_0 -ctv q4_0 --tensor-split 1,1 -fa on
```


## Draft model

### Qwen3.5 122B - Qwen3.5 0.8B ( draft )

- VRAM: ~80Gi

```bash
llama-cli -c 262144 -fa on --fit on -hfr unsloth/Qwen3.5-122B-A10B-GGUF:Q4_K_M -hfrd unsloth/Qwen3.5-0.8B-GGUF:UD-Q4_K_XL --device CUDA1
```

