## Shortcut (recommended)
If you want to launch graphical programs by pressing g-keys just set a shortcut to run a program in your shortcut manager, assign that shortcut to a GKey and you're good to go! If your not sure how to do it you can take a look at the [advanced How-To](Configuration-strict-user-environment.org).

## Run command (not recommended)
If you are in a single user environment you can config a run command to start a graphical program with `su <username> -c 'nohub <programm>'`. The use of `nohub` will keep the program open. If the program writes to stdout you need to redirect it to /dev/null. Here is an example how to open the gnome-terminal:
```
su <username> -c 'DISPLAY=:0 nohup gnome-terminal' & 2>&1 > /dev/null
```
Replace <username> with your username. If the program supports it you can define the DISPLAY variable with the screen you want the program to start up.

>**Important:**  
The keys are always active with the "run" type, even if nobody is logged in, logged in as another user, if the screen is locked, or even when the user is switched to another one (the first session still being active): In the first 2 cases the program will be launched but will fail (the DISPLAY does not exist), but will be successful in the 2 other cases (screen locked or user switched).
>
>If you are in a multi-user-environment you can't use the method explained above since there is only one global config for g-keys. The driver will be available soon after boot and even in none graphical environments you need to keep in mind that the run commands you put in your config will be executed with no limitations. The driver is handled as service by systemd and executed by root. There is a huge difference between a "run" command, with or without su and the simple mapping to another key by shortcut.

~~Well first of all. This driver is, as it is said a driver. It is not meant to run as a normal program that can start graphical processes and what not. There are multiple restrains for that:~~
 - ~~Once again it is a driver and a daemon. It is not designed to be like a Logitech "driver", that pops up, has weird configuration and if you force shut it down your computer won't boot. It is meant to sit between a keyboard and the system (even though it is run in userspace) and work regardless of the environment. It is not dependant on X server and because of that you can use it even in non graphical environment.~~
 - ~~Because it is not dependant of a graphical environment it also does not have any idea what are the DISPLAY variables, which Xorg server is used etc. and so, the graphical programs that would be spawned by the driver also don't have a clue so they cannot start.~~
 - ~~The daemon is also meant to start asap as the system boots, so that all the GKey support is right there even at login, so waiting for an Xorg server to start would be contradictory.~~

~~## But I REALLY want to start programs with it (also why I don't advise to run the driver as a program and not as a systemd service)~~
~~Ok. I give up. You actually can. But I don't recommend it. You can do that by disabling the service if you enabled it and then in your desktop environment set to autostart it when you log in. Now you can run any program as you would if you run it from command line just set the `hotkey_type` in [config](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration) to `run` and `do` to the command line argument (ex. `firefox`). Hurrah you win! But now listen to my concerns with this kind of abusing the driver:~~
 - ~~Using the driver like that, you can never know if its running or not (you can look for the pid with `pidof python`), the output of the driver is not saved, so you don't know if anything went wrong.~~ 
 - ~~Because of that you have to always check if the driver is already running, and if you by mistake spawn multiple instances of the driver, the actions can be duplicated, logs can be filled by warnings that the driver can't bind to the device and some more possible headaching behaviour.~~
 - ~~The system sometimes shuts this kind of programs correctly (by sending SIGTERM to them and waiting to shut down) or they can not wait for it sending it SIGKILL signal before it can properly shutdown. Because of that you can have problems like computer not even booting to bios, because uinput handler didn't close correctly. (If you do then I found out that unplugging the keyboard and hard resetting the computer does the trick)~~
 - ~~The driver now doesn't work in non graphical environments.~~
 - ~~All programs spawned have Superuser privileges (because the driver also has them) and that can also bring some unwanted problems, to not even touch the security concern.~~

~~So I hope I changed your mind, and you will use the driver as intended. (But if you don't and stumble on a problem that you can't fix yourself feel free to open an [issue](https://github.com/JSubelj/g910-gkey-macro-support/issues), and I'll try to help as much as I can).~~