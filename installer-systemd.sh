#!/usr/bin/env bash

# get system unit directory
DEST=$(pkg-config systemd --variable=systemdsystemunitdir)

python3 setup.py install --record files.txt
cp g910-gkeys.service "$DEST"/g910-gkeys.service
systemctl daemon-reload
