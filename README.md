# Logitech G910 keyboard gkey support for GNU/Linux (Project version: v0.2.5)

Because I didn't find any GKey support for Logitech G910 keyboard I decided to create this GKey mapper.
Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3)
in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more 
user friendly to add functionality to GKeys.

Everything is described in great depth (and actually much better) on [WIKI](https://github.com/JSubelj/g910-gkey-macro-support/wiki).

Note: From version 0.2.0 onwards the g810-led controller is no longer required because Gkey to Fkey mapping is disabled inside the driver.

## Requirements

To use this project you need:
 - Python >=3.7
 - git
 - uinput kernel module (more on this [here](http://tjjr.fi/sw/python-uinput/#Usage))
 - pip requirements are stored in requirements.txt
 - g810-led for color changing per profile, https://github.com/MatMoul/g810-led
 
## Installation \[[AUR](https://aur.archlinux.org/packages/g910-gkeys-git/)\]
 - ~~install [g810-led-git](https://github.com/MatMoul/g810-led) for your distro (for Arch based distros: [aur](https://aur.archlinux.org/packages/g810-led-git/))~~
 - ~~disable Gkeys to Fkeys mapping: `g910-led -gkm 1` (probably will include that on program start)~~
 - load uinput kernel module: `modprobe uinput` (on Manjaro is loaded by default afaik) 
 - clone repo: `git clone https://github.com/JSubelj/g910-gkey-macro-support.git`
 - move to cloned repo: `cd g910-gkey-macro-support`
 - run the installer shell: `chmod +x installer.sh; sudo ./installer.sh`
 - This will install the module, set a command `g910-gkeys`, add a service file to `/usr/lib/systemd/system/g910-gkeys.service` or `/lib/systemd/system/g910-gkeys.service`, install a default configuration file in `/etc/g910-gkeys/config.json` if none exists, and finally enable and start this service.

If you do not want to enable g910-gkeys automatically, use the `-n` switch: `sudo ./installer.sh -n`. You will have to do it yourself in this case: `sudo systemctl enable --now g910-gkeys.service`.
 
## Update
 If you update from version <= v0.2.4 you will need to make some manual changes to your `/etc/g910-gkeys/config.json` to make use of the new gkey profile feature.
 You don't need to do anything if you don't want to use the profile feature your old config will be loaded as default profile m1.

## Uninstalling
Run the uninstalling script: `chmod +x uninstall.sh; sudo ./uninstall.sh`. If you prefer to do it manually, these are the commands :

 1. Disable and stop the service: `sudo systemctl disable --now g910-gkeys`
 2. Remove installed files (list is in files.txt): `sudo xargs --arg-file=files.txt rm -rf`
 3. List pip packages that include g910-gkeys: `pip (or pip3) list | grep g910-gkeys`
 4. Remove the ones that concern this driver: `pip (or pip3) uninstall ${pkgs to uninstall}`
 5. Remove configuration directory if `-a` option is given to uninstall.sh: `rm -rf /etc/g910-gkeys`

If you deleted files.txt you can always run the installer again to create it.   
Run `uninstall.sh -d` to perform a dry-run (no actual removal will be done, actions will only be displayed).

## Configuration
Configuration should be located in `/etc/g910-gkeys/config.json` and should be syntactically correct. Example 
configuration can be found in docs folder: [ex_config](docs/ex_config/ex_config.json). 

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
 * `"typeout"` - Typeout syntax is same as you would type text out (ex. "tyPe Me Out!")
 * `"shortcut"` - Shortcuts are separated by a plus sign and a comma (ex. "ctrl+c,ctrl+v")
 * `"nothing"` - If `hotkey_type` is set to `"nothing"` then "do" key need not exist or can be anything.
 * `"run"` - Run has the same syntax as you would type a cli program in command line (ex. "systemctl daemon-reload")
 * `"python"` - A Python one-line script. If output is desired, the script should define a global variable named `output_string` and set it to the string to be output.

### Profiles
There are four profiles you can use and set up different gkey macros in config. Select the profile with M[1-3|R] key on your keyboard.
If you use the profile feature you can also use the following parameter:
 * `notify` - Send notifications if profile gets changed
 * `username` - Username to send notifications with (required if notify is used)
 * `profiles` - Define a profile which is bound to the matching mkey

The following example shows how to set slovenian layout and define the g1 key for profile m1 and m2 and shows how to run a app like firefox, chrome or similar. Please replace **\<username\>** with your username.
 ```
{
    "notify": "True",
    "username": "<username>",
    "keyboard_mapping": "si",
    "profiles": {
        "m1": {
            "g1": {
                "hotkey_type": "run",
                "do": "su <username> -c 'DISPLAY=:0 nohup firefox' & 2>&1 > /dev/null"
            },
            "g2": {
                "hotkey_type": "python",
                "do": "import datetime; global output_string; output_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')"
            }
        },
        "m2": {
            "g1": {
                "hotkey_type": "run",
                "do": "su <username> -c 'DISPLAY=:0 nohup chrome' & 2>&1 > /dev/null"
            },
            "g2": {
                "hotkey_type": "python",
                "do": "import datetime; global output_string; output_string = datetime.datetime.now().isoformat()"
            }
        }
    }
}
 ```

The code is tested on Logitech G910 keyboard with
- OS: Manjaro, 4.19.1 Linux kernel, DE: kde plasma 5.14.3
- OS: Ubuntu 20.04.5 LTS, Linux 5.4.0-131-generic, GNOME: 3.36.8

### Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. 
IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE 
BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
