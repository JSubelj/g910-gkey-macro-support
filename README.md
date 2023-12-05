# Logitech G910 keyboard gkey support for GNU/Linux (Project version: v0.4.1)
Because I didn't find any GKey support for Logitech G910 keyboard I decided to create this GKey mapper.
Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3)
in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more 
user-friendly to add functionality to GKeys.

Everything is described in great depth (and actually much better) on [WIKI](https://github.com/JSubelj/g910-gkey-macro-support/wiki).

## Requirements

To use this project you need:
 - Python >=3.7
 - pyusb & python-uinput
 - uinput kernel module (more on this [here](http://tjjr.fi/sw/python-uinput/#Usage))
 
#### Note: 
From version 0.2.0 onwards the g810-led controller is no longer required because G-key to F-key mapping is disabled inside the driver.

## Installation \[[AUR](https://aur.archlinux.org/packages/g910-gkeys-git/)\]
Be sure uinput kernel module is loaded: `modprobe uinput` (on Manjaro is loaded by default afaik) 

### Install script (recommended)
```bash
wget https://raw.githubusercontent.com/JSubelj/g910-gkey-macro-support/master/install_prebuild; chmod +x install_prebuild; ./install_prebuild
```

### Installation from source
 - clone repo:  
   ```
   git clone https://github.com/JSubelj/g910-gkey-macro-support.git
   ```  
   or download & unzip:  
   ```
   wget https://github.com/JSubelj/g910-gkey-macro-support/archive/refs/heads/master.zip; unzip master.zip
   ```
 - move to driver directory: `cd g910-gkey-macro-support`
 - run the installer script: `chmod +x install; ./install`
 - This will install the module, set a command `g910-gkeys`, add a service file to `/usr/lib/systemd/user/g910-gkeys.service` or similar, install a default configuration file in `$HOME/.config/g910-gkeys/config.json` if none exists, and finally enable and start this service.

If you do not want to enable g910-gkeys automatically, use the `-n` switch: `./install -n`. If you want to enable it later you can use: `systemctl --user enable --now g910-gkeys.service`. To just start the service till next reboot use: `systemctl --user start g910-gkeys`
 
## Update
### <= v0.3.0
If you use the installer your old config will be moved to the new location automatically. On pip and manual installations you need to move your old config file to the new location and set the permissions to your username.
```
sudo mv /etc/g910-gkeys/config.json "$HOME"/.config/g910-gkeys/config.json
sudo chown "$USER":"$USER" "$HOME"/.config/g910-gkeys/config.json
```

You can delete the old log file `sudo rm /var/log/g910-gkeys.log`.

### <= v0.2.4
 If you update from version <= v0.2.4 you will need to make some manual changes to your `/etc/g910-gkeys/config.json` to make use of the new gkey profile feature.
 You don't need to do anything if you don't want to use the profile feature your old config will be loaded as default profile m1.

## Uninstalling
### By script (recommended)
Run the uninstalling script: `chmod +x uninstall; ./uninstall`  
Run `./uninstall -d` to perform a dry-run (no actual removal will be done, actions will only be displayed).

### Manual uninstall
If you prefer to do it manually, these are the commands :

 1. Disable and stop the service: `systemctl --user disable --now g910-gkeys`
 2. List pip packages that include g910-gkeys: `pip (or pip3) list | grep g910-gkeys`
 3. Remove the ones that concern this driver: `pip (or pip3) uninstall ${pkgs to uninstall}`
 4. Optional: Remove configuration directory `rm -rf '$HOME/.config/g910-gkeys`  
    If you want to reinstall the driver again later consider keeping the config file.

## Configuration
Configuration should be located in `/home/[username]/.config/g910-gkeys/config.json` and should be syntactically correct. Example 
configuration can be found in etc/ folder: [config.json](etc/config.json). 

### Supported languages:
 * `"de"` - german
 * `"en"` - english (default)
 * `"fr"` - french
 * `"si"` - slovenian

Even if your language is not supported you can still use the driver with hotkey_type run. Other types won't work as expected with the wrong language configured.

### Hotkey types
The mapper supports five types of hotkeys (also described in [hotkey_types.txt](docs/hotkey_types.txt)):
 * `"typeout"` - Type out (ex. clicking on GKey types out a string)
 * `"shortcut"` - Shortcuts (ex. clicking on GKey presses shift+f4)
 * `"run"` - Starting a program (anything you can start from shell)
 * `"python"` - Execute a snippet of Python code and print provided output (see ex. below)
 * `"uinput"` - Direct mapping with uinput.KEY_XY
 * `"nothing"` - Do nothing (unbound key)

To add a hotkey add to `config.json` the following code:
```
"g<no_of_gkey>": {
    "hotkey_type": <type of command "nothing" or "typeout" or "shortcut" or "run">,
    "do": "<thing to do>"
}
```

Depending on the hotkey command, the syntax for "do" is different (supported characters for typeout and 
hotkeys are listed in [supported_keys.txt](docs/supported_keys.txt)):
 * `"typeout"` - Type out syntax is same as you would type text out (ex. "tyPe Me Out!")
 * `"shortcut"` - Shortcuts are separated by a plus sign and a comma (ex. "ctrl+c,ctrl+v")
 * `"nothing"` - If `hotkey_type` is set to `"nothing"` then "do" key need not exist or can be anything.
 * `"run"` - Run has the same syntax as you would type a cli program in command line (ex. "systemctl daemon-reload")
 * `"python"` - A Python one-line script. If output is desired, the script should define a global variable named `output_string` and set it to the string to be output.
 * `"uinput"` - A key defined by python3-uinput to emit (ex. KEY_F13 or KEY_KATAKANA)

**Important: Commands and python code is executed as root**

### Profiles
There are four profiles you can use and set up different gkey macros in config. Select the profile with M[1-3|R] key on your keyboard.
If you use the profile feature you can also use the following parameter:
 * `notify` - Send notifications if profile gets changed
 * `profiles` - Define a profile which is bound to the matching mkey

The following example shows how to set slovenian layout and define the g1-5 macro keys for profile m1 and m2 and shows an example of every `hotkey_type`.
 ```
{
    "notify": "True",
    "keyboard_mapping": "si",
    "profiles": {
        "MEMORY_1": {
            "MACRO_1": {
                "hotkey_type": "uinput",
                "do": "KEY_F13"
            },
            "MACRO_2": {
                "hotkey_type": "shortcut",
                "do": "ctrl+c"
            },
            "MACOR_3": {
                "hotkey_type": "typeout",
                "do": "averylongemailadressyoudontwanttowriteoutyourself@gmail.com"
            },
            "MACRO_4": {
                "hotkey_type": "run",
                "do": "/path/to/bash/script"
            },
            "MACRO_5": {
                "hotkey_type": "python",
                "do": "import datetime; global output_string; output_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')"
            }
        },
        "MEMORY_2": {
            "MACRO_1": {
                "hotkey_type": "uinput",
                "do": "KEY_KATAKANA"
            },
            "MACRO_2": {
                "hotkey_type": "shortcut",
                "do": "ctrl+v"
            },
            "MACRO_3": {
                "hotkey_type": "typeout",
                "do": "ssh -p1234 -i ~/.ssh/id_rsa user@domain\n"
            },
            "MACRO_4": {
                "hotkey_type": "run",
                "do": "DISPLAY=:0 nohup firefox & 2>&1 > /dev/null"
            },
            "MACRO_5": {
                "hotkey_type": "python",
                "do": "import datetime; global output_string; output_string = datetime.datetime.now().isoformat()"
            }
        }
    }
}
 ```
The DISPLAY variable defines the screen to open the app on a multi-screen-setup.

## Troubleshooting
To see a log of the running service use:
```sehll
journalctl --user --user-unit=g910-gkeys
```

The code is tested on Logitech G910 keyboard with
- OS: Ubuntu 20.04.6 LTS, Linux 5.4.0-159-generic, GNOME: 3.36.9

### Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. 
IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE 
BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
