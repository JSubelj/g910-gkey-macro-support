from lib.functionalities import gkey_functionality
from lib.keyboard_initialization import usb_and_keyboard_device_init
import time

def main():
    device = usb_and_keyboard_device_init.init_uinput_device()

    time.sleep(1)
    gkey_functionality.g1(device)
    gkey_functionality.g2(device)

