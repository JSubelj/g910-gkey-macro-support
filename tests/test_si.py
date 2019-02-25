from lib.uinput_keyboard import keyboard
import time
from lib.keyboard_initialization import usb_and_keyboard_device_init

device = usb_and_keyboard_device_init.init_uinput_device()
time.sleep(1)
layout = "si"


def shortcut(string):
    keyboard.shortcut(string, layout, device)
    keyboard.release(device)
    time.sleep(0.5)
    if len(keyboard.press_release_fifo):
        print("PRESS_RELEASE_FIFO is not empty!")


def writeout(string):
    keyboard.writeout(string, layout, device)
    time.sleep(0.5)


string = " ,'0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXzZyY=!\"#$%&/()˝~ˇ^˘°˛`˙""¸čćšžđ.-*?ŠĐČĆ¨Ž;:_\\|€¶ŧ←↓→øþ÷×æ„“[]ħłß¤‘’¢@{}<>—\t\n"
path = "/tmp/test_g910.txt"
shortcut("ctrl+alt+t")
writeout("rm " + path + "\n")
writeout("vim " + path + "\n")
writeout("i" + string)
shortcut("capslock+a,a,capslock+a,a")
print("pressing esc")
time.sleep(5)
shortcut("esc")
print("pressing :wq entr")
time.sleep(5)
shortcut("shift+.,w,q,enter")
print("typing exit")
time.sleep(5)
writeout("exit\n")
string+="AAAa"

print("testing", layout, "layout")

with open(path, "r") as f:
    read_string = f.read()

is_correct = True
for i in range(len(string)):
    if string[i] != read_string[i]:
        is_correct = False
        print("should be:", repr(string[i]), "; is:", repr(read_string[i]))

print("Everything ok:", is_correct)

device.__exit__()
