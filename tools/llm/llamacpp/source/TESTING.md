# Llama.cpp compiled from source testing

## TurboQuant

- TurboQuant enabled ( 9.22Gi )

```bash
./buun-llama-cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/Harmonic-Hermes-9B-Q5_K_M.gguf -c 262144 -ctk turbo3_tcq -ctv turbo3_tcq
```

- TurboQuant disabled ( 9.91Gi )

```bash
./llama.cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/Harmonic-Hermes-9B-Q5_K_M.gguf -c 262144 -ctk q4_0 -ctv q4_0 
```
