import os
import sys
from lib.misc import is_installed
from lib.misc import create_config


main_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
if is_installed.is_installed():
    config_dir = "/etc/g910-gkeys"
    config_path = config_dir + "/config.json"

    if not os.path.exists(config_dir):
        print("Creating directory: "+config_dir)
        os.makedirs(config_dir)
        create_config.create()

else:
    config_dir = os.path.join(main_dir, "config")
    config_path = config_dir + "/config.json"


pid_path = config_dir+"/g910-keys.pid"
logs_path = "/var/log/g910-gkeys.log"
