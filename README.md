# Logitech G910 keyboard gkey support for Linux

Because I didn't find any GKey support for Logitech G910 keyboard I decided to create this GKey mapper.
Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3)
in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more 
user friendly to add functionality to GKeys.

The code is tested on Logitech g910 keyboard, OS: Manjaro, 4.19.1 Linux kernel.

## Requirements

To use this project you need:
 - Python 3.7
 - git
 - [g810-led controller](https://github.com/MatMoul/g810-led)
 - uinput kernel module (more on this [here](tjjr.fi/sw/python-uinput/#Usage))
 - pip requirements are stored in requirements.txt
 
## Installation
 - install [g810-led-git](https://aur.archlinux.org/packages/g810-led-git/)
 - load uinput kernel module: `modprobe uinput` (on Manjaro is loaded by default afaik) 
 - clone repo: `git clone https://github.com/JSubelj/g910-gkey-macro-support.git`
 - disable Gkeys to Fkeys mapping: `g910-led -gkm 1` (probably will include that on program start)
 - edit configuration in `g910-gkey-macro-support/config/config.json`
 - start the program and you are ready to go: `python g910-gkey-macro-support/launcher.py`
 
## Configuration
Currently the mapper support three types of hotkeys:
 * [0] Type out (ex. clicking on GKey types out a string)
 * [1] Shortcuts (ex. clicking on GKey presses shift+f4)
 * [2] Starting a program (anything you can start from shell) (will terminate when mapper is terminated)
 * [-1] do nothing

To add a hotkey add to `config.json` the following code:
```
"g<no_of_gkey>": {
    "command": <type of command -1 or 0 or 1 or 2]>,
    "make": "<thing to do>"
  }
```

Depending on the hotkey command, the syntax for make is different:
... To be continued


 

