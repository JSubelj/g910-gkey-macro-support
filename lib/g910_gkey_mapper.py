# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3 and expanded

import usb.core
import usb.util
import time
from lib.functionalities import gkey_functionality, media_static_keys_functionality
from lib.data_mappers import command_bytearray, config_reader
from lib.keyboard_initialization import usb_and_keyboard_device_init
from lib.misc import logger, paths
import signal
import sys
import os
import fcntl

log = logger.logger(__name__)


def emitKeys(device, key):
    if key is 'g1':
        gkey_functionality.g1(device)
    elif key is 'g2':
        gkey_functionality.g2(device)
    elif key is 'g3':
        gkey_functionality.g3(device)
    elif key is 'g4':
        gkey_functionality.g4(device)
    elif key is 'g5':
        gkey_functionality.g5(device)
    elif key is 'g6':
        gkey_functionality.g6(device)
    elif key is 'g7':
        gkey_functionality.g7(device)
    elif key is 'g8':
        gkey_functionality.g8(device)
    elif key is 'g9':
        gkey_functionality.g9(device)
    elif key is "release":
        gkey_functionality.release(device)

    elif media_static_keys_functionality.resolve_key(device, key):
        pass


# uinput device
log.debug("gathering uinput device")
device = usb_and_keyboard_device_init.init_uinput_device()


def signal_handler(sig, frame):
    log.warning("Got signal, " + signal.Signals(sig).name + " terminating!")
    print("Got signal,", signal.Signals(sig).name, "terminating!")
    device.__exit__()
    log.info("Removed uinput device")
    print("Removed uinput device")
    # pid_handler.remove_pid()
    log.info("----------------------EXITING-----------------------")
    sys.exit(0)


def config_changed_handler(sig, frame):
    log.info("config changed")
    time.sleep(0.5)
    config_reader.update_config()


def main():
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

    dev, endpoint, USB_TIMEOUT, USB_IF = usb_and_keyboard_device_init.init_g910_keyboard()

    while True:
        try:
            usb.util.claim_interface(dev, USB_IF)
            # log.debug("reading control values")
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            usb.util.release_interface(dev, USB_IF)

            if control:
                b = bytearray(control)
                if b in command_bytearray.commands.values():
                    key = list(command_bytearray.commands.keys())[
                        list(command_bytearray.commands.values()).index(b)]
                    emitKeys(device, key)
                else:
                    log.warning(str(b) + ' no match')

        except Exception as e:
            if e.args[0] == 110:
                pass
            elif e.args[0] == 19 or e.args[0] == 5:
                try:
                    dev, endpoint, USB_TIMEOUT, USB_IF = usb_and_keyboard_device_init.init_g910_keyboard()
                except:
                    pass
            else:
                log.error("ERROR:" + str(e))

        time.sleep(0.001)


if __name__ == "__main__":
    main()
