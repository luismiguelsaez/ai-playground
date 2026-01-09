# Chatterbox TTS

## Models

- [chatterbox-turbo-ONNX](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX)

## Build

```bash
docker build -t chatterbox:text .
```

## Run

```bash
export HF_TOKEN=""

docker run -it --gpus all \
  -v $PWD/input:/input -v $PWD/output:/output -v $PWD/code:/code \
  -v $HOME/.cache/huggingface/hub:/root/.cache/huggingface/hub \
  -e HF_TOKEN \
  -u $(id -u) \
  chatterbox:test python /code/multilingual.py
```

