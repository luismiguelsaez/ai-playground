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

- TurboQuant enabled (  )

```bash
./buun-llama-cpp/build/bin/llama-server --host 0.0.0.0 --port 8002 --device CUDA0 --model /data/models/huggingface/hub/gemma-4-26B-A4B-it-UD-Q5_K_XL.gguf -c 262144 -ctk turbo3_tcq -ctv turbo3_tcq
```


## Big models

### GLM-4.7 REAP ( [GGUF](https://huggingface.co/unsloth/GLM-4.7-REAP-218B-A32B-GGUF) )


```bash
./llama.cpp/build/bin/llama-cli -m /data/models/huggingface/hub/GLM-4.7-REAP-218B-A32B-UD-Q4_K_XL-00001-of-00003.gguf -c 262144 -ctk q4_0 -ctv q4_0 --tensor-split 1,1 -fa on
```
```
```
