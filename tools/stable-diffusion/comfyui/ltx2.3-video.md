# LTX2 Video

## Links

- [ComfyUI Node](https://github.com/Lightricks/ComfyUI-LTXVideo)
- [Text Encoder](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)
- [Model](https://huggingface.co/Lightricks/LTX-2.3)
- [Howto](https://docs.ltx.video/open-source-model/integration-tools/comfy-ui)
- [Workflows](https://huggingface.co/RuneXX/LTX-2.3-Workflows)

## Install

### Custom nodes

```bash
CUSTOM_NODES_PATH="/data/models/comfy/custom_nodes"

git clone https://github.com/Lightricks/ComfyUI-LTXVideo $CUSTOM_NODES_PATH
git clone https://github.com/ClownsharkBatwing/RES4LYF $CUSTOM_NODES_PATH
git clone https://github.com/evanspearman/ComfyMath $CUSTOM_NODES_PATH
```

### Model files

#### Default

```bash
MODELS_PATH="/data/models/comfy/models"

curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled.safetensors -o $MODELS_PATH/checkpoints/ltx-2.3-22b-distilled.safetensors
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-22b-distilled-lora-384.safetensors -o $MODELS_PATH/loras/ltx-2.3-22b-distilled-lora-384.safetensors
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/blob/main/vae/LTX23_video_vae_bf16.safetensors -o $MODELS_PATH/LTX23_video_vae_bf16.safetensors
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/blob/main/vae/LTX23_audio_vae_bf16.safetensors -o $MODELS_PATH/LTX23_audio_vae_bf16.safetensors
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.0.safetensors -o ltx-2.3-spatial-upscaler-x2-1.0.safetensor
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-temporal-upscaler-x2-1.0.safetensors -o ltx-2.3-temporal-upscaler-x2-1.0.safetensors
hf download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir $MODELS_PATH/text_encoders/gemma-3-12b-it-qat-q4_0-unquantized
```

#### Rune workflow

```bash
MODELS_PATH="/data/models/comfy/models"

# GGUF model
curl -sL https://huggingface.co/unsloth/LTX-2.3-GGUF/resolve/main/ltx-2.3-22b-dev-Q8_0.gguf -o $MODELS_PATH
# Safeternsors model
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/diffusion_models/ltx-2.3-22b-distilled_transformer_only_fp8_input_scaled.safetensors -o $MODELS_PATH/diffusion_models/ltx-2.3-22b-distilled_transformer_only_fp8_input_scaled.safetensors
# Upscaler
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.0.safetensors -o $MODELS_PATH/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors
curl -sL https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-temporal-upscaler-x2-1.0.safetensors -o $MODELS_PATH/latent_upscale_models/ltx-2.3-temporal-upscaler-x2-1.0.safetensors
# Text encoder
curl -sL https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors -o $MODELS_PATH/text_encoders/gemma_3_12B_it_fp8_scaled.safetensors
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/text_encoders/ltx-2.3_text_projection_bf16.safetensors -o $MODELS_PATH/text_encoders/ltx-2.3_text_projection_bf16.safetensors
# VAE
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/vae/LTX23_video_vae_bf16.safetensors -o $MODELS_PATH/vae/LTX23_video_vae_bf16.safetensors
curl -sL https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/vae/LTX23_audio_vae_bf16.safetensors -o $MODELS_PATH/vae/LTX23_audio_vae_bf16.safetensors
```

#### Sulphur

```bash
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/sulphur_dev_fp8mixed.safetensors -o $MODELS_PATH/sulphur_dev_fp8mixed.safetensors
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/distill_loras/ltx-2.3-22b-distilled-lora-1.1_fro90_ceil72_condsafe.safetensors -o $MODELS_PATH/loras/ltx-2.3-22b-distilled-lora-1.1_fro90_ceil72_condsafe.safetensors
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/workflows/ltx23_i2v%20base.json -o /data2/models/comfy/workflows/ltx23_i2v_base.json
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/workflows/ltx23_t2v%20base.json -o  /data2/models/comfy/workflows/ltx23_t2v_base.json
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/workflows/ltx23_i2v%20distilled.json -o /data2/models/comfy/workflows/ltx23_i2v_distilled.json
curl -sL https://huggingface.co/SulphurAI/Sulphur-2-base/resolve/main/workflows/ltx23_t2v%20distilled.json -o /data2/models/comfy/workflows/ltx23_t2v_distilled.json
```
