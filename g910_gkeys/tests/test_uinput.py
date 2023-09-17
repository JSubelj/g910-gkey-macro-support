from lib.keyboard import Keyboard
# from lib.usb_device import USBDevice
from lib.data_mappers.config_reader import Config

class TestUInput:

    def test_uinput(self):
        config = Config()
        # usb keyboard
        # device = USBDevice()
        # uinput keyboard
        keyboard = Keyboard(config)
        # keyboard.set_keyboard(device.keyboard)
        assert keyboard.device is not None
