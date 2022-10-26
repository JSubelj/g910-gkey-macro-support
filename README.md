# Logitech G910 keyboard gkey support for GNU/Linux (Project version: v0.2.4)

Because I didn't find any GKey support for Logitech G910 keyboard I decided to create this GKey mapper.
Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3)
in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more 
user friendly to add functionality to GKeys.

The code is tested on Logitech G910 keyboard, OS: Manjaro, 4.19.1 Linux kernel, DE: kde plasma 5.14.3.

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
 - This will install the module and set a command `g910-gkeys`, add a service file to `/usr/lib/systemd/system/g910-gkeys.service` and reload systemd daemon
 - start the daemon: `systemctl start g910-gkeys`
 - you can also add it to start on startup: `systemctl enable g910-gkeys`
 
## Uninstalling
 - Uninstalling can be done with files.txt that was created on install (if you deleted it you can always run the installer again to create it)
 - run command: `cat files.txt | sudo xargs rm -rf`
 - list pip packages that include g910: `pip list | grep g910`
 - remove the ones that concern this driver: `pip uninstall ${pkgs to uninstall}`
 - it is also recommended to disable the service: `systemctl disable g910-gkeys`
 - and remove it from system folder: `rm /usr/lib/systemd/system/g910-gkeys.service`
 - you can also delete the configuration: `rm /etc/g910-gkeys -rf`
 
## Configuration
Configuration should be located in `/etc/g910-gkeys/config.json` and should be syntactically correct. Example 
configuration can be found in docs folder: [ex_config](docs/ex_config/ex_config.json). Currently supported keyboard layouts:
 * de - german
 * en - english
 * fr - french
 * si - slovenian (default)

Currently the mapper supports three types of hotkeys (also described in [hotkey_types.txt](docs/hotkey_types.txt)):
 * `"typeout"` - Type out (ex. clicking on GKey types out a string)
 * `"shortcut"` - Shortcuts (ex. clicking on GKey presses shift+f4)
 * `"run"` - Starting a program (anything you can start from shell) This works only on cli programs (see why: [Why can't I run graphic programs by default](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Why-can't-I-run-graphic-programs-by-default)).
 * `"nothing"` - Do nothing (unbound key)
 * `"swap_config"` - Change macro config file inuse

To add a hotkey add to `config.json` the following code:
```
"<g|m><no_of_key|r>": {
    "hotkey_type": <type of command "nothing" or "typeout" or "shortcut" or "run">,
    "do": "<thing to do>"
  }
```

Each config json file can have a color set for it that changes the color of the logo on the keyboard depending on which profile is active by adding, this can be edited by editing 

lib/functionalities/gkey_functionality.py

changing the g910-led call to what ever color group to color, since setting colors on gkeys stops keyboard effects, I have set mine to the logo and have it breathing

```
subprocess.call(["g910-led", "-fx", "breathing", "logo", paths.color, "0a"])
```
This prevents setting the color from stopping the current running animation

see https://github.com/MatMoul/g810-led for details

setting the color in each json to be used is as follows to the top

```
"color": "HEXCOLOR",
```
#

Depending on the hotkey command, the syntax for "do" is different (supported characters for typeout and 
hotkeys are listed in [supported_keys.txt](docs/supported_keys.txt)):
 * `"typeout"` - Typeout syntax is same as you would type text out (ex. "tyPe Me Out!")
 * `"shortcut"` - Shortcuts are separated by a plus sign and a comma (ex. "ctrl+c,ctrl+v")
 * `"nothing"` - If `hotkey_type` is set to `"nothing"` then "do" key need not exist or can be anything.
 * `"run"` - Run has the same syntax as you would type a cli program in command line (ex. "systemctl daemon-reload")
 * `"swap_config"` - Name of new config file to change to when called, isnide the same config dir

An example is uploaded alongside in the docs file

The current active profile is copied to config.json from its own json file

### Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. 
IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE 
BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
