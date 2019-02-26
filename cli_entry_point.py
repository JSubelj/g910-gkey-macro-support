#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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
        from lib.misc import logger
        from lib import g910_gkey_mapper
        from lib.misc import paths

        log = logger.logger("launcher")

        print("Starting g910-gkeys, logging at:", paths.logs_path)
        log.info("------------------------------------------------------------------------------------")
        log.info(
            "----------------------STARTED g910-keys-pid:" + str(os.getpid()) + "-----------------------------------")
        log.info("------------------------------------------------------------------------------------")
        #pid: ",os.getpid(),
        #pid_handler.kill_previous()
        g910_gkey_mapper.main()
        #pid_handler.write_pid(os.getpid())
        #Daemonize(app="g910-keys", pid=paths.pid_path, action=g910_gkey_mapper.main, keep_fds=[logger.fh.stream.fileno()]).start()
        '''else:
            print("g910-keys daemon already exists on pid:",paths.read_pid())
            print("if you made sure that the program isn't running ('ps -p "+paths.read_pid()+" -o comm=' returns nothing) then manually remove pid file:")
            print()
            print("    rm "+paths.pid_path)
            print()'''
if __name__=="__main__":
    main()
