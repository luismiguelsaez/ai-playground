# CUDA Toolkit ( https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Debian&target_version=13&target_type=deb_network )

## Repository

wget https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-13-2

## RUN file ( alternative )

wget https://developer.download.nvidia.com/compute/cuda/13.2.1/local_installers/cuda_13.2.1_595.58.03_linux.run
sudo sh cuda_13.2.1_595.58.03_linux.run

## Container toolkit ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html )

sudo apt install -y nvidia-container-runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker.service

# Install latest driver

#sudo apt install -y nvidia-open
sudo apt-get remove --purge '^nvidia-.*'
sudo apt-get remove --purge '^libnvidia-.*'
sudo apt-get remove --purge '^cuda-.*'

sudo apt install -y cuda-drivers
