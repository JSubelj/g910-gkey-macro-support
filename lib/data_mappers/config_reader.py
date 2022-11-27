import locale
import json
import os
from json.decoder import JSONDecodeError
from lib.misc import paths, logger
from lib.data_mappers import supported_configs, char_uinput_mapper
from lib import g910_gkey_mapper

log = logger.logger(__name__)


class ConfigException(Exception):
    pass


class Config:

    config: dict = None

    profile: str = None

    def __init__(self):
        self.profile = supported_configs.default_profile

    @staticmethod
    def validate_hotkey_action(do, hotkey_action, keyboard_mapping):
        if hotkey_action == "nothing" or hotkey_action == "run":
            return None
        if hotkey_action == "typeout":
            error = {}
            i = 0
            error["typeout"] = ""
            for c in do:
                try:
                    char_uinput_mapper.keys[keyboard_mapping][c]
                except KeyError:
                    error["typeout"] += f"Character \"{c}\" on position {str(i)} does not exist for keyboard mapping " \
                                        f"{keyboard_mapping}!"
                i += 1
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
                    i += 1
                    if len(key_string) == 1:
                        try:
                            char_uinput_mapper.keys[keyboard_mapping][key_string]
                        except KeyError:
                            error["shortcut"] += f"Character {key_string} on position {str(i)} for keyboard mapping: " \
                                                 f"{keyboard_mapping} does not exist! "

                    else:
                        try:
                            char_uinput_mapper.keys["control"][key_string]
                        except KeyError:
                            error["shortcut"] += "Control key "+key_string+" on position "+str(i)+" does not exist! "
            if error["shortcut"] == "":
                return None
            else:
                return error

    def validate_config(self, config_dic: dict):
        errors = []
        keyboard_mapping = config_dic.get("keyboard_mapping", supported_configs.default_keyboard_mapping)
        return_config = {"keyboard_mapping": keyboard_mapping}
        if keyboard_mapping not in supported_configs.keyboard_mappings:
            return {"keyboard_mapping": keyboard_mapping+" does not exist!"}, None

        return_config["notify"] = config_dic.get("notify", False)
        return_config["username"] = config_dic.get("username", "")

        profile_start_range = 1
        return_config["profiles"] = {}
        return_config["profiles"]["MEMORY_1"] = {}
        # backward compatibility if no profile is set in config default is used
        if config_dic.get("profiles", {}) is {}:
            profile_start_range = 2
            for i in range(1, 10):
                try:
                    return_config["profiles"]["MEMORY_1"]["MACRO_" + str(i)] = \
                        self.get_key_action(config_dic, "backward_compatibility", i)
                except ConfigException as e:
                    errors += [e]

        for profile_index in range(profile_start_range, 5):
            if profile_index == 4:
                profile_index = "RECORD"

            return_config["profiles"]["MEMORY_" + str(profile_index)] = {}
            for i in range(1, 10):
                try:
                    return_config["profiles"][f"MEMORY_{str(profile_index)}"][f"MACRO_{str(i)}"] = \
                        self.get_key_action(config_dic, profile_index, i)
                except ConfigException as e:
                    errors += [e]

        if len(errors) > 0:
            raise ConfigException(errors)
        else:
            return return_config

    def get_key_action(self, config_dic: dict, profile_index: str, i: int):
        keyboard_mapping = config_dic.get("keyboard_mapping", supported_configs.default_keyboard_mapping)
        key = "MACRO_" + str(i)
        if profile_index != "backward_compatibility":
            if config_dic.get("profiles", {}).get(f"MEMORY_{str(profile_index)}", {}) == {}:
                # compatibility < 0.3.0
                key = "g" + str(i)
                setting_for_gkey = config_dic.get("profiles", {}) \
                    .get("m" + str(profile_index), {}) \
                    .get(key, {})
            else:  # > 0.3.0
                setting_for_gkey = config_dic.get("profiles", {}) \
                    .get("MEMORY_" + str(profile_index), {}) \
                    .get(key, {})
        else:  # compatibility mode for old configs without profiles < 0.2.5
            key = "g" + str(i)
            setting_for_gkey = config_dic.get(key, {})

        hotkey_type = setting_for_gkey.get("hotkey_type", supported_configs.default_hotkey_type)
        if hotkey_type not in supported_configs.hotkey_types:
            raise ConfigException(f"{key} - hotkey_type {hotkey_type} does not exist!")
        do = setting_for_gkey.get("do", supported_configs.default_hotkey_do)
        do_validation = self.validate_hotkey_action(do, hotkey_type, keyboard_mapping)
        if do_validation:
            raise ConfigException(f"{key} - Do validation failed: {do_validation}")
        return {"hotkey_type": hotkey_type, "do": do}

    def update_config(self):
        self.config = self.read()

    def read(self):
        if self.config:
            return self.config

        log.info("Reading config from " + paths.config_path)
        try:
            with open(paths.config_path, "r") as f:
                self.config = self.validate_config(json.load(f))
                log.debug("using config: " + json.dumps(self.config, indent=4))
                return self.config

        except JSONDecodeError as e:
            log.error(f"JSONDecodeError: {str(e)} in {paths.config_path}")
        except ConfigException as e:
            log.warning(str(e))
        except FileNotFoundError:
            # this should no longer occur since config is created at start of the service if not exists
            log.error("No config found.")
        except Exception as e:
            log.exception(e)
        g910_gkey_mapper.program_running = False

    def get_profile(self):
        return self.read().get('profiles', {}).get(self.profile, {})

    @staticmethod
    def initialize_config(keyboard):
        # detect current locale and set as keyboard mapping
        user_lang, encoding = locale.getdefaultlocale()
        user_lang = user_lang.split("_")[0]
        # check for support and otherwise set to default
        if user_lang not in supported_configs.keyboard_mappings:
            log.warn(f"No support for {user_lang} keyboard layout. Using default (en).")
            user_lang = "en"
        config = {
            "keyboard_mapping": user_lang,
            "notify": "False",
            "username": "",
            "profiles": {}
        }
        for profile in keyboard.events.memoryKeys.values():
            config["profiles"].update({profile: {}})

            for macro_key in keyboard.events.macroKeys.values():
                key = "KEY_F" + str(12+int(macro_key.split("_")[1]))
                config["profiles"][profile][macro_key] = {"hotkey_type": "uinput", "do": key}

        return config

    @staticmethod
    def exists():
        return os.path.exists(paths.config_path)

    # Creates config
    @staticmethod
    def create(keyboard):
        if Config.exists():  # backup config if there is already one
            log.info("Backing up existing config to: " + paths.config_path + ".bak")
            os.rename(paths.config_path, paths.config_path + ".bak")

        config_json = Config.initialize_config(keyboard)
        with open(paths.config_path, "w") as f:
            log.info("Creating default config: " + paths.config_path)
            f.write(json.dumps(config_json, indent=4))
