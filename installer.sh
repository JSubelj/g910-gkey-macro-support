#!/usr/bin/env bash


python setup.py install --record files.txt
cp g910-gkeys.service /etc/systemd/system
systemctl daemon-reload