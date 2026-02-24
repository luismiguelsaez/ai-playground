## Build

```bash
cd llama.cpp
cmake -B build -DGGML_CUDA_FA_ALL_QUANTS=ON
cmake --build build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split -j48
```

