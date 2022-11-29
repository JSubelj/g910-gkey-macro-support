import logging
import os


class Logger:

    file_handler = None

    log_level: int

    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    def __init__(self, log_level: int = logging.DEBUG):
        from lib.data_mappers.config import Config
        config = Config()
        log_level = config.load().get('log_level', 'INFO')
        self.log_level = self.log_level_map[log_level]
        self.log_to_file(config.logs_path, self.log_level)

    def logger(self, name=None):
        log = logging.getLogger(name)
        log.setLevel(self.log_level)
        log.propagate = False
        if self.file_handler is not None:
            log.addHandler(self.file_handler)
        return log

    def log_to_file(self, filename, log_level):
        self.log_level = log_level
        self.file_handler = logging.FileHandler(filename, "a")
        self.file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] {%(name)s} - %(message)s')
        self.file_handler.setFormatter(formatter)

        try:
            # simple log rotation to avoid growing infinite
            size = os.path.getsize(filename)
            if size > 5000000:  # More than 5MB
                print(f"Moving {filename} (size {str(size / 1000000)} MB) to {filename}.old")
                os.rename(filename, filename + ".old")
        except:
            pass
