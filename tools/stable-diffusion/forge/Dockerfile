#FROM python:3.11.14-trixie
FROM nvidia/cuda:12.8.0-devel-ubuntu22.04 

ENV TZ=Europe/Madrid
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

ENV FORGE_REPO=https://github.com/lllyasviel/stable-diffusion-webui-forge.git
ENV FORGE_PORT=8877

## Install system packages

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone 

RUN apt update -y && \
    apt install -y git curl \
      python3 python3-pip python3-cairo \
      pkg-config libcairo2-dev \
      libgl1-mesa-glx \
      libglib2.0-0 \
      libsm6 \
      libxrender1 \
      libxext6 && \ 
    ln -sf /usr/bin/python3 /usr/bin/python

## Install forge

RUN mkdir -p /app/forge

RUN git clone $FORGE_REPO /app/forge/

RUN python -m pip install --upgrade pip setuptools wheel joblib
RUN python -m pip install -r /app/forge/requirements_versions.txt
RUN python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

ENTRYPOINT [ "python", "-u", "/app/forge/launch.py", "--cuda-malloc", "--listen" ]
