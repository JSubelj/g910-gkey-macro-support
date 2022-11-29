import subprocess
import os
from lib.data_mappers.config import Config
from lib.misc.logger import Logger


class Notification:

    log = None

    config: Config = None

    def __init__(self, config: Config):
        self.log = Logger().logger(__name__)
        self.config = config

    def send_notification(self, profile: str):
        config = self.config.read()
        if config['notify'] == "True":
            inner_command = f"notify-send -i keyboard Logitech-G910 \"Switched profile to {profile}\""
            command = None
            if os.geteuid() == 0:
                if config['username'] != "":
                    # if run as root service use su <username> wrapper
                    command = f"su {config['username']} -c '{inner_command}'"
                else:
                    self.log.warn("Notifications enabled but no username set in config!")
            else:
                command = inner_command  # if run as user we can use notify-send directly

            if command is not None:
                self.log.debug(f"Sending notification: /bin/bash -c {command}")
                subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
