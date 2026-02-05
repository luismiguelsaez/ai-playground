# ai-server Ansible Role

An Ansible role to automate the setup of an AI server on Ubuntu 24 with NVIDIA GPU support, Docker, and related tooling.

## Usage

To apply the role to your servers, run:

```bash
ansible-playbook -i inventory.yml playbook.yml --ask-pass
```

## Requirements

- Ansible 2.9+
- Target system: Ubuntu 24.04 (default)
- Root/sudo access on target systems
- NVIDIA GPU for full functionality

## Default Variables

See `defaults/main.yml` for configurable variables:

- `ai_server_system`: Target system (default: `ubuntu-24`)
- `ai_server_install_nvidia_driver`: Install NVIDIA driver (default: `true`)
- `ai_server_install_docker`: Install Docker CE (default: `true`)
- `ai_server_install_nvidia_toolkit`: Install NVIDIA Container Toolkit (default: `true`)
- `ai_server_install_nvidia_docker_toolkit`: Install nvidia-docker-toolkit (default: `true`)
- `docker_user`: User to add to docker group (default: `SUDO_USER` or `USER`)
- `docker_enable_user`: Enable user in docker group (default: `true`)

## Role Tasks

1. Update apt cache
2. Add NVIDIA and Docker repositories
3. Install NVIDIA driver (535 series)
4. Install Docker CE with compose plugin
5. Install NVIDIA Container Toolkit
6. Configure Docker to work with NVIDIA
7. Add user to docker group
8. Start and enable Docker service
9. Reboot if kernel modules were updated

## Usage Example

```yaml
- hosts: ai_servers
  become: true
  roles:
    - role: ai-server
      vars:
        ai_server_install_nvidia_driver: true
        ai_server_install_docker: true
        ai_server_install_nvidia_toolkit: true
        ai_server_install_nvidia_docker_toolkit: true
        docker_user: ubuntu
        docker_enable_user: true
```

## Verification

After running the role, verify installations:

```bash
# Check NVIDIA GPU
nvidia-smi

# Check Docker installation
docker --version

# Test Docker with GPU
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# Check Docker service
systemctl status docker
```

## Notes

- The role installs NVIDIA driver version 535 by default
- Docker is configured with the compose plugin
- User is added to the docker group for non-root container management
- System may reboot if kernel modules are updated