# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3 and expanded

import fcntl
import os
import signal
import time
from lib.data_mappers import bytearrays, config_reader
from lib.keyboard_initialization.usb_and_keyboard_device_init import USBDevice
from lib.uinput_keyboard.keyboard import Keyboard
from lib.misc import logger, paths

log = logger.logger(__name__)

program_running = True


def signal_handler(sig, frame):
    global program_running
    log.debug(f"Got signal, {signal.Signals(sig).name} terminating!")
    program_running = False


def config_changed_handler(sig, frame):
    log.info("config changed")
    time.sleep(0.5)
    config_reader.update_config()


def main():
    global program_running
    log.info("--------------------------------------------------------------------------------")
    log.info(f"----------------------STARTED g910-keys-pid:{str(os.getpid())}------------------------------")
    log.info("--------------------------------------------------------------------------------")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGIO, config_changed_handler)

    # sends signal if config is changed (or really anything in the config directory)
    fd = os.open(paths.config_dir, os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)
    # To see if config exists
    config_reader.read()

    device = keyboard = None
    if program_running:
        # uinput device
        keyboard = Keyboard()
        # usb device
        device = USBDevice()

    while program_running:
        try:
            # log.debug("reading control values")
            control = device.read()

            if control:
                b = bytearray(control)
                if b in command_bytearray.commands.values():
                    key = list(command_bytearray.commands.keys())[
                        list(command_bytearray.commands.values()).index(b)]
                    log.debug(f"Event {key}, bytecode: {b}")
                    keyboard.emit_keys(key)
                elif b[:3] in (bytearray(b'\x11\xff\x0f'), bytearray(b'\x11\xff\x10'), bytearray(b'\x11\xff\xff')):
                    # Suppress warnings on these values, these are return values from LEDs being set.
                    pass
                else:
                    log.warning(str(b) + ' no match')
        except SystemExit:
            program_running = False
        except Exception as e:
            log.exception(e)
            program_running = False

    try:
        keyboard.__exit__()
        device.__exit__()
    except UnboundLocalError:
        pass  # pass if no uinput or usb device is assigned

    log.info("------------------------------------EXITING-------------------------------------")


if __name__ == "__main__":
    main()
