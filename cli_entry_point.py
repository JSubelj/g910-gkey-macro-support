#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from lib import g910_gkey_mapper, PROJECT_INFO
from lib.misc.config import Config


def main():
    parser = argparse.ArgumentParser(description=PROJECT_INFO.DESCRIPTION)
    parser.add_argument("--create-config", help="Creates config in /etc/g910-gkeys",
                        action='store_true', default=False)
    parser.add_argument("-s", "--set-config", help="Set the config file to use",
                        default='/etc/g910-gkeys/config.json', dest="config_file")
    parser.add_argument("-v", "--version", help="Displays the information about the driver",
                        action='version', version=f"%(prog)s {PROJECT_INFO.VERSION} by {PROJECT_INFO.AUTHOR}")
    args = parser.parse_args()
    if args.create_config:
        from lib.usb_device import USBDevice
        config = Config()
        device = USBDevice()  # init usb device and keyboard interface
        config.create(device.keyboard)  # create config with keyboard interface
        device.__exit__()  # clean up usb connection
    elif args.config_file != "/etc/g910-gkeys/config.json":
        Config.config_path = args.config_file
        g910_gkey_mapper.main()
    else:
        g910_gkey_mapper.main()


if __name__ == "__main__":
    main()
