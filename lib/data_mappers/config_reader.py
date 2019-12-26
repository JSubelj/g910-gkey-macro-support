import json
from lib.misc import paths, logger
from lib.data_mappers import supported_configs, char_uinput_mapper

log = logger.logger(__name__)
config = None

def validate_hotkey_action(do, hotkey_action, keyboard_mapping):
    if hotkey_action == "nothing" or hotkey_action == "run" or hotkey_action == "swap_config":
        return None
    if hotkey_action == "typeout":
        error = {}
        i = 0
        error["typeout"] = ""
        for c in do:
            try:
                char_uinput_mapper.keys[keyboard_mapping][c]
            except:
                error["typeout"] += "Character "+c+" on position "+str(i)+" for keyboard mapping: "+keyboard_mapping+" does not exist! "
            i+=1
        if error["typeout"] == "":
            return None
        return error
    if hotkey_action == "shortcut":
        error = {}
        press_together = []

        together = do.split(",")
        for hotkey in together:
            keys_str = hotkey.split("+")
            press_together.append(keys_str)

        error["shortcut"] = ""
        i = 0
        for combo in press_together:
            for key_string in combo:
                i+=1
                if len(key_string) == 1:
                    try:
                        char_uinput_mapper.keys[keyboard_mapping][key_string]
                    except:
                        error["shortcut"]+="Character "+key_string+" on position "+str(i)+" for keyboard mapping: "+keyboard_mapping+" does not exist! "

                else:
                    try:
                        char_uinput_mapper.keys["control"][key_string]
                    except:
                        error["shortcut"]+="Control key "+key_string+" on position "+str(i)+" does not exist! "
        if error["shortcut"] == "":
            return None
        else:
            return error


def validate_config(config_dic : dict):
    errors = {}
    paths.color = config_dic.get("color", supported_configs.default_color)
    keyboard_mapping = config_dic.get("keyboard_mapping", supported_configs.default_keyboard_mapping)
    return_config = {"keyboard_mapping": keyboard_mapping}
    if keyboard_mapping not in supported_configs.keyboard_mappings:
        return {"keyboard_mapping": keyboard_mapping+" does not exist!"}, None
    
    #m 1-3 keys
    for i in range(1,4):
        setting_for_gkey = config_dic.get("m"+str(i), {})
        hotkey_type = setting_for_gkey.get("hotkey_type",supported_configs.default_hotkey_type)
        errors["m" + str(i)] = {}
        if hotkey_type not in supported_configs.hotkey_types:
            errors["m" + str(i)]["hotkey_type"] = hotkey_type + " does not exist!"
        do = setting_for_gkey.get("do",supported_configs.default_hotkey_do)
        do_validation = validate_hotkey_action(do, hotkey_type, keyboard_mapping)
        if do_validation:
            errors["m" + str(i)]["do"] = do_validation.copy()
            do = ""
            hotkey_type = "nothing"
        if len(errors["m" + str(i)]) == 0:
            errors.pop("m" + str(i))
        return_config["m" + str(i)] = {"hotkey_type": hotkey_type, "do": do}
    
    #mr key
    setting_for_gkey = config_dic.get("mr", {})
    hotkey_type = setting_for_gkey.get("hotkey_type",supported_configs.default_hotkey_type)
    errors["mr"] = {}
    if hotkey_type not in supported_configs.hotkey_types:
        errors["mr"]["hotkey_type"] = hotkey_type + " does not exist!"
    do = setting_for_gkey.get("do",supported_configs.default_hotkey_do)
    do_validation = validate_hotkey_action(do, hotkey_type, keyboard_mapping)
    if do_validation:
        errors["mr"]["do"] = do_validation.copy()
        do = ""
        hotkey_type = "nothing"
    if len(errors["mr"]) == 0:
        errors.pop("mr")
    return_config["mr"] = {"hotkey_type": hotkey_type, "do": do}

    #g keys
    for i in range(1,10):
        setting_for_gkey = config_dic.get("g"+str(i), {})
        hotkey_type = setting_for_gkey.get("hotkey_type",supported_configs.default_hotkey_type)
        errors["g" + str(i)] = {}
        if hotkey_type not in supported_configs.hotkey_types:
            errors["g" + str(i)]["hotkey_type"] = hotkey_type + " does not exist!"
        do = setting_for_gkey.get("do",supported_configs.default_hotkey_do)
        do_validation = validate_hotkey_action(do, hotkey_type, keyboard_mapping)
        if do_validation:
            errors["g" + str(i)]["do"] = do_validation.copy()
            do = ""
            hotkey_type = "nothing"
        if len(errors["g" + str(i)]) == 0:
            errors.pop("g" + str(i))
        return_config["g" + str(i)] = {"hotkey_type": hotkey_type, "do": do}

    if len(errors) == 0:
        return None, return_config

    return errors, return_config

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
                err, config = validate_config(json.load(f))
                log.debug("using config: " + str(config))
                if err:
                    log.warning("Error(s) in config: "+str(err))
                return config
            except:
                log.error("JSON FILE ERROR, CORRECT JSON! in path: " + paths.config_path)
                print("JSON FILE ERROR, CORRECT JSON! in path: " + paths.config_path)
                exit(1)
    except:
        log.error("NO CONFIG FOUND! Create config.json in " + paths.config_path)
        print("NO CONFIG FOUND! Create config.json in " + paths.config_path + "\n To create default config run: g910-gkeys --create-config\n")
        exit(1)
