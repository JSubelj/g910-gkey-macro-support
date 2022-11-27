import os
import sys
from lib.misc.helper import Helper
from lib.data_mappers.config_reader import Config


main_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
if Helper.is_installed():
    config_dir = "/etc/g910-gkeys"
    config_path = config_dir + "/config.json"

    if not os.path.exists(config_dir):
        print("Creating directory: "+config_dir)
        os.makedirs(config_dir)
        Config.create()

else:
    config_dir = os.path.join(main_dir, "config")
    config_path = config_dir + "/config.json"

if os.geteuid() != 0:
    logs_path = "g910-gkeys.log"
else:
    logs_path = "/var/log/g910-gkeys.log"

try:
    size = os.path.getsize(logs_path)
    if size > 5000000:  # More then 5MB
        print("Moving "+logs_path+" (size "+str(size/1000000)+"MB) to "+logs_path+".old")
        os.rename(logs_path, logs_path+".old")
except:
    pass
