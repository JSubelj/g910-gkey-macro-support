# this file has function that can help you get the right config for your layout. it is not optimized i dont even promise
# that it will work when u run it, if there's interest i can beautify it so it will be simpler to use. open an issue or smth idk.
import uinput
from lib.data_mappers import uinput_all_keys
from lib.data_mappers.char_uinput_mapper import keys

def click(uinput_key):
    return [(uinput_key, 3)]

def wrap_shift(key_array):
    return [(uinput.KEY_LEFTSHIFT, 1)]+key_array+[(uinput.KEY_LEFTSHIFT, 0)]


def wrap_altgr(key_array):
    return [(uinput.KEY_RIGHTALT, 1)]+key_array+[(uinput.KEY_RIGHTALT, 0)]

def get_shift_keys():
    import sys
    import time
    time.sleep(5)
    device = uinput.Device(uinput_all_keys.uinput_all_keys)
    for i in range(48, 58):
        sys.stdout.write("'")
        sys.stdout.flush()

        for key in wrap_shift(click(getattr(uinput, "KEY_" + chr(i)))):
            time.sleep(0.1)
            device.emit(*key)
        sys.stdout.write("': wrap_shift(click(uinput.KEY_" + chr(i) + ")),\n")
        sys.stdout.flush()

def get_altgr_keys():
    import sys
    import time
    time.sleep(5)
    device = uinput.Device(uinput_all_keys.uinput_all_keys)
    for i in range(48, 58):
        sys.stdout.write("'")
        sys.stdout.flush()

        for key in wrap_altgr(click(getattr(uinput, "KEY_" + chr(i)))):
            time.sleep(0.1)
            device.emit(*key)
        device.emit_click(uinput.KEY_SPACE)
        time.sleep(0.1)
        sys.stdout.write("': wrap_altgr(click(uinput.KEY_" + chr(i) + ")+click(uinput.KEY_SPACE)),\n")
        sys.stdout.flush()

def get_other_keys():
    keys = {"uinput.KEY_MINUS" : uinput.KEY_MINUS,
"uinput.KEY_EQUAL" : uinput.KEY_EQUAL,
"uinput.KEY_BACKSPACE" : uinput.KEY_BACKSPACE,
"uinput.KEY_TAB" : uinput.KEY_TAB,
"uinput.KEY_Q" : uinput.KEY_Q,
"uinput.KEY_W" : uinput.KEY_W,
"uinput.KEY_E" : uinput.KEY_E,
"uinput.KEY_R" : uinput.KEY_R,
"uinput.KEY_T" : uinput.KEY_T,
"uinput.KEY_Y" : uinput.KEY_Y,
"uinput.KEY_U" : uinput.KEY_U,
"uinput.KEY_I" : uinput.KEY_I,
"uinput.KEY_O" : uinput.KEY_O,
"uinput.KEY_P" : uinput.KEY_P,
"uinput.KEY_LEFTBRACE" : uinput.KEY_LEFTBRACE,
"uinput.KEY_RIGHTBRACE" : uinput.KEY_RIGHTBRACE,
"uinput.KEY_ENTER" : uinput.KEY_ENTER,
"uinput.KEY_LEFTCTRL" : uinput.KEY_LEFTCTRL,
"uinput.KEY_A" : uinput.KEY_A,
"uinput.KEY_S" : uinput.KEY_S,
"uinput.KEY_D" : uinput.KEY_D,
"uinput.KEY_F" : uinput.KEY_F,
"uinput.KEY_G" : uinput.KEY_G,
"uinput.KEY_H" : uinput.KEY_H,
"uinput.KEY_J" : uinput.KEY_J,
"uinput.KEY_K" : uinput.KEY_K,
"uinput.KEY_L" : uinput.KEY_L,
"uinput.KEY_SEMICOLON" : uinput.KEY_SEMICOLON,
"uinput.KEY_APOSTROPHE" : uinput.KEY_APOSTROPHE,
"uinput.KEY_GRAVE" : uinput.KEY_GRAVE,
"uinput.KEY_LEFTSHIFT" : uinput.KEY_LEFTSHIFT,
"uinput.KEY_BACKSLASH" : uinput.KEY_BACKSLASH,
"uinput.KEY_Z" : uinput.KEY_Z,
"uinput.KEY_X" : uinput.KEY_X,
"uinput.KEY_C" : uinput.KEY_C,
"uinput.KEY_V" : uinput.KEY_V,
"uinput.KEY_B" : uinput.KEY_B,
"uinput.KEY_N" : uinput.KEY_N,
"uinput.KEY_M" : uinput.KEY_M,
"uinput.KEY_COMMA" : uinput.KEY_COMMA,
"uinput.KEY_DOT" : uinput.KEY_DOT,
"uinput.KEY_SLASH" : uinput.KEY_SLASH,
"uinput.KEY_RIGHTSHIFT" : uinput.KEY_RIGHTSHIFT,
"uinput.KEY_KPASTERISK" : uinput.KEY_KPASTERISK,
"uinput.KEY_LEFTALT" : uinput.KEY_LEFTALT,
"uinput.KEY_SPACE" : uinput.KEY_SPACE,
"uinput.KEY_CAPSLOCK" : uinput.KEY_CAPSLOCK}
    import sys
    import time
    time.sleep(5)
    device = uinput.Device(uinput_all_keys.uinput_all_keys)
    for val,key in keys.items():
        sys.stdout.write("'")
        sys.stdout.flush()
        for key_event in click(key):
            time.sleep(0.1)
            device.emit(*key_event)
        #device.emit_click(uinput.KEY_SPACE)
        #time.sleep(0.1)
        sys.stdout.write("': click("+val+"),\n")
        sys.stdout.flush()


def get_keys():
    for i in range(48,58):
        print("'"+chr(i)+"': click(uinput.KEY_"+chr(i)+"),")

    for i in range(65,91):
        #if chr(i) == 'Z':
        #    print("'y': click(uinput.KEY_Z),")
        #    print("'Y': wrap_shift(click(uinput.KEY_Z)),")
        #elif chr(i) == 'Y':
        #    print("'z': click(uinput.KEY_Y),")
        #    print("'Z': wrap_shift(click(uinput.KEY_Y)),")

        #else:
        print("'"+chr(i).lower()+"': click(uinput.KEY_"+chr(i)+"),")
        print("'"+chr(i)+"': wrap_shift(click(uinput.KEY_"+chr(i)+")),")

def get_fkeys():
    for i in range(1,13):
        print("'F"+str(i)+"': click(uinput.KEY_F"+str(i)+"),")


def execute_events(events, device):
    import time
    for event in events:
        if event[1] == 3:
            device.emit_click(event[0])
        else:
            device.emit(*event)

        time.sleep(0.02)


def writeout(string, charset, device):
    for c in string:
        execute_events(keys[charset][c],device)

def test():
    import sys
    import time

    device = uinput.Device(uinput_all_keys.uinput_all_keys)
    time.sleep(4)
    events = keys['en']
    for key, event in events.items():
        sys.stdout.write("'"+key+"'=='")
        sys.stdout.flush()
        time.sleep(0.1)
        execute_events(event,device)
        time.sleep(0.1)
        sys.stdout.write("'\n")

if __name__ == "__main__":
    #print(keys)
    #get_keys()
    #get_shift_keys()
    #get_altgr_keys()
    #get_other_keys()
    #test()
    import uinput_all_keys

    import time
    device = uinput.Device(uinput_all_keys.uinput_all_keys)

    time.sleep(4)
    #writeout("šđčćžŠĐČĆŽ\n","si", device)
    #get_fkeysfdsaf( )
