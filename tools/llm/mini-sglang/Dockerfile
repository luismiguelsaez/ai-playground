# Use NVIDIA CUDA base image with Python
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Install git and python3
RUN apt-get update && apt-get install -y git python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

# Clone the mini-sglang repository
RUN git clone https://github.com/sgl-project/mini-sglang /mini-sglang

# Set working directory
WORKDIR /mini-sglang

# Create virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install the package from the repository
RUN pip install --upgrade pip && \
    pip install -e .

# Set the entry point to run mini-sglang
ENTRYPOINT ["python", "-m", "minisgl"]
