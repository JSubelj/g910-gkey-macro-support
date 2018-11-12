#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib import g910_gkey_mapper
import argparse
import os
from pathlib import Path
from lib.misc import create_config

config_path = os.path.join(Path.home(), ".g910-gkeys-config/config.json")


def main():
    parser = argparse.ArgumentParser(description="Support for Logitech G910 GKeys on Linux")
    parser.add_argument("--create-config", help="Creates config in "+config_path, action='store_true', default=False)
    args = parser.parse_args()
    if args.create_config:
        create_config.create()
    else:
        g910_gkey_mapper.main()

if __name__=="__main__":
    main()
