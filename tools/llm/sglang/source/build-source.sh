
# Install

- [Document](https://sgl-project.github.io/get_started/install.html#for-cuda-13)

## Install PyTorch

export SGLANG_VERSION="0.5.10"
export TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas
export CUDA_HOME=/usr/local/cuda-13

uv pip install torch==$SGLANG_VERSION torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130

uv pip install sglang>=$SGLANG_VERSION

uv pip install "https://github.com/sgl-project/whl/releases/download/v$SGLANG_VERSION/sglang_kernel-$SGLANG_VERSION+cu130-cp310-abi3-manylinux2014_x86_64.whl"

MAKEFLAGS="-j$(nproc)" uv pip install git+https://github.com/sgl-project/sglang@v$SGLANG_VERSION --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
