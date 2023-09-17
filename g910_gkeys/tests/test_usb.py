from lib.data_mappers.supported_devices import KeyboardInterface
from lib.usb_device import USBDevice

device = None


class TestUSB:

    def test_usb(self):
        global device
        # usb keyboard
        device = USBDevice()
        assert issubclass(device.keyboard, KeyboardInterface)

    def test_gkeymode(self):
        global device
        assert device is not None and device.disable_fkey_to_gkey_binding()

    def test_read(self):
        global device
        assert device is not None and device.read() is None

    def test_exit(self):
        global device
        assert device is not None and device.__exit__() is None
