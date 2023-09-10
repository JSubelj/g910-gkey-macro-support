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
if [[ $DRYRUN = "echo" ]]; then
    echo "systemctl --user disable --now g910-gkeys &>/dev/null"
else
    systemctl --user disable --now g910-gkeys &>/dev/null
fi

# remove pip package
if [[ -n "$PIPCMD" ]]; then
    PIPLST=$($PIPCMD list | grep 'g910-gkeys' | cut -d " " -f 1)
    [[ -n "$PIPLST" ]] &&
        ${DRYRUN} ${PIPCMD} uninstall -q "$PIPLST" &&
        [[ $DRYRUN = "" ]] && echo "Uninstalled $PIPCMD files"
fi

# remove service unit
if [[ -f "$HOME"/.config/systemd/user/g910-gkeys.service ]]; then
    ${DRYRUN} rm "$HOME"/.config/systemd/user/g910-gkeys.service &&
    [[ $DRYRUN = "" ]] && echo "Removed service unit"
fi