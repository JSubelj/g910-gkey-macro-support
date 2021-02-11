commands = {
    'release': bytearray(b'\x11\xff\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g1': bytearray(b'\x11\xff\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g2': bytearray(b'\x11\xff\x08\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g3': bytearray(b'\x11\xff\x08\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g4': bytearray(b'\x11\xff\x08\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g5': bytearray(b'\x11\xff\x08\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g6': bytearray(b'\x11\xff\x08\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g7': bytearray(b'\x11\xff\x08\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g8': bytearray(b'\x11\xff\x08\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g9': bytearray(b'\x11\xff\x08\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'm1': bytearray(b'\x11\xff\t\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'm2': bytearray(b'\x11\xff\t\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'm3': bytearray(b'\x11\xff\t\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'mr': bytearray(b'\x11\xff\n\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'm1-3_key_release': bytearray(b'\x11\xff\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'mr-key_release': bytearray(b'\x11\xff\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'vol_down': bytearray(b'\x02 '),
    'vol_up': bytearray(b'\x02\x10'),
    'media_release': bytearray(b'\x02\x00'),
    'vol_mute': bytearray(b'\x02@'),
    'play_pause': bytearray(b'\x02\x08'),
    'stop': bytearray(b'\x02\x04'),
    'next_song': bytearray(b'\x02\x01'),
    'prev_song': bytearray(b'\x02\x02'),
}

for base in range(1, 10):
    for secondary in range(base + 1, 10):
        base_g_command = commands['g' + str(base)]
        secondary_g_command = commands['g' + str(secondary)]
        combined_keys_command = bytearray(base_g_command);
        for index, byte in enumerate(secondary_g_command):
            combined_keys_command[index] = base_g_command[index] | secondary_g_command[index]
        commands['g'+str(base)+'+g'+str(secondary)] = combined_keys_command
