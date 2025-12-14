from asyncio import wait_for

import usb
from g910_gkeys.lib.usb_device import USBDevice
from g910_gkeys.misc.logger import Logger


def change_profile(device: USBDevice, profile: str):
    log = Logger().logger(__name__)
    # set memory key led to corresponding profile
    record_profile = profile if profile == "MEMORY_RECORD" else "MEMORY_RECORD_OFF"
    device.dev.ctrl_transfer(0x21, 0x09, 0x0211, 1, device.keyboard.events.memoryKeysLEDs[profile], device.usb_timeout)
    response = device.dev.read(device.endpoint, device.endpoint.wMaxPacketSize, device.usb_timeout)

    m_mask = {
        "MEMORY_1": 1,
        "MEMORY_2": 2,
        "MEMORY_3": 4,
        "MEMORY_RECORD": 0
    }.get(profile, 1)

    # (de-)activate M1-M3
    packet = bytearray(device.keyboard.events.memoryKeysLEDs["MEMORY_1"])
    packet[4] = m_mask
    device.dev.ctrl_transfer(0x21, 0x09, 0x0211, 1, bytes(packet), device.usb_timeout)

    # wait for previous action to finish
    device.dev.read(device.endpoint, device.endpoint.wMaxPacketSize, device.usb_timeout)

    # (de-) activate MR
    packet = bytearray(device.keyboard.events.memoryKeysLEDs[record_profile])
    device.dev.ctrl_transfer(0x21, 0x09, 0x0211, 1, bytes(packet), device.usb_timeout)

    return True