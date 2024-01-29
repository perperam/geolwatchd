#!/bin/bash

PROJECT_DIR="/opt/geolwatchd"
SYSTEMD_DIR="/etc/systemd/system"

systemctl stop geolwatchd
systemctl disable geolwatchd

rm "$SYSTEMD_DIR/geolwatchd.service"

rm -Rf "$PROJECT_DIR"

systemctl daemon-reload