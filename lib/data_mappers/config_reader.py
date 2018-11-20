import json
from lib.misc import paths
from lib.misc import logger

log = logger.logger(__name__)

config = None

def update_config():
    global config
    config = None
    config = read()

def read():
    global config
    if config:
        return config

    log.debug("Reading config from " + paths.config_path)
    try:
        with open(paths.config_path, "r") as f:
            try:
                config = json.load(f)
                return config
            except:
                log.error("JSON FILE ERROR, CORRECT JSON! in path: " + paths.config_path)
                print("JSON FILE ERROR, CORRECT JSON! in path: " + paths.config_path)
                exit(1)
    except:
        log.error("NO CONFIG FOUND! Create config.json in " + paths.config_path)
        print("NO CONFIG FOUND! Create config.json in " + paths.config_path + "\n To create default config run: g910-gkeys --create-config\n")
        exit(1)
