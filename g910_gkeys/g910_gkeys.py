import argparse
import fcntl
import importlib.metadata
import os
import signal
import time
import uinput
from g910_gkeys.misc.helper import Helper
from g910_gkeys.misc.config import Config
from g910_gkeys.lib.usb_device import USBDevice
from g910_gkeys.lib.keyboard import Keyboard
from g910_gkeys.misc import notify, memory_leds
from g910_gkeys.misc.logger import Logger

config: Config = Config()
log = Logger().logger(__name__)
notifier = notify.Notification(config)
program_running: bool = True
device: USBDevice
keyboard: Keyboard


def signal_handler(sig, frame):
    global program_running
    log.debug(f"Got signal, {signal.Signals(sig).name} terminating!")
    program_running = False


def config_changed_handler(sig, frame):
    log.info(f"Got signal, {signal.Signals(sig).name} config changed!")
    time.sleep(0.5)
    config.update_config()


def reload_handler(sig, frame):
    log.info(f"Reload g910-gkeys.")
    config.update_config()


def change_profile(dev: USBDevice, profile: str):
    log.info(f"Change profile to {profile}.")
    config.profile = profile
    if memory_leds.change_profile(dev, profile):
        log.debug(f"Changed memory key led for {profile}.")
    notifier.send_notification(profile)


def main():
    global device
    parser = argparse.ArgumentParser(description=importlib.metadata.metadata("g910-gkeys")["summary"])
    parser.add_argument("--create-config", help="Creates new config with current keyboard layout",
                        action='store_true', default=False)
    parser.add_argument("-s", "--set-config", help="Set the config file to use",
                        default='', dest="config_file")
    parser.add_argument("-v", "--version", help="Displays the information about the driver",
                        action='version', version=f"%(prog)s {Helper.get_version()} by {Helper.get_author()}")
    args = parser.parse_args()
    if args.create_config:
        device = USBDevice()  # init usb device and keyboard interface
        config.create(device.keyboard)  # create config with keyboard interface
        device.__exit__()  # clean up usb connection
    elif args.config_file != "":
        config.config_path = args.config_file
        start()
    else:
        start()


def start():
    global program_running, device, keyboard
    log.info("--------------------------------------------------------------------------------")
    log.info(f"----------------------STARTED g910-keys-pid:{str(os.getpid())}------------------------------")
    log.info("--------------------------------------------------------------------------------")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGIO, config_changed_handler)
    signal.signal(signal.SIGUSR1, reload_handler)

    if program_running:
        # usb keyboard
        device = USBDevice()
        # check paths, create config directory and default config if not exists
        config.check_paths(config, device)
        # sends signal if config is changed (or really anything in the config directory)
        fd = os.open(config.config_dir, os.O_RDONLY)
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
        loop()

    try:
        keyboard.__exit__()
        device.__exit__()
    except AttributeError:
        pass  # pass if no uinput or usb keyboard is assigned

    log.info("------------------------------------EXITING-------------------------------------")


def loop():
    try:
        control = device.read()  # listen for incoming traffic from usb device

        if control:
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
        signal.raise_signal(signal.SIGQUIT)
    except Exception as e:
        log.exception(e)
        signal.raise_signal(signal.SIGQUIT)


if __name__ == "__main__":
    main()
