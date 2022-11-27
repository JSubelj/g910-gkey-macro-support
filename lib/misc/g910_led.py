from lib.misc import logger
from lib.usb_device import USBDevice

installed = None

log = logger.logger(__name__)


def change_profile(device: USBDevice, profile: str):
    # set memory key led to corresponding profile
    device.dev.ctrl_transfer(0x21, 0x09, 0x0211, 1, device.keyboard.events.memoryKeysLEDs[profile], device.usb_timeout)
    response = device.dev.read(device.endpoint, device.endpoint.wMaxPacketSize, device.usb_timeout)
    return bytes(response) == device.keyboard.events.memoryKeysLEDs[profile]
