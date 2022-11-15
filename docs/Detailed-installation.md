## Requirements
First check that you have the needed requirements:
 - Python 3.7 (3.6 should work)
 - uinput kernel module (more on this [here](http://tjjr.fi/sw/python-uinput/#Usage))
 - [g810-led controller](https://github.com/MatMoul/g810-led) (optional) switch the lights on m keys to indicate active profile

For Arch based distros: It's live on [AUR](https://aur.archlinux.org/packages/g910-gkeys-git/)

### Preperation
If that's checked you can prepare for the setup:
 1. Load uinput kernel module: `modprobe uinput` (on Manjaro should be loaded by default afaik)
 
## Installation  
Download the driver  
- with git use `git clone https://github.com/JSubelj/g910-gkey-macro-support.git`  
or
- download & unzip `wget https://github.com/JSubelj/g910-gkey-macro-support/archive/refs/heads/master.zip; unzip master.zip`  

Open the directory: `cd g910-gkey-macro-support` or `cd g910-gkey-macro-support-master` if you have downloaded the zip.

### Installer (recommended)
To run the installer you need to make it executable `chmod +x installer.sh` and then execute it with admin privileges `sudo ./installer.sh`. You can do this with in one line `chmod +x installer.sh; sudo ./installer.sh`

### Build package from source
1. Build and install the package with setuptools: `sudo python3 setup.py install --record files.txt`
2. Verify a successful build and install by running `sudo g910-gkeys -v`  
    You should see something like this:
      ```
      g910-gkeys
      
      Support for Logitech G910 GKeys on GNU/Linux
      
      Created by Jan Šubelj
      Version 0.2.5
      ```
3. Install the driver as a system service: `cp g910-gkeys.service /usr/lib/systemd/system; systemctl daemon-reload`
4. To start the driver now and automatically on every boot run `systemctl enable --now g910-gkeys`
 
If you just want to start the driver for this session skip the last step and use: `systemctl start g910-gkeys`. You can also stop the service with `systemctl stop g910-gkeys`.

#### Why running the driver with a service manager is recommended
These are the plus sides to running the driver with a service manager and I believe there are many more:
- You don't have to worry about the number of instances spawned. There is only one, and you can't by mistake spawn more of them
- Service manager takes care of correctly shutting down the program
- The driver launches as soon as possible (if enabled with `systemctl enable g910-gkeys`), giving you functionality before even the graphical environment starts
- You can diagnose the driver by running `systemctl status g910-gkeys` and looking at systemd logs with `journalctl -u g910-gkeys`

## First Steps
The driver should work now and pressing the G1 key should typeout: *This is profile m1*  
Be sure to enter a text window/field before hitting G1, since the type out use the focus of the cursor.

### Configuring G910 macro keys
Now that you installed the driver successfully you can configure your Gkeys mapping as described here: [Configuration](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration)

If the driver still doesn't work correctly troubleshoot it as described here: [Troubleshooting](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Troubleshooting)


