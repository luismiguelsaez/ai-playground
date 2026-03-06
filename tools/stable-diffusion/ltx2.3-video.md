# LTX2 Video

## Links

- [ComfyUI Node](https://github.com/Lightricks/ComfyUI-LTXVideo)
- [Text Encoder](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)
- [Model](https://huggingface.co/Lightricks/LTX-2.3)

## Install

### Custom nodes

```bash
CUSTOM_NODES_PATH="/data/models/comfy/custom_nodes"

git clone https://github.com/Lightricks/ComfyUI-LTXVideo $CUSTOM_NODES_PATH
git clone https://github.com/ClownsharkBatwing/RES4LYF $CUSTOM_NODES_PATH
git clone https://github.com/evanspearman/ComfyMath $CUSTOM_NODES_PATH
```

### Model files

```bash
MODELS_PATH="/data/models/comfy/models/diffusion_models"

curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled.safetensors -o $MODELS_PATH/checkpoints/ltx-2.3-22b-distilled.safetensors
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled-lora-384.safetensors -o $MODELS_PATH/loras/ltx-2.3-22b-distilled-lora-384.safetensors
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.0.safetensors -o ltx-2.3-spatial-upscaler-x2-1.0.safetensor
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-temporal-upscaler-x2-1.0.safetensors -o ltx-2.3-temporal-upscaler-x2-1.0.safetensors
hf download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir gemma-3-12b-it-qat-q4_0-unquantized
```
