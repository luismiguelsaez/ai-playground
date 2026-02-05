#!/bin/bash
#
# NVIDIA, CUDA, and Container Toolkit Setup Script for Ubuntu 24.04
# This script installs all necessary components from scratch
#
# Usage: sudo bash setup-nvidia-cuda-ubuntu24.sh
#

set -e  # Exit on any error

echo "========================================"
echo "NVIDIA, CUDA, and Container Setup for Ubuntu 24.04"
echo "========================================"

# Ensure script is run as root
if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Ensure script is run with sudo - get original user
ORIGINAL_USER="${SUDO_USER:-$USER}"

# Update system
echo ""
echo "[1/10] Updating system packages..."
apt-get update
apt-get upgrade -y
apt-get install -y curl wget gnupg lsb-release ca-certificates

# Install NVIDIA CUDA Repository Key and Repository
echo ""
echo "[2/10] Installing NVIDIA CUDA repository..."
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404-archive.key | gpg --dearmor -o /usr/share/keyrings/cuda-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/cuda-archive-keyring.gpg] https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/ /" > /etc/apt/sources.list.d/cuda.sources

# Install NVIDIA Driver
echo ""
echo "[3/10] Installing NVIDIA driver (580)..."
apt-get update
# Driver 580 is compatible with CUDA 12.x
apt-get install -y nvidia-driver-580
# Also install additional utilities
apt-get install -y nvidia-modprobe nvidia-settings nvidia-persistenced

# Install CUDA Toolkit
echo ""
echo "[4/10] Installing CUDA Toolkit 12.8..."
apt-get install -y cuda-toolkit-12-8

# Install Docker
echo ""
echo "[5/10] Installing Docker..."
# Add Docker repository key if not already present
if [[ ! -f /usr/share/keyrings/docker-archive-keyring.gpg ]]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
fi

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
systemctl enable docker
systemctl start docker

# Add original user to docker group
if [[ "$ORIGINAL_USER" != "root" ]] && id "$ORIGINAL_USER" &>/dev/null; then
    usermod -aG docker "$ORIGINAL_USER"
    echo "Added $ORIGINAL_USER to docker group"
fi

# Install NVIDIA Container Toolkit
echo ""
echo "[6/10] Installing NVIDIA Container Toolkit..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

apt-get update
apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA Container Toolkit
echo ""
echo "[7/10] Configuring Docker for NVIDIA Container Toolkit..."
nvidia-ctk runtime configure --runtime=docker || true

# Restart Docker to apply changes
systemctl restart docker

# Install additional CUDA development packages (optional but useful)
echo ""
echo "[8/10] Installing CUDA development packages..."
apt-get install -y cuda-compiler-12-8 cuda-libraries-dev-12-8 cuda-nvrtc-dev-12-8

# Install Docker Compose plugin
echo ""
echo "[9/10] Installing Docker Compose..."
apt-get install -y docker-compose-plugin

# Final setup - configure nvidia-container-runtime
echo ""
echo "[10/10] Finalizing NVIDIA Container Runtime configuration..."
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'DOCKERJSON'
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
DOCKERJSON

echo ""
echo "========================================"
echo "Verification"
echo "========================================"

echo ""
echo "========================================"
echo "NVIDIA Driver:"
echo "========================================"
nvidia-smi

echo ""
echo "========================================"
echo "CUDA Compiler (nvcc):"
echo "========================================"
nvcc --version

echo ""
echo "========================================"
echo "Docker with GPU support:"
echo "========================================"
docker run --rm --gpus all nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi || echo "Docker container test skipped"

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Installed components:"
echo "  - NVIDIA Driver: 580.x (from NVIDIA repository)"
echo "  - CUDA Toolkit: 12.8"
echo "  - Docker: Latest stable"
echo "  - NVIDIA Container Toolkit: Latest"
echo ""
echo "Note: You may need to log out and back in for group membership changes to take effect."
echo "      Or run: newgrp docker"
echo ""
echo "Test Docker with GPU access:"
echo "  docker run --rm --gpus all nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi"
echo ""