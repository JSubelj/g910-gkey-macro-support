#!/usr/bin/env bash

# check if we are 'root' user.
(( EUID != 0 )) && echo Must be root to run this script. Exiting. &&
    exit 1

# get system unit directory
DEST=$(pkg-config systemd --variable=systemdsystemunitdir)
CONFDIR=/etc/g910-gkeys
FILES=files.txt

python3 setup.py install --record "$FILES"

# systemd service file
echo "$DEST"/g910-gkeys.service >> "$FILES"
cp g910-gkeys.service "$DEST"/g910-gkeys.service

# configuration file - will not overwrite existing files.
[[ -d "$CONFDIR" ]] ||  mkdir "$CONFDIR"
rsync -a -v --ignore-existing config/* "$CONFDIR"

# enable and start service
systemctl enable --now g910-gkeys.service
