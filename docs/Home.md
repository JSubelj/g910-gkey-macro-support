# Logitech G910 keyboard Gkey support for GNU/Linux

Because I didn't find any Gkey support for Logitech G910 keyboard I decided to create this Gkey mapper. Code is based on an [issue](https://github.com/CReimer/g910-gkey-uinput/issues/3) in [g910-gkey-uinput](https://github.com/CReimer/g910-gkey-uinput) project. I expanded the code, so that it is more user-friendly to add functionality to Gkeys.

## Features
With this driver run as a service you can bind every Gkeys with four different commands. You can bind shortcuts to it (ex. ctrl+c), type out stuff, run a bash command and execute short python snippets and type out the result.

To see what is coming next look at the [roadmap](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Roadmap).

## Installation
You can find a detailed installation guide [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Detailed-installation).

### Update
If you have already installed a previous version of the driver and want to upgrade take a look [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Upgrading).

### Configuration
Everything about the configuration you will find [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration).  
For a more advanced configuration limiting the usage of global gkey config, where user set the actions in his/her own environment. See [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration-strict-user-environment.md)

### Troubleshooting
If you have problems installing or running the driver you can have a look [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Troubleshooting).

### Uninstall
Information about how to remove driver from you system are [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Uninstalling)

## Contributing
If you like to contribute to this project please start [here](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Contributing)

The code is tested on Logitech G910 keyboard with
- OS: Ubuntu 20.04.6 LTS, Linux 5.4.0-159-generic, GNOME: 3.36.9