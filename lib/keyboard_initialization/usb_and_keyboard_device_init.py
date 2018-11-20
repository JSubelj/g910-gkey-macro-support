import uinput
import usb
from lib.data_mappers import uinput_all_keys
from lib.misc import logger

log = logger.logger(__name__)
import time

def init_uinput_device():
    device = uinput.Device(uinput_all_keys.uinput_all_keys)
    log.debug("got uinput device: " + str(device))
    return device

def init_usb_dev():
    USB_VENDOR = 0x046d
    USB_PRODUCT = 0xc335
    USB_IF = 1  # Interface
    USB_TIMEOUT = 5  # Timeout in MS

    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
    while not dev:
        log.debug("usb dev: not found. retrying")
        dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
        time.sleep(1)

    log.debug("usb dev: " + str(dev[0][(1, 0)]))
    endpoint = dev[0][(1, 0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        log.debug("detaching kernel driver")
        dev.detach_kernel_driver(USB_IF)

    return dev, endpoint, USB_TIMEOUT, USB_IF

