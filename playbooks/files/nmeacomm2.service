[Unit]
Description=nmeaComm
After=network.target
StartLimitIntervalSec=200
StartLimitBurst=5

[Service]
ExecStart=/usr/bin/python3 -u nmea-comm.py
WorkingDirectory=/home/midnite/
StandardOutput=inherit
StandardError=inherit
Restart=always
RestartSec=30
User=midnite

[Install]
WantedBy=multi-user.target
