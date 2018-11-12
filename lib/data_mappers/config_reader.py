import sys
import os
import json
from pathlib import Path

main_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
config_path_here = os.path.join(main_dir, "config/config.json")
config_path_home = os.path.join(Path.home(), ".g910-gkeys-config/config.json")

def read_config_from_home():
    print("Reading config from " + config_path_home)
    try:
        with open(config_path_home, "r") as f:
            try:
                return json.load(f)
            except:
                print("\nJSON FILE ERROR, CORRECT JSON! in path: " + config_path_home + "\n")
                exit(1)
    except:
        print("\nNO CONFIG FOUND! Create config.json in " + config_path_home)
        exit(1)

def read_config_from_here():
    print("Reading config from " + config_path_here)
    try:
        with open(config_path_here, "r") as f:
            try:
                return json.load(f)
            except:
                print("\nJSON FILE ERROR, CORRECT JSON! in path: " + config_path_here + "\n")
                exit(1)
    except:
        print("\nNO CONFIG FOUND! Create config.json in " + config_path_here)
        exit(1)

def read():
    command = sys.argv[0].split("/")[-1]
    if command == "launcher.py":
        return read_config_from_here()
    else:
        return read_config_from_home()

