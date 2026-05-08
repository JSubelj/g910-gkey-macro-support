from g910_gkeys.lib.hid_device import HIDDevice
from g910_gkeys.misc.logger import Logger


def change_profile(device: HIDDevice, profile: str):
    log = Logger().logger(__name__)
    # set memory key led to corresponding profile
    try:
        device.dev.write(device.keyboard.events.memoryKeysLEDs[profile])
        response = device.read()
        return bytes(response) == device.keyboard.events.memoryKeysLEDs[profile]
    except OSError as e:
        log.error(f"HID error: {e}")
    except Exception as e:
        log.exception(e)
