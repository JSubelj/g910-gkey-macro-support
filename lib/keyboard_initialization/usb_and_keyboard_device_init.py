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
    USB_PRODUCT = (0x0c32b, 0xc335)
    USB_IF = 1  # Interface
    USB_TIMEOUT = 5  # Timeout in MS

    select_product = 0
    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT[select_product])
    while not dev:
        select_product = abs(select_product - 1)
        log.debug("usb dev: not found. retrying with other product id")
        dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT[select_product])
        time.sleep(0.1)

    log.debug("usb dev: " + str(dev[0][(1, 0)]))
    endpoint = dev[0][(1, 0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        log.debug("detaching kernel driver")
        dev.detach_kernel_driver(USB_IF)

    return dev, endpoint, USB_TIMEOUT, USB_IF


def disable_fkey_to_gkey_binding(dev, endpoint, USB_TIMEOUT, USB_IF):
    usb.util.claim_interface(dev, USB_IF)
    log.info("Trying to disable mapping")
    log.debug("Sending disable")
    packet = [0x11, 0xff, 0x08, 0x2e, 0x2]
    for _ in range(len(packet), 20):
        packet.append(0)
    disable_return = dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, 2000)  # write(1,packet,USB_TIMEOUT))
    log.debug("Got: " + str(disable_return))
    time.sleep(0.001)

    buffer = []
    for _ in range(64):
        buffer.append(0)

    # Don't really know why this has to be send but its included in the original g810-leds
    ret = dev.write(0x82, buffer, 2000)
    log.debug("Got: " + str(ret))

    operation_successful = [17, 255, 8, 46, 2]
    while 1:
        time.sleep(0.001)
        confirmation_bytes = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        if list(confirmation_bytes[:5]) == operation_successful:
            log.info("Mapping disabled successfully")
            break
    usb.util.release_interface(dev, USB_IF)
    return True


def init_g910_keyboard():
    dev = endpoint = USB_TIMEOUT = USB_IF = None
    counter = 0
    log.debug("gathering usb device")
    while not dev:
        try:
            dev, endpoint, USB_TIMEOUT, USB_IF = init_usb_dev()
        except Exception as e:
            if e.args[0] == 5:
                counter += 1
                if counter >= 1000:
                    log.warning("USBError: Input/Output Error")
                    counter = 0
                time.sleep(0.01)
            else:
                log.warning("Getting keyboard error: " + str(e))

    successfully_disabled_mapping = False
    counter = 0
    while not successfully_disabled_mapping:
        try:
            successfully_disabled_mapping = disable_fkey_to_gkey_binding(dev, endpoint, USB_TIMEOUT, USB_IF)
        except Exception as e:
            if e.args[0] == 110:
                counter += 1
                if counter >= 5:
                    log.warning("Can't disable mapping")
                    counter = 0
                time.sleep(0.01)
            else:
                log.warning("Disable mapping error: " + str(e))
                try:
                    dev, endpoint, USB_TIMEOUT, USB_IF = init_usb_dev()
                except:
                    pass

    return dev, endpoint, USB_TIMEOUT, USB_IF
