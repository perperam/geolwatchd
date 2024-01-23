#!/bin/sh

PROJECT_DIR="/opt/geolwatchd"
PIP_PATH="$PROJECT_DIR/venv/bin/pip"

mkdir -p "$PROJECT_DIR"

python3 -m venv "$PROJECT_DIR/venv"

"$PIP_PATH" install -r requirements.txt

cp -r "./src" "$PROJECT_DIR/src/"

cp "./geolwatchd.service" "$PROJECT_DIR/"

systemctl enable geolwatchd
systemctl start geolwatchd