# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3

import usb.core
import usb.util
import time

import uinput
from lib.functionalities import gkey_functionality, media_static_keys_functionality
from lib.data_mappers import command_bytearray, config_reader
from lib.keyboard_initialization import usb_and_keyboard_device_init

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

def main():

    # To see if config exists
    config_reader.read()

    device, dev, endpoint, USB_TIMEOUT = usb_and_keyboard_device_init.init()

    while True:
        try:

            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)

            if control:
                b = bytearray(control)
                if b in command_bytearray.commands.values():
                    if b == command_bytearray.commands['dump']:
                        pass
                    else:
                        key = list(command_bytearray.commands.keys())[list(command_bytearray.commands.values()).index(b)]
                        emitKeys(device, key)
                else:
                    print(b, 'no match')

        except usb.core.USBError:
            pass

        time.sleep(0.01)  # Let CTRL+C actually exit```

if __name__ == "__main__":
    main()
