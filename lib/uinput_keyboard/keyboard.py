from lib.data_mappers.char_uinput_mapper import keys, reverse_keys
import time
from lib.misc import logger

log = logger.logger(__name__)


def execute_events(events, device):
    for event in events:
        if event[1] == 3:
            device.emit_click(event[0])
        else:
            device.emit(*event)

        time.sleep(0.02)


def writeout(string, charset, device):
    for c in string:
        execute_events(keys[charset][c],device)

press_release_fifo = []

def release(device):
    keys_to_release = press_release_fifo.pop(0)
    to_log = ""
    for key in keys_to_release:
        device.emit(key, 0)
        to_log+=" "+reverse_keys[key]+","

    log.info("Released keys:"+to_log[:-1]+" Shortcuts to release: "+str(len(press_release_fifo))+" (Should always be 0)")


def shortcut(value, keymap, device):
    press_together = []

    together = value.split(",")

    for hotkey in together:
        keys_str = hotkey.split("+")
        press_together.append(keys_str)

    uinput_groups = []
    for combo in press_together:
        uinput_combo = []
        for key_string in combo:
            if len(key_string) == 1:
                uinput_combo.append(keys[keymap][key_string][0][0])
            else:
                uinput_combo.append(keys["control"][key_string][0][0])

        uinput_groups.append(uinput_combo)

    if len(uinput_groups) == 1:
        keys_to_fifo = []
        for uinput_key in uinput_groups[0]:
            keys_to_fifo.insert(0, uinput_key)
            device.emit(uinput_key, 1)
            time.sleep(0.02)
        press_release_fifo.insert(0,keys_to_fifo)

    else:
        for group in uinput_groups:
            print(group)
            device.emit_combo(group)

if __name__=="__main__":
    import uinput, time
    from lib.data_mappers.uinput_all_keys import uinput_all_keys
    dev = uinput.Device(uinput_all_keys)
    time.sleep(4)
    shortcut("ctrl+c,f,d,s,a,f,ctrl+v","si",dev)
