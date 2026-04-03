## Build

```bash
cd llama.cpp
CMAKE_PREFIX_PATH=/usr/local/cuda cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_FA_ALL_QUANTS=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCMAKE_CUDA_ARCHITECTURES="86"
cmake --build build --config Release -j48 --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
```

## Build ( ik_llama)

```bash
cd ik_llama.cpp
cmake -B build -DGGML_NATIVE=ON -DGGML_CUDA=ON
cmake --build build --config Release -j$(nproc)
```

## Build ( turbo-tan llama )

```bash
cd llama.cpp-tq3

cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

