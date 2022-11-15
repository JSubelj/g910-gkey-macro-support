#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from lib import g910_gkey_mapper, PROJECT_INFO
from lib.misc.layout_config_helpers import LayoutHelper


def main():
    parser = argparse.ArgumentParser(description=PROJECT_INFO.DESCRIPTION)
    parser.add_argument("--create-config", help="Creates config in /etc/g910-gkeys",
                        action='store_true', default=False)
    parser.add_argument("-c", "--set-config", help="Set the config file to use",
                        default='/etc/g910-gkeys/config.json', dest="config_file")
    parser.add_argument("-l", "--layout-helper", help="Run layout helper tools.",
                        dest="layout_helper")
    parser.add_argument("-v", "--version", help="Displays the information about the driver",
                        action='store_true', default=False)
    args = parser.parse_args()
    if args.create_config:
        from lib.misc import create_config

        create_config.create()
    elif args.version:
        print(PROJECT_INFO.NAME)
        print()
        print(PROJECT_INFO.DESCRIPTION)
        print()
        print("Created by", PROJECT_INFO.AUTHOR)
        print("Version", PROJECT_INFO.VERSION)
    elif args.config_file != "/etc/g910-gkeys/config.json":
        from lib.misc import paths

        paths.config_path = args.config_file
        g910_gkey_mapper.main()
    elif args.layout_helper:
        LayoutHelper(args.layout_helper)
    else:
        g910_gkey_mapper.main()


if __name__ == "__main__":
    main()
