import ast
import subprocess
import inspect
import sys
from lib.data_mappers import config_reader, supported_configs
from lib.misc import logger
from lib.uinput_keyboard import keyboard
from lib.functionalities import g910_led

log = logger.logger(__name__)


def execute_writing(string_to_write: str, device):
    keyboard.writeout(string_to_write, config_reader.read()["keyboard_mapping"], device)


def execute_hotkey(string_for_hotkey: str, device):
    keyboard.shortcut(
        string_for_hotkey, config_reader.read()["keyboard_mapping"], device
    )


def execute_command(command):
    subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def execute_python(command: str, device):
    try:
        global output_string
        output_string = None
        ast.parse(command)
        exec(command)
        if output_string:
            keyboard.writeout(output_string,config_reader.read()['keyboard_mapping'],device)
    except Exception as e:
        log.error(f"{type(e).__name__} when running python command '{command}'\nDetails: '{str(e)}'")


def execute_change_profile(key):
    supported_configs.profile = key

    if g910_led.is_installed():
        n = key[1]
        if n == 'r':
            subprocess.run(['g910-led', '-mn', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mr', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif n == '1' or n == '2':
            subprocess.run(['g910-led', '-mr', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mn', n], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['g910-led', '-mr', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mn', '4'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    config = config_reader.read()
    notify = config['notify']
    username = config['username']
    if notify == 'True' and username != '':
        command = f"su {username} -c 'notify-send -i keyboard Logitech-G910 \"Switched profile to {key}\"'"
        log.debug('/bin/bash -c' + command)
        subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def release(device):
    keyboard.release(device)


def resolve_config(key):
    config = config_reader.read()['profiles'].get(supported_configs.profile, "m1")

    if key in [ "m1", "m2", "m3", "mr"]:
        log.info(f"{key} pressed, change profile to {key}")
        return lambda _: execute_change_profile(key)

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
    if command == 'python':
        log.info(f"{key} pressed, running: {do}")
        return lambda device: execute_python(do, device)

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
    if key in supported_configs.valid_keys:
        resolve_config(key)(device)
        return True
    return False
