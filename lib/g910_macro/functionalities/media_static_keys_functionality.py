import uinput


def volume_up(device):
    device.emit_click(uinput.KEY_VOLUMEUP)


def volume_down(device):
    device.emit_click(uinput.KEY_VOLUMEDOWN)


def volume_mute(device):
    device.emit_click(uinput.KEY_MUTE)


def play_pause(device):
    device.emit_click(uinput.KEY_PLAYPAUSE)


def stop(device):
    device.emit_click(uinput.KEY_STOPCD)


def next_song(device):
    device.emit_click(uinput.KEY_NEXTSONG)


def prev_song(device):
    device.emit_click(uinput.KEY_PREVIOUSSONG)


def resolve_key(device, key):
    if key is 'vol_down':
        volume_down(device)
        return True

    elif key is 'vol_up':
        volume_up(device)
        return True

    elif key is 'vol_mute':
        volume_mute(device)
        return True

    elif key is 'play_pause':
        play_pause(device)
        return True

    elif key is 'stop':
        stop(device)
        return True

    elif key is 'prev_song':
        prev_song(device)
        return True

    elif key is 'next_song':
        next_song(device)
        return True
    return False
