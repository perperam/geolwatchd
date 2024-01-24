#!/bin/bash

PROJECT_DIR="/opt/geolwatchd"
SYSTEMD_DIR="/etc/systemd/system"

rm -Rf "$PROJECT_DIR"

systemctl stop geolwatchd
systemctl disable geolwatchd

rm "$SYSTEMD_DIR/geolwatchd.service"

systemctl daemon-reload