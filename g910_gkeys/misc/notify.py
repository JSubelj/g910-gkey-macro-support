import subprocess
import os
from g910_gkeys.misc.config import Config
from g910_gkeys.misc.logger import Logger


class Notification:

    log = None

    config: Config = None

    def __init__(self, config: Config):
        self.log = Logger().logger(__name__)
        self.config = config

    def send_notification(self, profile: str):
        config = self.config.read()
        if config['notify'] != "False":
            command = f"notify-send -i keyboard Logitech-G910 \"Switched profile to {profile}\""
            self.log.debug(f"Sending notification: /bin/bash -c {command}")
            subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
