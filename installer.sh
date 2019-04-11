#!/usr/bin/env bash


python3 setup.py install --record files.txt
cp g910-gkeys.service /usr/lib/systemd/system
systemctl daemon-reload
