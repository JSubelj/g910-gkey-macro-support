As of version 0.2.5 the default language set in keyboard_mapping is `en`. In earlier versions the default keyboard_mapping was set to `si` for slovene, because the author of this package is from [Slovenia](https://en.wikipedia.org/wiki/Slovenia). If you have another keyboard layout configured in your system you need to change this in the configuration accordingly.

## Location
Config created on setup is located in: `/etc/g910-gkeys/config.json`

## Config layout
The driver is set up so that it will work without any data in config (using the default data written in [supported_configs.py](https://github.com/JSubelj/g910-gkey-macro-support/blob/master/lib/data_mappers/supported_configs.py)) so the data written in `config.json` can be `{}` and it will work, but that doesn't really add any functionality at all. So the default config (which the driver writes on first run) is:
```
{
  "__comment" : "following hotkey types are supported: nothing, typeout, shortcut and run; only en, fr, de and si keyboard mappings are currently supported",
  "keyboard_mapping": "en",
  "notify": "True",
  "username": "",
  "profiles": {
    "MEMORY_1": {
      "MACRO_1": {
        "hotkey_type": "typeout",
        "do": "This is profile m1"
      },
      "MACRO_2": {
        "hotkey_type": "shortcut",
        "do": "alt+F4"
      },
      "MACRO_3": {
        "hotkey_type": "run",
        "do": "su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null"
      },
      "MACRO_4": {
        "hotkey_type": "nothing"
      }
    },
    "MEMORY_2": {
      "MACRO_1": {
        "hotkey_type": "typeout",
        "do": "This is profile m2"
      },
      "MACRO_2": {
        "hotkey_type": "shortcut",
        "do": "alt+F4"
      },
      "MACRO_3": {
        "hotkey_type": "run",
        "do": "su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null"
      },
      "MACRO_4": {
        "hotkey_type": "nothing"
      }
    },
    "MEMORY_3": {
      "MACRO_1": {
        "hotkey_type": "typeout",
        "do": "This is profile m3"
      },
      "MACRO_2": {
        "hotkey_type": "shortcut",
        "do": "alt+F4"
      },
      "MACRO_3": {
        "hotkey_type": "run",
        "do": "su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null"
      },
      "MACRO_4": {
        "hotkey_type": "nothing"
      }
    },
    "MEMORY_RECORD": {
      "MACRO_1": {
        "hotkey_type": "typeout",
        "do": "This is profile mr"
      },
      "MACRO_2": {
        "hotkey_type": "shortcut",
        "do": "alt+F4"
      },
      "MACRO_3": {
        "hotkey_type": "run",
        "do": "su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null"
      },
      "MACRO_4": {
        "hotkey_type": "nothing"
      }
    }
  }
}
```

## Config keys
`keyboard_mapping` - Keyboard layout, supported languages:  
   * `"de"` - german
   * `"en"` - **english (default)**
   * `"fr"` - french
   * `"si"` - slovenian

`notify` - Show notifications on profile changed  

`username` - used to show notification (optional)  

`profiles` - use up to 4 profiles, define `MEMORY_[1-3|RECORD]` as entity of profile  

`MEMORY_[1-3|RECORD]` - switch profile (only if you have more than one profile in config.json)  

`MACRO_[1-N]` - G-keys macro definition, defined in root of config if no profiles are needed or as entity of the assigned profile. In each `MACRO_[1-N]` object you have two entities `hotkey_type` and `do` which set what to do when a gkey is pressed.

### Hotkey types
There are currently 6 hotkey types: `nothing`, `shortcut`, `typeout`, `run` and `python`, `uinput` their functionality is as follows:

#### Type out - `"typeout"`  
Types out what is written in "do" key by key, as you would on a keyboard. New line is `\n` and tab is `\t`.

#### Shortcuts - `"shortcut"`  
Press keys that are separated by a comma at the same time. For example copying "ctrl+c", or pasting and writing out: "ctrl+v,i, ,d,i,d, ,i,t"). For characters, only simple ones (without altgr or shift pressing) are supported, so characters like @ can't be typed in shortcut, you'll have to use typeout for that. (Or use `altgr+v` on slovenian layout). If there are no commas (`,`) in the `do` field the driver now releases the pressed keys when you release the GKey bind to it, so you can use them as a modifier.

#### Starting a program - `"run"`  
If you want to run something that interacts with gnome or your desktop service you need to wrap the call with su and your username:
   ```bash
   su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null
   ```

#### Execute a snippet of Python code - `"python"`  
A Python one-line script. If output is desired, the script should define a global variable named `output_string` and set it to the string to be output.

#### Map a G-Key to a different key - `"uinput"`
A key defined by python3-uinput to emit (ex. `KEY_F13` or `KEY_KATAKANA`)  
A full list of all available keys you can find [here](https://github.com/tuomasjjrasanen/python-uinput/blob/master/src/ev.py).

#### Do nothing - `"nothing"`

Also, not all possible characters and control keys are supported (yeah no emojis!). Supported characters and control keys can be viewed in [char_uinput_mapper.py](https://github.com/JSubelj/g910-gkey-macro-support/blob/master/lib/data_mappers/char_uinput_mapper.py).


>It is also worth pointing out that Enter and Tab keys are pressed while typing out `\n` and `\t`, so you can use this when controlling a program like vim or terminal without using `shortcut`.

## Example config for writing a test file by pressing gkeys
```
{
    "keyboard_mapping": "si",
    "profiles": {
        "MEMORY_1": {
            "MACRO_1": {
                "hotkey_type": "shortcut",
                "do": "ctrl+alt+t"
            },
            "MACRO_2": {
                "hotkey_type": "typeout",
                "do": "vim /tmp/test-gkey.txt\n"
            },
            "MACRO_3": {
                "hotkey_type": "typeout",
                "do": "iThis Is a Test \n \t also %$&$\"& characters."
            },
            "MACRO_4": {
                "hotkey_type": "shortcut",
                "do": "esc"
            },
            "MACRO_5": {
                "hotkey_type": "typeout",
                "do": ":wq\n"
            },
            "MACRO_6": {
                "hotkey_type": "typeout",
                "do": "cat /tmp/test-gkey.txt\n"
            }
        }
    }
}   
```

## Troubleshooting
### JSONDecoderError
So if you have written your config and the daemon doesn't run then you most likely have a syntax error in your config file. Since we parse the file you will get the error message from the parser in the log file:  
`tail -f /var/log/g910-gkeys.log`

### Other Config Problems
If the functionality still isn't what you expect, look into the logs: `/var/log/g910-gkey.log`  
There should be a warning of what is wrong, similar to this:  
`2018-11-21 19:21:40,576 [WARNING] {lib.data_mappers.config_reader} - Error(s) in config: {'g3': {'hotkey_type': 'typout does not exist!'}, 'g6': {'hotkey_type': 'typout does not exist!'}}`  
This says that `typout` does not exist for `hotkey_type`. To correct it I had to change `'hotkey_type': 'typout'` to `'hotkey_type': 'typeout`.

### Other Errors
If you find yourself with an error not listed above please take a look at the [troubleshooting](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Troubleshooting).