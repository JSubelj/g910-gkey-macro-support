
import json
import uinput
import os, sys


main_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
config_path = os.path.join(main_dir, "config/config.json")

def string_to_keys(cmd : str):
    keys = []
    for c in cmd:
        # TODO: to dictionary
        if c == " ":
            c = "SPACE"
        keys.append((getattr(uinput,"KEY_"+c.upper()), c))

    return keys

def keys_to_writing(device, keys : list):
    for key, char in keys:
        if char.isupper():
            device.emit(uinput.KEY_LEFTSHIFT, 1)
        device.emit_click(key)
        if char.isupper():
            device.emit(uinput.KEY_LEFTSHIFT, 0)

def execude_writing_command(device, str):
    keys_to_writing(device, string_to_keys(str))


def hotkeys_to_keys(string: str):
    keys_for_hotkey = string.split(",")
    keys = []
    for str_key in keys_for_hotkey:
        # TODO: to dictionary
        if str_key.upper() == "SHIFT":
            key = "LEFTSHIFT"
        elif str_key.upper() == "CTRL":
            key = "LEFTCTRL"
        elif str_key.upper() == "ALT":
            key = "LEFTALT"
        else:
            key=str_key
        print("KEY_" + key.upper())
        keys.append(getattr(uinput, "KEY_"+key.upper()))

    return keys

def hotkeys_list_execute(device, keys):
    for key in keys:
        print("pressing "+str(key))
        device.emit(key,1)

    for key in keys:
        print("releasing "+str(key))
        device.emit(key,0)


def execute_hotkey(device, str):
    keys = hotkeys_to_keys(str)
    print(keys)
    print("inhere")

    hotkeys_list_execute(device, keys)


import subprocess
def execute_command(command):
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def resolve_config(key):
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except:
            print("\nJSON FILE ERROR, CORRECT JSON!\n")
            exit(1)



    if key not in config.keys():
        return lambda _: None

    key_config : dict = config[key]
    command = key_config.get("command",-1)

    if command == 0:
        return lambda device: execude_writing_command(device, key_config["make"])
    if command == 1:
        return lambda device: execute_hotkey(device, key_config["make"])
    if command == 2:
        return lambda _: execute_command(key_config["make"])
    if command == -1:
        return lambda _: None




import inspect

def g1(device):
    resolve_config("g1")(device)

def g2(device):
    resolve_config("g2")(device)


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
