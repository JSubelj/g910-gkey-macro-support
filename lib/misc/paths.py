import os
import sys
from lib.misc.helper import Helper


def check_paths(config, device):
    if not os.path.exists(config_dir):
        print("Creating directory: "+config_dir)
        os.makedirs(config_dir)
    if not os.path.exists(config_path):
        config.create(device.keyboard)  # create config with keyboard interface


# set config path
if Helper.is_installed():
    config_dir = "/etc/g910-gkeys"
    config_path = config_dir + "/config.json"
else:
    main_dir = Helper.get_base_path()
    config_dir = os.path.join(main_dir, "config")
    config_path = config_dir + "/config.json"

# set log path
if os.geteuid() != 0:
    logs_path = "g910-gkeys.log"
else:
    logs_path = "/var/log/g910-gkeys.log"
# rename log to keep log storage low
try:
    size = os.path.getsize(logs_path)
    if size > 5000000:  # More then 5MB
        print("Moving "+logs_path+" (size "+str(size/1000000)+"MB) to "+logs_path+".old")
        os.rename(logs_path, logs_path+".old")
except:
    pass
