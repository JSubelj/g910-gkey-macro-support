import subprocess
from lib.data_mappers import config_reader
from lib.misc import logger

log = logger.logger(__name__)


def send_notification(profile: str):
    config = config_reader.read()
    if config['notify'] == 'True' and config['username'] != '':
        inner_command = f"'notify-send -i keyboard Logitech-G910 \"Switched profile to {profile}\"'"
        command = f"su {config['username']} -c {inner_command}"
        log.debug(f"/bin/bash -c {command}")
        subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
