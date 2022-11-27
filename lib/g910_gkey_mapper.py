# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3 and expanded

import fcntl
import os
import signal
import time
import uinput
from lib.data_mappers.config_reader import Config
from lib.usb_device import USBDevice
from lib.keyboard import Keyboard
from lib.misc import logger, paths, notify, g910_led

log = logger.logger(__name__)
config = Config()
notifier = notify.Notification(config)
program_running = True


def signal_handler(sig, frame):
    global program_running
    log.debug(f"Got signal, {signal.Signals(sig).name} terminating!")
    program_running = False


def config_changed_handler(sig, frame):
    log.info("config changed")
    time.sleep(0.5)
    config.update_config()


def change_profile(device: USBDevice, profile: str):
    log.debug(f"Change profile to {profile}.")
    config.profile = profile
    if g910_led.change_profile(device, profile):
        log.debug(f"Changed memory key led for {profile}.")
    notifier.send_notification(profile)


def main():
    global program_running
    log.info("--------------------------------------------------------------------------------")
    log.info(f"----------------------STARTED g910-keys-pid:{str(os.getpid())}------------------------------")
    log.info("--------------------------------------------------------------------------------")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGIO, config_changed_handler)

    device = keyboard = None
    if program_running:
        # usb keyboard
        device = USBDevice()
        # check paths, create config directory and default config if not exists
        paths.check_paths(config, device)
        # sends signal if config is changed (or really anything in the config directory)
        fd = os.open(paths.config_dir, os.O_RDONLY)
        fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
        fcntl.fcntl(fd, fcntl.F_NOTIFY, fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)
        # To see if config exists
        config.read()
        # disable macro key default f key binding on interface 0
        device.disable_fkey_to_gkey_binding()
        # uinput keyboard
        keyboard = Keyboard(config)
        keyboard.set_keyboard(device.keyboard)
        # set first profile out of event interface
        change_profile(device, list(keyboard.keyboard.events.memoryKeys.values())[0])

    while program_running:
        try:
            # main loop
            control = device.read()

            if control:
                key = None
                b = bytes(control)
                if b in device.keyboard.events.macroKeys.keys():
                    key = list(device.keyboard.events.macroKeys.values())[
                        list(device.keyboard.events.macroKeys.keys()).index(b)]
                    log.debug(f"Event {key}, bytecode: {b}")
                    keyboard.emit_keys(key)
                elif b in device.keyboard.events.memoryKeys.keys():
                    profile = list(device.keyboard.events.memoryKeys.values())[
                        list(device.keyboard.events.memoryKeys.keys()).index(b)]
                    change_profile(device, profile)
                elif b in device.keyboard.events.mediaKeys.keys():
                    key = list(device.keyboard.events.mediaKeys.values())[
                        list(device.keyboard.events.mediaKeys.keys()).index(b)]
                    log.debug(f"Media key {key} pressed, bytecode: {b}")
                    keyboard.device.emit_click(eval(f"uinput.{key}"))
                elif b in device.keyboard.events.releaseEvents.keys():
                    release = list(device.keyboard.events.releaseEvents.values())[
                        list(device.keyboard.events.releaseEvents.keys()).index(b)]
                    log.debug(f"Release event {release}.")
                    keyboard.release()
                elif b[:3] in (bytearray(b'\x11\xff\x0f'), bytearray(b'\x11\xff\x10'), bytearray(b'\x11\xff\xff')):
                    pass  # Suppress warnings on these values, these are return values from LEDs being set.
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
    except AttributeError:
        pass  # pass if no uinput or usb keyboard is assigned

    log.info("------------------------------------EXITING-------------------------------------")


if __name__ == "__main__":
    main()
