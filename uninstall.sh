#!/bin/bash
#
# uninstall g910-gkeys.
#
# options:
#  -d --dry-run     Only print what would be done

PIPCMD=""
DRYRUN=""
OPTIONS=$(getopt -l "all,dry-run" -o "ad" -- "$@")
eval set -- "$OPTIONS"

usage() {
    echo "usage: ${0##*/}" [-d]$'\n'
    echo "  -d --dry-run     Only print what would be done"
    echo Exiting.
}

while true; do
    case "$1" in
        -d|--dry-run) DRYRUN="echo"
           ;;
        --)
           break;;
    esac
    shift
done

# determine if we should use pip or pip3, pip3 being preferred
for p in pip pip3; do
    type "$p" &>/dev/null && PIPCMD="$p"
done

# stops and disable service
${DRYRUN} systemctl disable --now g910-gkeys &>/dev/null # <= 0.3.0
${DRYRUN} systemctl --user disable --now g910-gkeys &>/dev/null # >= 0.4.0

# remove pip package
if [[ -n "$PIPCMD" ]]; then
    PIPLST=$($PIPCMD list | grep 'g910-gkeys' | cut -d " " -f 1)
    [[ -n "$PIPLST" ]] &&
        ${DRYRUN} ${PIPCMD} uninstall -q "$PIPLST" &&
        [[ $DRYRUN = "" ]] && echo "Uninstalled $PIPCMD files"
fi

# remove service unit <= 0.3.0
if [[ -f /etc/systemd/system/g910-gkeys.service ]]; then
    ${DRYRUN} rm /etc/systemd/system/g910-gkeys.service &&
        [[ $DRYRUN = "" ]] && echo "Removed service unit"
fi

# remove service unit >= 0.4.0
if [[ -f "$HOME"/.config/systemd/user/g910-gkeys.service ]]; then
    ${DRYRUN} rm "$HOME"/.config/systemd/user/g910-gkeys.service &&
    [[ $DRYRUN = "" ]] && echo "Removed service unit"
fi

# remove udev rules
if [[ -f /etc/udev/rules.d/60-g910-gkeys.rules ]]; then
  ${DRYRUN} sudo rm /etc/udev/rules.d/60-g910-gkeys.rules &&
  [[ $DRYRUN = "" ]] && echo "Removed udev rules"
fi

# remove uinput config for kernel
if [[ -f /etc/modules-load.d/uinput-g910-gkeys.conf ]]; then
  ${DRYRUN} sudo rm /etc/modules-load.d/uinput-g910-gkeys.conf &&
  [[ $DRYRUN = "" ]] && echo "Removed uinput enable config"
fi
