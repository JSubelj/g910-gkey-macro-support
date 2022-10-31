#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from lib.misc import paths


def initialize_config():
    config = {}
    config["__comment"] = "following hotkey types are supported: nothing, typeout, shortcut, run and python; only en, fr, de and si keyboard mappings are currently supported"
    config["keyboard_mapping"] = "en"
    config["profiles"] = {
        "m1": {}, "m2": {}, "m3": {}, "mr": {}
    }
    for mkey in range(1, 4):
        config["profiles"]["m" + str(mkey)]["g1"] = {"hotkey_type": "typeout", "do": "Its WORKING!!!"}

        for i in range(2, 10):
            config["profiles"]["m" + str(mkey)]["g" + str(i)] = {"hotkey_type": "nothing", "do": ""}

    return config


def does_config_exists():
    return os.path.exists(paths.config_path)


# Creates config at home
def create():
    if does_config_exists():
        print("Backuping existing config to: " + paths.config_path + ".bak")
        os.rename(paths.config_path, paths.config_path + ".bak")

    with open(paths.config_path, "w") as f:
        print("Writting config at: " + paths.config_path)
        f.write(json.dumps(initialize_config(), indent=4))
