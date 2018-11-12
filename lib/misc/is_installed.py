import sys

def is_installed():
    command = sys.argv[0].split("/")[-1]
    return command!="launcher.py"
