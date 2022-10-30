#!/usr/bin/env bash
#
# installs g910-gkeys.
#
# options:
#  -n: DO NOT enable and start systemd service.

# check if we are 'root' user.
(( EUID != 0 )) && echo Must be root to run this script. Exiting. &&
    exit 1

# get system unit directory
DEST=$(pkg-config systemd --variable=systemdsystemunitdir)
CONFDIR=/etc/g910-gkeys
FILES=files.txt
STARTSERVICE=y
SUPPORTED_KEYBOARDS=(en fr si)
KEYBOARD=$(locale | grep LANG= | cut -d= -f2 | cut -d_ -f1)

usage() {
    echo "usage: ${0##*/} [-n]"
}

while getopts nl: opt ; do
    case "$opt" in
        n) STARTSERVICE=n
           ;;
        *) usage
           exit 1
           ;;
    esac
done

[[ ! " ${SUPPORTED_KEYBOARDS[@]} " =~ " ${KEYBOARD} " ]] &&
	echo "Your system default language is $KEYBOARD, but it's not supported." &&
	echo "Please open a feature request on github with your language:" &&
	echo "https://github.com/JSubelj/g910-gkey-macro-support/issues/new/choose" &&
	exit 1

python3 setup.py install --record "$FILES"

# systemd service file
echo "$DEST"/g910-gkeys.service >> "$FILES"
cp g910-gkeys.service "$DEST"/g910-gkeys.service

systemctl daemon-reload

# enable and start service if necessary
if [[ $STARTSERVICE = y ]]; then
    systemctl enable --now g910-gkeys.service
else
    echo "g910-gkeys service was not started."
    echo "You can enable/start it with this command: "
    echo "  systemctl enable --now g910-gkeys.service"
fi
