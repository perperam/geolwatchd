#!/bin/bash

PROJECT_DIR="/opt/geolwatchd"
PIP_PATH="$PROJECT_DIR/venv/bin/pip"
SYSTEMD_DIR="/etc/systemd/system"

mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/log"

python3 -m venv "$PROJECT_DIR/venv"

"$PIP_PATH" install -r requirements.txt

cp -r "./src" "$PROJECT_DIR/src/"

cp "./geolwatchd.service" "$SYSTEMD_DIR/"

systemctl daemon-reload

systemctl enable geolwatchd
systemctl start geolwatchd