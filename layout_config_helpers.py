"""
    This file contains functions that can help you get the right config for your layout.
"""
import signal
import sys
import tty
import termios
import uinput  # used to eval keys
import lib.data_mappers.char_uinput_mapper as uinput_mapper
from lib.data_mappers.char_uinput_mapper import keys as locale_key_mapping
from lib.usb_device import USBDevice
from lib.keyboard import Keyboard, KeyInputTimeoutException
from lib.data_mappers.bytearrays import keys as uinput_key_map, commands as uinput_if1
from lib.misc.helper import Helper
from lib.misc.config import Config


class LayoutHelper:
    device: USBDevice = None
    keyboard: Keyboard = None

    WRAPPING_CLICK: int = 0  # only use key click
    WRAPPING_SHIFT: int = 1  # key click and wrapped shift key click
    WRAPPING_ALTGR: int = 2  # key click, wrapped shift key click and wrapped alt key click

    skip_keys_altgr: list = [
        "uinput.KEY_EQUAL",
        "uinput.KEY_LEFTBRACE",
        "uinput.KEY_SEMICOLON",
        "uinput.KEY_APOSTROPHE",
        "uinput.KEY_GRAVE"
    ]

    def __init__(self, command: str):
        """
        Setup signals and run
        :param command:
        """
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)

        if command == "read1":
            self.read_raw_bytes(1)
        elif command == "read0":
            self.read_raw_bytes(0)
        elif command == "create":
            self.create()
        elif command == "test":
            self.test()
        elif command == "uinput":
            self.uinput_key()
        else:
            print(f"Syntax: g910-gkey [--help|--read0|--read1|--create|--test|--uinput]")
            if command != "help":
                print(f"No matching helper '{command}' found!")

        self.__exit__()

    def signal_handler(self, sig, frame):
        """
        Terminating signale handler
        :param sig:
        :param frame:
        """
        print(f"Got signal, {signal.Signals(sig).name} terminating!")
        print("The application will end the current process and needs to disconnect your usb and uinput device.")

    def read_raw_bytes(self, interface: int):
        """
        Read raw bytes send over usb from keyboard and try to get matching command or key from command_bytearray
        :param interface: 0 for all normal keys, 1 for g-, m- and media-keys
        """
        self.device = USBDevice(interface)
        if interface == 0:
            byte_map = uinput_key_map
        else:
            byte_map = uinput_if1
        bytes_received = None
        while bytes_received is None:
            bytes_received = self.device.read()
            if bytes_received is not None:
                try:
                    uinput_key = list(byte_map.keys())[list(byte_map.values()).index(bytes(bytes_received))]
                except ValueError:
                    uinput_key = "NO_MATCH"
                print(f"{uinput_key}: {bytes(bytes_received)}")

    def uinput_key(self):
        """
        Get uinput key by pressing a key on the keyboard
        """
        self.device = USBDevice(0)  # init keyboard interface 0 to read default keys
        write_config = ''
        print(f"Press a key you want to get the uinput key definition:")
        user_input = False
        while not user_input:
            bytes_received = self.device.read()
            if bytes_received is not None:
                if bytes(bytes_received) == uinput_key_map.get('KEY_LEFTSHIFT') or \
                        bytes(bytes_received) == uinput_key_map.get('KEY_RIGHTSHIFT') or \
                        bytes(bytes_received) == uinput_key_map.get('KEY_LEFTALT') or \
                        bytes(bytes_received) == uinput_key_map.get('KEY_RIGHTALT'):
                    pass
                elif bytes(bytes_received) != b'\x00\x00\x00\x00\x00\x00\x00\x00':
                    wrap_byte = bytes_received[0]
                    bytes_received[0] = 0  # remove shift wrap from byte array
                    try:
                        uinput_key = list(uinput_key_map.keys())[list(uinput_key_map.values()).index(bytes(bytes_received))]
                        if wrap_byte == uinput_key_map.get('KEY_LEFTSHIFT')[0]:
                            # wrapped with left shift
                            write_config = f"wrap_shift(click(uinput.{uinput_key}))"
                        elif wrap_byte == uinput_key_map.get('KEY_RIGHTALT')[0]:
                            # wrapped with right alt (altgr)
                            write_config = f"wrap_altgr(click(uinput.{uinput_key}))"
                        else:
                            write_config = f"click(uinput.{uinput_key})"
                    except ValueError:
                        pass  # just keep on going if a key is not found
                elif bytes(bytes_received) == b'\x00\x00\x00\x00\x00\x00\x00\x00':
                    user_input = True
        print(write_config)

    def create(self):
        """
        Create localized uinput key map
        """
        user_lang = Helper.get_locale()
        config = Config()
        try:
            self.keyboard = Keyboard(config)
            locale_map = self.get_keys()
            filename = f"char_uinput_mapping_{user_lang}"
            with open(filename, "w") as fd:
                fd.write("'" + user_lang + "': {\n")
                for row in locale_map:
                    fd.write(f"{row}\n")
                fd.write("}")
            print(f"Your local char to uinput map was saved to {filename}.")
        except Exception as e:
            print(repr(e))

    @staticmethod
    def get_key_timeout_handler(signum, frame):
        """
        Timeout handler for char to uinput mapping raise a KeyInputTimeoutException
        :param signum:
        :param frame:
        """
        raise KeyInputTimeoutException("No key emitted.")

    def get_emitted_char(self, event: list):
        """
        Get character written down to stdout on emit of given key
        :param event: uinput event
        :return: character written down in stdout on key emit
        :rtype: str
        """
        # set alarm signal to 1s to go on if key emit doesn't output any character
        signal.signal(signal.SIGALRM, self.get_key_timeout_handler)
        signal.alarm(1)
        file_descriptors = termios.tcgetattr(sys.stdin)  # save old file descriptors to reset later
        tty.setcbreak(sys.stdin)  # set cbreak to stdin (we will need no enter to read from stdin)
        if event == uinput_mapper.click((eval("uinput.KEY_GRAVE"))):
            # KEY_GRAVE have to be pressed two times
            event += event
        elif event == uinput_mapper.click((eval("uinput.KEY_EQUAL"))) or \
                event == uinput_mapper.wrap_shift(uinput_mapper.click(eval("uinput.KEY_EQUAL"))):
            # KEY_EQUAL have to be pressed two times alone and also together with shift
            event += event
        self.keyboard.execute_events(event)
        try:
            char = sys.stdin.read(1)[0]  # read the char which gets writen by uinput keyboard
            signal.alarm(0)  # remove the alarm signal
        except KeyInputTimeoutException:
            # if we capture an alarm, we set an empty character to remove from mapping later
            char = ''
        # reset file descriptor on stdin
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)
        return char

    @staticmethod
    def get_other_keys():
        """
        Get none alphanumeric keys
        :return: Return a list of keys with a string interpretation of uinput key (ex. ["uinput.KEY_COMMA", ...])
        :rtype: list
        """
        keys = [
            "uinput.KEY_EQUAL",
            "uinput.KEY_MINUS",
            "uinput.KEY_LEFTBRACE",
            "uinput.KEY_RIGHTBRACE",
            "uinput.KEY_SEMICOLON",
            "uinput.KEY_APOSTROPHE",
            "uinput.KEY_GRAVE",
            "uinput.KEY_BACKSLASH",
            "uinput.KEY_COMMA",
            "uinput.KEY_DOT",
            "uinput.KEY_SLASH"
        ]
        return keys

    def get_keys(self):
        """
        Get config list entries for all keys
        :return: config list entries for all keys
        :rtype: list
        """
        key_config = []
        for i in range(48, 58):  # digits 0-9
            key_config += self.get_key_config("uinput.KEY_" + chr(i), self.WRAPPING_ALTGR)

        for i in range(65, 91):  # characters a-z
            key_config += self.get_key_config("uinput.KEY_" + chr(i), self.WRAPPING_ALTGR)

        for key in self.get_other_keys():  # add other keys (no control keys)
            key_config += self.get_key_config(key, self.WRAPPING_ALTGR)

        return key_config

    def get_key_config(self, key: str, wrapping: int = 0):
        """
        Get key configuration by given uinput key
        :param key: uinput key as string (ex. uinput.KEY_0)
        :param wrapping: one of WRAPPING_CLICK | WRAPPING_SHIFT | WRAPPING_ALTGR
        :return: list entry/ies for key for use in the driver
        :rtype: list
        """
        locale_keys = []
        char = self.get_emitted_char(uinput_mapper.click((eval(key))))
        if char != '':
            locale_keys.append(f"\t'{char}': click({key}),")
        if wrapping > 0:  # wrap key with shift
            char = self.get_emitted_char(uinput_mapper.wrap_shift(uinput_mapper.click((eval(key)))))
            if char != '':
                locale_keys.append(f"\t'{char}': wrap_shift(click({key})),")
        if wrapping > 1 and key not in self.skip_keys_altgr:  # wrap key with right alt
            char = self.get_emitted_char(uinput_mapper.wrap_altgr(uinput_mapper.click((eval(key)))))
            if char != '':
                locale_keys.append(f"\t'{char}': wrap_altgr(click({key})),")

        return locale_keys

    def test(self):
        """
        Test the char to uinput map with current locale
        A virtual keyboard is initialized and all keys from the map will be emitted.
        After each key is emitted the written char gets checked against the key map.
        """
        user_lang = Helper.get_locale()
        config = Config()
        self.keyboard = Keyboard(config)
        events = locale_key_mapping[user_lang]
        error = False
        for key, event in events.items():
            if error:
                break
            try:
                char = self.get_emitted_char(event)
                if key != char:
                    error = True
                    print(f"{key} != {char}")
            except Exception as e:
                print(repr(e))
                error = True

        if error:
            print("Error in key map: Please correct char_uinput_mapper.py")
            return False
        else:
            print(f"'{user_lang}' Key map tested successfully.")
            return True

    def __exit__(self):
        """
        Disconnect the usb- and uinput-device on exit
        """
        try:
            self.device.__exit__()
        except AttributeError:
            pass  # pass if no usb device was initialized
        try:
            self.keyboard.__exit__()
        except AttributeError:
            pass  # pass if no uinput device was initialized


if __name__ == "__main__":
    import argparse
    from lib import PROJECT_INFO

    parser = argparse.ArgumentParser(description=PROJECT_INFO.DESCRIPTION)
    parser.add_argument("--read0", help="Read the raw bytes from interface 0 (default keys)",
                        action='store_true', default=False)
    parser.add_argument("--read1", help="Read the raw bytes from interface 1 (macro- and media-keys)",
                        action='store_true', default=False)
    parser.add_argument("-c", "--create", help="Create a keyboard mapping for your locale keyboard",
                        action='store_true', default=False)
    parser.add_argument("-t", "--test", help="Test the keyboard mapping set in config.json",
                        action='store_true', default=False)
    parser.add_argument("-u", "--uinput", help="Get uinput key from key press",
                        action='store_true', default=False)
    parser.add_argument("-v", "--version", help="Displays version of the driver",
                        action='version', version='%(prog)s ' + PROJECT_INFO.VERSION)
    args = parser.parse_args()

    command = "help"
    if args.read0:
        command = "read0"
    elif args.read1:
        command = "read1"
    elif args.create:
        command = "create"
    elif args.test:
        command = "test"
    elif args.uinput:
        command = "uinput"

    LayoutHelper(command)
