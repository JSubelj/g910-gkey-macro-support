#!/bin/bash
#
# uninstall/removes g910-gkeys.
#
# options:
#  -a               Remove all (configuration)
#  -d --dry-run     Only print what would be done

# check if we are 'root' user.
(( EUID != 0 )) && echo Must be root to run this script. Exiting. &&
    exit 1

FILESLST=files.txt
PIPCMD=""
REMOVECONF=n
DRYRUN=""
CONFDIR=/etc/g910-gkeys
OPTIONS=$(getopt -l "all,dry-run" -o "ad" -- "$@")
eval set -- "$OPTIONS"

usage() {
    echo "usage: ${0##*/}" [-a][-d]$'\n'
    echo "  -a --all         Remove all (configuration)"
    echo "  -d --dry-run     Only print what would be done"
    echo Exiting.
}

while true; do
    case "$1" in
        -a) REMOVECONF=y
           ;;
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
    echo "systemctl disable --now g910-gkeys &>/dev/null"
else
    systemctl disable --now g910-gkeys &>/dev/null
fi

# remove all installed files (not configuration files, in /etc/g910-gkeys)
[[ -f "$FILESLST" ]] &&
    ${DRYRUN} xargs --arg-file="$FILESLST" rm -rf &&
    [[ $DRYRUN = "" ]] && echo "Removed installed files"

# remove configuration file[s] if requested
if [[ "$REMOVECONF" = y ]]; then
    ${DRYRUN} rm -rf "$CONFDIR"
    [[ $DRYRUN = "" ]] && echo "Removed configuration files"
fi

# remove pip package
if [[ -n "$PIPCMD" ]]; then
    PIPLST=$($PIPCMD list | grep 'g910-gkeys' | cut -d " " -f 1)
    [[ -n "$PIPLST" ]] &&
        ${DRYRUN} ${PIPCMD} uninstall "$PIPLST" &&
        [[ $DRYRUN = "" ]] && echo "Uninstalled $PIPCMD files"
fi
