import logging
import os


class Logger:

    file_handler = None
    stream_handler = None

    log_level: int

    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    def __init__(self):
        from g910_gkeys.misc.config import Config
        config = Config()
        config_dict = config.load()
        log_level = config_dict.get('log_level', 'INFO')
        self.log_level = self.log_level_map[log_level]

        if self.stream_handler is None:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setLevel(self.log_level)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] {%(name)s} - %(message)s')
            self.stream_handler.setFormatter(formatter)

        if config_dict.get('logging', "False") != "False" and self.file_handler is None:
            self.rotate_log_file(config_dict.get('log_path', config.logs_path))
            self.file_handler = logging.FileHandler(config_dict.get('log_path', config.logs_path), "a")
            self.file_handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] {%(name)s} - %(message)s')
            self.file_handler.setFormatter(formatter)

    def logger(self, name=None):
        log = logging.getLogger(name)
        log.setLevel(self.log_level)
        log.propagate = False

        if self.stream_handler is not None and self.stream_handler not in log.handlers:
            log.addHandler(self.stream_handler)

        if self.file_handler is not None and self.file_handler not in log.handlers:
            log.addHandler(self.file_handler)

        return log

    @staticmethod
    def rotate_log_file(filename):
        try:
            # simple log rotation to avoid growing infinite
            size = os.path.getsize(filename)
            if size > 5000000:  # More than 5MB
                print(f"Moving {filename} (size {str(size / 1000000)} MB) to {filename}.old")
                os.rename(filename, filename + ".old")
        except:
            pass
