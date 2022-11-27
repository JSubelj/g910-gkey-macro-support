import time
import usb
from lib.misc import logger
from lib import g910_gkey_mapper
from lib.data_mappers.supported_devices import KeyboardInterface, SUPPORTED_DEVICES

log = logger.logger(__name__)


class USBDevice:
    keyboard: KeyboardInterface = None
    dev: usb.core.Device = None
    endpoint: usb.core.Endpoint = None

    usb_if: int = 1  # Interface
    usb_timeout: int = 1000  # Timeout in MS

    def __init__(self, usb_if: int = 1):
        if usb_if is not None:
            self.usb_if = usb_if
        self.init_usb_dev()
        if self.dev.is_kernel_driver_active(self.usb_if) is True:
            log.debug("detaching kernel driver")
            self.dev.detach_kernel_driver(self.usb_if)

    def init_usb_dev(self):
        for keyboard in SUPPORTED_DEVICES:
            self.dev = usb.core.find(idVendor=keyboard.usbVendor, idProduct=keyboard.usbProduct)
            if self.dev is not None:
                self.keyboard = keyboard  # set keyboard interface
                break
            time.sleep(0.1)

        if self.dev is None:
            log.warn(f"No supported keyboard found.")
        else:
            log.info(f"Keyboard {self.keyboard.deviceName} found.")

        log.debug("usb dev: " + str(self.dev[self.keyboard.usbConfiguration][(self.usb_if, 0)]))
        self.endpoint = self.dev[self.keyboard.usbConfiguration][(self.usb_if, 0)][self.keyboard.usbEndpoint]
        self.usb_timeout = self.dev.default_timeout
        log.debug(f"Device default timeout: {self.dev.default_timeout}ms")

    def disable_fkey_to_gkey_binding(self):
        time.sleep(0.5)
        log.info("Trying to disable f-key to g-key binding")

        if self.keyboard.disableGKeysInterface:
            for packet in self.keyboard.events.disableGKeys:
                log.debug(f"Sending ctrl command to keyboard {str(packet)}...")
                if self.keyboard.disableGKeysUseWrite:
                    byte_written = self.dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, self.usb_timeout)
                    # byte_written = self.dev.write(self.endpoint.bEndpointAddress, packet, self.usb_timeout)
                    log.debug(f"Completed (sent {byte_written} byte)")
                else:
                    # self.dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, self.usb_timeout)
                    pass

                # this doesn't work :/
                #time.sleep(0.5)
                #buffer = bytearray()
                #response = self.dev.ctrl_transfer(0xa1, 0x01, 0x0212, 1, buffer, self.usb_timeout)
                #log.debug(f"{response} {str(buffer)}")

                # im pretty sure this sequence of packets can be received with ctrl_transfer
                response_count = len(self.keyboard.events.disableGKeysResponse)
                while response_count:
                    try:
                        confirmation_bytes = self.dev.read(self.endpoint.bEndpointAddress,
                                                           self.endpoint.wMaxPacketSize, self.usb_timeout)
                        if bytes(confirmation_bytes) in self.keyboard.events.disableGKeysResponse:
                            log.debug(f"G-key-mode - response: {str(confirmation_bytes)}")
                            if bytes(confirmation_bytes) == packet:
                                log.info("G-key-mode - Disabled successfully")
                        else:
                            log.warn(f"Warning - G-key-mode - Unknown response: {str(confirmation_bytes)}")
                        response_count = response_count - 1
                    except usb.core.USBError as e:
                        log.debug(str(e))

                time.sleep(0.2)

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
                log.error(f"USBError {e.errno}")
                time.sleep(0.5)
                self.init_usb_dev()
            else:
                log.exception(e)
                g910_gkey_mapper.program_running = False

    def __exit__(self):
        try:
            if self.dev and self.dev.is_kernel_driver_active(self.usb_if) is False:
                usb.util.release_interface(self.dev, self.usb_if)
                log.debug("attaching kernel driver")
                self.dev.attach_kernel_driver(self.usb_if)
        except usb.core.USBError as e:
            log.error("Could not re-attach kernel driver: " + str(e))
        except UnboundLocalError:
            pass
