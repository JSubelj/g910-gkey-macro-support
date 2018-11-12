#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import json

config_path = os.path.join(Path.home(), ".g910-gkeys-config/config.json")
config_dir = os.path.join(Path.home(), ".g910-gkeys-config")

def initialize_config():
    config = {}
    config["__comment"] = "following hotkey types are supported: nothing, typeout, shortcut, run"
    for i in range(1,10):
        config["g"+str(i)] = {"hotkey_type": "nothing", "do":""}

    return config

# Creates config at home
def create():
    if not os.path.exists(config_dir):
        print("Creating directory: "+config_dir)
        os.makedirs(config_dir)

    if os.path.exists(config_path):
        print("Backuping existing config to: "+config_path+".bak")
        os.rename(config_path, config_path+".bak")


    with open(config_path,"w") as f:
        print("Writting config at: "+config_path)
        f.write(json.dumps(initialize_config(), indent=4))


