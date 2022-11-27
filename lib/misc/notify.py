import subprocess
import os
from lib.data_mappers.config_reader import Config
from lib.misc import logger

log = logger.logger(__name__)


class Notification:

    config: Config = None

    def __init__(self, config: Config):
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
                    log.warn("Notifications enabled but no username set in config!")
            else:
                command = inner_command  # if run as user we can use notify-send directly

            if command is not None:
                log.debug(f"Sending notification: /bin/bash -c {command}")
                subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
