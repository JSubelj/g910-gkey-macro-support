import subprocess
import inspect
from lib import g910_gkey_mapper
from lib.data_mappers import hotkey_type, config_reader
from lib.misc import logger
from lib.uinput_keyboard import keyboard

log = logger.logger(__name__)


def execute_writing(string_to_write: str, device):
    keyboard.writeout(string_to_write,config_reader.read()['keyboard_mapping'],device)

def execute_hotkey(string_for_hotkey: str, device):
    keyboard.shortcut(string_for_hotkey, config_reader.read()['keyboard_mapping'], device)

def execute_release(device):
    keyboard.release(device)

def execute_command(command):
    #subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def execute_change_profile(key):
    global profile 
    profile = key

    if g910_gkey_mapper.g910_led:
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


def resolve_config(key):


    config = config_reader.read()['profiles'][profile]

    if key not in config.keys():
        log.info(key+" pressed, unbound in config, doing nothing!")
        return lambda _: None

    key_config : dict = config[key]
    command = key_config.get("hotkey_type","nothing")
    try:
        command = hotkey_type.type[command]
    except KeyError:
        raise Exception("hotkey_type: \""+command+"\" for key "+key+" not known! hotkey_types can only be: nothing, typeout, shortcut and run!")
    if command == 0:

        log.info(key+" pressed, typing out: "+repr(key_config["do"]))
        return lambda device: execute_writing(key_config["do"], device)
    if command == 1:
        log.info(key+" pressed, pressing: "+key_config["do"])
        return lambda device: execute_hotkey(key_config["do"], device)
    if command == 2:
        log.info(key+" pressed, running: "+key_config["do"])
        return lambda _: execute_command(key_config["do"])
    if command == -1:
        log.info(key+" pressed, doing nothing!")
        return lambda _: None

def switch_profile(key):
    if key in [ "m1", "m2", "m3", "mr"]:
        log.info(key+" pressed, change profile to "+key)
        return lambda _: execute_change_profile(key)

def release(device):
    execute_release(device)

def g1(device):
    resolve_config(inspect.stack()[0][3])(device)

def g2(device):
    resolve_config(inspect.stack()[0][3])(device)


def g3(device):
    resolve_config(inspect.stack()[0][3])(device)


def g4(device):
    resolve_config(inspect.stack()[0][3])(device)


def g5(device):
    resolve_config(inspect.stack()[0][3])(device)


def g6(device):
    resolve_config(inspect.stack()[0][3])(device)


def g7(device):
    resolve_config(inspect.stack()[0][3])(device)


def g8(device):
    resolve_config(inspect.stack()[0][3])(device)


def g9(device):
    resolve_config(inspect.stack()[0][3])(device)


def m1(device):
    switch_profile(inspect.stack()[0][3])(device)


def m2(device):
    switch_profile(inspect.stack()[0][3])(device)


def m3(device):
    switch_profile(inspect.stack()[0][3])(device)


def mr(device):
    switch_profile(inspect.stack()[0][3])(device)
