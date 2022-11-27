import ast
import time
import uinput
import subprocess
from lib.data_mappers import supported_configs
from lib.data_mappers.config_reader import Config
from lib.data_mappers.char_uinput_mapper import keys, reverse_keys
from lib.data_mappers.uinput_all_keys import uinput_all_keys
from lib.data_mappers.supported_devices import KeyboardInterface
from lib.misc import logger

log = logger.logger(__name__)
output_string = ''


class Keyboard:
    # todo: this wouldn't be needed, so the whole release function
    press_release_fifo = []
    device = None
    keyboard: KeyboardInterface = None
    locale: str = 'en'
    config: Config

    def __init__(self, config: Config):
        self.config = config
        log.debug("gathering uinput keyboard")
        self.device = uinput.Device(uinput_all_keys)
        log.debug("got uinput keyboard: " + str(self.device))
        self.locale = self.config.read().get("keyboard_mapping", supported_configs.default_keyboard_mapping)
        log.debug(f"Set {self.locale} uinput mapping.")
        time.sleep(1)  # wait till keyboard is fully initialized

    def __enter__(self):
        return self

    def set_locale(self, locale: str):
        self.locale = locale

    def set_keyboard(self, keyboard: KeyboardInterface):
        self.keyboard = keyboard

    def emit_keys(self, key):
        # config = self.config.read()['profiles'].get(supported_configs.profile, "MEMORY_1")
        config = self.config.get_profile()

        if key not in config:
            log.info(f"{key} pressed, unbound in config, doing nothing!")
            return lambda _: None

        key_config: dict = config[key]

        do = key_config.get('do', supported_configs.default_hotkey_do)
        if not do:
            log.info(f"{key} pressed, but do is empty or not set, doing nothing!")
            return lambda _: None

        command = key_config.get("hotkey_type", supported_configs.default_hotkey_type)
        if command not in supported_configs.hotkey_types:
            raise Exception(
                f'hotkey_type: "{command}" for key "{key}" not known! hotkey_types '
                f"can only be one of: {supported_configs.hotkey_types}"
            )

        if command == 'typeout':
            log.info(f"{key} pressed, typing out: {repr(do)}")
            self.execute_writing(do)
        elif command == 'shortcut':
            log.info(f"{key} pressed, pressing: {do}")
            self.execute_hotkey(do)
        elif command == 'run':
            log.info(f"{key} pressed, running: {do}")
            self.execute_command(do)
        elif command == 'python':
            log.info(f"{key} pressed, running: {do}")
            self.execute_python(do)
        elif command == 'uinput':
            log.info(f"{key} pressed, mapped to: {do}")
            self.execute_events([(eval(f"uinput.{do}"), 3)])
        else:
            # only nothing key config remains
            log.info(f"{key} pressed, doing nothing!")

    def execute_events(self, events):
        for event in events:
            if event[1] == 3:
                self.device.emit_click(event[0])
            else:
                # todo: check why emit is used instead of emit_combo?
                #       This will only trigger pressed or released event.
                self.device.emit(*event)

            time.sleep(0.02)

    def execute_writing(self, string_to_write: str):
        for c in string_to_write:
            self.execute_events(keys[self.locale][c])

    def execute_hotkey(self, string_for_hotkey: str):
        press_together = []
        together = string_for_hotkey.split(",")

        for hotkey in together:
            keys_str = hotkey.split("+")
            press_together.append(keys_str)

        uinput_groups = []
        for combo in press_together:
            uinput_combo = []
            for key_string in combo:
                if len(key_string) == 1:
                    uinput_combo.append(keys[self.locale][key_string][0][0])
                else:
                    uinput_combo.append(keys["control"][key_string][0][0])

            uinput_groups.append(uinput_combo)

        if len(uinput_groups) == 1:
            # todo: this could be one line, why is emit used here?
            # self.keyboard.emit_combo(uinput_groups[0])
            keys_to_fifo = []
            for uinput_key in uinput_groups[0]:
                keys_to_fifo.insert(0, uinput_key)
                self.device.emit(uinput_key, 1)
                time.sleep(0.02)
            self.press_release_fifo.insert(0, keys_to_fifo)
        else:
            for group in uinput_groups:
                self.device.emit_combo(group)

    @staticmethod
    def execute_command(command):
        subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def execute_python(self, command: str):
        try:
            global output_string
            output_string = ''
            ast.parse(command)
            exec(command)
            if output_string:
                self.execute_writing(output_string)
        except Exception as e:
            log.error(f"{type(e).__name__} when running python command '{command}'\nDetails: '{str(e)}'")

    def release(self):
        if not len(self.press_release_fifo):
            return
        keys_to_release = self.press_release_fifo.pop(0)
        to_log = ""
        for key in keys_to_release:
            self.device.emit(key, 0)
            to_log += " " + reverse_keys[key] + ","

        log.info("Released keys:" + to_log[:-1] + " Shortcuts to release: " + str(
            len(self.press_release_fifo)) + " (Should always be 0)")

    def __exit__(self):
        try:
            self.device.__exit__()
            log.info("Removed uinput device")
        except UnboundLocalError:
            pass
        except Exception as e:
            log.error("Could not remove uinput device: " + str(e))


class KeyInputTimeoutException(Exception):
    pass
