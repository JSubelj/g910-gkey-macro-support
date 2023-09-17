import email.policy
import importlib.metadata
import locale
import os
import sys


class Helper:

    @staticmethod
    def is_installed():
        command = sys.argv[0].split("/")[-1]
        return command == "g910-gkeys"

    @staticmethod
    def get_locale():
        # detect current locale and set as keyboard mapping
        user_lang, encoding = locale.getdefaultlocale()
        return user_lang.split("_")[0]

    @staticmethod
    def get_base_path():
        main_dir = os.path.abspath(os.getcwd())
        return main_dir

    @staticmethod
    def get_version():
        return importlib.metadata.version('g910-gkeys')

    @staticmethod
    def get_author():
        em = email.message_from_string(
            f"To: {importlib.metadata.metadata('g910-gkeys')['author-email']}",
            policy=email.policy.default
        )

        for address in em['to'].addresses:
            return address.display_name
