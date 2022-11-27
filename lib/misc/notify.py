import subprocess
from lib.data_mappers.config_reader import Config
from lib.misc import logger

log = logger.logger(__name__)


class Notification:

    config: Config = None

    def __init__(self, config: Config):
        self.config = config

    def send_notification(self, profile: str):
        config = self.config.read()
        if config['notify'] == 'True' and config['username'] != '':
            inner_command = f"'notify-send -i keyboard Logitech-G910 \"Switched profile to {profile}\"'"
            command = f"su {config['username']} -c {inner_command}"
            log.debug(f"/bin/bash -c {command}")
            subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
