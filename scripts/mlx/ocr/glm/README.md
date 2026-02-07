# GLM OCR

## Install

```bash
pip install -U mlx-vlm torchvision
```

## Generate

```bash
python -m mlx_vlm generate --model mlx-community/GLM-OCR-4bit --max-tokens 100 --temperature 0.0 --prompt "Describe this image." --image <path_to_image>
```

