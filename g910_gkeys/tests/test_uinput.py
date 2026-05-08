from g910_gkeys.lib.keyboard import Keyboard
# from lib.usb_device import USBDevice
from g910_gkeys.misc.config import Config

class TestUInput:

    def test_uinput(self):
        config = Config()
        # usb keyboard
        # device = USBDevice()
        # uinput keyboard
        keyboard = Keyboard(config)
        # keyboard.set_keyboard(device.keyboard)
        assert keyboard.device is not None
