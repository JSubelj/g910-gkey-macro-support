import uinput
import usb
from lib.data_mappers import uinput_all_keys


def init_uinput_device():
    return uinput.Device(uinput_all_keys.uinput_all_keys)

def init():
    device = init_uinput_device()

    USB_IF = 1  # Interface
    USB_TIMEOUT = 5  # Timeout in MS

    USB_VENDOR = 0x046d
    USB_PRODUCT = 0xc335

    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
    #print(dev[0][(1, 0)])
    endpoint = dev[0][(1, 0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        dev.detach_kernel_driver(USB_IF)


    return device, dev, endpoint, USB_TIMEOUT, USB_IF

