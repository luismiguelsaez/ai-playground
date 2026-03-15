## Install open driver
sudo apt purge nvidia-*
sudo apt autoremove
apt search nvidia-open
apt install -y nvidia-open-580
sudo apt install -y nvidia-open-580
sudo systemctl reboot
nvidia-smi

## Install proprietary Nvidia driver ( optional )

- [Latest driver 580.142](https://us.download.nvidia.com/XFree86/Linux-x86_64/580.142/NVIDIA-Linux-x86_64-580.142.run)

## Disable DRM which makes the first GPU disappear
echo "options nvidia_drm modeset=0" | sudo tee /etc/modprobe.d/nvidia-drm-nomodeset.conf
sudo update-initramfs -u
sudo reboot

## Install container toolkit

- [Install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)


