#!/usr/bin/env bash

DEST=/usr/lib/systemd/system

python3 setup.py install --record files.txt
mkdir -p "$DEST" && cp g910-gkeys.service "$DEST"
systemctl daemon-reload
