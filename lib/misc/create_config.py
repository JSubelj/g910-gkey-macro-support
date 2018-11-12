#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from lib.misc import paths

def initialize_config():
    config = {}
    config["__comment"] = "following hotkey types are supported: nothing, typeout, shortcut, run"
    for i in range(1,10):
        config["g"+str(i)] = {"hotkey_type": "nothing", "do":""}

    return config

# Creates config at home
def create():
    if os.path.exists(paths.config_path):
        print("Backuping existing config to: "+paths.config_path+".bak")
        os.rename(paths.config_path, paths.config_path+".bak")


    with open(paths.config_path,"w") as f:
        print("Writting config at: "+paths.config_path)
        f.write(json.dumps(initialize_config(), indent=4))


