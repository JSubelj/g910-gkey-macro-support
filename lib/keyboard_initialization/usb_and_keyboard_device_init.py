import time
import usb
from lib.misc import logger
from lib import g910_gkey_mapper

log = logger.logger(__name__)


class USBDevice:
    dev = endpoint = None
    usb_vendor = 0x046d
    usb_product = (0x0c32b, 0xc335)
    usb_if = 1  # Interface
    usb_timeout = 1000  # Timeout in MS

    def __init__(self, usb_if: int):
        if usb_if is not None:
            self.usb_if = usb_if
        self.init_usb_dev()
        if self.dev.is_kernel_driver_active(self.usb_if) is True:
            log.debug("detaching kernel driver")
            self.dev.detach_kernel_driver(self.usb_if)

    def init_usb_dev(self):
        select_product = 0
        self.dev = usb.core.find(idVendor=self.usb_vendor, idProduct=self.usb_product[select_product])
        while not self.dev:
            select_product = abs(select_product - 1)
            log.debug("usb dev: not found. retrying with other product id")
            self.dev = usb.core.find(idVendor=self.usb_vendor, idProduct=self.usb_product[select_product])
            time.sleep(0.1)

        log.debug("usb dev: " + str(self.dev[0][(self.usb_if, 0)]))
        self.endpoint = self.dev[0][(self.usb_if, 0)][0]
        self.usb_timeout = self.dev.default_timeout
        log.debug(f"Device default timeout: {self.dev.default_timeout}ms")

    def disable_fkey_to_gkey_binding(self):
        log.info("Trying to disable mapping")
        log.debug("Sending disable")
        packet = [0x11, 0xff, 0x08, 0x2e, 0x2]
        for _ in range(len(packet), 20):
            packet.append(0)

        disable_return = self.dev.ctrl_transfer(0x21, 0x09, 0x0212, 1, packet, 2000)  # write(1,packet,USB_TIMEOUT))
        log.debug("Got: " + str(disable_return))
        time.sleep(0.001)

        buffer = []
        for _ in range(64):
            buffer.append(0)

        # Don't really know why this has to be sent, it's included in the original g810-leds
        ret = self.dev.write(0x82, buffer, 2000)
        log.debug("Got: " + str(ret))

        operation_successful = [17, 255, 8, 46, 2]
        while 1:
            time.sleep(0.001)
            confirmation_bytes = self.dev.read(self.endpoint.bEndpointAddress,
                                               self.endpoint.wMaxPacketSize, self.usb_timeout)
            if list(confirmation_bytes[:5]) == operation_successful:
                log.info("Mapping disabled successfully")
                break
        return True

    def init_g910_keyboard(self):
        counter = 0
        log.debug("gathering usb device")
        while not self.dev:
            try:
                self.init_usb_dev()
            except SystemExit:
                g910_gkey_mapper.program_running = False
            except usb.core.USBError as e:
                if e.errno == 5:
                    counter += 1
                    if counter >= 1000:
                        log.warning("USBError: Input/Output Error")
                        counter = 0
                    time.sleep(0.01)
                else:
                    log.warning("Getting keyboard error: " + str(e))
            except Exception as e:
                log.exception(e)
            '''
            successfully_disabled_mapping = False
            counter = 0
            while g910_gkey_mapper.program_running and not successfully_disabled_mapping:
                try:
                    successfully_disabled_mapping = self.disable_fkey_to_gkey_binding()
                except SystemExit:
                    g910_gkey_mapper.program_running = False
                except usb.core.USBError as e:
                    log.error(e)
                    g910_gkey_mapper.program_running = False
                except Exception as e:
                    log.debug(e)
                    if e.args[0] == 110:
                        counter += 1
                        if counter >= 5:
                            log.warning("Can't disable mapping")
                            counter = 0
                        time.sleep(0.01)
                    else:
                        log.warning("Disable mapping error!", e)
                        g910_gkey_mapper.program_running = False
                        try:
                            self.dev, self.endpoint, self.usb_timeout, self.usb_if = self.init_usb_dev()
                        except SystemExit:
                            g910_gkey_mapper.program_running = False
                        except:
                            pass
                '''
        return self.dev, self.endpoint, self.usb_timeout, self.usb_if

    def read(self):
        try:
            if self.dev:
                return self.dev.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize, self.usb_timeout)
        except usb.core.USBError as e:
            if e.errno == 110:  # Operation timed out
                pass  # nothing to read from device
            elif e.errno == 19 or e.errno == 5:
                # 19 - No such device
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
