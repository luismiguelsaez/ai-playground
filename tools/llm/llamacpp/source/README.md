## Build

```bash
CUDA_HOME=${CUDA_HOME:-/usr/local/cuda-13} \
CMAKE_PREFIX_PATH=$CUDA_HOME \
CUDA_ARCHS="${CUDA_ARCHS:-120}" \
cmake -B build \
  -DGGML_CUDA=ON \
  -DGGML_CUDA_FA=ON \
  -DGGML_CUDA_FA_ALL_QUANTS=ON \
  -DCMAKE_CUDA_COMPILER=$CUDA_HOME/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES="$CUDA_ARCHS" \
  -DLLAMA_OPENSSL=ON

cmake --build build --config Release -j$(nproc) --clean-first

sudo cp -rp build/bin/{llama-cli,llama-server,llama-bench,llama-quantize,llama-gguf-split} /usr/local/bin
```

