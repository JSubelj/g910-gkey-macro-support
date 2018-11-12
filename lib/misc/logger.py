import logging
from lib.misc import paths


def logger(name):
    logging.basicConfig(filename=paths.logs_path, format='%(asctime)s [%(levelname)s] {%(name)s} - %(message)s', filemode="a")
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    return log
