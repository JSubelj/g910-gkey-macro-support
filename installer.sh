#!/usr/bin/env bash
#
# installs g910-gkeys.
#
# options:
#  -n: DO NOT enable and start systemd service.

# get system unit directory
START_SERVICE=y
SUPPORTED_KEYBOARDS=(de en fr si)
KEYBOARD=$(locale | grep LANG= | cut -d= -f2 | cut -d_ -f1)

usage() {
    echo "usage: ${0##*/} [-n]"
}

while getopts nl: opt ; do
    case "$opt" in
        n) START_SERVICE=n
           ;;
        *) usage
           exit 1
           ;;
    esac
done

[[ ! " ${SUPPORTED_KEYBOARDS[*]} " =~ ${KEYBOARD} ]] &&
	echo "Your system default language is $KEYBOARD, but it's not supported." &&
	echo "You can try to run: sudo python3 cli_entry_point.py -l create" &&
	echo "You need to add the created mapping to lib.data_mappers.char_uinput_mapper and" &&
	echo "add your locale to lib.data_mappers.supported_configs, before installing again." &&
	echo "Please open a feature request on github with your language:" &&
	echo "https://github.com/JSubelj/g910-gkey-macro-support/issues/new/choose" &&
	exit 1

# install via pip
pip install -e ./

# make config dir
if [[ ! -d "$HOME"/.config/g910-gkeys ]]; then
  mkdir "$HOME"/.config/g910-gkeys
fi

# check for existing config file
if [[ ! -f "$HOME"/.config/g910-gkeys/config.json ]]; then
  if [[ -f /etc/g910-gkeys/config.json ]]; then
    # if old config exist move it to new location (will need root privileges)
    sudo mv /etc/g910-gkeys/config.json "$HOME"/.config/g910-gkeys/config.json
    sudo chown "$USER":"$USER" "$HOME"/.config/g910-gkeys/config.json
  else
    # if not copy default config to config dir
    cp ./etc/config.json "$HOME"/.config/g910-gkeys/config.json
  fi
fi

# copy service unit to user home
if [[ -d "$HOME"/.config/systemd/user ]]; then
  cp ./etc/g910-gkeys.service "$HOME"/.config/systemd/user/g910-gkeys.service
fi

# reload daemon
systemctl --user daemon-reload

# enable and start service if necessary
if [[ $START_SERVICE = y ]]; then
    systemctl --user enable --now g910-gkeys.service
else
    echo "g910-gkeys service was not started."
    echo "You can enable/start it with this command: "
    echo "  systemctl --user enable --now g910-gkeys.service"
fi
