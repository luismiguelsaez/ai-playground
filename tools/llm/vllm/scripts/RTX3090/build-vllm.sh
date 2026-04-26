# Build with PyTorch index matching CUDA Toolkit version
MAKEFLAGS="-j$(nproc)" uv pip install git+https://github.com/vllm-project/vllm@v0.20.0 --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
