import time
from lib.uinput_keyboard.keyboard import Keyboard

locale = "de"
keyboard = Keyboard()
keyboard.set_locale(locale)


def shortcut(keys):
    keyboard.execute_hotkey(keys)
    keyboard.release()


def write_out(data):
    keyboard.execute_writing(data)
    time.sleep(0.5)


string = "0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZäÄöÖüÜ!\"§$%&/()=²³¼½¬{[]}#'´`-_@~ß?\\^°*,;.:€"
path = "/tmp/test_g910.txt"
shortcut("ctrl+shift+t")
write_out("rm "+path)
shortcut("enter")
write_out("vim "+path)
shortcut("enter")
write_out("i"+string)
shortcut("esc")
write_out(":wq")
shortcut("enter")
write_out("exit")
shortcut("enter")

print("testing", locale, "layout")

with open(path, "r") as f:
    read_string = f.read()

is_correct = True
for i in range(len(string)):
    if string[i] != read_string[i]:
        is_correct = False
        print("should be:", repr(string[i]), "; is:", repr(read_string[i]))

print("Everything ok:", is_correct)
