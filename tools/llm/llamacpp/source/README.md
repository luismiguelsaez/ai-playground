## Build

```bash
cd llama.cpp
cmake -B build -DGGML_CUDA_FA_ALL_QUANTS=ON
cmake --build build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split -j48
```

## Build ( ik_llama)

```bash
cd ik_llama.cpp
cmake -B build -DGGML_NATIVE=ON -DGGML_CUDA=ON
cmake --build build --config Release -j$(nproc)
```
