import subprocess
from lib.data_mappers import config_reader, supported_configs
from lib.misc import logger
from lib.uinput_keyboard import keyboard

log = logger.logger(__name__)

valid_gkeys = ["g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9"]


def execute_writing(string_to_write: str, device):
    keyboard.writeout(string_to_write, config_reader.read()["keyboard_mapping"], device)


def execute_hotkey(string_for_hotkey: str, device):
    keyboard.shortcut(
        string_for_hotkey, config_reader.read()["keyboard_mapping"], device
    )


def execute_command(command):
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def release(device):
    keyboard.release(device)


def resolve_config(key):

    config = config_reader.read()

    if key not in config:
        log.info(f"{key} pressed, unbound in config, doing nothing!")
        return lambda _: None

    key_config: dict = config[key]

    do = key_config.get('do', supported_configs.default_hotkey_do)
    if not do:
        log.info(f"{key} pressed, but do is empty or not set, doing nothing!")
        return lambda _: None

    command = key_config.get("hotkey_type", supported_configs.default_hotkey_type)
    if command not in supported_configs.hotkey_types:
        raise Exception(
            f'hotkey_type: "{command}" for key "{key}" not known! hotkey_types '
            f"can only be one of: {supported_configs.hotkey_types}"
        )

    if command == 'typeout':
        log.info(f"{key} pressed, typing out: {repr(do)}")
        return lambda device: execute_writing(do, device)
    if command == 'shortcut':
        log.info(f"{key} pressed, pressing: {do}")
        return lambda device: execute_hotkey(do, device)
    if command == 'run':
        log.info(f"{key} pressed, running: {do}")
        return lambda _: execute_command(do)

    # only nothing key config remains
    log.info(f"{key} pressed, doing nothing!")
    return lambda _: None


def handle_gkey_press(device, key: str):
    """
    Handles a key press
    :param device: the usb device pressed
    :param key: the string of the gkey pressed (g1-g9)
    :return: True if keypress was handled, false if it was not
    """
    if key in valid_gkeys:
        resolve_config(key)(device)
        return True
    return False
