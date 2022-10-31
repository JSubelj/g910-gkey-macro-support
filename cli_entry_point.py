#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import lib.PROJECT_INFO as PROJECT_INFO

def main():
    parser = argparse.ArgumentParser(description="Support for Logitech G910 GKeys on Linux")
    parser.add_argument("--create-config", help="Creates config in /etc/g910-gkeys", action='store_true', default=False)
    parser.add_argument("-v","--version", help="Displays the information about the driver", action='store_true', default=False)
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
    else:
        from lib import g910_gkey_mapper
        from lib.misc import paths

        g910_gkey_mapper.main()

if __name__=="__main__":
    main()
