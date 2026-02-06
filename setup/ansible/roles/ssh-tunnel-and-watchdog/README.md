# ssh-tunnel-and-watchdog Ansible Role

An Ansible role to automate the configuration of SSH tunneling, watchdog daemon, and scheduled reboot on Linux systems.

## Usage

To apply the role to the VPN group, run:

```bash
ansible-playbook -i inventory.yml apply-ssh-tunnel.yml --ask-pass
```

This command will prompt you to enter the SSH password for the `pi` user on `raspi-vpn.local`.

## Requirements

- Ansible 2.9+
- Target Linux system (Debian/Ubuntu family)

## Default Variables

See `defaults/main.yml` for configurable variables:

- `ssh_tunnel_remote_host`: Remote SSH server (default: `tunnel@h4rdl1nk.chickenkiller.com`)
- `ssh_tunnel_remote_port`: Remote port (default: `2245`)
- `ssh_tunnel_local_forward_ports`: List of port forwards (default: SSH and custom port)
- `ssh_tunnel_service_user`: Systemd user for tunnel service (default: `pi`)
- `watchdog_device`: Watchdog device (default: `/dev/watchdog`)
- `watchdog_max_load_1`: Maximum CPU load for watchdog (default: `24`)
- `watchdog_min_memory`: Minimum memory in GB (default: `1`)
- `watchdog_interval`: Watchdog interval in seconds (default: `10`)
- `watchdog_realtime`: Run watchdog in realtime mode (default: `yes`)
- `watchdog_priority`: Watchdog priority (default: `1`)
- `scheduled_reboot_time`: Daily reboot time (default: `04:00`)

## Role Tasks

1. Install `autossh` and `watchdog` packages
2. Configure persistent SSH tunnel service
3. Configure watchdog daemon
4. Set up scheduled reboot timer
5. Optional: Copy SSH public key for authentication

## Usage Example

```yaml
- hosts: your_servers
  roles:
    - role: ssh-tunnel-and-watchdog
      vars:
        ssh_tunnel_remote_host: your-remote-host.com
        ssh_tunnel_remote_port: 2245
        ssh_tunnel_local_forward_ports:
          - "2222:localhost:22"
          - "33128:localhost:3128"
        ssh_tunnel_service_user: your-user
        scheduled_reboot_time: "03:00"
```

## Manual Verification

After running the role, verify services are running:

```bash
systemctl status ssh-tunnel
systemctl status watchdog
systemctl status scheduled-reboot.timer
```

## Manual Testing

Test the tunnel manually:

```bash
/usr/bin/autossh -M 0 \
  -o "ServerAliveInterval 30" \
  -o "ServerAliveCountMax 3" \
  -o "ExitOnForwardFailure yes" \
  -N -R 2222:localhost:22 -p 2245 \
  tunnel@h4rdl1nk.chickenkiller.com
```
