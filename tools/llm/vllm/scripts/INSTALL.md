# Install vLLM

## Specific CUDA version [Documentation](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/#pre-built-wheels)

```bash
export VLLM_VERSION=$(curl -s https://api.github.com/repos/vllm-project/vllm/releases/latest | jq -r .tag_name | sed 's/^v//')
export CUDA_VERSION=130 # or other
uv pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu${CUDA_VERSION}-cp38-abi3-manylinux_2_31_x86_64.whl --extra-index-url https://download.pytorch.org/whl/cu${CUDA_VERSION}
```

