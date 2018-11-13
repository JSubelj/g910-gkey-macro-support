import logging
from lib.misc import paths


fh = logging.FileHandler(paths.logs_path, "a")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] {%(name)s} - %(message)s')
fh.setFormatter(formatter)


def logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.propagate = False
    log.addHandler(fh)
    return log
