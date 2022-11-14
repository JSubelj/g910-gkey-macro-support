So, you want to launch graphical programs by pressing GKeys. Well you can. Just set a shortcut to run a program in your shortcut manager, assign that shortcut to a GKey and you'r good to go!

## But I don't want to invent a new shortcut, why can't the driver do that for me
Well first of all. This driver is, as it is said a driver. It is not meant to run as a normal program that can start graphical processes and what not. There are multiple restrains for that:
 - Once again it is a driver and a daemon. It is not designed to be like a Logitech "driver", that pops up, has weird configuration and if you force shut it down your computer won't boot. It is meant to sit between a keyboard and the system (even though it is run in userspace) and work regardless of the environment. It is not dependant on X server and because of that you can use it even in non graphical environment.
 - Because it is not dependant of a graphical environment it also does not have any idea what are the DISPLAY variables, which Xorg server is used etc. and so, the graphical programs that would be spawned by the driver also don't have a clue so they cannot start.
 - The daemon is also meant to start asap as the system boots, so that all the GKey support is right there even at login, so waiting for an Xorg server to start would be contradictory.
 
## But I REALLY want to start programs with it (also why I don't advise to run the driver as a program and not as a systemd service)
Ok. I give up. You actually can. But I don't recommend it. You can do that by disabling the service if you enabled it and then in your desktop environment set to autostart it when you log in. Now you can run any program as you would if you run it from command line just set the `hotkey_type` in [config](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration) to `run` and `do` to the command line argument (ex. `firefox`). Hurrah you win! But now listen to my concerns with this kind of abusing the driver:
 - Using the driver like that, you can never know if its running or not (you can look for the pid with `pidof python`), the output of the driver is not saved, so you don't know if anything went wrong. 
 - Because of that you have to always check if the driver is already running, and if you by mistake spawn multiple instances of the driver, the actions can be duplicated, logs can be filled by warnings that the driver can't bind to the device and some more possible headaching behaviour.
 - The system sometimes shuts this kind of programs correctly (by sending SIGTERM to them and waiting to shut down) or they can not wait for it sending it SIGKILL signal before it can properly shutdown. Because of that you can have problems like computer not even booting to bios, because uinput handler didn't close correctly. (If you do then I found out that unplugging the keyboard and hard resetting the computer does the trick)
 - The driver now doesn't work in non graphical environments.
 - All programs spawned have Superuser privileges (because the driver also has them) and that can also bring some unwanted problems, to not even touch the security concern.

## Why I recommend to run the driver with a service manager
This are some of the plus sides to running the driver with a service manager and I believe there are many more:
- You don't have to worry about the number of instances spawned. There is only one and you can't by mistake spawn more of them
- Service manager takes care of correctly shutting down the program
- The driver launches as soon as possible (if enabled with `systemctl enable g910-gkeys`), giving you functionality before even the graphical environment starts
- You can diagnose the driver by running `systemctl status g910-gkeys` and looking at systemd logs with `journalctl -u g910-gkeys`

So I hope I changed your mind and you will use the driver as intended. (But if you don't and stumble on a problem that you can't fix yourself feel free to open an [issue](https://github.com/JSubelj/g910-gkey-macro-support/issues) and I'll try to help as much as I can).