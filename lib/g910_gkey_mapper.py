# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3 and expanded

import fcntl
import os
import usb.core
import usb.util
import signal
import time
from lib.functionalities import gkey_functionality, media_static_keys_functionality
from lib.data_mappers import command_bytearray, config_reader
from lib.keyboard_initialization import usb_and_keyboard_device_init
from lib.misc import logger, paths

log = logger.logger(__name__)

program_running=True

def emitKeys(device, key):
    if gkey_functionality.handle_gkey_press(device, key):
        return
    elif key == "release":
        gkey_functionality.release(device)
    elif media_static_keys_functionality.resolve_key(device, key):
        pass


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
    
    if program_running:
        # uinput device
        log.debug("gathering uinput device")
        device = usb_and_keyboard_device_init.init_uinput_device()
        # usb device
        dev, endpoint, USB_TIMEOUT, USB_IF = usb_and_keyboard_device_init.init_g910_keyboard()

    while program_running:
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
                    log.debug(f"Pressed {key}, bytecode: {b}")
                    emitKeys(device, key)
                elif b[:3] in (bytearray(b'\x11\xff\x0f'), bytearray(b'\x11\xff\x10'), bytearray(b'\x11\xff\xff')):
                    #Suppress warnings on these values, these are return values from LEDs being set.
                    pass
                else:
                    log.warning(str(b) + ' no match')
        except SystemExit:
            program_running = False
        except Exception as e:
            if e.args[0] == 110:
                pass
            elif e.args[0] == 19 or e.args[0] == 5:
                try:
                    dev, endpoint, USB_TIMEOUT, USB_IF = usb_and_keyboard_device_init.init_g910_keyboard()
                except:
                    pass
            else:
                log.exception(e)

        time.sleep(0.001)

    try:
        if device:
            device.__exit__()
            log.info("Removed uinput device")
    except UnboundLocalError:
        pass # pass if no device is assigned
    except Exception as e:
        log.error("Could not remove uinput device.",e)

    log.info("------------------------------------EXITING-------------------------------------")

if __name__ == "__main__":
    main()
