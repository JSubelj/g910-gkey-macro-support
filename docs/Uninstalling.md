# Uninstall the package
To remove the package fully you need to navigate to the directory you installed the driver from.

>If you deleted the directory you can [install](https://github.com/JSubelj/g910-gkey-macro-support/wiki/Detailed-installation) the driver once again to run the uninstall script after. It is important to run the installer in the first place, because it will create the files.txt which is needed.

## Uninstaller (recommended)
Run the uninstalling script from the directory you installed the driver:  
`chmod +x uninstall.sh; sudo ./uninstall.sh`.

If you won't be reinstalling the program (sad to see you go), you should also remove the configuration, so it doesn't bloat your `/etc/` folder:  
`sudo ./uninstall.sh -a`

## Remove the package manually (versions below v0.2.5)
 1. Delete package files from installed system folder: `cat files.txt | sudo xargs rm -rf`
 2. Remove package from pip: `sudo pip uninstall g910-gkeys`
 3. Disable service: `systemctl disable g910-gkeys`

If you won't be reinstalling the program (sad to see you go), you should also remove the configuration, so it doesn't bloat your `/etc/` folder: `rm /etc/g910-gkeys -rf`

> For older Versions:  
> To remove the module from pip you should run `pip list | grep g910` and then `sudo pip uninstall ${names that were returned by the previous command}`. This is because I renamed the driver from "g910-gkey-macro-support" to "g910-gkeys" for shorter and easier understanding.  
> 
> Remove the service file with: `rm /usr/lib/systemd/system/g910-gkeys.service`