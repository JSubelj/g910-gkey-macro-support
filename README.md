# Logitech G910 keyboard gkey support for Linux

Because I didn't find any GKey support for Logitech G910 keyboard I decided to create this GKey mapper.
Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3)
in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more 
user friendly to add functionality to GKeys.

The code is tested on Logitech G910 keyboard, OS: Manjaro, 4.19.1 Linux kernel.

## Requirements

To use this project you need:
 - Python 3.7
 - git
 - [g810-led controller](https://github.com/MatMoul/g810-led)
 - uinput kernel module (more on this [here](tjjr.fi/sw/python-uinput/#Usage))
 - pip requirements are stored in requirements.txt
 
## Installation
 - install [g810-led-git](https://github.com/MatMoul/g810-led) for your distro (for Arch based distros: [aur](https://aur.archlinux.org/packages/g810-led-git/))
 - load uinput kernel module: `modprobe uinput` (on Manjaro is loaded by default afaik) 
 - clone repo: `git clone https://github.com/JSubelj/g910-gkey-macro-support.git`
 - move to cloned repo: `cd g910-gkey-macro-support`
 - (optionally create virtual environment: `pip install virtualenv && virtualenv venv && source venv/bin/activate`)
 - install pip requirements: `pip install -r requirements.txt` 
 - disable Gkeys to Fkeys mapping: `g910-led -gkm 1` (probably will include that on program start)
 - edit configuration: `vim config/config.json`
 - start the program and you are ready to go: `python launcher.py`
 
## Configuration
Configuration should be located in `/config/config.json` and should be syntactically correct. Example 
configuration can be found in docs folder: [ex_config](docs/ex_config/ex_config.json).
Currently the mapper supports three types of hotkeys (also described in [hotkey_types.txt](docs/hotkey_types.txt)):
 * `"typeout"` - Type out (ex. clicking on GKey types out a string)
 * `"shortcut"` - Shortcuts (ex. clicking on GKey presses shift+f4)
 * `"run"` - Starting a program (anything you can start from shell) (will terminate when mapper is terminated)
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
 * `"shortcut"` - Shortcuts are separated by a plus sign (ex. "ctrl+alt+f4")
 * `"run"` - Run has the same syntax as you would type a program in command line (ex. "firefox")
 * `"nothing"` - If `hotkey_type` is set to `"nothing"` then "do" key need not exist or can be anything.
 
## Contribution and requests
I am developing this software for personal use (for now). If you have any recommendations, complaints, anything you want to see included,
open an issue and I will gladly try to add it. To view the state of current features you can checkout the [TODO](TODO.md) file.

### Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. 
IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE 
BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.