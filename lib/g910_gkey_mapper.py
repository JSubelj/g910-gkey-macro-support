# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3 and expanded

import usb.core
import usb.util
import time
from lib.functionalities import gkey_functionality, media_static_keys_functionality
from lib.data_mappers import command_bytearray, config_reader
from lib.keyboard_initialization import usb_and_keyboard_device_init
from lib.misc import logger
import signal
import sys
import os

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

    elif media_static_keys_functionality.resolve_key(device, key):
        pass



def signal_handler(sig, frame):
    log.warning("Got signal "+signal.Signals(sig).name+" terminating!")
    print("Got signal",signal.Signals(sig).name,"terminating!")
    #pid_handler.remove_pid()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    log.info("------------------------------------------------------------------------------------")
    log.info("----------------------STARTED g910-keys-pid:"+str(os.getpid())+"-----------------------------------")
    log.info("------------------------------------------------------------------------------------")

    # To see if config exists
    config_reader.read()
    device, dev, endpoint, USB_TIMEOUT, USB_IF = usb_and_keyboard_device_init.init()

    while True:
        try:
            usb.util.claim_interface(dev, USB_IF)
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            usb.util.release_interface(dev, USB_IF)

            if control:
                b = bytearray(control)
                if b in command_bytearray.commands.values():
                    if b == command_bytearray.commands['dump']:
                        pass
                    else:
                        key = list(command_bytearray.commands.keys())[list(command_bytearray.commands.values()).index(b)]
                        emitKeys(device, key)
                else:
                    log.warning(str(b) + ' no match')

        except usb.core.USBError:
            pass

        time.sleep(0.001)

if __name__ == "__main__":
    main()
