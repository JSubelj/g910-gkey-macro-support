# Taken from https://github.com/CReimer/g910-gkey-uinput/issues/3

import usb.core
import usb.util
import time


import uinput
from lib.g910_macro.functionalities import gkey_functionality, media_static_keys_functionality
from lib.g910_macro.data_mappers import command_bytearray, uinput_all_keys

gkeys = command_bytearray.commands





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




def first_diff_index(ls1, ls2):
    l = min(len(ls1), len(ls2))
    return next((i for i in range(l) if ls1[i] != ls2[i]), l)

def init():
    device = uinput.Device(uinput_all_keys.uinput_all_keys)

    USB_IF = 1  # Interface
    USB_TIMEOUT = 5  # Timeout in MS

    USB_VENDOR = 0x046d
    USB_PRODUCT = 0xc335

    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
    print(dev[0][(1, 0)])
    endpoint = dev[0][(1, 0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        dev.detach_kernel_driver(USB_IF)

    usb.util.claim_interface(dev, USB_IF)

    return device, dev, endpoint, USB_TIMEOUT


def main():
    device, dev, endpoint, USB_TIMEOUT = init()


    while True:
        control = None

        try:

            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)

            if control:
                b = bytearray(control)
                if b in gkeys.values():
                    if b == gkeys['dump']:
                        pass
                    else:
                        key = list(gkeys.keys())[list(gkeys.values()).index(b)]
                        print(key)
                        emitKeys(device, key)
                else:
                    print(b, 'no match')

        except usb.core.USBError:
            pass



        time.sleep(0.01)  # Let CTRL+C actually exit```

if __name__ == "__main__":
    main()