# Build

## Architectures
# - RTX 3090: `86`
# - RTX Pro 6000: `90`

## Build command
BUILD_DIR=${1:-"llama.cpp"}

cd $BUILD_DIR
rm -rf ./build

export CUDA_HOME=${CUDA_HOME:-"/usr/local/cuda-13"}
export CMAKE_PREFIX_PATH=$CUDA_HOME
export CUDA_ARCHS=${CUDA_ARCHS:-"90"}

cmake -B build \
  -DGGML_CUDA=ON \
  -DGGML_CUDA_FA=ON \
  -DGGML_CUDA_FA_ALL_QUANTS=ON \
  -DCMAKE_CUDA_COMPILER=$CUDA_HOME/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=$CUDA_ARCHS \
  -DLLAMA_OPENSSL=ON

cmake --build build --config Release -j$(nproc) --clean-first --target llama-cli llama-server llama-bench llama-quantize llama-gguf-split

sudo cp -rp $BUILD_DIR/build/bin/{llama-cli,llama-server,llama-bench,llama-quantize,llama-gguf-split} /usr/local/bin
