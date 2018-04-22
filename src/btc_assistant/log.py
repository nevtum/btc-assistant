import logging
from os import environ

LOGLEVEL = environ.get("LOGLEVEL", "INFO")
level_nr = logging.getLevelName(LOGLEVEL)

def _set_root_logger_level():
    logging.basicConfig(level=level_nr)
    logging.getLogger('botocore.vendored').setLevel(logging.WARNING)
    # add any extra namespaces to override the default configuration

def get_logger(namespace):
    logger = logging.getLogger(namespace)
    logger.setLevel(level_nr)
    return logger

_set_root_logger_level()