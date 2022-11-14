So you stumbled on an issue and you don't know where to look at what went wrong. No problem, I'm here to help.

## Installation Troubleshooting

First you need to make sure that the version of Python is >=3.7 (3.6 should also work) with `python3 --version`.
If you have the 3.7 installed but the above command returns some other version, try command `python3.7 --version`. Then run `sudo python3.7 setup.py install`.

On some distros there was also problems with not having python devel, pip and gcc installed so try check that you have those packages installed.

There has also been a few reported issues with installing the software on various platforms. Check out the [Issues](https://github.com/JSubelj/g910-gkey-macro-support/issues?q=is%3Aissue+is%3Aclosed+label%3A%22good+first+issue%22) with tag `good first issue`.


## Execution Troubleshooting

The main information you can get is systemd logs and driver's log. Systemd status and logs can be found by running:

- status: `systemctl status g910-gkeys`
- logs: `journalctl -u g910-gkeys`

Those two should give you enough information to figure out why the driver didn't start or why it shut down unexpectedly.

If the driver runs but does not work as you expect it to, then your best place to look is in: `/var/log/g910-gkeys.log`, where the behaviour of the driver is logged. There you can see if there is a problem with your [configuration](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Configuration) or if there are errors (like not finding the device). 

If you want to see exactly if driver catches the GKey or media button event and what the HEX-code is, change logger level to `DEBUG` in [logger.py](https://github.com/JSubelj/g910-gkey-macro-support/blob/5caa954019a835906f80950d1f21877e9b1b7405/lib/misc/logger.py#L13) and rebuild the driver (will probably make it dynamically changeable in the future).

If you still can't figure out why it doesn't work, check that GKey to FKey mapping is disabled (you can do this by pressing G5 in a browser. If the page reloads the mapping is not disabled). If the mapping is not disabled try restarting the driver but if that still doesn't work install [g810-led controller](https://github.com/MatMoul/g810-led) and disable the mapping with `g910-led -gkm 1` then restart the driver. 
 
If still nothing then try restarting your computer or plugging the keyboard in and out. 

If still no luck, try reinstalling the software and then if still nothing please post an [issue](https://github.com/JSubelj/g910-gkey-macro-support/issues), describe the problem in detail add the configuration, logs and systemctl log via pastebin (or whatever you prefer) and I will try to help.
 

