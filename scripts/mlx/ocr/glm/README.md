# GLM OCR

## Install

```bash
pip install -U mlx-vlm torchvision
```

## Generate

```bash
MODEL="mlx-community/GLM-OCR-4bit"

python -m mlx_vlm generate \
  --model ${MODEL} \
  --max-tokens 1024 \
  --temperature 0.0 \
  --prompt "Describe this image." \
  --image <path_to_image>
```

