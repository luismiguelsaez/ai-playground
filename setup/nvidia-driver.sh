## Install open driver
sudo apt purge nvidia-*
sudo apt autoremove
apt search nvidia-open
apt install -y nvidia-open-580
sudo apt install -y nvidia-open-580
sudo systemctl reboot
nvidia-smi

## Disable DRM which makes the first GPU disappear
echo "options nvidia_drm modeset=0" | sudo tee /etc/modprobe.d/nvidia-drm-nomodeset.conf
sudo update-initramfs -u
sudo reboot
