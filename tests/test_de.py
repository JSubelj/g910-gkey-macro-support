from lib.uinput_keyboard import keyboard
import time
from lib.keyboard_initialization import usb_and_keyboard_device_init

device = usb_and_keyboard_device_init.init_uinput_device()
time.sleep(1)
layout="de"
def shortcut(string):
    keyboard.shortcut(string, layout, device)
    keyboard.release(device)
    time.sleep(0.5)
    if len(keyboard.press_release_fifo):
        print("PRESS_RELEASE_FIFO is not empty!")

def writeout(string):
    keyboard.writeout(string, layout, device)
    time.sleep(0.5)


string="0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZäÄöÖüÜ!\"§$%&/()=²³¼½¬{[]}#'´`-_@~ß?\\^°*,;.:€"
path = "/tmp/test_g910.txt"
shortcut("ctrl+shift+t")
writeout("rm "+path)
shortcut("enter")
writeout("vim "+path)
shortcut("enter")
writeout("i"+string)
shortcut("esc")
writeout(":wq")
shortcut("enter")
writeout("exit")
shortcut("enter")

print("testing",layout,"layout")

with open(path,"r") as f:
    read_string = f.read()

is_correct = True
for i in range(len(string)):
    if string[i] != read_string[i]:
        is_correct = False
        print("should be:",repr(string[i]),"; is:",repr(read_string[i]))

print("Everything ok:",is_correct)
