import usb
from g910_gkeys.lib.usb_device import USBDevice
from g910_gkeys.misc.logger import Logger


def change_profile(device: USBDevice, profile: str):
    log = Logger().logger(__name__)
    # set memory key led to corresponding profile
    try:
        device.dev.ctrl_transfer(0x21, 0x09, 0x0211, 1, device.keyboard.events.memoryKeysLEDs[profile], device.usb_timeout)
        response = device.dev.read(device.endpoint, device.endpoint.wMaxPacketSize, device.usb_timeout)
        return bytes(response) == device.keyboard.events.memoryKeysLEDs[profile]
    except usb.core.USBError as e:
        if e.errno == 110:  # Operation timed out
            pass
        elif e.errno == 19 or e.errno == 5:
            # 19 - No such keyboard
            # 5 - Input/Output Error
            log.error(f"USBError {e.errno}")
        else:
            log.exception(e)
