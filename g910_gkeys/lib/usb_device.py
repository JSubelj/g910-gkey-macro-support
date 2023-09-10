import time
import usb
import signal
from g910_gkeys.data_mappers.supported_devices import KeyboardInterface, SUPPORTED_DEVICES
from g910_gkeys.misc.logger import Logger


class USBDevice:
    log = None
    keyboard: KeyboardInterface = None
    dev: usb.core.Device = None
    endpoint: usb.core.Endpoint = None

    usb_if: int = 1  # Interface
    usb_timeout: int = 1000  # Timeout in MS

    def __init__(self, usb_if: int = 1):
        self.log = Logger().logger(__name__)
        if usb_if is not None:
            self.usb_if = usb_if
        self.init_usb_dev()
        if self.dev.is_kernel_driver_active(self.usb_if) is True:
            self.log.debug("detaching kernel driver")
            self.dev.detach_kernel_driver(self.usb_if)

    def init_usb_dev(self):
        for keyboard in SUPPORTED_DEVICES:
            self.dev = usb.core.find(idVendor=keyboard.usbVendor, idProduct=keyboard.usbProduct)
            if self.dev is not None:
                self.keyboard = keyboard  # set keyboard interface
                break
            time.sleep(0.1)

        if self.dev is None:
            self.log.warning(f"No supported keyboard found.")
        else:
            self.log.info(f"Keyboard {self.keyboard.deviceName} found.")

        self.log.debug("usb dev: " + str(self.dev[self.keyboard.usbConfiguration][(self.usb_if, 0)]))
        self.endpoint = self.dev[self.keyboard.usbConfiguration][(self.usb_if, 0)][self.keyboard.usbEndpoint]
        self.usb_timeout = self.dev.default_timeout
        self.log.debug(f"Device default timeout: {self.dev.default_timeout}ms")

    def disable_fkey_to_gkey_binding(self):
        time.sleep(0.5)
        self.log.info("Trying to disable f-key to g-key binding")

        if self.keyboard.disableGKeysInterface:
            for packet in self.keyboard.events.disableGKeys:
                self.log.debug(f"Sending ctrl command to keyboard {str(packet)}...")
                if self.keyboard.disableGKeysUseWrite:
                    byte_written = self.dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, self.usb_timeout)
                    # byte_written = self.dev.write(self.endpoint.bEndpointAddress, packet, self.usb_timeout)
                    self.log.debug(f"Completed (sent {byte_written} byte)")
                else:
                    # self.dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, self.usb_timeout)
                    pass

                response_count = len(self.keyboard.events.disableGKeysResponse)
                while response_count:
                    try:
                        confirmation_bytes = self.dev.read(self.endpoint.bEndpointAddress,
                                                           self.endpoint.wMaxPacketSize, self.usb_timeout)
                        if bytes(confirmation_bytes) in self.keyboard.events.disableGKeysResponse:
                            self.log.debug(f"G-key-mode - response: {str(confirmation_bytes)}")
                            if bytes(confirmation_bytes) == packet:
                                self.log.info("G-key-mode - Disabled successfully")
                        else:
                            self.log.warning(f"Warning - G-key-mode - Unknown response: {str(confirmation_bytes)}")
                            return False
                        response_count = response_count - 1
                    except usb.core.USBError as e:
                        self.log.debug(str(e))

                time.sleep(0.2)
        return True

    def read(self):
        try:
            if self.dev:
                return self.dev.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize, self.usb_timeout)
        except usb.core.USBError as e:
            if e.errno == 110:  # Operation timed out
                pass  # nothing to read from keyboard
            elif e.errno == 19 or e.errno == 5:
                # 19 - No such keyboard
                # 5 - Input/Output Error
                self.log.error(f"USBError {e.errno}")
                time.sleep(0.5)
                self.init_usb_dev()
            else:
                self.log.exception(e)
                signal.raise_signal(signal.SIGQUIT)  # raise sig quit to exit

    def __exit__(self):
        try:
            if self.dev and self.dev.is_kernel_driver_active(self.usb_if) is False:
                usb.util.release_interface(self.dev, self.usb_if)
                self.log.debug("attaching kernel driver")
                self.dev.attach_kernel_driver(self.usb_if)
        except usb.core.USBError as e:
            self.log.error("Could not re-attach kernel driver: " + str(e))
        except UnboundLocalError:
            pass
