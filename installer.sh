#!/usr/bin/env bash
#
# installs g910-gkeys.
#
# options:
#  -n: DO NOT enable and start systemd service.
#  -l keyboard-type:
#     Currently only "en" (english) and "si" (slovenian) are supported.
#     Default is "si".
#
# TODO: ask user if he/she wants to replace his/her configuration.

# check if we are 'root' user.
(( EUID != 0 )) && echo Must be root to run this script. Exiting. &&
    exit 1

# get system unit directory
DEST=$(pkg-config systemd --variable=systemdsystemunitdir)
CONFDIR=/etc/g910-gkeys
FILES=files.txt
STARTSERVICE=y
SUPPORTED_KEYBOARDS=(en si)
KEYBOARD="si"

usage() {
    echo "usage: ${0##*/} [-n][-l keyboard-type]"
    echo "   Supported keyboards are :"
    echo "    en: (english/us)"
    echo "    si: (slovenian, the default)"
    echo "Exiting."
}

while getopts nl: opt ; do
    case "$opt" in
        n) STARTSERVICE=n
           ;;
        l) KEYBOARD=${OPTARG}
           [[ ! " ${SUPPORTED_KEYBOARDS[@]} " =~ " ${KEYBOARD} " ]] && usage
           ;;
        *) usage
           exit 1
           ;;
    esac
done

python3 setup.py install --record "$FILES"

# systemd service file
echo "$DEST"/g910-gkeys.service >> "$FILES"
cp g910-gkeys.service "$DEST"/g910-gkeys.service

# configuration file - will not overwrite existing files.
[[ -d "$CONFDIR" ]] ||  mkdir "$CONFDIR"
cp -a -n "config/config.$KEYBOARD.json" "$CONFDIR"/config.json || true

systemctl daemon-reload

# enable and start service if necessary
if [[ $STARTSERVICE = y ]]; then
    systemctl enable --now g910-gkeys.service
else
    echo "g910-gkeys service was not started."
    echo "You can enable/start it with this command: "
    echo "  systemctl enable --now g910-gkeys.service"
fi
