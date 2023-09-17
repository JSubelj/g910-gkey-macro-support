import os
from lib.data_mappers import supported_configs
from lib.data_mappers.config_reader import ConfigException, Config
from lib.misc.helper import Helper
from lib.usb_device import USBDevice

config: Config

config_key_action = {
    "hotkey_type": "shortcut",
    "do": "ctrl+c"
}

config_dict = {
    "keyboard_mapping": Helper.get_locale(),
    "notify": "False",
    "profiles": {
        "MEMORY_1": {
            "MACRO_1": config_key_action
        }
    }
}

invalid_config_dict = {
    "keyboard_mapping": Helper.get_locale(),
    "notify": "False",
    "profiles": {
        "MEMORY_1": {
            "MACRO_1": {
                "hotkey_type": "invalid",
                "do": "invalid"
            }
        }
    }
}


class TestConfig:

    def test_config(self):
        """
        Initialize config class
        """
        global config
        config = Config()
        assert config is not None

    def test_config_delete(self):
        """
        Delete config for next test
        """
        if os.path.exists(config.config_path):
            os.remove(config.config_path)
        assert os.path.exists(config.config_path) is False

    def test_config_create(self):
        """
        Test creating config with found keyboard interface
        """
        global config
        # usb keyboard
        device = USBDevice()
        config.create(device.keyboard)
        assert config is not None and os.path.exists(config.config_path)

    def test_config_read(self):
        """
        Test reading from config
        """
        global config
        # detect current locale and set as keyboard mapping
        user_lang = Helper.get_locale()
        assert config is not None and config.read()["keyboard_mapping"] == user_lang

    def test_config_get_key_action(self):
        """
        Test get key action for assigned macro key
        """
        global config
        key_action = config.get_key_action(config_dict, "1", 1)
        assert key_action == config_key_action

    def test_config_get_key_action_not_defined(self):
        """
        Test get key action for not assigned macro key
        """
        global config
        key_action = config.get_key_action(config_dict, "1", 5)
        assert key_action != config_key_action and key_action == supported_configs.default_key_action

    def test_validate_config(self):
        """
        Test validation of config json
        """
        global config
        validated_config = config.validate_config(config_dict)
        assert type(validated_config) == dict

    def test_validate_config_not_valid(self):
        """
        Test detection of invalid config json
        """
        global config
        success = False
        try:
            config.validate_config(invalid_config_dict)
        except ConfigException:
            success = True
        assert success

    def test_validate_hotkey_action_typeout(self):
        """
        Test validation of hotkey type "typeout"
        """
        global config
        valid = config.validate_hotkey_action("This is a test!", "typeout", Helper.get_locale())
        assert valid is None

    def test_validate_hotkey_action_shortcut(self):
        """
        Test validation of hotkey type "shortcut"
        """
        global config
        valid = config.validate_hotkey_action("a,ctrl+c,ctrl+v", "shortcut", Helper.get_locale())
        assert valid is None

    def test_validate_hotkey_action_shortcut_unknown_control_key(self):
        """
        Test validation of hotkey type "shortcut" wit invalid control key
        """
        global config
        valid = config.validate_hotkey_action("ctrl+gaga", "shortcut", Helper.get_locale())
        assert valid == {'shortcut': 'Control key gaga on position 2 does not exist! '}
