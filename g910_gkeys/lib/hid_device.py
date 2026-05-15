import errno
import logging
import time
import signal
import hidraw
from g910_gkeys.data_mappers.supported_devices import KeyboardInterface, SUPPORTED_DEVICES
from g910_gkeys.misc.logger import Logger


class HIDDevice:
    log: logging.Logger = None
    keyboard: KeyboardInterface = None
    dev: hidraw.device = None

    interface: int = 1  # Interface
    timeout: int = 300  # Timeout in MS

    def __init__(self, interface: int = 1):
        self.log = Logger().logger(__name__)
        if interface is not None:
            self.interface = interface
        self.init_hid_device()

    def init_hid_device(self):
        for keyboard in SUPPORTED_DEVICES:
            try:
                self.open_specific_interface(keyboard.usbVendor, keyboard.usbProduct, self.interface)
                if self.dev is not None:
                    self.keyboard = keyboard
                    break
            except OSError:
                time.sleep(0.1)

        if self.dev is None:
            self.log.warning("No supported keyboard found.")
            return

        self.log.info(f"Keyboard {self.keyboard.deviceName} found.")
        self.log.debug(f"hid dev: {self.dev.get_serial_number_string()}")

    def open_specific_interface(self, vid, pid, target_interface):
        device_info_list = hidraw.enumerate(vid, pid)

        target_path = None
        for info in device_info_list:
            if info['interface_number'] == target_interface:
                target_path = info['path']
                break

        if target_path:
            self.dev = hidraw.device()
            self.dev.open_path(target_path)
            self.dev.set_nonblocking(True)

    def disable_fkey_to_gkey_binding(self):
        time.sleep(0.5)
        self.log.info("Trying to disable f-key to g-key binding")

        if self.keyboard.disableGKeysInterface:
            for packet in self.keyboard.events.disableGKeys:
                self.log.debug(f"Sending HID feature report to keyboard {str(packet)}...")
                if self.keyboard.disableGKeysUseWrite:
                    byte_written = self.dev.write(packet)
                    self.log.debug(f"Completed (sent {byte_written} byte)")
                else:
                    pass

                response_count = len(self.keyboard.events.disableGKeysResponse)
                while response_count:
                    try:
                        confirmation_bytes = self.read()
                        if confirmation_bytes is None:
                            response_count = response_count - 1
                            continue

                        if bytes(confirmation_bytes) in self.keyboard.events.disableGKeysResponse:
                            self.log.debug(f"G-key-mode - response: {str(confirmation_bytes)}")
                            if bytes(confirmation_bytes) == packet:
                                self.log.info("G-key-mode - Disabled successfully")
                        else:
                            self.log.warning(f"Warning - G-key-mode - Unknown response: {str(confirmation_bytes)}")
                            return False
                        response_count = response_count - 1
                    except OSError as e:
                        self.log.debug(str(e))

                time.sleep(0.2)
        return True

    def enable_fkey_to_gkey_binding(self):
        self.log.info("Trying to enable f-key to g-key binding")
        if self.keyboard.disableGKeysInterface:
            for packet in self.keyboard.events.enableGKeys:
                self.log.debug(f"Sending HID feature report to keyboard {str(packet)}...")
                if self.keyboard.disableGKeysUseWrite:
                    byte_written = self.dev.write(packet)
                    self.log.debug(f"Completed (sent {byte_written} byte)")
                else:
                    pass

                response_count = len(self.keyboard.events.enableGKeysResponse)
                while response_count:
                    try:
                        confirmation_bytes = self.read()
                        if confirmation_bytes is None:
                            response_count = response_count - 1
                            continue

                        if bytes(confirmation_bytes) in self.keyboard.events.enableGKeysResponse:
                            self.log.debug(f"G-key-mode - response: {str(confirmation_bytes)}")
                            if bytes(confirmation_bytes) == packet:
                                self.log.info("G-key-mode - Enabled successfully")
                        else:
                            self.log.warning(f"Warning - G-key-mode - Unknown response: {str(confirmation_bytes)}")
                            return False
                        response_count = response_count - 1
                    except OSError as e:
                        self.log.debug(str(e))

                time.sleep(0.2)
        return True

    def read(self):
        try:
            if self.dev and self.keyboard:
                data = self.dev.read(64, timeout_ms=self.timeout)
                return data or None
        except OSError as e:
            # If it's a generic "read error" string while non-blocking,
            # it almost always means the buffer was empty during a state change.
            if "read error" in str(e):
                return None

            # Log actual critical hardware errors (like device unplugged)
            self.log.error(f"Critical HID read error: {e}")
        except Exception as e:
            self.log.exception(e)
            signal.raise_signal(signal.SIGQUIT)

    def __exit__(self):
        try:
            if self.dev:
                self.dev.close()
        except OSError as e:
            self.log.error("Could not close HID device: " + str(e))
