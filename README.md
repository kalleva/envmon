## I2C

GPIO2 - SDA1 - PIN3
GPIO3 - SCL1 - PIN5

## Deploy on RPi

Deploy on RPi as systemd service

```bash
sudo nano /etc/systemd/system/envmon.service
```

```bash
[Unit]
Description=Envmon Python Service
After=multi-user.target network-online.target

[Service]
ExecStart=/home/kalleva/.venv/bin/python /home/kalleva/envmon/main.py
WorkingDirectory=/home/kalleva/envmon
StandardOutput=inherit
StandardError=inherit
Restart=always
User=kalleva

[Install]
WantedBy=multi-user.target
```