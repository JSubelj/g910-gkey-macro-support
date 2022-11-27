import sys


class Helper:

    @staticmethod
    def is_installed():
        command = sys.argv[0].split("/")[-1]
        return command != "cli_entry_point.py"
