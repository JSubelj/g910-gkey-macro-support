## Uninstall the old version
It is recommended to first uninstall the driver (as seen in [Uninstalling](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Uninstalling) section), of course not removing the `/etc/g910-gkeys/config.json`.

## For not an ArchLinux based distro
After the uninstall run `sudo python setup.py install` and the program should install itself.
 

## For ArchLinux based distro
Even though the upper command will work on Arch based distros it is better to install the program by pulling the pkgbuild folder, building the .tar.gz with `makepkg` and installing with pacman: `pacman -U g910-gkeys-git-*.*.*-1-any.pkg.tar.xz` where you fill in the correct version number.

Even better, use the [AUR](https://aur.archlinux.org/packages/g910-gkeys-git/)

### Use profile feature after upgrade to 0.2.4
 If you update from version <= v0.2.4 you will need to make some manual changes to your `/etc/g910-gkeys/config.json` to make use of the new gkey profile feature.
 You don't need to do anything if you don't want to use the profile feature your old config will be loaded as default profile m1.