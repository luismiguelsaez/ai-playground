## Create SSH key

```
ssh-keygen
ssh-copy-id -p 2245 tunnel@h4rdl1nk.chickenkiller.com
```

## Test tunnel

```
/usr/bin/autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -o "ExitOnForwardFailure yes" -N -R 2222:localhost:22 -p 2245 -vvv tunnel@h4rdl1nk.chickenkiller.com
```

## Create SystemD unit `/etc/systemd/system/ssh-tunnel.service`

```
[Unit]
Description=Persistent SSH Tunnel
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi

# Autossh settings
Environment="AUTOSSH_GATETIME=0"
Environment="AUTOSSH_FIRST_POLL=30"
Environment="AUTOSSH_POLL=60"

ExecStart=/usr/bin/autossh -M 0 \                                                                                                                                                                          -o "ServerAliveInterval 15" \
    -o "ServerAliveCountMax 3" \
    -o "ConnectTimeout 10" \
    -o "ExitOnForwardFailure yes" \
    -N -R 2222:localhost:22 \
    -R 33128:localhost:3128 \
    -p 2245 -vvv tunnel@h4rdl1nk.chickenkiller.com

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Enable SystemD unit

```
systemctl enable ssh-tunnel
systemctl start ssh-tunnel
```

## Install watchdog daemon

```
sudo apt install watchdog
```

## Configure `/etc/watchdog.conf`

```
watchdog-device = /dev/watchdog
max-load-1 = 24
min-memory = 1
interval = 10
realtime = yes
priority = 1
```

## Create timer

### `/etc/systemd/system/scheduled-reboot.timer`

```
[Unit]
Description=Scheduled reboot

[Timer]
OnCalendar=*-*-* 04:00
Persistent=true

[Install]
WantedBy=timers.target
```

### `/etc/systemd/system/scheduled-reboot.service`

```
[Unit]
Description=Scheduled reboot

[Service]
Type=oneshot
ExecStart=/usr/bin/systemctl reboot
```

### Enable timer

```
sudo systemctl enable --now scheduled-reboot.timer
```
